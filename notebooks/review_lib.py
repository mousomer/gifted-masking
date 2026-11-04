"""Helpers for ``notebooks/review_and_research.ipynb``.

Read-only review tooling: it inspects tests, model APIs, manifests and result
artifacts, and runs small simulations through the maintained package.  It never
writes into ``results/`` and never changes model semantics.

Only the standard library and numpy are required here; the notebook itself adds
pandas and matplotlib for display.
"""

from __future__ import annotations

import ast
import hashlib
import importlib
import inspect
import json
import math
import subprocess
import time
import unittest
from pathlib import Path
from typing import Any, Callable, Iterable

import numpy as np


MODEL_MODULES = (
    "gifted_masking.models.m0",
    "gifted_masking.models.m1",
    "gifted_masking.models.m2",
    "gifted_masking.models.m3",
    "gifted_masking.models.m4",
    "gifted_masking.analysis.m2_optimal",
    "gifted_masking.core",
)

# Fast, model-level tests: safe to run interactively (a few seconds).
# test_m2_optimal_policy.py is model-level too but takes ~80 s, so it runs with
# the full suite instead.
FAST_TEST_FILES = (
    "test_core.py",
    "test_m0.py",
    "test_m1.py",
    "test_m2.py",
    "test_m3.py",
    "test_m4.py",
    "test_determinism.py",
)

# AGENTS.md validation targets mapped to keyword patterns.  This is a heuristic
# index for reviewers ("where is this probably tested?"), not a proof of coverage.
AGENT_REQUIREMENTS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("core", "softmax normalisation and numerical stability", ("softmax",)),
    ("core", "loss aversion leaves nonnegative rewards unchanged", ("loss", "subjective", "lam")),
    ("core", "RNG determinism / seed reproducibility", ("determinis", "seed", "reproduc")),
    ("M0", "expected rewards and objective indifference threshold", ("indifference", "expected", "threshold")),
    ("M0", "empirical acceptance converges to p", ("acceptance", "converge", "empirical")),
    ("M1", "disclosure grid endpoints and E(d) endpoints", ("endpoint", "grid", "disclosure")),
    ("M1", "acceptance probability stays in [0, 1]", ("acceptance",)),
    ("M2", "explicit state transitions", ("transition",)),
    ("M2", "value-iteration optimal policy benchmark", ("value_iteration", "optimal", "bellman")),
    ("M2", "dynamic regret against optimal policy", ("regret",)),
    ("M3", "action indexing arm -> (group, behaviour)", ("decode", "index", "action")),
    ("M3", "BFLPE crossover bf*", ("bflpe", "crossover", "bf")),
    ("M3", "action-space ablations (hierarchical/global/fixed)", ("hierarch", "global", "fixed", "ablation")),
    ("M4", "receptivity bounded in [p_min, p_max]", ("bound", "receptivity", "clip")),
    ("M4", "hysteresis path (ramp up then down)", ("hysteresis", "path", "loop")),
    ("artifacts", "manifest completeness and raw schema", ("manifest", "schema")),
    ("artifacts", "summaries recompute from raw", ("summary", "recompute", "raw")),
)


# ---------------------------------------------------------------------------
# Repository and provenance
# ---------------------------------------------------------------------------

def repo_root(start: Path | None = None) -> Path:
    """Walk up from ``start`` (default: cwd) to the directory holding pyproject.toml."""
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "src" / "gifted_masking").is_dir():
            return candidate
    raise FileNotFoundError("could not locate the gifted-masking repository root")


def _git(root: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.stdout.strip()


def git_info(root: Path) -> dict[str, object]:
    porcelain = _git(root, "status", "--porcelain")
    return {
        "branch": _git(root, "rev-parse", "--abbrev-ref", "HEAD"),
        "commit": _git(root, "rev-parse", "HEAD"),
        "dirty_paths": None if porcelain is None else len([line for line in porcelain.splitlines() if line]),
    }


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(chunk), b""):
            digest.update(block)
    return digest.hexdigest()


# ---------------------------------------------------------------------------
# Model API inventory
# ---------------------------------------------------------------------------

