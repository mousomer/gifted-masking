"""Render ten integrated-article figures from frozen evidence, without experiments.

Edit all visible wording in figure_text.py; this file owns selectors and layout.
No-argument invocation rebuilds PNG/SVG files in this revision's figures/.
Examples (from the repository root, with the required workspace interpreter):

  python -B projects/frontiers_article/integrated_article_20261004/generate_figures.py --list
  python -B projects/frontiers_article/integrated_article_20261004/generate_figures.py
  python -B projects/frontiers_article/integrated_article_20261004/generate_figures.py --figure 8 --preview-dir /private/tmp/article-figure-preview

The six earlier drawing functions are loaded read-only from the preserved
revision. Local text, number mapping, PNG/SVG saving and provenance replace
their presentation hooks. The scientific selectors/calculations are unchanged.
Four added figures show the exact M2/M3 specifications and archived E03 counts.
Public read-only helpers grid_data() and sensitivity_data() expose the complete
plot inputs for focused tests. Nothing imports simulation/estimator modules.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from string import Formatter
import sys
import tempfile
import types

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = HERE.parent / "revision_20260929"
CANONICAL_OUT = HERE / "figures"
PUB = "projects/frontiers_article/publication_v1/data/"
CELLS = "results/summaries/frontiers_m2_regime_replication_v1_cells.csv"
REUSED_NUMBERS = {1: 1, 2: 4, 3: 5, 4: 6, 5: 9, 6: 10}
STEMS = {
    1: "figure_01_overview",
    2: "figure_02_state_kernel",
    3: "figure_03_architectures",
    4: "figure_04_weighting_history_information",
    5: "figure_05_graded_engagement_intensity",
    6: "figure_06_dynamic_thresholds_persistence",
    7: "figure_07_dynamic_grid",
    8: "figure_08_sensitivity_matrix",
    9: "figure_09_context_encounter_sustained_use",
    10: "figure_10_learned_boundary_actual_masking",
}
NAVY, RED, TEAL, GREY = "#245077", "#ac433c", "#287769", "#60666e"


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# A private package avoids modifying sys.path or colliding with another figure
# catalog already imported by a test runner. The legacy module's relative text
# import resolves to this revision's editable catalog by design.
_PACKAGE = "_gifted_integrated_article_figures_20261004"
if _PACKAGE not in sys.modules:
    _package = types.ModuleType(_PACKAGE)
    _package.__path__ = [str(HERE)]
    sys.modules[_PACKAGE] = _package
_text = _load_module(_PACKAGE + ".figure_text", HERE / "figure_text.py")
FIGURE_TEXT, SHARED_TEXT = _text.FIGURE_TEXT, _text.SHARED_TEXT
_legacy = _load_module(_PACKAGE + ".legacy", OLD / "generate_figures.py")

INPUT_HASHES = dict(_legacy.HASHES)
INPUT_HASHES.update({
    PUB + "e03_grid_map.csv": "c5def710116248b60ffcc347fa408519ce5d9094547e486fc73f2388e5babbab",
    PUB + "e03_grid_summary.csv": "90aebefa0fe66c1f3092879d365c2ede798e71114a1f3b0bb74ee6df083f096a",
    "src/gifted_masking/models/m2.py": "42b39f1bcf8aac96f830acd5747a215bac24c36a2a2be773294022c019170c5e",
    "src/gifted_masking/models/m3.py": "091824551b7c6cc5d7ad1ca04d787c82ac5763345d5f09f4eb735dc2f6f381c1",
    "projects/frontiers_article/revision_20260929/SUPPLEMENTARY_METHODS.md": "f4c9a5328d03db90f8ae5556302834a9c00950bba6316ff826588eadadc74569",
    "projects/frontiers_article/revision_20260929/generate_figures.py": "476b4e8ffafdee6dcb1c1134c91f5fdb1c5f1204834d860dfe37f3ca3e304678",
})

SENTINELS = ((.4, 0), (.55, 0), (.75, 0), (.55, .2), (.9, .2))
SETTINGS = (("baseline", None), ("T", 2000), ("T", 5000), ("n", 320),
            ("final_window_fraction", .1), ("final_window_fraction", .4),
            ("lambda", .5), ("lambda", 2.5), ("q0", .75),
            ("alpha", .03), ("alpha", .3), ("tau", .1), ("tau", .6),
            ("gamma", .5), ("gamma", .99))
EXPECTED_TOTALS = [25, 25, 25, 25, 25, 25, 25, 25, 25, 18, 25, 25, 21, 10, 25]
NEW_TEXT_KEYS = {
    2: "title flow_heading action_heading reward_heading next_heading neutral accepted stigmatized n_mask n_auth_success n_auth_reject a_mask a_auth s_mask s_auth_success s_auth_fail r_mask r_auth r_reject r_s_mask r_s_reject next_n next_a next_s next_turnover next_escape reward_order condition_note",
    3: "title key flat_title hier_title global_title known_title softmax context_softmax behavior_softmax context_format mask auth flat_update hier_update global_update known_context known_update shared_mask auth_context_format reward_key",
    7: "title xlabel ylabel suboptimal agreement inconclusive count_format design scope",
    8: "title xlabel column_format row_labels cell_format total_heading total_format colorbar scope discount_note",
}
OUT = CANONICAL_OUT
PROVENANCE = {}
CURRENT_NUMBER = 0


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def verify_sources():
    """Fail before drawing if any frozen evidence/specification source changed."""
    for name, expected in INPUT_HASHES.items():
        assert sha(ROOT / name) == expected, f"Frozen source hash mismatch: {name}"


def grid_data():
    """Return frozen E03 grid rows, axes and counts; assert a complete partition."""
    data = rows(PUB + "e03_grid_map.csv")
    counts = dict(Counter(r["publication_category"] for r in data))
    expected = {"learned_suboptimal_masking": 243,
                "learner_matches_objective": 107, "inconclusive": 7}
    assert len(data) == 357 and len({r["parameter_cell_id"] for r in data}) == 357
    assert counts == expected
    summary = {r["publication_category"]: int(r["cell_count"])
               for r in rows(PUB + "e03_grid_summary.csv")}
    assert counts == summary
    ps = sorted({float(r["p"]) for r in data})
    etas = sorted({float(r["eta"]) for r in data})
    assert len(ps) == 21 and len(etas) == 17
    assert len({(float(r["p"]), float(r["eta"])) for r in data}) == 357
    assert np.allclose(ps, np.arange(21) * .05)
    assert np.allclose(etas, np.arange(17) * .05)
    for row in data:
        if row["publication_category"] == "learned_suboptimal_masking":
            assert row["objective_neutral_action"] == "authentic"
            assert row["learned_neutral_action"] == "mask"
            assert row["neutral_visit_adequate_master_count"] == "5"
    return {"rows": data, "p": ps, "eta": etas, "counts": counts}


def sensitivity_data():
    """Return exact 15×5 master-count matrix plus selected archived records.

    Each entry counts five master classifications. The excluded sixth sentinel
    is an agreement/boundary control. Other outcomes must be oracle agreements;
    a new inconclusive or unexpected class fails closed rather than disappearing.
    """
    source = [r for r in rows(CELLS) if r["component"] == "sentinels"]
    matrix, selected, details = [], [], []
    expected_masters = set(range(2026081301, 2026081306))
    for factor, value in SETTINGS:
        row_counts = []
        for p, eta in SENTINELS:
            cell = [r for r in source if r["sensitivity_name"] == factor
                    and (float(r["p"]), float(r["eta"])) == (p, eta)
                    and (value is None or float(r[factor]) == value)]
            assert len(cell) == 5, (factor, value, p, eta, len(cell))
            assert {int(r["master_seed"]) for r in cell} == expected_masters
            classes = Counter(r["classification"] for r in cell)
            assert set(classes) <= {"learned_suboptimal_masking", "learner_matches_objective"}
            count = classes["learned_suboptimal_masking"]
            row_counts.append(count)
            selected.extend(cell)
            details.append({"factor": factor, "value": value, "p": p, "eta": eta,
                            "suboptimal_master_count": count, "classifications": dict(classes)})
        matrix.append(row_counts)
    totals = [sum(row) for row in matrix]
    assert len(selected) == 15 * 5 * 5 and totals == EXPECTED_TOTALS
    assert matrix[9] == [5, 5, 3, 5, 0]
    assert matrix[12] == [5, 5, 4, 5, 2]
    assert matrix[13] == [0, 0, 5, 0, 5]
    return {"matrix": matrix, "totals": totals, "settings": list(SETTINGS),
            "sentinels": list(SENTINELS), "records": selected, "details": details}


def record(panel, source, selector, values, note=""):
    PROVENANCE["panels"][panel] = {"source": source, "selector": selector,
                                    "values": values, "note": note}


def _legacy_record(panel, source, selector, values, note=""):
    panel = re.sub(r"\d+(?=[A-Z])", lambda m: str(REUSED_NUMBERS[int(m[0])]), panel)
    record(panel, source, selector, values, note)


def _box(ax, x, y, w, h, text, *, color=NAVY, fill="#f0f5f8", size=10, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=.008,rounding_size=.014",
                              linewidth=1, edgecolor=color, facecolor=fill))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, weight=weight)


def _arrow(ax, start, end):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=10,
                               linewidth=1, color=GREY))


def fig2():
    """Draw the exact M2 reward-first transition kernel; edit FIGURE_TEXT[2]."""
    t = FIGURE_TEXT[2]
    fig, ax = plt.subplots(figsize=(8.5, 6.1))
    ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis("off")
    ax.text(.02, .975, t["title"], fontsize=12, weight="bold", va="top")
    for x, key in [(.105, "flow_heading"), (.40, "action_heading"),
                   (.66, "reward_heading"), (.86, "next_heading")]:
        ax.text(x, .885, t[key], ha="center", fontsize=9, color=GREY, weight="bold")
    for label, y, h, color in [("neutral", .605, .24, NAVY),
                              ("accepted", .412, .155, TEAL),
                              ("stigmatized", .135, .24, RED)]:
        _box(ax, .01, y, .185, h, t[label], color=color, size=10, weight="bold")
    specs = [(.81, "n_mask", "r_mask", "next_n"),
             (.73, "n_auth_success", "r_auth", "next_a"),
             (.65, "n_auth_reject", "r_reject", "next_s"),
             (.53, "a_mask", "r_mask", "next_turnover"),
             (.45, "a_auth", "r_auth", "next_turnover"),
             (.34, "s_mask", "r_s_mask", "next_escape"),
             (.26, "s_auth_success", "r_auth", "next_a"),
             (.18, "s_auth_fail", "r_s_reject", "next_escape")]
    for y, action, reward, nxt in specs:
        ax.text(.225, y, t[action], va="center", fontsize=9.5)
        ax.text(.66, y, t[reward], ha="center", va="center", fontsize=11)
        _arrow(ax, (.71, y), (.745, y))
        ax.text(.86, y, t[nxt], ha="center", va="center", fontsize=9.5)
    ax.text(.5, .073, t["reward_order"], ha="center", fontsize=10, weight="bold")
    ax.text(.5, .028, t["condition_note"], ha="center", fontsize=9, color=GREY)
    fig.subplots_adjust(left=.035, right=.98, top=.98, bottom=.025)
    record("2", ["src/gifted_masking/models/m2.py",
                  "projects/frontiers_article/revision_20260929/SUPPLEMENTARY_METHODS.md"],
           "transition_step; supplementary S4.1", specs,
           "Specification diagram. Turnover is restricted to current Accepted; escape to non-redeemed Stigmatized paths.")
    save(fig)


def fig3():
    """Draw four M3 representations with illustrative K=3; edit FIGURE_TEXT[3]."""
    t = FIGURE_TEXT[3]
    fig, axes = plt.subplots(2, 2, figsize=(8.5, 6.7))
    for ax in axes.flat:
        ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis("off")
    fig.text(.5, .98, t["title"], ha="center", va="top", fontsize=12, weight="bold")
    fig.text(.5, .939, t["key"], ha="center", fontsize=10, color=GREY)
    a, b, c, d = axes.flat
    for ax, key in [(a, "flat_title"), (b, "hier_title"), (c, "global_title"), (d, "known_title")]:
        ax.text(0, .96, t[key], fontsize=11, weight="bold", va="top")
    _box(a, .28, .70, .44, .11, t["softmax"])
    for i, x in enumerate([.02, .36, .70], 1):
        a.text(x + .14, .29, t["context_format"].format(index=i), ha="center", fontsize=9)
        for text, offset in [(t["mask"], 0), (t["auth"], .15)]:
            _box(a, x + offset, .37, .12, .13, text)
            _arrow(a, (.5, .69), (x + offset + .06, .515))
    a.text(.5, .18, t["flat_update"], ha="center", fontsize=9.5)
    _box(b, .26, .73, .48, .10, t["context_softmax"])
    for i, x in enumerate([.02, .36, .70], 1):
        _box(b, x, .51, .28, .11, t["context_format"].format(index=i), size=9)
        _arrow(b, (.5, .72), (x + .14, .63))
        for text, offset in [(t["mask"], 0), (t["auth"], .15)]:
            _box(b, x + offset, .25, .12, .11, text)
            _arrow(b, (x + .14, .50), (x + offset + .06, .37))
    b.text(.5, .19, t["behavior_softmax"], ha="center", fontsize=8.5)
    b.text(.5, .073, t["hier_update"], ha="center", fontsize=9.5, va="center")
    _box(c, .28, .70, .44, .11, t["softmax"])
    for i, x in enumerate([.015, .27, .525, .78]):
        label = t["shared_mask"] if i == 0 else t["auth_context_format"].format(index=i)
        w = .205 if i == 0 else .19
        _box(c, x, .36, w, .15, label, size=9.5)
        _arrow(c, (.5, .69), (x + w / 2, .525))
    c.text(.5, .18, t["global_update"], ha="center", fontsize=9.5)
    _box(d, .17, .68, .66, .13, t["known_context"], color=TEAL)
    for x, text in [(.26, t["mask"]), (.61, t["auth"])]:
        _box(d, x, .36, .15, .15, text, color=TEAL)
        _arrow(d, (.5, .67), (x + .075, .525))
    d.text(.5, .18, t["known_update"], ha="center", fontsize=9.5)
    fig.text(.5, .035, t["reward_key"], ha="center", fontsize=10, color=NAVY)
    fig.subplots_adjust(left=.055, right=.98, bottom=.09, top=.90, hspace=.22, wspace=.15)
    record("3A-3D", ["src/gifted_masking/models/m3.py",
                      "projects/frontiers_article/revision_20260929/SUPPLEMENTARY_METHODS.md"],
           "simulate;simulate_hierarchical;simulate_global_mask;simulate_fixed_good_pond; supplementary S5.2",
           {"illustrative_K": 3, "flat_arms": 6, "global_arms": 4, "known_good_arms": 2,
            "reward_classes": {"mask": .75, "good_authentic": 1.15, "bad_authentic": -.8}},
           "Schematic only. K=3 is illustrative, not an additional simulated condition.")
    save(fig)


def fig7():
    """Plot the categorical 357-cell map without smoothing; edit FIGURE_TEXT[7]."""
    t, data = FIGURE_TEXT[7], grid_data()
    keys = ["learned_suboptimal_masking", "learner_matches_objective", "inconclusive"]
    labels = [t["suboptimal"], t["agreement"], t["inconclusive"]]
    colors = [RED, TEAL, "#e1e3e6"]
    grid = np.full((17, 21), -1, dtype=int)
    for row in data["rows"]:
        grid[round(float(row["eta"]) / .05), round(float(row["p"]) / .05)] = keys.index(row["publication_category"])
    assert (grid >= 0).all()
    fig, ax = plt.subplots(figsize=(8.5, 6.0))
    ax.imshow(grid, cmap=ListedColormap(colors), norm=BoundaryNorm([-.5, .5, 1.5, 2.5], 3),
              origin="lower", aspect="auto", extent=(-.025, 1.025, -.025, .825), interpolation="nearest")
    ax.set(xlabel=t["xlabel"], ylabel=t["ylabel"], xticks=np.arange(0, 1.01, .2), yticks=np.arange(0, .81, .2))
    ax.set_xticks(np.arange(-.025, 1.026, .05), minor=True)
    ax.set_yticks(np.arange(-.025, .826, .05), minor=True)
    ax.grid(which="minor", color="white", linewidth=.4); ax.tick_params(which="minor", length=0)
    ax.set_title(t["title"], fontsize=12, pad=28, loc="left")
    ax.text(0, 1.027, t["design"], transform=ax.transAxes, fontsize=10, color=GREY)
    handles = [Patch(facecolor=color, label=t["count_format"].format(label=label, count=data["counts"][key]))
               for key, label, color in zip(keys, labels, colors)]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(.5, .058), ncol=1, fontsize=10, frameon=False)
    fig.text(.5, .02, t["scope"], ha="center", fontsize=10, color=GREY)
    fig.subplots_adjust(left=.11, right=.98, top=.85, bottom=.27)
    record("7", [PUB + "e03_grid_map.csv", PUB + "e03_grid_summary.csv"],
           "all 357 frozen publication_category rows; p21×eta17; no reclassification",
           {"counts": data["counts"], "p": data["p"], "eta": data["eta"],
            "category_order": keys, "matrix": grid.tolist()},
           "Each square is a tested parameter cell. Inconclusive cells retained; no smoothing or inferred boundary.")
    save(fig)


def fig8():
    """Display five-master counts for 15 separate settings; edit FIGURE_TEXT[8]."""
    t, data = FIGURE_TEXT[8], sensitivity_data()
    matrix = np.asarray(data["matrix"])
    colors = ["#f4f5f6", "#dce7ef", "#b8d0df", "#87aec6", "#507fa1", NAVY]
    fig, ax = plt.subplots(figsize=(8.5, 7.0))
    cmap, norm = ListedColormap(colors), BoundaryNorm(np.arange(-.5, 6), 6)
    shown = ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto", interpolation="nearest")
    ax.set_xticks(range(5), [t["column_format"].format(p=p, eta=eta) for p, eta in SENTINELS])
    ax.set_yticks(range(15), t["row_labels"])
    ax.tick_params(axis="both", length=0, labelsize=10)
    ax.xaxis.tick_top(); ax.xaxis.set_label_position("top"); ax.set_xlabel(t["xlabel"], labelpad=12, fontsize=10)
    ax.set_xticks(np.arange(-.5, 5, 1), minor=True); ax.set_yticks(np.arange(-.5, 15, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1); ax.tick_params(which="minor", length=0)
    for i, row in enumerate(matrix):
        for j, count in enumerate(row):
            ax.text(j, i, t["cell_format"].format(count=count), ha="center", va="center",
                    fontsize=10, color="white" if count >= 4 else NAVY)
        ax.text(5.15, i, t["total_format"].format(count=data["totals"][i]),
                ha="left", va="center", fontsize=10,
                weight="bold" if data["totals"][i] != 25 else "normal")
    ax.text(5.15, -1.05, t["total_heading"], ha="left", va="center", fontsize=10, weight="bold")
    fig.text(.055, .976, t["title"], fontsize=12, weight="bold", va="top")
    cax = fig.add_axes([.36, .112, .39, .019])
    colorbar = fig.colorbar(shown, cax=cax, orientation="horizontal", ticks=range(6))
    colorbar.ax.tick_params(labelsize=9); colorbar.set_label(t["colorbar"], fontsize=9, labelpad=4)
    fig.text(.5, .034, t["scope"], ha="center", fontsize=9, color=GREY)
    fig.text(.5, .009, t["discount_note"], ha="center", fontsize=9, color=GREY)
    fig.subplots_adjust(left=.315, right=.845, top=.837, bottom=.19)
    record("8", CELLS, "component=sentinels; five explicit disagreement sentinels; 15 separate settings; five masters each",
           {key: value for key, value in data.items() if key != "records"},
           "375 archived classifications; integer count display, not an uncertainty estimate. Gamma also changes the objective.")
    save(fig)


def _compact_context_layout(fig):
    """Reflow the unchanged six E04 panels to a printable 3-column×2-row grid."""
    fig.set_size_inches(9.6, 6.25)
    xs, ys, width, height = [.085, .410, .735], [.565, .125], .235, .285
    for index, ax in enumerate(fig.axes):
        ax.set_position([xs[index % 3], ys[index // 3], width, height])
        ax.tick_params(labelsize=10)
        ax.xaxis.label.set_size(10.5); ax.yaxis.label.set_size(10.5)
        ax._left_title.set_fontsize(11); ax._left_title.set_position((0, 1.06))
        for artist in ax.texts:
            artist.set_fontsize(10)
        legend = ax.get_legend()
        if legend:
            for item in legend.get_texts():
                item.set_fontsize(9)
        if index in (2, 3):
            # Reserve headroom for the two-line legends without placing them
            # over percentage labels. Ticks remain limited to 0..100 percent.
            ax.set_ylim(0, 170)
    # Wrap long axis labels and legends locally through the editable catalog;
    # only layout changes here, never values, selectors or the number of panels.


def _assert_text_on_canvas(fig):
    fig.canvas.draw(); renderer = fig.canvas.get_renderer()
    artists = list(fig.texts)
    for ax in fig.axes:
        artists.extend([*ax.texts, ax.title, ax._left_title, ax._right_title,
                        ax.xaxis.label, ax.yaxis.label])
    clipped = []
    for artist in artists:
        if artist.get_visible() and artist.get_text().strip():
            box = artist.get_window_extent(renderer)
            if box.x0 < -1 or box.y0 < -1 or box.x1 > fig.bbox.width + 1 or box.y1 > fig.bbox.height + 1:
                clipped.append(artist.get_text())
    assert not clipped, f"Figure {CURRENT_NUMBER} text exceeds canvas: {clipped}"


def save(fig, unused_legacy_stem=None):
    """Write only local PNG/SVG outputs, with deterministic metadata and hashes."""
    if CURRENT_NUMBER == 9:
        _compact_context_layout(fig)
    _assert_text_on_canvas(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "svg"):
        destination = OUT / f"{STEMS[CURRENT_NUMBER]}.{extension}"
        metadata = {"Date": None, "Creator": "Integrated frozen-evidence article"} if extension == "svg" else {"Software": "Integrated frozen-evidence article"}
        fig.savefig(destination, dpi=240, facecolor="white", metadata=metadata)
        PROVENANCE["outputs"][str(destination.relative_to(ROOT)) if destination.is_relative_to(ROOT) else str(destination)] = sha(destination)
    plt.close(fig)


def validate_text_catalog():
    """Validate all ten sections and inherited text-template contracts."""
    if set(FIGURE_TEXT) != set(STEMS):
        raise ValueError("Text catalog must contain exactly figures 1..10")
    _legacy.validate_text_catalog(SHARED_TEXT, {old: FIGURE_TEXT[new] for old, new in REUSED_NUMBERS.items()})
    for number in (2, 3, 7, 8):
        if not isinstance(FIGURE_TEXT[number], dict) or set(FIGURE_TEXT[number]) != set(NEW_TEXT_KEYS[number].split()):
            raise ValueError(f"FIGURE_TEXT[{number}]: missing or unexpected keys")
        for key, value in FIGURE_TEXT[number].items():
            valid = isinstance(value, str)
            if number == 8 and key == "row_labels":
                valid = isinstance(value, list) and len(value) == 15 and all(isinstance(x, str) for x in value)
            if not valid:
                raise ValueError(f"FIGURE_TEXT[{number}][{key}]: invalid text type")
    templates = {(3, "context_format"): {"index": 1}, (3, "auth_context_format"): {"index": 1},
                 (7, "count_format"): {"label": "test", "count": 243},
                 (8, "column_format"): {"p": .4, "eta": 0},
                 (8, "cell_format"): {"count": 5}, (8, "total_format"): {"count": 25}}
    for (number, key), arguments in templates.items():
        value = FIGURE_TEXT[number][key]
        try:
            fields = {field for _, field, _, _ in Formatter().parse(value) if field is not None}
            if fields != set(arguments):
                raise ValueError(f"expected placeholders {sorted(arguments)}")
            value.format(**arguments)
        except (ValueError, KeyError, TypeError, IndexError, AttributeError) as exc:
            raise ValueError(f"FIGURE_TEXT[{number}][{key}]: invalid format ({exc})") from exc


def resolve_preview_dir(path):
    """Accept only an isolated absolute child of repo/tmp or a system temp root."""
    destination = Path(path).expanduser()
    if not destination.is_absolute():
        raise ValueError("Preview path must be absolute")
    destination = destination.resolve()
    roots = {(ROOT / "tmp").resolve(), Path("/private/tmp").resolve(), Path(tempfile.gettempdir()).resolve()}
    if not any(destination != root and destination.is_relative_to(root) for root in roots):
        raise ValueError("Preview path must be a child of repo/tmp or a system temporary directory")
    if destination.is_relative_to(ROOT) and not destination.is_relative_to((ROOT / "tmp").resolve()):
        raise ValueError("Preview path overlaps protected repository content")
    paths = [destination / "FIGURE_PROVENANCE.json", destination / "figures"]
    paths.extend(destination / "figures" / f"{stem}.{extension}"
                 for stem in STEMS.values() for extension in ("png", "svg"))
    if any(not path.resolve().is_relative_to(destination) for path in paths):
        raise ValueError("Preview output symlink escapes its isolated directory")
    if destination.exists() and not destination.is_dir():
        raise ValueError("Preview path is not a directory")
    return destination


def render_figures(figure_numbers=None, preview_dir=None):
    """Render all ten canonical outputs, or a selected isolated preview."""
    global OUT, PROVENANCE, CURRENT_NUMBER
    if figure_numbers is not None and preview_dir is None:
        raise ValueError("Selecting figures requires --preview-dir")
    selected = list(STEMS) if figure_numbers is None else list(figure_numbers)
    if not selected or any(type(number) is not int or number not in STEMS for number in selected):
        raise ValueError("Figure numbers must be integers 1..10")
    selected = sorted(set(selected))
    preview = resolve_preview_dir(preview_dir) if preview_dir is not None else None
    validate_text_catalog(); verify_sources()
    OUT = preview / "figures" if preview is not None else CANONICAL_OUT
    PROVENANCE = {"article": "integrated_article_20261004", "selected_figures": selected,
                  "mode": "preview" if preview else "canonical", "inputs": INPUT_HASHES,
                  "method": "Frozen-data display and exact specification diagrams; no simulations, refits or bootstrap",
                  "panels": {}, "outputs": {}}
    _legacy.style()
    plt.rcParams.update({"svg.hashsalt": "integrated-article-20261004", "svg.fonttype": "none"})
    _legacy.FIGURE_TEXT = {old: FIGURE_TEXT[new] for old, new in REUSED_NUMBERS.items()}
    _legacy.SHARED_TEXT = SHARED_TEXT; _legacy.LABELS = SHARED_TEXT["architectures"]
    _legacy.record = _legacy_record; _legacy.save = save
    inherited = {new: _legacy.FIGURES[old][0] for old, new in REUSED_NUMBERS.items()}
    added = {2: fig2, 3: fig3, 7: fig7, 8: fig8}
    for CURRENT_NUMBER in selected:
        (inherited | added)[CURRENT_NUMBER]()
    PROVENANCE["generator_sha256"] = sha(Path(__file__))
    PROVENANCE["text_source"] = str((HERE / "figure_text.py").relative_to(ROOT))
    PROVENANCE["text_sha256"] = sha(HERE / "figure_text.py")
    PROVENANCE["captions_sha256"] = sha(HERE / "FIGURE_CAPTIONS.md")
    manifest_root = preview if preview else HERE
    manifest_root.mkdir(parents=True, exist_ok=True)
    (manifest_root / "FIGURE_PROVENANCE.json").write_text(json.dumps(PROVENANCE, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return PROVENANCE


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List numbered figures without reading evidence or writing outputs")
    parser.add_argument("--figure", type=int, choices=tuple(STEMS), action="append", help="Select a preview figure; repeatable")
    parser.add_argument("--preview-dir", type=Path, help="Isolated absolute preview directory; required with --figure")
    args = parser.parse_args(argv)
    if args.list:
        if args.figure is not None or args.preview_dir is not None:
            parser.error("--list cannot be combined with render options")
        for number, stem in STEMS.items():
            print(f"{number:2d}  {stem}  |  FIGURE_TEXT[{number}]")
        return
    try:
        manifest = render_figures(args.figure, args.preview_dir)
    except (ValueError, AssertionError) as exc:
        parser.error(str(exc))
    print(f"Rendered {len(manifest['selected_figures'])} figures as PNG/SVG; mode={manifest['mode']}")


if __name__ == "__main__":
    main()
