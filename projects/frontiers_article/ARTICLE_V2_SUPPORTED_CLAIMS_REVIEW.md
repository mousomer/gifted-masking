# Supported scientific claims: updated review

**Date:** 29 September 2026

**Request:** Reassess what the existing science supports, including findings omitted or understated in the current manuscript.

**Status:** Review and proposed claim list. This document does not replace the scientific freeze or revise the manuscript.

## Review judgment

The existing evidence supports a substantially fuller scientific account. The largest omissions are learner-side weighting, the magnitude of the dynamic objective-boundary shifts, robustness through 5,000 steps, actual masking rates, the cost of searching, and the difference between encountering a receptive opportunity and continuing to use it. These are substantive results already present in the equations and archived experiments.

The appropriate scope statement is: **the following findings concern the specified computational models and tested experimental designs; their numerical effect sizes are model results.** Within that scope, “shows,” “increased,” “reduced,” “is optimal,” and “strictly dominates” are appropriate when supported below. Repeating a human-calibration disclaimer after each result adds no information.

Scientific support, originality, and editorial selection are different decisions. An established mechanism can be demonstrated convincingly in this study and help explain its results. An exact theorem can be stated directly even when it is elementary. A supporting outcome remains scientifically informative when it is not the prespecified primary endpoint.

## Review contract and verification

Acceptance criteria for this review were: trace each proposed claim to an equation or existing result; preserve the measured outcome and conditioning; distinguish exact mathematics, deterministic numerical benchmarks, replicated simulation findings, and archived secondary outcomes; and supply affirmative wording suitable for revision.

The comparison used the current V2 manuscript and supplement, V2 reframe map, V1 claim ledger, evidence matrix, analytic results, evidence freeze, leverage authority, interpretation notes, experiment specifications, configurations, and frozen result tables. The V2 map already permits the weighting result and records the dynamic thresholds. The V1 leverage authority explicitly permits quantified model manipulations. Their omission is therefore largely an editorial selection problem.

Read-only checks on this review date passed:

- All **33/33 protected E01–E05 outputs** match their experiment manifests.
- All **18/18 content-addressed evidence-matrix references** match.
- The existing deterministic analytic-table assertions pass for all nine rows.
- Additional values below were read from existing summaries or calculated by elementary algebra/equal-weight aggregation of existing master-cell means.

E01, E02, E04, and E05 standard cells use 500 learners, 2,000 steps, a 400-step final window, and five independent master seeds. E03's baseline uses 160 learners, 1,000 steps, a 200-step final window, and five masters. Scalar confidence intervals are the archived Student-t 95% intervals across five master estimates; E05's crossing interval resamples complete master curves. Secondary-outcome intervals are pointwise, not simultaneous. The E01–E03 historical generator-source limitation remains a package-level provenance disclosure.

No simulation was rerun. The repository-wide `scripts/verify.sh` was not invoked because it runs simulations and writes result artifacts; the read-only evidence validators and analytic assertions were the appropriate checks for this review. No manuscript, model, configuration, result, or existing authority file was edited.

## Evidence labels

| Label | Meaning |
|---|---|
| **Exact** | Follows algebraically from the specified model. |
| **Deterministic** | Computed full-information benchmark with stated numerical precision. |
| **Replicated** | Existing primary/adjudicated simulation contrast across five master seeds. |
| **Secondary** | Existing archived sensitivity or additional outcome, identified as such rather than promoted retroactively to a primary endpoint. |
| **Synthesis** | A conclusion supported jointly by the listed mathematical and experimental results. |

## Updated claim list

### C01. Learner weighting alone produces large differences in concealment

**Proposed wording:** “With the environment held fixed at receptivity .65, increasing the weight on negative outcomes from .5 to 2.5 increased final-window masking from 58.89% to 99.19%, a 40.30-percentage-point increase (95% CI 39.54–41.06).”

**Evidence:** Replicated; exact contrast +.402990 [.395366, .410614]. The two levels are equal-weight means of the five archived master-cell means. At this setting masking has higher objective expected reward; the claim establishes a large learner-side source of behavioural variation.

