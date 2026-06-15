from __future__ import annotations

import json
import sys
from pathlib import Path


DEFAULT_MANIFEST = Path("results/manifests/robustness_full.json")


class ManifestValidationError(ValueError):
    pass


def _require(mapping: dict[str, object], key: str, context: str) -> object:
    if key not in mapping:
        raise ManifestValidationError(f"Missing {context}.{key}")
    value = mapping[key]
    if value in ({}, [], ""):
        raise ManifestValidationError(f"Empty {context}.{key}")
    return value


def validate_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, object]:
    manifest = json.loads(path.read_text())
    for key in ["run_id", "command", "working_directory", "git", "environment", "simulation", "artifacts", "verification", "timestamps"]:
        _require(manifest, key, "manifest")

    simulation = manifest["simulation"]
    if not isinstance(simulation, dict):
        raise ManifestValidationError("manifest.simulation must be an object")
    for key in ["master_seed", "bootstrap_seed", "seed_strategy", "rng_stream_strategy", "parameter_grids", "n_per_cell", "T", "final_window_fraction", "code_config_hash"]:
        _require(simulation, key, "simulation")

    if not simulation["parameter_grids"]:
        raise ManifestValidationError("simulation.parameter_grids must not be empty")

    artifacts = manifest["artifacts"]
    if not isinstance(artifacts, dict):
        raise ManifestValidationError("manifest.artifacts must be an object")
    for key in ["primary_raw", "raw_legacy_or_summary", "summary", "report"]:
        artifact_path = Path(str(_require(artifacts, key, "artifacts")))
        if not artifact_path.exists():
            raise ManifestValidationError(f"Artifact path does not exist: {artifact_path}")

    environment = manifest["environment"]
    if not isinstance(environment, dict):
        raise ManifestValidationError("manifest.environment must be an object")
    _require(environment, "python_version", "environment")
    _require(environment, "platform", "environment")
    _require(environment, "packages", "environment")

    git = manifest["git"]
    if not isinstance(git, dict):
        raise ManifestValidationError("manifest.git must be an object")
    if git.get("commit") is None and not git.get("commit_unavailable_reason"):
        raise ManifestValidationError("git commit is null without commit_unavailable_reason")

    return manifest


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MANIFEST
    validate_manifest(path)
    print(path)


if __name__ == "__main__":
    main()
