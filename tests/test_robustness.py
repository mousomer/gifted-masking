import tempfile
import unittest
from pathlib import Path

from gifted_masking.experiments.robustness import run_m3_ablation_suite, run_m4_hysteresis_suite, run_smoke_suite, write_suite


class RobustnessTests(unittest.TestCase):
    def test_smoke_suite_checks_pass(self):
        results = run_smoke_suite()
        self.assertTrue(results)
        self.assertTrue(all(result.passed for result in results))

    def test_smoke_suite_writes_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            outputs = write_suite(Path(tmp_dir), suite="smoke")
            for path in outputs.values():
                self.assertTrue(Path(path).exists())

    def test_m3_ablation_suite_runs(self):
        results = run_m3_ablation_suite()
        self.assertTrue(results)
        self.assertTrue(all(result.suite == "m3_ablation" for result in results))

    def test_m4_hysteresis_suite_runs(self):
        results = run_m4_hysteresis_suite()
        self.assertEqual(len(results), 2)
        self.assertTrue(all(result.suite == "m4_hysteresis" for result in results))

    def test_full_suite_writes_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            outputs = write_suite(Path(tmp_dir), suite="full")
            for path in outputs.values():
                self.assertTrue(Path(path).exists())


if __name__ == "__main__":
    unittest.main()
