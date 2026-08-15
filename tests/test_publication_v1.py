"""Deterministic tests for the Article-V1 Stage-1 publication layer.

These tests never invoke a simulation, an experiment runner, or any stochastic
entry point. They verify that the publication build reads the frozen E01-E05
artifacts unchanged, keeps its selectors pinned, enforces the frozen scientific
invariants, stays inside the Article-V1 scope, and reproduces its recorded
output hashes.
"""

from __future__ import annotations

import ast
import json
import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PUB_ROOT = REPO_ROOT / "projects" / "frontiers_article" / "publication_v1"
sys.path.insert(0, str(PUB_ROOT / "scripts"))

import analytic  # noqa: E402
import extract  # noqa: E402
import pubcommon  # noqa: E402
from pubcommon import (  # noqa: E402
    FAMILIES,
    PublicationAssertionError,
    read_rows,
    sha256_file,
    verify_evidence_matrix,
    verify_frozen_family,
)

DATA = PUB_ROOT / "data"


def _docstring_nodes(tree: ast.AST) -> set[int]:
    """Ids of the string nodes that serve as module/class/function docstrings."""
    ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                if isinstance(body[0].value.value, str):
                    ids.add(id(body[0].value))
    return ids


def _code_strings(tree: ast.AST) -> list[str]:
    """Every string literal in a module except its docstrings."""
    skip = _docstring_nodes(tree)
    return [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in skip
    ]


def _imported_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
    return names


class FrozenEvidenceTest(unittest.TestCase):
    def test_all_protected_outputs_hash_match(self) -> None:
        total = valid = 0
        for experiment in FAMILIES:
            record = verify_frozen_family(experiment)
            self.assertEqual(record["status"], "PASS", experiment)
            total += record["protected_output_count"]
            valid += record["protected_outputs_valid"]
        self.assertEqual((valid, total), (33, 33))

    def test_evidence_matrix_referenced_files_hash_match(self) -> None:
        record = verify_evidence_matrix()
        self.assertEqual(record["status"], "PASS")
        self.assertEqual(record["referenced_files_valid"], record["referenced_file_count"])
        # 15 files referenced by the 29 frozen claim adjudications, plus three
        # further frozen summaries brought in by the four Stage-1 series rows.
        self.assertEqual(record["referenced_file_count"], 18)

    def test_series_rows_did_not_alter_existing_adjudications(self) -> None:
        rows = read_rows(REPO_ROOT / "projects/frontiers_article/ARTICLE_V1_EVIDENCE_MATRIX.csv")
        self.assertEqual(len(rows), 33)
        series = [r for r in rows if "-S1-" in r["claim_id"]]
        self.assertEqual(len(series), 4)
        self.assertEqual(
            sorted(r["claim_id"] for r in series),
            ["E02-S1-ARM-REWARDS", "E03-S1-GRID-MAP", "E04-S1-K-RESPONSE", "E05-S1-BF-RESPONSE"],
        )
        for row in series:
            self.assertIn("publication display series", row["evidence_class"])
            self.assertTrue(row["figure_or_table_target"].startswith("Figure "))
            self.assertIn("x field=", row["selector"])
            self.assertIn("y field=", row["selector"])

    def test_scope_excludes_e06_and_m4(self) -> None:
        self.assertNotIn("E06", FAMILIES)
        self.assertNotIn("M4", FAMILIES)
        self.assertEqual(sorted(FAMILIES), ["E01", "E02", "E03", "E04", "E05"])


class E01ExtractionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = {r["role"]: r for r in read_rows(DATA / "e01_primary_effects.csv")}

    def test_selector_is_pinned(self) -> None:
        for row in self.rows.values():
            self.assertEqual(row["level"], "across_master_seeds")
            self.assertEqual(row["p_selector"], "pooled_equal_weight_p_0.75_0.85")

    def test_frozen_headline_values(self) -> None:
        self.assertAlmostEqual(float(self.rows["primary"]["estimate"]), -0.02583704230615776, places=12)
        self.assertAlmostEqual(
            float(self.rows["linked_unit_translation"]["estimate"]), 0.025824123785003948, places=12
        )
        self.assertAlmostEqual(
            float(self.rows["secondary_null"]["estimate"]), -0.0003432658754774054, places=12
        )

    def test_regret_is_the_sampling_estimand_rescaled(self) -> None:
        sampling = float(self.rows["primary"]["estimate"])
        regret = float(self.rows["linked_unit_translation"]["estimate"])
        self.assertAlmostEqual(regret, -(1999 / 2000) * sampling, places=9)

    def test_final_mask_interval_spans_zero(self) -> None:
        row = self.rows["secondary_null"]
        self.assertEqual(row["interval_spans_zero"], "True")
        self.assertLess(float(row["ci_low"]), 0.0)
        self.assertGreater(float(row["ci_high"]), 0.0)


