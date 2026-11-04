# Article V1 E01–E05 Generator-Source Provenance Audit

**Audit date:** 15 August 2026

**Scope:** historical generator-source identity only; frozen scientific evidence unchanged

**Overall status:** `PROVENANCE_PARTIALLY_RECOVERED`

## A. Executive verdict

The bounded forensic search recovered fingerprint-exact historical source bundles for E04 and E05 from unreachable Git trees. It did not find a complete source state matching the recorded E01, E02, or E03 source fingerprints.

| Experiment | Historical generator-source status | Artifact identity | Maintained model semantics |
|---|---|---|---|
| E01 | `ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE` | 5/5 protected hashes pass | audited separately; unchanged |
| E02 | `ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE` | 6/6 protected hashes pass | audited separately; unchanged |
| E03 | `ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE` | 8/8 protected hashes pass | audited separately; unchanged |
| E04 | `HISTORICAL_SOURCE_RECOVERED` | 7/7 protected hashes pass | audited separately; unchanged |
| E05 | `HISTORICAL_SOURCE_RECOVERED` | 7/7 protected hashes pass | audited separately; unchanged |

These dimensions are deliberately separate:

- **Artifact identity** asks whether the frozen output bytes match the manifest SHA-256 values. All 33 do.
- **Model-semantics identity** asks whether maintained M0–M4 code matches the audited analytic specification. The prior consistency audit established that it does; current blob identities were also checked.
- **Generator-source identity** asks whether the complete dirty worktree bytes entering each historical source fingerprint are available. That identity is recovered only for E04 and E05.

Therefore `ARTIFACT_PROVENANCE_GAP_OPEN` remains for E01–E03. This is a historical reproducibility limitation, not evidence that the frozen artifacts are corrupted.

## B. Checkpoint commit

| Field | Value |
|---|---|
| Pre-checkpoint branch | `codex/frontiers-stage2-e06` |
| Pre-checkpoint HEAD | `441cfe44856d0cbc3da57089cbe91755b0cc4780` |
| Checkpoint commit | `907abfbfb8185d38f032312f52db9f1a4c3e8fe4` |
| Commit subject | `Checkpoint post-P0/P1 research workspace` |
| Hook bypass | None; no custom commit hook was present and the normal commit succeeded |
| Inclusion result | All legitimate tracked modifications and untracked files present before P2 were included |

The complete pre-checkpoint inventory is the 71-path name-status record of checkpoint commit `907abfbf`. It contained no deletions and comprised:

- root governance: `ARCHITECTURE.md`, `ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md`, `CURRENT_STATE.md`;
- 19 August-2026 research PDFs under `doc-reviews/docs_august2026/`;
- two August hand-off DOCX files and all 11 files under `doc-reviews/handoff_august2026/Gifted_Masking_Article_V1_Handoff_Pack_REVISED_2026-08-15/`;
- Article-V1 authorities and governance: `ARTICLE_V1_ANALYTIC_RESULTS.md`, `ARTICLE_V1_CLAIM_LEDGER.md`, `ARTICLE_V1_CURRENT_STATE.md`, `ARTICLE_V1_EVIDENCE_AUDIT.md`, `ARTICLE_V1_EVIDENCE_MATRIX.csv`, `ARTICLE_V1_EXECUTION_PLAN.md`, `ARTICLE_V1_INFERENTIAL_AUDIT.md`, `ARTICLE_V1_LITERATURE_AUDIT.md`, `ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md`, `ARTICLE_V1_NEXT_STAGE.md`, `ARTICLE_V1_P0_P1_HANDOFF_INTEGRATION_REPORT.md`, `ARTICLE_V1_SOURCE_LEDGER.csv`, `BACKLOG.md`, `CURRENT_STATE.md`, `HANDOFF.md`, `HANDOFF_CONSISTENCY_AUDIT.md`, `README.md`, `RESEARCH_PROGRAMME.md`, and `STAGE2_EXECUTION_LOG.md`;
- pre-existing E05/E06 work: `E05_SEED_EXTENSION_AUDIT.md`, the four E06 implementation/instruction documents, E06 approval/checkpoint/fixture files, the E06 runbook, E06 smoke manifest/report, `src/gifted_masking/experiments/e06.py`, and `tests/test_article_e06.py`.

