# Independent Code Review — gifted-masking

**Reviewer:** Claude (Opus 4.8)
**Date:** 2026-06-16
**Scope:** Maintained package `src/gifted_masking` and its tests. Legacy
`simulations_old/` and `simulations1..3` were treated as preserved reference
artifacts and not reviewed for correctness.
**Method:** Static read of every maintained module and test, plus **independent
execution** of the model kernels, the full robustness suite, and the M2
optimal-policy machinery on a separate machine (Python 3.12, NumPy 2.4.4) to
confirm that committed artifacts reproduce and that headline numbers are real
rather than transcribed.

---

## 1. Verdict

The maintained package is in good shape. The code faithfully implements the M0–M4
specification in `AGENTS.md`, the numerics are sound, runs are deterministic and
reproducible across machines and NumPy versions, and — most importantly — the
self-audit discipline is genuine: the claims that the earlier prose reports
overstated are correctly flagged and narrowed in `CLAIM_AUDIT.md`, and the code
now contains the machinery (M2 value iteration, M3 ablation controls, M4 ramp
experiment) needed to adjudicate those claims rather than assert them.

The remaining work is about *evidentiary strength and reproducibility metadata*,
not correctness. There are no correctness blockers in the model kernels. The
blockers that exist are in the artifact/manifest layer and in the breadth of the
robustness sweeps, and they are already enumerated accurately in the repo's own
`CURRENT_STATE.md` and `SECOND_PASS_AUDIT.md`.

One housekeeping issue: the audit documents are at **different vintages** and now
partially contradict each other (see §7). `SECOND_PASS_AUDIT.md` still lists "M2
lacks value iteration" as a Major gap, but `analysis/m2_optimal.py` implements
exactly that and passes its tests. This should be reconciled so a reader knows
which document is current.

---

## 2. What I verified by execution

| Check | Result |
| ----- | ------ |
| Model + core + determinism tests (29 tests) | **all pass** on Python 3.12 / NumPy 2.4.4 |
| Full robustness summary regenerated from source | **reproduces `robustness_full_summary.csv` to all printed digits** |
| M0 analytic identities (E[mask]=0.75, p\*=2.15/3) | confirmed |
| M3 BFLPE analytic crossover bf\* | `0.470588`, matches spec exactly |
| M2 value iteration on reference cell (p=0.55, η=0) | converges; V=[11.11, 15.25, 8.17] |
| M2 transition rows sum to 1 across all (state, action) | confirmed |
| M3 search-burden ablation contrast | flat +0.18, hierarchical +0.39, **global-mask +0.015**, fixed-pond ≈0 |

The exact reproduction of every headline number on a different OS and a NumPy
major version ahead of the repo's pin (`numpy>=1.26,<3`; I ran 2.4.4) is strong
evidence that the RNG handling is genuinely seed-local and not dependent on
global state or platform float quirks at the reported precision.

---

## 3. Per-model audit

### Core (`core.py`) — clean
- `softmax_probabilities` subtracts the row max before `exp` (numerically
  stable) and rejects `temp <= 0`.
- `subjective_value` applies loss aversion only to negative rewards via
  `np.where(reward < 0, lam*reward, reward)` — correct, and it rejects `lam < 0`
  as `AGENTS.md` requires. λ=1 is an exact identity.
- `final_window_size` uses `ceil` with a floor of 1; off-by-one is handled
  correctly (`start = horizon - window`, counted with `t >= start`).
- **Minor:** `bootstrap_ci` resamples whatever array the caller supplies. That's
  fine, but it means CI validity is entirely contingent on the caller passing
  genuine per-child units (it does today — see §4).

