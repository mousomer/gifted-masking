# Results and discussion deck — production record

Eight 16:9 slides: five results slides and three discussion slides. The section
contains 1,096 spoken words and 660 seconds of planned narration. It follows
the author-approved results/discussion plan and contains no introduction or
standalone model setup. Earlier decks and lecture text are preserved.

The final PPTX uses Helvetica Neue, warm cream, teal, rust and blue to match
the earlier deck. Five native charts, four native tables (including the
357-cell M2 map), text and diagram connectors are editable. The PDF is a
raster viewing copy of the final PowerPoint renders.

## Verification

Package, font, layout, native-chart and first-party import checks passed with
zero layout findings and zero warnings. Exact exported estimates, confidence
interval endpoints, E04 series, E05 series/crossings and all 357 map cell colors
match DATA.json. Source hashes and resolved notes references pass. E01
intervention contrasts explicitly reverse the archive's baseline-minus-
intervention sign, with interval endpoints reversed accordingly.

All eight final slides were visually reviewed. Labels on the confidence-
interval plots, map axes and feedback connector were repaired before delivery.
All eight PDF pages render at 1920×1080, and each embedded image is pixel-equal
to the final PowerPoint render. PDF pages 1, 3 and 6 were additionally inspected.
RENDERED_CONTENT.json contains exported text, notes, chart series and file hashes.

The read-only integrated-article verifier passed, preserving 33 experiment
outputs, 18 evidence references and 19 prior revision files. Governance and
whitespace checks passed. The full ./scripts/verify.sh was omitted because it
executes experiments and writes scientific evidence outside RDS 0.18's scope.
No simulation, model, parameter, estimator or prior figure was changed.

## Use and application limits

Append these slides after the author's existing introduction/model slides.
Speaker notes include timings and full source paths. M4 is an implemented
extension with formal E06 results deferred, and no confirmed hysteresis claim.

Native PowerPoint desktop execution was not tested. The package and first-party
import/render checks passed. Charts use exact literal native PowerPoint data
without embedded Excel workbooks. This preserves source precision; external
spreadsheet editing and cross-application rendering are not verified. Category
and window captions on the effect plots are editable slide annotations, while
estimate labels and confidence-interval segments belong to native charts.
The shaded E05 interval between boundaries is an editable slide shape.

Final artifacts: output/pptx/masking_results_discussion.pptx and
output/pdf/masking_results_discussion.pdf. SPEAKER_NOTES.md is the separate
spoken manuscript. DATA.json and build_deck.mjs retain authoring sources.
