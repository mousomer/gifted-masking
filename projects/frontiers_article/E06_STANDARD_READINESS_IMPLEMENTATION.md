# E06 standard-readiness implementation design

**Status:** deterministic-compression amendment implementation in progress
**Authority:** `approvals/E06_SMOKE_APPROVAL.md` and
`checkpoints/E06_ROUND2_SOL_SMOKE_REVIEW.md`
**Execution boundary:** implement and test; do not run standard or qualification

## Objective

Close the Round 2 `FIX_IMPLEMENTATION` findings without changing the frozen
M4 model, E06 configurations, RNG hierarchy, smoke scientific artifacts, or
claim boundaries. The implementation must make the exact five-master E06 core
standard executable only after a canonical `E06_STANDARD_GO.md` passes a
fail-closed binding check. Qualification remains unconditionally refused.

## Frozen standard contract

- exact config: `configs/frontiers_article/e06_m4_paths_standard.json`;
- five master seeds `2026081601`--`2026081605`;
- nine scenarios, 26 path families per master;
- 400 children per family;
- 52,000 packed primary rows and 913,000,000 learner steps;
- deterministic master → scenario-declaration → path-declaration → child order;
- 10,000 complete-master bootstrap replicates;
- no standard execution during this implementation pass.

## Authorization boundary

The standard runner accepts only the canonical repository path
`projects/frontiers_article/approvals/E06_STANDARD_GO.md`. Before creating any
output directory or file, it must parse a strict machine-readable binding block
and independently match:

- `Decision=GO_STANDARD` and `Experiment=E06`;
- exact standard config path and normalized config SHA-256;
- current E06 source fingerprint;
- sealed smoke-manifest path and SHA-256;
- exact authorized standard command;
- explicit `Qualification=REFUSED`.

Missing, copied, foreign-path, duplicate-key, malformed, wrong-hash, stale, or
source-drifted GO records fail before output creation. The GO record is not part
of the source fingerprint it authorizes.

## Bounded raw architecture

Standard raw generation is family-streamed. At most one 400-row path family is
materialized at a time:

1. derive the family from the frozen config and semantic segment seeds;
2. apply bounded identity, packed-length, count/reward, and bounds invariants;
3. append it to a temporary raw CSV;
4. reduce it to bounded cell aggregates;
5. release the family before continuing.

After generation, an independent streaming raw validator reads exactly 400
rows per expected family, reconstructs that family again, compares every field,
and rejects missing, duplicate, reordered, foreign, truncated, or trailing
rows. The same replay also reconstructs and validates every emitted standard
cell row, including quantiles. Raw and derived files are staged, the runner
refuses any pre-existing target package, and the manifest is promoted last;
any newly promoted files are removed if package publication fails.

This design avoids simultaneous candidate and expected 52,000-row materialized
lists. Derived artifacts are reconstructed from bounded cell/path aggregates,
then validated before atomic promotion. Shard or family boundaries may not
change canonical ordering or bytes.

## Standard derived package

Smoke retains its existing schemas and exact scientific bytes. Standard uses
explicit standard schemas where additional across-seed records are required.

- cells: per master/scenario/path/direction/km, including child quantiles;
- paths: seed-level aligned up/down curves; cold-start endpoint information is
  represented through cells/effects, not a fabricated directional gap;
- loops: seed-level records plus across-seed Student-t summary records;
- transitions: seed-level records plus pooled five-master PAVA/bootstrap records
  for targets `.5` and `.75`;
- effects: seed-level endpoint/control/speed/scenario contrasts plus paired
  five-master Student-t summaries, including S02--S07 versus S01 and active
  S01 versus disabled-feedback S08 placebo contrasts.

Pooled transition bootstrap resamples exactly five complete master pairs with
replacement 10,000 times. A pooled transition is marked decision-eligible only
when its pooled ascending/descending crossings are valid and at least 95% of
bootstrap draws retain valid paired widths; this is an estimability gate, not
C9 adjudication. Children are descriptive units only. Every standard
decision-bearing summary is derived from master-level quantities.

## Ordering and provenance

The manifest declares the actual canonical order:

```text
master_seeds declaration order,
scenarios declaration order,
path_types declaration order,
child_id ascending
```

