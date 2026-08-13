# E06 Codex Instruction Set

**Purpose:** canonical model routing, consumption manifest, prompts, outputs,
and stop conditions for every E06 pass.

## Model routing

| Pass | Task | Model | Effort | Authorization |
| --- | --- | --- | --- | --- |
| A | Scientific design | `gpt-5.6-sol` | `xhigh` | Complete; no run |
| B | Implement and run smoke | `gpt-5.6-terra` | `high` | Smoke only |
| C | Independent smoke audit | `gpt-5.6-sol` | `xhigh` | Review only |
| D | Execute GO-authorized core standard | `gpt-5.6-terra` | `high` | Core standard only |
| E | Adjudicate C8 and C9 eligibility | `gpt-5.6-sol` | `xhigh` | No new run |
| Q-A | Decide qualification GO | `gpt-5.6-sol` | `max` | Only if C9 eligible |
| Q-B | Execute qualification | `gpt-5.6-terra` | `high` | Q00--Q04 only |
| Q-C | Final C9 adjudication | `gpt-5.6-sol` | `max` | No new run |

Pass B is the active next task. Terra/high is appropriate because the science
is frozen and the work is bounded implementation, testing, deterministic
generation, and capacity measurement. Pass C must be a **fresh** Sol/xhigh
task: the implementation task cannot approve its own work. Reserve Sol/max for
the genuinely interpretation-sensitive qualification GO and final hysteresis
decision. Do not use Luna or an auto-selected alias for these passes.

## Consumption rule for every pass

“Consume” means read the complete file directly before acting. A prior summary,
current-state headline, or another agent's interpretation is not a substitute.
Continue truncated reads to EOF.

Every task must first:

1. confirm repository root
   `/Users/omer/workspace/personal/repos/gifted-masking`;
2. confirm Python `/Users/omer/workspace/venvs/venv314/bin/python`;
3. read its mandatory inputs in the listed order;
4. inspect `git status --short` and preserve unrelated changes;
5. state a concise plan and explicit acceptance criteria;
6. record any authority conflict before changing or running anything.

No pass inherits authorization from a previous pass. Smoke, core standard, and
qualification require separate exact authorization records.

## Pass B — active implementation and smoke task

The original Pass B smoke received `FIX_IMPLEMENTATION`. The active corrective
handoff is now governed by `E06_FIX_IMPLEMENTATION_CODEX_INSTRUCTIONS.md` and
stops before user-owned full repository verification. Where the original Pass B
instructions conflict with that corrective boundary, the corrective document
controls.

### Model

```text
gpt-5.6-terra
reasoning effort: high
mode: standard
```

### Mandatory governance documents — read fully in order

1. `AGENTS.md`
2. `projects/frontiers_article/E06_CODEX_INSTRUCTION_SET.md`
3. `projects/frontiers_article/RDS.md`
4. `projects/frontiers_article/STAGE2_EXPERIMENT_SPECIFICATIONS.md`
5. `projects/frontiers_article/CLAIM_LEDGER.md`
6. `projects/frontiers_article/CURRENT_STATE.md`
7. `projects/frontiers_article/approvals/E06_SMOKE_APPROVAL.md`
8. `projects/frontiers_article/runbooks/E06_OPERATIONAL_INSTRUCTIONS.md`
9. `ARCHITECTURE.md`
10. repository-root `CURRENT_STATE.md`
11. repository-root `BACKLOG.md`

`AGENTS.md` controls safety and verification. The E06 approval controls exact
science. The operational instructions control implementation order and output.

### Mandatory implementation context — inspect before editing

- `src/gifted_masking/core.py`
- `src/gifted_masking/models/m4.py`
- `src/gifted_masking/repro.py`
- `src/gifted_masking/cli.py`
- `src/gifted_masking/experiments/article.py`
- `src/gifted_masking/experiments/e05.py`
- `src/gifted_masking/experiments/robustness.py`
- `tests/test_core.py`
- `tests/test_m4.py`
- `tests/test_determinism.py`
- `tests/test_reproducibility.py`
- `tests/test_robustness.py`
- `tests/test_article_e05.py`
- `scripts/verify.sh`
- `pyproject.toml`

E05 is an infrastructure pattern only. Do not import its scientific
assumptions, decreasing-PAVA direction, action semantics, or authorization.

