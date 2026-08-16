# Article V1 Parameter Rationale and Provenance Audit (Revision 2)

**Audit date:** 16 August 2026
**Repository:** `gifted-masking`
**Branch:** `codex/frontiers-stage2-e06`
**HEAD at audit start:** `d22febd83e7e2e5594faf3a2aa8c36aac42c6bfa`
**Worktree at audit start:** clean except the two untracked Revision-1 audit artifacts this document supersedes
**Document class:** documentation only. No experiment was run; no config, default, model semantic, artifact or claim was changed; no literature search was performed. Deterministic algebra, code/config/Git inspection, and re-reading of frozen summaries only.
**Governing authority:** `ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md`, then `ARTICLE_V1_STAGE1_PUBLICATION_FREEZE.md`, then `ARTICLE_V1_CLAIM_LEDGER.md`, then `ARTICLE_V1_ANALYTIC_RESULTS.md` and `ARTICLE_V1_LITERATURE_AUDIT.md`. Where this audit and those differ, they govern.
**Companion artifacts:** `ARTICLE_V1_PARAMETER_REGISTER.csv` (86 rows, 29 columns); `ARTICLE_V1_METHODOLOGICAL_POSITION.md`; `ARTICLE_V1_PARAMETER_AUDIT_CHANGELOG.md`.

**Relation to Revision 1.** This is a rewrite, not an appendix. Revision 1 recovered the provenance and mathematical structure correctly, but its justification taxonomy was conceptually too permissive: it allowed provenance labels and hybrid classes such as `PSYCHOLOGICALLY_INFORMED_REFERENCE`, `CONVENIENCE_REFERENCE` and `HISTORICAL_COMPARABILITY` to stand in for justification. Every conclusion affected by that confusion has been re-derived. The class-by-class mapping is in the changelog.

---

# 1. Executive judgment

## 1.1 The fundamental correction

> **Provenance is not justification.**

Terms such as

```text
INHERITED_LEGACY        IMPORTED
PRESENT_IN_INITIAL_COMMIT        MAINTAINED_DEFAULT
```

describe *where a value came from*. They say nothing about *why it is scientifically appropriate*. That `r = 2.0` appears verbatim in a preserved legacy script is a provenance fact and is not a reason for `2.0`. Where no independent numerical rationale exists, the exact value is an

```text
ARBITRARY_REFERENCE_VALUE
```

even when the *existence* of a rejection-cost parameter is well motivated. This audit therefore records, for every parameter and every substantive relation, four independent judgements: **provenance**, **exact-value justification**, **structural rationale**, and **qualitative-relation support**.

## 1.2 Seven findings that matter for the manuscript

**Finding 1 — no parameter is empirically calibrated, and the count is exactly zero.** The approved literature authority supports qualitative propositions and explicitly refuses quantitative ones for the two parameters where the temptation is greatest (`r` and `bf`). No study in the source ledger reports a quantity convertible into any model parameter. `EMPIRICALLY_CALIBRATED = 0` is the single most important number in this audit and must be stated in the manuscript rather than implied.

**Finding 2 — all unresolved rationale in Article V1 is structural, not numerical.** Of the 55 register rows carrying a free numerical value, **none** is classified `RATIONALE_UNKNOWN`; 27 are `ARBITRARY_REFERENCE_VALUE`, which is an acceptable status for a stylized model. All five `RATIONALE_UNKNOWN` items are *structural* assumptions — functional forms and transition architecture — where changing the assumption would change the model rather than move a coordinate. This is a cleaner and more actionable result than Revision 1's mixed list, and it relocates the project's genuine debt from the constants to the structure.

**Finding 3 — two structural assumptions were not flagged by Revision 1 and are flagged here.** Inspection of `src/gifted_masking/models/m2.py` shows (a) a single rejection from Neutral moves the learner to Stigmatized **with probability 1** — the transition is deterministic given the outcome, with no partial or graded consequence; and (b) a successful redemption attempt pays the **full** `b + a` and restores Accepted, i.e. recovery is complete and costless. The literature authority states that one rejection event may not be treated as a validated developmental transition, and `GIFT-03` is `CUT`. Both assumptions are recorded as `RATIONALE_UNKNOWN` with structural-ablation resolution paths. Neither defeats a current claim, because every E03 claim is already scoped to the frozen M2 transition model.

**Finding 4 — the experimental *designs* are far better justified than the model *constants*, and the strongest case is E05.** Prospective, written, theory-anchored reasons exist for the E01 `p` values, the E02 regime ladder, the E03 grid retention, the E04 abundance and identity controls, the five-master-seed rule, and above all the E05 dense `bf` interval, which was deliberately built around an exact analytic benchmark. Eight register rows are `THEORY_ANCHORED_DESIGN`; 34 carry a fully prospective documented chronology. The manuscript can defend its design far more strongly than its constants, which is the right way round.

**Finding 5 — `b = 1` is a reward unit only under conditions the project does not currently state.** The maintained learner is exactly invariant under `(R, q₀, τ) → (sR, sq₀, sτ)`, but only with `α`, `λ`, `γ` held fixed, *every* reward quantity rescaled, RNG streams fixed, and with the absolute `1e-10` Q tolerances explicitly excluded from the covariance. Full scale invariance must not be claimed without those conditions. See §10.

**Finding 6 — the E03 fraction is measure-relative and this must be disclosed.** `243/357` is a count of tested cells under a rectangle whose `η` upper bound and `0.05` step have no recovered justification. The freeze already forbids reading it as prevalence or phase-space volume; it does not yet say that the fraction depends on the grid's own bounds and resolution. One appendix sentence closes this.

**Finding 7 — E04 is a reference-environment result.** `p_good = .85` and `p_bad = .20` are inherited reference instantiations, and the prescribed `p_good`, `p_bad` and `τ` sensitivity blocks **were not executed**. E04 therefore demonstrates the phenomenon in one receptivity environment across a search-burden ladder and four representations; it does not demonstrate robustness across receptivity contrasts. This does not invalidate the frozen E04 result and requires no new experiment — only accurate scoping.

## 1.3 Disposition

**No current Article-V1 claim is defeated, and no `ARTICLE_V1_BLOCKER` was found.** Every claim that depends on an arbitrary reference value or an unresolved structural assumption is already scoped conditionally by the freeze and the claim ledger. Two disclosures must be added to the appendix (E03 measure-relativity; the five structural `RATIONALE_UNKNOWN` items). Full disposition in §29 and §31.

---

# 2. Scope, sources, and boundaries

## 2.1 Repository state recorded at audit start

```text
git rev-parse --show-toplevel   /Users/omer/workspace/personal/repos/gifted-masking
git branch --show-current       codex/frontiers-stage2-e06
git rev-parse HEAD              d22febd83e7e2e5594faf3a2aa8c36aac42c6bfa
git status --short              only the two untracked Revision-1 artifacts superseded here
```

## 2.2 Sources consulted

| Class | Source | Use |
|---|---|---|
| Governing | `ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md` | wording ceilings, estimand definitions, prohibited claims |
| Governing | `ARTICLE_V1_STAGE1_PUBLICATION_FREEZE.md` | frozen headline values, Stage-2 constraints |
| Governing | `ARTICLE_V1_CLAIM_LEDGER.md` | claim decisions and maximum defensible wording |
| Mathematical | `ARTICLE_V1_ANALYTIC_RESULTS.md` | every exact identity cited below; re-verified independently |
| Literature | `ARTICLE_V1_LITERATURE_AUDIT.md`, `ARTICLE_V1_SOURCE_LEDGER.csv` | the only permitted source of literature support |
| Interpretation | `ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md`, `ARTICLE_V1_E0*_INTERPRETATION.md` | gap register, acknowledged confounds |
| Design intent | `STAGE2_EXPERIMENT_SPECIFICATIONS.md`, `approvals/E0*` | the primary source of prospective rationale |
| Implementation | `src/gifted_masking/params.py`, `core.py`, `models/m0.py`–`m3.py`, `experiments/e03.py`–`e05.py` | source of truth for current values and rules |
| Configuration | `configs/frontiers_article/e0{1..5}_*_standard.json` | frozen executed grids |
| Historical | `simulations_old/simulations{1,2,3}/masking_rl.py`, `scripts/map_m2_lock_in_regions.py`, `AGENTS.md` | recovered origin of every default |
| Frozen results | `results/summaries/frontiers_*_v1_*.csv` | existing sensitivity evidence only; nothing recomputed |

`doc-reviews/frontiers_submission/*` is not an authority and was consulted only to record stale wording.

## 2.3 What this audit did not do

No experiment was rerun; no stochastic entry point was invoked; no seed, sweep or trajectory was generated; no config, default or model semantic was altered; no literature, web or ASTA search was performed; no frozen result was changed. The only computation performed was exact rational arithmetic over the frozen constants, which reproduces `ARTICLE_V1_ANALYTIC_RESULTS.md`, plus deterministic generation of the companion register.

## 2.4 Provenance recovery method, unchanged from Revision 1

The repository's Git history begins with a single squashed draft commit that already contains `params.py`, all five model modules, all four legacy simulation scripts and the pre-Stage-2 M2 mapping script; `git log -S`/`-G` on every payoff constant returns exactly that commit. Provenance was therefore recovered from the *preserved legacy sources inside* it, successfully: `simulations_old/simulations1/masking_rl.py` contains `DEF = dict(b=1.0, a=0.6, c=0.25, r=2.0)`, `AGENT = dict(alpha=0.1, temp=0.25, lam=1.0, q0=0.0)`, `run_m2(..., b2=0.5, r2=2.5, delta=0.02, gamma=0.9)`, `win = T // 5` and `Ks = [1, 2, 4, 8, 16, 32]`. Every current default is byte-for-byte that legacy value.

**Under the revised taxonomy this recovery is filed as provenance and carries no justificatory weight.** It remains valuable: it establishes that no derivation was lost, and it lets the appendix state the origin honestly.

---

# 3. The revised taxonomy

Four independent axes. Every register row carries a value on all four.

## 3.1 Axis A — provenance (descriptive only, never a justification)

| Value | Meaning |
|---|---|
| `INHERITED_LEGACY` | byte-identical to a preserved legacy script; no recorded derivation |
| `PROSPECTIVE_SPECIFICATION` | written into `STAGE2_EXPERIMENT_SPECIFICATIONS.md` or an approval record before execution |
| `FROZEN_CONFIG` | fixed in an executed frozen config |
| `IMPLEMENTATION_CONSTANT` | hard-coded in maintained source |
| `DERIVED_ANALYTIC` | a mathematical consequence recorded in the analytic authority |
| `RECOVERED_IN_AUDIT` | reconstructed here from values or code; never a design record |

Combinations are permitted and are written with `+`.

Companion axis — **rationale chronology**: `PROSPECTIVE_DOCUMENTED` (34 rows), `INHERITED_NO_RECORDED_RATIONALE` (29), `RETROSPECTIVE_CHARACTERIZATION` (14), plus 9 explicitly compound rows.

## 3.2 Axis B — exact-value justification (one per row)

| Class | Meaning | Rows |
|---|---|---|
| `EXACTLY_DERIVED` | not freely chosen; follows mathematically, conditional on its inputs | 10 |
| `EMPIRICALLY_CALIBRATED` | the literal value was estimated from external empirical observation | **0** |
| `THEORY_ANCHORED_DESIGN` | deliberately chosen relative to an analytic boundary or a theoretically meaningful regime | 8 |
| `COMPUTATIONAL_ESTIMATION` | chosen for precision, runtime, replication, convergence or uncertainty estimation | 10 |
| `ARBITRARY_REFERENCE_VALUE` | no independent quantitative justification; provides a reference instantiation of an otherwise defensible structure | 27 |
| `RATIONALE_UNKNOWN` | the numerical rationale is insufficient *and* the deficiency requires later scientific work | **0** |
| `NOT_APPLICABLE_STRUCTURAL` | the row is a structure or relation with no free numerical value | 31 |

