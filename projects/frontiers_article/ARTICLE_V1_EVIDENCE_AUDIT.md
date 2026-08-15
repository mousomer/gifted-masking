# Article V1 Publication-Evidence Audit

**Status:** Stage V1-01 evidence audit complete  
**Date:** 2026-08-13  
**Evidence boundary:** E01–E05 adjudicated standard packages and established
analytic results only  
**Excluded:** E06, new simulation, new literature work, manuscript rewriting,
and Track B

## Audit outcome

Article V1 has a usable but deliberately narrow five-experiment evidence pool.
Every local E01–E05 standard output named in its manifest byte-matches the
manifest SHA-256. The strongest defensible story is:

1. E01 supports an information-restriction mechanism for later sampling and
   regret, plus information-restoration effects, but not a claim that one early
   rejection increased persistent final-window masking.
2. E02 shows that independent graded arms change the exposure distribution of
   exploration after rejection; they worsen full-endpoint selection and pooled
   normalized regret in the tested comparison.
3. E03 supports a tested-grid operational classifier: aggregate final-window
   Neutral-state action counts favored masking while the full-information
   objective M2 dynamic optimum favored authenticity. This is conditional on
   the frozen learner and tested grid; `243/357` is
   provenance/supplementary grid coverage, not a headline prevalence claim or
   an information-matched learner failure rate.
4. E04 supports representation-dependent search burden under scarce
   receptivity, not a generic claim that more contexts are harmful.
5. E05 supports a flat-2K learned retreat before objective indifference at
   `bf=.313` (`.308–.317`), with no estimable hierarchical crossing.

No Article-V1 confirmatory M4 result exists. M4 may appear in Methods/model
architecture, but its previous path result must not enter Article-V1 Results.

The machine-readable claim-by-claim record is
`ARTICLE_V1_EVIDENCE_MATRIX.csv`. `ARTICLE_V1_INFERENTIAL_AUDIT.md` gives the
replication trace, and `E05_SEED_EXTENSION_AUDIT.md` gives the seed-continuity
decision.

## Standard-package inventory and artifact identity

Hashes below are SHA-256 of current local file bytes. All publication-bearing
standard outputs recorded by the five manifests were also checked; no output
hash mismatch was found.

| Experiment | Run | Primary raw artifact (SHA-256) | Primary publication summary (SHA-256) | Manifest (SHA-256) |
| --- | --- | --- | --- | --- |
| E01 | `frontiers_hot_stove_v1` | `results/raw/frontiers_hot_stove_v1_units.csv` (`a4e78dcf…62dc01`) | `results/summaries/frontiers_hot_stove_v1_effects.csv` (`4ce67da8…684d8`) | `results/manifests/frontiers_hot_stove_v1.json` (`3f48573a…14e34`) |
| E02 | `frontiers_m1_binary_graded_v1` | `results/raw/frontiers_m1_binary_graded_v1_units.csv` (`3640b1a8…0619`) | `results/summaries/frontiers_m1_binary_graded_v1_effects.csv` (`11d29c72…15a8a`) | `results/manifests/frontiers_m1_binary_graded_v1.json` (`be541067…34e`) |
| E03 | `frontiers_m2_regime_replication_v1` | `results/raw/frontiers_m2_regime_replication_v1_units.csv` (`9561ff20…d150`) | effects `5a1ee392…b3af`; stable cells `91814ab4…aea7`; thresholds `0987aea9…f9bf` | `results/manifests/frontiers_m2_regime_replication_v1.json` (`18aa7b69…2646`) |
| E04 | `frontiers_m3_search_architectures_v1` | `results/raw/frontiers_m3_search_architectures_v1_units.csv` (`621227ff…19e`) | `results/summaries/frontiers_m3_search_architectures_v1_effects.csv` (`dd426992…d44`) | `results/manifests/frontiers_m3_search_architectures_v1.json` (`abf6fa74…9d71`) |
| E05 | `frontiers_m3_bflpe_crossover_v1` | `results/raw/frontiers_m3_bflpe_crossover_v1_units.csv` (`9de41835…947`) | analytic `e1045d05…2a42`; effects `33eb752c…00d5`; transitions `96b8d8dc…7097` | `results/manifests/frontiers_m3_bflpe_crossover_v1.json` (`cc600fd4…d3`) |

