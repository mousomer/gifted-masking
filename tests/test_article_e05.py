import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from gifted_masking.experiments.e05 import (
    BF_VALUES,
    E05_RAW_FIELDNAMES,
    analytic_values,
    derive_e05_policy_environment_seed,
    e05_standard_readiness_projection,
    e05_matched_family_id,
    invert_transition,
    load_e05_config,
    nonincreasing_pava,
    recompute_e05_cells,
    recompute_e05_effects,
    run_e05_experiment,
    record_e05_verification,
    simulate_e05_cell,
    validate_e05_derived,
    validate_e05_raw_rows,
    e05_bootstrap_transition,
    stream_e05_raw_rows,
    standard_cost_projection,
)
from gifted_masking.models import m3


ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "configs/frontiers_article/e05_m3_bflpe_crossover_smoke.json"
STANDARD = ROOT / "configs/frontiers_article/e05_m3_bflpe_crossover_standard.json"


class ArticleE05Tests(unittest.TestCase):
    def setUp(self): self.config = load_e05_config(SMOKE)

    def test_frozen_configs_and_standard_refusal(self):
        self.assertEqual(len(BF_VALUES), 18)
        self.assertFalse(load_e05_config(STANDARD)["approved_standard"])
        for key, value in (("n", 95), ("T", 301), ("workers", 2), ("bootstrap_replicates", 1)):
            with self.assertRaises(ValueError): load_e05_config(SMOKE, {key: value})
        duplicate = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        duplicate.write('{"experiment_id":"E05","experiment_id":"E05"}'); duplicate.close()
        with self.assertRaises(ValueError): load_e05_config(Path(duplicate.name))
        with self.assertRaises(PermissionError): run_e05_experiment(STANDARD, ROOT / "results")

    def test_exact_analytic_anchor_and_maintained_rewards(self):
        wanted = {0.: .4, .45: .0175, 8 / 17: 0., .475: -.00375, .8: -.28}
        for bf, advantage in wanted.items():
            values = analytic_values(bf, self.config)
            self.assertAlmostEqual(values["analytic_objective_advantage_good_auth_minus_mask"], advantage, places=12)
            replay = m3.expected_reward_for_action(np.arange(8), k_groups=4, bf=bf)
            self.assertAlmostEqual(float(replay[0]), values["expected_mask_reward"], places=12)
            self.assertAlmostEqual(float(replay[1]), values["expected_good_auth_reward"], places=12)
        anchor = analytic_values(8 / 17, self.config)
        self.assertEqual(anchor["objective_comparator"], "tie")
        self.assertEqual(anchor["objective_best_joint_actions"], [0, 1, 2, 4, 6])

    def test_bf_only_changes_accepted_good_auth_reward(self):
        low = analytic_values(0., self.config); high = analytic_values(.8, self.config)
        self.assertEqual(low["expected_mask_reward"], high["expected_mask_reward"])
        self.assertEqual(low["expected_bad_auth_reward"], high["expected_bad_auth_reward"])
        self.assertAlmostEqual(low["expected_good_auth_reward"] - high["expected_good_auth_reward"], .68)

    def test_family_pairing_order_and_small_raw_reconciliation(self):
        config = copy.deepcopy(self.config); config["n"] = 8; config["T"] = 30
        seed_flat = derive_e05_policy_environment_seed(config["master_seed"], "flat_2k")
        seed_hier = derive_e05_policy_environment_seed(config["master_seed"], "hierarchical")
        self.assertNotEqual(seed_flat, seed_hier)
        self.assertEqual(e05_matched_family_id(config["master_seed"], "flat_2k"), e05_matched_family_id(config["master_seed"], "flat_2k"))
        left = simulate_e05_cell(config, "flat_2k", 0., seed_flat)
        right = simulate_e05_cell(config, "flat_2k", .8, seed_flat)
        self.assertEqual([row["child_id"] for row in left], [row["child_id"] for row in right])
        self.assertTrue(all(list(row) == E05_RAW_FIELDNAMES for row in left))
        # Exact maintained replay at bf=0, including the accepted-uniform on masks.
        settled, mask, modal = m3.simulate(4, n=8, horizon=30, seed=seed_flat, final_window_fraction=.2)
        self.assertEqual([row["modal_good_auth_argmax"] == "True" for row in left], settled.tolist())
        np.testing.assert_allclose([float(row["final_window_mask_rate"]) for row in left], mask)
        self.assertEqual([int(row["final_window_modal_action_index"]) for row in left], modal.tolist())
        hierarchical = simulate_e05_cell(config, "hierarchical", 0., seed_hier)
        settled_h, mask_h, modal_h = m3.simulate_hierarchical(4, n=8, horizon=30, seed=seed_hier, final_window_fraction=.2)
        self.assertEqual([row["modal_good_auth_argmax"] == "True" for row in hierarchical], settled_h.tolist())
        np.testing.assert_allclose([float(row["final_window_mask_rate"]) for row in hierarchical], mask_h)
        self.assertEqual([int(row["final_window_modal_action_index"]) for row in hierarchical], modal_h.tolist())

    def test_pava_and_transition_boundaries(self):
        np.testing.assert_allclose(nonincreasing_pava([.9, .7, .3]), [.9, .7, .3])
        np.testing.assert_allclose(nonincreasing_pava([.9, .2, .5]), [.9, .35, .35])
        point, status = invert_transition([.3, .4, .5], [.9, .5, .1])
        self.assertEqual(status, "valid"); self.assertAlmostEqual(point, .4)
        self.assertEqual(invert_transition([.3, .4], [.9, .8])[1], "no_crossing_above")
        self.assertEqual(invert_transition([.3, .4], [.2, .1])[1], "no_crossing_below")
        for args in (([.9, float('nan')],), ([.9, .8], [1., 0.])):
            with self.assertRaises(ValueError): nonincreasing_pava(*args)
        with self.assertRaises(ValueError): invert_transition([.3, .3], [.8, .2])

    def test_standard_synthetic_bootstrap_is_architecture_isolated(self):
        curves = [[.9 - .05 * i for i in range(16)] for _ in range(5)]
        flat = e05_bootstrap_transition(curves, "flat_2k")
        hierarchical = e05_bootstrap_transition(curves, "hierarchical")
        self.assertEqual(flat["valid"], 10000); self.assertTrue(flat["estimable"])
        self.assertEqual(hierarchical["valid"], 10000)

    def test_phase_scaled_readiness_does_not_multiply_plot_startup(self):
        readiness = e05_standard_readiness_projection({"simulation": .8, "derived": .05, "serialization": .12, "figure": 3.0})
        self.assertAlmostEqual(readiness["projected_components_seconds"]["figure"], 3.0)
        self.assertAlmostEqual(readiness["scale_factors"]["simulation"], 173.61111111111111)
        self.assertAlmostEqual(readiness["scale_factors"]["serialization"], 26.041666666666668)
        self.assertTrue(readiness["within_runtime_limit"])
        with self.assertRaises(ValueError):
            e05_standard_readiness_projection({"simulation": 1.0})
        capacity = standard_cost_projection(3_500_000, 1.0, 64.0)
        self.assertAlmostEqual(capacity["row_ratio"], 90000 / 3456)
        self.assertTrue(capacity["within_limits"])
        with self.assertRaises(ValueError): standard_cost_projection(float("nan"), 1., 1.)

    def test_verification_seal_requires_passed_deterministic_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = {name: root / f"{name}.txt" for name in ("manifest", "raw", "analytic", "cells", "effects", "transitions", "figure", "report")}
            for name, path in paths.items():
                if name != "manifest": path.write_text(name)
            manifest = {"experiment_id": "E05", "tier": "smoke", "parameters": self.config, "outputs": {name: {"path": str(path)} for name, path in paths.items()}, "timing": {"wall_seconds": 1.0}, "standard_readiness": {"projected_standard_seconds": 100.0, "runtime_limit_seconds": 600.0, "within_runtime_limit": True}, "warnings": [], "verification": {"status": "pending_external_tests"}}
            paths["manifest"].write_text(json.dumps(manifest))
            with self.assertRaises(ValueError): record_e05_verification(paths, status="passed", command="verify", deterministic_scientific_artifacts=False)
            record_e05_verification(paths, status="passed", command="verify", deterministic_scientific_artifacts=True)
            sealed = json.loads(paths["manifest"].read_text())
            self.assertEqual(sealed["verification"]["status"], "passed")
            self.assertTrue(sealed["verification"]["deterministic_scientific_artifacts"])

    def test_smoke_shape_reconstructs(self):
        # Build in memory once, avoiding filesystem/plotting in the unit suite.
        rows = []
        for architecture in ("flat_2k", "hierarchical"):
            seed = derive_e05_policy_environment_seed(self.config["master_seed"], architecture)
            for bf in BF_VALUES: rows.extend(simulate_e05_cell(self.config, architecture, bf, seed))
        validate_e05_raw_rows(rows, self.config)
        cells = recompute_e05_cells(rows)
        effects = recompute_e05_effects(cells, self.config)
        from gifted_masking.experiments.e05 import _analytic_rows, _transition_rows
        transitions = _transition_rows(cells, self.config)
        validate_e05_derived(_analytic_rows(self.config), cells, effects, transitions, self.config, rows)
        self.assertEqual(len(rows), 3456); self.assertEqual(len(cells), 36); self.assertEqual(len(effects), 258); self.assertEqual(len(transitions), 4)

    def test_full_row_boundary_rejects_named_corruptions_in_memory_and_stream(self):
        rows = simulate_e05_cell(self.config, "flat_2k", 0., derive_e05_policy_environment_seed(self.config["master_seed"], "flat_2k"))
        # Build the whole ordered contract once, then mutate one frozen semantic
        # field at a time; the shared boundary must reject in both entry paths.
        all_rows = []
        for arch in ("flat_2k", "hierarchical"):
            seed = derive_e05_policy_environment_seed(self.config["master_seed"], arch)
            for bf in BF_VALUES: all_rows.extend(simulate_e05_cell(self.config, arch, bf, seed))
        for field, bad in (("tier", "standard"), ("model", "M0"), ("component", "other"), ("K", 5), ("good_context_id", 1), ("p_good", .84), ("bf_label", "bad"), ("n", 95), ("T", 301), ("final_window_start", 1), ("cell_seed", 0), ("final_window_mask_rate", .1), ("final_window_modal_action_index", 7), ("mean_expected_static_regret", .1), ("expected_good_auth_reward", 0.0)):
            mutated = copy.deepcopy(all_rows); mutated[0][field] = bad
            with self.assertRaises(ValueError, msg=field): validate_e05_raw_rows(mutated, self.config)
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ValueError, msg=f"stream {field}"):
                    stream_e05_raw_rows(Path(tmp) / "rows.csv", [mutated], self.config)
        anchored = copy.deepcopy(all_rows); anchored[8 * 96]["is_analytic_threshold_anchor"] = "False"
        with self.assertRaises(ValueError): validate_e05_raw_rows(anchored, self.config)
        coordinated = copy.deepcopy(all_rows)
        coordinated[0]["cumulative_realized_objective_reward"] = float(coordinated[0]["cumulative_realized_objective_reward"]) + 1
        coordinated[0]["mean_realized_objective_reward"] = float(coordinated[0]["mean_realized_objective_reward"]) + 1 / 300
        coordinated[0]["cumulative_realized_pseudo_regret"] = float(coordinated[0]["cumulative_realized_pseudo_regret"]) - 1
        coordinated[0]["mean_realized_pseudo_regret"] = float(coordinated[0]["mean_realized_pseudo_regret"]) - 1 / 300
        with self.assertRaises(ValueError): validate_e05_raw_rows(coordinated, self.config)
        q_corrupt = copy.deepcopy(all_rows); q_corrupt[0]["q_final_json"] = "[NaN,0,0,0,0,0,0,0]"
        with self.assertRaises(ValueError): validate_e05_raw_rows(q_corrupt, self.config)


if __name__ == "__main__": unittest.main()
