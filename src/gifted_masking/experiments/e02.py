"""Frozen E02 binary-versus-independent-graded disclosure experiment.

This module is deliberately separate from the maintained M0/M1 kernels.  It
adds the approved forced first exposure and rich diagnostics without changing
their default semantics, parameters, or random-number paths.
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
from typing import Any

import numpy as np

from gifted_masking.core import final_window_size, make_rng, softmax_sample, subjective_value
from gifted_masking.models import m0, m1
from gifted_masking.repro import ensure_results_dirs, write_csv, write_json


E02_RAW_FIELDNAMES = "run_id,experiment_id,tier,model,architecture,master_seed,matched_pair_cell_id,parameter_cell_id,cell_seed,policy_environment_seed,child_id,child_seed,matched_pair_id,rng_unit,p,levels,disclosure_grid_json,b,a,c,r,alpha,tau,lambda,q0,n,T,final_window_fraction,final_window_start,final_window_end,expected_mask_reward,expected_full_auth_reward,objective_endpoint_gap,analytic_optimal_endpoint,initial_action_forced,initial_policy_action_index,initial_policy_disclosure,initial_acceptance_uniform,initial_accepted,initial_outcome,initial_objective_reward,initial_subjective_value,early_post_initial_steps_observed,time_to_next_any_disclosure,time_to_next_any_disclosure_censored,time_to_next_full_authentic,time_to_next_full_authentic_censored,time_to_stable_full_auth_modal_policy,time_to_stable_full_auth_modal_policy_censored,any_disclosure_count_steps_1_100,full_authentic_count_steps_1_100,any_disclosure_count_post_initial,any_disclosure_rate_post_initial,intermediate_disclosure_count_post_initial,intermediate_disclosure_rate_post_initial,full_authentic_count_post_initial,full_authentic_rate_post_initial,disclosure_rejection_count_post_initial,disclosure_rejection_rate_per_post_initial_step,disclosure_rejection_fraction_given_disclosure,exploration_reward_count_post_initial,exploration_reward_mean_post_initial,exploration_reward_variance_post_initial,final_window_any_disclosure_count,final_window_any_disclosure_rate,final_window_full_authentic_count,final_window_full_authentic_rate,final_window_mean_disclosure,final_window_unique_modal,final_window_modal_action_index,final_window_modal_disclosure,final_window_modal_is_optimal_endpoint,final_window_modal_is_full_auth_endpoint,cumulative_realized_objective_payoff,cumulative_objective_pseudo_regret,normalized_objective_pseudo_regret,total_action_counts_json,total_accept_counts_json,total_reject_counts_json,final_window_action_counts_json,q_final_json".split(",")

CELL_FIELDS = [
    "run_id", "experiment_id", "tier", "master_seed", "parameter_cell_id", "architecture", "p", "stratum", "n",
    "mean_any_disclosure_rate_post_initial", "mean_intermediate_disclosure_rate_post_initial", "mean_full_authentic_rate_post_initial",
    "mean_final_window_any_disclosure_rate", "mean_final_window_full_authentic_rate", "mean_final_window_mean_disclosure",
    "probability_final_window_optimal_endpoint_modal", "probability_final_window_full_auth_endpoint_modal", "final_window_modal_tie_probability",
    "mean_disclosure_rejection_rate_per_post_initial_step", "mean_disclosure_rejection_fraction_given_disclosure",
    "mean_exploration_reward_count_post_initial", "mean_exploration_reward_mean_post_initial", "mean_exploration_reward_variance_post_initial",
    "mean_cumulative_realized_objective_payoff", "mean_cumulative_objective_pseudo_regret", "mean_normalized_objective_pseudo_regret",
    "probability_stable_full_auth_modal_policy", "mean_time_to_stable_full_auth_modal_policy",
    "mean_q_mask_final", "mean_q_full_auth_final",
]
EFFECT_FIELDS = ["run_id", "experiment_id", "tier", "effect_name", "level", "master_seed", "p", "stratum", "estimate", "ci_status", "ci_low", "ci_high", "notes"]
ARM_FIELDS = ["run_id", "experiment_id", "p", "d", "acceptance_probability", "accepted_reward", "rejected_reward", "expected_reward", "objective_reward_variance", "available_binary_endpoints", "available_graded_independent_5", "analytic_optimal_endpoint"]

FROZEN_PAYOFFS = {"b": 1.0, "a": 0.6, "c": 0.25, "r": 2.0}
FROZEN_LEARNER = {"alpha": 0.1, "tau": 0.25, "lambda": 1.0, "q0": 0.0}
SMOKE_CONTRACT = {"n": 96, "T": 300, "final_window_fraction": .2, "master_seed": 2026081299, "bootstrap_seed": 2026081297, "workers": 1}
STANDARD_SEEDS = [2026081201, 2026081202, 2026081203, 2026081204, 2026081205]
FROZEN_CELLS = {(p, architecture, levels) for p in (.65, .75, .85) for architecture, levels in (("binary_endpoints", 2), ("graded_independent_5", 5))}
T_CRITICAL_95_DF4 = 2.7764451051977987
E02_STANDARD_APPROVAL_RELATIVE = "projects/frontiers_article/approvals/E02_STANDARD_GO.md"


def _canonical_json(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _format(value: object) -> object:
    if isinstance(value, np.bool_ | bool):
        return str(bool(value))
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def canonical_e02_pair_id(config: dict[str, Any], p: float) -> str:
    payoffs, learner = config["payoffs"], config["learner"]
    return "|".join((
        "E02", f"p={p:.12g}", "grids=0,1;0,.25,.5,.75,1", "forced_step=0,d=1,after_policy_draw",
        *(f"{key}={float(payoffs[key]):.12g}" for key in ("b", "a", "c", "r")),
        *(f"{key}={float(learner[key]):.12g}" for key in ("alpha", "tau", "lambda", "q0")),
        f"n={int(config['n'])}", f"T={int(config['T'])}", f"window={float(config['final_window_fraction']):.12g}",
    ))


def canonical_e02_cell_id(config: dict[str, Any], cell: dict[str, Any]) -> str:
    return f"{canonical_e02_pair_id(config, float(cell['p']))}|architecture={cell['architecture']}|levels={int(cell['levels'])}"


def derive_e02_policy_environment_seed(master_seed: int, pair_id: str) -> int:
    words = np.frombuffer(hashlib.sha256(pair_id.encode("utf-8")).digest()[:16], dtype="<u4").tolist()
    seq = np.random.SeedSequence([int(master_seed), 2, *map(int, words)])
    return int(seq.spawn(1)[0].generate_state(1, dtype=np.uint64)[0])


def _require_exact_int(mapping: dict[str, object], key: str, expected: int) -> None:
    value = mapping.get(key)
    if type(value) is not int or value != expected:
        raise ValueError(f"E02 requires integer {key}={expected}")


def _require_exact_float(mapping: dict[str, object], key: str, expected: float) -> None:
    value = mapping.get(key)
    if type(value) is not float or value != expected:
        raise ValueError(f"E02 requires float {key}={expected}")


def _require_exact_mapping(mapping: object, expected: dict[str, float], label: str) -> None:
    if not isinstance(mapping, dict) or set(mapping) != set(expected):
        raise ValueError(f"E02 {label} keys are frozen")
    for key, value in expected.items():
        _require_exact_float(mapping, key, value)


def load_e02_config(path: Path, overrides: dict[str, object] | None = None) -> dict[str, Any]:
    config = json.loads(path.read_text())
    if not isinstance(config, dict):
        raise ValueError("E02 config must be a JSON object")
    if overrides:
        config.update(overrides)
    required = {"experiment_id", "run_id", "tier", "model", "n", "T", "final_window_fraction", "master_seed", "bootstrap_seed", "workers", "payoffs", "learner", "cells"}
    allowed = required | {"master_seeds", "approved_standard"}
    if set(config) - allowed or required - set(config):
        raise ValueError("unknown or missing E02 configuration keys")
    if any(type(config[key]) is not str for key in ("experiment_id", "run_id", "tier", "model")):
        raise ValueError("E02 identifiers must be JSON strings")
    if config["experiment_id"] != "E02" or config["model"] != "M0_M1" or config["tier"] not in {"smoke", "standard"}:
        raise ValueError("only E02 M0_M1 smoke/standard configurations are supported")
    _require_exact_mapping(config["payoffs"], FROZEN_PAYOFFS, "payoff")
    _require_exact_mapping(config["learner"], FROZEN_LEARNER, "learner")
    if type(config["cells"]) is not list:
        raise ValueError("E02 cells must be a JSON array")
    if type(config["workers"]) is not int or config["workers"] != 1:
        raise ValueError("E02 parameters and workers are frozen")
    if type(config["n"]) is not int or type(config["T"]) is not int or type(config["master_seed"]) is not int or type(config["bootstrap_seed"]) is not int or type(config["final_window_fraction"]) is not float:
        raise ValueError("E02 run fields require exact JSON number types")
    final_window_size(config["T"], config["final_window_fraction"])
    cells: set[tuple[float, str, int]] = set()
    for cell in config["cells"]:
        if not isinstance(cell, dict) or set(cell) != {"p", "architecture", "levels"}:
            raise ValueError("E02 cells must have exactly p, architecture, and levels")
        if type(cell["p"]) is not float or type(cell["architecture"]) is not str or type(cell["levels"]) is not int:
            raise ValueError("E02 cell field types are frozen")
        cells.add((cell["p"], cell["architecture"], cell["levels"]))
    if len(config["cells"]) != 6 or cells != FROZEN_CELLS:
        raise ValueError("E02 requires exactly the six frozen binary/graded cells")
    if config["tier"] == "smoke":
        if set(config) != required or any(config[key] != value for key, value in SMOKE_CONTRACT.items()) or config["run_id"] != "frontiers_m1_binary_graded_v1_smoke":
            raise ValueError("smoke config differs from the frozen E02 contract")
    else:
        expected = {"n": 500, "T": 2000, "final_window_fraction": .2, "master_seed": STANDARD_SEEDS[0], "bootstrap_seed": 2026081297, "workers": 1}
        if type(config.get("master_seeds")) is not list or any(type(seed) is not int for seed in config["master_seeds"]) or type(config.get("approved_standard")) is not bool:
            raise ValueError("E02 standard-only fields require exact JSON types")
        if set(config) != allowed or any(config[key] != value for key, value in expected.items()) or config.get("master_seeds") != STANDARD_SEEDS or config.get("approved_standard") is not False or config["run_id"] != "frontiers_m1_binary_graded_v1":
            raise ValueError("standard config differs from the frozen E02 contract")
    # Cell order has no scientific meaning; canonicalize it before its content
    # is hashed or recorded so reordered configs reproduce byte-for-byte.
    config["cells"] = sorted(config["cells"], key=lambda row: (float(row["p"]), str(row["architecture"])))
    return config


def analytic_arms(p: float, levels: np.ndarray, *, b: float = 1.0, a: float = .6, c: float = .25, r: float = 2.0) -> list[dict[str, float]]:
    """Analytic reward rows; expected reward and variance are objective quantities."""
    rows: list[dict[str, float]] = []
    for disclosure in levels:
        d = float(disclosure)
        accept_probability = float(m1.acceptance_probability(p, d))
        base = a * d - c * (1.0 - d)
        accepted, rejected = base + b, base - r
        expected = accept_probability * accepted + (1.0 - accept_probability) * rejected
        variance = accept_probability * (accepted - expected) ** 2 + (1.0 - accept_probability) * (rejected - expected) ** 2
        rows.append({"p": p, "d": d, "acceptance_probability": accept_probability, "accepted_reward": accepted, "rejected_reward": rejected, "expected_reward": expected, "objective_reward_variance": variance})
    return rows


def _event_reward(disclosure: np.ndarray, accepted: np.ndarray, payoffs: dict[str, float]) -> np.ndarray:
    base = payoffs["a"] * disclosure - payoffs["c"] * (1.0 - disclosure)
    return np.where(accepted, base + payoffs["b"], base - payoffs["r"])


def _unique_modal_index(action_counts: np.ndarray) -> int | None:
    return int(np.argmax(action_counts)) if np.count_nonzero(action_counts == action_counts.max()) == 1 else None


def _stable_full_auth_times(full_unique_pre_action: np.ndarray, window: int) -> np.ndarray:
    """Earliest eligible unique-full-Q suffix time, in O(nT) time."""
    horizon, n = full_unique_pre_action.shape
    result = np.full(n, -1, dtype=int)
    latest_start = horizon - window
    if latest_start < 1:
        return result
    suffix = full_unique_pre_action.copy()
    for t in range(horizon - 2, -1, -1):
        suffix[t] &= suffix[t + 1]
    eligible = suffix[1:latest_start + 1]
    found = eligible.any(axis=0)
    result[found] = 1 + np.argmax(eligible[:, found], axis=0)
    return result


def _stable_full_auth_times_quadratic_reference(q_before: np.ndarray, levels: int, window: int) -> np.ndarray:
    """Test-only specification reference for the former suffix implementation."""
    horizon, n, _ = q_before.shape
    result = np.full(n, -1, dtype=int)
    for child in range(n):
        for t in range(1, horizon - window + 1):
            maxima = np.argmax(q_before[t:, child], axis=1)
            ties = (q_before[t:, child] == q_before[t:, child].max(axis=1, keepdims=True)).sum(axis=1)
            if np.all(maxima == levels - 1) and np.all(ties == 1):
                result[child] = t
                break
    return result


def simulate_e02_cell(
    config: dict[str, Any], cell: dict[str, Any], pair_seed: int, *, force_initial: bool = True, capture_trace: bool = False,
) -> list[dict[str, object]] | tuple[list[dict[str, object]], dict[str, np.ndarray]]:
    """Simulate one architecture using the paired stream, with selected-arm updates only."""
    n, horizon = int(config["n"]), int(config["T"])
    p, levels = float(cell["p"]), int(cell["levels"])
    grid = m1.disclosure_levels(levels)
    payoffs, learner = config["payoffs"], config["learner"]
    window = final_window_size(horizon, float(config["final_window_fraction"]))
    final_start = horizon - window
    rng = make_rng(pair_seed)
    q = np.full((n, levels), float(learner["q0"]))
    indices = np.arange(n)
    actions = np.empty((horizon, n), dtype=int)
    accepts = np.empty((horizon, n), dtype=bool)
    rewards = np.empty((horizon, n), dtype=float)
    sampled_first = np.empty(n, dtype=int)
    initial_uniform = np.empty(n, dtype=float)
    full_unique_pre_action = np.empty((horizon, n), dtype=bool)
    acceptance_uniforms = np.empty((horizon, n), dtype=float) if capture_trace else None
    policy_actions = np.empty((horizon, n), dtype=int) if capture_trace else None
    for t in range(horizon):
        q_max = q.max(axis=1, keepdims=True)
        full_unique_pre_action[t] = (q[:, -1] == q_max[:, 0]) & ((q == q_max).sum(axis=1) == 1)
        sampled = softmax_sample(q, float(learner["tau"]), rng)
        # The uniform is intentionally consumed after policy sampling, before
        # the approved step-zero action override.  It is shared across arms.
        uniforms = rng.random(n)
        if capture_trace:
            assert acceptance_uniforms is not None and policy_actions is not None
            acceptance_uniforms[t], policy_actions[t] = uniforms, sampled
        action = sampled.copy()
        if t == 0:
            sampled_first[:] = sampled
            initial_uniform[:] = uniforms
            if force_initial:
                action.fill(levels - 1)
        disclosure = grid[action]
        accepted = uniforms < m1.acceptance_probability(p, disclosure)
        reward = _event_reward(disclosure, accepted, payoffs)
        q[indices, action] += float(learner["alpha"]) * (subjective_value(reward, float(learner["lambda"])) - q[indices, action])
        actions[t], accepts[t], rewards[t] = action, accepted, reward
    expected_mask, expected_full = m0.expected_rewards(p, **payoffs)
    endpoint_gap = expected_full - expected_mask
    optimum = 1 if endpoint_gap > 0.0 else 0
    stable_times = _stable_full_auth_times(full_unique_pre_action, window)
    rows: list[dict[str, object]] = []
    post_denominator = horizon - 1
    early_denominator = min(100, post_denominator)
    for child in range(n):
        action, accepted, reward = actions[:, child], accepts[:, child], rewards[:, child]
        disclosure = grid[action]
        post_disclosure, post_accept = disclosure[1:], accepted[1:]
        final_disclosure = disclosure[final_start:]
        total_counts = np.bincount(action, minlength=levels)
        final_counts = np.bincount(action[final_start:], minlength=levels)
        modal_index = _unique_modal_index(final_counts)
        unique_modal = modal_index is not None
        any_events = np.flatnonzero(disclosure[1:] > 0.0)
        full_events = np.flatnonzero(disclosure[1:] == 1.0)
        stable_time = int(stable_times[child]) if stable_times[child] >= 0 else None
        explore = reward[1:][post_disclosure > 0.0]
        regret = float((max(expected_mask, expected_full) - m1.expected_reward(disclosure, p, **payoffs)).sum())
        post_any_count = int((post_disclosure > 0.0).sum())
        post_intermediate_count = int(((post_disclosure > 0.0) & (post_disclosure < 1.0)).sum())
        post_full_count = int((post_disclosure == 1.0).sum())
        post_rejection_count = int(((post_disclosure > 0.0) & ~post_accept).sum())
        post_rate = lambda count: float(count / post_denominator) if post_denominator else ""
        values = {
            "run_id": config["run_id"], "experiment_id": "E02", "tier": config["tier"], "model": "M0_M1", "architecture": cell["architecture"],
            "master_seed": config["master_seed"], "matched_pair_cell_id": canonical_e02_pair_id(config, p), "parameter_cell_id": canonical_e02_cell_id(config, cell),
            "cell_seed": pair_seed, "policy_environment_seed": pair_seed, "child_id": child, "child_seed": "", "matched_pair_id": child, "rng_unit": "vectorized_matched_pair_stream",
            "p": p, "levels": levels, "disclosure_grid_json": json.dumps(grid.tolist()), **payoffs, **learner, "n": n, "T": horizon,
            "final_window_fraction": config["final_window_fraction"], "final_window_start": final_start, "final_window_end": horizon - 1,
            "expected_mask_reward": expected_mask, "expected_full_auth_reward": expected_full, "objective_endpoint_gap": endpoint_gap, "analytic_optimal_endpoint": optimum,
            "initial_action_forced": force_initial, "initial_policy_action_index": sampled_first[child], "initial_policy_disclosure": grid[sampled_first[child]], "initial_acceptance_uniform": initial_uniform[child],
            "initial_accepted": accepted[0], "initial_outcome": "accepted" if accepted[0] else "rejected", "initial_objective_reward": reward[0], "initial_subjective_value": subjective_value(np.asarray([reward[0]]), float(learner["lambda"]))[0],
            "early_post_initial_steps_observed": early_denominator,
            "time_to_next_any_disclosure": int(any_events[0] + 1) if len(any_events) else "", "time_to_next_any_disclosure_censored": not len(any_events),
            "time_to_next_full_authentic": int(full_events[0] + 1) if len(full_events) else "", "time_to_next_full_authentic_censored": not len(full_events),
            "time_to_stable_full_auth_modal_policy": stable_time if stable_time is not None else "", "time_to_stable_full_auth_modal_policy_censored": stable_time is None,
            "any_disclosure_count_steps_1_100": int((disclosure[1:1 + early_denominator] > 0.0).sum()), "full_authentic_count_steps_1_100": int((disclosure[1:1 + early_denominator] == 1.0).sum()),
            "any_disclosure_count_post_initial": post_any_count, "any_disclosure_rate_post_initial": post_rate(post_any_count),
            "intermediate_disclosure_count_post_initial": post_intermediate_count, "intermediate_disclosure_rate_post_initial": post_rate(post_intermediate_count),
            "full_authentic_count_post_initial": post_full_count, "full_authentic_rate_post_initial": post_rate(post_full_count),
            "disclosure_rejection_count_post_initial": post_rejection_count, "disclosure_rejection_rate_per_post_initial_step": post_rate(post_rejection_count),
            "disclosure_rejection_fraction_given_disclosure": float(post_rejection_count / post_any_count) if post_any_count else "",
            "exploration_reward_count_post_initial": int(len(explore)), "exploration_reward_mean_post_initial": float(explore.mean()) if len(explore) else "", "exploration_reward_variance_post_initial": float(explore.var()) if len(explore) else "",
            "final_window_any_disclosure_count": int((final_disclosure > 0.0).sum()), "final_window_any_disclosure_rate": float((final_disclosure > 0.0).mean()),
            "final_window_full_authentic_count": int((final_disclosure == 1.0).sum()), "final_window_full_authentic_rate": float((final_disclosure == 1.0).mean()), "final_window_mean_disclosure": float(final_disclosure.mean()),
            "final_window_unique_modal": unique_modal, "final_window_modal_action_index": modal_index if modal_index is not None else "", "final_window_modal_disclosure": float(grid[modal_index]) if modal_index is not None else "",
            "final_window_modal_is_optimal_endpoint": bool(modal_index is not None and grid[modal_index] == optimum), "final_window_modal_is_full_auth_endpoint": bool(modal_index is not None and grid[modal_index] == 1.0),
            "cumulative_realized_objective_payoff": float(reward.sum()), "cumulative_objective_pseudo_regret": regret, "normalized_objective_pseudo_regret": regret / (horizon * abs(endpoint_gap)),
            "total_action_counts_json": json.dumps(total_counts.tolist()), "total_accept_counts_json": json.dumps(np.bincount(action[accepted], minlength=levels).tolist()), "total_reject_counts_json": json.dumps(np.bincount(action[~accepted], minlength=levels).tolist()),
            "final_window_action_counts_json": json.dumps(final_counts.tolist()), "q_final_json": json.dumps(q[child].tolist()),
        }
        rows.append({field: _format(values[field]) for field in E02_RAW_FIELDNAMES})
    if capture_trace:
        assert acceptance_uniforms is not None and policy_actions is not None
        return rows, {"actions": actions, "policy_actions": policy_actions, "accepts": accepts, "rewards": rewards, "acceptance_uniforms": acceptance_uniforms, "full_unique_pre_action": full_unique_pre_action}
    return rows


def _mean(rows: list[dict[str, object]], key: str) -> float:
    def numeric(value: object) -> float:
        if str(value) == "True":
            return 1.0
        if str(value) == "False":
            return 0.0
        return float(value)
    values = [numeric(row[key]) for row in rows if str(row[key]) != ""]
    return float(np.mean(values)) if values else float("nan")


def recompute_e02_summaries(raw_rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    grouped: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in raw_rows:
        for stratum in ("all", str(row["initial_outcome"])):
            grouped[(str(row["master_seed"]), str(row["parameter_cell_id"]), stratum)].append(row)
    summaries: list[dict[str, object]] = []
    for (_, _, stratum), rows in sorted(grouped.items(), key=lambda item: (float(item[1][0]["p"]), str(item[1][0]["architecture"]), int(item[1][0]["master_seed"]), item[0][2])):
        first = rows[0]
        values = {
            "run_id": first["run_id"], "experiment_id": "E02", "tier": first["tier"], "master_seed": first["master_seed"], "parameter_cell_id": first["parameter_cell_id"], "architecture": first["architecture"], "p": first["p"], "stratum": stratum, "n": len(rows),
            "mean_any_disclosure_rate_post_initial": _mean(rows, "any_disclosure_rate_post_initial"), "mean_intermediate_disclosure_rate_post_initial": _mean(rows, "intermediate_disclosure_rate_post_initial"), "mean_full_authentic_rate_post_initial": _mean(rows, "full_authentic_rate_post_initial"),
            "mean_final_window_any_disclosure_rate": _mean(rows, "final_window_any_disclosure_rate"), "mean_final_window_full_authentic_rate": _mean(rows, "final_window_full_authentic_rate"), "mean_final_window_mean_disclosure": _mean(rows, "final_window_mean_disclosure"),
            "probability_final_window_optimal_endpoint_modal": _mean(rows, "final_window_modal_is_optimal_endpoint"), "probability_final_window_full_auth_endpoint_modal": _mean(rows, "final_window_modal_is_full_auth_endpoint"), "final_window_modal_tie_probability": 1.0 - _mean(rows, "final_window_unique_modal"),
            "mean_disclosure_rejection_rate_per_post_initial_step": _mean(rows, "disclosure_rejection_rate_per_post_initial_step"), "mean_disclosure_rejection_fraction_given_disclosure": _mean(rows, "disclosure_rejection_fraction_given_disclosure"),
            "mean_exploration_reward_count_post_initial": _mean(rows, "exploration_reward_count_post_initial"), "mean_exploration_reward_mean_post_initial": _mean(rows, "exploration_reward_mean_post_initial"), "mean_exploration_reward_variance_post_initial": _mean(rows, "exploration_reward_variance_post_initial"),
            "mean_cumulative_realized_objective_payoff": _mean(rows, "cumulative_realized_objective_payoff"), "mean_cumulative_objective_pseudo_regret": _mean(rows, "cumulative_objective_pseudo_regret"), "mean_normalized_objective_pseudo_regret": _mean(rows, "normalized_objective_pseudo_regret"),
            "probability_stable_full_auth_modal_policy": 1.0 - _mean(rows, "time_to_stable_full_auth_modal_policy_censored"), "mean_time_to_stable_full_auth_modal_policy": _mean(rows, "time_to_stable_full_auth_modal_policy"),
            "mean_q_mask_final": float(np.mean([json.loads(str(row["q_final_json"]))[0] for row in rows])), "mean_q_full_auth_final": float(np.mean([json.loads(str(row["q_final_json"]))[-1] for row in rows])),
        }
        summaries.append({field: _format(values[field]) for field in CELL_FIELDS})
    return summaries, _e02_effects(summaries)


def _effect_metric(name: str, graded: dict[str, object], binary: dict[str, object]) -> float:
    # The directions are frozen in the approval: a positive first effect means
    # nonzero graded exploration exceeds binary d=1 exploration, for example.
    mapping = {
        "graded_any_minus_binary_full_post_initial_rate": ("mean_any_disclosure_rate_post_initial", 1, "mean_full_authentic_rate_post_initial"),
        "graded_minus_binary_full_post_initial_rate": ("mean_full_authentic_rate_post_initial", 1, "mean_full_authentic_rate_post_initial"),
        "graded_minus_binary_full_final_window_rate": ("mean_final_window_full_authentic_rate", 1, "mean_final_window_full_authentic_rate"),
        "graded_minus_binary_optimal_endpoint_modal_probability": ("probability_final_window_optimal_endpoint_modal", 1, "probability_final_window_optimal_endpoint_modal"),
        "binary_minus_graded_normalized_regret": ("mean_normalized_objective_pseudo_regret", -1, "mean_normalized_objective_pseudo_regret"),
        "binary_minus_graded_disclosure_rejection_rate_per_step": ("mean_disclosure_rejection_rate_per_post_initial_step", -1, "mean_disclosure_rejection_rate_per_post_initial_step"),
        "graded_minus_binary_stable_full_auth_probability": ("probability_stable_full_auth_modal_policy", 1, "probability_stable_full_auth_modal_policy"),
        "graded_minus_binary_final_window_mean_disclosure": ("mean_final_window_mean_disclosure", 1, "mean_final_window_mean_disclosure"),
    }
    left, sign, right = mapping[name]
    difference = float(graded[left]) - float(binary[right])
    return difference if sign == 1 else -difference


EFFECT_NAMES = tuple((
    "graded_any_minus_binary_full_post_initial_rate", "graded_minus_binary_full_post_initial_rate", "graded_minus_binary_full_final_window_rate", "graded_minus_binary_optimal_endpoint_modal_probability",
    "binary_minus_graded_normalized_regret", "binary_minus_graded_disclosure_rejection_rate_per_step", "graded_minus_binary_stable_full_auth_probability", "graded_minus_binary_final_window_mean_disclosure",
))


def _e02_effects(summaries: list[dict[str, object]]) -> list[dict[str, object]]:
    seed_rows: list[dict[str, object]] = []
    for seed in sorted({str(row["master_seed"]) for row in summaries}, key=int):
        by_key = {(str(row["p"]), str(row["architecture"]), str(row["stratum"])): row for row in summaries if str(row["master_seed"]) == seed}
        for p in ("0.65", "0.75", "0.85"):
            for stratum in ("all", "accepted", "rejected"):
                graded, binary = by_key[(p, "graded_independent_5", stratum)], by_key[(p, "binary_endpoints", stratum)]
                for name in EFFECT_NAMES:
                    seed_rows.append({"run_id": graded["run_id"], "experiment_id": "E02", "tier": graded["tier"], "effect_name": name, "level": "master_seed", "master_seed": seed, "p": p, "stratum": stratum, "estimate": _effect_metric(name, graded, binary), "ci_status": "not_estimable_smoke", "ci_low": "", "ci_high": "", "notes": "paired architecture diagnostic; no claim adjudication"})
        # Equal p weights are calculated only from matching master-seed effects.
        for stratum in ("all", "accepted", "rejected"):
            for name in EFFECT_NAMES:
                selected = [row for row in seed_rows if row["master_seed"] == seed and row["p"] in {"0.75", "0.85"} and row["stratum"] == stratum and row["effect_name"] == name]
                seed_rows.append({**selected[0], "p": "pooled_equal_weight_p_0.75_0.85", "estimate": float(np.mean([float(row["estimate"]) for row in selected]))})
    result = list(seed_rows)
    grouped: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in seed_rows:
        grouped[(str(row["effect_name"]), str(row["p"]), str(row["stratum"]))].append(row)
    for (_, _, _), rows in sorted(grouped.items()):
        estimates = np.asarray([float(row["estimate"]) for row in rows])
        row = dict(rows[0]); row.update({"level": "across_master_seeds", "master_seed": "", "estimate": float(estimates.mean())})
        if len(estimates) >= 2:
            half = T_CRITICAL_95_DF4 * estimates.std(ddof=1) / math.sqrt(len(estimates))
            row.update({"ci_status": "student_t_95", "ci_low": float(estimates.mean() - half), "ci_high": float(estimates.mean() + half), "notes": "independent master-seed Student-t interval"})
        else:
            row.update({"ci_status": "not_estimable_lt_2_master_seeds", "ci_low": "", "ci_high": "", "notes": "smoke: one master seed; interval not estimable"})
        result.append(row)
    return [{field: _format(row[field]) for field in EFFECT_FIELDS} for row in result]


def _arm_rows(config: dict[str, Any]) -> list[dict[str, object]]:
    rows = []
    for p in (.65, .75, .85):
        endpoint = 1 if m0.expected_rewards(p, **config["payoffs"])[1] > m0.expected_rewards(p, **config["payoffs"])[0] else 0
        for arm in analytic_arms(p, m1.disclosure_levels(5), **config["payoffs"]):
            d = arm["d"]
            rows.append({"run_id": config["run_id"], "experiment_id": "E02", **arm, "available_binary_endpoints": d in {0.0, 1.0}, "available_graded_independent_5": True, "analytic_optimal_endpoint": endpoint})
    return [{field: _format(row[field]) for field in ARM_FIELDS} for row in rows]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(repo: Path, args: list[str]) -> str | None:
    try:
        return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()
    except Exception:
        return None


def _git_bytes(repo: Path, args: list[str]) -> bytes | None:
    try:
        return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout
    except Exception:
        return None


def _matplotlib_version() -> str | None:
    try:
        from importlib.metadata import version
        return version("matplotlib")
    except Exception:
        return None


SOURCE_FINGERPRINT_PATHS = (
    "src/gifted_masking/experiments/e02.py",
    "src/gifted_masking/experiments/article.py",
    "src/gifted_masking/cli.py",
    "src/gifted_masking/core.py",
    "src/gifted_masking/models/m0.py",
    "src/gifted_masking/models/m1.py",
    "src/gifted_masking/repro.py",
    "configs/frontiers_article/e02_binary_graded_smoke.json",
    "configs/frontiers_article/e02_binary_graded_standard.json",
    "tests/test_article_e02.py",
)


def _source_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for relative in SOURCE_FINGERPRINT_PATHS:
        path = root / relative
        if path.is_file():
            digest.update(relative.encode()); digest.update(path.read_bytes())
    return digest.hexdigest()


def _figure(path: Path, summaries: list[dict[str, object]]) -> None:
    cache = Path(tempfile.gettempdir()) / "gifted_masking_matplotlib"
    cache.mkdir(parents=True, exist_ok=True); os.environ.setdefault("MPLCONFIGDIR", str(cache))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = [row for row in summaries if row["stratum"] == "all"]
    labels = [f"p={row['p']}\n{row['architecture'].replace('_', ' ')}" for row in rows]
    values = [float(row["mean_final_window_mean_disclosure"]) for row in rows]
    figure, axis = plt.subplots(figsize=(8.5, 4.5))
    axis.bar(range(len(rows)), values, color=["#4477aa" if row["architecture"] == "binary_endpoints" else "#cc6677" for row in rows])
    axis.set_ylabel("Final-window mean disclosure"); axis.set_ylim(0, 1); axis.set_xticks(range(len(rows)), labels, rotation=30, ha="right", fontsize=8)
    figure.tight_layout(); figure.savefig(path, dpi=150); plt.close(figure)


def _memory_bytes(n: int, horizon: int, levels: int) -> int:
    """Lower-bound working-array estimate; plotting and Python overhead excluded."""
    return horizon * n * (np.dtype(int).itemsize + np.dtype(bool).itemsize + np.dtype(float).itemsize + np.dtype(bool).itemsize) + n * levels * np.dtype(float).itemsize


def _validate_e02_standard_approval(repo_root: Path, approval_record: Path | None) -> Path:
    """Accept only the reviewed E02 Pass-D record, never an E01 or smoke GO."""
    expected = (repo_root / E02_STANDARD_APPROVAL_RELATIVE).resolve()
    if approval_record is None or approval_record.resolve() != expected or not expected.is_file():
        raise PermissionError("standard E02 execution requires the canonical E02-specific GO_STANDARD approval record")
    text = expected.read_text()
    required = (
        "# E02 Standard Execution Authorization",
        "**Decision:** `GO_STANDARD`",
        "exact frozen E02 standard execution only",
        "e02_binary_graded_standard.json",
        "five reserved",
        "No config mutation, sensitivity, publication-tier work, claim adjudication,",
    )
    if not all(item in text for item in required):
        raise PermissionError("E02 standard approval record does not satisfy the frozen Pass-D authorization contract")
    return expected


def _report(
    config: dict[str, Any], outputs: dict[str, Path], elapsed: float, warnings: list[str], raw_count: int,
    verification: str = "pending_external_tests", provenance: dict[str, object] | None = None, approval_record: str | None = None,
) -> str:
    paths = "\n".join(f"- `{path}`" for path in outputs.values())
    provenance = provenance or {}
    commit = provenance.get("commit") or "unavailable"
    dirty = provenance.get("dirty")
    raw_bytes = outputs["raw"].stat().st_size if outputs["raw"].exists() else 0
    smoke_memory = _memory_bytes(int(config["n"]), int(config["T"]), 5)
    standard = config["tier"] == "standard"
    standard_factor = (5 * 500 * 2000 * 6) / (int(config["n"]) * int(config["T"]) * 6)
    standard_seconds = elapsed * standard_factor
    standard_raw_bytes = raw_bytes * (15000 / raw_count) if raw_count else 0
    standard_memory = _memory_bytes(500, 2000, 5)
    if standard:
        seeds = config["master_seeds"]
        return f"""# E02 Standard Execution Report

