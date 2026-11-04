# How the masking simulations work

Prepared 5 October 2026. This guide explains the maintained M0–M4 models and the E01–E06 experiment programme. The current article's numerical evidence covers E01–E05. M4/E06 is an implemented extension with diagnostic smoke evidence and deferred confirmatory work.

The models ask how a learner allocates behaviour when expressing ability can bring benefits, rejection, or consequences for later opportunities. They are constructed computational systems. Their simulated learners are not observations of children, and their reward units do not measure human welfare. “Masking” names the model's lower-visibility action. “Authenticity” names its ability-expressive action.

## 1. The map of the simulations

Models specify an environment and a learner. Experiments compare controlled conditions within those models. They are different numbering systems.

| Model | What changes relative to the simplest environment? | Main question | Experiment |
| --- | --- | --- | --- |
| M0: binary bandit | Two actions, fixed receptivity, no persistent social state | How do feedback, weighting, and information affect future choices? | E01 |
| M1: graded disclosure | Multiple independently learned disclosure levels | Can more participation coexist with less intense expression? | E02, compared with M0 |
| M2: persistent social state | Actions can change future rewards through social standing | Does persistence change optimal behaviour, and does learning attain that optimum? | E03 |
| M3: context search | The learner chooses among contexts and behaviours | How do representation and receptive-context abundance affect use? | E04 |
| M3 with comparison cost | Accepted authenticity in a good context has an additional cost | How far apart are learned and objective boundaries? | E05 |
| M4: endogenous receptivity | Behaviour changes the acceptance probability itself | Can history produce different continuation paths at the same control value? | E06, deferred extension |

This is a ladder of mechanisms, not a single cumulative simulation. M3 does not automatically include M2's stigma states. M4 does not automatically include M3's context search. Adding a mechanism identifies another possible explanation rather than asserting that every learner has every mechanism.

The maintained code lives under [src/gifted_masking](../../../src/gifted_masking). The old monolithic scripts under `simulations_old/` are historical reference implementations. The main narrative and figures used here come from the [integrated article](../integrated_article_20261004/ARTICLE.md). Machine-readable sources and hashes accompany this guide in [SOURCE_INDEX.json](SOURCE_INDEX.json).

## 2. The shared learning process

Each simulated learner stores an estimate, Q, for each available action. Except in M2, the estimate depends on the action alone. An individual simulation step has the following order:

1. Convert the current Q-values to choice probabilities.
2. Sample an action and the relevant environmental outcome.
3. Calculate the realized environmental reward R.
4. Transform negative rewards using lambda.
5. Update the selected Q-value.
6. Apply or record the model-specific next state. M2 computes the next state before its Q-learning target; M4 updates receptivity after the reward and Q update.
7. Accumulate the measurements for the stated window.

### Parameters and meanings

| Symbol | Code name | Reference value | Meaning |
| --- | --- | ---: | --- |
| b | `b` | 1.0 | Social benefit component |
| a | `a` | 0.6 | Reward component associated with expression |
| c | `c` | 0.25 | Cost of masking |
| r | `r` | 2.0 | Rejection penalty; distinct from realized reward R |
| alpha | `alpha` | 0.1 | Weight of a new learning target in an update |
| tau | `temp` in kernels, `tau` in configs | 0.25 | Softmax temperature governing choice randomness |
| lambda | `lam` in kernels, `lambda` in configs | 1.0 | Multiplicative weight on negative realized rewards |
| Q0 | `q0` | 0.0 | Initial value of every action or state-action pair |
| gamma | `gamma` | 0.9 | Discount on continuation value in M2 |
| p | `p` | Varied | Authentic acceptance probability in a neutral/static context |

These are modelling choices, not fitted psychological measurements. Changing alpha changes recency weighting; it does not change the frequency of rejection. Changing lambda changes valuation of outcomes; it does not change the environmental payoff. Changing tau changes action sampling. At Q0=0, all initially equal actions are equally likely; that symmetry has different consequences when there are two actions and when there are 2K actions.

### Choice and learning equations

For available actions x,

\[
\pi_t(x)=\frac{\exp(Q_t(x)/\tau)}{\sum_y\exp(Q_t(y)/\tau)}.
\]

The implementation subtracts the largest scaled Q-value before exponentiating. This preserves the probabilities and avoids large exponentials for ordinary finite inputs. Positive tau leaves a nonzero chance of selecting less-valued actions. Constant alpha and positive tau describe continuing learning and exploration, not a guarantee of convergence to a deterministic optimum.

The subjective transform is

\[
v_\lambda(R)=\begin{cases}R,&R\geq0,\\\lambda R,&R<0.\end{cases}
\]

Lambda=1 leaves rewards unchanged. Lambda>1 magnifies losses. Values between zero and one attenuate losses. The maintained helper permits lambda=0, which maps negative rewards to zero, and rejects lambda<0. Rejection need not yield a negative reward for every parameter choice: when r<a, rejected full authenticity still pays a-r>0 and receives no negative-outcome multiplier.