Complete segment-seed maps are keyed by master, scenario, and path so no master
can overwrite another. The manifest records config, GO, smoke seal, source,
Git state, schemas, counts, hashes, timings, streaming validation, bootstrap,
resource stops, and standard-only inference rules. All files are staged and
the manifest is published last, so a failed run cannot masquerade as a complete
standard package.

## Resource readiness

The execution stop limits remain the frozen approval limits: 600 seconds,
400 MiB raw, 500 MiB total, and 2 GiB RSS. Before another GO review, the
readiness fixture must also satisfy the stricter Round 2 reviewer thresholds:
600 seconds, 150 MiB raw, 200 MiB total, and 512 MiB RSS.

The fresh-process projection must account separately for:

- scientific simulation;
- first-pass family validation and serialization;
- second-pass streaming reconstruction/validation;
- bounded aggregation and derived validation;
- 10,000-replicate bootstrap;
- figure/report/manifest overhead;
- measured high-water RSS of the largest family and validation buffers.

It may use exact frozen-size deterministic fixtures and measured n=400 segment
probes, but may not execute the scientific standard or emit standard artifacts.

The corrected worst-width, field-shaped CSV fixture bounds the required 36,000
22-segment loop rows plus 16,000 11-segment cold-start rows at 344.136 MiB raw
and 376.136 MiB total. Runtime (434.753 s) and RSS (226.438 MiB) pass; the
formal approval limits of 400 MiB raw and 500 MiB total also pass. The later
Round 2 review limits of 150 MiB raw and 200 MiB total do not. Lossless
compression or a different primary format would violate the frozen
`<run_id>_units.csv` contract without a revised approval. The user-authorized
`approvals/E06_STANDARD_COMPRESSION_AMENDMENT.md` now narrowly revises the
future standard primary artifact to deterministic `<run_id>_units.csv.gz`.
Implementation must prove that stored compressed raw and total artifacts meet
the stricter limits while recording the logical CSV hash/size and retaining the
logical 400-MiB bound. No GO follows automatically from this amendment.

## Acceptance criteria before user verification

1. Smoke raw/derived/PNG/warnings bytes remain unchanged.
2. Standard and qualification remain refused without a valid canonical GO.
3. A valid temporary GO binding reaches only a non-executing readiness/dry-run
   path in focused tests; no standard scientific dispatch occurs.
4. Five-master ordering, 52,000-row count, 913,000,000-step count, and unique
   seed-map keys recompute from the exact config.
5. Standard inference helpers pass synthetic five-master tests, including
   censoring and bootstrap-validity boundaries.
6. Streaming validation rejects family-order, row, schema, identity, seed,
   traversal, state, and both-Q corruption.
7. Resource readiness includes both scientific passes. If the stricter Round 2
   thresholds fail—as the corrected CSV bound currently does—standard remains
   blocked pending an independently authorized contract/limit decision.
8. Qualification remains refused in every path.
9. Focused checks pass; `./scripts/verify.sh` is left for the user.

## Compression acceptance criteria

1. Standard writes one deterministic gzip member at level 9, `mtime=0`, with
   no original filename; decompression yields the exact 55-column CSV stream.
2. The manifest binds compressed and logical bytes/hashes and gzip settings.
3. Independent validation rejects noncanonical headers, corruption,
   concatenated members, trailing bytes, and raw/cell semantic changes.
4. An exact 52,000-row high-entropy non-scientific fixture demonstrates stored
   raw ≤150 MiB and total ≤200 MiB without executing standard science.
5. Smoke scientific artifacts remain byte-identical; qualification is refused.

## Compression release-gate correction

The former conflicting projections are superseded by one
`componentwise_conservative_maxima_v1` object. It retains the prior
conservative component floors, adds fresh fixture-authentication time, names
the evidence origins, and fail-closes every individual and aggregate limit.
Production reads only the canonical fixture record whose hash is bound in the
smoke projection, then independently regenerates and byte-authenticates the
52,000-row non-scientific fixture before output directories are created.

The standard guard is experiment-local and checked during fixture generation,
segments/families, logical and compressed writes, derived/bootstrap loops,
streaming replay, table writes, figures, reports, manifests, and promotion.
The second replay releases each expected row before reading its candidate, so
its recorded packed-row high-water is at most 400. A future GO must bind the
exact Sol review checkpoint path and SHA-256, and standard authorization
accepts post-seal Git drift only for explicitly content-bound allowed files.
