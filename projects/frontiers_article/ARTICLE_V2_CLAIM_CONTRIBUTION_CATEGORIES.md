# Scientific contribution categories

**Date:** 29 September 2026

**Purpose:** Categorize the 23 claims in `ARTICLE_V2_SUPPORTED_CLAIMS_REVIEW.md` using the author's requested distinction between intuitive demonstrations, expectations from gifted-children research, and surprising results.

## Classification rule

This is a judgment about explanatory interest and contribution, separate from the strength of evidence. “Post-hoc trivial” means understandable from familiar principles once the setup is considered; it does not mean the analysis was unplanned. “Surprising” means the result challenges a plausible expectation for a reader of this applied paper. It is not an assertion of first discovery in all of reinforcement learning or psychology.

Each claim has one primary category below. Some contain both an expected principle and an interesting quantitative consequence; the distinction is made explicit rather than using a large effect size alone to claim novelty.

## 1. Post-hoc trivial / expected once the mechanism is considered

These results establish that the model behaves coherently and demonstrate useful mechanisms. Present them clearly and compactly.

| Claim IDs | Result | Why its direction is expected | Scientific use |
|---|---|---|---|
| C01–C02 | Greater negative-outcome weighting raises masking and the subjective receptivity threshold. | The learner explicitly multiplies negative outcomes by lambda. At the example's p=.65, changing lambda crosses the analytic subjective boundary. | A strong quantitative illustration of the identification problem; the 40.3-point shift is important without requiring a new mechanism. |
| C03 | Initial rejection reduces subsequent authentic sampling. | Standard hot-stove learning: a bad sample lowers value, reduces sampling, and restricts corrective evidence. | A baseline demonstration connecting the framework to established learning theory. |
| C04–C05 | Forced exposure and counterfactual feedback reduce masking; the tested counterfactual treatment has the larger effect. | Both supply information lost through avoidance. The counterfactual treatment supplies a different amount/type of information than 5% exposure, so its larger reduction is readily understandable. | Establish information access as a model lever; report the measured magnitudes without presenting the ranking as surprising treatment efficiency. |
| C07 | Adding intermediate actions preserves the optimum of an affine payoff function. | A linear function is maximized at an endpoint. | An exact control: C06's behavioural trade-off occurs with the best attainable reward unchanged. |
| C10 | Easier escape from adverse standing makes authenticity more attractive. | Recovery reduces the future cost of a bad outcome. | A quantified environmental lever. |
| C11 | Authenticity dominates in Accepted by a+c. | The two actions have identical transition probabilities there; continuation values cancel and the immediate reward gap is positive by specification. | An exact explanation and validation of the persistent-state mechanism. |
| C13 | A finite learner can allocate actions suboptimally relative to a full-information oracle. | Incomplete information and stochastic finite learning need not attain the oracle policy. | Establishes the phenomenon; C14's persistence under tested perturbations supplies the more interesting extension. |
| C18 | A larger search problem can incur costs despite an apparently successful final endpoint. | Time to a good outcome and payoff accumulated along the way are different from final modal classification. | A useful measurement lesson; separates endpoint success from cost. |
| C22 | Increasing comparison cost raises actual masking while some objective advantage remains. | Higher cost reduces the authentic reward; a stochastic learner need not wait for exact indifference to alter its action frequencies. | Supplies actual behavioural rates underlying C21. |
| C23 | Similar behaviour can have multiple causes, and the same environment can produce different behaviour. | Equifinality and multiple determinants are familiar principles. | The framework's organizing synthesis and applied contribution; its value lies in the concrete decomposition and tests. |

The general principle in C12—future consequences can reverse an immediate payoff ranking—also belongs here. C08's exact rejection/variance formula and C20's exact crossover equation are similarly straightforward consequences of their specified payoffs.

