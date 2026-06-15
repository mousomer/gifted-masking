from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from gifted_masking.core import final_window_size, summarize_mean
from gifted_masking.models import m0, m1, m2, m3, m4
from gifted_masking.repro import build_manifest, ensure_results_dirs, write_csv, write_json


MASTER_SEED = 0
BOOTSTRAP_SEED = 7001
RUN_COMMAND = "python -m gifted_masking.cli robustness --suite {suite}"

RAW_FIELDNAMES = [
    "run_id",
    "suite",
    "model",
    "experiment",
    "formulation",
    "headline_effect_name",
    "condition_label",
    "master_seed",
    "cell_seed",
    "child_seed",
    "unit_id",
    "replicate_id",
    "parameter_cell_id",
    "p",
    "r",
    "lambda",
    "alpha",
    "tau",
    "q0",
    "gamma",
    "eta",
    "K",
    "p_good",
    "p_bad",
    "bf",
    "p0",
    "ka",
    "kr",
    "km",
    "T",
    "final_window_fraction",
    "final_window_start",
    "final_window_end",
    "mean_mask_rate_final",
    "mean_disclosure_final",
    "auth_lock",
    "mask_lock",
    "mixed",
    "modal_group",
    "modal_behavior",
    "settled_good_pond_auth",
    "final_receptivity",
    "path_direction",
    "path_gap_component",
    "reward_mean_final",
    "regret_if_available",
    "m2_neutral_mask_count_final",
    "m2_neutral_auth_count_final",
    "m2_accepted_mask_count_final",
    "m2_accepted_auth_count_final",
    "m2_stigmatized_mask_count_final",
    "m2_stigmatized_auth_count_final",
    "m2_neutral_visit_count_final",
    "m2_accepted_visit_count_final",
    "m2_stigmatized_visit_count_final",
    "m2_final_state",
    "m2_final_window_reward_mean_objective",
]


@dataclass(frozen=True)
class CheckResult:
    suite: str
    model: str
    check_name: str
    estimate: float
    standard_error: float
    ci_low: float
    ci_high: float
    passed: bool
    notes: str


@dataclass(frozen=True)
class EffectSpec:
    suite: str
    model: str
    check_name: str
    metric: str
    condition_a: str
    condition_b: str
    pass_threshold: float | None
    robust_direction: str
    notes: str