The complete 64-character hashes are in the evidence matrix and manifests.

### Config hash convention

The matrix records SHA-256 of config **file bytes**:

| Experiment | Config file SHA-256 | Manifest `config_sha256` |
| --- | --- | --- |
| E01 | `1d8ac3157a628c8115bdfe11a14ed46d794caeb2abb88c49b62bc2d2aa6b2f6a` | `cc5d0b5931d5ff0d855e6746a21b5f4ca1e280297280fe9e32cb2232e9b6b8fa` |
| E02 | `08aa809cbfdbf12f002a8b93e234923ef04e84d13a02c9e7ab12926ee84d431d` | `064cb856f0a9ed58452bc8a3014f2d913ed3034ffe1fddf6e0115b462ab797e6` |
| E03 | `52197a07751c03ca47872c2319aedd9705140eb38cb7048a091e48c40923e0e0` | `1d9e477274a1b6e83ef7fb7d08446c822113648d12a8744ca49464bd50104d1c` |
| E04 | `e8b73dc7c9904b75378d49f0772f1a3ea59e70a1c56581b1e95c98952f769e53` | `5c48d8d0358a54243e9ef1f2bad1ff106a293d5c6cab5771bd92a9e4cebc0981` |
| E05 | `571d3c93b46a97333839f81b53f8c21cc43a21a5427ec97c61cf38f0cd9d9e1f` | `60210519019688bf4acc0c3b5fcc9c1f4181d7b87c8eda1e1fdaecd0296446ae` |

These differ by design: the manifests hash canonical normalized JSON, not the
literal file bytes. Both identities are recorded; neither is substituted for
the other.

## E01–E05 headline evidence

### E01 — information restriction, restoration, and loss weighting

- Initial rejection reduced later authentic sampling by `0.025837` in absolute
  magnitude (`0.015922–0.035753`) and increased normalized objective
  pseudo-regret by `0.025824` (`0.015914–0.035735`).
- It did not measurably increase final-window masking: rejected minus accepted
  was `-0.000343` (`-0.011605–0.010918`).
- After rejection, 5% forced authentic exploration reduced final masking by
  `0.046590` (`0.033230–0.059951`) and normalized regret by `0.057954`
  (`0.045614–0.070293`). Counterfactual feedback reduced them by `0.118135`
  (`0.109683–0.126587`) and `0.141318` (`0.132369–0.150267`).
- At `p=.65`, changing `lambda` from `.5` to `2.5` increased final masking by
  `0.402990` (`0.395366–0.410614`) without changing objective payoff. The
  controlled high-minus-low early-rejection gap was null; loss weighting did
  not amplify that direct gap.
- **Disposition:** include the restoration and loss-weighting results; narrow
  the direct hot-stove claim and report the null final-mask effect.

### E02 — graded exploration exposure, not ladder benefit

- In the rejected stratum at equal-weight `p=.75/.85`, graded any disclosure
  minus binary full-authentic resampling was `0.255040`
  (`0.253004–0.257077`).
- Graded minus binary full-authentic final-window rate was `-0.328692`
  (`-0.342037–-0.315348`), and optimal-endpoint modal probability was
  `-0.221740` (`-0.288755–-0.154724`).
- Binary minus graded normalized regret was `-0.029761`
  (`-0.033874–-0.025648`): graded had worse pooled regret.
- **Disposition:** include only exposure-distribution wording. Cut protective
  ladder-climbing, smooth-generalization, endpoint-discovery, and regret-benefit
  language.

### E03 — aggregate final-window Neutral behavior versus the dynamic optimum

- In `243/357` exact-grid cells, the aggregate final-window Neutral-state
  action-count classifier favored masking while the full-information objective
  dynamic optimum favored authenticity (`0.680672`; the across-master
  interval collapses to that selected-stream value). Of 357 cells, 350 had a
  stable 4-of-5 operational classification: 243 aggregate-mask/objective-
  authenticity mismatches and 107 aggregate/objective matches; seven low-p
  eta-zero cells were inconclusive for inadequate Neutral visits.
- The comparator is the full-information, objective-reward M2 policy computed
  by value iteration over the exact three-state transition model, using the
  cell's gamma, tolerance `1e-10`, and maximum `100000` iterations. It is not an
  information-matched learner comparator.