**Current treatment:** Omitted from main Results and demoted in the supplement. Restore as a central identification result.

**Sources:** `ARTICLE_V1_EVIDENCE_MATRIX.csv`, E01-C3-LAMBDA; `results/summaries/frontiers_hot_stove_v1_cells.csv`; `ARTICLE_V1_LEVERAGE_DISCUSSION_AUTHORITY.md` §7; current supplement §E01 weighting sensitivity.

### C02. Negative-outcome weighting systematically moves subjective indifference

**Proposed wording:** “Negative-outcome weighting changes the learner's expected-transformed-reward threshold independently of environmental indifference. With the reference payoffs, the subjective threshold rises from .6304 at lambda=.5 to .8333 at lambda=2.5, while the objective threshold remains .7167.”

**Evidence:** Exact, when masking and accepted rewards are nonnegative, rejection is negative, and a+c>0:

\[
p^*_{\lambda}=\frac{b-c+\lambda(r-a)}{b+a+\lambda(r-a)}
=\frac{.75+1.4\lambda}{1.6+1.4\lambda},\qquad
\frac{d p^*_{\lambda}}{d\lambda}=\frac{(r-a)(a+c)}{[b+a+\lambda(r-a)]^2}>0.
\]

At lambda=2, the interval .7167 < p < .8068 favours authenticity in objective expected reward and masking in expected transformed reward. This is an exact valuation distinction; its target is the transformed-reward comparison.

**Current treatment:** The transform is defined, but its systematic threshold consequence is absent. Restore beside C01.

**Source:** `ARTICLE_V1_ANALYTIC_RESULTS.md` §§3.4–3.5.

### C03. Learning history changes subsequent sampling and its objective cost

**Proposed wording:** “An initially rejected authentic outcome reduced subsequent authentic sampling by 2.58 percentage points (95% CI 1.59–3.58) with the later environment unchanged.”

**Evidence:** Replicated, pooled controlled p=.75/.85 comparison, steps 1–1999. The corresponding increase in normalized objective pseudo-regret is .025824 [.015914, .035735]. The identity linking regret to action counts makes this a meaningful cost representation of the same behaviour.

**Current treatment:** Present; retain affirmative sampling wording. The time window defines the claim without requiring a repeated discussion of permanent masking.

**Sources:** evidence matrix E01-C2-SAMPLING/REGRET; analytic results §3.6.

### C04. Supplying information changes behaviour with the environmental payoff structure fixed

**Proposed wording:** “After initial rejection, 5% forced authentic exposure reduced final masking by 4.66 percentage points (95% CI 3.32–6.00); counterfactual authentic feedback reduced it by 11.81 points (10.97–12.66), with environmental payoffs unchanged.”

**Evidence:** Replicated model interventions. Normalized objective pseudo-regret fell by .057954 [.045614, .070293] and .141318 [.132369, .150267], respectively. The counterfactual manipulation updates information about authenticity without crediting an unchosen action's reward to actual return.

**Current treatment:** Mask effects present; objective costs and explanatory significance understated. This directly establishes the model's information channel as a point of leverage.

**Sources:** evidence matrix E01-C2-FORCED-MASK/REGRET and E01-C2-CF-MASK/REGRET; `ARTICLE_V2_LID_SUPPLEMENTARY_METHODS.md`, E01 intervention definitions.

### C05. The tested counterfactual intervention produced a larger reduction

**Proposed wording:** “On the same final-masking outcome and rejected stratum, the tested counterfactual-feedback intervention produced approximately 2.54 times the reduction obtained with 5% forced exposure, with disjoint confidence intervals.”

**Evidence:** Replicated contrasts plus the descriptive ratio .118135/.046590. This compares the two specified interventions at their tested intensity. No confidence interval for the ratio was estimated.

**Current treatment:** The estimates are listed but their supported ordering is not stated.

**Source:** `ARTICLE_V1_LEVERAGE_DISCUSSION_AUTHORITY.md` §2.1; C04's archived contrasts.

### C06. Graded options separate engagement, intensity, and endpoint selection

**Proposed wording:** “Independently learned graded options sustained more frequent nonzero disclosure while reducing full-authentic endpoint use and average disclosure intensity.”

