# Article V1 Stage-1 Publication Freeze

**Freeze date:** 16 August 2026
**Repository:** `gifted-masking`, branch `codex/frontiers-stage2-e06`
**Document class:** engineering/scientific handoff. This is **not** the manuscript. It records what the deterministic Article-V1 publication layer contains, what it is allowed to say, and what remains for Stage 2.
**Governing authority:** `projects/frontiers_article/ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md`. Where this document and that freeze appear to differ, the manuscript evidence freeze governs.

---

## 1. Stage-1 scope

Stage 1 is **publication assembly from frozen E01–E05 evidence**. It is not a new experiment, a robustness programme, a literature review, or a scientific reconsideration.

What Stage 1 did:

- verified the frozen E01–E05 artifacts against their manifests and against the evidence matrix;
- made the operative Article-V1 authority documents durable in the worktree;
- extracted compact publication-source CSVs from the frozen artifacts under pinned literal selectors;
- built an exact analytic-results table by closed-form derivation;
- built four main figures that read only those CSVs;
- recorded a machine-readable provenance and output manifest;
- added four minimal series-level evidence-matrix rows for the plotted series.

What Stage 1 did **not** do: no experiment was rerun, no stochastic entry point was invoked, no seed was added or extended, no config, learner, reward, or model semantic was changed, no comparator was added, no literature search was performed, and no scientific claim was introduced, strengthened, or reopened.

---

## 2. Frozen experiment families

| Experiment | Model | Run ID | Protected outputs | Status |
|---|---|---|---|---|
| E01 | M0 | `frontiers_hot_stove_v1` | 5 | verified |
| E02 | M0/M1 | `frontiers_m1_binary_graded_v1` | 6 | verified |
| E03 | M2 | `frontiers_m2_regime_replication_v1` | 8 | verified |
| E04 | M3 | `frontiers_m3_search_architectures_v1` | 7 | verified |
| E05 | M3 | `frontiers_m3_bflpe_crossover_v1` | 7 | verified |

**33/33 protected outputs valid. 18/18 evidence-matrix referenced files valid** (15 from the 29 frozen claim adjudications, plus three further frozen summaries introduced by the four Stage-1 series rows).

## 3. Exclusion of E06 and M4

E06 and M4 remain in the repository as Track-B/future material. They contribute **no** data, figure, panel, result, claim, caption, table, or manuscript-facing artifact to Article V1. There is no E06 standard GO.

The exclusion is enforced mechanically, not only by convention:

- `pubcommon.FAMILIES` admits exactly `E01`–`E05`;
- `build_publication_v1.py` fails closed if any source path entering the publication graph matches an E06/M4 token;
- `tests/test_publication_v1.py` asserts the same over the written manifest.

`src/gifted_masking/plotting/legacy_figures.py` is **not used**: it re-runs simulations and contains obsolete/M4 material. The historical manuscript TIFFs are historical artifacts only and carry no scientific authority. The previous five-TIFF/M4 figure structure is not resurrected.

---

## 4. Provenance and hash status

### 4.1 Frozen source artifacts consumed by the publication build

| Artifact | SHA-256 (16) |
|---|---|
| `results/summaries/frontiers_hot_stove_v1_effects.csv` | `4ce67da8b48e8d77` |
| `results/summaries/frontiers_m1_binary_graded_v1_effects.csv` | `11d29c72508649a1` |
| `results/summaries/frontiers_m1_binary_graded_v1_arms.csv` | `cc19fa67bd40f5c2` |
| `results/summaries/frontiers_m2_regime_replication_v1_cells.csv` | `198cb7be9b2a93aa` |
| `results/summaries/frontiers_m2_regime_replication_v1_stable_cells.csv` | `91814ab4430f63bc` |
| `results/summaries/frontiers_m3_search_architectures_v1_curves.csv` | `33f245b36ba6d784` |
| `results/summaries/frontiers_m3_search_architectures_v1_effects.csv` | `dd426992f0a1a0ae` |
| `results/summaries/frontiers_m3_bflpe_crossover_v1_cells.csv` | `59d780f3feb3ed03` |
| `results/summaries/frontiers_m3_bflpe_crossover_v1_transitions.csv` | `96b8d8dc1cf27e3a` |
| `results/summaries/frontiers_m3_bflpe_crossover_v1_analytic.csv` | `e1045d0593709561` |

