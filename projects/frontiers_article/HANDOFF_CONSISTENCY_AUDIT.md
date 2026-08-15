# Revised Hand-off Consistency Audit

**Audit date:** 15 August 2026  
**Scope:** verify that the revised hand-off pack incorporates the findings of `ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md` without silently changing frozen numerical evidence.

## 1. Overall verdict

**HANDOFF_INTERNAL_CONSISTENCY: PASS_WITH_EXTERNAL_BLOCKERS**

The revised hand-off documents are internally aligned with the 15 August model-analysis audit. The remaining blockers are external to this pack:

1. repository adoption of the revised authorities;
2. historical E01-E05 generator-source provenance;
3. four bounded novelty-critical literature searches;
4. later claim freeze and manuscript rebuild.

## 2. Corrected invariants

| Invariant | Result |
|---|---|
| Article-V1 confirmatory evidence is E01-E05 only | **PASS** |
| E06/M4 numerical results are excluded from V1 confirmatory Results/Discussion | **PASS** |
| E01 does not claim persistent final masking after one rejection | **PASS** |
| E01 sampling and normalized pseudo-regret are explicitly marked algebraically redundant | **PASS** |
| E02 normalized regret is explicitly identified as mean endpoint distance `1-d` in the affine authenticity-optimal cells | **PASS** |
| M1 intermediate actions are not claimed to create a superior static objective optimum | **PASS** |
| E03 classifier is described as aggregate final-window Neutral-state behavior, not individual learned-policy prevalence | **PASS** |
| E03 comparator is full-information DP, not information-matched optimum | **PASS** |
| `243/357` is treated as tested-grid coverage, not prevalence | **PASS** |
| Independent four-policy M2 verification (`8.99e-10` max discrepancy) is recorded | **PASS** |
| E04 is bounded to representation-dependent burden under scarce receptivity | **PASS** |
| K-alone, scarcity-alone, duplicate-normalization-alone and literal-mobility claims are prohibited | **PASS** |
| E05 exact objective crossover remains `8/17 ≈ 0.470588` | **PASS** |
| E05 empirical flat crossing remains `0.312852` with `[0.307836,0.316918]` master-bootstrap interval | **PASS** |
| Binary softmax Proposition G2 is restricted to two-action softmax probabilities | **PASS** |
| G2 is not used to rule out temperature/action-set normalization for E05 | **PASS** |
| E05 mechanism is explicitly `UNRESOLVED` | **PASS** |
| Post-hoc E04/E05 strict-unique-modal checks are labelled diagnostic only | **PASS** |
| Generator-source provenance gap is explicitly publication-blocking | **PASS** |
| Four novelty-critical literature searches remain | **PASS** |
| No stochastic experiment rerun is authorized by the revised hand-off | **PASS** |

## 3. Scientific changes from the 14 August hand-off

### E05

The previous hand-off over-applied a valid binary softmax theorem. The revised pack now states:

- the theorem remains mathematically correct for exactly two-action softmax probabilities;
- E05 measures an eight-action, across-child modal-arm fraction;
- temperature/action-set normalization are therefore **not ruled out** as contributors;
- the empirical learned/objective separation remains valid;
- the displacement mechanism is unresolved.

### E01

The revised analytic authority now proves that normalized pseudo-regret in the relevant E01 cells is exactly the suboptimal-mask action fraction. Sampling and regret are translations of the same action-frequency effect, not independent confirmations.

### E02

The revised analytic authority proves that, in the relevant affine authenticity-optimal cells, normalized regret is exactly `1-d`. It remains an objective endpoint-distance scale, not an independent welfare mechanism.

### E03

The revised pack:

- records independent deterministic verification of the full-information DP envelope across all 357 frozen cells;
- narrows “learned policy” wording to the actual aggregate final-window Neutral action-count classifier;
- preserves the information-matched-optimum limitation.

### E04

The revised pack uses the combined-control interpretation:

> representation-dependent learning burden under scarce receptivity.

It does not claim clean identification of K, scarcity, normalization, or literal social mobility as a unique mechanism.

## 4. Scope/provenance blockers intentionally not closed by this pack

### Historical generator source

The protected outputs are hash-valid, but the exact dirty source tree used to generate the historical E01-E05 runs has not yet been recovered. This pack does not fabricate that provenance.

### Legacy manuscript

The pack does not rewrite the stale Results/Discussion source chapters. It explicitly instructs the next stage to rebuild the manuscript after claim freeze.

### Repository authority

The files in this ZIP are a revised hand-off pack. They become repository authorities only after explicit adoption into the canonical Article-V1 documentation location.

## 5. Adoption rule

When adopted into the repository, older contradictory publication-state prose should be marked historical/superseded rather than deleted, so execution provenance remains traceable while publication authority is unambiguous.
