"""Deterministic extraction of Article-V1 publication-source data from frozen E01-E05 artifacts.

Each extractor verifies its frozen sources, pins a literal selector, projects the
exact required fields, asserts the frozen scientific invariants, and writes one
compact publication-source CSV plus a provenance record. Figures read only the
CSVs written here, never `results/raw/` and never `results/summaries/`.
"""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

from pubcommon import (
    DATA_DIR,
    SUMMARIES,
    provenance_record,
    read_rows,
    repr_float,
    require,
    source_ref,
    write_rows,
)

# ---------------------------------------------------------------------------
# Pinned selectors. These are literal and must never fall back to a default.
# ---------------------------------------------------------------------------

POOLED_P = "pooled_equal_weight_p_0.75_0.85"
ACROSS_MASTERS = "across_master_seeds"
E02_STRATUM = "rejected"
E03_COMPONENT = "exact_grid"
E03_SENSITIVITY = "baseline"
E04_RESPONSE = "mean_settled_any_good_auth_argmax"
E05_RESPONSE = "modal_good_auth_argmax_fraction"

# Frozen values the build refuses to proceed without. Tolerances cover floating
# point representation only, never a changed dataset.
TOL = 1e-12
E05_FLAT_CROSSING = 0.31285211267605634
E05_OBJECTIVE_CROSSING = 8 / 17
E03_TESTED_CELLS = 357
E03_LEARNED_SUBOPTIMAL_CELLS = 243


def _pick(rows: list[dict[str, str]], **selector: str) -> list[dict[str, str]]:
    return [r for r in rows if all(r[k] == v for k, v in selector.items())]


def _one(rows: list[dict[str, str]], label: str, **selector: str) -> dict[str, str]:
    hits = _pick(rows, **selector)
    require(len(hits) == 1, f"{label}: selector {selector} matched {len(hits)} rows, expected exactly 1")
    return hits[0]


# ---------------------------------------------------------------------------
# E01 - M0 hot stove
# ---------------------------------------------------------------------------

E01_ESTIMANDS = [
    (
        "E01-C2-SAMPLING",
        "rejected_minus_accepted_post_initial_authentic_rate",
        "primary",
        "Post-initial authentic action rate, rejected minus accepted.",
    ),
    (
        "E01-C2-REGRET",
        "rejected_minus_accepted_normalized_regret",
        "linked_unit_translation",
        "The same action-frequency information in normalized objective-loss units. "
        "Exact identity: regret contrast = -(T-1)/T x sampling contrast (freeze C.5). "
        "Not an independent confirmation.",
    ),
    (
        "E01-C2-FINAL-MASK",
        "rejected_minus_accepted_final_mask_rate",
        "secondary_null",
        "Final-window mask rate contrast. Interval spans zero: a failure to detect, "
        "not an established equivalence.",
    ),
]


def extract_e01() -> tuple[Path, dict[str, object]]:
    effects_path = SUMMARIES / "frontiers_hot_stove_v1_effects.csv"
    rows = read_rows(effects_path)

    selector = {"level": ACROSS_MASTERS, "p": POOLED_P, "lambda": "", "condition": "", "stratum": ""}
    present = {r["effect_name"] for r in rows}
    for _, name, _, _ in E01_ESTIMANDS:
        require(name in present, f"E01: expected metric {name!r} absent from frozen effects table")

    out: list[dict[str, object]] = []
    for claim_id, name, role, definition in E01_ESTIMANDS:
        row = _one(rows, f"E01/{name}", effect_name=name, **selector)
        require(row["ci_status"] == "student_t_95", f"E01/{name}: unexpected ci_status {row['ci_status']!r}")
        estimate, low, high = float(row["estimate"]), float(row["ci_low"]), float(row["ci_high"])
        out.append(
            {
                "claim_id": claim_id,
                "effect_name": name,
                "level": row["level"],
                "p_selector": row["p"],
                "role": role,
                "estimate": repr_float(estimate),
                "ci_low": repr_float(low),
                "ci_high": repr_float(high),
                "ci_status": row["ci_status"],
                "interval_spans_zero": str(low < 0.0 < high),
                "definition": definition,
            }
        )

    by_role = {r["role"]: r for r in out}
    sampling = float(by_role["primary"]["estimate"])
    regret = float(by_role["linked_unit_translation"]["estimate"])
    null_row = by_role["secondary_null"]

    # C.5: the two headline quantities are one estimand in two units.
    horizon = 2000
    require(
        math.isclose(regret, -(horizon - 1) / horizon * sampling, rel_tol=0, abs_tol=1e-9),
        "E01: the regret/sampling identity of freeze C.5 no longer holds; "
        f"regret={regret!r} sampling={sampling!r}",
    )
    # The null annotation may only be rendered if the interval really spans zero.
    require(
        null_row["interval_spans_zero"] == "True",
        "E01: final-mask interval no longer spans zero; the null annotation is not licensed",
    )

    path = DATA_DIR / "e01_primary_effects.csv"
    write_rows(path, list(out[0].keys()), out)
    return path, provenance_record(
        output=path,
        experiment="E01",
        sources=[source_ref(effects_path)],
        selector=selector,
        fields=["effect_name", "estimate", "ci_low", "ci_high", "ci_status"],
        transformation=["row_filter", "column_projection"],
        notes=(
            "Three primary E01 estimands at the pooled equal-weight p in {0.75, 0.85} "
            "across-master-seeds level. Roles encode freeze C.5: sampling is primary, "
            "regret is its unit translation, final-mask is a secondary null."
        ),
    )


