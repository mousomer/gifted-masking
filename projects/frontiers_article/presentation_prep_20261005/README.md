# Simulation explanations and PowerPoint preparation

**Current combined lecture — methods followed by results:**
[PowerPoint](../../../output/pptx/masking_methods_then_results.pptx) and
[matching 15-minute speaker notes](separated_20261006/SPEAKER_NOTES.md).
Sixteen slides: opening (1–3), methods M0–M4 (4–8), results M0/E01 through
M3/E05 (9–13), M4 deferred-results status (14), and discussion (15–16).
No results appear in the five methods slides. This combined sequence replaces
appending the earlier decks, which duplicated material. See
[production record](separated_20261006/QA.md). Actual duration needs rehearsal.

**Earlier separate results and discussion deck:** [PowerPoint](../../../output/pptx/masking_results_discussion.pptx)
and [PDF preview](../../../output/pdf/masking_results_discussion.pdf), with
[separate speaker notes](results_discussion_20261006/SPEAKER_NOTES.md).
This eight-slide section contains five results slides and three discussion
slides, with 660 seconds of planned narration. Append it after the author's
existing introduction/models. It contains no opening or standalone setup slides.
See [production records](results_discussion_20261006/QA.md).

**Earlier eleven-slide lecture version:** [15-minute spoken script](LECTURE_SCRIPT_15_MIN.md),
requested after the first-set delivery. It follows the same eleven slides and
allocates 900 seconds, including brief pauses and diagram cues. It contains
1,713 spoken words. The delivered PowerPoint/PDF and their shorter embedded notes
remain unchanged; the 12-minute production records below describe that earlier
edition. Use the newer combined lecture and its matching notes above for the current talk.

Prepared 5 October and revised 6 October 2026 for the author’s **12-minute presentation slot**. The active plan has **eleven main slides with 11 minutes of speaking and one minute reserved for pauses or a question**. Eight backup slides sit outside the timed talk. The audience remains a mixed research audience. The full simulation guide remains available as background. The **eleven-slide first set is built** as an [editable PowerPoint](../../../output/pptx/masking_mechanisms_first_set.pptx) with a [PDF viewing copy](../../../output/pdf/masking_mechanisms_first_set.pdf). It includes the generated child illustration, Dash film still, model diagrams, and source-grounded results. Eight backups remain planned and are not included in this first set. The existing one-slide draft remains preserved. See [production QA](main_deck_20261006/QA.md) and the [exact rendered content](main_deck_20261006/RENDERED_CONTENT.json).

## Files

| File | Use |
| --- | --- |
| [OPENING_AND_M0_PLAN.md](OPENING_AND_M0_PLAN.md) | Detailed S01–S04 plan: introduction, Dash, social learning, and M0 diagram/theory/simulation evidence |
| [SIMULATION_GUIDE.md](SIMULATION_GUIDE.md) | Detailed explanation of M0–M4 and E01–E06, equations, worked examples, measurements, findings, and limitations |
| [PPT_STORYBOARD.md](PPT_STORYBOARD.md) | Slide copy, visual plans, timing, speaker notes, and evidence references |
| [SLIDE_SPEC.json](SLIDE_SPEC.json) | Structured version of the 19-slide plan: eleven main slides and eight backups |
| [SOURCE_INDEX.json](SOURCE_INDEX.json) | Repository paths, SHA-256 hashes, figure-panel selectors, table definitions, exact configurations, and selected archived evidence rows |

The guide and storyboard are the explanation deliverables. The JSON files retain the authoring plan and identify the delivered main-slide artifacts. Exact rendered text and chart values are recorded in the production content manifest. Source IDs such as `FIG9` and `E02_EFFECTS` resolve in the source index. Paths inside that JSON are repository-relative, with the absolute repository root recorded for local use.

## Twelve-minute delivery plan