`ARBITRARY_REFERENCE_VALUE` is **not automatically a methodological defect.** `RATIONALE_UNKNOWN` is reserved for genuine future-work debt and is never applied merely because a number is uncalibrated.

## 3.3 Axis C — structural rationale (one per row, including numerical rows)

Applies to the existence of a parameter, its sign, its functional form, an ordering, a structural transition, a model state, and an action architecture.

| Class | Rows |
|---|---|
| `WELL_MOTIVATED` | 49 |
| `PLAUSIBLE_FIRST_ABSTRACTION` | 30 |
| `WEAKLY_MOTIVATED` | 2 |
| `RATIONALE_UNKNOWN` | 5 |

## 3.4 Axis D — qualitative-relation support

| Class | Meaning | Rows |
|---|---|---|
| `LITERATURE_SUPPORTED` | the qualitative relation is supported by the approved literature authority | 17 |
| `MODEL_ASSUMPTION` | a deliberate modelling assumption with no literature claim attached | 18 |
| `PLAUSIBLE_FIRST_ABSTRACTION` | a defensible direction with no evidential backing for the relation itself | 9 |
| `RATIONALE_UNKNOWN` | no rationale recovered for the relation | 6 |
| `NOT_APPLICABLE` | derived quantities, controls and estimation settings | 36 |

## 3.5 The worked example that defines the taxonomy

```text
rejection-cost parameter r exists          STRUCTURAL:  WELL_MOTIVATED
relation r > 0                             QUALITATIVE: LITERATURE_SUPPORTED (perceived cost)
relation r substantially exceeds c         QUALITATIVE: PLAUSIBLE_FIRST_ABSTRACTION
exact value r = 2.0                        EXACT VALUE: ARBITRARY_REFERENCE_VALUE
origin of the number 2.0                   PROVENANCE:  INHERITED_LEGACY
```

Five separate judgements about one symbol. Collapsing any two of them — in either direction — is the error this revision exists to prevent.

---

# 4. Provenance is not justification: what changes in practice

Three concrete consequences.

**(a) Legacy origin never appears in a justification column.** The register is validated mechanically: any row whose `exact_value_justification` contains a provenance term fails the build. `INHERITED_LEGACY` appears only in `provenance` and `rationale_chronology`.

**(b) Continuity with earlier work is a reason to *retain* a grid, not a reason for the grid's shape.** Revision 1 classified the E03 rectangle as `HISTORICAL_COMPARABILITY`, which reads as a justification for the rectangle. It is not. The *retention decision* is prospectively documented and legitimate; the rectangle's `η ≤ 0.8` bound and `0.05` step remain unjustified, and the resulting cell fraction is measure-relative to them. Revised classification: exact value `ARBITRARY_REFERENCE_VALUE`, structural rationale `PLAUSIBLE_FIRST_ABSTRACTION`, claim status `DISCLOSE_CONDITIONALITY`.

**(c) "Psychologically informed" is split in two.** Revision 1's `PSYCHOLOGICALLY_INFORMED_REFERENCE` compressed a structural judgement and a numerical one into a single label, which made `r = 2.0` look partly justified. Under the revision the structural judgement lives on Axis C and the numerical one on Axis B, and they are reported separately in every table and count.

---

# 5. Numerical versus structural arbitrariness

This distinction is mandatory throughout the manuscript.

## 5.1 Numerical arbitrariness

*Example:* `r = 2` rather than `1.8`; `α = 0.1` rather than `0.12`; `p_good = .85` rather than `.83`.

Moving the value moves a coordinate. If the qualitative role of the parameter is justified and the claim is stated conditionally, this is **acceptable for an existence-and-reference model**. It requires disclosure, not remediation.

## 5.2 Structural arbitrariness

*Example:* redemption probability equal to exactly `p/2`; acceptance falling exactly linearly in disclosure; stigmatization occurring with probability 1 after a single rejection.

Changing the assumption **changes the model**, not a coordinate. A phenomenon that exists only because of a structurally arbitrary assumption is at risk of being an artifact of that assumption. These are the items that carry future-work debt.

## 5.3 The audit's separation, stated once

| | Numerical | Structural |
|---|---|---|
| Register axis | B (`exact_value_justification`) | C (`structural_rationale_status`) |
| Acceptable uncalibrated status | `ARBITRARY_REFERENCE_VALUE` (27 rows) | `PLAUSIBLE_FIRST_ABSTRACTION` (30 rows) |
| Genuine debt status | `RATIONALE_UNKNOWN` (**0 rows**) | `RATIONALE_UNKNOWN` (**5 rows**) |
| Correct response | accurate disclosure | future ablation, formal analysis or calibration |

**The whole of Article V1's unresolved rationale sits in the right-hand column.** That is the single most useful structural fact this revision produces.

---

# 6. `RATIONALE_UNKNOWN` as future-work debt

`RATIONALE_UNKNOWN` means:

> The scientific rationale for the numerical choice, functional form, structural assumption or relevant relation is currently insufficient, and this issue requires later investigation, sensitivity analysis, formal analysis or empirical calibration.

Every such row carries `resolution_needed`, `future_resolution_type` and `claim_dependency`. Permitted resolution types: `FORMAL_ANALYSIS`, `TARGETED_SENSITIVITY`, `EMPIRICAL_CALIBRATION`, `MODEL_COMPARISON`, `LITERATURE_REVIEW`, `IDENTIFIABILITY_ANALYSIS`, `STRUCTURAL_ABLATION`.

**None of this work is performed now.** The purpose of the label is to distinguish

```text
an acceptable arbitrary reference value
```

from

```text
an unresolved assumption requiring future scientific work.
```

The full list is in §29.

---

# 7. The scientific objective: existence and structure

Article V1 is an **existence-and-structure computational modelling paper**. It seeks to establish, in a sequence of simplified models:

```text
existence                 the divergence occurs
non-isolation             it is not confined to one finely tuned point
tested-region extent      it occupies substantial regions of the tested space
structural progression    it changes as specific structural features are added
meaningful contrast       it is measured against exact objective benchmarks
```

It is not a quantitatively calibrated psychological model, a population prevalence model, a parameter-estimation study, a complete formal characterization, or a fitted model of individual gifted children. Complete formal analysis of sets such as

```text
Theta_div = { theta : pi_learner(theta) != pi_objective(theta) }
```

is a legitimate future theoretical programme. **Article V1 has not computed the full set and must not claim to have done so.** The full position is in `ARTICLE_V1_METHODOLOGICAL_POSITION.md`, which this audit is the evidence base for.

---

# 8. Limits of quantitative calibration

The approved literature authority does not supply a common quantitative measurement system for the model's variables. There is no shared scale on which belonging, authenticity, concealment effort and rejection are commensurable, and no source in the ledger reports a quantity convertible into

```text
a  b  c  r  alpha  tau  lambda  delta  eta  p_good  p_bad  bf
```

as a literal psychological quantity. Therefore:

```text
EMPIRICALLY_CALIBRATED  =  0 of 86 register rows
```

The only rationale statement attached to the payoff constants anywhere in the repository is the legacy docstring header "Payoff primitives (all grounded in the literature review)". That claim attaches to the *primitives*, not the numbers, and the literature authority supports it only qualitatively. `AGENTS.md` lists the same four values as regression fixtures. **No document anywhere derives `0.6`, `0.25` or `2.0`.**

This audit does not manufacture calibration to fill the gap, and the manuscript must not either.

---

# 9. Literature-supported qualitative relations

Drawn **only** from `ARTICLE_V1_LITERATURE_AUDIT.md` and `ARTICLE_V1_SOURCE_LEDGER.csv`. No new searching was performed.

| Model relation | Literature status | Strength | What the literature does NOT establish |
|---|---|---|---|
| gifted students selectively disclose or conceal ability | **supported — the strongest gifted-specific anchor** | good (publisher-verified primaries) | prevalence, persistence, longitudinal course |
| `c > 0` — concealment has an ongoing cost | supported: visibility management is documented and described as effortful | moderate | any magnitude, any per-step rate, linearity in time |
| `r > 0` — adverse peer response is a cost | supported as *perceived* social pressure | moderate | `r = 2.0`; any causal effect of an objective rejection event on later concealment |
| `p_good ≠ p_bad` — receptivity varies by context | supported; among the better-evidenced parts | moderate–good | transition dynamics, the size of the contrast, equating "receptive" with "gifted classroom" |
| a comparison cost exists in high-achieving reference groups | supported as background (BFLPE) | good as motivation | that `bf` is a calibrated BFLPE measure or that `bf*` is a behavioural threshold for real students |
| adverse early feedback suppresses later sampling | supported **generically**; established prior art | good, but not novel | that this is novel or that it applies to human gifted development |
| access to compatible peers differs across contexts | supported for *preference*; a plausible mapping only for *search* | weak–moderate | systematic sequential search over unknown contexts |
| `a > 0` — authenticity has intrinsic value | **not listed among the authority's defensible propositions** | — | that authentic expression has a measurable positive utility |
| `r ≫ c` — rejection cost far exceeds concealment cost | **not established**; a plausible first abstraction | — | any ratio |
| persistent stigmatized state (M2) | **not established** | none | longitudinal persistence, metastability or irreversibility |

## 9.1 The distinction stated in the audit's own terms

```text
SUPPORTED:      social rejection can be experienced as costly, and some gifted youth
                deliberately conceal or manage the visibility of ability in response.
NOT SUPPORTED:  r = 2.0 is an empirical estimate of that cost.

SUPPORTED:      social environments differ in how receptive they are to visible ability.
NOT SUPPORTED:  p_good = .85 and p_bad = .20 are measured receptivity rates.

SUPPORTED:      being in a high-achieving reference group can carry a comparison cost.
NOT SUPPORTED:  bf is a calibrated BFLPE quantity, or bf* = 8/17 is a behavioural
                threshold for real students.

NOT SUPPORTED:  concealment persists longitudinally — therefore the ENTIRE M2
                transition system has no external empirical anchor.
```

## 9.2 The relations audited as the substantive hypotheses

| Relation | Classification | Register row |
|---|---|---|
| `a > 0` | `MODEL_ASSUMPTION` | `REL-A-POS` |
| `c > 0` | `LITERATURE_SUPPORTED` | `REL-C-POS` |
| `r > 0` | `LITERATURE_SUPPORTED` | `REL-R-POS` |
| `r ≫ c` | `PLAUSIBLE_FIRST_ABSTRACTION` | `REL-R-VS-C` |
| `r > b > a > c` | `MODEL_ASSUMPTION`, recovered retrospectively | `REL-ORDER` |
| `p_good > p_bad` | `LITERATURE_SUPPORTED` | `REL-PG-PB` |
| separation large enough to straddle `p*` | `PLAUSIBLE_FIRST_ABSTRACTION` | `REL-PG-PB-SEP` |
| `b₂ < b` | `PLAUSIBLE_FIRST_ABSTRACTION` | `REL-B2-B` |
| `r₂ ≥ r` | `PLAUSIBLE_FIRST_ABSTRACTION` | `REL-R2-R` |