# ---------------------------------------------------------------------------
# E02 - M0/M1 binary versus graded
# ---------------------------------------------------------------------------

E02_ESTIMANDS = [
    (
        "E02-C4-EXPLORATION",
        "graded_any_minus_binary_full_post_initial_rate",
        "primary",
        "Graded nonzero-disclosure post-initial rate minus binary full-authentic post-initial rate.",
    ),
    (
        "E02-C4-FULL-ENDPOINT",
        "graded_minus_binary_full_final_window_rate",
        "adverse",
        "Graded minus binary full-authentic final-window selection rate.",
    ),
    (
        "E02-C4-MODAL",
        "graded_minus_binary_optimal_endpoint_modal_probability",
        "adverse",
        "Graded minus binary probability that the unique final-window modal arm is the objective endpoint d = 1.",
    ),
    (
        "E02-C4-REGRET",
        "binary_minus_graded_normalized_regret",
        "adverse_linked",
        "Binary minus graded normalized regret. In the affine cells per-step normalized regret "
        "is exactly 1 - d, so this is a horizon-average disclosure-distance contrast (freeze C.6).",
    ),
]


def extract_e02() -> tuple[Path, dict[str, object]]:
    effects_path = SUMMARIES / "frontiers_m1_binary_graded_v1_effects.csv"
    rows = read_rows(effects_path)

    # The rejected stratum is mandatory and may never be defaulted.
    strata = {r["stratum"] for r in rows}
    require(
        E02_STRATUM in strata,
        f"E02: mandatory stratum {E02_STRATUM!r} absent from frozen effects table (found {sorted(strata)})",
    )
    selector = {"level": ACROSS_MASTERS, "p": POOLED_P, "stratum": E02_STRATUM}

    out: list[dict[str, object]] = []
    for claim_id, name, role, definition in E02_ESTIMANDS:
        row = _one(rows, f"E02/{name}", effect_name=name, **selector)
        require(
            row["stratum"] == E02_STRATUM,
            f"E02/{name}: extracted row has stratum {row['stratum']!r}, expected {E02_STRATUM!r}",
        )
        require(row["ci_status"] == "student_t_95", f"E02/{name}: unexpected ci_status {row['ci_status']!r}")
        out.append(
            {
                "claim_id": claim_id,
                "effect_name": name,
                "level": row["level"],
                "p_selector": row["p"],
                "stratum": row["stratum"],
                "role": role,
                "estimate": repr_float(float(row["estimate"])),
                "ci_low": repr_float(float(row["ci_low"])),
                "ci_high": repr_float(float(row["ci_high"])),
                "ci_status": row["ci_status"],
                "definition": definition,
            }
        )

    require(
        {r["stratum"] for r in out} == {E02_STRATUM},
        "E02: publication extraction contains a stratum other than 'rejected'",
    )

    path = DATA_DIR / "e02_primary_effects.csv"
    write_rows(path, list(out[0].keys()), out)
    return path, provenance_record(
        output=path,
        experiment="E02",
        sources=[source_ref(effects_path)],
        selector=selector,
        fields=["effect_name", "stratum", "estimate", "ci_low", "ci_high", "ci_status"],
        transformation=["row_filter", "column_projection"],
        notes=(
            "Four E02 estimands for the approved rejected initial-outcome stratum only. "
            "The exploration result may not be shown without the three adverse results."
        ),
    )


