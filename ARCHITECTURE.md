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
- `src/gifted_masking/experiments/article.py`
  - config-driven, experiment-only Frontiers analyses that call maintained
    model kernels without changing baseline model paths
- `configs/frontiers_article/`
  - explicit smoke and standard article-experiment configurations; standard
    execution remains gated by reviewed smoke checkpoints
  - E01 currently uses a canonical semantic cell ID and a two-component
    `SeedSequence` hierarchy, producing sorted primary rows, summaries,
    diagnostics, and a self-excluding output-hash manifest
  - E02 uses a separate canonical matched-pair seed hierarchy for binary and
    independent graded-disclosure learners.  Its smoke runner forces only the
    initial full-disclosure action after consuming the policy/acceptance draws,
    records paired raw diagnostics, validates exact JSON types and values,
    computes stable-full-policy diagnostics with a linear suffix scan, and
    refuses standard execution without an E02-specific approval record.
  - standard E01 configuration is staged but execution is refused by the
    smoke-only runner until a separate authorized path is added
  - E05 uses an isolated M3 BFLPE crossover kernel with frozen accepted-good-
    authentic-only comparison-cost semantics, architecture-specific matched
    streams across `bf`, strict artifact validation, phase-scaled readiness
    accounting that does not multiply one-time plotting startup by learner
    work, and fail-closed external-verification sealing. Its staged standard
    configuration remains refused pending an E05-specific review
  - E06 uses an isolated M4 continuation-path diagnostic kernel. It delegates
    segment evolution to maintained `simulate_from_state`, packs child-level
    segment arrays, validates continuity/reset/bounds/count invariants, and
    refuses staged standard and qualification configurations until their own
    future approval records exist.
  - E06's local recorder additionally retains final-window action, authentic
    acceptance/rejection, objective-reward, and p/Q boundary diagnostics while
    replaying maintained M4 draw/update order. Its strict raw boundary and
    phase-separated capacity probe are experiment-local and do not alter M4.
    `validate_e06_derived` is the shared fail-closed boundary for materialized
    and parsed emitted tables: it requires validated packed raw rows and the
    exact frozen config, reconstructs ordered cells/paths/loops/transitions/
    effects, and rejects altered identities, ordering, cardinalities,
    unavailable smoke inference, or nonfinite/numerically inconsistent values.
    E06 uses materialized packed rows; no streaming writer exists, and that
    non-applicability is recorded with the frozen raw/RSS capacity rationale.
    The second bounded corrective pass reconstructs every ordered raw field
    from config and semantic seeds before derived validation. Standard dispatch
    remains refused: the canonical package is intentionally unsealed pending a
    new user-owned full verification and a fresh independent smoke review.
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
  - standard repo verification command, pinned to the required shared
    workspace Python rather than a repository-local environment
- `/Users/omer/workspace/venvs/venv314/`
  - required shared workspace environment for Python commands, installs, verification, and experiment runs

### Publication Artifacts

- `doc-reviews/frontiers_submission/`
  - official-template Original Research manuscript for Frontiers in Psychology
  - results-led assertive revision that foregrounds learned suboptimal masking,
    hot-stove persistence, and search burden before later limitations
  - separate 300-dpi RGB figure files
  - manuscript-specific independent-bootstrap estimates
  - author-facing submission and placeholder checklist
- `projects/frontiers_article/`
  - article-development sub-project governed by a Research Design Specification
  - source of truth for claim/evidence gates, the nine-stage delivery workflow,
    manuscript integration, figure planning, and submission readiness
  - does not supersede repository-level authority for model semantics

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
- The shared workspace venv workflow exists and the repo has a single documented
  verification command.
- `AGENTS.md` explicitly requires using `/Users/omer/workspace/venvs/venv314`.
- The Frontiers article sub-project has an explicit RDS, claim ledger, stage
  gates, and completion criteria without changing model semantics.

## E06 second corrective boundary

E06 reconstructs each packed raw row exclusively from frozen config,
scenario/path semantics, child index, and semantic segment seeds before it
accepts materialized or parsed-CSV evidence. The experiment-local external
sealer first reconstructs full-suite counts/runtimes from a strict full log,
requires the sole newline-terminated `verification_exit_code=0` record, and
recomputes config, approval, ordered source fingerprints, Git/dirty binding,
scientific hashes, focused evidence, and deterministic-regeneration evidence.
It updates report item 12 and the manifest atomically only after validation;
it never regenerates scientific artifacts. The canonical package remains
unsealed until the user-owned round-2 verification supplies that evidence.

## Verification and instruction isolation

E06 mechanism tests use disposable copies of the published source/configuration
inputs and Git state. Freshness mutations stay inside those fixtures. These unit
fixtures never refresh, authorize, or seal repository scientific packages; the
existing standard and qualification refusals remain unchanged. M2 deterministic
output tests use temporary result roots and protect canonical output bytes and
timestamps. Production model, reward, RNG, parameter, and evidence rules retain
their existing owners.

AGENTS.md owns its historical-example fence boundaries. Examples are not active
assignments; the shared installer owns only its marker-delimited dispatcher.

## Hosted offline software verification

The GitHub Actions workflow runs the existing `scripts/verify.sh` obligations on
macOS with Python 3.14.8. `GOVERNANCE_PYTHON` selects that hosted interpreter for
both governance and product verification; local execution retains its existing
shared-interpreter default. The selected interpreter must be executable, and a
failed governance hook stops product execution.

The workflow installs only the exact verification dependency pins from
`requirements-ci.txt`, then runs tests and the existing generated robustness
checks. It does not collect private inputs, run model downloads, seal scientific
evidence, or execute separately gated standard/qualification configurations.
`results/` and the full verification log stay on the disposable runner. No cache,
artifact upload, credentials, or secret inputs are configured. The Actions step
log contains only bounded verification status; the disposable hosted runner
holds the full raw log until it is discarded.

Acceptance requires the same complete verifier to pass locally, rejection of an
unavailable interpreter or failed governance hook, and source-only review of the
workflow and dependency pins. A hosted result is additional software evidence;
it does not adjudicate scientific claims or refresh a scientific package.
