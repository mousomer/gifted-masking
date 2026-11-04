# Supplementary Methods

## Ability Concealment Does Not Uniquely Reveal the Environment: Learning and Social Opportunity in Gifted Learners

This supplement specifies the five finite-learning experiments reported in the
article. It separates environmental reward, sampled information, learned value,
and full-information benchmarks. E01–E05 are the complete numerical evidence
boundary. The models are stylized computational environments rather than
calibrated models of children, and model steps have no calendar-time
interpretation.

## S1. Common learner and simulation conventions

### S1.1 Actions, values, and reward transformation

The common stateless learner assigned one value to each represented action,
initialized at

$$
Q_0(x)=q_0=0.
$$

The reference learning rate was $\alpha=.1$, softmax temperature was
$\tau=.25$, and negative-reward weighting was $\lambda=1$. For realized
environmental reward $R$,

$$
v_\lambda(R)=
\begin{cases}
R,&R\geq 0,\\
\lambda R,&R<0.
\end{cases}
$$

The transform affected the learning update only; it did not alter the
environment's objective payoff. All headline configurations used $\lambda=1$,
so $v_1(R)=R$. For a selected stateless action $x_t$,

$$
Q_{t+1}(x_t)
=Q_t(x_t)+\alpha\{v_\lambda(R_t)-Q_t(x_t)\},
$$

and unselected values were unchanged. M2 used the state-action update specified
in S4.

### S1.2 Choice rule

For an available action set $\mathcal A$, actions were sampled from

$$
\Pr(x_t=x)=
\frac{\exp\{(Q_t(x)-m_t)/\tau\}}
{\sum_{y\in\mathcal A}\exp\{(Q_t(y)-m_t)/\tau\}},
\qquad
m_t=\max_{y\in\mathcal A}Q_t(y).
$$

Subtracting the row maximum made the softmax numerically stable without
changing its probabilities. Temperature is a design parameter, not a measured
learner trait.

### S1.3 Payoffs and terminology

The shared reference payoffs were

| Symbol | Meaning in the model | Reference value |
| --- | --- | ---: |
| $b$ | benefit attached to accepted authenticity or masking | 1.00 |
| $a$ | authenticity value | 0.60 |
| $c$ | masking cost | 0.25 |
| $r$ | rejection penalty | 2.00 |

Model masking is the low-visibility action. Authenticity is the represented
higher-visibility action. A context is an option with its own acceptance
probability; it is not a literal peer group or physical relocation. Neutral,
Accepted, and Stigmatized are model states, not diagnoses.

### S1.4 Horizons and final windows

E01, E02, E04, and E05 used 500 simulated learners per cell, $T=2000$ steps,
and a 400-step final window (steps 1600–1999). E03 used 160 learners per cell,
$T=1000$, and a 200-step final window (steps 800–999). In general the final
window began at

$$
t_{\mathrm{start}}=T-\lceil .2T\rceil.
$$

Final-window modal classifications used action counts, not final $Q$ ordering.
They are operational finite-horizon summaries and do not assert convergence.

## S2. E01 — feedback-history experiment

### S2.1 M0 reward structure and objective boundary

M0 had masking ($M$) and authenticity ($A$). Masking returned

$$
R_M=b-c.
$$

Authenticity was accepted with probability $p$, returning $b+a$, and rejected
otherwise, returning $a-r$. Its expected reward was

$$
\mathbb E[R_A]
=p(b+a)+(1-p)(a-r)
=a+pb-(1-p)r.
$$

The authentic-minus-mask advantage was

$$
\Delta_0(p)=a+c-(1-p)(b+r).
$$

Thus,

$$
p^*=1-\frac{a+c}{b+r}
=1-\frac{.85}{3}
=\frac{43}{60}
\approx .716667.
$$

At the reference values $R_M=.75$. Authenticity was therefore objectively
optimal at both primary receptivity values, $p=.75$ and $p=.85$.

### S2.2 Conditioning and estimands

Every learner's step-0 action was forced to authenticity. Learners were
stratified by whether this first outcome was accepted or rejected. Subsequent
actions occupied steps 1 through $T-1$.

The primary sampling estimand was

$$
\Delta\bar A_{1:T-1}
=
\bar A_{1:T-1\mid\mathrm{rejected}}
-
\bar A_{1:T-1\mid\mathrm{accepted}},
$$

pooled with equal weight across $p=.75$ and $.85$ within each master seed.
The secondary persistence estimand replaced subsequent action rate with
final-window mask rate.