def extract_e02_arms() -> tuple[Path, dict[str, object]]:
    """M1 arm-level expected rewards: the affine objective backing Figure 2's E02 panel."""
    arms_path = SUMMARIES / "frontiers_m1_binary_graded_v1_arms.csv"
    rows = [r for r in read_rows(arms_path) if r["p"] in {"0.75", "0.85"}]
    require(rows, "E02 arms: no rows at p in {0.75, 0.85}")

    out = []
    for row in sorted(rows, key=lambda r: (float(r["p"]), float(r["d"]))):
        p, d = float(row["p"]), float(row["d"])
        expected = float(row["expected_reward"])
        # E[R(d)] = b - c + d[a + c - (1-p)(b+r)], affine in d.
        b, a, c, r_pen = 1.0, 0.6, 0.25, 2.0
        closed_form = (b - c) + d * (a + c - (1.0 - p) * (b + r_pen))
        require(
            math.isclose(expected, closed_form, rel_tol=0, abs_tol=1e-12),
            f"E02 arms: p={p} d={d} frozen expected_reward {expected!r} != affine closed form {closed_form!r}",
        )
        out.append(
            {
                "p": repr_float(p),
                "d": repr_float(d),
                "expected_reward": repr_float(expected),
                "analytic_optimal_endpoint": row["analytic_optimal_endpoint"],
                "available_binary_endpoints": row["available_binary_endpoints"],
                "available_graded_independent_5": row["available_graded_independent_5"],
            }
        )

    path = DATA_DIR / "e02_arm_expected_rewards.csv"
    write_rows(path, list(out[0].keys()), out)
    return path, provenance_record(
        output=path,
        experiment="E02",
        sources=[source_ref(arms_path)],
        selector={"p": ["0.75", "0.85"]},
        fields=["p", "d", "expected_reward", "analytic_optimal_endpoint"],
        transformation=["row_filter", "column_projection", "closed_form_analytic"],
        notes=(
            "M1 per-arm expected reward at the two controlled acceptance probabilities. "
            "Each frozen value is re-checked against E[R(d)] = b - c + d[a + c - (1-p)(b+r)], "
            "which is affine in d, so every strict static optimum is an endpoint."
        ),
    )


# ---------------------------------------------------------------------------
# E03 - M2 regime replication
# ---------------------------------------------------------------------------


def extract_e03() -> tuple[Path, dict[str, object]]:
    cells_path = SUMMARIES / "frontiers_m2_regime_replication_v1_cells.csv"
    stable_path = SUMMARIES / "frontiers_m2_regime_replication_v1_stable_cells.csv"

    selector = {"component": E03_COMPONENT, "sensitivity_name": E03_SENSITIVITY}
    cells = _pick(read_rows(cells_path), **selector)
    stable_rows = read_rows(stable_path)

    by_cell: dict[str, list[dict[str, str]]] = {}
    for row in cells:
        by_cell.setdefault(row["parameter_cell_id"], []).append(row)
    require(
        len(by_cell) == E03_TESTED_CELLS,
        f"E03: tested grid has {len(by_cell)} cells, expected {E03_TESTED_CELLS}",
    )
    stable_by_cell = {r["parameter_cell_id"]: r for r in stable_rows}
    require(
        set(stable_by_cell) == set(by_cell),
        "E03: stable-cell table and exact-grid cells do not cover the same parameter cells",
    )

    out: list[dict[str, object]] = []
    for cell_id, master_rows in by_cell.items():
        require(len(master_rows) == 5, f"E03: cell {cell_id} has {len(master_rows)} master rows, expected 5")
        # Objective quantities are deterministic: they must agree across masters.
        for field in ("p", "eta", "objective_neutral_action", "objective_neutral_q_gap_auth_minus_mask"):
            values = {r[field] for r in master_rows}
            require(len(values) == 1, f"E03: cell {cell_id} field {field} varies across masters: {values}")

        head = master_rows[0]
        stable_row = stable_by_cell[cell_id]
        adequate = sum(r["neutral_visit_adequate"] == "True" for r in master_rows)
        learned = {r["learned_neutral_action"] for r in master_rows if r["learned_neutral_action"]}
        require(
            len(learned) <= 1,
            f"E03: cell {cell_id} has conflicting learned neutral actions across masters: {learned}",
        )

        classification = stable_row["classification"]
        stable = stable_row["stable"]
        # Publication category: an unstable or unclassified cell is shown as
        # inconclusive and is never dropped from the map.
        category = classification if stable == "True" and classification else "inconclusive"

        out.append(
            {
                "parameter_cell_id": cell_id,
                "p": repr_float(float(head["p"])),
                "eta": repr_float(float(head["eta"])),
                "learned_neutral_action": next(iter(learned), ""),
                "objective_neutral_action": head["objective_neutral_action"],
                "objective_neutral_q_gap_auth_minus_mask": repr_float(
                    float(head["objective_neutral_q_gap_auth_minus_mask"])
                ),
                "classification": classification,
                "stable": stable,
                "neutral_visit_adequate": str(adequate == 5),
                "neutral_visit_adequate_master_count": adequate,
                "publication_category": category,
            }
        )

    out.sort(key=lambda r: (float(r["p"]), float(r["eta"])))

    counts = {c: sum(r["publication_category"] == c for r in out) for c in
              {r["publication_category"] for r in out}}
    require(
        counts.get("learned_suboptimal_masking") == E03_LEARNED_SUBOPTIMAL_CELLS,
        f"E03: learned_suboptimal_masking cells = {counts.get('learned_suboptimal_masking')}, "
        f"expected {E03_LEARNED_SUBOPTIMAL_CELLS}",
    )
    require(
        counts.get("inconclusive", 0) > 0,
        "E03: no inconclusive cells present; inconclusive cells must remain represented on the map",
    )
    require(sum(counts.values()) == E03_TESTED_CELLS, "E03: publication categories do not partition the tested grid")

    path = DATA_DIR / "e03_grid_map.csv"
    write_rows(path, list(out[0].keys()), out)
    return path, provenance_record(
        output=path,
        experiment="E03",
        sources=[source_ref(cells_path), source_ref(stable_path)],
        selector=selector,
        fields=[
            "p",
            "eta",
            "parameter_cell_id",
            "learned_neutral_action",
            "objective_neutral_action",
            "classification",
            "stable",
            "neutral_visit_adequate",
            "objective_neutral_q_gap_auth_minus_mask",
        ],
        notes=(
            "One row per tested parameter-grid cell of the frozen 21 x 17 baseline exact grid "
            f"({E03_TESTED_CELLS} cells). Objective fields are deterministic and verified identical "
            "across the five master seeds; learned action and visit adequacy are aggregated by count. "
            "publication_category maps an unstable or unclassified cell to 'inconclusive' so that no "
            "tested cell is omitted from the map. Counts are tested-grid coverage, not prevalence."
        ),
        transformation=["row_filter", "column_projection", "deterministic_join", "count_aggregation"],
    )