### Prior evidence to inspect but never treat as E06 evidence

- `results/summaries/robustness_full_recomputed_effects.csv`, rows
  `mask_path_gap` and `receptivity_path_gap`;
- M4 path rows in `results/raw/robustness_full_units.csv`;
- `higher_entrenchment_increases_masking` in
  `doc-reviews/frontiers_submission/data/manuscript_effect_estimates.csv`;
- `doc-reviews/frontiers_submission/figures/Figure_4_m4_ramp_paths.tif`;
- E05 smoke manifest/report only as sealing and capacity examples.

Do not copy prior values into E06 outputs, modify these artifacts, or claim
that they satisfy E06.

### Pass B must create

- `configs/frontiers_article/e06_m4_paths_smoke.json`
- `configs/frontiers_article/e06_m4_paths_standard.json`
- `configs/frontiers_article/e06_m4_hysteresis_qualification.json`
- an isolated E06 experiment module;
- a focused E06 test module;
- the minimal CLI route required by the approved experiment.

Standard and qualification configs must remain non-executable without their
different future approval records.

### Authorized work

- implement the exact E06 smoke infrastructure and tests;
- run small deterministic and unit checks;
- execute the exact smoke;
- independently regenerate the smoke in a fresh directory;
- run targeted tests and `./scripts/verify.sh`;
- seal smoke artifacts, provenance, and resource projections;
- update architecture/state/backlog/execution documentation.

### Prohibited work

- modifying maintained M4 semantics, defaults, or legacy artifacts;
- adding, dropping, or tuning scientific cells;
- running core standard, qualification, or extra ramps;
- adjudicating C8/C9 or updating their ledger evidence;
- editing article prose or replacing Figure 4;
- calling any smoke loop hysteresis;
- self-authorizing standard execution.

### Pass B completion

Stop at `PENDING_SOL_SMOKE_REVIEW`. The final response must report files,
diffstat, focused/full verification, artifact paths/counts/hashes,
runtime/storage/RSS, core and qualification projections, warnings, and explicit
confirmation that no standard or qualification run occurred.

### Copy-ready Pass B prompt

```markdown
Implement and execute E06 Pass B only.

Use gpt-5.6-terra with high reasoning in standard mode.
Repository: /Users/omer/workspace/personal/repos/gifted-masking
Python: /Users/omer/workspace/venvs/venv314/bin/python

First read `projects/frontiers_article/E06_CODEX_INSTRUCTION_SET.md` completely,
then consume every Pass B governance document, source file, test, and prior-
evidence input in its listed order. Do not act from summaries.

Implement only `projects/frontiers_article/approvals/E06_SMOKE_APPROVAL.md`,
following `projects/frontiers_article/runbooks/E06_OPERATIONAL_INSTRUCTIONS.md`.
Add the exact configs, isolated runner, packed raw output, strict validators,
raw-to-derived reconstruction, loop/transition estimators, synthetic standard-
inference tests, CLI route, and focused tests. Execute only
`frontiers_m4_path_diagnostics_v1_smoke`. Independently regenerate it, run
focused verification and `./scripts/verify.sh`, seal provenance, update project
documentation, and stop at `PENDING_SOL_SMOKE_REVIEW`.

Do not modify maintained M4 semantics or prior artifacts. Do not run standard,
qualification, extra cells, C8/C9 adjudication, ledger updates, article edits,
or Figure 4 replacement. Do not call smoke output hysteresis.
```

## Pass C — independent smoke-gate audit

### Model

```text
gpt-5.6-sol
reasoning effort: xhigh
mode: standard
fresh task: required
```

### Consume

Read all Pass B governance documents and implementation context, then read:

1. `projects/frontiers_article/STAGE2_EXECUTION_LOG.md`;
2. the final E06 checkpoint in `CURRENT_STATE.md`;
3. every E06 source, config, and test file created by Pass B;
4. the sealed smoke manifest, report, warnings log, and every summary table;
5. representative and adversarially selected packed raw rows.

### Independently verify

- approval/config/source/artifact hashes;
- maintained M4 forced and stochastic replay;
- reward--Q--receptivity order;
- inherited state continuity and all reset boundaries;
- segment seeds and inherited/reversal pairing;
- packed arrays, counts, rates, p/Q state, bounds, and finiteness;
- raw reconstruction of every derived table;
- loop-area sign/scale on manual and synthetic curves;
- transition interpolation, plateau, censoring, and invalid inputs;
- standard-only bootstrap logic on synthetic curves;
- fresh-process deterministic regeneration;
- core-standard capacity projection and all resource limits;
- focused/full verification and preservation of prior artifacts.