### M0 (`m0.py`) — matches spec
Reward `np.where(action==0, b-c, np.where(accept, b+a, a-r))` is exactly the
specified bandit. Analytic helpers (`objective_indifference_r`,
`subjective_indifference_r`) match the formulas in `AGENTS.md`. The loss-aversion
collision warning in `AGENTS.md` (don't reuse `r`) is respected: the realized
reward is the array `reward`, the penalty is the scalar `r`.

### M1 (`m1.py`) — matches spec, with the right caveat already noted
Acceptance `1-(1-p)d`, reward `a*d - c*(1-d) ± {b, r}`, grid includes exactly 0
and 1, and `expected_reward` equals the closed form `b-c + d[a+c-(1-p)(b+r)]`.
Q-values are **independent per disclosure level** — the code does not model
smooth generalization, and `CLAIM_AUDIT.md` correctly restricts the M1 claim to
"lower-risk exploration," not static optimality of intermediate disclosure. Good.

### M2 (`m2.py` + `analysis/m2_optimal.py`) — the strongest part of the review
The three-state transition is implemented exactly as specified, with separate
RNG draws for outcome / turnover / escape, and turnover/escape applied to the
*next* state after the current reward. The reuse of `outcome_uniform` for both
the neutral-acceptance draw and the stigmatized-redemption draw is **safe**
because a child occupies exactly one state per step, so the two masks are
disjoint.

The important addition since `SECOND_PASS_AUDIT.md` was written is
`analysis/m2_optimal.py`: a value-iteration solver with exact policy evaluation
(`np.linalg.solve` on `(I - γPπ)`). Critically, its transition table correctly
decomposes the stigmatized-authentic-failure branch into η-escape vs. stay
sub-branches — i.e. the analytic MDP and the sampled learner share the same
semantics. I verified on the reference cell (p=0.55, η=0) that:

- static M0 comparator says **mask** is optimal,
- the **dynamic** MDP optimum is **authentic** (continuation value of the
  accepted state dominates),
- the learner nonetheless converges to masking, giving **positive regret
  (~3.56)**.

This is exactly why the audit's relabeling from "structural lock-in" to
**"learned suboptimal lock-in"** is correct: the trap is in the learner's
sampling, not in the environment forcing a masking optimum. The code now
*measures* this distinction instead of assuming it. This is publication-relevant
nuance done right.

### M3 (`m3.py`) — ablation discipline is excellent
`decode_action` (group = a//2, authentic = a%2) is tested directly. BFLPE is
subtracted only on good-pond acceptance, never on masking or bad ponds. All four
formulations the spec demands are present (flat 2K, hierarchical, global-mask,
fixed-good-pond). My run reproduces the key result: the K-effect is large where
K genuinely enlarges the search space (flat, hierarchical) and **collapses to
~0.015 in the global-mask control** where masking is a single shared action. That
contrast is what licenses the narrowed claim "context multiplicity harms *when it
creates an asymmetric search burden*" and rules out the trivial "more arms"
confound. This is the most scientifically careful thing in the repo.

### M4 (`m4.py`) — honest about path-dependence vs. hysteresis
`update_receptivity` applies the three specified deltas and `np.clip`s to
`[p_min, p_max]` every step; bounds are tested. The `hysteresis_experiment`
carries **both** `p_t` and the Q-table across ramp segments and advances seeds by
segment — a genuine ramp-up/ramp-down design, far better than inferring
hysteresis from split trajectories. The committed result (mask path-gap +0.065,
CI excludes 0) supports **path dependence under the tested schedule**, which is
exactly the wording `CLAIM_AUDIT.md` now uses. The stronger word "hysteresis"
remains correctly withheld pending loop-area / threshold / ramp-speed /
seed-replication diagnostics.

---

## 4. Reproducibility and statistics

**Good:** seed-local generators throughout; the primary unit file
`robustness_full_units.csv` stores one row per child (confirmed in
`RAW_FIELDNAMES` and the `_unit_rows_for_values` logic), so the headline CIs are
bootstrapped over genuine per-child units, not over a summary. The `code_config_hash`
over (effect, condition, unit, seed) gives a cheap drift tripwire, and
`test_m2_headline_effect_does_not_drift` pins the M2 escape effect to a literal
constant — a real regression guard.

**Blocker-level gaps (already known to the repo):**
1. The manifest records seed *strategy* prose and per-effect grids, but the
   `MASTER_SEED`/`BOOTSTRAP_SEED` constants and the explicit per-condition seed
   integers are not all serialized into the manifest in a form that reconstructs
   a run without reading `robustness.py`. Given how clean the rest is, this is
   low-effort to close.
2. Package-version capture is `numpy` + `matplotlib` only; there's no full
   environment lock. For publication-grade reproducibility, snapshot the full
   resolved environment.

**Statistical breadth:** every headline rests on a **single master seed** and a
**single calibration**. `AGENTS.md` itself requires replication across ≥3
independent master seeds and sensitivity to (n, T, window fraction, α, τ, λ, q0,
γ, grid resolution). That sweep does not yet exist in the maintained suite. Until
it does, the CIs quantify Monte-Carlo noise *within one seed*, not robustness of
the effect to reseeding — which is a different and stronger claim.

The two M4 path-gap effects rest on **7 ramp points each**; the CIs are real but
the unit count is small, so treat those intervals as indicative.

---

## 5. Findings by severity

| Severity | Finding | Status |
| --- | --- | --- |
| Blocker | Manifest lacks fully-serialized seed hierarchy / master seed for one-file reproduction | known (`SECOND_PASS_AUDIT.md`) |
| Major | No ≥3 independent master-seed replication of any headline | known (`AGENTS.md` target) |
| Major | M4 hysteresis diagnostics (loop area, threshold separation, ramp-speed, seed replication) absent | known (`CLAIM_AUDIT.md`) |
| Major | M3 random-good-pond and multiple-good-pond variants absent | known (`CURRENT_STATE.md`) |
| Major | BFLPE: no sweep around bf\*≈0.4706 with uncertainty; only bf∈{0,0.8} contrast | known |
| Major | Full environment/version capture incomplete | known |
| Moderate | Plotting still regenerates data at figure time rather than consuming frozen tables | known |
| Moderate | **Audit docs are inconsistent in vintage** (see §7) | **new — not yet flagged in repo** |
| Minor | `numpy>=1.26,<3` pin; I ran 2.4.4 and everything reproduced, but CI should pin a tested version | new |
| Minor | M0 `p=0`/`p=1` edge cases implied but not explicitly unit-tested | new |

---

## 6. Mapping back to the written report

For cross-reference with the Word/Pages report deliverables, the claims that
should be **softened** in any prose write-up, per the verified code:

- "Context multiplicity is harmful" → "harmful **when it creates an asymmetric
  search burden**" (global-mask control is ~0).
- "M4 shows hysteresis / a closing window" → "**path dependence under the tested
  km ramp**"; hysteresis not yet established.
- "Sticky stigma is structural lock-in" → "**learned** suboptimal lock-in: the
  dynamic MDP optimum is authenticity, but the learner converges to masking";
  true *optimal-learner* lock-in appears only under harsher stigma/turnover
  settings (per `analyze_m2_regimes`).
- "Risk-taking is strictly protective / risk-aversion is close to fatal" →
  **not supported** by any maintained robustness artifact; the maintained
  evidence is only "higher λ increases masking in M0." The risk-type figures
  exist in plotting but are not in the robustness report.

The directionally-solid, fully-supported claims: M0 hot-stove learned masking,
M0 λ effect, M1 receptivity→disclosure, M2 escape→less masking, M3 search-burden
mechanism via ablation, M4 path dependence.

---

## 7. Documentation reconciliation needed

`SECOND_PASS_AUDIT.md` (older) and `CLAIM_AUDIT.md` + `CURRENT_STATE.md` (newer)
disagree on M2:
- Old: "M2 lacks value iteration / regret benchmark" (Major).
- Current code: `analysis/m2_optimal.py` implements value iteration, exact policy
  evaluation, and per-cell regret, with passing tests.

Recommend adding a one-line "superseded by CURRENT_STATE.md as of <date>" banner
to `SECOND_PASS_AUDIT.md`, or regenerating it, so a new reader is not misled
about M2's status.

---

## 8. Recommended next steps (in order)

1. **Reconcile the audit docs** (§7) — 10 minutes, prevents confusion.
2. **Serialize the full seed hierarchy** into the manifest so a run reproduces
   from the manifest alone. The values already exist as constants; this is
   plumbing.
3. **Three-master-seed replication** of all seven headline effects; report
   between-seed variance alongside the within-seed bootstrap CI. This is the
   single highest-value addition for defensibility.
4. **BFLPE sweep** across ~9 bf values bracketing 0.4706 with per-child CIs, to
   substantiate (or retract) the "anticipatory retreat" wording.
5. **M4 hysteresis diagnostics**: loop area, transition-threshold separation,
   and at least two ramp speeds × three seeds, before the word "hysteresis" is
   used anywhere.
6. **M3 variants**: random good-pond identity per child and multiple good ponds,
   to test whether the search-burden result survives a non-fixed pond location.
7. Pin a tested NumPy in CI; add explicit M0 `p∈{0,1}` edge tests.

No model-semantics changes are recommended. The kernels are correct as written.