def extract_e03_summary(grid_path: Path) -> tuple[Path, dict[str, object]]:
    rows = read_rows(grid_path)
    categories = ["learner_matches_objective", "learned_suboptimal_masking", "inconclusive"]
    out = [
        {
            "publication_category": category,
            "cell_count": sum(r["publication_category"] == category for r in rows),
            "tested_cell_total": E03_TESTED_CELLS,
            "coverage_statement": f"{sum(r['publication_category'] == category for r in rows)} "
            f"of {E03_TESTED_CELLS} tested parameter-grid cells",
        }
        for category in categories
    ]
    require(
        sum(r["cell_count"] for r in out) == E03_TESTED_CELLS,
        "E03 summary: category counts do not sum to the tested grid",
    )
    path = DATA_DIR / "e03_grid_summary.csv"
    write_rows(path, list(out[0].keys()), out)
    return path, provenance_record(
        output=path,
        experiment="E03",
        sources=[source_ref(grid_path)],
        selector={"component": E03_COMPONENT, "sensitivity_name": E03_SENSITIVITY},
        fields=["publication_category", "cell_count"],
        transformation=["count_aggregation"],
        notes=(
            "Tested-grid coverage counts. 243/357 means 243 of the 357 tested parameter-grid cells. "
            "It is not a prevalence, not a share of people or environments, not phase-space volume, "
            "and not a probability that masking occurs."
        ),
    )


# ---------------------------------------------------------------------------
# E04 - M3 search architectures
# ---------------------------------------------------------------------------

E04_HEADLINE_EFFECTS = [
    ("E04-C6-FLAT", "flat_2k_mean_settled_any_good_auth_argmax_S16_minus_S1_fixed_one", "primary"),
    ("E04-C6-HIER", "hierarchical_mean_settled_any_good_auth_argmax_S16_minus_S1_fixed_one", "primary"),
    ("E04-C6-CONTROL-GLOBALMASK", "global_mask_mean_settled_any_good_auth_argmax_S16_minus_S1_fixed_one", "control"),
    ("E04-C6-CONTROL-KNOWNGOOD", "fixed_known_good_mean_settled_any_good_auth_argmax_structural_K_effect", "control"),
    ("E04-C6-CONTROL-PROP25-FLAT", "flat_2k_mean_settled_any_good_auth_argmax_proportional25_minus_one_slope", "control"),
    ("E04-C6-CONTROL-PROP25-HIER", "hierarchical_mean_settled_any_good_auth_argmax_proportional25_minus_one_slope", "control"),
]


def _proportional_25_good_count(k: int) -> int:
    """Frozen regime definition from src/gifted_masking/experiments/e04.py:129."""
    return max(1, math.ceil(k / 4))


