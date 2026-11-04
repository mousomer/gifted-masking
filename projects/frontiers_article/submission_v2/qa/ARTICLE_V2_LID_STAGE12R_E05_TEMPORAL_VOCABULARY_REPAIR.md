# Article V2 L&ID — Stage 12R E05 Temporal-Vocabulary Repair

**Performed:** 21 August 2026

**Stage:** `ARTICLE_V2_LID_STAGE12R_SUBMISSION_UNBLOCKING_AND_FINAL_ACTIVATION`

**Authority:** explicit author instruction, 21 August 2026 — the E05 result
"should not suggest erroneously that there is a temporal finding".

**Supersedes:** the Stage 11.5 adjudication of the E05 temporal-vocabulary P3
concern as `REJECT_AFTER_AUTHORITY_CHECK`. That decision is not deleted; it is
overridden by the author on the record. Sections 10.1 and 10.2 of
`ARTICLE_V2_LID_AUTHOR_CONFIRMATION_DOSSIER.md` are closed by this repair.

## 1. Defect

E05 measures position along the comparison-cost parameter $b_f$. The learned
crossing (0.312852) lies **below** the exact environmental crossover
($8/17=0.470588\ldots$) on that axis. Nothing in E05 measures elapsed time,
number of attempts, or a chronological point of withdrawal.

The frozen text nevertheless used temporal vocabulary at the point of use
("preceded", "arise before") and then disclaimed it in a following sentence.
This disclaim-after-use pattern has two failure modes:

1. **Detached surfaces carry the word without the disclaimer.** A section
   heading appears in the table of contents and is quoted standalone; a
   Highlight is published as a standalone bullet with no surrounding text at
   all. Both asserted a temporal ordering with no correction attached.
2. **The disclaimers had drifted off their referents.** The §3.5 disclaimer
   quoted "preceded", which occurred only in the heading; the following
   disclaimer quoted "earlier", which did not occur anywhere in §3.5. A
   disclaimer that negates a word the reader never encounters is evidence the
   vocabulary, not the reader, was the problem.

## 2. Repair principle

Remove the temporal vocabulary **at the point of use** rather than disclaim it
afterwards, and retain one accurate disclaimer. This is strictly stronger than
the previous pattern: the misleading reading is never offered.

No numerical value, estimator, interval, architecture, or claim was changed.

## 3. Exact changes

| # | File | Before | After |
| ---: | --- | --- | --- |
| 1 | manuscript §3.5 heading | The learned masking boundary **preceded** the objective boundary | The learned masking boundary **lay below** the objective boundary |
| 2 | manuscript §3.5 disclaimer | Here, "**preceded**" and "below" refer only to position on the comparison-cost axis, … | Here, "below" and "**lower**" refer only to position on the comparison-cost axis, … |
| 3 | manuscript §3.5 disclaimer | Nor is the result temporal: "**earlier**" refers to position along the comparison-cost parameter, not to elapsed time or number of attempts. | Nor is the result temporal: **the displacement is a difference in position** along the comparison-cost parameter, not **in** elapsed time or number of attempts. |
| 4 | manuscript §4.6 | the learned transition occurred **while** good-context authenticity still retained an objective advantage | the learned transition occurred **where** good-context authenticity still retained an objective advantage |
| 5 | manuscript §4.6 | behavioural withdrawal can **arise before the environment reaches its own** indifference point | behavioural withdrawal can **occur at comparison costs below the environmental** indifference point |
| 6 | Highlights, item 4 | Learned masking shifted **before** the environmental cost crossover. | Learned masking shifted **at costs below** the environmental crossover. |

Each replacement was applied under an exact-match assertion requiring precisely
one occurrence, so no unintended site was touched.

## 4. Post-repair verification

| Check | Result |
| --- | --- |
| Residual temporal vocabulary on any E05 surface | **NONE** |
| Manuscript E05 numbers unchanged | PASS — 0.312852, $8/17$=0.470588, 0.157736, 0.134076, CI [0.307836, 0.316918], Abstract 0.313 / 0.471 all present and unchanged |
| Comparison-cost framing retained | PASS |
| Left-censoring statement retained | PASS |
| No G2 / binary-softmax inference introduced | PASS |
| Abstract unchanged by this repair | PASS — block SHA-256 `b9fc239c6a871d39f67aa3d53eb2f6610ec70558d45e3c589099cdc587321123` |
| Supplement unchanged | PASS — no E05 temporal hit existed; file untouched |
| Highlights count and length | PASS — 4 highlights, 67/65/67/67 characters, all ≤ 85 |

