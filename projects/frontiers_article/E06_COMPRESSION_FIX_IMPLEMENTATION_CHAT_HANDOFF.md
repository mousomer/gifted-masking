# E06 compression release repair — full handoff for a fresh Codex chat

## How to use this handoff

Start a fresh Codex task in:

`/Users/omer/workspace/personal/repos/gifted-masking`

Use:

- model: `gpt-5.6-terra`;
- reasoning effort: `high`;
- normal/default implementation mode.

Paste the prompt at the end of this document into the task. The task must then
read this handoff and the authoritative operational instruction set completely
before editing anything.

This is a bounded implementation repair. It is not a new scientific review,
not a standard experiment run, and not authorization to decide the article's
claims.

## Executive handoff

E06 is the M4 path-diagnostics experiment for the Frontiers article. The
diagnostic smoke has already been regenerated deterministically, subjected to
focused adversarial validation, verified through a user-owned full repository
verification, and externally sealed. Its model semantics, seed semantics, raw
rows, derived tables, figure, and warnings artifact were independently
reviewed and found internally valid.

The next standard run is still refused. An independent Sol release-gate review
returned `FIX_IMPLEMENTATION`, not because the scientific model or smoke result
failed, but because five production release controls remain incomplete:

1. production readiness trusts a self-consistent fixture record without
   independently authenticating the claimed fixture bytes;
2. resource limits are checked between some phases but not at bounded
   intervals throughout every long phase;
3. streaming replay retains two 400-row packed families at once, violating the
   approved one-family structural bound;
4. two defensible but different resource projections are exposed without one
   canonical conservative reconciliation;
5. post-seal Git drift is reviewed manually but is not enforced through a
   content-aware production authorization check.

The implementation task must repair exactly those five defects, prove the
repairs with focused and adversarial tests, regenerate only the permitted
non-scientific capacity fixture and diagnostic smoke, and stop with the
canonical package pending user-owned full verification.

The task must not run E06 standard or qualification. It must not run the full
repository verifier. It must not create the standard GO. It must not change
model semantics, configs, scientific claims, manuscript text, or Figure 4.

## Current repository identity

At handoff creation:

- branch: `codex/frontiers-stage2-e06`;
- HEAD: `441cfe44856d0cbc3da57089cbe91755b0cc4780`;
- working tree: intentionally dirty;
- canonical standard GO: absent;
- E06 standard: not run;
- E06 qualification: not run and must remain refused.

Do not assume that dirty files are disposable or produced by the new task.
There are tracked modifications and untracked E06 continuation artifacts from
earlier approved work. Inventory them before editing, preserve them, and report
the task-only scope as accurately as possible. Never reset, discard, or clean
the worktree.

## Decision and evidence history

The relevant sequence is:

1. E06 diagnostic raw-count semantics were repaired and validated.
2. Raw-grounded validation was added for all five derived tables.
3. Packed raw reconstruction and adversarial raw mutation coverage were added.
4. The external sealer was made fail-closed against user-owned verification
   evidence, source fingerprints, Git state, scientific artifacts, focused
   evidence, and deterministic regeneration evidence.
5. The user ran the repository verifier successfully.
6. The package was externally sealed as `passed` /
   `external_evidence_verified`.
7. Deterministic gzip and a full-cardinality, non-scientific compression
   fixture were introduced to make the standard raw artifact fit the frozen
   storage limits without changing its logical CSV contents.
8. A fresh independent Sol review accepted the sealed science, gzip semantics,
   standard inferential design, and exact fixture bytes, but found the five
   release-control defects listed above.

The controlling review is:

`projects/frontiers_article/checkpoints/E06_COMPRESSION_SOL_REVIEW.md`

Its decision is exactly `FIX_IMPLEMENTATION`.

## What has already been established

Do not reopen these matters unless a repair demonstrably breaks them.

### Model semantics

The maintained M4 implementation uses:

- stable row-wise softmax;
- one policy draw and one acceptance draw per learner per step, including when
  masking is chosen;
- objective reward computed from pre-update receptivity;
- loss aversion applied only to the selected-Q learning update;
- receptivity update after reward and Q update;
- clipping of receptivity to its configured bounds;
- ceiling-based final-window semantics.