def extract_e04_curves() -> tuple[Path, dict[str, object]]:
    curves_path = SUMMARIES / "frontiers_m3_search_architectures_v1_curves.csv"
    rows = read_rows(curves_path)
    require(
        E04_RESPONSE in rows[0],
        f"E04: primary response field {E04_RESPONSE!r} absent from frozen curves table",
    )

    selector = {
        "canonical_identity_mode": "fixed",
        "series": {
            "one_good": "effective_good_count == 1",
            "proportional_25": "effective_good_count == max(1, ceil(K/4))",
            "known_good_reference": "architecture == fixed_known_good (structurally K-invariant)",
        },
    }

    wanted: list[tuple[str, str, int, int]] = []
    for architecture in ("flat_2k", "hierarchical", "global_mask"):
        for k in (1, 2, 4, 8, 16):
            wanted.append(("one_good", architecture, k, 1))
            wanted.append(("proportional_25", architecture, k, _proportional_25_good_count(k)))
    wanted.append(("known_good_reference", "fixed_known_good", 1, 1))

    out: list[dict[str, object]] = []
    for series, architecture, k, good in wanted:
        hits = _pick(
            rows,
            architecture=architecture,
            canonical_identity_mode="fixed",
            K=str(k),
            effective_good_count=str(good),
        )
        if not hits:
            continue
        require(
            len(hits) == 5,
            f"E04: {architecture} K={k} m={good} has {len(hits)} master rows, expected 5",
        )
        values = [float(r[E04_RESPONSE]) for r in hits]
        mean = sum(values) / len(values)
        out.append(
            {
                "series": series,
                "architecture": architecture,
                "K": k,
                "effective_good_count": good,
                "effective_good_fraction": repr_float(good / k),
                "canonical_identity_mode": "fixed",
                "response_metric": E04_RESPONSE,
                "n_master_seeds": len(values),
                "n_per_cell": hits[0]["n"],
                "master_mean": repr_float(mean),
                "master_min": repr_float(min(values)),
                "master_max": repr_float(max(values)),
            }
        )

    for series in ("one_good", "proportional_25"):
        for architecture in ("flat_2k", "hierarchical"):
            points = [r for r in out if r["series"] == series and r["architecture"] == architecture]
            require(len(points) == 5, f"E04: {series}/{architecture} has {len(points)} K points, expected 5")

    out.sort(key=lambda r: (r["series"], r["architecture"], r["K"]))
    path = DATA_DIR / "e04_k_response.csv"
    write_rows(path, list(out[0].keys()), out)
    return path, provenance_record(
        output=path,
        experiment="E04",
        sources=[source_ref(curves_path)],
        selector=selector,
        fields=["architecture", "K", "effective_good_count", E04_RESPONSE],
        transformation=["row_filter", "column_projection", "equal_weight_master_mean", "master_range"],
        notes=(
            "K-response curves on the prespecified primary metric "
            f"{E04_RESPONSE}. master_min/master_max are the observed range across the five master "
            "seeds and are a descriptive spread, not a confidence interval; the inferential unit for "
            "E04 headline effects is the five master seeds, and those intervals are carried in "
            "e04_headline_effects.csv. The proportional_25 series uses the frozen regime definition "
            "m = max(1, ceil(K/4)), so it coincides with the one-good series at K = 1, 2, 4."
        ),
    )


def extract_e04_effects() -> tuple[Path, dict[str, object]]:
    effects_path = SUMMARIES / "frontiers_m3_search_architectures_v1_effects.csv"
    rows = read_rows(effects_path)
    present = {r["effect_name"] for r in rows}
    for claim_id, name, _ in E04_HEADLINE_EFFECTS:
        require(name in present, f"E04: frozen effect {name!r} ({claim_id}) absent from effects table")

    selector = {"level": ACROSS_MASTERS}
    out: list[dict[str, object]] = []
    for claim_id, name, role in E04_HEADLINE_EFFECTS:
        row = _one(rows, f"E04/{name}", effect_name=name, **selector)
        out.append(
            {
                "claim_id": claim_id,
                "effect_name": name,
                "level": row["level"],
                "role": role,
                "response_metric": E04_RESPONSE,
                "estimate": repr_float(float(row["estimate"])),
                "ci_low": repr_float(float(row["ci_low"])) if row["ci_low"] != "" else "",
                "ci_high": repr_float(float(row["ci_high"])) if row["ci_high"] != "" else "",
                "ci_status": row["ci_status"],
            }
        )

    flat = float(_one(out, "E04 flat", claim_id="E04-C6-FLAT")["estimate"])
    hier = float(_one(out, "E04 hier", claim_id="E04-C6-HIER")["estimate"])
    require(math.isclose(flat, -0.234, rel_tol=0, abs_tol=1e-9), f"E04: flat headline is {flat!r}, expected -0.234")
    require(math.isclose(hier, -0.4704, rel_tol=0, abs_tol=1e-9), f"E04: hierarchical headline is {hier!r}, expected -0.4704")

    path = DATA_DIR / "e04_headline_effects.csv"
    write_rows(path, list(out[0].keys()), out)
    return path, provenance_record(
        output=path,
        experiment="E04",
        sources=[source_ref(effects_path)],
        selector=selector,
        fields=["effect_name", "estimate", "ci_low", "ci_high", "ci_status"],
        transformation=["row_filter", "column_projection"],
        notes=(
            "Frozen K = 16 minus K = 1 contrasts on the primary metric for the two search "
            "architectures, plus the known-good, global-mask, and proportional-abundance controls "
            "that establish the effect is not a trivial K-only reward effect. Student-t across five "
            "master seeds (df = 4)."
        ),
    )


