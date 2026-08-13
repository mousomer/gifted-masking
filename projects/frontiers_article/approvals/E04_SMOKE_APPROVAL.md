# E04 Scientific Approval Record

**Decision:** `APPROVED_FOR_SMOKE`  
**Date:** 2026-08-12  
**Scope:** bounded E04 implementation and smoke only

Freeze the four maintained architectures (`flat_2k`, `hierarchical`,
`global_mask`, `fixed_known_good`), K=1,2,4,8,16, fixed/random-per-child
identity, and one/two/proportional-25 good-context regimes at p_good=.85,
p_bad=.20,bf=0, default payoffs/learner. Do not modify M3 or robustness code.

Canonicalize the 120 requested design cells to exactly 55 executable cells:
18 per search architecture and one K-invariant fixed-known cell. Emit a 120-row
equivalence table; aliases never duplicate observations or inference. Good sets
are fixed {0..m-1} or uniformly sampled sorted per-child subsets, with
m=1,min(2,K),max(1,ceil(K/4)). Honor K=1 and other count equivalences exactly.

Smoke config `configs/frontiers_article/e04_m3_search_architectures_smoke.json`,
run ID `frontiers_m3_search_architectures_v1_smoke`, n=96,T=300,window=.2,
seed 2026081499, bootstrap 2026081497, workers1. Expected 5,280 primary rows
and 1,584,000 learner-steps. Stage but do not execute the standard config with
n500,T2000,five seeds 2026081401-05 and approval false.

Preserve exact architecture action/update/RNG semantics from the scientific
approval. New diagnostic kernel records per-child good sets, discovery,
authentic context allocation/entropy, strict and maintained modal outcomes,
objective rewards and three regret measures. Best comparator is architecture-
available static action; expected regret is primary and nonnegative. Default
regrets are 0 good-auth, .40 mask, 1.95 bad-auth; p_good=.70 is a mask-optimal
sentinel.

Policy families share policy/environment draws across identity/good-count only
within architecture/K/master/sensitivity. Separate identity RNG never shifts
the maintained stream. Child pairing is allowed only inside the recorded
matched family. Use the exact ordered primary schema, summaries, K slopes,
endpoint effects, architecture/identity/good-count contrasts, Student-t rules,
decision rules, tests, manual sentinels, artifacts, and cost/stop rules in the
scientific approval response. The report must project standard runtime <10m,
raw <~400MiB, peak RSS <2GiB before GO. Smoke adjudicates nothing and stops for
separate review.
