# E06 Operational Instructions

**Current authorized substage:** Pass B implementation and diagnostic smoke  
**Scientific authority:** `approvals/E06_SMOKE_APPROVAL.md`  
**Required implementation model:** `gpt-5.6-terra`, high reasoning  
**Required smoke reviewer:** fresh `gpt-5.6-sol`, xhigh reasoning

The canonical model routing and per-pass consumption manifest are in
`../E06_CODEX_INSTRUCTION_SET.md`. Every E06 execution or review task must read
that file completely before using this runbook.

## Objective

Implement the isolated E06 M4 continuation-path experiment exactly as frozen,
execute only its diagnostic smoke, verify and seal the resulting package, and
stop for independent smoke-gate review.

The purpose of this pass is to prove that inherited state, reset controls,
RNG pairing, path alignment, loop estimators, transition censoring, packed raw
rows, and capacity projections are correct. The smoke cannot support C8 or C9.

## Required reading order

Read completely before making changes:

1. repository `AGENTS.md`;
2. `projects/frontiers_article/RDS.md`;
3. `projects/frontiers_article/STAGE2_EXPERIMENT_SPECIFICATIONS.md`;
4. `projects/frontiers_article/approvals/E06_SMOKE_APPROVAL.md`;
5. C8 and C9 in `projects/frontiers_article/CLAIM_LEDGER.md`;
6. `projects/frontiers_article/CURRENT_STATE.md`;
7. `src/gifted_masking/models/m4.py`;
8. `tests/test_m4.py` and maintained robustness M4 code/tests;
9. article experiment/reproducibility infrastructure from E01--E05.

If any conflict remains after applying that authority order, stop with
`REVISE_SPECIFICATION`. Do not resolve scientific ambiguity in implementation.

## Allowed work

1. Add the three exact E06 configs required by the approval record.
2. Add an isolated E06 experiment module and CLI route.
3. Add pure loop-area, monotone-transition, bootstrap, validation, and
   raw-to-derived reconstruction helpers needed only by E06.
4. Add focused E06 tests.
5. Execute exactly the approved E06 smoke.
6. Produce and seal its raw, summary, figure, manifest, report, and warnings
   artifacts.
7. Update architecture/state/backlog/execution documentation for the smoke
   implementation and checkpoint.

## Prohibited work

1. Do not modify `models/m4.py`, its defaults, update order, or RNG behavior.
2. Do not modify legacy scientific artifacts or the article's current Figure 4.
3. Do not execute the staged standard or qualification configs.
4. Do not reduce or add standard scenarios based on smoke behavior.
5. Do not run extra ramps, horizons, seeds, or parameter searches.
6. Do not adjudicate C8 or reconsider C9.
7. Do not update claim-ledger evidence, article prose, or the manuscript DOCX.
8. Do not use child-level resampling as independent inference.
9. Do not call any diagnostic loop “hysteresis.”

## Implementation order

1. Record a concise plan and acceptance criteria in the execution log.
2. Add strict duplicate-key/type-aware config loading and all three frozen
   configs; standard and qualification must default to non-executable.
3. Implement the exact seed hierarchy and segment pairing.
4. Implement packed primary rows with full state continuity/reset evidence.
5. Implement fail-closed raw validation.
6. Implement raw-to-derived reconstruction for cells, paths, loops, effects,
   and transitions.
7. Implement signed/absolute trapezoidal areas and synthetic tests.
8. Implement nondecreasing PAVA transition inversion and censoring tests.
9. Implement standard-only five-seed/10,000-bootstrap helpers using synthetic
   test curves; do not execute standard inference on smoke as if inferential.
10. Implement deterministic streaming/serialization and capacity projection.
11. Run focused E06 and M4 regression tests.
12. Execute the exact smoke once, inspect artifacts, independently regenerate
    it in a fresh directory, and compare normalized artifacts and hashes.
13. Run `./scripts/verify.sh` with the required workspace environment.
14. Reseal the manifest/report only after final source and verification state.
15. Stop at `PENDING_SOL_SMOKE_REVIEW`.

## Acceptance criteria

The implementation pass is complete only when:

- maintained stochastic and forced M4 replay matches exactly;
- reward--Q--receptivity update order is demonstrated;
- inherited state continuity and every reset boundary validate;
- inherited/reversal semantic segment seeds match exactly;
- global RNG and execution order do not affect results;
- every p value stays within bounds and recorded violations are zero;
- all packed counts, rates, states, Q-values, and array lengths reconcile;
- raw tables reconstruct every derived table exactly;
- synthetic loop and transition estimators pass all boundary cases;
- smoke rows and learner-step count equal 320 and 345,600;
- standard rows and learner-step projection equal 52,000 and 913,000,000;
- standard/qualification dispatch is refused without their exact future GO;
- same- and cross-directory smoke regeneration is deterministic;
- source fingerprint, output hashes, command, environment, and verification
  state are complete;
- the fresh-process standard projection satisfies or explicitly fails every
  frozen resource gate;
- the checkpoint contains all 13 required items and makes no scientific claim.

## Required final handoff

Report:

- files changed and diffstat;
- focused and full verification results;
- exact smoke artifact paths, row counts, hashes, runtime, storage, and RSS;
- standard and qualification projections;
- any warnings or deviations;
- confirmation that no maintained semantics or prior artifacts changed;
- final status `PENDING_SOL_SMOKE_REVIEW`.

Do not recommend `GO_STANDARD` in the implementation pass. That decision
belongs to the independent Sol smoke-gate reviewer.

## Copy-ready Pass B task

```markdown
Implement and execute only E06 Pass B under
`projects/frontiers_article/approvals/E06_SMOKE_APPROVAL.md` and
`projects/frontiers_article/runbooks/E06_OPERATIONAL_INSTRUCTIONS.md`.

Use `/Users/omer/workspace/venvs/venv314/bin/python`. Preserve maintained M4
semantics and all prior scientific artifacts. Add the exact configs, isolated
runner, strict packed-row and derived validators, loop/transition estimators,
synthetic standard-inference tests, CLI route, and E06 tests. Execute only
`frontiers_m4_path_diagnostics_v1_smoke`; independently regenerate it, run
focused tests and `./scripts/verify.sh`, seal provenance, update checkpoint
documentation, and stop at `PENDING_SOL_SMOKE_REVIEW`.

Standard, qualification, C8/C9 adjudication, claim-ledger changes, manuscript
edits, and extra simulation cells are prohibited.
```

## Copy-ready Pass C task

```markdown
Independently review the sealed E06 diagnostic smoke against
`projects/frontiers_article/approvals/E06_SMOKE_APPROVAL.md`.

Audit maintained M4 replay, reward/Q/receptivity order, inherited continuity,
reset controls, segment RNG pairing, packed raw semantics, raw-to-derived
reconstruction, loop/transition estimators, deterministic regeneration,
provenance, verification, and reproducible standard capacity. Run adversarial
checks rather than trusting the report. Do not run standard or change code
unless returning an implementation-fix specification.

Return exactly one: `GO_STANDARD`, `FIX_IMPLEMENTATION`,
`REVISE_SPECIFICATION`, or `NARROW_OR_STOP_CLAIM`. A GO must be written as a
canonical E06-specific standard authorization and may authorize only the
unchanged core standard, never the qualification tier.
```