**No exact quantitative ratio may be inferred from any of these.** The ordering `r > b > a > c` was recovered by this audit from the values and appears in no design document; the manuscript may present it as interpretable and may not present it as designed.

---

# 10. Reward scale, dimensionless formulation, and its exact conditions

## 10.1 The invariance, derived rather than assumed

From the maintained implementation only:

1. `core.subjective_value(R, λ) = R if R ≥ 0 else λR` is positively homogeneous: `φ_λ(sR) = s·φ_λ(R)` for `s > 0`.
2. The update `Q ← Q + α(φ_λ(R) − Q)` is linear in `(Q, φ_λ(R))`, so if `Q₀ → sQ₀` and every reward `R → sR` then `Q_t → sQ_t` at every step, pathwise, for the same random draws.
3. Proposition G3: `softmax(sQ, τ) = softmax(Q, τ/s)`.

Therefore the maintained learner is exactly invariant under

```text
(R, q0, tau)  ->  (sR, s*q0, s*tau)
```

## 10.2 The conditions, which must always be stated with the claim

- `s > 0`;
- `α`, `λ`, `γ` are dimensionless and are **not** rescaled;
- **every** reward-dimension quantity scales together, including `b, a, c, r, b₂, r₂, bf` and `q₀`;
- RNG streams are held fixed — the invariance is pathwise, not merely distributional;
- absolute numerical tolerances expressed in reward units — the `1e-10` value-iteration residual and Q-tie tolerances — are **not** scale-covariant, so the comparator's numerics are invariant only up to that tolerance.

**Do not claim full scale invariance without these.** Because the frozen `q₀ = 0` is itself scale-invariant, the only coupled quantity in practice is the temperature:

> `b = 1` sets the reward unit **if and only if** `τ` is read as `τ/b`.

## 10.3 The dimensionless quantities that matter

| Quantity | Value | Why it is the meaningful object |
|---|---|---|
| `a/b`, `c/b`, `r/b` | 0.60, 0.25, 2.00 | the substantive relative magnitudes |
| `(a+c)/(b+r)` | 17/60 | **the entire M0/M1 objective boundary**: `p* = 1 − this` |
| `τ/b` | 0.25 | exploration temperature relative to the reward unit |
| `Δ/τ` | cell-specific | **the only reward-side quantity entering the action rule** |
| `r/c` | 8.0 | the `r ≫ c` relation |
| `α·T` | 100–200 | horizon in learning time constants |
| `1/(1−γ)` | 10 steps | M2 planning horizon |
| `bf/b`, `bf/bf*` | design axis | comparison cost in payoff units and relative to the exact crossover |

## 10.4 `Δ/τ` as a behavioural reading of the design

Since the softmax odds ratio between two arms is `exp((Q_i − Q_j)/τ)` and each `Q` has its transformed-reward mean as conditional-mean fixed point, the asymptotic two-arm odds under continued sampling are `exp(Δ/τ)`:

| Cell | `Δ₀(p)` | `Δ₀/τ` | asymptotic two-arm odds |
|---|---|---|---|
| E02 `p = .65` | −0.20 | −0.80 | 0.45 : 1 (masking favoured) |
| E01/E02 `p = .75` | +0.10 | **+0.40** | **1.49 : 1** |
| E01/E02/E04 `p = .85` | +0.40 | +1.60 | 4.95 : 1 |
| E04 `p_bad = .20` | −1.55 | −6.20 | 0.002 : 1 |

**This is a retrospective mathematical characterization.** `STAGE2_EXPERIMENT_SPECIFICATIONS.md` justifies the E01 values by their position above `p* = 0.7167` and says nothing about temperature units. The manuscript may report the `Δ/τ` reading in the appendix as an explanation of the design's behavioural consequences; it may not present it as the prospective reason for the choices.

---

# 11. Identifiability

A new section, required because the model's parameters are unlikely to be separately inferable from behaviour.

## 11.1 What is established

- **Sum degeneracy.** The M0/M1 objective geometry depends on the four payoff constants only through `a + c = 17/20` and `b + r = 3`. `(a, c) = (0.6, 0.25)` and `(0.5, 0.35)` give identical M0 and M1 objective behaviour, as does any `(b, r)` with `b + r = 3`, subject to the sign regime `b − c ≥ 0`, `b + a ≥ 0`, `a − r < 0` that Propositions M0.3/M0.4 require.
- **Scale degeneracy.** By §10, absolute reward scale carries no independent behavioural meaning; only ratios and `Δ/τ` do.
- **Where the degeneracy breaks.** The individual constants re-enter through M2 (`b₂ − c` and `a − r₂`), through M3 (`b + a` and the `bf` subtraction point), and through the transient interaction of `q₀` with the absolute reward levels.

## 11.2 What follows

Observable choice depends primarily on combinations such as `ΔR/τ`. Different tuples of `(a, b, c, r, τ)` can generate similar behavioural distributions. Future empirical work should therefore expect to estimate

- dimensionless combinations,
- effective regimes,
- posterior parameter sets,

rather than unique literal psychological constants.

**This is not a flaw in the current paper.** It is an important methodological property of the modelling programme, and it is one reason the paper's claims are framed as existence and structure rather than as measurement. A complete identifiability analysis — which combinations are recoverable from which observables — has not been performed and is filed as future work (`IDENTIFIABILITY_ANALYSIS`).

## 11.3 An immediate appendix consequence

**The four raw payoff constants are over-parameterised relative to what the static objective geometry needs.** Reporting `(a, b, c, r)` as four independent quantities overstates how much the design determines. The appendix should present `(a/b, c/b, r/b, τ/b)` and note that only `((a+c)/(b+r), τ/b)` plus `p`, `p_good`, `p_bad` and `bf/b` are substantive for the static objective.

---

# 12. Payoff constants reclassified

## 12.1 The four-judgement table

| Parameter | Structural role | Qualitative rationale | Exact-value justification | Provenance |
|---|---|---|---|---|
| `b = 1.0` | value of belonging | positive belonging value: `LITERATURE_SUPPORTED`; structural `WELL_MOTIVATED` | `ARBITRARY_REFERENCE_VALUE` — a unit only jointly with `τ` | `INHERITED_LEGACY` |
| `a = 0.6` | intrinsic value of authentic expression | `MODEL_ASSUMPTION`; structural `PLAUSIBLE_FIRST_ABSTRACTION` | `ARBITRARY_REFERENCE_VALUE` | `INHERITED_LEGACY` |
| `c = 0.25` | ongoing cost of concealment | `LITERATURE_SUPPORTED`; structural `WELL_MOTIVATED` | `ARBITRARY_REFERENCE_VALUE` | `INHERITED_LEGACY` |
| `r = 2.0` | acute cost of a failed authentic display | `LITERATURE_SUPPORTED` (perceived); structural `WELL_MOTIVATED` | `ARBITRARY_REFERENCE_VALUE` | `INHERITED_LEGACY` |

**Deviation from the brief's expected form, and why.** The brief anticipated "positive authenticity value supported qualitatively" for `a`. The literature authority's own list of defensible propositions does not include intrinsic value of authentic expression; what it supports is that concealment is effortful and that adverse peer response is perceived as costly. `a > 0` is therefore recorded as a **modelling assumption**, not as qualitative literature support. This is the audit following the evidence rather than the template, as instructed.

## 12.2 Why `a > 0` is nonetheless load-bearing

`a > 0` makes the rejected payoff `a − r = −1.4` rather than `−2.0`, and with `c > 0` it gives `a + c > 0`, which is exactly the condition for M2 Accepted-state strict dominance (M2.2). An assumption that carries a structural theorem deserves to be labelled as an assumption rather than absorbed into the literature.

## 12.3 The reference relations, verified exactly

```text
b = 1        a = 3/5      c = 1/4      r = 2

r > b > a > c          TRUE   (2 > 1 > 0.6 > 0.25)
r >> c                 TRUE   (r/c = 8)
a > 0, c > 0           TRUE
a - r < 0              TRUE   (-1.4)   <- required by Props. M0.3/M0.4
b - c > 0              TRUE   (+0.75)
b + a > 0              TRUE   (+1.6)
```

**None of these inequalities is stated as a design constraint anywhere.** They are recovered here from the values. Their interpretation is defensible; their intentionality is not established.

## 12.4 The exact boundaries they produce

```text
Delta_0(p)  =  a + c - (1 - p)(b + r)  =  3p - 43/20          [Prop. M0.1]
p*_obj      =  1 - (a + c)/(b + r)     =  43/60 = 0.7166667    [Prop. M0.2]
p*_lambda   =  (15 + 28 lambda)/(32 + 28 lambda)               [Props. M0.3/M0.4]
bf*_GvsM    =  [p_good(b+a) + (1-p_good)(a-r) - (b-c)]/p_good  =  8/17   [Prop. M3.2]
bf*_GvsB    =  (p_good - p_bad)(b + r)/p_good                  =  39/17  [Prop. M3.4]
```

`p*_λ` at the tested values: `15/32` at `λ=0`, `29/46` at `λ=0.5`, `43/60` at `λ=1`, `5/6` at `λ=2.5`.

**`43/60` and `8/17` are reference-parameter realizations of general formulas, not psychological constants.** State the formula first and the number second, always labelled. `bf*` additionally depends on `p_good`, so it is a design-coupled quantity rather than a pure payoff quantity.

---

# 13. Learner constants reclassified

| | `α` | `τ` | `λ` (default) | `q₀` | `γ` |
|---|---|---|---|---|---|
| Reference | 0.1 | 0.25 | 1.0 | 0.0 | 0.9 (M2 only) |
| Exact-value class | `ARBITRARY_REFERENCE_VALUE` | `ARBITRARY_REFERENCE_VALUE` | **`THEORY_ANCHORED_DESIGN`** | `ARBITRARY_REFERENCE_VALUE` | `ARBITRARY_REFERENCE_VALUE` |
| Structural class | `PLAUSIBLE_FIRST_ABSTRACTION` | `PLAUSIBLE_FIRST_ABSTRACTION` | `WELL_MOTIVATED` | `PLAUSIBLE_FIRST_ABSTRACTION` | `PLAUSIBLE_FIRST_ABSTRACTION` |
| Provenance | `INHERITED_LEGACY` | `INHERITED_LEGACY` | `INHERITED_LEGACY` + `DERIVED_ANALYTIC` | `INHERITED_LEGACY` | `INHERITED_LEGACY` |
| Tested alternatives | {0.03, 0.3} E03 only | {0.1, 0.6} E03 only | {0.5, 2.5} E01 and E03 | {0.75} E03 only | {0.5, 0.99} E03 only |
| Dimensionless relation | `1/α = 10` steps | `Δ/τ` | `p*_λ` | `q₀/b = 0` | `1/(1−γ) = 10` steps |

## 13.1 `λ = 1` is the one learner constant with a genuine numerical anchor

`λ = 1` is exactly the identity transform and the unique value at which the learner-side boundary coincides with the objective boundary (`p*_λ = p*_obj`, Prop. M0.4). It is therefore `THEORY_ANCHORED_DESIGN` rather than arbitrary — with the honest qualification that the *recognition* of this property is retrospective; the value itself is inherited. The probe values `{0.5, 2.5}` are separately registered as `ARBITRARY_REFERENCE_VALUE` magnitudes within a `WELL_MOTIVATED` bracketing design.

**The reference learner is loss-*neutral*.** The legacy docstring calls `lam` "loss aversion", but the frozen default applies no transform at all. Every headline E01/E02/E04/E05 result comes from a loss-neutral agent. **Any Methods sentence implying the baseline agent is loss-averse would be factually wrong.**