The full exact path list remains recoverable with `git show --name-status --format= 907abfbf`. Before staging, the inventory was checked for credentials, private keys, `.env` files, virtual environments, and abnormal caches. No unsafe tracked/untracked material was found. A staged secret scan raised one generic-token heuristic at `e06.py:956`; inspection showed a negative floating-point sentinel named `token`, not a credential. A complete `gitleaks dir . --redact` scan passed. The checkpoint commit body explicitly states that preserving E06/M4 material does not make it confirmatory Article-V1 evidence. The worktree was clean immediately after this commit.

## C. Frozen provenance targets

### C1. Run and source target table

All manifest `config_sha256` values are hashes of the manifest's canonical normalized config string, not necessarily raw config-file hashes.

| ID | Run and manifest | Config and hash | Recorded Git state | Source fingerprint | Dirty evidence |
|---|---|---|---|---|---|
| E01 | `frontiers_hot_stove_v1`; `results/manifests/frontiers_hot_stove_v1.json` | `configs/frontiers_article/e01_hot_stove_standard.json`; `cc5d0b5931d5ff0d855e6746a21b5f4ca1e280297280fe9e32cb2232e9b6b8fa` | `e0e9a738986dd440180a228b024b0807336cd957`; dirty | `042a60b7bd196f2bd8dfcce6e248ea0c8c04448b1d3e61cebfffc12b52f0c480` | diff `93b6093b66252c3dc9664c323d469ae2ddf7b09719366ddb11ef43d12349db5c`; porcelain `7daa9b767346021b076301ca550619e803502e1349a418f0137d5a2bf07c1d1d` |
| E02 | `frontiers_m1_binary_graded_v1`; `results/manifests/frontiers_m1_binary_graded_v1.json` | `configs/frontiers_article/e02_binary_graded_standard.json`; `064cb856f0a9ed58452bc8a3014f2d913ed3034ffe1fddf6e0115b462ab797e6` | same commit; dirty | `891e5a4f22a0396b0a01bf02211dd4607e796c350b68666c48d99ad9165dcba6` | diff `41844d948d534dc415965698d14859e5adaa442730e37ed6ed3f58d8216e1ef5`; porcelain `9dd9a5dbf2b64a02ec43e5e936a726cb28ddfd14ffcfd89987dcccae827b9c0e` |
| E03 | `frontiers_m2_regime_replication_v1`; `results/manifests/frontiers_m2_regime_replication_v1.json` | `configs/frontiers_article/e03_m2_regime_standard.json`; `1d9e477274a1b6e83ef7fb7d08446c822113648d12a8744ca49464bd50104d1c` | same commit; dirty | `397fec836e415bf504810e0aa1da551773ddf7d989f4b20e93f6c6e330e43c6b` | diff `325bfd553c5edc38d1f87c938b183f3c77a5cefe2c7105eb2dd971ba285080d3`; porcelain `3fd1b600547ba8201f309eba837e795d8a1e06f88993cb0e28ecd28315972daf` |
| E04 | `frontiers_m3_search_architectures_v1`; `results/manifests/frontiers_m3_search_architectures_v1.json` | `configs/frontiers_article/e04_m3_search_architectures_standard.json`; `5c48d8d0358a54243e9ef1f2bad1ff106a293d5c6cab5771bd92a9e4cebc0981` | same commit; dirty | `8599406b776d23f9357d89664f456d84f45e3a3783df1c830c1772ceb86750ae` | diff `113b1214df47785977662a7a6e01b10c850c5d8ddab479036157be60c5feafa9`; porcelain `14e22d4bb9d53827af93dcf3a06a956529db0c64be0a805b9bfff7fc62c21d14` |
| E05 | `frontiers_m3_bflpe_crossover_v1`; `results/manifests/frontiers_m3_bflpe_crossover_v1.json` | `configs/frontiers_article/e05_m3_bflpe_crossover_standard.json`; `60210519019688bf4acc0c3b5fcc9c1f4181d7b87c8eda1e1fdaecd0296446ae` | same commit; dirty | `f229a17da2c710d3c76ea5ca571fbf170a21e7c4c6c9c15cadda0366cfa19c02` | diff `UNKNOWN / NOT_RECORDED`; porcelain `bbe01a2c1d49144aa6ab39d27b1f058eb3f7a4069b9e2cd73082e30258956a30` |

