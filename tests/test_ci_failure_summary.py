import tempfile
import unittest
from pathlib import Path

from scripts.ci_failure_summary import summarize


class CIFailureSummaryTests(unittest.TestCase):
    def test_only_published_test_identity_and_fixed_error_class_are_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            tests = Path(temporary)
            (tests / "test_example.py").write_text(
                "class ExampleTests:\n    def test_example(self): pass\n")
            text = ("FAIL: test_example (test_example.ExampleTests.test_example)\n"
                    "Traceback containing invented private prompt text\n"
                    "AssertionError: invented runtime value\n")
            self.assertEqual(summarize(text, tests), [
                "CI failure category: unit-test",
                "failed-test: test_example.ExampleTests.test_example [AssertionError]",
            ])

    def test_unknown_log_identifiers_and_messages_are_not_echoed(self):
        with tempfile.TemporaryDirectory() as temporary:
            text = ("ERROR: test_arbitrary (unpublished.Source.test_arbitrary)\n"
                    "ValueError: invented runtime value\n")
            self.assertEqual(summarize(text, Path(temporary)),
                             ["CI failure category: verifier-command"])
