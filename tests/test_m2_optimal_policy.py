import csv
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

from gifted_masking.analysis.m2_optimal import (
    M2Params,
    build_m2_transition_table,
    classify_m2_cell,
    solve_m2_value_iteration,
    static_m0_comparator,
    transition_arrays,
)
from gifted_masking.experiments.robustness import generate_unit_rows, summarize_unit_rows
from gifted_masking.models import m2
from scripts import benchmark_m2_optimal_policy
from scripts import analyze_m2_regimes
from scripts import map_m2_lock_in_regions


def canonical_state(path):
    return (path.read_bytes(), path.stat().st_mtime_ns) if path.exists() else None


class M2OptimalPolicyTests(unittest.TestCase):
    def test_transition_table_shape_and_validity(self):
        table = build_m2_transition_table(M2Params(p=0.55, eta=0.2))
        probabilities, rewards = transition_arrays(table)
        self.assertEqual(probabilities.shape, (3, 2, 3))
        self.assertEqual(rewards.shape, (3, 2, 3))
        np.testing.assert_allclose(probabilities.sum(axis=2), np.ones((3, 2)))
        self.assertTrue(np.all(probabilities >= 0.0))

    def test_value_iteration_converges(self):
        result = solve_m2_value_iteration(M2Params(p=0.55, eta=0.2), tol=1e-10)
        self.assertTrue(result["converged"])
        self.assertLessEqual(result["residual"], 1e-10)
        self.assertEqual(result["Q"].shape, (3, 2))
        self.assertIn(result["chosen_actions"]["neutral"], {"mask", "authentic"})

    def test_static_comparator_sanity(self):
        low = static_m0_comparator(M2Params(p=0.20, eta=0.0))
        high = static_m0_comparator(M2Params(p=0.85, eta=0.0))
        self.assertEqual(low["optimal_action"], "mask")
        self.assertEqual(high["optimal_action"], "authentic")
        self.assertAlmostEqual(low["E_mask"], 0.75)
        self.assertAlmostEqual(high["auth_advantage"], 0.4)

    def test_benchmark_output_is_deterministic(self):
        canonical = benchmark_m2_optimal_policy.ROOT / "results/summaries/m2_optimal_policy_benchmark.csv"
        before = canonical_state(canonical)
        with tempfile.TemporaryDirectory(prefix="m2_benchmark_test_") as temporary:
            with mock.patch.object(benchmark_m2_optimal_policy, "ROOT", Path(temporary)):
                benchmark_m2_optimal_policy.main()
                output = Path(temporary) / "results/summaries/m2_optimal_policy_benchmark.csv"
                first = output.read_text()
                benchmark_m2_optimal_policy.main()
                self.assertEqual(first, output.read_text())
                with output.open(newline="") as handle:
                    rows = list(csv.DictReader(handle))
        self.assertEqual(canonical_state(canonical), before)
        self.assertGreaterEqual(len(rows), 7)
        self.assertTrue(all(row["converged"] == "True" for row in rows))
        self.assertIn("regret_neutral", rows[0])

    def test_m2_headline_effect_does_not_drift(self):
        rows = generate_unit_rows(run_id="robustness_full", suite="full")
        summaries = {result.check_name: result for result in summarize_unit_rows(rows, suite="full")}
        self.assertAlmostEqual(summaries["higher_escape_rate_reduces_masking"].estimate, 0.20072916666666665)

    def test_classification_marks_learned_suboptimal_lock_in_for_reference_cell(self):
        params = M2Params(p=0.55, eta=0.0)
        diagnostics = m2.simulate_with_diagnostics(0.55, 0.0, n=160, horizon=1000, seed=9100)
        classified = classify_m2_cell(params, diagnostics)
        self.assertEqual(classified["dynamic_neutral_action"], "authentic")
        self.assertEqual(classified["learned_neutral_action"], "mask")
        self.assertEqual(classified["region"], "learned_suboptimal_lock_in")
        self.assertTrue(classified["regret_available"])
        self.assertGreater(classified["regret_neutral"], 0.0)

    def test_lock_in_map_output_is_deterministic(self):
        names = ("m2_lock_in_region_map.csv", "m2_lock_in_region_thresholds.csv")
        canonical = [map_m2_lock_in_regions.ROOT / "results/summaries" / name for name in names]
        before = [canonical_state(path) for path in canonical]
        with tempfile.TemporaryDirectory(prefix="m2_map_test_") as temporary:
            with mock.patch.object(map_m2_lock_in_regions, "ROOT", Path(temporary)):
                map_m2_lock_in_regions.main()
                output = Path(temporary) / "results/summaries" / names[0]
                thresholds = Path(temporary) / "results/summaries" / names[1]
                first_map = output.read_text()
                first_thresholds = thresholds.read_text()
                map_m2_lock_in_regions.main()
                self.assertEqual(first_map, output.read_text())
                self.assertEqual(first_thresholds, thresholds.read_text())
                with output.open(newline="") as handle:
                    rows = list(csv.DictReader(handle))
        self.assertEqual([canonical_state(path) for path in canonical], before)
        self.assertEqual(len(rows), len(map_m2_lock_in_regions.P_VALUES) * len(map_m2_lock_in_regions.ETA_VALUES))
        self.assertTrue(all(row["converged"] == "True" for row in rows))
        self.assertTrue(any(row["region"] == "learned_suboptimal_lock_in" for row in rows))

    def test_refined_thresholds_show_dynamic_authenticity_before_static_under_defaults(self):
        rows = analyze_m2_regimes.build_refined_threshold_rows()
        self.assertTrue(all(float(row["optimal_lock_in_width"]) == 0.0 for row in rows))
        self.assertTrue(all(float(row["dynamic_authenticity_before_static_width"]) > 0.0 for row in rows))

    def test_environment_sensitivity_finds_possible_optimal_policy_lock_in(self):
        rows = analyze_m2_regimes.build_optimal_sensitivity_rows()
        lock_rows = [row for row in rows if row["regime_note"] == "optimal_learner_lock_in_possible"]
        self.assertTrue(lock_rows)
        self.assertGreater(max(float(row["optimal_lock_in_width"]) for row in lock_rows), 0.04)


if __name__ == "__main__":
    unittest.main()
