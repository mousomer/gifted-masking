import copy
import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from gifted_masking.analysis.m2_optimal import M2Params
from gifted_masking.experiments.article import load_article_config
from gifted_masking.experiments.e02 import load_e02_config
from gifted_masking.experiments.e03 import (
    E03_RAW_FIELDNAMES,
    _validate_e03_standard_approval,
    _standard_specs,
    _within_one_ulp,
    canonical_e03_cell_id,
    canonical_e03_exact_grid,
    canonical_e03_trajectory_prefix_id,
    classify_e03_cell,
    derive_e03_cell_seed,
    e03_rng_family_id,
    load_e03_config,
    objective_threshold_bisection,
    recompute_e03_summaries,
    refine_learned_threshold,
    run_e03_experiment,
    simulate_e03_sentinel,
    standard_harsh_cases,
    standard_streaming_cost_plan,
    stream_e03_raw_rows,
    student_t_95_interval,
    summarize_e03_standard_classifications,
)
from gifted_masking.models import m2


ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "configs/frontiers_article/e03_m2_regime_smoke.json"
STANDARD = ROOT / "configs/frontiers_article/e03_m2_regime_standard.json"


class ArticleE03Tests(unittest.TestCase):
    def setUp(self):
        self.config = load_e03_config(SMOKE)

    def test_frozen_configs_and_standard_refusal(self):
        self.assertEqual(self.config["run_id"], "frontiers_m2_regime_replication_v1_smoke")
        self.assertFalse(load_e03_config(STANDARD)["approved_standard"])
        for key, value in (("n", 65), ("T", 301), ("workers", 2), ("master_seed", 2026081400)):
            with self.assertRaises(ValueError):
                load_e03_config(SMOKE, {key: value})
        with self.assertRaises(PermissionError):
            run_e03_experiment(STANDARD, Path(tempfile.gettempdir()) / "e03-forbidden")
        with self.assertRaises(PermissionError):
            _validate_e03_standard_approval(ROOT, None)
        approval = ROOT / "projects/frontiers_article/approvals/E03_STANDARD_GO.md"
        self.assertEqual(_validate_e03_standard_approval(ROOT, approval), approval)
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "E03_STANDARD_GO.md"; copied.write_text(approval.read_text())
            with self.assertRaises(PermissionError):
                _validate_e03_standard_approval(ROOT, copied)
        standard = load_e03_config(STANDARD)
        bad = copy.deepcopy(standard); bad["one_at_a_time"]["T"] = [4000]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad-standard.json"; path.write_text(json.dumps(bad))
            with self.assertRaises(ValueError): load_e03_config(path)

    def test_recursive_contract_rejects_nested_mutations(self):
        for mutate in (
            lambda payload: payload["environment"].__setitem__("b", 1),
            lambda payload: payload["learner"].__setitem__("gamma", .8),
            lambda payload: payload["smoke_sentinels"][0].__setitem__("p", ".35"),
            lambda payload: payload["legacy_provenance_replay"].__setitem__("seed_base", 9101),
            lambda payload: payload["smoke_sentinels"].append({"p": .1, "eta": 0.}),
        ):
            payload = copy.deepcopy(self.config); mutate(payload)
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "invalid.json"; path.write_text(json.dumps(payload))
                with self.assertRaises(ValueError): load_e03_config(path)

    def test_standard_dispatch_plan_has_only_authorized_factor_cells(self):
        standard = load_e03_config(STANDARD)
        specs = _standard_specs(standard)
        self.assertEqual(len(specs), 450)
        self.assertEqual(sum(spec["component"] == "exact_grid" for spec in specs), 357)
        self.assertEqual(sum(spec["component"] == "harsh" for spec in specs), 3)
        self.assertTrue(all(spec["component"] in {"exact_grid", "sentinels", "harsh"} for spec in specs))

    def test_semantic_seed_and_prefix_pairing_contract(self):
        cell = self.config["smoke_sentinels"][2]
        full = canonical_e03_cell_id(self.config, cell)
        altered = canonical_e03_cell_id(self.config, cell, horizon=5000, window=.4)
        prefix = canonical_e03_trajectory_prefix_id(self.config, cell, component="smoke_sentinels", sensitivity_name="baseline")
        altered_config = dict(self.config); altered_config["T"] = 5000; altered_config["final_window_fraction"] = .4
        altered_prefix = canonical_e03_trajectory_prefix_id(altered_config, cell, component="smoke_sentinels", sensitivity_name="baseline")
        self.assertNotEqual(full, altered)
        self.assertEqual(prefix, altered_prefix)
        self.assertEqual(derive_e03_cell_seed(self.config["master_seed"], full), derive_e03_cell_seed(self.config["master_seed"], full))
        self.assertNotEqual(derive_e03_cell_seed(self.config["master_seed"], full), derive_e03_cell_seed(self.config["master_seed"], altered))

    def test_component_and_sensitivity_aware_parameter_ids_do_not_collide(self):
        standard = load_e03_config(STANDARD); cell = standard["sentinels"][2]
        ids = {
            canonical_e03_cell_id(standard, cell, component="exact_grid", sensitivity_name="baseline", n=160, horizon=1000, window=.2),
            canonical_e03_cell_id(standard, cell, component="sentinels", sensitivity_name="baseline", n=160, horizon=1000, window=.2),
            canonical_e03_cell_id(standard, cell, component="sentinels", sensitivity_name="T", n=160, horizon=2000, window=.2),
            canonical_e03_cell_id(standard, cell, component="harsh", sensitivity_name="b2_r2_delta", n=160, horizon=1000, window=.2, environment={**standard["environment"], "b2": 0., "r2": 8., "delta": .3}),
            canonical_e03_cell_id(standard, cell, component="threshold_refinement", sensitivity_name="learned_dyadic", n=160, horizon=1000, window=.2),
        }
        self.assertEqual(len(ids), 5)

    def test_genuine_standard_t_window_prefix_family_and_independent_cases(self):
        standard = load_e03_config(STANDARD); cell = standard["sentinels"][2]
        base = e03_rng_family_id(standard, cell, component="sentinels", sensitivity_name="T", n=160, horizon=1000, window=.2)
        high_t = e03_rng_family_id(standard, cell, component="sentinels", sensitivity_name="T", n=160, horizon=2000, window=.2)
        short_window = e03_rng_family_id(standard, cell, component="sentinels", sensitivity_name="final_window_fraction", n=160, horizon=1000, window=.1)
        alpha = e03_rng_family_id(standard, cell, component="sentinels", sensitivity_name="alpha", n=160, horizon=1000, window=.2)
        larger_n = e03_rng_family_id(standard, cell, component="sentinels", sensitivity_name="n", n=320, horizon=1000, window=.2)
        altered_learner = copy.deepcopy(standard); altered_learner["learner"]["alpha"] = .3
        nondefault_t = e03_rng_family_id(altered_learner, cell, component="sentinels", sensitivity_name="T", n=160, horizon=2000, window=.2)
        self.assertEqual(base, high_t); self.assertEqual(base, short_window)
        self.assertNotEqual(base, alpha); self.assertNotEqual(base, larger_n); self.assertNotEqual(base, nondefault_t)
        seed = derive_e03_cell_seed(standard["master_seed"], base)
        self.assertEqual(seed, derive_e03_cell_seed(standard["master_seed"], high_t))
        trace_short, trace_long = [], []
        original = m2.transition_step
        def traced(target):
            def wrapper(state, action, **kwargs):
                target.append((state.copy(), action.copy()))
                return original(state, action, **kwargs)
            return wrapper
        with patch("gifted_masking.models.m2.transition_step", side_effect=traced(trace_short)):
            m2.simulate_with_diagnostics(.55, 0., n=4, horizon=15, seed=seed)
        with patch("gifted_masking.models.m2.transition_step", side_effect=traced(trace_long)):
            m2.simulate_with_diagnostics(.55, 0., n=4, horizon=30, seed=seed)
        self.assertEqual(len(trace_short), 15); self.assertEqual(len(trace_long), 30)
        for left, right in zip(trace_short, trace_long[:15], strict=True):
            np.testing.assert_array_equal(left[0], right[0]); np.testing.assert_array_equal(left[1], right[1])

    def test_global_rng_isolation_and_raw_count_window_reward_reconciliation(self):
        cell = self.config["smoke_sentinels"][2]; cell_id = canonical_e03_cell_id(self.config, cell); seed = derive_e03_cell_seed(self.config["master_seed"], cell_id)
        before = np.random.get_state(); rows, _ = simulate_e03_sentinel(self.config, cell, cell_id, seed); after = np.random.get_state()
        self.assertEqual(E03_RAW_FIELDNAMES, list(rows[0]))
        self.assertEqual(before[0], after[0]); np.testing.assert_array_equal(before[1], after[1]); self.assertEqual(before[2:], after[2:])
        self.assertEqual(len(rows), 64)
        summaries = recompute_e03_summaries(rows, self.config)
        self.assertEqual(len(summaries), 1)
        self.assertAlmostEqual(summaries[0]["mean_final_window_mask_rate"], np.mean([float(row["final_window_mask_rate"]) for row in rows]))
        corrupted = [dict(row) for row in rows]; corrupted[0]["neutral_visit_count"] = int(corrupted[0]["neutral_visit_count"]) + 1
        with self.assertRaises(ValueError): recompute_e03_summaries(corrupted, self.config)

    def test_tie_and_p1_missing_stigma_contract(self):
        def diagnostics(mask, auth, *, stigma=False):
            counts = np.zeros((64, 3, 2), dtype=int); visits = np.zeros((64, 3), dtype=int)
            counts[:, 0, 0] = mask; counts[:, 0, 1] = auth; visits[:, 0] = mask + auth
            counts[:, 1, 1] = 2; visits[:, 1] = 2
            if stigma:
                counts[:, 2, 0] = 2; visits[:, 2] = 2
            return {"state_action_counts_final": counts, "state_visit_counts_final": visits, "mask_rate_final": np.full(64, mask / (mask + auth + 2)), "reward_mean_final": np.ones(64)}
        tie = classify_e03_cell(M2Params(p=.55, eta=0), diagnostics(2, 2, stigma=True), n=64)
        self.assertEqual(tie["classification"], "inconclusive")
        self.assertEqual(tie["learner_status"], "inconclusive_neutral_tie")
        p1 = classify_e03_cell(M2Params(p=1.0, eta=0), diagnostics(3, 1, stigma=False), n=64)
        self.assertNotEqual(p1["learner_status"], "inconclusive_neutral_visit")
        self.assertEqual(p1["classification"], "learned_suboptimal_masking")
        self.assertEqual(p1["full_policy_status"], "available")
        self.assertGreater(float(p1["neutral_decision_regret"]), 0)
        match = classify_e03_cell(M2Params(p=1.0, eta=0), diagnostics(1, 3, stigma=False), n=64)
        self.assertEqual(match["neutral_decision_regret"], 0.0)

    def test_frozen_legacy_mean_uses_fsum_or_one_ulp_only(self):
        frozen = .9501766068109203
        self.assertTrue(_within_one_ulp(frozen, frozen))
        self.assertTrue(_within_one_ulp(math.nextafter(frozen, math.inf), frozen))
        self.assertTrue(_within_one_ulp(math.nextafter(frozen, -math.inf), frozen))
        self.assertFalse(_within_one_ulp(math.nextafter(math.nextafter(frozen, math.inf), math.inf), frozen))

    def test_e03_semantic_parity_uses_maintained_reward_first_m2_kernel(self):
        reward, state = m2.transition_step(
            np.array([m2.STATE_NEUTRAL, m2.STATE_ACCEPTED, m2.STATE_STIGMATIZED]), np.array([1, 1, 1]),
            p=.6, eta=.2, outcome_uniform=np.array([.8, .1, .1]), turnover_uniform=np.array([.9, .0, .9]), escape_uniform=np.array([.9, .9, .9]),
        )
        np.testing.assert_allclose(reward, np.array([-1.4, 1.6, 1.6]))
        np.testing.assert_array_equal(state, np.array([m2.STATE_STIGMATIZED, m2.STATE_NEUTRAL, m2.STATE_ACCEPTED]))

    def test_standard_helpers_intervals_stability_threshold_refinement_and_harsh_cells(self):
        estimate, low, high = student_t_95_interval([.4, .5, .6, .5, .5])
        self.assertAlmostEqual(estimate, .5); self.assertLess(low, estimate); self.assertGreater(high, estimate)
        self.assertEqual(student_t_95_interval([.5, .6]), ("", "", ""))
        records = self._valid_exact_grid_records()
        effects, stable = summarize_e03_standard_classifications(records)
        self.assertEqual(len(effects), 6); self.assertEqual(effects[-1]["ci_status"], "student_t_95")
        self.assertTrue(all(row["stable"] for row in stable))
        threshold = objective_threshold_bisection(M2Params(p=0., eta=.2), tolerance=1e-4)
        self.assertEqual(threshold["status"], "bracketed"); self.assertLessEqual(float(threshold["bracket_width"]), 1e-4)
        refined = refine_learned_threshold({0.: "mask", 1.: "authentic"}, lambda p: "mask" if p < .5 else "authentic")
        self.assertEqual(refined["status"], "bracketed"); self.assertLessEqual(refined["bracket"][1] - refined["bracket"][0], .0125)
        self.assertEqual(refine_learned_threshold({0.: "mask", .5: "authentic", 1.: "mask"}, lambda p: "mask")["status"], "nonmonotone")
        self.assertEqual(refine_learned_threshold({0.: "mask", 1.: None}, lambda p: "mask")["status"], "censored_inconclusive")
        harsh = standard_harsh_cases(load_e03_config(STANDARD)); self.assertEqual([case.b2 for case in harsh], [0., 0., 0.])

    @staticmethod
    def _valid_exact_grid_records():
        records = []
        canonical = canonical_e03_exact_grid()
        for seed in (2026081301, 2026081302, 2026081303, 2026081304, 2026081305):
            for index, (parameter_cell_id, fields) in enumerate(sorted(canonical.items())):
                records.append({"component": "exact_grid", "sensitivity_name": "baseline", "master_seed": seed, "parameter_cell_id": parameter_cell_id, "classification": "learned_suboptimal_masking" if index < 226 else "learner_matches_objective", **fields})
        return records

    def test_standard_summary_fails_closed_for_cardinality_seed_and_component_errors(self):
        valid = self._valid_exact_grid_records()
        effects, stable = summarize_e03_standard_classifications(valid)
        self.assertEqual(len(effects), 6); self.assertEqual(len(stable), 357)
        altered_id = dict(valid[0]); altered_id["parameter_cell_id"] = "arbitrary-cell-id"
        altered_p = dict(valid[0]); altered_p["p"] = .999
        non_grid = dict(valid[0]); non_grid["component"] = "sentinels"
        last_cell_id = valid[-1]["parameter_cell_id"]
        cases = [
            valid[:-1],
            valid + [dict(valid[0])],
            [dict(row, master_seed=2026081399) if row["master_seed"] == 2026081305 else row for row in valid],
            [row for row in valid if not (row["master_seed"] == 2026081305 and row["parameter_cell_id"] == last_cell_id)],
            valid[1:] + [altered_id],
            valid[1:] + [altered_p],
            valid[1:] + [non_grid],
        ]
        for rows in cases:
            with self.subTest(case=len(rows)):
                with self.assertRaises(ValueError): summarize_e03_standard_classifications(rows)

    def test_streaming_writer_matches_in_memory_recomputation_and_capacity_plan(self):
        cell = self.config["smoke_sentinels"][0]; cell_id = canonical_e03_cell_id(self.config, cell); seed = derive_e03_cell_seed(self.config["master_seed"], cell_id)
        rows, _ = simulate_e03_sentinel(self.config, cell, cell_id, seed)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "stream.csv"; streamed = stream_e03_raw_rows(path, (rows[:17], rows[17:]))
            with path.open(newline="") as handle:
                self.assertEqual(len(list(__import__("csv").DictReader(handle))), len(rows))
        recomputed = recompute_e03_summaries(rows, self.config)[0]
        self.assertEqual(streamed[0]["n"], recomputed["n"])
        self.assertAlmostEqual(float(streamed[0]["mean_final_window_mask_rate"]), float(recomputed["mean_final_window_mask_rate"]), places=12)
        plan = standard_streaming_cost_plan()
        self.assertEqual(plan["new_learner_steps"], 408_000_000); self.assertEqual(plan["estimated_primary_rows"], 384_000); self.assertEqual(plan["measured_raw_bytes"], 390_912_614); self.assertEqual(plan["measured_raw_mib"], 372.8); self.assertEqual(plan["raw_bound_mib"], "~400"); self.assertEqual(plan["streaming_peak_mib"], 35.6); self.assertEqual(plan["accepted_runtime_minutes"], "2.8-4"); self.assertLessEqual(plan["peak_memory_target_gib"], 2)

    def test_e01_e02_config_non_regression(self):
        self.assertEqual(load_article_config(ROOT / "configs/frontiers_article/e01_hot_stove_smoke.json")["experiment_id"], "E01")
        self.assertEqual(load_e02_config(ROOT / "configs/frontiers_article/e02_binary_graded_smoke.json")["experiment_id"], "E02")


if __name__ == "__main__":
    unittest.main()