def model_api(modules: Iterable[str] = MODEL_MODULES) -> list[dict[str, object]]:
    rows = []
    for name in modules:
        module = importlib.import_module(name)
        for attr, obj in vars(module).items():
            if attr.startswith("_") or getattr(obj, "__module__", None) != module.__name__:
                continue
            if not (inspect.isfunction(obj) or inspect.isclass(obj)):
                continue
            doc = inspect.getdoc(obj) or ""
            rows.append({
                "module": name.rsplit(".", 1)[-1],
                "name": attr,
                "kind": "class" if inspect.isclass(obj) else "function",
                "signature": str(inspect.signature(obj)),
                "line": inspect.getsourcelines(obj)[1],
                "doc": doc.splitlines()[0] if doc else "",
            })
    return rows


def simulate_defaults(functions: dict[str, Callable[..., Any]]) -> dict[str, dict[str, object]]:
    """Keyword defaults of each simulate-like function, keyed by label."""
    table: dict[str, dict[str, object]] = {}
    for label, fn in functions.items():
        params = inspect.signature(fn).parameters
        table[label] = {
            key: (param.default if param.default is not inspect.Parameter.empty else "<required>")
            for key, param in params.items()
        }
    return table


# ---------------------------------------------------------------------------
# Test catalogue and runner
# ---------------------------------------------------------------------------

def _imported_project_modules(tree: ast.AST) -> set[str]:
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("gifted_masking"):
            base = node.module.split(".", 1)[1] if "." in node.module else "gifted_masking"
            if base in {"models", "experiments", "analysis", "plotting"}:
                found.update(f"{base}.{alias.name}" for alias in node.names)
            else:
                found.add(base)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("gifted_masking."):
                    found.add(alias.name.split(".", 1)[1])
    return found


def catalog_tests(tests_dir: Path) -> list[dict[str, object]]:
    """Statically list every ``test_*`` method without importing the test modules."""
    rows = []
    for path in sorted(tests_dir.glob("test_*.py")):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        modules = sorted(_imported_project_modules(tree))
        for cls in (node for node in tree.body if isinstance(node, ast.ClassDef)):
            for fn in (node for node in cls.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))):
                if not fn.name.startswith("test"):
                    continue
                body = ast.get_source_segment(source, fn) or ""
                doc = ast.get_docstring(fn) or ""
                rows.append({
                    "file": path.name,
                    "class": cls.name,
                    "test": fn.name,
                    "test_id": f"{path.stem}.{cls.name}.{fn.name}",
                    "line": fn.lineno,
                    "body_lines": (fn.end_lineno or fn.lineno) - fn.lineno + 1,
                    "assertions": body.count("self.assert") + body.count("assert "),
                    "doc": doc.splitlines()[0] if doc else "",
                    "project_modules": ", ".join(modules),
                    "_body": body,
                })
    return rows


