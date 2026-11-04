# Single illustrated article

This edition consolidates the supported scientific claims, essential methods,
and robustness results into one article with ten figures. The technical appendix
is part of that same article. Earlier revision files and scientific evidence
remain unchanged.

## Read or edit the article

- `ARTICLE.md` is the single authoring source, including the technical appendix,
  references, inline figures, and captions.
- `../../../output/docx/integrated_article_20261004.docx` is the editable Word
  article. Its equations are native editable Word mathematics.
- `../../../output/pdf/integrated_article_20261004.pdf` is the matching PDF,
  exported from that Word document rather than laid out independently.
- `CLAIM_COVERAGE.md` is an internal route for all C01–C23 and the restored
  methods/results. It is not required reading alongside the article.

Edit `ARTICLE.md` and rebuild for repeatable production. Edits made only in Word
will not propagate back into the Markdown source and can be overwritten by a
later build. RDS version 0.11 records the scope and acceptance criteria.

## Change text inside a figure

All ten figures' visible labels are gathered in **`figure_text.py`**. Find the
figure number in `FIGURE_TEXT`; panel letters match the image. Shared axis labels
and architecture names are in `SHARED_TEXT`. Example edits:

```python
FIGURE_TEXT[4]["A"]["title"] = "Weighting at fixed\nreceptivity"
FIGURE_TEXT[8]["title"] = "Sensitivity of the learning gap"
FIGURE_TEXT[8]["row_labels"][9] = "Learning rate α = .03"
```

Change the existing dictionary entries in the file; do not append these examples
as additional overrides. `\n` creates a line break. Preserve the named braces in
`_format` strings, such as `{count}`, `{p:g}`, and `{eta:g}`. Numerical labels and
denominator descriptions are science-linked text: do not change their meaning
without checking the source table and caption.

Captions printed below the images live in `FIGURE_CAPTIONS.md` and appear inline
in `ARTICLE.md`. If changing a caption, keep those two copies identical. Changing
a figure label does not automatically rewrite its caption or the surrounding
article text.

From the repository root, list figures or preview a selected figure safely:

```sh
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/integrated_article_20261004/generate_figures.py --list
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/integrated_article_20261004/generate_figures.py --figure 8 --preview-dir /private/tmp/integrated-figure-8-preview
```

The preview goes into `figures/` below the chosen temporary directory, together
with its own provenance manifest. Repeating `--figure` selects multiple images.
Selection requires a preview directory and cannot silently replace the article's
canonical images. The renderer rejects protected paths and escaping symlinks.

## Figure and function directory

`generate_figures.py` is the one rendering entry point. Six existing drawing
functions are loaded read-only from the preserved September revision, with this
edition's text, numbering, output hooks, and layout. Four local functions draw
the additions. No experiment code is imported.

| Figure | Subject | Drawing function | Text key |
| ---: | --- | --- | --- |
| 1 | Mechanisms and opportunity use | Preserved `fig1()` | `FIGURE_TEXT[1]` |
| 2 | M2 state/reward/transition kernel — new | Local `fig2()` | `FIGURE_TEXT[2]` |
| 3 | Four context-choice architectures — new | Local `fig3()` | `FIGURE_TEXT[3]` |
| 4 | Weighting, history, information | Preserved `fig2()` | `FIGURE_TEXT[4]` |
| 5 | Engagement, intensity, and endpoint use | Preserved `fig3()` | `FIGURE_TEXT[5]` |
| 6 | Dynamic thresholds and persistence | Preserved `fig4()` | `FIGURE_TEXT[6]` |
| 7 | Complete 357-cell dynamic map — new | Local `fig7()` | `FIGURE_TEXT[7]` |
| 8 | Complete 15-setting sensitivity matrix — new | Local `fig8()` | `FIGURE_TEXT[8]` |
| 9 | Context encounter, use, and search costs | Preserved `fig5()`; local layout hook | `FIGURE_TEXT[9]` |
| 10 | Learned crossing and actual masking | Preserved `fig6()` | `FIGURE_TEXT[10]` |

`render_figures()` coordinates rendering. `grid_data()` and `sensitivity_data()`
provide the exact frozen inputs to the new quantitative displays and validate
their cardinalities and counts. `save()` writes PNG and SVG. PNG is embedded in
Word; SVG retains text as text for vector editing. Manual SVG changes are not
reproducible from the catalog and are overwritten on regeneration.

Do not edit the older revision to change this edition. The inherited drawing
functions deliberately preserve numerical artists; tests compare their data
fingerprints with the preceding revision. If a label needs more room, shorten
it or add a line break first; layout changes belong in the local generator.

## Rebuild the complete article

After approving the wording/preview, run from the repository root:

```sh
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/integrated_article_20261004/generate_figures.py
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/integrated_article_20261004/build_article.py
```

The first command regenerates ten PNG/SVG pairs and `FIGURE_PROVENANCE.json`.
The second regenerates the DOCX and matching PDF and writes
`BUILD_METADATA.json`. It uses existing Pandoc, native Word equations, and the
bundled LibreOffice renderer. It does not install dependencies or use desktop
LibreOffice. Page PNGs are saved under `output/qa/integrated_article_20261004/`
in a timestamped render directory for inspection.

## Verify after editing

```sh
./scripts/verify-governance.sh
/Users/omer/workspace/venvs/venv314/bin/python -m unittest tests.test_publication_v1 tests.test_revision_figure_text tests.test_integrated_article_figures tests.test_integrated_article_document -v
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/revision_20260929/verify_revision.py
/Users/omer/workspace/venvs/venv314/bin/python -B projects/frontiers_article/integrated_article_20261004/verify_integrated.py
```

Inspect every final rendered page after any production change. Tests establish
source identity, counts, numeric artist preservation, label propagation, preview
isolation, and artifact structure; they do not establish visual quality by
themselves. `QA.md` records the accepted final render and scientific checks.

The repository's full `./scripts/verify.sh` also reruns simulations and writes
`results/`. It was deliberately not run for this presentation-only task. The
separate governance hook and read-only focused tests are not a claim of full
product acceptance. No model semantics, parameters, random streams, experiment
outputs, or scientific estimators are changed by this edition.
