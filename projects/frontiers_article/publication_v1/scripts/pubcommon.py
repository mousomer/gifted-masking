"""Shared helpers for the Article-V1 deterministic publication build.

Stage 1 is publication assembly from frozen E01-E05 evidence. Nothing in this
package may invoke an experiment runner, a stochastic entry point, or any model
simulation. The only permitted transformations of frozen evidence are row
filters, column projections, deterministic joins, equal-weight aggregations that
reproduce a value already stored in the frozen artifacts, closed-form analytic
calculation, and rounding for display.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
PUB_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PUB_ROOT / "data"
FIGURES_DIR = PUB_ROOT / "figures"
TABLES_DIR = PUB_ROOT / "tables"
MANIFESTS_DIR = PUB_ROOT / "manifests"
SCRIPTS_DIR = PUB_ROOT / "scripts"

SUMMARIES = REPO_ROOT / "results" / "summaries"
MANIFEST_DIR = REPO_ROOT / "results" / "manifests"
AUTHORITY_DIR = REPO_ROOT / "projects" / "frontiers_article"

# Frozen experiment families admitted to Article V1. E06/M4 are excluded by
# scope and must never appear as a key here.
FAMILIES = {
    "E01": "frontiers_hot_stove_v1",
    "E02": "frontiers_m1_binary_graded_v1",
    "E03": "frontiers_m2_regime_replication_v1",
    "E04": "frontiers_m3_search_architectures_v1",
    "E05": "frontiers_m3_bflpe_crossover_v1",
}

# Article-V1 authority documents whose hashes are recorded in the manifest.
AUTHORITY_FILES = (
    "ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md",
    "ARTICLE_V1_EVIDENCE_MATRIX.csv",
    "ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md",
    "ARTICLE_V1_ANALYTIC_RESULTS.md",
    "ARTICLE_V1_E01_E02_INTERPRETATION.md",
    "ARTICLE_V1_E03_INTERPRETATION.md",
    "ARTICLE_V1_E04_INTERPRETATION.md",
    "ARTICLE_V1_E05_INTERPRETATION.md",
    "ARTICLE_V1_GENERATOR_SOURCE_PROVENANCE_AUDIT.md",
    "HANDOFF.md",
)


class PublicationAssertionError(AssertionError):
    """A frozen scientific invariant did not hold. The build must stop."""


def require(condition: bool, message: str) -> None:
    """Fail closed. Never adapt silently to a changed dataset."""
    if not condition:
        raise PublicationAssertionError(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return Path(path).resolve().relative_to(REPO_ROOT).as_posix()


def read_rows(path: Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    """Write a publication-source CSV with byte-stable formatting."""
    with Path(path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def repr_float(value: float) -> str:
    """Full-precision round-trippable float, so no precision is lost in transit."""
    return repr(float(value))


def verify_frozen_family(experiment: str) -> dict[str, object]:
    """Re-check every protected output of one frozen run against its manifest.

    Returns the per-artifact verification record. Raises if any protected output
    is missing or differs. A hash failure is never repaired by regeneration.
    """
    family = FAMILIES[experiment]
    manifest_path = MANIFEST_DIR / f"{family}.json"
    require(manifest_path.exists(), f"{experiment}: manifest missing at {manifest_path}")
    manifest = json.loads(manifest_path.read_text())
    outputs, hashes = manifest["outputs"], manifest["output_hashes"]

    artifacts, failures = {}, []
    for key in sorted(hashes):
        expected = hashes[key]["sha256"]
        expected_bytes = hashes[key]["bytes"]
        path = REPO_ROOT / outputs[key]["path"]
        if not path.exists():
            failures.append(f"{experiment}/{key}: MISSING {outputs[key]['path']}")
            continue
        payload = path.read_bytes()
        actual = hashlib.sha256(payload).hexdigest()
        if actual != expected or len(payload) != expected_bytes:
            failures.append(
                f"{experiment}/{key}: HASH MISMATCH {outputs[key]['path']} "
                f"manifest={expected} actual={actual} "
                f"bytes manifest={expected_bytes} actual={len(payload)}"
            )
            continue
        artifacts[key] = {"path": outputs[key]["path"], "sha256": actual, "bytes": len(payload)}

    require(
        not failures,
        f"{experiment}: frozen artifact verification failed; publication component stopped.\n"
        + "\n".join(failures),
    )
    return {
        "experiment": experiment,
        "run_id": family,
        "manifest_path": rel(manifest_path),
        "manifest_sha256": sha256_file(manifest_path),
        "protected_output_count": len(hashes),
        "protected_outputs_valid": len(artifacts),
        "artifacts": artifacts,
        "status": "PASS",
    }


def verify_evidence_matrix() -> dict[str, object]:
    """Re-check every artifact and config the evidence matrix content-addresses."""
    matrix_path = AUTHORITY_DIR / "ARTICLE_V1_EVIDENCE_MATRIX.csv"
    rows = read_rows(matrix_path)
    referenced: dict[str, str] = {}
    for row in rows:
        for path_field, hash_field in (
            ("current_artifact_path", "artifact_sha256"),
            ("config_path", "config_sha256"),
        ):
            path, digest = row[path_field].strip(), row[hash_field].strip()
            if path and digest:
                referenced[path] = digest

    checked, failures = {}, []
    for path, expected in sorted(referenced.items()):
        full = REPO_ROOT / path
        if not full.exists():
            failures.append(f"evidence matrix: MISSING {path}")
            continue
        actual = sha256_file(full)
        if actual != expected:
            failures.append(f"evidence matrix: HASH MISMATCH {path} matrix={expected} actual={actual}")
            continue
        checked[path] = actual

    require(not failures, "Evidence-matrix verification failed.\n" + "\n".join(failures))
    return {
        "matrix_path": rel(matrix_path),
        "matrix_sha256": sha256_file(matrix_path),
        "referenced_file_count": len(referenced),
        "referenced_files_valid": len(checked),
        "files": checked,
        "status": "PASS",
    }


def provenance_record(
    *,
    output: Path,
    experiment: str,
    sources: list[dict[str, str]],
    selector: dict[str, object],
    fields: list[str],
    transformation: list[str],
    notes: str,
) -> dict[str, object]:
    """Provenance sidecar for one publication-source CSV.

    `transformation` must name only the permitted deterministic operations, so
    that no step between a frozen artifact and a plotted number is hidden.
    """
    permitted = {
        "row_filter",
        "column_projection",
        "deterministic_join",
        "equal_weight_master_mean",
        "master_range",
        "count_aggregation",
        "closed_form_analytic",
        "rounding_for_display",
    }
    unknown = sorted(set(transformation) - permitted)
    require(not unknown, f"{output.name}: undeclared transformation(s) {unknown}")
    return {
        "output_file": rel(output),
        "output_sha256": sha256_file(output),
        "source_experiment": experiment,
        "sources": sources,
        "selector": selector,
        "fields": fields,
        "transformation": transformation,
        "notes": notes,
    }


def source_ref(path: Path) -> dict[str, str]:
    return {"path": rel(path), "sha256": sha256_file(path)}


def write_provenance(records: list[dict[str, object]]) -> Path:
    path = DATA_DIR / "PROVENANCE.json"
    path.write_text(json.dumps(records, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    return path