| Slide | Topic | Duration | Cumulative finish |
| --- | --- | ---: | ---: |
| S01 | What mechanisms could explain masking? | 0:35 | 0:35 |
| S02 | A close second | 0:30 | 1:05 |
| S03 | Learning from social experience | 0:45 | 1:50 |
| S04 | M0: masking or authenticity | 1:20 | 3:10 |
| S05 | M1 / E02: more participation can mean less expression | 1:25 | 4:35 |
| S06 | M2 / E03: persistent consequences change optimal behaviour | 1:40 | 6:15 |
| S07 | M3 / E04: finding a receptive context does not ensure repeated use | 1:40 | 7:55 |
| S08 | M3 / E05: learned and objective boundaries differ | 1:15 | 9:10 |
| S09 | M4 / E06: behaviour changes receptivity | 0:45 | 9:55 |
| S10 | What the evidence establishes | 0:35 | 10:30 |
| S11 | Similar concealment can require different explanations | 0:30 | 11:00 |
| Reserve | Pauses or one question | 1:00 | 12:00 |

Rehearse the approximately 1,070-word main script with the actual figures. The timings allow room for chart explanation; they are estimates until rehearsed. Start the conclusion at 10:30. The evidence slide S10 is already shortened to 35 seconds. Keep the model explanations and conclusion. Open backup slides only after the timed talk.

## Scientific contract for the deck

- Use the maintained kernels to explain mechanisms and the archived E01–E05 evidence to report findings. Current kernels alone do not establish historical reproduction of E01–E03.
- Keep M4/E06 in one explicitly labelled extension slide, with detailed controls in the backup slides. Describe the implemented mechanism and deferred design without promoting smoke diagnostics to confirmed hysteresis.
- Keep objective reward, transformed reward, learned values, and the full-information dynamic benchmark distinct.
- Preserve every sign, comparison direction, denominator, window, and interval. “Points” means percentage points only for proportions. Intensity remains on a unit disclosure scale unless explicitly converted.
- E01's history result concerns post-initial sampling. Its final-window history interval spans zero. E01's information interventions and weighting result answer different questions.
- E02's headline effects pool p=.75/.85 after initial rejection. Its regret/intensity identity is not independent corroboration, and independent arms do not generalize across disclosure levels.
- E03's 243/357 result counts parameter cells. Its sensitivity denominator is five disagreement sentinels times five masters. Numerical threshold brackets are not statistical confidence intervals.
- E04's context-count effect depends on architecture. Encounter, total masking, individual modal classification, and regret measure different outcomes.
- E05's learned threshold is a modal-population crossing, not the onset of majority masking. The hierarchical crossing is left-censored.
- Applied implications remain hypotheses about what to measure or test. Simulated learners are not human participant data.

## Visual and production brief

Use a 16:9 PowerPoint with a restrained scientific editorial design. A supplied template or author preference takes precedence. Without one, use a light background, dark text, consistent action colours, and a distinct extension colour for M4/E06. Do not rely on colour alone to identify curves. Keep setup titles factual and reserve claim titles for supported findings.

Use native editable tables, equations, and data charts. The author-requested explanation diagrams may be editable native diagrams. The ten integrated-article figures and their SVG versions are scientific references. Several contain multiple panels suitable for separate slides. Preserve full scientific labels when isolating panels. Do not shrink a journal page of panels onto a slide or imply that an imported SVG is an editable chart. If a reference figure remains an image, disclose that limitation in the handoff.

Preserve the archived series and uncertainty when reconstructing charts. For E05, retain archived crossing estimates and intervals without refitting or re-running the bootstrap. For E03, use the frozen grid and sensitivity classifications without new simulations. Avoid decorative imagery that adds no explanatory value, in line with the project RDS.

Prefer titles at least 32 pt and body text at least 20 pt for the main talk. Keep full equations, large tables, and technical qualifiers in speaker notes or the appendix when they cannot be read comfortably on the main slide. Caveats that change the interpretation, such as a denominator or E06's deferred status, must remain visible.

Each slide's speaker notes should contain the prepared explanation and its concrete source paths. Source identifiers alone are not sufficient citations in a delivered deck. Expand them using SOURCE_INDEX.json. Keep production and validation commentary out of the deck and its speaker notes.

