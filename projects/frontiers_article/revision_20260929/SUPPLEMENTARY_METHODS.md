# Supplementary Methods

## How Learning and Social Opportunity Shape Ability Concealment: A Computational Study

This supplement specifies the models, estimands, archived analyses, and
supporting results for the five experiments reported in the article.
Environmental reward, transformed reward, learned action value, and
full-information dynamic value are distinct quantities. E01–E05 supply the
numerical evidence; no E06/M4 numerical result is included. The environments
are deliberately simplified computational models, with normalized reference
payoffs and no conversion from model steps to calendar time.

The revised presentation makes additional archived outcomes explicit without
changing their original status. Primary contrasts, secondary outcomes,
deterministic benchmarks, and exact mathematical consequences are identified
below. Numerical summaries are drawn from existing artifacts; no experiment,
bootstrap, or sensitivity analysis was rerun for this revision.

## S1. Common learner and simulation conventions

### S1.1 Actions, values, and reward transformation

The stateless learner assigned one value to each represented action,
initialized at $Q_0(x)=q_0=0$. Reference learning parameters were
$\alpha=.1$, $\tau=.25$, and $\lambda=1$. For realized environmental reward
$R$,

$$
v_\lambda(R)=
\begin{cases}
R,&R\geq0,\\
\lambda R,&R<0.
\end{cases}
$$

The transform affected learning, not the environment's objective payoff.
Reference configurations were loss-neutral, so $v_1(R)=R$; the documented
weighting contrasts used $\lambda=.5$ and $2.5$. The selected stateless action
$x_t$ was updated by

$$
Q_{t+1}(x_t)=Q_t(x_t)+\alpha\{v_\lambda(R_t)-Q_t(x_t)\},
$$

with unselected values unchanged. M2 used the state-action update in S4.

### S1.2 Choice rule

For action set $\mathcal A$, choice probabilities were

$$
\Pr(x_t=x)=
\frac{\exp\{(Q_t(x)-m_t)/\tau\}}
{\sum_{y\in\mathcal A}\exp\{(Q_t(y)-m_t)/\tau\}},
\qquad m_t=\max_{y\in\mathcal A}Q_t(y).
$$

Subtracting the row maximum provided numerical stability without changing
probabilities. Temperature and negative-outcome weighting are model
parameters, not measured characteristics of gifted learners.

### S1.3 Payoffs and terminology

| Symbol | Meaning in the model | Reference value |
| --- | --- | ---: |
| $b$ | benefit attached to masking or accepted authenticity | 1.00 |
| $a$ | authenticity value | .60 |
| $c$ | masking cost | .25 |
| $r$ | rejection penalty | 2.00 |

Masking denotes the low-visibility action and authenticity the represented
higher-visibility action. A context is an option with an acceptance
probability. Neutral, Accepted, and Stigmatized are explicit model states.
An objective benchmark uses the specified untransformed environmental
rewards. Expected transformed reward instead averages $v_\lambda(R)$.
Learned $Q$ values depend on sampled experience; the dynamic objective
benchmark additionally values future state transitions.

### S1.4 Horizons, windows, and behavioural measures

| Experiment | Learners per standard cell | Steps $T$ | Final window | Master seeds |
| --- | ---: | ---: | --- | ---: |
| E01, E02, E04, E05 | 500 | 2000 | 1600–1999 | 5 |
| E03 baseline | 160 | 1000 | 800–999 | 5 |

Indices are zero based. With window fraction $f$, the final window begins at
$T-\lceil fT\rceil$; $f=.2$ except for named sensitivity settings. Final-window
modal classifications use action counts rather than final $Q$ ordering.

The outcomes answer different questions: any-disclosure frequency measures
engagement; mean disclosure measures intensity; endpoint frequency measures
use of a particular action; modal classification identifies the most frequent
individual action; total masking sums masking actions across contexts; ever
successful encounter records at least one accepted good-context authentic
action; and objective regret records payoff gaps accumulated during learning.
Finite-window summaries are not convergence criteria.

## S2. E01 — feedback history, outcome weighting, and information

### S2.1 M0 rewards and objective indifference

Masking returned $R_M=b-c$. Authenticity returned $b+a$ with probability $p$
and $a-r$ otherwise, so

$$
\mathbb E[R_A]=p(b+a)+(1-p)(a-r)=a+pb-(1-p)r,
$$

$$
\Delta_0(p)=\mathbb E[R_A]-R_M=a+c-(1-p)(b+r).
$$

With the reference payoffs, $R_M=.75$, $\mathbb E[R_A]=3p-1.4$, and

$$
p^*=1-\frac{a+c}{b+r}=\frac{43}{60}\approx .716667.
$$

Authenticity is objectively optimal at $p=.75$ and $.85$, the primary
history-comparison settings; masking is objectively optimal at $p=.65$.

### S2.2 Expected transformed reward and weighting contrast

When masking and accepted-authentic rewards are nonnegative but rejected
authenticity is negative, expected transformed authenticity is
$p(b+a)+(1-p)\lambda(a-r)$. Its equality with masking occurs at

$$
p^*_{\lambda}
=\frac{b-c+\lambda(r-a)}{b+a+\lambda(r-a)}
=\frac{.75+1.4\lambda}{1.6+1.4\lambda}.
$$

For $r>a$ and $a+c>0$,

$$
\frac{dp^*_{\lambda}}{d\lambda}
=\frac{(r-a)(a+c)}{[b+a+\lambda(r-a)]^2}>0.
$$