In authenticity-optimal binary cells, normalized objective pseudo-regret is an
exact action-count translation rather than independent confirmation:

$$
\Delta\overline{\mathrm{Regret}}_{\mathrm{norm}}
=-\frac{T-1}{T}\Delta\bar A_{1:T-1}.
$$

For $T=2000$, the factor is $1999/2000$.

### S2.3 Information manipulations

The controlled baseline supplied feedback only for the selected action. In the
forced-authentic condition, 5% of post-initial choices were replaced by an
authentic action using a separate intervention stream. In the counterfactual
feedback condition, the learner received the authentic outcome that would have
occurred on a masking trial. The environment used the same latent acceptance
draw for that counterfactual, while counterfactual reward was excluded from the
learner's realized objective return. These manipulations alter information
allocation inside the model; they are not human treatment estimates.

### S2.4 Design and uncertainty

The standard design used $n=500$, $T=2000$, five master seeds
2026081101–2026081105, and $p\in\{.75,.85\}$ for the controlled history
contrast. Within each master, the two $p$-specific effects were equally
weighted. The reported 95% interval was

$$
\bar\theta\pm t_{.975,4}\frac{s_\theta}{\sqrt5},
\qquad t_{.975,4}=2.776445.
$$

The top-level inferential units were the five master-specific effects, not
individual simulated learners.

Secondary archived cells compared $\lambda=.5$ and $2.5$ at $p=.75$ under the
controlled baseline and at $p=.65$ under the maintained baseline. They were
kept secondary because the article does not interpret $\lambda$ as a human
rejection-sensitivity construct. No horizon or learning-rate sweep was executed
for E01.

## S3. E02 — graded action representation

### S3.1 Binary and graded architectures

The binary architecture represented $d\in\{0,1\}$, where $d=0$ was masking and
$d=1$ was full authenticity. The graded architecture represented five
independently learned arms:

$$
d\in\{0,.25,.5,.75,1\}.
$$

Experience at one disclosure level updated only that level. It did not
generalize to neighbouring values.

For disclosure level $d$, acceptance probability was

$$
\Pr(\mathrm{accept}\mid d)=1-(1-p)d,
$$

which yields

$$
\mathbb E[R(d)]
=a d-c(1-d)+b\{1-(1-p)d\}-r(1-p)d
$$

and hence

$$
\mathbb E[R(d)]
=b-c+d\{a+c-(1-p)(b+r)\}
=b-c+d\Delta_0(p).
$$

The objective is affine in $d$. Except at exact indifference, a strict optimum
is therefore an endpoint; intermediate disclosure is not a distinct static
optimum in this model.

### S3.2 Conditioning, outcomes, and pairing

E02 used $p\in\{.65,.75,.85\}$, $n=500$, $T=2000$, and master seeds
2026081201–2026081205. The first action was full authenticity, and the
main comparison used the rejected-initial-outcome stratum at $p=.75$ and
$p=.85$, equally weighted within master.

The maintained outcomes were:

1. post-initial rate of any non-zero disclosure in the graded architecture
   minus post-initial full-authentic resampling in the binary architecture;
2. graded minus binary final-window full-authentic action rate;
3. graded minus binary probability that $d=1$ was the unique final-window
   modal arm; and
4. binary minus graded normalized pseudo-regret.

The unique-modal statistic required the objective endpoint to have a strictly
larger final-window count than every other represented arm. The broader
full-authentic action-rate statistic did not impose modal uniqueness. In
authenticity-optimal cells, graded normalized pseudo-regret is exactly the
horizon-average disclosure distance $1-d$; it is not independent welfare
evidence.

Binary and graded learners were reinitialized from the same
policy/environment stream within master seed and receptivity. Full latent
uniform sequences and child IDs were matched within those pairs. Pairing did
not cross receptivity values or master seeds. Student-$t$ intervals used five
master-specific paired architecture effects as the top-level units.

The $p=.65$ condition was a maintained control rather than a headline
decision input. Three- and nine-level graded architectures were planned but
not executed and are not represented as sensitivity evidence.

## S4. E03 — persistent-state environment and dynamic oracle

### S4.1 State and transition kernel

M2 used states Neutral ($N$), Accepted ($A$), and Stigmatized ($S$), with
actions $M$ and $A$. Reward was realized before the next-state transition.
The reference transition/reward kernel was:

| Current state | Action/outcome | Reward | Next state |
| --- | --- | ---: | --- |
| $N$ | mask | $b-c$ | $N$ |
| $N$ | authentic, accepted with $p$ | $b+a$ | $A$ |
| $N$ | authentic, rejected with $1-p$ | $a-r$ | $S$ |
| $A$ | mask | $b-c$ | $N$ with $\delta$, else $A$ |
| $A$ | authentic | $b+a$ | $N$ with $\delta$, else $A$ |
| $S$ | mask | $b_2-c$ | $N$ with $\eta$, else $S$ |
| $S$ | authentic, redeemed with $p/2$ | $b+a$ | $A$ |
| $S$ | authentic, not redeemed | $a-r_2$ | $N$ with $\eta$, else $S$ |

The reference values were $b_2=.5$, $r_2=2.5$, and $\delta=.02$. Escape
$\eta$ was applied after the current reward on non-redeemed Stigmatized
transitions. Masking in Neutral did not reset or create stigma.

### S4.2 Learner update

The selected state-action value followed

$$
Q_{t+1}(s_t,x_t)
=Q_t(s_t,x_t)+\alpha[
v_\lambda(R_t)+\gamma\max_{x'}Q_t(s_{t+1},x')
-Q_t(s_t,x_t)],
$$

with $\gamma=.9$. The values of unselected state-action pairs were unchanged.
The Neutral-state authentic-minus-mask advantage for continuation value $V$
was

$$
D_N(V)
=\Delta_0(p)+\gamma\{pV_A+(1-p)V_S-V_N\}.
$$

This expression makes explicit why the dynamic boundary can differ from the
static M0 boundary.

### S4.3 Full-information dynamic comparator

For each state-action pair, the oracle used the untransformed environmental
reward and known transition probabilities:

$$
Q^V(s,x)=
\sum_{s'}P(s'\mid s,x)
\{r(s,x,s')+\gamma V(s')\},
$$

$$
(\mathcal TV)(s)=\max_x Q^V(s,x).
$$

Value iteration began from $V_0(s)=0$ and repeatedly set
$V_{k+1}=\mathcal TV_k$ until

$$
\max_s|V_{k+1}(s)-V_k|<10^{-10},
$$

with a fail-closed maximum of 100,000 iterations. Objective action ties used a
$10^{-10}$ tolerance. The computed envelope was independently checked by
enumerating deterministic policies; the maximum recorded discrepancy was
$8.99\times10^{-10}$. The oracle is infinite-horizon and full-information. It
is intentionally not information-matched to the finite learner.

### S4.4 Grid, classifier, and stability

The exact grid was

$$
p\in\{0,.05,\ldots,1\},\qquad
\eta\in\{0,.05,\ldots,.8\},
$$

giving $21\times17=357$ cells. Each cell used $n=160$, $T=1000$, and five
master seeds 2026081301–2026081305.

Within each master and cell, final-window Neutral-state action counts were
aggregated across learners. Neutral exposure was adequate only if:

1. at least 160 Neutral-state final-window visits were observed in total; and
2. at least 32 learners contributed at least one Neutral-state visit.

Equal aggregate mask/authentic counts or inadequate exposure produced an
inconclusive learned action. A cell-master was labelled
learned_suboptimal_masking only when exposure was adequate, aggregate Neutral
counts favoured masking, and the full-information oracle favoured
authenticity in Neutral. Stability required the same non-inconclusive class in
at least four of five masters.

The reported $243/357$ statistic counts grid cells satisfying that
learned–objective disagreement classification in every master. The remaining
grid contained 107 agreement cells and seven inconclusive cells. Five of those
seven had inadequate Neutral exposure in all five masters. At $p=.25$ and
$p=.30$ with $\eta=0$, only one and two masters, respectively, had adequate
exposure and agreed on `learner_matches_objective`; those cells failed the
prespecified four-of-five stability rule and were therefore folded into the
inconclusive publication category. The statistic is tested-grid coverage, not
a fraction of learners, people, or naturally occurring environments.

## S5. E04 — contextual search architectures

### S5.1 Environmental structure and indexing

M3 contained $K$ contexts. In the primary condition, one context was receptive
with $p_{\mathrm{good}}=.85$ and the remaining $K-1$ contexts had
$p_{\mathrm{bad}}=.20$. Context indices were zero based in the maintained
implementation. In joint-action representations, action index $2g$ denoted
masking in context $g$, and $2g+1$ denoted authenticity in context $g$.

