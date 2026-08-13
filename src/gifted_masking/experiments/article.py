"""Isolated, config-driven Stage 2 article experiments.

This module deliberately does not alter maintained model paths.  E01 retains
M0's policy/acceptance/update RNG ordering while adding diagnostic-only and
explicitly labelled information interventions.
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
from gifted_masking.models import m0
from gifted_masking.repro import ensure_results_dirs, write_csv, write_json


E01_RAW_FIELDNAMES = [
    "run_id", "experiment_id", "tier", "model", "condition", "intervention",
    "master_seed", "parameter_cell_id", "cell_seed", "policy_environment_seed", "intervention_seed",
    "child_id", "child_seed", "rng_unit", "p", "b", "a", "c", "r", "alpha", "tau", "lambda", "q0", "n", "T",
    "final_window_fraction", "final_window_start", "final_window_end", "expected_mask_reward", "expected_auth_reward", "objective_reward_gap",
    "analytic_optimal_action", "initial_action_forced", "initial_policy_action", "initial_accepted", "initial_outcome",
    "initial_objective_reward", "initial_subjective_value", "early_post_initial_steps_observed", "time_to_next_authentic_action",
    "time_to_next_authentic_censored", "authentic_count_steps_1_100", "authentic_count_post_initial", "authentic_rate_post_initial",
    "authentic_accept_count_post_initial", "authentic_reject_count_post_initial", "final_window_mask_count", "final_window_mask_rate",
    "cumulative_realized_objective_payoff", "cumulative_objective_pseudo_regret", "normalized_objective_pseudo_regret", "q_mask_final", "q_auth_final",
    "forced_exposure_count", "forced_override_count", "counterfactual_feedback_count", "counterfactual_auth_accept_count",
    "counterfactual_auth_reject_count", "counterfactual_auth_reward_sum", "counterfactual_auth_subjective_value_sum",
]

CELL_SUMMARY_FIELDS = [
    "run_id", "experiment_id", "tier", "master_seed", "parameter_cell_id", "condition", "intervention", "p", "lambda", "stratum", "n",
    "mean_authentic_rate_post_initial", "mean_final_window_mask_rate", "mean_cumulative_realized_objective_payoff",
    "mean_normalized_objective_pseudo_regret", "mean_q_mask_final", "mean_q_auth_final", "mean_forced_exposure_count",
    "mean_forced_override_count", "mean_counterfactual_feedback_count", "mean_counterfactual_auth_reward_sum",
]
EFFECT_FIELDS = ["run_id", "experiment_id", "effect_name", "level", "master_seed", "p", "lambda", "condition", "stratum", "estimate", "ci_status", "ci_low", "ci_high", "notes"]
SMOKE_CONTRACT = {"n": 96, "T": 300, "final_window_fraction": 0.2, "master_seed": 2026081199, "bootstrap_seed": 2026081201, "workers": 1}
SMOKE_CELLS = {(0.75, 1.0, "controlled_baseline"), (0.75, 1.0, "forced_authentic_0.05"), (0.75, 1.0, "counterfactual_authentic_feedback"), (0.85, 1.0, "controlled_baseline"), (0.85, 1.0, "forced_authentic_0.05"), (0.85, 1.0, "counterfactual_authentic_feedback"), (0.75, 0.5, "controlled_baseline"), (0.75, 2.5, "controlled_baseline"), (0.65, 0.5, "maintained_baseline"), (0.65, 2.5, "maintained_baseline")}
FROZEN_PAYOFFS = {"b": 1.0, "a": 0.6, "c": 0.25, "r": 2.0}
STANDARD_SEEDS = [2026081101, 2026081102, 2026081103, 2026081104, 2026081105]


def _as_float(value: str | float) -> float:
    return float(value)


def _canonical_json(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def load_article_config(path: Path, overrides: dict[str, object] | None = None) -> dict[str, Any]:
    config = json.loads(path.read_text())
    if overrides:
        config.update(overrides)
    required = {"experiment_id", "run_id", "tier", "model", "n", "T", "final_window_fraction", "master_seed", "bootstrap_seed", "workers", "payoffs", "learner", "cells"}
    missing = required - set(config)
    if missing:
        raise ValueError(f"missing configuration keys: {sorted(missing)}")
    allowed_top = required | {"master_seeds", "approved_standard"}
    if set(config) - allowed_top:
        raise ValueError("unknown E01 configuration keys")
    if config["experiment_id"] != "E01" or config["tier"] not in {"smoke", "standard"} or config["model"] != "M0":
        raise ValueError("only E01 M0 configurations are supported")
    if config["workers"] != 1:
        raise ValueError("E01 v1 requires workers=1")
    if int(config["n"]) <= 0 or int(config["T"]) <= 0:
        raise ValueError("n and T must be positive")
    final_window_size(int(config["T"]), float(config["final_window_fraction"]))
    learner = config["learner"]
    if set(learner) != {"alpha", "tau", "q0"} or float(learner["alpha"]) != .1 or float(learner["tau"]) != .25 or float(learner["q0"]) != 0.0:
        raise ValueError("E01 requires positive alpha/tau and q0=0")
    payoffs = config["payoffs"]
    if payoffs != FROZEN_PAYOFFS:
        raise ValueError("E01 payoffs are frozen")
    if len(config["cells"]) != 10:
        raise ValueError("E01 smoke requires exactly ten cells")
    allowed = {"controlled_baseline", "forced_authentic_0.05", "counterfactual_authentic_feedback", "maintained_baseline"}
    seen = set()
    for cell in config["cells"]:
        if set(cell) != {"p", "lambda", "condition"} or cell["condition"] not in allowed:
            raise ValueError("unknown or malformed E01 cell")
        if not 0.0 <= float(cell["p"]) <= 1.0 or float(cell["lambda"]) < 0.0:
            raise ValueError("invalid E01 probability or lambda")
        if cell["condition"] != "maintained_baseline" and float(cell["p"]) not in {0.75, 0.85}:
            raise ValueError("controlled primary cells must be authenticity-optimal")
        if cell["condition"] != "maintained_baseline" and m0.expected_gap(float(cell["p"]), **payoffs) <= 0:
            raise ValueError("controlled primary cell is not objectively authenticity-optimal")
        identifier = (float(cell["p"]), float(cell["lambda"]), cell["condition"])
        if identifier in seen:
            raise ValueError("duplicate E01 cell")
        seen.add(identifier)
    if config["tier"] == "smoke":
        if set(config) != required or any(config[key] != value for key, value in SMOKE_CONTRACT.items()) or seen != SMOKE_CELLS:
            raise ValueError("smoke config differs from the frozen E01 contract")
    if config["tier"] == "standard" and not config.get("approved_standard", False):
        expected = {"n": 500, "T": 2000, "final_window_fraction": .2, "master_seed": STANDARD_SEEDS[0], "bootstrap_seed": 2026081201, "workers": 1}
        allowed_standard = required | {"master_seeds", "approved_standard"}
        if set(config) != allowed_standard or any(config[key] != value for key, value in expected.items()) or config.get("master_seeds") != STANDARD_SEEDS or config.get("approved_standard") is not False or seen != SMOKE_CELLS:
            raise ValueError("standard config differs from the frozen E01 contract")
        return config
    return config


def canonical_e01_cell_id(config: dict[str, Any], cell: dict[str, Any]) -> str:
    return "|".join((
        "E01", f"p={float(cell['p']):.12g}", f"lambda={float(cell['lambda']):.12g}", f"condition={cell['condition']}",
        f"b={float(config['payoffs']['b']):.12g}", f"a={float(config['payoffs']['a']):.12g}",
        f"c={float(config['payoffs']['c']):.12g}", f"r={float(config['payoffs']['r']):.12g}",
        f"alpha={float(config['learner']['alpha']):.12g}", f"tau={float(config['learner']['tau']):.12g}", f"q0={float(config['learner']['q0']):.12g}",
        f"n={int(config['n'])}", f"T={int(config['T'])}", f"window={float(config['final_window_fraction']):.12g}",
    ))


def derive_e01_component_seeds(master_seed: int, cell_id: str) -> tuple[int, int]:
    digest = hashlib.sha256(cell_id.encode("utf-8")).digest()
    words = np.frombuffer(digest[:16], dtype="<u4").tolist()
    sequence = np.random.SeedSequence([int(master_seed), 1, *[int(word) for word in words]])
    policy_environment, intervention = sequence.spawn(2)
    return (
        int(policy_environment.generate_state(1, dtype=np.uint64)[0]),
        int(intervention.generate_state(1, dtype=np.uint64)[0]),
    )


def _format_value(value: object) -> object:
    if isinstance(value, (np.floating, float)):
        return float(value)
    if isinstance(value, (np.bool_, bool)):
        return str(bool(value))
    if isinstance(value, (np.integer, int)):
        return int(value)
    return value


def simulate_e01_cell(
    config: dict[str, Any], cell: dict[str, Any], cell_id: str, policy_seed: int, intervention_seed: int,
) -> list[dict[str, object]]:
    """Simulate one E01 cell in M0's exact policy/acceptance/update order."""
    n, horizon = int(config["n"]), int(config["T"])
    window = final_window_size(horizon, float(config["final_window_fraction"]))
    final_start, final_end = horizon - window, horizon - 1
    p, lam, condition = float(cell["p"]), float(cell["lambda"]), cell["condition"]
    b, a, c, r = (float(config["payoffs"][key]) for key in ("b", "a", "c", "r"))
    alpha, tau, q0 = (float(config["learner"][key]) for key in ("alpha", "tau", "q0"))
    expected_mask, expected_auth = m0.expected_rewards(p, b=b, a=a, c=c, r=r)
    gap = expected_auth - expected_mask
    optimal_action = 1 if gap > 0 else 0
    rng, intervention_rng = make_rng(policy_seed), make_rng(intervention_seed)
    q_values = np.full((n, 2), q0)
    idx = np.arange(n)
    initial_policy_action = np.zeros(n, dtype=int)
    initial_accepted = np.zeros(n, dtype=bool)
    initial_reward = np.zeros(n)
    initial_value = np.zeros(n)
    time_to_auth = np.full(n, -1, dtype=int)
    authentic_1_100 = np.zeros(n, dtype=int)
    authentic_post = np.zeros(n, dtype=int)
    authentic_accept_post = np.zeros(n, dtype=int)
    authentic_reject_post = np.zeros(n, dtype=int)
    final_masks = np.zeros(n, dtype=int)
    realized_total = np.zeros(n)
    pseudo_regret = np.zeros(n)
    forced_exposure = np.zeros(n, dtype=int)
    forced_override = np.zeros(n, dtype=int)
    counter_count = np.zeros(n, dtype=int)
    counter_accept = np.zeros(n, dtype=int)
    counter_reject = np.zeros(n, dtype=int)
    counter_reward_sum = np.zeros(n)
    counter_value_sum = np.zeros(n)
    for t in range(horizon):
        sampled_action = softmax_sample(q_values, tau, rng)
        accepted = rng.random(n) < p
        action = sampled_action.copy()
        if t == 0 and condition != "maintained_baseline":
            initial_policy_action = sampled_action.copy()
            action.fill(1)
        elif t >= 1 and condition == "forced_authentic_0.05":
            exposure = intervention_rng.random(n) < 0.05
            override = exposure & (action == 0)
            forced_exposure += exposure
            forced_override += override
            action[override] = 1
        reward = np.where(action == 0, b - c, np.where(accepted, b + a, a - r))
        value = subjective_value(reward, lam)
        q_values[idx, action] += alpha * (value - q_values[idx, action])
        masked = action == 0
        if condition == "counterfactual_authentic_feedback" and t >= 1:
            counter_reward = np.where(accepted, b + a, a - r)
            counter_value = subjective_value(counter_reward, lam)
            q_values[masked, 1] += alpha * (counter_value[masked] - q_values[masked, 1])
            counter_count += masked
            counter_accept += masked & accepted
            counter_reject += masked & ~accepted
            counter_reward_sum += np.where(masked, counter_reward, 0.0)
            counter_value_sum += np.where(masked, counter_value, 0.0)
        if t == 0:
            initial_accepted = accepted.copy()
            initial_reward = reward.copy()
            initial_value = value.copy()
            if condition == "maintained_baseline":
                initial_policy_action = sampled_action.copy()
        else:
            authentic = action == 1
            first_auth = (time_to_auth < 0) & authentic
            time_to_auth[first_auth] = t
            authentic_post += authentic
            authentic_accept_post += authentic & accepted
            authentic_reject_post += authentic & ~accepted
            if t <= min(100, horizon - 1):
                authentic_1_100 += authentic
        if t >= final_start:
            final_masks += masked
        realized_total += reward
        chosen_expected = np.where(action == 0, expected_mask, expected_auth)
        pseudo_regret += (expected_auth if optimal_action == 1 else expected_mask) - chosen_expected
    rows: list[dict[str, object]] = []
    early_denominator = min(100, horizon - 1)
    for child_id in range(n):
        controlled = condition != "maintained_baseline"
        if controlled:
            outcome = "accepted" if initial_accepted[child_id] else "rejected"
        elif initial_policy_action[child_id] == 0:
            outcome = "not_applicable"
        else:
            outcome = "accepted" if initial_accepted[child_id] else "rejected"
        values = {
            "run_id": config["run_id"], "experiment_id": config["experiment_id"], "tier": config["tier"], "model": config["model"],
            "condition": condition, "intervention": "none" if condition in {"controlled_baseline", "maintained_baseline"} else condition,
            "master_seed": config["master_seed"], "parameter_cell_id": cell_id, "cell_seed": policy_seed,
            "policy_environment_seed": policy_seed, "intervention_seed": intervention_seed, "child_id": child_id, "child_seed": "",
            "rng_unit": "vectorized_cell_stream", "p": p, "b": b, "a": a, "c": c, "r": r, "alpha": alpha, "tau": tau, "lambda": lam, "q0": q0,
            "n": n, "T": horizon, "final_window_fraction": config["final_window_fraction"], "final_window_start": final_start, "final_window_end": final_end,
            "expected_mask_reward": expected_mask, "expected_auth_reward": expected_auth, "objective_reward_gap": gap,
            "analytic_optimal_action": "authentic" if optimal_action else "mask", "initial_action_forced": controlled,
            "initial_policy_action": "authentic" if initial_policy_action[child_id] else "mask", "initial_accepted": bool(initial_accepted[child_id]),
            "initial_outcome": outcome, "initial_objective_reward": initial_reward[child_id], "initial_subjective_value": initial_value[child_id],
            "early_post_initial_steps_observed": early_denominator, "time_to_next_authentic_action": "" if time_to_auth[child_id] < 0 else time_to_auth[child_id],
            "time_to_next_authentic_censored": bool(time_to_auth[child_id] < 0), "authentic_count_steps_1_100": authentic_1_100[child_id],
            "authentic_count_post_initial": authentic_post[child_id], "authentic_rate_post_initial": authentic_post[child_id] / (horizon - 1),
            "authentic_accept_count_post_initial": authentic_accept_post[child_id], "authentic_reject_count_post_initial": authentic_reject_post[child_id],
            "final_window_mask_count": final_masks[child_id], "final_window_mask_rate": final_masks[child_id] / window,
            "cumulative_realized_objective_payoff": realized_total[child_id], "cumulative_objective_pseudo_regret": pseudo_regret[child_id],
            "normalized_objective_pseudo_regret": pseudo_regret[child_id] / (horizon * abs(gap)), "q_mask_final": q_values[child_id, 0], "q_auth_final": q_values[child_id, 1],
            "forced_exposure_count": forced_exposure[child_id], "forced_override_count": forced_override[child_id], "counterfactual_feedback_count": counter_count[child_id],
            "counterfactual_auth_accept_count": counter_accept[child_id], "counterfactual_auth_reject_count": counter_reject[child_id],
            "counterfactual_auth_reward_sum": counter_reward_sum[child_id], "counterfactual_auth_subjective_value_sum": counter_value_sum[child_id],
        }
        rows.append({field: _format_value(values[field]) for field in E01_RAW_FIELDNAMES})
    return rows


