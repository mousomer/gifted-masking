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
  - E06 uses an isolated M4 continuation-path diagnostic recorder. It uses the
    maintained learner/receptivity helpers in the maintained draw/update order,
    parity-tests local traces against `simulate_from_state`, packs child-level
    segment arrays, validates continuity/reset/bounds/count invariants, and
    refuses standard without an exact canonical GO; qualification is always
    refused by the core-standard route.
  - E06's local recorder additionally retains final-window action, authentic
    acceptance/rejection, objective-reward, and p/Q boundary diagnostics while
    replaying maintained M4 draw/update order. Its strict raw boundary and
    phase-separated capacity probe are experiment-local and do not alter M4.
    `validate_e06_derived` is the shared fail-closed boundary for materialized
    and parsed emitted tables: it requires validated packed raw rows and the
    exact frozen config, reconstructs ordered cells/paths/loops/transitions/
    effects, and rejects altered identities, ordering, cardinalities,
    unavailable smoke inference, or nonfinite/numerically inconsistent values.
    Smoke uses materialized packed rows and retains byte-frozen smoke schemas.
    The second bounded corrective pass reconstructs every ordered raw field
    from config and semantic seeds before derived validation. The subsequent
    standard-readiness design is family-streamed: generate, apply bounded
    first-pass invariants, and append one 400-row path family at a time, retain
    bounded aggregates, and perform an independent full raw-and-cell streaming
    reconstruction before staged package publication with the manifest last.
    Future standard dispatch is fail-closed on a canonical GO record binding
    the exact config, source fingerprint, sealed smoke manifest, and authorized
    command. Standard-only schemas add master-level inference, pooled
    transition/bootstrap records, and master-qualified seed maps. Qualification
    remains separate and unconditionally refused. A field-shaped standard CSV
    size fixture bounds logical raw output at 344.136 MiB: inside the formal
    400-MiB approval stop but outside the later 150-MiB stored-artifact gate.
    The user-authorized standard-only compression amendment changes the future
    primary path to deterministic `.csv.gz` while preserving the exact logical
    55-column CSV. The manifest binds compressed and logical hashes/sizes, and
    a high-entropy exact-cardinality fixture must pass the 150/200-MiB stored
    limits before independent GO review. Smoke remains unchanged.
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

## E06 compression release-gate boundary

The E06 standard preflight authenticates the exact fixture-record hash bound
by the smoke projection and regenerates the full non-scientific fixture in a
unique `/private/tmp` directory before it creates a requested output root.
An experiment-local resource guard checks runtime, RSS, logical CSV bytes,
compressed bytes, and stored bytes throughout production phases. Streaming
replay retains no more than one 400-row expected family. The release projection
is a single componentwise-conservative object, including fixture
authentication. Sealed Git evidence includes dirty-file status, bytes, and
content hash; a future GO additionally binds the exact independent-review
checkpoint path/hash. These are release controls only and do not change M4.