### C2. Generator and model/core inputs

| ID | Generator/infrastructure paths entering source fingerprint | Model/core paths entering source fingerprint |
|---|---|---|
| E01 | `experiments/article.py`, `cli.py`, recursively all then-present files under `configs/frontiers_article/`, `test_article_e01.py` | none included by this fingerprint algorithm |
| E02 | `experiments/e02.py`, `cli.py`, `repro.py`, smoke/standard E02 configs, `test_article_e02.py` | `core.py`, `models/m0.py`, `models/m1.py` |
| E03 | `experiments/e03.py`, `cli.py`, `analysis/m2_optimal.py`, `scripts/map_m2_lock_in_regions.py`, smoke/standard E03 configs, `E03_STANDARD_GO.md`, `test_article_e03.py` | `models/m2.py` |
| E04 | `experiments/e04.py`, `cli.py`, `repro.py`, smoke/standard E04 configs, `test_article_e04.py`, `pyproject.toml`, `scripts/verify.sh` | `core.py`, `models/m3.py` |
| E05 | `experiments/e05.py`, `cli.py`, `repro.py`, smoke/standard E05 configs, `test_article_e05.py`, `E05_SMOKE_APPROVAL.md`, `pyproject.toml`, `scripts/verify.sh` | `core.py`, `models/m3.py` |

The audited maintained model blob identities are: `core.py` `f25723fed941a4c6cd8338f076a1b2d97d67041f`; M0 `a142fc04aee3451bca50d110d3ea0fda1c0972e4`; M1 `e64546cad9db5d376326ea3dea461daf0b926c10`; M2 `91df8ae77a3555b060732ff059eb94f2bd525e33`; M3 `d4b38cb0620460d096d7fd6f1b005b00a7c1949a`; M4 `df61944a8b3f71a1a339399486ad23b3e022ee0d`.

### C3. Artifact identity

Paths are the manifest `outputs` paths; values below are the protected SHA-256 identities.