## 13.2 `q₀ = 0` is not behaviourally neutral

It is the unique value fixed by the rescaling equivalence, but in the reward geometry it sits *below* the deterministic mask reward `R_M = 0.75` and *above* the rejected authentic reward `a − r = −1.4`. The first masking sample always raises `Q_M`; any early rejection always lowers `Q_A`. That asymmetry is part of the hot-stove setup and must be disclosed rather than presented as neutral. The single E03 probe at `q₀ = 0.75` (exactly `R_M`) left all six sentinel classifications unchanged.

## 13.3 `γ` belongs to both the learner and the comparator

At `γ = 0.5` three of the six E03 sentinels became `learner_matches_objective` — because *the objective policy changed*, not because learning improved. `γ` is the one learner constant that alters what counts as correct. The manuscript must preserve that distinction.

## 13.4 Timescales

| Quantity | Reference | Implied timescale |
|---|---|---|
| `α = 0.1` | learning rate | recency constant `1/α = 10` steps |
| `γ = 0.9` | discount (M2) | planning horizon `1/(1−γ) = 10` steps |
| `T = 2000` | E01/E02/E04/E05 | 200 learning time constants |
| `T = 1000` | E03 | 100 learning time constants and 100 planning horizons |
| final window `0.2·T` | all | 400 steps = 40 time constants (E01/E02/E04/E05) |

The horizon is long relative to both the learning and the planning timescales. The finite-horizon effects the project reports are therefore **not** artefacts of a horizon too short for the learner to settle in the ordinary sense; they arise from endogenous sampling suppression. **There is no authorized mapping from model steps to days, weeks, months or years anywhere in the repository**, and the manuscript must never imply one.

## 13.5 The final 20% window

Purely inherited and demonstrably so: all four legacy model runners compute `win = T // 5`. `RunParams.final_window_fraction = 0.2` is the same quantity re-expressed, and there is no theoretical motivation anywhere for one fifth. Classification: exact value `ARBITRARY_REFERENCE_VALUE`; structural `PLAUSIBLE_FIRST_ABSTRACTION` (it defines the estimand "behaviour by the end of the episode", which is a reasonable thing to want). The E03 check at `{0.1, 0.4}` left all six sentinel classifications unchanged in all five masters — genuinely reassuring, but six cells in one experiment using a classification outcome coarser than the continuous means the other experiments report. **It must not be oversold as general window-robustness.**

---

# 14. M1 reclassified

Six separable choices, previously compressed into two register rows.

| Choice | Structural class | Exact-value class | Treatment |
|---|---|---|---|
| graded disclosure as a concept | `WELL_MOTIVATED` / `LITERATURE_SUPPORTED` | n/a | **Methods** |
| grid must contain exactly 0 and 1 | `WELL_MOTIVATED` | n/a | appendix — it is what makes M1.2/M1.4 apply |
| acceptance decreasing in disclosure | `WELL_MOTIVATED` | n/a | Methods |
| five equally spaced levels `{0,.25,.5,.75,1}` | `PLAUSIBLE_FIRST_ABSTRACTION` | `ARBITRARY_REFERENCE_VALUE` | appendix |
| `base(d) = a·d − c·(1−d)` linear | `PLAUSIBLE_FIRST_ABSTRACTION` | n/a | appendix |
| **`q(d) = 1 − (1−p)d` exactly linear** | **`RATIONALE_UNKNOWN`** | n/a | appendix, as future-work debt |
| independent tabular arms | `WEAKLY_MOTIVATED` | n/a | **Methods, as a stated limitation** |

## 14.1 Why graded disclosure exists versus why exactly five equally spaced levels exist

These are different questions and the manuscript must separate them.

**The structural graded-action idea is well motivated.** Real self-presentation is not all-or-nothing, and the gifted literature's own vocabulary — information management, visibility management, minimizing visibility — is explicitly graded.

**The exact discretization is an arbitrary clean first discretization.** `disclosure_levels()` uses `np.linspace` and asserts the endpoints; the count `5` is the legacy default; equal spacing has no psychological interpretation recovered anywhere. **That is acceptable, and the audit states it plainly.** Only `2` and `5` were executed; the prescribed `{3, 9}` sensitivity was not run, so "binary versus graded" remains confounded with "2 arms versus 5 arms". `E02-05` is already `UNRESOLVED` and `E02-02`/`E02-03` are already `CUT`, so no current claim is defeated.

## 14.2 The linearity finding, restated as structural arbitrariness

`q(d)` linear *and* `base(d)` linear jointly imply `E[R(d)] = b − c + d·Δ₀(p)`, which is exactly why Proposition M1.2 gives an endpoint optimum. The endpoint theorem is presented in the analytic authority as a *result*; it is more accurately a *consequence of an undefended geometric choice*. A concave acceptance relation would produce interior optima and would change E02's entire interpretation.

Revision 1 called this a `CONVENIENCE_REFERENCE`. That understates it: the assumption is not a coordinate, it is the model's geometry. Revised classification `RATIONALE_UNKNOWN`, resolution `STRUCTURAL_ABLATION; FORMAL_ANALYSIS`, current action `DISCLOSE_CONDITIONALITY`.

Note the deliberate asymmetry with `base(d)`: proportional mixing of the authentic and concealed payoff components is a natural first interpolation, and it is classified `PLAUSIBLE_FIRST_ABSTRACTION`. Linearity of the *acceptance probability* has no comparable reading.

---

# 15. M2 transition assumptions reclassified

The section the brief singles out, and the one where the revision changes the most.

## 15.1 Each element judged separately

| Element | Exact-value class | Structural class | Note |
|---|---|---|---|
| `b₂ = 0.5` | `ARBITRARY_REFERENCE_VALUE` | `PLAUSIBLE_FIRST_ABSTRACTION` | sets the Stigmatized fallback `r_S(M) = 0.25` |
| `r₂ = 2.5` | `ARBITRARY_REFERENCE_VALUE` | `PLAUSIBLE_FIRST_ABSTRACTION` | gives `r_S(A) = −1.9 + 1.75p < 0.25` for all `p` |
| `δ = 0.02` | `ARBITRARY_REFERENCE_VALUE` | `PLAUSIBLE_FIRST_ABSTRACTION` | appears identically in **both** Accepted rows, which is why M2.2 holds for **any** `δ` |
| the redemption factor `1/2` | `ARBITRARY_REFERENCE_VALUE` | `PLAUSIBLE_FIRST_ABSTRACTION` | hard-coded; not a config parameter |
| **redemption probability = `p/2` (the form)** | n/a | **`RATIONALE_UNKNOWN`** | nothing motivates proportionality to `p` |
| **one rejection ⇒ Stigmatized w.p. 1** | n/a | **`RATIONALE_UNKNOWN`** | deterministic; no partial consequence |
| **redemption pays full `b + a` and restores Accepted** | n/a | **`RATIONALE_UNKNOWN`** | recovery is complete and costless |
| escape `η` is action-independent | n/a | `WEAKLY_MOTIVATED` | decouples recovery from behaviour |
| Accepted-state masking pays `b − c` | n/a | `PLAUSIBLE_FIRST_ABSTRACTION` | load-bearing for M2.2 |
| `γ = 0.9` | `ARBITRARY_REFERENCE_VALUE` | `PLAUSIBLE_FIRST_ABSTRACTION` | belongs to the comparator too |
| `η` as a swept dimension | n/a | `WELL_MOTIVATED` | sweeping is motivated *because* persistence is unestablished |

## 15.2 `δ = 0.02` is reclassified downward in severity

Revision 1 called `δ` the weakest-justified M2 constant and marked it `RATIONALE_UNKNOWN`. Under the revised taxonomy that is wrong: the *structural role* (acceptance is not permanent) is a defensible first abstraction, and the *analytic role* is `δ`-independent — `δ` appears identically in both Accepted-state action rows, which is precisely why M2.2 dominance holds for any `δ`. An uncalibrated magnitude whose structural role is defensible and whose analytic consequence does not depend on it is an ordinary `ARBITRARY_REFERENCE_VALUE`. **No current claim depends on `0.02`.**

## 15.3 `p/2` is reclassified upward in severity

Revision 1 marked the *value* `RATIONALE_UNKNOWN`. The brief is right that this understates the problem. The constant `1/2` is an ordinary arbitrary reference value; the **functional relation** is the serious item:

- nothing motivates recovery scaling *proportionally* with baseline receptivity;
- the form forces recovery probability to vanish as `p → 0`, so in unreceptive environments a stigmatized learner can never recover by acting — a substantive dynamical consequence of an unexamined choice;
- `p/2` is **hard-coded in `transition_step` and is not exposed as a configurable parameter**, so it has never been and currently cannot be varied without a code change.

Resolution path: `STRUCTURAL_ABLATION; FORMAL_ANALYSIS; EMPIRICAL_CALIBRATION`. **No such work is performed now.**

## 15.4 Two structural assumptions newly flagged

**(a) Deterministic stigmatization.** `src/gifted_masking/models/m2.py` sets `next_state[rejected] = STATE_STIGMATIZED` unconditionally: a single failed authentic attempt from Neutral always produces the labelled state. There is no probability of escaping unlabelled and no graded consequence. The literature authority states directly that the exact probability of rejection, the update strength after rejection and the persistence of a stigmatized state are theoretical model choices, and that one rejection event may not be treated as a validated developmental transition; `GIFT-03` is `CUT`. Determinism here is a stronger assumption than any of the numerical constants and had not been recorded anywhere.

**(b) Full-value redemption.** `reward[redeemed] = b + a` and `next_state[redeemed] = STATE_ACCEPTED`: a successful attempt while Stigmatized is rewarded exactly as if the label had never existed. This is asymmetric with the stigmatization side, which is deterministic and immediate, and it partly offsets the trap that `r₂ > r` creates. No rationale was recovered.

Both are `RATIONALE_UNKNOWN` with `STRUCTURAL_ABLATION` resolution paths, and both are `DISCLOSE_CONDITIONALITY` rather than blockers, because every E03 claim is already scoped to "the frozen M2 transition model".

## 15.5 What survives regardless of the transition constants

Two consequences are structural rather than value-dependent, and they are what the manuscript should lean on:

- **Accepted-state authenticity strictly dominates masking** for *any* `δ, γ, p, η, b₂, r₂`, provided `a + c > 0` (M2.2). This reduces the relevant policy set from 8 to 4.
- **The Neutral decomposition** `D_N(V) = Δ₀(p) + γ[p·V_A + (1−p)·V_S − V_N]` holds for any parameterization (M2.5). The *existence* of a dynamic term that can reverse the static ordering is the structural result; its size at the reference values is not.

The defensible framing is: **M2 asks what changes when the act of disclosure alters the future social situation rather than only the current payoff.** That question is well posed regardless of whether the specific transition constants are right.

## 15.6 The wording "persistent social consequences"

Accurate, but it conceals four specific assumptions a reader cannot recover from it: that stigmatized masking pays exactly `b₂ − c = 0.25`; that stigmatized rejection costs `r₂ = 2.5`; that recovery succeeds with probability exactly `p/2`; and that a single rejection stigmatizes with certainty while a single success restores full standing. **The appendix must expose all four, and must state that `p/2` is hard-coded rather than configurable.**

## 15.7 The single joint probe

The harsh sentinel `b₂ = 0, r₂ = 8, δ = 0.30, η = 0` at `p ∈ {.70, .75, .80}` moves three constants at once, so **no individual attribution is possible**. Results, consistent across all five masters:

| `p` | objective Neutral action | learned Neutral action | classification | objective Q gap |
|---|---|---|---|---|
| .70 | mask | mask | `learner_matches_objective` | −1.3027 |
| .75 | mask | mask | `optimal_policy_masking` | −0.4063 |
| .80 | authentic | mask | `learned_suboptimal_masking` | +0.1203 |

This is Level-1 point-existence evidence and is correctly labelled as a single boundary cell.

---

# 16. M3 structure reclassified

| Choice | Structural class | Qualitative support | Treatment |
|---|---|---|---|
| multiple heterogeneous contexts | `WELL_MOTIVATED` | `LITERATURE_SUPPORTED` | Methods |
| scarce receptive contexts (one good of `K`) | `WELL_MOTIVATED` | `LITERATURE_SUPPORTED` | Methods + **mandatory `1/K` appendix disclosure** |
| four action representations | `WELL_MOTIVATED` | n/a | Methods — the controls are the substance |
| **hierarchical dual update with the same reward** | **`RATIONALE_UNKNOWN`** | `RATIONALE_UNKNOWN` | appendix, as future-work debt |
| a comparison cost exists (`bf`) | `WELL_MOTIVATED` | `LITERATURE_SUPPORTED` | Methods, with explicit non-calibration |
| `bf` placement (accepted-only, good-context-only) | `PLAUSIBLE_FIRST_ABSTRACTION` | `MODEL_ASSUMPTION` | appendix, with the exact rule |

## 16.1 The `1/K` coupling — mandatory disclosure

In the one-good design the receptive fraction is exactly `1/K`:

| `K` | receptive fraction | joint arms (flat) |
|---|---|---|
| 1 | 100% | 2 |
| 2 | 50% | 4 |
| 4 | 25% | 8 |
| 8 | 12.5% | 16 |
| 16 | 6.25% | 32 |

Increasing `K` simultaneously increases the number of arms to search and decreases the prevalence of the receptive context. These cannot be separated within the one-good design; that is gap G-13 and it is why `E04-01` and `E04-02` are both `CUT`. The abundance regimes are the prospectively designed partial control and behave as expected.

## 16.2 The hierarchical dual update

`simulate_hierarchical` updates *both* the context Q-table and the behaviour Q-table with the *same* realized reward: the context value is credited with the behaviour's outcome. This is a substantive credit-assignment choice with no recovered rationale, and it is a plausible contributor to the much larger hierarchical `K` decline (`−0.4704` versus flat `−0.2340`) and to the E05 hierarchical left-censoring. **It is currently flagged nowhere else in the repository.**

Because `E04-03` is a `CANDIDATE` claim *about representation*, the claim survives conditionally — but the magnitude of the hierarchical decline may not be attributed to hierarchy as such. Resolution: `STRUCTURAL_ABLATION; MODEL_COMPARISON`.

## 16.3 `bf` placement analytics

Because `bf` is subtracted only on acceptance in the good context, `R_G(bf) = p_good(b + a − bf) + (1 − p_good)(a − r)` has slope `−p_good`, so `bf* = 0.40/0.85 = 8/17`. Had `bf` been applied unconditionally the slope would be `−1` and the crossover `0.40`. **The placement changes the exact threshold**, which is worth an appendix line.

---

# 17. E01 reclassified

| Choice | Exact-value class | Chronology | Note |
|---|---|---|---|
| primary `p ∈ {.75, .85}` | **`THEORY_ANCHORED_DESIGN`** | `PROSPECTIVE_DOCUMENTED` | spec: "both exceed the default objective threshold 0.7167" |
| maintained `p = .65` | `ARBITRARY_REFERENCE_VALUE` | `INHERITED` | config labels these cells `maintained_baseline` |
| `λ` default 1.0 | `THEORY_ANCHORED_DESIGN` | inherited value, retrospective reading | the exact no-transform point |
| `λ` probes `{0.5, 2.5}` | `ARBITRARY_REFERENCE_VALUE` | `PROSPECTIVE_DOCUMENTED` | bracketing design is what is motivated |
| forced authentic at step 0 | n/a (`WELL_MOTIVATED`) | `PROSPECTIVE_DOCUMENTED` | creates the controlled strata; makes the regret identity exact |
| forced-exploration rate 0.05 | `ARBITRARY_REFERENCE_VALUE` | prospective manipulation, inherited magnitude | `{2%, 10%}` prescribed, **not executed** |
| counterfactual feedback | n/a (`WELL_MOTIVATED`) | `PROSPECTIVE_DOCUMENTED` | information manipulation only |
| `n`, `T`, window | `COMPUTATIONAL_ESTIMATION` | tier table / inherited | `T ∈ {1000, 5000}` prescribed, **not executed** |
| master seeds | `COMPUTATIONAL_ESTIMATION` | `PROSPECTIVE_DOCUMENTED` with a stated reason | "the first three are the RDS minimum; seeds four and five expose fragility" |

## 17.1 The region rationale is prospective; the fine reading is retrospective

Exact arithmetic confirms both primary values lie above `p* = 43/60 = 0.716667`; the specification's prospective statement is correct as written. The values are therefore properly classified `THEORY_ANCHORED_DESIGN` — chosen relative to an analytic boundary.

The deterministic characterization in temperature units is valid:

```text
p = .75:   Delta_0 / tau  ~  +0.40    (asymptotic two-arm odds 1.49 : 1)
p = .85:   Delta_0 / tau  ~  +1.60    (asymptotic two-arm odds 4.95 : 1)
```

so one point is genuinely near the boundary and one genuinely more strongly authenticity-favouring — behaviourally as well as objectively. **This is a retrospective mathematical characterization.** The design documents justify the values by their position above `p*` and say nothing about temperature units. Present it in the appendix as an explanation, never as the prospective reason.

There is **no deeper reason** for `.75` and `.85` rather than `.74` and `.86`. They are round, evenly spaced probes on the authenticity-optimal side. Do not overjustify them.

## 17.2 The `p = .65` λ cells

`p*_λ(0.5) = 29/46 = 0.6304` and `p*_λ(2.5) = 5/6 = 0.8333`, so the maintained cells at `p = .65` sit **above** the subjective boundary for the low-`λ` arm and **below** it for the high-`λ` arm. The two arms are on opposite sides of the learner-side indifference point, which is precisely why the contrast is the largest effect in the frozen evidence base (`+0.402990`).

No document states this was the intent, and the config labels the cells `maintained_baseline`. Report the algebra in the appendix as an *explanation* of the effect size, never as the original reason.

## 17.3 Information-restoration controls

Both are model information manipulations, not human intervention estimates, and richer feedback as a remedy is established prior art. The single forced rate of 5% means **no dose-response statement is available**.

---

# 18. E02 reclassified

| Choice | Exact-value class | Chronology |
|---|---|---|
| `p ∈ {.65, .75, .85}` | `THEORY_ANCHORED_DESIGN` | **prospective**, with regime labels in the spec |
| `d` grid `{0,.25,.5,.75,1}` | `ARBITRARY_REFERENCE_VALUE` | inherited |
| `α, τ, λ, q₀` matched to E01 | as in §13 | inherited; the matching is prospective |
| `n = 500`, `T = 2000`, window `.2` | `COMPUTATIONAL_ESTIMATION` | prospective (tier) |
| architectures compared | 2 arms versus 5 arms | prospective |

## 18.1 Why `.65` was included

The specification is explicit and prospective: `.65` is the **mask-optimal** cell. `Δ₀(.65) = −0.20`, i.e. `−0.80 τ`, so masking is objectively correct there. The ladder therefore straddles the static objective boundary: one cell where masking is right, one just above the boundary, one comfortably above. Since Proposition M1.3 proves M0 and M1 share the same boundary, the ladder tests the same geometry in both architectures.

The **frozen headline pools only `p ∈ {.75, .85}` with equal weight**; `.65` is a design cell, not a headline cell.

## 18.2 The two questions, kept apart

**Why graded disclosure exists — Methods, `WELL_MOTIVATED`, `LITERATURE_SUPPORTED`.**

**Why exactly five equally spaced levels exist — appendix, `ARBITRARY_REFERENCE_VALUE`.** It is a clean first discretization. `np.linspace` guarantees the endpoints, which is what makes Proposition M1.2 applicable; that is the only defensible property of the spacing beyond convenience. **This is acceptable and the audit states it as such.**

---

# 19. E03 reclassified, and the measure-discipline requirement

## 19.1 The grid questions answered under the revised taxonomy

1. **Why does `p` cover `[0,1]`?** It is the complete admissible domain of a probability. A clear domain interpretation; unobjectionable.
2. **Why `.05` resolution?** No recorded reason. A round decimal step yielding 21 points, inherited from `scripts/map_m2_lock_in_regions.py`. **A design/grid-resolution choice**, classified `ARBITRARY_REFERENCE_VALUE`.
3. **Why does `η` end at `.8`?** **No recovered substantive justification.** The legacy figure swept `η ∈ [0, 0.2]`; the pre-Stage-2 mapping script widened it to `[0, 0.8]`. Nothing explains either the widening or the stopping point.
4. **Why `.05` in `η`?** Same as `p`: an unrecorded round step.
5. **Why was the rectangle retained?** **Prospectively and explicitly** — the specification says the exact-grid replication "preserves comparability with 226/357". The *retention decision* is documented and legitimate; it does not justify the rectangle's shape.
6. **Does the rectangle represent a distribution of real environments?** **No.** It is a tested set, and equal-weight cell counting induces an arbitrary grid measure.

## 19.2 The measure-dependence of `243/357`

`243/357 = 0.6808` is a **count of tested cells**, relative to the rectangle `[0,1] × [0,0.8]` at step `.05` with uniform spacing. Under a different rectangle the same underlying result would produce a different fraction: extending `η` to 1.0 adds four rows; using step `.025` quadruples the cell count without adding information; restricting `p` to `[0.3, 1.0]` removes most of the low-`p` cells where the learner matches the objective.

```text
243/357  IS      tested-grid coverage under the frozen rectangular grid
                 and its uniform counting measure
243/357  IS NOT  population prevalence
                 natural parameter-space volume
                 a probability that masking occurs
                 prevalence among gifted children
```

**Required appendix sentence:**

> The reported cell fraction depends on the prespecified grid bounds and resolution and should not be interpreted as prevalence or as a natural measure of parameter-space volume.

The freeze already forbids prevalence and phase-space readings; it does not yet state the measure-relativity. This sentence closes that gap. The claim itself — `E03-01 / CANDIDATE`, wording fixed at "243 of 357 tested cells" — survives unchanged.

**The scientifically stronger result available from the same evidence:**

> the learned/objective mismatch occurs over a substantial, structured region of the tested plane rather than at isolated cells.

## 19.3 Why `η` is an appropriate dimension to vary

`η` is the only parameter controlling how *persistent* the Stigmatized state is, and persistence is the entire structural novelty candidate for M2 (`E03-06 / CANDIDATE`). Varying it spans the qualitative range from a permanent label (`η = 0`) to a rapidly escapable one (`η = .8`). Sweeping it is `WELL_MOTIVATED` **precisely because** the literature does not establish persistence: the model spans the range rather than asserting a value. The frozen threshold refinement shows the objective threshold falling across the three refined values (`.384 → .339 → .269`), which is the expected direction, though the analytic authority correctly refuses to claim monotonicity as a theorem.

## 19.4 Other E03 choices