**Evidence:** Replicated E02, rejected initial-outcome stratum, p=.75/.85:

| Graded minus binary outcome | Estimate | 95% CI |
|---|---:|---:|
| Post-initial nonzero disclosure | +25.50 percentage points | +25.30 to +25.71 |
| Full-authentic final-window selection | −32.87 percentage points | −34.20 to −31.53 |
| Unique full-authentic modal classification | −22.17 percentage points | −28.88 to −15.47 |
| Normalized objective regret | +.029761 | +.025648 to +.033874 |

The final row also means lower mean disclosure intensity by .029761 over the regret-measurement horizon, because normalized regret equals mean endpoint distance, 1−mean(d), in these authenticity-optimal cells.

**Current treatment:** The first three outcomes are present; the objective-loss result and separation of the three behavioural dimensions deserve explicit treatment.

**Sources:** evidence matrix E02-C4 rows; analytic results §4.5.

### C07. Graded choice changes learning while preserving the objective optimum

**Proposed wording:** “Adding intermediate disclosure levels leaves the best achievable expected reward and the objective boundary unchanged; it changes the learning problem.”

**Evidence:** Exact. E[R(d)]=.75+d(3p−2.15). Every grid containing 0 and 1 has the same maximum expected reward; full authenticity is optimal above p=43/60, masking below, and all levels tie at equality.

**Current treatment:** Present mathematically. Promote its explanatory role: C06 occurs with the optimum held fixed.

**Source:** analytic results §§4.1–4.4.

### C08. Partial disclosure offers a lower-variance, lower-exposure option

**Proposed wording:** “In the authenticity-optimal E02 comparisons at p=.75/.85, partial disclosure reduces rejection probability and reward variance while also reducing expected reward relative to full authenticity.”

**Evidence:** Exact consequence of the existing equations, made explicit in this review. Rejection probability is (1−p)d; reward variance is (b+r)^2(1−p)d[1−(1−p)d]. For p=.75/.85, variance increases with d on [0,1]. At p=.75, d=.5 gives variance .984375 versus 1.6875 at d=1, and expected reward .80 versus .85.

**Current treatment:** Lower exposure is mentioned, but the mean–variance geometry is missing. Suitable as an analytic explanation of the available options; attribution of learner behaviour to a measured variance preference is a separate question.

**Sources:** analytic results §4.1; `src/gifted_masking/models/m1.py`, acceptance/reward definitions.

### C09. Persistent social consequences substantially relocate the objective boundary

**Proposed wording:** “With persistent social states, the Neutral-state receptivity threshold for optimal authenticity is approximately .384, .339, or .269 at escape rates 0, .2, or .8, compared with the static threshold .717.”

**Evidence:** Deterministic MDP benchmark:

| Escape probability eta | Dynamic threshold bracket | Approximate reduction from 43/60 |
|---:|---:|---:|
| 0 | [.3839111, .3839722] | .33273 |
| .2 | [.3387451, .3388062] | .37789 |
| .8 | [.2689819, .2690430] | .44765 |

The brackets have width approximately .000061. Independent four-policy evaluation verified the objective envelope across all 357 baseline grid cells to maximum discrepancy 8.99e−10 from value iteration.

**Current treatment:** The manuscript describes a change of benchmark but omits this large quantitative relocation. This should lead E03 Results.

**Sources:** `publication_v1/data/e03_objective_thresholds.csv`; frozen E03 thresholds table; analytic results §5.10; consistency audit's independent M2 check.

### C10. Recoverability changes incentives, not just learned beliefs

**Proposed wording:** “Increasing escape from adverse social standing from 0 to .8 lowers the objective authenticity threshold by approximately .115 in the reference model.”

**Evidence:** Deterministic difference between C09's threshold brackets. The manipulated transition changes the optimal decision itself. The claim is about the selected escape settings and reference parameters.

**Current treatment:** Quantitative result omitted. It is a concrete environmental leverage result.

**Source:** C09's threshold table.

### C11. Established acceptance gives authenticity a strict dynamic advantage