No file under `results/raw/` is read by any extractor or figure. Raw files remain provenance and backstop evidence only. The ~391 MB E03 raw file is never loaded.

### 4.2 Article-V1 authority documents

| Authority | SHA-256 (16) |
|---|---|
| `ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md` | `1862d6fc5f8a62b5` |
| `ARTICLE_V1_EVIDENCE_MATRIX.csv` | `7befebf2f7a463f5` |
| `ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md` | `d93adeec7def0c02` |
| `ARTICLE_V1_ANALYTIC_RESULTS.md` | `368ca73a86983d50` |
| `ARTICLE_V1_E01_E02_INTERPRETATION.md` | `4ac5d20f9560508d` |
| `ARTICLE_V1_E03_INTERPRETATION.md` | `ca10fea29ff37a88` |
| `ARTICLE_V1_E04_INTERPRETATION.md` | `56bd98c1bf55d8ac` |
| `ARTICLE_V1_E05_INTERPRETATION.md` | `79f735b1ac4a727f` |
| `ARTICLE_V1_GENERATOR_SOURCE_PROVENANCE_AUDIT.md` | `bfa3afa9b8b952f9` |
| `HANDOFF.md` | `cbf5db82130b2e54` |

The five previously untracked authority documents (the manuscript evidence freeze and the four per-experiment interpretation notes) were committed before any publication generation, so the operative scientific authority state is durable in git rather than in the worktree alone. Frozen E01–E05 result artifacts remain ignored under `results/` and were **not** committed; their identity is carried by the content-addressed manifests under `results/manifests/`.

### 4.3 Build provenance

`publication_v1/manifests/publication_v1_manifest.json` records, for every generated data CSV, table, and figure: output path and SHA-256, generating script paths and SHA-256s, source artifact paths and SHA-256s, the exact selectors and fields, the declared transformation, the generation command and timestamp, the Article-V1 authority hashes, and the git commit plus whether the worktree was dirty at generation time. `publication_v1/data/PROVENANCE.json` carries the same per-dataset record in extractor order.

This is **current publication-build provenance**. It is a separate question from the historical E01–E03 generator-source provenance recorded in Section 10.

---

## 5. Publication-source data

Figures read only from `publication_v1/data/`. They never read `results/raw/`, never read `results/summaries/` at plot time, and never import an experiment runner.

| File | SHA-256 (16) | Contents |
|---|---|---|
| `e01_primary_effects.csv` | `9b9227f43146b96a` | three E01 estimands with roles (primary / linked unit translation / secondary null) |
| `e02_primary_effects.csv` | `fe37531296d986f0` | four E02 estimands, rejected stratum only |
| `e02_arm_expected_rewards.csv` | `e58f0603e27a34ab` | M1 per-arm expected reward at p ∈ {0.75, 0.85} |
| `e03_grid_map.csv` | `c5def710116248b6` | 357 tested cells: p, η, learned and objective Neutral action, classification, stability, visit adequacy, exact Q gap |
| `e03_grid_summary.csv` | `90aebefa0fe66c1f` | tested-grid coverage counts by publication category |
| `e04_k_response.csv` | `c01c04359b30d425` | K-response series by architecture and abundance regime |
| `e04_headline_effects.csv` | `ebcf58f06eef99fa` | frozen K = 16 minus K = 1 contrasts and controls |
| `e05_response_vs_bf.csv` | `0d47aeae4dc4c15e` | pooled modal good-authentic fraction against bf |
| `e05_crossings.csv` | `866697afb0cdd66f` | frozen learned crossing, bootstrap interval, exact objective crossover, hierarchical censoring |
| `e05_displacement.csv` | `4357f2fc10a07d76` | closed-form displacement and objective advantage at the learned crossing |
| `PROVENANCE.json` | `66a3db568544d0cd` | per-dataset provenance index |

### 5.1 Pinned selectors

