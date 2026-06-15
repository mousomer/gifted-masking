#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"

if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "Missing $VENV_PYTHON. Run ./scripts/bootstrap_venv.sh first." >&2
  exit 1
fi

export PYTHONPATH="$ROOT_DIR/src"

"$VENV_PYTHON" -m unittest discover -s "$ROOT_DIR/tests" -v
"$VENV_PYTHON" -m gifted_masking.cli robustness --suite full --output-dir "$ROOT_DIR/results"
"$VENV_PYTHON" "$ROOT_DIR/scripts/validate_manifest.py" "$ROOT_DIR/results/manifests/robustness_full.json"
"$VENV_PYTHON" "$ROOT_DIR/scripts/recompute_headline_effects.py" \
  "$ROOT_DIR/results/raw/robustness_full_units.csv" \
  "$ROOT_DIR/results/summaries/robustness_full_summary.csv" \
  "$ROOT_DIR/results/summaries/robustness_full_recomputed_effects.csv"
"$VENV_PYTHON" "$ROOT_DIR/scripts/compute_headline_uncertainty.py" \
  "$ROOT_DIR/results/raw/robustness_full_units.csv" \
  "$ROOT_DIR/results/summaries/robustness_full_headline_uncertainty.csv"
"$VENV_PYTHON" "$ROOT_DIR/scripts/benchmark_m2_optimal_policy.py"
"$VENV_PYTHON" "$ROOT_DIR/scripts/map_m2_lock_in_regions.py"
"$VENV_PYTHON" "$ROOT_DIR/scripts/analyze_m2_regimes.py"
"$VENV_PYTHON" -m unittest \
  "$ROOT_DIR/tests/test_manifest_completeness.py" \
  "$ROOT_DIR/tests/test_primary_raw_schema.py" \
  "$ROOT_DIR/tests/test_summary_matches_raw.py" \
  -v
