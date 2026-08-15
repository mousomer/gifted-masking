# E06 compression-ready independent Sol release-gate review

**Decision:** `FIX_IMPLEMENTATION`  
**Date:** 2026-08-13  
**Reviewer:** `gpt-5.6-sol`, `xhigh`  
**Scope:** sealed diagnostic smoke, deterministic-compression amendment,
standard readiness, provenance, resource and authorization gates  
**Standard:** not executed; not authorized  
**Qualification:** not executed; refused

## Release decision

`FIX_IMPLEMENTATION`

The sealed smoke and the regenerated compression fixture are genuine, the
frozen five-master scientific design is defensible, and the bounded standard
implementation is substantially complete. A canonical standard GO cannot be
issued because the current production readiness/dispatch boundary does not
authenticate the compression-fixture evidence that drives its stored-size
projection, does not enforce all formal stops throughout every expensive
phase, and exceeds the strict one-family streaming retention contract during
the second pass. These are bounded implementation/provenance defects; they do
not require a scientific specification change or a claim decision.

No `projects/frontiers_article/approvals/E06_STANDARD_GO.md` was created.

## Independently recomputed evidence

### Seal, provenance, and immutable smoke

- Normalized smoke config SHA-256:
  `475a8630acc73ab21520fd90024f85712b0002aec52d39d18e74e96cb8e4c40b`.
- Normalized standard config SHA-256:
  `58ebab7e6811369df90e14a697908eb0a106f6adcc1f897a4b201ca2a915cd7e`.
- Compression-amendment SHA-256:
  `8e3be4063004f87b92f32acd70cac3adf70bf372a305d4d448c3cd6365c2b297`.
- All 23 ordered source records recomputed exactly; aggregate fingerprint:
  `01d70e593fe213616a0d9ca3883c5d98fb0e305c3677661e89a13105aefd0d44`.
  The live ordered map matches the sealed manifest byte-for-byte.
- Sealed pre-review Git binding: HEAD
  `441cfe44856d0cbc3da57089cbe91755b0cc4780`, branch
  `codex/frontiers-stage2-e06`, dirty `true`, pre-review porcelain SHA-256
  `9fd1010d9b225db94628b507707ac6bd1aa8ccec64bce264faf675f18f6be0b5`.
  Removing only the subsequently added review-instruction record from the live
  porcelain payload reproduces that exact hash. Current drift is limited to
  that review instruction and this permitted review checkpoint; no
  source-fingerprinted file or scientific artifact changed during review.
- Manifest verification is exactly `passed` /
  `external_evidence_verified`.
- Archived full log SHA-256:
  `0b516c8eac187da4459e2d81a28a52c817bad802b9a7f9ea94511b72dc7a6e7e`.
- Exact exit-record SHA-256:
  `e0eb8bd605bbfaa0c7eac5a1e11fd892eb29a2831a8b8f3601c2e5d01f410063`;
  exact bytes are `verification_exit_code=0\n`.
- Strict log reconstruction, not caller totals, yields 122 + 1 + 1 + 2 = 126
  passing tests and 138.444 + 1.705 + 1.690 + 3.328 = 145.167 seconds.
- The external seal changed only the manifest/report seal fields. The eight
  scientific artifacts remain the original smoke bytes:

| Artifact | Rows | Bytes | SHA-256 |
|---|---:|---:|---|
| raw | 320 | 817,314 | `bbfa5b54034c96df825234f616e32480dfa3a1fdc3c82c6a76a9484a3d59e327` |
| cells | 45 | 10,596 | `0a22befa4021e997b980da84f0d3520df418f7ec9834533e5c67b1cf7b0c8bdc` |
| paths | 20 | 4,340 | `498f26914e7dfa30fe0f5c2cd782654c00bdee64bfa6122450997df22c7f4558` |
| loops | 8 | 1,833 | `fb72f0eab5b0d54658f4193ed18bbbe439da39edcb19795317f9ebfc51cf9364` |
| transitions | 8 | 1,488 | `94c41e2ed3736213b2da08be271ef1fb911f7b166b8715b708ba22c52dca0a3e` |
| effects | 6 | 1,198 | `a95778cd4dc5f09a3c0c9af134c3bf9cbb76a32fa043e8a3f2ef8cb44e6497e8` |
| PNG | — | 71,971 | `29448d540101f75e2ac4c32b050b5d5733b47c525bea21a2388976bac2e0661e` |
| warnings | — | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

