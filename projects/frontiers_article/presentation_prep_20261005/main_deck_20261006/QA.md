# First-set presentation production — 6 October 2026

Delivered eleven main slides as `output/pptx/masking_mechanisms_first_set.pptx`
and `output/pdf/masking_mechanisms_first_set.pdf`. The PDF is a raster viewing
copy; the PowerPoint contains editable text, shapes, connectors, native tables,
and native charts. Eight backup slides remain planned, outside this delivery.

## Scope and scientific acceptance

- The opening introduces possible mechanisms, using source-qualified age wording.
  A generated child-apart-from-peers illustration is conceptual, not empirical.
- The actual Dash race still illustrates explicit social instruction. The short
  quotation, image source, official film context, and exact generated-image
  prompt are recorded in `../assets/ASSET_SOURCES.json` and speaker notes.
- M0 distinguishes the two-action setup, analytic expected-payoff threshold,
  and archived simulation effects. M1 retains distinct outcomes and windows.
- M2 separates three social states from two actions and the six Q-values.
  M3 explains joint context–behaviour actions with fixed receptivities. M4
  distinguishes continuous environmental receptivity from two learned values.
- E01–E05 are the numerical evidence boundary. M4/E06 is explicitly an
  implemented extension with formal results deferred; no confirmed hysteresis
  or human causal identification is claimed.
- All eleven slides have speaking notes and source references. The spoken
  paragraphs total 1,070 words. Allocated durations sum to 660 seconds, leaving
  60 seconds within the user's 12-minute slot. Actual pacing needs rehearsal.
- No model, random-number behavior, parameter default, archived experiment,
  article figure, or earlier one-slide draft was changed by this production.

## Artifact checks

`validation.json` records the final PPTX package, layout, font, import, native
table, and native chart checks. Eleven 16:9 slides passed with zero layout
findings and zero warnings. Helvetica Neue is encoded in 203 checked text
scripts. There are three native charts (slides 5, 7, 8), four native tables
(6, 7, 9, 10), and two raster pictures (1, 2).

All slides were rendered from the reimported final PPTX and visually inspected.
The final slide PNGs were byte-identical to the inspected versions for slides
1–4 and 6–11; slide 5's final render was inspected directly after its labels
were repaired. Connector arrowheads and M1 outcome/window labels were checked.
No clipping, overlapping labels, reversed arrows, or unreadable chart labels
remained in the delivered renders.

`RENDERED_CONTENT.json` records exact exported slide text, table text, notes,
native chart series, preview paths, and final file hashes. Exported M1 values
match the archived effect estimates exactly. M3 search curves match all three
five-master series in `../MAIN_DECK_DATA.json`; the comparison-cost plot
matches its archived x/y series exactly. Source-table hashes are recorded.
Displayed rounded estimates and uncertainty retain their source definitions.

The PDF contains eleven 16:9 pages. Poppler rendered all eleven at 1920×1080.
`PDF_RENDER_CHECK.json` records page dimensions and mean absolute pixel
differences against the source renders (maximum channel mean 1.25–3.81 on a
0–255 scale, from PDF rasterization). Pages 1, 5, and 9 were additionally
visually inspected after PDF rendering. This is not a text-selectable PDF;
the editable source is the PPTX.

## Known application limits

Native PowerPoint desktop execution has not been tested. The first-party
renderer/importer and structural PowerPoint checks passed. Charts retain
native PowerPoint literal values without embedded Excel workbooks. A portable
workbook conversion was rejected because Excel could not preserve exact
literal precision; source numbers were not rounded to bypass that check.
Cross-application chart data editing is therefore not claimed. The source
data and JavaScript builder are included for reproducible edits. The M1 bars
are native chart objects; their two outcome/window captions are separate
editable text boxes to avoid the renderer flattening multiline chart labels.

## Build and verification record

`build_deck.mjs` is the final Artifact Tool authoring source. It uses the
bundled Node runtime and `@oai/artifact-tool`, plus the installed Presentations
skill helpers; no project runtime dependency was added. `DECK_VERSION=v4`
identifies the final private build. The source embeds local assets and reads
the slide specification, source index, and chart data in the preparation pack.

The read-only integrated article verifier passed during production, preserving
all 33 protected experiment outputs, 18 evidence references, and 19 earlier
revision files. `./gov check` and the final whitespace/source checks are
recorded in `FINAL_CHECKS.json`.

The declared full verifier remains `./scripts/verify.sh`. It was not run for
this presentation-only change because its experiment execution and evidence
writes exceed RDS 0.16's preserved-evidence boundary. Existing model test
results remain historical, not newly claimed. Product acceptance here covers
the authored presentation and preservation checks, not new scientific
robustness or the deferred E06 experiment.

## Outstanding work

Rehearse with the actual deck. Produce the eight backup slides only as a
subsequent presentation extension. No other work is required to deliver this
first set.
