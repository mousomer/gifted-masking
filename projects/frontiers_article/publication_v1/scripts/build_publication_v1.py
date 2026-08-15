"""Deterministic Article-V1 Stage-1 publication build.

    python projects/frontiers_article/publication_v1/scripts/build_publication_v1.py

Pipeline:

    1. verify frozen E01-E05 source hashes against their manifests and the evidence matrix
    2. extract publication-source CSVs from the frozen artifacts
    3. verify the frozen scientific assertions (fail closed)
    4. generate the exact analytic-results table
    5. generate Figures 1-4 and their captions
    6. write the publication manifest
    7. verify output hashes

This entry point never runs an experiment. It imports no module from
`src/gifted_masking/experiments/`, no stochastic entry point, and no plotting
utility that re-runs a simulation. Given identical frozen inputs it reproduces
identical publication data, tables, and figures.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analytic
import captions
import extract
import figures
from pubcommon import (
    AUTHORITY_DIR,
    AUTHORITY_FILES,
    DATA_DIR,
    FAMILIES,
    FIGURES_DIR,
    MANIFESTS_DIR,
    PUB_ROOT,
    REPO_ROOT,
    SCRIPTS_DIR,
    TABLES_DIR,
    rel,
    require,
    sha256_file,
    verify_evidence_matrix,
    verify_frozen_family,
    write_provenance,
)

BUILD_COMMAND = "python projects/frontiers_article/publication_v1/scripts/build_publication_v1.py"

# Article V1 admits E01-E05 only. Any path or identifier matching one of these
# tokens would be out-of-scope evidence and must never enter the build graph.
FORBIDDEN_SCOPE_TOKENS = ("e06", "m4_", "_m4", "m4path", "path_diagnostics", "hysteresis")


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def _git_state() -> dict[str, object]:
    status = _git("status", "--porcelain")
    return {
        "commit": _git("rev-parse", "HEAD"),
        "branch": _git("rev-parse", "--abbrev-ref", "HEAD"),
        "worktree_dirty": bool(status),
        "worktree_dirty_paths": sorted(line[3:] for line in status.splitlines()) if status else [],
    }


def _hash_tree(paths: list[Path]) -> list[dict[str, object]]:
    return [
        {"path": rel(path), "sha256": sha256_file(path), "bytes": path.stat().st_size}
        for path in sorted(paths, key=lambda p: rel(p))
    ]


def _assert_scope_clean(records: list[dict[str, object]]) -> list[str]:
    """Fail closed if any source feeding the publication graph is E06/M4 material."""
    sources: list[str] = []
    for record in records:
        for source in record["sources"]:
            sources.append(source["path"])
    offending = [
        path for path in sources if any(token in Path(path).name.lower() for token in FORBIDDEN_SCOPE_TOKENS)
    ]
    require(
        not offending,
        "Scope violation: out-of-scope (E06/M4) artifacts entered the publication graph: " + ", ".join(offending),
    )
    return sorted(set(sources))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the Article-V1 Stage-1 publication package.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Rebuild and fail if any data, table, or caption output changed (determinism check).",
    )
    args = parser.parse_args()

    baseline = {}
    if args.check:
        for path in sorted(list(DATA_DIR.glob("*")) + list(TABLES_DIR.glob("*")) + list(FIGURES_DIR.glob("*"))):
            if path.is_file():
                baseline[rel(path)] = sha256_file(path)

    print("[1/7] verifying frozen E01-E05 source hashes")
    evidence = {experiment: verify_frozen_family(experiment) for experiment in FAMILIES}
    for experiment, record in evidence.items():
        print(
            f"      {experiment} {record['run_id']}: "
            f"{record['protected_outputs_valid']}/{record['protected_output_count']} protected outputs valid"
        )
    matrix = verify_evidence_matrix()
    print(
        f"      evidence matrix: {matrix['referenced_files_valid']}/{matrix['referenced_file_count']} "
        "referenced files valid"
    )

    print("[2/7] extracting publication-source data")
    data_paths, provenance = extract.extract_all()
    for path in data_paths:
        print(f"      wrote {rel(path)}")

    print("[3/7] verifying scientific assertions and Article-V1 scope")
    sources = _assert_scope_clean(provenance)
    print(f"      {len(provenance)} publication-source datasets, {len(sources)} distinct frozen source artifacts")
    print("      all pinned selectors and frozen invariants asserted during extraction")
    provenance_path = write_provenance(provenance)

    print("[4/7] generating the analytic-results table")
    table_csv, table_md = analytic.build_table()
    print(f"      wrote {rel(table_csv)}")
    print(f"      wrote {rel(table_md)}")

    print("[5/7] generating Figures 1-4")
    figure_paths = figures.build_all()
    for path in figure_paths:
        print(f"      wrote {rel(path)}")
    caption_path = captions.build()
    print(f"      wrote {rel(caption_path)}")

    print("[6/7] writing the publication manifest")
    script_paths = sorted(SCRIPTS_DIR.glob("*.py"))
    manifest = {
        "manifest_version": "1.0",
        "package": "ARTICLE_V1_STAGE1_PUBLICATION",
        "description": (
            "Deterministic Article-V1 publication build from frozen E01-E05 evidence. "
            "No experiment is rerun and no stochastic entry point is invoked."
        ),
        "scope": {
            "included_experiments": sorted(FAMILIES),
            "included_run_ids": {k: v for k, v in sorted(FAMILIES.items())},
            "excluded": ["E06", "M4"],
            "exclusion_note": (
                "E06/M4 contribute no data, figure, result, claim, caption, table, or "
                "manuscript-facing artifact to Article V1."
            ),
        },
        "generation": {
            "command": BUILD_COMMAND,
            "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "python": sys.version.split()[0],
            "git": _git_state(),
        },
        "frozen_evidence_verification": {
            "experiments": evidence,
            "evidence_matrix": matrix,
            "protected_outputs_valid": sum(r["protected_outputs_valid"] for r in evidence.values()),
            "protected_outputs_total": sum(r["protected_output_count"] for r in evidence.values()),
        },
        "article_v1_authorities": [
            {"path": rel(AUTHORITY_DIR / name), "sha256": sha256_file(AUTHORITY_DIR / name)}
            for name in AUTHORITY_FILES
            if (AUTHORITY_DIR / name).exists()
        ],
        "generating_scripts": _hash_tree(script_paths),
        "publication_source_data": provenance,
        "outputs": {
            "data": _hash_tree([p for p in DATA_DIR.glob("*") if p.is_file()]),
            "tables": _hash_tree([p for p in TABLES_DIR.glob("*") if p.is_file()]),
            "figures": _hash_tree([p for p in FIGURES_DIR.glob("*") if p.is_file()]),
        },
        "determinism": {
            "data_tables_captions": "byte-stable across rebuilds from identical frozen inputs",
            "figures": (
                "PDF CreationDate is suppressed and PNG Software metadata is cleared, so figure "
                "bytes are stable across rebuilds on the same Matplotlib version. The authoritative "
                "reproducibility layer is the source, script, and publication-data hash chain, "
                "which is independent of any renderer metadata."
            ),
        },
        "reproducibility_limitation": {
            "artifact_identity": "INTACT — 33/33 protected E01-E05 outputs hash-match their manifests",
            "model_semantics_identity": "INTACT — maintained model blobs match the audited mathematical reference",
            "generator_source_identity": {
                "E01": "ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE",
                "E02": "ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE",
                "E03": "ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE",
                "E04": "HISTORICAL_SOURCE_RECOVERED",
                "E05": "HISTORICAL_SOURCE_RECOVERED",
            },
            "statement": (
                "The frozen E01-E03 result artifacts and their manifests were preserved and "
                "independently validated, but the exact dirty-worktree generator source state used "
                "for those historical runs was not fully recoverable. E04-E05 retain "
                "fingerprint-exact historical generator-source bundles. Article-V1 figures and "
                "tables are generated deterministically from the preserved frozen artifacts rather "
                "than by rerunning the experiments."
            ),
        },
        "provenance_index": rel(provenance_path),
    }

    manifest_path = MANIFESTS_DIR / "publication_v1_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"      wrote {rel(manifest_path)}")

    print("[7/7] verifying output hashes")
    recorded = {
        entry["path"]: entry["sha256"]
        for group in manifest["outputs"].values()
        for entry in group
    }
    mismatches = [path for path, digest in recorded.items() if sha256_file(REPO_ROOT / path) != digest]
    require(not mismatches, "Output hash verification failed for: " + ", ".join(mismatches))
    print(f"      {len(recorded)} outputs re-hashed and consistent with the manifest")

    if args.check:
        changed = []
        for path, digest in baseline.items():
            full = REPO_ROOT / path
            if not full.exists():
                changed.append(f"{path}: removed")
            elif sha256_file(full) != digest:
                changed.append(f"{path}: content changed")
        require(
            not changed,
            "Determinism check FAILED — rebuilding from identical frozen inputs changed:\n  "
            + "\n  ".join(changed),
        )
        print(f"      determinism check PASSED — {len(baseline)} previously built outputs are byte-identical")

    print("\nARTICLE_V1_STAGE1_PUBLICATION_BUILD_OK")
    print(f"  package: {rel(PUB_ROOT)}")
    print(f"  no experiment was rerun; {manifest['frozen_evidence_verification']['protected_outputs_valid']}"
          f"/{manifest['frozen_evidence_verification']['protected_outputs_total']} protected outputs valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
