from __future__ import annotations

import csv
import sys
from pathlib import Path

from gifted_masking.core import summarize_mean
from gifted_masking.experiments.robustness import BOOTSTRAP_SEED, EFFECT_SPECS, _values_for_effect
from gifted_masking.repro import write_csv


DEFAULT_UNITS = Path("results/raw/robustness_full_units.csv")
DEFAULT_OUTPUT = Path("results/summaries/robustness_full_headline_uncertainty.csv")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def compute_headline_uncertainty(
    units_path: Path = DEFAULT_UNITS,
    output_path: Path = DEFAULT_OUTPUT,
) -> list[dict[str, object]]:
    unit_rows = read_csv(units_path)
    output_rows = []
    for spec in EFFECT_SPECS:
        values = _values_for_effect(unit_rows, spec)
        summary = summarize_mean(values, seed=BOOTSTRAP_SEED)
        if spec.robust_direction == "positive":
            robust = summary.ci_low > 0.0
        elif spec.robust_direction == "negative":
            robust = summary.ci_high < 0.0
        else:
            robust = False
        output_rows.append(
            {
                "effect": spec.check_name,
                "estimate": summary.estimate,
                "ci95_low": summary.ci_low,
                "ci95_high": summary.ci_high,
                "resampling_unit": "matched child unit" if values.size > 20 else "matched ramp-grid unit",
                "n_units": int(values.size),
                "method": f"bootstrap over matched units; bootstrap_seed={BOOTSTRAP_SEED}",
                "robust_direction": robust,
                "notes": spec.notes,
            }
        )
    write_csv(output_path, output_rows)
    return output_rows


def main() -> None:
    units_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_UNITS
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT
    compute_headline_uncertainty(units_path, output_path)
    print(output_path)


if __name__ == "__main__":
    main()