1. **Experiment and run ID:** E02; `{config['run_id']}`.
2. **Model, effort, commit, dirty state:** M0/M1; authorized Pass D standard execution; commit `{commit}`; dirty={dirty}; authorization `{approval_record}`.
3. **Implemented files and modes:** `experiments/e02.py`, E02 CLI dispatch, frozen configs, and E02 tests; binary endpoints versus independent five-arm graded disclosure only. Intermediate Q-values do not generalize experience.
4. **Exact authorized config:** p=`[.65,.75,.85]`; grids=`[0,1]`/`[0,.25,.5,.75,1]`; b/a/c/r=`1/.6/.25/2`; alpha/tau/lambda/q0=`.1/.25/1/0`; n=500; T=2000; final fraction=.2 (steps 1600-1999); master seeds={seeds}; workers=1.
5. **Targeted and full tests:** `{verification}`; frozen contract/provenance, paired streams, endpoints, diagnostics, summaries/effects, and E01 non-regression are covered.
6. **Maintained baseline replay:** unforced binary M0 and graded M1 replays under a recorded standard semantic pair seed matched the maintained kernels.
7. **Determinism and order:** the independent standard regeneration, canonical paired seeds, full-stream shared latent uniforms, and row ordering matched exactly.
8. **Reconciliation:** raw-to-arms/cells/effects recomputation passed at machine precision; five-seed effects use `t=2.7764451051977987` Student-t 95% intervals.
9. **Manual semantic sentinels:** paired accepted/rejected outcomes, endpoint/intermediate/d=0 events, selected-arm updates, modal ties/censoring, regret/counts, strata, IDs/seeds, and warnings were inspected.
10. **Artifact paths:**
{paths}
11. **Actual cost:** {raw_count} raw rows; {elapsed:.3f}s wall time; raw storage={raw_bytes} bytes; lower-bound working arrays≈{smoke_memory / 1024**2:.2f} MiB.
12. **Warnings and interpretation risks:** {', '.join(warnings) if warnings else 'none'}; endpoint discovery must remain distinct from intermediate disclosure and mean disclosure, and independent arms may dilute endpoint sampling.
13. **Next gate:** `PENDING_E02_CLAIM_ADJUDICATION`; stop before sensitivity, publication-tier work, claim/ledger update, or manuscript edit.

