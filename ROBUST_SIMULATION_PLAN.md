# Robust Simulation Hardening Plan

## 14.1 Simulation Tiers

Current full verification runs in about `6.7s` wall time on the local machine.
The following tiers keep CI fast while defining a path to paper-grade evidence.

| Tier | Purpose | n per cell | T | Grid size | Master seeds | Use |
| ---- | ------- | ---------: | -: | --------- | -----------: | --- |
| smoke | CI and bug detection | 96-250 | 200-1200 | tiny targeted contrasts | 1 | every commit |
| standard | reproduce current artifacts | 220-600 | 1200-2000 | current targeted grids | 3+ | normal analysis |
| publication | final robustness claims | 1000+ | 5000+ | dense grid plus sampled perturbations | 10+ | paper-grade claims |

## 14.2 Reproducibility

Required improvements:

- config files for each named suite;
- manifest JSON with complete parameter grids;
- deterministic seed hierarchy with a master seed;
- independent RNG streams per parameter cell and child;
- deterministic output ordering;
- git commit hash when available;
- code hash or config hash when git is unavailable;
- Python version and package versions;
- run command and working directory;
- artifact paths;
- verification status;
- warnings and skipped-test records.

## 14.3 Statistical Uncertainty

Required improvements:

- confidence intervals for every headline effect;
- saved primary units used to compute intervals;
- independent master-seed replication;
- threshold-location uncertainty for phase boundaries;
- effect-size reporting;
- bootstrap intervals for per-child or per-seed units;
- analytic or binomial intervals where appropriate.

Current limitation: the saved `raw` robustness artifact is summary-level. Future
runs should persist per-child or per-seed outputs.

## 14.4 Sensitivity Analysis

Required one-at-a-time sweeps:

- `n`;
- `T`;
- final-window fraction;
- `alpha`;
- `tau` / `temp`;
- `lambda`;
- `q0`;
- `gamma` for M2;
- `p/r` grid resolution;
- `eta` for M2;
- `K`, `p_good`, `p_bad` for M3;
- `bf` for BFLPE;
- `ka`, `kr`, `km`, `p0` for M4.

If runtime remains manageable, add joint sensitivity with Latin hypercube or a
Sobol-style design. Do this after primary raw outputs and seed hierarchy are
fixed.

## 14.5 Model-Specific Ablations

Required:

- M1 with and without action generalization, if a generalization model is added;
- M2 learned policy versus optimal MDP policy;
- M3 flat 2K versus hierarchical versus global-mask versus fixed-known-good-pond;
- M3 randomized good-pond identity;
- M3 multiple-good-pond variant;
- M4 `km = 0`;
- M4 `ka = 0`;
- M4 `kr = 0`;
- M4 `ka < kr`;
- M4 `ka = kr`;
- M4 `ka > kr`;
- M4 ramp-speed sensitivity;
- M4 loop-area and transition-threshold diagnostics.

## 14.6 Artifact Layout

All robust runs should produce:

```text
results/
  manifests/
  raw/
  summaries/
  figures/
  reports/
```

Each run should produce:

- manifest JSON;
- primary raw results;
- cell summaries;
- confidence intervals;
- figures;
- warnings;
- runtime metadata;
- human-readable report.

## Implementation Order

1. Add manifest completeness tests and fail on missing seed strategy and
   parameter grid for publication suites.
2. Replace summary-level `raw` artifact with primary per-child or per-seed rows.
3. Add summary-vs-raw recomputation tests.
4. Add M2 value-iteration benchmark. Status: implemented for selected target
   and current robustness cells; next step is parameterized perturbation sweeps.
5. Add M4 loop area and threshold diagnostics.
6. Add M3 randomized and multiple-good-pond variants.