# ---------------------------------------------------------------------------
# E05 - M3 comparison-cost crossover
# ---------------------------------------------------------------------------


def extract_e05_response() -> tuple[Path, dict[str, object]]:
    cells_path = SUMMARIES / "frontiers_m3_bflpe_crossover_v1_cells.csv"
    transitions_path = SUMMARIES / "frontiers_m3_bflpe_crossover_v1_transitions.csv"
    cells = read_rows(cells_path)
    transitions = [r for r in read_rows(transitions_path) if r["level"] == ACROSS_MASTERS]

    require(
        E05_RESPONSE in cells[0],
        f"E05: primary response field {E05_RESPONSE!r} absent from frozen cells table",
    )
    dense_min = float(transitions[0]["dense_bf_min"])
    dense_max = float(transitions[0]["dense_bf_max"])

    grouped: dict[tuple[str, float], list[dict[str, str]]] = {}
    for row in cells:
        grouped.setdefault((row["architecture"], float(row["bf"])), []).append(row)

    out: list[dict[str, object]] = []
    for (architecture, bf), master_rows in sorted(grouped.items()):
        require(
            len(master_rows) == 5,
            f"E05: {architecture} bf={bf} has {len(master_rows)} master rows, expected 5",
        )
        values = [float(r[E05_RESPONSE]) for r in master_rows]
        pooled = sum(values) / len(values)
        out.append(
            {
                "architecture": architecture,
                "architecture_role": master_rows[0]["architecture_role"],
                "bf": repr_float(bf),
                "bf_label": master_rows[0]["bf_label"],
                "in_dense_range": str(dense_min - TOL <= bf <= dense_max + TOL),
                "is_analytic_threshold_anchor": master_rows[0]["is_analytic_threshold_anchor"],
                "response_metric": E05_RESPONSE,
                "n_master_seeds": len(values),
                "n_per_cell": master_rows[0]["n"],
                "pooled_response": repr_float(pooled),
                "master_min": repr_float(min(values)),
                "master_max": repr_float(max(values)),
                "analytic_objective_advantage_good_auth_minus_mask": repr_float(
                    float(master_rows[0]["analytic_objective_advantage_good_auth_minus_mask"])
                ),
                "objective_comparator": master_rows[0]["objective_comparator"],
            }
        )

    # The equal-n pooled mean must reproduce the value the frozen fit recorded at
    # the dense boundary; that is what licenses this aggregation.
    for transition in transitions:
        architecture = transition["architecture"]
        for boundary, stored_field in (("dense_bf_min", "raw_dense_start_response"), ("dense_bf_max", "raw_dense_end_response")):
            bf = float(transition[boundary])
            match = _one(out, f"E05 pooled {architecture}@{bf}", architecture=architecture, bf=repr_float(bf))
            require(
                math.isclose(float(match["pooled_response"]), float(transition[stored_field]), rel_tol=0, abs_tol=1e-12),
                f"E05: pooled mean at {architecture} bf={bf} is {match['pooled_response']}, "
                f"frozen {stored_field} is {transition[stored_field]}",
            )

    path = DATA_DIR / "e05_response_vs_bf.csv"
    write_rows(path, list(out[0].keys()), out)
    return path, provenance_record(
        output=path,
        experiment="E05",
        sources=[source_ref(cells_path), source_ref(transitions_path)],
        selector={"response_metric": E05_RESPONSE, "dense_range": [dense_min, dense_max]},
        fields=["architecture", "bf", E05_RESPONSE, "analytic_objective_advantage_good_auth_minus_mask"],
        transformation=["row_filter", "column_projection", "equal_weight_master_mean", "master_range"],
        notes=(
            "Across-child modal good-context authentic fraction against comparison cost bf. "
            "pooled_response is the equal-n mean over the five master-seed fractions, which is the "
            "pooling the frozen PAVA fit used; it is verified to reproduce the frozen "
            "raw_dense_start_response and raw_dense_end_response exactly. master_min/master_max are "
            "a descriptive range, not a confidence interval. No fit is recomputed here: the reported "
            "crossing and its bootstrap interval are read from the frozen transitions table."
        ),
    )