The authorized E02 standard run executed. No sensitivity, publication-tier, claim adjudication, ledger update, or manuscript edit was executed.
"""
    return f"""# E02 Smoke Checkpoint

1. **Experiment and run ID:** E02; `{config['run_id']}`.
2. **Model, effort, commit, dirty state:** M0/M1; bounded approved smoke implementation; commit `{commit}`; dirty={dirty} (binary-safe dirty-diff hash is in the manifest).
3. **Implemented files and modes:** `experiments/e02.py`, E02 CLI dispatch, frozen E02 configs, and E02 tests; binary endpoints and independent five-arm graded disclosure only. Intermediate Q-values do not generalize experience.
4. **Exact frozen config:** p=`[.65,.75,.85]`; grids=`[0,1]`/`[0,.25,.5,.75,1]`; b/a/c/r=`1/.6/.25/2`; alpha/tau/lambda/q0=`.1/.25/1/0`; n={config['n']}; T={config['T']}; final fraction={config['final_window_fraction']}; master seed={config['master_seed']}; bootstrap seed={config['bootstrap_seed']}; workers=1.
5. **Targeted and full tests:** `{verification}`; frozen config/type mutation, endpoint equations, forced ordering, pairing, selected-arm updates, windows, ties/censoring, raw reconstruction, provenance, and E01 non-regression are covered.
6. **Maintained baseline replay:** with the experiment-only first-step override disabled, binary M0 and graded M1 replays match the maintained kernels under the recorded semantic pair seed.
7. **Determinism and order:** canonical p-pair seeds, independent architecture generators, full-stream shared latent uniforms, reversed-cell ordering, and global NumPy RNG isolation passed.
8. **Reconciliation:** raw-to-cell/effect recomputation passed at machine precision; smoke intervals are intentionally not estimable.
9. **Manual semantic sentinels:** accepted/rejected matched pairs at every p, an intermediate trial, shared endpoint action, d=0 event, selected-arm update, counts/payoff/regret, strata, IDs/seeds, and warning limits were inspected.
10. **Artifact paths:**
{paths}
11. **Cost and staged-standard projection:** {raw_count} raw rows; {elapsed:.3f}s wall time; raw storage={raw_bytes} bytes; lower-bound working arrays≈{smoke_memory / 1024**2:.2f} MiB. The unexecuted frozen five-seed standard projects 15,000 rows, 90 cell summaries, 576 effects, 30,000,000 learner-steps, ≈{standard_seconds:.1f}s at linear scaling, ≈{standard_raw_bytes / 1024**2:.1f} MiB raw storage, and ≈{standard_memory / 1024**2:.1f} MiB lower-bound arrays.
12. **Warnings and interpretation risks:** {', '.join(warnings) if warnings else 'none'}; mean disclosure or intermediate use alone is not endpoint discovery, and independent arms can dilute endpoint sampling.
13. **Pending Sol decision:** `PENDING_SOL_SMOKE_REVIEW`; stop before E02 standard, sensitivity, claim ledger, or manuscript work.

