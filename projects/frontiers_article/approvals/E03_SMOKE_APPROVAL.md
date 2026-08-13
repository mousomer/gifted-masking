# E03 Scientific Approval Record

**Decision:** `APPROVED_FOR_SMOKE`  
**Date:** 2026-08-12  
**Scientific owner:** `gpt-5.6-sol`, `xhigh`  
**Scope:** bounded E03 implementation and smoke only

## Frozen provenance

The maintained 226/357 result was independently reproduced at commit
`e0e9a738986dd440180a228b024b0807336cd957` from
`scripts/map_m2_lock_in_regions.py`, `models/m2.py`, and
`analysis/m2_optimal.py`. The grid is p=0:.05:1 by eta=0:.05:.8, default
environment/learner, n=160, T=1000, final .2. There is no original master seed:
the exact cell seed is `9100 + 100*eta_index + p_index`. Replay matched all 357
stored rows, 226 legacy learned-suboptimal cells, fraction
`.6330532212885154`, and classified-cell mean neutral masking
`.9501766068109203`. Stored map SHA-256 is
`bb220dddc16335e9fc901a2e8be53f6d7c1a90aed8198fae3b2fd56e46e3ef2b`.

## Comparator and classification freeze

Use the maintained reward-first objective transition table. Accepted turnover
and stigma escape affect next state as implemented; successful redemption
remains accepted. Comparator discount equals cell gamma. Value iteration uses
Bellman tolerance 1e-10, max 100000, absolute Q-tie tolerance 1e-10, and must
converge. Threshold bracket tolerance 1e-4 is separate.

Keep `legacy_region`, `objective_regime`, and `learner_status` separate. State
visit adequacy requires total visits >=max(100,n) and visiting children
>=max(16,ceil(.2*n)). Learned neutral ties and inadequate visits are
inconclusive. Missing stigma visits at p=1 do not erase an adequate neutral
mismatch. Full policy value/regret is blank unless every dynamically required
state has adequate action counts. Neutral decision regret is the strict optimal
neutral Q gap.

## Frozen smoke

Config `configs/frontiers_article/e03_m2_regime_smoke.json`, run ID
`frontiers_m2_regime_replication_v1_smoke`, master seed 2026081399, bootstrap
2026081397, workers 1, default environment and learner. It contains:

1. `legacy_provenance_replay`: all 357 original cells with original n/T/window
   and seed mapping, emitting cell diagnostics only.
2. `smoke_sentinels`: six cells (.35,0),(.40,0),(.55,0),(.55,.20),(.75,0),
   (.90,.20), n=64,T=300,window=.2, producing 384 child rows.

Stop if legacy replay differs in any row/count/mean. Expected smoke is 57.24m
learner-steps, about 18 seconds, under 60 seconds and 20 MB.

New E03 streams use canonical semantic IDs, SHA-256 first 16 bytes as four
little-endian uint32 words, `SeedSequence([master_seed,3,words...])`, one
spawned uint64 cell seed, and the maintained vectorized M2 kernel. Child seed is
blank. Parameter IDs include every parameter/run field. Only T/window variants
share a trajectory-prefix RNG family; record that pairing.

Implement the exact ordered primary schema frozen in the scientific approval:
identifiers/component/sensitivity/seed fields; all environment/learner/run
parameters; window/count/reward diagnostics; six state-action counts; three
state visits; and final state. Per-child totals must reconcile exactly.

## Staged standard, not executable in smoke pass

Config `configs/frontiers_article/e03_m2_regime_standard.json`, approval false,
five seeds 2026081301-05:

- exact 357 grid/seed, n160/T1000/window.2;
- six sentinels with OAT variants n320; T2000/5000; window .1/.4;
  alpha .03/.3; tau .1/.6; lambda .5/2.5; q0 .75; gamma .5/.99;
- harsh p=.70/.75/.80, eta0, **b2=0**, r2=8, delta=.30, gamma=.9;
- objective and learned threshold refinement under the approved bounded rules.

No factor crossing. Exact-grid denominator remains 357. Objective thresholds
bisect for eta 0/.2/.8 to width <=1e-4. Learned refinement uses five seeds,
dyadic adjacent-boundary points, width <=.0125 or eight added p values per eta,
reports reversals, and never extrapolates missing crossings.

Required outputs: manifest; primary units; cell, effects/seed-fraction,
stable-cell, threshold, and legacy-replay CSVs; diagnostic PNG; self-contained
report. Smoke must include strict E03 config/approval validation, semantic and
VI tests, tie/visit/p=1 tests, count/window/reward reconciliation, deterministic
order/prefix/global-RNG tests, raw-summary at 1e-12, interval/refinement tests,
b2=0 harsh test, E01/E02 non-regression, and full verification. Do not place the
full 357 replay in routine unit tests.

Decision rules and all sentinel counts/Q gaps are exactly those in the
scientific approval response and `STAGE2_EXPERIMENT_SPECIFICATIONS.md`. Broad
support later requires >=179 stable learned-suboptimal cells, lower seed-level
fraction CI >.40, and stable n/T/window directions at five dynamic-authenticity
sentinels. The legacy 226/357 remains provenance, not the publication headline.
