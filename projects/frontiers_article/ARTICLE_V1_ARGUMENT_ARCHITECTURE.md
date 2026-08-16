# Article V1 Argument Architecture

**Freeze date:** 16 August 2026
**Status:** controlling intellectual map for Article V1 manuscript construction
**Scope:** architecture only; not manuscript prose
**Evidence boundary:** frozen E01–E05 evidence and maintained M0–M3 models only

This document is subordinate to the frozen scientific evidence and the
methodological position. It controls later manuscript organization and claim
selection. If later prose conflicts with a frozen mathematical, numerical,
inferential, or methodological authority, the prose must change.

## 1. One-sentence research question

> **How can finite experience and progressively richer social-learning
> structures shift learned behaviour away from authenticity—including toward
> concealment—even when the corresponding full-information objective benchmark
> in the specified model continues to favour authenticity?**

This is an existence-and-structure question. It does not promise a complete
characterization of all parameter regimes, a calibrated psychological model,
or an estimate of human or parameter-space prevalence.

## 2. One-paragraph contribution

Article V1 pairs exact objective benchmarks with finite-horizon learning
experiments to establish that learned concealment, reduced authenticity, or a
behavioural transition away from authenticity need not imply that concealment
is objectively advantageous within the specified model. M0 establishes the
minimal finite-sampling problem; M1 shows that a richer action vocabulary can
change learned behaviour without creating an interior static objective optimum;
M2 shows a broad tested region of learner/objective disagreement once outcomes
alter persistent future social state; and M3 shows that the existence of a
receptive context does not guarantee its discovery, and that a learned
comparison-cost transition can occur before exact objective indifference. The
paper does not claim that these mechanisms have all been independently
isolated. Its contribution is the controlled progression and the repeated exact
contrast between what a finite learner does and what a full-information
benchmark says is better.

## 3. Model progression

The Article V1 model order is frozen as `M0 -> M1 -> M2 -> M3`.

| Model | Structural addition | Newly answerable question | Objective comparator | Architectural role |
|---|---|---|---|---|
| **M0** | Binary mask/authentic action under stochastic acceptance | Can adverse finite experience reduce sampling of authenticity even where authenticity has higher expected objective value? | Static expected reward; general boundary `p* = 1 - (a+c)/(b+r)` | Establishes the minimal distinction `objective preference != necessarily learned behaviour`. The reference `43/60` is a realization of the general formula. |
| **M1** | Finite graded-disclosure action set | What changes when authenticity is not all-or-nothing? | Affine static objective `E[R(d)]`; strict optima remain endpoints | Separates action representation and finite exploration from static optimality. Intermediate actions may alter exposure and endpoint discovery; they are not generally new objective optima. |
| **M2** | Neutral, Accepted, and Stigmatized states with persistent consequences | What changes when current action and outcome alter future social state? | Exact full-information discounted MDP optimum | Makes continuation value essential. It is the central structural step because the relevant objective is no longer one-step expected reward. |
| **M3** | Heterogeneous contexts, scarce receptivity, context discovery, and comparison cost | What changes when authenticity is worthwhile somewhere, but a finite learner must discover where? | Exact reward classes; `K`-invariant best value in the one-good-context construction; general `bf*` formula | Separates availability of a good option from the learner's ability to find and settle on it. E05 varies comparison cost within M3; it is not a new model rung. |

M2 and M3 are conceptually distinct. M2 asks whether the learner values the
future consequences of an action correctly within a persistent state
structure. M3 asks whether the learner can locate the favourable context in
which the action is worthwhile. E05 belongs under M3 because it changes the
payoff of good-context authenticity without changing the context-search
architecture.

M4 is not a fifth Article V1 rung. M4/E06 may appear only as excluded future
work or as a limitation/model-extension direction; no M4/E06 numerical result
may enter Article V1 Results or support a V1 conclusion.

## 4. Evidence progression

