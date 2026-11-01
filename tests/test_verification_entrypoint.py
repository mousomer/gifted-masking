"""Prove interpreter selection and governance fail-fast without running models."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class VerificationEntrypointTests(unittest.TestCase):
    def fixture(self, directory, governance_status=0):
        root = Path(directory)
        (root / "scripts").mkdir()
        source = Path(__file__).resolve().parents[1] / "scripts/verify.sh"
        shutil.copy2(source, root / "scripts/verify.sh")
        hook = root / "scripts/verify-governance.sh"
        hook.write_text(f"#!/bin/sh\nexit {governance_status}\n")
        hook.chmod(0o755)
        selected = root / "selected-python"
        selected.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$INTERPRETER_MARKER"\nexit 37\n')
        selected.chmod(0o755)
        marker = root / "interpreter-call"
        environment = {**os.environ, "GOVERNANCE_PYTHON": str(selected),
                       "INTERPRETER_MARKER": str(marker)}
        return root, marker, environment

    def test_selected_interpreter_runs_product_checks(self):
        with tempfile.TemporaryDirectory(prefix="verifier_selection_") as temporary:
            root, marker, environment = self.fixture(temporary)
            result = subprocess.run([str(root / "scripts/verify.sh")], env=environment,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 37)
            self.assertEqual(marker.read_text().splitlines()[:3], ["-m", "unittest", "discover"])

    def test_governance_failure_prevents_product_execution(self):
        with tempfile.TemporaryDirectory(prefix="verifier_rejection_") as temporary:
            root, marker, environment = self.fixture(temporary, governance_status=29)
            result = subprocess.run([str(root / "scripts/verify.sh")], env=environment,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 29)
            self.assertFalse(marker.exists())
