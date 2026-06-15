from __future__ import annotations

import csv
import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "results" / ".matplotlib"))

from gifted_masking.analysis.m2_optimal import (  # noqa: E402
    M2Params,
    classify_m2_cell,
    dynamic_authenticity_threshold,
)
from gifted_masking.models import m2  # noqa: E402
from gifted_masking.repro import ensure_results_dirs, write_csv  # noqa: E402
from scripts import map_m2_lock_in_regions  # noqa: E402


REGION_CODES = {
    "masking_optimal_and_learned_not_proven_suboptimal": 0,
    "dynamic_authenticity_overrides_static_masking": 1,
    "learned_suboptimal_lock_in": 2,
    "authenticity_optimal_or_learned_matches": 3,
    "optimal_learner_lock_in": 4,
}
REGION_LABELS = {
    0: "mask optimal",
    1: "dynamic auth beats static mask",
    2: "learned suboptimal masking",
    3: "auth optimal / learned match",
    4: "optimal-policy masking despite static auth",
}

THRESHOLD_COLUMNS = [
    "run_id",
    "eta",
    "static_authenticity_threshold_p",
    "dynamic_authenticity_threshold_p",
    "optimal_lock_in_width",
    "dynamic_authenticity_before_static_width",
]

LEARNER_COLUMNS = [
    "run_id",
    "learner_case",
    "p",
    "eta",
    "alpha",
    "tau",
    "lambda",
    "q0",
    "gamma",
    "n",
    "horizon",
    "seed",
    "static_m0_optimal_action",
    "m2_optimal_action_neutral",
    "learned_neutral_action",
    "learned_neutral_mask_probability",
    "learned_mean_mask_rate_final",
    "regret_neutral",
    "region",
]

OPTIMAL_SENSITIVITY_COLUMNS = [
    "run_id",
    "gamma",
    "r2",
    "b2",
    "delta",
    "eta",
    "static_authenticity_threshold_p",
    "dynamic_authenticity_threshold_p",
    "optimal_lock_in_width",
    "dynamic_authenticity_before_static_width",
    "regime_note",
]


def _load_pyplot():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import BoundaryNorm, ListedColormap
    from matplotlib.patches import Patch

    return plt, BoundaryNorm, ListedColormap, Patch


def _format(value: object) -> object:
    if isinstance(value, float):
        return f"{value:.12g}"
    return value


def _static_threshold(params: M2Params) -> float:
    return 1.0 - ((params.a + params.c) / (params.b + params.r))


def build_refined_threshold_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for eta in map_m2_lock_in_regions.ETA_VALUES:
        params = M2Params(p=0.0, eta=eta)
        static_threshold = _static_threshold(params)
        dynamic_threshold = dynamic_authenticity_threshold(params)
        optimal_width = 0.0
        dynamic_before_static_width = 0.0
        if dynamic_threshold is None:
            optimal_width = max(0.0, 1.0 - static_threshold)
        else:
            optimal_width = max(0.0, dynamic_threshold - static_threshold)
            dynamic_before_static_width = max(0.0, static_threshold - dynamic_threshold)
        rows.append(
            {
                "run_id": "m2_regime_analysis",
                "eta": eta,
                "static_authenticity_threshold_p": static_threshold,
                "dynamic_authenticity_threshold_p": "" if dynamic_threshold is None else dynamic_threshold,
                "optimal_lock_in_width": optimal_width,
                "dynamic_authenticity_before_static_width": dynamic_before_static_width,
            }
        )
    return rows