| Evidence | Scientific role | Evidence level | Required ceiling |
|---|---|---|---|
| **E01** | Minimal behavioural precursor: early rejected authenticity reduces later authentic sampling and raises the linked regret translation. | Level 1: controlled reference configurations | Do not claim persistent final-mask separation. Sampling and normalized regret are algebraically linked, not independent confirmations. |
| **E02** | Action-representation support: independent graded arms preserve more nonzero disclosure while reducing full-authentic and optimal-endpoint selection. | Level 1 for the frozen architecture; paired with the Level-3 M1 affine result | Do not claim that graded disclosure solves masking, improves endpoint discovery, establishes independent welfare change, or creates an interior optimum. |
| **E03** | **Central region result:** persistent-state dynamics yield a substantial structured region in which aggregate final-window Neutral behaviour favours masking while exact full-information dynamic programming favours authenticity. | Level 2 in the swept `(p, eta)` plane; Level 1 in unswept parameters | `243/357` is tested-grid coverage only: 243 stable divergence cells, 107 matches, 7 inconclusive. Do not infer prevalence, natural phase-space volume, individual-policy frequency, or information-matched failure. |
| **E04** | **Central discovery result:** receptive-context authenticity declines with context-search burden in flat and hierarchical learners while the one-good-context full-information optimum remains `K`-invariant. | Level 2 in `K`, action representation, abundance regime, and identity mode under reference settings | State the conjunction: scarcity + discovery + finite sampling + maintained representation in the reference environment. Do not say that `K` intrinsically causes masking or that any control isolates a unique mechanism. |
| **E05** | **Strong quantitative displacement result:** the learned flat-architecture modal-response crossing occurs before the exact objective comparison-cost crossover. | Level 2 in `bf` under the frozen flat `K=4` architecture; the general objective crossover formula is Level 3 | Report `0.312852` descriptively against `8/17 ~= 0.470588`; objective advantage at the learned crossing is about `0.134076`. Do not use binary-softmax Proposition G2 as mechanism proof. Fixed temperature, action-set normalization, endogenous sampling, and learned-value effects remain possible contributors. The hierarchical crossing is left-censored and unidentified in range. |

The evidence hierarchy is:

1. E03 — central tested-region learner/dynamic-objective disagreement;
2. E04 — central context-discovery result under an invariant objective best
   value;
3. E05 — quantitative learned/objective transition displacement within M3;
4. E01 and E02 — supporting minimal and action-representation results.

E01 and E02 could be removed without invalidating the narrow E03–E05
conclusion. They are retained because they make the progression intelligible:
E01 identifies the minimal finite-sampling precursor, and E02 shows that action
representation can change behaviour before persistent state or context search
is introduced. They must not receive equal headline weight with E03–E05.

## 5. Canonical logical spine

1. A risky authentic action can have higher expected objective value while an
   adverse early outcome reduces its later sampling; this affects the learning
   trajectory without establishing a persistent final-mask contrast.
2. Replacing binary actions with independent graded-disclosure actions changes
   the learner's exposure distribution and endpoint use, even though the M1
   objective is affine and strict static optima remain endpoints.
3. Once outcomes alter persistent social state, the relevant comparator becomes
   an exact dynamic full-information optimum. Across a substantial structured
   region of the tested `(p, eta)` grid, finite-horizon Neutral behaviour favours
   masking while that dynamic optimum favours authenticity.
4. Once receptivity differs across contexts, the availability of a valuable
   authentic option is no longer equivalent to discovering it. In the reference
   environment, receptive-context authentic settling declines as the finite
   search problem expands even though the one-good-context full-information
   optimum remains `K`-invariant.
5. Adding comparison cost within M3 produces a learned flat-architecture
   behavioural crossing substantially before exact objective indifference,
   while authenticity retains positive objective advantage at that crossing.
6. Therefore observed concealment or reduced authenticity by a finite learner
   cannot, by itself, be interpreted as evidence that concealment is objectively
   preferable in the modeled environment.

## 6. Claim hierarchy