| Experiment | Literal selector |
|---|---|
| E01 | `level=across_master_seeds`; `p=pooled_equal_weight_p_0.75_0.85`; `lambda=""`; `condition=""`; `stratum=""` |
| E02 | `level=across_master_seeds`; `p=pooled_equal_weight_p_0.75_0.85`; **`stratum=rejected`** |
| E03 | `component=exact_grid`; `sensitivity_name=baseline` |
| E04 | `canonical_identity_mode=fixed`; `effective_good_count=1` (one-good) or `max(1, ceil(K/4))` (proportional-25); response `mean_settled_any_good_auth_argmax` |
| E05 | `level=across_master_seeds`; `response_metric=modal_good_auth_argmax_fraction`; `fit_method=nonincreasing_pava_equal_n`; dense range bf ∈ [0.30, 0.65] |

No selector may be defaulted. The E02 `stratum=rejected` filter is mandatory and is asserted at extraction, again after extraction, and again in the test suite.

### 5.2 Permitted transformations

Every dataset declares its transformation from a closed vocabulary, and an undeclared transformation aborts the build: `row_filter`, `column_projection`, `deterministic_join`, `equal_weight_master_mean`, `master_range`, `count_aggregation`, `closed_form_analytic`, `rounding_for_display`.

Two aggregations warrant explicit note:

- **`equal_weight_master_mean`.** For E04 and E05 the plotted point is the equal-weight mean over the five master-seed cell values. For E05 this is verified at build time to reproduce the frozen `raw_dense_start_response` and `raw_dense_end_response` exactly, which is what licenses it as the frozen pooling rather than a new estimator.
- **`master_range`.** The shaded bands in Figure 4 are the observed minimum and maximum across the five master seeds. They are a **descriptive spread, not a confidence interval**. All inferential claims rest on the frozen Student-t intervals carried in the effects CSVs.

**No fit is recomputed anywhere in this layer.** The E05 PAVA crossing and its bootstrap interval are read from the frozen transitions table, never re-estimated.

---

## 6. Figures

Four main figures. Each is written as vector PDF plus a 400 dpi PNG counterpart. Captions are generated from the same CSVs the panels plot, so a caption number cannot drift from a panel number; they live in `publication_v1/figures/FIGURE_CAPTIONS.md`.

| Figure | File stem | PDF SHA-256 (16) | Content |
|---|---|---|---|
| 1 | `Figure_1_model_progression` | `c81fb3ff5abb18da` | M0 → M1 → M2 → M3 progression with each model's exact analytic anchor. Conceptual/analytic; no simulation data. |
| 2 | `Figure_2_early_feedback_and_graded_disclosure` | `5aa0f66ed9fb062e` | (a) E01 effects; (b) E02 effects, rejected stratum; (c) the affine M1 objective. |
| 3 | `Figure_3_persistent_state_contrast_map` | `1f4f244017bda601` | (a) E03 per-cell learner/objective contrast map over the tested grid; (b) exact objective Neutral Q gap with its zero contour. |
| 4 | `Figure_4_discovery_and_comparison_cost` | `a441ecda19239344` | (a) E04 K-response with controls and the frozen K = 16 minus K = 1 contrasts inset; (b) E05 response against bf with the learned and objective crossings. |

Figure-specific notes that bind any use of these panels:

- **Figure 2a** shows the regret row as the sampling row rescaled, in a distinct grey open marker, with the panel subtitle stating the relation. It must never be read as a second, independent confirmation. The final-mask row is annotated as spanning zero; the build refuses to render that annotation unless the interval genuinely spans zero.
- **Figure 2b** carries `rejected stratum only` in the panel itself, not only in the caption.
- **Figure 3a** shows all 357 tested cells. Inconclusive cells are drawn, never dropped. Because the learner masked in the Neutral state in every cell whose Neutral visits were adequate, the contrast region coincides exactly with the region where the full-information optimum is authenticity; the overlaid contour makes that visible. The panel is titled as a learner/objective contrast and is **not** titled or captioned as prevalence.
- **Figure 3b** uses a zero-anchored diverging scale with independent scaling on each side, because the exact Q gap spans roughly −6.65 to +0.85 and a symmetric scale would flatten the entire authenticity-favouring side. The colour bar carries true values and the caption states the choice.
- **Figure 4a** plots the primary architectures with master-range bands and the controls as thin reference lines; the known-good control is K-invariant by construction.
- **Figure 4b** shows the flat learned crossing with its bootstrap interval shaded, the exact objective crossover, and the displacement between them. The hierarchical response is labelled left-censored below the observed range. **No hierarchical threshold is estimated or extrapolated.**