For the bandits, only the chosen action receives the ordinary update:

\[
Q_{t+1}(x_t)=Q_t(x_t)+\alpha\{v_\lambda(R_t)-Q_t(x_t)\}.
\]

E01's counterfactual-information condition explicitly adds an update for the unchosen authentic action on masking trials. M3's hierarchical architecture updates both the selected context and the selected within-context behaviour. Those are specified experimental differences.

### A one-step example

Start with Q(mask)=Q(auth)=0, alpha=.1, tau=.25, and lambda=1. A rejected authentic choice earns -1.4. Its estimate becomes -.14, while masking stays at zero. The next authentic choice probability is about .364. If the first authentic outcome is accepted instead, Q(auth)=.16 and its next choice probability is about .655. Nothing in the environment changed between these two calculations. Experience changed the learner's next sampling probability. These are illustrative calculations, not estimated population effects.

## 3. M0: binary masking and authenticity

**Question.** Can different learning histories produce different behaviour under the same current environment?

M0 is a two-armed bandit: choose masking or authenticity repeatedly. “Bandit” means that the action produces an outcome but does not change a persistent environmental state. The learner normally observes the reward of its chosen action.

| Action/outcome | Probability conditional on the action | Environmental reward | Default reward |
| --- | ---: | --- | ---: |
| Mask | 1 | b-c | .75 |
| Authentic, accepted | p | b+a | 1.60 |
| Authentic, rejected | 1-p | a-r | -1.40 |

Expected rewards are

\[
E[M]=b-c,\qquad E[A]=a+pb-(1-p)r.
\]

At the reference values, E[A]=-1.4+3p. Its advantage over masking is 3p-2.15, so objective indifference occurs at p*=2.15/3=.716667. At p=.75, authenticity pays .85 on average versus .75 for masking. At p=.85, its expected reward is 1.15. At p=0 and p=1 it gives -1.4 and 1.6 respectively.

When the mask and accepted rewards are nonnegative and the rejected reward is negative, expected transformed-reward indifference is

\[
p^*_{\lambda}=\frac{b-c+\lambda(r-a)}{b+a+\lambda(r-a)}.
\]

It is .630435 at lambda=.5, .716667 at lambda=1, .806818 at lambda=2, and .833333 at lambda=2.5. This calculation describes the transformed target. It is neither an observed population transition nor a change in environmental value. The expression must be reconsidered when reward signs change.

**Mechanism.** An adverse outcome lowers the authentic estimate, reducing resampling and thus reducing access to corrective authentic experiences. This is the hot-stove mechanism. It can operate at lambda=1. A history effect and an extra negative-outcome weight are separate mechanisms.

**Implementation and output.** [m0.py](../../../src/gifted_masking/models/m0.py) defines `expected_rewards`, `expected_gap`, `objective_indifference_r`, `subjective_indifference_r`, and `simulate`. The baseline `simulate` returns one final-window mask fraction per learner. Richer histories and regret come from the experiment recorder, not that return array. Baseline kernel defaults are n=300 and T=1500; E01 uses its own recorded design below.

### E01: feedback history, weighting, and corrective information

E01 uses 500 learners per cell, 2,000 steps, and five independent master seeds. The final window is steps 1600–1999. The controlled conditions force the step-0 choice to authenticity after consuming the usual random draws. The outcome is still random. Initially accepted and rejected learners form disjoint strata, not paired copies of one person.

The exact standard design has ten cells: at p=.75 and .85, lambda=1 crosses controlled baseline, 5% forced authentic exposure, and counterfactual authentic feedback; two additional controlled-baseline cells use p=.75 and lambda=.5/2.5; two maintained-baseline cells use p=.65 and lambda=.5/2.5. The maintained-baseline condition does not force the initial action.

Forced exposure uses an independent intervention stream: on 5% of post-initial steps the action must be authentic, overriding a sampled mask when necessary. Counterfactual feedback supplies the authentic reward associated with the same latent acceptance draw on a masking trial and updates Q(auth). It does not add that unchosen reward to the realized return. The two information conditions have different exposure and information intensities.

| Archived result | Estimate and 95% interval | Interpretation |
| --- | --- | --- |
| Initial rejection minus acceptance, post-initial authentic sampling | -2.58 percentage points [-3.58, -1.59] | Early feedback affects later sampling across steps 1–1999 |
| Same contrast, final-window masking | -.034 points [-1.160, 1.092] | No detected final-window difference in this comparison; this does not establish equivalence |
| Forced exposure minus controlled baseline, rejected stratum | -4.66 points of final masking [-6.00, -3.32] | Additional authentic experience changes later allocation |
| Counterfactual feedback minus controlled baseline, rejected stratum | -11.81 points of final masking [-12.66, -10.97] | Information on masking trials changes allocation more at this tested intensity |
| Lambda=2.5 minus .5 at p=.65, maintained baseline | +40.30 points of final masking [39.54, 41.06] | Weighting changes behaviour under unchanged payoffs |