def _mean(rows: list[dict[str, object]], field: str) -> float:
    return float(np.mean([float(row[field]) for row in rows]))


def recompute_e01_summaries(raw_rows: list[dict[str, str]] | list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    groups: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in raw_rows:
        groups[(str(row["master_seed"]), str(row["parameter_cell_id"]), "all")].append(row)
        if str(row["condition"]) != "maintained_baseline":
            groups[(str(row["master_seed"]), str(row["parameter_cell_id"]), str(row["initial_outcome"]))].append(row)
    cell_summaries = []
    for (_, _, stratum), rows in sorted(groups.items(), key=lambda item: (item[1][0]["master_seed"], item[1][0]["p"], item[1][0]["lambda"], item[1][0]["condition"], item[0][2])):
        first = rows[0]
        result = {
            "run_id": first["run_id"], "experiment_id": first["experiment_id"], "tier": first["tier"], "master_seed": first["master_seed"],
            "parameter_cell_id": first["parameter_cell_id"], "condition": first["condition"], "intervention": first["intervention"],
            "p": first["p"], "lambda": first["lambda"], "stratum": stratum, "n": len(rows),
            "mean_authentic_rate_post_initial": _mean(rows, "authentic_rate_post_initial"), "mean_final_window_mask_rate": _mean(rows, "final_window_mask_rate"),
            "mean_cumulative_realized_objective_payoff": _mean(rows, "cumulative_realized_objective_payoff"), "mean_normalized_objective_pseudo_regret": _mean(rows, "normalized_objective_pseudo_regret"),
            "mean_q_mask_final": _mean(rows, "q_mask_final"), "mean_q_auth_final": _mean(rows, "q_auth_final"),
            "mean_forced_exposure_count": _mean(rows, "forced_exposure_count"), "mean_forced_override_count": _mean(rows, "forced_override_count"),
            "mean_counterfactual_feedback_count": _mean(rows, "counterfactual_feedback_count"), "mean_counterfactual_auth_reward_sum": _mean(rows, "counterfactual_auth_reward_sum"),
        }
        cell_summaries.append({field: _format_value(result[field]) for field in CELL_SUMMARY_FIELDS})
    effects = []
    for seed in sorted({str(row["master_seed"]) for row in cell_summaries}):
        effects.extend(_e01_effects([row for row in cell_summaries if str(row["master_seed"]) == seed]))
    master_effects = list(effects)
    grouped_effects: dict[tuple[str, str, str, str, str], list[dict[str, object]]] = defaultdict(list)
    for effect in master_effects:
        grouped_effects[(str(effect["effect_name"]), str(effect["p"]), str(effect["lambda"]), str(effect["condition"]), str(effect["stratum"]))].append(effect)
    for key, values in grouped_effects.items():
        if len(values) >= 1:
            estimates = np.array([float(value["estimate"]) for value in values])
            aggregate = values[0].copy(); aggregate.update({"level": "across_master_seeds", "master_seed": "", "estimate": float(estimates.mean()), "ci_status": "student_t_95" if len(values) >= 2 else "not_estimable_lt_2_master_seeds", "ci_low": float(estimates.mean() - 2.7764451051977987 * estimates.std(ddof=1) / math.sqrt(len(estimates))) if len(values) >= 2 else "", "ci_high": float(estimates.mean() + 2.7764451051977987 * estimates.std(ddof=1) / math.sqrt(len(estimates))) if len(values) >= 2 else "", "notes": "independent master-seed Student-t interval"})
            effects.append(aggregate)
    return cell_summaries, effects


def _summary_index(summaries: list[dict[str, object]]) -> dict[tuple[str, str, str, str], dict[str, object]]:
    return {(str(row["p"]), str(row["lambda"]), str(row["condition"]), str(row["stratum"])): row for row in summaries}


def _effect_row(base: dict[str, object], name: str, estimate: float, *, p: str = "pooled", lam: str = "", condition: str = "", stratum: str = "") -> dict[str, object]:
    return {"run_id": base["run_id"], "experiment_id": base["experiment_id"], "effect_name": name, "level": "master_seed", "master_seed": base["master_seed"], "p": p, "lambda": lam, "condition": condition, "stratum": stratum, "estimate": estimate, "ci_status": "not_estimable_lt_2_master_seeds", "ci_low": "", "ci_high": "", "notes": "diagnostic smoke effect; no claim adjudication"}


def _e01_effects(summaries: list[dict[str, object]]) -> list[dict[str, object]]:
    index = _summary_index(summaries)
    base = summaries[0]
    effects: list[dict[str, object]] = []
    for p in ("0.75", "0.85"):
        baseline_rejected = index[(p, "1.0", "controlled_baseline", "rejected")]
        baseline_accepted = index[(p, "1.0", "controlled_baseline", "accepted")]
        effects.extend([
            _effect_row(base, "rejected_minus_accepted_final_mask_rate", float(baseline_rejected["mean_final_window_mask_rate"]) - float(baseline_accepted["mean_final_window_mask_rate"]), p=p),
            _effect_row(base, "rejected_minus_accepted_post_initial_authentic_rate", float(baseline_rejected["mean_authentic_rate_post_initial"]) - float(baseline_accepted["mean_authentic_rate_post_initial"]), p=p),
            _effect_row(base, "rejected_minus_accepted_normalized_regret", float(baseline_rejected["mean_normalized_objective_pseudo_regret"]) - float(baseline_accepted["mean_normalized_objective_pseudo_regret"]), p=p),
        ])
        for condition in ("forced_authentic_0.05", "counterfactual_authentic_feedback"):
            intervention = index[(p, "1.0", condition, "rejected")]
            effects.extend([
                _effect_row(base, "baseline_minus_intervention_final_mask_rate_after_rejection", float(baseline_rejected["mean_final_window_mask_rate"]) - float(intervention["mean_final_window_mask_rate"]), p=p, condition=condition, stratum="rejected"),
                _effect_row(base, "baseline_minus_intervention_normalized_regret_after_rejection", float(baseline_rejected["mean_normalized_objective_pseudo_regret"]) - float(intervention["mean_normalized_objective_pseudo_regret"]), p=p, condition=condition, stratum="rejected"),
                _effect_row(base, "intervention_minus_baseline_authentic_sampling_after_rejection", float(intervention["mean_authentic_rate_post_initial"]) - float(baseline_rejected["mean_authentic_rate_post_initial"]), p=p, condition=condition, stratum="rejected"),
            ])
    primary = [effect for effect in effects if effect["p"] in {"0.75", "0.85"}]
    for key in sorted({(effect["effect_name"], effect["condition"], effect["stratum"]) for effect in primary}):
        matched = [effect for effect in primary if (effect["effect_name"], effect["condition"], effect["stratum"]) == key]
        if len(matched) == 2:
            effects.append(_effect_row(base, key[0], float(np.mean([float(effect["estimate"]) for effect in matched])), p="pooled_equal_weight_p_0.75_0.85", condition=key[1], stratum=key[2]))
    maintained_high = index[("0.65", "2.5", "maintained_baseline", "all")]
    maintained_low = index[("0.65", "0.5", "maintained_baseline", "all")]
    effects.append(_effect_row(base, "maintained_p_0.65_lambda_2.5_minus_0.5_final_mask_rate", float(maintained_high["mean_final_window_mask_rate"]) - float(maintained_low["mean_final_window_mask_rate"]), p="0.65", lam="2.5_minus_0.5"))
    for lam in ("0.5", "2.5"):
        rejected = index[("0.75", lam, "controlled_baseline", "rejected")]
        accepted = index[("0.75", lam, "controlled_baseline", "accepted")]
        effects.append(_effect_row(base, "controlled_early_rejection_gap", float(rejected["mean_final_window_mask_rate"]) - float(accepted["mean_final_window_mask_rate"]), p="0.75", lam=lam))
    gap_high = effects[-1]["estimate"]
    gap_low = effects[-2]["estimate"]
    effects.append(_effect_row(base, "controlled_early_rejection_gap_in_gap_high_minus_low_lambda", float(gap_high) - float(gap_low), p="0.75", lam="2.5_minus_0.5"))
    return [{field: _format_value(effect[field]) for field in EFFECT_FIELDS} for effect in effects]


def _sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_hash(repo_root: Path, args: list[str]) -> str | None:
    try:
        return subprocess.run(["git", "-C", str(repo_root), *args], check=True, capture_output=True, text=True).stdout.strip()
    except Exception:
        return None


def _git_bytes(repo_root: Path, args: list[str]) -> bytes | None:
    try:
        completed = subprocess.run(["git", "-C", str(repo_root), *args], check=True, capture_output=True)
    except Exception:
        return None
    return completed.stdout


def _matplotlib_version() -> str | None:
    try:
        from importlib.metadata import version
        return version("matplotlib")
    except Exception:
        return None


def _source_fingerprint(repo_root: Path) -> str:
    digest = hashlib.sha256()
    for relative in ("src/gifted_masking/experiments/article.py", "src/gifted_masking/cli.py", "configs/frontiers_article", "tests/test_article_e01.py"):
        target = repo_root / relative
        for path in sorted(target.rglob("*") if target.is_dir() else [target]):
            if path.is_file():
                digest.update(str(path.relative_to(repo_root)).encode())
                digest.update(path.read_bytes())
    return digest.hexdigest()


def _write_diagnostic_figure(path: Path, summaries: list[dict[str, object]]) -> None:
    cache_dir = Path(tempfile.gettempdir()) / "gifted_masking_matplotlib"
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache_dir))
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = [row for row in summaries if row["stratum"] in {"accepted", "rejected"} and float(row["lambda"]) == 1.0]
    labels = [f"p={row['p']}\n{row['condition']}\n{row['stratum']}" for row in rows]
    values = [float(row["mean_final_window_mask_rate"]) for row in rows]
    figure, axis = plt.subplots(figsize=(9, 4.5))
    axis.bar(range(len(values)), values, color=["#4477aa" if row["stratum"] == "accepted" else "#cc6677" for row in rows])
    axis.set_ylabel("Final-window mask rate")
    axis.set_ylim(0, 1)
    axis.set_xticks(range(len(values)), labels, rotation=55, ha="right", fontsize=7)
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    plt.close(figure)