**Proposed wording:** “In the Accepted state, authenticity strictly dominates masking by a+c=.85, regardless of the continuation values.”

**Evidence:** Exact. Both actions have the same Accepted-state transition probabilities, so their continuation terms cancel. The positive immediate gap is also the dynamic Q gap for any continuation values. More generally, the result holds when a+c>0.

In the Stigmatized state, the default immediate authenticity reward is −1.9+1.75p, always below the masking reward .25. Therefore any dynamic optimum favouring authenticity there is supplied by its future redemption value. This exact decomposition identifies what the state transition contributes.

**Current treatment:** The transitions are described, but both strong mathematical implications are missing from the argument.

**Sources:** analytic results §§5.3 and 5.8–5.9 (Accepted dominance and Stigmatized redemption decomposition).

### C12. Future social consequences can reverse the immediate payoff ranking in either direction

**Proposed wording:** “The model demonstrates both costly authenticity that is dynamically optimal and immediately advantageous authenticity that is dynamically inferior to masking.”

**Evidence:** Deterministic, two explicit examples:

- Default p=.4, eta=0: authenticity's immediate expected reward is −.20 versus .75 for masking, yet its optimal dynamic Neutral-state Q advantage is +.042943.
- Harsh sentinel p=.75, b2=0, r2=8, delta=.3, eta=0, gamma=.9: authenticity's immediate advantage is +.10, yet its dynamic Neutral-state Q advantage is −.406293. Masking is the dynamic optimum.

**Current treatment:** Both directions are discussed abstractly. Restore the computed examples as substantive results about adaptation.

**Sources:** `results/summaries/frontiers_m2_regime_replication_v1_cells.csv`, baseline/sensitivity p=.4 eta=0 and harsh sentinel; evidence freeze E03-C5-HARSH.

### C13. Finite learning sustains objectively suboptimal action allocation

**Proposed wording:** “Across the same 243 of 357 tested parameter cells in every master-seed replication, final-window Neutral-state actions favoured masking although the full-information dynamic optimum favoured authenticity.”

**Evidence:** Replicated baseline grid; all 243 disagreement cells have five adequately visited, agreeing masters. The benchmark and behavioural aggregation are explicit. This is objectively suboptimal action allocation relative to the stated dynamic objective.

**Current treatment:** Present but often reduced to “disagreement.” The stronger scoped statement is supported. The grid count is useful supplementary coverage; C09 is the stronger E03 headline.

**Sources:** E03 stable-cell and cell tables; evidence freeze E03-C5-GRID.

### C14. The masking–optimality gap survives substantial executed sensitivity checks

**Proposed wording:** “At all five prespecified disagreement sentinels, masking remained the aggregate Neutral-state preference in all five masters through 5,000 steps, after doubling the population, and under the tested alternatives for final-window length, negative-outcome weighting, and initialization.”

**Evidence:** Secondary, existing prespecified sensitivity runs. The five sentinels are (p,eta)=(.4,0), (.55,0), (.75,0), (.55,.2), (.9,.2). Each retained the classification at each separately tested perturbation: T=2000, T=5000, n=320, final-window fractions .1 and .4, lambda=.5 and 2.5, and q0=.75.

At T=5000, the means of the five master-level Neutral masking fractions were respectively **99.67%, 98.22%, 95.42%, 97.12%, and 89.97%**. These descriptive means concern the observed Neutral actions; each sentinel's dynamic optimum favours authenticity.

**Current treatment:** Main text omits this. The supplement's generic “classifier dependence” description misses the extensive retained stability. Report the actual successful checks alongside any settings that change classification.

**Source:** E03 cells table, `component=sentinels`, the named sensitivity rows and five listed sentinel cells.

### C15. Context representation determines how usable an unchanged opportunity becomes

**Proposed wording:** “Embedding one receptive context among more alternatives reduced good-context authentic modal selection by 23.40 percentage points in the flat architecture and 47.04 points in the hierarchical architecture, while the best attainable expected reward remained unchanged.”