Inherited paths continue receptivity and both Q values. Reversal and cold
paths reset both. The km-disabled paths retain the nominal path coordinate but
execute with actual `km=0`. Semantic segment seeds use the frozen SHA-256 and
`SeedSequence` construction with documented reuse and isolation behavior.

Compression must not change any of this.

### Smoke scientific artifacts

The eight frozen smoke artifacts and reviewed hashes are:

| Artifact | Rows | Bytes | SHA-256 |
|---|---:|---:|---|
| packed raw CSV | 320 | 817,314 | `bbfa5b54034c96df825234f616e32480dfa3a1fdc3c82c6a76a9484a3d59e327` |
| cells CSV | 45 | 10,596 | `0a22befa4021e997b980da84f0d3520df418f7ec9834533e5c67b1cf7b0c8bdc` |
| paths CSV | 20 | 4,340 | `498f26914e7dfa30fe0f5c2cd782654c00bdee64bfa6122450997df22c7f4558` |
| loops CSV | 8 | 1,833 | `fb72f0eab5b0d54658f4193ed18bbbe439da39edcb19795317f9ebfc51cf9364` |
| transitions CSV | 8 | 1,488 | `94c41e2ed3736213b2da08be271ef1fb911f7b166b8715b708ba22c52dca0a3e` |
| effects CSV | 6 | 1,198 | `a95778cd4dc5f09a3c0c9af134c3bf9cbb76a32fa043e8a3f2ef8cb44e6497e8` |
| PNG | — | 71,971 | `29448d540101f75e2ac4c32b050b5d5733b47c525bea21a2388976bac2e0661e` |
| warnings log | — | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

All eight bytes must remain identical after the implementation. A changed
manifest/report is expected because source/provenance/resource evidence will
be refreshed; a changed scientific artifact is a blocker.

### Archived verification and seal

The archived user-owned full verification reconstructs:

- 122 + 1 + 1 + 2 = 126 passing tests;
- 138.444 + 1.705 + 1.690 + 3.328 = 145.167 seconds;
- verification log SHA-256:
  `0b516c8eac187da4459e2d81a28a52c817bad802b9a7f9ea94511b72dc7a6e7e`;
- exit-record SHA-256:
  `e0eb8bd605bbfaa0c7eac5a1e11fd892eb29a2831a8b8f3601c2e5d01f410063`;
- exact exit-record bytes: `verification_exit_code=0\n`.

Those archived results establish the old sealed source state. Once source is
changed for these repairs, they cannot be reused to reseal the new package.
The implementation must therefore finish at
`pending_user_full_verification` / `unsealed` and give the user a fresh
verification command.

### Exact standard design

The frozen standard contract is:

- masters `2026081601` through `2026081605`, in declaration order;
- nine scenarios;
- 26 families per master;
- 130 total families;
- `n=400` children per family;
- 52,000 packed rows;
- 36,000 rows with 22 segments;
- 16,000 rows with 11 segments;
- exactly 913,000,000 learner steps;
- bootstrap seed `2026081697`;
- exactly 10,000 complete-five-master paired bootstrap resamples;
- deterministic master → scenario → path → child ordering;
- standard raw filename ending `_units.csv.gz`;
- qualification refused unconditionally.

None of these values may change.

### Inferential boundary

The standard implementation uses masters—not children—as inferential
replicates. It provides the frozen Student-t, PAVA, complete-master bootstrap,
speed/scenario/placebo contrasts, path and loop summaries, and five-panel
continuation-diagnostic report. E06 does not yet adjudicate C8 or C9.

The current figure is a continuation/path diagnostic. Do not rename it as
proof of hysteresis. Compression fixtures are capacity evidence only; they are
not scientific simulation evidence.

## Exact non-scientific fixture evidence

The independently regenerated full-cardinality fixture produced:

- 52,000 rows;
- 36,000 22-segment rows;
- 16,000 11-segment rows;
- logical bytes: `311405905` (`296.979814 MiB`);
- logical SHA-256:
  `5a8e579d258b7be88923fd90f5b23896226eb27956f5d89de55fb6b439fa2a3a`;
- gzip bytes: `95016226` (`90.614534 MiB`);
- gzip SHA-256:
  `9a7318b9f3d7609490ce8ce7e060bdbb25f44138611eaea40319e7988c602ffe`;
