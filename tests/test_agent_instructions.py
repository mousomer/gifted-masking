"""Guard active dispatch placement without treating examples as assignments."""

from pathlib import Path
import re
import unittest


def active_dispatch_outside_examples(text):
    fence = None
    found = False
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token, suffix = marker.groups()
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not suffix.strip():
                fence = None
        if "<!-- BEGIN workspace-governance managed dispatch -->" in line:
            if fence is not None or found:
                return False
            found = True
    return found and fence is None


class InstructionPlacementTests(unittest.TestCase):
    def test_project_dispatch_is_active(self):
        text = (Path(__file__).resolve().parents[1] / "AGENTS.md").read_text()
        self.assertTrue(active_dispatch_outside_examples(text))
        self.assertIn("One-off Codex task prompt", text)
        self.assertIn("Optional follow-up prompt", text)

    def test_open_example_rejects_even_with_valid_managed_marker(self):
        marker = "<!-- BEGIN workspace-governance managed dispatch -->"
        for fence in ("```markdown", "~~~text", "````markdown"):
            with self.subTest(fence=fence):
                self.assertFalse(active_dispatch_outside_examples(fence + "\nexample\n" + marker))
                closing = re.match(r"[`~]+", fence).group()
                self.assertTrue(active_dispatch_outside_examples(fence + "\nexample\n" + closing + "\n" + marker))
