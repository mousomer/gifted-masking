# E05 Seed-Extension Audit

**Date:** 2026-08-13  
**Mode:** inspection and deterministic seed-map verification only  
**Scientific simulation:** not run

## Classification

**NOT_EXTENDABLE_AS_FROZEN**

The original five E05 master seeds and every recorded within-master family seed
are frozen and exactly reproducible. No repository authority defines how to
select a sixth or later independent master. Extending the explicit list with a
new `range(...)`, an inferred consecutive integer, a second master key, or an
unrelated list would add a new seed-selection rule and would not be an extension
of frozen E05 semantics.

Article V1 therefore keeps E05 at `n=5` independent master curves.

## 1. Original five master seeds

```text
2026081501
2026081502
2026081503
2026081504
2026081505
```

They are identical in the standard config, smoke approval's staged standard
contract, `E05_STANDARD_GO.md`, runner constant `STANDARD_SEEDS`, manifest, raw
rows, transitions, tests, and adjudication.

## 2. How the five were selected

The repository calls them “reserved” and records them as explicit constants.
No inspected RDS, experiment specification, approval/GO record, execution log,
config, manifest, runner, seed utility, test, report, or adjudication provides a
random draw, parent `SeedSequence`, hash namespace, index-to-master function,
or other deterministic generation rule for the master list itself.

The fact that the constants are consecutive is a naming pattern, not a frozen
extension rule. The bootstrap seed `2026081597` and smoke seed `2026081599` are
separate roles and do not generate standard masters.

## 3. Frozen within-master hierarchy

For architecture `A` and master `M`, the family ID is:

```text
E05|master=M|architecture=A|K=4|identity=fixed0|policy_environment
```

The runner:

1. SHA-256 hashes that exact string;
2. reads the first 16 bytes as four little-endian uint32 words;
3. constructs `SeedSequence([M,5,*words])`;
4. calls `.spawn(1)`;
5. generates one uint64 policy/environment seed;
6. reinitializes that same architecture/master family seed at every `bf`.

This preserves common-random-number child pairing across `bf` inside an
architecture/master family. Flat and hierarchical architectures have distinct
family IDs and are not paired. Acceptance draws remain part of the maintained
architecture-specific policy/environment stream and are consumed on masking.

The analysis-only crossing bootstrap uses
`SeedSequence([2026081597,50,architecture_code])`, with architecture codes 0
and 1. It does not generate scientific learner streams.

## 4. Deterministic verification of recorded families

A lightweight check imported only `derive_e05_policy_environment_seed` and
compared it with the ten manifest rows. It ran no learner or simulation. All
ten matched exactly:

| Master | Architecture | Recorded/derived seed |
| ---: | --- | ---: |
| 2026081501 | flat_2k | 10176655251632140377 |
| 2026081502 | flat_2k | 17052190067641228135 |
| 2026081503 | flat_2k | 11896625273363160903 |
| 2026081504 | flat_2k | 1055363506907428816 |
| 2026081505 | flat_2k | 1966359709496387759 |
| 2026081501 | hierarchical | 11987654733599175808 |
| 2026081502 | hierarchical | 8674624756262987657 |
| 2026081503 | hierarchical | 9519192235456945935 |
| 2026081504 | hierarchical | 8601174811265771167 |
| 2026081505 | hierarchical | 12517807700019067240 |

Thus existing seed maps regenerate exactly. This proves continuity for the
original five only; it does not answer which new master is authorized.

## 5. Extension test

| Question | Finding |
| --- | --- |
| Documented deterministic master-seed generation rule? | No |
| Same frozen derivation usable after a master is supplied? | Yes |
| Frozen authority for choosing additional masters? | No |
| Original five maps reproducible without semantic change? | Yes, exactly |
| Can adding masters be defined as the same frozen design? | No |

An E05 extension could be designed later only as a newly authorized evidence
extension with an explicit selection rule and a clear relationship to the
original five. It cannot be described as merely continuing the current frozen
derivation. No expanded N is selected here and no publication result was
generated.

## Authorities inspected

- `configs/frontiers_article/e05_m3_bflpe_crossover_{smoke,standard}.json`
- `projects/frontiers_article/approvals/E05_{SMOKE_APPROVAL,STANDARD_GO}.md`
- `projects/frontiers_article/STAGE2_EXPERIMENT_SPECIFICATIONS.md`
- `projects/frontiers_article/STAGE2_EXECUTION_LOG.md`
- `projects/frontiers_article/E05_MAIN_RESULTS.md`
- `src/gifted_masking/experiments/e05.py`
- `tests/test_article_e05.py`
- `results/manifests/frontiers_m3_bflpe_crossover_v1.json`
- E05 raw, cell, effect, transition, report, and adjudication records