The history and information comparisons pool p=.75/.85 equally within each master. The weighting comparison is at p=.65, where the environmental optimum is masking. It therefore demonstrates a weighting effect rather than suboptimal masking at that cell. History's normalized pseudo-regret contrast is an exact action-count translation of the sampling contrast, not an independent replication.

**Presentation sentence.** “What the learner has experienced, how it weights outcomes, and what it can learn while avoiding an action are distinct influences on behaviour.”

**Visual.** Integrated Figure 4, split into weighting and history/information panels across slides. Keep the null final-window history result visible when describing persistence.

## 4. M1: graded disclosure

**Question.** What changes when a learner can express a little rather than choosing only complete concealment or full expression?

M1 offers a grid of levels d between zero and one, normally {0,.25,.5,.75,1}. Acceptance probability is 1-(1-p)d. Thus complete masking is always accepted in this payoff construction, while full authenticity receives the original probability p.

The base reward is ad-c(1-d). Acceptance adds b; rejection subtracts r. Therefore

\[
E[R(d)]=b-c+d\{a+c-(1-p)(b+r)\}.
\]

This objective is affine in d. Full authenticity is uniquely optimal when the term in braces is positive; masking is uniquely optimal when it is negative; all levels tie when it is zero. Adding intermediate arms cannot create a strictly superior interior optimum under these equations.

**Worked example at p=.75.** Expected reward is .75+.10d. Masking pays .75. Half disclosure pays .80 on average, has acceptance probability .875, and earns either 1.175 or -1.825. Full authenticity pays .85 on average, with acceptance probability .75, and earns 1.6 or -1.4. Partial disclosure lowers the probability of rejection here, although its realized rejection reward is more negative because it also retains some masking cost and less expression benefit.

The reward variance is

\[
\operatorname{Var}[R(d)]=(b+r)^2(1-p)d\{1-(1-p)d\}.
\]

At p=.75, half and full disclosure have variances .984375 and 1.6875. Variance increases with d over the reported p=.75/.85 cells. It need not increase over every possible p and d, so “partial disclosure always has lower variance” is too broad.

**Learning assumption.** Each level has its own independent Q-value. Success at d=.25 does not directly update Q at d=.5 or d=1. The current experiment contains no smooth transfer of learning across levels. A staircase illustration must not imply such generalization.

**Implementation and output.** [m1.py](../../../src/gifted_masking/models/m1.py) defines `disclosure_levels`, `acceptance_probability`, `expected_reward`, and `simulate`. It checks grid endpoints and probability bounds. Its baseline return is each learner's final-window mean d, not a mask fraction or endpoint frequency. Baseline defaults are five levels, n=300, and T=1500.

### E02: binary versus independent graded actions

The exact design crosses p=.65/.75/.85 with binary endpoints and five independent graded arms, using n=500, T=2000, and five masters. The first choice is full authenticity. Within each p/master, the two architectures share latent uniform sequences and learner identifiers. Headline contrasts use the initially rejected stratum and equally pool p=.75/.85. The p=.65 condition supplies an objective-mask control.

| Graded minus binary outcome | Archived estimate and 95% interval | Measurement |
| --- | --- | --- |
| Any disclosure | +25.50 percentage points [25.30, 25.71] | d>0 over post-initial steps 1–1999 |
| Full-authentic frequency | -32.87 points [-34.20, -31.53] | d=1 during the last 400 steps |
| Unique-modal full authenticity | -22.17 points [-28.88, -15.47] | Fraction of learners whose d=1 count strictly exceeds every other arm |
| Normalized objective regret | +.029761 [.025648, .033874] | All 2,000 steps |
| Mean disclosure intensity | -.032088 [-.038941, -.025236] | Direct final-window mean d |

In the authenticity-optimal cells, normalized regret equals 1 minus full-horizon mean d. Its increase therefore implies a .029761 decrease in pooled full-horizon disclosure intensity. That identity does not supply independent confirmation of the same effect. The final-window intensity row uses a different window and is a separately measured outcome. The pooled result does not mean that every receptivity cell decreases: the archived final-window intensity contrasts are +.046511 at p=.75 and -.110688 at p=.85.

**Interpretation.** More learners' actions contain some expression, yet expression is less intense and the optimal endpoint is used less often. This demonstrates an engagement–intensity trade-off under independent action learning. It does not establish that intermediate levels are objectively best or that graded exposure reliably produces progressive movement to full expression.

**Presentation sentence.** “Graded options preserved participation while reducing average expression and use of the full-authentic endpoint.”

**Visual.** Integrated Figure 5. Separate the exact payoff lines from observed contrast estimates. A useful future ablation compares independent Q-values with explicitly specified cross-level generalization.

## 5. M2: persistent stigma and acceptance

**Question.** What if an action changes the conditions of later interactions?

M2 is a Markov decision process with Neutral, Accepted, and Stigmatized states. Each learner holds a 3-by-2 Q-table and begins Neutral. Rewards and state transitions depend on both the current state and chosen action.

