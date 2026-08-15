# E06 compression release-gate repair — Codex implementation instructions

## Task configuration

- **Model:** `gpt-5.6-terra`
- **Reasoning effort:** `high`
- **Mode:** standard/default task mode
- **Working directory:** `/Users/omer/workspace/personal/repos/gifted-masking`
- **Task type:** bounded `FIX_IMPLEMENTATION`

Use a fresh implementation task. Do not continue the independent Sol review
task. Terra owns implementation only; it must not make the release decision.

## Objective

Repair exactly the five release-gate defects identified in
`projects/frontiers_article/checkpoints/E06_COMPRESSION_SOL_REVIEW.md`:

1. authenticate the canonical compression fixture and its deterministic bytes
   during production readiness/preflight;
2. enforce every resource stop at bounded intervals throughout all expensive
   standard phases;
3. reduce second-pass packed-row retention to one 400-row family;
4. emit one reconciled conservative resource projection everywhere;
5. enforce a content-aware post-seal Git-drift policy at standard preflight.

End at one of:

- `READY_FOR_USER_FULL_VERIFICATION`; or
- `BLOCKED_BEFORE_FULL_VERIFICATION` with exact evidence.

This task cannot return `GO_STANDARD` and cannot create
`projects/frontiers_article/approvals/E06_STANDARD_GO.md`.

## Absolute prohibitions

Do not:

1. run E06 standard;
2. run E06 qualification;
3. run `./scripts/verify.sh`;
4. execute any 913,000,000-step scientific workload;
5. adjudicate C8 or C9;
6. update the claim ledger, manuscript, submission files, or Figure 4;
7. change maintained M4 semantics or RNG behavior;
8. change standard/smoke/qualification configs;
9. change scenarios, seeds, horizons, n, km grid, bootstrap count, schemas,
   gzip settings, or resource limits;
10. weaken validation or convert a stop into a delayed warning;
11. make smoke inferential;
12. create a Git commit or push unless the user separately requests it.

Temporary non-scientific fixtures and synthetic test packages are allowed only
under fresh `/private/tmp` or test temporary directories. Preserve user-owned
working-tree changes and do not delete unrelated outputs.

## Required preparation

Before editing:

1. read `AGENTS.md` completely;
2. run and record `git status --short`, `git branch --show-current`, and
   `git rev-parse HEAD`;
3. verify `projects/frontiers_article/approvals/E06_STANDARD_GO.md` is absent;
4. verify the canonical smoke is currently `passed` /
   `external_evidence_verified`;
5. record all eight smoke scientific hashes;
6. write a concise implementation plan and acceptance criteria;
7. compare the planned design with `ARCHITECTURE.md`, the compression
   amendment, readiness design, and Sol review;
8. update design/state/backlog documentation before finalizing code.

Read these files completely before acting:

- `ARCHITECTURE.md`
- `projects/frontiers_article/RDS.md`
- `projects/frontiers_article/STAGE2_EXPERIMENT_SPECIFICATIONS.md`
- `projects/frontiers_article/E06_CODEX_INSTRUCTION_SET.md`
- `projects/frontiers_article/E06_STANDARD_READINESS_IMPLEMENTATION.md`
- `projects/frontiers_article/E06_COMPRESSION_SOL_REVIEW_CODEX_INSTRUCTIONS.md`
- `projects/frontiers_article/approvals/E06_SMOKE_APPROVAL.md`
- `projects/frontiers_article/approvals/E06_STANDARD_COMPRESSION_AMENDMENT.md`
- `projects/frontiers_article/checkpoints/E06_STANDARD_COMPRESSION_FIXTURE.json`
- `projects/frontiers_article/checkpoints/E06_STANDARD_READINESS_IMPLEMENTATION_CHECKPOINT.md`
- `projects/frontiers_article/checkpoints/E06_COMPRESSION_SOL_REVIEW.md`
- `projects/frontiers_article/CURRENT_STATE.md`
- `projects/frontiers_article/BACKLOG.md`
- all E06 entries in `projects/frontiers_article/STAGE2_EXECUTION_LOG.md`
- `configs/frontiers_article/e06_m4_paths_smoke.json`
- `configs/frontiers_article/e06_m4_paths_standard.json`
- `configs/frontiers_article/e06_m4_hysteresis_qualification.json`
- `src/gifted_masking/experiments/e06.py`
- `src/gifted_masking/models/m4.py`
- `src/gifted_masking/core.py`
- `src/gifted_masking/cli.py`
- `tests/test_article_e06.py`
- `scripts/verify.sh`