| Negative-outcome weight | Transformed-reward threshold | Objective threshold |
| ---: | ---: | ---: |
| $\lambda=.5$ | .630435 | .716667 |
| $\lambda=1$ | .716667 | .716667 |
| $\lambda=2$ | .806818 | .716667 |
| $\lambda=2.5$ | .833333 | .716667 |

Thus, at $\lambda=2$, objective authenticity and transformed-reward masking
are favoured on opposite sides of the comparison throughout
$.716667<p<.806818$. This is an exact valuation result, not an equation for
the finite learner's final action frequency.

In the archived maintained-baseline contrast at $p=.65$, changing
$\lambda=.5$ to $2.5$ increased final-window masking from 58.89% to 99.19%.
The increase was 40.30 percentage points (95% CI 39.54–41.06).
These levels are equal-weight means of five archived master-cell means; the
interval is the archived master-level contrast. The environment was unchanged.
This secondary weighting result supports Claims C01–C02 and Figure 2.

### S2.3 History conditioning and estimands

Every learner's step-0 action was forced to authenticity. Learners were then
stratified by the accepted or rejected outcome of that action. The primary
sampling estimand was the rejected-minus-accepted difference in authentic
action rate over steps 1 through $T-1$, equally pooled over $p=.75$ and $.85$
within master. It was not a pairing of learners across outcome strata.

In authenticity-optimal binary cells, normalized objective pseudo-regret is
the horizon-average gap from the optimal action divided by the authentic-minus-
mask expected-reward gap. Consequently,

$$
\Delta\overline{\mathrm{Regret}}_{\mathrm{norm}}
=-\frac{T-1}{T}\Delta\bar A_{1:T-1}.
$$

The factor is $1999/2000$ because every learner's initial action was authentic.
The regret contrast expresses the objective cost of the same action allocation.

Initial rejection reduced subsequent authentic sampling by .025837
(95% CI .015922–.035753), or 2.58 percentage points. The corresponding
increase in normalized pseudo-regret was .025824 [.015914, .035735].
The secondary rejected-minus-accepted final-window masking contrast was
−.000343 [−.011605, .010918]. The supported history result therefore concerns
subsequent sampling over the specified horizon (C03).

### S2.4 Information manipulations and their results

The controlled baseline supplied feedback only for the chosen action. In the
forced-authentic condition, 5% of post-initial choices were replaced by an
authentic action using a separate intervention stream. In the counterfactual
condition, a masking trial also supplied the authentic outcome that would have
occurred, using the same latent acceptance draw. Counterfactual feedback updated
information about authenticity but did not credit an unchosen reward to realized
objective return. The comparisons below condition on initial rejection and
equally pool $p=.75/.85$ within master.

| Information manipulation | Reduction in final masking, percentage points [95% CI] | Reduction in normalized objective regret [95% CI] |
| --- | ---: | ---: |
| Forced authentic exposure, 5% | 4.66 [3.32, 6.00] | .057954 [.045614, .070293] |
| Counterfactual authentic feedback | 11.81 [10.97, 12.66] | .141318 [.132369, .150267] |

These archived intervention outcomes establish information access as a model
lever with environmental payoffs fixed (C04). At the specified intensities,
the counterfactual treatment produced approximately 2.54 times the final-mask
reduction of forced exposure (.118135/.046590; C05). This descriptive ratio
has no estimated confidence interval and compares two different information
protocols, not equal-cost treatments.

### S2.5 Design, inference, and source selectors

E01 used master seeds 2026081101–2026081105. Controlled history comparisons
used $n=500$, $T=2000$, and $p\in\{.75,.85\}$. The 95% interval for five
master-level effects was

$$
\bar\theta\pm t_{.975,4}\frac{s_\theta}{\sqrt5},
\qquad t_{.975,4}=2.776445.
$$

The maintained weighting contrast used $p=.65$; separate controlled cells
also compared $\lambda=.5/2.5$ at $p=.75$. No E01 horizon or learning-rate
sweep was executed. Restoring the weighting and intervention results to the
main narrative does not change their archived secondary status.

Sources are `frontiers_hot_stove_v1_cells.csv` and
`frontiers_hot_stove_v1_effects.csv` under `results/summaries/`. History and
intervention selectors use `level=across_master_seeds` and
`p=pooled_equal_weight_p_0.75_0.85`, with the named condition and rejected
stratum where applicable. The weighting effect is
`maintained_p_0.65_lambda_2.5_minus_0.5_final_mask_rate`. Equations are also
recorded in `ARTICLE_V1_ANALYTIC_RESULTS.md`, Sections 3.4–3.6.

## S3. E02 — graded action representation

### S3.1 Choice sets and unchanged objective optimum

The binary architecture used $d\in\{0,1\}$, and the graded architecture used
$d\in\{0,.25,.5,.75,1\}$. Experience updated only the selected level; it did
not generalize to neighbouring levels. Acceptance probability was
$1-(1-p)d$. Therefore,

$$
\mathbb E[R(d)]
=ad-c(1-d)+b\{1-(1-p)d\}-r(1-p)d
=b-c+d\Delta_0(p).
$$

At the reference values, $\mathbb E[R(d)]=.75+d(3p-2.15)$. Every grid
containing 0 and 1 has the same maximum expected reward and objective boundary:
full authenticity is optimal above $43/60$, masking below, and all levels tie
at equality. Adding intermediate levels changes the learning problem while
preserving the optimum (C07).

### S3.2 Rejection exposure and reward variance

For a fixed level, the two realized rewards differ by $b+r$. Consequently,

$$
\Pr(\mathrm{rejection}\mid d)=(1-p)d,
\qquad
\operatorname{Var}[R(d)]=(b+r)^2(1-p)d[1-(1-p)d].
$$