- gzip level 9;
- `mtime=0`;
- empty gzip filename;
- one member and no trailing bytes;
- header `1f8b08000000000002ff`;
- 5,000 distinct terminal floating tokens in the first 5,000 sampled rows.

Worst-width conservative bounds are approximately:

- logical raw: `344.136 MiB`;
- compressed raw: `105.003 MiB`;
- stored total: `137.003 MiB`.

These values currently fit all frozen byte limits. The production defect is
that the record can be replaced by a fabricated but internally consistent
record and still pass readiness. The repair must authenticate the evidence,
not merely repeat its arithmetic.

## Frozen resource limits

The standard must fail closed at:

| Resource | Limit |
|---|---:|
| wall runtime | 600 seconds |
| compressed raw | 150 MiB |
| stored package total | 200 MiB |
| peak RSS | 512 MiB |
| logical raw CSV | 400 MiB |

Do not increase these limits. Do not make a formal stop advisory. Do not rely
on a check that occurs only after a phase has already exceeded a limit.

## Authoritative implementation specification

The complete operational requirements are in:

`projects/frontiers_article/E06_COMPRESSION_FIX_IMPLEMENTATION_CODEX_INSTRUCTIONS.md`

Read that file completely. It is authoritative for the repair architecture,
test matrix, artifact refresh, documentation, acceptance criteria, and final
response. This handoff explains context but does not weaken any requirement in
that instruction set or in `AGENTS.md`.

## The five repairs in plain language

### 1. Authenticate the compression fixture

Current behavior establishes that a JSON record is internally well formed. It
does not establish that the claimed 52,000-row bytes ever existed.

The production standard preflight must, before creating the requested output
root:

1. require the exact canonical fixture-record path;
2. bind the record's file hash through the bound smoke manifest;
3. verify its exact config, source, generator, row split, gzip, schema,
   scientific=false, arithmetic, measurement, and limit fields;
4. freshly regenerate the complete non-scientific fixture under a unique
   temporary path;
5. independently reproduce both logical and compressed bytes/hashes and the
   deterministic gzip contract;
6. enforce runtime and RSS limits during regeneration;
7. remove temporary artifacts on success and every failure path.

A fabricated record and a correspondingly fabricated temporary manifest must
still fail because fresh regeneration disagrees with them. Passing only an
altered-record-hash test is insufficient.

### 2. Enforce resource stops continuously

Create an E06-local resource guard with injectable clock/RSS sources for tests.
It must enforce all five resource dimensions at bounded, documented intervals
throughout fixture regeneration, simulation, CSV/gzip writing, derived work,
bootstrap, independent replay, serialization, parsed validation, rendering,
report/manifest creation, and promotion.

The logical CSV writer must stop as it crosses 400 MiB; it cannot wait until
gzip closes. Inject deterministic failures in every major phase and prove the
run aborts before final publication, with temporary cleanup.

Do not add generic callbacks to maintained M4 model code. Keep operational
guarding within E06.

### 3. Retain at most one packed family

The current replay retains 400 parsed candidate rows and independently creates
400 expected rows. Although bounded, this violates the reviewed architecture.

The new replay must perform exact 55-field, ordered, type-safe row comparison
while retaining no more than 400 packed-row dictionaries in total. A transient
candidate row counts if it coexists with 400 expected rows. Instrument and
report the actual peak. Preserve every existing corruption rejection and cell
validation.

Do not redefine the requirement as “two small families are okay.”

### 4. Produce one conservative projection

The readiness checkpoint and sealed manifest currently expose different
passing estimates:

- approximately `434.753 s / 226.438 MiB RSS`;
- approximately `387.706 s / 237.219 MiB RSS`.

Neither implies a failed limit, but release evidence cannot have two governing
answers. Build one machine-readable projection from componentwise conservative
maxima, keep named evidence origins, preserve prior conservative component
floors, and add fixture-authentication time explicitly.

Use the exact same object in the smoke manifest, report, readiness checkpoint,
preflight evidence, and any later standard manifest. If the reconciled value
exceeds any frozen limit, stop as blocked.

### 5. Enforce content-aware post-seal drift

Porcelain state alone is insufficient: an already-untracked file can change
bytes without changing `git status --porcelain`.

