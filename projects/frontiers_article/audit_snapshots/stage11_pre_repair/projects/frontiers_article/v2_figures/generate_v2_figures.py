"""Deterministically assemble the four Article-V2 figures from frozen tables.

This is a presentation-only generator.  It reads the hash-pinned compact CSVs
from ``publication_v1/data`` and imports neither an experiment module nor any
simulation/plotting utility from ``src``.  Running it must never generate new
stochastic evidence.
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "publication_v1" / "data"
OUT = Path(__file__).resolve().parent / "figures"

# This explicitly pins every numerical input used below to the frozen
# publication-source data chain checked during Stage 7.
SOURCES = {
    "e01_primary_effects.csv": "9b9227f43146b96ae7000f572d2249ae6bd4d39bf414715bdd780203afa38d36",
    "e01_intervention_effects.csv": "12a1f4befa1ade1a9065a3782fc40a20d9bbed2f91d31a1d3d4dd5771d55a42b",
    "e02_primary_effects.csv": "fe37531296d986f0662ce74d6e3976680163e4f19da7240deef5f8e5d97f966f",
    "e03_grid_map.csv": "c5def710116248b60ffcc347fa408519ce5d9094547e486fc73f2388e5babbab",
    "e03_grid_summary.csv": "90aebefa0fe66c1f3092879d365c2ede798e71114a1f3b0bb74ee6df083f096a",
    "e04_k_response.csv": "c01c04359b30d425d518566190dcfb27b10f9003e4123d9a6f05ce44382c11b7",
    "e04_headline_effects.csv": "ebcf58f06eef99fa890bbf9039b3c59293bb743417e3e279f35723f3ef501868",
    "e05_response_vs_bf.csv": "0d47aeae4dc4c15e08176c7ff44466740712f3a47000a68d2b7a1231d48a7e10",
    "e05_crossings.csv": "866697afb0cdd66f6e6d008cc6b06e52786d1e27f7ba3f71601a56512349076b",
    "e05_displacement.csv": "4357f2fc10a07d763e2ec140d30adb5732f71ce1933644e83230af5492098213",
}

INK = "#1a1a1a"
NAVY = "#1f3b73"
RED = "#9c2f2f"
GREY = "#666666"
PALE = "#e6e6e6"
BLUE_PALE = "#d6e4f0"
RED_PALE = "#f0d7d7"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources() -> None:
    for name, expected in SOURCES.items():
        path = DATA / name
        actual = sha256(path) if path.exists() else "MISSING"
        if actual != expected:
            raise RuntimeError(f"Frozen publication source mismatch: {name}: {actual} != {expected}")


def rows(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def style() -> None:
    matplotlib.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 400,
            "font.family": "DejaVu Sans",
            "font.size": 8,
            "axes.labelsize": 8,
            "axes.titlesize": 8.5,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "xtick.labelsize": 7.2,
            "ytick.labelsize": 7.2,
            "legend.fontsize": 6.8,
            "legend.frameon": False,
            "axes.linewidth": 0.6,
            "lines.linewidth": 1.25,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def save(fig: plt.Figure, stem: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{stem}.pdf", metadata={"CreationDate": None, "Creator": "Article V2 frozen-evidence figure assembly"})
    fig.savefig(OUT / f"{stem}.png", metadata={"Software": None})
    plt.close(fig)


def panel(ax: plt.Axes, label: str) -> None:
    ax.text(-0.08, 1.06, label, transform=ax.transAxes, fontweight="bold", fontsize=10, ha="right", va="bottom")


def forest(ax: plt.Axes, entries: list[dict[str, object]], xlabel: str) -> None:
    ys = list(range(len(entries)))[::-1]
    ax.axvline(0, color=INK, linestyle=(0, (4, 3)), linewidth=.65, zorder=1)
    for y, item in zip(ys, entries):
        ax.plot([item["lo"], item["hi"]], [y, y], color=item["colour"], linewidth=1.4, zorder=3)
        ax.plot([item["est"]], [y], marker=item.get("marker", "o"), ms=4.8, color=item["colour"],
                markerfacecolor=item.get("face", item["colour"]), markeredgewidth=.85, linestyle="none", zorder=4)
    ax.set_yticks(ys, [str(item["label"]) for item in entries])
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(-.75, len(entries)-.25)
    ax.set_xlabel(xlabel)


def figure_1() -> None:
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.25, 3.75), gridspec_kw={"width_ratios": [1.18, 1]})
    for ax in (ax_a, ax_b):
        ax.set_axis_off()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    inputs = [
        ("Learning\nhistory", .08, .79, .22),
        ("Current social\nconditions", .36, .79, .22),
        ("Action\nrepresentation", .64, .79, .22),
        ("Persistent social\nconsequences", .05, .49, .34),
        ("Contextual availability\nand discoverability", .51, .49, .42),
    ]
    for text, x, y, width in inputs:
        ax_a.add_patch(FancyBboxPatch((x, y), width, .12, boxstyle="round,pad=.015,rounding_size=.015",
                                      facecolor="#f4f6fa", edgecolor=NAVY, linewidth=.8))
        ax_a.text(x+width/2, y+.06, text, ha="center", va="center", fontsize=7.0)
        ax_a.add_patch(FancyArrowPatch((x+width/2, y), (.50, .34), arrowstyle="-|>", mutation_scale=9,
                                       color=GREY, linewidth=.65, connectionstyle="arc3,rad=0.05"))
    ax_a.add_patch(FancyBboxPatch((.31, .27), .38, .13, boxstyle="round,pad=.018,rounding_size=.018",
                                  facecolor=BLUE_PALE, edgecolor=NAVY, linewidth=1))
    ax_a.text(.50, .335, "Learner information\nand expectations", ha="center", va="center", fontsize=8, fontweight="bold")
    ax_a.add_patch(FancyArrowPatch((.50, .27), (.50, .13), arrowstyle="-|>", mutation_scale=10, color=INK, linewidth=.8))
    ax_a.add_patch(FancyBboxPatch((.25, .03), .50, .10, boxstyle="round,pad=.018,rounding_size=.018",
                                  facecolor=RED_PALE, edgecolor=RED, linewidth=1))
    ax_a.text(.50, .08, "Observed ability visibility / concealment", ha="center", va="center", fontsize=7.8, fontweight="bold")
    ax_a.text(.50, .94, "Different upstream conditions can converge\non similar observed concealment", ha="center", va="center", fontsize=6.7, color=GREY)
    ax_a.text(.50, .17, "Similar current conditions can yield different behaviour\nwhen learning histories and expectations differ", ha="center", va="center", fontsize=6.4, color=GREY)
    ax_a.set_title("Underidentification architecture", pad=10)
    panel(ax_a, "A")

    cards = [
        ("E01", "Restricted\nsampling", .08, .69, NAVY),
        ("E02", "Action\nrepresentation", .56, .69, NAVY),
        ("E03", "Persistent state\nand dynamic value", .08, .39, RED),
        ("E04", "Contextual\ndiscoverability", .56, .39, RED),
        ("E05", "Learned–environmental\nboundary", .32, .10, INK),
    ]
    ax_b.add_patch(FancyBboxPatch((.30, .46), .40, .12, boxstyle="round,pad=.018,rounding_size=.018",
                                  facecolor=PALE, edgecolor=INK, linewidth=.8))
    ax_b.text(.50, .52, "Experimental\ndecomposition", ha="center", va="center", fontsize=8, fontweight="bold")
    for ident, text, x, y, colour in cards:
        ax_b.add_patch(FancyBboxPatch((x, y), .34, .13, boxstyle="round,pad=.014,rounding_size=.014",
                                      facecolor="white", edgecolor=colour, linewidth=.9))
        ax_b.text(x+.04, y+.065, ident, ha="left", va="center", fontsize=7.5, fontweight="bold", color=colour)
        ax_b.text(x+.13, y+.065, text, ha="left", va="center", fontsize=6.75)
        ax_b.add_patch(FancyArrowPatch((.50, .52), (x+.17, y+.13 if y < .46 else y), arrowstyle="-", color=GREY, linewidth=.55))
    ax_b.text(.50, .92, "Five experimental routes to the same\nobserved behavioural endpoint", ha="center", va="center", fontsize=7.0, color=GREY)
    ax_b.set_title("Experimental mechanism map", pad=10)
    panel(ax_b, "B")
    fig.subplots_adjust(left=.055, right=.985, top=.89, bottom=.07, wspace=.25)
    save(fig, "Figure_1_underidentification_architecture")


def figure_2() -> None:
    e01 = {r["claim_id"]: r for r in rows("e01_primary_effects.csv")}
    interventions = {r["claim_id"]: r for r in rows("e01_intervention_effects.csv")}
    e02 = {r["claim_id"]: r for r in rows("e02_primary_effects.csv")}
    fig, axes = plt.subplots(1, 3, figsize=(7.25, 3.1), gridspec_kw={"width_ratios": [1, 1, 1.08]})
    a = [
        {"label": "authentic\nsampling", "est": float(e01["E01-C2-SAMPLING"]["estimate"]), "lo": float(e01["E01-C2-SAMPLING"]["ci_low"]), "hi": float(e01["E01-C2-SAMPLING"]["ci_high"]), "colour": NAVY},
        {"label": "final mask\nrate", "est": float(e01["E01-C2-FINAL-MASK"]["estimate"]), "lo": float(e01["E01-C2-FINAL-MASK"]["ci_low"]), "hi": float(e01["E01-C2-FINAL-MASK"]["ci_high"]), "colour": INK, "face": "white"},
    ]
    forest(axes[0], a, "rejected minus accepted")
    axes[0].set_title("History (E01)", pad=13); axes[0].set_xlim(-.045, .022); panel(axes[0], "A")
    axes[0].text(.0, 1.02, "sampling effect; final mask near zero", transform=axes[0].transAxes, fontsize=6.1, color=GREY)
    b = [
        {"label": "5% forced\nexploration", "est": float(interventions["E01-C2-FORCED-MASK"]["estimate"]), "lo": float(interventions["E01-C2-FORCED-MASK"]["ci_low"]), "hi": float(interventions["E01-C2-FORCED-MASK"]["ci_high"]), "colour": GREY, "marker": "s", "face": "white"},
        {"label": "counterfactual\nfeedback", "est": float(interventions["E01-C2-CF-MASK"]["estimate"]), "lo": float(interventions["E01-C2-CF-MASK"]["ci_low"]), "hi": float(interventions["E01-C2-CF-MASK"]["ci_high"]), "colour": RED},
    ]
    forest(axes[1], b, "mask reduction")
    axes[1].set_title("Information (E01)", pad=13); axes[1].set_xlim(-.012, .145); panel(axes[1], "B")
    axes[1].text(.0, 1.02, "rejected stratum", transform=axes[1].transAxes, fontsize=6.1, color=GREY)
    c = [
        {"label": "non-zero\ndisclosure", "est": float(e02["E02-C4-EXPLORATION"]["estimate"]), "lo": float(e02["E02-C4-EXPLORATION"]["ci_low"]), "hi": float(e02["E02-C4-EXPLORATION"]["ci_high"]), "colour": NAVY},
        {"label": "full-authentic\nselection", "est": float(e02["E02-C4-FULL-ENDPOINT"]["estimate"]), "lo": float(e02["E02-C4-FULL-ENDPOINT"]["ci_low"]), "hi": float(e02["E02-C4-FULL-ENDPOINT"]["ci_high"]), "colour": RED, "face": "white"},
        {"label": "unique-modal\nfull authenticity", "est": float(e02["E02-C4-MODAL"]["estimate"]), "lo": float(e02["E02-C4-MODAL"]["ci_low"]), "hi": float(e02["E02-C4-MODAL"]["ci_high"]), "colour": GREY, "marker": "D", "face": "white"},
    ]
    forest(axes[2], c, "graded minus binary")
    axes[2].set_title("Representation (E02)", pad=13); axes[2].set_xlim(-.43, .34); panel(axes[2], "C")
    axes[2].text(.0, 1.02, "five independently learned arms", transform=axes[2].transAxes, fontsize=6.1, color=GREY)
    fig.subplots_adjust(left=.16, right=.985, top=.83, bottom=.20, wspace=.86)
    save(fig, "Figure_2_history_and_action_representation")


def _edges(values: np.ndarray) -> np.ndarray:
    mid = (values[:-1] + values[1:]) / 2
    return np.concatenate([[values[0] - (mid[0] - values[0])], mid, [values[-1] + (values[-1] - mid[-1])]])


def figure_3() -> None:
    grid = rows("e03_grid_map.csv")
    summary = {r["publication_category"]: int(r["cell_count"]) for r in rows("e03_grid_summary.csv")}
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.25, 3.45), gridspec_kw={"width_ratios": [.83, 1.17]})
    ax_a.set_axis_off(); ax_a.set_xlim(0, 1); ax_a.set_ylim(0, 1)
    states = [("Neutral", .12, .46, BLUE_PALE, NAVY), ("Accepted", .62, .72, "#edf4ed", "#3a7040"), ("Stigmatized", .62, .20, RED_PALE, RED)]
    for name, x, y, fill, edge in states:
        ax_a.add_patch(FancyBboxPatch((x, y), .25, .14, boxstyle="round,pad=.015,rounding_size=.02", facecolor=fill, edgecolor=edge, linewidth=1))
        ax_a.text(x+.125, y+.07, name, ha="center", va="center", fontweight="bold", fontsize=7.8)
    arrows = [((.37, .56), (.62, .79), "authentic / accepted"), ((.37, .51), (.62, .27), "authentic / rejected"), ((.74, .72), (.37, .60), "turnover"), ((.74, .34), (.37, .49), "escape $\\eta$")]
    for start, end, label in arrows:
        ax_a.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=9, color=INK, linewidth=.75, connectionstyle="arc3,rad=.12"))
        ax_a.text((start[0]+end[0])/2, (start[1]+end[1])/2 + (.05 if end[1] > start[1] else -.055), label, fontsize=6.1, ha="center", va="center")
    ax_a.add_patch(FancyArrowPatch((.16, .44), (.16, .59), arrowstyle="-|>", mutation_scale=8, color=GREY, linewidth=.7, connectionstyle="arc3,rad=.75"))
    ax_a.text(.03, .65, "masking:\nstate remains", ha="left", va="center", fontsize=6.2, color=GREY)
    ax_a.text(.50, .06, "Dynamic value = immediate reward +\nfuture-state value", ha="center", va="center", fontsize=7, fontweight="bold")
    ax_a.set_title("Persistent social state (E03)", pad=13); panel(ax_a, "A")

    pvals = np.array(sorted({float(r["p"]) for r in grid}))
    etas = np.array(sorted({float(r["eta"]) for r in grid}))
    order = ["learner_matches_objective", "learned_suboptimal_masking", "inconclusive"]
    image = np.full((len(etas), len(pvals)), np.nan)
    for r in grid:
        image[etas.tolist().index(float(r["eta"])), pvals.tolist().index(float(r["p"]))] = order.index(r["publication_category"])
    cmap = matplotlib.colors.ListedColormap(["#d4d4d4", "#5a5a5a", "#ffffff"])
    ax_b.pcolormesh(_edges(pvals), _edges(etas), image, cmap=cmap, vmin=-.5, vmax=2.5, edgecolors="white", linewidth=.15)
    # Markers preserve category distinctions in grayscale reproduction.
    for r in grid:
        marker = {"learner_matches_objective": "o", "learned_suboptimal_masking": "x", "inconclusive": "s"}[r["publication_category"]]
        colour = "white" if r["publication_category"] == "learned_suboptimal_masking" else INK
        ax_b.plot(float(r["p"]), float(r["eta"]), marker=marker, ms=1.6 if marker != "x" else 2.2, color=colour, markeredgewidth=.35, linestyle="none")
    objective = np.array([[1 if r["objective_neutral_action"] == "authentic" else 0 for r in grid if float(r["eta"]) == eta] for eta in etas])
    ax_b.contour(pvals, etas, objective, levels=[.5], colors=[INK], linewidths=.9)
    ax_b.set_xlabel("acceptance probability $p$"); ax_b.set_ylabel("recovery $\\eta$")
    ax_b.set_title("Learned–objective classifier", pad=13); panel(ax_b, "B")
    handles = [
        Line2D([], [], marker="o", color=INK, markerfacecolor="#d4d4d4", linestyle="none", label=f"agreement — {summary[order[0]]}/357"),
        Line2D([], [], marker="x", color=INK, linestyle="none", label=f"disagreement — {summary[order[1]]}/357"),
        Line2D([], [], marker="s", color=INK, markerfacecolor="white", linestyle="none", label=f"inconclusive — {summary[order[2]]}/357"),
        Line2D([], [], color=INK, linewidth=.9, label="oracle switch"),
    ]
    ax_b.legend(handles=handles, loc="upper center", bbox_to_anchor=(.5, -.23), ncol=2, columnspacing=.8, handletextpad=.35)
    ax_b.text(.01, 1.02, "aggregate final-window Neutral-state action counts", transform=ax_b.transAxes, fontsize=6.1, color=GREY)
    fig.subplots_adjust(left=.08, right=.98, top=.86, bottom=.28, wspace=.31)
    save(fig, "Figure_3_persistent_state_and_disagreement")


def pava_nonincreasing(values: np.ndarray) -> np.ndarray:
    """Deterministic unweighted PAVA for the frozen pooled-response points."""
    blocks: list[list[float]] = []
    for value in values:
        blocks.append([float(value), 1.0])
        while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] < blocks[-1][0] / blocks[-1][1]:
            total = [blocks[-2][0] + blocks[-1][0], blocks[-2][1] + blocks[-1][1]]
            blocks[-2:] = [total]
    return np.array([total / count for total, count in blocks for _ in range(int(count))])


def figure_4() -> None:
    curves = rows("e04_k_response.csv")
    effects = {r["claim_id"]: r for r in rows("e04_headline_effects.csv")}
    response = rows("e05_response_vs_bf.csv")
    crossings = {r["architecture"]: r for r in rows("e05_crossings.csv")}
    displacement = {r["quantity"]: r for r in rows("e05_displacement.csv")}
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.25, 3.5), gridspec_kw={"width_ratios": [1.05, 1]})
    series = [("flat_2k", NAVY, "-", "flat 2K"), ("hierarchical", RED, "-", "hierarchical"), ("global_mask", GREY, (0, (3, 2)), "global-mask control")]
    for architecture, colour, linestyle, label in series:
        pts = sorted((int(r["K"]), float(r["master_mean"]), float(r["master_min"]), float(r["master_max"])) for r in curves if r["series"] == "one_good" and r["architecture"] == architecture)
        x = np.array([p[0] for p in pts], dtype=float); y = np.array([p[1] for p in pts])
        ax_a.plot(x, y, color=colour, linestyle=linestyle, marker="o", ms=3.2, label=label, zorder=4)
        if architecture in {"flat_2k", "hierarchical"}:
            ax_a.fill_between(x, [p[2] for p in pts], [p[3] for p in pts], color=colour, alpha=.12, linewidth=0)
    known = next(r for r in curves if r["series"] == "known_good_reference")
    ax_a.axhline(float(known["master_mean"]), color=INK, linestyle=(0, (1, 2)), linewidth=.8, label="fixed-known-good control")
    ax_a.set_xscale("log", base=2); ax_a.set_xticks([1, 2, 4, 8, 16], ["1", "2", "4", "8", "16"])
    ax_a.set_xlabel("number of contexts $K$"); ax_a.set_ylabel("final-window good-context\nauthentic action (first-index argmax)")
    ax_a.set_ylim(.43, 1.035); ax_a.set_title("Context discoverability (E04)", pad=13); panel(ax_a, "A")
    ax_a.text(.0, 1.02, "one good context; shaded ranges are descriptive master ranges", transform=ax_a.transAxes, fontsize=5.9, color=GREY)
    ax_a.legend(loc="lower left", fontsize=5.9, handlelength=1.8, labelspacing=.25)
    inset = ax_a.inset_axes([.12, .28, .50, .27])
    selected = [("E04-C6-FLAT", "flat 2K", NAVY), ("E04-C6-HIER", "hier.", RED), ("E04-C6-CONTROL-GLOBALMASK", "global", GREY), ("E04-C6-CONTROL-KNOWNGOOD", "known", INK)]
    for y, (key, label, colour) in enumerate(selected[::-1]):
        r = effects[key]; inset.plot([float(r["ci_low"]), float(r["ci_high"])], [y, y], color=colour, linewidth=1)
        inset.plot(float(r["estimate"]), y, marker="o", ms=2.8, color=colour, linestyle="none")
    inset.axvline(0, color=INK, linewidth=.5, linestyle=(0, (3, 2)))
    inset.set_yticks(range(4), [x[1] for x in selected[::-1]], fontsize=5.3); inset.tick_params(axis="x", labelsize=5.2, length=1.5)
    inset.set_xlabel("$K=16$ minus $K=1$ (95% CI)", fontsize=5.2, labelpad=1)
    inset.set_xlim(-.57, .10)

    dense = sorted((float(r["bf"]), float(r["pooled_response"])) for r in response if r["architecture"] == "flat_2k" and r["in_dense_range"] == "True")
    x = np.array([p[0] for p in dense]); y = np.array([p[1] for p in dense]); fitted = pava_nonincreasing(y)
    ax_b.plot(x, y, marker="o", markersize=2.7, color=GREY, linestyle="none", label="frozen pooled response", zorder=3)
    ax_b.step(x, fitted, where="mid", color=NAVY, linewidth=1.5, label="non-increasing PAVA fit", zorder=4)
    ax_b.axhline(.5, color=INK, linestyle=(0, (4, 3)), linewidth=.65, zorder=1)
    flat = crossings["flat_2k"]; learned, lo, hi, objective = (float(flat[k]) for k in ("transition_bf", "ci_low", "ci_high", "analytic_threshold_bf"))
    ax_b.axvspan(learned, objective, color=BLUE_PALE, alpha=.7, zorder=0)
    ax_b.axvspan(lo, hi, color=NAVY, alpha=.22, zorder=1)
    ax_b.axvline(learned, color=NAVY, linewidth=1.05); ax_b.axvline(objective, color=INK, linestyle=(0, (5, 2)), linewidth=1.0)
    ax_b.annotate("", xy=(objective, .93), xytext=(learned, .93), arrowprops={"arrowstyle": "<|-|>", "linewidth": .75, "color": INK})
    ax_b.text((learned+objective)/2, .955, f"displacement {float(displacement['displacement_objective_minus_learned']['value']):.3f}", ha="center", va="bottom", fontsize=6.1)
    ax_b.text(learned-.004, .78, "learned behavioural\ncrossing\n0.312852", ha="right", va="top", fontsize=6.0, color=NAVY)
    ax_b.text(objective+.006, .69, "environmental/objective\ncrossover $8/17$\n= 0.470588", ha="left", va="top", fontsize=6.0)
    ax_b.text(.645, .19, "hierarchical: left-censored\nbelow tested range", ha="right", va="center", fontsize=6.0, color=RED)
    ax_b.set_xlim(.292, .658); ax_b.set_ylim(-.025, 1.02); ax_b.set_xlabel("comparison cost $b_f$")
    ax_b.set_ylabel("fraction selecting good-context\nauthentic action")
    ax_b.set_title("Boundary displacement (E05)", pad=13); panel(ax_b, "B")
    ax_b.legend(loc="upper right", fontsize=5.9, handlelength=1.6)
    fig.subplots_adjust(left=.10, right=.985, top=.86, bottom=.18, wspace=.37)
    save(fig, "Figure_4_discoverability_and_boundary_displacement")


def main() -> None:
    verify_sources()
    style()
    figure_1(); figure_2(); figure_3(); figure_4()
    print("ARTICLE_V2_FIGURE_ASSEMBLY_OK — deterministic visualization only; no experiment code imported or executed")


if __name__ == "__main__":
    main()
