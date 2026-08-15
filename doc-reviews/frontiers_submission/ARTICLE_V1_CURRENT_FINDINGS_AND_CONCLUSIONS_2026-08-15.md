# Article V1 — Current Findings and Conclusions

**Date:** 2026-08-15  
**Status:** Post-P0/P1 authority integration, post-P2 provenance audit, post-P3A persistent-social-state prior-art verification  
**Evidence boundary:** E01–E05 only. E06/M4 numerical findings are excluded from Article V1 confirmatory evidence.

## 1. Executive scientific state

The frozen E01–E05 numerical evidence remains intact. Maintained M0–M4 model semantics match the mathematical reference, protected E01–E05 artifact hashes reconcile, and the reported headline results can be reconstructed from the frozen evidence. The main corrections produced by the model-analysis audit concern interpretation, inferential scope, and provenance rather than corrupted numerical outputs.

The emerging Article V1 result is not that reinforcement learning can generically become stuck in concealment. That mechanism is established prior art. The potentially distinctive contribution is narrower: established incomplete-learning mechanisms are embedded in social environments with persistent consequences and scarce receptive contexts, producing bounded computational effects relevant to concealment/visibility management.

After P3A primary-source verification, E03 should currently be treated as a **synthesis-novelty candidate / central structural result**, not as a claim of wholly new formal ingredients. Strong prior art exists for dynamic concealment/reputation, evolutionary concealment under stigma, conceptual disclosure feedback, and self-confirming learning, but no verified same-mechanism predecessor was located that combines focal-agent learning, action-induced persistent individual social state, endogenous selective feedback, persistent defensive behavior, and comparison to a better-informed dynamic benchmark.

## 2. Governance and evidence status

### 2.1 Article V1 scope

- Confirmatory evidence: **E01, E02, E03, E04, E05**.
- **E06 is excluded** from Article V1 Results.
- **M4 numerical findings are excluded** from Article V1 confirmatory evidence.
- M4 may appear only as architecture/future-work context.
- Track B remains deferred until Article V1 submission freeze.

### 2.2 Provenance

P2 established:

- **E04:** `HISTORICAL_SOURCE_RECOVERED` — fingerprint-exact historical generator source archived.
- **E05:** `HISTORICAL_SOURCE_RECOVERED` — fingerprint-exact historical generator source archived.
- **E01–E03:** `ORIGINAL_GENERATOR_SOURCE_NOT_RECOVERABLE`.

For E01–E03 this is a historical generator-provenance limitation, not evidence corruption. Frozen artifact hashes pass, model semantics are verified, and numerical results reconstruct. Clean reruns are not currently required for scientific continuation; a clean reproduction anchor may be considered later as a reproducibility-packaging task.

## 3. Exact model-level conclusions

### 3.1 M0 — binary conceal/reveal baseline

Environmental expected rewards are:

- mask: `R_M = b - c`
- authentic: `E[R_A] = a + p b - (1-p) r`

so the objective gap is:

`Delta_0 = a + c - (1-p)(b+r)`.

At the frozen defaults `b=1, a=.6, c=.25, r=2`, the objective crossover is exactly:

`p* = 43/60 ≈ .716667`.

Loss weighting `lambda` changes the learner's update target for negative realized rewards; it does **not** change the environmental objective payoff.

### 3.2 M1 — graded disclosure

Expected reward is affine in disclosure level `d`:

`E[R(d)] = b - c + d[a+c-(1-p)(b+r)]`.

Therefore every strict static optimum is an endpoint (`d=0` or `d=1`) when both endpoints are available. Intermediate disclosure levels can change exploration/exposure, but they do not create a superior static interior optimum in this model.

In the relevant authenticity-optimal E02 cells, normalized pseudo-regret is exactly the horizon-average endpoint distance `1-d`. It is therefore not an independent welfare mechanism beyond disclosure intensity/end-point distance.