### Model, raw semantics, and smoke reconstruction

Source inspection and independent replay confirm the maintained M4 contract:
stable row-wise softmax; one policy draw and one acceptance draw per learner,
including masking; objective reward from pre-update receptivity; loss aversion
only in the selected-Q learning update; then clipped receptivity update. The
ceiling final window is used. Inherited paths continue p and both Q values;
reversal/cold paths reset both; km-disabled paths traverse nominal km while
passing actual `km=0`. Semantic segment seeds use the frozen SHA-256 /
`SeedSequence` construction, matched inherited/reversal reuse, and cold-stream
isolation. Compression does not alter these semantics.

All 320 canonical rows and every derived smoke table were independently
validated. Counts reconstructed to 43,887 masking, 25,233 authentic, 22,608
accepted-authentic, 2,625 rejected-authentic, and zero post-update bounds
violations. All smoke decision fields remain ineligible/unavailable.

### Exact standard dispatch and inference contract

The standard config independently reconstructs:

- masters `2026081601`--`2026081605` in declaration order;
- nine scenarios;
- 26 families/master and 130 families total;
- `n=400` and exactly 52,000 packed rows;
- 36,000 22-segment loop rows plus 16,000 11-segment cold rows;
- exactly 913,000,000 learner steps;
- 130 unique master/scenario/path seed-map keys;
- bootstrap seed `2026081697` and exactly 10,000 complete-five-master paired
  resamples;
- deterministic master → scenario → path → child ordering;
- standard raw path ending `_units.csv.gz`;
- unconditional qualification refusal.

The implementation provides per-master cells and p-end quantiles; aligned
seed-level paths; seed/across-master loops; signed/absolute area, mean/maximum
separation and control excess; seed transitions at `.5` and `.75`; pooled
equal-master PAVA transitions; paired complete-master bootstrap widths with the
95% validity gate; five-master Student-t effects; cold endpoints; inherited
versus reversal effects; S01-versus-S00 speed effects; S02--S07-versus-S01
contrasts; and active-S01-versus-disabled-S08 placebo contrasts. Children are
descriptive units, not inferential replicates. No C8/C9 disposition is embedded.

Synthetic valid, censored-below, censored-above, boundary, plateau, nonfinite,
reordered, and mutated-derived probes behaved as specified. A valid synthetic
five-master pair produced 10,000/10,000 valid bootstrap widths.

### Gzip, fixture, and resources

Independent gzip generation produced identical bytes across two roots with
level 9, `mtime=0`, empty filename, canonical header
`1f8b08000000000002ff`, one member, no trailing bytes, UTF-8 Python-CSV
semantics, and separate logical/compressed fingerprints. Streaming checks
rejected non-gzip input, changed mtime/flags, checksum corruption, truncation,
concatenated members, trailing bytes, changed/reordered/duplicate/missing/
foreign rows, schema drift, and emitted-cell quantile corruption. Smoke remains
uncompressed and byte-identical.

The exact 52,000-row non-scientific fixture was freshly regenerated under
`/private/tmp` and then removed. It reproduced exactly:

- 36,000 22-segment and 16,000 11-segment rows;
- 311,405,905 logical bytes = 296.979814 MiB;
- logical SHA-256
  `5a8e579d258b7be88923fd90f5b23896226eb27956f5d89de55fb6b439fa2a3a`;
- 95,016,226 gzip bytes = 90.614534 MiB;
- compressed SHA-256
  `9a7318b9f3d7609490ce8ce7e060bdbb25f44138611eaea40319e7988c602ffe`;
- 5,000 distinct terminal floating tokens in the first 5,000 sampled rows,
  confirming a varying high-entropy rather than repetition-only fixture.

The conservative release arithmetic recomputes to approximately 344.136 MiB
worst-width logical CSV, 105.003 MiB worst-width-adjusted gzip, and 137.003 MiB
stored total. The fingerprinted readiness record gives 434.753 seconds and
226.438 MiB RSS; the currently sealed manifest contains a later current-source
projection of 387.706 seconds and 237.219 MiB RSS. Both numerical projections
pass 600 seconds, 150 MiB stored raw, 200 MiB stored total, 512 MiB RSS, and
400 MiB logical raw. The discrepancy is a provenance consistency problem
described below, not evidence that a limit itself fails.

### Figure and report boundary