Record and validate an ordered dirty-path inventory containing status, path,
byte count, and SHA-256 for each regular dirty file. Reject ambiguous or unsafe
states such as renames, deletions, symlinks, directories, unreadable paths, and
paths outside the repository.

At eventual standard preflight, allow only the exact sealed baseline plus:

1. the canonical smoke manifest bound by the GO;
2. the smoke report bound by the manifest;
3. the independent Sol review checkpoint bound by new GO fields;
4. the strict canonical GO itself.

Extend the future GO schema with exactly:

- `review_checkpoint_path`;
- `review_checkpoint_sha256`.

Do not create the real GO in this task. Test the schema and authorization only
with temporary synthetic packages/repositories.

## Required working method

Before editing:

1. read `AGENTS.md` fully;
2. inventory the live worktree, branch, and HEAD;
3. verify the real standard GO is absent;
4. verify the canonical smoke's current seal and eight artifact hashes;
5. read every file listed under “Required preparation” in the authoritative
   instruction set;
6. write a concise implementation plan and explicit acceptance criteria;
7. compare the design with `ARCHITECTURE.md`, RDS, readiness design,
   compression amendment, and Sol review;
8. update design/state/backlog documentation as required by repository
   governance.

Implement in small, auditable units. Run focused tests after each repair. Use
only `/Users/omer/workspace/venvs/venv314/bin/python` for Python work and use
isolated `MPLCONFIGDIR` locations.

Do not install dependencies. Do not create a repository-local environment.

## Required verification without the full verifier

The implementation task may run:

- the complete focused E06 test file;
- M4 tests;
- core and determinism tests;
- focused manifest/raw/summary contract tests;
- new fixture-authentication adversarial tests;
- new injected phase-stop tests;
- new one-family retention tests;
- new content-drift and extended-GO-schema tests;
- Python compilation checks;
- `git diff --check`;
- two full-cardinality non-scientific fixture generations;
- two diagnostic smoke regenerations.

The two fixture generations must use separate temporary roots and be removed
after evidence capture. The two smoke regenerations must use separate output
and Matplotlib configuration roots.

The task must not run `./scripts/verify.sh`. That remains a user-owned gate
after the source-changing repairs finish.

## Required end state

Return `READY_FOR_USER_FULL_VERIFICATION` only when every acceptance criterion
in the authoritative instruction set passes.

The canonical smoke must end as:

```text
verification.status=pending_user_full_verification
verification.seal_state=unsealed
```

This is expected. Editing source invalidates the old external seal. It is not a
regression if the newly refreshed package is pending; it is the only honest
state before the user reruns full verification.

If any required check fails, return `BLOCKED_BEFORE_FULL_VERIFICATION`, state
the exact failed gate and evidence, and do not tell the user to run the full
verifier.

## Mandatory non-actions

The implementation chat is not authorized to:

- run E06 standard;
- run E06 qualification;
- run the 913,000,000-step workload;
- run `./scripts/verify.sh`;
- create `projects/frontiers_article/approvals/E06_STANDARD_GO.md`;
- make a Sol release decision;
- adjudicate C8 or C9;
- change the claim ledger;
- edit manuscript/submission content;
- replace or reinterpret Figure 4;
- change M4 semantics or RNG order;
- change frozen configs, scenarios, seeds, horizons, n, bootstrap count,
  schemas, gzip settings, or resource limits;
- weaken validation or delete coverage;
- commit, push, reset, clean, or discard user-owned work without a separate
  explicit user request.

## Expected changed surfaces

The exact implementation will determine the minimal set, but likely surfaces
include:

- `src/gifted_masking/experiments/e06.py`;
- `tests/test_article_e06.py`;
- `ARCHITECTURE.md`;
- `projects/frontiers_article/E06_STANDARD_READINESS_IMPLEMENTATION.md`;
- the compression amendment and future review/GO operational instructions;
- `projects/frontiers_article/CURRENT_STATE.md`;
- `projects/frontiers_article/BACKLOG.md`;
- `projects/frontiers_article/STAGE2_EXECUTION_LOG.md`;
- `projects/frontiers_article/checkpoints/E06_STANDARD_COMPRESSION_FIXTURE.json`;
- a new preverification checkpoint;
- a machine assessment index;
- focused logs and user full-verification instructions;
- the canonical smoke manifest/report after the pending-package refresh.

