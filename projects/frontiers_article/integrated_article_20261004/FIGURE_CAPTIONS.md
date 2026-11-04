# Integrated article figure captions

Ten figures combine six archived-evidence displays with four additional diagrams
and deterministic summaries. No simulation, model fit, bootstrap refit, or new
uncertainty estimate was performed. Each figure is exported as PNG for article
embedding and SVG for vector editing. Source selectors and hashes are recorded
in `FIGURE_PROVENANCE.json`. Visible text lives in `figure_text.py`.

## Figure 1. Learning mechanisms and the use of receptive opportunity.

**(A)** Valuation and feedback history (E01), action representation (E02), and
persistent social consequences (E03) shape learned values and action allocation.
Engagement, expression intensity, and concealment are distinct outcomes. E05
compares a learned modal-population crossing with objective indifference.
**(B)** A receptive option being available, accepted authenticity being
encountered, and the option being used repeatedly are different achievements.
E04 varies action/context representation and receptive-context abundance to
separate these outcomes. The diagram is a conceptual synthesis, not a fitted
causal model or a quantitative result about children.

## Figure 2. Social states change rewards and future opportunity.

The M2 kernel contains Neutral (N), Accepted (A), and Stigmatized (S) states.
Each card follows an action from its current state through realized reward
to next state. Neutral masking remains Neutral. Authenticity from Neutral
reaches Accepted with probability p and Stigmatized otherwise. In Accepted,
both actions share the same turnover transition, but authenticity pays b+a
rather than b-c; its immediate advantage is a+c=.85. In Stigmatized,
authenticity redeems to Accepted with probability p/2. Masking and
non-redeemed authenticity return to Neutral with escape probability eta;
otherwise they retain Stigmatized. Reward is realized before the displayed
transition. Turnover applies only when the current state is Accepted, and
escape only to non-redeemed Stigmatized paths; neither changes the reward
already earned. Reference values are b=1, a=.6, c=.25, r=2, b2=.5, r2=2.5,
and delta=.02. This is a model specification diagram, not an estimated
transition graph from children.

## Figure 3. Four ways to represent the same context and behavior problem.

An illustrative K=3 makes the action organizations visible; it is a diagram,
not an additional simulated condition. M denotes masking and A authenticity.
**(A)** Flat choice uses a single softmax over 2K context-behavior arms and
updates only the selected arm. **(B)** Hierarchical choice first selects one
of K contexts and then masking or authenticity within it. The same realized
subjective reward updates the selected context value and the selected
within-context behavior value. **(C)** Global masking uses one shared mask
arm plus K context-specific authentic arms, updating only the selected arm.
**(D)** The known-good-context control offers two actions in an already
identified receptive context and is invariant to requested K. At zero
comparison cost, the three environmental expected-reward classes are .75
for masking, 1.15 for authenticity in the receptive context, and -.80 for
authenticity in other contexts. Keeping those reward classes fixed makes
representation and search burden distinct experimental factors.

## Figure 4. Weighting, feedback history, and information change learned behavior.

**(A)** With receptivity fixed at p=.65, final-window masking increased from
58.89% at lambda=.5 to 99.19% at lambda=2.5. The contrast was +40.30 percentage
points (95% CI [39.54, 41.06]); bars are equal-weight means of five master-seed
estimates, not confidence limits. **(B)** The exact transformed-reward threshold
is (.75+1.4 lambda)/(1.6+1.4 lambda), increasing from .6304 to .8333 between these
weights while objective indifference remains .7167. **(C)** Initial rejection,
relative to acceptance, reduced subsequent authentic sampling by 2.58 points
(95% CI [-3.58, -1.59] for rejected minus accepted), whereas the final-window
masking contrast was -0.034 points [-1.161, 1.092]. **(D)** Within the rejected
stratum, 5% forced authentic exposure and counterfactual authentic feedback
reduced final masking by 4.66 [3.32, 6.00] and 11.81 [10.97, 12.66] points,
respectively. These are two specified information manipulations, not
intensity-matched treatments. Panels C-D pool p=.75/.85 with equal weighting.
Their intervals, and the contrast interval in A, are the archived Student-t
95% intervals across five independent master seeds. E01 used 500 learners and
2,000 steps per cell, with the last 400 steps defining the final window.