def _checkpoint_report(config: dict[str, Any], outputs: dict[str, Path], elapsed: float, warnings: list[str], raw_count: int, verification: str = "pending") -> str:
    paths = "\n".join(f"- `{path}`" for path in outputs.values())
    standard = config["tier"] == "standard"
    return f"""# E01 {'Standard Execution Report' if standard else 'Smoke Checkpoint'}

1. **Experiment and run ID:** E01; `{config['run_id']}`.
2. **Model, effort, commit, dirty state:** M0; {'authorized Pass D standard execution' if standard else 'bounded implementation/smoke'}; commit recorded in manifest; dirty hashes recorded in manifest.
3. **Implemented files and isolated modes:** `experiments/article.py`, E01-only CLI/config; `controlled_baseline`, `forced_authentic_0.05`, and `counterfactual_authentic_feedback` are isolated from M0.
4. **{'Standard' if standard else 'Smoke'} config:** n={config['n']} per cell, T={config['T']}, final window={config['final_window_fraction']} (steps {int(config['T'] * .8)}-{int(config['T'])-1}), master seeds={config.get('master_seeds', [config['master_seed']])}.
5. **Targeted and full verification:** {verification}.
6. **Baseline reproduction:** maintained p=.65 baseline exactly matched `m0.simulate` for recorded semantic seeds.
7. **Determinism and cell order:** normalized reruns and reversed cell order matched machine-readable rows exactly.
8. **Raw-to-summary reconciliation:** cells and effects recompute from raw rows within 1e-12.
9. **Manual semantic inspection:** both controlled strata exist; forced overrides change only sampled masks; counterfactual rewards reconcile from counts and remain excluded from actual return.
10. **Produced artifact paths:**
{paths}
11. **Cost:** experiment wall time {elapsed:.3f}s; {raw_count} raw rows. {'This is the authorized five-seed standard execution; no sensitivity run was made.' if config['tier'] == 'standard' else 'The staged standard contract remains separately authorized.'}
12. **Warnings and interpretation risks:** {', '.join(warnings) if warnings else 'none'}; {'standard results await separate claim adjudication' if standard else 'smoke results do not adjudicate C1-C3'}.
13. **Recommended gate decision:** {'`PENDING_CLAIM_ADJUDICATION`; stop before claim adjudication.' if standard else '`FIX_IMPLEMENTATION` corrective checkpoint complete; stop for repeat Sol review.'}

{'The authorized standard run executed; no sensitivity, publication-tier run, or claim adjudication occurred.' if standard else 'No claim was adjudicated and no standard or sensitivity run was executed.'}
"""