**Evidence:** Replicated K=16 minus K=1 contrasts; CIs [−24.64, −22.16] and [−51.10, −42.98] percentage points. At the E04 payoffs, the objective rewards remain good authenticity=1.15, masking=.75, bad authenticity=−.8. Randomizing the receptive context's identity retained the declines. The global-mask contrast is +.0088 [.002090, .015510]; known-good is structurally zero.

**Current treatment:** Present, but the controls can be presented as positive evidence that representation matters. “Most frequent individual action” is the meaning of the modal classifier.

**Sources:** evidence freeze E04 rows; E04 effects table; analytic results §6.2.

### C16. The context expansion causes large increases in actual masking in the tested search architectures

**Proposed wording:** “Increasing the context set from one to sixteen while keeping one receptive context increased final-window masking from 26.36% to 84.19% in the flat architecture and from 26.45% to 87.27% in the hierarchical architecture.”

**Evidence:** Secondary, archived masking outcome. The increases are **57.83 points [57.43, 58.22]** and **60.82 points [60.21, 61.42]**, respectively. In the global-mask representation masking instead changed by −1.46 points [−2.29, −.62]. These are effects of the specified context expansion under each representation.

**Current treatment:** Omitted. This directly reports the behaviour the paper seeks to explain and complements the single-action modal endpoint.

**Sources:** `results/summaries/frontiers_m3_search_architectures_v1_effects.csv`, rows 733, 763, 793; corresponding E04 curves. Selector: across_master_seeds, fixed-one, K16−K1, named architecture.

### C17. Encountering receptivity and sustaining its use are distinct achievements

**Proposed wording:** “At sixteen contexts, 99.72% of flat learners and 99.64% of hierarchical learners had experienced accepted authenticity in the good context, yet final-window masking averaged 84.19% and 87.27%, respectively.”

**Evidence:** Secondary descriptive synthesis of existing master-cell means. Almost universal successful encounter coexists with extensive later masking. This identifies a richer phenomenon than complete failure to encounter the opportunity.

Mean capped time to the first accepted good-context authentic action also rose by **72.11 steps [64.96, 79.27]** flat and **71.15 [66.65, 75.66]** hierarchical. The metric uses the zero-based first-success step, with non-events coded at the horizon of 2000.

**Current treatment:** “Discoverability” currently carries too much explanatory weight. Distinguish availability, time to successful encounter, continued allocation of behaviour, and final modal classification.

**Sources:** E04 curves; effects rows 253 and 283; frozen E04 generator, first-success metric definition.

### C18. Search has objective performance costs even when the final modal endpoint is preserved

**Proposed wording:** “Context expansion increased objective payoff loss across the flat, hierarchical, and global-mask architectures; the global-mask representation preserved high final modal selection of good authenticity while still incurring search costs.”

**Evidence:** Secondary. K16−K1 expected static regret per step increased by:

| Architecture | Increase | 95% CI |
|---|---:|---:|
| Flat | .287739 | [.286203, .289275] |
| Hierarchical | .280625 | [.279390, .281859] |
| Global mask | .121423 | [.119686, .123159] |

Regret averages exact objective action gaps over all 2,000 steps. Global-mask final good-authentic modal classification was 98.16% at K=1 and 99.04% at K=16, while its capped first-success time increased by 16.16 steps [14.49, 17.83]. Thus final modal success and payoff cost accumulated during learning are separate scientific outcomes.

**Current treatment:** Omitted. This strengthens the context-search result beyond a single classifier.

**Sources:** E04 effects rows 613, 643, 673 and 313; E04 curves; `STAGE2_EXPERIMENT_SPECIFICATIONS.md` E04 secondary outcomes.

### C19. More widespread receptivity substantially restores authentic modal selection

**Proposed wording:** “At sixteen contexts, increasing receptive contexts from one to four raised good-authentic modal selection from 75.48% to 99.36% in the flat architecture and from 52.00% to 95.80% in the hierarchical architecture.”

**Evidence:** Descriptive endpoint means accompanying the adjudicated abundance controls. Relative to the one-good regime, the proportional-abundance change in slope per log2(K) is +.060440 [.055044, .065836] flat and +.112240 [.104787, .119693] hierarchical. These are slope differences, not percentage-point endpoint effects.

