# Article V1 Methodological Position

**Date:** 16 August 2026
**Repository:** `gifted-masking`
**Branch:** `codex/frontiers-stage2-e06`
**HEAD:** `d22febd83e7e2e5594faf3a2aa8c36aac42c6bfa`
**Document class:** authority document. Documentation only. No experiment was run; no parameter, config, model semantic, artifact or frozen result was changed; no literature search was performed.
**Authority precedence:** `ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md` → `ARTICLE_V1_STAGE1_PUBLICATION_FREEZE.md` → `ARTICLE_V1_CLAIM_LEDGER.md` → `ARTICLE_V1_ANALYTIC_RESULTS.md` → `ARTICLE_V1_LITERATURE_AUDIT.md`. Where this document and those differ, they govern.
**Evidential basis:** `ARTICLE_V1_PARAMETER_RATIONALE_AUDIT.md` and `ARTICLE_V1_PARAMETER_REGISTER.csv` (86 rows).
**Consumers:** the future Methods chapter, the future parameter appendix, the future Discussion and Limitations sections. This document is an authority for those chapters; it is not manuscript prose.

---

## 1. Purpose of Article V1

Article V1 asks whether a specific class of divergence can arise in simplified learning systems: a divergence between what a learner comes to do and what an exactly computable objective benchmark says is better, in environments abstracted from documented features of gifted social experience.

Concretely the paper seeks to establish five things, in this order:

1. **Existence.** The divergence occurs at least somewhere in each model.
2. **Non-isolation.** It is not confined to a single finely tuned parameter point.
3. **Tested-region extent.** It occupies substantial, structured regions of the *tested* model space.
4. **Structural progression.** It becomes stronger, weaker, or qualitatively different as specific structural features are added — graded disclosure (M1), persistent social state (M2), heterogeneous scarce contexts and comparison cost (M3).
5. **Exact comparison.** Each divergence is measured against an exactly derived objective benchmark rather than an informal notion of "better".

That is the whole contribution. Nothing in Article V1 depends on the exact numerical coordinates at which these properties are demonstrated.

## 2. What kind of model this is

Article V1 is an **existence-and-structure computational modelling paper**.

It is **not**:

| Not this | Why not |
|---|---|
| a quantitatively calibrated psychological model | no parameter is estimated from human data (§3) |
| a population prevalence model | no probability measure over parameter space or over people is defined (§7) |
| a parameter-estimation study | no observable-to-parameter mapping exists yet (§11) |
| a complete formal characterization of the models | selected exact results only; the full divergence set is not computed (§10) |
| a fitted model of individual gifted children | model steps have no calibrated real-time interpretation and no child-level data are used |

The models are stylized. Their scientific content lies in their **structure** and in **selected qualitative relations among variables**. Many of their exact numerical values are coordinates at which that structure is instantiated, not measured properties of anyone.

## 3. What the current literature can and cannot calibrate

The governing literature authority (`ARTICLE_V1_LITERATURE_AUDIT.md`) does not supply a common quantitative measurement system for the model's variables. There is no shared scale on which belonging, authenticity, concealment effort and rejection are measured in commensurable units, and no study in the approved source ledger reports a quantity convertible into any of

```text
a   b   c   r   alpha   tau   lambda   delta   eta   p_good   p_bad   bf
```

as a literal numerical psychological quantity.

**Therefore the count of `EMPIRICALLY_CALIBRATED` parameters in Article V1 is zero.** This is stated plainly rather than disguised. It is the expected outcome for this class of model and it is not a defect, provided the paper does not claim otherwise.

What the literature *does* support is listed in §4. Manufacturing calibration where the audit found none is prohibited.

## 4. Qualitative motivation versus quantitative calibration

The inability to estimate literal numbers does not make the model structure arbitrary. The following qualitative propositions are drawn **only** from the approved literature authority and are the propositions the reference parameterization instantiates:

