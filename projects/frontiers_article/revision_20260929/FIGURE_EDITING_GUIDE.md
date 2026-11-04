# Editing text in the paper figures

To change wording in the current paper's six figures, edit
[`figure_text.py`](figure_text.py). Titles, axes, legends, diagram boxes,
outcome labels, and annotation templates are collected there by figure number
and panel letter. You do not need to edit the plotting calculations.

The six image-generating functions remain together in
[`generate_figures.py`](generate_figures.py). They read existing archived
results; rebuilding these images does not run a simulation or fit an estimator.

## Quick start

1. Open `figure_text.py` and find the figure number and panel letter.
2. Change the quoted wording, keeping the dictionary keys and any template
   placeholders unchanged.
3. Preview the affected figure in a separate directory using the command below.
4. Inspect the PNG or PDF for wrapping, clipping, and meaning. Once satisfied,
   rebuild all six canonical figures and run the read-only verification.

For example, Figure 2 panel A uses `FIGURE_TEXT[2]["A"]["title"]`:

```python
"title": "Weighting at fixed\nreceptivity (p = .65)",
```

You can replace the wording with, for example:

```python
"title": "Outcome weighting\nat fixed receptivity (p = .65)",
```

The `\n` makes a line break. This changes the heading only; it does not change
the receptivity value or the plotted results. Do not change the `"title"` key.

All shell commands below are run from the repository root:

```sh
cd /Users/omer/workspace/personal/repos/gifted-masking
```

List the available figure functions without writing any outputs:

```sh
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/revision_20260929/generate_figures.py --list
```

Preview just Figure 2:

```sh
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/revision_20260929/generate_figures.py --figure 2 --preview-dir /Users/omer/workspace/personal/repos/gifted-masking/tmp/figure-preview
```

Preview several figures by repeating `--figure`:

```sh
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/revision_20260929/generate_figures.py --figure 2 --figure 6 --preview-dir /Users/omer/workspace/personal/repos/gifted-masking/tmp/figure-preview
```

Preview outputs appear under `tmp/figure-preview/png/` and
`tmp/figure-preview/pdf/`, with a separate `FIGURE_PROVENANCE.json` in the
preview directory. Omitting `--figure` while supplying `--preview-dir` previews
all six. Reusing a preview directory replaces the selected figures and its
manifest; older, unselected images may remain there, so use the manifest or a
fresh directory to identify the latest build.

Preview directories must use an absolute path to a child of repository `tmp/`
or an allowed system temporary directory, not the temporary root itself.
Paths are resolved before
validation, including symlinks. `--figure` without `--preview-dir` is rejected
so a partial build cannot replace the canonical provenance.

When ready to replace the paper's six current figure pairs:

```sh
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/revision_20260929/generate_figures.py
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/revision_20260929/verify_revision.py
```

The no-argument build overwrites only this revision's six PNGs in `figures/`,
six PDFs in repository `output/pdf/revision_20260929/`, and
`FIGURE_PROVENANCE.json`. It does not rebuild older article packages or update
the manuscript's DOCX/PDF previews.

## Figure function directory

Each `figN()` has no arguments and draws one figure using its corresponding
catalog section. Use the command-line entry point or `render_figures()` for
normal work: these verify source hashes, validate text, configure outputs,
and write provenance. Calling a `figN()` directly bypasses that orchestration.

| Figure | Function | Text section | Panels and subject |
| --- | --- | --- | --- |
| 1 | `fig1()` | `FIGURE_TEXT[1]` | A: mechanism boxes and learned allocation; B: availability, encounter, and sustained use. |
| 2 | `fig2()` | `FIGURE_TEXT[2]` | A: weighting; B: subjective threshold; C: early history; D: information. |
| 3 | `fig3()` | `FIGURE_TEXT[3]` | A: expected reward; B: variance; C: engagement, intensity, and endpoint use. |
| 4 | `fig4()` | `FIGURE_TEXT[4]` | A: static and dynamic thresholds; B: five long-horizon sentinels. |
| 5 | `fig5()` | `FIGURE_TEXT[5]` | A–F: masking, modal selection, successful encounter, receptive abundance, regret, and timing. |
| 6 | `fig6()` | `FIGURE_TEXT[6]` | A: learned versus objective boundaries; B: actual masking versus modal classification. |