---

## 7. Analytic-results table

`publication_v1/tables/analytic_results_v1.csv` (`34b3f9d4f36db014`) and `.md` (`efd360fdd34c91e9`). Every row is closed-form and is re-derived and asserted at build time; no stochastic calculation is involved.

| ID | Result | Exact value |
|---|---|---|
| M0.1 | Static objective reward gap `Δ₀(p) = a + c − (1−p)(b+r)` | `3p − 43/20` |
| M0.2 | **Static M0 objective boundary** `p* = 1 − (a+c)/(b+r)` | `43/60` |
| M1.1 | `E[R(d)] = b − c + d[a + c − (1−p)(b+r)]`, affine in `d` | `3/4 + d(3p − 43/20)` |
| M1.2 | Strict optimum at an endpoint except at exact indifference | endpoint |
| M2.5 | `D_N(V) = Δ₀(p) + γ[p V_A + (1−p) V_S − V_N]` | — |
| M2.VI | Full-information dynamic optimum (value iteration; envelope error ≤ 8.99e−10) | — |
| M3.1 | Full-information optimum is K-invariant under one good context | `R_G = 23/20` at bf = 0 |
| M3.2 | Objective comparison-cost crossover `R_G(bf) − R_M = 0.40 − 0.85·bf` | `8/17` |
| M3.3 | Good-versus-bad context crossover | `39/17` |

`p* = 43/60` is labelled the **static M0 objective boundary** and must never be conflated with the M2 dynamic threshold.

---

## 8. Exact headline values

### E01 — M0 hot stove

| Estimand | Value | 95% Student-t |
|---|---|---|
| rejected − accepted post-initial authentic rate | **−0.025837** | [−0.035753, −0.015922] |
| rejected − accepted normalized regret (same estimand, regret units) | **+0.025824** | [+0.015914, +0.035735] |
| rejected − accepted final-window mask rate | **−0.000343** | [−0.011605, +0.010918] |

### E02 — binary versus graded, `stratum = rejected`

| Estimand | Value | 95% Student-t |
|---|---|---|
| graded any − binary full post-initial rate | **+0.255040** | [+0.253004, +0.257077] |
| graded − binary full-authentic final-window rate | **−0.328692** | [−0.342037, −0.315348] |
| graded − binary optimal-endpoint modal probability | **−0.221740** | [−0.288755, −0.154724] |
| binary − graded normalized regret | **−0.029761** | [−0.033874, −0.025648] |

### E03 — M2 regime replication, frozen baseline exact grid

| Quantity | Value |
|---|---|
| tested parameter-grid cells | **357** (21 p × 17 η) |
| stable learned-suboptimal masking | **243 / 357** |
| learner matches objective | **107 / 357** |
| inconclusive (Neutral visits inadequate) | **7 / 357**, all at η = 0, p ≤ 0.30 |

### E04 — M3 search architectures, `mean_settled_any_good_auth_argmax`

| Estimand | Value | 95% Student-t |
|---|---|---|
| `flat_2k_..._S16_minus_S1_fixed_one` | **−0.234000** | [−0.246417, −0.221583] |
| `hierarchical_..._S16_minus_S1_fixed_one` | **−0.470400** | [−0.511031, −0.429769] |
| `global_mask_..._S16_minus_S1_fixed_one` (control) | **+0.008800** | [+0.002090, +0.015510] |
| `fixed_known_good_..._structural_K_effect` (control) | **0** | [0, 0] |

### E05 — M3 comparison-cost crossover

