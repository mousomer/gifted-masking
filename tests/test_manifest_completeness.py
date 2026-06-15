import tempfile
import unittest
from pathlib import Path

from gifted_masking.experiments.robustness import write_suite
from scripts.validate_manifest import validate_manifest


class ManifestCompletenessTests(unittest.TestCase):
    def test_manifest_has_required_reproducibility_fields(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            outputs = write_suite(Path(tmp_dir), suite="full")
            manifest = validate_manifest(Path(outputs["manifest"]))

        simulation = manifest["simulation"]
        self.assertEqual(simulation["master_seed"], 0)
        self.assertIn("seed_strategy", simulation)
        self.assertIn("rng_stream_strategy", simulation)
        self.assertTrue(simulation["parameter_grids"])
        self.assertTrue(simulation["n_per_cell"])
        self.assertTrue(simulation["T"])
        self.assertTrue(simulation["final_window_fraction"])
        self.assertIn("primary_raw", manifest["artifacts"])


if __name__ == "__main__":
    unittest.main()