| ID | Protected artifact identities |
|---|---|
| E01 | raw `a4e78dcf4094e03ed36fbb0e3cfbebecdc427247810cc359d6a4b5bfa362dc01`; cells `9d619166b5cdbc0525ea087a762a27ed767a4d039ae3fc280a9c5524825bdfd4`; effects `4ce67da8b48e8d770388db9e2c6ebe240b868c0696ba90678cc9940de02684d8`; figure `85db4225be7162ad7771dc6bcc43544c75a319dbffb572834100b1b25461155b`; report `4fab6b0ce576d12464256a9024edc1fda65c319fb9e09c28731091551ce1b57f` |
| E02 | raw `3640b1a83605791916ec150be66ef578bc100cee08b6b61f909d2a7ff2220619`; arms `cc19fa67bd40f5c2d5ab59f1f2a7c909c524b80b082c3354c7ad4283694abaf4`; cells `741b5cca90b7412eba6d9e79c3ef71adf6810a50144ca9761c3e94a5df94f226`; effects `11d29c72508649a174b285957dfec3752edff76a099aa76de9f6fe3a4e515a8a`; figure `08062c09b307e2838285b08058447ed19eb9d8edf3a15b16b89009d61dcc5cca`; report `c311720f6dc8e6c0ee196db9aff6e8a5c2172806b9536d2556ecef3dead892dd` |
| E03 | raw `9561ff20d91cd07cc57f61db9bdb60072ea8b381bcb43968825932c30da6d150`; cells `198cb7be9b2a93aa89569d9dd656326f521b7a2ec99543733fd6e779e0508851`; effects `5a1ee392560e94695dfe0d04ff89caeafdb0b58fa2b70e6def365726d66ab3af`; stable `91814ab4430f63bc5e46596c61718e1fec6705d355b6cab3d8c18d29c1dfaea7`; thresholds `0987aea9f6085f81bad791454eaca03127c6144f172a7cc9f41cdad6c316f9bf`; legacy `bb220dddc16335e9fc901a2e8be53f6d7c1a90aed8198fae3b2fd56e46e3ef2b`; figure `4328d076730235580ca0bd387d303e9f0c43b217d6512126782f78ab8cd136fc`; report `7339dbe5d1140e58a7f1536fd14d42cba41bad7f6228ca8f83c87ef194ab1498` |
| E04 | raw `621227ffeac600ffbfc85852ef2784d4e409880e329ff4b6d947553e2b4e419e`; canonical cells `65cebddb4621be63e67f1dc525c64f6968b1f0a798bd2b52589889f7d89e5777`; curves `33f245b36ba6d78489cd9b88948d07d4d3aaf58ef7f8395b4394431df2dd39b4`; effects `dd426992f0a1a0ae05542756dc6dca918fbf56a589347676a93a309d08a41d44`; equivalences `9820053b3236a68817cb98c28eb3c7fc20dbaff78b646111a6d45bd5ad31aecb`; figure `0fe46d1165050817a4aa68398cea48bc6a3a420349e61120b14398ecfc9cec7b`; report `553c5822fb9840abfbfb74f940785f89e76c7dda07b42d4913290cd958bb7503` |
| E05 | raw `9de41835a72986fc5ca7cbd591a16ed3781a3cfdd24f194d126b27012bafb947`; analytic `e1045d0593709561761ec8c9ba0684ef1a80e26d6b0b15f12f57434b74f22a42`; cells `59d780f3feb3ed03e665de0a75eabd8975fb394d58cbd9c2193a03bb68d73ab7`; effects `33eb752c89d87ce79ef13bfe196623fb4d4f53c4fff63e03b84af413a68200d5`; transitions `96b8d8dc1cf27e3a226282e4d8755effde74e855d81b8f8bbc6db6515c607097`; figure `0001f0ba2ef2c0fbf7cf65ae5535fa195d7ee223acaeac5d56043752dd473a9f`; report `f60e6bb634616e9e1e96b970a31264bec17fdff86554f47f415d56f7517652e7` |

Exact manifest output paths are:

| ID | Output paths |
|---|---|
| E01 | `results/raw/frontiers_hot_stove_v1_units.csv`; `results/summaries/frontiers_hot_stove_v1_cells.csv`; `results/summaries/frontiers_hot_stove_v1_effects.csv`; `results/figures/frontiers_hot_stove_v1_stratum_diagnostics.png`; `results/reports/frontiers_hot_stove_v1_report.md` |
| E02 | `results/raw/frontiers_m1_binary_graded_v1_units.csv`; `results/summaries/frontiers_m1_binary_graded_v1_arms.csv`; `results/summaries/frontiers_m1_binary_graded_v1_cells.csv`; `results/summaries/frontiers_m1_binary_graded_v1_effects.csv`; `results/figures/frontiers_m1_binary_graded_v1_disclosure_diagnostics.png`; `results/reports/frontiers_m1_binary_graded_v1_report.md` |
| E03 | `results/raw/frontiers_m2_regime_replication_v1_units.csv`; `results/summaries/frontiers_m2_regime_replication_v1_cells.csv`; `results/summaries/frontiers_m2_regime_replication_v1_effects.csv`; `results/summaries/frontiers_m2_regime_replication_v1_legacy_replay.csv`; `results/summaries/frontiers_m2_regime_replication_v1_stable_cells.csv`; `results/summaries/frontiers_m2_regime_replication_v1_thresholds.csv`; `results/figures/frontiers_m2_regime_replication_v1_standard_regime_diagnostics.png`; `results/reports/frontiers_m2_regime_replication_v1_report.md` |
| E04 | `results/raw/frontiers_m3_search_architectures_v1_units.csv`; `results/summaries/frontiers_m3_search_architectures_v1_canonical_cells.csv`; `results/summaries/frontiers_m3_search_architectures_v1_curves.csv`; `results/summaries/frontiers_m3_search_architectures_v1_effects.csv`; `results/summaries/frontiers_m3_search_architectures_v1_equivalences.csv`; `results/figures/frontiers_m3_search_architectures_v1_k_curve_diagnostics.png`; `results/reports/frontiers_m3_search_architectures_v1_report.md` |
| E05 | `results/raw/frontiers_m3_bflpe_crossover_v1_units.csv`; `results/summaries/frontiers_m3_bflpe_crossover_v1_analytic.csv`; `results/summaries/frontiers_m3_bflpe_crossover_v1_cells.csv`; `results/summaries/frontiers_m3_bflpe_crossover_v1_effects.csv`; `results/summaries/frontiers_m3_bflpe_crossover_v1_transitions.csv`; `results/figures/frontiers_m3_bflpe_crossover_v1_bflpe_crossover_diagnostics.png`; `results/reports/frontiers_m3_bflpe_crossover_v1_report.md` |

