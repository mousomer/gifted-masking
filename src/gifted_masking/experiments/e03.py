"""Frozen E03 M2 regime-replication smoke experiment.

This module is intentionally an orchestration layer over the maintained M2
kernel and objective value-iteration comparator.  It must never alter M2
transition order, defaults, or the historic map's RNG stream.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
import tempfile
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator

import numpy as np

from gifted_masking.analysis.m2_optimal import (
    ACTION_NAMES,
    STATE_NAMES,
    M2Params,
    build_m2_transition_table,
    evaluate_policy_value,
    solve_m2_value_iteration,
    static_m0_comparator,
    transition_arrays,
)
from gifted_masking.models import m2
from gifted_masking.repro import ensure_results_dirs, write_csv, write_json


E03_RAW_FIELDNAMES = [
    "run_id", "experiment_id", "tier", "model", "component", "sensitivity_name",
    "master_seed", "parameter_cell_id", "cell_seed", "child_id", "child_seed", "rng_unit", "rng_family_id", "trajectory_prefix_family",
    "p", "eta", "b", "a", "c", "r", "b2", "r2", "delta", "alpha", "tau", "lambda", "q0", "gamma", "n", "T",
    "final_window_fraction", "final_window_start", "final_window_end", "final_window_mask_count", "final_window_mask_rate",
    "final_window_objective_reward_sum", "final_window_objective_reward_mean",
    "neutral_mask_count", "neutral_authentic_count", "accepted_mask_count", "accepted_authentic_count",
    "stigmatized_mask_count", "stigmatized_authentic_count", "neutral_visit_count", "accepted_visit_count", "stigmatized_visit_count", "final_state",
]

E03_CELL_FIELDS = [
    "run_id", "experiment_id", "tier", "component", "sensitivity_name", "master_seed", "parameter_cell_id", "cell_seed", "p", "eta",
    "b", "a", "c", "r", "b2", "r2", "delta", "alpha", "tau", "lambda", "q0", "gamma", "n", "T", "final_window_fraction",
    "vi_converged", "vi_iterations", "vi_residual", "static_neutral_action", "objective_neutral_action", "objective_neutral_q_gap_auth_minus_mask",
    "objective_regime", "neutral_mask_probability", "learned_neutral_action", "learner_status", "neutral_visits_total", "neutral_visiting_children",
    "neutral_visit_adequate", "accepted_visits_total", "stigmatized_visits_total", "full_policy_value_neutral", "full_policy_regret_neutral",
    "full_policy_status", "neutral_decision_regret", "mean_final_window_mask_rate", "mean_final_window_objective_reward", "legacy_region", "classification",
]

E03_EFFECT_FIELDS = ["run_id", "experiment_id", "tier", "component", "effect_name", "level", "master_seed", "denominator", "estimate", "ci_status", "ci_low", "ci_high", "notes"]
E03_STABLE_FIELDS = ["run_id", "experiment_id", "tier", "parameter_cell_id", "p", "eta", "classification", "non_inconclusive_seed_count", "matching_seed_count", "stable", "notes"]
E03_THRESHOLD_FIELDS = ["run_id", "experiment_id", "tier", "eta", "threshold_kind", "lower_p", "upper_p", "midpoint_p", "bracket_width", "status", "notes"]

FROZEN_ENVIRONMENT = {"b": 1.0, "a": 0.6, "c": 0.25, "r": 2.0, "b2": 0.5, "r2": 2.5, "delta": 0.02}
FROZEN_LEARNER = {"alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0, "gamma": 0.9}
SMOKE_CONTRACT = {"run_id": "frontiers_m2_regime_replication_v1_smoke", "master_seed": 2026081399, "bootstrap_seed": 2026081397, "workers": 1, "n": 64, "T": 300, "final_window_fraction": 0.2}
LEGACY_CONTRACT = {"p_start": 0.0, "p_stop": 1.0, "p_step": 0.05, "eta_start": 0.0, "eta_stop": 0.8, "eta_step": 0.05, "n": 160, "T": 1000, "final_window_fraction": 0.2, "seed_base": 9100}
SMOKE_SENTINELS = ((0.35, 0.0), (0.4, 0.0), (0.55, 0.0), (0.55, 0.2), (0.75, 0.0), (0.9, 0.2))
LEGACY_MAP_SHA256 = "bb220dddc16335e9fc901a2e8be53f6d7c1a90aed8198fae3b2fd56e46e3ef2b"
VI_TOL = 1e-10
VISIT_TOTAL_FLOOR = 100
VISIT_CHILD_FRACTION = 0.2
T_CRITICAL_95_DF4 = 2.7764451051977987
E03_STANDARD_APPROVAL_RELATIVE = "projects/frontiers_article/approvals/E03_STANDARD_GO.md"
E03_STANDARD_MASTER_SEEDS = (2026081301, 2026081302, 2026081303, 2026081304, 2026081305)


def _canonical_json(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _format(value: object) -> object:
    if isinstance(value, (np.bool_, bool)):
        return str(bool(value))
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def _require_exact_keys(value: object, keys: set[str], label: str) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"E03 {label} keys are frozen")
    return value


def _require_numbers(mapping: dict[str, object], expected: dict[str, float], label: str) -> None:
    for key, target in expected.items():
        value = mapping.get(key)
        if type(value) is not float or value != target:
            raise ValueError(f"E03 requires exact float {label}.{key}={target}")


def _smoke_expected_config() -> dict[str, object]:
    return {
        "experiment_id": "E03", "run_id": SMOKE_CONTRACT["run_id"], "tier": "smoke", "model": "M2",
        "master_seed": 2026081399, "bootstrap_seed": 2026081397, "workers": 1,
        "environment": FROZEN_ENVIRONMENT, "learner": FROZEN_LEARNER, "legacy_provenance_replay": LEGACY_CONTRACT,
        "smoke_sentinels": [{"p": p, "eta": eta} for p, eta in SMOKE_SENTINELS], "n": 64, "T": 300, "final_window_fraction": 0.2,
    }


def _standard_expected_config() -> dict[str, object]:
    sentinels = [{"p": p, "eta": eta} for p, eta in SMOKE_SENTINELS]
    return {
        "experiment_id": "E03", "run_id": "frontiers_m2_regime_replication_v1", "tier": "standard", "model": "M2",
        "master_seed": 2026081301, "master_seeds": [2026081301, 2026081302, 2026081303, 2026081304, 2026081305],
        "bootstrap_seed": 2026081397, "workers": 1, "approved_standard": False, "environment": FROZEN_ENVIRONMENT, "learner": FROZEN_LEARNER,
        "exact_grid": LEGACY_CONTRACT, "sentinels": sentinels,
        "one_at_a_time": {"n": [320], "T": [2000, 5000], "final_window_fraction": [0.1, 0.4], "alpha": [0.03, 0.3], "tau": [0.1, 0.6], "lambda": [0.5, 2.5], "q0": [0.75], "gamma": [0.5, 0.99]},
        "harsh_sentinel": {"p": [0.7, 0.75, 0.8], "eta": 0.0, "b2": 0.0, "r2": 8.0, "delta": 0.3, "gamma": 0.9},
        "threshold_refinement": {"etas": [0.0, 0.2, 0.8], "objective_bracket_tolerance": 0.0001, "learned_max_added_p_per_eta": 8, "learned_target_width": 0.0125, "learned_method": "five_seed_dyadic_adjacent_boundary"},
    }


def load_e03_config(path: Path, overrides: dict[str, object] | None = None) -> dict[str, Any]:
    config = json.loads(path.read_text())
    if not isinstance(config, dict):
        raise ValueError("E03 config must be a JSON object")
    if overrides:
        config.update(overrides)
    required = {"experiment_id", "run_id", "tier", "model", "master_seed", "bootstrap_seed", "workers", "environment", "learner"}
    if config.get("tier") == "smoke":
        required |= {"legacy_provenance_replay", "smoke_sentinels", "n", "T", "final_window_fraction"}
    elif config.get("tier") == "standard":
        required |= {"master_seeds", "approved_standard", "exact_grid", "sentinels", "one_at_a_time", "harsh_sentinel", "threshold_refinement"}
    if set(config) != required:
        raise ValueError("unknown or missing E03 configuration keys")
    if not all(type(config.get(key)) is str for key in ("experiment_id", "run_id", "tier", "model")):
        raise ValueError("E03 identifiers require JSON strings")
    if config["experiment_id"] != "E03" or config["model"] != "M2" or config["tier"] not in {"smoke", "standard"}:
        raise ValueError("only frozen E03 M2 configurations are supported")
    if type(config["master_seed"]) is not int or type(config["bootstrap_seed"]) is not int or type(config["workers"]) is not int:
        raise ValueError("E03 seed and worker fields require exact JSON integers")
    if config["workers"] != 1:
        raise ValueError("E03 v1 requires workers=1")
    environment = _require_exact_keys(config["environment"], set(FROZEN_ENVIRONMENT), "environment")
    learner = _require_exact_keys(config["learner"], set(FROZEN_LEARNER), "learner")
    _require_numbers(environment, FROZEN_ENVIRONMENT, "environment")
    _require_numbers(learner, FROZEN_LEARNER, "learner")
    if config["tier"] == "smoke":
        if _canonical_json(config) != _canonical_json(_smoke_expected_config()):
            raise ValueError("smoke config differs from the frozen E03 contract")
        return config
    if type(config["approved_standard"]) is not bool or config["approved_standard"] is not False:
        raise ValueError("E03 standard must remain explicitly unapproved")
    if _canonical_json(config) != _canonical_json(_standard_expected_config()):
        raise ValueError("standard config differs from the frozen E03 contract")
    return config


def canonical_e03_cell_id(
    config: dict[str, Any], cell: dict[str, float], *, component: str = "smoke_sentinels", sensitivity_name: str = "baseline",
    n: int | None = None, horizon: int | None = None, window: float | None = None,
    environment: dict[str, float] | None = None, learner: dict[str, float] | None = None,
) -> str:
    """Canonical parameter ID, excluding only the independent master seed.

    The master seed is a separate repeated-measure identifier; including it in
    the cell key would make five-seed stability grouping impossible. Every
    model, component, sensitivity, environment, learner, and run-shape field
    that can change the generated trajectory remains in this identifier.
    """
    env, learner_values = environment or config["environment"], learner or config["learner"]
    return "|".join((
        "E03", f"run_id={config['run_id']}", f"tier={config['tier']}", f"model={config['model']}",
        f"component={component}", f"sensitivity={sensitivity_name}", f"p={float(cell['p']):.12g}", f"eta={float(cell['eta']):.12g}",
        *(f"{key}={float(env[key]):.12g}" for key in ("b", "a", "c", "r", "b2", "r2", "delta")),
        *(f"{key}={float(learner_values[key]):.12g}" for key in ("alpha", "tau", "lambda", "q0", "gamma")),
        f"n={int(config['n'] if n is None else n)}", f"T={int(config['T'] if horizon is None else horizon)}",
        f"window={float(config['final_window_fraction'] if window is None else window):.12g}",
    ))


def canonical_e03_trajectory_prefix_id(
    config: dict[str, Any], cell: dict[str, float], *, component: str, sensitivity_name: str, n: int | None = None,
) -> str:
    """ID used only when staged T/window sensitivity reuses a latent prefix.

    The full parameter-cell ID always retains T and window.  This separate
    identifier intentionally omits only those two fields, so population-size
    or semantic changes cannot silently become paired RNG streams.
    """
    env, learner = config["environment"], config["learner"]
    return "|".join((
        "E03", f"run_id={config['run_id']}", f"tier={config['tier']}", f"model={config['model']}",
        "component=trajectory_prefix", f"paired_component={component}", "paired_sensitivity=default_T_or_window", f"p={float(cell['p']):.12g}", f"eta={float(cell['eta']):.12g}",
        *(f"{key}={float(env[key]):.12g}" for key in ("b", "a", "c", "r", "b2", "r2", "delta")),
        *(f"{key}={float(learner[key]):.12g}" for key in ("alpha", "tau", "lambda", "q0", "gamma")),
        f"n={int(config['n'] if n is None else n)}",
    ))


def e03_rng_family_id(
    config: dict[str, Any], cell: dict[str, float], *, component: str, sensitivity_name: str,
    n: int, horizon: int, window: float,
) -> str:
    """Return the seed semantic ID, pairing only approved standard T/window OATs.

    `parameter_cell_id` always retains T and window.  The family omits them
    only for default-environment/default-learner standard variants that change
    exactly one of those fields; every other planned case gets its own family.
    """
    parameter_id = canonical_e03_cell_id(config, cell, component=component, sensitivity_name=sensitivity_name, n=n, horizon=horizon, window=window)
    default_horizon = int(config.get("exact_grid", {}).get("T", config.get("T", horizon)))
    default_window = float(config.get("exact_grid", {}).get("final_window_fraction", config.get("final_window_fraction", window)))
    default_n = int(config.get("exact_grid", {}).get("n", config.get("n", n)))
    approved_cells = {(float(row["p"]), float(row["eta"])) for row in config.get("sentinels", [])}
    approved_pair = (
        config.get("tier") == "standard"
        and component == "sentinels"
        and sensitivity_name in {"T", "final_window_fraction"}
        and (float(cell["p"]), float(cell["eta"])) in approved_cells
        and config.get("environment") == FROZEN_ENVIRONMENT
        and config.get("learner") == FROZEN_LEARNER
        and n == default_n
        and ((sensitivity_name == "T" and window == default_window) or (sensitivity_name == "final_window_fraction" and horizon == default_horizon))
    )
    if approved_pair:
        return canonical_e03_trajectory_prefix_id(config, cell, component=component, sensitivity_name=sensitivity_name, n=n)
    if config.get("tier") == "standard":
        return f"{parameter_id}|component={component}|sensitivity={sensitivity_name}"
    return parameter_id


def derive_e03_cell_seed(master_seed: int, cell_id: str) -> int:
    words = np.frombuffer(hashlib.sha256(cell_id.encode("utf-8")).digest()[:16], dtype="<u4").tolist()
    sequence = np.random.SeedSequence([int(master_seed), 3, *map(int, words)])
    return int(sequence.spawn(1)[0].generate_state(1, dtype=np.uint64)[0])


def _within_one_ulp(observed: float, frozen: float) -> bool:
    """Accept only exact equality or an adjacent IEEE-754 representable value."""
    return observed == frozen or observed in {
        math.nextafter(frozen, -math.inf), math.nextafter(frozen, math.inf),
    }


def _params(config: dict[str, Any], p: float, eta: float) -> M2Params:
    return M2Params(p=p, eta=eta, **config["environment"], gamma=float(config["learner"]["gamma"]), lam=float(config["learner"]["lambda"]))


def _visit_adequacy(state_visit_counts: np.ndarray, n: int) -> dict[str, dict[str, object]]:
    total_min = max(VISIT_TOTAL_FLOOR, n)
    child_min = max(16, math.ceil(VISIT_CHILD_FRACTION * n))
    result: dict[str, dict[str, object]] = {}
    for index, name in enumerate(STATE_NAMES):
        total = int(state_visit_counts[:, index].sum())
        children = int(np.count_nonzero(state_visit_counts[:, index]))
        result[name] = {"total": total, "children": children, "adequate": total >= total_min and children >= child_min, "required_total": total_min, "required_children": child_min}
    return result


def _reachable_states(params: M2Params, mask_probabilities: np.ndarray) -> set[int]:
    probabilities, _ = transition_arrays(build_m2_transition_table(params))
    policy = np.column_stack([mask_probabilities, 1.0 - mask_probabilities])
    induced = np.einsum("sa,san->sn", policy, probabilities)
    reached = {m2.STATE_NEUTRAL}
    frontier = [m2.STATE_NEUTRAL]
    while frontier:
        state = frontier.pop()
        for successor in np.flatnonzero(induced[state] > 0.0):
            successor_int = int(successor)
            if successor_int not in reached:
                reached.add(successor_int); frontier.append(successor_int)
    return reached


def _validate_state_action_visit_counts(counts: np.ndarray, visits: np.ndarray) -> None:
    if counts.ndim != 3 or counts.shape[1:] != (3, 2) or visits.shape != counts.shape[:2]:
        raise ValueError("E03 state-action and visit diagnostics have incompatible shapes")
    if np.any(counts < 0) or np.any(visits < 0) or not np.array_equal(counts.sum(axis=2), visits):
        raise ValueError("E03 each state's mask+auth count must equal its visit count")


def classify_e03_cell(params: M2Params, diagnostics: dict[str, np.ndarray], *, n: int) -> dict[str, object]:
    """Apply the frozen E03 objective/visit/tie classification contract."""
    solution = solve_m2_value_iteration(params, tol=VI_TOL, max_iter=100_000)
    if not bool(solution["converged"]):
        raise RuntimeError("E03 value iteration did not converge")
    counts = np.asarray(diagnostics["state_action_counts_final"], dtype=int)
    visits = np.asarray(diagnostics["state_visit_counts_final"], dtype=int)
    _validate_state_action_visit_counts(counts, visits)
    totals = counts.sum(axis=0)
    adequacy = _visit_adequacy(visits, n)
    neutral_mask, neutral_auth = (int(totals[m2.STATE_NEUTRAL, action]) for action in (0, 1))
    q_gap = float(solution["Q"][m2.STATE_NEUTRAL, 1] - solution["Q"][m2.STATE_NEUTRAL, 0])
    if abs(q_gap) <= VI_TOL:
        objective_action, objective_regime = "", "inconclusive_objective_tie"
    elif q_gap > 0.0:
        objective_action, objective_regime = "authentic", "dynamic_authenticity"
    else:
        objective_action, objective_regime = "mask", "dynamic_masking"
    if not bool(adequacy["neutral"]["adequate"]):
        learned_action, learner_status = "", "inconclusive_neutral_visit"
    elif neutral_mask == neutral_auth:
        learned_action, learner_status = "", "inconclusive_neutral_tie"
    elif neutral_mask > neutral_auth:
        learned_action, learner_status = "mask", "neutral_mask"
    else:
        learned_action, learner_status = "authentic", "neutral_authentic"
    static = static_m0_comparator(params)
    raw_mask_probabilities = np.full(3, 0.5, dtype=float)
    for state in range(3):
        total = int(totals[state].sum())
        if total:
            raw_mask_probabilities[state] = totals[state, 0] / total
    reachable = _reachable_states(params, raw_mask_probabilities)
    full_ready = all(bool(adequacy[STATE_NAMES[state]]["adequate"]) for state in reachable)
    if full_ready:
        full_policy = np.column_stack([raw_mask_probabilities, 1.0 - raw_mask_probabilities])
        full_value = float(evaluate_policy_value(params, full_policy)[m2.STATE_NEUTRAL])
        full_regret = float(solution["V"][m2.STATE_NEUTRAL] - full_value)
        full_status = "available"
    else:
        full_value, full_regret, full_status = "", "", "blank_inadequate_required_state_visits"
    if not learned_action or not objective_action:
        neutral_decision_regret: object = ""
    elif learned_action == objective_action:
        neutral_decision_regret = 0.0
    else:
        neutral_decision_regret = abs(q_gap)
    if not objective_action or not learned_action:
        classification = "inconclusive"
    elif learned_action == "mask" and objective_action == "authentic":
        classification = "learned_suboptimal_masking"
    elif objective_action == "mask" and static["optimal_action"] == "authentic":
        classification = "optimal_policy_masking"
    elif learned_action == objective_action:
        classification = "learner_matches_objective"
    else:
        classification = "learner_differs_without_masking_claim"
    # This field deliberately retains the maintained historical taxonomy;
    # strict E03 classification above is the only field used for new evidence.
    if str(static["optimal_action"]) == "authentic" and objective_action == "mask":
        legacy_region = "optimal_learner_lock_in"
    elif learned_action == "mask" and objective_action == "authentic":
        legacy_region = "learned_suboptimal_lock_in"
    elif str(static["optimal_action"]) == "mask" and objective_action == "authentic":
        legacy_region = "dynamic_authenticity_overrides_static_masking"
    elif objective_action == "mask":
        legacy_region = "masking_optimal_and_learned_not_proven_suboptimal"
    else:
        legacy_region = "authenticity_optimal_or_learned_matches"
    return {
        "solution": solution, "counts": counts, "visits": visits, "adequacy": adequacy, "static": static,
        "q_gap": q_gap, "objective_action": objective_action, "objective_regime": objective_regime,
        "neutral_mask_probability": neutral_mask / (neutral_mask + neutral_auth) if neutral_mask + neutral_auth else "",
        "learned_action": learned_action, "learner_status": learner_status, "full_policy_value": full_value,
        "full_policy_regret": full_regret, "full_policy_status": full_status, "neutral_decision_regret": neutral_decision_regret,
        "mean_final_window_mask_rate": float(np.asarray(diagnostics["mask_rate_final"], dtype=float).mean()),
        "mean_final_window_objective_reward": float(np.asarray(diagnostics["reward_mean_final"], dtype=float).mean()),
        "legacy_region": legacy_region, "classification": classification,
    }


def simulate_e03_sentinel(
    config: dict[str, Any], cell: dict[str, float], cell_id: str, cell_seed: int, rng_family_id: str | None = None,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Call the maintained vectorized M2 kernel without altering its RNG order."""
    n, horizon = int(config["n"]), int(config["T"])
    window = int(math.ceil(horizon * float(config["final_window_fraction"])))
    diagnostics = m2.simulate_with_diagnostics(
        float(cell["p"]), float(cell["eta"]), n=n, horizon=horizon, seed=cell_seed,
        **config["environment"], alpha=float(config["learner"]["alpha"]), temp=float(config["learner"]["tau"]),
        lam=float(config["learner"]["lambda"]), q0=float(config["learner"]["q0"]), gamma=float(config["learner"]["gamma"]),
        final_window_fraction=float(config["final_window_fraction"]),
    )
    counts = np.asarray(diagnostics["state_action_counts_final"], dtype=int)
    visits = np.asarray(diagnostics["state_visit_counts_final"], dtype=int)
    masks = np.asarray(diagnostics["mask_rate_final"], dtype=float)
    rewards = np.asarray(diagnostics["reward_mean_final"], dtype=float)
    final_states = np.asarray(diagnostics["final_state"], dtype=int)
    rows = []
    for child_id in range(n):
        values = {
            "run_id": config["run_id"], "experiment_id": "E03", "tier": "smoke", "model": "M2", "component": "smoke_sentinels", "sensitivity_name": "baseline",
            "master_seed": config["master_seed"], "parameter_cell_id": cell_id, "cell_seed": cell_seed, "child_id": child_id, "child_seed": "",
            "rng_unit": "vectorized_cell_stream", "rng_family_id": rng_family_id or cell_id, "trajectory_prefix_family": rng_family_id or cell_id,
            "p": cell["p"], "eta": cell["eta"], **config["environment"], **config["learner"], "n": n, "T": horizon,
            "final_window_fraction": config["final_window_fraction"], "final_window_start": horizon - window, "final_window_end": horizon - 1,
            "final_window_mask_count": int(round(masks[child_id] * window)), "final_window_mask_rate": masks[child_id],
            "final_window_objective_reward_sum": rewards[child_id] * window, "final_window_objective_reward_mean": rewards[child_id],
            "neutral_mask_count": counts[child_id, 0, 0], "neutral_authentic_count": counts[child_id, 0, 1],
            "accepted_mask_count": counts[child_id, 1, 0], "accepted_authentic_count": counts[child_id, 1, 1],
            "stigmatized_mask_count": counts[child_id, 2, 0], "stigmatized_authentic_count": counts[child_id, 2, 1],
            "neutral_visit_count": visits[child_id, 0], "accepted_visit_count": visits[child_id, 1], "stigmatized_visit_count": visits[child_id, 2],
            "final_state": STATE_NAMES[int(final_states[child_id])],
        }
        rows.append({field: _format(values[field]) for field in E03_RAW_FIELDNAMES})
    return rows, classify_e03_cell(_params(config, float(cell["p"]), float(cell["eta"])), diagnostics, n=n)


