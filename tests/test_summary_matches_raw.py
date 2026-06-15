import csv
import tempfile
import unittest
from pathlib import Path

from gifted_masking.experiments.robustness import write_suite
from scripts.compute_headline_uncertainty import compute_headline_uncertainty
from scripts.recompute_headline_effects import recompute_headline_effects


class SummaryMatchesRawTests(unittest.TestCase):
    def test_summary_values_recompute_from_primary_raw_units(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            outputs = write_suite(Path(tmp_dir), suite="full")
            recomputed_path = Path(tmp_dir) / "summaries" / "recomputed.csv"
            rows = recompute_headline_effects(
                Path(outputs["primary_raw"]),
                Path(outputs["summary"]),
                recomputed_path,
            )
        self.assertTrue(rows)
        self.assertTrue(all(row["match"] for row in rows))

    def test_uncertainty_file_is_computed_from_primary_raw_units(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            outputs = write_suite(Path(tmp_dir), suite="full")
            uncertainty_path = Path(tmp_dir) / "summaries" / "uncertainty.csv"
            rows = compute_headline_uncertainty(Path(outputs["primary_raw"]), uncertainty_path)
            with uncertainty_path.open(newline="") as handle:
                written_rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), len(written_rows))
        self.assertTrue(all(row["n_units"] for row in written_rows))


if __name__ == "__main__":
    unittest.main()
