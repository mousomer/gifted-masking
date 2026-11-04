"""Editable visible wording for all ten integrated-article figures.

Edit this file, not the archived data or plotting functions, to change labels.
Each numbered entry follows its figure's panel letters. ``\n`` inserts a line
break; keep breaks when fitting long text into the fixed publication layout.
Strings ending in ``_format`` use Python ``str.format``: preserve the named
placeholders (and braces used for Matplotlib math text) when changing wording.
Numbers in ordinary strings are science-linked labels, not recalculations:
changing them requires checking the evidence and caption, not just the style.
No data selectors, numerical calculations or paths live here. The generator
validates inherited text and required new sections before rendering. Examples:
FIGURE_TEXT[4]['A']['title'] changes the weighting heading;
FIGURE_TEXT[8]['row_labels'][9] changes the low-alpha matrix label.
Run generate_figures.py --list, then --figure 8 --preview-dir /private/tmp/name.
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
    "good_authentic_modal_percent": "Good-authentic modal\nclassification (%)",
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
    4: {
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
    5: {
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
    6: {
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
    9: {
        "shared": {
            "xlabel": "Number of contexts K",
            "context_tick_format": "{k}",
            "bar_format": "{value:.2f}",
        },
        "A": {"title": "Masking depends on\nrepresentation"},
        "B": {"title": "Modal selection is\na distinct outcome"},
        "C": {
            "title": "Successful encounter is\nnearly universal",
            "encounter_legend": "Ever accepted in\ngood context",
            "masking_legend": "Final-window masking",
            "ylabel": "Learners / actions (%)",
        },
        "D": {
            "title": "Receptive abundance\nrestores selection",
            "one_context_legend_format": "{count} receptive context",
            "many_contexts_legend_format": "{count} receptive contexts",
        },
        "E": {"title": "Endpoint success does\nnot remove cost", "ylabel": "Expected static regret\nper step"},
        "F": {"title": "Larger sets delay\nsuccessful encounter", "ylabel": "Capped first-success step\n(zero-based)"},
    },
    10: {
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

    2: {
        "title": "Social state determines reward and the next opportunity",
        "flow_heading": "CURRENT STATE",
        "action_heading": "ACTION / OUTCOME",
        "reward_heading": "REWARD",
        "next_heading": "NEXT STATE",
        "neutral": "Neutral (N)",
        "accepted": "Accepted (A)",
        "stigmatized": "Stigmatized (S)",
        "n_mask": "Mask",
        "n_auth_success": "Authentic: accepted (p)",
        "n_auth_reject": "Authentic: rejected (1−p)",
        "a_mask": "Mask",
        "a_auth": "Authentic",
        "s_mask": "Mask",
        "s_auth_success": "Authentic: redeemed (p/2)",
        "s_auth_fail": "Authentic: not redeemed (1−p/2)",
        "r_mask": "b−c",
        "r_auth": "b+a",
        "r_reject": "a−r",
        "r_s_mask": "b₂−c",
        "r_s_reject": "a−r₂",
        "next_n": "N",
        "next_a": "A",
        "next_s": "S",
        "next_turnover": "N with δ; otherwise A",
        "next_escape": "N with η; otherwise S",
        "reward_order": "Reward is realized first; then the displayed transition occurs.",
        "condition_note": "Turnover applies to current A. Escape applies only to non-redeemed S paths.",
    },
    3: {
        "title": "Four representations, the same environmental reward classes",
        "key": "Illustrative K = 3; M = mask, A = authentic",
        "flat_title": "A  Flat joint choice: 2K arms",
        "hier_title": "B  Hierarchical: context, then behavior",
        "global_title": "C  Global mask: K + 1 arms",
        "known_title": "D  Known good context: 2 arms",
        "softmax": "One softmax",
        "context_softmax": "Context softmax",
        "behavior_softmax": "Within-context softmax",
        "context_format": "Context {index}",
        "mask": "M",
        "auth": "A",
        "flat_update": "Update only the selected joint arm",
        "hier_update": "Same reward updates selected context\nand selected behavior values",
        "global_update": "Update only the selected arm",
        "known_context": "Known receptive context",
        "known_update": "No context search; invariant to requested K",
        "shared_mask": "Shared M",
        "auth_context_format": "A{index}",
        "reward_key": "Expected rewards: mask .75 | good authenticity 1.15 | other authenticity −.80",
    },
    7: {
        "title": "Dynamic optimality and learned behavior across the full grid",
        "xlabel": "Receptivity p",
        "ylabel": "Escape probability η",
        "suboptimal": "Learned suboptimal masking",
        "agreement": "Agreement with objective",
        "inconclusive": "Inconclusive",
        "count_format": "{label}: {count} / 357",
        "design": "21 receptivity levels × 17 escape levels; five masters per cell",
        "scope": "Counts describe tested parameter cells, not population prevalence.",
    },
    8: {
        "title": "Which separate perturbations retain the learning gap?",
        "xlabel": "Five disagreement sentinels (receptivity p, escape η)",
        "column_format": "({p:g}, {eta:g})",
        "row_labels": [
            "Reference", "Horizon T = 2,000", "Horizon T = 5,000",
            "Learners n = 320", "Final window = .1", "Final window = .4",
            "Weight λ = .5", "Weight λ = 2.5", "Initial value q₀ = .75",
            "Learning rate α = .03", "Learning rate α = .3",
            "Temperature τ = .1", "Temperature τ = .6",
            "Discount γ = .5", "Discount γ = .99",
        ],
        "cell_format": "{count}/5",
        "total_heading": "Total",
        "total_format": "{count}/25",
        "colorbar": "Masters retaining suboptimal-mask classification",
        "scope": "Rows change one factor at a time; other classifications are oracle agreement.",
        "discount_note": "Changing γ also changes the dynamic objective; the sixth control sentinel is excluded.",
    },
}