| Current state | Action/event | Current reward | Next-state distribution |
| --- | --- | --- | --- |
| Neutral | Mask | b-c=.75 | Neutral with probability 1 |
| Neutral | Authentic acceptance, probability p | b+a=1.6 | Accepted |
| Neutral | Authentic rejection, probability 1-p | a-r=-1.4 | Stigmatized |
| Accepted | Mask | .75 | Neutral with probability delta, otherwise Accepted |
| Accepted | Authentic | 1.6 | Neutral with probability delta, otherwise Accepted |
| Stigmatized | Mask | b2-c=.25 | Neutral with probability eta, otherwise Stigmatized |
| Stigmatized | Authentic redemption, probability p/2 | 1.6 | Accepted |
| Stigmatized | Failed redemption, probability 1-p/2 | a-r2=-1.9 | Neutral with probability eta, otherwise Stigmatized |

Reference b2=.5, r2=2.5, and delta=.02. Reward comes before the next-state change. Turnover applies only to learners who began the step Accepted. Escape applies only to paths that began Stigmatized and remain Stigmatized after the action. A newly accepted Neutral learner does not immediately undergo turnover. A newly rejected Neutral learner does not immediately escape. Successful redemption takes precedence over escape. Masking itself does not reset stigma; the explicitly modelled escape process can do so after masking.

The Q-learning target includes future value:

\[
Q_{t+1}(s_t,x_t)=Q_t(s_t,x_t)+\alpha\big[v_\lambda(R_t)+\gamma\max_yQ_t(s_{t+1},y)-Q_t(s_t,x_t)\big].
\]

### Why immediate reward is insufficient

The known-model objective benchmark solves the discounted Bellman equation with untransformed environmental rewards. For any continuation values V, the Neutral authentic-minus-mask advantage is

\[
D_N(V)=a+c-(1-p)(b+r)+\gamma[pV_A+(1-p)V_S-V_N].
\]

The first term is the static advantage. The second prices the change in future social opportunity. At p=.4 and eta=0, immediate authentic reward is -.20 versus .75 for masking, yet the archived dynamic Neutral advantage is +.042943. Under the separate harsh setting p=.75, b2=0, r2=8, delta=.3, eta=0, gamma=.9, the immediate advantage is +.10 but the dynamic advantage is -.406293. Persistence can reverse the immediate ranking in either direction.

In Accepted, both actions have the same transition distribution, and authenticity earns .85 more immediately. Authenticity therefore strictly dominates masking there. In the reference Stigmatized state, immediate authentic expectation is -1.9+1.75p, below masking's .25 throughout p in [0,1]. Any dynamic preference for authenticity there depends on future redemption.

**Implementation and output.** [m2.py](../../../src/gifted_masking/models/m2.py) defines explicit state constants, `transition_step`, `simulate`, and `simulate_with_diagnostics`. Diagnostics include final-window state-action counts, state visits, objective reward, and final state. [m2_optimal.py](../../../src/gifted_masking/analysis/m2_optimal.py) supplies `build_m2_transition_table` and `solve_m2_value_iteration`. Baseline simulation defaults are n=300 and T=2000; E03's baseline grid differs.

### E03: optimal policy versus finite learning

The reference grid crosses p=0,.05,...,1 with eta=0,.05,...,.8: 357 parameter cells. Each uses 160 learners, 1,000 steps, a 200-step final window, and five masters. Value iteration uses gamma=.9, a 1e-10 stopping tolerance, and a 100,000-iteration maximum. An independent deterministic-policy envelope agreed over the baseline grid to a maximum difference of 8.99e-10.

| Escape probability eta | Objective Neutral authenticity threshold | Meaning |
| ---: | ---: | --- |
| 0 | .383942 approximately | Persistent acceptance can make expression worthwhile at lower initial receptivity |
| .2 | .338776 approximately | Recovery lowers the cost of entering adverse standing |
| .8 | .269012 approximately | Greater recovery lowers the objective threshold further |
| Static M0 comparator | .716667 | No persistent social state |

These dynamic thresholds are midpoints of numerical brackets about .000061 wide, not statistical confidence intervals.

Within each master and cell, E03 aggregates final-window Neutral actions. Adequacy requires at least 160 Neutral visits and at least 32 visiting learners. Equal action counts or inadequate exposure are inconclusive. “Learned suboptimal masking” means that adequate Neutral counts favour masking while the oracle favours authenticity. Stable classification requires at least four of five masters to agree on a non-inconclusive class.

The full partition is 243 learned-suboptimal-mask cells, 107 agreement cells, and seven inconclusive cells. All 243 suboptimal-mask cells have that classification in every master. These are counts of grid cells, not percentages of children.

Five disagreement sentinels, (.4,0), (.55,0), (.75,0), (.55,.2), and (.9,.2), retained the classification through T=5000. Their mean Neutral masking fractions were 99.67%, 98.22%, 95.42%, 97.12%, and 89.97%. The denominator is observed Neutral actions, not all steps or learners. A sixth sentinel, (.35,0), is a boundary/agreement control and is excluded from that five-cell set.