Use the current Presentations skill for generation, including its template picker if available, the JavaScript artifact-tool workflow, rendering, and visual inspection. Load workspace dependencies through the Codex dependency tool if needed. Do not install a new presentation dependency or use a desktop LibreOffice installation as a workaround.

## Full-deck generation request (future backups)

The request below is retained for the eventual 19-slide edition. The delivered first set contains only S01–S11.

> Generate an editable 16:9 PowerPoint from `projects/frontiers_article/presentation_prep_20261005/SLIDE_SPEC.json`, using `SIMULATION_GUIDE.md` for the detailed explanations and `SOURCE_INDEX.json` for evidence. Produce exactly 19 slides: S01–S11 as the 11-minute main talk within the author’s 12-minute slot, and A01–A08 as backup slides outside the timed talk. Reserve one minute for pauses or a question. Use the shortened speaker notes and keep each main slide to its assigned time. Do not add an agenda slide, turn the backup slides into main content, or restore the former 31-minute narrative. Follow OPENING_AND_M0_PLAN.md for the first four slides, including the child illustration, Dash film still, learning diagram, and M0 setup/theory/simulation distinction. Revise the earlier S01 render. Include the prepared speaker notes and resolved source citations. Follow the scientific and visual contract in this directory's README. Use editable scientific charts, equations, tables, and explanatory diagrams wherever specified, preserving all denominators, comparison signs, uncertainty, and archived values. Keep M4/E06 explicitly marked as an implemented, deferred extension. Use the integrated article's figures as references and their archived source tables as the numerical authority. Do not run simulations, refit curves, change scientific claims, or alter existing article assets. Render the deck, inspect every slide, repair clipping or unreadable text, and deliver the final PPTX with a PDF preview. Use the current Presentations skill and the bundled dependency/runtime paths. Record any evidence object that must remain an image.

## Preparation acceptance and verification

The complete pack retains all five model mechanisms and all six experiment designs. The timed main talk gives each model its mechanism and central lesson. The full guide and backup slides retain detailed methods and additional findings. Acceptance requires eleven main slides totalling 660 seconds, a 60-second reserve within the 720-second slot, eight backup slides outside that timing, explicit evidence status, matched source references, and one-to-one correspondence between the Markdown storyboard and JSON slide specification. Every selected file hash and every local link must resolve. The three illustrative numeric examples must agree with the maintained equations.

Governed context: LOCAL_FIX/development for this documentation-only request. The generic task probe suggested FEATURE without matching a named scenario; no additional route exists. RDS 0.16 records the scope, the 12-minute limit, and acceptance criteria. Existing source, article, and evidence changes in the working tree predate this task and remain preserved.

The declared full verifier remains `./scripts/verify.sh`. Its full robustness runs and writes to scientific outputs are outside this presentation preparation under the RDS's preserved-evidence boundary, so it is not a claimed full-project acceptance gate here. Focused model and publication checks, the governance hook, the integrated article's read-only evidence verifier, and local pack checks establish this task's narrower acceptance. Preparation does not establish rendered-slide or PowerPoint visual acceptance.

### Initial long-form preparation checks, 6 October 2026

- `./gov check`: passed. The governance verification hook passed, with its existing repository sanitation warnings for parent-traversal references and spaced filenames.
- Workspace Python with `PYTHONPATH="$PWD/src"`: 104 focused tests passed in 66.997 seconds. Modules: `test_core`, `test_m0`, `test_m1`, `test_m2`, `test_m2_optimal_policy`, `test_m3`, `test_m4`, `test_determinism`, `test_publication_v1`, `test_revision_figure_text`, `test_integrated_article_figures`, and `test_integrated_article_document`. The initial invocation omitted PYTHONPATH and failed package imports; the corrected invocation above passed. The M2 benchmark tests exercise auxiliary benchmark/map CSV writers, so this entire test selection is not described as read-only.
- `python -B projects/frontiers_article/integrated_article_20261004/verify_integrated.py`, using the workspace interpreter: passed. This read-only verifier confirmed all 33 protected experiment outputs, 18 evidence-matrix references, prior-revision preservation, and the integrated article's source/figure/build identities.
- Preparation checks passed: 85 SHA-256 checks, 37 local Markdown links, 26 main slides, eight appendix slides, 31 minutes of main-slide timing, exact storyboard/specification correspondence, and deterministic worked examples.
- `git diff --check`: passed. Full `./scripts/verify.sh` was not run for the preserved-evidence reason above. No rendered PPTX, PDF preview, or slide visual acceptance is claimed.

