# Article V2 — Figure-to-text consistency matrix

All numerical rows were checked against the frozen publication-source CSV hashes
listed in `FIGURE_PROVENANCE.md`. Values below retain source precision where it
is needed to distinguish the frozen estimator from display rounding.

| Figure/panel | Evidence source | Result statement | Exact statistic | Caption consistent? |
|---|---|---|---|---|
| 1A–B | Conceptual V2 framing and E01–E05 mapping | Multiple upstream routes converge on observed behaviour through information/expectations; similar current conditions permit history-dependent divergence | Conceptual; no numerical statistic | Yes |
| 2A | E01 `e01_primary_effects.csv` | Post-initial authentic sampling | −0.0258370423; 95% CI [−0.0357525160, −0.0159215686] | Yes |
| 2A | E01 `e01_primary_effects.csv` | Final-window mask contrast | −0.0003432659; 95% CI [−0.0116046768, 0.0109181450] | Yes |
| 2B | E01 `e01_intervention_effects.csv` | 5% forced authentic exploration | 0.0465902272; 95% CI [0.0332295269, 0.0599509275] | Yes |
| 2B | E01 `e01_intervention_effects.csv` | Counterfactual authentic feedback | 0.1181350847; 95% CI [0.1096831991, 0.1265869703] | Yes |
| 2C | E02 `e02_primary_effects.csv` | Continued non-zero disclosure | +0.2550404005; 95% CI [0.2530035110, 0.2570772901] | Yes |
| 2C | E02 `e02_primary_effects.csv` | Full-authentic final-window selection | −0.3286922326; 95% CI [−0.3420366913, −0.3153477738] | Yes |
| 2C | E02 `e02_primary_effects.csv` | Unique-modal full-authenticity | −0.2217395930; 95% CI [−0.2887553012, −0.1547238847] | Yes |
| 3B | E03 `e03_grid_map.csv`, `e03_grid_summary.csv`, frozen stable-cell table | Learned–objective disagreement classifier | 243/357 tested parameter cells; 7 inconclusive = 5 inadequate across all masters + 2 four-of-five stability failures | Yes |
| 4A | E04 `e04_headline_effects.csv` | Flat $K=16-K=1$ effect | −0.234000; 95% CI [−0.246417, −0.221583] | Yes |
| 4A | E04 `e04_headline_effects.csv` | Hierarchical $K=16-K=1$ effect | −0.470400; 95% CI [−0.511031, −0.429769] | Yes |
| 4A | E04 `e04_headline_effects.csv` | Fixed-known-good control | 0 exactly | Yes |
| 4A | E04 `e04_headline_effects.csv` | Global-mask control | +0.008800; 95% CI [0.002090, 0.015510] | Yes |
| 4B | E05 `e05_crossings.csv` | Learned PAVA crossing | 0.3128521127; 95% CI [0.3078358209, 0.3169178027] | Yes |
| 4B | E05 `e05_crossings.csv` | Objective crossover | $8/17=0.4705882353$ | Yes |
| 4B | E05 `e05_displacement.csv` | Objective minus learned displacement | 0.1577361226 | Yes |