## Frozen scientific and operational contract

All repairs must preserve:

- five masters `2026081601`--`2026081605`;
- nine scenarios and 26 families per master;
- 130 total families;
- n=400 and 52,000 packed rows;
- 36,000 22-segment plus 16,000 11-segment rows;
- 913,000,000 learner steps;
- 10,000 complete-master bootstrap resamples;
- exact semantic segment seeds and declaration ordering;
- standard raw `_units.csv.gz`;
- gzip level 9, `mtime=0`, empty filename, one member;
- exact logical 55-column CSV;
- 600-second, 150-MiB compressed-raw, 200-MiB stored-total,
  512-MiB RSS, and 400-MiB logical-raw limits;
- smoke scientific bytes and noninferential status;
- unconditional qualification refusal.

## Repair 1 — authenticate fixture evidence at production preflight

### Required behavior

The production standard authorization/readiness path must reject unless all of
the following are true before the requested output directory is created:

1. the canonical fixture-record path is exact;
2. its file SHA-256 equals
   `sealed_manifest.standard_projection.compression_fixture_record.sha256`;
3. the sealed smoke manifest used for this comparison is the same manifest
   whose SHA-256 is bound by the future GO;
4. config hash, current source fingerprint, fixture version, row split,
   scientific=false marker, gzip settings, arithmetic, and limits are exact;
5. a fresh deterministic full-cardinality fixture regeneration independently
   reproduces:
   - 52,000 rows;
   - 36,000 22-segment and 16,000 11-segment records;
   - logical byte count and SHA-256;
   - compressed byte count and SHA-256;
   - canonical gzip header/member/trailing-byte contract;
   - the high-entropy generator identity/version;
6. both the recorded and fresh fixture runtime/RSS measurements pass their
   applicable limits;
7. the fresh temporary artifact is removed on success and failure.

Do not trust caller-supplied hashes merely because they are hexadecimal and
arithmetically consistent.

### Implementation guidance

- Keep the fixture JSON outside `SOURCE_FINGERPRINT_PATHS`; including a record
  that contains the source fingerprint would create a self-reference.
- Bind the fixture record through its exact SHA-256 embedded in the sealed
  smoke manifest.
- Bind generator code through the normal ordered source fingerprint.
- Add a production preflight helper that receives canonical root/config/smoke
  paths and does not accept arbitrary caller-provided readiness dictionaries.
- Regenerate under a unique `/private/tmp` path created by `tempfile`; do not
  write under the requested standard output root.
- Count fixture-authentication runtime in the standard 600-second readiness
  projection.
- Compare deterministic fields exactly. Runtime/RSS may vary, but both the
  canonical observation and fresh observation must be finite and within
  limits.

### Required adversarial tests

Reject before requested output-root creation:

- canonical record altered without updating the sealed record hash;
- internally consistent record with `compressed_bytes=1`, recomputed MiB
  arithmetic, and fabricated all-zero hashes;
- fabricated record plus a correspondingly fabricated temporary manifest;
- correct sizes with wrong logical hash;
- correct hashes with wrong row split;
- wrong fixture version or generator identity;
- correct record but fresh regeneration mismatch;
- stale config or source fingerprint;
- noncanonical gzip metadata or multiple members;
- fixture regeneration exceeding time or RSS;
- missing or undeletable temporary fixture.

