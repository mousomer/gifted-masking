import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from gifted_masking.experiments.e04 import (
    E04_RAW_FIELDNAMES,
    STANDARD_SEEDS,
    canonical_e04_cells,
    derive_e04_identity_seed,
    derive_e04_policy_environment_seed,
    e04_matched_family_id,
    e04_effects,
    load_e04_config,
    recompute_e04_summaries,
    run_e04_experiment,
    simulate_e04_cell,
    normalize_e04_machine_artifacts,
    standard_cost_projection,
    stream_e04_raw_rows,
    _expected_rewards,
    _good_sets,
    objective_best_actions,
    validate_e04_raw_rows,
    validate_e04_curves,
    validate_e04_effects,
)
from gifted_masking.models import m3


ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "configs/frontiers_article/e04_m3_search_architectures_smoke.json"
STANDARD = ROOT / "configs/frontiers_article/e04_m3_search_architectures_standard.json"


class ArticleE04Tests(unittest.TestCase):
    def setUp(self):
        self.config = load_e04_config(SMOKE)

    def _small(self):
        config = copy.deepcopy(self.config)
        config["n"], config["T"] = 8, 30
        return config

    def test_frozen_config_and_e04_standard_refusal(self):
        self.assertEqual(self.config["run_id"], "frontiers_m3_search_architectures_v1_smoke")
        self.assertFalse(load_e04_config(STANDARD)["approved_standard"])
        for key, value in (("n", 95), ("T", 301), ("workers", 2), ("master_seed", 3)):
            with self.assertRaises(ValueError):
                load_e04_config(SMOKE, {key: value})
        with self.assertRaises(PermissionError):
            run_e04_experiment(STANDARD, Path(tempfile.gettempdir()) / "e04-forbidden")

    def test_canonicalization_has_exact_55_and_120_rows(self):
        cells, equivalences = canonical_e04_cells()
        self.assertEqual(len(cells), 55); self.assertEqual(len(equivalences), 120)
        self.assertEqual(sum(row["architecture"] == "flat_2k" for row in cells), 18)
        self.assertEqual(sum(row["architecture"] == "hierarchical" for row in cells), 18)
        self.assertEqual(sum(row["architecture"] == "global_mask" for row in cells), 18)
        fixed = [row for row in cells if row["architecture"] == "fixed_known_good"]
        self.assertEqual(len(fixed), 1)
        self.assertEqual(sum(row["is_canonical"] == "True" for row in equivalences), 55)
        self.assertTrue(all(row["canonical_request_id"] == row["canonical_source_request_id"] for row in equivalences))
        k2_two = [row for row in equivalences if row["requested_K"] == 2 and row["requested_good_context_regime"] == "two"]
        self.assertTrue(all(row["parameter_cell_id"].endswith("|identity=fixed|m=2") or "fixed_known_good" in row["parameter_cell_id"] for row in k2_two))

    def test_fixed_identity_replays_all_maintained_architecture_kernels(self):
        config = self._small()
        cells, _ = canonical_e04_cells()
        for k in (1, 2, 4, 8, 16):
            cell = next(row for row in cells if row["architecture"] == "flat_2k" and row["K"] == k and row["canonical_identity_mode"] == "fixed" and row["effective_good_count"] == 1)
            rows = simulate_e04_cell(config, cell, 123, 999)
            settled, mask, modal = m3.simulate(k, n=8, horizon=30, seed=123, final_window_fraction=.2)
            self.assertEqual([row["settled_any_good_auth_argmax"] for row in rows], [str(bool(x)) for x in settled])
            np.testing.assert_allclose([float(row["final_window_mask_rate"]) for row in rows], mask)
            self.assertEqual([int(row["final_window_modal_action_index"]) for row in rows], modal.tolist())
        replay_cases = (
            ("hierarchical", 4, lambda: m3.simulate_hierarchical(4, n=8, horizon=30, seed=321, final_window_fraction=.2)),
            ("global_mask", 4, lambda: m3.simulate_global_mask(4, n=8, horizon=30, seed=321, final_window_fraction=.2)),
            ("fixed_known_good", 1, lambda: m3.simulate_fixed_good_pond(n=8, horizon=30, seed=321, final_window_fraction=.2)),
        )
        for architecture, k, maintained in replay_cases:
            cell = next(row for row in cells if row["architecture"] == architecture and row["K"] == k)
            rows = simulate_e04_cell(config, cell, 321, 999)
            settled, mask, modal = maintained()
            self.assertEqual([row["settled_any_good_auth_argmax"] for row in rows], [str(bool(x)) for x in settled])
            np.testing.assert_allclose([float(row["final_window_mask_rate"]) for row in rows], mask)
            self.assertEqual([int(row["final_window_modal_action_index"]) for row in rows], modal.tolist())

    def test_action_shapes_identity_and_regret_sentinels(self):
        config = self._small(); cells, _ = canonical_e04_cells()
        flat = next(row for row in cells if row["architecture"] == "flat_2k" and row["K"] == 16 and row["canonical_identity_mode"] == "fixed" and row["effective_good_count"] == 1)
        random = next(row for row in cells if row["architecture"] == "flat_2k" and row["K"] == 16 and row["canonical_identity_mode"] == "random_per_child" and row["effective_good_count"] == 1)
        fixed_rows = simulate_e04_cell(config, flat, 2, 3); random_rows = simulate_e04_cell(config, random, 2, 4)
        self.assertEqual(int(fixed_rows[0]["joint_action_count"]), 32)
        self.assertTrue(all(json.loads(row["good_context_ids_json"]) == [0] for row in fixed_rows))
        self.assertTrue(any(0 not in json.loads(row["good_context_ids_json"]) for row in random_rows))
        self.assertAlmostEqual(float(fixed_rows[0]["expected_good_auth_reward"]), 1.15)
        self.assertAlmostEqual(float(fixed_rows[0]["expected_mask_reward"]), .75)
        self.assertAlmostEqual(float(fixed_rows[0]["expected_bad_auth_reward"]), -.8)
        self.assertAlmostEqual(float(fixed_rows[0]["objective_best_expected_reward"]) - float(fixed_rows[0]["expected_mask_reward"]), .4)
        self.assertAlmostEqual(float(fixed_rows[0]["objective_best_expected_reward"]) - float(fixed_rows[0]["expected_bad_auth_reward"]), 1.95)
        global_cell = next(row for row in cells if row["architecture"] == "global_mask" and row["K"] == 2 and row["canonical_identity_mode"] == "fixed" and row["effective_good_count"] == 1)
        global_rows = simulate_e04_cell(config, global_cell, 5, 6)
        self.assertEqual(int(global_rows[0]["joint_action_count"]), 3)
        self.assertIn(0, range(int(global_rows[0]["joint_action_count"])))
        self.assertEqual((30 // 2, 30 % 2), (15, 0)); self.assertEqual((31 // 2, 31 % 2), (15, 1))
        np.testing.assert_array_equal(_good_sets(3, 2, 2, "fixed", 1), np.array([[0, 1], [0, 1], [0, 1]]))
        self.assertEqual(_good_sets(1, 16, 1, "fixed", 1)[0].tolist(), [0])
        self.assertEqual(_good_sets(1, 16, 2, "fixed", 1)[0].tolist(), [0, 1])
        self.assertEqual(_good_sets(1, 16, 4, "fixed", 1)[0].tolist(), [0, 1, 2, 3])
        mask, good, bad = _expected_rewards(.7, .2, self.config["payoffs"])
        self.assertGreater(mask, good); self.assertAlmostEqual(mask - good, .05); self.assertAlmostEqual(mask - bad, 1.55)
        self.assertEqual(objective_best_actions("flat_2k", 16, np.array([0, 3]), False), list(range(0, 32, 2)))
        self.assertEqual(objective_best_actions("hierarchical", 16, np.array([0, 3]), False), list(range(0, 32, 2)))
        self.assertEqual(objective_best_actions("global_mask", 16, np.array([0, 3]), False), [0])
        self.assertEqual(objective_best_actions("fixed_known_good", 1, np.array([0]), False), [0])

    def test_rng_separation_schema_entropy_and_raw_reconciliation(self):
        config = self._small(); cells, _ = canonical_e04_cells()
        cell = next(row for row in cells if row["architecture"] == "hierarchical" and row["K"] == 4 and row["canonical_identity_mode"] == "fixed" and row["effective_good_count"] == 1)
        policy = derive_e04_policy_environment_seed(9, "hierarchical", 4)
        identity = derive_e04_identity_seed(9, str(cell["parameter_cell_id"]))
        before = np.random.get_state(); rows = simulate_e04_cell(config, cell, policy, identity); after = np.random.get_state()
        self.assertEqual(list(rows[0]), E04_RAW_FIELDNAMES); self.assertEqual(before[0], after[0]); np.testing.assert_array_equal(before[1], after[1])
        summary = recompute_e04_summaries(rows); self.assertEqual(len(summary), 1)
        self.assertAlmostEqual(float(summary[0]["mean_final_window_mask_rate"]), np.mean([float(row["final_window_mask_rate"]) for row in rows]))
        corrupted = [dict(row) for row in rows]; corrupted.pop()
        with self.assertRaises(ValueError): recompute_e04_summaries(corrupted)
        self.assertEqual(derive_e04_policy_environment_seed(9, "hierarchical", 4), derive_e04_policy_environment_seed(9, "hierarchical", 4))
        self.assertNotEqual(policy, identity)

    def test_smoke_effects_are_noninferential(self):
        config = self._small(); cells, _ = canonical_e04_cells(); summaries = []; raw = []
        for cell in cells:
            policy = derive_e04_policy_environment_seed(config["master_seed"], str(cell["architecture"]), int(cell["K"]))
            identity = derive_e04_identity_seed(config["master_seed"], str(cell["parameter_cell_id"]))
            cell_rows = simulate_e04_cell(config, cell, policy, identity); raw.extend(cell_rows); summaries.extend(recompute_e04_summaries(cell_rows))
        raw.sort(key=lambda row: (str(row["parameter_cell_id"]), int(row["master_seed"]), int(row["child_id"])))
        validate_e04_raw_rows(raw, config); validate_e04_curves(summaries, config, raw)
        self.assertIn("mean_distinct_contexts_sampled_authentically", summaries[0]); self.assertIn("normalized_entropy_status", summaries[0])
        bad_rows = [dict(row) for row in raw]; bad_rows[0]["parameter_cell_id"] = "arbitrary"
        with self.assertRaises(ValueError): validate_e04_raw_rows(bad_rows, config)
        effects = e04_effects(summaries, "smoke")
        self.assertTrue(effects); self.assertTrue(all(row["ci_status"] == "not_estimable_smoke" and row["ci_low"] == "" for row in effects))
        validate_e04_effects(effects, self.config, summaries)
        with self.assertRaises(ValueError): e04_effects(summaries, "standard")
        standard_curves = []
        for seed in STANDARD_SEEDS:
            for row in summaries:
                copied = dict(row); copied.update({"run_id": "frontiers_m3_search_architectures_v1", "tier": "standard", "master_seed": seed})
                standard_curves.append(copied)
        self.assertEqual(e04_effects(standard_curves, "standard"), e04_effects(list(reversed(standard_curves)), "standard"))

    def test_standard_cost_projection_stays_inside_review_targets(self):
        plan = standard_cost_projection(6_400_000, 2.0)
        self.assertEqual(plan["standard_rows"], 137_500)
        self.assertEqual(plan["standard_learner_steps"], 275_000_000)
        self.assertLess(float(plan["projected_runtime_minutes"]), 10.0)
        self.assertLess(float(plan["projected_raw_mib"]), 400.0)
        self.assertLess(float(plan["projected_peak_mib"]), 2 * 1024)
        config = self._small(); cells, _ = canonical_e04_cells(); rows = simulate_e04_cell(config, cells[0], 2, 3)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "stream.csv"
            self.assertEqual(stream_e04_raw_rows(path, (rows[:3], rows[3:])), 8)
            with path.open() as handle: self.assertEqual(len(list(csv.DictReader(handle))), 8)
        all_rows = []
        for cell in cells:
            policy = derive_e04_policy_environment_seed(config["master_seed"], str(cell["architecture"]), int(cell["K"]))
            identity = derive_e04_identity_seed(config["master_seed"], str(cell["parameter_cell_id"]))
            all_rows.extend(simulate_e04_cell(config, cell, policy, identity))
        all_rows.sort(key=lambda row: (str(row["parameter_cell_id"]), int(row["master_seed"]), int(row["child_id"])))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "strict_stream.csv"
            self.assertEqual(stream_e04_raw_rows(path, (all_rows[:17], all_rows[17:]), config), 440)
            wrong_order = all_rows[:]; wrong_order[0], wrong_order[1] = wrong_order[1], wrong_order[0]
            with self.assertRaises(ValueError): stream_e04_raw_rows(Path(directory) / "wrong.csv", (wrong_order,), config)

    def test_duplicate_json_types_and_matched_family_are_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            duplicate = Path(directory) / "duplicate.json"; duplicate.write_text('{"experiment_id":"E04","experiment_id":"E04"}')
            with self.assertRaises(ValueError): load_e04_config(duplicate)
            bad = json.loads(SMOKE.read_text()); bad["design"]["K"][0] = True
            typed = Path(directory) / "typed.json"; typed.write_text(json.dumps(bad))
            with self.assertRaises(ValueError): load_e04_config(typed)
        self.assertNotEqual(e04_matched_family_id(1, "flat_2k", 4), e04_matched_family_id(2, "flat_2k", 4))
        self.assertIn("sensitivity=baseline", e04_matched_family_id(1, "flat_2k", 4))

    def test_adversarial_raw_curve_effect_and_normalized_manifest_rejection(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_outputs = run_e04_experiment(SMOKE, Path(first))
            second_outputs = run_e04_experiment(SMOKE, Path(second))
            self.assertEqual(normalize_e04_machine_artifacts(first_outputs), normalize_e04_machine_artifacts(second_outputs))
            self.assertLessEqual(float(json.loads(first_outputs["manifest"].read_text())["standard_readiness"]["projected_runtime_minutes"]), 10.0)
            with first_outputs["raw"].open() as handle: raw = list(csv.DictReader(handle))
            broken = [dict(row) for row in raw]; broken[0]["child_id"] = "00"
            with self.assertRaises(ValueError): validate_e04_raw_rows(broken, self.config)
            broken = [dict(row) for row in raw]; broken[0]["final_window_mask_count"] = "999"
            with self.assertRaises(ValueError): validate_e04_raw_rows(broken, self.config)
            for field, value in (("b", "2"), ("alpha", ".2"), ("bf", ".1"), ("effective_good_fraction", ".5"), ("child_seed", "corrupt"), ("rng_unit", "corrupt"), ("group_action_count", "99"), ("settled_any_good_auth_argmax", "False"), ("good_auth_count_total", "999")):
                broken = [dict(row) for row in raw]; broken[0][field] = value
                with self.subTest(field=field):
                    with self.assertRaises(ValueError): validate_e04_raw_rows(broken, self.config)
            undefined = next(row for row in raw if row["final_window_auth_context_entropy_status"] == "undefined_no_authentic_samples")
            broken = [dict(row) for row in raw]; broken[raw.index(undefined)]["final_window_auth_context_entropy"] = "0"
            with self.assertRaises(ValueError): validate_e04_raw_rows(broken, self.config)
            accepted = next(row for row in raw if int(row["good_auth_accept_count_total"]) > 0)
            broken = [dict(row) for row in raw]; index = raw.index(accepted); broken[index]["ever_accepted_good_auth"] = "False"; broken[index]["time_to_first_accepted_good_auth_step"] = ""; broken[index]["time_to_first_accepted_good_auth_censored"] = "True"; broken[index]["time_to_first_accepted_good_auth_capped"] = str(self.config["T"])
            with self.assertRaises(ValueError): validate_e04_raw_rows(broken, self.config)
            never_accepted = next(row for row in raw if int(row["good_auth_accept_count_total"]) == 0)
            broken = [dict(row) for row in raw]; index = raw.index(never_accepted); broken[index]["ever_accepted_good_auth"] = "True"; broken[index]["time_to_first_accepted_good_auth_step"] = "0"; broken[index]["time_to_first_accepted_good_auth_censored"] = "False"; broken[index]["time_to_first_accepted_good_auth_capped"] = "0"
            with self.assertRaises(ValueError): validate_e04_raw_rows(broken, self.config)
            with first_outputs["curves"].open() as handle: curves = list(csv.DictReader(handle))
            broken_curves = [dict(row) for row in curves]; broken_curves[0]["mean_final_window_mask_rate"] = "0"
            with self.assertRaises(ValueError): validate_e04_curves(broken_curves, self.config, raw)
            with self.assertRaises(ValueError): validate_e04_curves(curves, self.config)
            with first_outputs["effects"].open() as handle: effects = list(csv.DictReader(handle))
            broken_effects = [dict(row) for row in effects]; broken_effects[0]["estimate"] = "1"
            with self.assertRaises(ValueError): validate_e04_effects(broken_effects, self.config, curves)
            with self.assertRaises(ValueError): validate_e04_effects(effects, self.config)
            ordered = sorted(raw, key=lambda row: (str(row["parameter_cell_id"]), int(row["master_seed"]), int(row["child_id"])))
            for field, value in (("policy_environment_seed", "1"), ("final_window_mask_count", "0"), ("bf", ".1"), ("effective_good_fraction", ".5"), ("good_context_ids_json", "[99]"), ("final_window_modal_action_index", "0"), ("cumulative_expected_static_regret", "0")):
                corrupted = [dict(row) for row in ordered]; corrupted[0][field] = value
                with self.subTest(stream_field=field):
                    with self.assertRaises(ValueError): stream_e04_raw_rows(Path(first) / f"bad-{field}.csv", (corrupted,), self.config)
            for label, source, ever, first_step, censored, capped in (("accepted_false", next(row for row in ordered if int(row["good_auth_accept_count_total"]) > 0), "False", "", "True", str(self.config["T"])), ("zero_true", next(row for row in ordered if int(row["good_auth_accept_count_total"]) == 0), "True", "0", "False", "0")):
                corrupted = [dict(row) for row in ordered]; index = ordered.index(source)
                corrupted[index].update({"ever_accepted_good_auth": ever, "time_to_first_accepted_good_auth_step": first_step, "time_to_first_accepted_good_auth_censored": censored, "time_to_first_accepted_good_auth_capped": capped})
                with self.subTest(stream_discovery_equivalence=label):
                    with self.assertRaises(ValueError): stream_e04_raw_rows(Path(first) / f"bad-discovery-{label}.csv", (corrupted,), self.config)


if __name__ == "__main__":
    unittest.main()