### Tier A — central Article V1 claim

> Learned concealment or reduced authenticity is not sufficient evidence that
> concealment is objectively advantageous within the specified model.

### Tier B — main supporting claims

- Persistent-state dynamics can produce a broad, structured tested region of
  aggregate learner/full-information-policy disagreement (E03).
- A receptive context can remain objectively best while finite learners become
  less likely to discover and settle on it as the reference search problem
  expands (E04).
- A learned behavioural transition can occur before the exact objective
  transition under the frozen M3 architecture (E05).

### Tier C — orienting/supporting claims

- Early adverse authentic feedback can reduce later authentic sampling without
  a detectable final-mask contrast (E01).
- Independent graded actions can preserve nonzero disclosure while worsening
  use of the objective endpoint, without creating an interior static optimum
  (E02 plus the M1 affine theorem).

### Tier D — exact structural anchors

- M0 objective boundary formula and its reference realization `43/60`.
- M1 affine objective and endpoint-optimum theorem, conditional on the frozen
  linear acceptance function.
- M2 Bellman comparator, Accepted-state dominance, dynamic-gap decomposition,
  and deterministic policy-enumeration verification.
- M3 one-good-context `K`-invariance and general comparison-cost crossover,
  with reference realization `8/17`.

## 7. End-of-paper belief target

### What the paper establishes

1. Exact full-information benchmarks can disagree with finite-horizon learned
   behaviour in the maintained M0–M3 structures.
2. This disagreement is not confined to a single isolated reference point:
   E03 maps a structured tested region, E04 maps a tested `K` response under
   controlled representations, and E05 maps a tested comparison-cost response.
3. Persistent state changes the objective problem from a static payoff
   comparison to dynamic planning.
4. The existence of a receptive context is not equivalent to a finite learner's
   discovery and use of it.
5. A learned transition need not coincide with an exact objective transition.

### What the paper suggests

6. Finite experience, action representation, persistent consequences, and
   context discovery are useful theoretical lenses for interpreting observed
   concealment without treating behaviour as a direct readout of objective
   value.

### What the paper explicitly does not establish

7. It does not estimate human prevalence, calibrate psychological parameters,
   fully characterize divergence regions, identify every displacement
   mechanism, or show irreversible/hysteretic masking.

## 8. Negative/non-claims

- Masking behaviour does not necessarily reveal that masking is objectively
  optimal.
- Availability of a receptive context does not imply that a finite learner will
  discover it.
- A learned crossover need not coincide with an objective crossover.
- A richer action set does not necessarily eliminate concealment or improve
  objective-endpoint discovery.
- Strong masking in a simulation does not establish human prevalence.
- No exact parameter is quantitatively calibrated from gifted-child data;
  provenance is not justification.
- The baseline uses `lambda = 1`; baseline phenomena are not consequences of
  explicit loss aversion.
- E01 does not show persistent final masking; E03 does not define an
  information-matched failure; E04 does not isolate `K` or scarcity alone; E05
  does not identify a mechanism; M4/E06 is not V1 evidence.

## 9. Figure-to-claim map

| Figure | First introduced in | Main purpose | Claim supported | Must not be read as showing |
|---|---|---|---|---|
| **1 — M0–M3 progression** | Formal Model | Orient the reader to the nested cascade and exact objective anchor at each rung. | Why the comparator and scientific question change from M0 through M3. | Simulation evidence, an empirical developmental sequence, or an M4-inclusive ladder. |
| **2 — E01, E02, M1 affine objective** | Results: “Finite feedback and action representation” | Establish the minimal sampling precursor and the behavioural consequence of graded independent actions alongside the endpoint theorem. | Early feedback changes sampling; action vocabulary changes learning without an interior objective optimum. | Persistent E01 masking, independent sampling/regret confirmation, graded welfare improvement, smooth generalization, or an optimal compromise. |
| **3 — E03 contrast map and objective Q gap** | Results: “Persistent consequences create learner/dynamic-objective divergence” | Provide the central visual evidence of a substantial structured tested region of disagreement. | Aggregate Neutral masking can differ from exact full-information dynamic policy across the tested `(p, eta)` region. | Prevalence, natural phase-space volume, individual-policy frequency, causal decomposition, or information-matched regret. |
| **4 — E04 discovery and E05 displacement** | Results: “Discovery burden and learned/objective transition separation” | Join the M3 discovery result to the comparison-cost response within the same model architecture. | A good option can remain objectively available yet under-discovered; the learned transition can precede the objective crossover. | A pure `K` effect, universal robustness across unswept settings, a hierarchical E05 threshold, or a proved displacement mechanism. |