For the authenticity-optimal comparisons at $p=.75/.85$, both rejection
probability and variance increase with $d$ on $[0,1]$. At $p=.75$, $d=.5$
has expected reward .80 and variance .984375, whereas $d=1$ has expected
reward .85 and variance 1.6875. Partial disclosure therefore offers lower
exposure and variance at a cost in expected reward (C08). This characterizes
the available outcomes; the learner has no separately fitted variance-preference
parameter.

### S3.3 Conditioning, measures, and pairing

E02 used $p\in\{.65,.75,.85\}$, $n=500$, $T=2000$, and master seeds
2026081201–2026081205. The first action was full authenticity. Main contrasts
used the rejected-initial-outcome stratum at $p=.75/.85$, equally pooled
within master. The $p=.65$ cells were maintained controls.

The measures distinguish post-initial nonzero disclosure, final-window full-
authentic frequency, unique modal full authenticity, and mean disclosure
intensity. Unique-modal classification requires $d=1$ to have a strictly
larger final-window count than every alternative. In authenticity-optimal
cells, normalized pseudo-regret is exactly

$$
\overline{\mathrm{Regret}}_{\mathrm{norm}}
=\frac1T\sum_{t=0}^{T-1}(1-d_t)=1-\bar d_{0:T-1}.
$$

This full-horizon intensity identity differs from final-window mean disclosure.

Binary and graded learners were reinitialized from the same policy/environment
stream within master and receptivity. Latent uniform sequences and child IDs
were matched within those pairs, not across receptivity values or masters.
Intervals used the five master-level paired architecture effects.

### S3.4 Engagement, intensity, and endpoint results

| Graded minus binary outcome | Estimate [95% CI] | Measurement window |
| --- | ---: | --- |
| Nonzero disclosure | +25.50 percentage points [25.30, 25.71] | Steps 1–1999 |
| Full-authentic action frequency | −32.87 percentage points [−34.20, −31.53] | Final 400 steps |
| Unique full-authentic modal classification | −22.17 percentage points [−28.88, −15.47] | Final 400 steps |
| Mean disclosure intensity | −.032088 [−.038941, −.025236] | Final 400 steps |
| Normalized objective regret | +.029761 [.025648, .033874] | Full 2000 steps |
| Mean disclosure intensity, equivalent regret translation | −.029761 [−.033874, −.025648] | Full 2000 steps |

The last two rows are one result in two units, not independent observations.
The archive records the regret contrast as binary minus graded; the table
reverses its sign and interval endpoints to align the direction with the other
rows. These outcomes show that the graded representation sustains engagement
while lowering intensity and full-endpoint use, with the optimum held fixed
(C06; Figure 3).

Sources are `frontiers_m1_binary_graded_v1_effects.csv` and the corresponding
cells/arms tables. Select `level=across_master_seeds`,
`p=pooled_equal_weight_p_0.75_0.85`, and `stratum=rejected`. The direct
final-window intensity effect is
`graded_minus_binary_final_window_mean_disclosure`. Three- and nine-level
graded sensitivity conditions were planned but not executed.

## S4. E03 — persistent social state and dynamic optimality

### S4.1 State and transition kernel

M2 used Neutral ($N$), Accepted ($A$), and Stigmatized ($S$) states. Reward
was realized before transition. The reference kernel was:

| Current state | Action/outcome | Reward | Next state |
| --- | --- | ---: | --- |
| $N$ | Mask | $b-c$ | $N$ |
| $N$ | Authentic, accepted with $p$ | $b+a$ | $A$ |
| $N$ | Authentic, rejected with $1-p$ | $a-r$ | $S$ |
| $A$ | Mask | $b-c$ | $N$ with $\delta$, else $A$ |
| $A$ | Authentic | $b+a$ | $N$ with $\delta$, else $A$ |
| $S$ | Mask | $b_2-c$ | $N$ with $\eta$, else $S$ |
| $S$ | Authentic, redeemed with $p/2$ | $b+a$ | $A$ |
| $S$ | Authentic, not redeemed | $a-r_2$ | $N$ with $\eta$, else $S$ |

Reference values were $b_2=.5$, $r_2=2.5$, $\delta=.02$. Escape occurred
after reward on non-redeemed Stigmatized transitions. Neutral masking retained
Neutral; it did not reset stigma elsewhere.

### S4.2 Learning and exact value decompositions

The state-action learner used $\gamma=.9$ and

$$
Q_{t+1}(s_t,x_t)=Q_t(s_t,x_t)+\alpha[
v_\lambda(R_t)+\gamma\max_{x'}Q_t(s_{t+1},x')-Q_t(s_t,x_t)].
$$

Unselected state-action values were unchanged. For continuation values $V$,
the Neutral authentic-minus-mask advantage is

$$
D_N(V)=\Delta_0(p)+\gamma\{pV_A+(1-p)V_S-V_N\}.
$$

In Accepted, both actions have identical transitions. Their continuation
terms cancel, leaving an authenticity advantage $a+c=.85$ for any $V$.
Authenticity thus strictly dominates masking there. In Stigmatized, immediate
expected authenticity is $-1.9+1.75p$, always below the masking payoff .25
on $p\in[0,1]$. Whenever authenticity is dynamically optimal in Stigmatized,
its future redemption value supplies that advantage (C11).

### S4.3 Oracle and threshold computation

The oracle used known transitions and untransformed environmental reward:

$$
Q^V(s,x)=\sum_{s'}P(s'\mid s,x)
\{r(s,x,s')+\gamma V(s')\},\qquad
(\mathcal TV)(s)=\max_x Q^V(s,x).
$$