def _legacy_replay_rows() -> tuple[list[dict[str, object]], dict[str, float | int | str]]:
    """Rebuild the historic map with its original stream, then freeze its hash."""
    from scripts import map_m2_lock_in_regions as legacy

    rows, _ = legacy.build_rows()
    formatted = [{key: legacy._format(row[key]) for key in legacy.CELL_COLUMNS} for row in rows]
    payload = tempfile.NamedTemporaryFile(mode="w", newline="", delete=False)
    try:
        with payload:
            writer = csv.DictWriter(payload, fieldnames=legacy.CELL_COLUMNS)
            writer.writeheader(); writer.writerows(formatted)
        encoded = Path(payload.name).read_bytes()
    finally:
        Path(payload.name).unlink(missing_ok=True)
    digest = hashlib.sha256(encoded).hexdigest()
    learned = [row for row in formatted if row["region"] == "learned_suboptimal_lock_in"]
    stats: dict[str, float | int | str] = {
        "rows": len(formatted), "learned_suboptimal_count": len(learned), "fraction": len(learned) / len(formatted),
        "mean_neutral_mask_probability": math.fsum(float(row["learned_neutral_mask_probability"]) for row in learned) / len(learned), "sha256": digest,
    }
    # The exported legacy CSV hash is the exact provenance authority. The
    # approved mean is `math.fsum` over its exported numeric values. A caller
    # may reconcile a platform aggregate one ULP away, never a broad epsilon.
    frozen_mean = 0.9501766068109203
    if not (stats["rows"] == 357 and stats["learned_suboptimal_count"] == 226 and stats["fraction"] == 0.6330532212885154 and stats["sha256"] == LEGACY_MAP_SHA256 and _within_one_ulp(float(stats["mean_neutral_mask_probability"]), frozen_mean)):
        raise RuntimeError(f"E03 legacy provenance replay mismatch: observed={stats!r}")
    return formatted, stats


