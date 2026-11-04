# Article V2 L&ID — Persistent Evidence Archive Metadata Dossier

**Opened:** 21 August 2026

**Stage:** `ARTICLE_V2_LID_STAGE12R_SUBMISSION_UNBLOCKING_AND_FINAL_ACTIVATION`

**Status:** `AUTHOR_INPUT_REQUIRED_FOR_ARCHIVE_PROVIDER` /
`AUTHOR_INPUT_REQUIRED_FOR_ARCHIVE_LICENSE`

This supersedes `DEPOSIT_METADATA_PENDING_CONFIRMATION.md` as the working
deposit record. That file is retained unchanged as the Stage 12 historical
state.

---

## 1. Object to be deposited

The deposit is the **E01–E05 publication evidence archive only**. It is not the
research workspace, and E06/M4 is outside the deposit boundary.

| Field | Value | Status |
| --- | --- | --- |
| Local path | `projects/frontiers_article/submission_v2/archive/ability_concealment_e01_e05_evidence.zip` | `CONFIRMED` |
| Upload filename | `ability_concealment_e01_e05_evidence.zip` | `CONFIRMED` |
| SHA-256 | `44304ca7f3350dd13183d9163753ac76827cd7cff3cf9ddaa7b0dc1ceefa8dbb` | `CONFIRMED` — rebuilt and re-verified 21 August 2026; see §1.2 |
| Payload files | 101 manifest-bound files plus `MANIFEST.sha256` | `CONFIRMED` — 101/101 re-validated this stage |
| ZIP structural validity | valid | `CONFIRMED` |

### 1.2 Authorized pre-deposit rebuild, 21 August 2026

The archive was rebuilt **once**, on author instruction, before any deposit and
while no persistent identifier existed. The trigger was the E05 axis-semantics
repair to the Supplement: the staging directory is assembled with hardlinks, so
the repaired Supplement had to be carried into the deposited object, or the
deposit would have shipped a Supplement differing from the submitted one.

