# Backlog

## Completed In This Restructure

- [x] Preserve legacy scripts instead of deleting them.
- [x] Define a modular package architecture.
- [x] Separate core simulation code from plotting imports.
- [x] Add a verification entrypoint.
- [x] Add baseline robustness and perturbation suites.
- [x] Make repo-local `.venv` usage an explicit policy in `AGENTS.md`.
- [x] Add RNG determinism tests across M0-M4.
- [x] Add maintained M3 ablation formulations.
- [x] Add an explicit M4 ramp-up/ramp-down path experiment.

## Next Work

- [ ] Expand M2 lock-in mapping beyond the current coarse `p`/`eta` grid to
      learner-parameter perturbations and threshold-local refinement.
- [ ] Add additional M3 ablation families for randomized and multi-good-pond settings.
- [ ] Tighten the M4 hysteresis experiment into a stronger claim test with
      explicit acceptance criteria for path separation.
- [ ] Add richer report templates and comparison dashboards.
- [ ] Convert CSV outputs to a columnar format if the repo later accepts an
      additional dependency for that purpose.
