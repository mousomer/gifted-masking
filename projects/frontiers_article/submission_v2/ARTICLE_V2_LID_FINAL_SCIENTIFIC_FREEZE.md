# Article V2 L&ID Final Scientific Freeze

**Prepared:** 21 August 2026

**Freeze activation:** `NOT_ACTIVATED_BLOCKED`

**Readiness verdict:** `BLOCKED_BY_JOURNAL_WORD_LIMIT`

This record binds the scientifically frozen Stage 11.5 candidate to the Stage
12 production previews. It is present to make the conversion trace auditable,
but it is not an activated submitted-version authority. Activation requires a
journal-compliant authorized Abstract, a real persistent evidence identifier,
completed author metadata/declarations, rebuilt final-format files, revalidation,
and a final selective checkpoint.

## 1. Predecessor authority

| Authority | SHA-256 | Validation |
| --- | --- | --- |
| `projects/frontiers_article/ARTICLE_V2_LID_STAGE11_5_REPAIRED_CANDIDATE_PACKAGE.md` | `1ef1a5252891d7f69c8e4f112765256d4a41dd51381ef4672d15b06801168124` | 67/67 valid |
| Sol audit | `1d5f3986a0389d6013dca6323ffeca97b18c7fce2bbc8adb622b83c16b96cfa4` | exact |
| Fable audit | `c413cabccff320395f953e868f9a9bbed1104b876d4b1b9c6205c7b6efc595eb` | exact |
| Stage 11.5 reconciliation | `59d9fbaec87a6660986fb3cc99c666c8cb2f99d4c3b970b51fa86cd777743f30` | exact |
| Article V1 manuscript | `cd27687bdb5f3144172822ba2ff996f59efcdbf5398a905564a8177a345cdae9` | preserved |

## 2. Scientific source hashes

| Scientific source | SHA-256 | Status |
| --- | --- | --- |
| `projects/frontiers_article/ARTICLE_V2_LID_MANUSCRIPT_DRAFT.md` | `217d259929f5d0c585bf9da1de3c33befb8403b57a79a0c4f5257627ab0f5199` | Frozen Stage 11.5 source; unchanged |
| `projects/frontiers_article/ARTICLE_V2_LID_SUPPLEMENTARY_METHODS.md` | `a413ee282e108dc225d8e2f29b74263dbdb514eb5cc6af89eeec64267dc929ce` | Frozen Stage 11.5 source; unchanged |
| `projects/frontiers_article/v2_figures/FIGURE_CAPTIONS.md` | `82155c9fe3c0855a7ad54eaf13893f4b76173f0674177d8a0b59804db9dcc912` | Frozen captions |
| `projects/frontiers_article/v2_figures/FIGURE_PROVENANCE.md` | `70133a0f4311caf445c062ecda8348bfc6fa3e0a3ca4d272ab4cbc29f13ab720` | Frozen provenance |
| `projects/frontiers_article/v2_figures/FIGURE_TEXT_CONSISTENCY_MATRIX.md` | `06515fad93e5811fc625e396a7037b9b182f85dc005bf371c500555b1142f39c` | Frozen consistency record |

## 3. Figure identities

| Figure | PDF SHA-256 | Scientific status |
| --- | --- | --- |
| Figure 1 | `02ab24130d8554eb95725bdb64fcb8b6f091ed94e3e5d4af6834b6c2c7cdd54f` | Repaired Stage 11.5 figure; source PNG `68b4794f12ee09f4bd9a43a6660e6a13c2aa8c5b199d5142408688cdee9ae391` |
| Figure 2 | `f7dc27b4c2054409c8db96358e0b805c0c1c8db4c7d3edd5eda3454590027cd0` | Unchanged |
| Figure 3 | `432d554138a43614b94101381fdca6c73e4b2ced165859feb3a4d42d6b74dc99` | Unchanged; production review `NO_CHANGE` |
| Figure 4 | `a8a39d4a58faeac95b0dfad2d4ec34a58fde1455d3ee63112c3e13cdfbb31dbf` | Unchanged |

The separate upload PDFs are byte-identical to these frozen scientific PDFs.

## 4. Frozen evidence and archive

| Item | Identity/status |
| --- | --- |
| Included evidence | E01-E05 only |
| Protected outputs | 33/33 `ARTIFACT_VERIFIED` |
| Evidence-matrix references | 18/18 valid |
| E01-E03 historical generator states | `HISTORICAL_SOURCE_STATE_UNRECOVERED` |
| E04-E05 historical source | Fingerprint-exact bundles retained |
| Local deposit payload | `submission_v2/archive/ability_concealment_e01_e05_evidence.zip` |
| Local payload SHA-256 | `71e3d3879c3878cc7fd692df3cc1c129b6b0b6dd5169d386c837db7074474adb` |
| Payload validation | 101/101 manifest entries valid; ZIP structure valid |
| Provider | Not selected/confirmed |
| Persistent identifier/DOI | None; `BLOCKED_BY_ARCHIVAL_IDENTIFIER` |

E06/M4, unrelated exploration, superseded drafts, non-authoritative figure
experiments, and the former cross-estimand Figure 6 are not Article V2 evidence.

## 5. Public Data/Code statement

The final public statement is not frozen because no persistent identifier
exists. The controlled pending statement is
`submission_v2/declarations/ARTICLE_V2_LID_DATA_CODE_STATEMENT_PENDING_ARCHIVE.md`,
SHA-256
`e753afa13c86761729085fc12819f133729ff78c4e8499f9f7cbcdfe2cfc3a73`.
It correctly names the public repository, reserves a real persistent identifier,
retains E01-E05 artifact verification, and discloses the E01-E03 historical
source-state limit. It must not be submitted with its placeholder.

## 6. Reference identities

- Main reference list: 13 entries; 13/13 citation-reference bijection passed.
- Supplement-only list: one Best and Chakravarti (1990) PAVA reference; 1/1
  citation-reference bijection passed.
- Cross author/year ambiguity is production-normalized using `T. L.` for 1993
  and `J. R.` for 2019 without changing the reference records.

## 7. Production-format identities

Production hashes identify conversion containers, not new scientific
authorities. The controlled upload/preview inventory is
`submission_v2/ARTICLE_V2_LID_FINAL_SUBMISSION_MANIFEST.md`, SHA-256
`3c6a25d544e987dcfcd3aa2be22096834714832da47902cd3eb5724cf17f2f15`.
The final production QA is
`submission_v2/qa/ARTICLE_V2_LID_STAGE12_FINAL_QA.md`, SHA-256
`39cd5076f95d2b6d302cfa476c57a6c10edfd261ab42cda79674fa0b478b46f1`.

The conversion trace is:

`Stage 11.5 repaired candidate -> frozen scientific Markdown -> declared blinded-production transformations -> DOCX -> PDF preview`.

Declared transformations are removal/movement of author metadata for double
anonymization, reduction to five keywords, initials for the two Cross citations,
embedding unchanged figures, movement of declarations to the title page, and
a bounded anonymized availability statement. No result, equation, estimator,
interval, numerical interpretation, main scientific section, or caption
meaning changed.

## 8. Non-activation conditions

This freeze is not activated because:

1. the frozen Abstract contains 221 words and the journal hard maximum is 150;
2. the evidence archive has no persistent identifier;
3. mandatory author metadata and declarations are unconfirmed; and
4. the final public Data/Code statement cannot yet name the archive.

No checkpoint commit, push, PR, archive publication, or journal submission was
performed. After the blockers are resolved, all affected scientific and
production hashes must be regenerated and this record replaced by an activated
final freeze.
