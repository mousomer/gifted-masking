# E02 Scientific Approval Record

**Decision:** `APPROVED_FOR_SMOKE`  
**Date:** 2026-08-12  
**Scientific owner:** `gpt-5.6-sol`, `xhigh`  
**Scope:** E02 bounded implementation and smoke only

No scientific blocker remains. This record does not authorize E02 standard,
sensitivity, publication-tier work, claim adjudication, or manuscript edits.

## Frozen configurations

Smoke `configs/frontiers_article/e02_binary_graded_smoke.json` uses run ID
`frontiers_m1_binary_graded_v1_smoke`, architectures `binary_endpoints` with
grid `[0,1]` and `graded_independent_5` with grid `[0,.25,.5,.75,1]`,
`p=[.65,.75,.85]`, payoffs `b=1,a=.6,c=.25,r=2`, learner
`alpha=.1,tau=.25,lambda=1,q0=0`, `n=96`, `T=300`, final fraction `.2`,
master seed `2026081299`, bootstrap seed `2026081297`, and `workers=1`.
Force `d=1` at step 0 in all six architecture cells.

Stage but do not execute `configs/frontiers_article/e02_binary_graded_standard.json`
with the same six cells, `n=500`, `T=2000`, final fraction `.2`, five seeds
`2026081201` through `2026081205`, and `approved_standard=false`. It must reject
execution without a future E02-specific GO record and must reject E01 approval.
Levels 3/9, tau changes, and horizon sensitivities are unauthorized.

At the frozen payoffs, endpoint expected rewards are `.75/.55` at p=.65,
`.75/.85` at p=.75, and `.75/1.15` at p=.85. The unique optimum is d=0 at
.65 and d=1 at .75/.85. Intermediate arms are never statically optimal.

## Matched RNG and semantics

For each master-seed/p pair, make a canonical ID containing E02, p, both grids,
forced-step semantics, payoffs, learner values, n, T, and window. SHA-256 it,
read the first 16 bytes as four little-endian uint32 words, construct
`SeedSequence([master_seed,2,word0,word1,word2,word3])`, spawn one sequence, and
generate one uint64 policy/environment seed. Initialize separate architecture
generators with that identical seed.

Each step: sample softmax action; draw one latent acceptance uniform per
learner; after consuming the policy draw force d=1 at t=0; accept when
`u < 1-(1-p)d`; calculate objective reward; apply subjective value only to the
selected-arm update; accumulate diagnostics. Matched rows must share the exact
initial uniform, outcome, and reward. Child pairing is valid only within the
same master seed and p.

Do not share endpoint experience with intermediate arms, update unchosen arms,
redistribute softmax mass, rescale temperature, or add full-auth exposures.

## Definitions

- Any disclosure: d>0; full authenticity: d=1; intermediate: 0<d<1.
- Post-initial exploration metrics exclude t=0.
- Modal arms must be unique; ties are explicit and are not selections.
- Stable full-auth modal-policy time is the earliest pre-action t>=1 from which
  d=1 remains the unique Q-maximizer through T-1 with at least one final-window
  length remaining; otherwise censored.
- Pseudo-regret is `max(E0,E1)-E(d_t)` and includes the forced initial action.
- Normalized regret divides by `T*abs(E1-E0)`. For graded learners this is mean
  distance from the optimal endpoint, not a suboptimal-action count.
- Rejection exposure is rejected d>0 trials after t=0 divided by T-1.
- Exploration reward variance is population variance over post-initial d>0
  rewards, with denominator/undefined cases recorded.

## Primary schema

One row per child/architecture/p with ordered fields covering identifiers and
the matched seed; p/grid/payoff/learner/run metadata; analytic endpoint values;
forced initial policy index/disclosure/uniform/outcome/reward/value; time to
next any/full disclosure and stable full-auth policy with censoring; steps
1-100 and post-initial any/intermediate/full counts/rates; disclosure rejection
and exploration reward count/mean/variance; final-window any/full counts/rates,
mean disclosure, unique modal/index/disclosure/endpoint flags; realized payoff,
regret; compact ordered total action/accept/reject/final counts and final Q.

Exact ordered field list is the `Ordered raw schema` under E02 in the scientific
approval response recorded in this task history and must be copied into the
implementation as a constant. Compact JSON vectors follow disclosure-grid
order. `child_seed` is blank and `rng_unit=vectorized_matched_pair_stream`.
Sort by matched-pair cell ID, master seed, child ID, architecture.

## Outputs and effects

Create a 15-row arm benchmark with p, d, acceptance probability, accepted and
rejected rewards, expected reward, analytic variance, architecture
availability, and optimal endpoint. Cell summaries are per
master-seed/p/architecture/stratum (`all`, `accepted`, `rejected`) and include
all exploration, endpoint, tie, variance, payoff, regret, and Q summaries.

Paired architecture effects by p and stratum:

1. graded any-disclosure minus binary full-auth post-initial rate;
2. graded minus binary full-auth post-initial rate;
3. graded minus binary full-auth final-window rate;
4. graded minus binary optimal-endpoint modal probability;
5. binary minus graded normalized regret;
6. binary minus graded disclosure rejection rate per step;
7. graded minus binary stable-full-auth probability;
8. graded minus binary final-window mean disclosure.

Equal-weight p=.75/.85 seed effects; never pool children across p. Smoke
intervals are blank/not-estimable. Standard uses five-seed Student-t 95%
intervals with t=2.7764451051977987. Expected smoke rows: raw 576, cells 18,
arms 15, effects 192. Standard: raw 15,000, cells 90, effects 576.

Decision rules: nonzero-disclosure preservation requires effect 1 positive in
4/5 seeds separately at p=.75/.85 and pooled interval above zero. Endpoint
discovery requires both effects 3 and 4 under that rule. Regret benefit requires
effect 5. Effect 8 is never a decision input. If only exploration passes,
wording is limited to changing exploration exposure; negative endpoint effects
are action-space dilution. p=.65 is control only.

## Tests, sentinels, artifacts, and cost

Tests must cover analytic rows/event rewards; unforced replay of maintained M0
and M1; forced-step draw order; matched initial outcomes; selected-arm-only Q
updates; seed/order/global-RNG behavior; exact/noninteger windows; count/payoff/
regret reconciliation; ties/censoring; intermediate-only non-discovery;
raw-to-summary/effects at 1e-12; deterministic reordered reruns; strict config
mutations; E02-specific standard approval; frozen E01 non-regression; and full
`./scripts/verify.sh`.

Manually inspect accepted/rejected matched pairs at every p, an intermediate
event, a shared d=1 step, a d=0 event, selected-arm Q update, counts, regret,
strata, sort IDs/seeds, and warnings.

Required smoke artifacts use prefix `frontiers_m1_binary_graded_v1_smoke`:
manifest, raw units, arm/cell/effect summaries, disclosure diagnostic PNG, and
13-item report. Expected load is 172,800 learner-steps, 576 rows, under one MB
and roughly 0.5-1 second. Stop for review if over 10 seconds or 5 MB.