def extract_e05_crossings() -> tuple[Path, dict[str, object]]:
    transitions_path = SUMMARIES / "frontiers_m3_bflpe_crossover_v1_transitions.csv"
    analytic_path = SUMMARIES / "frontiers_m3_bflpe_crossover_v1_analytic.csv"
    transitions = [r for r in read_rows(transitions_path) if r["level"] == ACROSS_MASTERS]
    analytic = read_rows(analytic_path)

    selector = {"level": ACROSS_MASTERS, "response_metric": E05_RESPONSE, "fit_method": "nonincreasing_pava_equal_n"}
    out: list[dict[str, object]] = []
    for row in transitions:
        require(
            row["response_metric"] == E05_RESPONSE and row["fit_method"] == "nonincreasing_pava_equal_n",
            f"E05: unexpected transition row selector {row['response_metric']!r}/{row['fit_method']!r}",
        )
        out.append(
            {
                "architecture": row["architecture"],
                "architecture_role": row["architecture_role"],
                "transition_status": row["transition_status"],
                "transition_bf": repr_float(float(row["transition_bf"])) if row["transition_bf"] else "",
                "ci_low": repr_float(float(row["ci_low"])) if row["ci_low"] else "",
                "ci_high": repr_float(float(row["ci_high"])) if row["ci_high"] else "",
                "ci_method": row["ci_method"],
                "bootstrap_replicates": row["bootstrap_replicates"],
                "bootstrap_valid_crossings": row["bootstrap_valid_crossings"],
                "analytic_threshold_bf": repr_float(float(row["analytic_threshold_bf"])),
                "learned_minus_analytic_threshold": repr_float(float(row["learned_minus_analytic_threshold"]))
                if row["learned_minus_analytic_threshold"]
                else "",
                "dense_bf_min": repr_float(float(row["dense_bf_min"])),
                "dense_bf_max": repr_float(float(row["dense_bf_max"])),
                "decision_eligible": row["decision_eligible"],
                "censoring_note": ""
                if row["transition_status"] == "valid"
                else "Left-censored below the observed dense range; no in-range crossing is estimable "
                "and none may be extrapolated.",
            }
        )

    flat = _one(out, "E05 flat crossing", architecture="flat_2k")
    hier = _one(out, "E05 hierarchical crossing", architecture="hierarchical")

    require(
        math.isclose(float(flat["transition_bf"]), E05_FLAT_CROSSING, rel_tol=0, abs_tol=TOL),
        f"E05: flat learned crossing is {flat['transition_bf']}, expected {E05_FLAT_CROSSING!r}",
    )
    require(flat["transition_status"] == "valid", f"E05: flat transition_status is {flat['transition_status']!r}")
    require(
        float(flat["analytic_threshold_bf"]) == float(Fraction(8, 17)),
        f"E05: objective crossing is {flat['analytic_threshold_bf']}, expected exactly 8/17 = {E05_OBJECTIVE_CROSSING!r}",
    )
    require(
        hier["transition_status"] == "no_crossing_below"
        and hier["transition_bf"] == ""
        and hier["decision_eligible"] == "False"
        and int(hier["bootstrap_valid_crossings"]) == 0,
        "E05: hierarchical transition no longer indicates an unestimable in-range crossing "
        f"(status={hier['transition_status']!r}, bf={hier['transition_bf']!r}, "
        f"valid_bootstrap={hier['bootstrap_valid_crossings']!r})",
    )

    anchors = [r for r in analytic if r["is_analytic_threshold_anchor"] == "True"]
    require(len(anchors) == 1, f"E05: analytic table has {len(anchors)} threshold anchors, expected 1")
    require(
        anchors[0]["analytic_threshold_exact"] == "8/17",
        f"E05: frozen exact threshold is {anchors[0]['analytic_threshold_exact']!r}, expected '8/17'",
    )
    require(
        math.isclose(float(anchors[0]["analytic_objective_advantage_good_auth_minus_mask"]), 0.0, rel_tol=0, abs_tol=1e-12),
        "E05: objective advantage at the exact crossover is not zero",
    )

    path = DATA_DIR / "e05_crossings.csv"
    write_rows(path, list(out[0].keys()), out)
    return path, provenance_record(
        output=path,
        experiment="E05",
        sources=[source_ref(transitions_path), source_ref(analytic_path)],
        selector=selector,
        fields=["architecture", "transition_bf", "ci_low", "ci_high", "analytic_threshold_bf", "transition_status"],
        transformation=["row_filter", "column_projection"],
        notes=(
            "Frozen learned crossing and its master-seed bootstrap interval for flat_2k, the exact "
            "objective crossover 8/17, and the hierarchical left-censored status. The empirical "
            "crossing is reportable descriptively; the design does not isolate a mechanism, and "
            "fixed temperature and action-set normalization remain possible contributors."
        ),
    )


