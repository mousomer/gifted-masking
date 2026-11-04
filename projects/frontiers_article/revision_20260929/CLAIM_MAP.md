# Supported-claims revision: claim, chapter, and evidence map

Date: 29 September 2026. This map implements the author's approved rewrite.
It changes editorial coverage, not the frozen experimental estimands.

Category 1 = expected demonstration; 2 = literature-anticipated direction;
3 = surprising combination, interaction, extent, or persistence. Category is
distinct from evidence strength. The 14/2/7 primary assignments are editorial,
not counts of independent discoveries. Category-2 interpretations also overlap
claims assigned primarily to categories 1 and 3.

## Complete claim routing

| ID | Category | Affirmative result | Main home | Supplement home | Evidence and source selector | Figure |
| --- | ---: | --- | --- | --- | --- | --- |
| C01 | 1 | Weighting changes masking by 40.30 percentage points with environmental payoffs fixed. | 2.2; 3.1; 4.2 | S2 | E01 cells/effects: maintained baseline, p=.65, lambda=.5 versus 2.5; E01-C3-LAMBDA | 2 |
| C02 | 1 | Subjective indifference moves from .6304 to .8333 while the objective threshold stays .7167. | 2.2; 3.1 | S2 | Exact transformed-reward threshold; analytic authority §§3.4–3.5 | 2 |
| C03 | 1 | Initial rejection reduces subsequent authentic sampling by 2.58 points. | 2.2; 3.1; 4.2 | S2 | E01-C2-SAMPLING; pooled p=.75/.85; steps 1–1999 | 2 |
| C04 | 1 | Corrective information reduces masking and objective loss. | 2.2; 3.1; 4.2 | S2 | E01-C2-FORCED-MASK/REGRET and CF-MASK/REGRET; rejected stratum | 2 |
| C05 | 1 | The specified counterfactual treatment produces the larger reduction. | 3.1; 4.2 | S2 | Descriptive .118135/.046590 ratio; different specified treatment intensities | 2 |
| C06 | 3 | Graded options increase any disclosure while reducing intensity and full-endpoint use. | 2.3; 3.2; 4.3 | S3 | E02-C4 contrasts; rejected stratum, p=.75/.85 | 3 |
| C07 | 1 | Intermediate actions preserve the affine objective optimum. | 2.3; 3.2 | S3 | Exact M1 expectation and endpoint maximum; analytic authority §§4.1–4.5 | 3 |
| C08 | 1 | Partial disclosure reduces rejection exposure and variance in the favourable E02 cells. | 2.3; 3.2 | S3 | Exact variance at p=.75/.85; no attribution to an estimated variance preference | 3 |
| C09 | 3 | Persistent states move the objective threshold from .717 to .384–.269. | 2.4; 3.3; 4.4 | S4 | E03 thresholds: objective bisection brackets at eta=0,.2,.8 | 4 |
| C10 | 1 | Recovery changes objective incentives: eta=0 to .8 lowers the threshold about .115. | 3.3; 4.4 | S4 | Difference between the C09 deterministic threshold brackets | 4 |
| C11 | 1 | Accepted-state authenticity strictly dominates by a+c=.85. | 2.4; 3.3 | S4 | Identical continuation transitions; analytic authority §§5.3,5.8–5.9 | Text / S4; 1 provides mechanism context |
| C12 | 1 | Future social consequences reverse immediate payoff rankings in either direction. | 2.4; 3.3; 4.4 | S4 | E03 default p=.4 eta=0 and harsh p=.75,b2=0,r2=8,delta=.3,eta=0,gamma=.9 | Text / S4; 4 shows related thresholds |
| C13 | 1 | Aggregate Neutral masking is dynamically suboptimal in the same 243/357 tested cells across masters. | 2.4; 3.3 | S4 | E03 baseline grid and stable-cell tables; adequacy and oracle requirements | Text / S4; 4 shows selected sentinels |
| C14 | 3 | The five-sentinel masking gap survives 5,000 steps and the named separate perturbations. | 2.4; 3.3; 4.4 | S4; S8 | E03 cells, component=sentinels; the five specified (p,eta) cells | 4 |
| C15 | 3 | Representation changes use of an unchanged best opportunity. | 2.5; 3.4; 4.5 | S5 | E04 fixed-one K16–K1 modal contrasts, flat/hierarchical/global-mask/known-good | 5 |
| C16 | 3 | Context expansion raises actual masking to 84–87% in two architectures. | 2.5; 3.4; 4.5 | S5; S8 | E04 curves and effects: actual-mask K16–K1, fixed-one; global-mask contrast | 5 |
| C17 | 3 | Nearly universal accepted-good encounters coexist with extensive later masking. | 2.5; 3.4; 4.5 | S5; S8 | E04 fixed-one K16 ever-accepted-good and final-mask means; first-success timing | 5 |
| C18 | 1 | Search incurs payoff costs even when final modal success is preserved. | 2.5; 3.4; 4.5 | S5; S8 | E04 regret-per-step and capped first-success K16–K1; global-mask modal levels | 5 |
| C19 | 2 | More widespread receptivity restores good-authentic modal selection. | 3.4; 4.5 | S5 | E04 K16 fixed-one versus proportional-25%; endpoint means and slope-difference contrasts | 5 |
| C20 | 2 | Comparison cost changes the global objective optimum at 8/17. | 2.6; 3.5 | S6 | Exact expected rewards: good 1.15−.85bf, mask .75, bad −.8 | 6 |
| C21 | 3 | The modal-population boundary .312852 lies below objective indifference .470588 at lambda=1. | 2.6; 3.5; 4.6 | S6 | E05 archived transition estimate/whole-master bootstrap CI and analytic reward advantage | 6 |
| C22 | 1 | Actual masking rises while authenticity retains objective advantage. | 2.6; 3.5; 4.6 | S6; S8 | E05 flat K4 cells at bf=0,.30,.325,8/17; equal master means | 6 |
| C23 | 1 | Distinct mechanisms change behaviour, opportunity value, and their alignment. | 1.2; 3.6; 4.1; 6 | S1–S8 | Synthesis C01–C22; no joint fitted human causal decomposition | 1 |