| Model relation | Literature status | Strength |
|---|---|---|
| some gifted youth deliberately conceal or manage the visibility of ability | supported (the strongest gifted-specific anchor) | good |
| concealment carries an ongoing cost (`c > 0`) | supported: visibility management is documented and described as effortful | moderate |
| adverse peer response is a cost (`r > 0`) | supported as *perceived* social pressure, not as an identified causal effect | moderate |
| receptivity varies across social contexts (`p_good ≠ p_bad`) | supported; among the better-evidenced parts of the gifted literature | moderate–good |
| high-achieving reference groups can impose comparison costs (`bf` exists) | supported as background (BFLPE) | good as motivation |
| adverse early feedback can suppress later sampling | supported generically, and it is established prior art | good, but not novel |
| receptive contexts can be scarce and access to them differs | supported for *preference*; only a plausible mapping for *search* | weak–moderate |

The following are **not** literature-supported and must never be presented as such:

- that authentic expression has a measurable positive utility independent of the social response (`a > 0` is a modelling assumption, not a documented quantity);
- that rejection cost substantially exceeds concealment cost (`r ≫ c` is a plausible first abstraction, not a measured comparison);
- **that concealment persists longitudinally.** The literature does not establish persistence, metastability or irreversibility. Consequently the entire M2 persistent-state transition system has *no* external empirical anchor;
- any magnitude, any transition probability, any prevalence, and any calibrated BFLPE reading.

**The correct inference:** qualitative model structure may be empirically informed even when exact parameter values are not quantitatively calibrated. Those are two separate judgements and the manuscript must keep them apart.

## 5. Role of arbitrary reference parameters

An **arbitrary reference value** is a number whose exact magnitude has no independent quantitative justification but which provides a reference instantiation of an otherwise defensible model structure.

This is **not automatically a methodological defect.** It is the correct description of a stylized model. Three conditions make it acceptable:

1. the number is never presented as empirically calibrated;
2. the structure it instantiates is independently defensible;
3. the claims that rest on it are stated conditionally on the reference parameterization.

The canonical case is the rejection-cost parameter:

```text
parameter r exists                      WELL_MOTIVATED
relation r > 0                          LITERATURE_SUPPORTED (perceived cost)
relation r substantially exceeds c      PLAUSIBLE_FIRST_ABSTRACTION
exact value r = 2.0                     ARBITRARY_REFERENCE_VALUE
provenance                              INHERITED_LEGACY
```

Those are four independent judgements about one symbol. Collapsing them — in either direction — is the error the revised audit exists to prevent. In particular, **provenance is not justification**: that `r = 2.0` was inherited verbatim from a legacy script explains where the number came from and says nothing whatever about whether `2.0` is right.

**Numerical arbitrariness is tolerable; structural arbitrariness is more consequential.** Choosing `r = 2` rather than `1.8` moves a coordinate. Choosing a redemption probability of exactly `p/2` rather than some other functional form changes the model. The audit reports the two separately, and §9 of the audit lists every structural assumption for which no rationale was recovered.

## 6. Existence, tested-region, and structural results

Article V1 results are reported at exactly three levels of evidential strength. The level must be stated wherever a result is used.

**Level 1 — point existence.** The phenomenon occurs at at least one model configuration. Weakest.
*Examples:* the E03 harsh sentinel (one labelled cell, three transition constants moved jointly); the E05 flat crossing (one `K`, one architecture, one criterion, one learner setting); the E01 controlled contrasts (two receptivity cells).

**Level 2 — tested-region existence.** The phenomenon is observed over a nontrivial tested region, i.e. many configurations along one or more deliberately swept dimensions.
*Examples:* E03 over the 357-cell `(p, η)` grid; E04 over the `K` ladder crossed with four action representations, three abundance regimes and two identity modes; E05 over the 18-point `bf` sweep.
**Mandatory qualification:** a Level-2 result is Level 2 *only along the swept dimensions*. Every unswept parameter remains at a single reference coordinate, so with respect to those parameters the same result is Level 1. E03 is a tested region in `(p, η)` and a single point in `(b, a, c, r, α, τ, λ, q₀, γ, b₂, r₂, δ)`. E04 and E05 are single points in receptivity (`p_good`, `p_bad` were never varied) and in every learner constant.

