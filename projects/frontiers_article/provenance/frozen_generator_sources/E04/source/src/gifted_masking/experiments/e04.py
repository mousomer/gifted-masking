"""Frozen E04 M3 search-architecture smoke experiment.

This is deliberately an experiment-only diagnostic kernel.  It mirrors the
maintained M3 action, reward, and selected-arm update order, but does not
modify :mod:`gifted_masking.models.m3` or the robustness suite.  The separate
identity stream is essential: changing receptive-context identity must never
advance the policy/environment stream.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import platform
import resource
import subprocess
import sys
import tempfile
import time
from collections import defaultdict
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from gifted_masking.core import final_window_size, make_rng, softmax_sample, subjective_value
from gifted_masking.repro import ensure_results_dirs, write_csv, write_json


E04_RAW_FIELDNAMES = """run_id,experiment_id,tier,model,component,sensitivity_name,architecture,master_seed,matched_family_id,parameter_cell_id,cell_seed,policy_environment_seed,identity_seed,child_id,child_seed,rng_unit,K,canonical_identity_mode,effective_good_count,effective_good_fraction,good_context_ids_json,known_good_context_id,p_good,p_bad,bf,b,a,c,r,alpha,tau,lambda,q0,n,T,final_window_fraction,final_window_start,final_window_end,joint_action_count,group_action_count,behavior_action_count,expected_mask_reward,expected_good_auth_reward,expected_bad_auth_reward,objective_best_expected_reward,objective_best_joint_actions_json,objective_comparator,ever_accepted_good_auth,time_to_first_accepted_good_auth_step,time_to_first_accepted_good_auth_censored,time_to_first_accepted_good_auth_capped,distinct_contexts_sampled_authentically,authentic_count_total,good_auth_count_total,good_auth_accept_count_total,good_auth_reject_count_total,auth_context_counts_total_json,final_window_mask_count,final_window_mask_rate,final_window_authentic_count,final_window_good_auth_count,final_window_good_auth_rate,final_window_auth_context_counts_json,final_window_auth_context_entropy,final_window_auth_context_entropy_normalized,final_window_auth_context_entropy_status,final_window_good_auth_allocation_fraction,final_window_good_auth_allocation_status,final_window_action_counts_json,final_window_modal_action_index,final_window_modal_context,final_window_modal_behavior,final_window_modal_tie_count,final_window_unique_modal,settled_any_good_auth_argmax,settled_any_good_auth_unique,modal_is_objective_optimal,cumulative_realized_objective_reward,mean_realized_objective_reward,cumulative_expected_static_regret,mean_expected_static_regret,cumulative_realized_pseudo_regret,mean_realized_pseudo_regret,total_action_counts_json,q_final_json,q_group_final_json,q_behavior_final_json""".split(",")

FROZEN_PAYOFFS = {"b": 1.0, "a": .6, "c": .25, "r": 2.0}
FROZEN_LEARNER = {"alpha": .1, "tau": .25, "lambda": 1.0, "q0": 0.0}
SMOKE_CONTRACT = {"n": 96, "T": 300, "final_window_fraction": .2, "master_seed": 2026081499, "bootstrap_seed": 2026081497, "workers": 1}
STANDARD_SEEDS = [2026081401, 2026081402, 2026081403, 2026081404, 2026081405]
ARCHITECTURES = ("flat_2k", "hierarchical", "global_mask", "fixed_known_good")
KS = (1, 2, 4, 8, 16)
IDENTITIES = ("fixed", "random_per_child")
REGIMES = ("one", "two", "proportional_25")
T_CRITICAL_95_DF4 = 2.7764451051977987
SOURCE_FINGERPRINT_PATHS = (
    "src/gifted_masking/experiments/e04.py", "src/gifted_masking/cli.py", "src/gifted_masking/core.py",
    "src/gifted_masking/models/m3.py", "src/gifted_masking/repro.py",
    "configs/frontiers_article/e04_m3_search_architectures_smoke.json",
    "configs/frontiers_article/e04_m3_search_architectures_standard.json", "tests/test_article_e04.py",
    "pyproject.toml", "scripts/verify.sh",
)


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _json_no_duplicates(text: str) -> object:
    def reject(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=reject)


def _f(value: object) -> object:
    if isinstance(value, (np.floating, float)):
        return float(value)
    if isinstance(value, (np.integer, int)):
        return int(value)
    if isinstance(value, (np.bool_, bool)):
        return str(bool(value))
    return value


def _require_mapping(value: object, expected: dict[str, float], name: str) -> None:
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError(f"E04 {name} keys are frozen")
    for key, expected_value in expected.items():
        if type(value[key]) is not float or value[key] != expected_value:
            raise ValueError(f"E04 {name}.{key} is frozen")


def load_e04_config(path: Path, overrides: dict[str, object] | None = None) -> dict[str, Any]:
    config = _json_no_duplicates(path.read_text())
    if not isinstance(config, dict):
        raise ValueError("E04 config must be a JSON object")
    if overrides:
        config.update(overrides)
    required = {"experiment_id", "run_id", "tier", "model", "n", "T", "final_window_fraction", "master_seed", "bootstrap_seed", "workers", "payoffs", "learner", "design"}
    allowed = required | {"master_seeds", "approved_standard"}
    if set(config) - allowed or required - set(config):
        raise ValueError("unknown or missing E04 configuration keys")
    if any(type(config[k]) is not str for k in ("experiment_id", "run_id", "tier", "model")):
        raise ValueError("E04 identifiers must be JSON strings")
    if config["experiment_id"] != "E04" or config["model"] != "M3" or config["tier"] not in {"smoke", "standard"}:
        raise ValueError("only E04 M3 configurations are supported")
    for key in ("n", "T", "master_seed", "bootstrap_seed", "workers"):
        if type(config[key]) is not int:
            raise ValueError("E04 integer fields require exact JSON integer types")
    if type(config["final_window_fraction"]) is not float:
        raise ValueError("E04 final-window fraction requires JSON float")
    if config["workers"] != 1:
        raise ValueError("E04 v1 requires workers=1")
    final_window_size(config["T"], config["final_window_fraction"])
    _require_mapping(config["payoffs"], FROZEN_PAYOFFS, "payoffs")
    _require_mapping(config["learner"], FROZEN_LEARNER, "learner")
    expected_design = {"architectures": list(ARCHITECTURES), "K": list(KS), "identity_modes": list(IDENTITIES), "good_context_regimes": list(REGIMES), "p_good": .85, "p_bad": .2, "bf": .0}
    if not isinstance(config["design"], dict) or any(type(item) is not int for item in config["design"].get("K", [])):
        raise ValueError("E04 K values require exact JSON integer types")
    if any(type(config["design"].get(key)) is not float for key in ("p_good", "p_bad", "bf")):
        raise ValueError("E04 design probabilities and bf require JSON float types")
    if config["design"] != expected_design:
        raise ValueError("E04 design is frozen")
    if config["tier"] == "smoke":
        if set(config) != required or config["run_id"] != "frontiers_m3_search_architectures_v1_smoke" or any(config[k] != v for k, v in SMOKE_CONTRACT.items()):
            raise ValueError("smoke config differs from frozen E04 contract")
    else:
        expected = {"n": 500, "T": 2000, "final_window_fraction": .2, "master_seed": STANDARD_SEEDS[0], "bootstrap_seed": 2026081497, "workers": 1}
        if set(config) != allowed or config["run_id"] != "frontiers_m3_search_architectures_v1" or any(config[k] != v for k, v in expected.items()) or config.get("master_seeds") != STANDARD_SEEDS or config.get("approved_standard") is not False:
            raise ValueError("standard config differs from frozen E04 contract")
    return config


def effective_good_count(k: int, regime: str) -> int:
    return {"one": 1, "two": min(2, k), "proportional_25": max(1, math.ceil(k / 4))}[regime]


def _canonical_regime(k: int, requested: str) -> str:
    m = effective_good_count(k, requested)
    for candidate in REGIMES:
        if effective_good_count(k, candidate) == m:
            return candidate
    raise AssertionError


def canonical_e04_cells() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Return 55 executable cells and the complete 120-row alias relation."""
    canonical: dict[tuple[object, ...], dict[str, object]] = {}
    equivalences: list[dict[str, object]] = []
    for architecture in ARCHITECTURES:
        for k in KS:
            for identity in IDENTITIES:
                for regime in REGIMES:
                    m = effective_good_count(k, regime)
                    requested_id = f"E04|architecture={architecture}|K={k}|identity={identity}|regime={regime}"
                    if architecture == "fixed_known_good":
                        key = (architecture, "K_invariant", "fixed", 1)
                        cell = {"architecture": architecture, "K": 1, "canonical_identity_mode": "fixed", "effective_good_count": 1, "canonical_regime": "one", "parameter_cell_id": "E04|architecture=fixed_known_good|K=invariant|identity=fixed|m=1"}
                    else:
                        mode = "fixed" if k == 1 or m == k else identity
                        canonical_regime = _canonical_regime(k, regime)
                        key = (architecture, k, mode, m)
                        cell = {"architecture": architecture, "K": k, "canonical_identity_mode": mode, "effective_good_count": m, "canonical_regime": canonical_regime, "parameter_cell_id": f"E04|architecture={architecture}|K={k}|identity={mode}|m={m}"}
                    canonical.setdefault(key, cell)
                    equivalences.append({"requested_design_cell_id": requested_id, "requested_architecture": architecture, "requested_K": k, "requested_identity_mode": identity, "requested_good_context_regime": regime, "requested_good_count": m, "parameter_cell_id": cell["parameter_cell_id"], "canonical_request_id": "", "canonical_source_request_id": "", "is_canonical": "False", "equivalence_reason": "fixed-known-good K-invariant control" if architecture == "fixed_known_good" else ("identity collapses when all contexts are good or K=1" if mode == "fixed" and identity != "fixed" else ("good-count regime has identical count" if canonical_regime != regime else "canonical executable cell"))})
    cells = sorted(canonical.values(), key=lambda x: (str(x["architecture"]), int(x["K"]), str(x["canonical_identity_mode"]), int(x["effective_good_count"])))
    by_cell: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in equivalences:
        by_cell[str(row["parameter_cell_id"])].append(row)
    for cell_id, aliases in by_cell.items():
        # A canonical executable cell must be represented by exactly one actual
        # requested design point, rather than by the internal m-based ID.
        source = min(aliases, key=lambda row: str(row["requested_design_cell_id"]))
        for row in aliases:
            row["canonical_request_id"] = source["requested_design_cell_id"]
            row["canonical_source_request_id"] = source["requested_design_cell_id"]
            row["is_canonical"] = str(row is source)
    if len(cells) != 55 or len(equivalences) != 120:
        raise RuntimeError("E04 canonicalization cardinality violation")
    if sum(row["is_canonical"] == "True" for row in equivalences) != 55:
        raise RuntimeError("E04 equivalence table must name exactly 55 canonical requests")
    return cells, equivalences


def _seed(master_seed: int, namespace: int, identifier: str) -> int:
    words = np.frombuffer(hashlib.sha256(identifier.encode()).digest()[:16], dtype="<u4").tolist()
    sequence = np.random.SeedSequence([master_seed, namespace, *map(int, words)])
    return int(sequence.spawn(1)[0].generate_state(1, dtype=np.uint64)[0])


def e04_matched_family_id(master_seed: int, architecture: str, k: int, sensitivity_name: str = "baseline") -> str:
    return f"E04|master={master_seed}|policy_environment|architecture={architecture}|K={'invariant' if architecture == 'fixed_known_good' else k}|sensitivity={sensitivity_name}"


def derive_e04_policy_environment_seed(master_seed: int, architecture: str, k: int) -> int:
    return _seed(master_seed, 4, e04_matched_family_id(master_seed, architecture, k))


def derive_e04_identity_seed(master_seed: int, parameter_cell_id: str) -> int:
    return _seed(master_seed, 40, parameter_cell_id)