The fabricated-manifest test must still fail through deterministic
regeneration, proving the record is not self-authenticating.

## Repair 2 — continuous resource-stop enforcement

### Required design

Introduce one experiment-local resource guard used throughout the standard
path. It should support dependency injection for tests and own:

- monotonic clock source;
- RSS source;
- started time;
- runtime limit;
- compressed-raw limit;
- logical-raw limit;
- stored-total limit;
- RSS limit;
- current phase name;
- check counter/diagnostics.

The guard must raise immediately when a limit is crossed and include the phase
and breached limit in the error. Production defaults remain exactly the frozen
limits. Tests may inject fake clock/RSS/byte counters; production may not.

### Required check points

Call the guard at bounded intervals—not only before and after—inside:

1. fixture authentication/regeneration;
2. every standard family generation;
3. long segment simulation loops, at a documented bounded step interval;
4. every logical CSV write or bounded row interval;
5. compressed-output growth checks;
6. standard cell/loop/effect derivation outer loops;
7. bootstrap loops at a documented bounded replicate interval;
8. every family and bounded child interval in second-pass replay;
9. table serialization, preferably per row/chunk;
10. parsed-derived validation outer loops;
11. before and after each figure panel and before/after save;
12. report construction;
13. manifest construction;
14. immediately before each promotion;
15. immediately after promotion and before returning.

Give `_LogicalCsvWriter` a checked logical-byte ceiling so the 400-MiB stop is
enforced while writing rather than after gzip closure. Stored raw/total sizes
must likewise be checked as files grow.

Do not add a new dependency. Do not thread a generic callback through
maintained M4 code; resource guarding remains E06 experiment-local.

### Required injected-failure tests

For each major phase, inject deterministic crossings and prove:

- time breach aborts within the documented interval;
- RSS breach aborts within the documented interval;
- logical-byte breach stops the writer at or before the first over-limit write;
- compressed/stored-byte breach aborts before publication;
- bootstrap breach stops before completing all 10,000 replicates;
- replay breach stops before completing all 130 families;
- figure/report/manifest breach prevents manifest promotion;
- no final package file exists after failure;
- temporary files are cleaned.

Tests must use small synthetic configs/data and must not execute standard.

## Repair 3 — enforce one-family packed-row retention

### Required second-pass architecture

For each expected family:

1. independently reconstruct exactly one 400-row expected family;
2. read one candidate CSV row at a time from the decompressed stream;
3. compare that single parsed row with the corresponding expected row;
4. discard the candidate row immediately;
5. derive or validate cells using the already validated expected family or
   bounded online aggregates;
6. release the expected family before reconstructing the next family.

Never retain a 400-row `candidate` list alongside the 400-row expected list.
Do not weaken the comparison: all 55 fields, exact types, packed JSON,
ordering, continuity, seeds, counts, rewards, p, and both Q values still apply.

Refactor the comparator as needed into a single-row primitive plus a list
wrapper used by existing materialized smoke tests.

### Instrumentation

Expose non-scientific validation diagnostics such as:

- `peak_retained_packed_rows`;
- `families_validated`;
- `rows_validated`;
- `cells_validated`.

The production second pass must report
`peak_retained_packed_rows <= 400`. Define precisely what counts as a retained
packed row; the current expected family counts, the transient candidate row
counts as one only if it coexists, so a design retaining 400 expected rows plus
one candidate dictionary must document whether its structural maximum is 401.

Prefer a strict maximum of 400 total packed row dictionaries by comparing the
candidate row against a serialized/field expectation generated per child, or
by releasing/replacing one expected entry before retaining the candidate. If a
transient parser dictionary is unavoidable, revise the design so the expected
family contains 399 remaining rows at that moment. Do not reinterpret the gate
as “two bounded families are acceptable.”

### Required tests

