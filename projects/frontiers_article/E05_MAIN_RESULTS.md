# E05 Main Results — Analytic and Learned Comparison-Cost Crossovers

**Status:** canonical Stage 2 result record  
**Disposition:** `SUPPORTED_IN_NARROW_DOMAIN`  
**Run:** `frontiers_m3_bflpe_crossover_v1`

## Result that must survive article revision

E05 produced a paired analytic and simulation result. The analytic calculation
shows when comparison cost removes the objective advantage of authenticity in
the receptive context. The simulation shows that the frozen flat-2K learner
retreated from that action substantially earlier.

> In the frozen K=4 flat-2K M3 representation, the learned population response
> crossed below `.5` at `bf=0.312852` (95% master-seed bootstrap interval
> `0.307836--0.316918`), while receptive-context authenticity remained
> objectively preferable to masking until the exact payoff crossover
> `bf=8/17=0.470588`. At the learned crossing, authenticity still retained an
> objective advantage of approximately `0.134`. E05 therefore demonstrates a
> model regime of learned retreat before objective indifference.

The old two-endpoint result (`bf=0` versus `.80`) is supporting context only.
It must not replace the dense E05 transition result in later Results,
Discussion, abstract, figure, table, or DOCX revisions.

## Analytic result

At the frozen defaults,

```text
E(mask) = b - c = 0.75
E(good-context authenticity) = 1.15 - 0.85*bf
objective advantage = 0.40 - 0.85*bf
```

Consequently,

```text
bf_objective = 0.40 / 0.85 = 8/17 = 0.47058823529411764.
```

Below this value, good-context authenticity has the higher expected objective
payoff. At the value, it ties masking. Above it, masking has the higher
expected objective payoff. This threshold is an exact consequence of the
frozen reward equation, not a simulation estimate.

## Corresponding simulation result

The standard E05 experiment used two architectures, 18 prescribed `bf`
values, five independent master seeds, `n=500` learners per cell, `T=2000`,
and the final 20% of trials. Its primary response was the fraction of learners
whose modal final-window joint action was authenticity in the receptive
context. The learned `.5` crossing was estimated with a prespecified
nonincreasing PAVA fit and an architecture-isolated 10,000-resample
master-seed bootstrap.

For flat 2K:

- all five seed curves yielded valid crossings inside `(.30,.65)`;
- the pooled crossing was `bf=0.31285211267605634`;
- the 95% bootstrap interval was `[0.3078358208955224,
  0.3169178027050235]`;
- 10,000 of 10,000 bootstrap samples yielded valid crossings;
- no adjacent dense-grid comparison had a material upward violation;
- the good-context-authentic modal fraction was `.9400` at `bf=0`, `.5292`
  at `.30`, `.4724` at `.325`, `.1416` at `8/17`, and `0` at `.80`;
- the endpoint change was `-.9400` (95% five-seed Student-t interval
  `[-.957993,-.922007]`).

The learned crossing preceded objective indifference by
`0.470588-0.312852=0.157736`. Substitution into the analytic advantage gives
`0.40-0.85(0.312852) approximately 0.134`. Thus roughly one-third of the
initial `.40` authenticity advantage remained when the learned response fell
below `.5`.

For the hierarchical architecture, the response was already below `.5` at
the lower dense boundary (`.1176` at `bf=.30`). It produced zero of five valid
seed crossings and zero of 10,000 valid bootstrap crossings in the approved
range. This is a censored boundary result, not evidence that no hierarchical
transition exists. Its crossing may lie below `.30`, but E05 did not estimate
it and does not permit extrapolation.

## What E05 establishes

1. Comparison cost can analytically eliminate the objective advantage of an
   otherwise receptive context.
2. In the frozen flat-2K learner, majority-level behavioral retreat occurred
   while receptive-context authenticity was still objectively advantageous.
3. The learned-objective separation was stable across the five reserved
   master seeds under the tested design.
4. The numerical learned crossing depends on action representation; it did
   not generalize as an estimable crossing to the tested hierarchical model.

## What remains hypothesis

- E05 is consistent with hot-stove persistence, risky exploration, and
  multidimensional search burden, but it does not isolate any one of them as
  the unique cause of the learned-objective gap.
- `bf` is an imposed model payoff term, not a calibrated measure of academic
  self-concept, school placement, or human BFLPE.
- The `.5` response crossing is a prespecified population summary, not a human
  tipping point, psychological type, or discontinuous phase transition.
- The result is conditional on the frozen K, receptivity, learner parameters,
  action representation, and `T=2000`; `T=5000` and broader sensitivity were
  not run.
- The bootstrap interval quantifies Monte Carlo variation across the five
  frozen master-seed curves. It does not include model-specification or human
  population uncertainty.

## Preservation checklist

Every later article version must:

- report the analytic and learned crossovers as distinct quantities;
- state that the learned crossing occurred before objective indifference;
- report `bf=0.313` and its `0.308--0.317` interval when numerical detail is
  appropriate;
- retain the hierarchical no-estimable-crossing boundary;
- identify the endpoint contrast as secondary rather than primary evidence;
- avoid calling the flat crossing a human threshold;
- avoid attributing the gap uniquely to hot-stove persistence without a
  mechanism-isolating ablation.

## Authoritative machine evidence

- `results/manifests/frontiers_m3_bflpe_crossover_v1.json`
- `results/raw/frontiers_m3_bflpe_crossover_v1_units.csv`
- `results/summaries/frontiers_m3_bflpe_crossover_v1_analytic.csv`
- `results/summaries/frontiers_m3_bflpe_crossover_v1_cells.csv`
- `results/summaries/frontiers_m3_bflpe_crossover_v1_effects.csv`
- `results/summaries/frontiers_m3_bflpe_crossover_v1_transitions.csv`
- `results/reports/frontiers_m3_bflpe_crossover_v1_report.md`

The final adjudication is recorded in `STAGE2_EXECUTION_LOG.md` and the
claim boundary in `CLAIM_LEDGER.md`.