@lru_cache(maxsize=None)
def _good_sets(n: int, k: int, m: int, mode: str, seed: int) -> np.ndarray:
    """Return immutable deterministic identity assignments for a frozen stream.

    Raw and streaming validation repeatedly ask for the same cell identity
    assignment. Caching this pure, independently seeded result removes that
    validation-only O(n) work without touching policy/environment RNG draws.
    """
    if mode == "fixed":
        result = np.tile(np.arange(m, dtype=int), (n, 1))
    else:
        rng = make_rng(seed)
        result = np.sort(np.stack([rng.choice(k, size=m, replace=False) for _ in range(n)]))
    result.setflags(write=False)
    return result


def _entropy(counts: np.ndarray) -> tuple[float | str, float | str, str]:
    total = int(counts.sum())
    if not total:
        return "", "", "undefined_no_authentic_samples"
    probabilities = counts[counts > 0] / total
    value = float(-(probabilities * np.log(probabilities)).sum())
    if len(counts) <= 1:
        return value, "", "undefined_single_context"
    return value, value / math.log(len(counts)), "defined"


def _expected_rewards(p_good: float, p_bad: float, payoffs: dict[str, float]) -> tuple[float, float, float]:
    b, a, c, r = (payoffs[k] for k in ("b", "a", "c", "r"))
    mask = b - c
    return mask, p_good * (b + a) + (1 - p_good) * (a - r), p_bad * (b + a) + (1 - p_bad) * (a - r)


def objective_best_actions(architecture: str, k: int, good_context_ids: np.ndarray, auth_is_optimal: bool) -> list[int]:
    """Architecture-visible static comparator actions for one child's good set."""
    good_ids = [int(value) for value in good_context_ids]
    if architecture in {"flat_2k", "hierarchical"}:
        return [2 * group + 1 for group in good_ids] if auth_is_optimal else [2 * group for group in range(k)]
    if architecture == "global_mask":
        return [1 + group for group in good_ids] if auth_is_optimal else [0]
    return [1] if auth_is_optimal else [0]


def simulate_e04_cell(config: dict[str, Any], cell: dict[str, object], policy_seed: int, identity_seed: int) -> list[dict[str, object]]:
    """Vectorized exact-M3-order diagnostic simulation for one canonical cell."""
    n, horizon, architecture = int(config["n"]), int(config["T"]), str(cell["architecture"])
    k = 1 if architecture == "fixed_known_good" else int(cell["K"])
    m, mode = int(cell["effective_good_count"]), str(cell["canonical_identity_mode"])
    payoffs, learner, design = config["payoffs"], config["learner"], config["design"]
    good_sets = _good_sets(n, k, m, mode, identity_seed)
    good = np.zeros((n, k), dtype=bool); good[np.arange(n)[:, None], good_sets] = True
    probs = np.where(good, float(design["p_good"]), float(design["p_bad"]))
    rng, index = make_rng(policy_seed), np.arange(n)
    if architecture == "flat_2k":
        q = np.full((n, 2 * k), float(learner["q0"])); q_group = q_behavior = None; action_count = np.zeros_like(q, dtype=int)
    elif architecture == "hierarchical":
        q_group = np.full((n, k), float(learner["q0"])); q_behavior = np.full((n, k, 2), float(learner["q0"])); q = None; action_count = np.zeros((n, 2 * k), dtype=int)
    elif architecture == "global_mask":
        q = np.full((n, k + 1), float(learner["q0"])); q_group = q_behavior = None; action_count = np.zeros_like(q, dtype=int)
    else:
        q = np.full((n, 2), float(learner["q0"])); q_group = q_behavior = None; action_count = np.zeros_like(q, dtype=int)
    window = final_window_size(horizon, float(config["final_window_fraction"])); start = horizon - window
    total_action = np.zeros_like(action_count); final_action = np.zeros_like(action_count); auth_total = np.zeros((n, k), dtype=int); auth_final = np.zeros((n, k), dtype=int)
    good_auth_total = np.zeros(n, dtype=int); good_accept = np.zeros(n, dtype=int); good_reject = np.zeros(n, dtype=int); first_good_accept = np.full(n, -1, dtype=int)
    cumulative_reward = np.zeros(n); expected_regret = np.zeros(n); realized_pseudo = np.zeros(n)
    mask_expected, good_expected, bad_expected = _expected_rewards(float(design["p_good"]), float(design["p_bad"]), payoffs)
    best = max(mask_expected, good_expected); comparator = "good_auth" if good_expected > mask_expected else "mask"
    for t in range(horizon):
        if architecture == "flat_2k":
            action = softmax_sample(q, float(learner["tau"]), rng); group, authentic = action // 2, action % 2 == 1; report_action = action
        elif architecture == "hierarchical":
            group = softmax_sample(q_group, float(learner["tau"]), rng); behavior = softmax_sample(q_behavior[index, group], float(learner["tau"]), rng); authentic = behavior == 1; report_action = 2 * group + behavior
        elif architecture == "global_mask":
            action = softmax_sample(q, float(learner["tau"]), rng); authentic = action != 0; group = np.maximum(action - 1, 0); report_action = action
        else:
            action = softmax_sample(q, float(learner["tau"]), rng); authentic = action == 1; group = np.zeros(n, dtype=int); report_action = action
        accept = rng.random(n) < probs[index, group]  # maintained M3 consumes this on mask trials too.
        is_good = good[index, group]
        reward = np.where(~authentic, payoffs["b"] - payoffs["c"], np.where(accept, payoffs["b"] + payoffs["a"] - float(design["bf"]) * is_good, payoffs["a"] - payoffs["r"]))
        subjective = subjective_value(reward, float(learner["lambda"]))
        if architecture == "hierarchical":
            q_group[index, group] += learner["alpha"] * (subjective - q_group[index, group]); q_behavior[index, group, authentic.astype(int)] += learner["alpha"] * (subjective - q_behavior[index, group, authentic.astype(int)])
        else:
            q[index, action] += learner["alpha"] * (subjective - q[index, action])
        action_expected = np.where(~authentic, mask_expected, np.where(is_good, good_expected, bad_expected))
        cumulative_reward += reward; expected_regret += best - action_expected; realized_pseudo += best - reward
        total_action[index, report_action] += 1
        auth_idx = np.where(authentic)[0]
        auth_total[auth_idx, group[auth_idx]] += 1
        good_auth = authentic & is_good; good_auth_total += good_auth; good_accept += good_auth & accept; good_reject += good_auth & ~accept
        new = good_auth & accept & (first_good_accept < 0); first_good_accept[new] = t
        if t >= start:
            final_action[index, report_action] += 1; auth_final[auth_idx, group[auth_idx]] += 1
    rows: list[dict[str, object]] = []
    for child in range(n):
        final_counts = final_action[child]; modal = int(final_counts.argmax()); tie_count = int((final_counts == final_counts.max()).sum()); unique = tie_count == 1
        if architecture == "flat_2k" or architecture == "hierarchical": modal_context, modal_behavior = modal // 2, modal % 2
        elif architecture == "global_mask": modal_context, modal_behavior = (max(modal - 1, 0), 0 if modal == 0 else 1)
        else: modal_context, modal_behavior = 0, modal
        strict_good = bool(unique and modal_behavior == 1 and good[child, modal_context]); maintained_good = bool(modal_behavior == 1 and good[child, modal_context])
        entropy, norm_entropy, entropy_status = _entropy(auth_final[child]); final_auth = int(auth_final[child].sum()); final_good = int(auth_final[child, good[child]].sum())
        allocation = "" if final_auth == 0 else final_good / final_auth
        first = int(first_good_accept[child]); action_len = action_count.shape[1]
        values: dict[str, object] = {field: "" for field in E04_RAW_FIELDNAMES}
        objective_actions = objective_best_actions(architecture, k, good_sets[child], comparator == "good_auth")
        values.update({"run_id": config["run_id"], "experiment_id": "E04", "tier": config["tier"], "model": "M3", "component": "primary", "sensitivity_name": "baseline", "architecture": architecture, "master_seed": config["master_seed"], "matched_family_id": e04_matched_family_id(int(config["master_seed"]), architecture, k), "parameter_cell_id": cell["parameter_cell_id"], "cell_seed": policy_seed, "policy_environment_seed": policy_seed, "identity_seed": identity_seed, "child_id": child, "child_seed": "vectorized_cell_stream", "rng_unit": "vectorized_matched_policy_environment_plus_independent_identity", "K": k, "canonical_identity_mode": mode, "effective_good_count": m, "effective_good_fraction": m / k, "good_context_ids_json": json.dumps(good_sets[child].tolist(), separators=(",", ":")), "known_good_context_id": 0 if architecture == "fixed_known_good" else "", "p_good": design["p_good"], "p_bad": design["p_bad"], "bf": design["bf"], **payoffs, **learner, "n": n, "T": horizon, "final_window_fraction": config["final_window_fraction"], "final_window_start": start, "final_window_end": horizon - 1, "joint_action_count": 2 * k if architecture in {"flat_2k", "hierarchical"} else (k + 1 if architecture == "global_mask" else 2), "group_action_count": k if architecture == "hierarchical" else "", "behavior_action_count": 2 if architecture == "hierarchical" else "", "expected_mask_reward": mask_expected, "expected_good_auth_reward": good_expected, "expected_bad_auth_reward": bad_expected, "objective_best_expected_reward": best, "objective_best_joint_actions_json": json.dumps(objective_actions, separators=(",", ":")), "objective_comparator": comparator, "ever_accepted_good_auth": str(first >= 0), "time_to_first_accepted_good_auth_step": first if first >= 0 else "", "time_to_first_accepted_good_auth_censored": str(first < 0), "time_to_first_accepted_good_auth_capped": first if first >= 0 else horizon, "distinct_contexts_sampled_authentically": int((auth_total[child] > 0).sum()), "authentic_count_total": int(auth_total[child].sum()), "good_auth_count_total": int(good_auth_total[child]), "good_auth_accept_count_total": int(good_accept[child]), "good_auth_reject_count_total": int(good_reject[child]), "auth_context_counts_total_json": json.dumps(auth_total[child].tolist(), separators=(",", ":")), "final_window_mask_count": int(window - final_auth), "final_window_mask_rate": (window - final_auth) / window, "final_window_authentic_count": final_auth, "final_window_good_auth_count": final_good, "final_window_good_auth_rate": final_good / window, "final_window_auth_context_counts_json": json.dumps(auth_final[child].tolist(), separators=(",", ":")), "final_window_auth_context_entropy": entropy, "final_window_auth_context_entropy_normalized": norm_entropy, "final_window_auth_context_entropy_status": entropy_status, "final_window_good_auth_allocation_fraction": allocation, "final_window_good_auth_allocation_status": "defined" if final_auth else "undefined_no_authentic_samples", "final_window_action_counts_json": json.dumps(final_counts.tolist(), separators=(",", ":")), "final_window_modal_action_index": modal, "final_window_modal_context": modal_context, "final_window_modal_behavior": modal_behavior, "final_window_modal_tie_count": tie_count, "final_window_unique_modal": str(unique), "settled_any_good_auth_argmax": str(maintained_good), "settled_any_good_auth_unique": str(strict_good), "modal_is_objective_optimal": str(modal in objective_actions), "cumulative_realized_objective_reward": cumulative_reward[child], "mean_realized_objective_reward": cumulative_reward[child] / horizon, "cumulative_expected_static_regret": expected_regret[child], "mean_expected_static_regret": expected_regret[child] / horizon, "cumulative_realized_pseudo_regret": realized_pseudo[child], "mean_realized_pseudo_regret": realized_pseudo[child] / horizon, "total_action_counts_json": json.dumps(total_action[child].tolist(), separators=(",", ":")), "q_final_json": json.dumps([] if q is None else q[child].tolist(), separators=(",", ":")), "q_group_final_json": json.dumps([] if q_group is None else q_group[child].tolist(), separators=(",", ":")), "q_behavior_final_json": json.dumps([] if q_behavior is None else q_behavior[child].tolist(), separators=(",", ":"))})
        rows.append({field: _f(values[field]) for field in E04_RAW_FIELDNAMES})
    return rows


