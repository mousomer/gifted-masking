"""Emit fixed failure classes and published test IDs, never raw log content."""

import ast
from pathlib import Path
import re
import sys

LIMIT = 2 * 1024 * 1024
ERROR_TYPES = {"AssertionError", "CalledProcessError", "FileNotFoundError", "ImportError",
               "ModuleNotFoundError", "PermissionError", "RuntimeError", "TypeError", "ValueError"}
GUARD_REASONS = {
    "linear standard runtime projection exceeded 10 minutes": "runtime-projection-limit",
    "smoke runtime exceeded 60 seconds": "smoke-runtime-limit",
    "smoke raw output exceeded 20 MiB": "smoke-size-limit",
    "E04 canonicalization cardinality violation": "canonicalization-cardinality",
    "E04 equivalence table must name exactly 55 canonical requests": "equivalence-cardinality",
    "E04 tier cardinality mismatch": "tier-cardinality",
}


def summarize(text, tests):
    known = set()
    for path in tests.glob("test_*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.ClassDef):
                known.update(f"{path.stem}.{node.name}.{method.name}" for method in node.body
                             if isinstance(method, ast.FunctionDef) and method.name.startswith("test_"))
    failures = []
    for section in re.split(r"(?m)^(?:FAIL|ERROR): ", text)[1:]:
        header = section.splitlines()[0]
        match = re.fullmatch(r"test_\w+ \(([A-Za-z0-9_.]+)\)", header)
        if not match or match[1] not in known:
            continue
        category = "unclassified"
        for error in re.findall(r"(?m)^([A-Za-z0-9_.]+):", section):
            candidate = error.rsplit(".", 1)[-1]
            if candidate in ERROR_TYPES:
                category = candidate
        failures.append(f"failed-test: {match[1]} [{category}]")
        failures.extend("guard-reason: " + code for message, code in GUARD_REASONS.items()
                        if message in section)
    return ["CI failure category: " + ("unit-test" if failures else "verifier-command"),
            *failures[:20]]


def main():
    try:
        with Path(sys.argv[1]).open("rb") as stream:
            raw = stream.read(LIMIT + 1)
        if len(raw) > LIMIT:
            raise ValueError
        lines = summarize(raw.decode("utf8", errors="replace"), Path(__file__).resolve().parents[1] / "tests")
    except (OSError, ValueError, SyntaxError):
        lines = ["CI failure category: diagnostic-input-refused"]
    print("\n".join(lines))


if __name__ == "__main__":
    main()