EFFECT_SPECS = [
    EffectSpec("smoke", "M0", "higher_receptivity_reduces_masking", "mean_mask_rate_final", "p_0.20", "p_0.85", 0.15, "positive", "Compare p=0.20 against p=0.85 under default payoffs."),
    EffectSpec("smoke", "M0", "higher_loss_aversion_increases_masking", "mean_mask_rate_final", "lam_2.50", "lam_0.50", 0.05, "positive", "Compare lam=2.5 against lam=0.5 at p=0.65."),
    EffectSpec("smoke", "M1", "higher_receptivity_increases_disclosure", "mean_disclosure_final", "p_0.85", "p_0.20", 0.10, "positive", "Compare mean disclosure at p=0.85 against p=0.20."),
    EffectSpec("smoke", "M2", "higher_escape_rate_reduces_masking", "mean_mask_rate_final", "eta_0.00", "eta_0.20", 0.02, "positive", "Compare eta=0.0 against eta=0.2 at p=0.55."),
    EffectSpec("smoke", "M3", "more_contexts_reduce_settling_in_good_pond", "settled_good_pond_auth", "K_1", "K_8", 0.05, "positive", "Compare K=1 against K=8 in the 2K-arm formulation."),
    EffectSpec("smoke", "M3", "higher_bflpe_cost_reduces_good_pond_authenticity", "settled_good_pond_auth", "bf_0.00", "bf_0.80", 0.05, "positive", "Compare modal good-pond authenticity at bf=0.0 against bf=0.8."),
    EffectSpec("smoke", "M4", "higher_entrenchment_increases_masking", "mean_mask_rate_final", "km_0.003", "km_0.000", 0.05, "positive", "Compare km=0.003 against km=0.0 at p0=0.45."),
    EffectSpec("m3_ablation", "M3", "flat_2k_k1_vs_k8_settling_gap", "settled_good_pond_auth", "K_1", "K_8", None, "positive", "Ablation formulation=flat_2k; positive values mean settling in the good pond drops as K increases."),
    EffectSpec("m3_ablation", "M3", "hierarchical_k1_vs_k8_settling_gap", "settled_good_pond_auth", "K_1", "K_8", None, "positive", "Ablation formulation=hierarchical; positive values mean settling in the good pond drops as K increases."),
    EffectSpec("m3_ablation", "M3", "global_mask_k1_vs_k8_settling_gap", "settled_good_pond_auth", "K_1", "K_8", None, "positive", "Ablation formulation=global_mask; positive values mean settling in the good pond drops as K increases."),
    EffectSpec("m3_ablation", "M3", "fixed_good_pond_k1_vs_k8_settling_gap", "settled_good_pond_auth", "K_1", "K_8", None, "positive", "Ablation formulation=fixed_good_pond; positive values mean settling in the good pond drops as K increases."),
    EffectSpec("m4_hysteresis", "M4", "mask_path_gap", "mean_mask_rate_final", "down", "up", None, "positive", "Difference between descending-km and ascending-km masking paths at matched km values."),
    EffectSpec("m4_hysteresis", "M4", "receptivity_path_gap", "final_receptivity", "down", "up", None, "negative", "Difference between descending-km and ascending-km receptivity paths at matched km values."),
]


def _blank_row(run_id: str, suite: str, model: str, experiment: str, effect: str, condition: str) -> dict[str, object]:
    row = {key: "" for key in RAW_FIELDNAMES}
    row.update(
        {
            "run_id": run_id,
            "suite": suite,
            "model": model,
            "experiment": experiment,
            "headline_effect_name": effect,
            "condition_label": condition,
            "master_seed": MASTER_SEED,
            "replicate_id": 0,
        }
    )
    return row


def _add_common_run_fields(row: dict[str, object], *, n: int, horizon: int, final_window_fraction: float) -> None:
    window = final_window_size(horizon, final_window_fraction)
    row["T"] = horizon
    row["final_window_fraction"] = final_window_fraction
    row["final_window_start"] = horizon - window
    row["final_window_end"] = horizon