The hot-stove mechanism is directly established in [Denrell and March (2001)](https://pubsonline.informs.org/doi/10.1287/orsc.12.5.523.10092), which explains how adaptive sampling can favour familiar successful alternatives and prematurely exclude risky or novel ones.

## 2. Expected from the gifted-children literature

This category concerns the direction and interpretation expected from prior gifted research. It establishes why the model is relevant to this population. The exact parameter values and computational effect sizes remain contributions of the present model.

| Claim IDs/aspect | Literature-anticipated claim | What the present analysis adds |
|---|---|---|
| C12, social interpretation; C23 overlap | Concealment can be a purposeful response to social consequences. | An explicit criterion distinguishing dynamically adaptive concealment from masking that sacrifices available objective value. |
| C08, behavioural interpretation; C06's engagement component | Students can manage visibility selectively or partially instead of choosing only complete concealment or full display. | A quantitative action representation and the consequences of separately learning each level. The adverse endpoint trade-off belongs in category 3. |
| C19; C11's broad social interpretation | Receptive peers/settings should facilitate expression and reduce the need for visibility management. | Controlled variation in receptive-context abundance and representation; exact model effect sizes. |
| C20, comparison-cost ingredient | A high-ability peer environment can bring social-comparison costs alongside other advantages. | A transparent comparison-cost parameter and exact objective crossover; the learned/objective separation belongs in category 3. |
| C23, contextual variation | Visibility management varies across learners and social settings. | A formal set of mechanisms and measurements that can distinguish those variations. |

[Coleman and Cross (1988)](https://journals.sagepub.com/doi/10.1177/016235328801100406) documented information management used by some gifted adolescents to reduce visible giftedness. [Swiatek (1995)](https://journals.sagepub.com/doi/10.1177/001698629503900305) investigated distinct social-coping strategies. [Klimecká's study](https://doi.org/10.1080/02671522.2022.2065523) documents social costs of labeling together with coping through conformity, helping, and denial. These findings make socially responsive and selective concealment an expected application, rather than a surprising discovery of this model.

The contextual reading is also supported by the primary research described in [Irish Gifted Students: Self, Social, and Academic Explorations](https://www.dcu.ie/ctyi/irish-gifted-students-self-social-and-academic-explorations), which examines hiding, conformity, social interaction, and differences between regular school and gifted-program settings. The prediction that a greater receptive share helps is an inference from this literature's context-sensitive account, not an empirical confirmation of the model's one-to-four-context manipulation.

For the comparison-cost ingredient, the [gifted-child BFLPE study by Zeidner and Schleyer (1999)](https://doi.org/10.1006/ceps.1998.0985) reports reference-group effects on academic self-concept, test anxiety, and grades. This supports anticipating social-comparison costs; the model represents that idea through an explicit payoff term rather than measuring those empirical constructs.

Greater lambda should not be classified as a known gifted-child characteristic. In this study it is a general learner parameter; C01–C02 therefore belong primarily in category 1.

## 3. Surprising results

### Strongest applied surprises

**A. More gradual options sustain engagement while reducing intensity and use of the best endpoint — C06.**

A plausible educational expectation is that intermediate steps preserve participation and help approach fuller expression. The model gives the first benefit together with an endpoint deficit: nonzero disclosure rises 25.50 points, full-authentic endpoint use falls 32.87 points, and normalized objective loss rises .02976. The payoff optimum is held fixed. The scientific interest is the combination and its dependence on independently learned levels. This is a useful applied surprise even though independent-arm learning makes its explanation intelligible.

**B. An unchanged receptive opportunity becomes much less usable under some representations but stays usable under another — C15–C16.**

The opportunity's best expected reward is unchanged, yet expanding the context set raises masking from approximately 26% to 84–87% in the flat and hierarchical representations. Under global-mask representation, masking instead changes from 27.23% to 25.77%. Some cost of added alternatives is expected; the strong interaction with how actions are represented is the more interesting result. Hierarchically separating context and behaviour also fails to protect the good-authentic modal outcome in the tested formulation.

**C. Successful exposure is nearly universal, yet extensive masking continues — C17.**

Over 99.6% of learners have experienced accepted authenticity in the good context, while final-window masking remains 84–87%. A plausible first explanation—learners simply never encountered the favourable opportunity—does not account for this conjunction. The result motivates separating first encounter, learned valuation, and sustained allocation of behaviour. It concerns encountering acceptance at least once, not verified accurate knowledge of the full payoff structure.

**D. The learned population boundary lies well inside the objectively favourable region — C21.**

The good-authentic modal-classification crossing is .312852 [.307836, .316918], while objective indifference is .470588. Authenticity retains an expected-reward advantage of .134076 at that crossing. The result occurs at lambda=1. The general possibility of learned/objective mismatch is familiar; its resolved extent in this architecture and its occurrence without enhanced loss weighting make this a useful quantitative result. Its distinctiveness is less strong than a demonstrated new causal mechanism for that separation would be.

### Surprising extent and persistence of familiar mechanisms

**E. Durable social consequences relocate the objective threshold dramatically — C09, with C12 examples.**

Dynamic values can differ from immediate rewards, which is expected. The substantial implication here is a shift from a static threshold of .717 to .384–.269. At one verified setting, an action with immediate expected reward −.20 is dynamically optimal over an action paying +.75. Lead with that concrete reversal and magnitude, supported by the exact state structure.

**F. Suboptimal masking survives substantial additional opportunity to learn — C14.**

Finite-learning error is expected. Retention of the masking–optimality gap at all five prespecified sentinels through 5,000 steps, and across the named population/window/weighting/initialization checks, adds nontrivial persistence. Mean Neutral masking at those extended-horizon sentinels is about 90–99.7%. This is a stronger contribution than the mere existence of an oracle gap.

## Complete primary assignment of the 23 claims

| Claim | Primary category | Aspect governing the assignment |
|---|---:|---|
| C01 | 1 | Changing the negative-outcome weight changes behaviour; a large demonstration. |
| C02 | 1 | Exact subjective-threshold movement follows from the reward transform. |
| C03 | 1 | Established hot-stove mechanism. |
| C04 | 1 | Restoring information changes sampling and learned values. |
| C05 | 1 | Relative effect of the two differently specified information treatments. |
| C06 | 3 | Engagement rises while endpoint use and intensity fall. |
| C07 | 1 | Affine expected-reward geometry. |
| C08 | 1 | Rejection and variance results follow the model; selective/partial visibility has category-2 relevance. |
| C09 | 3 | Magnitude and concrete consequences of the dynamic threshold relocation. |
| C10 | 1 | Recoverability improves the value of taking the risk. |
| C11 | 1 | Dominance follows directly from identical transitions and positive payoff gap. |
| C12 | 1 | Dynamic reversal of immediate rankings is expected; adaptive concealment has category-2 relevance. |
| C13 | 1 | Existence of finite-learner/oracle suboptimality. |
| C14 | 3 | Persistence across the executed sensitivity checks. |
| C15 | 3 | Representation-dependent response to context expansion. |
| C16 | 3 | Large actual masking effects with contrasting global-mask behaviour, read with C15. |
| C17 | 3 | Nearly universal successful encounter alongside extensive later masking. |
| C18 | 1 | Endpoint success and payoff cost along the path are different measures. |
| C19 | 2 | More widespread receptive settings improve the relevant behavioural outcome. |
| C20 | 2 | Literature-anticipated comparison-cost ingredient; exact payoff crossover is category 1. |
| C21 | 3 | Quantified population-boundary displacement at lambda=1. |
| C22 | 1 | Rate response to increased cost; supports the interpretation of C21. |
| C23 | 1 | General multiple-cause principle; the concrete integration supplies the paper's contribution. |

Primary assignment: **14 category-1 claims, 2 category-2 claims, 7 category-3 claims**. Several category-1 claims also have a literature-anticipated social interpretation, listed in category 2 above. The seven category-3 entries form six themes because C15 and C16 describe complementary outcomes of one representation experiment. These counts are editorial categories, not counts of statistically independent discoveries.

The three M4 mathematical additions in the supported-claims review belong primarily in category 1: geometric decay, conditional expected drift, and roots of the specified mean-drift equation. They are useful theoretical results and do not need a surprise claim.

## Recommended role in the paper

Use category 1 to establish the machinery and demonstrate familiar mechanisms. Use category 2 to establish the model's relevance to gifted learners. Give category 3 the most space in the Abstract, main Results, and Discussion: particularly the graded-action trade-off, representation interaction, and successful-encounter/sustained-use separation, followed by the dynamic thresholds, persistence checks, and learned-boundary displacement.

This classification changes emphasis only. It does not revise the numerical evidence, manuscript, model, or existing scientific freeze. The external source check was targeted to the research traditions above; it is not an exhaustive novelty search.
