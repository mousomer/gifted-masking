# Article V1 Parameter Audit — Taxonomy Changelog

**Date:** 16 August 2026
**Purpose:** preserve how the Revision-1 justification taxonomy was replaced, so that no reader of the superseded classes mistakes them for current ones.
**Scope:** documentation only. No experiment, parameter, model semantic or frozen result was changed.

Revision 1 recovered provenance and mathematical structure correctly. Its defect was conceptual: several classes mixed *where a value came from* with *why it is appropriate*, and one class mixed a structural judgement with a numerical one. Revision 2 splits every judgement across four independent axes.

---

## 1. Axis split

| Revision 1 | Revision 2 |
|---|---|
| one `justification_class` column, sometimes compound | **Axis B** `exact_value_justification` (one value, numerical judgement only) |
| — | **Axis C** `structural_rationale_status` (existence, sign, functional form, ordering, transition, state, action architecture) |
| `literature_support` free text | **Axis D** `qualitative_relation_support` (controlled vocabulary) |
| `exact_value_origin`, `rationale_chronology` | **Axis A** `provenance` + `rationale_chronology`, never usable as justification |

Register schema: 22 columns → **29 columns**; rows 58 → **86**. No historical provenance field was dropped.

---

## 2. Class-by-class mapping

| Revision-1 class | Status | Revision-2 treatment |
|---|---|---|
| `EXACTLY_DERIVED` | retained | unchanged meaning |
| `EMPIRICALLY_CALIBRATED` | retained | still **0 rows** |
| `THEORY_ANCHORED_DESIGN` | retained | tightened: requires a deliberate relation to an analytic boundary or theoretically meaningful regime |
| `COMPUTATIONAL_ESTIMATION` | retained | unchanged meaning |
| `RATIONALE_UNKNOWN` | **redefined** | now means genuine future-work debt with a named resolution path; never applied merely because a number is uncalibrated |
| `PSYCHOLOGICALLY_INFORMED_REFERENCE` | **removed** | split: structural judgement → Axis C; numerical judgement → `ARBITRARY_REFERENCE_VALUE`; literature judgement → Axis D |
| `QUALITATIVELY_LITERATURE_CONSISTENT` | **removed** | → Axis D `LITERATURE_SUPPORTED` or `PLAUSIBLE_FIRST_ABSTRACTION` |
| `NORMALIZATION` | **removed** | a unit choice is still a choice: → `ARBITRARY_REFERENCE_VALUE` (`b`, `q₀`) or `THEORY_ANCHORED_DESIGN` (`λ = 1`), with the scale conditions recorded in `REL-SCALE` |
| `CONVENIENCE_REFERENCE` | **removed** | → `ARBITRARY_REFERENCE_VALUE` where structurally defensible; → structural `RATIONALE_UNKNOWN`/`WEAKLY_MOTIVATED` where the item is a functional form |
| `DOMAIN_COVERAGE` | **removed** | domain extent → Axis C; grid resolution → `ARBITRARY_REFERENCE_VALUE` |
| `HISTORICAL_COMPARABILITY` | **removed** | a reason to *retain* a grid, not a justification for its shape: → provenance + `ARBITRARY_REFERENCE_VALUE` |
| `LOG_SCALE_OR_STRUCTURAL_COVERAGE` | **removed** | → `ARBITRARY_REFERENCE_VALUE` (the ladder) + structural `WELL_MOTIVATED` (increasing search space and scarcity) |
| `INHERITED_LEGACY` used as justification | **prohibited** | provenance only; the register build fails if a provenance term appears in a justification column |

---

## 3. Substantive reclassifications