def _cell_rows(config: dict[str, Any], classified: dict[str, object], cell: dict[str, float], cell_id: str, cell_seed: int) -> dict[str, object]:
    solution = classified["solution"]
    adequacy = classified["adequacy"]
    values = {
        "run_id": config["run_id"], "experiment_id": "E03", "tier": "smoke", "component": "smoke_sentinels", "sensitivity_name": "baseline",
        "master_seed": config["master_seed"], "parameter_cell_id": cell_id, "cell_seed": cell_seed, "p": cell["p"], "eta": cell["eta"],
        **config["environment"], **config["learner"], "n": config["n"], "T": config["T"], "final_window_fraction": config["final_window_fraction"],
        "vi_converged": solution["converged"], "vi_iterations": solution["iterations"], "vi_residual": solution["residual"],
        "static_neutral_action": classified["static"]["optimal_action"], "objective_neutral_action": classified["objective_action"],
        "objective_neutral_q_gap_auth_minus_mask": classified["q_gap"], "objective_regime": classified["objective_regime"],
        "neutral_mask_probability": classified["neutral_mask_probability"], "learned_neutral_action": classified["learned_action"], "learner_status": classified["learner_status"],
        "neutral_visits_total": adequacy["neutral"]["total"], "neutral_visiting_children": adequacy["neutral"]["children"], "neutral_visit_adequate": adequacy["neutral"]["adequate"],
        "accepted_visits_total": adequacy["accepted"]["total"], "stigmatized_visits_total": adequacy["stigmatized"]["total"],
        "full_policy_value_neutral": classified["full_policy_value"], "full_policy_regret_neutral": classified["full_policy_regret"],
        "full_policy_status": classified["full_policy_status"], "neutral_decision_regret": classified["neutral_decision_regret"],
        "mean_final_window_mask_rate": classified["mean_final_window_mask_rate"], "mean_final_window_objective_reward": classified["mean_final_window_objective_reward"],
        "legacy_region": classified["legacy_region"], "classification": classified["classification"],
    }
    return {field: _format(values[field]) for field in E03_CELL_FIELDS}


def recompute_e03_summaries(raw_rows: list[dict[str, object]], config: dict[str, Any]) -> list[dict[str, object]]:
    """Reconstruct raw count/window/reward identities without simulation state."""
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in raw_rows:
        groups[str(row["parameter_cell_id"])].append(row)
    summaries = []
    for identifier, rows in sorted(groups.items()):
        first = rows[0]
        n, window = int(first["n"]), int(first["T"]) - int(first["final_window_start"])
        if len(rows) != n:
            raise ValueError("E03 raw child count does not match n")
        for row in rows:
            states = (("neutral", "neutral_visit_count"), ("accepted", "accepted_visit_count"), ("stigmatized", "stigmatized_visit_count"))
            for state, visit_key in states:
                if int(row[f"{state}_mask_count"]) + int(row[f"{state}_authentic_count"]) != int(row[visit_key]):
                    raise ValueError("E03 state action counts do not reconcile to that state visit count")
            visit_total = sum(int(row[key]) for _, key in states)
            if visit_total != window:
                raise ValueError("E03 state action/visit totals do not reconcile to final window")
            if int(row["final_window_mask_count"]) != sum(int(row[key]) for key in ("neutral_mask_count", "accepted_mask_count", "stigmatized_mask_count")):
                raise ValueError("E03 final mask count does not reconcile")
            if not math.isclose(float(row["final_window_objective_reward_sum"]), float(row["final_window_objective_reward_mean"]) * window, rel_tol=0.0, abs_tol=1e-12):
                raise ValueError("E03 final reward does not reconcile")
        summaries.append({"parameter_cell_id": identifier, "n": n, "mean_final_window_mask_rate": float(np.mean([float(row["final_window_mask_rate"]) for row in rows])), "mean_final_window_objective_reward": float(np.mean([float(row["final_window_objective_reward_mean"]) for row in rows]))})
    return summaries


def student_t_95_interval(values: Iterable[float]) -> tuple[float | str, float | str, float | str]:
    """Return the prespecified five-seed Student-t estimate and interval."""
    array = np.asarray(list(values), dtype=float)
    if array.size != 5:
        return "", "", ""
    estimate = float(array.mean())
    half = T_CRITICAL_95_DF4 * float(array.std(ddof=1)) / math.sqrt(array.size)
    return estimate, estimate - half, estimate + half