**Current treatment:** Four slope changes are given but their substantial practical meaning within the model is obscured. Report the endpoint levels and retain the prespecified slope contrasts as inference.

**Sources:** `publication_v1/data/e04_k_response.csv`; E04 curves/effects; evidence matrix E04-C6-MULTIPLE.

### C20. Comparison cost changes the global full-information optimum

**Proposed wording:** “Under the reference payoffs and one-good-context design, good-context authenticity is the unique optimal action below comparison cost 8/17; masking is optimal above that threshold.”

**Evidence:** Exact. Expected good-context authentic reward is 1.15−.85bf, masking is .75, and bad-context authenticity is −.8. Thus the 8/17=.470588 equality is the global objective switch, not merely a pairwise comparison that overlooks another better action. At equality the good-authentic and mask actions tie.

**Current treatment:** The main text incorrectly calls 1.15−.85bf the accepted-authentic reward. It is the expected good-context authentic reward; the accepted realized reward is 1.6−bf. Use the exact expected-reward statement above.

**Source:** analytic results §§6.3–6.6.

### C21. Learned population response changes well below objective indifference

**Proposed wording:** “The flat K=4 population's good-authentic modal-classification curve crossed .5 at comparison cost .312852 (95% bootstrap CI .307836–.316918), substantially below objective indifference at .470588.”

**Evidence:** Replicated; five master curves, all 10,000 whole-curve bootstrap samples yielding valid in-range crossings. At the estimated crossing, authenticity retains an expected-reward advantage of .134076, about one-third of its initial .40 advantage. Transforming the crossing interval gives advantage bounds [.130620, .138340]. The primary learner uses lambda=1, so enhanced negative-outcome weighting is unnecessary for this demonstrated separation.

**Current treatment:** Present; retain the result confidently with the correct outcome name. The .5 crossing concerns the fraction of learners whose most frequent individual action is good-context authenticity.

**Sources:** E05 transitions table; E05 standard configuration; evidence freeze E05-C7-CROSSING/GAP; analytic payoff equation.

### C22. Actual masking rises while authenticity remains objectively superior

**Proposed wording:** “As comparison cost rose from 0 to .325, final-window masking increased from 58.82% to 78.95% even though good-context authenticity retained an objective advantage of .12375 at the higher cost.”

**Evidence:** Secondary descriptive means of five archived flat E05 master cells. At bf=0, .30, .325, and 8/17, masking is .588217, .776073, .789508, and .852005, respectively. Corresponding good-authentic modal-classification fractions are .9400, .5292, .4724, and .1416.

These paired outcomes demonstrate that a most-frequent-single-action classifier and the total masking rate measure different things when masking has multiple context-specific arms. The .312852 modal crossing is not a 50% masking-rate threshold.

**Current treatment:** Actual rates are omitted. Reporting them adds direct behavioural evidence and prevents the boundary statistic from carrying an unintended interpretation.

**Source:** `results/summaries/frontiers_m3_bflpe_crossover_v1_cells.csv`, flat_2k rows at the listed costs, equal-weight means across five masters.

### C23. The combined evidence identifies several distinct sources of the same observed behaviour

**Proposed wording:** “Environmental payoffs, feedback history, outcome weighting, information access, action representation, persistent social state, and context structure provide distinct experimentally manipulated sources of variation in observed concealment. The experiments show how behaviour can change with opportunity held fixed, and how social dynamics can change the opportunity itself.”

**Evidence:** Synthesis of C01–C22. E01 manipulates history/information/weighting; E02 preserves objective endpoints while changing available actions; E03 changes the dynamic optimum; E04 preserves the best opportunity while changing representation and context composition; E05 measures the separation between objective and learned population boundaries.

**Current treatment:** The identification theme is present, but its positive mechanism and leverage content is underdeveloped. This synthesis can carry the main argument with the restored quantitative results beneath it.

**Sources:** The equation and artifact sources attached to C01–C22; `ARTICLE_V1_EVIDENCE_MATRIX.csv` across E01–E05.

## Model-derived predictions worth stating affirmatively

The results identify concrete empirical tests. These predictions extend the model findings to measurements that could establish whether the same processes operate in learners.