### C4. Recorded invocation and environment

| ID | Recorded command | Recorded time |
|---|---|---|
| E01 | `PYTHONPATH=src /Users/omer/workspace/venvs/venv314/bin/python -m gifted_masking.cli article-experiment --config configs/frontiers_article/e01_hot_stove_standard.json --approval-record projects/frontiers_article/approvals/E01_STANDARD_GO.md` | start `2026-08-11T23:50:33.924505+00:00`; end `2026-08-11T23:50:42.242901+00:00` |
| E02 | `PYTHONPATH=src /Users/omer/workspace/venvs/venv314/bin/python -m gifted_masking.cli article-experiment --config configs/frontiers_article/e02_binary_graded_standard.json --approval-record /Users/omer/workspace/personal/repos/gifted-masking/projects/frontiers_article/approvals/E02_STANDARD_GO.md` | start `2026-08-12T00:57:16.268212+00:00`; end `2026-08-12T00:57:24.820000+00:00` |
| E03 | `PYTHONPATH=src /Users/omer/workspace/venvs/venv314/bin/python -m gifted_masking.cli article-experiment --config configs/frontiers_article/e03_m2_regime_standard.json --approval-record /Users/omer/workspace/personal/repos/gifted-masking/projects/frontiers_article/approvals/E03_STANDARD_GO.md` | start `2026-08-12T02:50:00.796860+00:00`; end `2026-08-12T02:52:48.655055+00:00` |
| E04 | `PYTHONPATH=src /Users/omer/workspace/venvs/venv314/bin/python -m gifted_masking.cli article-experiment --config configs/frontiers_article/e04_m3_search_architectures_standard.json --approval-record projects/frontiers_article/approvals/E04_STANDARD_GO.md --output-dir results` | start `2026-08-12T04:57:18.543650+00:00`; end `2026-08-12T04:59:27.267708+00:00` |
| E05 | `PYTHONPATH=src /Users/omer/workspace/venvs/venv314/bin/python -m gifted_masking.cli article-experiment --config configs/frontiers_article/e05_m3_bflpe_crossover_standard.json --approval-record projects/frontiers_article/approvals/E05_STANDARD_GO.md --output-dir results` | recovery recorded `2026-08-12T23:22:00.257688+00:00`; original start/end `UNKNOWN / NOT_RECORDED` |

Recorded execution environment was Python 3.14.6, macOS 26.6.1 arm64, and NumPy 2.4.6 for all five; E01, E02, E04, and E05 also record Matplotlib 3.10.8. Exact byte counts, row counts, normalized configs, parameters, and seed hierarchies remain canonical in the five manifests. E05 states that existing core artifacts were validated after interrupted report finalization, with no simulation rerun; its three block hashes and assembled-raw match are retained in the manifest.

## D. Fingerprint algorithm

All five source fingerprints hash worktree bytes directly. Git commit/tree metadata does not enter. A tracked dirty file and an untracked file are treated identically if their path is included. Paths are repository-relative UTF-8 bytes. No newline normalization or content canonicalization occurs.

