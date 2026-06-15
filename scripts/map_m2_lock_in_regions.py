from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from gifted_masking.analysis.m2_optimal import M2Params, classify_m2_cell  # noqa: E402
from gifted_masking.models import m2  # noqa: E402
from gifted_masking.repro import ensure_results_dirs, write_csv  # noqa: E402


P_VALUES = [step / 100.0 for step in range(0, 101, 5)]
ETA_VALUES = [step / 100.0 for step in range(0, 81, 5)]
SIMULATION_CONFIG = {
    "n": 160,
    "horizon": 1000,
    "alpha": 0.1,
    "temp": 0.25,
    "lam": 1.0,
    "q0": 0.0,
    "gamma": 0.9,
    "seed_base": 9100,
    "final_window_fraction": 0.2,
}

CELL_COLUMNS = [
    "run_id",
    "p",
    "eta",
    "n",
    "horizon",
    "seed",
    "static_m0_optimal_action",
    "static_m0_auth_advantage",
    "m2_optimal_action_neutral",
    "m2_optimal_action_accepted",
    "m2_optimal_action_stigmatized",
    "m2_q_gap_neutral_auth_minus_mask",
    "m2_v_neutral",
    "bellman_residual",
    "iterations",
    "converged",
    "learned_neutral_action",
    "learned_neutral_mask_probability",
    "learned_accepted_mask_probability",
    "learned_stigmatized_mask_probability",
    "learned_mean_mask_rate_final",
    "learned_mean_reward_final",
    "learned_policy_value_neutral",
    "regret_neutral",
    "regret_available",
    "region",
]

SUMMARY_COLUMNS = [
    "run_id",
    "eta",
    "static_authenticity_threshold_p",
    "dynamic_authenticity_threshold_p",
    "learned_authenticity_threshold_p",
    "optimal_learner_lock_in_p_range",
    "learned_suboptimal_lock_in_p_range",
]


def _format(value: object) -> object:
    if isinstance(value, float):
        return f"{value:.12g}"
    return value


def _first_p(rows: list[dict[str, object]], key: str, value: str) -> str:
    for row in rows:
        if row[key] == value:
            return f"{float(row['p']):.2f}"
    return ""


def _range_for_region(rows: list[dict[str, object]], region: str) -> str:
    matching = [float(row["p"]) for row in rows if row["region"] == region]
    if not matching:
        return ""
    return f"{min(matching):.2f}-{max(matching):.2f}"


def build_rows() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    cell_rows: list[dict[str, object]] = []
    seed_base = int(SIMULATION_CONFIG["seed_base"])
    for eta_index, eta in enumerate(ETA_VALUES):
        for p_index, p in enumerate(P_VALUES):
            seed = seed_base + eta_index * 100 + p_index
            params = M2Params(p=p, eta=eta)
            diagnostics = m2.simulate_with_diagnostics(
                p,
                eta,
                n=int(SIMULATION_CONFIG["n"]),
                horizon=int(SIMULATION_CONFIG["horizon"]),
                alpha=float(SIMULATION_CONFIG["alpha"]),
                temp=float(SIMULATION_CONFIG["temp"]),
                lam=float(SIMULATION_CONFIG["lam"]),
                q0=float(SIMULATION_CONFIG["q0"]),
                gamma=float(SIMULATION_CONFIG["gamma"]),
                seed=seed,
                final_window_fraction=float(SIMULATION_CONFIG["final_window_fraction"]),
            )
            classified = classify_m2_cell(params, diagnostics)
            solution = classified["solution"]
            learned = classified["learned"]
            static = classified["static"]
            mask_probabilities = learned["learned_mask_probabilities"]
            cell_rows.append(
                {
                    "run_id": "m2_lock_in_region_map",
                    "p": p,
                    "eta": eta,
                    "n": SIMULATION_CONFIG["n"],
                    "horizon": SIMULATION_CONFIG["horizon"],
                    "seed": seed,
                    "static_m0_optimal_action": static["optimal_action"],
                    "static_m0_auth_advantage": static["auth_advantage"],
                    "m2_optimal_action_neutral": solution["chosen_actions"]["neutral"],
                    "m2_optimal_action_accepted": solution["chosen_actions"]["accepted"],
                    "m2_optimal_action_stigmatized": solution["chosen_actions"]["stigmatized"],
                    "m2_q_gap_neutral_auth_minus_mask": float(solution["Q"][0, 1] - solution["Q"][0, 0]),
                    "m2_v_neutral": float(solution["V"][0]),
                    "bellman_residual": float(solution["residual"]),
                    "iterations": solution["iterations"],
                    "converged": solution["converged"],
                    "learned_neutral_action": classified["learned_neutral_action"] or "",
                    "learned_neutral_mask_probability": mask_probabilities["neutral"] if mask_probabilities["neutral"] is not None else "",
                    "learned_accepted_mask_probability": mask_probabilities["accepted"] if mask_probabilities["accepted"] is not None else "",
                    "learned_stigmatized_mask_probability": mask_probabilities["stigmatized"] if mask_probabilities["stigmatized"] is not None else "",
                    "learned_mean_mask_rate_final": learned["learned_mean_mask_rate_final"],
                    "learned_mean_reward_final": learned["learned_mean_reward_final"],
                    "learned_policy_value_neutral": "" if classified["learned_policy_value_neutral"] is None else classified["learned_policy_value_neutral"],
                    "regret_neutral": "" if classified["regret_neutral"] is None else classified["regret_neutral"],
                    "regret_available": classified["regret_available"],
                    "region": classified["region"],
                }
            )

    summary_rows: list[dict[str, object]] = []
    for eta in ETA_VALUES:
        rows = [row for row in cell_rows if float(row["eta"]) == eta]
        summary_rows.append(
            {
                "run_id": "m2_lock_in_region_map",
                "eta": eta,
                "static_authenticity_threshold_p": _first_p(rows, "static_m0_optimal_action", "authentic"),
                "dynamic_authenticity_threshold_p": _first_p(rows, "m2_optimal_action_neutral", "authentic"),
                "learned_authenticity_threshold_p": _first_p(rows, "learned_neutral_action", "authentic"),
                "optimal_learner_lock_in_p_range": _range_for_region(rows, "optimal_learner_lock_in"),
                "learned_suboptimal_lock_in_p_range": _range_for_region(rows, "learned_suboptimal_lock_in"),
            }
        )
    return cell_rows, summary_rows


def main() -> int:
    paths = ensure_results_dirs(ROOT / "results")
    cell_rows, summary_rows = build_rows()
    cell_rows = [{key: _format(row[key]) for key in CELL_COLUMNS} for row in cell_rows]
    summary_rows = [{key: _format(row[key]) for key in SUMMARY_COLUMNS} for row in summary_rows]
    cell_path = paths["summaries"] / "m2_lock_in_region_map.csv"
    summary_path = paths["summaries"] / "m2_lock_in_region_thresholds.csv"
    write_csv(cell_path, cell_rows)
    write_csv(summary_path, summary_rows)
    print(cell_path)
    print(summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