### 4.1 Residual hits inspected and cleared

Four lines still contain a temporal token near boundary/crossover language.
All four were inspected and are correct as written:

| Line | Token | Verdict |
| ---: | --- | --- |
| §3.6, L175 | "while" | contrastive ("whereas"), not temporal. The E05 clause already reads "at comparison-cost values **below** those required". CLEAR |
| §3.6, L267 | "early" | belongs to **E01**, where early feedback is a genuine and correct temporal finding. The E05 clause reads "at a **lower comparison-cost value** than the objective environmental crossover". CLEAR |
| Figure 1 caption, L499 | "after early feedback (E01)" | **E01**, correct. Two further "while" tokens are contrastive. CLEAR |
| Data/Code statement, L533 | "deposited before submission" | production language about the deposit workflow, not a scientific claim; replaced when the persistent identifier is inserted. CLEAR |

## 5. Hashes after repair

| Artifact | SHA-256 |
| --- | --- |
| Manuscript source | `5813ea98567d39cc844d6973ee563a18f30e3a635d4f9ecaa0eb806f74a6f431` |
| Highlights source | `3437c76d7ae8351621995633b0aa3cf22cc06b5e2fc56b52ea742b1c7f1290d7` |
| Abstract block (unchanged by this repair) | `b9fc239c6a871d39f67aa3d53eb2f6610ec70558d45e3c589099cdc587321123` |

Predecessor states are recorded in
`ARTICLE_V2_LID_STAGE12R_ABSTRACT_COMPRESSION_AUDIT.md`.

## 6. Propagation

`submission_v2/manuscript/ARTICLE_V2_LID_Anonymized_Manuscript_SOURCE.md` is a
generated production artifact derived from the manuscript source. It still
holds the pre-repair text and will pick up both the compressed Abstract and
this repair at the next production rebuild. It was **not** hand-edited.

## 7. Verdict

`E05_TEMPORAL_VOCABULARY_RESOLVED`

E05 is stated purely as position on the comparison-cost axis on every
submission-facing surface, including detached surfaces.

---

# Pass 2 — Full axis-semantics sweep and disclaimer removal

**Authority:** author instruction, 21 August 2026, reopening edit authority
narrowly for an E05 axis-semantics terminology repair across every E05-facing
public artifact, including removal of anti-temporal disclaimers rendered
redundant by the terminology correction.

## P2.1 Artifacts swept

Manuscript body and headings, Abstract, Highlights, Supplement, figure
captions, title page, cover letter, submission metadata, Data/Code statement,
archive README, and archive REPRODUCIBILITY. Search terms: *before, precede\**,
*earlier, later, too soon, soon\**, *delay\**, *prior, premature\**, *onset,
chronolog\**, *elapsed, temporal\**, *withdraw\**, *stopping, give(s) up, time*,
restricted to lines also matching E05/crossover/crossing/comparison-cost/
b_f/displacement/boundary/isotonic/PAVA/censoring.

## P2.2 Disclaimer inventory found

The frozen text carried **seven** separate anti-temporal disclaimers. That
volume was itself diagnostic: the vocabulary, not the reader, was the problem.

| # | Location | Disposition |
| ---: | --- | --- |
| 1 | §1.5, concept introduction | **retained**, rewritten positively as axis language; the "give up" clause removed |
| 2 | §3.5, after the displacement statement | **removed** — redundant once "preceded" was gone |
| 3 | §3.5, after the cause statement | **removed** — it disclaimed "earlier", a word that occurred nowhere in §3.5 |
| 4 | §4.6, opening of the final paragraph | **removed** — redundant with the corrected §4.6 body |
| 5 | Limitations | **trimmed** — the general "no direct calendar interpretation" caveat kept; the E05-specific negation removed |
| 6 | Figure 4 caption | **replaced** with a positive statement: "The horizontal axis is comparison cost $b_f$." |
| 7 | Supplement S6 | **trimmed** to the positive definitional sentence; the negation, including "gives up", removed |

Net: seven defensive negations reduced to one positive axis definition at the
point of introduction, plus positive axis statements in the Figure 4 caption
and Supplement.

## P2.3 Additional terminology corrections in this pass

| Location | Before | After |
| --- | --- | --- |
| §4.6 | behavioural **withdrawal** can occur at comparison costs below … | **the shift toward masking** can occur at comparison costs below … |
| §1.5 | ordering is along a comparison-cost axis, not elapsed time, number of attempts, or a moment at which learners "give up." | ordering is along a comparison-cost axis: **both boundaries are values of the payoff parameter $b_f$**, not points in time or numbers of attempts. |