Separate perturbations change n to 320; T to 2000/5000; window fraction to .1/.4; alpha to .03/.3; tau to .1/.6; lambda to .5/2.5; Q0 to .75; gamma to .5/.99. Baseline and 11 perturbations retain 25/25 disagreement cell-master classifications. Alpha=.03 retains 18/25, tau=.6 retains 21/25, and gamma=.5 retains 10/25. The remaining classifications in those rows agree with the oracle. Changing gamma changes the objective as well as learning. These are one-factor tests, not a joint robustness guarantee.

**Interpretation.** Here “suboptimal” has an explicit, model-relative dynamic benchmark. The learner acquires information over a finite horizon; the oracle knows the environment and optimizes an infinite discounted horizon. Persistence to 5,000 steps does not establish permanent entrenchment or asymptotic convergence failure. The reported classification gap is also distinct from a cumulative dynamic-regret estimate.

**Presentation sentence.** “Persistent social consequences changed what was optimal, while finite learners often continued masking in Neutral states where the dynamic benchmark favoured expression.”

**Visuals.** Integrated Figures 2, 6, 7, and 8 cover transitions, thresholds, the grid partition, and sensitivity exceptions respectively.

## 6. M3: choosing contexts and behaviours

**Question.** Does access to a receptive group translate into repeated expression, and does the way choices are represented matter?

The reference environment has K contexts, one good context with p_good=.85, and K-1 bad contexts with p_bad=.2. At zero comparison cost, expected rewards are .75 for masking anywhere, 1.15 for authenticity in a good context, and -.80 for authenticity in a bad context. Increasing K leaves the best achievable reward unchanged.

### Four ways to represent the same opportunities

| Architecture | Learned values | Choice and update | What it isolates |
| --- | --- | --- | --- |
| Flat 2K | One Q per context-behaviour pair | Single softmax, selected pair updated | Duplicated context-specific mask arms and authentic arms |
| Hierarchical | K context values plus two behaviour values per context | Choose context, then behaviour; update both from the same transformed reward | Sequential choice without pooling mask values |
| Global mask | One shared mask Q plus K authentic-context Qs | Single softmax, selected action updated | Removes duplication of masking estimates |
| Fixed known good | Two behaviour Qs in a known good context | Binary learning within that context | Removes context search |

For flat/hierarchical joint indices, action 2g is masking in context g and 2g+1 is authenticity there. For K=4, there are eight flat arms. The global-mask architecture instead has five actions. At equal initial Q-values, its total mask probability is 1/(K+1), while flat and hierarchical representations start at one half. Thus the architecture ablation changes both information sharing and initial action allocation. It does not isolate a single pure psychological mechanism.

In the hierarchical implementation, the context receives the same reward update as the behaviour. It does not automatically learn the context's best achievable reward or share masking knowledge across contexts.

**Implementation and outputs.** [m3.py](../../../src/gifted_masking/models/m3.py) defines `group_probabilities`, `decode_action`, `expected_reward_for_action`, `simulate`, `simulate_hierarchical`, `simulate_global_mask`, and `simulate_fixed_good_pond`. Simulation returns a good-authentic modal indicator, actual final mask fraction, and modal action index. Its internal name `optimal_action` always identifies the good-authentic arm. At costs above objective crossover that arm is no longer objectively optimal, so the returned indicator must not be described as general optimality. E05 separately records the true objective comparator. Baseline defaults are n=400 and T=2000.

### E04: context number, identity, abundance, and architecture

The standard design requests all four architectures, K in {1,2,4,8,16}, fixed/random-per-learner good-context identity, and one/two/proportional-good regimes. Good-context counts are 1, min(2,K), or max(1,ceil(K/4)). The latter guarantees at least one good context and rounds upward. Equivalent requests reduce 120 requested configurations to 55 distinct executable cells. Each has n=500, T=2000, and five masters. Multiple-good-context and randomized identity controls live in the experiment implementation, beyond the baseline module's single-good-context helper.

| Architecture, one good context | Masking at K=1 | Masking at K=16 | K=16 minus K=1, 95% interval |
| --- | ---: | ---: | --- |
| Flat 2K | 26.36% | 84.19% | +57.83 percentage points [57.43, 58.22] |
| Hierarchical | 26.45% | 87.27% | +60.82 points [60.21, 61.42] |
| Global mask | 27.23% | 25.77% | -1.46 points [-2.29, -.62] |

The fixed-known-good control has no structural K effect. This is a property of its canonical two-action task. Sampled K=1 levels in separate architecture streams need not match exactly despite equivalent opportunities.

At K=16, 99.72% of flat learners and 99.64% of hierarchical learners experienced accepted authenticity in the good context at least once. Extensive later masking therefore coexists with successful encounter. Encounter is a learner indicator over the whole trajectory; masking is a final-window action fraction. Experiencing acceptance once is not equivalent to accurately knowing all reward distributions.