Starting at $V_0=0$, value iteration stopped when
$\max_s|V_{k+1}(s)-V_k(s)|<10^{-10}$, with a fail-closed maximum of
100,000 iterations and objective action-tie tolerance $10^{-10}$.
An independent four-policy evaluation, using Accepted-state dominance to
fix that action, checked the envelope over all 357 baseline grid cells;
maximum discrepancy from value iteration was $8.99\times10^{-10}$.
The benchmark is full-information, infinite-horizon, and discounted.

Archived bisection brackets locate the Neutral-state objective switch:

| Escape $\eta$ | Lower receptivity | Upper receptivity | Midpoint | Reduction from static $43/60$ |
| ---: | ---: | ---: | ---: | ---: |
| 0 | .383911133 | .383972168 | .383941650 | .332725 |
| .2 | .338745117 | .338806152 | .338775635 | .377891 |
| .8 | .268981934 | .269042969 | .269012451 | .447654 |

Each numerical bracket has width .0000610352; these are numerical-resolution
brackets, not Monte Carlo confidence intervals. Persistent social state
therefore relocates the objective threshold substantially (C09). Raising
escape from 0 to .8 lowers its midpoint by .114929, showing that recoverability
changes objective incentives, not only learned beliefs (C10; Figure 4).

### S4.4 Immediate and dynamic ranking reversals

| Setting | Immediate authentic-minus-mask advantage | Optimal dynamic Neutral Q advantage | Optimal Neutral action |
| --- | ---: | ---: | --- |
| Reference kernel, $p=.4$, $\eta=0$ | −.950000 | +.042943 | Authentic |
| Harsh sentinel, $p=.75$, $\eta=0$ | +.100000 | −.406293 | Mask |

In the first setting, immediate authenticity pays −.20 in expectation against
masking's +.75, yet its future-state return makes it dynamically optimal. The
harsh kernel used $b_2=0$, $r_2=8$, $\delta=.3$, and $\gamma=.9$; its
adverse persistence reverses an immediate authenticity advantage. These
verified examples establish both directions of reversal (C12). Harsh archived
cells additionally used $p=.70$ and $.80$.

### S4.5 Grid, behavioural classifier, and replication

The baseline grid crossed $p\in\{0,.05,\ldots,1\}$ with
$\eta\in\{0,.05,\ldots,.8\}$, producing 357 cells. Each cell used 160
learners, 1000 steps, and masters 2026081301–2026081305. Final-window Neutral
counts were aggregated across learners. Exposure was adequate with at least
160 Neutral visits and at least 32 visiting learners. Equal mask/authentic
counts or inadequate exposure produced an inconclusive learned action.

The `learned_suboptimal_masking` label required adequate exposure, aggregate
Neutral masking preference, and an oracle Neutral authenticity preference.
The same 243 cells satisfied it in all five masters (C13). These are
objectively suboptimal action allocations relative to the stated dynamic
benchmark. The remaining publication categories were 107 agreement cells
and seven inconclusive cells. Overall, 350/357 cells met the four-of-five
non-inconclusive stability rule.

Five of the seven inconclusive cells had inadequate Neutral exposure in every
master. At $p=.25$ and $.30$ with $\eta=0$, respectively one and two masters
had adequate exposure and agreement, below the stability criterion. The count
243/357 describes tested parameter cells, not a population prevalence or
individual learned-$Q$ ordering.

### S4.6 Five disagreement sentinels and extended-horizon persistence

Six prespecified sentinels were archived: $(p,\eta)=(.35,0),(.4,0),(.55,0),
(.75,0),(.55,.2),(.9,.2)$. The first is a boundary/agreement control under
the reference kernel. The other five define the baseline-disagreement set
used for the persistence claim.

| Disagreement sentinel $(p,\eta)$ | Mean Neutral masking at $T=5000$ | Masters retaining suboptimal-mask classification |
| --- | ---: | ---: |
| $(.4,0)$ | 99.67% | 5/5 |
| $(.55,0)$ | 98.22% | 5/5 |
| $(.75,0)$ | 95.42% | 5/5 |
| $(.55,.2)$ | 97.12% | 5/5 |
| $(.9,.2)$ | 89.97% | 5/5 |

The percentages are equal-weight means of the five master-level aggregate
Neutral masking fractions, not whole-population masking at every state. All
five settings have an authentic dynamic optimum. Their retained classification
through 5000 steps supports C14 and Figure 4.

### S4.7 Separately executed sensitivity settings

Each row below changed one listed factor from the reference configuration.
The denominator is five disagreement sentinels times five masters. Counts are
deterministic summaries of archived classifications, not new inferential tests.

| Changed factor | Executed value | Suboptimal-mask cell-master classifications | Other classifications among the 25 |
| --- | ---: | ---: | --- |
| None: baseline | Reference | 25/25 | None |
| Horizon $T$ | 2000 | 25/25 | None |
| Horizon $T$ | 5000 | 25/25 | None |
| Learners $n$ | 320 | 25/25 | None |
| Final-window fraction | .1 | 25/25 | None |
| Final-window fraction | .4 | 25/25 | None |
| Negative-outcome weight $\lambda$ | .5 | 25/25 | None |
| Negative-outcome weight $\lambda$ | 2.5 | 25/25 | None |
| Initial value $q_0$ | .75 | 25/25 | None |
| Learning rate $\alpha$ | .03 | 18/25 | 7 oracle agreements |
| Learning rate $\alpha$ | .3 | 25/25 | None |
| Temperature $\tau$ | .1 | 25/25 | None |
| Temperature $\tau$ | .6 | 21/25 | 4 oracle agreements |
| Discount $\gamma$ | .5 | 10/25 | 15 oracle agreements |
| Discount $\gamma$ | .99 | 25/25 | None |

