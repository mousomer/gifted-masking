# Article V1 — Exact analytic results

Closed-form results only. No stochastic calculation is involved: every value below is
re-derived in closed form by `scripts/analytic.py` and asserted against its exact rational
form at build time. Authority for each row is the maintained analytic document and the
model module named in the final column.

| Model | Role | ID | Result | Closed form | Exact | Decimal |
|---|---|---|---|---|---|---|
| M0 | E01 objective baseline | M0.1 | Static objective reward gap | `Delta_0(p) = a + c - (1 - p)(b + r)` | `3p - 43/20` | 3p - 2.15 |
| M0 | E01 objective baseline | M0.2 | Static M0 objective boundary | `p*_obj = 1 - (a + c)/(b + r)` | `43/60` | 0.7166667 |
| M1 | E02 objective structure | M1.1 | Expected reward is affine in disclosure | `E[R(d)] = b - c + d[a + c - (1 - p)(b + r)]` | `3/4 + d(3p - 43/20)` | 0.75 + d(3p - 2.15) |
| M1 | E02 objective structure | M1.2 | Endpoint optimum | `argmax_d E[R(d)] in {d_min, d_max} unless Delta_0(p) = 0` | `endpoint` | n/a |
| M2 | E03 objective comparator | M2.5 | Neutral dynamic-gap decomposition | `D_N(V) = Delta_0(p) + gamma[p V_A + (1 - p) V_S - V_N]` | `n/a` | n/a |
| M2 | E03 objective comparator | M2.VI | Full-information dynamic optimum | `V(s) = max_a { r(s, a) + gamma * sum_s' P(s'|s, a) V(s') }` | `n/a` | max envelope error 8.99e-10 |
| M3 | E04 objective benchmark | M3.1 | Full-information optimum is K-invariant (one good context) | `max{R_M, R_G, R_B} independent of K` | `R_G = 23/20 at bf = 0` | 1.15 |
| M3 | E05 objective anchor | M3.2 | Objective comparison-cost crossover | `R_G(bf) - R_M = 0.40 - 0.85 bf; bf* = 0.40/0.85` | `8/17` | 0.4705882 |
| M3 | E05 competing arm | M3.3 | Good-versus-bad context crossover | `R_G(bf) = R_B` | `39/17` | 2.2941176 |

## Interpretation constraints

- **M0.1 — Static objective reward gap.** Authenticity minus masking in expected static reward, affine and strictly increasing in p with slope b + r. _Authority:_ ARTICLE_V1_ANALYTIC_RESULTS.md 3.1; src/gifted_masking/models/m0.py
- **M0.2 — Static M0 objective boundary.** The static objective acceptance crossover under the frozen M0/M1 reward parameters. This is the static M0 objective boundary and is not the M2 dynamic threshold. _Authority:_ ARTICLE_V1_ANALYTIC_RESULTS.md 3.2, Appendix A; src/gifted_masking/models/m0.py
- **M1.1 — Expected reward is affine in disclosure.** Expected reward is affine in the disclosure level d, so the derivative in d is constant and no interior level can strictly dominate both endpoints. _Authority:_ ARTICLE_V1_ANALYTIC_RESULTS.md 4; src/gifted_masking/models/m1.py
- **M1.2 — Endpoint optimum.** The strict static optimum lies at an endpoint except at exact indifference, for any number of disclosure levels. Intermediate disclosure is therefore never objectively superior in the static problem, and E02's graded effects are learning and action-representation effects. _Authority:_ ARTICLE_V1_ANALYTIC_RESULTS.md 4, 10.1; src/gifted_masking/models/m1.py
- **M2.5 — Neutral dynamic-gap decomposition.** The Neutral-state Q gap splits into the M0 static gap plus the discounted value of entering Accepted or Stigmatized rather than remaining Neutral, so dynamic M2 can reverse the static ordering in either direction. _Authority:_ ARTICLE_V1_ANALYTIC_RESULTS.md 5.7; src/gifted_masking/models/m2.py
- **M2.VI — Full-information dynamic optimum.** The E03 comparator is the exact full-information discounted optimum obtained by value iteration, independently reproduced by deterministic stationary-policy enumeration over all 357 frozen cells. It knows the complete payoff structure and is not information-matched to the learner. _Authority:_ ARTICLE_V1_ANALYTIC_RESULTS.md 5.10; src/gifted_masking/analysis/m2_optimal.py
- **M3.1 — Full-information optimum is K-invariant (one good context).** With one fixed good context, increasing K changes only the multiplicity of R_M and R_B, never the distinct reward set, so the value attainable by a fully informed agent does not change with K. Any decline in settling is a learner and representation effect, not a change in what is objectively achievable. _Authority:_ ARTICLE_V1_ANALYTIC_RESULTS.md 6.2, B9; src/gifted_masking/models/m3.py
- **M3.2 — Objective comparison-cost crossover.** The exact M3 good-context objective comparison-cost crossover under the frozen defaults R_M = 0.75 and R_G(bf) = 1.15 - 0.85 bf. It is an environmental boundary, not a learned threshold. _Authority:_ ARTICLE_V1_ANALYTIC_RESULTS.md 6, Appendix A, B10; src/gifted_masking/models/m3.py
- **M3.3 — Good-versus-bad context crossover.** Bad-context authenticity is not the competing optimum anywhere in the tested dense range: the good-versus-bad crossover lies far outside it. _Authority:_ ARTICLE_V1_ANALYTIC_RESULTS.md Appendix A, B11; src/gifted_masking/models/m3.py