Good-authentic modal classification falls from K=1 to 16 by 23.40 points in flat choice and 47.04 points in hierarchical choice. Randomizing good-context identity and applying a strict unique-mode diagnostic retain those directions. Global-mask modal classification rises slightly from 98.16% to 99.04%. Nevertheless, its full-horizon expected static regret per step increases by .121423 [.119686,.123159], and its capped first-success time increases by 16.16 steps [14.49,17.83]. A favourable final modal action does not imply costless learning.

At K=16, changing from one to four good contexts raises good-authentic modal classification from 75.48% to 99.36% in flat choice and from 52.00% to 95.80% in hierarchical choice. These endpoint levels are descriptive means; the planned abundance inference uses within-master slope differences per log2(K).

**Interpretation.** The broad claim “larger K causes masking” does not survive every architecture. The supported finding is representation-dependent. Opportunity abundance and use matter alongside first encounter. Softmax normalization over multiple arms, duplicated mask estimates, and feedback to selected actions are part of the model, not nuisances to hide.

**Presentation sentence.** “Almost everyone encountered receptive feedback, yet sustained expression depended strongly on how the available choices were represented.”

**Visuals.** Integrated Figure 3 for architectures and Figure 9 for observed contrasts. Split its panels across slides and preserve each denominator.

## 7. E05: comparison cost and the learned boundary

E05 uses M3 with K=4, one fixed good context, lambda=1, n=500, T=2000, and five masters. It changes bf, a simplified comparison cost motivated by the big-fish–little-pond idea. It subtracts bf only from accepted authenticity in the good context. It leaves masking and rejected authenticity unchanged. It is a stipulated payoff mechanism, not a fitted empirical estimate of the big-fish–little-pond effect.

\[
R_{G,accepted}=1.6-b_f,\qquad E[R_G]=1.15-.85b_f.
\]

Good-authentic advantage over masking is .40-.85bf. Consequently the objective crossover is bf*=8/17=.470588. At bf=.325, good authenticity still has an expected advantage of .12375.

The exact grid is {0,.30,.325,.35,.375,.40,.425,.45,8/17,.475,.50,.525,.55,.575,.60,.625,.65,.80}. The 16 points in [.30,.65] resolve the crossing; zero and .80 supply external diagnostics. Flat 2K is the primary architecture and hierarchical choice is the secondary comparison.

**What crosses 50%?** The fraction of learners whose most frequent individual final-window action is the good-authentic arm. Final action counts use deterministic first-index `argmax`, retaining ties. This is different from a learner's probability of authenticity or a population's total mask fraction.

Five complete master response curves receive equal weights. A non-increasing isotonic fit regularizes the dense curve. The .5 inverse uses interpolation, or the midpoint of a plateau. A crossing must be strictly inside (.30,.65). Ten thousand bootstrap resamples retain complete master curves, refit, and reinvert; they do not independently resample cost points.

| Quantity | Archived value | Evidence type |
| --- | --- | --- |
| Objective crossover | .470588 | Exact payoff identity |
| Flat learned modal-population crossing | .312852, 95% CI [.307836,.316918] | Whole-master-curve bootstrap, 10,000/10,000 valid crossings |
| Objective minus learned crossing | .157736 | Difference between those defined quantities |
| Objective authentic advantage at the learned crossing | .134076 | Algebraic translation, bounds [.130620,.138340] |
| Hierarchical crossing | Left-censored below .30 | No estimable in-range crossing; do not extrapolate a point |

At bf=0, actual masking is already 58.82%, while 94.00% of learners have a good-authentic modal arm. There are four mask arms: one authentic arm can beat each mask arm individually while all mask arms together account for most actions. At bf=.30, .325, and 8/17, masking is 77.61%, 78.95%, and 85.20%, while good-authentic modal classification is 52.92%, 47.24%, and 14.16%.

**Interpretation.** The learned population boundary occurs inside the objectively favourable region at lambda=1. This is an architecture-specific finite-learning finding. It is not the onset of majority masking and is not the objective point at which comparison cost removes the opportunity's value.

**Presentation sentence.** “The learned modal-population crossing occurred near .313 even though good-context authenticity remained objectively preferable until .471.”

**Visual.** Integrated Figure 10. Keep the mathematical and learned thresholds distinct, and show total masking separately.

## 8. M4: behaviour changes receptivity

**Question.** What if behaviour changes the probability of future acceptance?

Each learner has its own evolving p_t, bounded by p_min=.05 and p_max=.95. It selects one of two actions using action-only Q-values. The environment samples acceptance using the current p_t, pays the M0 reward, and updates Q. It then changes p:

\[
p_{t+1}=\operatorname{clip}_{[p_{min},p_{max}]}\begin{cases}
p_t+k_a(p_{max}-p_t),&\text{accepted authenticity},\\
p_t-k_r(p_t-p_{min}),&\text{rejected authenticity},\\
p_t-k_m(p_t-p_{min}),&\text{masking}.
\end{cases}
\]