- Objective neutral-authenticity thresholds were bracketed at
  `.383911–.383972` (`eta=0`), `.338745–.338806` (`eta=.2`), and
  `.268982–.269043` (`eta=.8`). No learned transition was estimable.
- Sensitivity is conditional: `gamma=.5` changed the first three of five
  dynamic-authenticity sentinels to learner/objective matches because the
  objective policy changed to masking. At `alpha=.03`, two high-p sentinels
  changed stability/classification; at `tau=.6`, the `.90,.2` sentinel became
  unstable and `.75,0` was only 4/5. Specified perturbations therefore changed
  some sentinel classifications.
- In the separately labeled harsh boundary (`b2=0,r2=8,delta=.3,eta=0`), only
  `p=.75` showed static M0 authenticity but objective M2 masking in all five
  masters (objective neutral Q gap `-0.4062934363`).
- **Disposition:** include a learner-setting-qualified mismatch result and the
  full-information comparator; keep `243/357` supplementary/provenance, not a
  headline. Reserve structural lock-in for the harsh objective-policy result.

### E04 — representation-dependent search burden

- Fixed-one receptive context: K=16 minus K=1 settling was `-0.234000`
  (`-0.246417–-0.221583`) for flat 2K and `-0.470400`
  (`-0.511031–-0.429769`) for hierarchical search.
- The global-mask change was `0.008800` (`0.002090–0.015510`) and remained
  inside the prespecified practical-equivalence band; fixed-known-good was
  structurally zero.
- Randomized receptive-context identity did not materially change the flat or
  hierarchical slopes. Two receptive contexts attenuated both declines, and
  the tested proportional-25 regime brought the slopes near zero.
- **Disposition:** include search burden only as representation- and scarcity-
  dependent. Do not state that context count alone causes masking.

### E05 — descriptive response crossing before objective indifference

- Exact objective advantage is `0.40 - 0.85*bf`; objective indifference is
  `8/17 = 0.4705882353`.
- The flat-K=4 across-child final-window modal-good-authentic response pooled
  PAVA crossing was `0.312852`, with 10,000/10,000 valid master-curve
  bootstrap crossings and interval `0.307836–0.316918`.
- At this descriptive response crossing the analytic objective advantage was
  about `0.134`.
  The flat endpoint response change from `bf=0` to `.80` was `-0.9400`
  (`-0.957993–-0.922007`).
- Hierarchical response was already below `.5` at `bf=.30`; 0/5 seed curves
  and 0/10,000 bootstrap curves produced an in-range crossing.
- **Disposition:** include the paired analytic/learned flat result with its
  representation boundary; retain the hierarchical non-estimability. The
  mechanism producing the flat displacement is unresolved: the binary softmax
  theorem does not adjudicate this eight-action across-child modal statistic,
  and fixed temperature, multi-action normalization, finite-horizon learning,
  endogenous sampling, and their interaction remain possible contributors.

## E01/E02 commensurability

**Classification: NOT_COMPARABLE** for a publication claim of cross-mechanism
dissociation.

| Dimension | E01 | E02 | Audit finding |
| --- | --- | --- | --- |
| Regret definition | best binary endpoint expected reward minus chosen binary action expected reward | best endpoint expected reward minus chosen disclosure action expected reward | Same objective pseudo-regret family, but graded regret is a continuous distance over five independent arms |
| Normalization | divide by `T*abs(E_auth-E_mask)`; equals binary suboptimal-action fraction in non-tie cells | same endpoint-gap denominator; equals normalized endpoint distance, not a simple action error count | Algebraically aligned scale in the auth-optimal linear domain, different behavioral meaning |
| Primary contrast | rejected minus accepted within controlled binary baseline; or baseline minus intervention among rejected | binary minus graded among rejected | Different estimands |
| Population | accepted and rejected strata, or rejected-only intervention rows | rejected stratum only | Not the same population contrast |
| Aggregation | equal weight p=.75/.85 within each E01 master | equal weight p=.75/.85 within each E02 master | Similar aggregation form, different masters and estimands |
| Pairing | no child pairing across E01 conditions | binary/graded common-random-number child pairing within master/p | Different dependence structure |
| Horizon/window/comparator | T=2000, final .2; static analytic binary optimum | T=2000, final .2; static analytic endpoint optimum | Matched horizon/window, related comparator |
| Sign | positive rejected-minus-accepted means rejection worsens regret | positive binary-minus-graded means graded improves regret | Opposite labels and different reference groups |