### 3.3 M2 — persistent social state

M2 uses three states: Neutral, Accepted, and Stigmatized. Authentic action from Neutral can move the agent to Accepted or Stigmatized, and later rewards/transitions depend on the social state. The full-information objective comparator is the exact discounted MDP optimum.

Independent deterministic enumeration of the four relevant stationary policies reproduces the value-iteration envelope over all 357 frozen cells with maximum absolute discrepancy `8.99e-10`.

The comparator remains a **full-information oracle**. No information-matched optimum `pi_I*` has been computed, so the observed gap cannot be decomposed into information cost versus algorithmic inefficiency.

Selected deterministic objective thresholds move approximately from `.384` to `.339` to `.269` as `eta` changes from `0` to `.2` to `.8`. These are selected-parameter results, not a general monotonicity theorem.

### 3.4 M3 — heterogeneous contexts

Under frozen defaults:

- mask reward: `.75`
- good-context authenticity: `1.15 - .85 bf`
- bad-context authenticity: `-.8`

The exact environmental good-authentic/mask crossover is:

`bf* = 8/17 ≈ .470588`.

With one good context, increasing `K` changes multiplicity and learning/search structure but does not alter this full-information best-option payoff boundary.

### 3.5 M4 — future work only

The maintained M4 equations are mathematically verified as architecture, including the pure-masking recurrence and conditional authenticity drift. They are **not Article V1 numerical evidence**. Claims of hysteresis, bistability, irreversible entrenchment, or endogenous-receptivity confirmation remain unsupported for V1.

## 4. Experiment-level findings

## 4.1 E01 — restricted feedback changes learning dynamics

### Demonstrated

- Initial rejection reduced subsequent authentic sampling by approximately `0.025837` in the tested `p=.75/.85` domain.
- The corresponding normalized pseudo-regret contrast is approximately `+0.025824`.
- No increase in final-window masking was detected: rejected-minus-accepted approximately `-0.000343`, with interval `[-0.011605, 0.010918]`.
- Five-percent forced authentic exploration reduced final masking and normalized pseudo-regret after rejection.
- Counterfactual authentic feedback reduced final masking and normalized pseudo-regret after rejection.
- Increasing negative-outcome weighting (`lambda=.5` to `2.5`) produced a large increase in final masking at `p=.65` (approximately `+0.402990`).
- No detected interaction showed that greater loss weighting specifically amplified the effect of one controlled initial rejection.

### Important identity

In the relevant authenticity-optimal binary cells:

`normalized_regret = (# mask actions)/T`.

Because the first action is forced authentic, the E01 sampling and normalized-regret contrasts are algebraically the same action-frequency information expressed in two scales. They must not be presented as independent confirmations.

### Maximum conclusion

E01 supports a **finite-horizon restricted-feedback effect on subsequent sampling** and shows that information-restoring manipulations reduce model masking/regret. It does **not** demonstrate persistent final masking after one rejection.

### Scientific role

Generic incomplete-learning / hot-stove-like baseline and supporting demonstration; not expected to carry formal novelty.

## 4.2 E02 — graded disclosure preserves nonzero exposure but not endpoint discovery

### Demonstrated

- Independent graded arms increased post-rejection nonzero disclosure relative to the binary full-authentic action by approximately `+0.255040`.
- Graded arms reduced final-window full-authentic selection by approximately `-0.328692`.
- Graded arms reduced the probability that the unique modal endpoint was the objective endpoint by approximately `-0.221740`.
- Graded arms did not improve pooled normalized pseudo-regret; the frozen sign indicates worse performance for graded arms.

### Important identity / limitation

Because M1 is affine, normalized pseudo-regret in the relevant cells is exactly average endpoint distance `1-d`. The five graded levels are also independent tabular actions with no interpolation or structured generalization.

### Maximum conclusion