def extract_e05_displacement(crossings_path: Path) -> tuple[Path, dict[str, object]]:
    """Closed-form quantities read off the frozen crossing. No refitting."""
    flat = _one(read_rows(crossings_path), "E05 flat", architecture="flat_2k")
    learned = float(flat["transition_bf"])
    objective = float(flat["analytic_threshold_bf"])
    ci_low, ci_high = float(flat["ci_low"]), float(flat["ci_high"])

    # R_G(bf) - R_M = 0.40 - 0.85 bf under the frozen M3 payoffs.
    def advantage(bf: float) -> float:
        return 0.40 - 0.85 * bf

    displacement = objective - learned
    out = [
        {
            "quantity": "learned_flat_crossing_bf",
            "value": repr_float(learned),
            "display": f"{learned:.6f}",
            "basis": "frozen PAVA crossing, e05_crossings.csv",
        },
        {
            "quantity": "learned_flat_crossing_ci_low",
            "value": repr_float(ci_low),
            "display": f"{ci_low:.6f}",
            "basis": "frozen master-seed bootstrap, 10,000 resamples",
        },
        {
            "quantity": "learned_flat_crossing_ci_high",
            "value": repr_float(ci_high),
            "display": f"{ci_high:.6f}",
            "basis": "frozen master-seed bootstrap, 10,000 resamples",
        },
        {
            "quantity": "objective_crossing_bf",
            "value": repr_float(objective),
            "display": f"{objective:.6f}",
            "basis": "exact analytic 8/17",
        },
        {
            "quantity": "displacement_objective_minus_learned",
            "value": repr_float(displacement),
            "display": f"{displacement:.6f}",
            "basis": "closed form: 8/17 - learned crossing",
        },
        {
            "quantity": "objective_advantage_at_learned_crossing",
            "value": repr_float(advantage(learned)),
            "display": f"{advantage(learned):.6f}",
            "basis": "closed form: 0.40 - 0.85 bf at the learned crossing",
        },
    ]

    require(
        math.isclose(abs(displacement), 0.1577361226180613, rel_tol=0, abs_tol=1e-9),
        f"E05: displacement magnitude is {abs(displacement)!r}, expected 0.157736",
    )
    require(
        math.isclose(advantage(learned), 0.13407570422535212, rel_tol=0, abs_tol=1e-9),
        f"E05: objective advantage at the learned crossing is {advantage(learned)!r}, expected ~0.134076",
    )

    path = DATA_DIR / "e05_displacement.csv"
    write_rows(path, list(out[0].keys()), out)
    return path, provenance_record(
        output=path,
        experiment="E05",
        sources=[source_ref(crossings_path)],
        selector={"architecture": "flat_2k"},
        fields=["transition_bf", "ci_low", "ci_high", "analytic_threshold_bf"],
        transformation=["closed_form_analytic", "rounding_for_display"],
        notes=(
            "Displacement between the learned behavioural crossing and the exact objective crossover, "
            "and the objective authenticity advantage still available at the learned crossing, both "
            "evaluated in closed form from the frozen crossing. Conditional on the point crossing; "
            "the advantage figure carries no separately tabulated uncertainty."
        ),
    )


def extract_all() -> tuple[list[Path], list[dict[str, object]]]:
    paths: list[Path] = []
    records: list[dict[str, object]] = []

    for path, record in (extract_e01(), extract_e02(), extract_e02_arms()):
        paths.append(path)
        records.append(record)

    e03_path, e03_record = extract_e03()
    paths.append(e03_path)
    records.append(e03_record)
    e03_sum_path, e03_sum_record = extract_e03_summary(e03_path)
    paths.append(e03_sum_path)
    records.append(e03_sum_record)

    for path, record in (extract_e04_curves(), extract_e04_effects(), extract_e05_response()):
        paths.append(path)
        records.append(record)

    e05_path, e05_record = extract_e05_crossings()
    paths.append(e05_path)
    records.append(e05_record)
    e05_disp_path, e05_disp_record = extract_e05_displacement(e05_path)
    paths.append(e05_disp_path)
    records.append(e05_disp_record)

    return paths, records