Do not hand-edit scientific CSVs or the figure. They must be regenerated by the
approved deterministic smoke path and match the frozen bytes.

## What the final response must prove

The fresh chat's final response must begin with exactly one of:

- `READY_FOR_USER_FULL_VERIFICATION`; or
- `BLOCKED_BEFORE_FULL_VERIFICATION`.

It must then report, with exact values:

- every file changed or created;
- what was implemented for each of the five findings;
- deterministic fixture hashes, sizes, runtimes, and RSS;
- the single reconciled projection and every frozen limit;
- actual peak retained packed rows;
- adversarial case counts for fixture, phase-stop, retention, and Git-drift
  coverage;
- focused test counts and runtimes;
- two-root smoke scientific-byte comparison;
- normalized manifest/report comparison;
- canonical pending/unsealed state;
- confirmation that standard, qualification, full verification, C8/C9,
  ledger, manuscript, and Figure 4 were untouched;
- `git diff --check`;
- task-only diffstat, with pre-existing dirty-state caveat;
- the exact user verification command only if ready.

No full unified diff should be pasted.

## What happens after a ready hand-back

This sequence is informational; the implementation chat must stop after the
ready hand-back:

1. the user runs the supplied repository verification command and preserves
   the log and exact exit record;
2. a bounded sealing task validates that evidence and reseals the refreshed
   smoke package;
3. a fresh independent `gpt-5.6-sol` review at `xhigh` reassesses the complete
   compression/authorization package;
4. only an independent `GO_STANDARD` decision may create the canonical GO;
5. only then may the user consider executing E06 standard;
6. qualification remains refused unless a separate future protocol explicitly
   authorizes it.

Do not collapse those stages.

## Copy-ready prompt for the fresh chat

```markdown
Implement the bounded E06 compression release-gate repairs in
`/Users/omer/workspace/personal/repos/gifted-masking`.

Use gpt-5.6-terra with high reasoning. This is an implementation task, not an
independent release review.

Before editing, read these two files completely:

1. `projects/frontiers_article/E06_COMPRESSION_FIX_IMPLEMENTATION_CHAT_HANDOFF.md`
2. `projects/frontiers_article/E06_COMPRESSION_FIX_IMPLEMENTATION_CODEX_INSTRUCTIONS.md`

Then read every prerequisite named in their “Required preparation” sections,
including `AGENTS.md` and the controlling Sol review. Inventory and preserve the
existing dirty worktree. Write a concise plan and explicit acceptance criteria
before changing code.

Repair exactly the five findings from
`projects/frontiers_article/checkpoints/E06_COMPRESSION_SOL_REVIEW.md`:

1. authenticate the canonical full-cardinality compression fixture and its
   deterministic bytes during production preflight;
2. enforce runtime, RSS, logical-byte, compressed-byte, and stored-total stops
   at bounded intervals throughout every expensive phase;
3. enforce and instrument a strict maximum of one 400-row packed family during
   independent replay;
4. create one componentwise-conservative canonical resource projection with
   named origins and use it everywhere;
5. implement content-aware post-seal dirty-state validation and extend the
   future GO schema to bind the exact independent review checkpoint path/hash.

Use only the workspace environment at
`/Users/omer/workspace/venvs/venv314`. Add focused and adversarial tests. Run
two deterministic non-scientific fixture regenerations and two smoke
regenerations only after focused gates pass. Preserve all eight frozen smoke
scientific artifacts byte-for-byte. Refresh the canonical package to
`pending_user_full_verification` / `unsealed` and stop.

Do not run E06 standard, E06 qualification, the 913,000,000-step workload, or
`./scripts/verify.sh`. Do not create `E06_STANDARD_GO.md`. Do not adjudicate
C8/C9, change model/RNG semantics, alter frozen configs or limits, edit claims
or manuscript content, replace Figure 4, commit, push, reset, or clean the
worktree.

Return exactly `READY_FOR_USER_FULL_VERIFICATION` if every documented gate
passes. Otherwise return exactly `BLOCKED_BEFORE_FULL_VERIFICATION` with the
failed gate and evidence. Follow the full final-report contract in the
instruction set.
```