## Figure 5. Graded options preserve engagement while reducing endpoint use and intensity.

**(A)** At p=.75 and .85, expected reward is affine in disclosure level d, with
full authenticity (d=1) optimal in both cases. Adding intermediate actions
leaves the endpoint optimum unchanged. **(B)** Partial disclosure lowers reward
variance: Var(R)=9(1-p)d[1-(1-p)d]. Rejection probability is (1-p)d; this is exact
payoff geometry, not evidence of an independently measured learner preference
for low variance. **(C)** Following initial rejection, five independently
learned graded actions, relative to binary choice, increased post-initial
nonzero disclosure by 25.50 points [25.30, 25.71], changed full-authentic
final-window selection by -32.87 points [-34.20, -31.53], and changed unique
full-authentic modal classification by -22.17 points [-28.88, -15.47]. Mean
disclosure intensity over the full measurement horizon changed by -2.976 points of
the unit disclosure scale [-3.387, -2.565]. The last contrast is an exact
re-expression of the archived normalized-regret contrast, because normalized
objective regret is 1-mean(d) in these cells; it is not an independent outcome.
The different time windows and denominators are shown in the labels. Intervals
are archived Student-t 95% intervals across five independent master seeds,
pooling p=.75/.85 with equal weighting. E02 used 500 learners and 2,000 steps
per cell, with a 400-step final window. Experience at one graded level did not
update neighboring levels.

## Figure 6. Persistent social state relocates objective thresholds and sustains a learning gap.

**(A)** The static authenticity threshold is .7167. The full-information dynamic
Neutral-state thresholds are approximately .38394, .33878, and .26901 at escape
rates eta=0, .2, and .8. Bars use the midpoints of archived numerical brackets
of width .00006104; these brackets are computational precision intervals, not
statistical confidence intervals. **(B)** At five prespecified disagreement
sentinels, extended-horizon runs at T=5,000 retained aggregate Neutral-state
masking while the dynamic oracle favored authenticity in every master. From
left to right, the (p,eta) pairs are (.4,0), (.55,0), (.75,0), (.55,.2), and
(.9,.2), with mean Neutral masking of 99.67%, 98.22%, 95.42%, 97.12%, and 89.97%.
Bars are equal-weight means of five master-seed fractions and dots are the five
individual fractions. These archived secondary sensitivity runs used n=160
and the last 20% of steps; the denominator is observed Neutral-state actions,
not all actions or a fraction of learners. The displayed persistence does not
assert asymptotic irreversibility.

## Figure 7. The full dynamic grid separates agreement, suboptimal masking, and inconclusive cells.

The 21 by 17 reference grid crosses receptivity p=0,.05,...,1 with escape
eta=0,.05,...,.8. Each displayed square is one parameter cell summarized
from five independent master seeds, with n=160 learners, T=1,000 steps,
and a final 200-step window per master. The publication categories partition
all 357 cells: 243 show learned suboptimal masking, 107 show agreement with
the objective benchmark, and seven are inconclusive. The 243 suboptimal-mask
cells have adequate Neutral-state exposure, aggregate learned preference
for masking, and a full-information dynamic authenticity optimum in all five
masters. Stable non-inconclusive classification requires agreement in at
least four of five masters. Five inconclusive cells lack adequate exposure
in every master; at (p,eta)=(.25,0) and (.30,0), only one and two masters,
respectively, have adequate agreement. Exposure requires at least 160
Neutral visits and 32 visiting learners per master. Categories are taken
directly from the frozen publication map. These are tested parameter-cell
counts, not population prevalence or classifications of individual learners.

