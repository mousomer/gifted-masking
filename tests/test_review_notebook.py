"""Bounded checks for the review notebook and its helper module (no kernel, no pandas)."""

from __future__ import annotations

import ast
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "review_and_research.ipynb"
sys.path.insert(0, str(ROOT / "notebooks"))

import review_lib  # noqa: E402


class ReviewNotebookTests(unittest.TestCase):
    def test_notebook_is_valid_json_with_compilable_code_cells(self) -> None:
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        self.assertEqual(notebook["nbformat"], 4)
        self.assertEqual(notebook["metadata"]["kernelspec"]["name"], "venv314")
        code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
        self.assertGreater(len(code_cells), 20)
        for index, cell in enumerate(code_cells):
            self.assertEqual(cell.get("outputs", []), [], f"code cell {index} is committed with outputs")
            ast.parse("".join(cell["source"]), filename=f"cell-{index}")

    def test_catalog_covers_every_test_file(self) -> None:
        catalog = review_lib.catalog_tests(ROOT / "tests")
        files = {row["file"] for row in catalog}
        on_disk = {path.name for path in (ROOT / "tests").glob("test_*.py")}
        self.assertEqual(files, on_disk)
        self.assertIn("test_review_notebook.py", files)
        self.assertTrue(all(str(row["test"]).startswith("test") for row in catalog))

    def test_fast_test_files_exist(self) -> None:
        for name in review_lib.FAST_TEST_FILES:
            self.assertTrue((ROOT / "tests" / name).is_file(), name)

    def test_check_row_semantics(self) -> None:
        self.assertTrue(review_lib.check("close", 0.1 + 0.2, 0.3, tol=1e-12)["passed"])
        self.assertFalse(review_lib.check("far", 0.31, 0.3, tol=1e-6)["passed"])
        self.assertTrue(review_lib.check("tuple", (0.75, 0), (0.75, 0))["passed"])
        self.assertFalse(review_lib.check("bool", False, True)["passed"])

    def test_manifest_hash_verification_detects_match_mismatch_and_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = root / "good.csv"
            good.write_text("a,b\n1,2\n", encoding="utf-8")
            bad = root / "bad.csv"
            bad.write_text("changed\n", encoding="utf-8")
            manifest = {
                "run_id": "synthetic",
                "outputs": {key: {"path": f"{key}.csv"} for key in ("good", "bad", "gone")},
                "output_hashes": {
                    "good": {"sha256": hashlib.sha256(good.read_bytes()).hexdigest(), "bytes": good.stat().st_size},
                    "bad": {"sha256": "0" * 64, "bytes": bad.stat().st_size},
                    "gone": {"sha256": "0" * 64, "bytes": 1},
                },
            }
            status = {row["output"]: row["status"] for row in review_lib.verify_manifest_hashes(manifest, root)}
        self.assertEqual(status, {"good": "match", "bad": "MISMATCH", "gone": "missing"})

    def test_replicate_reports_between_seed_spread(self) -> None:
        summary = review_lib.replicate(lambda seed, offset: [seed + offset], [0, 1, 2], offset=1.0)
        self.assertEqual(summary["mean"], 2.0)
        self.assertEqual(summary["n_seeds"], 3)
        self.assertAlmostEqual(summary["se_between_seeds"], 1.0 / 3 ** 0.5)


if __name__ == "__main__":
    unittest.main()
