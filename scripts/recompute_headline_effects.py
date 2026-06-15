from __future__ import annotations

import csv
import sys
from pathlib import Path

from gifted_masking.experiments.robustness import EFFECT_SPECS, _values_for_effect
from gifted_masking.repro import write_csv


DEFAULT_UNITS = Path("results/raw/robustness_full_units.csv")
DEFAULT_SUMMARY = Path("results/summaries/robustness_full_summary.csv")
DEFAULT_OUTPUT = Path("results/summaries/robustness_full_recomputed_effects.csv")
TOLERANCE = 1e-12


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def recompute_headline_effects(
    units_path: Path = DEFAULT_UNITS,
    summary_path: Path = DEFAULT_SUMMARY,
    output_path: Path = DEFAULT_OUTPUT,
) -> list[dict[str, object]]:
    unit_rows = read_csv(units_path)
    summary_rows = {row["check_name"]: row for row in read_csv(summary_path)}
    output_rows = []
    failures = []
    for spec in EFFECT_SPECS:
        values = _values_for_effect(unit_rows, spec)
        recomputed = float(values.mean())
        reported = float(summary_rows[spec.check_name]["estimate"])
        diff = abs(recomputed - reported)
        match = diff <= TOLERANCE
        if not match:
            failures.append(spec.check_name)
        output_rows.append(
            {
                "claim": spec.check_name,
                "reported_value": reported,
                "recomputed_value": recomputed,
                "absolute_difference": diff,
                "tolerance": TOLERANCE,
                "match": match,
                "notes": "recomputed from primary unit rows",
            }
        )
    write_csv(output_path, output_rows)
    if failures:
        raise SystemExit(f"Headline recomputation mismatch: {', '.join(failures)}")
    return output_rows


def main() -> None:
    units_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_UNITS
    summary_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_SUMMARY
    output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_OUTPUT
    recompute_headline_effects(units_path, summary_path, output_path)
    print(output_path)


if __name__ == "__main__":
    main()