## P2.4 Post-sweep residual hits — all cleared

Three lines remain across all artifacts. Each was inspected and is correct.

| Location | Token | Verdict |
| --- | --- | --- |
| §1.5 | "time" | the single retained axis definition. INTENTIONAL |
| §4.2 | "later" | **E01**, where reduced later sampling is a genuine and correct temporal finding. CLEAR |
| Data/Code statement | "before" | production workflow language ("deposited before submission"); replaced when the persistent identifier is inserted. CLEAR |

Supplement, Highlights, title page, cover letter, submission metadata, archive
README and REPRODUCIBILITY: **zero hits**.

## P2.5 Invariants revalidated after pass 2

| Check | Result |
| --- | --- |
| Abstract | UNCHANGED by this pass — block SHA-256 `b9fc239c6a871d39f67aa3d53eb2f6610ec70558d45e3c589099cdc587321123`, 144 words |
| E05 values | PASS — 0.312852, $8/17$=0.470588, 0.157736, 0.134076, CI [0.307836, 0.316918], Abstract 0.313 / 0.471 all present, unchanged |
| Estimator and procedure | PASS — non-increasing PAVA fit, 10,000 bootstrap resamples, complete-master-curve bootstrap unit all unchanged |
| Left-censoring result | PASS — hierarchical left-censoring retained in §3.5, Figure 4 caption, and Supplement |
| Scientific interpretation | PASS — displacement, non-identification of a unique cause, and the availability/discoverability distinction unchanged |
| Highlights | PASS — 4 items, 71/65/67/67 characters, all ≤ 85 |
| §30 prohibited-regression scan | PASS — "gives up" hit eliminated by the Supplement trim; remaining hits are archive scope-exclusion statements only |
| Full diff containment | PASS — every change is inside the Abstract, §1.5, §3.5, §4.6, Limitations, the Figure 4 caption, Supplement S6, and Highlight 4 |

## P2.6 Hashes after pass 2

| Artifact | SHA-256 |
| --- | --- |
| Manuscript source | `7742f7542541d61ee74fb22183b400e796f8a8d2c770dae1d9883a0d079df1f9` |
| Supplement source | `341a91b2ff5386c54a86d761de25e60e1f02da280802e8d8865f8f12daea6a26` |
| Highlights source | `3437c76d7ae8351621995633b0aa3cf22cc06b5e2fc56b52ea742b1c7f1290d7` |
| Abstract block | `b9fc239c6a871d39f67aa3d53eb2f6610ec70558d45e3c589099cdc587321123` |

## P2.7 Evidence-archive consequence — DECISION REQUIRED

`submission_v2/archive/build_evidence_archive.sh` stages the package with
**hardlinks** (`ln`), not copies. The staged Supplement therefore shares an
inode with the live Supplement, and the pass-2 edit propagated into
`evidence_package/` automatically.

Current state, established by direct inspection:

| Object | State |
| --- | --- |
| `ability_concealment_e01_e05_evidence.zip` | **unchanged**, SHA-256 `71e3d3879c3878cc7fd692df3cc1c129b6b0b6dd5169d386c837db7074474adb`; internally self-consistent; contains the **pre-repair** Supplement `a413ee28…` |
| `evidence_package/` staging directory | **100/101** against its own `MANIFEST.sha256`; the single failure is the Supplement, now carrying the repaired text |

Nothing was lost: the ZIP is the authoritative frozen object and was not
touched. But the archive has not yet been deposited and **no DOI exists**, so
§16's prohibition on rebuilding does not yet bind.

Two coherent options:

1. **Rebuild the ZIP before deposit** (recommended). The deposited evidence
   Supplement then matches the submitted Supplement. Requires
   `rm -rf evidence_package ability_concealment_e01_e05_evidence.zip` followed
   by `sh build_evidence_archive.sh`, which regenerates `MANIFEST.sha256`
   deterministically. Cost: a new ZIP SHA-256, which must be propagated to the
   submission manifest, Stage 12 QA, current state, and both dossiers.
2. **Keep the ZIP frozen.** The deposit would ship a Supplement differing from
   the submitted one by exactly one removed sentence — a discoverable
   inconsistency.

Not actioned in this pass. It belongs to the single final rebuild.

## P2.8 Pass 2 verdict

`E05_AXIS_SEMANTICS_RESOLVED`

E05 is expressed purely as position on the comparison-cost axis on every
submission-facing surface. The disclaimers that existed to compensate for the
old vocabulary have been removed rather than accumulated.