def build_learner_sensitivity_rows() -> list[dict[str, object]]:
    learner_cases = [
        ("default", {"alpha": 0.1, "temp": 0.25, "lam": 1.0, "q0": 0.0, "gamma": 0.9}),
        ("low_tau", {"alpha": 0.1, "temp": 0.10, "lam": 1.0, "q0": 0.0, "gamma": 0.9}),
        ("high_tau", {"alpha": 0.1, "temp": 0.60, "lam": 1.0, "q0": 0.0, "gamma": 0.9}),
        ("low_alpha", {"alpha": 0.03, "temp": 0.25, "lam": 1.0, "q0": 0.0, "gamma": 0.9}),
        ("high_alpha", {"alpha": 0.30, "temp": 0.25, "lam": 1.0, "q0": 0.0, "gamma": 0.9}),
        ("loss_averse", {"alpha": 0.1, "temp": 0.25, "lam": 2.5, "q0": 0.0, "gamma": 0.9}),
        ("risk_taking", {"alpha": 0.1, "temp": 0.25, "lam": 0.5, "q0": 0.0, "gamma": 0.9}),
        ("optimistic_prior", {"alpha": 0.1, "temp": 0.25, "lam": 1.0, "q0": 1.5, "gamma": 0.9}),
        ("low_gamma_learner", {"alpha": 0.1, "temp": 0.25, "lam": 1.0, "q0": 0.0, "gamma": 0.5}),
    ]
    cells = [(0.35, 0.0), (0.40, 0.0), (0.55, 0.0), (0.55, 0.2), (0.75, 0.0), (0.90, 0.2)]
    rows: list[dict[str, object]] = []
    for case_index, (case_name, config) in enumerate(learner_cases):
        for cell_index, (p, eta) in enumerate(cells):
            seed = 12000 + case_index * 100 + cell_index
            params = M2Params(p=p, eta=eta, gamma=float(config["gamma"]), lam=float(config["lam"]))
            diagnostics = m2.simulate_with_diagnostics(
                p,
                eta,
                n=120,
                horizon=900,
                alpha=float(config["alpha"]),
                temp=float(config["temp"]),
                lam=float(config["lam"]),
                q0=float(config["q0"]),
                gamma=float(config["gamma"]),
                seed=seed,
            )
            classified = classify_m2_cell(params, diagnostics)
            learned = classified["learned"]
            mask_probability = learned["learned_mask_probabilities"]["neutral"]
            rows.append(
                {
                    "run_id": "m2_regime_analysis",
                    "learner_case": case_name,
                    "p": p,
                    "eta": eta,
                    "alpha": config["alpha"],
                    "tau": config["temp"],
                    "lambda": config["lam"],
                    "q0": config["q0"],
                    "gamma": config["gamma"],
                    "n": 120,
                    "horizon": 900,
                    "seed": seed,
                    "static_m0_optimal_action": classified["static_neutral_action"],
                    "m2_optimal_action_neutral": classified["dynamic_neutral_action"],
                    "learned_neutral_action": classified["learned_neutral_action"],
                    "learned_neutral_mask_probability": "" if mask_probability is None else mask_probability,
                    "learned_mean_mask_rate_final": learned["learned_mean_mask_rate_final"],
                    "regret_neutral": "" if classified["regret_neutral"] is None else classified["regret_neutral"],
                    "region": classified["region"],
                }
            )
    return rows


def build_optimal_sensitivity_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for gamma in [0.0, 0.3, 0.6, 0.9, 0.97]:
        for r2 in [2.5, 5.0, 8.0]:
            for b2 in [0.5, 0.0, -0.5]:
                for delta in [0.02, 0.10, 0.30]:
                    for eta in [0.0, 0.10, 0.20, 0.40, 0.80]:
                        params = M2Params(p=0.0, eta=eta, b2=b2, r2=r2, delta=delta, gamma=gamma)
                        static_threshold = _static_threshold(params)
                        dynamic_threshold = dynamic_authenticity_threshold(params)
                        if dynamic_threshold is None:
                            optimal_width = max(0.0, 1.0 - static_threshold)
                            early_width = 0.0
                            note = "dynamic_authenticity_never_optimal"
                        else:
                            optimal_width = max(0.0, dynamic_threshold - static_threshold)
                            early_width = max(0.0, static_threshold - dynamic_threshold)
                            if optimal_width > 0.0:
                                note = "optimal_learner_lock_in_possible"
                            elif early_width > 0.0:
                                note = "dynamic_authenticity_before_static"
                            else:
                                note = "thresholds_aligned"
                        rows.append(
                            {
                                "run_id": "m2_regime_analysis",
                                "gamma": gamma,
                                "r2": r2,
                                "b2": b2,
                                "delta": delta,
                                "eta": eta,
                                "static_authenticity_threshold_p": static_threshold,
                                "dynamic_authenticity_threshold_p": "" if dynamic_threshold is None else dynamic_threshold,
                                "optimal_lock_in_width": optimal_width,
                                "dynamic_authenticity_before_static_width": early_width,
                                "regime_note": note,
                            }
                        )
    return rows


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def _plot_region_map(cell_rows: list[dict[str, str]], figure_path: Path) -> None:
    plt, BoundaryNorm, ListedColormap, Patch = _load_pyplot()
    p_values = sorted({float(row["p"]) for row in cell_rows})
    eta_values = sorted({float(row["eta"]) for row in cell_rows})
    z_values = np.zeros((len(eta_values), len(p_values)))
    regret = np.full_like(z_values, np.nan, dtype=float)
    for row in cell_rows:
        eta_index = eta_values.index(float(row["eta"]))
        p_index = p_values.index(float(row["p"]))
        z_values[eta_index, p_index] = REGION_CODES[row["region"]]
        if row["regret_neutral"] != "":
            regret[eta_index, p_index] = float(row["regret_neutral"])
    cmap = ListedColormap(["#d8dee9", "#88c0d0", "#bf616a", "#a3be8c", "#5e81ac"])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5, 4.5], cmap.N)
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8), constrained_layout=True)
    axes[0].pcolormesh(p_values, eta_values, z_values, shading="auto", cmap=cmap, norm=norm)
    axes[0].set(title="M2 regime map", xlabel="receptivity p", ylabel="escape eta")
    axes[0].legend(
        handles=[Patch(facecolor=cmap(index), label=REGION_LABELS[index]) for index in sorted(REGION_LABELS)],
        loc="upper right",
        fontsize=7,
        frameon=True,
    )
    im = axes[1].pcolormesh(p_values, eta_values, regret, shading="auto", cmap="magma")
    axes[1].set(title="Neutral-state regret of learned policy", xlabel="receptivity p", ylabel="escape eta")
    fig.colorbar(im, ax=axes[1])
    fig.set_layout_engine(None)
    fig.subplots_adjust(left=0.06, right=0.93, bottom=0.12, top=0.88, wspace=0.28)
    fig.savefig(figure_path, dpi=160)
    plt.close(fig)