Masking returned $b-c$ in every context. Authenticity used that context's
acceptance probability. With comparison cost $b_f=0$ in E04, the distinct
expected-reward classes were mask, good-context authenticity, and bad-context
authenticity. Increasing $K$ duplicated classes but did not change their
values or the full-information maximum. The full-information best opportunity
was therefore $K$-invariant in the primary one-good-context design.

### S5.2 Four action representations

| Architecture | Choice and update |
| --- | --- |
| flat_2k | One softmax over the $2K$ joint context–behaviour arms; only the selected joint arm was updated. |
| hierarchical | A $K$-way context softmax followed by a two-way behaviour softmax within the selected context; the selected context value and selected within-context behaviour value were both updated from the same realized reward. |
| global_mask | One shared mask arm plus $K$ context-specific authentic arms; the selected arm alone was updated. |
| fixed_known_good | A two-action mask/authentic problem in the known good context; context discovery was removed and the architecture was structurally invariant to requested $K$. |

All architectures used the same reference learner settings. Acceptance
uniforms were consumed on every trial in the maintained random-number order.

### S5.3 Design, canonicalization, and outcome

The requested design crossed the four architectures,
$K\in\{1,2,4,8,16\}$, fixed versus random-per-learner good-context identity,
and one, two, or proportional-25%-good-context regimes. Conditions that were
structurally equivalent were canonicalized: 120 requested rows mapped to 55
executable cells, recorded in the equivalence table. Each executable cell used
$n=500$, $T=2000$, and master seeds 2026081401–2026081405.

For each learner, deterministic NumPy first-index argmax was applied to
final-window joint-action counts. The learner indicator equalled one only when
that selected indexed arm was authentic in a good context. Non-unique modes
remained eligible because a tie was resolved to its first indexed maximum.
The primary cell response was the mean of this indicator across learners.
This is not the superseded rule under which any tied good-authentic maximum
would qualify.

A separate strict diagnostic required a unique modal good-authentic arm. It
was not substituted for the prespecified primary estimator. The diagnostic
retained the direction of the primary flat and hierarchical contrasts.

The main one-good-context curves were accompanied by fixed/random identity
controls, a two-good-context control when feasible, the proportional-25%
receptive control, global-mask and fixed-known-good ablations, and complete
$K$ curves. Planned sensitivity over $p_{\mathrm{good}}$,
$p_{\mathrm{bad}}$, and $\tau$ was not executed and is not reported as
evidence.

### S5.4 Inference

Each architecture contrast or $K$ slope was first reduced within master seed.
The reported interval then used the five master-specific estimates in the
Student-$t$ construction from S2.4. Learners and $K$ cells were not treated as
additional independent top-level replicates.

## S6. E05 — learned and environmental boundary estimation

### S6.1 Environmental boundary

E05 fixed $K=4$, one good context at index 0,
$p_{\mathrm{good}}=.85$, $p_{\mathrm{bad}}=.20$, and evaluated the flat
eight-action and hierarchical representations separately. Comparison cost
$b_f$ was subtracted only from accepted authenticity in the good context.
Thus,

$$
R_M=.75,
$$

$$
R_G(b_f)
=.85(1.6-b_f)+.15(-1.4)
=1.15-.85b_f,
$$

and

$$
R_G(b_f)-R_M=.40-.85b_f.
$$

The exact environmental crossover was

$$
b_f^*=\frac{.40}{.85}=\frac8{17}=.470588\ldots.
$$

Bad-context authenticity did not become the competing objective optimum in the
tested range.

### S6.2 Grid and learned response

The complete cost grid was

$$
\{0,.30,.325,.35,.375,.40,.425,.45,8/17,.475,
.50,.525,.55,.575,.60,.625,.65,.80\}.
$$

The monotone crossing fit used the 16 points inside the dense range
$[.30,.65]$, including the exact $8/17$ anchor. The $0$ and $.80$ cells were
endpoint diagnostics outside that fit.

At each cost and master seed, the learned response was the fraction of 500
learners whose deterministic final-window first-index argmax selected the
single good-context authentic arm. It was an across-learner modal-arm
classification fraction, not a binary softmax action probability. The same
architecture/master policy-environment stream was reinitialized at every cost,
providing common-random-number pairing across $b_f$ within an architecture.
Flat and hierarchical architectures used separate random-stream families.

### S6.3 PAVA fit and crossing

The five master responses were averaged equally at each cost. A non-increasing,
equal-weight pool-adjacent-violators fit was then applied to the pooled dense
curve (Best & Chakravarti, 1990). The fitted .5 crossing was defined as follows:

1. if a fitted plateau equalled .5, use the midpoint of that plateau's
   $b_f$ range;
2. otherwise linearly interpolate between the adjacent fitted values that
   bracketed .5;
3. accept a crossing only when it lay strictly inside $(.30,.65)$;
4. do not extrapolate.

A response already below .5 at $.30$ was classified no_crossing_below and was
left-censored below the tested range. This was the hierarchical result; it was
not interpreted as absence of a crossing over all possible costs.

### S6.4 Complete-master-curve bootstrap

The crossing interval used 10,000 bootstrap replicates. Each replicate sampled
five complete master curves with replacement, averaged the sampled curves,
refitted PAVA, and reinverted the fit. Percentile limits at 2.5% and 97.5% were
reported only if at least 95% of replicates yielded valid in-range crossings.
All 10,000 flat replicates were valid. Zero hierarchical replicates were valid,
so no hierarchical point or interval was estimated. The bootstrap unit was a
complete master curve, not a learner or individual cost row.

The cost axis orders environmental parameter values. No binary-softmax
indifference identity was used to interpret the learned crossing.

## S7. Randomization, seed hierarchy, and inferential units

### S7.1 Master seeds and semantic streams

The archived master lists were:

| Experiment | Master seeds |
| --- | --- |
| E01 | 2026081101–2026081105 |
| E02 | 2026081201–2026081205 |
| E03 | 2026081301–2026081305 |
| E04 | 2026081401–2026081405 |
| E05 | 2026081501–2026081505 |

Semantic cell or family identifiers were hashed with SHA-256. The first four
little-endian 32-bit words from the digest were supplied to NumPy
SeedSequence together with the master and experiment namespace:

| Experiment | Archived construction |
| --- | --- |
| E01 | SeedSequence([master, 1, words]).spawn(2), separating policy/environment and intervention streams |
| E02 | SeedSequence([master, 2, words]).spawn(1) for the matched binary/graded pair |
| E03 | SeedSequence([master, 3, words]).spawn(1); approved horizon/window sentinels alone shared trajectory-prefix families |
| E04 | SeedSequence([master, 4, words]).spawn(1) for policy/environment and independent SeedSequence([master, 40, words]).spawn(1) for identity |
| E05 | SeedSequence([master, 5, words]).spawn(1), reinitialized across cost within architecture/master; bootstrap SeedSequence([2026081597, 50, architecture code]) |

Vectorized child draws were generated inside each cell/family stream. Child IDs
were not additional top-level inferential replicates. E01 acceptance and
rejection strata were disjoint outcome strata, not paired learners. E02 paired
architectures only within master and receptivity. E04 reduced K and
architecture effects inside master. E05 resampled complete master curves.

### S7.2 Inferential scope

Student-$t$ intervals in E01, E02, and E04 used five master-specific estimates
(df=4). E05's scalar endpoint effects used the same master-level convention,
whereas its crossing used the complete-curve bootstrap. E03's grid fraction
was identical across the five selected masters; this records stability across
those streams, not zero model uncertainty. Master lists were fixed constants,
not draws from a documented population of seeds.

## S8. Secondary estimands and sensitivity analyses

Secondary archived evidence was retained to test interpretation boundaries
without promoting it to a headline mechanism.

| Experiment | Secondary material | Status and role |
| --- | --- | --- |
| E01 | forced-authentic 5% and counterfactual-authentic feedback; $\lambda=.5/2.5$ cells | Archived. Information-channel effects support the sampling interpretation. Weighting remains learner-side sensitivity, not a human construct. |
| E02 | full-authentic rate, unique-modal endpoint, and disclosure-distance pseudo-regret; $p=.65$ control | Archived. These outcomes prevent interpreting increased non-zero disclosure as improved endpoint discovery. |
| E03 | six sentinels; $n=320$; $T=2000/5000$; windows .1/.4; $\alpha=.03/.3$; $\tau=.1/.6$; $\lambda=.5/2.5$; $q_0=.75$; $\gamma=.5/.99$; harsh boundary cells | Archived where present. They show classifier dependence on learner and dynamic settings. They do not define a population-wide phase boundary. |
| E04 | all four architectures; fixed/random identity; one, two, and proportional-25% good-context regimes; strict unique-mode diagnostic | Archived baseline ablations. Planned $p$ and temperature sensitivity was not run. |
| E05 | five master curves; endpoint contrast; strict unique-mode diagnostic; flat PAVA/bootstrap; hierarchical censoring | Archived. A longer-horizon crossing was planned but not executed. |

