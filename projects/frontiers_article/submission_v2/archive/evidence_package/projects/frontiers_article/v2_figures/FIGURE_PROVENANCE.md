# Article V2 — Figure provenance and routing record

## Evidence boundary

The four figures are a deterministic presentation package assembled on
2026-08-20, with a layout-only Figure 1 repair on 2026-08-21. The generator reads only the compact publication-source tables
under `projects/frontiers_article/publication_v1/data/`, checks their SHA-256
values before plotting, and imports no experiment module or simulation entry
point. It does not rerun an E01–E05 experiment, derive an estimate from a
pixel, or use E06/M4 material.

The historical frozen evidence remains authoritative. For E01–E03, the exact
historical generator worktrees remain unrecoverable; for E04/E05, frozen source
bundles are recovered. This display-layer generator does not claim to recreate
either historical execution state.

## Final main-text figures

| Figure | Final files | Evidence/source table(s) | Generator | Assembly status |
|---|---|---|---|---|
| 1 | `figures/Figure_1_underidentification_architecture.pdf/.png` | Conceptual V2 framing and E01–E05 mapping; no numerical source | `generate_v2_figures.py::figure_1` | Newly authored; `CONCEPTUAL_FIGURE_NO_NUMERICAL_EVIDENCE` |
| 2 | `figures/Figure_2_history_and_action_representation.pdf/.png` | `e01_primary_effects.csv`, `e01_intervention_effects.csv`, `e02_primary_effects.csv` | `generate_v2_figures.py::figure_2` | Newly assembled from frozen publication-source rows |
| 3 | `figures/Figure_3_persistent_state_and_disagreement.pdf/.png` | `e03_grid_map.csv`, `e03_grid_summary.csv` | `generate_v2_figures.py::figure_3` | Newly assembled from frozen publication-source rows |
| 4 | `figures/Figure_4_discoverability_and_boundary_displacement.pdf/.png` | `e04_k_response.csv`, `e04_headline_effects.csv`, `e05_response_vs_bf.csv`, `e05_crossings.csv`, `e05_displacement.csv` | `generate_v2_figures.py::figure_4` | Newly assembled from frozen publication-source rows; PAVA presentation is deterministic |

Generator command:

```text
MPLCONFIGDIR=/private/tmp/gifted_masking_mplconfig /Users/omer/workspace/venvs/venv314/bin/python projects/frontiers_article/v2_figures/generate_v2_figures.py
```

The only outputs are the four PDF/PNG pairs. No stochastic experiment code is
imported or executed.

Stage 11.5 used the bounded Figure-1-only entry point:

```text
MPLCONFIGDIR=/private/tmp/gifted_masking_mplconfig /Users/omer/workspace/venvs/venv314/bin/python projects/frontiers_article/v2_figures/generate_v2_figures.py --figure 1
```

That path renders only the conceptual Figure 1 PDF/PNG pair, reads no numerical
table, and imports no experiment code. The generator SHA-256 after the bounded
entry-point and layout repair is
`066500d8c758a1a51248400cb43442cbc7ad4573911045dcdc7954c5b9fc895d`.

## Final output hashes

| Output | SHA-256 |
|---|---|
| `Figure_1_underidentification_architecture.pdf` | `02ab24130d8554eb95725bdb64fcb8b6f091ed94e3e5d4af6834b6c2c7cdd54f` |
| `Figure_1_underidentification_architecture.png` | `68b4794f12ee09f4bd9a43a6660e6a13c2aa8c5b199d5142408688cdee9ae391` |
| `Figure_2_history_and_action_representation.pdf` | `f7dc27b4c2054409c8db96358e0b805c0c1c8db4c7d3edd5eda3454590027cd0` |
| `Figure_2_history_and_action_representation.png` | `d05e7266eef729398a0e36b18daa20134fdb12c208d3c0117aad7c20d486844c` |
| `Figure_3_persistent_state_and_disagreement.pdf` | `432d554138a43614b94101381fdca6c73e4b2ced165859feb3a4d42d6b74dc99` |
| `Figure_3_persistent_state_and_disagreement.png` | `417c1eb186e3eaa2d6a77918fad4db7c1b41ec9267a7d71b091123ab3d4e2d85` |
| `Figure_4_discoverability_and_boundary_displacement.pdf` | `a8a39d4a58faeac95b0dfad2d4ec34a58fde1455d3ee63112c3e13cdfbb31dbf` |
| `Figure_4_discoverability_and_boundary_displacement.png` | `566a43bc6ff8b4f4c0d7c34551149fe54526ea2764ac57d41264fb3ee4f2b34a` |