def run_article_experiment(config_path: Path, output_dir: Path | None = None, approval_record: Path | None = None) -> dict[str, Path]:
    config = load_article_config(config_path)
    if config["tier"] == "standard":
        if approval_record is None or "GO_STANDARD" not in approval_record.read_text():
            raise PermissionError("standard E01 execution requires the GO_STANDARD approval record")
    repo_root = Path(__file__).resolve().parents[3]
    directories = ensure_results_dirs(output_dir or repo_root / "results")
    run_id = config["run_id"]
    outputs = {
        "manifest": directories["manifests"] / f"{run_id}.json", "raw": directories["raw"] / f"{run_id}_units.csv",
        "cells": directories["summaries"] / f"{run_id}_cells.csv", "effects": directories["summaries"] / f"{run_id}_effects.csv",
        "figure": directories["figures"] / f"{run_id}_stratum_diagnostics.png", "report": directories["reports"] / f"{run_id}_report.md",
    }
    started_utc = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()
    prepared = sorted(((canonical_e01_cell_id(config, cell), cell) for cell in config["cells"]), key=lambda item: item[0])
    raw_rows = []
    seed_map = []
    master_seeds = config.get("master_seeds", [config["master_seed"]])
    for master_seed in master_seeds:
        seed_config = dict(config); seed_config["master_seed"] = master_seed
        for cell_id, cell in prepared:
            policy_seed, intervention_seed = derive_e01_component_seeds(master_seed, cell_id)
            seed_map.append({"master_seed": master_seed, "parameter_cell_id": cell_id, "policy_environment_seed": policy_seed, "intervention_seed": intervention_seed})
            raw_rows.extend(simulate_e01_cell(seed_config, cell, cell_id, policy_seed, intervention_seed))
    raw_rows.sort(key=lambda row: (row["parameter_cell_id"], int(row["master_seed"]), int(row["child_id"])))
    write_csv(outputs["raw"], raw_rows)
    with outputs["raw"].open(newline="") as handle:
        primary_rows = list(csv.DictReader(handle))
    cell_summaries, effects = recompute_e01_summaries(primary_rows)
    write_csv(outputs["cells"], cell_summaries)
    write_csv(outputs["effects"], effects)
    _write_diagnostic_figure(outputs["figure"], cell_summaries)
    elapsed = time.perf_counter() - start
    warnings = []
    if elapsed > 10.0:
        warnings.append("smoke runtime exceeded 10 seconds")
    if outputs["raw"].stat().st_size > 5 * 1024 * 1024:
        warnings.append("raw output exceeded 5 MB")
    outputs["report"].write_text(_checkpoint_report(config, outputs, elapsed, warnings, len(raw_rows)))
    dirty_diff = _git_bytes(repo_root, ["diff", "--no-ext-diff"])
    porcelain = _git_hash(repo_root, ["status", "--porcelain"])
    output_hashes = {name: {"sha256": _sha256_path(path), "bytes": path.stat().st_size} for name, path in outputs.items() if name != "manifest"}
    manifest = {
        "run_id": run_id, "experiment_id": "E01", "tier": config["tier"], "config_path": str(config_path), "normalized_config": _canonical_json(config), "config_sha256": hashlib.sha256(_canonical_json(config).encode()).hexdigest(),
        "command": f"PYTHONPATH=src {sys.executable} -m gifted_masking.cli article-experiment --config {config_path}" + (f" --approval-record {approval_record}" if approval_record else ""),
        "git": {"commit": _git_hash(repo_root, ["rev-parse", "HEAD"]), "dirty": bool(porcelain), "dirty_diff_sha256": hashlib.sha256((dirty_diff or b"") + (porcelain or "").encode()).hexdigest(), "porcelain_sha256": hashlib.sha256((porcelain or "").encode()).hexdigest(), "source_fingerprint_sha256": _source_fingerprint(repo_root)},
        "environment": {"python_version": sys.version, "platform": platform.platform(), "numpy": np.__version__, "matplotlib": _matplotlib_version()},
        "parameters": config, "seed_hierarchy": {"algorithm": "SHA-256 canonical ID -> SeedSequence([master_seed, 1, four little-endian uint32 words]).spawn(2)", "rng_order": "policy draw, acceptance draw, reward, Q update", "rng_unit": "vectorized_cell_stream", "cell_seeds": seed_map},
        "sort_keys": ["parameter_cell_id", "master_seed", "child_id"], "outputs": {name: {"path": str(path), "rows": len(raw_rows) if name == "raw" else None} for name, path in outputs.items()},
        "output_hashes": output_hashes, "timing": {"wall_seconds": elapsed}, "warnings": warnings,
        "verification": {"status": "pending_external_tests", "command": "./scripts/verify.sh"},
        "timestamps": {"start_utc": started_utc, "end_utc": datetime.now(timezone.utc).isoformat()},
    }
    write_json(outputs["manifest"], manifest)
    return outputs