| Quantity | Value |
|---|---|
| flat learned 0.5 crossing | **0.312852** (`0.31285211267605634`) |
| master-seed bootstrap interval | **[0.307836, 0.316918]** (10,000 resamples, 10,000 valid) |
| exact objective crossover | **8/17 = 0.470588** |
| displacement | **0.157736** |
| objective authenticity advantage at the learned crossing | **≈ 0.134076** |
| hierarchical | **left-censored, `no_crossing_below`; no in-range crossing estimable** |

---

## 9. Wording constraints binding on Stage-2 prose

These restate the constraints the publication layer was built to respect. The manuscript evidence freeze remains the governing authority, including its Section I prohibited-claims list.

1. **E01 is not persistence.** Early adverse authentic feedback caused a finite-horizon reduction in subsequent authentic sampling and associated regret, **without detectable persistent final-mask separation in this design**. The final-mask result is a failure to detect, not an established equivalence; no equivalence margin was tested.
2. **E01 sampling and E01 regret are one estimand in two units**, linked by `regret = −(T−1)/T × sampling`. They may never be presented as independent confirmations.
3. **E02 does not make intermediate disclosure objectively superior.** `E[R(d)]` is affine in `d`, so the strict static optimum is an endpoint except at exact indifference. The defensible statement is that adding graded disclosure options changes learned behaviour and preserves nonzero disclosure after adverse feedback. The exploration result may not appear without the three adverse results beside it. Prohibited: ladder climbing, endpoint discovery, smooth generalization, protective effect, independent welfare improvement.
4. **E02 regret is a disclosure-distance identity**, not independent welfare evidence.
5. **`243/357` is tested-grid coverage.** It means 243 of the 357 tested parameter-grid cells. It is **not** 68% prevalence, not a share of people, not a share of environments generally, not phase-space volume, and not a probability that masking occurs. Use "tested-grid coverage" or equivalent.
6. **The E03 comparator is the exact full-information dynamic optimum.** It is not information-matched to the learner. No sentence may claim the learner underperformed the best policy attainable under its own information constraints. No decomposition of the gap is required or claimed for V1.
7. **E04 is scarcity plus discovery plus finite sampling plus maintained representation, as a conjunction.** Use: as receptive contexts become scarcer and must be discovered under finite sampling, learned authenticity can decline substantially even though the full-information objective optimum itself is K-invariant. Do **not** use: more contexts intrinsically cause masking. K alone does not identify scarcity; global-mask does not isolate duplicate-mask normalization; M3 does not model literal human movement between peer groups.
8. **E05 is descriptive.** The learned behavioural crossover occurs substantially before the exact objective crossover. The design does not isolate a mechanism. **Fixed softmax temperature and action-set normalization remain possible contributors** and must be listed among unresolved contributors; the standing BLOCKER in Section E of the manuscript evidence freeze is unresolved and binds any E05 sentence. No hierarchical threshold may be estimated or implied.
9. **Inferential unit.** Every simulation interval here is Student-t across five master seeds (df = 4). `n = 500` (E01/E02/E04/E05) or `n = 160` (E03) is the number of simulated learners per cell, not the replicate count.
10. **No M4 or E06 numerical result is Article-V1 evidence.**

### 9.1 Expected scientific spine

E01: early adverse authentic feedback can reduce subsequent authentic sampling over the finite horizon. E02: adding graded disclosure preserves intermediate/nonzero disclosure behaviour even though the static objective remains endpoint-optimal. E03: when behaviour changes future social state, a broad tested parameter region exhibits learned masking while the exact full-information dynamic optimum favours authenticity. E04: when favourable contexts are scarce and must be discovered, learned authenticity declines strongly with search burden even though the full-information optimum is K-invariant in the frozen one-good-context design. E05: with increasing authentic-expression comparison cost, the learned behavioural crossover occurs substantially earlier than the exact objective crossover.

Together: ability concealment can emerge not simply because authenticity is objectively disadvantageous, but because finite-horizon learning operates under incomplete feedback, graded options, persistent social consequences, heterogeneous receptive contexts, discovery burden, and comparison costs. This may not be strengthened into universal or causal claims beyond what the frozen experiments establish, and should not be weakened unnecessarily either.