## Figure 8. Persistence is broad across separate perturbations, with identifiable exceptions.

Each matrix entry is the number of five master seeds retaining the
learned-suboptimal-mask classification at one prespecified disagreement
sentinel; the adjacent total sums five sentinel columns to a denominator
of 25 cell-master classifications. Rows are separate executed one-factor
changes from the reference setting, not a joint factorial experiment.
Baseline and 11 perturbation rows retain 25/25 classifications. Lowering
alpha to .03 retains 18/25; raising tau to .6 retains 21/25; lowering gamma
to .5 retains 10/25. All remaining classifications in these rows agree
with the dynamic oracle; none are inconclusive. The discount factor gamma
changes both the learning target and the full-information objective.
The boundary/agreement control (p,eta)=(.35,0) is excluded from this
five-sentinel denominator. Counts summarize archived classifications without
new estimation, uncertainty intervals, or simulation.

## Figure 9. Representation separates encounter, sustained use, endpoint selection, and search cost.

Panels A-C and E-F use one receptive context among K=1,2,4,8,16 contexts, with
fixed good-context identity and unchanged best expected reward 1.15.
**(A)** Final-window masking rises from 26.36% to 84.19% in the flat 2K
representation and from 26.45% to 87.27% in the hierarchical representation;
under global masking it changes from 27.23% to 25.77%. **(B)** The fraction
classified with a good-authentic final-window modal action is a different
outcome; classification uses deterministic first-index argmax, retaining ties.
**(C)** At K=16, 99.72% of flat learners and 99.64% of hierarchical learners
experienced accepted authenticity in the good context, alongside 84.19% and
87.27% final-window masking. Successful encounter has a learner denominator;
masking summarizes action fractions. **(D)** At K=16, increasing receptive
contexts from one to four increases good-authentic modal classification from
75.48% to 99.36% (flat) and 52.00% to 95.80% (hierarchical). **(E)** Context
expansion increases expected static regret per step, including under global
masking despite its high final modal selection. **(F)** Mean time to the first
accepted good-context authentic action also rises. Time is a zero-based first
success index, with non-events capped at T=2,000. All displayed values are
descriptive, equal-weight means across five master seeds; connecting lines are
visual guides and no confidence bands are implied. E04 used 500 learners and
2,000 steps per cell, with a 400-step final window. A, C, E, and F display
archived secondary outcomes; D displays endpoint means for the abundance
control rather than the prespecified slope contrast.

## Figure 10. The learned modal crossing lies below objective indifference, while actual masking is a separate quantity.

**(A)** Archived, equally pooled master-seed response points are shown for the
flat eight-action and hierarchical representations at K=4 and lambda=1.
Connecting lines only join the archived points; they are not a newly fitted
curve. The frozen flat good-authentic modal-population .5 crossing is .312852
(95% complete-master-curve bootstrap CI [.307836, .316918]), below the exact
objective crossover 8/17=.470588. The narrow shaded strip marks the archived
crossing interval; the light region separates learned and objective boundaries.
At the learned crossing, good-context authenticity retains an expected reward
advantage of .134076. The hierarchical crossing is left-censored below .30.
No estimator or bootstrap was rerun to construct this figure. **(B)** At
comparison costs 0, .30, .325, and 8/17, actual final masking is 58.82%, 77.61%,
78.95%, and 85.20%, whereas good-authentic modal classification is 94.00%,
52.92%, 47.24%, and 14.16%. Masking has an action denominator and modal
classification a learner denominator; the .5 modal crossing is not the onset
of majority masking. These bars are descriptive means of five master-seed
estimates. E05 used 500 learners and 2,000 steps per cell, with a 400-step final
window. Expected good-context authentic reward is 1.15-.85 bf, whereas the
accepted realized reward is 1.6-bf.