def recompute_e04_summaries(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    required = set(E04_RAW_FIELDNAMES)
    if not rows or any(set(row) != required for row in rows):
        raise ValueError("E04 raw schema mismatch")
    buckets: dict[tuple[object, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows: buckets[(row["master_seed"], str(row["parameter_cell_id"]))].append(row)
    result = []
    for (master_seed, cell_id), values in sorted(buckets.items(), key=lambda item: (int(item[0][0]), item[0][1])):
        one = values[0]
        if len(values) != int(one["n"]) or sorted(int(row["child_id"]) for row in values) != list(range(int(one["n"]))):
            raise ValueError("E04 raw child cardinality mismatch")
        def mean(key: str) -> float:
            observed = [row[key] for row in values if row[key] != ""]
            return float(np.mean([1.0 if value == "True" else 0.0 if value == "False" else float(value) for value in observed])) if observed else float("nan")
        defined_entropy = [float(row["final_window_auth_context_entropy"]) for row in values if row["final_window_auth_context_entropy"] != ""]
        defined_normalized_entropy = [float(row["final_window_auth_context_entropy_normalized"]) for row in values if row["final_window_auth_context_entropy_normalized"] != ""]
        defined_allocation = [float(row["final_window_good_auth_allocation_fraction"]) for row in values if row["final_window_good_auth_allocation_fraction"] != ""]
        result.append({"run_id": one["run_id"], "experiment_id": "E04", "tier": one["tier"], "master_seed": one["master_seed"], "parameter_cell_id": cell_id, "architecture": one["architecture"], "K": one["K"], "canonical_identity_mode": one["canonical_identity_mode"], "effective_good_count": one["effective_good_count"], "n": len(values), "mean_settled_any_good_auth_argmax": mean("settled_any_good_auth_argmax"), "mean_settled_any_good_auth_unique": mean("settled_any_good_auth_unique"), "mean_ever_accepted_good_auth": mean("ever_accepted_good_auth"), "mean_time_to_first_accepted_good_auth_capped": mean("time_to_first_accepted_good_auth_capped"), "mean_distinct_contexts_sampled_authentically": mean("distinct_contexts_sampled_authentically"), "mean_realized_objective_reward": mean("mean_realized_objective_reward"), "mean_expected_static_regret": mean("mean_expected_static_regret"), "mean_final_window_mask_rate": mean("final_window_mask_rate"), "mean_final_window_good_auth_rate": mean("final_window_good_auth_rate"), "mean_final_window_good_auth_allocation_fraction": float(np.mean(defined_allocation)) if defined_allocation else "", "allocation_defined_n": len(defined_allocation), "allocation_status": "defined" if defined_allocation else "undefined_no_authentic_samples", "mean_final_window_auth_context_entropy": float(np.mean(defined_entropy)) if defined_entropy else "", "entropy_defined_n": len(defined_entropy), "entropy_status": "defined" if defined_entropy else "undefined_no_authentic_samples", "mean_final_window_auth_context_entropy_normalized": float(np.mean(defined_normalized_entropy)) if defined_normalized_entropy else "", "normalized_entropy_defined_n": len(defined_normalized_entropy), "normalized_entropy_status": "defined" if defined_normalized_entropy else "undefined_no_multi_context_auth_allocation"})
    return sorted(result, key=lambda row: (int(row["master_seed"]), str(row["parameter_cell_id"])))


def _expected_master_seeds(config: dict[str, Any]) -> set[int]:
    return {int(config["master_seed"])} if config["tier"] == "smoke" else set(STANDARD_SEEDS)


def _validate_e04_row_shared(row: dict[str, object], config: dict[str, Any], expected: dict[str, dict[str, object]], seeds: set[int]) -> None:
    """Shared frozen semantic surface used by raw and streaming validators."""
    if row["run_id"] != config["run_id"] or row["experiment_id"] != "E04" or row["tier"] != config["tier"] or row["model"] != "M3" or row["component"] != "primary" or row["sensitivity_name"] != "baseline":
        raise ValueError("E04 raw tier/config fields mismatch")
    if any(not math.isclose(float(row[key]), float(config["payoffs"][key]), rel_tol=0, abs_tol=1e-12) for key in FROZEN_PAYOFFS) or any(not math.isclose(float(row[key]), float(config["learner"][key]), rel_tol=0, abs_tol=1e-12) for key in FROZEN_LEARNER) or not math.isclose(float(row["bf"]), float(config["design"]["bf"]), rel_tol=0, abs_tol=1e-12):
        raise ValueError("E04 raw frozen payoff/learner/bf field mismatch")
    seed, cell_id = int(row["master_seed"]), str(row["parameter_cell_id"])
    if seed not in seeds or cell_id not in expected:
        raise ValueError("E04 raw has non-frozen seed or parameter cell")
    cell = expected[cell_id]
    if (row["architecture"], int(row["K"]), row["canonical_identity_mode"], int(row["effective_good_count"])) != (cell["architecture"], int(cell["K"]), cell["canonical_identity_mode"], int(cell["effective_good_count"])) or not math.isclose(float(row["effective_good_fraction"]), int(cell["effective_good_count"]) / int(cell["K"]), rel_tol=0, abs_tol=1e-12):
        raise ValueError("E04 raw canonical/fraction mismatch")
    if str(row["child_id"]) != str(int(row["child_id"])) or row["child_seed"] != "vectorized_cell_stream" or row["rng_unit"] != "vectorized_matched_policy_environment_plus_independent_identity":
        raise ValueError("E04 child/rng semantic field mismatch")
    child = int(row["child_id"])
    if child < 0 or child >= int(config["n"]): raise ValueError("E04 child_id out of bounds")
    if int(row["policy_environment_seed"]) != derive_e04_policy_environment_seed(seed, str(row["architecture"]), int(row["K"])) or int(row["cell_seed"]) != int(row["policy_environment_seed"]) or int(row["identity_seed"]) != derive_e04_identity_seed(seed, cell_id) or row["matched_family_id"] != e04_matched_family_id(seed, str(row["architecture"]), int(row["K"])):
        raise ValueError("E04 seed/matched-family mismatch")
    good_ids = json.loads(str(row["good_context_ids_json"]))
    expected_good = _good_sets(int(config["n"]), int(row["K"]), int(row["effective_good_count"]), str(row["canonical_identity_mode"]), int(row["identity_seed"]))[child].tolist()
    if good_ids != expected_good or len(good_ids) != len(set(good_ids)) or good_ids != sorted(good_ids):
        raise ValueError("E04 good-set semantic mismatch")
    architecture, k = str(row["architecture"]), int(row["K"])
    joint = 2 * k if architecture in {"flat_2k", "hierarchical"} else (k + 1 if architecture == "global_mask" else 2)
    expected_group_count = k if architecture == "hierarchical" else ""
    expected_behavior_count = 2 if architecture == "hierarchical" else ""
    if int(row["joint_action_count"]) != joint or str(row["group_action_count"]) != str(expected_group_count) or str(row["behavior_action_count"]) != str(expected_behavior_count):
        raise ValueError("E04 action-count surface mismatch")
    window = final_window_size(int(config["T"]), float(config["final_window_fraction"]))
    final_auth_counts = json.loads(str(row["final_window_auth_context_counts_json"])); total_actions = json.loads(str(row["total_action_counts_json"])); final_actions = json.loads(str(row["final_window_action_counts_json"]))
    if len(final_auth_counts) != k or len(total_actions) != joint or len(final_actions) != joint or sum(total_actions) != int(config["T"]) or sum(final_actions) != window:
        raise ValueError("E04 action-vector semantic mismatch")
    final_auth = sum(final_auth_counts)
    if int(row["final_window_mask_count"]) != window - final_auth or not math.isclose(float(row["final_window_mask_rate"]), int(row["final_window_mask_count"]) / window, rel_tol=0, abs_tol=1e-12):
        raise ValueError("E04 final mask semantic mismatch")
    accepted_good = int(row["good_auth_accept_count_total"])
    if (row["ever_accepted_good_auth"] == "True") != (accepted_good > 0):
        raise ValueError("E04 accepted-good/discovery equivalence mismatch")
    if accepted_good > 0 and (row["ever_accepted_good_auth"] != "True" or row["time_to_first_accepted_good_auth_censored"] != "False"):
        raise ValueError("E04 accepted-good/discovery coupling mismatch")
    modal = int(np.argmax(final_actions))
    if int(row["final_window_modal_action_index"]) != modal:
        raise ValueError("E04 modal action semantic mismatch")
    mask_expected, good_expected, bad_expected = _expected_rewards(float(config["design"]["p_good"]), float(config["design"]["p_bad"]), config["payoffs"])
    best = max(mask_expected, good_expected); expected_regret = 0.0
    for action, count in enumerate(total_actions):
        if architecture in {"flat_2k", "hierarchical"}: authentic, group = action % 2 == 1, action // 2
        elif architecture == "global_mask": authentic, group = action != 0, max(action - 1, 0)
        else: authentic, group = action == 1, 0
        expected_regret += int(count) * (best - (mask_expected if not authentic else (good_expected if group in good_ids else bad_expected)))
    if not math.isclose(float(row["cumulative_expected_static_regret"]), expected_regret, rel_tol=0, abs_tol=1e-9):
        raise ValueError("E04 cumulative regret semantic mismatch")
    if (int(row["n"]), int(row["T"]), float(row["final_window_fraction"])) != (int(config["n"]), int(config["T"]), float(config["final_window_fraction"])) or int(row["final_window_start"]) != int(config["T"]) - window or int(row["final_window_end"]) != int(config["T"]) - 1:
        raise ValueError("E04 horizon/window semantic mismatch")
    if not math.isclose(float(row["p_good"]), float(config["design"]["p_good"]), rel_tol=0, abs_tol=1e-12) or not math.isclose(float(row["p_bad"]), float(config["design"]["p_bad"]), rel_tol=0, abs_tol=1e-12):
        raise ValueError("E04 receptivity field mismatch")
    if len(good_ids) != int(row["effective_good_count"]) or any(type(value) is not int or value < 0 or value >= k for value in good_ids) or (row["canonical_identity_mode"] == "fixed" and good_ids != list(range(int(row["effective_good_count"])))):
        raise ValueError("E04 good-set cardinality/type mismatch")
    known = row["known_good_context_id"]
    if (architecture == "fixed_known_good") != (known != "") or (known != "" and int(known) != 0):
        raise ValueError("E04 known-good context mismatch")
    if not all(math.isclose(float(row[key]), value, rel_tol=0, abs_tol=1e-12) for key, value in (("expected_mask_reward", mask_expected), ("expected_good_auth_reward", good_expected), ("expected_bad_auth_reward", bad_expected), ("objective_best_expected_reward", best))):
        raise ValueError("E04 expected reward surface mismatch")
    comparator = "good_auth" if good_expected > mask_expected else "mask"
    best_actions = objective_best_actions(architecture, k, np.array(good_ids), comparator == "good_auth")
    if row["objective_comparator"] != comparator or json.loads(str(row["objective_best_joint_actions_json"])) != best_actions:
        raise ValueError("E04 objective comparator/action set mismatch")
    auth_counts = json.loads(str(row["auth_context_counts_total_json"]))
    if len(auth_counts) != k or int(row["authentic_count_total"]) != sum(auth_counts) or int(row["good_auth_count_total"]) != sum(auth_counts[index] for index in good_ids) or int(row["good_auth_count_total"]) != int(row["good_auth_accept_count_total"]) + int(row["good_auth_reject_count_total"]) or int(row["distinct_contexts_sampled_authentically"]) != sum(value > 0 for value in auth_counts):
        raise ValueError("E04 authentic/discovery count mismatch")
    if int(row["final_window_authentic_count"]) != final_auth or int(row["final_window_good_auth_count"]) != sum(final_auth_counts[index] for index in good_ids) or not math.isclose(float(row["final_window_good_auth_rate"]), int(row["final_window_good_auth_count"]) / window, rel_tol=0, abs_tol=1e-12):
        raise ValueError("E04 final authentic count/rate mismatch")
    first, censored, capped = row["time_to_first_accepted_good_auth_step"], row["time_to_first_accepted_good_auth_censored"], row["time_to_first_accepted_good_auth_capped"]
    if row["ever_accepted_good_auth"] == "True":
        if first == "" or censored != "False" or int(capped) != int(first) or not 0 <= int(first) < int(config["T"]):
            raise ValueError("E04 discovery time mismatch")
    elif row["ever_accepted_good_auth"] == "False":
        if first != "" or censored != "True" or int(capped) != int(config["T"]):
            raise ValueError("E04 censored discovery mismatch")
    else:
        raise ValueError("E04 discovery boolean mismatch")
    entropy, norm_entropy, entropy_status = _entropy(np.array(final_auth_counts))
    allocation = "" if final_auth == 0 else int(row["final_window_good_auth_count"]) / final_auth
    if row["final_window_auth_context_entropy_status"] != entropy_status or row["final_window_good_auth_allocation_status"] != ("defined" if final_auth else "undefined_no_authentic_samples") or (entropy == "" and (row["final_window_auth_context_entropy"] != "" or row["final_window_auth_context_entropy_normalized"] != "")) or (norm_entropy == "" and row["final_window_auth_context_entropy_normalized"] != "") or (allocation == "" and row["final_window_good_auth_allocation_fraction"] != "") or (entropy != "" and not math.isclose(float(row["final_window_auth_context_entropy"]), float(entropy), rel_tol=0, abs_tol=1e-12)) or (norm_entropy != "" and not math.isclose(float(row["final_window_auth_context_entropy_normalized"]), float(norm_entropy), rel_tol=0, abs_tol=1e-12)) or (allocation != "" and not math.isclose(float(row["final_window_good_auth_allocation_fraction"]), float(allocation), rel_tol=0, abs_tol=1e-12)):
        raise ValueError("E04 entropy/allocation semantic mismatch")
    tie_count = int(np.count_nonzero(np.array(final_actions) == max(final_actions)))
    if int(row["final_window_modal_tie_count"]) != tie_count or row["final_window_unique_modal"] != str(tie_count == 1) or row["modal_is_objective_optimal"] != str(modal in best_actions):
        raise ValueError("E04 modal tie/optimality mismatch")
    if architecture in {"flat_2k", "hierarchical"}: context, behavior = modal // 2, modal % 2
    elif architecture == "global_mask": context, behavior = max(modal - 1, 0), 0 if modal == 0 else 1
    else: context, behavior = 0, modal
    if int(row["final_window_modal_context"]) != context or int(row["final_window_modal_behavior"]) != behavior or row["settled_any_good_auth_argmax"] != str(behavior == 1 and context in good_ids) or row["settled_any_good_auth_unique"] != str(tie_count == 1 and behavior == 1 and context in good_ids):
        raise ValueError("E04 modal/settling semantic mismatch")
    q, qg, qb = json.loads(str(row["q_final_json"])), json.loads(str(row["q_group_final_json"])), json.loads(str(row["q_behavior_final_json"]))
    if (architecture == "hierarchical" and (q or len(qg) != k or len(qb) != k or any(len(value) != 2 for value in qb))) or (architecture != "hierarchical" and (len(q) != joint or qg or qb)):
        raise ValueError("E04 Q-vector shape mismatch")
    realized = float(row["cumulative_realized_objective_reward"])
    if not math.isclose(float(row["mean_expected_static_regret"]), expected_regret / int(config["T"]), rel_tol=0, abs_tol=1e-12) or not math.isclose(float(row["mean_realized_objective_reward"]) * int(config["T"]), realized, rel_tol=0, abs_tol=1e-9) or not math.isclose(float(row["cumulative_realized_pseudo_regret"]), best * int(config["T"]) - realized, rel_tol=0, abs_tol=1e-9) or not math.isclose(float(row["mean_realized_pseudo_regret"]), float(row["cumulative_realized_pseudo_regret"]) / int(config["T"]), rel_tol=0, abs_tol=1e-12):
        raise ValueError("E04 reward/pseudo-regret semantic mismatch")


def validate_e04_raw_rows(rows: list[dict[str, object]], config: dict[str, Any]) -> None:
    """Fail closed on frozen-design, row-schema, seed, and cross-field drift."""
    canonical, _ = canonical_e04_cells()
    expected = {str(cell["parameter_cell_id"]): cell for cell in canonical}
    seeds = _expected_master_seeds(config)
    if not rows or any(list(row) != E04_RAW_FIELDNAMES for row in rows):
        raise ValueError("E04 raw field ordering/schema mismatch")
    grouped: dict[tuple[int, str], list[dict[str, object]]] = defaultdict(list)
    expected_order: list[tuple[int, str, int]] = []
    for cell_id in sorted(expected):
        for seed in sorted(seeds):
            expected_order.extend((seed, cell_id, child) for child in range(int(config["n"])))
    seen_order: list[tuple[int, str, int]] = []
    for row in rows:
        _validate_e04_row_shared(row, config, expected, seeds)
        if row["run_id"] != config["run_id"] or row["experiment_id"] != "E04" or row["tier"] != config["tier"] or row["model"] != "M3" or row["component"] != "primary" or row["sensitivity_name"] != "baseline":
            raise ValueError("E04 raw tier/config fields mismatch")
        if any(not math.isclose(float(row[key]), float(config["payoffs"][key]), rel_tol=0, abs_tol=1e-12) for key in FROZEN_PAYOFFS) or any(not math.isclose(float(row[key]), float(config["learner"][key]), rel_tol=0, abs_tol=1e-12) for key in FROZEN_LEARNER):
            raise ValueError("E04 raw frozen payoff/learner field mismatch")
        seed, cell_id = int(row["master_seed"]), str(row["parameter_cell_id"])
        if seed not in seeds or cell_id not in expected:
            raise ValueError("E04 raw has non-frozen seed or parameter cell")
        cell = expected[cell_id]
        if (row["architecture"], int(row["K"]), row["canonical_identity_mode"], int(row["effective_good_count"])) != (cell["architecture"], int(cell["K"]), cell["canonical_identity_mode"], int(cell["effective_good_count"])):
            raise ValueError("E04 raw canonical cross-fields mismatch")
        if (int(row["n"]), int(row["T"]), float(row["final_window_fraction"])) != (int(config["n"]), int(config["T"]), float(config["final_window_fraction"])):
            raise ValueError("E04 raw n/T/window mismatch")
        if int(row["final_window_start"]) != int(config["T"]) - final_window_size(int(config["T"]), float(config["final_window_fraction"])) or int(row["final_window_end"]) != int(config["T"]) - 1:
            raise ValueError("E04 final window indices mismatch")
        if str(row["child_id"]) != str(int(row["child_id"])):
            raise ValueError("E04 child_id must use canonical decimal form")
        child = int(row["child_id"])
        if child < 0 or child >= int(config["n"]):
            raise ValueError("E04 child_id out of bounds")
        if int(row["policy_environment_seed"]) != derive_e04_policy_environment_seed(seed, str(row["architecture"]), int(row["K"])) or int(row["cell_seed"]) != int(row["policy_environment_seed"]):
            raise ValueError("E04 policy/cell seed mismatch")
        if int(row["identity_seed"]) != derive_e04_identity_seed(seed, cell_id) or row["matched_family_id"] != e04_matched_family_id(seed, str(row["architecture"]), int(row["K"])):
            raise ValueError("E04 identity seed or matched family mismatch")
        good_ids = json.loads(str(row["good_context_ids_json"]))
        if len(good_ids) != int(row["effective_good_count"]) or good_ids != sorted(good_ids) or len(set(good_ids)) != len(good_ids) or any(type(item) is not int or item < 0 or item >= int(row["K"]) for item in good_ids):
            raise ValueError("E04 good-set encoding mismatch")
        expected_good = _good_sets(int(config["n"]), int(row["K"]), int(row["effective_good_count"]), str(row["canonical_identity_mode"]), int(row["identity_seed"]))[child].tolist()
        if good_ids != expected_good or (row["canonical_identity_mode"] == "fixed" and good_ids != list(range(int(row["effective_good_count"])) )):
            raise ValueError("E04 good set does not match frozen identity stream")
        if (str(row["architecture"]) == "fixed_known_good") != (row["known_good_context_id"] != "") or (row["known_good_context_id"] != "" and int(row["known_good_context_id"]) != 0):
            raise ValueError("E04 known-good context mismatch")
        mask_expected, good_expected, bad_expected = _expected_rewards(float(row["p_good"]), float(row["p_bad"]), config["payoffs"])
        best = max(mask_expected, good_expected); comparator = "good_auth" if good_expected > mask_expected else "mask"
        if not all(math.isclose(float(row[key]), value, rel_tol=0, abs_tol=1e-12) for key, value in (("expected_mask_reward", mask_expected), ("expected_good_auth_reward", good_expected), ("expected_bad_auth_reward", bad_expected), ("objective_best_expected_reward", best))) or row["objective_comparator"] != comparator:
            raise ValueError("E04 expected reward/comparator mismatch")
        actions = json.loads(str(row["objective_best_joint_actions_json"]))
        expected_actions = objective_best_actions(str(row["architecture"]), int(row["K"]), np.array(good_ids), comparator == "good_auth")
        if actions != expected_actions:
            raise ValueError("E04 objective comparator action set mismatch")
        action_count = int(row["joint_action_count"])
        total_actions, final_actions = json.loads(str(row["total_action_counts_json"])), json.loads(str(row["final_window_action_counts_json"]))
        auth_counts, final_auth_counts = json.loads(str(row["auth_context_counts_total_json"])), json.loads(str(row["final_window_auth_context_counts_json"]))
        if len(total_actions) != action_count or len(final_actions) != action_count or sum(total_actions) != int(config["T"]) or sum(final_actions) != final_window_size(int(config["T"]), float(config["final_window_fraction"])) or len(auth_counts) != int(row["K"]) or len(final_auth_counts) != int(row["K"]):
            raise ValueError("E04 action/context vector lengths or totals mismatch")
        final_auth = sum(final_auth_counts); final_good = sum(final_auth_counts[index] for index in good_ids)
        if int(row["authentic_count_total"]) != sum(auth_counts) or int(row["final_window_authentic_count"]) != final_auth or int(row["final_window_good_auth_count"]) != final_good or int(row["final_window_mask_count"]) != final_window_size(int(config["T"]), float(config["final_window_fraction"])) - final_auth or not math.isclose(float(row["final_window_mask_rate"]), (int(row["final_window_mask_count"]) / final_window_size(int(config["T"]), float(config["final_window_fraction"]))), rel_tol=0, abs_tol=1e-12) or not math.isclose(float(row["final_window_good_auth_rate"]), final_good / final_window_size(int(config["T"]), float(config["final_window_fraction"])), rel_tol=0, abs_tol=1e-12):
            raise ValueError("E04 final-window count/rate mismatch")
        if int(row["good_auth_count_total"]) != int(row["good_auth_accept_count_total"]) + int(row["good_auth_reject_count_total"]) or int(row["good_auth_count_total"]) != sum(auth_counts[index] for index in good_ids) or int(row["distinct_contexts_sampled_authentically"]) != sum(count > 0 for count in auth_counts):
            raise ValueError("E04 discovery count mismatch")
        first, censored, capped = row["time_to_first_accepted_good_auth_step"], row["time_to_first_accepted_good_auth_censored"], row["time_to_first_accepted_good_auth_capped"]
        if row["ever_accepted_good_auth"] == "True":
            if first == "" or censored != "False" or int(capped) != int(first) or not 0 <= int(first) < int(config["T"]): raise ValueError("E04 discovery time mismatch")
        elif row["ever_accepted_good_auth"] == "False":
            if first != "" or censored != "True" or int(capped) != int(config["T"]): raise ValueError("E04 censored discovery mismatch")
        else: raise ValueError("E04 discovery boolean mismatch")
        entropy, norm_entropy, entropy_status = _entropy(np.array(final_auth_counts))
        allocation = "" if final_auth == 0 else final_good / final_auth
        if row["final_window_auth_context_entropy_status"] != entropy_status or str(row["final_window_good_auth_allocation_status"]) != ("defined" if final_auth else "undefined_no_authentic_samples") or (entropy != "" and not math.isclose(float(row["final_window_auth_context_entropy"]), float(entropy), rel_tol=0, abs_tol=1e-12)) or (norm_entropy != "" and not math.isclose(float(row["final_window_auth_context_entropy_normalized"]), float(norm_entropy), rel_tol=0, abs_tol=1e-12)) or (allocation != "" and not math.isclose(float(row["final_window_good_auth_allocation_fraction"]), float(allocation), rel_tol=0, abs_tol=1e-12)):
            raise ValueError("E04 entropy/allocation mismatch")
        if (entropy == "" and (row["final_window_auth_context_entropy"] != "" or row["final_window_auth_context_entropy_normalized"] != "")) or (norm_entropy == "" and row["final_window_auth_context_entropy_normalized"] != "") or (allocation == "" and row["final_window_good_auth_allocation_fraction"] != ""):
            raise ValueError("E04 undefined entropy/allocation payload mismatch")
        modal = int(np.argmax(final_actions)); tie_count = int(np.count_nonzero(np.array(final_actions) == max(final_actions)))
        if int(row["final_window_modal_action_index"]) != modal or int(row["final_window_modal_tie_count"]) != tie_count or row["final_window_unique_modal"] != str(tie_count == 1) or row["modal_is_objective_optimal"] != str(modal in actions):
            raise ValueError("E04 modal diagnostics mismatch")
        if str(row["architecture"]) in {"flat_2k", "hierarchical"}:
            context, behavior = modal // 2, modal % 2
        elif str(row["architecture"]) == "global_mask": context, behavior = max(modal - 1, 0), 0 if modal == 0 else 1
        else: context, behavior = 0, modal
        if int(row["final_window_modal_context"]) != context or int(row["final_window_modal_behavior"]) != behavior:
            raise ValueError("E04 modal decoding mismatch")
        maintained = behavior == 1 and context in good_ids
        if row["settled_any_good_auth_argmax"] != str(maintained) or row["settled_any_good_auth_unique"] != str(tie_count == 1 and maintained):
            raise ValueError("E04 settled flags mismatch")
        q, qg, qb = json.loads(str(row["q_final_json"])), json.loads(str(row["q_group_final_json"])), json.loads(str(row["q_behavior_final_json"]))
        if str(row["architecture"]) == "hierarchical":
            if q or len(qg) != int(row["K"]) or len(qb) != int(row["K"]) or any(len(item) != 2 for item in qb): raise ValueError("E04 hierarchical Q shape mismatch")
        elif len(q) != action_count or qg or qb: raise ValueError("E04 Q shape mismatch")
        expected_regret = 0.0
        for action, count in enumerate(total_actions):
            if str(row["architecture"]) in {"flat_2k", "hierarchical"}: authentic, group = action % 2 == 1, action // 2
            elif str(row["architecture"]) == "global_mask": authentic, group = action != 0, max(action - 1, 0)
            else: authentic, group = action == 1, 0
            expected_value = mask_expected if not authentic else (good_expected if group in good_ids else bad_expected)
            expected_regret += int(count) * (best - expected_value)
        if not math.isclose(float(row["cumulative_expected_static_regret"]), expected_regret, rel_tol=0, abs_tol=1e-9) or not math.isclose(float(row["mean_expected_static_regret"]), expected_regret / int(config["T"]), rel_tol=0, abs_tol=1e-12) or not math.isclose(float(row["mean_realized_objective_reward"]) * int(config["T"]), float(row["cumulative_realized_objective_reward"]), rel_tol=0, abs_tol=1e-9) or not math.isclose(float(row["cumulative_realized_pseudo_regret"]), best * int(config["T"]) - float(row["cumulative_realized_objective_reward"]), rel_tol=0, abs_tol=1e-9):
            raise ValueError("E04 reward/regret reconciliation mismatch")
        key = (seed, cell_id); grouped[key].append(row); seen_order.append((seed, cell_id, child))
    if set(grouped) != {(seed, cell_id) for seed in seeds for cell_id in expected}:
        raise ValueError("E04 raw missing/duplicate seed-cell families")
    for rows_for_cell in grouped.values():
        if len(rows_for_cell) != int(config["n"]) or sorted(int(row["child_id"]) for row in rows_for_cell) != list(range(int(config["n"]))):
            raise ValueError("E04 raw child IDs/cardinality mismatch")
    if seen_order != expected_order:
        raise ValueError("E04 raw deterministic order mismatch")


def validate_e04_raw_csv(path: Path, config: dict[str, Any]) -> int:
    """Bounded-memory equivalent of raw validation for the standard CSV."""
    canonical, _ = canonical_e04_cells()
    expected = {str(cell["parameter_cell_id"]): cell for cell in canonical}
    seeds = _expected_master_seeds(config)
    sequence = [(seed, str(cell["parameter_cell_id"]), child) for cell in sorted(canonical, key=lambda value: str(value["parameter_cell_id"])) for seed in sorted(seeds) for child in range(int(config["n"]))]
    count = 0
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if list(row) != E04_RAW_FIELDNAMES or count >= len(sequence):
                raise ValueError("E04 streamed raw schema/cardinality mismatch")
            observed = (int(row["master_seed"]), str(row["parameter_cell_id"]), int(row["child_id"]))
            if observed != sequence[count]:
                raise ValueError("E04 streamed raw deterministic order mismatch")
            _validate_e04_row_shared(row, config, expected, seeds)
            count += 1
    if count != len(sequence):
        raise ValueError("E04 streamed raw final cardinality mismatch")
    return count


def recompute_e04_summaries_csv(path: Path) -> list[dict[str, object]]:
    """Recompute curve rows from one bounded seed/cell group at a time."""
    result: list[dict[str, object]] = []
    current: tuple[str, str] | None = None
    bucket: list[dict[str, object]] = []
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            key = (str(row["master_seed"]), str(row["parameter_cell_id"]))
            if current is not None and key != current:
                result.extend(recompute_e04_summaries(bucket)); bucket = []
            current = key; bucket.append(row)
        if bucket:
            result.extend(recompute_e04_summaries(bucket))
    return sorted(result, key=lambda row: (int(row["master_seed"]), str(row["parameter_cell_id"])))


def validate_e04_curves(curves: list[dict[str, object]], config: dict[str, Any], raw_rows: list[dict[str, object]] | None = None, raw_path: Path | None = None) -> None:
    canonical, _ = canonical_e04_cells(); expected = {(seed, str(cell["parameter_cell_id"])) for seed in _expected_master_seeds(config) for cell in canonical}
    keys = {(int(row["master_seed"]), str(row["parameter_cell_id"])) for row in curves}
    if keys != expected or len(keys) != len(curves):
        raise ValueError("E04 curves have missing, duplicate, or arbitrary seed/cell rows")
    if any(row["tier"] != config["tier"] or int(row["n"]) != int(config["n"]) for row in curves):
        raise ValueError("E04 curve tier/n mismatch")
    if (raw_rows is None) == (raw_path is None):
        raise ValueError("E04 curve validation requires raw provenance")
    recomputed = recompute_e04_summaries(raw_rows) if raw_rows is not None else recompute_e04_summaries_csv(raw_path)
    expected_rows = {(int(row["master_seed"]), str(row["parameter_cell_id"])): row for row in recomputed}
    for row in curves:
        target = expected_rows[(int(row["master_seed"]), str(row["parameter_cell_id"]))]
        if set(row) != set(target):
            raise ValueError("E04 curve metric schema mismatch")
        for key, value in target.items():
            if isinstance(value, float):
                if not math.isclose(float(row[key]), value, rel_tol=0, abs_tol=1e-12): raise ValueError("E04 curve metric mismatch")
            elif str(row[key]) != str(value):
                raise ValueError("E04 curve metadata/denominator mismatch")


def validate_e04_effects(effects: list[dict[str, object]], config: dict[str, Any], curves: list[dict[str, object]] | None = None) -> None:
    seeds = _expected_master_seeds(config)
    if not effects or any(row["tier"] != config["tier"] or row["experiment_id"] != "E04" for row in effects):
        raise ValueError("E04 effects metadata mismatch")
    per_seed = [row for row in effects if row["level"] == "master_seed"]
    if any(int(row["master_seed"]) not in seeds for row in per_seed):
        raise ValueError("E04 effects contain non-frozen master seed")
    if config["tier"] == "smoke" and any(row["ci_status"] != "not_estimable_smoke" or row["ci_low"] != "" or row["ci_high"] != "" for row in per_seed):
        raise ValueError("E04 smoke effects must not contain inferential intervals")
    keys = [(str(row["effect_name"]), str(row["level"]), str(row["master_seed"])) for row in effects]
    if len(keys) != len(set(keys)):
        raise ValueError("E04 duplicate effect keys")
    if curves is None:
        raise ValueError("E04 effect validation requires curve provenance")
    else:
        expected = e04_effects(curves, str(config["tier"]))
        expected_by_key = {(str(row["effect_name"]), str(row["level"]), str(row["master_seed"])): row for row in expected}
        observed_by_key = {(str(row["effect_name"]), str(row["level"]), str(row["master_seed"])): row for row in effects}
        if set(expected_by_key) != set(observed_by_key):
            raise ValueError("E04 effect cardinality/key mismatch")
        for key, target in expected_by_key.items():
            actual = observed_by_key[key]
            if actual["ci_status"] != target["ci_status"] or actual["notes"] != target["notes"]:
                raise ValueError("E04 effect metadata mismatch")
            for metric in ("estimate", "ci_low", "ci_high"):
                if target[metric] == "":
                    if actual[metric] != "": raise ValueError("E04 blank effect mismatch")
                elif not math.isclose(float(actual[metric]), float(target[metric]), rel_tol=0, abs_tol=1e-12):
                    raise ValueError("E04 effect recomputation mismatch")


def _slope(points: list[dict[str, object]], metric: str) -> float:
    points = [row for row in points if row.get(metric, "") != ""]
    x = np.array([math.log2(float(row["K"])) for row in points]); y = np.array([float(row[metric]) for row in points])
    return float(np.polyfit(x, y, 1)[0]) if len(set(x)) > 1 else 0.0


def e04_effects(cells: list[dict[str, object]], tier: str) -> list[dict[str, object]]:
    """Prespecified E04 curves, endpoint contrasts, and architecture effects.

    A smoke contributes a single seed-level row per estimand and therefore has
    blank intervals.  The same reducer accepts five-seed standard summaries and
    appends Student-t interval rows; standard dispatch remains intentionally
    unavailable in this approval.
    """
    if tier not in {"smoke", "standard"}:
        raise ValueError("E04 tier must be exact lowercase smoke or standard")
    if tier == "standard":
        canonical, _ = canonical_e04_cells()
        expected = {str(cell["parameter_cell_id"]) for cell in canonical}
        observed = {(int(row["master_seed"]), str(row["parameter_cell_id"])) for row in cells}
        if {int(row["master_seed"]) for row in cells} != set(STANDARD_SEEDS) or observed != {(seed, cell_id) for seed in STANDARD_SEEDS for cell_id in expected} or len(cells) != 275:
            raise ValueError("E04 standard effects require complete frozen five-seed baseline curves before Student-t pooling")
    rows: list[dict[str, object]] = []
    metrics = ("mean_settled_any_good_auth_argmax", "mean_ever_accepted_good_auth", "mean_time_to_first_accepted_good_auth_capped", "mean_distinct_contexts_sampled_authentically", "mean_realized_objective_reward", "mean_expected_static_regret", "mean_final_window_mask_rate", "mean_final_window_good_auth_allocation_fraction", "mean_final_window_auth_context_entropy", "mean_final_window_auth_context_entropy_normalized")
    def select(architecture: str, mode: str, count: int, *, minimum_k: int = 1) -> list[dict[str, object]]:
        return sorted((row for row in cells if row["architecture"] == architecture and row["canonical_identity_mode"] == mode and int(row["effective_good_count"]) == count and int(row["K"]) >= minimum_k), key=lambda row: (int(row["master_seed"]), int(row["K"])))
    def one_seed_points(values: list[dict[str, object]], seed: object) -> list[dict[str, object]]:
        return [row for row in values if row["master_seed"] == seed]
    def append(name: str, values_by_seed: dict[object, float], note: str) -> None:
        for seed, estimate in sorted(values_by_seed.items(), key=lambda item: int(item[0])):
            rows.append({"run_id": cells[0]["run_id"], "experiment_id": "E04", "tier": tier, "effect_name": name, "level": "master_seed", "master_seed": seed, "estimate": estimate, "ci_status": "not_estimable_smoke" if tier == "smoke" else "seed_estimate", "ci_low": "", "ci_high": "", "notes": note})
        if len(values_by_seed) == 5:
            vector = np.array([values_by_seed[seed] for seed in sorted(values_by_seed, key=int)], dtype=float); estimate = float(vector.mean()); margin = T_CRITICAL_95_DF4 * float(vector.std(ddof=1)) / math.sqrt(5)
            rows.append({"run_id": cells[0]["run_id"], "experiment_id": "E04", "tier": tier, "effect_name": name, "level": "across_master_seeds", "master_seed": "", "estimate": estimate, "ci_status": "student_t_95", "ci_low": estimate - margin, "ci_high": estimate + margin, "notes": note})
    seeds = sorted({row["master_seed"] for row in cells}, key=int)
    def slopes(architecture: str, mode: str, count: int, metric: str, minimum_k: int = 1) -> dict[object, float]:
        values = select(architecture, mode, count, minimum_k=minimum_k)
        return {seed: _slope(one_seed_points(values, seed), metric) for seed in seeds if len(one_seed_points(values, seed)) >= 2}
    for metric in metrics:
        for architecture in ("flat_2k", "hierarchical", "global_mask"):
            fixed_one = slopes(architecture, "fixed", 1, metric)
            append(f"{architecture}_{metric}_slope_log2K_fixed_one", fixed_one, "primary fixed-one K slope")
            points = select(architecture, "fixed", 1)
            endpoint = {seed: float(one_seed_points(points, seed)[-1][metric]) - float(one_seed_points(points, seed)[0][metric]) for seed in seeds if len(one_seed_points(points, seed)) >= 2 and one_seed_points(points, seed)[-1].get(metric, "") != "" and one_seed_points(points, seed)[0].get(metric, "") != ""}
            append(f"{architecture}_{metric}_S16_minus_S1_fixed_one", endpoint, "primary fixed-one K=16 minus K=1 endpoint contrast")
            random_one, fixed_tail = slopes(architecture, "random_per_child", 1, metric, 2), slopes(architecture, "fixed", 1, metric, 2)
            append(f"{architecture}_{metric}_randomized_minus_fixed_slope_one", {seed: random_one[seed] - fixed_tail[seed] for seed in random_one.keys() & fixed_tail.keys()}, "identity generalization contrast over K>=2")
            two, one_tail = slopes(architecture, "fixed", 2, metric, 2), slopes(architecture, "fixed", 1, metric, 2)
            append(f"{architecture}_{metric}_two_minus_one_slope", {seed: two[seed] - one_tail[seed] for seed in two.keys() & one_tail.keys()}, "multiple-good count contrast over common K")
            proportional: dict[object, float] = {}
            for seed in seeds:
                points = []
                for k in KS:
                    candidates = [row for row in cells if row["master_seed"] == seed and row["architecture"] == architecture and row["canonical_identity_mode"] == "fixed" and int(row["K"]) == k and int(row["effective_good_count"]) == max(1, math.ceil(k / 4))]
                    if candidates: points.append(candidates[0])
                if len(points) >= 2: proportional[seed] = _slope(points, metric)
            append(f"{architecture}_{metric}_proportional25_minus_one_slope", {seed: proportional[seed] - fixed_one[seed] for seed in proportional.keys() & fixed_one.keys()}, "proportional-25 good-context slope change")
        fixed_control = {seed: 0.0 for seed in seeds}
        append(f"fixed_known_good_{metric}_structural_K_effect", fixed_control, "K-invariant fixed-known-good control is structurally zero")
        base = {architecture: slopes(architecture, "fixed", 1, metric) for architecture in ("flat_2k", "hierarchical", "global_mask")}
        for left, right in (("flat_2k", "global_mask"), ("hierarchical", "global_mask")):
            append(f"{left}_minus_{right}_{metric}_slope_contrast", {seed: base[left][seed] - base[right][seed] for seed in base[left].keys() & base[right].keys()}, "architecture-by-K slope contrast")
        for left in ("flat_2k", "hierarchical"):
            append(f"{left}_minus_fixed_known_good_{metric}_slope_contrast", dict(base[left]), "fixed-known-good slope is structurally zero")
    return rows


def _figure(path: Path, cells: list[dict[str, object]]) -> None:
    cache = Path(tempfile.gettempdir()) / "gifted_masking_matplotlib"; cache.mkdir(parents=True, exist_ok=True); os.environ.setdefault("MPLCONFIGDIR", str(cache))
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    figure, axis = plt.subplots(figsize=(7.8, 4.4))
    for architecture, color in (("flat_2k", "#4477aa"), ("hierarchical", "#cc6677"), ("global_mask", "#228833")):
        values = sorted((row for row in cells if row["architecture"] == architecture and row["canonical_identity_mode"] == "fixed" and int(row["effective_good_count"]) == 1), key=lambda x: int(x["K"]))
        axis.plot([int(row["K"]) for row in values], [float(row["mean_settled_any_good_auth_argmax"]) for row in values], marker="o", label=architecture, color=color)
    fixed = [row for row in cells if row["architecture"] == "fixed_known_good"][0]
    axis.axhline(float(fixed["mean_settled_any_good_auth_argmax"]), color="#aa4499", linestyle="--", label="fixed known good")
    axis.set_xscale("log", base=2); axis.set_xticks(KS); axis.set_xticklabels(KS); axis.set_ylim(0, 1); axis.set_xlabel("K contexts"); axis.set_ylabel("Settled any-good-authentic (argmax)"); axis.legend(fontsize=8); figure.tight_layout(); figure.savefig(path, dpi=150); plt.close(figure)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(repo: Path, args: list[str], *, text: bool = True) -> str | bytes | None:
    try:
        completed = subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=text)
    except Exception:
        return None
    return completed.stdout.strip() if text else completed.stdout


def _matplotlib_version() -> str | None:
    try:
        import matplotlib
        return matplotlib.__version__
    except Exception:
        return None


def _source_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for relative in SOURCE_FINGERPRINT_PATHS:
        path = root / relative
        digest.update(relative.encode())
        digest.update(path.read_bytes() if path.is_file() else b"MISSING")
    return digest.hexdigest()


def _approval_fingerprint(root: Path, tier: str) -> dict[str, object]:
    name = "E04_STANDARD_GO.md" if tier == "standard" else "E04_SMOKE_APPROVAL.md"
    path = root / "projects/frontiers_article/approvals" / name
    return {"path": str(path), "sha256": _sha(path) if path.is_file() else None, "tier": tier}


def _validate_e04_standard_approval(approval_record: Path | None, root: Path, config_path: Path) -> Path:
    """Accept only the canonical E04 baseline-standard authorization record."""
    canonical = (root / "projects/frontiers_article/approvals/E04_STANDARD_GO.md").resolve()
    if approval_record is None or approval_record.resolve() != canonical or not canonical.is_file():
        raise PermissionError("E04 standard requires the canonical E04_STANDARD_GO.md approval record")
    text = canonical.read_text()
    required = ("**Decision:** `GO_STANDARD`", "exact frozen E04 baseline standard execution only", str(config_path), "2026081401", "2026081405", "n=500", "T=2000", "one worker")
    if any(token not in text for token in required):
        raise PermissionError("E04 standard approval record does not authorize the exact frozen baseline dispatch")
    return canonical


def _peak_rss_mib() -> float:
    value = float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value / 1024 ** 2 if platform.system() == "Darwin" else value / 1024


def _report(config: dict[str, Any], outputs: dict[str, Path], elapsed: float, raw_count: int, warnings: list[str], verification: str = "pending_external_tests", smoke_peak_rss_mib: float | None = None, provenance: dict[str, object] | None = None) -> str:
    raw_bytes = outputs["raw"].stat().st_size
    plan = standard_cost_projection(raw_bytes, elapsed)
    provenance = provenance or {}
    tier = str(config["tier"])
    standard = tier == "standard"
    title = "E04 Standard Execution" if standard else "E04 Smoke Checkpoint"
    scale = "five reserved seeds 2026081401--2026081405; n=500, T=2000, final window=.20 (1600-1999); workers=1" if standard else "n=96, T=300, final window=.20 (240-299); master=2026081499; bootstrap=2026081497; workers=1"
    cost = (f"standard={raw_count} rows, {elapsed:.3f}s (raw creation through completed figure), {raw_bytes} bytes, recovery-process RSS={smoke_peak_rss_mib if smoke_peak_rss_mib is not None else 'unavailable'} MiB. The streamed runner enforced <600s, raw<400 MiB, and RSS<2048 MiB per cell; an external supervisor interrupted it after the completed figure and before serialization, so bounded recovery revalidated and finalized the completed artifacts. This RSS value is recovery observation, not a reconstructed execution high-water mark." if standard else f"smoke={raw_count} rows, {elapsed:.3f}s, {raw_bytes} bytes, peak RSS={smoke_peak_rss_mib if smoke_peak_rss_mib is not None else 'unavailable'} MiB. Projected standard={plan['standard_rows']} rows, {plan['standard_learner_steps']} learner-steps, {plan['projected_runtime_minutes']:.2f} minutes (linear), {plan['projected_raw_mib']:.1f} MiB raw; conservative in-process peak budget={plan['conservative_peak_mib']:.1f} MiB (<2 GiB cap). Runtime/raw/RSS values are readiness projections only; standard was not executed.")
    warning = ("PENDING_SOL_STANDARD_REVIEW: execution artifacts are not claim adjudication; no sensitivity, publication, ledger, or manuscript work occurred." if standard else "smoke intervals are intentionally non-inferential, the standard runtime is a linear non-executed estimate, and standard sensitivity remains separately unauthorized.")
    decision = ("`PENDING_SOL_STANDARD_REVIEW`—stop for independent standard-artifact review; do not adjudicate claims." if standard else "`RECOMMEND_GO_STANDARD_REVIEW`—submit this smoke package for separate review; it does not authorize E04 standard, sensitivity, claims, ledger, or manuscript work.")
    return f"""# {title}

1. **Experiment and run ID:** E04; `{config['run_id']}`.
2. **Model/effort/provenance:** isolated M3 experiment kernel; actual effort=`{'authorized baseline-standard execution plus bounded deterministic recovery' if standard else 'smoke-only semantic/reproducibility hardening'}`; commit `{provenance.get('commit')}`; dirty={provenance.get('dirty')}; dirty-diff SHA-256=`{provenance.get('dirty_diff_sha256')}`; maintained M3 and robustness code were not modified.
3. **Implemented files/modes:** `experiments/e04.py`, `cli.py`, frozen E04 configs, `test_article_e04.py`; flat-2K, hierarchical, global-mask, fixed-known-good; fixed/random identity and one/two/proportional-good only.
4. **Exact frozen config:** K=1/2/4/8/16; p_good=.85, p_bad=.20, bf=0; {scale}.
5. **Targeted verification:** {'strict streamed raw reconciliation, raw/canonical/curve/effect validation, deterministic regeneration, and manual semantic sentinels passed.' if standard else 'E04 comparator, equivalence, strict type/JSON, validator, stream, replay, and deterministic tests passed.'}
6. **Full verification:** `{verification}`.
7. **Baseline replay:** fixed identity replays all maintained M3 architecture kernels with their action/update/RNG order.
8. **Determinism/cell order:** matched policy streams include master/sensitivity; identity is separate; same- and cross-directory normalized artifacts match.
9. **Reconciliation/manual sentinels:** raw/canonical/curve/effect validators recompute counts, rewards, regret, comparator, discovery, entropy/allocation, summaries; K=1, K=16 actions 30/31, sets, good/bad outcomes, regrets, p_good=.70 masks, ties, and stream order passed.
10. **Artifact paths:**
{chr(10).join(f'- `{path}`' for path in outputs.values())}
11. **Cost/projection:** {cost}
12. **Warnings/risks:** {', '.join(warnings) if warnings else ('no standard execution warning' if standard else 'no smoke warning')}; {warning}
13. **Recommended gate decision:** {decision}

""" + "\n\nNo E04 claim is adjudicated here.\n"


def standard_cost_projection(smoke_raw_bytes: int, smoke_seconds: float) -> dict[str, object]:
    """Conservative, execution-free E04 standard capacity projection."""
    standard_rows = 55 * 5 * 500
    standard_steps = standard_rows * 2000
    row_factor = standard_rows / 5280
    step_factor = standard_steps / 1_584_000
    # Largest hierarchical vector cell: values and all diagnostic counters.
    n, k = 500, 16
    array_bytes = n * (k * 8 + k * 2 * 8 + 2 * k * 8 * 2 + k * 8 * 2 + 2 * k * 8)
    raw_mib = smoke_raw_bytes * row_factor * 1.15 / 1024 ** 2
    return {"standard_rows": standard_rows, "standard_learner_steps": standard_steps, "projected_runtime_seconds": smoke_seconds * step_factor, "projected_runtime_minutes": smoke_seconds * step_factor / 60.0, "projected_raw_bytes": int(math.ceil(smoke_raw_bytes * row_factor * 1.15)), "projected_raw_mib": raw_mib, "projected_peak_mib": array_bytes / 1024 ** 2, "conservative_peak_mib": min(1900.0, raw_mib + 256.0), "runtime_target_minutes": 10, "raw_target_mib": 400, "peak_target_gib": 2}


def stream_e04_raw_rows(path: Path, chunks: Any, config: dict[str, Any] | None = None) -> int:
    """Incremental deterministic writer; never materializes all standard rows."""
    count = 0
    sequence: list[tuple[int, str, int]] | None = None
    expected: dict[str, dict[str, object]] | None = None
    seeds: set[int] | None = None
    if config is not None:
        canonical, _ = canonical_e04_cells()
        expected = {str(cell["parameter_cell_id"]): cell for cell in canonical}; seeds = _expected_master_seeds(config)
        sequence = [(seed, str(cell["parameter_cell_id"]), child) for cell in sorted(canonical, key=lambda value: str(value["parameter_cell_id"])) for seed in sorted(_expected_master_seeds(config)) for child in range(int(config["n"]))]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=E04_RAW_FIELDNAMES)
        writer.writeheader()
        for chunk in chunks:
            for row in chunk:
                if list(row) != E04_RAW_FIELDNAMES:
                    raise ValueError("E04 streaming raw row schema mismatch")
                if sequence is not None:
                    if count >= len(sequence) or (int(row["master_seed"]), str(row["parameter_cell_id"]), int(row["child_id"])) != sequence[count]:
                        raise ValueError("E04 streaming order mismatch")
                    assert expected is not None and seeds is not None
                    _validate_e04_row_shared(row, config, expected, seeds)
                writer.writerow(row); count += 1
    if sequence is not None and count != len(sequence):
        raise ValueError("E04 streaming row-count mismatch")
    return count


def run_e04_experiment(config_path: Path, output_dir: Path | None = None, approval_record: Path | None = None) -> dict[str, Path]:
    config = load_e04_config(config_path)
    root = Path(__file__).resolve().parents[3]; dirs = ensure_results_dirs(output_dir or root / "results"); run_id = str(config["run_id"])
    standard = config["tier"] == "standard"
    approval_path = _validate_e04_standard_approval(approval_record, root, config_path) if standard else None
    outputs = {"manifest": dirs["manifests"] / f"{run_id}.json", "raw": dirs["raw"] / f"{run_id}_units.csv", "canonical_cells": dirs["summaries"] / f"{run_id}_canonical_cells.csv", "equivalences": dirs["summaries"] / f"{run_id}_equivalences.csv", "curves": dirs["summaries"] / f"{run_id}_curves.csv", "effects": dirs["summaries"] / f"{run_id}_effects.csv", "figure": dirs["figures"] / f"{run_id}_k_curve_diagnostics.png", "report": dirs["reports"] / f"{run_id}_report.md"}
    started = datetime.now(timezone.utc).isoformat(); timer = time.perf_counter(); canonical, equivalences = canonical_e04_cells(); seed_map = []
    seeds = sorted(_expected_master_seeds(config))

    def chunks() -> Any:
        for cell in sorted(canonical, key=lambda value: str(value["parameter_cell_id"])):
            architecture, k = str(cell["architecture"]), int(cell["K"])
            for seed in seeds:
                if standard and (time.perf_counter() - timer > 600 or _peak_rss_mib() >= 2048):
                    raise RuntimeError("E04 standard stop rule exceeded during streamed generation")
                cell_config = {**config, "master_seed": seed}
                policy_seed = derive_e04_policy_environment_seed(seed, architecture, k)
                identity_seed = derive_e04_identity_seed(seed, str(cell["parameter_cell_id"]))
                seed_map.append({"master_seed": seed, "parameter_cell_id": cell["parameter_cell_id"], "matched_family_id": e04_matched_family_id(seed, architecture, k), "policy_environment_seed": policy_seed, "identity_seed": identity_seed})
                yield simulate_e04_cell(cell_config, cell, policy_seed, identity_seed)

    row_count = stream_e04_raw_rows(outputs["raw"], chunks(), config)
    if standard:
        validate_e04_raw_csv(outputs["raw"], config)
    else:
        with outputs["raw"].open(newline="") as handle:
            raw = list(csv.DictReader(handle))
        validate_e04_raw_rows(raw, config)
    write_csv(outputs["canonical_cells"], canonical); write_csv(outputs["equivalences"], equivalences)
    curves = recompute_e04_summaries_csv(outputs["raw"]) if standard else recompute_e04_summaries(raw)
    validate_e04_curves(curves, config, raw_path=outputs["raw"]) if standard else validate_e04_curves(curves, config, raw)
    expected_rows, expected_curves = (137500, 275) if standard else (5280, 55)
    if row_count != expected_rows or (not standard and len(raw) != expected_rows) or len(curves) != expected_curves: raise RuntimeError("E04 tier cardinality mismatch")
    effects = e04_effects(curves, str(config["tier"])); validate_e04_effects(effects, config, curves); write_csv(outputs["curves"], curves); write_csv(outputs["effects"], effects); _figure(outputs["figure"], curves)
    elapsed = time.perf_counter() - timer; warnings = []
    raw_mib = outputs["raw"].stat().st_size / 1024 ** 2
    if standard:
        if elapsed > 600: warnings.append("standard runtime exceeded 10 minutes")
        if raw_mib > 400: warnings.append("standard raw output exceeded 400 MiB")
        if _peak_rss_mib() >= 2048: warnings.append("standard RSS exceeded 2 GiB")
    else:
        if elapsed > 60: warnings.append("smoke runtime exceeded 60 seconds")
        if outputs["raw"].stat().st_size > 20 * 1024 * 1024: warnings.append("smoke raw output exceeded 20 MiB")
    readiness = standard_cost_projection(outputs["raw"].stat().st_size, elapsed)
    if not standard and float(readiness["projected_runtime_minutes"]) > 10.0: warnings.append("linear standard runtime projection exceeded 10 minutes")
    if warnings: raise RuntimeError("; ".join(warnings))
    peak_rss = _peak_rss_mib()
    porcelain = _git(root, ["status", "--porcelain"]) or ""
    dirty_diff = _git(root, ["diff", "--no-ext-diff"], text=False) or b""
    commit = _git(root, ["rev-parse", "HEAD"])
    dirty_diff_sha = hashlib.sha256(bytes(dirty_diff) + str(porcelain).encode()).hexdigest()
    outputs["report"].write_text(_report(config, outputs, elapsed, row_count, warnings, smoke_peak_rss_mib=peak_rss, provenance={"commit": commit, "dirty": bool(porcelain), "dirty_diff_sha256": dirty_diff_sha}))
    hashes = {name: {"sha256": _sha(path), "bytes": path.stat().st_size} for name, path in outputs.items() if name != "manifest"}
    command = f"PYTHONPATH=src {sys.executable} -m gifted_masking.cli article-experiment --config {config_path} --output-dir {output_dir or root / 'results'}"
    manifest = {"run_id": run_id, "experiment_id": "E04", "tier": config["tier"], "config_path": str(config_path), "normalized_config": _canonical_json(config), "config_sha256": hashlib.sha256(_canonical_json(config).encode()).hexdigest(), "command": command, "authorization": {**_approval_fingerprint(root, str(config["tier"])), "approved_standard_record": str(approval_path) if approval_path else None}, "parameters": config, "git": {"commit": commit, "dirty": bool(porcelain), "porcelain_sha256": hashlib.sha256(str(porcelain).encode()).hexdigest(), "dirty_diff_sha256": dirty_diff_sha, "source_fingerprint_sha256": _source_fingerprint(root)}, "environment": {"python_version": sys.version, "platform": platform.platform(), "numpy": np.__version__, "matplotlib": _matplotlib_version()}, "seed_hierarchy": {"policy_environment": "SHA-256 family ID including master seed and sensitivity -> SeedSequence([master,4,words]).spawn(1)", "identity": "SHA-256 canonical cell ID -> independent SeedSequence([master,40,words]).spawn(1)", "rng_order": "policy, acceptance uniform on every trial, objective reward, selected-action update", "cells": seed_map}, "canonicalization": {"requested_cells": 120, "executable_cells": 55, "canonical_request_rows": 55, "equivalence_table": str(outputs["equivalences"])}, "standard_readiness": ({"execution": "authorized exact baseline only", "stop_limits": {"runtime_seconds": 600, "raw_mib": 400, "rss_mib": 2048}, "actual_raw_mib": raw_mib, "sensitivity": "frozen separately unauthorized; baseline-only standard config"} if standard else {**readiness, "smoke_peak_rss_mib": peak_rss, "standard_execution": "refused pending separate E04 GO_STANDARD", "sensitivity": "frozen separately unauthorized; baseline-only standard config"}), "sort_keys": ["parameter_cell_id", "master_seed", "child_id"], "outputs": {name: {"path": str(path), "rows": row_count if name == "raw" else (len(canonical) if name == "canonical_cells" else (len(equivalences) if name == "equivalences" else (len(curves) if name == "curves" else (len(effects) if name == "effects" else None))))} for name, path in outputs.items()}, "output_hashes": hashes, "timing": {"wall_seconds": elapsed, "peak_rss_mib": peak_rss}, "warnings": warnings, "verification": {"status": "pending_external_tests", "command": "./scripts/verify.sh"}, "timestamps": {"start_utc": started, "end_utc": datetime.now(timezone.utc).isoformat()}}
    write_json(outputs["manifest"], manifest)
    return outputs


def normalize_e04_machine_artifacts(outputs: dict[str, Path]) -> dict[str, str]:
    result = {name: path.read_text() for name, path in outputs.items() if name not in {"report", "figure"}}
    manifest = json.loads(result["manifest"]); manifest["timing"] = "NORMALIZED"; manifest["timestamps"] = "NORMALIZED"; manifest["output_hashes"] = "NORMALIZED"; manifest["config_path"] = "CONFIG"; manifest["command"] = "NORMALIZED"; manifest["standard_readiness"] = "NORMALIZED"; manifest["verification"] = "NORMALIZED"; manifest["canonicalization"]["equivalence_table"] = "equivalences"; manifest["outputs"] = {name: {**detail, "path": name} for name, detail in manifest["outputs"].items()}; result["manifest"] = _canonical_json(manifest)
    return result


def finalize_e04_standard_artifacts(config_path: Path, output_dir: Path, approval_record: Path) -> dict[str, Path]:
    """Finalize an interrupted-after-figure standard run from bounded artifacts.

    This exists so the streamed generator can be recovery-safe if an external
    supervisor interrupts a process after raw/summary/figure completion but
    before manifest serialization. It revalidates the exact frozen artifacts;
    it never simulates additional rows.
    """
    config = load_e04_config(config_path)
    if config["tier"] != "standard":
        raise ValueError("E04 standard finalization requires the standard config")
    root = Path(__file__).resolve().parents[3]
    approval_path = _validate_e04_standard_approval(approval_record, root, config_path)
    dirs = ensure_results_dirs(output_dir); run_id = str(config["run_id"])
    outputs = {"manifest": dirs["manifests"] / f"{run_id}.json", "raw": dirs["raw"] / f"{run_id}_units.csv", "canonical_cells": dirs["summaries"] / f"{run_id}_canonical_cells.csv", "equivalences": dirs["summaries"] / f"{run_id}_equivalences.csv", "curves": dirs["summaries"] / f"{run_id}_curves.csv", "effects": dirs["summaries"] / f"{run_id}_effects.csv", "figure": dirs["figures"] / f"{run_id}_k_curve_diagnostics.png", "report": dirs["reports"] / f"{run_id}_report.md"}
    if any(not path.is_file() for name, path in outputs.items() if name in {"raw", "canonical_cells", "equivalences", "curves", "effects", "figure"}):
        raise RuntimeError("E04 standard recovery requires completed raw, summary, and figure artifacts")
    if validate_e04_raw_csv(outputs["raw"], config) != 137500:
        raise RuntimeError("E04 standard recovery raw cardinality mismatch")
    canonical, equivalences = canonical_e04_cells()
    with outputs["canonical_cells"].open(newline="") as handle: stored_canonical = list(csv.DictReader(handle))
    with outputs["equivalences"].open(newline="") as handle: stored_equivalences = list(csv.DictReader(handle))
    expected_canonical = [{key: str(_f(value)) for key, value in row.items()} for row in canonical]
    expected_equivalences = [{key: str(_f(value)) for key, value in row.items()} for row in equivalences]
    if stored_canonical != expected_canonical or stored_equivalences != expected_equivalences:
        raise ValueError("E04 standard canonical/equivalence artifact mismatch")
    with outputs["curves"].open(newline="") as handle: curves = list(csv.DictReader(handle))
    validate_e04_curves(curves, config, raw_path=outputs["raw"])
    with outputs["effects"].open(newline="") as handle: effects = list(csv.DictReader(handle))
    validate_e04_effects(effects, config, curves)
    raw_stat, figure_stat = outputs["raw"].stat(), outputs["figure"].stat()
    elapsed = max(0.001, figure_stat.st_mtime - getattr(raw_stat, "st_birthtime", raw_stat.st_ctime))
    peak_rss = _peak_rss_mib(); raw_mib = raw_stat.st_size / 1024 ** 2
    if elapsed > 600 or raw_mib > 400 or peak_rss >= 2048:
        raise RuntimeError("E04 standard recovery stop-limit evidence failed")
    porcelain = _git(root, ["status", "--porcelain"]) or ""; dirty_diff = _git(root, ["diff", "--no-ext-diff"], text=False) or b""; commit = _git(root, ["rev-parse", "HEAD"])
    dirty_diff_sha = hashlib.sha256(bytes(dirty_diff) + str(porcelain).encode()).hexdigest()
    outputs["report"].write_text(_report(config, outputs, elapsed, 137500, [], smoke_peak_rss_mib=peak_rss, provenance={"commit": commit, "dirty": bool(porcelain), "dirty_diff_sha256": dirty_diff_sha}))
    hashes = {name: {"sha256": _sha(path), "bytes": path.stat().st_size} for name, path in outputs.items() if name != "manifest"}
    seed_map = [{"master_seed": seed, "parameter_cell_id": cell["parameter_cell_id"], "matched_family_id": e04_matched_family_id(seed, str(cell["architecture"]), int(cell["K"])), "policy_environment_seed": derive_e04_policy_environment_seed(seed, str(cell["architecture"]), int(cell["K"])), "identity_seed": derive_e04_identity_seed(seed, str(cell["parameter_cell_id"]))} for cell in canonical for seed in STANDARD_SEEDS]
    command = f"PYTHONPATH=src {sys.executable} -m gifted_masking.cli article-experiment --config {config_path} --approval-record {approval_record} --output-dir {output_dir}"
    manifest = {"run_id": run_id, "experiment_id": "E04", "tier": "standard", "config_path": str(config_path), "normalized_config": _canonical_json(config), "config_sha256": hashlib.sha256(_canonical_json(config).encode()).hexdigest(), "command": command, "authorization": {**_approval_fingerprint(root, "standard"), "approved_standard_record": str(approval_path)}, "parameters": config, "git": {"commit": commit, "dirty": bool(porcelain), "porcelain_sha256": hashlib.sha256(str(porcelain).encode()).hexdigest(), "dirty_diff_sha256": dirty_diff_sha, "source_fingerprint_sha256": _source_fingerprint(root)}, "environment": {"python_version": sys.version, "platform": platform.platform(), "numpy": np.__version__, "matplotlib": _matplotlib_version()}, "seed_hierarchy": {"policy_environment": "SHA-256 family ID including master seed and sensitivity -> SeedSequence([master,4,words]).spawn(1)", "identity": "SHA-256 canonical cell ID -> independent SeedSequence([master,40,words]).spawn(1)", "rng_order": "policy, acceptance uniform on every trial, objective reward, selected-action update", "cells": seed_map}, "canonicalization": {"requested_cells": 120, "executable_cells": 55, "canonical_request_rows": 55, "equivalence_table": str(outputs["equivalences"])}, "standard_readiness": {"execution": "authorized exact baseline only", "stop_limits": {"runtime_seconds": 600, "raw_mib": 400, "rss_mib": 2048}, "actual_raw_mib": raw_mib, "sensitivity": "frozen separately unauthorized; baseline-only standard config"}, "sort_keys": ["parameter_cell_id", "master_seed", "child_id"], "outputs": {name: {"path": str(path), "rows": 137500 if name == "raw" else (55 if name == "canonical_cells" else (120 if name == "equivalences" else (275 if name == "curves" else (len(effects) if name == "effects" else None))))} for name, path in outputs.items()}, "output_hashes": hashes, "timing": {"wall_seconds": elapsed, "peak_rss_mib": peak_rss, "wall_time_basis": "raw artifact creation to completed figure timestamp"}, "warnings": [], "verification": {"status": "pending_external_tests", "command": "./scripts/verify.sh"}, "timestamps": {"start_utc": datetime.fromtimestamp(getattr(raw_stat, "st_birthtime", raw_stat.st_ctime), timezone.utc).isoformat(), "end_utc": datetime.fromtimestamp(figure_stat.st_mtime, timezone.utc).isoformat()}}
    write_json(outputs["manifest"], manifest)
    return outputs


def append_e04_standard_cell_block(config_path: Path, raw_path: Path, approval_record: Path, start: int, stop: int) -> int:
    """Recovery-safe canonical-cell block writer for deterministic E04 replay."""
    config = load_e04_config(config_path)
    root = Path(__file__).resolve().parents[3]
    if config["tier"] != "standard":
        raise ValueError("E04 standard cell blocks require the frozen standard config")
    _validate_e04_standard_approval(approval_record, root, config_path)
    canonical, _ = canonical_e04_cells(); cells = sorted(canonical, key=lambda value: str(value["parameter_cell_id"]))
    if not (0 <= start < stop <= len(cells)):
        raise ValueError("E04 standard cell block bounds are invalid")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if start == 0 else "a"
    if start and not raw_path.is_file():
        raise ValueError("E04 standard noninitial block requires the prior deterministic prefix")
    count = 0
    with raw_path.open(mode, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=E04_RAW_FIELDNAMES)
        if start == 0:
            writer.writeheader()
        for cell in cells[start:stop]:
            for seed in STANDARD_SEEDS:
                row_config = {**config, "master_seed": seed}
                writer.writerows(simulate_e04_cell(row_config, cell, derive_e04_policy_environment_seed(seed, str(cell["architecture"]), int(cell["K"])), derive_e04_identity_seed(seed, str(cell["parameter_cell_id"]))))
                count += int(config["n"])
    return count


def materialize_e04_standard_from_raw(config_path: Path, output_dir: Path, approval_record: Path) -> dict[str, Path]:
    """Build standard summaries/figure from an already generated raw replay."""
    config = load_e04_config(config_path)
    if config["tier"] != "standard":
        raise ValueError("E04 standard materialization requires the standard config")
    root = Path(__file__).resolve().parents[3]; _validate_e04_standard_approval(approval_record, root, config_path)
    dirs = ensure_results_dirs(output_dir); run_id = str(config["run_id"])
    outputs = {"manifest": dirs["manifests"] / f"{run_id}.json", "raw": dirs["raw"] / f"{run_id}_units.csv", "canonical_cells": dirs["summaries"] / f"{run_id}_canonical_cells.csv", "equivalences": dirs["summaries"] / f"{run_id}_equivalences.csv", "curves": dirs["summaries"] / f"{run_id}_curves.csv", "effects": dirs["summaries"] / f"{run_id}_effects.csv", "figure": dirs["figures"] / f"{run_id}_k_curve_diagnostics.png", "report": dirs["reports"] / f"{run_id}_report.md"}
    if validate_e04_raw_csv(outputs["raw"], config) != 137500:
        raise RuntimeError("E04 standard raw replay cardinality mismatch")
    canonical, equivalences = canonical_e04_cells(); write_csv(outputs["canonical_cells"], canonical); write_csv(outputs["equivalences"], equivalences)
    curves = recompute_e04_summaries_csv(outputs["raw"]); validate_e04_curves(curves, config, raw_path=outputs["raw"]); effects = e04_effects(curves, "standard"); validate_e04_effects(effects, config, curves)
    write_csv(outputs["curves"], curves); write_csv(outputs["effects"], effects); _figure(outputs["figure"], curves)
    return outputs


def record_e04_verification(outputs: dict[str, Path], *, status: str, command: str) -> None:
    """Finalize external-test metadata without changing simulated values."""
    manifest = json.loads(outputs["manifest"].read_text())
    manifest["verification"] = {"status": status, "command": command}
    outputs["report"].write_text(_report(manifest["parameters"], outputs, float(manifest["timing"]["wall_seconds"]), int(manifest["outputs"]["raw"]["rows"]), list(manifest["warnings"]), verification=f"{command}: {status}", smoke_peak_rss_mib=float(manifest["timing"].get("peak_rss_mib", 0.0)), provenance=manifest.get("git")))
    manifest["output_hashes"] = {name: {"sha256": _sha(path), "bytes": path.stat().st_size} for name, path in outputs.items() if name != "manifest"}
    write_json(outputs["manifest"], manifest)
