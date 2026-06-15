# Architecture

## Purpose

Convert the repository from a set of notebook-style scripts into a buildable
simulation package without deleting the original scripts or changing model
semantics by accident.

## Comparison Against Current Design Source Of Truth

The existing design source of truth is the combination of `AGENTS.md` and the
legacy simulation scripts. Those scripts currently mix:

- model definitions,
- simulation kernels,
- plotting,
- figure orchestration,
- and implicit reproducibility assumptions.

The new architecture keeps the same model ladder but separates responsibilities
so the scientific claims can be tested directly.

## Target Structure

### Legacy Preservation

- Keep `simulations1/`, `simulations2/`, and `simulations3/` unchanged.
- Treat them as preserved reference implementations and artifact snapshots.

### Maintained Package

- `src/gifted_masking/core.py`
  - shared numerics, validation, sampling, uncertainty helpers
- `src/gifted_masking/params.py`
  - validated dataclasses for learner and experiment parameters
- `src/gifted_masking/models/`
  - one module per model rung: `m0` through `m4`
- `src/gifted_masking/experiments/robustness.py`
  - perturbation suites, M3 ablation summaries, M4 hysteresis-path summaries,
    manifests, report generation
- `src/gifted_masking/plotting/legacy_figures.py`
  - figure generation only, with lazy `matplotlib` imports
- `src/gifted_masking/repro.py`
  - run metadata, environment snapshot, artifact manifest writing

### Verification

- `tests/`
  - formula checks,
  - transition checks,
  - RNG determinism checks,
  - perturbation smoke checks,
  - M3 ablation coverage,
  - M4 hysteresis experiment coverage,
  - artifact-generation smoke coverage
- `scripts/verify.sh`
  - standard repo verification command
- `.venv/`
  - required local execution environment for Python commands and installs

## Dependency Policy

Base runtime:

- `numpy`
  - required for vectorized simulation kernels

Optional plotting:

- `matplotlib`
  - only required for figure generation
  - kept optional so core tests can run without it

Avoided for now:

- `pandas`
  - avoided to keep the repo lightweight; CSV and JSON are sufficient
- `scipy`
  - avoided because current verification needs do not require it
- `pytest`
  - avoided because `unittest` is sufficient and has zero extra dependency cost

## Acceptance Criteria

- Legacy scripts remain present.
- Core simulations are importable without `matplotlib`.
- Each model has direct tests for mathematical or transition-level invariants.
- A robustness suite runs parameter perturbations and emits reproducibility
  artifacts under `results/`.
- The maintained suite includes M3 action-space ablations and an explicit M4
  ramp-up/ramp-down path experiment.
- A local `.venv` workflow exists and the repo has a single documented
  verification command.
- `AGENTS.md` explicitly requires using the repo-local `.venv`.
