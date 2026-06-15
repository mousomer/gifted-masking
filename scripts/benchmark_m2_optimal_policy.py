from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from gifted_masking.analysis.m2_optimal import (  # noqa: E402
    ACTION_NAMES,
    M2Params,
    STATE_NAMES,
    evaluate_policy_value,
    policy_from_mask_probabilities,
    solve_m2_value_iteration,
    static_m0_comparator,
)
from gifted_masking.repro import ensure_results_dirs, write_csv  # noqa: E402


OUTPUT_COLUMNS = [
    "run_id",
    "case",
    "p",
    "eta",
    "b",
    "a",
    "c",
    "r",
    "b2",
    "r2",
    "delta",
    "gamma",
    "lambda",
    "reward_mode",
    "transition_ordering",
    "static_m0_E_mask",
    "static_m0_E_auth",
    "static_m0_auth_advantage",
    "static_m0_optimal_action",
    "m2_optimal_action_neutral",
    "m2_optimal_action_accepted",
    "m2_optimal_action_stigmatized",
    "m2_optimal_actions_neutral_all",
    "m2_V_neutral",
    "m2_V_accepted",
    "m2_V_stigmatized",
    "m2_Q_neutral_mask",
    "m2_Q_neutral_authentic",
    "m2_Q_accepted_mask",
    "m2_Q_accepted_authentic",
    "m2_Q_stigmatized_mask",
    "m2_Q_stigmatized_authentic",
    "bellman_residual",
    "iterations",
    "converged",
    "learned_mean_mask_rate_final",
    "learned_neutral_mask_probability",
    "learned_accepted_mask_probability",
    "learned_stigmatized_mask_probability",
    "learned_policy_value_neutral",
    "regret_neutral",
    "regret_available",
    "interpretation",
    "target_p",
    "target_eta",
    "cell_source",
]


BENCHMARK_CASES = [
    ("target_low_p_low_eta", 0.20, 0.00, 0.20, 0.00, "explicit_target_no_empirical_policy"),
    ("target_mid_p_low_eta", 0.60, 0.00, 0.60, 0.00, "explicit_target_no_empirical_policy"),
    ("target_mid_p_high_eta", 0.60, 0.20, 0.60, 0.20, "explicit_target_no_empirical_policy"),
    ("target_high_p_low_eta", 0.85, 0.00, 0.85, 0.00, "explicit_target_no_empirical_policy"),
    ("target_high_p_high_eta", 0.85, 0.20, 0.85, 0.20, "explicit_target_no_empirical_policy"),
    ("robustness_higher_escape_eta_0.00", 0.55, 0.00, 0.55, 0.00, "robustness_full_units"),
    ("robustness_higher_escape_eta_0.20", 0.55, 0.20, 0.55, 0.20, "robustness_full_units"),
]


def _load_empirical_policies(primary_raw: Path) -> dict[tuple[float, float], dict[str, float]]:
    if not primary_raw.exists():
        return {}
    grouped: dict[tuple[float, float], dict[str, float]] = {}
    with primary_raw.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("model") != "M2":
                continue
            key = (float(row["p"]), float(row["eta"]))
            cell = grouped.setdefault(
                key,
                {
                    "mask_rate_sum": 0.0,
                    "n": 0.0,
                    "neutral_mask": 0.0,
                    "neutral_visit": 0.0,
                    "accepted_mask": 0.0,
                    "accepted_visit": 0.0,
                    "stigmatized_mask": 0.0,
                    "stigmatized_visit": 0.0,
                },
            )
            cell["mask_rate_sum"] += float(row["mean_mask_rate_final"])
            cell["n"] += 1.0
            cell["neutral_mask"] += float(row.get("m2_neutral_mask_count_final") or 0.0)
            cell["neutral_visit"] += float(row.get("m2_neutral_visit_count_final") or 0.0)
            cell["accepted_mask"] += float(row.get("m2_accepted_mask_count_final") or 0.0)
            cell["accepted_visit"] += float(row.get("m2_accepted_visit_count_final") or 0.0)
            cell["stigmatized_mask"] += float(row.get("m2_stigmatized_mask_count_final") or 0.0)
            cell["stigmatized_visit"] += float(row.get("m2_stigmatized_visit_count_final") or 0.0)
    return grouped


def _mask_probability(cell: dict[str, float], state: str) -> float | None:
    visits = cell[f"{state}_visit"]
    if visits <= 0:
        return None
    return cell[f"{state}_mask"] / visits


def _format(value: object) -> object:
    if isinstance(value, float):
        return f"{value:.12g}"
    return value


