"""Editable visible wording for the six supported-claims revision figures.

Edit this file, not the archived data or plotting functions, to change labels.
Each numbered entry follows its figure's panel letters. ``\n`` inserts a line
break; keep breaks when fitting long text into the fixed publication layout.
Strings ending in ``_format`` use Python ``str.format``: preserve the named
placeholders (and braces used for Matplotlib math text) when changing wording.
Numbers in ordinary strings are science-linked labels, not recalculations:
changing them requires checking the evidence and caption, not just the style.
The generator validates catalog keys/types and format placeholders before any
output is written. No data selectors, numerical calculations or paths live here.
"""

# Shared wording appears in more than one panel or figure.
SHARED_TEXT = {
    "panel_title_format": "{letter}  {text}",
    "architectures": {
        "flat_2k": "Flat 2K",
        "hierarchical": "Hierarchical",
        "global_mask": "Global mask",
    },
    "final_window_masking_percent": "Final-window masking (%)",
    "good_authentic_modal_percent": "Good-authentic modal classification (%)",
    "comparison_cost": "Comparison cost bf",
}

FIGURE_TEXT = {
    1: {
        "A": {
            "heading": "A  Mechanisms shape the value and use of opportunity",
            "valuation_box": "Valuation and feedback\nE01: weighting, history,\ninformation",
            "action_box": "Action representation\nE02: independently\nlearned levels",
            "social_box": "Persistent social\nconsequences\nE03: future-state value",
            "allocation_box": "Learned values and action allocation\nEngagement | intensity | concealment",
            "crossing_note": "E05: learned modal crossing differs from objective indifference",
        },
        "B": {
            "heading": "B  Different achievements in a receptive-context search (E04)",
            "available_box": "Receptive option\nis available",
            "encountered_box": "Accepted authenticity\nhas been encountered",
            "used_box": "Receptive option\nis used repeatedly",
            "footer": "Action/context representation affects the links; one success does not guarantee sustained use.",
        },
    },
    2: {
        "A": {
            "title": "Weighting at fixed\nreceptivity (p = .65)",
            "ticks": [r"$\lambda=0.5$", r"$\lambda=2.5$"],
            "bar_format": "{value:.2f}%",
            # Science-linked estimate and confidence interval from archived E01.
            "effect_note": "+40.30 percentage points\n95% CI [39.54, 41.06]",
        },
        "B": {
            "title": "Subjective indifference\nmoves with weighting",
            "transformed_legend": "Transformed-reward threshold",
            "objective_legend": "Objective threshold .7167",
            "xlabel": r"Negative-outcome weight $\lambda$",
            "ylabel": "Receptivity threshold",
        },
        "C": {
            "title": "History changes sampling",
            "sampling_outcome": "Post-initial authentic\nsampling",
            "masking_outcome": "Final-window\nmasking",
            "xlabel": "Rejected minus accepted\n(percentage points)",
        },
        "D": {
            "title": "Information reduces\nmasking",
            "forced_outcome": "5% forced\nauthentic exposure",
            "counterfactual_outcome": "Counterfactual\nauthentic feedback",
            "xlabel": "Final-masking reduction\n(percentage points)",
        },
    },
    3: {
        "shared": {
            "receptivity_legend_format": "p = {p:.2f}",
            "xlabel": "Disclosure level d",
        },
        "A": {"title": "The optimal endpoint is unchanged", "ylabel": "Expected objective reward"},
        "B": {"title": "Partial disclosure has lower exposure", "ylabel": "Realized reward variance"},
        "C": {
            "title": "Engagement rises while endpoint use and intensity fall",
            "engagement_outcome": "Any disclosure (post-initial)",
            "endpoint_outcome": "Full authenticity (final window)",
            "modal_outcome": "Unique full-authentic mode",
            "intensity_outcome": "Mean disclosure intensity (full horizon)",
            "xlabel": "Graded minus binary (percentage points of the defined outcome)",
        },
    },
    4: {
        "A": {
            "title": "Future states move the optimum",
            "static_tick": "Static M0",
            "dynamic_tick_format": "Dynamic: escape {eta:g}",
            "bar_format": "{value:.3f}",
            "xlabel": "Objective receptivity threshold",
        },
        "B": {
            "title": "Persistence at 5,000 steps",
            "bar_format": "{value:.2f}",
            "sentinel_tick_format": "{p:g}\n{eta:g}",
            "xlabel": "Sentinel receptivity p / escape rate eta",
            "ylabel": "Neutral-state masking (%)",
            "optimality_note": "Authenticity is dynamically optimal\nat all five sentinels",
        },
    },
    5: {
        "shared": {
            "xlabel": "Number of contexts K",
            "context_tick_format": "{k}",
            "bar_format": "{value:.2f}",
        },
        "A": {"title": "Masking depends on representation"},
        "B": {"title": "Modal selection is a distinct outcome"},
        "C": {
            "title": "Successful encounter is nearly universal",
            "encounter_legend": "Ever accepted in good context",
            "masking_legend": "Final-window masking",
            "ylabel": "Learners / actions (%)",
        },
        "D": {
            "title": "Receptive abundance restores selection",
            "one_context_legend_format": "{count} receptive context",
            "many_contexts_legend_format": "{count} receptive contexts",
        },
        "E": {"title": "Endpoint success does not remove cost", "ylabel": "Expected static regret per step"},
        "F": {"title": "Larger sets delay successful encounter", "ylabel": "Capped first-success step (zero-based)"},
    },
    6: {
        "A": {
            "title": "Learned versus objective boundaries",
            "crossing_note_format": "Archived crossing: {learned:.3f}\n95% CI [{lo:.3f}, {hi:.3f}]",
            # Science-linked reference threshold and archived censoring limit.
            "objective_note": "Objective\n0.471",
            "hierarchical_note": "Hierarchical crossing:\nleft-censored below .30",
            "ylabel": "Good-authentic modal fraction",
        },
        "B": {
            "title": "Masking and modal selection",
            "masking_legend": "Actual masking",
            "modal_legend": "Good-authentic mode",
            "bar_format": "{value:.1f}",
            "ticks": ["0", ".300", ".325", ".471\n(objective)"],
            "ylabel": "Actions / learners (%)",
        },
    },
}