| Item | Revision 1 | Revision 2 | Why |
|---|---|---|---|
| `b, a, c, r` | `PSYCHOLOGICALLY_INFORMED_REFERENCE` / `INHERITED_LEGACY` | `ARBITRARY_REFERENCE_VALUE` + separate structural and qualitative verdicts | provenance is not justification; the sign and the magnitude are different judgements |
| `a > 0` | implied qualitative literature support | `MODEL_ASSUMPTION` | the literature authority's defensible list does not include intrinsic value of authentic expression |
| `δ = 0.02` | `RATIONALE_UNKNOWN` | `ARBITRARY_REFERENCE_VALUE` | structural role defensible; analytic role is `δ`-independent (M2.2); no claim depends on `0.02` |
| redemption `p/2` | `RATIONALE_UNKNOWN` (the value) | value → `ARBITRARY_REFERENCE_VALUE`; **form → structural `RATIONALE_UNKNOWN`** | labelling only the constant understates a functional-form problem |
| `b₂`, `r₂` magnitudes | `RATIONALE_UNKNOWN` | `ARBITRARY_REFERENCE_VALUE` | uncalibrated but structurally defensible and claim-conditional |
| M1 linear acceptance | `CONVENIENCE_REFERENCE` | **structural `RATIONALE_UNKNOWN`** | it is the model's geometry, not a coordinate; it produces the endpoint theorem |
| M1 independent arms | `CONVENIENCE_REFERENCE` | `WEAKLY_MOTIVATED` | the structured-bandit literature is load-bearing against it |
| E03 rectangle | `HISTORICAL_COMPARABILITY` | `ARBITRARY_REFERENCE_VALUE` + `DISCLOSE_CONDITIONALITY` | retention is documented; the shape is not, and it fixes the counting measure |
| `K` ladder | `LOG_SCALE_OR_STRUCTURAL_COVERAGE` | `ARBITRARY_REFERENCE_VALUE` + structural `WELL_MOTIVATED` | powers of two are efficient, not psychologically natural |
| E05 `0.5` criterion | `CONVENIENCE_REFERENCE` | `ARBITRARY_REFERENCE_VALUE` + `TARGETED_SENSITIVITY` flag | it is an operational definition of the estimand, not a model parameter |
| `λ = 1` | `NORMALIZATION` | `THEORY_ANCHORED_DESIGN` | it is exactly the identity transform and the unique point where `p*_λ = p*_obj` |

---

## 4. Rows added in Revision 2

Twenty-eight rows were added by splitting compound Revision-1 rows and by auditing structural assumptions that Revision 1 discussed in prose without registering, or did not identify at all.

**Newly identified, not present in Revision 1 in any form:**

| Row | Finding |
|---|---|
| `S-M2-DETSTIG` | a single rejection from Neutral moves the learner to Stigmatized **with probability 1** — deterministic, with no partial or graded consequence |
| `S-M2-REDEEM-REWARD` | a successful redemption pays the **full** `b + a` and restores Accepted — recovery is complete and costless, asymmetric with the stigmatization side |
| `S-M2-ESCAPE` | stigma escape is **action-independent** and can follow a failed redemption within the same step |
| `S-M2-ACC-REWARD` | Accepted-state masking pays `b − c`, identical to Neutral — load-bearing for M2.2 dominance |
| `REL-SCALE` | the reward-scale invariance recorded with its **full precondition list**, including that the absolute `1e-10` Q tolerances are not scale-covariant |

**Split from existing rows:** the `a>0`/`c>0`/`r>0`/`r≫c` relations; `p_good > p_bad` and its separation; `b₂ < b` and `r₂ ≥ r`; the M1 graded concept / endpoints / monotone exposure / linear acceptance / linear base / independent arms; the M3 context structure / architectures / hierarchical update / `bf` existence / `bf` placement; the `λ` default versus its probes; `S-LEARNER`; `E01-CF`; `E05-K4`; `E05-PAVA`.

---

## 5. What did not change

- Every frozen E01–E05 numerical result.
- Every recovered provenance fact, including the legacy-source reconstruction method and its findings.
- Every exact analytic identity: `Δ₀(p)`, `p*`, `p*_λ`, `bf*`, `39/17`, the M2 thresholds, M2.2/M2.5/M2.6, M3.1/M3.2/M3.4, G1–G3.
- The judgement that **no parameter is empirically calibrated**.
- The judgement that **no current Article-V1 claim is defeated**.
- The E03 measure-relativity recommendation and the `1/K` disclosure requirement, both carried forward unchanged.
