import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from gifted_masking.experiments.article import (
    E01_RAW_FIELDNAMES,
    canonical_e01_cell_id,
    derive_e01_component_seeds,
    load_article_config,
    normalize_machine_artifacts,
    recompute_e01_summaries,
    run_article_experiment,
    simulate_e01_cell,
    _checkpoint_report,
)
from gifted_masking.models import m0


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "configs" / "frontiers_article" / "e01_hot_stove_smoke.json"


class ArticleE01Tests(unittest.TestCase):
    def setUp(self):
        self.config = load_article_config(CONFIG_PATH)

    def test_config_is_frozen_smoke_contract(self):
        self.assertEqual(self.config["run_id"], "frontiers_hot_stove_v1_smoke")
        self.assertEqual(len(self.config["cells"]), 10)
        self.assertEqual(self.config["n"], 96)
        self.assertEqual(self.config["T"], 300)
        self.assertEqual(self.config["workers"], 1)
        with self.assertRaises(ValueError):
            load_article_config(CONFIG_PATH, overrides={"workers": 2})
        for key, value in (("n", 95), ("T", 299), ("final_window_fraction", .25), ("master_seed", 1)):
            with self.assertRaises(ValueError):
                load_article_config(CONFIG_PATH, overrides={key: value})
        mutated = dict(self.config); mutated["cells"] = self.config["cells"][:-1]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"; path.write_text(json.dumps(mutated))
            with self.assertRaises(ValueError): load_article_config(path)
            for mutation in ({"payoffs": {"b": 1.1, "a": .6, "c": .25, "r": 2.0}}, {"cells": [{"p": .70, "lambda": 1.0, "condition": "controlled_baseline"}] * 10}):
                invalid = dict(self.config); invalid.update(mutation); path.write_text(json.dumps(invalid))
                with self.assertRaises(ValueError): load_article_config(path)

    def test_baseline_cell_matches_m0_exactly(self):
        cell = next(cell for cell in self.config["cells"] if cell["condition"] == "maintained_baseline" and cell["lambda"] == 0.5)
        cell_id = canonical_e01_cell_id(self.config, cell)
        policy_seed, _ = derive_e01_component_seeds(self.config["master_seed"], cell_id)
        rows = simulate_e01_cell(self.config, cell, cell_id, policy_seed, intervention_seed=0)
        observed = np.array([float(row["final_window_mask_rate"]) for row in rows])
        expected = m0.simulate(
            cell["p"], b=1.0, a=0.6, c=0.25, r=2.0, n=96, horizon=300,
            alpha=0.1, temp=0.25, lam=0.5, q0=0.0, seed=policy_seed,
            final_window_fraction=0.2,
        )
        np.testing.assert_array_equal(observed, expected)

    def test_forced_initial_and_interventions_preserve_objective_semantics(self):
        baseline = next(cell for cell in self.config["cells"] if cell["condition"] == "controlled_baseline" and cell["p"] == 0.75)
        forced = next(cell for cell in self.config["cells"] if cell["condition"] == "forced_authentic_0.05" and cell["p"] == 0.75)
        counterfactual = next(cell for cell in self.config["cells"] if cell["condition"] == "counterfactual_authentic_feedback" and cell["p"] == 0.75)
        for cell in (baseline, forced, counterfactual):
            cell_id = canonical_e01_cell_id(self.config, cell)
            policy_seed, intervention_seed = derive_e01_component_seeds(self.config["master_seed"], cell_id)
            rows = simulate_e01_cell(self.config, cell, cell_id, policy_seed, intervention_seed)
            self.assertTrue(all(row["initial_action_forced"] == "True" for row in rows))
            self.assertTrue(all(float(row["initial_objective_reward"]) in {1.6, -1.4} for row in rows))
        forced_rows = simulate_e01_cell(self.config, forced, canonical_e01_cell_id(self.config, forced), *derive_e01_component_seeds(self.config["master_seed"], canonical_e01_cell_id(self.config, forced)))
        self.assertGreater(sum(int(row["forced_override_count"]) for row in forced_rows), 0)
        counter_rows = simulate_e01_cell(self.config, counterfactual, canonical_e01_cell_id(self.config, counterfactual), *derive_e01_component_seeds(self.config["master_seed"], canonical_e01_cell_id(self.config, counterfactual)))
        self.assertGreater(sum(int(row["counterfactual_feedback_count"]) for row in counter_rows), 0)
        self.assertTrue(all(int(row["counterfactual_feedback_count"]) == int(row["counterfactual_auth_accept_count"]) + int(row["counterfactual_auth_reject_count"]) for row in counter_rows))
        self.assertTrue(all(np.isclose(float(row["counterfactual_auth_reward_sum"]), 1.6 * int(row["counterfactual_auth_accept_count"]) - 1.4 * int(row["counterfactual_auth_reject_count"])) for row in counter_rows))
        self.assertTrue(all(float(row["cumulative_realized_objective_payoff"]) != float(row["counterfactual_auth_reward_sum"]) for row in counter_rows))

    def test_seed_derivation_is_canonical_and_cell_order_independent(self):
        cells = list(self.config["cells"])
        forward = {canonical_e01_cell_id(self.config, cell): derive_e01_component_seeds(self.config["master_seed"], canonical_e01_cell_id(self.config, cell)) for cell in cells}
        reverse = {canonical_e01_cell_id(self.config, cell): derive_e01_component_seeds(self.config["master_seed"], canonical_e01_cell_id(self.config, cell)) for cell in reversed(cells)}
        self.assertEqual(forward, reverse)
        self.assertEqual(len(set(forward.values())), len(cells))

    def test_cell_reordering_preserves_machine_readable_results(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reversed_config = dict(self.config)
            reversed_config["cells"] = list(reversed(self.config["cells"]))
            reversed_path = root / "reordered.json"
            reversed_path.write_text(json.dumps(reversed_config))
            forward = run_article_experiment(CONFIG_PATH, output_dir=root / "forward")
            reverse = run_article_experiment(reversed_path, output_dir=root / "reverse")
            for name in ("raw", "cells", "effects"):
                self.assertEqual(forward[name].read_bytes(), reverse[name].read_bytes())

    def test_global_numpy_rng_is_not_used_and_final_window_uses_ceiling(self):
        cell = self.config["cells"][0]
        cell_id = canonical_e01_cell_id(self.config, cell)
        np.random.seed(9842)
        before = np.random.get_state()
        rows = simulate_e01_cell(self.config, cell, cell_id, *derive_e01_component_seeds(self.config["master_seed"], cell_id))
        after = np.random.get_state()
        self.assertEqual(before[0], after[0])
        np.testing.assert_array_equal(before[1], after[1])
        self.assertEqual(before[2:], after[2:])
        noninteger = dict(self.config)
        noninteger["final_window_fraction"] = 0.205
        noninteger_cell_id = canonical_e01_cell_id(noninteger, cell)
        noninteger_rows = simulate_e01_cell(noninteger, cell, noninteger_cell_id, *derive_e01_component_seeds(noninteger["master_seed"], noninteger_cell_id))
        self.assertEqual(rows[0]["final_window_start"], 240)
        self.assertEqual(rows[0]["final_window_end"], 299)
        self.assertEqual(noninteger_rows[0]["final_window_start"], 238)

    def test_raw_schema_and_recomputed_summaries(self):
        with tempfile.TemporaryDirectory() as directory:
            outputs = run_article_experiment(CONFIG_PATH, output_dir=Path(directory) / "results")
            with outputs["raw"].open(newline="") as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(reader.fieldnames, E01_RAW_FIELDNAMES)
                rows = list(reader)
            self.assertEqual(len(rows), 960)
            cells, effects = recompute_e01_summaries(rows)
            with outputs["cells"].open(newline="") as handle:
                written_cells = list(csv.DictReader(handle))
            with outputs["effects"].open(newline="") as handle:
                written_effects = list(csv.DictReader(handle))
            self.assertEqual([{key: str(value) for key, value in row.items()} for row in cells], written_cells)
            self.assertEqual([{key: str(value) for key, value in row.items()} for row in effects], written_effects)

    def test_normalized_reruns_match_and_manifest_is_complete(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = run_article_experiment(CONFIG_PATH, output_dir=root / "first")
            second = run_article_experiment(CONFIG_PATH, output_dir=root / "second")
            self.assertEqual(normalize_machine_artifacts(first), normalize_machine_artifacts(second))
            manifest = json.loads(first["manifest"].read_text())
            self.assertEqual(manifest["seed_hierarchy"]["rng_order"], "policy draw, acceptance draw, reward, Q update")
            self.assertEqual(manifest["outputs"]["raw"]["rows"], 960)
            self.assertNotIn("manifest", manifest["output_hashes"])
            self.assertTrue(manifest["git"]["source_fingerprint_sha256"])
            self.assertIsNotNone(manifest["environment"]["matplotlib"])
            for name, detail in manifest["output_hashes"].items():
                self.assertEqual(detail["sha256"], hashlib.sha256(first[name].read_bytes()).hexdigest())
            digest = hashlib.sha256()
            for relative in ("src/gifted_masking/experiments/article.py", "src/gifted_masking/cli.py", "configs/frontiers_article", "tests/test_article_e01.py"):
                target = REPO_ROOT / relative
                for path in sorted(target.rglob("*") if target.is_dir() else [target]):
                    if path.is_file(): digest.update(str(path.relative_to(REPO_ROOT)).encode()); digest.update(path.read_bytes())
            self.assertEqual(manifest["git"]["source_fingerprint_sha256"], digest.hexdigest())

    def test_pooled_effects_and_nonblank_figure(self):
        with tempfile.TemporaryDirectory() as directory:
            outputs = run_article_experiment(CONFIG_PATH, output_dir=Path(directory) / "results")
            effects = list(csv.DictReader(outputs["effects"].open()))
            pooled = next(row for row in effects if row["effect_name"] == "rejected_minus_accepted_final_mask_rate" and row["p"] == "pooled_equal_weight_p_0.75_0.85" and row["level"] == "master_seed")
            by_p = [float(row["estimate"]) for row in effects if row["effect_name"] == "rejected_minus_accepted_final_mask_rate" and row["p"] in {"0.75", "0.85"} and row["level"] == "master_seed"]
            self.assertAlmostEqual(float(pooled["estimate"]), sum(by_p) / 2.0)
            import matplotlib.image as image
            pixels = image.imread(outputs["figure"])
            blue = np.array([68, 119, 170]) / 255.0
            red = np.array([204, 102, 119]) / 255.0
            self.assertGreater(np.count_nonzero(np.all(np.isclose(pixels[..., :3], blue, atol=.02), axis=-1)), 100)
            self.assertGreater(np.count_nonzero(np.all(np.isclose(pixels[..., :3], red, atol=.02), axis=-1)), 100)

    def test_standard_config_is_not_executable(self):
        standard = REPO_ROOT / "configs" / "frontiers_article" / "e01_hot_stove_standard.json"
        with self.assertRaises(PermissionError):
            run_article_experiment(standard, output_dir=Path(tempfile.gettempdir()) / "e01_forbidden")
        frozen = load_article_config(standard)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad_standard.json"
            for key, value in (("n", 5), ("master_seeds", [2026081101])):
                invalid = dict(frozen); invalid[key] = value; path.write_text(json.dumps(invalid))
                with self.assertRaises(ValueError): load_article_config(path)

    def test_report_wording_is_tier_aware(self):
        paths = {"manifest": Path("manifest.json"), "raw": Path("raw.csv"), "cells": Path("cells.csv"), "effects": Path("effects.csv"), "figure": Path("figure.png"), "report": Path("report.md")}
        smoke = _checkpoint_report(self.config, paths, .1, [], 960)
        standard = load_article_config(REPO_ROOT / "configs/frontiers_article/e01_hot_stove_standard.json")
        standard_report = _checkpoint_report(standard, paths, 1.0, [], 25000, verification="passed")
        self.assertIn("implementation/smoke", smoke); self.assertIn("smoke results", smoke); self.assertIn("no standard or sensitivity", smoke)
        self.assertIn("Pass D standard", standard_report); self.assertIn("standard results await", standard_report); self.assertIn("authorized standard run executed", standard_report)
        self.assertNotIn("implementation/smoke", standard_report); self.assertNotIn("smoke results", standard_report); self.assertNotIn("no standard or sensitivity run was executed", standard_report)


if __name__ == "__main__":
    unittest.main()