### Twelve-minute revision checks, 6 October 2026

The active storyboard and JSON now match exactly at ten main slides and eight backups. Main timings total 660 seconds, with a 60-second reserve inside the 720-second slot. The main spoken notes contain 1,025 words. Coverage checks retain M0–M4 and E01–E06. All 85 source/dependency hash checks and 37 local links passed; only the deliberately updated RDS/current-state hashes were refreshed. The full simulation guide is byte-identical to its pre-revision version. Governance and whitespace checks passed. The integrated article's read-only verifier passed again, including all 33 protected experiment outputs. The earlier 104-test model/publication result remains historical evidence; those tests and the full simulation-running verifier were not rerun for this content-and-timing-only revision. Actual speaking duration remains a rehearsal check.

### First-slide creation, 6 October 2026

S01 now introduces the documented phenomenon and an explicit learning-mechanism question. See [SLIDE_01_SOURCES.md](SLIDE_01_SOURCES.md) for the primary citations and the reason for using qualified age wording. The one-slide PPTX contains native editable text and full notes. Package, font, layout, and import checks passed; the reimported final slide was rendered and visually inspected. The 35-second opening and 660-second main total are unchanged. The full deck remains unrendered. No model or archived experiment output changed, and the simulation-running verifier was not rerun for this slide-only change.

### Opening and M0 planning revision, 6 October 2026

The author requests a documented plan for the introduction, Dash running second, learning from social experience, and M0. The active specification and storyboard now have eleven main slides, with Dash inserted as S02 and M0 as S04. The first four take 190 seconds; all main slides total 660 seconds. S10 and S11 are shortened to 35 and 30 seconds. OPENING_AND_M0_PLAN.md contains the visual drafts, notes, analytic threshold, exact archived comparisons and intervals, and evidence boundaries. Existing S01 renders remain unchanged earlier drafts and are not representations of the new plan. This is documentation only; production and rehearsal remain pending.

Focused documentation checks passed: exact storyboard/spec correspondence, eleven main slides and eight backups, 660+60 seconds, unchanged M1–M4 and backup content, 73 source/artifact path-and-hash checks, 29 local links, analytic reward arithmetic, and archived effect signs/intervals. The read-only integrated-article verifier passed, including preservation of all 33 protected experiment outputs. The detailed guide, M0 code, and earlier PPTX/PNG remain byte-identical. Governance and whitespace checks passed. The earlier model-test result remains historical; no simulation, estimator, or full `./scripts/verify.sh` run was performed for this documentation-only revision under the preserved-evidence boundary.

### First-set production, 6 October 2026

All eleven main slides are delivered as an editable PPTX and matching raster PDF preview. Every reimported PPTX slide was visually inspected. Package, layout, font, native-chart and source-value checks passed; all eleven PDF pages rendered at 1920×1080. There are three native charts, four native tables, editable diagram shapes and connectors, and two raster images. The built-in image generator created the child illustration; the Dash image is an actual film still. See [asset sources and exact prompt](assets/ASSET_SOURCES.json) and [production QA](main_deck_20261006/QA.md). Main notes total 1070 words, with 660 seconds allocated and a 60-second reserve. Rehearsal and the eight backup slides remain pending. M4/E06 remains explicitly deferred. No scientific output was regenerated. Native PowerPoint application execution was not tested; native charts retain exact literal data without an embedded Excel workbook.
