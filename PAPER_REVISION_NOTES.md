# Paper Revision Notes

## Assertive findings revision (2026-08-10)

- Created `doc-reviews/frontiers_submission/gifted_masking_frontiers_original_research_assertive_revision.docx` while retaining the earlier manuscript as a comparison copy.
- Exported the visually verified 14-page manuscript to `output/pdf/gifted_masking_frontiers_original_research_assertive_revision.pdf`.
- Rebuilt the claim hierarchy so that the Abstract, Results headings, opening Discussion paragraphs, implications, and Conclusion lead with the study outcomes before presenting boundary conditions.
- Elevated the central M2 result: `226/357` coarse-grid cells (`63.3%`) were classified as learned suboptimal masking, with mean learned neutral-state masking probability `0.950` across those cells.
- Added explicit, results-led statements for hot-stove persistence, negative-outcome weighting, graded disclosure, sticky stigma, multidimensional context search, comparison cost, and endogenous receptivity.
- Replaced the threshold-only M2 submission figure with a two-panel phase-map and optimal-threshold figure that makes the size of the suboptimal-masking regime visible.
- Consolidated human-population, calibration, seed-replication, and hysteresis qualifications in the later `Boundary conditions and limitations` section.

## Frontiers Original Research manuscript (2026-08-10)

- Created `doc-reviews/frontiers_submission/gifted_masking_frontiers_original_research.docx` from the official Frontiers Word template.
- Replaced the prior evidence-dump format with a full Original Research article organized as Abstract, Introduction, Materials and Methods, Results, and Discussion.
- Limited conclusions to maintained evidence: M0/M1 directional checks, M2 learned-policy regret relative to value iteration, M3 search-burden ablations, and M4 schedule-specific path dependence.
- Removed or rejected claims of generic context harm, default optimal-learner lock-in, robust hysteresis, human causality, and intervention efficacy.
- Recomputed manuscript confidence intervals with independent within-condition bootstrap resampling because the source conditions use distinct RNG streams; the earlier child-index pairing was administrative rather than experimental.
- Added four submission-ready figures, three editable tables, complete declarations, an AI-use disclosure, figure alt text, and a submission scope statement.
- Kept explicit placeholders for author identity, affiliations, correspondence, archive DOI, funding, contributions, and conflict-of-interest confirmation.

## Abstract / Executive Summary

Replace broad claims that "context multiplicity is harmful" and "true
hysteresis" is established with:

```text
The simulations support a narrower mechanism: persistent masking emerges when
authenticity is risky, when receptive contexts must be discovered through
search, and when endogenous peer receptivity creates path-dependent feedback.
The current M3 ablations indicate that the context effect is strongest when many
contexts impose an asymmetric search burden. The current M4 ramp experiment
shows path dependence under the tested schedule, but stronger hysteresis claims
require additional diagnostics.
```

## M2 Results

Replace "structural lock-in traps even optimal learners" with:

```text
In the stigma-state MDP, lower stigma escape rates increase learned masking in
the tested Q-learning simulations. A value-iteration benchmark now provides the
optimal MDP policy, static M0 comparator, and neutral-state regret for current
robustness cells with empirical state-conditional policies. Broad claims that
sticky stigma traps optimal learners still require denser parameter and learner
sensitivity sweeps.
```

## M3 Results

Replace "context multiplicity is harmful" with:

```text
Context multiplicity increases masking when it imposes a search burden:
authenticity must be discovered in the receptive context, while masking remains
reliably available. In controls that remove or sharply reduce that search
burden, the K effect attenuates toward zero. The supported mechanism is
therefore not generic context multiplicity, but the asymmetric search problem
created by many possible contexts and few receptive ones.
```

Do not claim that "more groups always causes masking" or that the K effect is
independent of action-space design.

## BFLPE Results

Use:

```text
The BFLPE comparison cost is applied to accepted authenticity in the good pond.
At high comparison cost, good-pond authenticity decreases in the maintained
simulation. The analytic crossover identifies where good-pond authenticity
ceases to dominate masking in objective payoff terms; behavioral crossover
claims require a sweep around that threshold with uncertainty.
```

## M4 Results

Replace "true hysteresis" with:

```text
The ramp-up/ramp-down experiment shows path dependence under the tested
schedule. The evidence is consistent with hysteresis-like dynamics, but the
current diagnostics do not yet justify treating hysteresis as fully established.
A stronger claim would require loop-area estimates, transition-threshold
separation, ramp-speed sensitivity, and independent-seed replication.
```

## Risk-Type Results

Replace "risk-taking is strictly protective" and "risk-aversion is close to
fatal" with:

```text
Loss aversion changes learned avoidance in the tested bandit settings. Stronger
claims about risk-taking or risk-aversion across dynamic worlds require
maintained robustness sweeps across M2-M4, including uncertainty and seed
replication.
```

## Consolidated Outcome Map

Use:

```text
The model ladder separates candidate routes into persistent masking: risky
authenticity, graded disclosure dynamics, sticky stigma, context search burden,
and endogenous receptivity feedback. The current evidence is strongest for the
M0, M1, and M3 directional checks, and for M4 path dependence under one tested
ramp schedule. Publication-grade consolidation requires stronger M2 optimal
benchmarks, M3 good-pond variants, and M4 hysteresis diagnostics.
```

## Limitations

Add:

```text
Current robustness artifacts now store primary child-level rows for the
maintained checks, including M2 state-conditional final-window action counts.
Future runs still need independent master-seed replication and denser
parameter-grid artifacts for publication-grade uncertainty.
```

Add:

```text
The maintained M2 implementation is now benchmarked against an optimal MDP
policy for selected cells. We still avoid broad claims about suboptimal lock-in
or traps for optimal learners until the benchmark is extended across learner
parameters, seeds, and a denser `p`/`eta` grid.
```

## Reproducibility / Implementation Section

Use:

```text
The maintained implementation separates model kernels, plotting utilities,
robustness experiments, and reproducibility helpers. Verification is run through
the repository-local virtual environment using `./scripts/verify.sh`. The
current manifest records Python, platform, NumPy, matplotlib, command, working
directory, timestamps, and output paths. Publication-grade reproducibility still
requires serialized parameter grids, seed hierarchy, primary raw observations,
and a code or config hash.
```

## Phrases To Remove Or Soften

| Phrase | Replacement |
| ------ | ----------- |
| "context multiplicity is harmful" | "context multiplicity can increase masking when it imposes search burden" |
| "structural lock-in traps even optimal learners" | "sticky stigma increases learned masking; optimal-policy effects require benchmarking" |
| "true hysteresis" | "path dependence under the tested ramp schedule" |
| "timing matters more than environment quality" | "timing and environment feedback interact in the tested path-dependent model" |
| "no temperament saves the child" | "learner parameters did not eliminate masking in the tested settings; broader sweeps are needed" |
| "risk-taking is strictly protective" | "lower loss aversion reduced avoidance in selected settings" |
| "risk-aversion is close to fatal" | "higher loss aversion increased avoidance in selected settings" |
| "no learner parameter substitutes" | "substitution between learner parameters and environmental fresh starts remains to be benchmarked" |