- exact smoke gzip replay succeeds;
- synthetic standard-shaped family replay succeeds;
- instrumented peak is at most 400;
- a deliberately reintroduced candidate-family list makes the instrumentation
  test fail;
- reordered, duplicate, missing, foreign, schema-altered, and cell/quantile
  corruptions still fail;
- memory diagnostics are deterministic and included in validation evidence.

## Repair 4 — one canonical conservative resource projection

### Required projection

Create one machine-readable canonical projection object. It must use
componentwise conservative maxima with named origins and include at least:

- primary scientific simulation;
- independent replay simulation;
- logical CSV/gzip serialization;
- fixture-authentication regeneration;
- derived analysis;
- 10,000-replicate bootstrap;
- figure/report/manifest overhead;
- startup/fixed overhead;
- compressed raw bound;
- logical raw bound;
- stored-total bound;
- RSS bound.

Do not select a lower total merely because a later probe was faster. Preserve
the prior conservative component floors that produced the approximately
434.753-second estimate, add fixture-authentication time explicitly, and use
componentwise maxima against fresh measurements. The resulting canonical time
may therefore be higher than 434.753 seconds but must remain ≤600 seconds to
pass. Fail closed if it does not.

Recommended structure:

```json
{
  "method": "componentwise_conservative_maxima_v1",
  "components": {
    "simulation": {"seconds": 0, "origins": []},
    "streaming_replay": {"seconds": 0, "origins": []},
    "serialization": {"seconds": 0, "origins": []},
    "fixture_authentication": {"seconds": 0, "origins": []},
    "derived_bootstrap": {"seconds": 0, "origins": []},
    "figure_report_manifest": {"seconds": 0, "origins": []}
  },
  "seconds": 0,
  "compressed_raw_mib": 0,
  "logical_raw_mib": 0,
  "stored_total_mib": 0,
  "peak_rss_mib": 0,
  "limits": {},
  "within_limits": true
}
```

The exact same canonical object must appear in:

- smoke manifest;
- smoke report;
- readiness checkpoint;
- standard preflight evidence;
- future standard manifest, if later authorized.

If prose rounds values, retain full machine precision in the canonical object
and state the rounding rule. Remove or explicitly supersede conflicting
434.753/226.438 and 387.706/237.219 figures.

### Required tests

- componentwise maximum selects the larger value for every component;
- fixture-authentication time cannot be omitted;
- changing a lower/faster observation does not lower a preserved conservative
  floor;
- each individual and aggregate limit is fail-closed;
- manifest/report/checkpoint serialization derives from one object;
- altered projection arithmetic or origin metadata is rejected.

## Repair 5 — content-aware post-seal Git drift

### Problem to solve

`git status --porcelain` records status/path but not file content. A path that
was already untracked at seal time can change content without changing the
porcelain payload. The production boundary must therefore bind file content,
not only the porcelain text.

### Required sealed Git evidence

The next smoke manifest must record:

- Git HEAD;
- branch;
- exact porcelain payload;
- porcelain SHA-256;
- an ordered dirty-path inventory containing for every regular file named by
  porcelain:
  - status code;
  - canonical relative path;
  - file byte count;
  - SHA-256;
- explicit handling/rejection for renames, deleted files, symlinks,
  directories, unreadable paths, and paths outside the repository.

The preverification recorder and external sealer must independently reconstruct
and validate this complete inventory before sealing.

### Allowed post-seal drift

At future standard preflight, every sealed baseline dirty-path entry must still
match status, bytes, and SHA-256 except these narrowly justified records:

1. the canonical sealed smoke manifest itself, whose exact bytes are bound by
   `smoke_manifest_sha256` in the GO;
2. the sealed smoke report, whose exact hash is bound by the sealed manifest;
3. the fresh independent Sol review checkpoint, whose exact path and SHA-256
   must be bound by the GO;
4. the canonical GO file, whose complete strict machine binding is validated
   directly.

No other new, removed, status-changed, or content-changed path is allowed.