def canonical_e03_exact_grid(config: dict[str, Any] | None = None) -> dict[str, dict[str, object]]:
    """Return the one permitted 21×17 exact-grid parameter-ID map.

    The map is generated from the frozen standard contract rather than caller
    input, so a same-cardinality arbitrary identifier set cannot enter a
    standard fraction, interval, or stable-cell result.
    """
    frozen = _standard_expected_config()
    if config is not None and _canonical_json(config) != _canonical_json(frozen):
        raise ValueError("E03 exact-grid canonicalization requires the frozen standard config")
    grid = frozen["exact_grid"]
    environment, learner = frozen["environment"], frozen["learner"]
    result: dict[str, dict[str, object]] = {}
    for eta_index in range(17):
        eta = eta_index * .05
        for p_index in range(21):
            p = p_index * .05
            cell = {"p": p, "eta": eta}
            identifier = canonical_e03_cell_id(
                frozen, cell, component="exact_grid", sensitivity_name="baseline",
                n=int(grid["n"]), horizon=int(grid["T"]), window=float(grid["final_window_fraction"]),
            )
            result[identifier] = {"p": p, "eta": eta, **environment, **learner, "n": int(grid["n"]), "T": int(grid["T"]), "final_window_fraction": float(grid["final_window_fraction"])}
    if len(result) != 357:
        raise AssertionError("frozen E03 exact grid did not yield 357 unique canonical IDs")
    return result


def _validate_exact_grid_row(row: dict[str, object], expected: dict[str, object]) -> None:
    required = {"component", "sensitivity_name", "master_seed", "parameter_cell_id", "classification", *expected}
    missing = required - set(row)
    if missing:
        raise ValueError(f"E03 exact-grid row is missing canonical fields: {sorted(missing)}")
    if str(row["component"]) != "exact_grid" or str(row["sensitivity_name"]) != "baseline":
        raise ValueError("E03 standard summarizer accepts only exact_grid baseline rows")
    for key, expected_value in expected.items():
        observed = row[key]
        if key in {"n", "T"}:
            if type(observed) is not int or observed != expected_value:
                raise ValueError(f"E03 exact-grid row has mismatched {key}")
        elif type(observed) not in {float, int} or isinstance(observed, bool) or float(observed) != float(expected_value):
            raise ValueError(f"E03 exact-grid row has mismatched {key}")