def requirement_coverage(catalog: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for area, requirement, keywords in AGENT_REQUIREMENTS:
        hits = [
            row["test_id"]
            for row in catalog
            if any(keyword in (str(row["test"]) + " " + str(row["_body"])).lower() for keyword in keywords)
            and (area in {"core", "artifacts"} or area.lower() in str(row["file"]).lower() or area.lower() in str(row["_body"]).lower())
        ]
        rows.append({
            "area": area,
            "requirement": requirement,
            "candidate_tests": len(hits),
            "examples": "; ".join(str(hit).split(".", 1)[1] for hit in hits[:3]),
        })
    return rows


class _TimingResult(unittest.TextTestResult):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.records: list[dict[str, object]] = []
        self._started: dict[str, float] = {}

    def startTest(self, test: unittest.TestCase) -> None:  # noqa: N802 - unittest API
        self._started[test.id()] = time.perf_counter()
        super().startTest(test)

    def _record(self, test: unittest.TestCase, status: str, message: str = "") -> None:
        elapsed = time.perf_counter() - self._started.get(test.id(), time.perf_counter())
        self.records.append({"test_id": test.id(), "status": status, "seconds": round(elapsed, 3), "message": message})

    def addSuccess(self, test: unittest.TestCase) -> None:  # noqa: N802
        super().addSuccess(test)
        self._record(test, "pass")

    def addFailure(self, test: unittest.TestCase, err: Any) -> None:  # noqa: N802
        super().addFailure(test, err)
        self._record(test, "FAIL", self._exc_info_to_string(err, test).strip().splitlines()[-1])

    def addError(self, test: unittest.TestCase, err: Any) -> None:  # noqa: N802
        super().addError(test, err)
        self._record(test, "ERROR", self._exc_info_to_string(err, test).strip().splitlines()[-1])

    def addSkip(self, test: unittest.TestCase, reason: str) -> None:  # noqa: N802
        super().addSkip(test, reason)
        self._record(test, "skip", reason)

    def addExpectedFailure(self, test: unittest.TestCase, err: Any) -> None:  # noqa: N802
        super().addExpectedFailure(test, err)
        self._record(test, "xfail")

    def addUnexpectedSuccess(self, test: unittest.TestCase) -> None:  # noqa: N802
        super().addUnexpectedSuccess(test)
        self._record(test, "UNEXPECTED_PASS")


def run_tests(tests_dir: Path, files: Iterable[str] | None = None, *, name_filter: str | None = None) -> list[dict[str, object]]:
    """Run unittest files in-process and return one record per test.

    ``files`` defaults to every ``test_*.py``; ``name_filter`` keeps tests whose
    id contains the substring.  Runner output and anything the tests print go
    to an in-memory buffer.
    """
    import contextlib
    import io

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    selected = list(files) if files is not None else sorted(path.name for path in tests_dir.glob("test_*.py"))
    for filename in selected:
        suite.addTests(loader.discover(str(tests_dir), pattern=filename, top_level_dir=str(tests_dir.parent)))
    if name_filter:
        def _flatten(item: unittest.TestSuite | unittest.TestCase) -> Iterable[unittest.TestCase]:
            if isinstance(item, unittest.TestSuite):
                for child in item:
                    yield from _flatten(child)
            else:
                yield item
        suite = unittest.TestSuite(test for test in _flatten(suite) if name_filter in test.id())
    buffer = io.StringIO()
    runner = unittest.TextTestRunner(stream=buffer, resultclass=_TimingResult, verbosity=0)
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        result = runner.run(suite)
    return result.records  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Results artifacts and manifests
# ---------------------------------------------------------------------------

def list_artifacts(results_dir: Path) -> list[dict[str, object]]:
    rows = []
    for path in sorted(results_dir.rglob("*")):
        if path.is_file():
            rows.append({
                "kind": path.relative_to(results_dir).parts[0],
                "path": str(path.relative_to(results_dir)),
                "suffix": path.suffix,
                "mib": round(path.stat().st_size / (1 << 20), 3),
            })
    return rows


def _manifest_output_paths(manifest: dict[str, Any]) -> dict[str, str]:
    outputs = manifest.get("outputs")
    if isinstance(outputs, dict):
        return {key: value["path"] for key, value in outputs.items() if isinstance(value, dict) and "path" in value}
    artifacts = manifest.get("artifacts")
    if isinstance(artifacts, dict):
        return {key: value for key, value in artifacts.items() if isinstance(value, str)}
    return {}


def load_manifests(results_dir: Path) -> list[dict[str, object]]:
    rows = []
    for path in sorted((results_dir / "manifests").glob("*.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        git = manifest.get("git") if isinstance(manifest.get("git"), dict) else {}
        verification = manifest.get("verification")
        status = verification.get("status") if isinstance(verification, dict) else verification
        normalized = manifest.get("normalized_config")
        config_sha = manifest.get("config_sha256")
        config_ok = None
        if isinstance(normalized, str) and isinstance(config_sha, str):
            config_ok = hashlib.sha256(normalized.encode("utf-8")).hexdigest() == config_sha
        outputs = manifest.get("outputs") if isinstance(manifest.get("outputs"), dict) else {}
        raw_rows = outputs.get("raw", {}).get("rows") if isinstance(outputs.get("raw"), dict) else None
        rows.append({
            "manifest": path.name,
            "run_id": manifest.get("run_id"),
            "experiment_id": manifest.get("experiment_id"),
            "tier": manifest.get("tier"),
            "config_path": manifest.get("config_path"),
            "config_sha_matches": config_ok,
            "git_commit": (git.get("commit") or "")[:10] or None,
            "git_dirty": git.get("dirty"),
            "verification": status,
            "raw_rows": raw_rows,
            "n_outputs": len(_manifest_output_paths(manifest)),
            "_manifest": manifest,
        })
    return rows


def verify_manifest_hashes(manifest: dict[str, Any], root: Path, *, max_mib: float = 50.0) -> list[dict[str, object]]:
    """Recompute sha256 of each declared output that has a recorded hash."""
    hashes = manifest.get("output_hashes") if isinstance(manifest.get("output_hashes"), dict) else {}
    paths = _manifest_output_paths(manifest)
    rows = []
    for key, recorded in hashes.items():
        if not isinstance(recorded, dict) or "sha256" not in recorded or key not in paths:
            continue
        path = Path(paths[key])
        path = path if path.is_absolute() else root / path
        row = {"run_id": manifest.get("run_id"), "output": key, "path": str(path.relative_to(root)) if path.is_relative_to(root) else str(path)}
        if not path.is_file():
            row.update(status="missing")
        elif path.stat().st_size > max_mib * (1 << 20):
            row.update(status=f"skipped (> {max_mib:g} MiB)", bytes_match=path.stat().st_size == recorded.get("bytes"))
        else:
            row.update(status="match" if sha256_file(path) == recorded["sha256"] else "MISMATCH", bytes_match=path.stat().st_size == recorded.get("bytes"))
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Review checks and research helpers
# ---------------------------------------------------------------------------

def check(name: str, observed: Any, expected: Any, *, tol: float = 1e-9) -> dict[str, object]:
    """One row of a pass/fail table comparing an observed value with a specification."""
    if isinstance(expected, bool) or isinstance(observed, bool):
        passed = bool(observed) == bool(expected)
    elif isinstance(expected, (int, float, np.floating, np.integer)) and isinstance(observed, (int, float, np.floating, np.integer)):
        passed = math.isclose(float(observed), float(expected), rel_tol=0.0, abs_tol=tol)
    else:
        passed = np.array_equal(np.asarray(observed), np.asarray(expected))
    return {"check": name, "expected": expected, "observed": observed, "passed": bool(passed)}


def replicate(fn: Callable[..., Any], seeds: Iterable[int], *, select: Callable[[Any], np.ndarray] | None = None, **kwargs: Any) -> dict[str, float]:
    """Run ``fn(seed=s, **kwargs)`` for each master seed and summarise the per-seed means.

    The uncertainty is between independent master seeds (the replication unit
    required by AGENTS.md), not between children inside one seed.
    """
    means = []
    for seed in seeds:
        out = fn(seed=int(seed), **kwargs)
        values = select(out) if select else np.asarray(out)
        means.append(float(np.mean(values)))
    arr = np.asarray(means)
    se = float(arr.std(ddof=1) / math.sqrt(arr.size)) if arr.size > 1 else float("nan")
    return {"mean": float(arr.mean()), "se_between_seeds": se, "n_seeds": int(arr.size), "min": float(arr.min()), "max": float(arr.max())}


def sweep(fn: Callable[..., Any], param: str, values: Iterable[Any], seeds: Iterable[int], *, select: Callable[[Any], np.ndarray] | None = None, **fixed: Any) -> list[dict[str, object]]:
    """One-at-a-time sweep of ``param`` with master-seed replication at each value."""
    seeds = list(seeds)
    rows = []
    for value in values:
        summary = replicate(fn, seeds, select=select, **{**fixed, param: value})
        rows.append({param: value, **summary})
    return rows


def learner_steps(n: int, horizon: int, cells: int = 1, seeds: int = 1) -> int:
    """Child-steps a run will cost; use it to size a sweep before launching it."""
    return int(n) * int(horizon) * int(cells) * int(seeds)