**Level 3 — structural / analytic.** The result follows from the mathematical form of the model rather than from numerical sampling.
*Examples:* the M1 affine disclosure objective and its endpoint consequence (conditional on the linear acceptance relation); the M0 objective threshold formula; the M2 Bellman comparator, Accepted-state dominance, and the Neutral static-plus-dynamic decomposition; M3 full-information `K`-invariance under the frozen one-good-context structure; the general comparison-cost crossover formula; the reward-scale/temperature coupling.

**Simulation findings may never be promoted to Level 3.** Every reported magnitude and location — including `43/60`, `8/17`, `.384/.339/.269`, `243/357`, `−0.2340`, `−0.4704`, `0.312852` — is either a reference-parameter realization of a general formula or a reference-parameter simulation estimate. The general formulas are Level 3; their numerical realizations are not.

## 7. Interpretation of parameter-space coverage

The word **prevalent** is prohibited for model phenomena, because no probability measure over parameter space is defined anywhere in Article V1. Permitted formulations:

> occurs across substantial regions of the tested model space
> occurs broadly across tested simplified learner regimes
> is not confined to a single finely tuned parameter point
> tested-grid coverage

Five quantities are routinely confused and must be kept distinct:

| Quantity | What it is | Where it appears |
|---|---|---|
| many learners within a fixed parameter cell | `n` simulated learners; **not** the inferential unit (freeze C.1) | E01–E05 |
| many tested parameter cells | coverage of a prespecified grid under its counting measure | E03 `243/357` |
| many independently seeded replications | five master seeds; the inferential replicate unit, df = 4 | all experiments |
| natural parameter-space prevalence | would require a measure over parameter space | **not defined anywhere** |
| real-world population prevalence | would require empirical sampling of people | **not attempted** |

For E03 specifically:

```text
243/357  IS      tested-grid coverage under the frozen rectangular grid
                 [0,1] x [0,0.8] at step 0.05 and its uniform counting measure

243/357  IS NOT  population prevalence
                 natural parameter-space volume
                 a probability that masking occurs
                 prevalence among gifted children
```

Required appendix sentence:

> The reported cell fraction depends on the prespecified grid bounds and resolution and should not be interpreted as prevalence or as a natural measure of parameter-space volume.

The scientifically stronger statement available from the same evidence is that the learned/objective mismatch occupies a substantial, structured and contiguous region of the tested plane rather than isolated cells.

## 8. Objective benchmarks and reference-model conditionality

Article V1's distinctive methodological asset is that every environment has an exactly computable objective answer:

- M0/M1: `Δ₀(p) = a + c − (1−p)(b+r)`, with crossover `p* = 1 − (a+c)/(b+r)`;
- M2: a full-information Bellman optimum, independently verified by exact four-policy enumeration;
- M3: exact expected-reward classes and the general comparison-cost crossover `bf*`.

Three conditions bind every use of these benchmarks:

1. **They are full-information oracles.** They know the complete payoff structure and do not share the learner's information limits. No sentence may claim the learner underperformed the best policy attainable under its own information constraints (freeze C.8).
2. **Their numerical values are reference realizations.** `p* = 43/60` and `bf* = 8/17` are what the general formulas return at the reference parameterization. They are exactly derived *conditional on* uncalibrated inputs, and `bf*` additionally depends on `p_good`. State the general formula first and the number second, always labelled.
3. **The comparator can move with the learner.** `γ` belongs to both the learner and the M2 objective comparator. When `γ` changes, what counts as correct changes. A sentinel that "matches the objective" at `γ = 0.5` does so because the objective moved, not because learning improved.

## 9. What Article V1 does not claim

1. That any parameter is empirically calibrated.
2. That any reported fraction is a prevalence — human, learner-level, or parameter-space.
3. That the models describe how children actually learn.
4. That model steps correspond to days, weeks, months or years. **No authorized mapping from model steps to real time exists anywhere in the repository.**
5. That the divergence set has been formally characterized.
6. That the learner failed relative to an information-matched optimum.
7. That the exact thresholds `43/60` and `8/17` are constants of the phenomenon.
8. That any structural feature has been causally isolated where the claim ledger records a confound (`K` versus `1/K` scarcity; graded disclosure versus arm count; shared-mask versus action cardinality).
9. That concealment is widespread or longitudinally persistent.
10. That the exact numerical coordinates are measured properties of gifted children.

## 10. Future formal-analysis programme