A richer graded action set can preserve some nonzero disclosure while making discovery/selection of the optimal full-authentic endpoint worse under independent-arm learning. This does not demonstrate that partial disclosure is protective, welfare-improving, or a successful ladder to authenticity.

### Scientific role

Supporting/representation-sensitive result. Disclosure-specific novelty remains secondary and requires only bounded prior-art adjudication.

## 4.3 E03 — persistent social state and oracle/behavior divergence

### Demonstrated

- In `243/357` frozen tested cells, **aggregate final-window Neutral-state behavior favored masking while the full-information dynamic optimum favored authenticity**.
- `350/357` cells had stable classifications across the selected master streams; seven low-`p`, `eta=0` cells were visit-inconclusive.
- The `243/357` statistic is a **tested-grid operational classification**, not prevalence, learner fraction, or parameter-space measure.
- The full-information dynamic optimum is independently verified by policy enumeration to `8.99e-10` maximum discrepancy.

### Interpretation boundary

This result does not show failure relative to the best policy attainable under the learner's own information structure. No `pi_I*` comparator exists.

### P3A literature conclusion

Primary-source verification found strong component prior art but no verified same-mechanism predecessor containing the entire conjunction of:

- conceal/reveal choice;
- action-induced persistent individual social state;
- state-dependent future consequences;
- focal-agent incomplete learning;
- endogenous selective feedback;
- persistent defensive behavior arising from learning;
- comparison to a better-informed dynamic benchmark.

Strong component precedents include:

- dynamic concealment/reputation models (Gietzmann; Bertomeu et al.);
- evolutionary concealment under stigma (Ferguson et al.);
- signal-burying/evolutionary persistence (Hoffman et al.);
- the conceptual Disclosure Processes Model (Chaudoir & Fisher);
- generic self-confirming learning (Fudenberg & Levine).

The Disclosure Processes Model is conceptual rather than a formal mathematical state-transition/learning model. Dynamic financial disclosure models are strong structural prior art but generally analyze optimal behavior by a focal actor who knows the environment, rather than focal-agent learning under unknown social response. Self-confirming equilibrium provides the generic endogenous-feedback learning ingredient but not the disclosure/persistent-social-state application itself.

### Provisional novelty role

`SYNTHESIS_NOVELTY_CANDIDATE` and `CENTRAL_STRUCTURAL_RESULT`.

The defensible candidate contribution is the **combination/operationalization**, not invention of the individual ingredients.

### Provisional maximum novelty wording

Prior work separately establishes dynamic concealment under reputational or stigmatic consequences and incomplete-learning mechanisms in which endogenous feedback can sustain incorrect beliefs. E03 combines these ingredients in a minimal persistent-social-state learning model and demonstrates a tested regime in which aggregate learned behavior favors concealment while the full-information dynamic optimum favors authenticity.

This wording remains provisional until the final P4 novelty synthesis.

## 4.4 E04 — representation-dependent burden under scarce receptivity

### Demonstrated

- Flat `2K` architecture: K=16 minus K=1 final-window good-authentic argmax fraction approximately `-0.2340`.
- Hierarchical architecture: approximately `-0.4704`.
- Randomizing the identity of the good context preserves the qualitative decline, arguing against a fixed-label artifact.
- A global-mask representation largely removes the large K-associated decline.
- A known-good-context control is structurally K-invariant.
- Two good contexts attenuate the decline.
- Maintaining a proportional set of good contexts largely removes the decline.
- Post-hoc strict-unique-modal diagnostics preserve the main direction; these remain robustness diagnostics rather than prespecified confirmatory estimands.

### Maximum current conclusion

Combined controls support a **representation-dependent learning/search burden when receptive contexts are scarce and must be discriminated among**.

The experiment does **not** isolate:

- K alone;
- scarcity alone;
- duplicate-mask normalization alone;
- literal human movement among peer groups.

The model should be described as an abstract repeated context/action-selection problem.

### Scientific role

Currently a `CENTRAL_STRUCTURAL_RESULT` candidate. Its novelty status is the main target of P3B.