| Choice | Value | Exact-value class |
|---|---|---|
| `n` per cell | 160 | `COMPUTATIONAL_ESTIMATION` |
| `T` | 1000 | `COMPUTATIONAL_ESTIMATION` |
| window | 0.2 | `ARBITRARY_REFERENCE_VALUE` |
| stability rule | ≥ 4 of 5 seeds | `ARBITRARY_REFERENCE_VALUE` (prospectively fixed convention) |
| visit adequacy | total ≥ max(100, n) and children ≥ max(16, 0.2n) | `COMPUTATIONAL_ESTIMATION` |
| VI tolerance | `1e-10`, max 100 000 iterations | `COMPUTATIONAL_ESTIMATION` (validated to `8.99e-10`) |
| objective bisection tolerance | `1e-4` (achieved `6.1e-05`) | `COMPUTATIONAL_ESTIMATION` |
| learned refinement target width | `0.0125` | `COMPUTATIONAL_ESTIMATION` |

`n = 160` is inherited from the mapping script and has a visible consequence: seven cells (all `η = 0`, `p ≤ 0.30`) fail the visit-adequacy rule and are correctly reported as inconclusive rather than forced into a regime.

---

# 20. E04 reclassified

| Choice | Exact-value class | Structural class |
|---|---|---|
| `K ∈ {1,2,4,8,16}` | `ARBITRARY_REFERENCE_VALUE` | `WELL_MOTIVATED` |
| `p_good = 0.85` | `ARBITRARY_REFERENCE_VALUE` | `WELL_MOTIVATED` |
| `p_bad = 0.20` | `ARBITRARY_REFERENCE_VALUE` | `WELL_MOTIVATED` |
| one-good design | n/a | `WELL_MOTIVATED` (with the `1/K` confound) |
| abundance regimes | `THEORY_ANCHORED_DESIGN` | `WELL_MOTIVATED` |
| identity mode | `THEORY_ANCHORED_DESIGN` | `WELL_MOTIVATED` |
| four architectures | n/a | `WELL_MOTIVATED` |
| `n`, `T`, window | `COMPUTATIONAL_ESTIMATION` | `WELL_MOTIVATED` |

## 20.1 `p_good` and `p_bad` are reference instantiations

Both are legacy defaults. `p_good = .85` is the same value as the E01 comfortable cell, itself unjustified beyond being a round number above the boundary.

**The substantive assumption is `p_good > p_bad`**, with a separation large enough that one context is clearly receptive and the others clearly unreceptive under the reference payoff system. That placement is analytically verifiable:

```text
p*        = 43/60 = 0.716667
Delta_0(.85)   = +0.40   ->  good context is authenticity-optimal   (+1.60 tau)
Delta_0(.20)   = -1.55   ->  bad contexts are masking-optimal       (-6.20 tau)
R_M = 0.75      R_G(0) = 1.15      R_B = -0.80
```

**The exact magnitudes are uncalibrated.** The literature supports the ordering, not the size of the contrast.

## 20.2 The unexecuted sensitivity, and what follows

The specification prescribed `p_good ∈ {.70, .85, .95}`, `p_bad ∈ {.05, .20, .40}` and `τ ∈ {.1, .25, .6}` on `K ∈ {2, 8, 16}`. **None was executed**; the frozen manifest records `"sensitivity": "frozen separately unauthorized; baseline-only standard config"`. E04 therefore has **zero** parameter sensitivity for its two defining receptivity constants and for temperature.

> **E04 is a reference-environment result, not demonstrated global robustness across receptivity contrasts.**

This does not invalidate the frozen E04 result. It fixes its scope. **Robustness may never be implied from an unexecuted specification.**

---

# 21. `K` reclassified

`K = {1, 2, 4, 8, 16}` is an **arbitrary but efficient design choice**: exact-value class `ARBITRARY_REFERENCE_VALUE`, structural class `WELL_MOTIVATED`.

What matters structurally is increasing

```text
search-space size    2K  =  2, 4, 8, 16, 32
```

and, in the one-good design,

```text
receptive-context scarcity  =  1/K  =  100%, 50%, 25%, 12.5%, 6.25%
```

**Evidence on the powers-of-two question.** *For:* the frozen effects file reports `..._slope_log2K_...` as a primary statistic, so the analysis treats `K` as log-uniform, and `log₂K = 0..4` is exactly evenly spaced. *Against:* the legacy source is a bare `Ks = [1,2,4,8,16,32]` with no comment, and the Stage-2 specification says only "K curve | 1, 2, 4, 8, 16" without justification; the truncation from 32 to 16 is unexplained.

**Verdict.** The manuscript may say the ladder *spans* search-space size approximately logarithmically. It may not say the ladder was *designed* for that purpose, and **it may not dress powers of two up as psychologically natural group counts.**

---

# 22. E05 reclassified

| Choice | Exact-value class | Note |
|---|---|---|
| `K = 4` | `ARBITRARY_REFERENCE_VALUE` | a mid-ladder point; never varied within E05 |
| good-context identity fixed at 0 | `THEORY_ANCHORED_DESIGN` | comparability |
| dense `bf` interval `0.30 : 0.025 : 0.65` | **`THEORY_ANCHORED_DESIGN`** | the strongest numerical design justification in the paper |
| anchors `0`, `8/17`, `0.80` | `THEORY_ANCHORED_DESIGN` | endpoint and exact-indifference references, excluded from the fit |
| crossing criterion `0.5` | `ARBITRARY_REFERENCE_VALUE` | a descriptive operational definition |
| nonincreasing equal-`n` PAVA fit | `COMPUTATIONAL_ESTIMATION` | prespecified, dependency-free |
| bootstrap 10 000 resamples of five master curves | `COMPUTATIONAL_ESTIMATION` | uncertainty quantification only |

## 22.1 Separate the reference payoff choice from the experimental range

This separation is the key to E05 and the audit makes it explicit.

**The reference payoff values that make `bf* = 8/17` are uncalibrated.** `bf*` depends on `b, a, c, r` and on `p_good`, every one of which is an arbitrary reference value.

**But once that reference model is fixed, bracketing its exact threshold is a strongly justified design choice.** The specification says the grid should include "the analytic threshold between grid points"; the approval record confirms `[.30, .65]` is "the decision-bearing dense range … including the exact threshold anchor", and that `0` and `.80` "cannot create an in-range crossing". In objective-advantage units the interval is close to symmetric about `bf*`:

```text
Delta_obj(bf)  =  0.40 - 0.85 * bf
Delta_obj(.30)   = +0.1450  = +0.58 tau
Delta_obj(8/17)  =  0        (exact tie at 0.75)
Delta_obj(.65)   = -0.1525  = -0.61 tau
```

So the dense range spans roughly `±0.6` temperature units of objective advantage around exact indifference — a principled bracket, not an arbitrary window.

**The bracket nevertheless proved too narrow on the left.** The hierarchical response was already `0.1176` at `bf = .30`, giving `no_crossing_below` and `0/10 000` valid bootstrap crossings. The bracket was designed around the *objective* threshold and the hierarchical learner's behavioural crossing lies well below it. This is correctly reported as **left-censored, not absent globally** (`E05-05 / CUT`).

## 22.2 Separate the analytic crossover from the empirical `0.5` crossing

| | Objective threshold | Behavioural crossing |
|---|---|---|
| Quantity | `bf*` where `R_G(bf) = R_M` | `bf` where the across-child modal-arm fraction crosses 0.5 |
| Value | `8/17 = 0.470588` | `0.312852`, bootstrap `[0.307836, 0.316918]` |
| Type | exact analytic | simulation estimate, PAVA-fitted |
| Depends on | `b, a, c, r, p_good` | additionally on `τ, α, q₀, λ, K, n, T`, window, architecture |
| Criterion | reward equality | **a chosen 0.5 cut on a classification fraction** |

**`0.5` is a descriptive operational definition.** It is the conventional midpoint of a `[0,1]` response, it is not psychologically privileged, and **no softmax identity governs it**: Proposition G2 (`π_A = 0.5 ⟺ Q_A = Q_M`) applies to a *two-action softmax probability*, whereas E05 measures the across-child fraction whose final-window *modal arm* is one specific arm in an *eight-action* policy. That mismatch is the standing BLOCKER. A different criterion (0.25 or 0.75) would report a different crossing location from the same frozen data, and the design does not identify which, if any, criterion is privileged. Say so plainly.

---

# 23. Three levels of evidence applied

| Result | Level | Qualification |
|---|---|---|
| M0/M1 objective boundary formula `p* = 1 − (a+c)/(b+r)` | **3** | general in the parameters |
| M1 affine disclosure objective and endpoint optimum | **3** | *conditional on the linear acceptance relation* (§14.2) |
| M1 action-count invariance of the objective optimum | **3** | any grid containing 0 and 1 |
| M2 Accepted-state strict dominance | **3** | any `δ, γ, p, η, b₂, r₂` with `a + c > 0` |
| M2 Neutral static-plus-dynamic decomposition | **3** | parameter-free in form |
| M2 Bellman comparator and its uniqueness | **3** | conditional on the frozen transition *structure* |
| M3 `K`-invariance of the full-information optimum | **3** | under the frozen one-good-context structure |
| general comparison-cost crossover formula | **3** | general in the parameters |
| reward-scale/temperature coupling | **3** | under the conditions in §10.2 |
| `p* = 43/60`, `bf* = 8/17`, `39/17`, `.384/.339/.269` | reference realizations | exact given uncalibrated inputs; **not** Level-3 facts about the world |
| E01 controlled contrasts | **1** | two `p` cells, one learner setting |
| E01 `λ` contrast | **1–2** | three `λ` values at two `p` cells |
| E02 architecture contrast | **1–2** | three `p` cells, two level counts |
| E03 grid result | **2 in `(p, η)`** | **Level 1 in every other parameter**: payoffs, learner constants, M2 transition constants all at a single reference coordinate |
| E03 sentinel sensitivity | **1** | six of 357 cells |
| E03 harsh sentinel | **1** | one labelled cell, three constants moved jointly |
| E04 `K` decline | **2 in `K` and across four representations and three abundance regimes** | **Level 1 in receptivity** (`p_good`/`p_bad` never varied) and in every learner constant |
| E05 crossing | **2 in `bf`** | **Level 1 in `K`, `τ`, architecture and criterion** |

**Two rules follow.**

1. A Level-2 result is Level 2 *only along the swept dimensions*. Every unswept parameter leaves the same result at Level 1 with respect to that parameter. This qualification is mandatory wherever tested-region language is used.
2. **Simulation findings may never be promoted to Level 3.** Every reported magnitude and location is a reference-parameter result.

---

# 24. Sensitivity: done versus not done

## 24.1 The required matrix