Their stable output stems, used for both PNG and PDF, are:

```text
Figure_1_mechanisms_and_opportunity_use
Figure_2_weighting_history_information
Figure_3_graded_engagement_intensity
Figure_4_dynamic_thresholds_persistence
Figure_5_context_encounter_sustained_use
Figure_6_learned_boundary_actual_masking
```

## Where to change each kind of text

| You want to change | Edit in the catalog |
| --- | --- |
| A panel heading | `FIGURE_TEXT[number][letter]["title"]`; Figure 1 uses `"heading"`. |
| A horizontal or vertical axis label | The panel's `"xlabel"` or `"ylabel"`; repeated labels may be in `"shared"` or `SHARED_TEXT`. |
| Architecture names across figures | `SHARED_TEXT["architectures"]`. Keep keys `flat_2k`, `hierarchical`, and `global_mask`; change only their display names. |
| The repeated masking, modal-classification, or comparison-cost labels | `SHARED_TEXT["final_window_masking_percent"]`, `"good_authentic_modal_percent"`, or `"comparison_cost"`. |
| Conceptual boxes in Figure 1 | Keys ending in `"_box"` in panels A and B. |
| The names of outcomes in the forest plots | Keys ending in `"_outcome"` in Figure 2 C/D or Figure 3 C. |
| A legend entry | Keys ending in `"_legend"` or `"_legend_format"`, or the shared architecture names. |
| Text beside a bar or threshold | Keys ending in `"_note"`, `"_format"`, or `"ticks"`. |
| The spacing between a panel letter and title | `SHARED_TEXT["panel_title_format"]`. |
| The caption underneath a figure in the paper | `FIGURE_CAPTIONS.md` and the matching caption in `MANUSCRIPT.md`, not this catalog. |

Some labels are shared deliberately. For example, changing the architecture
name in `SHARED_TEXT` updates legends and categorical ticks consistently in
Figures 5 and 6. It does not rename the architecture in any data table.

### Line breaks and mathematical symbols

Use `\n` in an ordinary quoted string to wrap text. Keep the comma after each
dictionary entry. Use double quotes around wording containing apostrophes.
Existing raw strings beginning with `r`, such as
`r"Negative-outcome weight $\lambda$"`, preserve the backslash required by
Matplotlib's mathematical notation. Do not add an `r` prefix to a string whose
`\n` must create a real line break.

### Numbers and templates

Keys ending in `_format` receive numbers from the generator. For example:

```python
"bar_format": "{value:.2f}%",
"crossing_note_format": "Archived crossing: {learned:.3f}\n95% CI [{lo:.3f}, {hi:.3f}]",
```

Here `.2f` means two decimal places and `.3f` means three. The generator
supplies `value`, `learned`, `lo`, and `hi`; preserve those placeholder names.
For literal braces in a `_format` string, use `{{` and `}}`. Ordinary strings
without `_format` are not passed through formatting and do not need doubled
braces. The catalog is checked before output is written; missing keys,
incorrect types, and invalid placeholders produce an error.

Some scientific numbers are intentionally fixed wording, such as Figure 2's
40.30-point difference and Figure 6's objective-threshold label. They are not
new calculations or editable model parameters. Keep numerical statements,
units, time windows, and denominators consistent with the plotted data and
captions. In particular, a modal learner fraction is not an action-level mask
rate, and a descriptive range is not a confidence interval.

## Layout and helper functions

For wording changes, start with `figure_text.py`. If the new wording is longer,
add a line break or shorten it before changing the layout. The generator's
layout controls remain near the drawing code:

| Function or setting | Responsibility |
| --- | --- |
| `style()` | Shared font family, sizes, line widths, resolution, and PDF font settings. |
| `title(ax, letter, text)` | Panel letters and title spacing. |
| `forest(ax, entries, xlabel, xlim)` | Effect estimates, interval bars, and outcome labels. |
| Nested `box()` and `arrow()` in `fig1()` | Conceptual diagram box geometry and arrows. |
| `figsize`, `subplots_adjust`, and `set_position` inside each builder | Canvas size, margins, and panel positions. |
| `save(fig, stem)` | Canvas-bound checks, PNG/PDF output, and output hashes. |
| `rows(name)`, `sha(path)`, and `record(...)` | Read archived CSVs, hash files, and record plotted data and selectors. |
| `validate_text_catalog(...)` | Check catalog structure, value types, and template placeholders before rendering. |
| `resolve_preview_dir(...)` | Validate an isolated preview destination, including existing output symlinks. |
| `new_provenance(...)` | Create fresh build bookkeeping without retaining previous output hashes. |
| `FIGURES`, `render_figures(...)`, and `main(argv=None)` | Function registry, validated builds, and command-line selection. |

The bounds check catches authored headings, annotations, and axis labels
extending beyond the canvas. It does not prove that text does not overlap
another element, and it does not fully check legends and tick labels. Always
look at the preview after an edit, especially if it lengthens a legend.

Rendering uses Matplotlib's non-interactive backend and updates process-local
plot style and output/provenance state. Build invocations reset their state;
the functions are intended for one build at a time, not concurrent threads
inside one Python process. No random generator is used.

## Captions and verification

Captions are separate from the text drawn inside the images. If you change a
caption, edit both [`FIGURE_CAPTIONS.md`](FIGURE_CAPTIONS.md) and its matching
section in [`MANUSCRIPT.md`](MANUSCRIPT.md). The revision checker requires them
to agree. Image rebuilding does not synchronize or rewrite either document.

Every build records the generator hash, the text-catalog hash, the 11 protected
input hashes, and the rendered output hashes. If you edit the catalog without
rebuilding the canonical figures, `verify_revision.py` reports that the catalog
has changed since the last build. Previewing alone does not mark canonical
figures as current.

Focused tooling tests are available without running a scientific experiment:

```sh
/Users/omer/workspace/venvs/venv314/bin/python -B -m unittest tests.test_revision_figure_text -v
```

Do not use `scripts/verify.sh` or the repository's general `figures` command
for text-only work. They can run simulations and write scientific results.

## Historical generators

The following files are retained for their earlier versions. They are not the
editing targets for the current six figures, and were not relocated or changed.
Paths below are relative to the repository root.

| File | Entry points | Status |
| --- | --- | --- |
| `projects/frontiers_article/v2_figures/generate_v2_figures.py` | `figure_1()`–`figure_4()`, `main()` | Historical four-figure V2 package. |
| `projects/frontiers_article/publication_v1/scripts/figures.py` | `figure_1()`–`figure_6()`, `build_all()` | Earlier six-figure publication layer; its surrounding build also updates extracted data and manifests. |
| `src/gifted_masking/plotting/legacy_figures.py` | `fig_m0`, `fig_m1`, `fig_m2`, `fig_m3`, `fig_m0_bistability`, `fig_m3_bflpe`, `fig_m4`, `fig_m0_by_risk`, `fig_downstream_by_risk`, `generate_all` | Simulation-driven plotting; not appropriate for wording-only rebuilds. |
| `simulations_old/simulations1/masking_rl.py`, `simulations_old/simulations2/masking_rl.py`, `simulations_old/simulations3/masking_rl.py` | Historical `fig_*` functions | Combined simulation and plotting sources. |
| `projects/frontiers_article/audit_snapshots/` and `submission_v2/archive/evidence_package/` | Archived copies | Historical provenance; leave intact. |
