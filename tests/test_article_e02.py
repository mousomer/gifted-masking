import csv
import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np

from gifted_masking.experiments.e02 import (
    E02_RAW_FIELDNAMES,
    EFFECT_NAMES,
    SOURCE_FINGERPRINT_PATHS,
    T_CRITICAL_95_DF4,
    _e02_effects,
    _report,
    _source_fingerprint,
    _stable_full_auth_times,
    _stable_full_auth_times_quadratic_reference,
    _unique_modal_index,
    _validate_e02_standard_approval,
    analytic_arms,
    canonical_e02_pair_id,
    derive_e02_policy_environment_seed,
    load_e02_config,
    normalize_e02_machine_artifacts,
    recompute_e02_summaries,
    run_e02_experiment,
    simulate_e02_cell,
)
from gifted_masking.models import m0, m1


ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "configs/frontiers_article/e02_binary_graded_smoke.json"
STANDARD = ROOT / "configs/frontiers_article/e02_binary_graded_standard.json"


class ArticleE02Tests(unittest.TestCase):
    def setUp(self):
        self.config = load_e02_config(SMOKE)

    def _cell(self, architecture, p=.75):
        return next(cell for cell in self.config["cells"] if cell["architecture"] == architecture and cell["p"] == p)

    def _seed(self, cell):
        return derive_e02_policy_environment_seed(self.config["master_seed"], canonical_e02_pair_id(self.config, cell["p"]))

    def test_frozen_config_and_standard_refusal(self):
        self.assertEqual(self.config["run_id"], "frontiers_m1_binary_graded_v1_smoke")
        for key, value in (("n", 95), ("T", 299), ("workers", 2), ("final_window_fraction", .25)):
            with self.assertRaises(ValueError):
                load_e02_config(SMOKE, {key: value})
        with self.assertRaises(PermissionError):
            run_e02_experiment(STANDARD, Path(tempfile.gettempdir()) / "e02-forbidden")
        # An E01 GO record cannot authorize E02 standard execution.
        with tempfile.TemporaryDirectory() as directory:
            approval = Path(directory) / "e01.md"; approval.write_text("E01 GO_STANDARD")
            with self.assertRaises(PermissionError): run_e02_experiment(STANDARD, Path(directory) / "out", approval)

    def test_e02_standard_authorization_is_canonical_and_tier_report_is_correct(self):
        standard = load_e02_config(STANDARD)
        canonical = ROOT / "projects/frontiers_article/approvals/E02_STANDARD_GO.md"
        self.assertEqual(_validate_e02_standard_approval(ROOT, canonical), canonical.resolve())
        with tempfile.TemporaryDirectory() as directory:
            wrong = Path(directory) / "wrong.md"; wrong.write_text("# E02 Standard Execution Authorization\n**Decision:** `GO_STANDARD`")
            with self.assertRaises(PermissionError): _validate_e02_standard_approval(ROOT, wrong)
        paths = {name: Path(f"{name}.artifact") for name in ("manifest", "raw", "arms", "cells", "effects", "figure", "report")}
        report = _report(standard, paths, 1.0, [], 15000, verification="passed", provenance={"commit": "abc", "dirty": True}, approval_record=str(canonical))
        self.assertIn("E02 Standard Execution Report", report)
        self.assertIn("steps 1600-1999", report)
        self.assertIn("authorized Pass D standard execution", report)
        self.assertIn("No sensitivity, publication-tier, claim adjudication", report)

    def test_strict_json_types_and_recursive_contract_reject_mutations(self):
        def invalid(mutator):
            payload = copy.deepcopy(self.config); mutator(payload)
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "bad.json"; path.write_text(json.dumps(payload))
                with self.assertRaises(ValueError): load_e02_config(path)
        for key, value in (("n", 96.0), ("T", "300"), ("workers", True), ("master_seed", False), ("final_window_fraction", "0.2")):
            invalid(lambda payload, key=key, value=value: payload.__setitem__(key, value))
        invalid(lambda payload: payload["cells"][0].__setitem__("p", "0.65"))
        invalid(lambda payload: payload["cells"][0].__setitem__("levels", "2"))
        invalid(lambda payload: payload["cells"][0].__setitem__("levels", 2.9))
        invalid(lambda payload: payload["payoffs"].__setitem__("b", True))
        invalid(lambda payload: payload["learner"].__setitem__("alpha", "0.1"))
        invalid(lambda payload: payload["payoffs"].__setitem__("unexpected", 1.0))
        invalid(lambda payload: payload["learner"].pop("tau"))
        invalid(lambda payload: payload["cells"][0].__setitem__("unknown", 1))
        invalid(lambda payload: payload["cells"][0].pop("architecture"))

    def test_analytic_endpoint_and_intermediate_equations(self):
        for p, endpoint in ((.65, 0), (.75, 1), (.85, 1)):
            arms = analytic_arms(p, m1.disclosure_levels(5))
            self.assertAlmostEqual(arms[0]["expected_reward"], .75)
            self.assertAlmostEqual(arms[-1]["expected_reward"], m0.expected_rewards(p)[1])
            self.assertEqual(max(arms, key=lambda row: row["expected_reward"])["d"], float(endpoint))
            self.assertTrue(all(0 <= row["acceptance_probability"] <= 1 for row in arms))
            self.assertTrue(all(row["d"] in {0., 1.} or row["expected_reward"] < max(arms[0]["expected_reward"], arms[-1]["expected_reward"]) for row in arms))

    def test_unforced_replay_matches_maintained_m0_and_m1(self):
        binary = self._cell("binary_endpoints", .75); seed = self._seed(binary)
        rows = simulate_e02_cell(self.config, binary, seed, force_initial=False)
        observed_mask = 1 - np.array([float(row["final_window_full_authentic_rate"]) for row in rows])
        expected_mask = m0.simulate(.75, n=96, horizon=300, alpha=.1, temp=.25, lam=1, q0=0, seed=seed, final_window_fraction=.2)
        np.testing.assert_allclose(observed_mask, expected_mask, rtol=0, atol=1e-15)
        graded = self._cell("graded_independent_5", .75)
        graded_rows = simulate_e02_cell(self.config, graded, seed, force_initial=False)
        observed_disclosure = np.array([float(row["final_window_mean_disclosure"]) for row in graded_rows])
        expected_disclosure = m1.simulate(.75, levels=5, n=96, horizon=300, alpha=.1, temp=.25, lam=1, q0=0, seed=seed, final_window_fraction=.2)
        np.testing.assert_allclose(observed_disclosure, expected_disclosure, rtol=0, atol=1e-15)

    def test_forced_draw_order_and_matched_initial_potential_outcomes(self):
        binary = self._cell("binary_endpoints", .75); graded = self._cell("graded_independent_5", .75); seed = self._seed(binary)
        rng = np.random.default_rng(seed)
        sampled = (rng.random((96, 1)) > np.full((96, 2), .5).cumsum(axis=1)).sum(axis=1)
        uniforms = rng.random(96)
        left, right = simulate_e02_cell(self.config, binary, seed), simulate_e02_cell(self.config, graded, seed)
        self.assertEqual([int(row["initial_policy_action_index"]) for row in left], sampled.tolist())
        self.assertEqual([float(row["initial_acceptance_uniform"]) for row in left], uniforms.tolist())
        for a, b in zip(left, right, strict=True):
            self.assertEqual(a["initial_acceptance_uniform"], b["initial_acceptance_uniform"])
            self.assertEqual(a["initial_outcome"], b["initial_outcome"])
            self.assertEqual(a["initial_objective_reward"], b["initial_objective_reward"])
            self.assertEqual(a["initial_action_forced"], "True")
            self.assertEqual(b["initial_action_forced"], "True")

    def test_full_stream_common_potential_outcomes_and_shared_endpoint_actions(self):
        binary = self._cell("binary_endpoints", .75); graded = self._cell("graded_independent_5", .75); seed = self._seed(binary)
        _, left = simulate_e02_cell(self.config, binary, seed, capture_trace=True)
        _, right = simulate_e02_cell(self.config, graded, seed, capture_trace=True)
        np.testing.assert_array_equal(left["acceptance_uniforms"], right["acceptance_uniforms"])
        binary_disclosure = np.array([0., 1.])[left["actions"]]
        graded_disclosure = np.linspace(0., 1., 5)[right["actions"]]
        common_endpoint = (binary_disclosure == graded_disclosure) & np.isin(binary_disclosure, [0., 1.])
        self.assertGreater(np.count_nonzero(common_endpoint), 0)
        np.testing.assert_array_equal(left["accepts"][common_endpoint], right["accepts"][common_endpoint])
        np.testing.assert_array_equal(left["rewards"][common_endpoint], right["rewards"][common_endpoint])

    def test_selected_arm_update_counts_payoff_and_regret_reconcile(self):
        cell = self._cell("graded_independent_5", .85); rows = simulate_e02_cell(self.config, cell, self._seed(cell))
        for row in rows:
            counts = np.array(json.loads(row["total_action_counts_json"])); accepts = np.array(json.loads(row["total_accept_counts_json"])); rejects = np.array(json.loads(row["total_reject_counts_json"]))
            grid = np.array(json.loads(row["disclosure_grid_json"])); self.assertEqual(int(counts.sum()), 300); np.testing.assert_array_equal(counts, accepts + rejects)
            accepted_reward = .6 * grid - .25 * (1-grid) + 1; rejected_reward = .6 * grid - .25 * (1-grid) - 2
            self.assertAlmostEqual(float(row["cumulative_realized_objective_payoff"]), float((accepts * accepted_reward + rejects * rejected_reward).sum()))
            expected = m1.expected_reward(grid, .85)
            regret = ((max(.75, 1.15) - expected) * counts).sum()
            self.assertAlmostEqual(float(row["cumulative_objective_pseudo_regret"]), float(regret))
            q = np.array(json.loads(row["q_final_json"])); self.assertEqual(q.size, 5)

    def test_forced_selected_arm_only_update_and_noninteger_window(self):
        mini = dict(self.config); mini["n"] = 1; mini["T"] = 1
        cell = self._cell("graded_independent_5", .75)
        row = simulate_e02_cell(mini, cell, self._seed(cell))[0]
        q = np.array(json.loads(row["q_final_json"]))
        # At t=0 the forced d=1 arm alone learns; all independent intermediate
        # arms, including the policy-sampled one, retain their initial Q value.
        np.testing.assert_array_equal(q[:-1], np.zeros(4))
        self.assertAlmostEqual(q[-1], .1 * float(row["initial_objective_reward"]))
        fractional = dict(self.config); fractional["final_window_fraction"] = .205
        rows = simulate_e02_cell(fractional, self._cell("binary_endpoints", .75), self._seed(self._cell("binary_endpoints", .75)))
        self.assertEqual(rows[0]["final_window_start"], 238)

    def test_window_ties_censoring_and_intermediate_non_discovery_fields(self):
        rows = simulate_e02_cell(self.config, self._cell("graded_independent_5", .65), self._seed(self._cell("graded_independent_5", .65)))
        self.assertTrue(all(row["final_window_start"] == 240 and row["final_window_end"] == 299 for row in rows))
        for row in rows:
            final_counts = np.array(json.loads(row["final_window_action_counts_json"])); self.assertEqual(int(final_counts.sum()), 60)
            unique = int((final_counts == final_counts.max()).sum()) == 1
            self.assertEqual(row["final_window_unique_modal"], str(unique))
            if not unique: self.assertEqual(row["final_window_modal_action_index"], "")
            if row["time_to_stable_full_auth_modal_policy_censored"] == "True": self.assertEqual(row["time_to_stable_full_auth_modal_policy"], "")
        self.assertTrue(all(row["analytic_optimal_endpoint"] == 0 for row in rows))

    def test_synthetic_modal_tie_intermediate_and_stable_boundary_cases(self):
        self.assertIsNone(_unique_modal_index(np.array([10, 10])))
        self.assertEqual(_unique_modal_index(np.array([1, 2, 5, 9, 3])), 3)  # d=.75 is an intermediate modal arm.
        full_unique = np.zeros((10, 2), dtype=bool)
        full_unique[5:, 0] = True
        full_unique[8:, 1] = True
        np.testing.assert_array_equal(_stable_full_auth_times(full_unique, window=3), np.array([5, -1]))
        rng = np.random.default_rng(14)
        q_before = rng.normal(size=(19, 7, 5))
        # Force exact ties and a final-arm suffix to cover equality semantics.
        q_before[4, 2] = 0.0; q_before[10:, 3, -1] = 9.0
        full = (q_before[:, :, -1] == q_before.max(axis=2)) & ((q_before == q_before.max(axis=2, keepdims=True)).sum(axis=2) == 1)
        np.testing.assert_array_equal(_stable_full_auth_times(full, 5), _stable_full_auth_times_quadratic_reference(q_before, 5, 5))

    def test_rng_order_global_rng_and_cell_order_independence(self):
        cell = self._cell("binary_endpoints", .85); before = np.random.get_state(); first = simulate_e02_cell(self.config, cell, self._seed(cell)); after = np.random.get_state()
        self.assertEqual(before[0], after[0]); np.testing.assert_array_equal(before[1], after[1]); self.assertEqual(before[2:], after[2:])
        with tempfile.TemporaryDirectory() as directory:
            reordered = dict(self.config); reordered["cells"] = list(reversed(self.config["cells"])); path = Path(directory) / "reordered.json"; path.write_text(json.dumps(reordered))
            forward = run_e02_experiment(SMOKE, Path(directory) / "forward"); reverse = run_e02_experiment(path, Path(directory) / "reverse")
            for name in ("raw", "arms", "cells", "effects"): self.assertEqual(forward[name].read_bytes(), reverse[name].read_bytes())
            self.assertEqual(normalize_e02_machine_artifacts(forward), normalize_e02_machine_artifacts(reverse))

    def test_raw_summary_effect_recomputation_and_artifact_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            outputs = run_e02_experiment(SMOKE, Path(directory) / "result")
            with outputs["raw"].open(newline="") as handle:
                reader = csv.DictReader(handle); self.assertEqual(reader.fieldnames, E02_RAW_FIELDNAMES); raw = list(reader)
            self.assertEqual(len(raw), 576)
            cells, effects = recompute_e02_summaries(raw)
            with outputs["cells"].open(newline="") as handle: written_cells = list(csv.DictReader(handle))
            with outputs["effects"].open(newline="") as handle: written_effects = list(csv.DictReader(handle))
            self.assertEqual([{k: str(v) for k, v in row.items()} for row in cells], written_cells)
            self.assertEqual([{k: str(v) for k, v in row.items()} for row in effects], written_effects)
            self.assertEqual(len(written_cells), 18); self.assertEqual(len(written_effects), 192)
            with outputs["arms"].open(newline="") as handle:
                self.assertEqual(len(list(csv.DictReader(handle))), 15)
            self.assertTrue(outputs["figure"].stat().st_size > 1000)

    def test_provenance_hashes_report_and_fingerprint_are_independently_recomputable(self):
        with tempfile.TemporaryDirectory() as directory:
            outputs = run_e02_experiment(SMOKE, Path(directory) / "result")
            manifest = json.loads(outputs["manifest"].read_text())
            self.assertIsNotNone(manifest["environment"]["matplotlib"])
            normalized_config = json.dumps(manifest["parameters"], sort_keys=True, separators=(",", ":"))
            self.assertEqual(manifest["normalized_config"], normalized_config)
            self.assertEqual(manifest["config_sha256"], hashlib.sha256(normalized_config.encode()).hexdigest())
            self.assertEqual(manifest["git"]["source_fingerprint_sha256"], _source_fingerprint(ROOT))
            digest = hashlib.sha256()
            for relative in SOURCE_FINGERPRINT_PATHS:
                path = ROOT / relative; digest.update(relative.encode()); digest.update(path.read_bytes())
            self.assertEqual(manifest["git"]["source_fingerprint_sha256"], digest.hexdigest())
            porcelain = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"], check=True, capture_output=True, text=True).stdout.strip()
            diff = subprocess.run(["git", "-C", str(ROOT), "diff", "--no-ext-diff"], check=True, capture_output=True).stdout
            self.assertEqual(manifest["git"]["dirty"], bool(porcelain))
            self.assertEqual(manifest["git"]["porcelain_sha256"], hashlib.sha256(porcelain.encode()).hexdigest())
            self.assertEqual(manifest["git"]["dirty_diff_sha256"], hashlib.sha256(diff + porcelain.encode()).hexdigest())
            for name, detail in manifest["output_hashes"].items():
                self.assertEqual(detail["sha256"], hashlib.sha256(outputs[name].read_bytes()).hexdigest())
            report = outputs["report"].read_text()
            self.assertIn("13. **Pending Sol decision:**", report)
            self.assertIn("staged-standard projection", report)

    def test_synthetic_five_seed_student_t_interval(self):
        summaries = []
        for seed in range(5):
            for p in ("0.65", "0.75", "0.85"):
                for stratum in ("all", "accepted", "rejected"):
                    for architecture, offset in (("binary_endpoints", 0.0), ("graded_independent_5", .1 + seed * .01)):
                        summaries.append({"run_id": "r", "experiment_id": "E02", "tier": "standard", "master_seed": str(seed), "p": p, "architecture": architecture, "stratum": stratum,
                            "mean_any_disclosure_rate_post_initial": .2 + offset, "mean_full_authentic_rate_post_initial": .3 + offset, "mean_final_window_full_authentic_rate": .4 + offset,
                            "probability_final_window_optimal_endpoint_modal": .5 + offset, "mean_normalized_objective_pseudo_regret": .6 - offset, "mean_disclosure_rejection_rate_per_post_initial_step": .7 - offset,
                            "probability_stable_full_auth_modal_policy": .8 + offset, "mean_final_window_mean_disclosure": .9 + offset})
        effects = _e02_effects(summaries)
        target = next(row for row in effects if row["level"] == "across_master_seeds" and row["effect_name"] == EFFECT_NAMES[0] and row["p"] == "0.75" and row["stratum"] == "all")
        values = np.array([seed * .01 for seed in range(5)])
        half = T_CRITICAL_95_DF4 * values.std(ddof=1) / np.sqrt(5)
        self.assertAlmostEqual(float(target["estimate"]), values.mean())
        self.assertAlmostEqual(float(target["ci_low"]), values.mean() - half)
        self.assertAlmostEqual(float(target["ci_high"]), values.mean() + half)


if __name__ == "__main__":
    unittest.main()