## Source resolution

All experiment tables above are the existing protected CSVs under
`results/summaries/`. Family names are:

- E01: `frontiers_hot_stove_v1`.
- E02: `frontiers_m1_binary_graded_v1`.
- E03: `frontiers_m2_regime_replication_v1`.
- E04: `frontiers_m3_search_architectures_v1`.
- E05: `frontiers_m3_bflpe_crossover_v1`.

The complete source selectors, exact intervals, and derivations for C01–C23
are retained in `../ARTICLE_V2_SUPPORTED_CLAIMS_REVIEW.md`. Matrix identifiers
resolve through `../ARTICLE_V1_EVIDENCE_MATRIX.csv`; analytic sections resolve
through `../ARTICLE_V1_ANALYTIC_RESULTS.md`. Figure provenance records exact
paths, hashes, selectors, and plotted values. No historical evidence matrix is
rewritten to relabel a secondary outcome as primary.

## Chapter implementation contract

| Chapter | Change implemented in this revision |
| --- | --- |
| Title and Abstract | Affirmative title; non-obvious results lead; compact computational scope. |
| 1. Introduction | Literature expectations motivate the application; weighting, dynamic incentives, and encounter/use separation motivate the questions. |
| 2. Methods | Restored outcome definitions, reference versus sensitivity conditions, exact mathematics, dynamic comparator, and evidence classes. |
| 3. Results | C01–C23 routed above, including previously omitted scientific outcomes. |
| 4. Discussion | Mechanistic interpretation and empirically discriminating predictions; completed robustness is stated affirmatively. |
| 5. Limitations | Consolidated restrictions on extrapolation and provenance; architecture dependence is also a result. |
| 6. Conclusion | Positive findings and distinct measurable mechanisms, not only inferential ambiguity. |
| Educational implications | Separate expectation/weighting, information, recovery, graduated learning, and sustained use. |
| Figures and supplement | Six figure subjects and S1–S10 aligned to the fuller results. |

## Meaning-preservation checks

- C01 p=.65 is an objectively mask-favouring environment, not an example of
  objectively suboptimal masking caused by high lambda.
- C03 measures subsequent sampling; its final-window null is reported once.
- C05 is a descriptive comparison of specified interventions, not matched-dose
  treatment efficiency. C06 regret is an algebraic intensity translation.
- C08's monotone variance statement uses p=.75/.85, not all possible p.
- C13 counts parameter cells; C14 describes five sentinels, not a long-horizon
  rerun of the complete grid. Perturbations are separate, not factorial.
- C17 measures at least one accepted-good encounter, not perfect knowledge.
- C19 endpoint differences are separate from per-log2(K) slope differences.
- C20 uses expected reward, not reward conditional on acceptance.
- C21 is a modal-classification crossing, not 50% total masking; C22 makes
  the outcome distinction visible.