class E02ExtractionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = {r["claim_id"]: r for r in read_rows(DATA / "e02_primary_effects.csv")}

    def test_every_row_is_the_rejected_stratum(self) -> None:
        self.assertTrue(self.rows)
        for row in self.rows.values():
            self.assertEqual(row["stratum"], "rejected")
            self.assertEqual(row["p_selector"], "pooled_equal_weight_p_0.75_0.85")

    def test_frozen_headline_values(self) -> None:
        self.assertAlmostEqual(float(self.rows["E02-C4-EXPLORATION"]["estimate"]), 0.25504040052777677, places=12)
        self.assertAlmostEqual(float(self.rows["E02-C4-FULL-ENDPOINT"]["estimate"]), -0.3286922325725828, places=12)
        self.assertAlmostEqual(float(self.rows["E02-C4-MODAL"]["estimate"]), -0.22173959296185813, places=12)
        self.assertAlmostEqual(float(self.rows["E02-C4-REGRET"]["estimate"]), -0.029761004211474734, places=12)

    def test_exploration_is_never_shown_without_the_adverse_results(self) -> None:
        roles = [r["role"] for r in self.rows.values()]
        self.assertIn("primary", roles)
        self.assertEqual(sum(role.startswith("adverse") for role in roles), 3)

    def test_a_non_rejected_stratum_selector_fails_closed(self) -> None:
        with self.assertRaises(PublicationAssertionError):
            extract._one(
                read_rows(pubcommon.SUMMARIES / "frontiers_m1_binary_graded_v1_effects.csv"),
                "wrong stratum",
                effect_name="graded_any_minus_binary_full_post_initial_rate",
                level="across_master_seeds",
                p="pooled_equal_weight_p_0.75_0.85",
                stratum="not_a_stratum",
            )

    def test_arm_expected_rewards_match_the_affine_closed_form(self) -> None:
        for row in read_rows(DATA / "e02_arm_expected_rewards.csv"):
            p, d = float(row["p"]), float(row["d"])
            expected = (1.0 - 0.25) + d * (0.6 + 0.25 - (1.0 - p) * (1.0 + 2.0))
            self.assertAlmostEqual(float(row["expected_reward"]), expected, places=12)


class E03ExtractionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = read_rows(DATA / "e03_grid_map.csv")
        self.summary = {r["publication_category"]: int(r["cell_count"]) for r in read_rows(DATA / "e03_grid_summary.csv")}

    def test_tested_grid_size(self) -> None:
        self.assertEqual(len(self.rows), 357)
        self.assertEqual(len({r["parameter_cell_id"] for r in self.rows}), 357)
        self.assertEqual(len({r["p"] for r in self.rows}), 21)
        self.assertEqual(len({r["eta"] for r in self.rows}), 17)

    def test_learned_suboptimal_masking_count(self) -> None:
        self.assertEqual(self.summary["learned_suboptimal_masking"], 243)

    def test_inconclusive_cells_remain_represented(self) -> None:
        self.assertEqual(self.summary["inconclusive"], 7)
        self.assertGreater(self.summary["inconclusive"], 0)

    def test_categories_partition_the_tested_grid(self) -> None:
        self.assertEqual(sum(self.summary.values()), 357)

    def test_objective_action_is_carried_for_every_cell(self) -> None:
        for row in self.rows:
            self.assertIn(row["objective_neutral_action"], {"authentic", "mask"})

    def test_contrast_cells_have_an_objectively_authentic_optimum(self) -> None:
        contrast = [r for r in self.rows if r["publication_category"] == "learned_suboptimal_masking"]
        self.assertEqual(len(contrast), 243)
        for row in contrast:
            self.assertEqual(row["objective_neutral_action"], "authentic")
            self.assertEqual(row["learned_neutral_action"], "mask")
            self.assertGreater(float(row["objective_neutral_q_gap_auth_minus_mask"]), 0.0)