def summarize_e03_standard_classifications(rows: Iterable[dict[str, object]], config: dict[str, Any] | None = None) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Produce future five-seed fractions and 4/5 stable-cell labels.

    This pure helper consumes already-classified cell records. It executes no
    simulations and keeps the exact-grid denominator separate from sentinels.
    """
    canonical_grid = canonical_e03_exact_grid(config)
    values = list(rows)
    expected_seeds = {str(seed) for seed in E03_STANDARD_MASTER_SEEDS}
    by_seed: dict[str, list[dict[str, object]]] = defaultdict(list)
    seen_seed_cell: set[tuple[str, str]] = set()
    for row in values:
        seed, cell_id = str(row["master_seed"]), str(row["parameter_cell_id"])
        if cell_id not in canonical_grid:
            raise ValueError("E03 exact-grid row has an unapproved or mismatched parameter_cell_id")
        _validate_exact_grid_row(row, canonical_grid[cell_id])
        if seed not in expected_seeds:
            raise ValueError(f"E03 exact-grid row has unexpected master seed: {seed}")
        key = (seed, cell_id)
        if key in seen_seed_cell:
            raise ValueError(f"E03 duplicate exact-grid seed/cell key: {key}")
        seen_seed_cell.add(key); by_seed[seed].append(row)
    if set(by_seed) != expected_seeds:
        raise ValueError("E03 exact-grid summary requires exactly the five expected unique master seeds")
    cell_sets = {seed: {str(row["parameter_cell_id"]) for row in selected} for seed, selected in by_seed.items()}
    expected_cells = set(canonical_grid)
    if len(expected_cells) != 357 or any(len(cells) != 357 for cells in cell_sets.values()):
        raise ValueError("E03 exact-grid summary requires exactly 357 unique cells per master seed")
    if any(cells != expected_cells for cells in cell_sets.values()):
        raise ValueError("E03 exact-grid cells have missing or extra parameter IDs across master seeds")
    effects: list[dict[str, object]] = []
    seed_fractions = []
    for seed, selected in sorted(by_seed.items(), key=lambda item: int(item[0])):
        denominator = len(selected)
        fraction = sum(str(row["classification"]) == "learned_suboptimal_masking" for row in selected) / denominator if denominator else float("nan")
        seed_fractions.append(fraction)
        effects.append({"effect_name": "learned_suboptimal_masking_fraction", "level": "master_seed", "master_seed": seed, "denominator": denominator, "estimate": fraction, "ci_status": "not_estimable_within_seed", "ci_low": "", "ci_high": "", "notes": "exact-grid seed fraction"})
    estimate, low, high = student_t_95_interval(seed_fractions)
    effects.append({"effect_name": "learned_suboptimal_masking_fraction", "level": "across_master_seeds", "master_seed": "", "denominator": 357, "estimate": estimate, "ci_status": "student_t_95" if estimate != "" else "not_estimable_lt_5_master_seeds", "ci_low": low, "ci_high": high, "notes": "five independent master-seed exact-grid fractions"})
    by_cell: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in values:
        by_cell[str(row["parameter_cell_id"])].append(row)
    stable: list[dict[str, object]] = []
    for cell_id, records in sorted(by_cell.items()):
        if len(records) != 5 or {str(row["master_seed"]) for row in records} != expected_seeds:
            raise ValueError(f"E03 exact-grid cell does not have one record for every expected master seed: {cell_id}")
        classified = [str(row["classification"]) for row in records if str(row["classification"]) != "inconclusive"]
        frequencies: dict[str, int] = defaultdict(int)
        for classification in classified:
            frequencies[classification] += 1
        winner, matching = (max(frequencies.items(), key=lambda item: (item[1], item[0])) if frequencies else ("", 0))
        stable.append({"parameter_cell_id": cell_id, "classification": winner, "non_inconclusive_seed_count": len(classified), "matching_seed_count": matching, "stable": len(records) == 5 and matching >= 4, "notes": "stable iff same non-inconclusive classification in at least four of five seeds"})
    return effects, stable


def objective_threshold_bisection(params: M2Params, *, tolerance: float = 1e-4) -> dict[str, object]:
    """Bracket the objective neutral authenticity threshold without Monte Carlo."""
    if tolerance <= 0.0:
        raise ValueError("objective threshold tolerance must be positive")

    def gap(p_value: float) -> float:
        candidate = M2Params(p=p_value, eta=params.eta, b=params.b, a=params.a, c=params.c, r=params.r, b2=params.b2, r2=params.r2, delta=params.delta, gamma=params.gamma, lam=params.lam)
        solution = solve_m2_value_iteration(candidate, tol=VI_TOL, max_iter=100_000)
        if not bool(solution["converged"]):
            raise RuntimeError("E03 value iteration did not converge during objective bisection")
        return float(solution["Q"][m2.STATE_NEUTRAL, 1] - solution["Q"][m2.STATE_NEUTRAL, 0])

    low, high = 0.0, 1.0
    low_gap, high_gap = gap(low), gap(high)
    if low_gap >= 0.0:
        return {"status": "threshold_at_or_below_zero", "lower_p": 0.0, "upper_p": 0.0, "midpoint_p": 0.0, "bracket_width": 0.0}
    if high_gap < 0.0:
        return {"status": "no_threshold_in_unit_interval", "lower_p": "", "upper_p": "", "midpoint_p": "", "bracket_width": ""}
    while high - low > tolerance:
        middle = (low + high) / 2.0
        if gap(middle) >= 0.0:
            high = middle
        else:
            low = middle
    return {"status": "bracketed", "lower_p": low, "upper_p": high, "midpoint_p": (low + high) / 2.0, "bracket_width": high - low}


def refine_learned_threshold(
    observations: dict[float, str | None], evaluate: Callable[[float], str | None], *, target_width: float = 0.0125, max_added: int = 8,
) -> dict[str, object]:
    """Bounded dyadic learned-threshold refinement with censoring safeguards.

    Valid outcomes are `mask` and `authentic`; ties/inadequate visits use
    ``None``. The routine refuses to extrapolate absent crossings and returns
    `nonmonotone` if more than one observed transition appears.
    """
    if target_width <= 0.0 or max_added < 0:
        raise ValueError("invalid learned-refinement bounds")
    seen = dict(observations)
    added: list[float] = []
    while True:
        ordered = sorted(seen.items())
        if any(action not in {"mask", "authentic"} for _, action in ordered):
            return {"status": "censored_inconclusive", "observations": seen, "added_p": added, "reversals": 0, "bracket": None}
        transitions = [(left, right) for left, right in zip(ordered, ordered[1:]) if left[1] != right[1]]
        if not transitions:
            return {"status": "censored_no_crossing", "observations": seen, "added_p": added, "reversals": 0, "bracket": None}
        if len(transitions) > 1:
            return {"status": "nonmonotone", "observations": seen, "added_p": added, "reversals": len(transitions) - 1, "bracket": None}
        (left_p, left_action), (right_p, right_action) = transitions[0]
        width = right_p - left_p
        if width <= target_width:
            return {"status": "bracketed", "observations": seen, "added_p": added, "reversals": 0, "bracket": (left_p, right_p, left_action, right_action)}
        if len(added) >= max_added:
            return {"status": "censored_budget", "observations": seen, "added_p": added, "reversals": 0, "bracket": (left_p, right_p, left_action, right_action)}
        midpoint = (left_p + right_p) / 2.0
        seen[midpoint] = evaluate(midpoint)
        added.append(midpoint)


def standard_harsh_cases(config: dict[str, Any]) -> list[M2Params]:
    """Expose, but do not execute, the approved `b2=0` harsh M2 cells."""
    harsh = config["harsh_sentinel"]
    return [M2Params(p=float(p), eta=float(harsh["eta"]), b=1.0, a=0.6, c=0.25, r=2.0, b2=float(harsh["b2"]), r2=float(harsh["r2"]), delta=float(harsh["delta"]), gamma=float(harsh["gamma"]), lam=1.0) for p in harsh["p"]]


class E03StreamingAggregator:
    """Constant-memory raw-row aggregator for the future standard writer."""

    def __init__(self) -> None:
        self._totals: dict[str, dict[str, float]] = {}

    def add(self, row: dict[str, object]) -> None:
        cell = str(row["parameter_cell_id"])
        record = self._totals.setdefault(cell, {"n": 0.0, "mask": 0.0, "reward": 0.0})
        record["n"] += 1.0; record["mask"] += float(row["final_window_mask_rate"]); record["reward"] += float(row["final_window_objective_reward_mean"])

    def summaries(self) -> list[dict[str, object]]:
        return [{"parameter_cell_id": cell, "n": int(total["n"]), "mean_final_window_mask_rate": total["mask"] / total["n"], "mean_final_window_objective_reward": total["reward"] / total["n"]} for cell, total in sorted(self._totals.items())]


def stream_e03_raw_rows(path: Path, chunks: Iterable[Iterable[dict[str, object]]]) -> list[dict[str, object]]:
    """Write chunks and aggregate in one pass; never retain/re-read raw rows."""
    aggregator = E03StreamingAggregator()
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=E03_RAW_FIELDNAMES); writer.writeheader()
        for chunk in chunks:
            for row in chunk:
                ordered = {field: row[field] for field in E03_RAW_FIELDNAMES}
                writer.writerow(ordered); aggregator.add(ordered)
    return aggregator.summaries()


def standard_streaming_cost_plan() -> dict[str, object]:
    """Frozen capacity target for future authorization; no standard simulation."""
    return {"new_learner_steps": 408_000_000, "legacy_replay_steps": 57_120_000, "estimated_primary_rows": 384_000, "measured_raw_bytes": 390_912_614, "measured_raw_mib": 372.8, "raw_bound_mib": "~400", "streaming_peak_mib": 35.6, "peak_memory_target_gib": 2, "accepted_runtime_minutes": "2.8-4", "strategy": "cell/chunk streaming CSV writer plus online aggregation; never retain or reread all raw rows"}


def _threshold_rows(config: dict[str, Any]) -> list[dict[str, object]]:
    rows = []
    for eta in (0.0, 0.2, 0.8):
        result = objective_threshold_bisection(_params(config, 0.0, eta), tolerance=1e-4)
        rows.append({"run_id": config["run_id"], "experiment_id": "E03", "tier": "smoke", "eta": eta, "threshold_kind": "objective_dynamic_authenticity", "lower_p": result["lower_p"], "upper_p": result["upper_p"], "midpoint_p": result["midpoint_p"], "bracket_width": result["bracket_width"], "status": result["status"], "notes": "learned refinement is staged in unexecuted standard config"})
    return [{field: _format(row[field]) for field in E03_THRESHOLD_FIELDS} for row in rows]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(root: Path, args: list[str], *, text: bool = True) -> str | bytes | None:
    try:
        result = subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=text)
        return result.stdout.strip() if text else result.stdout
    except Exception:
        return None


SOURCE_FINGERPRINT_PATHS = (
    "src/gifted_masking/experiments/e03.py", "src/gifted_masking/cli.py", "src/gifted_masking/models/m2.py", "src/gifted_masking/analysis/m2_optimal.py",
    "scripts/map_m2_lock_in_regions.py", "configs/frontiers_article/e03_m2_regime_smoke.json", "configs/frontiers_article/e03_m2_regime_standard.json", "projects/frontiers_article/approvals/E03_STANDARD_GO.md", "tests/test_article_e03.py",
)


def _source_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for relative in SOURCE_FINGERPRINT_PATHS:
        path = root / relative
        if path.is_file():
            digest.update(relative.encode()); digest.update(path.read_bytes())
    return digest.hexdigest()


def _validate_e03_standard_approval(repo_root: Path, approval_record: Path | None) -> Path:
    """Reserve a narrowly scoped future E03 GO record; smoke approval is invalid."""
    expected = (repo_root / E03_STANDARD_APPROVAL_RELATIVE).resolve()
    if approval_record is None or approval_record.resolve() != expected or not expected.is_file():
        raise PermissionError("standard E03 execution requires the canonical E03-specific GO_STANDARD approval record")
    required = (
        "# E03 Standard Execution Authorization", "**Decision:** `GO_STANDARD`", "exact frozen E03 standard execution only",
        "e03_m2_regime_standard.json", "five reserved", "No config mutation, factor crossing, additional sensitivity, publication-tier",
    )
    if not all(item in expected.read_text() for item in required):
        raise PermissionError("E03 standard approval record does not satisfy the frozen Pass-D authorization contract")
    return expected


def _standard_spec(
    config: dict[str, Any], *, component: str, sensitivity_name: str, p: float, eta: float,
    n: int, horizon: int, window: float, environment: dict[str, float] | None = None, learner: dict[str, float] | None = None,
) -> dict[str, object]:
    env, learner_values = dict(config["environment"]), dict(config["learner"])
    if environment:
        env.update(environment)
    if learner:
        learner_values.update(learner)
    cell = {"p": float(p), "eta": float(eta)}
    cell_id = canonical_e03_cell_id(config, cell, component=component, sensitivity_name=sensitivity_name, n=n, horizon=horizon, window=window, environment=env, learner=learner_values)
    family = e03_rng_family_id(config if env == config["environment"] and learner_values == config["learner"] else {**config, "environment": env, "learner": learner_values}, cell, component=component, sensitivity_name=sensitivity_name, n=n, horizon=horizon, window=window)
    return {"component": component, "sensitivity_name": sensitivity_name, "p": float(p), "eta": float(eta), "n": int(n), "T": int(horizon), "final_window_fraction": float(window), "environment": env, "learner": learner_values, "parameter_cell_id": cell_id, "rng_family_id": family}


def _standard_specs(config: dict[str, Any]) -> list[dict[str, object]]:
    """Enumerate exactly the GO-authorized standard cells; no factor crossings."""
    grid = config["exact_grid"]
    specs = []
    for eta_index in range(17):
        for p_index in range(21):
            specs.append(_standard_spec(config, component="exact_grid", sensitivity_name="baseline", p=eta_index * 0 + p_index * .05, eta=eta_index * .05, n=160, horizon=1000, window=.2))
    for sentinel in config["sentinels"]:
        p, eta = float(sentinel["p"]), float(sentinel["eta"])
        specs.append(_standard_spec(config, component="sentinels", sensitivity_name="baseline", p=p, eta=eta, n=160, horizon=1000, window=.2))
        specs.append(_standard_spec(config, component="sentinels", sensitivity_name="n", p=p, eta=eta, n=320, horizon=1000, window=.2))
        for horizon in config["one_at_a_time"]["T"]:
            specs.append(_standard_spec(config, component="sentinels", sensitivity_name="T", p=p, eta=eta, n=160, horizon=int(horizon), window=.2))
        for window in config["one_at_a_time"]["final_window_fraction"]:
            specs.append(_standard_spec(config, component="sentinels", sensitivity_name="final_window_fraction", p=p, eta=eta, n=160, horizon=1000, window=float(window)))
        for field in ("alpha", "tau", "lambda", "q0", "gamma"):
            for value in config["one_at_a_time"][field]:
                specs.append(_standard_spec(config, component="sentinels", sensitivity_name=field, p=p, eta=eta, n=160, horizon=1000, window=.2, learner={field: float(value)}))
    harsh = config["harsh_sentinel"]
    for p in harsh["p"]:
        specs.append(_standard_spec(config, component="harsh", sensitivity_name="b2_r2_delta", p=float(p), eta=float(harsh["eta"]), n=160, horizon=1000, window=.2, environment={"b2": float(harsh["b2"]), "r2": float(harsh["r2"]), "delta": float(harsh["delta"])}, learner={"gamma": float(harsh["gamma"])}))
    return sorted(specs, key=lambda spec: str(spec["parameter_cell_id"]))


def _simulate_standard_spec(config: dict[str, Any], spec: dict[str, object], master_seed: int) -> tuple[list[dict[str, object]], dict[str, object], dict[str, object]]:
    """Run one bounded standard cell through the maintained vectorized M2 kernel."""
    n, horizon, window_fraction = int(spec["n"]), int(spec["T"]), float(spec["final_window_fraction"])
    window = int(math.ceil(horizon * window_fraction))
    seed = derive_e03_cell_seed(master_seed, str(spec["rng_family_id"]))
    env, learner = spec["environment"], spec["learner"]
    diagnostics = m2.simulate_with_diagnostics(float(spec["p"]), float(spec["eta"]), n=n, horizon=horizon, seed=seed, **env, alpha=float(learner["alpha"]), temp=float(learner["tau"]), lam=float(learner["lambda"]), q0=float(learner["q0"]), gamma=float(learner["gamma"]), final_window_fraction=window_fraction)
    params = M2Params(p=float(spec["p"]), eta=float(spec["eta"]), **env, gamma=float(learner["gamma"]), lam=float(learner["lambda"]))
    classified = classify_e03_cell(params, diagnostics, n=n)
    counts, visits = np.asarray(diagnostics["state_action_counts_final"], dtype=int), np.asarray(diagnostics["state_visit_counts_final"], dtype=int)
    masks, rewards, final_states = (np.asarray(diagnostics[key]) for key in ("mask_rate_final", "reward_mean_final", "final_state"))
    rows: list[dict[str, object]] = []
    for child_id in range(n):
        values = {
            "run_id": config["run_id"], "experiment_id": "E03", "tier": "standard", "model": "M2", "component": spec["component"], "sensitivity_name": spec["sensitivity_name"],
            "master_seed": master_seed, "parameter_cell_id": spec["parameter_cell_id"], "cell_seed": seed, "child_id": child_id, "child_seed": "", "rng_unit": "vectorized_cell_stream", "rng_family_id": spec["rng_family_id"], "trajectory_prefix_family": spec["rng_family_id"],
            "p": spec["p"], "eta": spec["eta"], **env, **learner, "n": n, "T": horizon, "final_window_fraction": window_fraction, "final_window_start": horizon - window, "final_window_end": horizon - 1,
            "final_window_mask_count": int(round(float(masks[child_id]) * window)), "final_window_mask_rate": masks[child_id], "final_window_objective_reward_sum": rewards[child_id] * window, "final_window_objective_reward_mean": rewards[child_id],
            "neutral_mask_count": counts[child_id, 0, 0], "neutral_authentic_count": counts[child_id, 0, 1], "accepted_mask_count": counts[child_id, 1, 0], "accepted_authentic_count": counts[child_id, 1, 1], "stigmatized_mask_count": counts[child_id, 2, 0], "stigmatized_authentic_count": counts[child_id, 2, 1], "neutral_visit_count": visits[child_id, 0], "accepted_visit_count": visits[child_id, 1], "stigmatized_visit_count": visits[child_id, 2], "final_state": STATE_NAMES[int(final_states[child_id])],
        }
        rows.append({field: _format(values[field]) for field in E03_RAW_FIELDNAMES})
    return rows, classified, {**spec, "master_seed": master_seed, "cell_seed": seed}


def _standard_cell_row(config: dict[str, Any], classified: dict[str, object], spec: dict[str, object]) -> dict[str, object]:
    solution, adequacy = classified["solution"], classified["adequacy"]
    env, learner = spec["environment"], spec["learner"]
    values = {
        "run_id": config["run_id"], "experiment_id": "E03", "tier": "standard", "component": spec["component"], "sensitivity_name": spec["sensitivity_name"], "master_seed": spec["master_seed"], "parameter_cell_id": spec["parameter_cell_id"], "cell_seed": spec["cell_seed"], "p": spec["p"], "eta": spec["eta"], **env, **learner, "n": spec["n"], "T": spec["T"], "final_window_fraction": spec["final_window_fraction"],
        "vi_converged": solution["converged"], "vi_iterations": solution["iterations"], "vi_residual": solution["residual"], "static_neutral_action": classified["static"]["optimal_action"], "objective_neutral_action": classified["objective_action"], "objective_neutral_q_gap_auth_minus_mask": classified["q_gap"], "objective_regime": classified["objective_regime"], "neutral_mask_probability": classified["neutral_mask_probability"], "learned_neutral_action": classified["learned_action"], "learner_status": classified["learner_status"], "neutral_visits_total": adequacy["neutral"]["total"], "neutral_visiting_children": adequacy["neutral"]["children"], "neutral_visit_adequate": adequacy["neutral"]["adequate"], "accepted_visits_total": adequacy["accepted"]["total"], "stigmatized_visits_total": adequacy["stigmatized"]["total"], "full_policy_value_neutral": classified["full_policy_value"], "full_policy_regret_neutral": classified["full_policy_regret"], "full_policy_status": classified["full_policy_status"], "neutral_decision_regret": classified["neutral_decision_regret"], "mean_final_window_mask_rate": classified["mean_final_window_mask_rate"], "mean_final_window_objective_reward": classified["mean_final_window_objective_reward"], "legacy_region": classified["legacy_region"], "classification": classified["classification"],
    }
    return {field: _format(values[field]) for field in E03_CELL_FIELDS}


def _figure(path: Path, cells: list[dict[str, object]]) -> None:
    cache = Path(tempfile.gettempdir()) / "gifted_masking_matplotlib"
    cache.mkdir(parents=True, exist_ok=True); os.environ.setdefault("MPLCONFIGDIR", str(cache))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    figure, axis = plt.subplots(figsize=(7.5, 4.2))
    labels = [f"p={row['p']}, eta={row['eta']}" for row in cells]
    values = [float(row["neutral_mask_probability"]) if row["neutral_mask_probability"] != "" else np.nan for row in cells]
    colors = ["#cc6677" if row["classification"] == "learned_suboptimal_masking" else "#4477aa" for row in cells]
    axis.bar(range(len(cells)), values, color=colors); axis.set_ylim(0, 1); axis.set_ylabel("Final-window neutral masking probability")
    axis.set_xticks(range(len(cells)), labels, rotation=25, ha="right", fontsize=8); axis.set_title("E03 smoke sentinels (diagnostic only)")
    figure.tight_layout(); figure.savefig(path, dpi=150); plt.close(figure)


def _report(config: dict[str, Any], outputs: dict[str, Path], elapsed: float, raw_count: int, legacy: dict[str, object], warnings: list[str], verification: str = "pending_external_tests") -> str:
    paths = "\n".join(f"- `{path}`" for path in outputs.values())
    return f"""# E03 Smoke Checkpoint