- **E01:** iterate, in order, `article.py`, `cli.py`, the `configs/frontiers_article` directory, and `test_article_e01.py`. A directory expands to lexicographically sorted recursive filesystem paths. For each regular file, append path bytes then raw bytes with no separator. Missing/non-file targets contribute nothing. The manifest does not record which dynamic config-directory members existed.
- **E02 and E03:** iterate their fixed path tuples in declaration order. Existing regular files contribute path bytes then raw bytes, without separators; missing paths are skipped.
- **E04:** iterate its fixed ten-path tuple. Every path contributes path bytes followed by raw bytes when present or the literal ASCII bytes `MISSING` when absent; there is no separator.
- **E05:** iterate its fixed eleven-path tuple. Each entry contributes path bytes, then the two literal bytes `\\0` (hex `5c30`, not NUL), raw file bytes, and the same two bytes again.

For E01–E04, the dirty-diff digest is SHA-256 of raw `git diff --no-ext-diff` output followed by the stripped `git status --porcelain` text bytes. The porcelain digest hashes that stripped status text. Consequently, the diff digest includes tracked unstaged patch bytes but only names/status for untracked files; source fingerprints content-hash the enumerated untracked files separately. E05 records only the porcelain digest and source fingerprint; its dirty-diff digest is `UNKNOWN / NOT_RECORDED`.

The maintained algorithms were not modified. A temporary read-only helper enumerated candidate blob combinations and implemented these exact byte rules outside production source; it was not committed.

## E. Search procedure

The search was bounded to repository and repository-linked evidence:

1. Inspected all local/remote branches, tags, stashes, linked worktrees, all reflogs with timestamps, the full reachable commit/file history, and the recorded run commit `e0e9a738986dd440180a228b024b0807336cd957` plus neighboring commits.
2. Confirmed there are no tags, no stashes, one worktree, no `.git/worktrees/`, and no reflog-only commits. The reachable sequence after the run commit is `e0e9a738` → `10018bd` → `c760d4f` → `9b25502` → `441cfe4` → checkpoint `907abfb`.
3. Ran read-only `git fsck --full --no-reflogs --unreachable`; found no unreachable commits, 96 unreachable trees, and 81 unreachable blobs. No garbage collection, prune, clean, checkout, reset, restore, or stash operation was used.
4. Inspected the 18 unreachable root trees containing relevant E01–E05 paths, enumerated relevant blob versions/absence states, reconstructed candidates in temporary memory/directories, and recomputed fingerprints.
5. Searched repository-local `doc-reviews/`, project/checkpoint/runbook/manifest/report areas, and file names/extensions for retained patches, diffs, bundles, source archives, or source snapshots. None contained another generator bundle.
6. Checked the one sibling location explicitly named by a repository record, `/Users/omer/workspace/test-code/gifted-masking`; it is absent. No unbounded home-directory search was performed.

Candidate coverage was exhaustive over the recovered path-blob variants for each fixed algorithm: E02 96 combinations, E03 96, E04 96, and E05 768 after applying the exact `5c30` delimiter semantics. For E01, all three recovered `cli.py` variants and every subset of the ten recovered config-directory members were tested with the recovered article/test variants (3,072 combinations). Reachable commits were checked as well. E01–E03 yielded zero exact matches. E04 and E05 each yielded one unique fingerprint-participating path/blob combination, duplicated across several unreachable root trees.

Remaining uncertainty is bounded but real: an external editor history, deleted filesystem backup, or unrecorded Codex workspace outside repository-linked locations could contain E01–E03 bytes. No evidence in the repository identifies such a location strongly enough to justify searching the user's entire home directory.

## F. Recovery results

### E01 — `ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE`

The recorded run commit predates the checked-in article generator/test source. Reachable history, reflog, and unreachable trees provide plausible later versions, but no candidate reproduces `042a60b7…`. E01's dynamic recursive config-directory membership makes the missing state especially underdetermined: the manifest did not record its member list. Similar/current sources and valid artifacts do not satisfy exact historical recovery.

### E02 — `ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE`

The recorded run commit does not contain the E02 generator or its test. Exhaustive combinations of recovered relevant blobs/absence states produced 96 candidate bundles and no match to `891e5a4f…`. The recovered pre-E06 candidate fingerprint `a818b98e…` is a mismatch and is not archived as recovered source.