class E04ExtractionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.curves = read_rows(DATA / "e04_k_response.csv")
        self.effects = {r["claim_id"]: r for r in read_rows(DATA / "e04_headline_effects.csv")}

    def test_primary_response_field_is_not_substituted(self) -> None:
        self.assertEqual(extract.E04_RESPONSE, "mean_settled_any_good_auth_argmax")
        for row in self.curves:
            self.assertEqual(row["response_metric"], "mean_settled_any_good_auth_argmax")
        for row in self.effects.values():
            self.assertEqual(row["response_metric"], "mean_settled_any_good_auth_argmax")

    def test_both_frozen_headline_effects_exist(self) -> None:
        self.assertEqual(
            self.effects["E04-C6-FLAT"]["effect_name"],
            "flat_2k_mean_settled_any_good_auth_argmax_S16_minus_S1_fixed_one",
        )
        self.assertEqual(
            self.effects["E04-C6-HIER"]["effect_name"],
            "hierarchical_mean_settled_any_good_auth_argmax_S16_minus_S1_fixed_one",
        )
        self.assertAlmostEqual(float(self.effects["E04-C6-FLAT"]["estimate"]), -0.234, places=9)
        self.assertAlmostEqual(float(self.effects["E04-C6-HIER"]["estimate"]), -0.4704, places=9)

    def test_priority_controls_are_present(self) -> None:
        for claim_id in (
            "E04-C6-CONTROL-KNOWNGOOD",
            "E04-C6-CONTROL-GLOBALMASK",
            "E04-C6-CONTROL-PROP25-FLAT",
            "E04-C6-CONTROL-PROP25-HIER",
        ):
            self.assertIn(claim_id, self.effects)

    def test_proportional_25_regime_matches_the_frozen_definition(self) -> None:
        for row in self.curves:
            if row["series"] == "proportional_25":
                k = int(row["K"])
                self.assertEqual(int(row["effective_good_count"]), max(1, math.ceil(k / 4)))

    def test_master_range_brackets_the_mean(self) -> None:
        for row in self.curves:
            self.assertLessEqual(float(row["master_min"]), float(row["master_mean"]))
            self.assertLessEqual(float(row["master_mean"]), float(row["master_max"]))
            self.assertEqual(int(row["n_master_seeds"]), 5)


class E05ExtractionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.crossings = {r["architecture"]: r for r in read_rows(DATA / "e05_crossings.csv")}
        self.displacement = {r["quantity"]: r for r in read_rows(DATA / "e05_displacement.csv")}
        self.response = read_rows(DATA / "e05_response_vs_bf.csv")

    def test_learned_flat_crossing(self) -> None:
        flat = self.crossings["flat_2k"]
        self.assertEqual(flat["transition_status"], "valid")
        self.assertAlmostEqual(float(flat["transition_bf"]), 0.31285211267605634, places=12)
        self.assertAlmostEqual(float(flat["ci_low"]), 0.3078358208955224, places=12)
        self.assertAlmostEqual(float(flat["ci_high"]), 0.3169178027050235, places=12)

    def test_objective_crossing_is_exactly_eight_seventeenths(self) -> None:
        self.assertEqual(
            float(self.crossings["flat_2k"]["analytic_threshold_bf"]), float(Fraction(8, 17))
        )

    def test_hierarchical_has_no_in_range_crossing(self) -> None:
        hier = self.crossings["hierarchical"]
        self.assertEqual(hier["transition_status"], "no_crossing_below")
        self.assertEqual(hier["transition_bf"], "")
        self.assertEqual(hier["decision_eligible"], "False")
        self.assertEqual(int(hier["bootstrap_valid_crossings"]), 0)
        self.assertIn("left-censored", hier["censoring_note"].lower())

    def test_displacement_and_advantage(self) -> None:
        self.assertAlmostEqual(
            abs(float(self.displacement["displacement_objective_minus_learned"]["value"])),
            0.1577361226180613,
            places=9,
        )
        self.assertAlmostEqual(
            float(self.displacement["objective_advantage_at_learned_crossing"]["value"]),
            0.13407570422535212,
            places=9,
        )

    def test_pooled_response_reproduces_the_frozen_dense_boundary(self) -> None:
        frozen = {
            r["architecture"]: r
            for r in read_rows(pubcommon.SUMMARIES / "frontiers_m3_bflpe_crossover_v1_transitions.csv")
            if r["level"] == "across_master_seeds"
        }
        for architecture, row in frozen.items():
            match = [
                r
                for r in self.response
                if r["architecture"] == architecture
                and math.isclose(float(r["bf"]), float(row["dense_bf_min"]), abs_tol=1e-12)
            ]
            self.assertEqual(len(match), 1)
            self.assertAlmostEqual(
                float(match[0]["pooled_response"]), float(row["raw_dense_start_response"]), places=12
            )