**Figure sufficiency decision:** `SUFFICIENT_WITH_MINOR_EDITORIAL_CHANGE`.
The four figures cover orientation, minimal/supporting effects, the central
persistent-state region, and the M3 discovery/threshold result. No structural
figure gap requires a fifth main figure. Minor editorial work may improve
cross-references, panel labels, and caption economy; no new scientific panel is
authorized at Stage 1.

## 10. Dependency into Model/Methods

The recommended substantive section is **Formal Model and Methods**, with the
formal model progression before procedural experiment details. A split
`Formal Model` / `Methods` arrangement is acceptable if required by the journal,
but M0–M3 and their objective comparators must remain prominent and contiguous.

Before Results can be drafted, the Model/Methods authority must establish:

- variables, rewards, learner update, softmax selection, `lambda=1`, and the
  distinction between objective reward and learned/subjective value;
- M0 general objective boundary before the reference `43/60` realization;
- M1 linear acceptance assumption, affine reward, and endpoint consequence;
- M2 state/transition order and exact full-information dynamic comparator;
- M3 context/reward structure, one-good-context `K`-invariance, and general
  comparison-cost crossover before the reference `8/17` realization;
- full-information status of the comparators, stylized status of the states,
  arbitrary-reference parameter position, and experiment/inference definitions.

Results must then be organized by scientific finding:

1. finite feedback and action representation (E01–E02);
2. persistent consequences and dynamic-objective divergence (E03);
3. receptive-context discovery burden (E04);
4. learned/objective comparison-cost separation (E05).

## 11. Architecture freeze

1. **One clear question?** Yes; Section 1 controls.
2. **Does every experiment contribute?** Yes, but not equally; E01/E02 orient,
   while E03–E05 carry the main inference.
3. **Could E01/E02 be removed?** Yes without breaking the narrow central claim,
   but the minimal and action-representation progression would be lost.
4. **Strongest evidence?** E03 is the strongest direct region-level evidence;
   E04 and E05 provide the strongest M3 extension and quantitative separation.
5. **Is M2 essential?** Yes; it introduces the dynamic comparator.
6. **Is M3 distinct?** Yes; it introduces heterogeneous-context discovery.
7. **Does E05 belong under M3?** Yes; it varies comparison cost inside M3.
8. **Any over-level claims?** The prohibited promotions are listed above.
9. **Does every figure have a function?** Yes; Section 9 defines it.
10. **Does the argument need M4?** No. M4/E06 is excluded from V1 evidence.
11. **Is the contribution meaningful without calibration?** Yes. Simplification
    limits external quantitative inference but permits controlled existence,
    exact-comparator, and tested-region claims.
12. **Can readers distinguish evidence types?** Yes, if claims retain their
    Level 1/2/3 designation and reference-parameter conditionality.

The authority order for later writing is:

```text
frozen scientific evidence and artifacts
        -> methodological position
        -> argument architecture
        -> master plan
        -> frozen chapter authorities
        -> integrated manuscript
```

No later prose may silently override frozen evidence. No agent should generate
a complete Article V1 manuscript before the Formal Model/Methods, Results,
Discussion, literature framing, and appendix have each stabilized.

```text
ARTICLE_V1_ARGUMENT_ARCHITECTURE_FROZEN
```