The underlying normalized metric can be placed on a common endpoint-gap scale,
but the stored publication effects cannot be compared as if they measured the
same outcome in the same stratum. Final masking and endpoint discovery are also
distinct outcomes and must not be substituted for regret.

## Reconciliation findings

When prose and artifacts disagree, the content-addressed adjudicated artifact
wins. No manuscript was changed in this stage.

| Location/old wording or value | Current authority | Disposition |
| --- | --- | --- |
| Assertive DOCX abstract, Results, Discussion, figure legend, and tables: `226/357` (`63.3%`) as a central M2 result | E03: `243/357` under five masters; Article V1 task bars it as a headline | **NARROW:** retain only tested-grid provenance/supplement if needed; do not headline |
| `RESULTS_BY_FINDING_CHAPTER.md` and `DISCUSSION_CHAPTER.md`: same `226/357`, mean mask `.950`, broad-regime prose | E03 exact-grid/stability artifacts | **REWRITE/NARROW** in a later stage |
| DOCX/source conclusion that early adverse experience restricted corrective evidence and produced persistent final masking | E01 sampling/regret effects pass; final-mask effect is null | **NARROW:** information restriction for sampling/regret only; explicitly report null final-mask contrast |
| DOCX/source M0 lambda result `0.403` with child-bootstrap interval `.386–.421`, `n=250` | E01 `0.402990`, five-master Student-t `.395366–.410614`, `n=500` per cell/master | **REWRITE** from E01 |
| DOCX/source M1 result `0.569` and wording that graded disclosure preserved exploration | E02 direct effect `0.255040`; endpoint and regret effects are adverse | **REWRITE/NARROW:** within-M1 `.569` may be legacy context only; direct architecture claim uses E02 and no benefit language |
| DOCX/source M2 escape effect `.201` with child-bootstrap `.115–.287` and one maintained seed | Not an E03 adjudicated headline; E03 supports classifications and specified sensitivities instead | **CUT** from Article-V1 confirmatory Results unless explicitly labeled legacy descriptive evidence |
| DOCX/source original M3 K=1/K=8 `.200` and ablation `.168/.377` with child bootstraps | E04 K=1/K=16 five-master effects `-.234/-.4704`, controls, identity/count variants | **REWRITE** from E04 |
| Assertive DOCX comparison-cost section/table: old `bf=0` versus `.80` endpoint only (`.918`) | E05 dense flat crossing `.312852` (`.307836–.316918`) before `8/17`; endpoint is secondary | **REWRITE:** dense result must lead |
| Source Markdown E05 section already has the dense result, while current DOCX does not | E05 transitions/analytic/effects and `E05_MAIN_RESULTS.md` | **RECONCILE:** source is newer; artifact values win |
| Any old E03 `226/357` replaced mechanically by `243/357` as a headline | Article-V1 task and E03 boundary | **CUT as headline:** do not promote `243/357`; use only provenance/supplement |
| Default M2 learned mismatch described as “structural lock-in” | Full-information VI says authenticity is optimal in those cells; harsh `p=.75` is the separate objective-policy case | **REWRITE:** use “learned suboptimal masking”; reserve structural language |
| Any wording implying an information-matched M2 optimum | No such analysis exists; comparator has full transition/reward information | **CUT:** say full-information objective M2 dynamic optimum |
| DOCX Methods: master seed 0, cell seeds 11–24/301/308/500–513; most contrasts n=200–250 and T=900–1200 | E01–E05 configs/manifests use experiment-specific five-master sets, n=160/500, T=1000/2000 as applicable | **REWRITE** tested-domain/RNG table |
| DOCX uncertainty section/figure legends: intervals reflect within-run synthetic dispersion and not uncertainty across masters | E01–E05 article intervals are across five master estimates/curves | **REWRITE:** state each experiment's actual top-level unit; retain no-human-inference boundary |
| DOCX Table 3 and Figure 1 use `manuscript_effect_estimates.csv` (`98ca0b7a…`) | E01–E05 adjudicated summaries | **SUPERSEDE** for publication claims |
| Existing M4 numerical result, path figure, and “path-dependent” Results wording | E06 excluded; no Article-V1 confirmatory M4 experiment | **CUT from Results:** retain M4 architecture only |
| Any M4 hysteresis or irreversible-entrenchment wording | No Article-V1 confirmatory evidence | **CUT** |
| Any wording mapping grid share/effects to human prevalence or intervention efficacy | No human calibration or causal human design | **CUT**; current boundary wording may be retained |

