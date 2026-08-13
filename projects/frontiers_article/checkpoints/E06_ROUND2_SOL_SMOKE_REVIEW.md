# E06 Round 2 independent external-seal and smoke-gate review

**Decision:** `FIX_IMPLEMENTATION`
**Date:** 2026-08-13
**Reviewer:** `gpt-5.6-sol`, `xhigh`
**Scope:** Round 2 external seal and independent scientific smoke gate
**Standard:** not executed; not authorized
**Qualification:** not executed; refused

## Immutable pre-seal binding

The canonical pending package and v2 preverification index both matched the
live pre-seal repository state:

- Git HEAD: `9b2550248540152ad0d76758ee786bf228592880`;
- branch: `codex/frontiers-stage2-e06`;
- dirty: `true`;
- exact `git status --porcelain` byte count: `516`;
- porcelain SHA-256:
  `5fe733cc7c6f7d9155cd965032ea3716ff83a9c95653c21271cae239429f7316`;
- normalized smoke-config SHA-256:
  `475a8630acc73ab21520fd90024f85712b0002aec52d39d18e74e96cb8e4c40b`;
- E06 smoke-approval SHA-256:
  `9fc0434c86da23815afc3327f79c0e9824918417839aadda39dc1ba061cb76f7`;
- ordered source-fingerprint SHA-256:
  `ad053db7cd51846c2e2c2418d4bc9679d2e617045c712969e4c6bf11a6547d8d`.

The pending manifest parsed as strict JSON without duplicate keys or nonfinite
values. Its state was exactly `pending_user_full_verification` / `unsealed`.
The complete normalized config, approval, ordered source paths and hashes,
Git/dirty binding, focused evidence, two fresh deterministic roots, and all
canonical scientific artifacts matched the v2 index. No fingerprinted source
was newer than either Round 2 verification-evidence file.

## Durable Round 2 verification evidence

The two user-owned evidence files were copied with metadata preservation to
the ignored durable directory without changing the 516-byte porcelain payload
or its SHA-256:

- `results/reports/e06_round2_user_verification/user_full_repository_verification_round2.log`
  - SHA-256:
    `73a5922e137972d87f8a7baf2cfc1fb600cb16eb2e324ae3af8208a6ec029de9`;
- `results/reports/e06_round2_user_verification/user_full_repository_verification_round2_exit.txt`
  - SHA-256:
    `e0eb8bd605bbfaa0c7eac5a1e11fd892eb29a2831a8b8f3601c2e5d01f410063`;
  - exact bytes: `verification_exit_code=0\n`.

Independent strict parsing found the required workspace Python and four
successful suite completions, with no failure/error termination:

| Suite | Tests | Runtime (s) |
| --- | ---: | ---: |
| repository discovery | 116 | 128.321 |
| manifest completeness | 1 | 1.694 |
| primary raw schema | 1 | 1.679 |
| summary/raw reconciliation | 2 | 3.240 |
| **Total** | **120** | **134.934** |

One non-failing `ResourceWarning` in the E01 suite reports an unclosed CSV
handle. It is not an E06 seal failure.

## Production seal probe and canonical seal

A fresh temporary directory contained only copies of the pending manifest and
report. `build_e06_full_verification_evidence(...)` reconstructed the exact
four suite records and totals from the durable log/exit files, and
`seal_e06_verification(...)` accepted them. The probe produced
`passed` / `external_evidence_verified`, updated report item 12 with the exact
command and evidence hashes, and left the canonical manifest, report, and all
scientific artifacts unchanged.

The production sealer was then invoked once against the canonical output map.
The resulting package is:

- manifest:
  `results/manifests/frontiers_m4_path_diagnostics_v1_smoke.json`;
  SHA-256
  `3cf23f2082f4d8b770d0fc44b8d1c5f5082fa66cc3d9f4e0f64f8abff7cf7b5d`;
  34,256 bytes;
- report:
  `results/reports/frontiers_m4_path_diagnostics_v1_smoke_report.md`;
  SHA-256
  `45a2809bc4cc25b792badfcb2fbc7ad42384ca0b894015c2e3fbb573785bf36e`;
  3,401 bytes;
- verification state: `passed`;
- seal state: `external_evidence_verified`;
- evidence command:
  `MPLCONFIGDIR=/private/tmp/e06_user_verify_round2 ./scripts/verify.sh`;
- parsed total: 120 tests in 134.934 seconds.

The manifest's report bytes/hash recompute exactly. No `.e06tmp` or partial
file remains. The sealer was not invoked a second time against the canonical
package.

## Scientific byte preservation

The canonical seal changed only the manifest and report. These eight
scientific artifacts retained their exact pre-seal bytes:

| Artifact | Rows | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| raw | 320 | 817,314 | `bbfa5b54034c96df825234f616e32480dfa3a1fdc3c82c6a76a9484a3d59e327` |
| cells | 45 | 10,596 | `0a22befa4021e997b980da84f0d3520df418f7ec9834533e5c67b1cf7b0c8bdc` |
| paths | 20 | 4,340 | `498f26914e7dfa30fe0f5c2cd782654c00bdee64bfa6122450997df22c7f4558` |
| loops | 8 | 1,833 | `fb72f0eab5b0d54658f4193ed18bbbe439da39edcb19795317f9ebfc51cf9364` |
| transitions | 8 | 1,488 | `94c41e2ed3736213b2da08be271ef1fb911f7b166b8715b708ba22c52dca0a3e` |
| effects | 6 | 1,198 | `a95778cd4dc5f09a3c0c9af134c3bf9cbb76a32fa043e8a3f2ef8cb44e6497e8` |
| figure | — | 71,971 | `29448d540101f75e2ac4c32b050b5d5733b47c525bea21a2388976bac2e0661e` |
| warnings | — | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

All 33 E01--E05 standard artifacts recorded by their five canonical manifests
also retained their recorded byte counts and SHA-256 values.

## Raw, derived, adversarial, and deterministic review

The complete packed raw file contains 320 rows and all 55 ordered fields.
Production validation reconstructed every row from the frozen config,
scenario/path semantics, child index, and semantic segment seeds. Independent
count/reward reconstruction found:

- 43,887 masking actions;
- 25,233 authentic actions;
- 22,608 accepted-authentic outcomes;
- 2,625 rejected-authentic outcomes;
- zero post-update bounds violations.

Every segment satisfied mask plus authentic equals 24 final-window actions,
accepted plus rejected equals authentic, mask rate equals the count ratio, and
mean objective reward reconstructs from `0.75`, `1.6`, and `-1.4` outcome
payoffs within `1e-12`.

The five derived tables reconstruct exactly and retain smoke
`decision_eligible=false`. Smoke confidence fields are blank/unavailable, not
zero-filled. An independent table-driven audit confirmed rejection of 30
distinct materialized mutations, the same 30 mutations after production CSV
parsing, and seven representative raw-boundary mutations through derived
validation. The cases cover identity, seed map and nested seed, exact types,
nonfinite values, traversal substitution, reset drift, both-Q continuity,
row cardinality/order, and duplicate JSON keys.

Source inspection and the sealed focused evidence agree on maintained M4
semantics: stable softmax action selection, one acceptance draw for every
learner including masking, objective reward from pre-update receptivity,
selected-Q-only subjective update, then bounded receptivity update. The
ceiling final-window convention, inherited p/both-Q continuity, reversal/cold
resets, and absence of global NumPy RNG are preserved. Focused replay covers
zero and positive `km`, multiple seeds, reset and inherited starts, and the
non-integral window case.

The two fresh roots in the manifest still exist. Their raw, five summaries,
PNG, and warnings files match each other and canonical scientifically; the
production normalized manifest/report comparison also passes. The canonical
report has exactly the required 13 subjects.

## Inference and interpretation boundary

The sealed smoke is diagnostic only. It does not establish C8 or C9,
bistability, hysteresis, irreversibility, or entrenchment. The recorded
one-seed paths and loop/transition diagnostics remain decision-ineligible.
The pure five-seed Student-t, PAVA/transition, isolated bootstrap-seed, and
10,000-top-level-resample helpers are present and pass their synthetic focused
checks, but the current standard execution/package path is not implemented as
required below.

No standard or qualification artifact exists. No E06 standard or
qualification execution, C8/C9 adjudication, claim-ledger change, manuscript
change, or Figure 4 replacement occurred.

## Resource review

The recorded core projection is 229.699 seconds, 126.661 MiB raw, 140.829 MiB
total, and 121.828 MiB peak RSS, numerically within the review's 600-second,
150-MiB raw, 200-MiB total, and 512-MiB RSS limits. Qualification projects
634.772 seconds and remains refused regardless of the estimate.

The core RSS/runtime method does not, however, close the executable-standard
resource gate. It multiplies smoke RSS by only 1.5 while the current design
would materialize 52,000 packed candidate rows plus a second deterministic
replay/cache and a shallow expected-row copy. Its serialization phase also
contains a complete replay validator but is scaled only by row count rather
than by the frozen standard segment/horizon workload. This does not affect the
sealed smoke but makes the projected standard high-water and validator runtime
non-conservative.

## Findings

### Blocker — no GO-gated five-seed standard execution/package path

**Location:** `src/gifted_masking/experiments/e06.py:466-480`, especially the
unconditional non-smoke refusal at line 468 and single `master_seed` loop at
lines 473-474; standard-ineligible derived output at lines 381-398; seed-map
key construction at line 507.

**Evidence:** `run_e06_experiment(...)` rejects every standard config before
examining an approval record. If that guard were bypassed, it would iterate
only `config["master_seed"]`, not the five `master_seeds`, while
`expected_rows(...)` requires five copies. The shared derived builder always
emits `decision_eligible=False`, zero bootstrap replicates, blank intervals,
and diagnostic-only master-seed effects. It does not emit the frozen five-seed
Student-t, pooled transition/bootstrap, speed/horizon, or decision records.
The seed-map manifest key omits master seed and would overwrite maps across
masters.