Horizon, population, window, weighting, and initialization changes each
retained the gap throughout the five-sentinel set. The additional learning-rate,
temperature, and discount checks identify settings that alter the outcome.
Changing $\gamma$ also changes the full-information objective itself.
These are separately executed perturbations, not a joint factorial robustness
claim. For the sixth sentinel, changing $\gamma$ to .99 changes its reference
agreement into learned suboptimal masking; it is not included in the table's
five-sentinel denominator.

The source is `frontiers_m2_regime_replication_v1_cells.csv`, selected by
`component=sentinels`, `sensitivity_name`, and the named parameter value.
Grid, harsh, and threshold results respectively use `component=exact_grid`,
`component=harsh`, and `frontiers_m2_regime_replication_v1_thresholds.csv`
with `threshold_kind=objective_dynamic_authenticity`. The publication table
`publication_v1/data/e03_objective_thresholds.csv` carries the same objective
threshold evidence. Learned-boundary searches were censored; they do not
supply a measured learned threshold to pair with the objective brackets.

## S5. E04 — contextual representation, encounter, and sustained use

### S5.1 Environmental classes and action indexing

M3 contained $K$ contexts. The one-good-context design used
$p_{\mathrm{good}}=.85$ and $p_{\mathrm{bad}}=.20$ elsewhere. Context indices
were zero based; joint index $2g$ denoted masking in context $g$ and $2g+1$
authenticity there. At comparison cost $b_f=0$, expected rewards were

$$
R_M=.75,\qquad R_G=1.15,\qquad R_B=-.80.
$$

Increasing $K$ with one receptive context added copies of mask and bad-context
reward classes while preserving the best full-information opportunity.

### S5.2 Four action representations

| Architecture | Choice and update |
| --- | --- |
| `flat_2k` | One softmax over $2K$ joint context–behaviour arms; update only the selected arm. |
| `hierarchical` | Context softmax followed by within-context behaviour softmax; update the selected context value and selected within-context behaviour value from the same reward. |
| `global_mask` | One shared mask arm and $K$ context-specific authentic arms; update only the selected arm. |
| `fixed_known_good` | Two actions in a known good context; structurally invariant to requested $K$. |

All used the reference learner settings. Acceptance uniforms were consumed
on every trial in the maintained random-number order.

### S5.3 Design, canonicalization, and primary classifier

The requested design crossed four architectures, $K\in\{1,2,4,8,16\}$,
fixed/random-per-learner good-context identity, and one, two, or proportional-
25%-good-context regimes. Equivalent requests were canonicalized: 120
requested rows mapped to 55 executable cells. Each executable cell used
$n=500$, $T=2000$, and masters 2026081401–2026081405.

For each learner, deterministic NumPy first-index `argmax` of final-window
joint-action counts selected one indexed arm. The primary indicator was one
if that arm was authentic in a good context. Ties remained eligible but
resolved to the first indexed maximum. This is not an any-tied-good-maximum
rule. A separate strict unique-mode diagnostic retained the direction of the
primary flat and hierarchical contrasts without replacing their estimator.

### S5.4 Secondary behavioural and performance measures

Total final-window masking is the fraction of final-window actions that mask,
summed over mask arms where context-specific masks exist. Ever accepted
good authenticity is a learner indicator for at least one such successful
action over all 2000 steps. Capped first-success time is the zero-based index
of that first accepted good-authentic action, or 2000 if no event occurred.
The mean combines event times and horizon-coded non-events.

Expected static regret per step is

$$
\frac1T\sum_{t=0}^{T-1}
\{\max_x\mathbb E[R_x]-\mathbb E[R_{x_t}]\}.
$$

It uses exact objective action gaps over the full trajectory, unlike noisy
realized reward or a final-window endpoint. A successful encounter indicates
experience of acceptance at least once, not verified knowledge of the entire
reward distribution.

### S5.5 Representation-dependent context expansion

The following levels are equal-weight means of five archived master cells
with fixed identity and one good context. Intervals are archived K16-minus-K1
master-level effects.

| Architecture | Masking at $K=1$ | Masking at $K=16$ | Change in masking, percentage points [95% CI] | Good-authentic modal classification, $K=1\to16$ |
| --- | ---: | ---: | ---: | ---: |
| Flat | 26.36% | 84.19% | +57.83 [57.43, 58.22] | 98.88% $\to$ 75.48% |
| Hierarchical | 26.45% | 87.27% | +60.82 [60.21, 61.42] | 99.04% $\to$ 52.00% |
| Global mask | 27.23% | 25.77% | −1.46 [−2.29, −.62] | 98.16% $\to$ 99.04% |

The primary modal declines were 23.40 points [22.16, 24.64] for flat and
47.04 [42.98, 51.10] for hierarchical. The global-mask modal contrast was
+.88 points [.209, 1.551], and fixed-known-good was structurally invariant.
Randomizing good-context identity retained the primary declines. These
controls identify a representation-dependent response to the same expansion,
while the best expected reward remains 1.15 (C15–C16; Figure 5).

### S5.6 Successful encounter, later allocation, and search costs

| Architecture | Ever accepted good authenticity at $K=16$ | Final masking at $K=16$ | Increase in capped first-success time, steps [95% CI] | Increase in expected regret per step [95% CI] |
| --- | ---: | ---: | ---: | ---: |
| Flat | 99.72% | 84.19% | 72.11 [64.96, 79.27] | .287739 [.286203, .289275] |
| Hierarchical | 99.64% | 87.27% | 71.15 [66.65, 75.66] | .280625 [.279390, .281859] |
| Global mask | 100.00% | 25.77% | 16.16 [14.49, 17.83] | .121423 [.119686, .123159] |