The future standard renderer has five distinct diagnostic content panels:
speed-separated inherited mask paths; speed-separated receptivity paths;
inherited versus reversal gaps; seed loop areas plus transition widths; and
included scenario sensitivity/ablation endpoints. The sixth axes cell is
annotation only. It is named a continuation diagnostic, not hysteresis. The
report and manifest explicitly state that execution is not C8/C9 adjudication
and qualification remains refused.

## Findings

### Blocker — compression fixture is not authenticated at production readiness/dispatch

**Location:** `src/gifted_masking/experiments/e06.py:920-961`, especially
`load_e06_standard_compression_fixture` and
`e06_standard_readiness_projection`; standard preflight at lines 964-967.

**Evidence:** the loader validates only record shape, arithmetic, config/source
fields, syntactically hexadecimal hashes, and inequalities. It neither
regenerates/opens the fixture bytes nor compares the current fixture-record
SHA-256 with the hash sealed in the smoke manifest's
`standard_projection.compression_fixture_record`. An adversarial temporary
record with `compressed_bytes=1`, a fabricated all-zero compressed SHA-256,
recomputed MiB arithmetic, and unchanged binding fields was accepted as
`within_limits=true`. Production readiness then uses that caller-controlled
ratio at line 949, and `_run_e06_standard` accepts the resulting projection.

**Why it matters:** after this review creates a GO, the GO binds config, source,
and smoke-manifest hashes but not the separately mutable fixture record. A
substituted record can understate stored-size projection without invalidating
the GO or source fingerprint, defeating the required strict resource gate.

**Required fix/test:** make readiness fail unless the canonical fixture-record
file hash equals the fixture-record SHA-256 sealed in the bound smoke manifest,
and authenticate the claimed fingerprint by deterministic regeneration or a
preserved canonical fixture byte artifact whose compressed/logical hashes,
row split, schema, and high-entropy generator identity are independently
verified. Add an adversarial test with internally consistent fabricated
sizes/hashes, not only arithmetic-inconsistent mutations. Ensure standard
authorization/readiness repeats this check before any directory creation.

**Risk if ignored:** a valid GO can dispatch with resource authorization based
on forged capacity evidence and silently bypass the 150/200-MiB release gates.

### Major — strict/formal stops are not enforced throughout every expensive phase

**Location:** `src/gifted_masking/experiments/e06.py:964-1015`, with stop calls
at lines 979, 984, 995, 1001, and 1012.

**Evidence:** the stop helper correctly rejects over-limit runtime, compressed
raw, logical raw, stored total, and RSS when called. The runner does not call it
inside the standard-derived/bootstrap work at line 987, during table
serialization at 991-993, during each family of the second replay at 995, or
during parsed-derived validation/figure rendering at 997-999. In particular,
the independent replay executes all 913,000,000 learner steps before the next
runtime/RSS stop check. Logical raw is checked only after gzip closes and at
later publication boundaries, not during generation. The instructions require
runtime, stored raw, logical raw, stored total, and RSS stops during and before
publication.

**Why it matters:** a slow or memory-regressed phase can exceed the 600-second
or 512-MiB gate for a long interval before detection, and logical output can
cross 400 MiB before the writer is stopped. This weakens the resource gate from
an operational stop to a delayed postcondition.

**Required fix/test:** call stop checks at bounded intervals inside simulation
generation, logical serialization, bootstrap/derived loops, streaming replay,
and figure/report creation. Give the logical writer a checked byte ceiling.
Inject deterministic time/RSS/logical/stored-limit crossings into each phase
and prove the run aborts before promotion.

**Risk if ignored:** the authorized process can violate formal resource limits,
continue expensive work after a required stop, or be externally killed before
its own atomic cleanup completes.

### Major — second-pass replay retains two 400-row family buffers

**Location:** `src/gifted_masking/experiments/e06.py:451-481`.

**Evidence:** for every second-pass family, the validator accumulates 400
parsed candidate dictionaries in `candidate` (lines 466-471), independently
materializes another 400-row expected family in `expected` (line 472), and
then constructs candidate/expected cell lists. This is bounded and avoids a
52,000-row materialization, but it does not satisfy the explicit gate “at most
one 400-row family plus bounded aggregates is retained.”

**Why it matters:** the independently reviewed RSS bound and streaming
architecture were premised on one family, while the production implementation
retains two full packed families. The current projected RSS still lies below
512 MiB, but the acceptance criterion is structural and strict, not merely a
numerical estimate.