Because the review checkpoint must be content-bound, extend the future GO
binding schema in a documented, fail-closed way to include exactly:

- `review_checkpoint_path`;
- `review_checkpoint_sha256`.

Update `GO_BINDING_FIELDS`, the parser, the independent validator, standard
authorization, tests, operational instructions, and the future Sol prompt.
The GO must still have exactly one fenced machine block, ordered keys, string
values, exact canonical paths, exact command, and `qualification=REFUSED`.

The GO file cannot hash itself; its contents are authenticated by strict schema
and independently recomputed field values. Do not introduce a self-referential
GO hash.

### Required adversarial tests

Reject before requested output-root creation:

- unrelated new untracked file;
- unrelated modified tracked file;
- changed content at a path that was already untracked during sealing;
- status-preserving content drift;
- missing/deleted/renamed baseline dirty path;
- symlink substitution;
- altered smoke report;
- altered review checkpoint;
- wrong review checkpoint path/hash in GO;
- an extra nominally “allowed” path;
- changed manifest not matching GO smoke-manifest SHA;
- copied GO at a noncanonical path;
- malformed or duplicate-key GO;
- qualification attempt.

Use temporary synthetic repositories/packages where practical. Do not create
the real canonical GO during this task.

## Canonical fixture and resource evidence regeneration

After the implementation and focused tests pass:

1. regenerate the exact 52,000-row non-scientific fixture in a fresh process
   under `/private/tmp`;
2. independently regenerate it a second time;
3. require byte-identical gzip, logical/compressed hashes, row split, and
   deterministic metadata;
4. record measured runtime/RSS from both and use their maxima;
5. remove temporary 90-MiB fixture files after evidence capture;
6. refresh `E06_STANDARD_COMPRESSION_FIXTURE.json` through a documented
   generator/validator, not manual guessed values;
7. compute the reconciled canonical projection;
8. ensure both strict and formal gates pass.

This is non-scientific capacity work. It must never be interpreted as C8/C9
evidence.

## Focused verification matrix

Run with `/Users/omer/workspace/venvs/venv314/bin/python` and isolated
`MPLCONFIGDIR` paths:

1. full `tests/test_article_e06.py`;
2. `tests/test_m4.py`;
3. `tests/test_core.py tests/test_determinism.py`;
4. `tests/test_manifest_completeness.py tests/test_primary_raw_schema.py
   tests/test_summary_matches_raw.py`;
5. new phase-stop injection cases;
6. new single-family retention instrumentation cases;
7. new fabricated-but-consistent fixture cases;
8. new post-seal content-drift cases;
9. `py_compile` for changed Python files;
10. `git diff --check`.

Do not run the repository-wide verifier. Do not lower test counts by deleting or
merging existing coverage.

## Smoke preservation and pending-package refresh

Only after all implementation/focused gates pass:

1. record the current eight canonical smoke scientific hashes;
2. regenerate smoke into two distinct fresh output roots with distinct
   `MPLCONFIGDIR` directories;
3. require raw, cells, paths, loops, transitions, effects, PNG, and warnings to
   match each other and the frozen hashes byte-for-byte;
4. require normalized manifests and reports to match under the explicit
   permitted normalization rules;
5. regenerate canonical smoke against current source;
6. attach fresh focused and deterministic evidence;
7. leave canonical verification exactly:

```text
verification.status=pending_user_full_verification
verification.seal_state=unsealed
```

8. produce user verification instructions and stop.

Do not call the production sealer without new user-owned verification evidence.
Historical verification cannot seal changed source.

## Documentation deliverables

Update:

- `ARCHITECTURE.md`;
- `projects/frontiers_article/E06_STANDARD_READINESS_IMPLEMENTATION.md`;
- `projects/frontiers_article/CURRENT_STATE.md`;
- `projects/frontiers_article/BACKLOG.md`;
- `projects/frontiers_article/STAGE2_EXECUTION_LOG.md`;
- the E06 operational/review instruction documents affected by the extended GO
  schema;