class AnalyticTableTest(unittest.TestCase):
    def test_closed_forms_hold(self) -> None:
        rows = analytic.build_rows()
        self.assertTrue(rows)
        by_id = {r["result_id"]: r for r in rows}
        self.assertEqual(by_id["M0.2"]["exact_value"], "43/60")
        self.assertEqual(by_id["M3.2"]["exact_value"], "8/17")
        self.assertEqual(by_id["M0.2"]["label"], "Static M0 objective boundary")
        self.assertIn("not the M2 dynamic threshold", by_id["M0.2"]["interpretation"])

    def test_m0_boundary(self) -> None:
        self.assertAlmostEqual(analytic._delta0(float(Fraction(43, 60))), 0.0, places=12)

    def test_m1_is_affine_and_endpoint_optimal(self) -> None:
        for p in (0.65, 0.75, 0.85):
            values = [analytic._m1_expected_reward(d / 20.0, p) for d in range(21)]
            seconds = [values[i + 2] - 2 * values[i + 1] + values[i] for i in range(len(values) - 2)]
            self.assertTrue(all(abs(s) < 1e-12 for s in seconds))
            self.assertAlmostEqual(max(values), max(values[0], values[-1]), places=12)

    def test_m3_k_invariance_and_crossover(self) -> None:
        mask, good, bad = analytic._m3_rewards(0.0)
        self.assertAlmostEqual(good, 1.15, places=12)
        self.assertAlmostEqual(mask, 0.75, places=12)
        self.assertAlmostEqual(bad, -0.80, places=12)
        # K changes multiplicity only; the distinct reward set and its max are fixed.
        self.assertAlmostEqual(max(mask, good, bad), 1.15, places=12)
        mask_star, good_star, _ = analytic._m3_rewards(float(Fraction(8, 17)))
        self.assertAlmostEqual(mask_star, good_star, places=12)


class PublicationGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        manifest_path = PUB_ROOT / "manifests" / "publication_v1_manifest.json"
        self.assertTrue(manifest_path.exists(), "run build_publication_v1.py first")
        self.manifest = json.loads(manifest_path.read_text())

    def test_recorded_output_hashes_still_hold(self) -> None:
        checked = 0
        for group in self.manifest["outputs"].values():
            for entry in group:
                path = REPO_ROOT / entry["path"]
                self.assertTrue(path.exists(), entry["path"])
                self.assertEqual(sha256_file(path), entry["sha256"], entry["path"])
                checked += 1
        self.assertGreater(checked, 0)

    def test_no_e06_or_m4_artifact_feeds_the_publication_graph(self) -> None:
        for record in self.manifest["publication_source_data"]:
            self.assertIn(record["source_experiment"], {"E01", "E02", "E03", "E04", "E05"})
            for source in record["sources"]:
                name = Path(source["path"]).name.lower()
                self.assertNotIn("e06", name)
                self.assertNotIn("m4", name)
                # A source is either a frozen summary artifact or an earlier
                # publication-source CSV built in this same package.
                self.assertTrue(
                    source["path"].startswith("results/summaries/")
                    or source["path"].startswith("projects/frontiers_article/publication_v1/data/"),
                    source["path"],
                )

    def test_no_publication_source_reads_raw_results(self) -> None:
        for record in self.manifest["publication_source_data"]:
            for source in record["sources"]:
                self.assertNotIn("results/raw/", source["path"])

    def test_figures_read_only_from_the_publication_data_directory(self) -> None:
        # Judge executable content only: prose in docstrings legitimately names
        # the directories the figures are forbidden to read.
        tree = ast.parse((PUB_ROOT / "scripts" / "figures.py").read_text())
        for forbidden in ("results/raw", "results/summaries", "legacy_figures"):
            self.assertFalse(
                any(forbidden in text for text in _code_strings(tree)),
                f"{forbidden!r} referenced in figures.py code",
            )
        imported = _imported_names(tree)
        self.assertNotIn("SUMMARIES", imported)
        self.assertIn("DATA_DIR", imported)

    def test_build_never_imports_an_experiment_runner(self) -> None:
        for script in sorted((PUB_ROOT / "scripts").glob("*.py")):
            source = script.read_text()
            for forbidden in ("gifted_masking.experiments", "gifted_masking.cli", "from gifted_masking"):
                self.assertNotIn(forbidden, source, script.name)

    def test_declared_transformations_are_all_permitted(self) -> None:
        permitted = {
            "row_filter",
            "column_projection",
            "deterministic_join",
            "equal_weight_master_mean",
            "master_range",
            "count_aggregation",
            "closed_form_analytic",
            "rounding_for_display",
        }
        for record in self.manifest["publication_source_data"]:
            self.assertTrue(record["transformation"])
            self.assertTrue(set(record["transformation"]) <= permitted, record["output_file"])


if __name__ == "__main__":
    unittest.main()