---

## 10. Reproducibility limitation

Artifact identity, model-semantics identity, and generator-source identity resolve differently and must not be conflated:

- **Artifact identity — intact.** 33/33 protected E01–E05 outputs hash-match their manifests.
- **Model-semantics identity — intact.** The maintained model implementation matches the audited mathematical reference.
- **Generator-source identity — partial.** E04 and E05 retain fingerprint-exact historical generator-source bundles. E01, E02, and E03 remain `ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE`.

**Publication-facing statement.** The frozen E01–E03 result artifacts and their manifests were preserved and independently validated, but the exact dirty-worktree generator source state used for those historical runs was not fully recoverable. E04–E05 retain fingerprint-exact historical generator-source bundles. Article-V1 figures and tables are generated deterministically from the preserved frozen artifacts rather than by rerunning the experiments.

Do not describe E01–E05 as byte-exactly reproducible from source, and do not silently omit this limitation. It is a bounded historical disclosure issue and is **not** a reason to rerun E01–E03. P2B was not run and is not authorized by this freeze.

---

## 11. Deterministic regeneration

```bash
python projects/frontiers_article/publication_v1/scripts/build_publication_v1.py
```

The entry point verifies frozen source hashes, extracts the publication-source CSVs, verifies the scientific assertions, generates the analytic table, generates Figures 1–4 and their captions, writes the manifest, and re-verifies every output hash. `--check` additionally fails if a rebuild from identical frozen inputs changes any previously built output.

It runs no experiment. It imports nothing from `src/gifted_masking/`; dependencies are the Python standard library, NumPy, and Matplotlib only.

Deterministic test subset:

```bash
python -m unittest tests.test_publication_v1
```

**Do not run `scripts/verify.sh` for this layer.** It invokes `cli robustness --suite full`, which is stochastic full-suite generation. Only the deterministic subset above is appropriate.

### 11.1 Determinism status

Rebuilding from identical frozen inputs reproduced **all 22 outputs byte-identically**, PDFs and PNGs included: PDF `CreationDate` is suppressed, PNG `Software` metadata is cleared, and the SVG hash salt is fixed. Verified both by the build's own `--check` mode and by an independent recursive byte diff against a snapshot taken before the rebuild.

Figure bytes are nevertheless renderer-dependent across Matplotlib versions. The authoritative reproducibility layer is therefore the **source → script → publication-data hash chain** in the manifest, which is independent of renderer metadata. This build: Python 3.14.6, NumPy 2.5.1, Matplotlib 3.11.1.

---

## 12. Confirmations

- **No E01–E05 experiment was rerun.** No stochastic simulation entry point was invoked; no seed was added or extended; no trajectory was generated; no sensitivity sweep was run.
- **The publication scripts consume frozen derived artifacts only.** Extractors read `results/summaries/` and the frozen manifests; figures read only `publication_v1/data/`. No experiment runner appears anywhere in the dependency graph, and the test suite asserts that no publication script imports `gifted_masking`.
- **No frozen result was silently replaced by a recomputed value.** Where a value is recomputed, it is a closed-form re-derivation asserted to equal the frozen value, and the build stops if it does not.
- **No E06/M4 evidence was used**, and no new scientific claim was introduced.

### 12.1 Fail-closed assertions enforced at build time

| Experiment | Assertion |
|---|---|
| E01 | pinned selector and all three metric names exist; `ci_status = student_t_95`; the C.5 identity `regret = −(T−1)/T × sampling` holds; the final-mask interval spans zero before any null annotation is drawn |
| E02 | the `rejected` stratum exists and every extracted row carries it; each frozen arm reward equals the affine closed form |
| E03 | 357 tested cells; exactly 5 master rows per cell; objective fields identical across masters; no conflicting learned action; 243 learned-suboptimal cells; inconclusive cells present; categories partition the grid |
| E04 | primary response field is `mean_settled_any_good_auth_argmax`; both frozen headline effect names exist; values equal −0.2340 and −0.4704; every series has five K points |
| E05 | flat crossing equals `0.31285211267605634`; objective crossing equals `8/17` exactly; hierarchical status is `no_crossing_below` with no bf, zero valid bootstrap crossings, and `decision_eligible = False`; pooled means reproduce the frozen dense-boundary responses; displacement and objective advantage match in closed form |
| scope | no E06/M4 path enters the graph; every declared transformation is in the permitted vocabulary |