1. **Experiment and run ID:** E03; `{config['run_id']}`.
2. **Scope and authority:** bounded `APPROVED_FOR_SMOKE` implementation only; no standard, sensitivity, claim, ledger, or manuscript work was executed.
3. **Maintained semantics:** `models/m2.py` remained unchanged. The runner calls its vectorized reward-first diagnostic kernel; turnover and escape affect next state only.
4. **Frozen smoke:** 357 historic replay cells at n=160/T=1000/window=.2 plus six new-stream sentinels at n=64/T=300/window=.2; workers=1.
5. **Legacy provenance gate:** {legacy['rows']} rows, {legacy['learned_suboptimal_count']}/357 learned-suboptimal, fraction={legacy['fraction']}, classified neutral-mask mean={legacy['mean_neutral_mask_probability']}, SHA-256 `{legacy['sha256']}`.
6. **Comparator:** objective, reward-first transition table; VI tolerance=1e-10, max iterations=100000, absolute Q tie tolerance=1e-10; every emitted comparison converged.
7. **Classification:** `legacy_region`, `objective_regime`, and `learner_status` are distinct. Neutral ties/inadequate visits are inconclusive; full policy value/regret is blank unless every dynamically required state is visit-adequate.
8. **New-stream RNG:** each `parameter_cell_id` retains every run parameter; its recorded `rng_family_id` is SHA-256 hashed into four little-endian uint32 words and fed to `SeedSequence([master_seed,3,...])`. Only approved default standard T/window OAT variants share a family; smoke cells remain one family per full parameter ID and child seeds are blank.
9. **Reconciliation:** {raw_count} raw child rows; within every state mask+authentic counts equal visits, and all final mask and final-window objective reward identities reconciled exactly. Smoke intervals are intentionally not estimable.
10. **Artifacts:**
{paths}
11. **Cost and staged standard:** {elapsed:.3f}s wall time; raw storage={outputs['raw'].stat().st_size} bytes. The staged five-seed standard/refinement config is validated but intentionally non-executable. Its streaming plan is 408m new plus 57.12m legacy learner-steps, about 384k rows, measured 390,912,614 bytes (372.8 MiB) with a conservative ~400 MiB raw bound, ~35.6 MiB streaming peak (<2 GiB cap), and accepted 2.8-4 minute runtime via chunked CSV writing plus online aggregation without rereading raw data.
12. **Warnings and interpretation limits:** {', '.join(warnings) if warnings else 'none'}; the historic 226/357 is provenance only, not a publication headline or prevalence estimate.
13. **Pending scientific gate:** `PENDING_SOL_SMOKE_REVIEW`; stop before standard execution, sensitivity, claim adjudication, ledger update, or manuscript edit.

Targeted tests and external repository verification are recorded in the manifest after they run.
"""


def _standard_figure(path: Path, cells: list[dict[str, object]]) -> None:
    cache = Path(tempfile.gettempdir()) / "gifted_masking_matplotlib"
    cache.mkdir(parents=True, exist_ok=True); os.environ.setdefault("MPLCONFIGDIR", str(cache))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    exact = [row for row in cells if row["component"] == "exact_grid"]
    grid: dict[tuple[float, float], list[dict[str, object]]] = defaultdict(list)
    for row in exact:
        grid[(float(row["p"]), float(row["eta"]))].append(row)
    p_values, eta_values = [index * .05 for index in range(21)], [index * .05 for index in range(17)]
    image = np.zeros((len(eta_values), len(p_values)), dtype=float)
    for eta_index, eta in enumerate(eta_values):
        for p_index, p in enumerate(p_values):
            records = grid[(p, eta)]
            image[eta_index, p_index] = sum(row["classification"] == "learned_suboptimal_masking" for row in records) / len(records)
    figure, axis = plt.subplots(figsize=(8.4, 4.8)); im = axis.imshow(image, origin="lower", aspect="auto", vmin=0, vmax=1, cmap="magma")
    axis.set(title="E03 standard: learned-suboptimal masking frequency", xlabel="receptivity p", ylabel="escape eta")
    axis.set_xticks(range(0, 21, 4), [f"{p_values[index]:.1f}" for index in range(0, 21, 4)]); axis.set_yticks(range(0, 17, 4), [f"{eta_values[index]:.1f}" for index in range(0, 17, 4)])
    figure.colorbar(im, ax=axis, label="fraction of five master seeds"); figure.tight_layout(); figure.savefig(path, dpi=150); plt.close(figure)


def _standard_report(config: dict[str, Any], outputs: dict[str, Path], *, elapsed: float, raw_count: int, learner_steps: int, legacy: dict[str, object], warnings: list[str], verification: str) -> str:
    paths = "\n".join(f"- `{path}`" for path in outputs.values())
    return f"""# E03 Standard Execution Report