A later mathematical treatment could characterize the learner/objective divergence regions analytically or semi-analytically, for example the set

```text
Theta_div = { theta : pi_learner(theta) != pi_objective(theta) }
```

or its finite-horizon and stochastic analogues. Potential objectives:

- existence conditions and analytic region boundaries;
- connectedness and geometry of the divergence regions;
- monotonicity in `p`, `η`, `λ`, `τ`, `α`, `γ`;
- asymptotic and limiting behaviour (large horizon, small `α`, small `τ`);
- dimensionless reductions and the minimal sufficient parameter set;
- bifurcation / crossover structure, including the mechanism of the E05 displacement.

**None of this is performed now, and none of it is a prerequisite for Article V1.** Article V1 establishes selected exact benchmarks together with computational existence and tested-region results; complete characterization would strengthen and generalize the theory, and is a legitimate separate programme.

## 11. Future empirical-calibration programme

A distinct future programme could make the model quantitatively descriptive. Its logic:

```text
empirical observations
        |
        v
observable behavioural summaries
        |
        v
model-generated summaries
        |
        v
parameter / effective-regime inference
```

Steps such a programme would need:

1. define observable real-life counterparts to model variables;
2. collect behavioural, longitudinal and social-context data;
3. fit effective model parameters or parameter combinations to observed patterns;
4. quantify uncertainty in those fits;
5. test whether empirically fitted individuals and environments fall inside the divergence regimes found in the simulations;
6. only then, estimate how frequent those regimes are under an *empirically justified* parameter distribution.

**Only at step 6 would a question resembling real-world prevalence become meaningful.**

Candidate conceptual mappings — future, not validated operationalizations:

```text
receptivity          -> empirical probability of a positive social response
masking/disclosure   -> observable self-presentation or ability-disclosure choices
state persistence    -> persistence of peer reputation / social consequence
context discovery    -> access to, or identification of, compatible peers or groups
comparison cost      -> measurable self-evaluative or upward-comparison burden
```

These are conceptual future mappings only. None is a current validated operationalization, and none may be presented as one.

**On method choice:** likelihood-based estimation, simulation-based inference, approximate Bayesian computation, hierarchical Bayesian models and minimum-distance estimation are all plausible. No method is prescribed here; premature commitment would be unjustified.

**On bootstrapping — a required correction.** Bootstrapping does not estimate psychological parameters. It quantifies uncertainty around estimates derived from data. In Article V1 the bootstrap resamples five complete master curves to produce an interval for a simulation-derived crossing location; it identifies nothing about people. In a future calibration study, bootstrap or posterior methods would enter only at step 4 — *after* observables are defined and a fit is performed — as an uncertainty quantification on that fit.

## 12. Identifiability and effective parameter combinations

The model's parameters are unlikely to be separately inferable from behaviour, and this is a property of the modelling programme rather than a flaw in the present paper.

**What is proved.** From the positive homogeneity of the maintained subjective-reward transform (`φ_λ(sx) = s·φ_λ(x)` for `s > 0`), the linearity of the constant-step update, and Proposition G3 (`softmax(sQ, τ) = softmax(Q, τ/s)`), the maintained learner is exactly invariant under

```text
(R, q0, tau)  ->  (sR, s*q0, s*tau)        for any s > 0
```

**under these conditions, which must be stated whenever the invariance is claimed:**

- `s > 0`;
- `α`, `λ`, `γ` are dimensionless and are **not** rescaled;
- *every* reward-dimension quantity scales together, including `b, a, c, r, b₂, r₂, bf` and `q₀`;
- the RNG streams are held fixed (the invariance is pathwise, not merely distributional);
- absolute numerical tolerances stated in reward units — the `1e-10` value-iteration and Q-tie tolerances — are **not** scale-covariant, so the comparator's numerics are exactly invariant only up to that tolerance.

**Consequences.** Absolute reward scale has no independent behavioural interpretation unless temperature and initialization are specified relative to that scale. `b = 1` is a legitimate reward unit **if and only if** `τ` is read as `τ/b`. Prefer dimensionless relationships where useful, above all `ΔR/τ`.