## Local-path and generation-authority audit

- Every explicit E01–E05 config, GO record, manifest, raw path, summary path,
  report, source-data CSV, manuscript source chapter, DOCX, TIFF, and the root
  PDF referenced by the inspected authority set exists locally.
- No missing publication-bearing E01–E05 machine artifact was recreated.
- The manuscript source tables
  `doc-reviews/frontiers_submission/data/manuscript_effect_estimates.csv`
  (SHA-256 `98ca0b7a…`) and
  `m2_suboptimal_masking_regime_summary.csv` (`82188a39…`) are present but
  superseded for claims updated by E01–E05.
- The existing article TIFFs are present, but no checked-in deterministic
  Article-V1 generator/source-data contract maps the adjudicated E01–E05
  artifacts to those TIFFs. Figure regeneration authority is therefore
  **MISSING_LOCAL** and is a Stage V1-03 blocker. The files themselves were not
  modified or recreated.

## Historical generator-source provenance disposition

P2 independently rechecked all 33 protected artifact hashes and then searched
reachable Git history, all refs/reflogs, stashes, worktrees, unreachable
objects, and bounded repository-linked archives for the dirty generator states
recorded by the E01–E05 manifests.

- E04 and E05 are `HISTORICAL_SOURCE_RECOVERED`: their minimal source bundles
  were recovered from unreachable Git trees, fingerprint-matched exactly, and
  archived under `provenance/frozen_generator_sources/`.
- E01, E02, and E03 are
  `ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE`: no recovered candidate matched
  their exact source fingerprints.
- `ARTIFACT_PROVENANCE_GAP_OPEN` therefore remains for E01–E03. This does not
  alter the frozen results, the protected artifact identities, or the prior
  maintained-model semantics audit.

The controlling record is
`ARTICLE_V1_GENERATOR_SOURCE_PROVENANCE_AUDIT.md`. The next gate is a separately
authorized P2B deterministic reproduction anchor for E01–E03, unless the owner
explicitly accepts the limitation for submission. No experiment was run in P2.

## Questions Stage V1-02 must resolve through literature work

These are questions only; this audit did not answer them.

1. Which recent empirical sources support selective disclosure/masking among
   gifted students without treating masking as a unitary trait?
2. Which source best supports the hot-stove/information-restriction mechanism,
   and how directly may it be connected to the educational setting?
3. What evidence supports interpreting graded disclosure as an opportunity for
   lower-exposure sampling rather than an intervention with established human
   benefit?
4. Which peer-context, person-group-fit, and classroom-composition sources are
   needed to bound E04's representation-dependent search claim?
5. How should BFLPE literature be used to motivate `bf` while making clear that
   E05 does not estimate a human placement threshold?
6. Which sources support the distinction among persistence, state dependence,
   path dependence, and hysteresis?
7. Are all current citations and bibliographic details accurate, current, and
   sufficient for the target Frontiers section?
8. What empirical longitudinal designs have actually measured sequences of
   disclosure, peer response, context change, and later masking?

## Blockers for the next stages

### Stage V1-02

- Complete P2B for E01–E03, or record explicit owner acceptance of the
  remaining historical-source limitation, before beginning the bounded
  literature searches.
- Resolve the eight literature questions without importing claims into the
  evidence matrix unless they are separately sourced and bounded.
- Decide whether legacy within-model descriptive contrasts are omitted or
  explicitly labeled non-confirmatory context.
- Keep E01/E02 cross-mechanism dissociation out unless a new harmonized,
  authorized analysis is designed; none is authorized by this audit.

### Stage V1-03

- Rewrite the DOCX and source chapters from `INCLUDE`/`NARROW` matrix rows,
  not by editing old numbers in place.
- Replace tested-domain, RNG, and uncertainty descriptions experiment by
  experiment.
- Create deterministic Article-V1 figure source tables/generators from the
  adjudicated artifact hashes.
- Remove quantitative M4 Results while retaining model architecture as needed.
- Re-render and visually verify the complete manuscript after authorized edits.
