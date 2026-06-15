# Claim Audit

| Claim | Evidence | Status | Required wording |
| ----- | -------- | ------ | ---------------- |
| M0 hot-stove lock-in | M0 reward equations are implemented; higher receptivity reduces masking; higher loss aversion increases masking; deterministic tests pass | Supported for learned avoidance under tested settings | "M0 shows learned masking can persist when authentic attempts are risky and negative outcomes are weighted more strongly." |
| M1 graded disclosure is protective | Higher receptivity increases disclosure; endpoints and expected reward are tested | Partially supported | "Graded disclosure can support lower-risk exploration in this independent-action model." |
| M2 sticky stigma is structural lock-in | Transition mechanics are implemented; higher escape reduces masking; value-iteration benchmark now compares learned policies against the optimal MDP policy for current robustness cells | Partially supported | "Sticky stigma changes the dynamic MDP optimum relative to the static M0 comparator in some cells, and learned-policy regret can now be measured for current M2 robustness cells." |
| M3 context multiplicity is harmful | Flat and hierarchical K gaps are positive, but global-mask and fixed-known-good-pond controls are near zero | Overstated | "Context multiplicity increases masking when it creates an asymmetric search burden." |
| M3 search burden explains the K effect | Positive K gaps in flat/hierarchical formulations and near-zero gaps in controls that reduce/remove search burden | Supported | "The maintained ablations support search burden as the active mechanism behind the K effect." |
| BFLPE causes anticipatory retreat | High `bf` reduces good-pond authenticity; analytic crossover is implemented; no local sweep around `bf*` with uncertainty | Partially supported | "High BFLPE costs can reduce good-pond authenticity in the tested comparison; behavioral threshold claims need a sweep around the analytic crossover." |
| M4 shows true hysteresis | Ramp-up/down path gap exists; loop area, threshold separation, ramp speed sensitivity, and seed/grid replication are missing | Overstated | "The model shows path dependence under the tested ramp schedule; true hysteresis remains unestablished." |
| M4 shows path dependence | Ramp-up/down mask and receptivity path gaps have CIs excluding zero | Supported under tested schedule | "M4 shows path dependence under the tested `km` ramp schedule." |
| Risk-taking is strictly protective in dynamic worlds | No current full-suite risk-type artifact; older risk plots are not in maintained robustness report | Not supported | "Risk-type effects require maintained robustness tests before directional claims." |
| Risk-aversion is close to fatal in M4 | No maintained evidence for this phrase; M4 smoke tests only high entrenchment and ramp paths | Not supported | "Higher loss aversion can increase masking in M0; dynamic-world risk-type claims require further tests." |
| Consolidated outcome map identifies four mechanistically distinct routes into persistent masking | Maintained package has M0-M4 mechanisms, but publication-grade robustness and claim-level uncertainty are incomplete | Partially supported | "The model ladder distinguishes candidate mechanisms for persistent masking; publication-grade claims require stronger model-specific benchmarks." |
| No learner parameter substitutes for environmental fresh starts in M2 | Optimal-policy benchmark exists for selected M2 cells, but no maintained learner-parameter sweep against environmental reset/escape exists | Not supported | "Whether learner parameters substitute for environmental fresh starts in M2 requires sensitivity benchmarking over learner parameters and environmental reset/escape." |

## Strict Summary

The old paper language should be narrowed. The strongest maintained evidence is
for M3 search burden and M4 path dependence. M2 now has an optimal-policy
benchmark for selected cells, but broad M2 optimal-learner lock-in claims still
need parameter sensitivity. True M4 hysteresis and broad temperament/risk-type
claims remain weak.