E03's harsh labelled boundary used $b_2=0$, $r_2=8$, $\delta=.3$,
$\eta=0$, $\gamma=.9$, and $p\in\{.70,.75,.80\}$. It demonstrates a bounded
case in which dynamic masking can be objectively optimal despite a static M0
authenticity advantage; it is not evidence for a region beyond the tested
cells.

## S9. Evidence provenance and reproduction

### S9.1 Three distinct provenance claims

The evidence package distinguishes:

1. ARTIFACT_VERIFIED: existing outputs byte-match the hashes stored in their
   archived manifests and evidence records;
2. CURRENT_IMPLEMENTATION_REPRODUCIBLE: a maintained procedure can be run from
   the present code, where separately authorized;
3. HISTORICAL_BIT_REPRODUCTION_VERIFIED: the exact historical source state and
   outputs can be reconstructed.

All 33 protected E01–E05 outputs are ARTIFACT_VERIFIED. Fingerprint-exact
historical generator-source bundles are retained for E04 and E05. E01–E03 are
HISTORICAL_SOURCE_STATE_UNRECOVERED.

Historical generator states underlying some archived E01–E03 artifacts are not
fully recoverable. The published claims are therefore governed by archived
result artifacts, hashes, configurations, and verification records rather than
by asserting bit-identical regeneration from the present implementation.
This does not imply that the archived artifacts changed; it limits source-level
historical reconstruction.

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

The five standard manifests under results/manifests retain the normalized
configuration, exact parameters, seed hierarchy, environment versions,
output paths and hashes, timestamps, and source fingerprints. The recorded
execution environment was Python 3.14.6 on macOS arm64 with NumPy 2.4.6;
E01, E02, E04, and E05 also recorded Matplotlib 3.10.8.

### S9.3 Validation and presentation reproduction

Read-only artifact validation loads the archived manifests and evidence matrix
and rehashes their declared outputs. It does not run a simulation. Figure
presentation can be regenerated deterministically from the pinned
publication-source tables, but that operation is distinct from experiment
reproduction. The figure-generation script imports no experiment module or
stochastic entry point.

The figure-source hashes used by the final display package are recorded in
the accompanying figure-provenance record. Examples include
e01_primary_effects.csv
(9b9227f43146b96ae7000f572d2249ae6bd4d39bf414715bdd780203afa38d36),
e03_grid_map.csv
(c5def710116248b60ffcc347fa408519ce5d9094547e486fc73f2388e5babbab),
e04_k_response.csv
(c01c04359b30d425d518566190dcfb27b10f9003e4123d9a6f05ce44382c11b7),
and e05_crossings.csv
(866697afb0cdd66f6e6d008cc6b06e52786d1e27f7ba3f71601a56512349076b).

No claim in this supplement requires a current-code experiment rerun, and no
historical-bit-reproduction claim is made for E01–E03.

## S10. Supplementary figure and table inventory

The following inventory lists supplementary material available from the
archived configurations and result artifacts. Secondary evidence remains
separate from the main Results.

| Candidate | Content | Status |
| --- | --- | --- |
| Table S1 | common parameters, horizons, and master seeds | Available from archived configurations |
| Figure/Table S2 | E01 master-level sampling and information-manipulation diagnostics | Available from archived artifacts |
| Figure/Table S3 | E02 secondary full-endpoint, unique-modal, and regret outcomes | Available from archived artifacts |
| Figure/Table S4 | E03 five-master stability, seven inconclusive cells, sentinels, and threshold brackets | Available from archived artifacts |
| Figure/Table S5 | E04 complete K curves, identity/good-count ablations, equivalence mapping, and strict tie diagnostic | Available from archived artifacts |
| Figure/Table S6 | E05 five master curves, pooled PAVA fit, bootstrap validity, endpoint and strict-mode diagnostics | Available from archived artifacts |
| Former cross-estimand Figure 6 | synthesis across noncommensurate estimands | Not included; comparability review required |

The former cross-estimand Figure 6 is not included because its quantities
require a separate scientific comparability and interpretation review.

## Supplement reference

Best, M. J., & Chakravarti, N. (1990). Active set algorithms for isotonic
regression: A unifying framework. *Mathematical Programming, 47*(1–3),
425–439. https://doi.org/10.1007/BF01580873