**Why it matters:** a new `E06_STANDARD_GO.md` would authorize a command that
cannot execute the frozen standard or produce its required 52,000-row,
five-master inference package. Any post-GO code change needed to add that path
would alter the source fingerprint bound by the GO, invalidating the
authorization.

**Required fix/test:** implement the exact standard path before another gate:
validate only the canonical future GO record; iterate the five frozen masters
and nine scenarios in deterministic order; preserve complete per-master seed
maps; construct every standard cell/path/loop/transition/effect record; apply
the five-seed Student-t and 10,000-master-bootstrap rules; enforce exact
cardinality and output reconstruction; and prove missing, copied, wrong-path,
wrong-hash, or stale GO records fail before output creation. Keep qualification
unconditionally refused.

**Risk if ignored:** the release gate would approve a non-executable or
scientifically incomplete standard command, and any improvised Pass D repair
would run code not bound by this review.

### Major — standard resource projection omits materialized validation cost

**Location:** `src/gifted_masking/experiments/e06.py:210-236` and
`src/gifted_masking/experiments/e06.py:473-486`.

**Evidence:** projected peak RSS is `smoke RSS * 1.5` even though the runner
retains all packed rows and fail-closed validation reconstructs/caches a second
full scientific row set. The measured `serialization` phase includes that
deterministic replay, but its standard projection scales only by
`52000/320`, while segment horizons and the five-master standard workload also
increase. No fresh process has measured a standard-cardinality non-scientific
materialization or a streaming-equivalent high-water.

**Why it matters:** the numerical 121.828-MiB estimate does not bound the
actual materialized standard process against the frozen 512-MiB review limit;
the reported 229.699-second total also understates the second full replay.

**Required fix/test:** implement deterministic streaming or bounded chunked
raw generation/validation and aggregation, or measure an exact
standard-cardinality serialization/validation fixture without executing the
scientific standard. Record a conservative fresh-process RSS/runtime bound
that includes candidate rows, reconstructed expected rows/cache, parsed-CSV
validation, derived aggregation, bootstrap, and figure phases.

**Risk if ignored:** the authorized process can exceed memory/runtime stops or
be killed after expensive simulation, leaving a partial package.

### Moderate — declared raw sort keys do not describe emitted order

**Location:** `src/gifted_masking/experiments/e06.py:473-474` and manifest
construction at line 514.

**Evidence:** rows are emitted in config path order (`inherited_loop`,
`reversal_only`, `cold_start`, disabled inherited, disabled reversal), whereas
the manifest declares lexical `path_type` in `sort_keys`. The bytes and
validator order are deterministic, but the metadata is inaccurate.

**Consequence:** a consumer sorting by the declared keys will not reproduce the
canonical row order. Correct the declaration or use an explicit path-order
field without changing model/RNG semantics.

### Minor — non-failing E01 resource warning

The Round 2 full log reports one unclosed-file `ResourceWarning` from
`tests/test_article_e01.py:159`. It did not fail the suite and is unrelated to
the E06 seal, but should be closed in a separate low-risk test cleanup.

## Decision and exact next action

Decision: `FIX_IMPLEMENTATION`. The frozen E06 scientific specification is
coherent, and the canonical smoke is sealed, deterministic, and scientifically
valid as a diagnostic. The remaining defect is implementation readiness for
the standard, not a reason to revise the E06 specification or narrow C8/C9
before the standard exists.

Do not create `E06_STANDARD_GO.md`. Implement only the exact GO-gated core
standard execution/packaging and conservative bounded-resource path described
above, plus the sort-key metadata correction. Then repeat focused adversarial
checks, deterministic smoke regeneration, user-owned full repository
verification, external sealing, and a fresh independent smoke gate. Do not run
standard during that correction. Qualification, C8/C9 adjudication, ledger,
manuscript, and Figure 4 work remain refused.

## Files and task-only diffstat

This review created the durable ignored evidence archive and changed only the
canonical seal/review records permitted after sealing:

- created
  `projects/frontiers_article/checkpoints/E06_ROUND2_SOL_SMOKE_REVIEW.md`;
- updated the canonical E06 smoke manifest and report through the production
  sealer only;
- updated only E06-specific entries in `CURRENT_STATE.md`, `BACKLOG.md`, and
  `STAGE2_EXECUTION_LOG.md`;
- copied the 20,778-byte log and 25-byte exit record to the ignored
  `results/reports/e06_round2_user_verification/` directory;
- did not create `projects/frontiers_article/approvals/E06_STANDARD_GO.md`.

Relative to the exact pre-task copies, the six repository seal/review files
have 436 inserted and 36 deleted lines. This task-only count is separate from
the pre-existing implementation changes already present in the dirty worktree.