def _row_for_case(case: tuple[str, float, float, float, float, str], empirical: dict[tuple[float, float], dict[str, float]]) -> dict[str, object]:
    case_name, p, eta, target_p, target_eta, source = case
    params = M2Params(p=p, eta=eta)
    solution = solve_m2_value_iteration(params, reward_mode="objective")
    static = static_m0_comparator(params)
    q_values = solution["Q"]
    values = solution["V"]
    chosen = solution["chosen_actions"]
    optimal_all = solution["optimal_actions_all"]
    cell = empirical.get((p, eta))
    learned_mask = [None, None, None]
    learned_value = None
    regret = None
    regret_available = False
    if cell is not None:
        learned_mask = [
            _mask_probability(cell, "neutral"),
            _mask_probability(cell, "accepted"),
            _mask_probability(cell, "stigmatized"),
        ]
        if all(value is not None for value in learned_mask):
            policy = policy_from_mask_probabilities(float(value) for value in learned_mask if value is not None)
            policy_values = evaluate_policy_value(params, policy)
            learned_value = float(policy_values[0])
            regret = float(values[0] - learned_value)
            regret_available = True

    if len(optimal_all["neutral"]) > 1:
        interpretation = "inconclusive_due_to_tie"
    elif not regret_available:
        interpretation = "inconclusive_due_to_missing_empirical_policy"
    else:
        learned_neutral_action = "mask" if float(learned_mask[0]) >= 0.5 else "authentic"
        interpretation = "learned_matches_m2_optimal" if learned_neutral_action == chosen["neutral"] else "learned_suboptimal_vs_m2"
    if interpretation == "inconclusive_due_to_missing_empirical_policy" and static["optimal_action"] != chosen["neutral"]:
        interpretation = "stigma_changes_static_optimum"

    row = {
        "run_id": "m2_optimal_policy_benchmark",
        "case": case_name,
        "p": params.p,
        "eta": params.eta,
        "b": params.b,
        "a": params.a,
        "c": params.c,
        "r": params.r,
        "b2": params.b2,
        "r2": params.r2,
        "delta": params.delta,
        "gamma": solution["gamma"],
        "lambda": params.lam,
        "reward_mode": solution["reward_mode"],
        "transition_ordering": solution["transition_ordering"],
        "static_m0_E_mask": static["E_mask"],
        "static_m0_E_auth": static["E_auth"],
        "static_m0_auth_advantage": static["auth_advantage"],
        "static_m0_optimal_action": static["optimal_action"],
        "m2_optimal_action_neutral": chosen["neutral"],
        "m2_optimal_action_accepted": chosen["accepted"],
        "m2_optimal_action_stigmatized": chosen["stigmatized"],
        "m2_optimal_actions_neutral_all": ";".join(optimal_all["neutral"]),
        "m2_V_neutral": float(values[0]),
        "m2_V_accepted": float(values[1]),
        "m2_V_stigmatized": float(values[2]),
        "m2_Q_neutral_mask": float(q_values[0, 0]),
        "m2_Q_neutral_authentic": float(q_values[0, 1]),
        "m2_Q_accepted_mask": float(q_values[1, 0]),
        "m2_Q_accepted_authentic": float(q_values[1, 1]),
        "m2_Q_stigmatized_mask": float(q_values[2, 0]),
        "m2_Q_stigmatized_authentic": float(q_values[2, 1]),
        "bellman_residual": float(solution["residual"]),
        "iterations": solution["iterations"],
        "converged": solution["converged"],
        "learned_mean_mask_rate_final": "" if cell is None else cell["mask_rate_sum"] / cell["n"],
        "learned_neutral_mask_probability": "" if learned_mask[0] is None else float(learned_mask[0]),
        "learned_accepted_mask_probability": "" if learned_mask[1] is None else float(learned_mask[1]),
        "learned_stigmatized_mask_probability": "" if learned_mask[2] is None else float(learned_mask[2]),
        "learned_policy_value_neutral": "" if learned_value is None else learned_value,
        "regret_neutral": "" if regret is None else regret,
        "regret_available": regret_available,
        "interpretation": interpretation,
        "target_p": target_p,
        "target_eta": target_eta,
        "cell_source": source,
    }
    return {key: _format(row[key]) for key in OUTPUT_COLUMNS}


def main() -> int:
    paths = ensure_results_dirs(ROOT / "results")
    empirical = _load_empirical_policies(paths["raw"] / "robustness_full_units.csv")
    rows = [_row_for_case(case, empirical) for case in BENCHMARK_CASES]
    output_path = paths["summaries"] / "m2_optimal_policy_benchmark.csv"
    write_csv(output_path, rows)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