| Parameter | Exact value arbitrary? | Existing variation? | Claim conditional? | Future work needed? |
|---|---|---|---|---|
| `b, a, c, r` | yes | **none** | yes — all region claims | flagged only; disclosure suffices |
| `τ` | yes | E03 only, 6 cells | yes — E03 explicitly; E05 BLOCKER names it | flagged (E04/E05 have none) |
| `α` | yes | E03 only, 6 cells | yes — E03 explicitly | flagged |
| `λ` | default is theory-anchored | **E01 and E03, by design** | no — `λ` is a probe | none |
| `q₀` | yes | E03 only, 6 cells (unchanged) | no | none |
| `γ` | yes | E03 only (comparator moves) | yes — E03 explicitly | none |
| `b₂`, `r₂`, `δ` | yes | **one joint probe only** | yes — scoped to the frozen M2 model | flagged; individual probes never specified |
| redemption `p/2` | value yes; **form is RATIONALE_UNKNOWN** | **none, and not configurable** | yes | **required future work** |
| deterministic stigmatization | n/a; **RATIONALE_UNKNOWN** | **none** | yes | **required future work** |
| full-value redemption | n/a; **RATIONALE_UNKNOWN** | **none** | yes | **required future work** |
| M1 linear acceptance | n/a; **RATIONALE_UNKNOWN** | **none** | yes | **required future work** |
| M1 level count | yes | 2 versus 5 only | yes | **planned `{3,9}` NOT executed** |
| hierarchical dual update | n/a; **RATIONALE_UNKNOWN** | **none** | yes | **required future work** |
| `p_good`, `p_bad` | yes | **none** | yes | **planned NOT executed** |
| `K` | yes | 1–16 ladder | yes | none |
| `bf` | range theory-anchored | dense sweep | yes | none |
| E05 criterion `0.5` | yes | **none** | yes | flagged (`TARGETED_SENSITIVITY`) |
| E01 forced rate | yes | **none** | yes | **planned `{2%,10%}` NOT executed** |
| `n` | no (computational) | E03 `n=320` unchanged | no | none |
| `T` | no (computational) | E03 `{2000,5000}` | yes — finite horizon by design | **E01 `{1000,5000}` NOT executed** |
| final window | yes | E03 `{0.1,0.4}` unchanged | no | none |
| analytic invariance | — | `λ`-boundary, M2.2, M3.1, reward scale | — | available *instead of* sweeps for these |

## 24.2 The four categories, kept apart

```text
ALREADY TESTED            lambda (E01/E03), alpha, tau, q0, gamma, n, T, window (E03 six cells);
                          K, bf, abundance, identity, architecture, modal-tie handling
PLANNED BUT NOT EXECUTED  E01 T {1000,5000}; E01 forced rate {2%,10%};
                          E02 levels {3,9}; E04 p_good/p_bad/tau; E05 T=5000
NEVER PLANNED             b, a, c, r; individual b2/r2/delta; redemption p/2;
                          M1 acceptance form; hierarchical credit assignment;
                          E05 criterion; K > 16
ANALYTIC INVARIANCE       M2.2 holds for any delta/gamma/p/eta/b2/r2 given a+c>0;
                          M3.1 K-invariance; M1.4 action-count invariance;
                          reward-scale equivalence (under the section 10.2 conditions)
```

**Do not imply robustness from an unexecuted specification.** The honest framing, verbatim:

> A one-at-a-time sensitivity block was run for E03 only, on six prespecified cells of the 357-cell grid, varying `n`, `T`, final-window fraction, `α`, `τ`, `λ`, `q₀` and `γ`. Classifications were unchanged under `n`, `T`, window, `q₀` and `λ`; `α`, `τ` and `γ` changed specific sentinels, and the `γ` change was a change in the objective comparator rather than in learning. The remaining experiments were executed at the frozen learner settings only.

---

# 25. Tested-region versus prevalence language

The word **prevalent** is prohibited for model phenomena, because no probability measure over parameter space is defined. Permitted formulations:

```text
occurs across substantial regions of the tested model space
occurs broadly across tested simplified learner regimes
is not confined to a single finely tuned parameter point
tested-grid coverage
```

Five quantities routinely confused, and kept distinct throughout:

| Quantity | What it is |
|---|---|
| many learners within a fixed parameter cell | `n` simulated learners; **not** the inferential unit (freeze C.1) |
| many tested parameter cells | coverage of a prespecified grid under its counting measure |
| many independently seeded replications | five master seeds; the inferential replicate unit, df = 4 |
| natural parameter-space prevalence | would require a measure over parameter space — **not defined anywhere** |
| real-world population prevalence | would require empirical sampling of people — **not attempted** |

---

# 26. Methods versus appendix treatment

## 26.1 What the Methods chapter should say

For each component: why it exists; what qualitative phenomenon it abstracts; why it is an appropriate minimal first abstraction; what comparison is being made; what exact mathematical relations define the relevant regimes. **The Methods should not attempt to justify every literal constant.**

Four statements are mandatory in Methods rather than the appendix:

- disclosure levels are represented as **independent actions**, so the learner does not generalize across neighbouring levels;
- the M2 states are **abstractions, not measured psychological states**, and persistence is not established by the literature;
- the comparators are **full-information oracles** and no claim is made about the best policy attainable under the learner's own information constraints;
- the baseline learner is **loss-neutral**; asymmetric weighting appears only as an explicit manipulation.

Plus, once and plainly: payoffs are normalized reference values, no parameter in the work is empirically calibrated, and exact values are in the appendix.

## 26.2 What must move to the parameter appendix

For every numerical parameter: `value`, `role`, `provenance`, `exact-value justification`, `qualitative rationale`, `existing sensitivity`, `analytic consequences`, `future calibration status`.

Specifically, the appendix must carry:

- **A.** exact defaults — `b, a, c, r`; `α, τ, λ, q₀, γ`; `b₂, r₂, δ`, redemption `p/2` (hard-coded); `p_good, p_bad`, `bf = 0` in E04.
- **B.** exact ranges and grids for E01–E05, including the harsh sentinel and the E05 anchors.
- **C.** exact structural probabilities — M1 `q(d)`; the full M2 transition table including `(1−p/2)η`, `p/2`, the deterministic stigmatization and the full-value redemption; M3 `p_vec`, the `bf` placement rule, `1/K`, `ceil(K/4)`.
- **D.** the scale-equivalence with **all** conditions from §10.2, then the dimensionless table.
- **E.** the historical-origin paragraph, labelled as provenance and explicitly not as justification.
- **F.** the taxonomy, defined once, with the counts of §28 — **including that no parameter is `EMPIRICALLY_CALIBRATED`**.
- **G.** the §9 literature table including the "what the literature does NOT establish" column. This is the single most important defensive element of the appendix.
- **H.** the §24 sensitivity matrix, the four categories, and the honest-framing paragraph.
- **I.** analytic consequences — general formulas first, reference realizations second — plus the `Δ/τ` table and the E05 bracket symmetry.
- **J.** caveats: no real-time mapping; `243/357` is measure-relative; the `0.5` criterion is conventional; `p/2` is not configurable; the unexecuted sensitivity blocks; the E05 hierarchical left-censoring; the `1/K` coupling; the five structural `RATIONALE_UNKNOWN` items.

Acceptable and expected wording throughout:

> Exact numerical value not empirically calibrated; retained as an arbitrary reference instantiation.

**Do not treat this phrase as an embarrassment.** It is the correct description of a stylized model.

---

# 27. The decision rule applied

## 27.1 No immediate action required when

- the exact value is arbitrary; **and**
- the structural assumption is defensible; **and**
- the claim is explicitly conditional or reference-model based; **and**
- the result demonstrates the intended phenomenon without claiming calibration.

**38 register rows meet this test** (`NO_CHANGE_REQUIRED`).

## 27.2 Future-work flag when

- a functional form is poorly motivated; **or**
- the phenomenon might be an artifact of a structurally arbitrary assumption; **or**
- the claim currently generalizes beyond the tested reference parameterization; **or**
- empirical calibration would materially change interpretation.

**48 register rows are `DISCLOSE_CONDITIONALITY`**, of which five carry genuine `RATIONALE_UNKNOWN` debt.

## 27.3 Article-V1 blocker when

> a current central claim cannot be defended even conditionally without assuming an unsupported structural relation.

**No such case was found.** The three candidates were examined explicitly:

**Candidate 1 — E03 and the M2 transition assumptions.** `E03-01` (`CANDIDATE`) asserts that aggregate final-window Neutral behaviour can favour masking while full-information DP favours authenticity. It depends on the deterministic-stigmatization, `p/2`-redemption and full-value-restoration assumptions. **Not a blocker:** the claim is already scoped to the frozen M2 transition model, the wording is fixed at "243 of 357 tested cells", and the phenomenon is asserted as *can occur in this model*, not as a general property. Conditional defence succeeds.

**Candidate 2 — E02 and the linear acceptance relation.** The endpoint-optimum theorem follows from an undefended geometric choice. **Not a blocker:** `E02-04` (a strictly optimal intermediate level) is already `CUT`, `E02-05` is `UNRESOLVED`, and the surviving E02 claims are about resampling behaviour under two action architectures, not about the endpoint geometry being a general truth.

**Candidate 3 — E05 and `τ`.** `E05-C7-CROSSING` reports a behavioural crossing at `0.312852` against an objective crossover at `8/17`, with `τ` never varied in E05 and named among the unresolved contributors. **Not a blocker:** this is already the freeze's position (`E05-01 / KEEP` as descriptive, `E05-02 / CUT`, `E05-03 / UNRESOLVED`, BLOCKER open). The arbitrariness is numerical, not structural; the existing wording ceiling handles it. The appendix must add that `τ` is unprobed in E05 specifically.

**No new experiment is proposed by this audit. The correct response to a weakly justified value is accurate disclosure, not a new sweep.**

---

# 28. Required audit summary — counts

Counts are over the 86 rows of `ARTICLE_V1_PARAMETER_REGISTER.csv` and are reported **separately** by axis, never combined.

## 28.1 Exact-value justification

```text
EXACTLY_DERIVED                 10
EMPIRICALLY_CALIBRATED           0
THEORY_ANCHORED_DESIGN           8
COMPUTATIONAL_ESTIMATION        10
ARBITRARY_REFERENCE_VALUE       27
RATIONALE_UNKNOWN                0
--------------------------------------
numerical rows                  55
NOT_APPLICABLE_STRUCTURAL       31
--------------------------------------
total                           86
```

## 28.2 Structural rationale

```text
WELL_MOTIVATED                  49
PLAUSIBLE_FIRST_ABSTRACTION     30
WEAKLY_MOTIVATED                 2
RATIONALE_UNKNOWN                5
--------------------------------------
total                           86
```

## 28.3 Qualitative-relation support

```text
LITERATURE_SUPPORTED            17
MODEL_ASSUMPTION                18
PLAUSIBLE_FIRST_ABSTRACTION      9
RATIONALE_UNKNOWN                6
NOT_APPLICABLE                  36
```

## 28.4 Provenance and chronology

```text
provenance includes INHERITED_LEGACY            43 rows
provenance includes PROSPECTIVE_SPECIFICATION   32 rows
provenance includes DERIVED_ANALYTIC            11 rows
provenance includes RECOVERED_IN_AUDIT          10 rows
provenance includes IMPLEMENTATION_CONSTANT     11 rows
provenance includes FROZEN_CONFIG                6 rows

(rows may carry a compound provenance, so these do not sum to 86)

rationale_chronology PROSPECTIVE_DOCUMENTED             34
rationale_chronology INHERITED_NO_RECORDED_RATIONALE    29
rationale_chronology RETROSPECTIVE_CHARACTERIZATION     14
rationale_chronology compound                            9
```

## 28.5 Current claim status

```text
NO_CHANGE_REQUIRED         38
DISCLOSE_CONDITIONALITY    48
NARROW_CLAIM                0
ARTICLE_V1_BLOCKER          0
```

**The empty `EMPIRICALLY_CALIBRATED` row and the empty `ARTICLE_V1_BLOCKER` row are the two most important lines in this section.**

---

# 29. Required unresolved-rationale table

All five `RATIONALE_UNKNOWN` items, plus the two `WEAKLY_MOTIVATED` items recorded for completeness.