Default ka=.12 and kr=.04; p0 and km are explicit simulation inputs. Reward and learning use the old receptivity. Recorded trajectories then store the updated value. There is no shared peer population whose decisions couple different learners: receptivity evolves separately for each simulated learner.

**Worked example.** At p_t=.45 with km=.003, accepted authenticity moves p to .51, rejected authenticity moves it to .434, and masking moves it to .4488. These are alternative one-step calculations from the same starting value, not a three-step trajectory. Repeated masking lowers receptivity and can make the avoided authentic action less attractive. Accepted authenticity supplies an opposing feedback.

The Q-table has two action values and does not condition on p_t. M4 is therefore an endogenous, nonstationary bandit. A fully observed stateful learner would need an explicit representation of receptivity or a policy conditional on it. The full simulated system has evolving state, but its current learner does not use M2-style state-dependent Q-learning.

**Implementation and outputs.** [m4.py](../../../src/gifted_masking/models/m4.py) defines `update_receptivity`, `simulate`, `simulate_from_state`, and `hysteresis_experiment`. `simulate` returns final-window mask fractions, terminal p, and optional post-update p trajectories. `simulate_from_state` preserves supplied p/Q history through a segment and returns the final Q-values as well. Baseline simulation defaults are n=300 and T=2000. The generic ramp helper defaults to 600 steps per segment and carries both p and Q through ascending and descending km values.

### E06: continuation paths and the limits of hysteresis evidence

The implemented diagnostic smoke uses 64 learners, 120 steps per segment, final fraction .2, one master seed 2026081699, p0=.45, and km={0,.001,.002,.003,.004}. It has five path families and no bootstrap replicates. Its purpose is diagnostic rather than confirmatory inference.

| Path/control | Actual state handling | What it checks |
| --- | --- | --- |
| `inherited_loop` | Carry both p and Q through the full ascending and descending path | Combined environmental and learner history |
| `reversal_only` | Reset both p and Q before every segment, while retaining up/down traversal labels | Direction/order and independent-segment stochastic differences without inherited state |
| `cold_start` | Reset both p and Q at each km, single traversal | Response from identical initialization |
| `km_disabled_inherited_loop` | Carry history but set actual km=0 throughout | History effects that remain without the swept masking-feedback mechanism |
| `km_disabled_reversal_only` | Reset each segment and set actual km=0 | Matching disabled-feedback control |

The name `reversal_only` is easy to misread: the code resets at every segment, not only at the turning point. The endpoints appear in both directions in a full loop. Dwell time and direction-specific random streams matter when interpreting loop differences.

The staged standard configuration proposes 400 learners per family, five masters, km=0,.0004,...,.004, 500/1000-step primary segment durations, p0=.1/.9, ka<kr and ka=kr, ka=0, kr=0, and a km-disabled placebo. The qualification configuration adds 2,000-step segments, lambda=.5/2.5, and tau=.1/.6. Those configurations are plans, not executed standard/qualification evidence. Their approval flags are false; the current execution record defers E06 and no canonical standard GO record is present.

Path dependence means that history affects the observed state or response. Bistability requires evidence of distinct persistent regimes under the same fixed controls. A finite ramp loop can reflect lag or learning memory. Stronger hysteresis evidence needs replicated paired paths, appropriate reset/placebo controls, speed and dwell-time checks, estimable transition differences, and prespecified uncertainty. Permanent irreversibility is stronger still. The existence of a function named `hysteresis_experiment` proves none of these claims by itself.

**Presentation sentence.** “M4 makes receptivity responsive to behaviour. Its formal E06 work remains a deferred test of whether continuation differences exceed transient and control effects.”

**Visual.** Use the update equations and the worked three-outcome table. Present the ramp design as a proposed experiment. Do not import an old split-trajectory image as confirmed hysteresis evidence.

## 9. Measurements, uncertainty, and reproducibility

For horizon T and final fraction f, the maintained final window contains W=max(1,ceil(fT)) steps, beginning at zero-based T-W. For T=2000 and f=.2 it is exactly steps 1600–1999. The experiment-specific horizon and window override a kernel's defaults.

| Quantity | Denominator and interpretation | Frequent presentation error |
| --- | --- | --- |
| Mask rate | Mask actions / measured actions for a learner, then summarized | Calling it a fraction of permanently locked learners |
| Any disclosure | Count of d>0 / specified steps | Treating all nonzero disclosure as full expression |
| Intensity | Average d in the specified window | Mixing it with endpoint frequency |
| Full-authentic frequency | Count of d=1 / measured steps | Treating it as modal classification |
| Modal classification | One indicator per learner, based on individual arm counts | Aggregating all mask arms before applying the original classifier |
| Ever accepted in a good context | Learners with at least one such event / learners | Equating one success with accurate knowledge or sustained use |
| E03 Neutral mask fraction | Neutral mask counts / all observed Neutral counts, within master/cell | Using all actions or all learners as the denominator |
| Static objective regret | Mean known expected-reward gap to the best static action | Treating random realized losses as the exact expected regret |
| Objective numerical bracket | Solver precision for a boundary | Calling it a Monte Carlo confidence interval |