def _plot_thresholds(threshold_rows: list[dict[str, object]], sensitivity_rows: list[dict[str, object]], figure_path: Path) -> None:
    plt, _, _, _ = _load_pyplot()
    etas = [float(row["eta"]) for row in threshold_rows]
    static = [float(row["static_authenticity_threshold_p"]) for row in threshold_rows]
    dynamic = [float(row["dynamic_authenticity_threshold_p"]) for row in threshold_rows]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    axes[0].plot(etas, static, "k--", label="static M0 threshold")
    axes[0].plot(etas, dynamic, "-o", ms=3, label="dynamic M2 threshold")
    axes[0].fill_between(etas, dynamic, static, where=np.asarray(dynamic) < np.asarray(static), color="#88c0d0", alpha=0.35, label="dynamic auth before static")
    axes[0].set(title="Default M2 authenticity thresholds", xlabel="escape eta", ylabel="p threshold", ylim=(0.0, 1.0))
    axes[0].legend(fontsize=8)
    by_gamma: dict[float, list[float]] = {}
    for row in sensitivity_rows:
        gamma = float(row["gamma"])
        by_gamma.setdefault(gamma, []).append(float(row["optimal_lock_in_width"]))
    gammas = sorted(by_gamma)
    widths = [max(by_gamma[gamma]) for gamma in gammas]
    axes[1].bar([str(gamma) for gamma in gammas], widths, color="#5e81ac")
    axes[1].set(title="Max optimal-policy masking width", xlabel="gamma", ylabel="p-width")
    axes[1].text(
        0.5,
        1.02,
        "environment perturbations",
        transform=axes[1].transAxes,
        ha="center",
        va="bottom",
        fontsize=9,
    )
    fig.savefig(figure_path, dpi=160)
    plt.close(fig)


def _plot_learner_sensitivity(rows: list[dict[str, object]], figure_path: Path) -> None:
    plt, _, _, _ = _load_pyplot()
    cases = list(dict.fromkeys(str(row["learner_case"]) for row in rows))
    cells = list(dict.fromkeys(f"p={float(row['p']):.2f}, eta={float(row['eta']):.2f}" for row in rows))
    z_values = np.zeros((len(cases), len(cells)))
    for row in rows:
        case_index = cases.index(str(row["learner_case"]))
        cell_index = cells.index(f"p={float(row['p']):.2f}, eta={float(row['eta']):.2f}")
        z_values[case_index, cell_index] = float(row["learned_neutral_mask_probability"] or 0.0)
    fig, ax = plt.subplots(figsize=(11, 4.8))
    im = ax.imshow(z_values, aspect="auto", cmap="RdYlBu_r", vmin=0.0, vmax=1.0)
    ax.set(title="Learned neutral-state mask probability", xlabel="cell", ylabel="learner case")
    ax.set_xticks(range(len(cells)))
    ax.set_xticklabels(cells, rotation=35, ha="right", fontsize=8)
    ax.set_yticks(range(len(cases)))
    ax.set_yticklabels(cases, fontsize=8)
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(figure_path, dpi=160)
    plt.close(fig)


def main() -> int:
    paths = ensure_results_dirs(ROOT / "results")
    figure_dir = paths["figures"]
    map_m2_lock_in_regions.main()
    cell_rows_for_graph = _read_csv(paths["summaries"] / "m2_lock_in_region_map.csv")
    threshold_rows = build_refined_threshold_rows()
    learner_rows = build_learner_sensitivity_rows()
    optimal_rows = build_optimal_sensitivity_rows()
    write_csv(paths["summaries"] / "m2_regime_refined_thresholds.csv", [{key: _format(row[key]) for key in THRESHOLD_COLUMNS} for row in threshold_rows])
    write_csv(paths["summaries"] / "m2_learner_parameter_sensitivity.csv", [{key: _format(row[key]) for key in LEARNER_COLUMNS} for row in learner_rows])
    write_csv(paths["summaries"] / "m2_optimal_regime_sensitivity.csv", [{key: _format(row[key]) for key in OPTIMAL_SENSITIVITY_COLUMNS} for row in optimal_rows])
    _plot_region_map(cell_rows_for_graph, figure_dir / "m2_lock_in_region_map.png")
    _plot_thresholds(threshold_rows, optimal_rows, figure_dir / "m2_regime_thresholds.png")
    _plot_learner_sensitivity(learner_rows, figure_dir / "m2_learner_sensitivity.png")
    print(paths["summaries"] / "m2_regime_refined_thresholds.csv")
    print(paths["summaries"] / "m2_learner_parameter_sensitivity.csv")
    print(paths["summaries"] / "m2_optimal_regime_sensitivity.csv")
    print(figure_dir / "m2_lock_in_region_map.png")
    print(figure_dir / "m2_regime_thresholds.png")
    print(figure_dir / "m2_learner_sensitivity.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