| Choice | Why unresolved | Current claim impact | Current action | Future resolution |
|---|---|---|---|---|
| **M1 acceptance `q(d) = 1 − (1−p)d`** | monotone exposure is motivated; exact linearity is not, and it is what *produces* the endpoint-optimum theorem | the affine-reward framing of E02; `E02-04` already `CUT`, `E02-05` `UNRESOLVED` | `DISCLOSE_CONDITIONALITY` | `STRUCTURAL_ABLATION` (concave/convex acceptance); `FORMAL_ANALYSIS` |
| **M2 deterministic stigmatization after one rejection** | no rationale recovered; the literature refuses to treat one rejection as a validated transition; `GIFT-03` `CUT` | the E03 dynamic comparator and the geometry behind `243/357`; already scoped to the frozen M2 model | `DISCLOSE_CONDITIONALITY` | `STRUCTURAL_ABLATION` (probabilistic/graded stigmatization); `EMPIRICAL_CALIBRATION` |
| **M2 redemption probability `= p/2`** | nothing motivates proportionality to `p`; the form forces recovery to vanish as `p → 0`; hard-coded and not configurable | the E03 dynamic comparator; the phrase "persistent social consequences" | `DISCLOSE_CONDITIONALITY` | `STRUCTURAL_ABLATION`; `FORMAL_ANALYSIS`; `EMPIRICAL_CALIBRATION` |
| **M2 full-value redemption (`b + a`, restore Accepted)** | recovery is complete and costless, asymmetric with deterministic stigmatization; no rationale recovered | the E03 dynamic threshold; partly offsets the `r₂ > r` trap | `DISCLOSE_CONDITIONALITY` | `STRUCTURAL_ABLATION`; `FORMAL_ANALYSIS` |
| **M3 hierarchical dual update with the same reward** | the context value is credited with the behaviour's outcome; no rationale recovered; flagged nowhere else | the *magnitude* of the hierarchical E04 decline and the E05 hierarchical censoring; `E04-03` is a claim *about* representation | `DISCLOSE_CONDITIONALITY` | `STRUCTURAL_ABLATION`; `MODEL_COMPARISON` |
| M1 independent tabular arms (`WEAKLY_MOTIVATED`) | discards the ordinal structure of disclosure; the structured-bandit literature is load-bearing against a disclosure-specific reading | every E02 contrast; already handled by `E02-05 / UNRESOLVED` | `DISCLOSE_CONDITIONALITY` | `MODEL_COMPARISON`; `STRUCTURAL_ABLATION` |
| M2 action-independent stigma escape (`WEAKLY_MOTIVATED`) | escape is exogenous to behaviour and can follow a failed redemption within the same step | the interpretation of the `η` axis as label stickiness alone | `DISCLOSE_CONDITIONALITY` | `STRUCTURAL_ABLATION` |

**Additional items requiring disclosure but carrying no future-work debt** (arbitrary reference values whose structural role is defensible and whose claims are already conditional): the four payoff constants; `α`, `τ`, `q₀`, `γ`; `b₂`, `r₂`, `δ`; the E03 rectangle bounds and `0.05` steps; `p_good`, `p_bad`; the `K` ladder; the E05 `0.5` criterion; the E01 forced rate; the final-window fraction; the E03 stability rule.

**No item in either list is an `ARTICLE_V1_BLOCKER`.**

---

# 30. The four explicit questions

## 30.1 Can Article V1 scientifically use arbitrary exact parameter values?

**Yes.** All six conditions are met by the current evidence base:

1. **The exact numbers are not presented as empirically calibrated.** The literature authority refuses quantitative readings; the claim ledger `CUT`s `GIFT-03`, `BFLPE-01` and the `λ`-calibration reading; the count of `EMPIRICALLY_CALIBRATED` parameters is zero and will be stated as such.
2. **The structural assumptions are defensible.** 49 of 86 rows are `WELL_MOTIVATED` and 30 are `PLAUSIBLE_FIRST_ABSTRACTION`; only 7 are weaker, and all 7 are disclosed with resolution paths.
3. **The paper makes existence, structural and reference-model claims.** Every contribution candidate in the ledger is phrased as *can occur in this model* or *is supported in this frozen design*, never as a measurement.
4. **Findings are not represented as human prevalence estimates.** The freeze prohibits it explicitly, and §19 and §25 tighten the language further.
5. **Relevant parameter dependence is disclosed.** 48 rows carry `DISCLOSE_CONDITIONALITY` with the specific dependency named.
6. **Unresolved structural assumptions are flagged as future work.** Five items, each with a named resolution type, in §29.

**No central counterexample was found.** The answer is a qualified yes, not a forced one: it holds *because* the paper's claims are already conditional, and it would fail immediately if any headline were restated as a calibrated or population quantity.

## 30.2 What does it mean to say the phenomena are broad or common in the simplified models?

It means one or more of three things, which must be named individually:

```text
many learners within a fixed parameter cell     n = 500 (or 160) simulated learners.
                                                NOT the inferential unit.
many tested parameter cells                     e.g. 243 of 357 cells of a prespecified
                                                rectangle, under its counting measure.
many independently seeded replications          five master seeds; df = 4. This is the
                                                inferential replicate unit.
```

It does **not** mean either of these:

```text
real-world population prevalence         would require empirical sampling of people.
                                         Not attempted.
natural parameter-space prevalence       would require a probability measure over
                                         parameter space. Not defined anywhere.
```

The disciplined formulations are in §25 and are mandatory throughout the manuscript.

## 30.3 How could this become a quantitatively descriptive model later?

Through a distinct empirical-calibration programme, in this order:

1. **Observable definitions** — identify real-life counterparts to model variables (receptivity → probability of a positive social response; masking/disclosure → observable self-presentation choices; state persistence → persistence of peer reputation; context discovery → access to compatible peers; comparison cost → measurable self-evaluative burden). These are **conceptual future mappings, not current validated operationalizations.**
2. **Model-to-data mapping** — define behavioural summaries computable from both data and simulation.
3. **Parameter or effective-regime fitting** — likelihood-based estimation, simulation-based inference, ABC, hierarchical Bayes or minimum-distance estimation. **No method is prescribed here**; premature commitment would be unjustified.
4. **Identifiability** — expect to recover dimensionless combinations, effective regimes or posterior sets rather than literal constants (§11).
5. **Uncertainty** — bootstrap or posterior methods quantify uncertainty *around a fit*. **Bootstrapping does not by itself identify psychological parameters**, and the E05 bootstrap in the present paper resamples five master simulation curves and identifies nothing about people.
6. **Empirical parameter distributions and external validation** — only once these exist would a question resembling real-world prevalence become meaningful.

**No new experiment is initiated by this audit.**

## 30.4 Why is complete formal analysis not required for Article V1?

- **Complete characterization would genuinely strengthen and generalize the theory.** Deriving `Θ_div = {θ : π_L(θ) ≠ π_O(θ)}` — its boundaries, connectedness, monotonicity, asymptotics, dimensionless reductions and bifurcation structure — is a legitimate and valuable programme.
- **Article V1 instead establishes selected exact benchmarks plus computational existence and tested-region results.** Nine Level-3 analytic results are available (§23), and each simulation result is compared against an exactly computable objective answer.
- **That is sufficient for the narrower present contribution**, which is existence, non-isolation, structural progression and meaningful contrast — not measurement and not complete characterization.
- **Future work can characterize the full parameter geometry**, and Article V1's exact benchmarks are the natural starting point for it.

**Formal analysis is not unnecessary. It is a separate, later, and welcome piece of work.**

---

# 31. Final assessment and disposition

## 31.1 Are the models quantitatively calibrated models of gifted children?

**No.** No parameter qualifies as `EMPIRICALLY_CALIBRATED`. The models are stylized formal models with a normalized reference parameterization.

## 31.2 Are the parameterizations arbitrary?

Not globally, and the answer differs sharply by category:

- **Exactly derived — not arbitrary at all.** `p*`, `p*_λ`, `bf*`, `39/17`, `Δ₀(p)`, `a+c`, `b+r`, `Δ/τ`, the reward-scale equivalence, the M2 dynamic thresholds, and the M2.2/M2.5/M3.1/M1.2/M1.4 structural results.
- **Theory-anchored design.** The E01 and E02 `p` regions, the E05 `bf` bracket and anchors, the E04 abundance and identity controls, the E03 sentinels, and the `λ = 1` reference point.
- **Computational.** `n`, `T`, seed count, bootstrap replicates, tolerances, visit adequacy, the isotonic fit.
- **Arbitrary reference values.** Every payoff and learner magnitude, all four M2 transition constants, the E03 rectangle and step, the `K` ladder, `p_good`/`p_bad`, the M1 level count, the final-window fraction, the E05 criterion, and the E01 forced rate. **This is the largest category, and it is acceptable.**
- **Structurally unresolved.** Five items, all functional forms or transition architecture (§29).

## 31.3 Which aspects of the results are structural rather than dependent on literal constants?

**Structural:** the existence of finite-horizon learned concealment while the objective comparator favours authenticity; the affine-in-disclosure structure and its endpoint consequence (conditional on the linear acceptance relation); the action-count invariance of the M1 objective optimum; Accepted-state dominance for any parameterization with `a + c > 0`; the static-plus-dynamic decomposition of the M2 Neutral gap; the `K`-invariance of the M3 full-information optimum; the general formulas for both thresholds; and the reward-scale equivalence.

**Reference-parameter:** every reported magnitude and location — `−0.025837`, `+0.402990`, `+0.255040`, `−0.328692`, `243/357`, `−0.2340`, `−0.4704`, `0.312852`, `≈0.134076` — and every numeric threshold including `43/60`, `8/17` and `.384/.339/.269`.

**The pattern:** every *existence* and *invariance* result is structural; every *magnitude* and *location* result is reference-parameter. That division should organize the Results section.

## 31.4 Claim impact

| Claim | Impact |
|---|---|
| every frozen E01–E05 numerical result | **unchanged** |
| `E03-01` / `E03-C5-GRID` (`243/357`) | **unchanged wording**; one appendix sentence on measure-relativity added |
| `E04-C6-*` | **unchanged**; scope reworded as a reference-environment result rather than demonstrated robustness across receptivity contrasts |
| `E05-C7-CROSSING` | **unchanged**; already descriptive and BLOCKER-scoped; add that `τ` is unprobed in E05 specifically |
| `E02-*` | **unchanged**; the linear-acceptance dependency is disclosed |
| any claim | **removed** — none |
| any claim | **narrowed** — none beyond the E04 scope wording, which restates existing conditionality rather than reducing the claim |

## 31.5 The final methodological principle

> **The scientific hypothesis resides primarily in the structure of the model and in qualitative relations among variables. Many exact numerical values merely provide coordinates at which that structure is instantiated.**

Article V1 asks whether the resulting learner/objective divergences **exist and extend beyond isolated configurations**. It does not claim that the arbitrary numerical coordinates are measured properties of gifted children. Formally characterizing the full model regimes, fitting effective parameters to real observations, quantifying uncertainty, and estimating empirically weighted regime frequency are natural continuations — **not prerequisites** for the present existence-and-structure contribution.

---

**Audit disposition**

```text
ARTICLE_V1_PARAMETER_AUDIT_REVISION_2_COMPLETE
```

This verdict does not assert that every parameter has a strong rationale. It asserts the opposite, precisely: some values are exactly derived, some are theory-anchored experimental anchors, some are computational, most are arbitrary reference instantiations of defensible structures, and five *structural* assumptions remain unresolved and are recorded as future-work debt. The audit has established which is which, with provenance and justification separated for every row in `ARTICLE_V1_PARAMETER_REGISTER.csv`.
