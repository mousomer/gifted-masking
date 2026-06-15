# Robustness Infrastructure Notes

## Baseline Verification Before Changes

| Field | Value |
| ----- | ----- |
| Command | `./scripts/verify.sh` |
| Working directory | `/Users/omer/workspace/test-code/gifted-masking` |
| Exit code | `0` |
| Test count | `34` |
| Runtime | about `6.764s` wall time |
| Generated artifacts | `results/raw/robustness_full.csv`, `results/summaries/robustness_full_summary.csv`, `results/reports/robustness_full_report.md`, `results/manifests/robustness_full.json` |
| Git status before changes | unavailable; directory is not a git repository |

## Current Artifact-Generation Path

| File/module | Function/class | Role | Current output rows | Current output granularity | Proposed change |
| ----------- | -------------- | ---- | ------------------: | -------------------------- | --------------- |
| `src/gifted_masking/experiments/robustness.py` | `generate_unit_rows` | Runs existing model simulations and emits primary units | `5008` for full suite | matched child-level units for most effects; matched ramp-grid units for M4 path gaps | Implemented as new primary raw source |
| `src/gifted_masking/experiments/robustness.py` | `summarize_unit_rows` | Derives headline summaries from primary units | `13` | one row per headline effect | Implemented; summaries no longer need independent in-memory-only arrays |
| `src/gifted_masking/experiments/robustness.py` | `write_suite` | Writes robustness artifacts and manifest | `13` summary rows plus `5008` unit rows | mixed: compatibility summary and primary raw units | Implemented; existing filenames preserved |
| `results/raw/robustness_full.csv` | compatibility artifact | Legacy summary-level raw path | `13` | one row per headline effect | Preserved; no longer treated as primary raw |
| `results/raw/robustness_full_units.csv` | primary raw artifact | Recomputable unit-level data | `5008` | per matched unit | New canonical primary raw artifact |
| `results/summaries/robustness_full_summary.csv` | headline summary | Headline effects and CIs | `13` | one row per headline effect | Derived from primary raw units |
| `results/manifests/robustness_full.json` | manifest | Reproducibility metadata | n/a | run metadata | Expanded with seeds, parameter grids, `n`, `T`, final window, artifact paths |

Current `results/raw/robustness_full.csv` rows are one row per headline effect.
They are not per model, condition, parameter cell, seed, or child. The new
primary unit file is `results/raw/robustness_full_units.csv`.

## Implemented Checks

- `scripts/validate_manifest.py` validates manifest completeness.
- `scripts/recompute_headline_effects.py` recomputes headline values from
  primary raw units and fails on mismatches.
- `scripts/compute_headline_uncertainty.py` computes headline CIs from primary
  raw units.
- `tests/test_manifest_completeness.py` covers required manifest fields.
- `tests/test_primary_raw_schema.py` covers primary raw schema and granularity.
- `tests/test_summary_matches_raw.py` covers raw-to-summary recomputation and
  uncertainty output.

## Remaining Infrastructure Limits

- M4 ramp path uncertainty still uses seven matched ramp-grid units, not
  replicated master seeds.
- The repo is not a git repository, so the manifest records an explicit
  unavailable commit reason.
- The manifest records package versions for core dependencies, but not a full
  locked environment.