## 4.5 E05 — learned/objective transition separation

### Demonstrated

For flat K=4:

- across-child final-window modal-good-authentic response crosses `.5` at approximately `bf=.312852`;
- master-level bootstrap interval approximately `[.307836, .316918]`;
- exact environmental good-authentic/mask crossover is `8/17 ≈ .470588`;
- objective authenticity advantage at the empirical crossing is approximately `.134076`;
- transformed crossing interval gives an objective-advantage interval approximately `[.130620, .138340]` conditional on crossing uncertainty;
- hierarchical response is already below `.5` at the start of the approved dense range, so the hierarchical crossing is left-censored rather than absent.

### Corrected analytic interpretation

The binary-softmax theorem `P(A)=.5 iff Q_A=Q_B` is correct only for a genuine two-action softmax probability. E05's primary statistic is an across-child modal-arm fraction in an eight-action policy. Therefore the theorem cannot rule out fixed temperature or multi-action normalization as contributors to the observed displacement.

### Maximum conclusion

E05 demonstrates a real **descriptive quantitative separation** between the learned modal-response transition and the exact environmental payoff transition in the frozen flat architecture. The causal mechanism producing the displacement remains unresolved.

### Scientific role

`SUPPORTING_QUANTITATIVE_RESULT`, not currently a central novelty result.

## 5. Current literature/novelty picture

### Established background

The following should not be claimed as new:

- early adverse outcomes can suppress future exploration under restricted feedback;
- chosen actions determine observed feedback, allowing beliefs/values about unchosen actions to remain poorly learned;
- forced exploration and counterfactual/full feedback can restore information;
- richer independent action sets can increase exploration burden;
- structured/generalizing bandit models can mitigate independent-arm learning costs;
- gifted youth use social coping, concealment/hiding of ability, conformity/popularity management, and peer-acceptance strategies;
- concealable stigmatized identities involve selective disclosure and feedback from disclosure outcomes;
- dynamic disclosure/reputation and evolutionary concealment models already exist.

### Potential Article V1 contribution after P3A

The weakest novelty thesis is rejected:

> "RL can become stuck masking even when authenticity is objectively better."

That is too generic.

The remaining candidate thesis is narrower:

> Established incomplete-learning mechanisms may acquire distinct consequences when embedded in environments with persistent social consequences and scarce receptive contexts. Article V1 isolates these structures in a controlled model cascade and quantifies the resulting concealment-related behavior.

The E03 portion of that thesis has survived the P3A bounded verification as a **synthesis/combination novelty candidate**. E04 still requires P3B adjudication.

## 6. Construct and terminology conclusions to date

Gifted-specific literature directly supports social coping and deliberate concealment/hiding or management of ability visibility. Concealment is best treated as one branch of broader gifted social coping, rather than the entirety of it.

Current hierarchy:

`gifted social coping -> information/visibility management -> concealment of ability`

The term **masking** remains useful as project shorthand but has not yet been established as the safest canonical gifted-education term. A later terminology pass should decide among masking, concealment, hiding giftedness/ability, visibility management, and related constructs without importing autism-specific findings wholesale.

Current construct mapping:

- conceal/reduce visible ability: directly grounded;
- adverse peer/social response: directly grounded as reported experience, but model transition probabilities are theoretical;
- receptive social context: plausibly grounded;
- graded disclosure: plausible model mapping;
- persistent stigmatized/accepted state: theoretical/indirect mapping;
- sequential discovery of receptive contexts: plausible but weakly direct in gifted empirical literature;
- persistent concealment trajectory after a single rejection: not established.

## 7. Provisional experiment roles for the paper