A failed assertion stops the build. The build never adapts to a changed dataset, and an artifact is never regenerated to make a hash pass.

---

## 13. Evidence-matrix handling

Four **series-level** rows were appended for the plotted series. All 29 existing claim adjudications are byte-identical and untouched; no reconciliation status, wording ceiling, or estimate was altered. The matrix was not exploded into one row per plotted point.

| New row | Series | Panel |
|---|---|---|
| `E02-S1-ARM-REWARDS` | M1 per-arm expected reward against d | Figure 2c |
| `E03-S1-GRID-MAP` | per-cell classification and exact Q gap over the tested grid | Figure 3a, 3b |
| `E04-S1-K-RESPONSE` | K-response by architecture and abundance regime | Figure 4a |
| `E05-S1-BF-RESPONSE` | modal good-authentic fraction against bf | Figure 4b |

Each carries its source artifact, literal selector with x and y fields, panel target, inferential unit, and scientific role. E01's panel plots only already-adjudicated rows, so it needed no addition.

---

## 14. Remaining work for Stage 2

Stage 2 is manuscript construction. It is out of scope here and no manuscript prose was written.

1. **Write the manuscript from the frozen authorities**, not by patching the stale Results/Discussion chapters. The removal register in Section G of the manuscript evidence freeze must be executed: `226/357`, `63.3%`, the `0.950` figure, one-run child-bootstrap intervals, obsolete E04 K = 8 comparisons, and all M4 numerical path results must not survive into V1.
2. **Resolve or formally accept the standing E05 BLOCKER.** Proposition G2 is a two-action softmax result and does not govern E05's eight-action across-child modal fraction. Until this is closed, every E05 sentence is descriptive only and fixed temperature stays on the unresolved-contributor list.
3. **Resolve or formally accept the E01–E03 generator-source provenance gap.** Either the owner accepts the limitation as worded in Section 10, or a separately authorized P2B reproduction anchor is created. `ARTIFACT_PROVENANCE_GAP_OPEN` remains until one of those happens. Neither is authorized by this freeze.
4. **Complete the outstanding novelty adjudication** described in the handoff before V1-02 closes.
5. **Decide supplementary material.** Several frozen adjudicated results are not in the four main figures — E01 forced-exploration and counterfactual-feedback manipulations, E01 λ contrasts, E03 sentinel sensitivities and the harsh boundary cell, E04 identity and multiple-good controls, E05 endpoint contrast. They are verified and available; whether they appear as supplement is a Stage-2 editorial decision, not a new experiment.
6. **Journal formatting.** Figure sizes target a ~7.2 in double-column width; final trim sizes, file format, and numbering follow the target journal's specification once chosen.

None of the above authorizes new stochastic science.

---

## 15. Stage-1 status

| Item | Status |
|---|---|
| Frozen E01–E05 artifact verification | **PASS** — 33/33 protected outputs, 18/18 matrix-referenced files |
| Article-V1 authority durability | **COMMITTED** before publication generation |
| Publication-source data | **BUILT** — 10 CSVs, all selectors pinned |
| Analytic-results table | **BUILT** — closed-form, asserted |
| Figures 1–4 | **BUILT** — PDF + PNG, captions generated from the same data |
| Publication manifest | **WRITTEN** — full provenance chain |
| Determinism | **VERIFIED** — 22/22 outputs byte-identical on rebuild |
| Scientific assertions | **ALL PASS** |
| Experiments rerun | **NONE** |
| E06/M4 leakage | **NONE** |
| E05 G2 / temperature exclusion | **BLOCKER OPEN** — descriptive reporting only |
| E01–E03 generator-source provenance | **LIMITATION DOCUMENTED, NOT RESOLVED** |
| Manuscript | **NOT WRITTEN** — Stage 2 |

**ARTICLE_V1_STAGE1_COMPLETE**
