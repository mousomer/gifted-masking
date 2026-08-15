# Article V1 Publication Claim Ledger

**As of:** 15 August 2026  
**Status:** pre-freeze adjudication ledger updated after `ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md`.

This ledger governs publication wording. It does not replace the frozen evidence matrix, inferential audit, analytic authority, or literature authority.

## Decision labels

- `KEEP` — supported with the stated scope.
- `NARROW` — usable only with stricter wording.
- `BACKGROUND_ONLY` — true/illustrated but not contribution-bearing.
- `CANDIDATE` — may carry contribution weight if remaining prior-art review permits.
- `DIAGNOSTIC_ONLY` — scientifically useful post-hoc check; not a prespecified headline.
- `UNRESOLVED` — do not make a positive mechanistic/novelty claim.
- `CUT` — unsupported, contradicted, or outside V1.

## Claim table

| ID | Proposed claim | Evidence / analytic anchor | Decision | Maximum defensible wording |
|---|---|---|---|---|
| GEN-01 | A finite-horizon learner can conceal although authenticity has higher objective value. | Maintained models + generic prior art. | **BACKGROUND_ONLY** | Use as setup, not novelty. |
| E01-01 | Initial rejection reduces later authentic sampling in the tested M0 cells. | `-0.025837`; five master effects. | **KEEP / BACKGROUND_ONLY** | “Initial rejection reduced subsequent authentic sampling in the tested domain.” |
| E01-02 | Initial rejection independently increases normalized regret. | `+0.025824`; exact M0 action-count identity. | **NARROW / NOT INDEPENDENT** | “The same sampling shift corresponds to increased normalized objective pseudo-regret; the two estimands are algebraically linked.” |
| E01-03 | One rejection causes persistent final masking. | Final-mask contrast `-0.000343`, interval spans zero. | **CUT** | “No increase in final-window masking was detected.” |
| E01-04 | Forced authentic exploration reduces model masking after rejection. | Frozen E01 intervention contrast. | **KEEP / BACKGROUND_ONLY** | “Five-percent forced authentic exploration reduced final masking in the tested rejection stratum.” |
| E01-05 | Counterfactual authentic feedback reduces model masking after rejection. | Frozen E01 intervention contrast. | **KEEP / BACKGROUND_ONLY** | “Counterfactual authentic feedback reduced final masking in the tested rejection stratum.” |
| E01-06 | Higher negative-reward weighting increases masking without changing objective rewards. | Lambda contrast + analytic objective invariance. | **NARROW** | “Increasing the learner’s negative-reward weight increased masking under the tested settings while environmental rewards were unchanged.” |
| E01-07 | Loss weighting specifically amplifies the effect of one initial rejection. | Interaction `-0.001067`, interval spans zero. | **CUT** | “No amplification of the controlled initial-rejection gap was detected.” |
| E02-01 | Independent graded arms preserve more nonzero disclosure after rejection. | `+0.255040`. | **NARROW** | “Five independent graded actions produced more `d>0` resampling than binary full-authentic resampling in the frozen E02 architecture.” |
| E02-02 | Graded disclosure improves full-authentic endpoint discovery. | Full-authentic `-0.328692`; modal optimum `-0.221740`. | **CUT** | No positive endpoint-discovery claim. |
| E02-03 | Graded disclosure independently improves/worsens welfare beyond disclosure intensity. | M1 identity `normalized regret=1-d`. | **CUT AS INDEPENDENT WELFARE CLAIM** | “The graded architecture had greater normalized objective endpoint distance; this is the mean `1-d` statistic in the affine cells.” |
| E02-04 | M1 has a strictly optimal intermediate disclosure level. | Endpoint-optimum theorem. | **CUT** | “Intermediate actions change learning/exposure; the static objective remains endpoint-optimal except at indifference.” |
| E02-05 | E02 identifies a disclosure-specific mechanism beyond independent-arm dilution. | Current design cannot isolate. | **UNRESOLVED** | Await bounded graded-disclosure prior-art adjudication. |
| E03-01 | Aggregate final-window Neutral behavior can favor masking while full-information DP favors authenticity. | 243/357 frozen grid cells; exact DP. | **CANDIDATE** | Use exactly this aggregate-behavior vs full-information wording. |
| E03-02 | The E03 classifier is an individual learned-policy prevalence. | Classifier uses aggregate Neutral action counts across learners. | **CUT** | Do not call it individual-policy prevalence. |
| E03-03 | 243/357 estimates human prevalence or intrinsic phase-space volume. | Tested grid only. | **CUT** | “243 of 357 tested cells” only. |
| E03-04 | The learner failed relative to the best policy attainable under its information constraints. | No `pi_I*`. | **CUT** | Comparator is full-information DP only. |
| E03-05 | The full-information M2 comparator is numerically trustworthy. | Four-policy enumeration matches all 357 cells to max error `8.99e-10`. | **KEEP** | “Independent deterministic policy enumeration verified the frozen DP envelope.” |
| E03-06 | Persistent social-state structure may be contribution-bearing. | M2 dynamics + exact comparator; prior art open. | **CANDIDATE** | Candidate only until persistent-state prior-art search closes. |
| E04-01 | Increasing K alone causes masking. | Controls contradict a pure-K reading. | **CUT** | Do not use “more contexts cause masking.” |
| E04-02 | Scarcity alone has been causally isolated. | Combined controls constrain but do not isolate a unique component. | **CUT** | Do not attribute the result to scarcity alone. |
| E04-03 | Combined controls support representation-dependent burden under scarce receptivity. | Flat/hierarchical + global-mask + known-good + identity + abundance controls. | **CANDIDATE** | “Combined controls support representation-dependent learning burden under scarce receptivity in the frozen M3 design.” |
| E04-04 | Global-mask isolates duplicate-mask softmax normalization. | It also changes action count, aggregate policy mass, competition and updates. | **CUT** | Call it a shared-mask representation control. |
| E04-05 | M3 literally models children moving sequentially among peer groups. | Repeated context/action selection abstraction. | **CUT** | “Context selection is an abstract repeated search/selection problem.” |
| E04-D1 | Strict unique-modal endpoint diagnostics preserve E04 directions. | Post-hoc frozen diagnostic. | **DIAGNOSTIC_ONLY** | May be reported as robustness if explicitly labelled post hoc. |
| E05-01 | The flat E05 modal-response crossing occurs before the exact objective crossover. | `0.312852` `[.307836,.316918]` vs `8/17`. | **KEEP** | Report as learner/configuration-specific descriptive quantitative separation. |
| E05-02 | Binary Proposition G2 rules out temperature as a contributor to E05. | E05 statistic is eight-action across-child modal fraction. | **CUT / CONTRADICTED** | “The binary theorem does not identify or exclude the mechanism of the E05 statistic.” |
| E05-03 | Fixed temperature or action-set normalization explains the E05 displacement. | Not decomposed. | **UNRESOLVED** | List as possible contributors only. |
| E05-04 | Objective authenticity still has positive advantage at the empirical crossing. | Exact transform gives ~`.134076`; transformed bounds `[.130620,.138340]`. | **KEEP / CONDITIONAL** | State that uncertainty derives only from the crossing estimate, not model uncertainty. |
| E05-05 | The hierarchical crossing is absent globally. | Left-censored below approved dense range. | **CUT** | “No in-range hierarchical crossing was estimable.” |
| E05-D1 | Strict unique-modal E05 diagnostic gives a nearby crossing. | Post-hoc frozen diagnostic ~`.3103`. | **DIAGNOSTIC_ONLY** | Use only to show deterministic argmax ties do not create the flat finding. |
| GIFT-01 | Some gifted youth deliberately conceal/manage visible ability for social reasons. | Gifted-specific literature. | **KEEP** | “Some gifted youth report deliberate concealment or visibility management in response to social concerns.” |
| GIFT-02 | Gifted social coping is broader than concealment. | SCQ/stigma-management literature. | **KEEP** | Concealment is one strategy family within broader social coping. |
| GIFT-03 | Peer rejection/jealousy is a calibrated causal transition probability. | No calibration. | **CUT** | Report as empirical/social motivation, not calibrated model dynamics. |
| GIFT-04 | Concealment is widespread or longitudinally persistent. | Current literature does not establish either. | **CUT** | Treat prevalence/persistence as empirical limitations. |
| TERM-01 | “Masking” is definitively the best technical term. | Terminology audit open. | **UNRESOLVED** | Prefer “concealment/visibility management” when technical precision matters. |
| BFLPE-01 | `bf` is an empirically calibrated BFLPE measure. | Model comparison-cost parameter only. | **CUT** | “BFLPE-inspired/model comparison cost.” |
| M4-01 | M4/E06 numerical results are V1 confirmatory evidence. | Active scope excludes them. | **CUT FROM V1** | Future/Track-B architecture only. |
| PROV-01 | Frozen E01-E05 artifacts have complete historical source provenance. | P2 recovered fingerprint-exact E04/E05 bundles; E01–E03 exact generator states were not recoverable from bounded forensics. | **CUT UNTIL RESOLVED** | “Artifacts are hash-valid; E04/E05 historical generator source is archived, while the E01–E03 historical-source gap remains open pending P2B or explicit owner acceptance.” |

## Current contribution candidates

Only these may currently carry prospective contribution weight:

1. **E03 persistent social-state structure**, subject to formal prior-art search.
2. **E04 representation-dependent burden under scarce receptivity**, subject to formal prior-art search.
3. A possible **synthesis/application contribution** combining established incomplete-learning mechanisms with empirically grounded visibility management, persistent social consequences, and heterogeneous receptive contexts.

E01 is background/supporting. E02 is representation-constrained supporting/negative evidence. E05 is a descriptive quantitative result with unresolved mechanism.

## Freeze rule

No manuscript scientific assertion may survive V1-03 unless it has a claim-ledger ID and passes all of:

1. frozen computational evidence;
2. inferential-unit/uncertainty audit;
3. analytic compatibility;
4. literature/construct prior-art adjudication;
5. scope/provenance requirements.

After V1-03, new scientific claims require explicit reopening of claim freeze.