### E03 — `ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE`

The recorded run commit does not contain the E03 generator or its test. Exhaustive combinations of recovered relevant blobs/absence states produced 96 candidate bundles and no match to `397fec83…`. The recovered pre-E06 candidate fingerprint `0c330c26…` is a mismatch and is not archived as recovered source.

### E04 — `HISTORICAL_SOURCE_RECOVERED`

Unreachable root tree `53f905a2902496bf129e8125c718d78d48695d29` contains the exact ten participating path/blob values. Recomputing E04's algorithm gives `8599406b776d23f9357d89664f456d84f45e3a3783df1c830c1772ceb86750ae`, identical to the manifest. Six other unreachable root trees contain the same participating combination. The minimal verified bundle is archived at `provenance/frozen_generator_sources/E04/` with per-file blob/SHA-256 inventory.

### E05 — `HISTORICAL_SOURCE_RECOVERED`

The same unreachable root tree contains the exact eleven participating path/blob values. Recomputing E05's literal-backslash-zero algorithm gives `f229a17da2c710d3c76ea5ca571fbf170a21e7c4c6c9c15cadda0366cfa19c02`, identical to the manifest. Two other unreachable root trees contain the same participating combination. The minimal verified bundle is archived at `provenance/frozen_generator_sources/E05/` with per-file blob/SHA-256 inventory.

## G. Verification

| Check | Result |
|---|---|
| Recompute all 33 protected artifact SHA-256 values from local files | PASS |
| Compare maintained core/M0–M4 blob IDs with analytic-audit authority | PASS |
| Recompute E04 fingerprint from archived bytes | expected `8599406b…`; recovered `8599406b…`; exact PASS |
| Recompute E05 fingerprint from archived bytes | expected `f229a17d…`; recovered `f229a17d…`; exact PASS |
| Compare archived file bytes with recorded unreachable-tree blobs | PASS for all 21 archived path entries |
| Parse provenance index CSV and archive JSON | PASS |
| Scan recovered bundles for secrets | One false-positive phrase in byte-exact E05 approval prose (`duplicate JSON keys, ...`); inspection and blob comparison confirm it is not a credential |
| `git diff --check` | P2-authored files pass; three pre-existing Markdown hard-break lines remain in the byte-exact E05 archive and cannot be normalized without invalidating recovery |
| Run stochastic/scientific experiment | NOT RUN |
| Run `./scripts/verify.sh` | NOT RUN, as required by P2's default boundary |

Fingerprint matching establishes historical generator-source identity for E04/E05 only. It does not mean those archived sources were rerun, installed as production code, or used to alter scientific results.

## H. Remaining gap

`ARTIFACT_PROVENANCE_GAP_OPEN` remains for E01, E02, and E03 because their exact historical dirty generator states are not recoverable from the bounded sources examined. Their manifest source and dirty-state hashes identify the missing states, and their artifact hashes remain valid, but the generator bytes cannot be reconstructed exactly.

E04 and E05 have no remaining historical generator-source gap under the manifest fingerprint contract. The broader Article-V1 figure generation-authority gap identified by the evidence audit is a separate issue and is not closed by these bundles.

## I. Scientific consequence

**No frozen scientific result was changed or rerun by P2.**

P2 changed no model, learner, RNG, config, seed, artifact, figure, experiment output, or scientific claim status. E01–E05 remain the confirmatory evidence boundary. E06/M4 remain excluded from Article-V1 confirmatory evidence. The recovery result changes only the historical-source provenance record.

## J. Recommended next step

Before P3, request separate authorization for:

> **P2B — create a clean deterministic reproduction anchor from the current maintained source, frozen configs, frozen seed hierarchies, and frozen artifact expectations for E01–E03.**

P2B must explicitly define whether exact byte equality or deterministic semantic/table equality is the acceptance target, preserve the historical manifests, and record any expected divergence. It will execute evidence-generating code and was therefore not started here. If the project owner explicitly accepts the E01–E03 provenance limitation for submission, that decision should be recorded as an authority; only then should work proceed directly to P3 bounded literature search.