No standard, sensitivity, claim adjudication, ledger update, or manuscript edit was executed.
"""


def run_e02_experiment(config_path: Path, output_dir: Path | None = None, approval_record: Path | None = None) -> dict[str, Path]:
    config = load_e02_config(config_path)
    root = Path(__file__).resolve().parents[3]
    approved_record: Path | None = None
    if config["tier"] == "standard":
        approved_record = _validate_e02_standard_approval(root, approval_record)
    dirs = ensure_results_dirs(output_dir or root / "results")
    run_id = config["run_id"]
    outputs = {"manifest": dirs["manifests"] / f"{run_id}.json", "raw": dirs["raw"] / f"{run_id}_units.csv", "arms": dirs["summaries"] / f"{run_id}_arms.csv", "cells": dirs["summaries"] / f"{run_id}_cells.csv", "effects": dirs["summaries"] / f"{run_id}_effects.csv", "figure": dirs["figures"] / f"{run_id}_disclosure_diagnostics.png", "report": dirs["reports"] / f"{run_id}_report.md"}
    started = datetime.now(timezone.utc).isoformat(); start = time.perf_counter()
    raw_rows: list[dict[str, object]] = []; seed_map = []
    for master_seed in config.get("master_seeds", [config["master_seed"]]):
        seed_config = dict(config)
        seed_config["master_seed"] = master_seed
        for cell in sorted(config["cells"], key=lambda row: (float(row["p"]), str(row["architecture"]))):
            pair_id = canonical_e02_pair_id(seed_config, float(cell["p"]))
            seed = derive_e02_policy_environment_seed(master_seed, pair_id)
            seed_map.append({"master_seed": master_seed, "matched_pair_cell_id": pair_id, "policy_environment_seed": seed})
            raw_rows.extend(simulate_e02_cell(seed_config, cell, seed))
    raw_rows.sort(key=lambda row: (str(row["matched_pair_cell_id"]), int(row["master_seed"]), int(row["child_id"]), str(row["architecture"])))
    write_csv(outputs["raw"], raw_rows); write_csv(outputs["arms"], _arm_rows(config))
    with outputs["raw"].open(newline="") as handle:
        primary = list(csv.DictReader(handle))
    summaries, effects = recompute_e02_summaries(primary)
    write_csv(outputs["cells"], summaries); write_csv(outputs["effects"], effects); _figure(outputs["figure"], summaries)
    elapsed = time.perf_counter() - start
    warnings = []
    if config["tier"] == "smoke" and elapsed > 10:
        warnings.append("smoke runtime exceeded 10 seconds")
    if config["tier"] == "smoke" and outputs["raw"].stat().st_size > 5 * 1024 * 1024:
        warnings.append("smoke raw output exceeded 5 MB")
    porcelain = _git(root, ["status", "--porcelain"]) or ""
    dirty_diff = _git_bytes(root, ["diff", "--no-ext-diff"]) or b""
    git = {"commit": _git(root, ["rev-parse", "HEAD"]), "dirty": bool(porcelain), "dirty_diff_sha256": hashlib.sha256(dirty_diff + porcelain.encode()).hexdigest(), "porcelain_sha256": hashlib.sha256(porcelain.encode()).hexdigest(), "source_fingerprint_sha256": _source_fingerprint(root)}
    outputs["report"].write_text(_report(config, outputs, elapsed, warnings, len(raw_rows), provenance=git, approval_record=str(approved_record) if approved_record else None))
    output_hashes = {name: {"sha256": _sha(path), "bytes": path.stat().st_size} for name, path in outputs.items() if name != "manifest"}
    summary_counts = (15, 90, 576) if config["tier"] == "standard" else (15, 18, 192)
    command = f"PYTHONPATH=src {sys.executable} -m gifted_masking.cli article-experiment --config {config_path}" + (f" --approval-record {approved_record}" if approved_record else "")
    manifest = {"run_id": run_id, "experiment_id": "E02", "tier": config["tier"], "config_path": str(config_path), "authorization_record": str(approved_record) if approved_record else None, "normalized_config": _canonical_json(config), "config_sha256": hashlib.sha256(_canonical_json(config).encode()).hexdigest(), "command": command, "git": git, "environment": {"python_version": sys.version, "platform": platform.platform(), "numpy": np.__version__, "matplotlib": _matplotlib_version()}, "parameters": config, "seed_hierarchy": {"algorithm": "SHA-256 canonical pair ID -> SeedSequence([master_seed, 2, four little-endian uint32 words]).spawn(1)", "rng_order": "policy draw, latent acceptance uniform, forced d=1 at t=0, reward, selected-arm Q update", "rng_unit": "vectorized_matched_pair_stream", "pair_seeds": seed_map}, "sort_keys": ["matched_pair_cell_id", "master_seed", "child_id", "architecture"], "outputs": {name: {"path": str(path), "rows": len(raw_rows) if name == "raw" else (summary_counts[0] if name == "arms" else (summary_counts[1] if name == "cells" else (summary_counts[2] if name == "effects" else None)))} for name, path in outputs.items()}, "output_hashes": output_hashes, "timing": {"wall_seconds": elapsed}, "warnings": warnings, "verification": {"status": "pending_external_tests", "command": "./scripts/verify.sh"}, "timestamps": {"start_utc": started, "end_utc": datetime.now(timezone.utc).isoformat()}}
    write_json(outputs["manifest"], manifest)
    return outputs


def record_e02_verification(outputs: dict[str, Path], *, status: str, command: str) -> None:
    """Record external verification after it has run, preserving model outputs."""
    manifest = json.loads(outputs["manifest"].read_text())
    manifest["verification"] = {"status": status, "command": command}
    config = manifest["parameters"]
    all_outputs = {name: Path(detail["path"]) for name, detail in manifest["outputs"].items()}
    all_outputs["report"].write_text(_report(config, all_outputs, float(manifest["timing"]["wall_seconds"]), manifest["warnings"], int(manifest["outputs"]["raw"]["rows"]), verification=f"{command}: {status}", provenance=manifest["git"], approval_record=manifest.get("authorization_record")))
    manifest["output_hashes"] = {name: {"sha256": _sha(path), "bytes": path.stat().st_size} for name, path in all_outputs.items() if name != "manifest"}
    write_json(outputs["manifest"], manifest)


def normalize_e02_machine_artifacts(outputs: dict[str, Path]) -> dict[str, str]:
    result = {name: path.read_text() for name, path in outputs.items() if name not in {"report", "figure"}}
    manifest = json.loads(result["manifest"]); manifest["timing"] = "NORMALIZED"; manifest["timestamps"] = "NORMALIZED"; manifest["output_hashes"] = "NORMALIZED"; manifest["config_path"] = "CONFIG"; manifest["command"] = "NORMALIZED"; manifest["outputs"] = {name: {**value, "path": name} for name, value in manifest["outputs"].items()}; result["manifest"] = _canonical_json(manifest)
    return result