Legacy lock, basin, and bistability summaries use their own threshold definitions. They are not interchangeable with the current article's modal classification or E03 state-conditional counts. Do not add them to the deck without specifying the relevant original estimator.

| Experiment | n per cell/family | T | Independent masters |
| --- | ---: | ---: | --- |
| E01 | 500 | 2000 | 2026081101–2026081105 |
| E02 | 500 | 2000 | 2026081201–2026081205 |
| E03 baseline | 160 | 1000 | 2026081301–2026081305 |
| E04 | 500 | 2000 | 2026081401–2026081405 |
| E05 | 500 | 2000 | 2026081501–2026081505 |
| E06 diagnostic smoke | 64 | 120 per segment | 2026081699 only |

E01/E02/E04 scalar effects use five master-level contrasts and Student-t 95% intervals with four degrees of freedom. E01/E02 pool specified receptivity cells equally within master. E05 resamples complete master curves. E03 reports explicit classifications and exposure criteria. Secondary intervals are pointwise. Five masters are not five hundred independent master replications simply because each cell contains five hundred learners.

The maintained baseline kernels initialize a local NumPy generator from a seed and draw vectorized arrays for the learner population. They do not give each child a separately addressable independent generator. Increasing n can change later draws assigned to an existing child. Article recorders use semantic cell/family identifiers, hashing, and SeedSequence namespaces, with intentional matching where the design calls for it. E02 matches architectures within p/master. E05 matches cost conditions within architecture/master. These pairings must survive analysis and resampling.

Manifests preserve configurations, master/stream hierarchy, environment versions, source fingerprints, timings, and output hashes. The historical runs record Python 3.14.6, NumPy 2.4.6, and macOS arm64. This describes the archived environment, not necessarily the current interpreter. Exact historical generator sources are recovered for E04/E05; the E01–E03 source states remain incompletely recovered. Verified archived outputs support the retained results without establishing byte-identical historical regeneration from current code.

## 10. What the presentation can conclude

The simulations demonstrate several distinct relationships: feedback and information alter learning under fixed payoffs; graded action representation separates engagement from intensity; persistent states change the objective opportunity itself; context representation determines how available receptivity translates into sustained use; and a learned population boundary can lie inside an objectively favourable region.

Their educational interpretation is a set of testable hypotheses. Measure expectations, experienced outcomes, cross-action transfer, recovery opportunities, and repeated contextual use separately. The models do not determine an appropriate disclosure choice for an individual child.

Outstanding tests include E01 horizon and learning-rate sensitivity, E02 additional grids and generalization, broader E04 receptivity/temperature tests, longer-horizon E05 crossings, and separately authorized E06 standard/qualification work. The completed E03 checks include informative exceptions and do not establish robustness over all joint parameter combinations.

For the presentation, the central scientific point is: similar visible concealment can arise through different learning and environmental processes, and apparently favourable outcomes such as participation or first success can coexist with continuing underuse of opportunity.

## 11. Source navigation

- Current scientific account and detailed figure captions: [ARTICLE.md](../integrated_article_20261004/ARTICLE.md), especially Sections 2–3 and Appendix A.
- Maintained numerics: [core.py](../../../src/gifted_masking/core.py), [params.py](../../../src/gifted_masking/params.py).
- Model kernels: [M0](../../../src/gifted_masking/models/m0.py), [M1](../../../src/gifted_masking/models/m1.py), [M2](../../../src/gifted_masking/models/m2.py), [M3](../../../src/gifted_masking/models/m3.py), [M4](../../../src/gifted_masking/models/m4.py).
- Experiment recorders: [E01](../../../src/gifted_masking/experiments/article.py), [E02](../../../src/gifted_masking/experiments/e02.py), [E03](../../../src/gifted_masking/experiments/e03.py), [E04](../../../src/gifted_masking/experiments/e04.py), [E05](../../../src/gifted_masking/experiments/e05.py), [E06](../../../src/gifted_masking/experiments/e06.py).
- Exact experiment designs: [configs/frontiers_article](../../../configs/frontiers_article).
- Numerical source tables: [publication_v1/data](../publication_v1/data) and [results/summaries](../../../results/summaries).
- Figure sources, panel selectors, and hashes: [FIGURE_PROVENANCE.json](../integrated_article_20261004/FIGURE_PROVENANCE.json).
- E06's execution/evidence boundary: [CURRENT_STATE.md](../CURRENT_STATE.md), [standard-readiness design](../E06_STANDARD_READINESS_IMPLEMENTATION.md), and [E06 standard configuration](../../../configs/frontiers_article/e06_m4_paths_standard.json).

All reported intervals and experimental estimates above are retained archived findings. Worked examples are labelled deterministic illustrations. Preparing this guide did not create a new experiment result or change model semantics.