| | |
| --- | --- |
| Superseded SHA-256 | `71e3d3879c3878cc7fd692df3cc1c129b6b0b6dd5169d386c837db7074474adb` |
| Current SHA-256 | `44304ca7f3350dd13183d9163753ac76827cd7cff3cf9ddaa7b0dc1ceefa8dbb` |
| File list | **identical** — 101 payload files plus `MANIFEST.sha256`, verified by extraction diff |
| Content delta | exactly two files: `ARTICLE_V2_LID_SUPPLEMENTARY_METHODS.md` (the intended repair) and `MANIFEST.sha256` (which records that file's new hash) |
| Manifest validation | 101/101 VALID |
| ZIP structural validity | valid |

**Do not rebuild this ZIP again.** The object that receives the persistent
identifier must be exactly this validated artifact. A further rebuild is
authorized only if a genuine defect is demonstrated, and once a DOI exists it
would require a new archive version.

### 1.1 Deposit boundary

Included: five frozen configurations; five experiment manifests; all 33
protected E01–E05 outputs including raw unit tables; the evidence matrix;
analytic and inferential authorities; interpretation and provenance records;
publication-source figure tables; figure captions, provenance, and generator;
recovered E04/E05 generator-source bundles; the Supplementary Methods; and
public reproducibility documentation.

Excluded: E06/M4; unrelated exploratory work and large sweeps; superseded
manuscript and figure drafts; the former cross-estimand Figure 6; and
current-code artifacts outside the publication evidence boundary.

## 2. Deposit metadata

| Field | Proposed value | Status |
| --- | --- | --- |
| Archive title | Ability Concealment Does Not Uniquely Reveal the Environment: E01–E05 Publication Evidence | `AUTHOR_INPUT_REQUIRED` |
| Creators | Guy Sion; Omer Moussaffi | `AUTHOR_INPUT_REQUIRED` |
| Creator ORCIDs | none established | `AUTHOR_INPUT_REQUIRED` |
| Creator affiliations | as on the title page | `AUTHOR_INPUT_REQUIRED` |
| Resource type | Dataset / research compendium — exact provider category depends on provider | `AUTHOR_INPUT_REQUIRED` |
| Description | Frozen, content-addressed evidence boundary supporting experiments E01–E05, including protected result artifacts, configurations, manifests, figure-source tables, provenance records, validation records, and checksums. E06/M4 is excluded. All protected E01–E05 outputs are artifact-verified. The exact historical generator states for E01–E03 were not recovered; those results are supported by verified archived artifacts, configurations, manifests, and validation records rather than by a claim of bit-identical regeneration from the current code. | `AUTHOR_INPUT_REQUIRED` |
| Version | 1.0 | `AUTHOR_INPUT_REQUIRED` |
| Keywords | ability concealment; masking; reinforcement learning; gifted learners; reproducibility; simulation | `AUTHOR_INPUT_REQUIRED` |
| Related article title | Ability Concealment Does Not Uniquely Reveal the Environment: Learning and Social Opportunity in Gifted Learners | `CONFIRMED` |
| Publication relation | "is supplement to" the related article (article DOI not yet assigned; add on acceptance) | `AUTHOR_INPUT_REQUIRED` |
| Related Git repository | `https://github.com/mousomer/gifted-masking` | `CONFIRMED` — public, verified this stage |
| Publication date | deposit date; not yet available | `AUTHOR_INPUT_REQUIRED` |
| DOI / persistent URL | **not available — must not be fabricated** | `BLOCKED_BY_ARCHIVAL_IDENTIFIER` |

## 3. License — requires explicit confirmation

Status: `AUTHOR_INPUT_REQUIRED_FOR_ARCHIVE_LICENSE`

**Established governance.** The public repository
`https://github.com/mousomer/gifted-masking` carries a `LICENSE` file on its
default branch and is registered as **GPL-3.0**. This is verified fact and
establishes the license of the *code*.

**Why that does not settle the deposit license.** The deposit is a mixed
compendium — predominantly result artifacts, tables, configurations, manifests,
and documentation, plus two recovered generator-source bundles. GPL-3.0 is a
software license and is a poor instrument for the data majority of the payload.
The common alternative for a research-data deposit is CC-BY-4.0, but §15 of the
governing instruction forbids selecting a license merely because it is common.

**Therefore no license is selected here.** The authors must choose. The three
coherent options:

| Option | Effect |
| --- | --- |
| GPL-3.0 for the whole deposit | consistent with the repository, awkward for the data majority |
| CC-BY-4.0 for the whole deposit | conventional for research data, weaker fit for the embedded source bundles |
| CC-BY-4.0 for data/documentation, GPL-3.0 retained for the embedded source bundles | most accurate, requires the provider to accept a split statement or a README note |

Do not publish under an unapproved license.

## 4. Provider — requires explicit confirmation

Status: `AUTHOR_INPUT_REQUIRED_FOR_ARCHIVE_PROVIDER`

No repository authority has selected a persistent archive provider. Zenodo was
*inspected* at Stage 12 as an appropriate DOI-granting research archive, but
inspection is not selection: a deposit must not be created merely because a
provider was previously looked at.

Additionally, this session has no authenticated archive credentials, and
depositing is an outward-facing publication action that transmits author names,
affiliations, and contact metadata to an external service. Both conditions
independently prevent deposition here.

Applicable blocking states: `AUTHOR_INPUT_REQUIRED_FOR_ARCHIVE_PROVIDER` and
`BLOCKED_BY_ARCHIVAL_AUTHENTICATION`.

## 5. Post-deposit record — to be completed by whoever performs the deposit

All fields empty. **No value below may be guessed or filled in advance.**

| Field | Value |
| --- | --- |
| Provider | _(pending)_ |
| Record ID | _(pending)_ |
| DOI / persistent identifier | _(pending)_ |
| Public persistent URL | _(pending)_ |
| Version | _(pending)_ |
| Deposition date | _(pending)_ |
| Uploaded filename | _(pending)_ |
| Uploaded checksum as reported by provider | _(pending)_ |
| Byte-identity verdict | _(pending)_ — see §6 |
| Deposit metadata as actually published | _(pending)_ |

## 6. Byte-identity verification rule

After deposit, compare the provider-reported checksum against
`44304ca7f3350dd13183d9163753ac76827cd7cff3cf9ddaa7b0dc1ceefa8dbb`.

- If the provider reports a matching SHA-256 for the stored object, record
  **`BYTE_IDENTICAL_UPLOAD_VERIFIED`**.
- If the provider reports only a different digest algorithm, re-verify by
  downloading the published object and hashing it locally, then record the
  same verdict on that basis.
- If the provider transforms the archive (re-packing, adding metadata files),
  record **`CONTENT_EQUIVALENT_TRANSFORMED_ARCHIVE`** and state exactly what
  changed.

Do not claim byte identity unless it was actually checked.

## 7. Credentials

No archive credentials, tokens, or API keys are recorded in this dossier, and
none may ever be committed to this repository.

## 8. Verdict

`BLOCKED_BY_ARCHIVAL_IDENTIFIER`

The archive object is built, validated, and ready. Provider selection, license
selection, metadata approval, authentication, and the publication action all
require the authors.
