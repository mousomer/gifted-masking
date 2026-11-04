# gifted-masking

This repository contains reinforcement-learning simulations for masking,
authenticity, stigma, peer-group search, and endogenous receptivity in gifted
children.

The original simulation scripts remain in:

- `simulations1/masking_rl.py`
- `simulations2/masking_rl.py`
- `simulations3/masking_rl.py`

Those files are preserved as legacy reference artifacts. New development lives
in the `src/gifted_masking` package, which separates:

- model mathematics and simulation kernels,
- robustness and perturbation experiments,
- plotting and figure generation,
- reproducibility and result-manifest tooling.

## Design Source Of Truth

The current source of truth for model semantics is:

1. `AGENTS.md`
2. the preserved legacy scripts under `simulations1` to `simulations3`
3. `ARCHITECTURE.md`

The new package is intended to reproduce the legacy behavior while making the
models testable and easier to perturb.

Article development is governed separately by
`projects/frontiers_article/RDS.md`. That RDS controls manuscript scope,
claim/evidence gates, figures, and submission delivery, but it does not override
the model-semantics sources above.

## Local Setup

The required shared workspace environment is
`/Users/omer/workspace/venvs/venv314`. Confirm it is available with:

```bash
/Users/omer/workspace/venvs/venv314/bin/python --version
```

This repository expects all normal Python work to run from the shared workspace
environment. Using system Python directly is unsupported except to repair that
environment.

If the repository package needs to be installed or refreshed in that
environment, use:

```bash
/Users/omer/workspace/venvs/venv314/bin/python -m pip install -e .
```

Activate it:

```bash
source /Users/omer/workspace/venvs/venv314/bin/activate
```

Install optional plotting support if needed:

```bash
python -m pip install ".[plot]"
```

## Verification

Run the full verification flow:

```bash
./scripts/verify.sh
```

That command runs:

- unit and integration tests with `unittest`,
- RNG determinism tests,
- robustness suites covering smoke checks, M3 ablation summaries, and an M4
  hysteresis-style path experiment,
- machine-readable manifests and reports under `results/`.

## Legacy Figure Regeneration

The maintained figure generation path is:

```bash
python -m gifted_masking.cli legacy-figures --output-dir results/figures
```

If `matplotlib` is not installed, the command will fail fast with a clear
message. Core simulations do not import plotting dependencies at module import
time.

## Review And Research Notebook

`notebooks/review_and_research.ipynb` brings review of every test, model rung
(M0-M4), article experiment (E01-E06), robustness check and manifest together in
one place, with a small simulation sandbox. It is read-only with respect to the
repository: it never writes to `results/` and never changes model semantics.
Open it with the `venv314` kernel:

```bash
/Users/omer/workspace/venvs/venv314/bin/python -m jupyter lab notebooks/review_and_research.ipynb
```

The notebook needs `pandas`, `matplotlib` and `jupyterlab`, which are
notebook-only dependencies already present in the workspace venv. Its helpers
live in `notebooks/review_lib.py` (stdlib and numpy only) and are covered by
`tests/test_review_notebook.py`. The default run takes about two minutes. The
committed notebook has no outputs.

## Repository Layout

```text
src/gifted_masking/
  core.py
  params.py
  repro.py
  models/
  experiments/
  plotting/
tests/
scripts/
notebooks/
results/
projects/frontiers_article/
```