The increases compare $K=16$ with $K=1$. Near-universal successful encounter
coexists with extensive subsequent masking in the flat and hierarchical
architectures (C17). Global-mask preserves high good-authentic modal selection
yet still incurs delay and accumulated objective cost (C18). These archived
secondary outcomes distinguish encounter, sustained allocation, and performance.

### S5.7 Receptive-context abundance and inference

At $K=16$, increasing receptive contexts from one to four raised good-authentic
modal selection from 75.48% to 99.36% in flat and 52.00% to 95.80% in
hierarchical (C19). These descriptive endpoints accompany the adjudicated
proportional-abundance slope contrasts: +.060440 [.055044, .065836] for flat
and +.112240 [.104787, .119693] for hierarchical per $\log_2 K$ relative
to the one-good regime. Slope differences and endpoint percentage-point
differences are different estimands.

Architecture effects and K slopes were reduced within master before applying
the five-master Student-$t$ interval. Learners and K cells were not additional
top-level replicates. Sources are `frontiers_m3_search_architectures_v1_curves.csv`,
`frontiers_m3_search_architectures_v1_effects.csv`, and the equivalence table.
Level selectors use the named architecture, `canonical_identity_mode=fixed`,
K=1/16, and `effective_good_count=1` (or 4 for the abundance endpoint).
Complete K curves, identity controls, two-good controls, and strict-mode
diagnostics remain archived. Planned $p_{\mathrm{good}}$, $p_{\mathrm{bad}}$,
and temperature sensitivity was not executed.

## S6. E05 — learned modal and environmental boundaries

### S6.1 Global objective switch

E05 fixed $K=4$, good context at index 0, $p_{\mathrm{good}}=.85$, and
$p_{\mathrm{bad}}=.20$. Comparison cost $b_f$ was subtracted only from the
accepted good-authentic reward, which is $1.6-b_f$. The expected rewards are

$$
R_M=.75,\qquad
R_G(b_f)=.85(1.6-b_f)+.15(-1.4)=1.15-.85b_f,\qquad
R_B=-.80.
$$

Thus $R_G-R_M=.40-.85b_f$, and objective indifference is at
$b_f^*=8/17=.470588\ldots$. Good authenticity is the unique optimum below
this value, mask actions are optimal above it, and they tie at equality.
The bad-authentic alternatives never exceed masking. This is the global
objective switch, not merely an incomplete pairwise comparison (C20).

### S6.2 Design and modal-population response

Flat eight-action and hierarchical representations were evaluated separately.
The complete cost grid was

$$
\{0,.30,.325,.35,.375,.40,.425,.45,8/17,.475,
.50,.525,.55,.575,.60,.625,.65,.80\}.
$$

Each cell used 500 learners, 2000 steps, the final 400-step window, and masters
2026081501–2026081505, with $\lambda=1$. The learned response was the
fraction of learners whose deterministic first-index final-window `argmax`
selected the single good-authentic arm. The response is a population
classification fraction, not a binary choice probability.

Within architecture and master, the same policy/environment stream was
reinitialized across costs to provide common-random-number pairing. Flat and
hierarchical architectures used separate stream families.

### S6.3 PAVA inversion and complete-curve bootstrap

The 16 points inside $[.30,.65]$, including $8/17$, formed the dense crossing
grid; costs 0 and .80 were external endpoint diagnostics. Five master responses
were averaged equally at each cost. A non-increasing, equal-weight
pool-adjacent-violators fit was applied (Best & Chakravarti, 1990). If a fitted
plateau equalled .5, the crossing was its cost-range midpoint; otherwise
adjacent fitted values bracketing .5 were linearly interpolated. A valid
crossing had to lie strictly inside $(.30,.65)$; no extrapolation was used.

The archived interval used 10,000 bootstrap samples of five complete master
curves, sampled with replacement, then averaged, refitted, and reinverted.
Percentile limits were reported only with at least 95% valid crossings.
All 10,000 flat samples were valid. Hierarchical response was already below
.5 at .30: zero bootstrap samples yielded in-range crossings, and the result
was left-censored below the resolved range, not evidence that no crossing
exists at any cost. The bootstrap unit was the complete master curve.

### S6.4 Boundary displacement and actual masking

The flat modal-classification crossing was .312852 (95% bootstrap CI
.307836–.316918), .157736 below objective indifference. At that crossing,
good authenticity retained objective advantage .134076; transforming the
crossing interval gives advantage bounds .130620–.138340. The result occurs
at loss-neutral $\lambda=1$ (C21; Figure 6).

| Comparison cost $b_f$ | Good-authentic modal fraction | Total final-window masking | Objective good-authentic advantage |
| ---: | ---: | ---: | ---: |
| 0 | .9400 | 58.82% | .40000 |
| .30 | .5292 | 77.61% | .14500 |
| .325 | .4724 | 78.95% | .12375 |
| $8/17$ | .1416 | 85.20% | 0 |

Entries are equal-weight descriptive means of five flat master cells. Masking
increases as comparison cost rises while good authenticity still has an
objective advantage (C22). Because four mask arms contribute to total masking,
one good-authentic arm can be the most frequent individual arm even when
masking dominates in aggregate. The modal curve's .5 crossing is therefore
not a 50% masking-rate threshold.