- a new checkpoint:
  `projects/frontiers_article/checkpoints/E06_COMPRESSION_RELEASE_FIX_PREVERIFY.md`;
- a machine assessment index under `results/manifests/`;
- focused logs under a new E06-specific `results/reports/` directory;
- user-owned full-verification instructions under `results/reports/`.

Correct the stale backlog checkbox identified by Sol. Do not rewrite historical
review decisions.

## Acceptance criteria

Return `READY_FOR_USER_FULL_VERIFICATION` only if all are true:

1. no canonical GO exists;
2. standard and qualification were not run;
3. fixture record hash is bound by the sealed/pending smoke projection;
4. fresh deterministic full fixture authentication is required by production
   standard preflight before output-root creation;
5. internally consistent fabricated fixture evidence is rejected;
6. all long phases enforce runtime/RSS/byte stops at bounded intervals;
7. injected phase breaches abort before promotion and clean temporary files;
8. replay peak retained packed rows is instrumented and ≤400;
9. all raw/cell adversarial rejection remains intact;
10. exactly one canonical componentwise-conservative projection is used in all
    evidence surfaces;
11. projection includes fixture authentication and passes every frozen limit;
12. sealed dirty inventory is content-aware;
13. future standard preflight rejects every unallowed post-seal change;
14. extended GO schema binds exact independent-review checkpoint path/hash;
15. qualification remains refused in parser, validator, CLI, and tests;
16. focused suites and post-artifact tests pass;
17. two fixture regenerations are deterministic;
18. two smoke regenerations preserve all eight scientific artifacts;
19. canonical package is refreshed and remains pending/unsealed;
20. `git diff --check` passes;
21. no claim, manuscript, or scientific result changed.

If any criterion fails, return `BLOCKED_BEFORE_FULL_VERIFICATION`. Do not ask
the user to run the full verifier.

## Required final response

Lead with exactly `READY_FOR_USER_FULL_VERIFICATION` or
`BLOCKED_BEFORE_FULL_VERIFICATION`.

Then report:

- files changed/created;
- exact implementation of each of the five repairs;
- fixture deterministic hashes, sizes, runtimes, and RSS;
- reconciled canonical projection and all limits;
- peak retained packed rows;
- adversarial fixture/phase/drift coverage counts;
- focused suite counts/runtimes;
- two-root smoke scientific-byte and normalized comparisons;
- canonical pending/seal status;
- explicit confirmation that standard, qualification, full verification,
  C8/C9 adjudication, ledger, manuscript, and Figure 4 were not run/changed;
- `git diff --check` and task-only diffstat;
- exact next user command only if status is ready.

Do not include a full unified diff.

## Copy-ready prompt

```markdown
Implement the bounded E06 compression release-gate repairs.

Use gpt-5.6-terra with high reasoning in
`/Users/omer/workspace/personal/repos/gifted-masking`.

Read
`projects/frontiers_article/E06_COMPRESSION_FIX_IMPLEMENTATION_CODEX_INSTRUCTIONS.md`
completely and follow it exactly. Repair only the five findings in
`projects/frontiers_article/checkpoints/E06_COMPRESSION_SOL_REVIEW.md`:
fixture authentication, continuous phase resource stops, strict one-family
replay retention, one reconciled conservative projection, and content-aware
post-seal Git drift.

Do not run E06 standard, qualification, or `./scripts/verify.sh`. Do not create
`E06_STANDARD_GO.md`, adjudicate C8/C9, or modify scientific semantics,
configs, claims, manuscript, or Figure 4. Use focused tests and non-scientific
fixtures only. Refresh smoke only after all focused gates pass, preserve all
eight scientific artifact bytes, leave the package pending/unsealed, and
return exactly `READY_FOR_USER_FULL_VERIFICATION` or
`BLOCKED_BEFORE_FULL_VERIFICATION`.
```