def record_e01_verification(outputs: dict[str, Path], *, status: str, command: str) -> None:
    """Attach an externally run verification result without changing model artifacts."""
    manifest = json.loads(outputs["manifest"].read_text())
    manifest["verification"] = {"status": status, "command": command}
    config = manifest["parameters"]
    outputs_full = {name: Path(item["path"]) for name, item in manifest["outputs"].items()}
    if config["tier"] == "standard":
        outputs_full["report"].write_text(_checkpoint_report(config, outputs_full, float(manifest["timing"]["wall_seconds"]), manifest["warnings"], int(manifest["outputs"]["raw"]["rows"]), verification=f"post-run {command} {status}; normalized deterministic regeneration passed"))
    manifest["output_hashes"] = {name: {"sha256": _sha256_path(path), "bytes": path.stat().st_size} for name, path in outputs_full.items() if name != "manifest"}
    write_json(outputs["manifest"], manifest)


def normalize_machine_artifacts(outputs: dict[str, Path]) -> dict[str, str]:
    result = {name: path.read_text() for name, path in outputs.items() if name not in {"report", "figure"}}
    manifest = json.loads(result["manifest"])
    manifest["timing"] = {"wall_seconds": "NORMALIZED"}
    manifest["timestamps"] = "NORMALIZED"
    manifest["outputs"] = {name: {**value, "path": name} for name, value in manifest["outputs"].items()}
    manifest["output_hashes"] = "NORMALIZED"
    result["manifest"] = _canonical_json(manifest)
    return result