Sources are `frontiers_m3_bflpe_crossover_v1_cells.csv` (flat architecture and
the listed costs), the analytic table, and
`frontiers_m3_bflpe_crossover_v1_transitions.csv`. The archived strict unique-mode
diagnostic remains separate from the maintained estimator. A longer-horizon
crossing analysis was planned but not executed.

## S7. Randomization, seed hierarchy, and inferential units

### S7.1 Master lists and semantic streams

| Experiment | Master seeds |
| --- | --- |
| E01 | 2026081101–2026081105 |
| E02 | 2026081201–2026081205 |
| E03 | 2026081301–2026081305 |
| E04 | 2026081401–2026081405 |
| E05 | 2026081501–2026081505 |

Semantic cell/family identifiers were SHA-256 hashed. The first four
little-endian 32-bit digest words entered NumPy `SeedSequence` with the master
and experiment namespace. In the table, `*words` expands that four-word
sequence into the entropy list.

| Experiment | Archived construction |
| --- | --- |
| E01 | `SeedSequence([master, 1, *words]).spawn(2)`; separate policy/environment and intervention streams |
| E02 | `SeedSequence([master, 2, *words]).spawn(1)`; matched binary/graded pair |
| E03 | `SeedSequence([master, 3, *words]).spawn(1)`; approved horizon/window sentinels alone shared trajectory-prefix families |
| E04 | `SeedSequence([master, 4, *words]).spawn(1)` for policy/environment; independent `SeedSequence([master, 40, *words]).spawn(1)` for identity |
| E05 | `SeedSequence([master, 5, *words]).spawn(1)`, reinitialized across cost within architecture/master; bootstrap `SeedSequence([2026081597, 50, architecture code])` |

Child draws were vectorized within cell/family streams. Child IDs were not
additional top-level inferential replicates. E01 outcome strata were disjoint,
not paired learners. E02 paired architectures within master/receptivity; E04
reduced architecture/K effects within master; E05 resampled whole master curves.

### S7.2 Interval and replication interpretation

Student-$t$ intervals in E01, E02, and E04 use five master-level estimates
(df=4). E05 scalar endpoint effects use the same convention; its crossing
uses the complete-curve bootstrap. Secondary-outcome intervals are pointwise,
not simultaneous. Descriptive levels calculated as equal-weight means are
identified as such; the revision did not generate new uncertainty estimates.

The E03 grid fraction's equality across the five masters documents stability
over those streams, not zero model uncertainty. Sentinel classification counts
summarize the executed perturbations. Fixed master lists were not sampled
from a documented population of seeds. Numerical objective threshold brackets
describe solver resolution, whereas simulation intervals describe between-
master variation.

## S8. Evidence status, sensitivity coverage, and synthesis

### S8.1 Status of the restored scientific content

| Experiment | Primary/adjudicated structure | Restored or expanded supporting content |
| --- | --- | --- |
| E01 | Rejected-versus-accepted subsequent sampling | Secondary weighting and information outcomes; exact transformed threshold; objective cost translation (C01–C05) |
| E02 | Paired binary/graded action-representation contrasts | Secondary intensity and regret outcomes; exact unchanged optimum and mean–variance geometry (C06–C08) |
| E03 | Fixed-grid learner/oracle classification | Deterministic dynamic thresholds and reversal examples; exact state decompositions; archived separate sentinel sensitivities (C09–C14) |
| E04 | Context-architecture modal contrasts, identity and abundance controls | Secondary masking, ever-success, capped timing, and objective-regret outcomes; descriptive abundance endpoint levels (C15–C19) |
| E05 | Flat modal-population crossing and hierarchical censoring | Exact global objective crossover; secondary descriptive total-masking levels alongside modal fractions (C20–C22) |

The editorial prominence of a result does not change its original primary or
secondary status. Exact implications can be stated directly; archived secondary
outcomes retain their selectors and definitions. Figure panels label each
quantity's denominator, measurement window, and descriptive or inferential
status. Sharing an axis where units permit comparison does not imply a shared
estimand or a ranking of efficacy across different mechanisms.

### S8.2 Mechanistic synthesis and its empirical interpretation

Environmental payoffs, feedback history, outcome weighting, information access,
action representation, persistent state, and context composition provide distinct
modelled sources of concealment variation (C23). E01, E02, and E04 demonstrate
behavioural changes with relevant objective opportunities fixed; E03 changes
the dynamic opportunity itself; E05 resolves the separation between an objective
switch and an acquired population response. This is the synthesis represented
in Figure 1.

The model-derived empirical targets follow these distinctions: measure expected
social responses separately from actual responses; distinguish initial
successful exposure from repeated use; record disclosure frequency and
intensity separately; examine whether experience generalizes across disclosure
levels; measure the duration and recoverability of adverse standing; and
distinguish receptive-context abundance from the mere existence of one receptive
setting. These are proposed tests of the mechanisms, not additional empirical
findings about children.

### S8.3 Executed and unexecuted sensitivity boundaries

E03's executed settings are enumerated in S4.7, including settings that alter
classification. E04 includes the four representations, fixed/random identity,
and one/two/proportional-good regimes. E05 includes five master curves,
strict-mode diagnostics, the archived flat bootstrap, and hierarchical
censoring. E01 horizon/learning-rate sweeps, E02 alternative grid cardinalities,
E04 receptivity/temperature sweeps, and E05 longer-horizon crossings were not
executed. No such unexecuted condition is used as support for the revised claims.

## S9. Evidence provenance and reproduction

### S9.1 Three distinct provenance claims

The evidence package distinguishes:

1. `ARTIFACT_VERIFIED`: outputs byte-match archived manifest/evidence hashes.
2. `CURRENT_IMPLEMENTATION_REPRODUCIBLE`: a maintained procedure can be run
   from current code, where separately authorized.