Return exactly one:

- `GO_STANDARD`
- `FIX_IMPLEMENTATION`
- `REVISE_SPECIFICATION`
- `NARROW_OR_STOP_CLAIM`

A GO must create `approvals/E06_STANDARD_GO.md` with exact hashes, scenarios,
seeds, counts, limits, and command. It may authorize only the unchanged core
standard and must explicitly refuse qualification.

### Copy-ready Pass C prompt

```markdown
Perform the independent E06 Pass C smoke-gate audit.

Use a fresh gpt-5.6-sol task with xhigh reasoning in standard mode. First read
`projects/frontiers_article/E06_CODEX_INSTRUCTION_SET.md` completely, then
consume every Pass C source and artifact it lists. Audit against
`approvals/E06_SMOKE_APPROVAL.md`; do not trust the report without independent
replay, reconstruction, adversarial mutation, fresh regeneration, provenance,
verification, and capacity checks.

Do not run standard or qualification. Return exactly `GO_STANDARD`,
`FIX_IMPLEMENTATION`, `REVISE_SPECIFICATION`, or `NARROW_OR_STOP_CLAIM`. A GO
may authorize only the unchanged core standard and must refuse qualification.
```

## Pass D — exact core standard execution

### Model

`gpt-5.6-terra`, high reasoning, standard mode.

Do not start unless canonical `E06_STANDARD_GO.md` exists and its approval,
config, and source hashes match. Read all Pass B inputs, the complete Pass C
record, smoke artifacts, and GO. Recompute authorization hashes before
dispatch.

Execute the exact core standard unchanged. Produce all frozen artifacts,
reconcile raw-to-derived output, run post-artifact and full verification, seal
provenance, and stop at `PENDING_SOL_STANDARD_REVIEW`. Do not run qualification,
change scenarios, adjudicate claims, update the ledger, or edit the article.

## Pass E — C8 adjudication and C9 eligibility

### Model

Fresh `gpt-5.6-sol`, xhigh reasoning, standard mode.

Read all governing documents, the core GO, implementation/tests, complete
standard manifest/report, every raw/derived artifact, and C8/C9 ledger entries.
Independently reconstruct decision inputs and apply Sections 12 and 13 of the
E06 approval without tuning or new simulation.

Return one C8 disposition:

- `SUPPORTED`
- `SUPPORTED_IN_NARROW_DOMAIN`
- `DESCRIPTIVE_ONLY`
- `NOT_SUPPORTED`
- `IMPLEMENTATION_INVALID`

Separately return C9 as `ELIGIBLE_FOR_QUALIFICATION` or `REMAINS_EXCLUDED`.
Update C8/C9 and project checkpoint documents only after adjudication. Do not
edit article prose. Eligibility does not authorize qualification.

## Qualification route

### Q-A — qualification GO

Use a fresh `gpt-5.6-sol/max` task. Consume the complete core evidence and
adjudication, verify every C9 eligibility predicate, and review a fresh
resource projection. Issue the exact separate GO or keep C9 excluded. Do not
run the qualification package.

### Q-B — qualification execution

Use `gpt-5.6-terra/high`. Consume the qualification GO and all governing
sources. Execute only Q00--Q04 unchanged, verify, seal, and stop for review.
Do not adjudicate.

### Q-C — final C9 adjudication

Use a fresh `gpt-5.6-sol/max` task. Independently reconstruct core and
qualification evidence and apply the long-horizon/material-decay rule. Maximum
positive wording is “hysteresis in the frozen M4 continuation experiment.”
Otherwise retain schedule-specific or transient path-dependence wording and
keep human irreversibility/entrenchment excluded.

## Non-authoritative context

These never override the E06 contract:

- assistant summaries;
- old Figure 4 captions;
- the legacy function name `hysteresis_experiment`;
- the old single-seed path-gap interval;
- manuscript language predating E06;
- smooth visual loops;
- a theoretically desirable outcome.

The function name is not evidence. A smooth loop is not evidence. A nonzero
single-schedule gap is not hysteresis. The frozen decision rules control.
