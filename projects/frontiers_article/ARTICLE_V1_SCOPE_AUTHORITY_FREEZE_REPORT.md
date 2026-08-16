# Article V1 Scope and Authority Freeze — Execution Report

**Date:** 16 August 2026

**Result:** `READY_FOR_SHORT_ARTICLE`

## Task classification

```text
TASK TYPE:
Documentation / manuscript governance / evidence-authority reconciliation.

SCIENTIFIC STATUS:
No new experiment.
No new numerical inference.
No model change.
No result regeneration.
No artifact modification.

ARTICLE SCOPE:
Primary Article V1 = E01–E05.
E06/M4 = deferred future work.

TARGET END STATE:
READY_FOR_SHORT_ARTICLE
```

## Repository state

| Item | Recorded state |
|---|---|
| Starting branch | `codex/frontiers-stage2-e06` |
| Starting HEAD | `1217847c29365a293559c816a3ce6ef69e51c4e6` |
| Historical handoff HEAD | `ea46c9d9bbd39c1bfcd84a9b818d7bd16e30bf32` |
| Difference | Actual HEAD had advanced by later documentation commits; work continued from actual state. |
| Starting worktree | Clean (`git status --short` returned no paths). |
| Ending worktree | Documentation/governance changes listed by `git status --short`; no code, config, artifact, raw result, or figure-data path changed. |

No reset, checkout, clean, stash, discard, commit, or push was performed.

## Authority result

```text
PRIMARY ARTICLE V1 = E01–E05 ONLY
E06/M4 = DEFERRED
STATUS = READY_FOR_SHORT_ARTICLE
```

The RDS, manuscript evidence freeze, current state, handoff, master plan,
next-stage pointer, authority index, and backlog now agree. The next task is the
article skeleton and claim/evidence/figure map, not prose drafting. The article
target is 6,000–8,000 main-text words, including 1,200–1,600 words of main
Methods, approximately four to five main figures, and a conclusion of no more
than two paragraphs. The long Formal Model and Methods authority remains
preserved for later main/supplementary/technical separation.

## Duplicate consistency-audit authority

Three copies exist:

| Path | SHA-256 | Status |
|---|---|---|
| `ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md` | `d93adeec7def0c02b402519dfb3744c2f1f19da86c5aee76686617b5b96dfa6e` | Byte-identical |
| `projects/frontiers_article/ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md` | `d93adeec7def0c02b402519dfb3744c2f1f19da86c5aee76686617b5b96dfa6e` | Byte-identical |
| `doc-reviews/handoff_august2026/Gifted_Masking_Article_V1_Handoff_Pack_REVISED_2026-08-15/ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md` | `d93adeec7def0c02b402519dfb3744c2f1f19da86c5aee76686617b5b96dfa6e` | Byte-identical archived snapshot |

The project-directory copy is canonical for Article V1 routing because it sits
inside the active authority directory and is linked by the authority index.
The root copy is an identical convenience authority; the handoff-pack copy is
immutable provenance. No copy was deleted or silently consolidated.

## Contamination audit and corrections

| Pattern or claim | Classification | Action |
|---|---|---|
| Legacy E03 `226/357`, `63.3%`, and `.950` in Results/Discussion/revision notes | `HISTORICAL / EXPLICITLY STALE` after this stage | Added conspicuous non-authority banners. Values were preserved as historical text, not mechanically replaced. Active routing forbids their use. |
| `226/357` in consistency audits, old execution records, approvals, and provenance documents | `ACTIVE AND CORRECT` when documenting the legacy replay, otherwise `NON-MANUSCRIPT / IRRELEVANT` | Preserved; these passages explicitly distinguish legacy provenance from the Article V1 result. |
| E03 `243/357` | `ACTIVE AND CORRECT` | Preserved with the aggregate final-window Neutral-action, visit-adequacy, tested-grid, non-prevalence definition and `n=160`, `T=1000` boundary. |
| E05 temperature/G2 exclusion inside `ARTICLE_V1_E05_INTERPRETATION.md` | `ACTIVE AND NEEDS CORRECTION` | Added a binding top-of-file supersession notice. The evidence freeze/audit now explicitly govern; the demonstrated displacement remains, while quantitative decomposition is unresolved. |
| Correct binary-softmax lemmas in the analytic authority | `ACTIVE AND CORRECT` | Preserved because they are explicitly scoped away from the E05 modal-classification fraction. |
| Non-unit `lambda` sensitivity claims | `ACTIVE AND CORRECT` when labelled E01/E03 sensitivity | Preserved. Active routing now states that all headline E01–E05 configurations use `lambda=1` and forbids loss-aversion explanations of headline results. |
| E06/M4 mathematical or programme material | `ACTIVE AND CORRECT` only as future/Track-B context, otherwise `HISTORICAL / EXPLICITLY STALE` | Primary scope was frozen to E01–E05. Historical E06 material remains intact and was not scientifically re-audited or deleted. |
| E04 “settling/settled” | `ACTIVE AND CORRECT` only where defined as final-window argmax classification | Brief/current-state/handoff prefer the exact classification wording and require a definition wherever shorthand is used. |
| Hysteresis, bistability, irreversible, or self-maintaining language | `ACTIVE AND CORRECT` only as a prohibition, limitation, or deferred research question; historical otherwise | No such claim was admitted to primary Article V1 evidence. |

## Provenance statement retained

Frozen standard result artifacts and their recorded hashes are preserved and
pass deterministic validation. Exact historical generator-source
reconstruction is available for E04 and E05. The precise uncommitted generator
state used for E01–E03 was not fully retained, limiting exact source-level
regeneration from Git alone. This does not invalidate the frozen numerical
results and does not authorize replacement runs.

## Validation

- `git branch --show-current`, `git rev-parse HEAD`, `git status --short`, and
  `git log -5 --oneline`: recorded actual start state.
- `shasum -a 256` plus `cmp -s` across the three consistency-audit copies:
  all hashes equal and byte comparisons passed.
- Targeted `rg` searches for the requested contamination patterns: reviewed and
  classified; no blind replacements performed.
- Read-only checks through the repository publication helper using
  `/Users/omer/workspace/venvs/venv314/bin/python`: `33/33` protected outputs
  valid and `18/18` evidence-matrix referenced files valid.
- `git diff --check`: passed after removing one trailing-space defect.
- Full diff review: documentation/governance paths only; no code, config,
  artifact, raw data, result, or figure-source-data modifications.

The full experiment suite and deterministic publication build were not run,
because this stage is documentation-only and the build would rewrite generated
publication outputs. No research output was regenerated.

## Unexpected issues

The actual starting HEAD differed from the historical handoff reference. The
active RDS also retained an 8,000–9,000-word/M0–M4 programme target while the
scientific freeze already bounded Article V1 to E01–E05, and the current-state
documents routed the next task to a standalone Results authority. These were
editorial/governance contradictions, not scientific contradictions. They were
reconciled to the user-authorized short-article scope.

No unresolved contradiction was found between the evidence matrix and the two
byte-identical active consistency-audit copies. The E05 interpretation-note
conflict was already identified by both governing authorities and is now
conspicuously superseded at its source.