| Experiment | Current role | Current novelty status |
|---|---|---|
| E01 | Supporting/background baseline | Generic mechanism established |
| E02 | Supporting representation-sensitive result | Novelty limited/unresolved; likely not central |
| E03 | Central structural result | `SYNTHESIS_NOVELTY_CANDIDATE` after P3A |
| E04 | Central structural result candidate | Requires P3B scarce-receptive-context adjudication |
| E05 | Supporting quantitative result | Mechanism unresolved; not central novelty |
| E06/M4 | Excluded from V1 confirmatory evidence | Track B/future work |

These roles remain provisional until P4/P5.

## 8. Remaining literature tasks

The remaining literature work should be bounded and independent rather than reopening the whole review.

### P3B — E04 scarce receptive-context prior art

Determine whether prior formal work already combines:

- heterogeneous contexts/alternatives;
- rare favorable/receptive contexts;
- discovery through selected feedback;
- defensive/default behavior;
- learning burden attenuated when good contexts are known or less scarce;
- representation effects distinct from raw K.

The critical distinction is among:

`larger K`, `lower favorable proportion`, `unknown identity`, and `action representation`.

### P3C — E02 graded/partial disclosure prior art

Determine whether any disclosure-specific mechanism remains after accounting for independent-arm action-space and structured-bandit prior art.

### P3D — terminology

Resolve canonical Article V1 language for masking/concealment/visibility management/social coping/camouflaging.

After P3B–P3D, literature search stops unless a specifically identified unresolved primary source is publication-critical.

## 9. Remaining paper pipeline

After literature gap closure:

1. **P4 — final novelty and construct synthesis.** Classify E01–E05 as formal/application/synthesis novelty, structural/supporting/background, and determine giftedness framing.
2. **P5 — adversarial claim freeze.** Every manuscript scientific claim receives KEEP/NARROW/BACKGROUND_ONLY/SUPPLEMENT_ONLY/CUT; no unledgered claim may enter the manuscript.
3. **P6A — rebuild Results from the frozen evidence matrix + analytic authority + claim ledger.** Do not patch stale legacy Results line-by-line.
4. **P6B — rebuild Methods from model contracts, frozen configs, manifests, inferential audit, and provenance audit.**
5. **P6C — write Introduction only after novelty freeze.**
6. **P6D — write Discussion/limitations only after Results and Intro are stable.**
7. **P7 — full numerical/citation/mathematical/provenance/claim audit.**
8. **P8 — abstract/title and final adversarial reviewer-style audit.**
9. **P9 — submission freeze with commit and file hashes.**

## 10. Current prohibitions

Do not state or imply:

- one initial rejection causes persistent final masking;
- E01 sampling and regret are independent confirmations;
- E02 demonstrates a beneficial disclosure ladder or welfare improvement;
- `243/357` is prevalence or a proportion of learners;
- E03 compares the learner with an information-matched optimum;
- E04 proves K alone or scarcity alone causes masking;
- E04 literally models human peer-group movement;
- E05 fixed temperature has been ruled out as a cause of the displacement;
- M4/E06 provides Article V1 confirmatory evidence;
- the combined E03 mechanism is definitively unprecedented in the literature.

## 11. Current overall conclusion

Article V1 now has a coherent candidate structure:

- **E01** establishes the generic restricted-feedback/information baseline.
- **E02** shows that adding graded independent actions changes exposure but does not automatically improve endpoint discovery.
- **E03** adds persistent social consequences and currently survives primary-source prior-art verification as a synthesis/combination novelty candidate rather than an already-located same-mechanism model.
- **E04** adds scarce receptive-context discovery and representation dependence; this is the next decisive novelty question.
- **E05** quantifies a learned/objective transition separation but does not identify its causal mechanism.

The likely paper contribution, if E04 survives P3B in a similarly bounded form, is not a new generic learning pathology but a **minimal computational synthesis showing how known incomplete-learning dynamics interact with persistent social-state structure and scarce receptive-context structure in a concealment/visibility-management application**.

This conclusion remains provisional until P3B–P3D, P4 novelty synthesis, and P5 claim freeze are complete.