Only Figure 1 changed in Stage 11.5. PDF and PNG inspection confirmed that its
labels, boxes, and connectors no longer overlap, while the caption-governed
many-to-one convergence, history-dependent divergence, information/expectation
mediator, observed-behaviour endpoint, and E01–E05 mapping remain unchanged.
Figures 2–4 retained the six hashes shown above exactly.

## Verified source hashes

| Source file | SHA-256 |
|---|---|
| `e01_primary_effects.csv` | `9b9227f43146b96ae7000f572d2249ae6bd4d39bf414715bdd780203afa38d36` |
| `e01_intervention_effects.csv` | `12a1f4befa1ade1a9065a3782fc40a20d9bbed2f91d31a1d3d4dd5771d55a42b` |
| `e02_primary_effects.csv` | `fe37531296d986f0662ce74d6e3976680163e4f19da7240deef5f8e5d97f966f` |
| `e03_grid_map.csv` | `c5def710116248b60ffcc347fa408519ce5d9094547e486fc73f2388e5babbab` |
| `e03_grid_summary.csv` | `90aebefa0fe66c1f3092879d365c2ede798e71114a1f3b0bb74ee6df083f096a` |
| `e04_k_response.csv` | `c01c04359b30d425d518566190dcfb27b10f9003e4123d9a6f05ce44382c11b7` |
| `e04_headline_effects.csv` | `ebcf58f06eef99fa890bbf9039b3c59293bb743417e3e279f35723f3ef501868` |
| `e05_response_vs_bf.csv` | `0d47aeae4dc4c15e08176c7ff44466740712f3a47000a68d2b7a1231d48a7e10` |
| `e05_crossings.csv` | `866697afb0cdd66f6e6d008cc6b06e52786d1e27f7ba3f71601a56512349076b` |
| `e05_displacement.csv` | `4357f2fc10a07d763e2ec140d30adb5732f71ce1933644e83230af5492098213` |

## Existing-asset routing

| Existing working or historical asset | Routing decision | Reason |
|---|---|---|
| `Figure_1_model_progression.*` | `RETIRE_DUPLICATE` | It is a model-cascade diagram; V2 Figure 1 instead uses the underidentification architecture and E01–E05 map. |
| `Figure_2_adverse_history_information_and_weighting.*` | `MERGE_INTO_FIGURE_1_4` | Frozen E01 rows were recomposed into V2 Figure 2; its weighting panel is not a V2 headline. |
| `Figure_3_graded_disclosure_and_affine_objective.*` | `MERGE_INTO_FIGURE_1_4` | Frozen E02 effects were recomposed into V2 Figure 2. |
| `Figure_4_persistent_state_relocation_and_divergence.*` | `MERGE_INTO_FIGURE_1_4` | The E03 schematic and authoritative classifier are recomposed into V2 Figure 3. |
| `Figure_5_discovery_and_comparison_cost.*` | `MERGE_INTO_FIGURE_1_4` | E04/E05 frozen inputs were recomposed into V2 Figure 4. |
| `Figure_6_boundary_displacement_and_leverage.*` | `ROUTE_TO_SUPPLEMENT` | Cross-estimand synthesis is not part of the V2 main-text evidence plan; retain as a non-main working artifact pending separate authority review. |
| Deleted tracked `Figure_2_early_feedback_and_graded_disclosure.*` | `RETIRE_DUPLICATE` | Recoverable from `HEAD`; superseded by V2 Figure 2. |
| Deleted tracked `Figure_3_persistent_state_contrast_map.*` | `RETIRE_DUPLICATE` | Recoverable from `HEAD`; superseded by V2 Figure 3. |
| Deleted tracked `Figure_4_discovery_and_comparison_cost.*` | `RETIRE_DUPLICATE` | Recoverable from `HEAD`; superseded by V2 Figure 4. |

The main-text package contains exactly Figures 1–4. Existing assets are not
deleted, reset, or altered by this stage. Supplementary routing includes E01
seed-level diagnostics, E02 secondary outcomes, full E03 stability/sentinel
diagnostics, E04 sensitivity and architecture panels, and E05 master curves,
PAVA/bootstrap diagnostics, and the Figure 6 synthesis subject to its distinct
authority concern.