**Required fix/test:** compare the parsed family against the deterministic
replay incrementally, or replay one expected row/child at a time and reduce
cells online so no second 400-row packed family coexists with the candidate.
Add instrumentation/assertions covering peak retained packed-row cardinality.

**Risk if ignored:** the implementation violates its reviewed streaming
contract and makes the RSS proof depend on an unapproved two-family high-water.

### Moderate — sealed resource projection and fingerprinted readiness record disagree

**Location:** sealed manifest/report resource projection versus
`projects/frontiers_article/checkpoints/E06_STANDARD_READINESS_IMPLEMENTATION_CHECKPOINT.md`
and the current fixture record.

**Evidence:** the fingerprinted readiness checkpoint records 434.753 seconds,
226.438 MiB RSS, and a 36.985-second/157.375-MiB fixture observation. The sealed
manifest/report record 387.706 seconds, 237.219 MiB RSS, and the canonical
fixture record's 37.635-second/134.375-MiB observation. All values pass, and
the exact fixture bytes are deterministic, but there is no single canonical
explanation of which projection governs release.

**Consequence:** resource evidence is internally inconsistent even though the
decision direction is unchanged. Reseal one conservative canonical projection,
preferably componentwise maxima with named evidence origins, and update the
readiness checkpoint accordingly before another review.

### Moderate — post-seal drift policy is documented but not enforced by standard authorization

**Location:** `src/gifted_masking/experiments/e06.py:764-789` and source list at
lines 36-40.

**Evidence:** authorization binds the current source fingerprint and the sealed
smoke manifest, but neither the sealed Git/porcelain state nor an allowed
post-seal drift set. The current review-instruction file is deliberately
outside the source fingerprint and changed porcelain after sealing; future
unrelated untracked/modified files could do the same without invalidating the
GO.

**Consequence:** this review proved current drift benign, but production does
not prove that property. Bind an allowed drift inventory/hash in the GO or add
a pre-dispatch check that live porcelain equals the sealed payload plus only
explicit approval/review records.

### Minor — stale project backlog wording

The project backlog still leaves the Round 2 implementation-correction item
unchecked while later entries correctly record completion. Correct this only
as part of the next documentation/seal refresh; it is not scientific evidence.

## Acceptance gates that passed

- Frozen model semantics and exact draw/update order.
- Exact raw/action/outcome/reward reconstruction and p/Q continuity/reset.
- Segment-seed semantics, reuse/isolation, and global-RNG independence.
- Exact standard config, masters, scenario/family/row/step cardinalities,
  declaration order, and complete seed-map keys.
- Standard-only master-level Student-t, PAVA and complete-master bootstrap
  inference on synthetic valid/censored/boundary/plateau/nonfinite/mutated
  cases.
- Deterministic gzip container and logical CSV semantics, including every
  required adversarial container/raw/cell rejection.
- Exact high-entropy fixture regeneration and conservative size arithmetic.
- Missing/copy-path/wrong-config/malformed/duplicate/wrong-binding/unsealed/
  qualification authorization refusal before requested output-root creation.
- Existing package refusal, staged outputs, manifest-last promotion, and
  cleanup of newly promoted partial files by source inspection.
- Sealed focused evidence and fresh unchanged-source E06 suite: 16/16 passed
  in 57.016 seconds during this review. The archived full verification remains
  126/126 in 145.167 seconds; `./scripts/verify.sh` was not rerun.
- Five-panel continuation-diagnostic figure/report contract and explicit lack
  of C8/C9 adjudication.

## Exact next action

Implement only the five bounded release-gate repairs above: authenticate the
canonical fixture record/bytes at standard readiness, enforce every resource
stop within all long phases, reduce second-pass retention to one 400-row
family, reconcile one conservative canonical resource projection, and bind
allowed post-seal Git drift. Add focused adversarial tests, regenerate only the
non-scientific fixture and diagnostic smoke as required, obtain new user-owned
full verification and external sealing, and repeat this fresh Sol review.

Do not run E06 standard or qualification. Do not adjudicate C8/C9 or change the
claim ledger, manuscript, figures, model semantics, frozen configs, scenarios,
seeds, horizons, `n`, bootstrap count, schemas, gzip settings, or resource
limits.

`FIX_IMPLEMENTATION`