1. **Experiment and run ID:** E03; `{config['run_id']}`.
2. **Authority:** canonical `E03_STANDARD_GO.md`; exact frozen Pass D only.
3. **Frozen design:** five reserved seeds; exact 21×17 grid (denominator 357), six sentinels with one-factor-at-a-time variants, three `b2=0` harsh cells, and bounded objective/learned refinement.
4. **Semantics:** maintained reward-first M2 kernel and objective value iteration (tolerance `1e-10`, max `100000`) only; no model/default/RNG semantic change.
5. **RNG and pairing:** canonical component-aware parameter IDs; SHA-256 `rng_family_id` streams; only approved default T/window OAT cells share a trajectory prefix.
6. **Classification:** exact-grid five-seed fractions, Student-t intervals, and stability use only canonical exact-grid rows. Ties/insufficient visits remain inconclusive.
7. **Provenance replay:** {legacy['rows']} rows; {legacy['learned_suboptimal_count']}/357; fraction `{legacy['fraction']}`; fsum neutral-mask mean `{legacy['mean_neutral_mask_probability']}`; SHA-256 `{legacy['sha256']}`.
8. **Reconciliation:** streamed child rows were checked state-by-state (mask+authentic=visits), final-window counts/rewards, per-cell summaries, VI convergence, and canonical exact-grid grouping before output.
9. **Thresholds:** objective bisection is bounded to width <=`1e-4`; learned refinement reports bracket, censoring, or nonmonotonicity and never extrapolates a missing crossing.
10. **Artifacts:**
{paths}
11. **Actual cost:** {raw_count} primary rows; {learner_steps} new learner-steps plus 57,120,000 legacy replay steps; {elapsed:.3f}s wall; raw storage={outputs['raw'].stat().st_size} bytes. Limits: <400 MiB raw, <2 GiB peak, and <=4 minutes per generation.
12. **Warnings/interpretation:** {', '.join(warnings) if warnings else 'none'}; results await separate claim adjudication and cannot be treated as prevalence or publication evidence yet.
13. **Post-run verification:** {verification}. Stop before adjudication, publication-tier work, claim/ledger updates, or manuscript edits.
"""


def _write_standard_raw_batch(writer: csv.DictWriter, handle: Any, path: Path, rows: list[dict[str, object]], *, raw_limit: int) -> None:
    for row in rows:
        writer.writerow({field: row[field] for field in E03_RAW_FIELDNAMES})
    handle.flush()
    if path.stat().st_size > raw_limit:
        raise RuntimeError("E03 standard raw output exceeded the authorized ~400 MiB limit")


def _standard_outputs(dirs: dict[str, Path], run_id: str) -> dict[str, Path]:
    return {
        "manifest": dirs["manifests"] / f"{run_id}.json", "raw": dirs["raw"] / f"{run_id}_units.csv", "cells": dirs["summaries"] / f"{run_id}_cells.csv",
        "effects": dirs["summaries"] / f"{run_id}_effects.csv", "stable": dirs["summaries"] / f"{run_id}_stable_cells.csv", "thresholds": dirs["summaries"] / f"{run_id}_thresholds.csv",
        "legacy": dirs["summaries"] / f"{run_id}_legacy_replay.csv", "figure": dirs["figures"] / f"{run_id}_standard_regime_diagnostics.png", "report": dirs["reports"] / f"{run_id}_report.md",
    }


def run_e03_standard_experiment(config_path: Path, output_dir: Path | None, approval_record: Path | None) -> dict[str, Path]:
    """Execute only the canonical GO-authorized E03 standard design.

    Child rows are written cell-by-cell.  The retained records are cell-level
    classifications (roughly two thousand rows), never the raw population.
    """
    config = load_e03_config(config_path)
    root = Path(__file__).resolve().parents[3]
    approval = _validate_e03_standard_approval(root, approval_record)
    dirs = ensure_results_dirs(output_dir or root / "results")
    outputs = _standard_outputs(dirs, str(config["run_id"]))
    started, started_perf = datetime.now(timezone.utc).isoformat(), time.perf_counter()
    raw_limit, row_limit, runtime_limit = 400 * 1024 * 1024, 384_000, 4.0 * 60.0
    warnings: list[str] = []

    legacy_rows, legacy_stats = _legacy_replay_rows()
    write_csv(outputs["legacy"], legacy_rows)
    if _sha(outputs["legacy"]) != LEGACY_MAP_SHA256:
        raise RuntimeError("written E03 legacy replay hash differs from frozen map hash")

    cells: list[dict[str, object]] = []
    seed_map: list[dict[str, object]] = []
    raw_count, learner_steps = 0, 0

    def enforce_runtime() -> None:
        if time.perf_counter() - started_perf > runtime_limit:
            raise RuntimeError("E03 standard generation exceeded the authorized four-minute runtime limit")

    def execute_spec(spec: dict[str, object], master_seed: int, writer: csv.DictWriter, handle: Any) -> dict[str, object]:
        nonlocal raw_count, learner_steps
        enforce_runtime()
        rows, classified, seeded_spec = _simulate_standard_spec(config, spec, master_seed)
        reconstructed = recompute_e03_summaries(rows, config)
        if len(reconstructed) != 1:
            raise RuntimeError("E03 standard cell produced an ambiguous raw reconciliation")
        cell_row = _standard_cell_row(config, classified, seeded_spec)
        recovered = reconstructed[0]
        for metric in ("mean_final_window_mask_rate", "mean_final_window_objective_reward"):
            if not math.isclose(float(recovered[metric]), float(cell_row[metric]), rel_tol=0.0, abs_tol=1e-12):
                raise RuntimeError(f"E03 standard raw/cell {metric} mismatch")
        _write_standard_raw_batch(writer, handle, outputs["raw"], rows, raw_limit=raw_limit)
        raw_count += len(rows)
        learner_steps += int(spec["n"]) * int(spec["T"])
        if raw_count > row_limit:
            raise RuntimeError("E03 standard primary-row count exceeded the authorized 384,000-row plan")
        cells.append(cell_row)
        seed_map.append({"master_seed": master_seed, "parameter_cell_id": spec["parameter_cell_id"], "rng_family_id": spec["rng_family_id"], "cell_seed": seeded_spec["cell_seed"], "component": spec["component"], "sensitivity_name": spec["sensitivity_name"]})
        return cell_row

    with outputs["raw"].open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=E03_RAW_FIELDNAMES)
        writer.writeheader()
        for spec in _standard_specs(config):
            for master_seed in E03_STANDARD_MASTER_SEEDS:
                execute_spec(spec, master_seed, writer, handle)

        # Learned refinement is limited to consensus actions from the frozen
        # exact grid.  Inconclusive cells are censoring evidence, never votes.
        thresholds: list[dict[str, object]] = []
        for eta in config["threshold_refinement"]["etas"]:
            objective = objective_threshold_bisection(_params(config, 0.0, float(eta)), tolerance=float(config["threshold_refinement"]["objective_bracket_tolerance"]))
            thresholds.append({"run_id": config["run_id"], "experiment_id": "E03", "tier": "standard", "eta": eta, "threshold_kind": "objective_dynamic_authenticity", **objective, "notes": "value-iteration bisection; frozen tolerance"})
            initial: dict[float, str | None] = {}
            exact_for_eta = [row for row in cells if row["component"] == "exact_grid" and float(row["eta"]) == float(eta)]
            for p in sorted({float(row["p"]) for row in exact_for_eta}):
                actions = {str(row["learned_neutral_action"]) for row in exact_for_eta if float(row["p"]) == p}
                initial[p] = next(iter(actions)) if actions in ({"mask"}, {"authentic"}) else None

            def evaluate(midpoint: float) -> str | None:
                spec = _standard_spec(config, component="threshold_refinement", sensitivity_name="learned_dyadic", p=midpoint, eta=float(eta), n=160, horizon=1000, window=.2)
                records = [execute_spec(spec, master_seed, writer, handle) for master_seed in E03_STANDARD_MASTER_SEEDS]
                actions = {str(row["learned_neutral_action"]) for row in records}
                return next(iter(actions)) if actions in ({"mask"}, {"authentic"}) else None

            learned = refine_learned_threshold(initial, evaluate, target_width=float(config["threshold_refinement"]["learned_target_width"]), max_added=int(config["threshold_refinement"]["learned_max_added_p_per_eta"]))
            bracket = learned["bracket"]
            thresholds.append({
                "run_id": config["run_id"], "experiment_id": "E03", "tier": "standard", "eta": eta, "threshold_kind": "learned_neutral_dyadic",
                "lower_p": bracket[0] if bracket else "", "upper_p": bracket[1] if bracket else "", "midpoint_p": (bracket[0] + bracket[1]) / 2.0 if bracket else "", "bracket_width": bracket[1] - bracket[0] if bracket else "", "status": learned["status"],
                "notes": _canonical_json({"added_p": learned["added_p"], "reversals": learned["reversals"], "observations": learned["observations"]}),
            })
    enforce_runtime()
    if outputs["raw"].stat().st_size > raw_limit:
        raise RuntimeError("E03 standard raw output exceeded the authorized ~400 MiB limit")

    exact_cells = [row for row in cells if row["component"] == "exact_grid"]
    effects_raw, stable_raw = summarize_e03_standard_classifications(exact_cells, config)
    effects = [{"run_id": config["run_id"], "experiment_id": "E03", "tier": "standard", "component": "exact_grid", **row} for row in effects_raw]
    canonical_grid = canonical_e03_exact_grid(config)
    stable = [{"run_id": config["run_id"], "experiment_id": "E03", "tier": "standard", "p": canonical_grid[row["parameter_cell_id"]]["p"], "eta": canonical_grid[row["parameter_cell_id"]]["eta"], **row} for row in stable_raw]
    cells.sort(key=lambda row: (str(row["component"]), str(row["sensitivity_name"]), float(row["eta"]), float(row["p"]), int(row["master_seed"])))
    write_csv(outputs["cells"], cells)
    write_csv(outputs["effects"], [{field: _format(row[field]) for field in E03_EFFECT_FIELDS} for row in effects])
    write_csv(outputs["stable"], [{field: _format(row[field]) for field in E03_STABLE_FIELDS} for row in stable])
    write_csv(outputs["thresholds"], [{field: _format(row[field]) for field in E03_THRESHOLD_FIELDS} for row in thresholds])
    _standard_figure(outputs["figure"], cells)
    elapsed = time.perf_counter() - started_perf
    if learner_steps > 408_000_000:
        raise RuntimeError("E03 standard learner-step budget exceeded the approved 408,000,000 new steps")
    if elapsed > runtime_limit:
        raise RuntimeError("E03 standard generation exceeded the authorized four-minute runtime limit")

    porcelain = _git(root, ["status", "--porcelain"]) or ""
    dirty_diff = _git(root, ["diff", "--no-ext-diff"], text=False) or b""
    git = {"commit": _git(root, ["rev-parse", "HEAD"]), "dirty": bool(porcelain), "porcelain_sha256": hashlib.sha256(str(porcelain).encode()).hexdigest(), "dirty_diff_sha256": hashlib.sha256(bytes(dirty_diff) + str(porcelain).encode()).hexdigest(), "source_fingerprint_sha256": _source_fingerprint(root)}
    outputs["report"].write_text(_standard_report(config, outputs, elapsed=elapsed, raw_count=raw_count, learner_steps=learner_steps, legacy=legacy_stats, warnings=warnings, verification="pending_independent_regeneration_and_repository_tests"))
    output_hashes = {name: {"sha256": _sha(path), "bytes": path.stat().st_size} for name, path in outputs.items() if name != "manifest"}
    command = f"PYTHONPATH=src {sys.executable} -m gifted_masking.cli article-experiment --config {config_path} --approval-record {approval}"
    output_rows = {
        "raw": raw_count, "cells": len(cells), "effects": len(effects), "stable": len(stable),
        "thresholds": len(thresholds), "legacy": len(legacy_rows),
    }
    manifest = {
        "run_id": config["run_id"], "experiment_id": "E03", "tier": "standard", "config_path": str(config_path), "normalized_config": _canonical_json(config), "config_sha256": hashlib.sha256(_canonical_json(config).encode()).hexdigest(), "command": command,
        "authorization": {"record": str(approval), "decision": "GO_STANDARD", "scope": "exact frozen E03 standard execution only"}, "git": git,
        "environment": {"python_version": sys.version, "platform": platform.platform(), "numpy": np.__version__}, "parameters": config, "legacy_provenance": legacy_stats,
        "seed_hierarchy": {"legacy": "seed=9100 + 100*eta_index + p_index", "new": "SHA-256 rng_family_id -> first 16 bytes as four little-endian uint32 -> SeedSequence([master_seed, 3, words...]).spawn(1) uint64", "rng_unit": "vectorized_cell_stream", "trajectory_prefix_pairing": "only approved default standard T/window OAT variants share a family; parameter_cell_id always includes T/window", "cells": seed_map},
        "standard_streaming_cost_plan": standard_streaming_cost_plan(), "actual_execution": {"primary_rows": raw_count, "new_learner_steps": learner_steps, "legacy_replay_steps": 57_120_000, "raw_bytes": outputs["raw"].stat().st_size, "raw_limit_bytes": raw_limit, "runtime_limit_seconds": runtime_limit}, "sort_keys": ["component", "sensitivity_name", "eta", "p", "master_seed"],
        "outputs": {name: {"path": str(path), "rows": output_rows.get(name)} for name, path in outputs.items()}, "output_hashes": output_hashes, "timing": {"wall_seconds": elapsed}, "warnings": warnings, "verification": {"status": "pending_independent_regeneration_and_repository_tests", "command": "./scripts/verify.sh"}, "timestamps": {"start_utc": started, "end_utc": datetime.now(timezone.utc).isoformat()},
    }
    write_json(outputs["manifest"], manifest)
    return outputs


def run_e03_experiment(config_path: Path, output_dir: Path | None = None, approval_record: Path | None = None) -> dict[str, Path]:
    config = load_e03_config(config_path)
    root = Path(__file__).resolve().parents[3]
    if config["tier"] != "smoke":
        return run_e03_standard_experiment(config_path, output_dir, approval_record)
    dirs = ensure_results_dirs(output_dir or root / "results")
    run_id = str(config["run_id"])
    outputs = {
        "manifest": dirs["manifests"] / f"{run_id}.json", "raw": dirs["raw"] / f"{run_id}_units.csv", "cells": dirs["summaries"] / f"{run_id}_cells.csv",
        "effects": dirs["summaries"] / f"{run_id}_effects.csv", "stable": dirs["summaries"] / f"{run_id}_stable_cells.csv", "thresholds": dirs["summaries"] / f"{run_id}_thresholds.csv",
        "legacy": dirs["summaries"] / f"{run_id}_legacy_replay.csv", "figure": dirs["figures"] / f"{run_id}_sentinel_diagnostics.png", "report": dirs["reports"] / f"{run_id}_report.md",
    }
    started = datetime.now(timezone.utc).isoformat(); started_perf = time.perf_counter()
    legacy_rows, legacy_stats = _legacy_replay_rows()  # Gate new evidence on exact historic provenance first.
    write_csv(outputs["legacy"], legacy_rows)
    if _sha(outputs["legacy"]) != LEGACY_MAP_SHA256:
        raise RuntimeError("written E03 legacy replay hash differs from frozen map hash")
    raw_rows: list[dict[str, object]] = []; cells: list[dict[str, object]] = []; seed_map: list[dict[str, object]] = []
    for cell in sorted(config["smoke_sentinels"], key=lambda row: (float(row["eta"]), float(row["p"]))):
        cell_id = canonical_e03_cell_id(config, cell)
        family_id = e03_rng_family_id(config, cell, component="smoke_sentinels", sensitivity_name="baseline", n=int(config["n"]), horizon=int(config["T"]), window=float(config["final_window_fraction"]))
        seed = derive_e03_cell_seed(int(config["master_seed"]), family_id)
        rows, classified = simulate_e03_sentinel(config, cell, cell_id, seed, family_id)
        raw_rows.extend(rows); cells.append(_cell_rows(config, classified, cell, cell_id, seed)); seed_map.append({"parameter_cell_id": cell_id, "rng_family_id": family_id, "cell_seed": seed})
    raw_rows.sort(key=lambda row: (str(row["parameter_cell_id"]), int(row["child_id"])))
    cells.sort(key=lambda row: str(row["parameter_cell_id"]))
    write_csv(outputs["raw"], raw_rows); write_csv(outputs["cells"], cells)
    with outputs["raw"].open(newline="") as handle:
        reconstructed = recompute_e03_summaries(list(csv.DictReader(handle)), config)
    by_cell = {str(row["parameter_cell_id"]): row for row in cells}
    for row in reconstructed:
        stored = by_cell[str(row["parameter_cell_id"])]
        if not math.isclose(float(row["mean_final_window_mask_rate"]), float(stored["mean_final_window_mask_rate"]), rel_tol=0.0, abs_tol=1e-12):
            raise RuntimeError("E03 raw mean mask summary mismatch")
        if not math.isclose(float(row["mean_final_window_objective_reward"]), float(stored["mean_final_window_objective_reward"]), rel_tol=0.0, abs_tol=1e-12):
            raise RuntimeError("E03 raw mean reward summary mismatch")
    learned_count = sum(row["classification"] == "learned_suboptimal_masking" for row in cells)
    effects = [{"run_id": run_id, "experiment_id": "E03", "tier": "smoke", "component": "smoke_sentinels", "effect_name": "learned_suboptimal_masking_fraction", "level": "master_seed", "master_seed": config["master_seed"], "denominator": len(cells), "estimate": learned_count / len(cells), "ci_status": "not_estimable_smoke", "ci_low": "", "ci_high": "", "notes": "six diagnostic sentinels only; not an exact-grid estimate"}]
    stable = [{"run_id": run_id, "experiment_id": "E03", "tier": "smoke", "parameter_cell_id": row["parameter_cell_id"], "p": row["p"], "eta": row["eta"], "classification": row["classification"], "non_inconclusive_seed_count": 0 if row["classification"] == "inconclusive" else 1, "matching_seed_count": 0 if row["classification"] == "inconclusive" else 1, "stable": "", "notes": "requires five standard master seeds; staged only"} for row in cells]
    thresholds = _threshold_rows(config)
    write_csv(outputs["effects"], [{field: _format(row[field]) for field in E03_EFFECT_FIELDS} for row in effects])
    write_csv(outputs["stable"], [{field: _format(row[field]) for field in E03_STABLE_FIELDS} for row in stable]); write_csv(outputs["thresholds"], thresholds); _figure(outputs["figure"], cells)
    elapsed = time.perf_counter() - started_perf
    warnings = []
    if elapsed > 60.0:
        warnings.append("smoke runtime exceeded 60 seconds")
    if outputs["raw"].stat().st_size > 20 * 1024 * 1024:
        warnings.append("smoke raw output exceeded 20 MiB")
    if warnings:
        raise RuntimeError("; ".join(warnings))
    porcelain = _git(root, ["status", "--porcelain"]) or ""
    dirty_diff = _git(root, ["diff", "--no-ext-diff"], text=False) or b""
    git = {"commit": _git(root, ["rev-parse", "HEAD"]), "dirty": bool(porcelain), "porcelain_sha256": hashlib.sha256(str(porcelain).encode()).hexdigest(), "dirty_diff_sha256": hashlib.sha256(bytes(dirty_diff) + str(porcelain).encode()).hexdigest(), "source_fingerprint_sha256": _source_fingerprint(root)}
    outputs["report"].write_text(_report(config, outputs, elapsed, len(raw_rows), legacy_stats, warnings))
    output_hashes = {name: {"sha256": _sha(path), "bytes": path.stat().st_size} for name, path in outputs.items() if name != "manifest"}
    command = f"PYTHONPATH=src {sys.executable} -m gifted_masking.cli article-experiment --config {config_path}"
    manifest = {"run_id": run_id, "experiment_id": "E03", "tier": "smoke", "config_path": str(config_path), "normalized_config": _canonical_json(config), "config_sha256": hashlib.sha256(_canonical_json(config).encode()).hexdigest(), "command": command, "git": git, "environment": {"python_version": sys.version, "platform": platform.platform(), "numpy": np.__version__}, "parameters": config, "legacy_provenance": legacy_stats, "seed_hierarchy": {"legacy": "seed=9100 + 100*eta_index + p_index", "new": "SHA-256 rng_family_id -> first 16 bytes as four little-endian uint32 -> SeedSequence([master_seed, 3, words...]).spawn(1) uint64", "rng_unit": "vectorized_cell_stream", "trajectory_prefix_pairing": "only approved default standard T/window OAT variants share a family; parameter_cell_id always includes T/window", "cells": seed_map}, "standard_streaming_cost_plan": standard_streaming_cost_plan(), "sort_keys": ["parameter_cell_id", "child_id"], "outputs": {name: {"path": str(path), "rows": len(raw_rows) if name == "raw" else (len(cells) if name in {"cells", "stable"} else (len(effects) if name == "effects" else (len(thresholds) if name == "thresholds" else (len(legacy_rows) if name == "legacy" else None))))} for name, path in outputs.items()}, "output_hashes": output_hashes, "timing": {"wall_seconds": elapsed}, "warnings": warnings, "verification": {"status": "pending_external_tests", "command": "./scripts/verify.sh"}, "timestamps": {"start_utc": started, "end_utc": datetime.now(timezone.utc).isoformat()}}
    write_json(outputs["manifest"], manifest)
    return outputs


def record_e03_verification(outputs: dict[str, Path], *, status: str, command: str) -> None:
    manifest = json.loads(outputs["manifest"].read_text()); manifest["verification"] = {"status": status, "command": command}; write_json(outputs["manifest"], manifest)


def normalize_e03_machine_artifacts(outputs: dict[str, Path]) -> dict[str, str]:
    result = {name: path.read_text() for name, path in outputs.items() if name not in {"report", "figure"}}
    manifest = json.loads(result["manifest"]); manifest["timing"] = "NORMALIZED"; manifest["timestamps"] = "NORMALIZED"; manifest["output_hashes"] = "NORMALIZED"; manifest["config_path"] = "CONFIG"; manifest["command"] = "NORMALIZED"; manifest["outputs"] = {name: {**value, "path": name} for name, value in manifest["outputs"].items()}; result["manifest"] = _canonical_json(manifest)
    return result
