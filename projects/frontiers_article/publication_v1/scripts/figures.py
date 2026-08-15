"""Article-V1 main figures 1-4.

Every panel reads only the compact publication-source CSVs under
`publication_v1/data/`. No figure touches `results/raw/`, `results/summaries/`, or
any simulation entry point, and none of the bespoke stochastic plotting utilities
in `src/gifted_masking/plotting/` is used.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch

from pubcommon import DATA_DIR, FIGURES_DIR, read_rows, require

# Restrained, print-safe palette. One accent for the learner, one for the
# objective comparator, greys for controls and context.
INK = "#1a1a1a"
PRIMARY = "#1f3b73"
SECONDARY = "#b2182b"
CONTROL = "#7a7a7a"
LIGHT = "#c8c8c8"
MATCHES = "#a6cee3"
SUBOPTIMAL = "#b2182b"
INCONCLUSIVE = "#e4e4e4"


def apply_style() -> None:
    matplotlib.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 400,
            "savefig.bbox": "standard",
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans"],
            "font.size": 8.0,
            "axes.labelsize": 8.0,
            "axes.titlesize": 8.5,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            "legend.fontsize": 7.0,
            "legend.frameon": False,
            "axes.linewidth": 0.6,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "xtick.major.size": 2.8,
            "ytick.major.size": 2.8,
            "lines.linewidth": 1.2,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "article-v1-publication",
        }
    )


def _panel_label(ax, text: str) -> None:
    ax.text(
        -0.06,
        1.06,
        text,
        transform=ax.transAxes,
        fontsize=9.5,
        fontweight="bold",
        va="bottom",
        ha="right",
    )


def save(fig, stem: str) -> list[Path]:
    """Write vector PDF plus a high-resolution raster counterpart.

    PDF CreationDate is suppressed so repeated builds from identical frozen
    inputs produce identical bytes.
    """
    pdf = FIGURES_DIR / f"{stem}.pdf"
    png = FIGURES_DIR / f"{stem}.png"
    fig.savefig(
        pdf,
        format="pdf",
        metadata={"CreationDate": None, "Creator": "article-v1-publication-build", "Producer": "matplotlib"},
    )
    fig.savefig(png, format="png", metadata={"Software": None})
    plt.close(fig)
    return [pdf, png]


# ---------------------------------------------------------------------------
# Figure 1 - model progression and analytic structure (conceptual, no simulation data)
# ---------------------------------------------------------------------------

STAGES = [
    (
        "M0",
        "Binary authenticity vs masking",
        "Static expected reward",
        r"$\Delta_0(p) = a + c - (1-p)(b+r)$" "\n" r"static M0 objective boundary  $p^{*} = 43/60$",
        "E01",
    ),
    (
        "M1",
        "Graded disclosure",
        "Affine objective",
        r"$E[R(d)] = b - c + d\,[a + c - (1-p)(b+r)]$" "\n" "affine in $d$: strict optimum at an endpoint",
        "E02",
    ),
    (
        "M2",
        "Actions change future state",
        "Dynamic Bellman optimum",
        r"$D_N(V) = \Delta_0(p) + \gamma\,[\,p V_A + (1-p) V_S - V_N\,]$" "\n"
        "full-information dynamic comparator",
        "E03",
    ),
    (
        "M3",
        "Heterogeneous contexts",
        "Discovery, scarcity, comparison cost",
        r"$\max\{R_M, R_G, R_B\}$ invariant in $K$ (one good context)" "\n"
        r"objective comparison-cost crossover  $b_f^{*} = 8/17$",
        "E04, E05",
    ),
]

TRANSITIONS = [
    "add graded action space",
    "add persistent social state",
    "add heterogeneous receptive contexts",
]


def figure_1() -> list[Path]:
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    box_h, gap = 0.172, 0.075
    top = 0.972
    for index, (model, mechanism, objective, anchor, experiments) in enumerate(STAGES):
        y1 = top - index * (box_h + gap)
        y0 = y1 - box_h
        ax.add_patch(
            FancyBboxPatch(
                (0.035, y0),
                0.93,
                box_h,
                boxstyle="round,pad=0.004,rounding_size=0.010",
                linewidth=0.9,
                edgecolor=PRIMARY,
                facecolor="#f4f6fa",
                mutation_aspect=1.0,
            )
        )
        mid = (y0 + y1) / 2
        ax.text(0.068, mid + 0.022, model, fontsize=13, fontweight="bold", color=PRIMARY, va="center")
        ax.text(0.070, mid - 0.036, experiments, fontsize=7.4, fontweight="bold", color=SECONDARY, va="center")
        ax.text(0.163, mid + 0.030, mechanism, fontsize=8.6, fontweight="bold", va="center")
        ax.text(0.163, mid - 0.012, objective, fontsize=7.6, color="#4a4a4a", va="center")
        ax.plot([0.455, 0.455], [y0 + 0.026, y1 - 0.026], color="#c3ccdb", linewidth=0.7)
        ax.text(0.482, mid, anchor, fontsize=7.3, va="center", linespacing=1.75)

        if index < len(TRANSITIONS):
            ax.annotate(
                "",
                xy=(0.28, y0 - gap + 0.006),
                xytext=(0.28, y0 - 0.006),
                arrowprops={"arrowstyle": "-|>", "linewidth": 0.9, "color": INK, "shrinkA": 0, "shrinkB": 0},
            )
            ax.text(
                0.30,
                y0 - gap / 2,
                TRANSITIONS[index],
                fontsize=7.6,
                style="italic",
                va="center",
                ha="left",
            )

    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    return save(fig, "Figure_1_model_progression")


# ---------------------------------------------------------------------------
# Figure 2 - early adverse feedback (E01) and graded disclosure (E02)
# ---------------------------------------------------------------------------


def _forest(ax, entries, *, xlabel: str) -> None:
    """Horizontal effect plot: estimate with interval, zero reference line."""
    positions = list(range(len(entries)))[::-1]
    ax.axvline(0.0, color=INK, linewidth=0.7, linestyle=(0, (4, 3)), zorder=1)
    for y, entry in zip(positions, entries):
        colour = entry["colour"]
        ax.plot(
            [entry["low"], entry["high"]],
            [y, y],
            color=colour,
            linewidth=1.4,
            solid_capstyle="butt",
            zorder=3,
        )
        ax.plot(
            [entry["estimate"]],
            [y],
            marker=entry.get("marker", "o"),
            markersize=5.0,
            markerfacecolor=entry.get("face", colour),
            markeredgecolor=colour,
            markeredgewidth=1.1,
            linestyle="none",
            zorder=4,
        )
    ax.set_yticks(positions)
    ax.set_yticklabels([e["label"] for e in entries])
    ax.set_ylim(-0.7, len(entries) - 0.3)
    ax.set_xlabel(xlabel)
    ax.tick_params(axis="y", length=0)


def figure_2() -> list[Path]:
    e01 = {r["role"]: r for r in read_rows(DATA_DIR / "e01_primary_effects.csv")}
    e02 = read_rows(DATA_DIR / "e02_primary_effects.csv")
    arms = read_rows(DATA_DIR / "e02_arm_expected_rewards.csv")

    fig, (ax_a, ax_b, ax_c) = plt.subplots(
        1, 3, figsize=(7.4, 3.0), gridspec_kw={"width_ratios": [1.0, 1.0, 0.62]}
    )

    # --- Panel A: E01 -------------------------------------------------------
    order = ["primary", "linked_unit_translation", "secondary_null"]
    labels = {
        "primary": "authentic sampling",
        "linked_unit_translation": "normalized regret\n(same estimand)",
        "secondary_null": "final-window mask rate",
    }
    entries = []
    for role in order:
        row = e01[role]
        entries.append(
            {
                "label": labels[role],
                "estimate": float(row["estimate"]),
                "low": float(row["ci_low"]),
                "high": float(row["ci_high"]),
                "colour": PRIMARY if role == "primary" else (CONTROL if role == "linked_unit_translation" else INK),
                "marker": "o" if role == "primary" else ("s" if role == "linked_unit_translation" else "o"),
                "face": PRIMARY if role == "primary" else "white",
            }
        )
    _forest(ax_a, entries, xlabel="rejected minus accepted")
    ax_a.set_title("Early adverse feedback (E01)", pad=14)
    _panel_label(ax_a, "a")
    ax_a.set_xlim(-0.052, 0.052)
    ax_a.set_ylim(-0.8, 2.85)

    # Make the exact linkage between the top two rows visible rather than
    # letting them read as two independent confirmations.
    ax_a.text(
        0.0,
        1.02,
        "regret row is the sampling row rescaled",
        transform=ax_a.transAxes,
        fontsize=6.6,
        style="italic",
        color=CONTROL,
        ha="left",
        va="bottom",
    )
    ax_a.text(
        0.0,
        -0.66,
        "interval spans zero",
        fontsize=6.2,
        color=CONTROL,
        ha="center",
        va="center",
    )

    # --- Panel B: E02 -------------------------------------------------------
    e02_labels = {
        "E02-C4-EXPLORATION": "nonzero disclosure\nafter rejection",
        "E02-C4-FULL-ENDPOINT": "full-authentic\nfinal-window rate",
        "E02-C4-MODAL": "modal arm is the\nobjective endpoint",
        "E02-C4-REGRET": "normalized regret\n(binary minus graded)",
    }
    entries = []
    for row in e02:
        entries.append(
            {
                "label": e02_labels[row["claim_id"]],
                "estimate": float(row["estimate"]),
                "low": float(row["ci_low"]),
                "high": float(row["ci_high"]),
                "colour": PRIMARY if row["role"] == "primary" else SECONDARY,
                "marker": "o" if row["role"] == "primary" else "D",
                "face": PRIMARY if row["role"] == "primary" else "white",
            }
        )
    _forest(ax_b, entries, xlabel="graded minus binary")
    ax_b.set_title("Graded disclosure (E02)", pad=14)
    ax_b.text(
        0.0,
        1.02,
        "rejected stratum only",
        transform=ax_b.transAxes,
        fontsize=6.6,
        style="italic",
        color=CONTROL,
        ha="left",
        va="bottom",
    )
    _panel_label(ax_b, "b")
    ax_b.set_xlim(-0.42, 0.42)

    # --- Panel C: the M1 objective that bounds any reading of panel b -------
    for p_value, style, colour in (("0.85", "-", INK), ("0.75", (0, (3, 2)), CONTROL)):
        points = sorted(
            ((float(r["d"]), float(r["expected_reward"])) for r in arms if abs(float(r["p"]) - float(p_value)) < 1e-12),
        )
        require(len(points) >= 2, f"Figure 2: E02 arm curve at p={p_value} has too few points")
        ax_c.plot(
            [d for d, _ in points],
            [v for _, v in points],
            linestyle=style,
            color=colour,
            linewidth=1.1,
            marker="o",
            markersize=2.6,
            zorder=3,
        )
    for p_value, colour, anchor in (("0.85", INK, (0.30, 0.905, "bottom")), ("0.75", CONTROL, (0.55, 0.792, "top"))):
        ax_c.text(anchor[0], anchor[1], f"$p={p_value}$", fontsize=6.4, color=colour, va=anchor[2], ha="left")
    ax_c.set_title("M1 objective", pad=14)
    _panel_label(ax_c, "c")
    ax_c.set_xlabel("disclosure $d$")
    ax_c.set_ylabel("expected reward $E[R(d)]$")
    ax_c.set_xlim(-0.06, 1.08)
    ax_c.set_xticks([0.0, 0.5, 1.0])
    ax_c.text(
        0.0,
        1.02,
        "affine in $d$",
        transform=ax_c.transAxes,
        fontsize=6.6,
        style="italic",
        color=CONTROL,
        ha="left",
        va="bottom",
    )

    fig.subplots_adjust(left=0.185, right=0.978, top=0.855, bottom=0.165, wspace=0.85)
    return save(fig, "Figure_2_early_feedback_and_graded_disclosure")


# ---------------------------------------------------------------------------
# Figure 3 - persistent-state learner/objective contrast map (E03)
# ---------------------------------------------------------------------------

CATEGORY_ORDER = ["learner_matches_objective", "learned_suboptimal_masking", "inconclusive"]
CATEGORY_COLOUR = {
    "learner_matches_objective": MATCHES,
    "learned_suboptimal_masking": SUBOPTIMAL,
    "inconclusive": INCONCLUSIVE,
}
CATEGORY_LABEL = {
    "learner_matches_objective": "learner matches objective",
    "learned_suboptimal_masking": "learned-suboptimal masking",
    "inconclusive": "inconclusive (Neutral visits inadequate)",
}


def _edges(values: np.ndarray) -> np.ndarray:
    mids = (values[:-1] + values[1:]) / 2.0
    return np.concatenate([[values[0] - (mids[0] - values[0])], mids, [values[-1] + (values[-1] - mids[-1])]])


def figure_3() -> list[Path]:
    rows = read_rows(DATA_DIR / "e03_grid_map.csv")
    summary = {r["publication_category"]: int(r["cell_count"]) for r in read_rows(DATA_DIR / "e03_grid_summary.csv")}

    p_values = np.array(sorted({float(r["p"]) for r in rows}))
    eta_values = np.array(sorted({float(r["eta"]) for r in rows}))
    require(
        len(p_values) * len(eta_values) == len(rows) == 357,
        f"Figure 3: grid is {len(p_values)} x {len(eta_values)} covering {len(rows)} rows, expected 21 x 17 = 357",
    )
    p_index = {value: i for i, value in enumerate(p_values)}
    eta_index = {value: i for i, value in enumerate(eta_values)}

    category = np.full((len(eta_values), len(p_values)), np.nan)
    objective_authentic = np.zeros_like(category)
    q_gap = np.full_like(category, np.nan)
    for row in rows:
        i, j = eta_index[float(row["eta"])], p_index[float(row["p"])]
        category[i, j] = CATEGORY_ORDER.index(row["publication_category"])
        objective_authentic[i, j] = 1.0 if row["objective_neutral_action"] == "authentic" else 0.0
        q_gap[i, j] = float(row["objective_neutral_q_gap_auth_minus_mask"])
    require(not np.isnan(category).any(), "Figure 3: tested grid has unfilled cells")

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.2, 3.4), gridspec_kw={"width_ratios": [1.0, 1.0]})
    p_edges, eta_edges = _edges(p_values), _edges(eta_values)

    # --- Panel A: contrast classification ----------------------------------
    cmap = matplotlib.colors.ListedColormap([CATEGORY_COLOUR[c] for c in CATEGORY_ORDER])
    ax_a.pcolormesh(
        p_edges,
        eta_edges,
        category,
        cmap=cmap,
        vmin=-0.5,
        vmax=len(CATEGORY_ORDER) - 0.5,
        edgecolors="white",
        linewidth=0.15,
    )
    ax_a.contour(
        p_values,
        eta_values,
        objective_authentic,
        levels=[0.5],
        colors=[INK],
        linewidths=1.1,
    )
    ax_a.set_xlabel("acceptance probability $p$")
    ax_a.set_ylabel(r"Stigmatized-to-Neutral recovery $\eta$")
    ax_a.set_title("Learner vs objective optimum (E03)", pad=7)
    _panel_label(ax_a, "a")

    handles = [
        Patch(facecolor=CATEGORY_COLOUR[c], edgecolor="white", linewidth=0.4,
              label=f"{CATEGORY_LABEL[c]} — {summary[c]}/357")
        for c in CATEGORY_ORDER
    ] + [Line2D([], [], color=INK, linewidth=1.1, label="full-information optimum switches to authenticity")]
    ax_a.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.24),
        ncol=1,
        handlelength=1.4,
        handleheight=0.9,
        labelspacing=0.35,
        borderaxespad=0.0,
    )

    # --- Panel B: exact objective Neutral Q gap -----------------------------
    # The gap is strongly asymmetric (roughly -6.6 to +0.85). A symmetric scale
    # would flatten the entire authenticity-favouring side, which is the region
    # of interest, so the diverging scale is anchored at zero and stretched
    # independently on each side. The colourbar carries the true values.
    mesh = ax_b.pcolormesh(
        p_edges,
        eta_edges,
        q_gap,
        cmap="RdBu_r",
        norm=matplotlib.colors.TwoSlopeNorm(
            vmin=float(np.nanmin(q_gap)), vcenter=0.0, vmax=float(np.nanmax(q_gap))
        ),
        edgecolors="white",
        linewidth=0.15,
    )
    ax_b.contour(p_values, eta_values, q_gap, levels=[0.0], colors=[INK], linewidths=1.1)
    ax_b.set_xlabel("acceptance probability $p$")
    ax_b.set_ylabel(r"recovery $\eta$")
    ax_b.set_title("Exact objective Neutral $Q$ gap", pad=7)
    _panel_label(ax_b, "b")
    bar = fig.colorbar(mesh, ax=ax_b, fraction=0.046, pad=0.03)
    bar.set_label(r"$Q(N, A_u) - Q(N, M)$", fontsize=7.0)
    bar.set_ticks([-6, -4, -2, 0, 0.4, 0.8])
    bar.ax.tick_params(labelsize=6.5, length=2.0)
    bar.outline.set_linewidth(0.5)

    fig.subplots_adjust(left=0.085, right=0.955, top=0.90, bottom=0.36, wspace=0.42)
    return save(fig, "Figure_3_persistent_state_contrast_map")


# ---------------------------------------------------------------------------
# Figure 4 - receptive-context discovery (E04) and comparison-cost displacement (E05)
# ---------------------------------------------------------------------------

E04_SERIES = [
    ("one_good", "flat_2k", PRIMARY, "-", "flat 2K", True),
    ("one_good", "hierarchical", SECONDARY, "-", "hierarchical", True),
    ("one_good", "global_mask", CONTROL, (0, (4, 2)), "global-mask control", False),
    ("proportional_25", "flat_2k", PRIMARY, (0, (1, 1.7)), "flat 2K, proportional", False),
    ("proportional_25", "hierarchical", SECONDARY, (0, (1, 1.7)), "hier., proportional", False),
]


def figure_4() -> list[Path]:
    curves = read_rows(DATA_DIR / "e04_k_response.csv")
    effects = {r["claim_id"]: r for r in read_rows(DATA_DIR / "e04_headline_effects.csv")}
    response = read_rows(DATA_DIR / "e05_response_vs_bf.csv")
    crossings = {r["architecture"]: r for r in read_rows(DATA_DIR / "e05_crossings.csv")}
    displacement = {r["quantity"]: r for r in read_rows(DATA_DIR / "e05_displacement.csv")}

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.2, 3.5))

    # --- Panel A: E04 K response -------------------------------------------
    for series, architecture, colour, style, label, band in E04_SERIES:
        points = sorted(
            ((int(r["K"]), float(r["master_mean"]), float(r["master_min"]), float(r["master_max"])) for r in curves
             if r["series"] == series and r["architecture"] == architecture),
        )
        require(len(points) == 5, f"Figure 4: {series}/{architecture} has {len(points)} K points, expected 5")
        ks = np.array([p[0] for p in points], dtype=float)
        mean = np.array([p[1] for p in points])
        if band:
            ax_a.fill_between(
                ks,
                [p[2] for p in points],
                [p[3] for p in points],
                color=colour,
                alpha=0.14,
                linewidth=0,
                zorder=2,
            )
        ax_a.plot(
            ks,
            mean,
            color=colour,
            linestyle=style,
            linewidth=1.5 if band else 1.0,
            marker="o" if band else "",
            markersize=3.2,
            label=label,
            zorder=4 if band else 3,
        )

    known_good = [r for r in curves if r["series"] == "known_good_reference"]
    require(len(known_good) == 1, "Figure 4: known-good reference row missing")
    ax_a.axhline(
        float(known_good[0]["master_mean"]),
        color=INK,
        linestyle=(0, (1, 2.5)),
        linewidth=0.9,
        label="known-good control",
        zorder=3,
    )

    ax_a.set_xscale("log", base=2)
    ax_a.set_xticks([1, 2, 4, 8, 16])
    ax_a.set_xticklabels(["1", "2", "4", "8", "16"])
    ax_a.set_xlabel("number of contexts $K$")
    ax_a.set_ylabel("settled on receptive-context authenticity")
    ax_a.set_ylim(-0.03, 1.06)
    ax_a.set_title("Receptive-context discovery (E04)", pad=14)
    ax_a.text(
        0.0,
        1.02,
        "one fixed receptive context unless noted",
        transform=ax_a.transAxes,
        fontsize=6.6,
        style="italic",
        color=CONTROL,
        ha="left",
        va="bottom",
    )
    _panel_label(ax_a, "a")
    ax_a.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.20),
        ncol=2,
        handlelength=1.9,
        labelspacing=0.30,
        columnspacing=1.0,
    )

    # Frozen K = 16 minus K = 1 contrasts, which are the primary E04 comparison.
    inset = ax_a.inset_axes([0.17, 0.13, 0.42, 0.28])
    contrast_entries = [
        ("E04-C6-FLAT", "flat 2K", PRIMARY),
        ("E04-C6-HIER", "hier.", SECONDARY),
        ("E04-C6-CONTROL-GLOBALMASK", "glob. mask", CONTROL),
    ]
    for y, (claim_id, label, colour) in enumerate(contrast_entries[::-1]):
        row = effects[claim_id]
        inset.plot([float(row["ci_low"]), float(row["ci_high"])], [y, y], color=colour, linewidth=1.2)
        inset.plot([float(row["estimate"])], [y], marker="o", markersize=3.0, color=colour, linestyle="none")
    inset.axvline(0.0, color=INK, linewidth=0.5, linestyle=(0, (3, 2)))
    inset.set_yticks(range(len(contrast_entries)))
    inset.set_yticklabels([label for _, label, _ in contrast_entries[::-1]], fontsize=5.6)
    inset.set_ylim(-0.6, len(contrast_entries) - 0.4)
    inset.set_xlabel("$K=16$ minus $K=1$", fontsize=5.8, labelpad=1.0)
    inset.tick_params(labelsize=5.4, length=1.8, pad=1.2)
    inset.locator_params(axis="x", nbins=3)

    # --- Panel B: E05 response against comparison cost ----------------------
    dense = [r for r in response if r["in_dense_range"] == "True"]
    for architecture, colour, style, label in (
        ("flat_2k", PRIMARY, "-", "flat 2K"),
        ("hierarchical", SECONDARY, (0, (4, 2)), "hierarchical"),
    ):
        points = sorted(
            ((float(r["bf"]), float(r["pooled_response"]), float(r["master_min"]), float(r["master_max"]))
             for r in dense if r["architecture"] == architecture),
        )
        require(points, f"Figure 4: no dense-range points for {architecture}")
        bfs = np.array([p[0] for p in points])
        ax_b.fill_between(
            bfs, [p[2] for p in points], [p[3] for p in points], color=colour, alpha=0.14, linewidth=0, zorder=2
        )
        ax_b.plot(
            bfs,
            [p[1] for p in points],
            color=colour,
            linestyle=style,
            linewidth=1.5,
            marker="o",
            markersize=2.8,
            label=label,
            zorder=4,
        )

    ax_b.axhline(0.5, color=INK, linewidth=0.7, linestyle=(0, (4, 3)), zorder=1)

    learned = float(crossings["flat_2k"]["transition_bf"])
    ci_low, ci_high = float(crossings["flat_2k"]["ci_low"]), float(crossings["flat_2k"]["ci_high"])
    objective = float(crossings["flat_2k"]["analytic_threshold_bf"])
    ax_b.axvspan(ci_low, ci_high, color=PRIMARY, alpha=0.30, linewidth=0, zorder=3)
    ax_b.axvline(learned, color=PRIMARY, linewidth=1.1, zorder=5)
    ax_b.axvline(objective, color=INK, linewidth=1.1, linestyle=(0, (5, 2)), zorder=5)

    ax_b.annotate(
        "",
        xy=(objective, 0.93),
        xytext=(learned, 0.93),
        arrowprops={"arrowstyle": "<|-|>", "linewidth": 0.9, "color": INK, "shrinkA": 0, "shrinkB": 0},
    )
    ax_b.text(
        (learned + objective) / 2,
        0.955,
        f"displacement {abs(float(displacement['displacement_objective_minus_learned']['value'])):.6f}",
        fontsize=6.6,
        ha="center",
        va="bottom",
    )
    ax_b.text(
        learned - 0.0125,
        1.28,
        f"learned crossing\n{learned:.6f}\n[{ci_low:.6f}, {ci_high:.6f}]",
        fontsize=6.2,
        color=PRIMARY,
        ha="left",
        va="top",
        linespacing=1.6,
    )
    ax_b.text(
        objective + 0.010,
        1.28,
        f"exact objective crossover\n$8/17 = {objective:.6f}$",
        fontsize=6.2,
        ha="left",
        va="top",
        linespacing=1.6,
    )
    ax_b.text(
        objective + 0.010,
        0.58,
        "hierarchical response is\nleft-censored: already below\n0.5 at the lower dense\nboundary, so no in-range\ncrossing is estimable",
        fontsize=6.2,
        color=SECONDARY,
        ha="left",
        va="top",
        linespacing=1.6,
    )

    ax_b.set_xlabel("comparison cost $b_f$")
    ax_b.set_ylabel("modal arm is receptive-context authentic")
    ax_b.set_xlim(0.291, 0.662)
    ax_b.set_ylim(-0.03, 1.32)
    ax_b.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax_b.set_title("Comparison-cost displacement (E05)", pad=14)
    _panel_label(ax_b, "b")
    ax_b.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=2, handlelength=1.9)

    fig.subplots_adjust(left=0.088, right=0.988, top=0.905, bottom=0.325, wspace=0.34)
    return save(fig, "Figure_4_discovery_and_comparison_cost")


def build_all() -> list[Path]:
    apply_style()
    outputs: list[Path] = []
    for builder in (figure_1, figure_2, figure_3, figure_4):
        outputs.extend(builder())
    return outputs