**What follows for identifiability.** The M0/M1 objective geometry depends on the four payoff constants only through the two sums `a + c` and `b + r`; the pairs `(a, c) = (0.6, 0.25)` and `(0.5, 0.35)` are objectively indistinguishable there, as is any `(b, r)` with `b + r = 3` inside the required sign regime. Behaviour depends on reward differences measured in temperature units. Different tuples of `(a, b, c, r, τ)` can therefore generate similar behavioural distributions. Future empirical work should expect to estimate **dimensionless combinations, effective regimes, or posterior parameter sets** rather than unique literal psychological constants. A complete identifiability analysis — which combinations are recoverable from which observables, and where M2 and M3 break the M0 degeneracy through `b₂ − c`, `a − r₂`, `b + a` and the `bf` subtraction point — has not been performed and is future work.

## 13. Implications for the Methods chapter

The Methods chapter should explain, for each component:

1. **why it exists** — what question it makes askable;
2. **what qualitative phenomenon it abstracts** — with the literature status of that phenomenon stated honestly;
3. **why it is an appropriate minimal first abstraction** — what would be lost by adding or removing structure;
4. **what comparison is being made** — learner behaviour against which exactly specified benchmark;
5. **what exact mathematical relations define the relevant regimes** — as general formulas in the model parameters.

The Methods chapter should **not** attempt to justify every literal constant. It should say once, plainly, that payoffs are normalized reference values rather than quantities fitted to a human population, that no parameter in the work is empirically calibrated, and that exact values are given in the appendix.

Four statements are mandatory in Methods rather than the appendix, because omitting them would mislead:

- disclosure levels are represented as **independent actions**, so the learner does not generalize across neighbouring levels;
- the M2 states are **abstractions, not measured psychological states**, and the literature does not establish longitudinal persistence;
- the comparators are **full-information oracles**;
- the baseline learner is **loss-neutral** (`λ = 1` applies no transform); asymmetric weighting appears only as an explicit manipulation.

## 14. Implications for the parameter appendix

The appendix exposes exact numerical choices without disguising arbitrariness. For every numerical parameter it must give:

```text
value
role
provenance
exact-value justification
qualitative rationale
existing sensitivity
analytic consequences
future calibration status
```

Acceptable and expected wording:

> Exact numerical value not empirically calibrated; retained as an arbitrary reference instantiation.

That sentence is not an embarrassment. It is the correct description of a stylized model, and a reader who encounters it alongside a defensible structural rationale and a conditional claim has been told exactly the truth.

The appendix must additionally carry: the exact scale-equivalence and its conditions; the dimensionless presentation; the `1/K` scarcity coupling; the measure-relativity of `243/357`; the hard-coded, non-configurable redemption probability; the unexecuted sensitivity blocks; and the full list of structural assumptions for which no rationale was recovered.

## 15. Frozen methodological position

> Article V1 uses stylized computational models to establish the existence and structure of learner–objective divergences, not to estimate the numerical psychology of gifted children. The current empirical literature does not provide a common quantitative scale from which the reward, learning, or transition parameters of these models can be calibrated, and no parameter in this work is empirically calibrated. The model structure and a specific, enumerable subset of qualitative parameter relations — that some gifted youth deliberately manage the visibility of ability, that concealment carries an ongoing cost, that adverse peer response is experienced as costly, that receptivity varies across social contexts, and that high-achieving reference groups can impose comparison costs — are motivated by documented features of gifted social experience. Every remaining exact numerical value that is not a mathematical consequence of the model or a computational setting is an arbitrary reference instantiation, and the transition parameters of the persistent-state model have no external empirical anchor at all. The simulations therefore ask whether the proposed phenomena can arise, whether they extend beyond isolated parameter points, and how they change as specific structural features are introduced. Quantitative calibration to real-world populations, probability distributions over parameter space, and complete formal characterization of the resulting regimes are separate future research problems, and none of them is a prerequisite for the present existence-and-structure contribution.

**The distinction this document exists to enforce:**

> The scientific hypothesis resides primarily in the structure of the model and in qualitative relations among variables. Many exact numerical values merely provide coordinates at which that structure is instantiated.

```text
ARTICLE_V1_METHODOLOGICAL_POSITION_FROZEN
```