3. `HISTORICAL_BIT_REPRODUCTION_VERIFIED`: the exact historical source state
   and outputs can be reconstructed.

All 33 protected E01–E05 outputs are artifact-verified in the existing
verification record. Fingerprint-exact historical generator-source bundles
are retained for E04 and E05. E01–E03 retain status
`HISTORICAL_SOURCE_STATE_UNRECOVERED`: their claims are governed by archived
outputs, hashes, configurations, and verification records, not an assertion
of bit-identical regeneration from current code. This limits source-level
historical reconstruction; it does not imply that the archived artifacts changed.

### S9.2 Archived summary-artifact identities

| Experiment/artifact | SHA-256 |
| --- | --- |
| E01 effects | 4ce67da8b48e8d770388db9e2c6ebe240b868c0696ba90678cc9940de02684d8 |
| E02 effects | 11d29c72508649a174b285957dfec3752edff76a099aa76de9f6fe3a4e515a8a |
| E03 effects | 5a1ee392560e94695dfe0d04ff89caeafdb0b58fa2b70e6def365726d66ab3af |
| E03 stable cells | 91814ab4430f63bc5e46596c61718e1fec6705d355b6cab3d8c18d29c1dfaea7 |
| E03 thresholds | 0987aea9f6085f81bad791454eaca03127c6144f172a7cc9f41cdad6c316f9bf |
| E03 cells | 198cb7be9b2a93aa89569d9dd656326f521b7a2ec99543733fd6e779e0508851 |
| E04 effects | dd426992f0a1a0ae05542756dc6dca918fbf56a589347676a93a309d08a41d44 |
| E05 analytic | e1045d0593709561761ec8c9ba0684ef1a80e26d6b0b15f12f57434b74f22a42 |
| E05 transitions | 96b8d8dc1cf27e3a226282e4d8755effde74e855d81b8f8bbc6db6515c607097 |
| E05 effects | 33eb752c89d87ce79ef13bfe196623fb4d4f53c4fff63e03b84af413a68200d5 |

The five standard manifests under `results/manifests/` retain normalized
configuration, exact parameters, seed hierarchy, environment versions, output
paths/hashes, timestamps, and source fingerprints. Recorded execution used
Python 3.14.6 on macOS arm64 and NumPy 2.4.6; E01, E02, E04, and E05 also
recorded Matplotlib 3.10.8.

### S9.3 Validation and deterministic presentation

Read-only artifact validation loads manifests and the evidence matrix and
rehashes declared outputs without simulation. Revised figures deterministically
select and aggregate pinned result tables; presentation reproduction is distinct
from experiment reproduction. The revision's figure-provenance record identifies
the source paths and hashes for the new six-figure display layer.

Retained publication-source identities include `e01_primary_effects.csv`
(9b9227f43146b96ae7000f572d2249ae6bd4d39bf414715bdd780203afa38d36),
`e03_grid_map.csv`
(c5def710116248b60ffcc347fa408519ce5d9094547e486fc73f2388e5babbab),
`e04_k_response.csv`
(c01c04359b30d425d518566190dcfb27b10f9003e4123d9a6f05ce44382c11b7),
and `e05_crossings.csv`
(866697afb0cdd66f6e6d008cc6b06e52786d1e27f7ba3f71601a56512349076b).

The earlier manuscript, supplement, and submission package remain preserved.
This separately identified revision changes exposition and deterministic
displays, not model semantics, parameters, seed rules, or frozen evidence.

## S10. Figure, table, and claim inventory

### S10.1 Main-article figure mapping

| Figure | Content | Supplement home | Claims |
| --- | --- | --- | --- |
| 1 | Conceptual distinction among objective opportunity, information/valuation, and acquired behaviour | S1, S8.2 | C23 synthesis |
| 2 | Negative-outcome weighting, feedback history, and information manipulations | S2 | C01–C05 |
| 3 | Graded engagement, intensity, endpoint use, and objective geometry | S3 | C06–C08 |
| 4 | Dynamic thresholds and five $T=5000$ disagreement sentinels | S4.3–S4.7 | C09–C14 |
| 5 | Context representation, masking, successful encounter, and receptive abundance | S5 | C15–C19 |
| 6 | Objective versus modal-population boundary and actual masking | S6 | C20–C22 |

Each figure groups related outcomes without treating their different scales
as commensurate intervention effects. The former cross-estimand synthesis
display is not reused; revised Figure 6 specifically concerns E05.

### S10.2 Supporting tables and archived diagnostics

The tables embedded here provide common settings (S1.3–S1.4), subjective
thresholds and intervention effects (S2.2/S2.4), graded outcome contrasts
(S3.4), objective threshold brackets and ranking reversals (S4.3–S4.4),
extended-horizon sentinel levels and all separately executed sensitivities
(S4.6–S4.7), context outcomes and search costs (S5.5–S5.6), paired modal and
masking rates (S6.4), seed construction (S7.1), and provenance hashes (S9.2).

Additional archived diagnostics include E01 master-specific/stratum cells;
E02 arm and endpoint summaries; E03 full-grid stability and seven inconclusive
cells; E04 complete K curves, identity/abundance controls, equivalence mapping,
and strict tie diagnostic; and E05 master curves, pooled fit, bootstrap-validity
records, endpoint effects, and strict-mode diagnostic. These remain available
from the source artifacts identified in each experiment section.

## Supplement reference

Best, M. J., & Chakravarti, N. (1990). Active set algorithms for isotonic
regression: A unifying framework. *Mathematical Programming, 47*(1–3),
425–439. https://doi.org/10.1007/BF01580873