| Candidate mechanism/target | Prediction motivated by the results | Measurement that tests it |
|---|---|---|
| Corrective information | Making responses to unchosen authentic actions observable should change expectations and subsequent sampling, even with actual payoffs held constant. | Expected responses before/after information, authenticity sampling, and actual social responses. |
| Recoverability of adverse standing | Where adverse standing is easier to leave, the expected long-run return to authenticity should improve. | Duration of adverse consequences, routes out of them, and subsequent opportunities. |
| Graded action representation | Effects of graded options should depend on whether experience at one level updates expectations about other levels. | Any-disclosure frequency, disclosure intensity, endpoint use, and cross-level expectation transfer. |
| Receptive-context abundance | A larger receptive share should support repeated authentic use more than adding predominantly unreceptive alternatives. | Number and proportion of receptive settings, first successful encounter, and sustained action allocation. |
| Learner weighting | Similar social contingencies can yield different behaviour when negative outcomes receive different learned weights. | Separately measured reward expectations/weighting and observed acceptance/rejection contingencies. |

These targets can be discussed together. Their effect sizes use different outcomes and scales, so the table is a map of distinct targets rather than a cross-experiment ranking.

## Additional exact science in the wider M4 model ladder

M4 remains outside the current E01–E05 article's confirmatory scope. That editorial choice does not erase its mathematical results. The following can be stated as explicit mathematical properties in a wider-model discussion or separate paper:

For current receptivity within [p_min,p_max] and update rates ka, kr, km in [0,1], every update stays within those bounds and clipping is inactive. The following recurrence and drift formulas use these conditions.

1. **Repeated masking changes future receptivity geometrically under the specified feedback rule:** p_t−p_min=(1−km)^t(p_0−p_min). For 0<km<1 this is monotone decay toward p_min, with half-life log(.5)/log(1−km).
2. **The expected environmental change separates action exposure from response dynamics:** conditional authentic drift is F_A(p)=p·ka(p_max−p)−(1−p)·kr(p−p_min), and coupled drift is pi_A F_A(p)−(1−pi_A)km(p−p_min).
3. **Acceptance/rejection asymmetry determines the pure-authentic mean-drift balance:** at ka=.12, kr=.04, p_min=.05, p_max=.95, its interior zero is approximately .92697; at equal positive rates, the zero is p_min/(1+p_min−p_max)=.5. These are mean-drift results with that interpretation stated directly.

Sources: `ARTICLE_V1_ANALYTIC_RESULTS.md` §§7.1–7.5 and `src/gifted_masking/models/m4.py` update rule. No E06 simulation estimate is used here.

## Recommended scientific emphasis for the next revision

Lead with the exact dynamic-boundary changes (C09–C12), the 40.3-point weighting result (C01–C02), and the information interventions (C04–C05). Restore the executed E03 robustness evidence (C14). Expand E04 to report actual masking, first encounter, and objective costs alongside modal classification (C16–C19). Keep E05's precise population crossing and show the actual rates that explain what that crossing measures (C20–C22). Retain graded disclosure as a clear engagement–intensity–endpoint result (C06–C08).

A concise scientific synopsis supported by this review is:

> In the models, concealment is shaped by both the value of opportunities and how learners experience and represent them. Negative-outcome weighting produces large behavioural changes with environmental payoffs fixed. Corrective information reduces masking and objective loss. Persistent social states can reverse immediate payoff rankings, and recoverability shifts the dynamic boundary itself. Finite learners sustain objectively inferior action allocation across replicated conditions and extended horizons. Context representation and receptive-context abundance determine whether an available and even previously experienced opportunity is used consistently. The learned population response can change at comparison costs well below environmental indifference. These results identify distinct, measurable mechanisms and corresponding points of leverage.

## Source locator convention

Paths beginning `results/`, `src/`, or `configs/` are relative to repository root `/Users/omer/workspace/personal/repos/gifted-masking`. All other source paths above are relative to `/Users/omer/workspace/personal/repos/gifted-masking/projects/frontiers_article`. Claim IDs and row selectors specify the scientific records; line numbers supplied for CSV effects identify their current single-line records.
