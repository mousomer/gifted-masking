import csv
import tempfile
import unittest
from pathlib import Path

from gifted_masking.experiments.robustness import RAW_FIELDNAMES, write_suite


class PrimaryRawSchemaTests(unittest.TestCase):
    def test_primary_raw_schema_and_granularity(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            outputs = write_suite(Path(tmp_dir), suite="full")
            primary_raw = Path(outputs["primary_raw"])
            legacy_raw = Path(outputs["raw"])
            with primary_raw.open(newline="") as handle:
                rows = list(csv.DictReader(handle))
            with legacy_raw.open(newline="") as handle:
                legacy_rows = list(csv.DictReader(handle))

        self.assertTrue(primary_raw.name.endswith("_units.csv"))
        self.assertTrue(set(RAW_FIELDNAMES).issubset(rows[0].keys()))
        self.assertGreater(len(rows), len(legacy_rows))
        self.assertEqual({"M0", "M1", "M2", "M3", "M4"}, {row["model"] for row in rows})
        self.assertTrue({"flat_2k", "hierarchical", "global_mask", "fixed_good_pond"}.issubset({row["formulation"] for row in rows}))
        self.assertTrue({"up", "down"}.issubset({row["path_direction"] for row in rows if row["model"] == "M4"}))
        self.assertTrue(all(row["unit_id"] != "" for row in rows))
        self.assertTrue(all(row["cell_seed"] != "" for row in rows))


if __name__ == "__main__":
    unittest.main()
