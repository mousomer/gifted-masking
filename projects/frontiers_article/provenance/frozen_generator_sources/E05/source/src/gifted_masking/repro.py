from __future__ import annotations

import csv
import json
import os
import platform
import subprocess
import sys
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def _package_version(name: str) -> str | None:
    try:
        from importlib.metadata import version

        return version(name)
    except Exception:
        return None


def git_commit_hash(repo_root: Path) -> str | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None
    return completed.stdout.strip()


def normalize_payload(payload: object) -> object:
    if is_dataclass(payload):
        return asdict(payload)
    if isinstance(payload, Path):
        return str(payload)
    if isinstance(payload, (list, tuple)):
        return [normalize_payload(item) for item in payload]
    if isinstance(payload, dict):
        return {key: normalize_payload(value) for key, value in payload.items()}
    return payload


def ensure_results_dirs(output_dir: Path) -> dict[str, Path]:
    paths = {
        "root": output_dir,
        "manifests": output_dir / "manifests",
        "raw": output_dir / "raw",
        "summaries": output_dir / "summaries",
        "reports": output_dir / "reports",
        "figures": output_dir / "figures",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def timestamp_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(normalize_payload(payload), indent=2) + "\n")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError("rows must not be empty")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def git_dirty_status(repo_root: Path) -> bool | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None
    return bool(completed.stdout.strip())


def environment_snapshot(repo_root: Path) -> dict[str, object]:
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "packages": {
            "numpy": np.__version__,
            "matplotlib": _package_version("matplotlib"),
        },
        "git_commit": git_commit_hash(repo_root),
        "git_unavailable_reason": None if git_commit_hash(repo_root) else "not a git repository or commit unavailable",
    }


def build_manifest(
    *,
    repo_root: Path,
    run_id: str,
    command: str,
    parameters: dict[str, object],
    output_paths: dict[str, str],
    verification: dict[str, object] | None = None,
) -> dict[str, object]:
    commit = git_commit_hash(repo_root)
    return {
        "run_id": run_id,
        "command": command,
        "working_directory": os.getcwd(),
        "git": {
            "commit": commit,
            "commit_unavailable_reason": None if commit else "not a git repository or commit unavailable",
            "dirty": git_dirty_status(repo_root),
            "diff_hash": None,
        },
        "parameters": normalize_payload(parameters),
        "simulation": normalize_payload(parameters),
        "environment": environment_snapshot(repo_root),
        "timestamps": {
            "start": timestamp_utc(),
            "end": timestamp_utc(),
        },
        "artifacts": output_paths,
        "output_paths": output_paths,
        "verification": verification or {
            "status": None,
            "test_count": None,
            "command": None,
            "runtime_seconds": None,
        },
        "cwd": os.getcwd(),
    }
