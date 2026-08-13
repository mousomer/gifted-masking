# E06 independent smoke-gate review

**Decision:** `FIX_IMPLEMENTATION`  
**Date:** 2026-08-13  
**Scope:** corrected diagnostic smoke and user-owned full-verification evidence  
**Standard:** refused  
**Qualification:** refused

## Authority and verification binding

The review used `AGENTS.md`, the E06 instruction and corrective records, and
`approvals/E06_SMOKE_APPROVAL.md` as the design source of truth. The current
approval SHA-256 is
`9fc0434c86da23815afc3327f79c0e9824918417839aadda39dc1ba061cb76f7`;
the normalized smoke-config SHA-256 is
`475a8630acc73ab21520fd90024f85712b0002aec52d39d18e74e96cb8e4c40b`;
and the independently recomputed current source fingerprint is
`8b404d6cb3493d48c2469881e798772ff93bd415caaeec64b0e41beec734e4a6`.
All match the preverification package and canonical smoke manifest. No
fingerprinted source/config/approval path was newer than the user verification
log.

The user-owned verification evidence is valid:

- result log:
  `results/reports/e06_preverification_logs/user_full_repository_verification.log`;
- log SHA-256:
  `ce9ebaaf2278e2bc1f058355129de29b1af0705a9ccc1171f99e848ee9745749`;
- exit record:
  `results/reports/e06_preverification_logs/user_full_repository_verification_exit.txt`;
- exit-record SHA-256:
  `e0eb8bd605bbfaa0c7eac5a1e11fd892eb29a2831a8b8f3601c2e5d01f410063`;
- exit code: `0`;
- repository discovery suite: 113 tests passed in 128.937 seconds;
- post-artifact suites: 1, 1, and 2 tests passed in 1.937, 1.956, and
  3.861 seconds.

The full log names the required workspace Python and contains no failed or
errored suite. This validates the user-owned repository gate, but it does not
override the independent adversarial failure below.

## Evidence that passed

1. The raw artifact contains 320 ordered packed rows and 55 columns. Independent
   reconstruction found 43,887 mask actions, 25,233 authentic actions, 22,608
   accepted-authentic outcomes, 2,625 rejected-authentic outcomes, and zero
   recorded post-update bounds violations. Every final-window count, mask rate,
   and objective reward reconciled.
2. Source inspection and replay confirm softmax action, one acceptance draw per
   learner including masking, objective reward from pre-update receptivity,
   selected-Q update, then receptivity update and clipping. Focused parity tests
   against maintained M4 passed for `km=0` and positive `km`, multiple seeds,
   reset/inherited starts, and the ceiling final-window convention.
3. Independent reconstruction of canonical rows confirmed the semantic segment
   seed derivation, inherited/reversal seed reuse, direction isolation, inherited
   p/Q continuity, all reset boundaries, and final packed state.
4. All five derived tables reconstruct exactly from the unaltered validated raw
   rows. The loop, transition, PAVA, five-seed Student-t, bootstrap-seed, and
   10,000-replicate synthetic helpers passed their focused checks. Smoke
   intervals remain blank and every decision-bearing field remains ineligible.
5. Two fresh CLI processes used separate output roots and Matplotlib cache
   directories. Raw, cells, paths, loops, transitions, effects, PNG, and warnings
   were byte-identical to canonical and to each other. The conservative maximum
   core projection was 198.137 seconds, 126.661 MiB raw, 140.829 MiB total, and
   129.281 MiB peak RSS, within all frozen limits.
6. Standard and qualification CLI dispatch both refused with `PermissionError`.
   No standard or qualification artifact was created. Thirty-three recorded
   E01--E05 scientific artifacts still match their canonical manifest hashes.

## Blocking findings

### Blocker — packed raw validation is not fail-closed

**Location:** `src/gifted_masking/experiments/e06.py`,
`validate_e06_raw`, especially the partial checks around lines 246--277.

**Evidence:** direct mutations were accepted for `scenario_role`,
`matched_family_id`, the complete policy/environment seed map, `child_seed`,
`rng_unit`, declared `n`, final-window start/end, `ka`, `km_mode`, the declared
nominal grid, `alpha`, inherited authentic-Q continuity, disabled-reversal p
reset, and same-length traversal direction/nominal-km/actual-km semantics. Fourteen
of the initial 17 representative mutation cases passed validation. Moreover,
`validate_e06_derived(...)` accepted raw rows with a foreign matched-family ID
or empty seed map because its raw-grounding boundary delegates to this validator.

**Why it matters:** the canonical raw file happens to be correct, but a damaged
or substituted standard row could pass the exact boundary intended to prove
scenario identity, RNG pairing, parameters, continuity, and reset semantics.
Derived reconstruction cannot repair an unvalidated provenance field.

**Required fix/test:** reconstruct the entire expected row from the exact frozen
config and semantic seed derivation; compare every scalar and packed field with
strict JSON types, lengths, order, and finiteness; validate both Q components;
include disabled reset path types; and add materialized/parsed-CSV adversarial
tests covering at least one corruption from every frozen schema group.

**Risk if ignored:** standard inference could be based on rows whose RNG family,
parameters, path traversal, or inherited state differs from the approved design
while validation and derived tables still report success.

### Major — canonical report and provenance do not meet the frozen package

**Location:** `run_e06_experiment` report/manifest construction around lines
401--404 and
`results/reports/frontiers_m4_path_diagnostics_v1_smoke_report.md`.

**Evidence:** the canonical report has seven numbered items, not the required
13, and still says `pending_user_full_verification`. The canonical manifest
does not record the Git commit, complete segment seed map, focused commands and
runtimes, deterministic-regeneration evidence, or the actual user-owned full
verification result/log/hash. Its source-fingerprint list also omits some
governing E06 instruction/runbook documents. The separate preverification
checkpoint carries more detail but does not make the canonical report or
manifest complete.

**Why it matters:** the standard gate requires one self-consistent package that
binds science, authorization, source, verification, and artifacts. Split or
stale metadata is not a reproducible release seal.

**Required fix/test:** make the runner emit the complete 13-item canonical
report and full manifest schema, expand the fingerprint consumption set, and
add an external sealing step that records the exact user command, test counts,
log path/hash, exit code, and runtime without changing scientific outputs.
Tests must independently recompute all fields and reject missing/stale data.

**Risk if ignored:** a future GO could cite a manifest that neither proves the
tested commit/instructions nor records the verification event on which the GO
depends.

## Boundary and next action

Do not update the canonical manifest or preverification index to
`verification.status=passed` while the raw boundary remains fail-open. Do not
create `approvals/E06_STANDARD_GO.md`. Correct only validation, adversarial
coverage, report/provenance sealing, and their documentation; preserve model
semantics, config payloads, random behavior, and scientific artifact bytes.
Then rerun focused checks and user-owned full verification and submit the
package to another fresh independent smoke review. Qualification remains
refused regardless of any core correction.