def _unit_rows_for_values(
    *,
    run_id: str,
    suite: str,
    model: str,
    experiment: str,
    formulation: str,
    effect: str,
    condition: str,
    values: np.ndarray,
    metric: str,
    cell_seed: int,
    params: dict[str, object],
    horizon: int,
    final_window_fraction: float = 0.2,
    extra_by_unit: list[dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    rows = []
    for unit_id, value in enumerate(values):
        row = _blank_row(run_id, suite, model, experiment, effect, condition)
        row["formulation"] = formulation
        row["cell_seed"] = cell_seed
        row["child_seed"] = f"{cell_seed}:{unit_id}"
        row["unit_id"] = unit_id
        row["parameter_cell_id"] = condition
        row[metric] = float(value)
        for key, param_value in params.items():
            row[key] = param_value
        if extra_by_unit is not None:
            row.update(extra_by_unit[unit_id])
        _add_common_run_fields(row, n=len(values), horizon=horizon, final_window_fraction=final_window_fraction)
        rows.append(row)
    return rows


def _append_pair(
    rows: list[dict[str, object]],
    *,
    run_id: str,
    spec: EffectSpec,
    experiment: str,
    formulation: str,
    condition_a: str,
    values_a: np.ndarray,
    seed_a: int,
    params_a: dict[str, object],
    extra_a: list[dict[str, object]] | None = None,
    condition_b: str,
    values_b: np.ndarray,
    seed_b: int,
    params_b: dict[str, object],
    extra_b: list[dict[str, object]] | None = None,
    horizon: int,
    final_window_fraction: float = 0.2,
) -> None:
    rows.extend(
        _unit_rows_for_values(
            run_id=run_id,
            suite=spec.suite,
            model=spec.model,
            experiment=experiment,
            formulation=formulation,
            effect=spec.check_name,
            condition=condition_a,
            values=values_a,
            metric=spec.metric,
            cell_seed=seed_a,
            params=params_a,
            horizon=horizon,
            final_window_fraction=final_window_fraction,
            extra_by_unit=extra_a,
        )
    )
    rows.extend(
        _unit_rows_for_values(
            run_id=run_id,
            suite=spec.suite,
            model=spec.model,
            experiment=experiment,
            formulation=formulation,
            effect=spec.check_name,
            condition=condition_b,
            values=values_b,
            metric=spec.metric,
            cell_seed=seed_b,
            params=params_b,
            horizon=horizon,
            final_window_fraction=final_window_fraction,
            extra_by_unit=extra_b,
        )
    )


def _m2_extra_by_unit(diagnostics: dict[str, np.ndarray]) -> list[dict[str, object]]:
    state_action_counts = diagnostics["state_action_counts_final"]
    state_visit_counts = diagnostics["state_visit_counts_final"]
    final_state = diagnostics["final_state"]
    reward_mean = diagnostics["reward_mean_final"]
    extras = []
    for unit_id in range(state_action_counts.shape[0]):
        extras.append(
            {
                "m2_neutral_mask_count_final": int(state_action_counts[unit_id, m2.STATE_NEUTRAL, 0]),
                "m2_neutral_auth_count_final": int(state_action_counts[unit_id, m2.STATE_NEUTRAL, 1]),
                "m2_accepted_mask_count_final": int(state_action_counts[unit_id, m2.STATE_ACCEPTED, 0]),
                "m2_accepted_auth_count_final": int(state_action_counts[unit_id, m2.STATE_ACCEPTED, 1]),
                "m2_stigmatized_mask_count_final": int(state_action_counts[unit_id, m2.STATE_STIGMATIZED, 0]),
                "m2_stigmatized_auth_count_final": int(state_action_counts[unit_id, m2.STATE_STIGMATIZED, 1]),
                "m2_neutral_visit_count_final": int(state_visit_counts[unit_id, m2.STATE_NEUTRAL]),
                "m2_accepted_visit_count_final": int(state_visit_counts[unit_id, m2.STATE_ACCEPTED]),
                "m2_stigmatized_visit_count_final": int(state_visit_counts[unit_id, m2.STATE_STIGMATIZED]),
                "m2_final_state": int(final_state[unit_id]),
                "m2_final_window_reward_mean_objective": float(reward_mean[unit_id]),
            }
        )
    return extras


def generate_unit_rows(run_id: str = "robustness_full", suite: str = "full") -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    specs = {spec.check_name: spec for spec in EFFECT_SPECS}

    low_p = m0.simulate(0.20, n=250, horizon=900, seed=11)
    high_p = m0.simulate(0.85, n=250, horizon=900, seed=12)
    _append_pair(
        rows,
        run_id=run_id,
        spec=specs["higher_receptivity_reduces_masking"],
        experiment="receptivity_contrast",
        formulation="two_arm_bandit",
        condition_a="p_0.20",
        values_a=low_p,
        seed_a=11,
        params_a={"p": 0.20, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0},
        condition_b="p_0.85",
        values_b=high_p,
        seed_b=12,
        params_b={"p": 0.85, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0},
        horizon=900,
    )

    low_lambda = m0.simulate(0.65, lam=0.5, n=250, horizon=900, seed=13)
    high_lambda = m0.simulate(0.65, lam=2.5, n=250, horizon=900, seed=14)
    _append_pair(
        rows,
        run_id=run_id,
        spec=specs["higher_loss_aversion_increases_masking"],
        experiment="loss_aversion_contrast",
        formulation="two_arm_bandit",
        condition_a="lam_2.50",
        values_a=high_lambda,
        seed_a=14,
        params_a={"p": 0.65, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 2.5, "q0": 0.0},
        condition_b="lam_0.50",
        values_b=low_lambda,
        seed_b=13,
        params_b={"p": 0.65, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 0.5, "q0": 0.0},
        horizon=900,
    )

    low_disclosure = m1.simulate(0.20, levels=5, n=250, horizon=900, seed=15)
    high_disclosure = m1.simulate(0.85, levels=5, n=250, horizon=900, seed=16)
    _append_pair(
        rows,
        run_id=run_id,
        spec=specs["higher_receptivity_increases_disclosure"],
        experiment="graded_disclosure_receptivity_contrast",
        formulation="independent_disclosure_levels",
        condition_a="p_0.85",
        values_a=high_disclosure,
        seed_a=16,
        params_a={"p": 0.85, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0},
        condition_b="p_0.20",
        values_b=low_disclosure,
        seed_b=15,
        params_b={"p": 0.20, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0},
        horizon=900,
    )

    low_eta_diag = m2.simulate_with_diagnostics(0.55, 0.0, n=200, horizon=1200, seed=17)
    high_eta_diag = m2.simulate_with_diagnostics(0.55, 0.2, n=200, horizon=1200, seed=18)
    low_eta = low_eta_diag["mask_rate_final"]
    high_eta = high_eta_diag["mask_rate_final"]
    _append_pair(
        rows,
        run_id=run_id,
        spec=specs["higher_escape_rate_reduces_masking"],
        experiment="stigma_escape_contrast",
        formulation="three_state_mdp",
        condition_a="eta_0.00",
        values_a=low_eta,
        seed_a=17,
        params_a={"p": 0.55, "eta": 0.0, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0, "gamma": 0.9},
        extra_a=_m2_extra_by_unit(low_eta_diag),
        condition_b="eta_0.20",
        values_b=high_eta,
        seed_b=18,
        params_b={"p": 0.55, "eta": 0.2, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0, "gamma": 0.9},
        extra_b=_m2_extra_by_unit(high_eta_diag),
        horizon=1200,
    )

    settle_k1 = m3.simulate(1, n=220, horizon=1200, seed=19)[0].astype(float)
    settle_k8 = m3.simulate(8, n=220, horizon=1200, seed=20)[0].astype(float)
    _append_pair(
        rows,
        run_id=run_id,
        spec=specs["more_contexts_reduce_settling_in_good_pond"],
        experiment="context_count_contrast",
        formulation="flat_2k",
        condition_a="K_1",
        values_a=settle_k1,
        seed_a=19,
        params_a={"K": 1, "p_good": 0.85, "p_bad": 0.2, "bf": 0.0, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0},
        condition_b="K_8",
        values_b=settle_k8,
        seed_b=20,
        params_b={"K": 8, "p_good": 0.85, "p_bad": 0.2, "bf": 0.0, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0},
        horizon=1200,
    )

    low_bf = (m3.simulate(4, bf=0.0, n=220, horizon=1200, seed=21)[2] == 1).astype(float)
    high_bf = (m3.simulate(4, bf=0.8, n=220, horizon=1200, seed=22)[2] == 1).astype(float)
    _append_pair(
        rows,
        run_id=run_id,
        spec=specs["higher_bflpe_cost_reduces_good_pond_authenticity"],
        experiment="bflpe_cost_contrast",
        formulation="flat_2k",
        condition_a="bf_0.00",
        values_a=low_bf,
        seed_a=21,
        params_a={"K": 4, "p_good": 0.85, "p_bad": 0.2, "bf": 0.0, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0},
        condition_b="bf_0.80",
        values_b=high_bf,
        seed_b=22,
        params_b={"K": 4, "p_good": 0.85, "p_bad": 0.2, "bf": 0.8, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0},
        horizon=1200,
    )

    low_km = m4.simulate(0.45, 0.0, n=220, horizon=1200, seed=23)[0]
    high_km = m4.simulate(0.45, 0.003, n=220, horizon=1200, seed=24)[0]
    _append_pair(
        rows,
        run_id=run_id,
        spec=specs["higher_entrenchment_increases_masking"],
        experiment="entrenchment_contrast",
        formulation="endogenous_bandit",
        condition_a="km_0.003",
        values_a=high_km,
        seed_a=24,
        params_a={"p0": 0.45, "ka": 0.12, "kr": 0.04, "km": 0.003, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0},
        condition_b="km_0.000",
        values_b=low_km,
        seed_b=23,
        params_b={"p0": 0.45, "ka": 0.12, "kr": 0.04, "km": 0.0, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0},
        horizon=1200,
    )

    m3_runners = {
        "flat_2k": lambda k, seed: m3.simulate(k, n=220, horizon=1200, seed=seed)[0].astype(float),
        "hierarchical": lambda k, seed: m3.simulate_hierarchical(k, n=220, horizon=1200, seed=seed)[0].astype(float),
        "global_mask": lambda k, seed: m3.simulate_global_mask(k, n=220, horizon=1200, seed=seed)[0].astype(float),
        "fixed_good_pond": lambda k, seed: m3.simulate_fixed_good_pond(n=220, horizon=1200, seed=seed)[0].astype(float),
    }
    for formulation, runner in m3_runners.items():
        effect_name = f"{formulation}_k1_vs_k8_settling_gap"
        k1 = runner(1, 301)
        k8 = runner(8, 308)
        _append_pair(
            rows,
            run_id=run_id,
            spec=specs[effect_name],
            experiment="m3_action_space_ablation",
            formulation=formulation,
            condition_a="K_1",
            values_a=k1,
            seed_a=301,
            params_a={"K": 1, "p_good": 0.85, "p_bad": 0.2, "bf": 0.0, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0},
            condition_b="K_8",
            values_b=k8,
            seed_b=308,
            params_b={"K": 8, "p_good": 0.85, "p_bad": 0.2, "bf": 0.0, "r": 2.0, "alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0},
            horizon=1200,
        )

    km_values = np.linspace(0.0, 0.003, 7)
    experiment = m4.hysteresis_experiment(0.45, km_values, n=220, horizon=500, seed=500)
    for effect_name, metric, up_values, down_values in [
        ("mask_path_gap", "mean_mask_rate_final", experiment["mask_up"], experiment["mask_down"][::-1]),
        ("receptivity_path_gap", "final_receptivity", experiment["p_up"], experiment["p_down"][::-1]),
    ]:
        spec = specs[effect_name]
        for direction, values in [("up", up_values), ("down", down_values)]:
            for unit_id, value in enumerate(values):
                row = _blank_row(run_id, spec.suite, spec.model, "km_ramp_path", effect_name, direction)
                row["formulation"] = "endogenous_bandit_ramp"
                row["cell_seed"] = 500 + unit_id + (7 if direction == "down" else 0)
                row["child_seed"] = f"ramp:{direction}:{unit_id}"
                row["unit_id"] = unit_id
                row["parameter_cell_id"] = f"km_{km_values[unit_id]:.4f}_{direction}"
                row["path_direction"] = direction
                row["path_gap_component"] = metric
                row[metric] = float(value)
                row["p0"] = 0.45
                row["ka"] = 0.12
                row["kr"] = 0.04
                row["km"] = float(km_values[unit_id])
                row["r"] = 2.0
                row["alpha"] = 0.1
                row["tau"] = 0.25
                row["lambda"] = 1.0
                row["q0"] = 0.0
                _add_common_run_fields(row, n=7, horizon=500, final_window_fraction=0.2)
                rows.append(row)

    if suite == "smoke":
        return [row for row in rows if row["suite"] == "smoke"]
    if suite == "full":
        return rows
    raise ValueError(f"unknown suite: {suite}")


def _values_for_effect(rows: list[dict[str, object]], spec: EffectSpec) -> np.ndarray:
    relevant = [row for row in rows if row["headline_effect_name"] == spec.check_name]
    by_condition: dict[str, dict[str, float]] = {}
    for row in relevant:
        condition = str(row["condition_label"])
        unit_id = str(row["unit_id"])
        value = row.get(spec.metric, "")
        if value == "":
            continue
        by_condition.setdefault(condition, {})[unit_id] = float(value)
    left = by_condition.get(spec.condition_a, {})
    right = by_condition.get(spec.condition_b, {})
    units = sorted(set(left).intersection(right), key=lambda item: int(item) if item.isdigit() else item)
    if not units:
        raise ValueError(f"No matched units for {spec.check_name}")
    return np.asarray([left[unit] - right[unit] for unit in units], dtype=float)


def summarize_unit_rows(rows: list[dict[str, object]], suite: str = "full") -> list[CheckResult]:
    allowed = {"smoke"} if suite == "smoke" else {"smoke", "m3_ablation", "m4_hysteresis"}
    results: list[CheckResult] = []
    for spec in EFFECT_SPECS:
        if spec.suite not in allowed:
            continue
        values = _values_for_effect(rows, spec)
        summary = summarize_mean(values, seed=BOOTSTRAP_SEED)
        if spec.pass_threshold is None:
            passed = True
        elif spec.robust_direction == "positive":
            passed = summary.estimate > spec.pass_threshold
        elif spec.robust_direction == "negative":
            passed = summary.estimate < -spec.pass_threshold
        else:
            passed = True
        results.append(
            CheckResult(
                suite=spec.suite,
                model=spec.model,
                check_name=spec.check_name,
                estimate=summary.estimate,
                standard_error=summary.standard_error,
                ci_low=summary.ci_low,
                ci_high=summary.ci_high,
                passed=passed,
                notes=spec.notes,
            )
        )
    return results


def run_smoke_suite() -> list[CheckResult]:
    return summarize_unit_rows(generate_unit_rows(run_id="robustness_smoke", suite="smoke"), suite="smoke")


def run_m3_ablation_suite() -> list[CheckResult]:
    rows = generate_unit_rows(run_id="robustness_full", suite="full")
    return [result for result in summarize_unit_rows(rows, suite="full") if result.suite == "m3_ablation"]


def run_m4_hysteresis_suite() -> list[CheckResult]:
    rows = generate_unit_rows(run_id="robustness_full", suite="full")
    return [result for result in summarize_unit_rows(rows, suite="full") if result.suite == "m4_hysteresis"]


def _result_rows(results: list[CheckResult]) -> list[dict[str, object]]:
    return [
        {
            "suite": result.suite,
            "model": result.model,
            "check_name": result.check_name,
            "estimate": result.estimate,
            "standard_error": result.standard_error,
            "ci_low": result.ci_low,
            "ci_high": result.ci_high,
            "passed": result.passed,
            "notes": result.notes,
        }
        for result in results
    ]


def _code_config_hash(rows: list[dict[str, object]]) -> str:
    joined = "\n".join(
        f"{row['headline_effect_name']}|{row['condition_label']}|{row['unit_id']}|{row['cell_seed']}"
        for row in rows
    )
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def _manifest_parameters(suite: str, rows: list[dict[str, object]]) -> dict[str, object]:
    by_effect: dict[str, dict[str, object]] = {}
    for row in rows:
        effect = str(row["headline_effect_name"])
        condition = str(row["condition_label"])
        cell = by_effect.setdefault(effect, {"conditions": {}, "n_units": 0})
        cell["conditions"].setdefault(
            condition,
            {
                "cell_seed": row["cell_seed"],
                "T": row["T"],
                "final_window_fraction": row["final_window_fraction"],
                "parameters": {
                    key: row[key]
                    for key in ["p", "r", "lambda", "alpha", "tau", "q0", "gamma", "eta", "K", "p_good", "p_bad", "bf", "p0", "ka", "kr", "km"]
                    if row.get(key, "") != ""
                },
            },
        )
        cell["n_units"] = int(cell["n_units"]) + 1
    return {
        "suite": suite,
        "checks": len([spec for spec in EFFECT_SPECS if suite == "full" or spec.suite == "smoke"]),
        "master_seed": MASTER_SEED,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "seed_strategy": "Fixed deterministic cell seeds are recorded per condition; child_seed is '<cell_seed>:<unit_id>' for child-level units and 'ramp:<direction>:<unit_id>' for M4 ramp units.",
        "rng_stream_strategy": "Each condition calls a model simulation with its own local np.random.default_rng(cell_seed); no global RNG state is used.",
        "parameter_grids": by_effect,
        "n_per_cell": {
            effect: {
                condition: len([row for row in rows if row["headline_effect_name"] == effect and row["condition_label"] == condition])
                for condition in sorted({str(row["condition_label"]) for row in rows if row["headline_effect_name"] == effect})
            }
            for effect in sorted({str(row["headline_effect_name"]) for row in rows})
        },
        "T": {
            effect: sorted({int(row["T"]) for row in rows if row["headline_effect_name"] == effect})
            for effect in sorted({str(row["headline_effect_name"]) for row in rows})
        },
        "final_window_fraction": {
            effect: sorted({float(row["final_window_fraction"]) for row in rows if row["headline_effect_name"] == effect})
            for effect in sorted({str(row["headline_effect_name"]) for row in rows})
        },
        "code_config_hash": _code_config_hash(rows),
    }


def write_suite(output_dir: Path, suite: str = "full") -> dict[str, str]:
    output_dir = Path(output_dir)
    paths = ensure_results_dirs(output_dir)
    if suite not in {"smoke", "full"}:
        raise ValueError(f"unknown suite: {suite}")

    run_id = "robustness_smoke" if suite == "smoke" else "robustness_full"
    unit_rows = generate_unit_rows(run_id=run_id, suite=suite)
    results = summarize_unit_rows(unit_rows, suite=suite)
    rows = _result_rows(results)

    raw_path = paths["raw"] / f"{run_id}.csv"
    units_path = paths["raw"] / f"{run_id}_units.csv"
    summary_path = paths["summaries"] / f"{run_id}_summary.csv"
    report_path = paths["reports"] / f"{run_id}_report.md"
    manifest_path = paths["manifests"] / f"{run_id}.json"

    write_csv(raw_path, rows)
    write_csv(units_path, unit_rows)
    write_csv(summary_path, rows)

    report_lines = [
        f"# Robustness Report: {suite}",
        "",
        "| Suite | Model | Check | Estimate | Passed |",
        "| --- | --- | --- | ---: | :---: |",
    ]
    for row in rows:
        report_lines.append(
            f"| {row['suite']} | {row['model']} | {row['check_name']} | {row['estimate']:.4f} | {'yes' if row['passed'] else 'no'} |"
        )
    report_path.write_text("\n".join(report_lines) + "\n")

    repo_root = Path(__file__).resolve().parents[3]
    manifest = build_manifest(
        repo_root=repo_root,
        run_id=run_id,
        command=RUN_COMMAND.format(suite=suite),
        parameters=_manifest_parameters(suite, unit_rows),
        output_paths={
            "primary_raw": str(units_path),
            "raw_legacy_or_summary": str(raw_path),
            "summary": str(summary_path),
            "report": str(report_path),
        },
        verification={
            "status": "generated",
            "test_count": None,
            "command": "./scripts/verify.sh",
            "runtime_seconds": None,
        },
    )
    write_json(manifest_path, manifest)

    return {
        "raw": str(raw_path),
        "primary_raw": str(units_path),
        "summary": str(summary_path),
        "report": str(report_path),
        "manifest": str(manifest_path),
    }
