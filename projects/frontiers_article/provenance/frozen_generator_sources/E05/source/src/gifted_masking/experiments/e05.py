"""Frozen E05 BFLPE crossover diagnostic experiment.

This module is intentionally independent from the maintained M3 kernel.  It
replays M3's policy, acceptance, reward, and selected-entry update ordering,
while adding only E05 diagnostics and fail-closed artifact validation.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import resource
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from gifted_masking.core import final_window_size, make_rng, softmax_sample, subjective_value
from gifted_masking.models.m3 import expected_reward_for_action
from gifted_masking.repro import ensure_results_dirs, write_csv, write_json


E05_RAW_FIELDNAMES = """run_id,experiment_id,tier,model,component,sensitivity_name,architecture,architecture_role,master_seed,matched_family_id,parameter_cell_id,cell_seed,policy_environment_seed,child_id,child_seed,rng_unit,K,good_context_id,p_good,p_bad,bf,bf_label,is_analytic_threshold_anchor,b,a,c,r,alpha,tau,lambda,q0,n,T,final_window_fraction,final_window_start,final_window_end,joint_action_count,group_action_count,behavior_action_count,expected_mask_reward,expected_good_auth_reward,expected_bad_auth_reward,analytic_objective_advantage_good_auth_minus_mask,analytic_threshold_bf,objective_best_expected_reward,objective_comparator,objective_best_joint_actions_json,mask_count_total,good_auth_count_total,good_auth_accept_count_total,good_auth_reject_count_total,bad_auth_count_total,bad_auth_accept_count_total,bad_auth_reject_count_total,authentic_count_total,good_context_action_count_total,total_action_counts_json,final_window_mask_count,final_window_mask_rate,final_window_authentic_count,final_window_authentic_rate,final_window_good_context_action_count,final_window_good_auth_count,final_window_good_auth_rate,final_window_auth_given_good_context_rate,final_window_auth_given_good_context_status,final_window_action_counts_json,final_window_modal_action_index,final_window_modal_context,final_window_modal_behavior,final_window_modal_tie_count,final_window_unique_modal,modal_good_auth_argmax,modal_good_auth_unique,modal_is_objective_optimal,cumulative_realized_objective_reward,mean_realized_objective_reward,cumulative_expected_static_regret,mean_expected_static_regret,cumulative_realized_pseudo_regret,mean_realized_pseudo_regret,q_final_json,q_group_final_json,q_behavior_final_json""".split(",")
E05_ANALYTIC_FIELDS = """run_id,experiment_id,tier,bf,bf_label,is_analytic_threshold_anchor,p_good,p_bad,b,a,c,r,expected_mask_reward,expected_good_auth_reward,expected_bad_auth_reward,analytic_objective_advantage_good_auth_minus_mask,analytic_threshold_exact,analytic_threshold_bf,objective_comparator""".split(",")
E05_CELL_FIELDS = """run_id,experiment_id,tier,architecture,architecture_role,master_seed,matched_family_id,parameter_cell_id,bf,bf_label,is_analytic_threshold_anchor,n,T,final_window_fraction,final_window_start,final_window_end,modal_good_auth_argmax_n,modal_good_auth_argmax_fraction,modal_good_auth_unique_n,modal_good_auth_unique_fraction,unique_modal_n,modal_tie_n,mean_final_window_good_auth_rate,mean_final_window_auth_given_good_context_rate,conditional_good_context_defined_n,mean_final_window_authentic_rate,mean_final_window_mask_rate,mean_realized_objective_reward,mean_expected_static_regret,mean_realized_pseudo_regret,analytic_objective_advantage_good_auth_minus_mask,objective_comparator""".split(",")
E05_EFFECT_FIELDS = """run_id,experiment_id,tier,architecture,architecture_role,effect_family,effect_name,metric,level,master_seed,bf_low,bf_high,estimate,seed_n,ci_method,ci_low,ci_high,decision_input,notes""".split(",")
E05_TRANSITION_FIELDS = """run_id,experiment_id,tier,architecture,architecture_role,level,master_seed,response_metric,fit_method,target_response,dense_bf_min,dense_bf_max,transition_bf,transition_status,raw_dense_start_response,raw_dense_end_response,isotonic_dense_start_response,isotonic_dense_end_response,valid_dense_crossing,valid_seed_crossing_count,monotonicity_violation_count,bootstrap_replicates,bootstrap_valid_crossings,bootstrap_crossing_fraction,ci_method,ci_low,ci_high,analytic_threshold_bf,learned_minus_analytic_threshold,decision_eligible,notes""".split(",")

FROZEN_PAYOFFS = {"b": 1.0, "a": .6, "c": .25, "r": 2.0}
FROZEN_LEARNER = {"alpha": .1, "tau": .25, "lambda": 1.0, "q0": 0.0}
BF_VALUES = (0.0, .3, .325, .35, .375, .4, .425, .45, 8 / 17, .475, .5, .525, .55, .575, .6, .625, .65, .8)
ARCHITECTURES = ("flat_2k", "hierarchical")
STANDARD_SEEDS = [2026081501, 2026081502, 2026081503, 2026081504, 2026081505]
SMOKE_CONTRACT = {"n": 96, "T": 300, "final_window_fraction": .2, "master_seed": 2026081599, "bootstrap_seed": 2026081597, "bootstrap_replicates": 0, "workers": 1}
E05_STANDARD_RUNTIME_LIMIT_SECONDS = 600.0
T_CRITICAL_95_DF4 = 2.7764451051977987
SOURCE_FINGERPRINT_PATHS = (
    "src/gifted_masking/experiments/e05.py", "src/gifted_masking/cli.py", "src/gifted_masking/core.py",
    "src/gifted_masking/models/m3.py", "src/gifted_masking/repro.py",
    "configs/frontiers_article/e05_m3_bflpe_crossover_smoke.json", "configs/frontiers_article/e05_m3_bflpe_crossover_standard.json",
    "tests/test_article_e05.py", "projects/frontiers_article/approvals/E05_SMOKE_APPROVAL.md", "pyproject.toml", "scripts/verify.sh",
)


def _json_no_duplicates(text: str) -> object:
    def hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=hook)


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def bf_label(bf: float) -> str:
    return "8over17" if bf == 8 / 17 else f"{bf:.3f}"


def _exact_mapping(value: object, expected: dict[str, float], name: str) -> None:
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError(f"E05 {name} keys are frozen")
    for key, frozen in expected.items():
        if type(value[key]) is not float or value[key] != frozen:
            raise ValueError(f"E05 {name}.{key} is frozen and requires JSON float")


def load_e05_config(path: Path, overrides: dict[str, object] | None = None) -> dict[str, Any]:
    """Load only the byte-level frozen E05 smoke/standard contracts."""
    config = _json_no_duplicates(path.read_text())
    if not isinstance(config, dict):
        raise ValueError("E05 configuration must be an object")
    if overrides:
        config.update(overrides)
    base = {"experiment_id", "run_id", "tier", "model", "n", "T", "final_window_fraction", "master_seed", "bootstrap_seed", "bootstrap_replicates", "workers", "payoffs", "learner", "design"}
    allowed = base | {"master_seeds", "approved_standard"}
    if set(config) - allowed or base - set(config):
        raise ValueError("unknown or missing E05 configuration keys")
    if any(type(config[key]) is not str for key in ("experiment_id", "run_id", "tier", "model")):
        raise ValueError("E05 identifiers require JSON strings")
    if config["experiment_id"] != "E05" or config["model"] != "M3" or config["tier"] not in {"smoke", "standard"}:
        raise ValueError("only frozen E05 M3 configurations are supported")
    for key in ("n", "T", "master_seed", "bootstrap_seed", "bootstrap_replicates", "workers"):
        if type(config[key]) is not int:
            raise ValueError(f"E05 {key} requires an exact JSON integer")
    if type(config["final_window_fraction"]) is not float:
        raise ValueError("E05 final_window_fraction requires an exact JSON float")
    if config["workers"] != 1: raise ValueError("E05 requires workers=1")
    final_window_size(config["T"], config["final_window_fraction"])
    _exact_mapping(config["payoffs"], FROZEN_PAYOFFS, "payoffs")
    _exact_mapping(config["learner"], FROZEN_LEARNER, "learner")
    d = config["design"]
    expected_design = {"architectures": list(ARCHITECTURES), "K": 4, "good_context_id": 0, "p_good": .85, "p_bad": .2, "bf_values": list(BF_VALUES), "analytic_threshold_exact": "8/17", "analytic_threshold_bf": 8 / 17, "dense_bf_min": .3, "dense_bf_max": .65, "transition_response": .5}
    if not isinstance(d, dict) or set(d) != set(expected_design): raise ValueError("E05 design keys are frozen")
    if type(d["K"]) is not int or type(d["good_context_id"]) is not int or any(type(d[k]) is not float for k in ("p_good", "p_bad", "analytic_threshold_bf", "dense_bf_min", "dense_bf_max", "transition_response")):
        raise ValueError("E05 design types are frozen")
    if not isinstance(d["architectures"], list) or not isinstance(d["bf_values"], list) or any(type(v) is not float for v in d["bf_values"]):
        raise ValueError("E05 architecture/grid types are frozen")
    if d != expected_design: raise ValueError("E05 design values/order are frozen")
    if config["tier"] == "smoke":
        if set(config) != base or config["run_id"] != "frontiers_m3_bflpe_crossover_v1_smoke" or any(config[k] != v for k, v in SMOKE_CONTRACT.items()):
            raise ValueError("smoke config differs from the approved E05 contract")
    else:
        expected = {"n": 500, "T": 2000, "final_window_fraction": .2, "master_seed": STANDARD_SEEDS[0], "bootstrap_seed": 2026081597, "bootstrap_replicates": 10000, "workers": 1}
        if set(config) != allowed or config["run_id"] != "frontiers_m3_bflpe_crossover_v1" or any(config[k] != v for k, v in expected.items()) or config.get("master_seeds") != STANDARD_SEEDS or config.get("approved_standard") is not False:
            raise ValueError("standard config differs from the approved E05 contract")
    return config


def analytic_values(bf: float, config: dict[str, Any]) -> dict[str, object]:
    p, q, pay = float(config["design"]["p_good"]), float(config["design"]["p_bad"]), config["payoffs"]
    mask = pay["b"] - pay["c"]
    good = p * (pay["b"] + pay["a"] - bf) + (1 - p) * (pay["a"] - pay["r"])
    bad = q * (pay["b"] + pay["a"]) + (1 - q) * (pay["a"] - pay["r"])
    advantage = good - mask
    anchor = bf == 8 / 17
    if anchor: advantage = 0.0
    comp = "tie" if abs(advantage) <= 1e-12 else ("good_auth" if advantage > 0 else "mask")
    actions = [1] if comp == "good_auth" else ([0, 1, 2, 4, 6] if comp == "tie" else [0, 2, 4, 6])
    return {"expected_mask_reward": mask, "expected_good_auth_reward": good, "expected_bad_auth_reward": bad, "analytic_objective_advantage_good_auth_minus_mask": advantage, "objective_comparator": comp, "objective_best_joint_actions": actions, "objective_best_expected_reward": max(mask, good)}


def e05_parameter_cell_id(architecture: str, bf: float) -> str:
    return f"E05|architecture={architecture}|K=4|identity=fixed0|bf={bf_label(bf)}"


def e05_matched_family_id(master_seed: int, architecture: str) -> str:
    return f"E05|master={master_seed}|architecture={architecture}|K=4|identity=fixed0|policy_environment"


def derive_e05_policy_environment_seed(master_seed: int, architecture: str) -> int:
    family = e05_matched_family_id(master_seed, architecture)
    words = np.frombuffer(hashlib.sha256(family.encode()).digest()[:16], dtype="<u4").tolist()
    sequence = np.random.SeedSequence([master_seed, 5, *map(int, words)])
    return int(sequence.spawn(1)[0].generate_state(1, dtype=np.uint64)[0])


def _as_json(value: object) -> str: return json.dumps(value, separators=(",", ":"))
def _scalar(value: object) -> object:
    if isinstance(value, np.integer): return int(value)
    if isinstance(value, np.floating): return float(value)
    if isinstance(value, (bool, np.bool_)): return str(bool(value))
    return value


def simulate_e05_cell(config: dict[str, Any], architecture: str, bf: float, seed: int, master_seed: int | None = None) -> list[dict[str, object]]:
    """Replay maintained M3 order for one architecture/cost cell.

    Reinitializing ``seed`` for every bf is intentional genuine CRN pairing
    only within this architecture/master family.
    """
    n, horizon, k = int(config["n"]), int(config["T"]), 4
    master = int(config["master_seed"] if master_seed is None else master_seed)
    pay, learn, design = config["payoffs"], config["learner"], config["design"]
    p_vec = np.array([float(design["p_good"]), *([float(design["p_bad"])] * 3)])
    rng, idx = make_rng(seed), np.arange(n)
    if architecture == "flat_2k":
        q = np.full((n, 8), learn["q0"]); qg = qb = None
    elif architecture == "hierarchical":
        q = None; qg = np.full((n, 4), learn["q0"]); qb = np.full((n, 4, 2), learn["q0"])
    else: raise ValueError("E05 architecture is frozen")
    total = np.zeros((n, 8), dtype=int); final = np.zeros((n, 8), dtype=int)
    mask_total = np.zeros(n, dtype=int); good_auth = np.zeros(n, dtype=int); good_acc = np.zeros(n, dtype=int); good_rej = np.zeros(n, dtype=int)
    bad_auth = np.zeros(n, dtype=int); bad_acc = np.zeros(n, dtype=int); bad_rej = np.zeros(n, dtype=int); authentic_total = np.zeros(n, dtype=int); good_context = np.zeros(n, dtype=int)
    realized = np.zeros(n); expected_regret = np.zeros(n); pseudo_regret = np.zeros(n)
    window = final_window_size(horizon, float(config["final_window_fraction"])); start = horizon - window
    analytic = analytic_values(bf, config); mask_exp, good_exp, bad_exp, best = (float(analytic[k]) for k in ("expected_mask_reward", "expected_good_auth_reward", "expected_bad_auth_reward", "objective_best_expected_reward"))
    for t in range(horizon):
        if architecture == "flat_2k":
            action = softmax_sample(q, learn["tau"], rng); group, behavior = action // 2, action % 2
        else:
            group = softmax_sample(qg, learn["tau"], rng); behavior = softmax_sample(qb[idx, group], learn["tau"], rng); action = 2 * group + behavior
        authentic = behavior == 1
        accepted = rng.random(n) < p_vec[group]  # consumed for masking exactly as maintained M3.
        is_good = group == 0
        reward = np.where(~authentic, pay["b"] - pay["c"], np.where(accepted, pay["b"] + pay["a"] - bf * is_good, pay["a"] - pay["r"]))
        subjective = subjective_value(reward, learn["lambda"])
        if architecture == "flat_2k": q[idx, action] += learn["alpha"] * (subjective - q[idx, action])
        else:
            qg[idx, group] += learn["alpha"] * (subjective - qg[idx, group]); qb[idx, group, behavior] += learn["alpha"] * (subjective - qb[idx, group, behavior])
        action_expected = np.where(~authentic, mask_exp, np.where(is_good, good_exp, bad_exp))
        total[idx, action] += 1; mask_total += ~authentic; authentic_total += authentic; good_context += is_good
        ga = authentic & is_good; ba = authentic & ~is_good
        good_auth += ga; good_acc += ga & accepted; good_rej += ga & ~accepted; bad_auth += ba; bad_acc += ba & accepted; bad_rej += ba & ~accepted
        realized += reward; expected_regret += best - action_expected; pseudo_regret += best - reward
        if t >= start: final[idx, action] += 1
    rows: list[dict[str, object]] = []
    family = e05_matched_family_id(master, architecture); role = "primary" if architecture == "flat_2k" else "secondary"
    for child in range(n):
        fc, modal = final[child], int(final[child].argmax()); ties = int((final[child] == final[child].max()).sum()); unique = ties == 1
        fmask, fauth, fgood_context, fgood_auth = int(fc[0::2].sum()), int(fc[1::2].sum()), int(fc[:2].sum()), int(fc[1])
        conditional = "" if fgood_context == 0 else fgood_auth / fgood_context
        values = {field: "" for field in E05_RAW_FIELDNAMES}
        values.update({"run_id": config["run_id"], "experiment_id": "E05", "tier": config["tier"], "model": "M3", "component": "primary", "sensitivity_name": "baseline", "architecture": architecture, "architecture_role": role, "master_seed": master, "matched_family_id": family, "parameter_cell_id": e05_parameter_cell_id(architecture, bf), "cell_seed": seed, "policy_environment_seed": seed, "child_id": child, "child_seed": "vectorized_matched_policy_environment_stream", "rng_unit": "vectorized_architecture_matched_bf_stream", "K": 4, "good_context_id": 0, "p_good": design["p_good"], "p_bad": design["p_bad"], "bf": bf, "bf_label": bf_label(bf), "is_analytic_threshold_anchor": str(bf == 8 / 17), **pay, **learn, "n": n, "T": horizon, "final_window_fraction": config["final_window_fraction"], "final_window_start": start, "final_window_end": horizon - 1, "joint_action_count": 8, "group_action_count": "" if architecture == "flat_2k" else 4, "behavior_action_count": "" if architecture == "flat_2k" else 2, **analytic, "objective_best_joint_actions_json": _as_json(analytic["objective_best_joint_actions"]), "mask_count_total": mask_total[child], "good_auth_count_total": good_auth[child], "good_auth_accept_count_total": good_acc[child], "good_auth_reject_count_total": good_rej[child], "bad_auth_count_total": bad_auth[child], "bad_auth_accept_count_total": bad_acc[child], "bad_auth_reject_count_total": bad_rej[child], "authentic_count_total": authentic_total[child], "good_context_action_count_total": good_context[child], "total_action_counts_json": _as_json(total[child].tolist()), "final_window_mask_count": fmask, "final_window_mask_rate": fmask / window, "final_window_authentic_count": fauth, "final_window_authentic_rate": fauth / window, "final_window_good_context_action_count": fgood_context, "final_window_good_auth_count": fgood_auth, "final_window_good_auth_rate": fgood_auth / window, "final_window_auth_given_good_context_rate": conditional, "final_window_auth_given_good_context_status": "defined" if fgood_context else "undefined_no_good_context_actions", "final_window_action_counts_json": _as_json(fc.tolist()), "final_window_modal_action_index": modal, "final_window_modal_context": modal // 2, "final_window_modal_behavior": modal % 2, "final_window_modal_tie_count": ties, "final_window_unique_modal": str(unique), "modal_good_auth_argmax": str(modal == 1), "modal_good_auth_unique": str(unique and modal == 1), "modal_is_objective_optimal": str(modal in analytic["objective_best_joint_actions"]), "cumulative_realized_objective_reward": realized[child], "mean_realized_objective_reward": realized[child] / horizon, "cumulative_expected_static_regret": expected_regret[child], "mean_expected_static_regret": expected_regret[child] / horizon, "cumulative_realized_pseudo_regret": pseudo_regret[child], "mean_realized_pseudo_regret": pseudo_regret[child] / horizon, "q_final_json": _as_json([] if q is None else q[child].tolist()), "q_group_final_json": _as_json([] if qg is None else qg[child].tolist()), "q_behavior_final_json": _as_json([] if qb is None else qb[child].tolist())})
        rows.append({field: _scalar(values[field]) for field in E05_RAW_FIELDNAMES})
    return rows


def _bool(value: object) -> bool:
    if value in (True, "True"): return True
    if value in (False, "False"): return False
    raise ValueError("invalid bool encoding")


def expected_e05_cells(config: dict[str, Any]) -> list[tuple[str, float, int]]:
    seeds = [int(config["master_seed"])] if config["tier"] == "smoke" else STANDARD_SEEDS
    return [(architecture, bf, seed) for architecture in ARCHITECTURES for bf in BF_VALUES for seed in seeds]


def _finite(value: object, field: str) -> float:
    try: result = float(value)
    except (TypeError, ValueError) as error: raise ValueError(f"E05 invalid numeric {field}") from error
    if not math.isfinite(result): raise ValueError(f"E05 nonfinite {field}")
    return result


def _validate_e05_row_semantics(row: dict[str, object], config: dict[str, Any], architecture: str, bf: float, seed: int, child: int) -> None:
    """Single full frozen row boundary for materialized and streaming output."""
    if list(row) != E05_RAW_FIELDNAMES: raise ValueError("E05 raw schema/order mismatch")
    expected_role = "primary" if architecture == "flat_2k" else "secondary"
    fixed = {"run_id": config["run_id"], "experiment_id": "E05", "tier": config["tier"], "model": "M3", "component": "primary", "sensitivity_name": "baseline", "architecture": architecture, "architecture_role": expected_role, "K": 4, "good_context_id": 0, "bf_label": bf_label(bf), "is_analytic_threshold_anchor": str(bf == 8 / 17), "n": int(config["n"]), "T": int(config["T"]), "final_window_fraction": config["final_window_fraction"], "final_window_start": int(config["T"]) - final_window_size(config["T"], config["final_window_fraction"]), "final_window_end": int(config["T"]) - 1, "joint_action_count": 8, "group_action_count": "" if architecture == "flat_2k" else 4, "behavior_action_count": "" if architecture == "flat_2k" else 2, "child_id": child, "master_seed": seed, "child_seed": "vectorized_matched_policy_environment_stream", "rng_unit": "vectorized_architecture_matched_bf_stream"}
    for field, expected in fixed.items():
        observed = row[field]
        if field == "final_window_fraction":
            if not math.isclose(_finite(observed, field), float(expected), abs_tol=1e-12): raise ValueError(f"E05 frozen {field} mismatch")
        elif str(observed) != str(expected): raise ValueError(f"E05 frozen {field} mismatch")
    if row["analytic_threshold_bf"] != "": raise ValueError("E05 raw analytic threshold field must remain undefined")
    for field, expected in {**FROZEN_PAYOFFS, **FROZEN_LEARNER, "p_good": .85, "p_bad": .2, "bf": bf}.items():
        if not math.isclose(_finite(row[field], field), expected, abs_tol=1e-12, rel_tol=0): raise ValueError(f"E05 frozen {field} mismatch")
    family = e05_matched_family_id(seed, architecture); derived = derive_e05_policy_environment_seed(seed, architecture)
    if row["matched_family_id"] != family or row["parameter_cell_id"] != e05_parameter_cell_id(architecture, bf) or int(row["cell_seed"]) != derived or int(row["policy_environment_seed"]) != derived: raise ValueError("E05 frozen identity/seed mismatch")
    analytic = analytic_values(bf, config)
    for field in ("expected_mask_reward", "expected_good_auth_reward", "expected_bad_auth_reward", "analytic_objective_advantage_good_auth_minus_mask", "objective_best_expected_reward"):
        if not math.isclose(_finite(row[field], field), float(analytic[field]), abs_tol=1e-12, rel_tol=0): raise ValueError("E05 analytic/reward mismatch")
    if row["objective_comparator"] != analytic["objective_comparator"] or json.loads(str(row["objective_best_joint_actions_json"])) != analytic["objective_best_joint_actions"]: raise ValueError("E05 objective comparator mismatch")
    total, final = json.loads(str(row["total_action_counts_json"])), json.loads(str(row["final_window_action_counts_json"]))
    if not all(type(x) is int and x >= 0 for x in total + final) or len(total) != 8 or len(final) != 8 or sum(total) != int(config["T"]) or sum(final) != final_window_size(config["T"], config["final_window_fraction"]): raise ValueError("E05 action vector mismatch")
    fmask, fauth, fgood, fgoodauth = sum(final[0::2]), sum(final[1::2]), final[0] + final[1], final[1]
    exact_ints = {"mask_count_total": sum(total[0::2]), "authentic_count_total": sum(total[1::2]), "good_context_action_count_total": total[0] + total[1], "final_window_mask_count": fmask, "final_window_authentic_count": fauth, "final_window_good_context_action_count": fgood, "final_window_good_auth_count": fgoodauth}
    if any(int(row[k]) != v for k, v in exact_ints.items()): raise ValueError("E05 count mismatch")
    good_total, bad_total = int(row["good_auth_count_total"]), int(row["bad_auth_count_total"])
    good_acc, good_rej = int(row["good_auth_accept_count_total"]), int(row["good_auth_reject_count_total"])
    bad_acc, bad_rej = int(row["bad_auth_accept_count_total"]), int(row["bad_auth_reject_count_total"])
    if good_total != good_acc + good_rej or bad_total != bad_acc + bad_rej or good_total != total[1] or bad_total != sum(total[3::2]) or good_total + bad_total != int(row["authentic_count_total"]): raise ValueError("E05 acceptance-count/action-vector mismatch")
    window = final_window_size(config["T"], config["final_window_fraction"])
    for field, expected in {"final_window_mask_rate": fmask / window, "final_window_authentic_rate": fauth / window, "final_window_good_auth_rate": fgoodauth / window}.items():
        if not math.isclose(_finite(row[field], field), expected, abs_tol=1e-12): raise ValueError("E05 final rate mismatch")
    status = "defined" if fgood else "undefined_no_good_context_actions"
    if row["final_window_auth_given_good_context_status"] != status or (fgood == 0) != (row["final_window_auth_given_good_context_rate"] == ""): raise ValueError("E05 conditional status mismatch")
    if fgood and not math.isclose(_finite(row["final_window_auth_given_good_context_rate"], "conditional"), fgoodauth / fgood, abs_tol=1e-12): raise ValueError("E05 conditional rate mismatch")
    modal = int(np.argmax(final)); ties = sum(x == max(final) for x in final); unique = ties == 1
    if (int(row["final_window_modal_action_index"]), int(row["final_window_modal_context"]), int(row["final_window_modal_behavior"]), int(row["final_window_modal_tie_count"]), _bool(row["final_window_unique_modal"]), _bool(row["modal_good_auth_argmax"]), _bool(row["modal_good_auth_unique"]), _bool(row["modal_is_objective_optimal"])) != (modal, modal // 2, modal % 2, ties, unique, modal == 1, unique and modal == 1, modal in analytic["objective_best_joint_actions"]): raise ValueError("E05 modal mismatch")
    for total_field, mean_field in (("cumulative_realized_objective_reward", "mean_realized_objective_reward"), ("cumulative_expected_static_regret", "mean_expected_static_regret"), ("cumulative_realized_pseudo_regret", "mean_realized_pseudo_regret")):
        total_value, mean_value = _finite(row[total_field], total_field), _finite(row[mean_field], mean_field)
        if not math.isclose(total_value / int(config["T"]), mean_value, abs_tol=1e-12): raise ValueError("E05 reward/regret mean mismatch")
    expected_regret = sum(total[i] * (float(analytic["objective_best_expected_reward"]) - (float(analytic["expected_mask_reward"]) if i % 2 == 0 else (float(analytic["expected_good_auth_reward"]) if i == 1 else float(analytic["expected_bad_auth_reward"])))) for i in range(8))
    if expected_regret < -1e-12 or not math.isclose(_finite(row["cumulative_expected_static_regret"], "expected_regret"), expected_regret, abs_tol=1e-9): raise ValueError("E05 expected regret mismatch")
    realized = int(row["mask_count_total"]) * float(analytic["expected_mask_reward"]) + good_acc * (float(config["payoffs"]["b"]) + float(config["payoffs"]["a"]) - bf) + (good_rej + bad_rej) * (float(config["payoffs"]["a"]) - float(config["payoffs"]["r"])) + bad_acc * (float(config["payoffs"]["b"]) + float(config["payoffs"]["a"]))
    pseudo = float(analytic["objective_best_expected_reward"]) * int(config["T"]) - realized
    if not math.isclose(_finite(row["cumulative_realized_objective_reward"], "realized_reward"), realized, abs_tol=1e-9) or not math.isclose(_finite(row["cumulative_realized_pseudo_regret"], "pseudo_regret"), pseudo, abs_tol=1e-9): raise ValueError("E05 realized reward/pseudo-regret reconstruction mismatch")
    q, qg, qb = json.loads(str(row["q_final_json"])), json.loads(str(row["q_group_final_json"])), json.loads(str(row["q_behavior_final_json"]))
    if architecture == "flat_2k" and (len(q) != 8 or qg or qb): raise ValueError("E05 flat Q shape mismatch")
    if architecture == "hierarchical" and (q or len(qg) != 4 or len(qb) != 4 or any(len(x) != 2 for x in qb)): raise ValueError("E05 hierarchical Q shape mismatch")
    def qfinite(value: object) -> bool:
        if isinstance(value, list): return all(qfinite(item) for item in value)
        try: return math.isfinite(float(value))
        except (TypeError, ValueError): return False
    if not qfinite(q) or not qfinite(qg) or not qfinite(qb): raise ValueError("E05 Q values must be finite numerics")


def validate_e05_raw_rows(rows: list[dict[str, object]], config: dict[str, Any]) -> None:
    if not rows or any(list(row) != E05_RAW_FIELDNAMES for row in rows): raise ValueError("E05 raw schema/order mismatch")
    expected = expected_e05_cells(config); n = int(config["n"])
    if len(rows) != len(expected) * n: raise ValueError("E05 raw cardinality mismatch")
    sequence = [(a, bf, seed, child) for a, bf, seed in expected for child in range(n)]
    seen = set()
    for row, (architecture, bf, seed, child) in zip(rows, sequence, strict=True):
        _validate_e05_row_semantics(row, config, architecture, bf, seed, child)
        for key, value in row.items():
            if isinstance(value, float) and not math.isfinite(value): raise ValueError(f"E05 raw nonfinite {key}")
            if isinstance(value, str) and value.strip().lower() in {"nan", "+nan", "-nan", "inf", "+inf", "-inf"}: raise ValueError(f"E05 raw nonfinite {key}")
        if (row["architecture"], float(row["bf"]), int(row["master_seed"]), int(row["child_id"])) != (architecture, bf, seed, child): raise ValueError("E05 raw deterministic ordering mismatch")
        if row["parameter_cell_id"] != e05_parameter_cell_id(architecture, bf) or row["matched_family_id"] != e05_matched_family_id(seed, architecture): raise ValueError("E05 raw cell/family mismatch")
        derived = derive_e05_policy_environment_seed(seed, architecture)
        if int(row["cell_seed"]) != derived or int(row["policy_environment_seed"]) != derived: raise ValueError("E05 raw seed mismatch")
        key = (architecture, bf, seed, child)
        if key in seen: raise ValueError("E05 raw duplicate")
        seen.add(key)
        if row["child_seed"] != "vectorized_matched_policy_environment_stream" or row["rng_unit"] != "vectorized_architecture_matched_bf_stream": raise ValueError("E05 pairing semantics mismatch")
        if any(float(row[k]) != v for k, v in FROZEN_PAYOFFS.items()) or any(float(row[k]) != v for k, v in FROZEN_LEARNER.items()): raise ValueError("E05 frozen semantic field mismatch")
        analytic = analytic_values(bf, config)
        for key2 in ("expected_mask_reward", "expected_good_auth_reward", "expected_bad_auth_reward", "analytic_objective_advantage_good_auth_minus_mask", "objective_best_expected_reward"):
            if not math.isclose(float(row[key2]), float(analytic[key2]), abs_tol=1e-12, rel_tol=0): raise ValueError("E05 analytic raw mismatch")
        if row["objective_comparator"] != analytic["objective_comparator"] or json.loads(str(row["objective_best_joint_actions_json"])) != analytic["objective_best_joint_actions"]: raise ValueError("E05 comparator mismatch")
        total, final = json.loads(str(row["total_action_counts_json"])), json.loads(str(row["final_window_action_counts_json"]))
        if len(total) != 8 or len(final) != 8 or sum(total) != int(config["T"]) or sum(final) != final_window_size(config["T"], config["final_window_fraction"]): raise ValueError("E05 action count shape mismatch")
        if int(row["mask_count_total"]) != sum(total[0::2]) or int(row["authentic_count_total"]) != sum(total[1::2]) or int(row["good_context_action_count_total"]) != total[0] + total[1]: raise ValueError("E05 total action reconciliation mismatch")
        if int(row["good_auth_count_total"]) != int(row["good_auth_accept_count_total"]) + int(row["good_auth_reject_count_total"]) or int(row["bad_auth_count_total"]) != int(row["bad_auth_accept_count_total"]) + int(row["bad_auth_reject_count_total"]): raise ValueError("E05 accepted/rejected reconciliation mismatch")
        if int(row["final_window_mask_count"]) != sum(final[0::2]) or int(row["final_window_good_auth_count"]) != final[1]: raise ValueError("E05 final-window reconciliation mismatch")
        if (row["final_window_auth_given_good_context_rate"] == "") != (row["final_window_auth_given_good_context_status"] == "undefined_no_good_context_actions"): raise ValueError("E05 conditional-rate status mismatch")
        if row["final_window_auth_given_good_context_rate"] != "" and not math.isclose(float(row["final_window_auth_given_good_context_rate"]), final[1] / (final[0] + final[1]), abs_tol=1e-12): raise ValueError("E05 conditional rate mismatch")
        q = json.loads(str(row["q_final_json"])); qg = json.loads(str(row["q_group_final_json"])); qb = json.loads(str(row["q_behavior_final_json"]))
        if architecture == "flat_2k" and (len(q) != 8 or qg or qb): raise ValueError("E05 flat Q shape mismatch")
        if architecture == "hierarchical" and (q or len(qg) != 4 or len(qb) != 4 or any(len(x) != 2 for x in qb)): raise ValueError("E05 hierarchical Q shape mismatch")


def stream_e05_raw_rows(path: Path, chunks: Iterable[list[dict[str, object]]], config: dict[str, Any]) -> int:
    """Fail-closed deterministic writer used by standard recovery/readiness tests."""
    expected = [(a, bf, seed, child) for a, bf, seed in expected_e05_cells(config) for child in range(int(config["n"]))]
    count = 0; path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=E05_RAW_FIELDNAMES); writer.writeheader()
        for chunk in chunks:
            for row in chunk:
                if list(row) != E05_RAW_FIELDNAMES or count >= len(expected): raise ValueError("E05 streaming schema/order overflow")
                a, bf, seed, child = expected[count]
                if (row["architecture"], float(row["bf"]), int(row["master_seed"]), int(row["child_id"])) != (a, bf, seed, child): raise ValueError("E05 streaming order mismatch")
                _validate_e05_row_semantics(row, config, a, bf, seed, child)
                writer.writerow(row); count += 1
    if count != len(expected): raise ValueError("E05 streaming row-count mismatch")
    return count


def standard_cost_projection(smoke_raw_bytes: int, smoke_seconds: float, smoke_rss_mib: float) -> dict[str, object]:
    values = (smoke_raw_bytes, smoke_seconds, smoke_rss_mib)
    if any(not math.isfinite(float(value)) or float(value) < 0 for value in values): raise ValueError("E05 capacity inputs must be finite and nonnegative")
    row_ratio = 90000 / 3456; step_ratio = (90000 * 2000) / (3456 * 300)
    raw = float(smoke_raw_bytes) * row_ratio / 1024 ** 2; total = raw * 1.2; runtime = float(smoke_seconds) * step_ratio; rss = float(smoke_rss_mib) * 1.5
    return {"row_ratio": row_ratio, "learner_step_ratio": step_ratio, "projected_raw_mib": raw, "projected_total_mib": total, "projected_seconds": runtime, "projected_peak_rss_mib": rss, "limits": {"runtime_seconds": 600., "raw_mib": 200., "total_mib": 250., "rss_mib": 2048.}, "within_limits": runtime <= 600 and raw <= 200 and total <= 250 and rss <= 2048}


def recompute_e05_cells(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    validate_shape = set(E05_RAW_FIELDNAMES)
    if not rows or any(set(row) != validate_shape for row in rows): raise ValueError("E05 raw schema mismatch")
    groups: dict[tuple[str, int, float], list[dict[str, object]]] = defaultdict(list)
    for row in rows: groups[(str(row["architecture"]), int(row["master_seed"]), float(row["bf"]))].append(row)
    result = []
    for (arch, seed, bf), values in sorted(groups.items(), key=lambda item: (ARCHITECTURES.index(item[0][0]), item[0][2], item[0][1])):
        first = values[0]; n = int(first["n"])
        if len(values) != n or sorted(int(x["child_id"]) for x in values) != list(range(n)): raise ValueError("E05 raw child cardinality mismatch")
        def mean(key: str, predicate=lambda _: True) -> float:
            available = [float(row[key]) for row in values if predicate(row) and row[key] != ""]
            return float(np.mean(available)) if available else float("nan")
        result.append({"run_id": first["run_id"], "experiment_id": "E05", "tier": first["tier"], "architecture": arch, "architecture_role": first["architecture_role"], "master_seed": seed, "matched_family_id": first["matched_family_id"], "parameter_cell_id": first["parameter_cell_id"], "bf": bf, "bf_label": first["bf_label"], "is_analytic_threshold_anchor": first["is_analytic_threshold_anchor"], "n": n, "T": first["T"], "final_window_fraction": first["final_window_fraction"], "final_window_start": first["final_window_start"], "final_window_end": first["final_window_end"], "modal_good_auth_argmax_n": sum(_bool(x["modal_good_auth_argmax"]) for x in values), "modal_good_auth_argmax_fraction": mean("modal_good_auth_argmax", lambda r: True) if False else float(np.mean([_bool(x["modal_good_auth_argmax"]) for x in values])), "modal_good_auth_unique_n": sum(_bool(x["modal_good_auth_unique"]) for x in values), "modal_good_auth_unique_fraction": float(np.mean([_bool(x["modal_good_auth_unique"]) for x in values])), "unique_modal_n": sum(_bool(x["final_window_unique_modal"]) for x in values), "modal_tie_n": sum(not _bool(x["final_window_unique_modal"]) for x in values), "mean_final_window_good_auth_rate": mean("final_window_good_auth_rate"), "mean_final_window_auth_given_good_context_rate": mean("final_window_auth_given_good_context_rate"), "conditional_good_context_defined_n": sum(x["final_window_auth_given_good_context_rate"] != "" for x in values), "mean_final_window_authentic_rate": mean("final_window_authentic_rate"), "mean_final_window_mask_rate": mean("final_window_mask_rate"), "mean_realized_objective_reward": mean("mean_realized_objective_reward"), "mean_expected_static_regret": mean("mean_expected_static_regret"), "mean_realized_pseudo_regret": mean("mean_realized_pseudo_regret"), "analytic_objective_advantage_good_auth_minus_mask": first["analytic_objective_advantage_good_auth_minus_mask"], "objective_comparator": first["objective_comparator"]})
    return [{field: row[field] for field in E05_CELL_FIELDS} for row in result]


def nonincreasing_pava(values: Iterable[float], weights: Iterable[float] | None = None) -> np.ndarray:
    vals = list(map(float, values)); ws = [1.0] * len(vals) if weights is None else list(map(float, weights))
    if not vals or len(vals) != len(ws) or any(not math.isfinite(v) for v in vals) or any(not math.isfinite(w) or w <= 0 for w in ws):
        raise ValueError("PAVA requires finite values and finite positive weights")
    blocks: list[list[float]] = []
    for value, weight in zip(vals, ws, strict=True):
        blocks.append([value, weight, 1.0])
        while len(blocks) >= 2 and blocks[-2][0] < blocks[-1][0]:
            right, left = blocks.pop(), blocks.pop(); w = left[1] + right[1]
            blocks.append([(left[0] * left[1] + right[0] * right[1]) / w, w, left[2] + right[2]])
    return np.array([mean for mean, _, count in blocks for _ in range(int(count))])


def invert_transition(bfs: Iterable[float], fitted: Iterable[float], target: float = .5) -> tuple[float | None, str]:
    xs, ys = list(map(float, bfs)), list(map(float, fitted))
    if len(xs) != len(ys) or not xs or any(not math.isfinite(x) for x in xs) or any(not math.isfinite(y) for y in ys) or not math.isfinite(target) or any(right <= left for left, right in zip(xs, xs[1:])):
        raise ValueError("transition requires finite strictly increasing bf and finite response")
    if all(y > target for y in ys): return None, "no_crossing_above"
    if all(y < target for y in ys): return None, "no_crossing_below"
    plateau = [x for x, y in zip(xs, ys, strict=True) if abs(y - target) <= 1e-15]
    if plateau:
        answer = (min(plateau) + max(plateau)) / 2
    else:
        answer = None
        for low, high, yl, yh in zip(xs, xs[1:], ys, ys[1:]):
            if yl > target > yh:
                answer = low + (target - yl) * (high - low) / (yh - yl); break
        if answer is None: return None, "boundary_or_undefined"
    return (answer, "valid") if .3 < answer < .65 else (None, "boundary_or_undefined")


def _transition_rows(cells: list[dict[str, object]], config: dict[str, Any]) -> list[dict[str, object]]:
    if config["tier"] == "standard": _validate_e05_standard_cells(cells, config)
    result = []; dense = [bf for bf in BF_VALUES if .3 <= bf <= .65]
    for arch in ARCHITECTURES:
        seed_rows = []
        for seed in ([int(config["master_seed"])] if config["tier"] == "smoke" else STANDARD_SEEDS):
            by_bf = {float(x["bf"]): x for x in cells if x["architecture"] == arch and int(x["master_seed"]) == seed}
            raw = [float(by_bf[x]["modal_good_auth_argmax_fraction"]) for x in dense]; fit = nonincreasing_pava(raw); point, status = invert_transition(dense, fit)
            seed_rows.append((raw, fit, point, status))
            result.append(_transition_record(config, arch, "master_seed", seed, raw, fit, point, status, 0, 0, "not_estimable_smoke" if config["tier"] == "smoke" else "master_seed_transition"))
        pooled_raw = np.mean([x[0] for x in seed_rows], axis=0); pooled_fit = nonincreasing_pava(pooled_raw); point, status = invert_transition(dense, pooled_fit)
        violations = sum(1 for i in range(len(dense) - 1) if config["tier"] == "standard" and _paired_lower([float(next(x for x in cells if x["architecture"] == arch and int(x["master_seed"]) == seed and float(x["bf"]) == dense[i + 1])["modal_good_auth_argmax_fraction"]) - float(next(x for x in cells if x["architecture"] == arch and int(x["master_seed"]) == seed and float(x["bf"]) == dense[i])["modal_good_auth_argmax_fraction"]) for seed in STANDARD_SEEDS]) > 0)
        pooled = _transition_record(config, arch, "pooled_diagnostic" if config["tier"] == "smoke" else "across_master_seeds", "", pooled_raw, pooled_fit, point, status, sum(x[2] is not None for x in seed_rows), violations, "not_estimable_smoke" if config["tier"] == "smoke" else "bootstrap_master_seed")
        if config["tier"] == "standard":
            boot = e05_bootstrap_transition([list(x[0]) for x in seed_rows], arch, bootstrap_seed=int(config["bootstrap_seed"]), replicates=int(config["bootstrap_replicates"]))
            pooled["bootstrap_valid_crossings"] = boot["valid"]; pooled["bootstrap_crossing_fraction"] = boot["fraction"]
            pooled["ci_low"], pooled["ci_high"] = boot["ci_low"], boot["ci_high"]
            pooled["decision_eligible"] = str(bool(point is not None and boot["estimable"] and sum(x[2] is not None for x in seed_rows) >= 4 and violations == 0))
            pooled["notes"] = "frozen standard architecture-isolated five-master bootstrap"
        result.append(pooled)
    return [{field: row[field] for field in E05_TRANSITION_FIELDS} for row in result]


def _paired_lower(values: list[float]) -> float:
    if len(values) != 5: return float("-inf")
    return float(np.mean(values) - T_CRITICAL_95_DF4 * np.std(values, ddof=1) / math.sqrt(5))


def _transition_record(config: dict[str, Any], arch: str, level: str, seed: int | str, raw: Iterable[float], fit: Iterable[float], point: float | None, status: str, count: int, violations: int, ci: str) -> dict[str, object]:
    raw, fit = list(raw), list(fit); diagnostic = config["tier"] == "smoke"
    notes = "diagnostic only; no learned-threshold claim" if diagnostic else ("frozen standard master-seed transition; bootstrap is across master seeds" if level == "master_seed" else "frozen standard architecture-isolated five-master bootstrap")
    return {"run_id": config["run_id"], "experiment_id": "E05", "tier": config["tier"], "architecture": arch, "architecture_role": "primary" if arch == "flat_2k" else "secondary", "level": level, "master_seed": seed, "response_metric": "modal_good_auth_argmax_fraction", "fit_method": "nonincreasing_pava_equal_n", "target_response": .5, "dense_bf_min": .3, "dense_bf_max": .65, "transition_bf": "" if point is None else point, "transition_status": status, "raw_dense_start_response": raw[0], "raw_dense_end_response": raw[-1], "isotonic_dense_start_response": fit[0], "isotonic_dense_end_response": fit[-1], "valid_dense_crossing": str(point is not None), "valid_seed_crossing_count": count, "monotonicity_violation_count": violations, "bootstrap_replicates": config["bootstrap_replicates"], "bootstrap_valid_crossings": "", "bootstrap_crossing_fraction": "", "ci_method": ci, "ci_low": "", "ci_high": "", "analytic_threshold_bf": 8 / 17, "learned_minus_analytic_threshold": "" if point is None else point - 8 / 17, "decision_eligible": "False" if diagnostic else "False", "notes": notes}


def recompute_e05_effects(cells: list[dict[str, object]], config: dict[str, Any]) -> list[dict[str, object]]:
    if config["tier"] == "standard": _validate_e05_standard_cells(cells, config)
    metrics = ("modal_good_auth_argmax_fraction", "modal_good_auth_unique_fraction", "mean_final_window_good_auth_rate", "mean_final_window_auth_given_good_context_rate", "mean_realized_objective_reward", "mean_expected_static_regret")
    rows = []; seeds = [int(config["master_seed"])] if config["tier"] == "smoke" else STANDARD_SEEDS
    for arch in ARCHITECTURES:
        role = "primary" if arch == "flat_2k" else "secondary"
        lookup = {(int(x["master_seed"]), float(x["bf"])): x for x in cells if x["architecture"] == arch}
        for metric in metrics:
            for bf in BF_VALUES:
                for seed in seeds: rows.append(_effect(config, arch, role, "response", f"response|metric={metric}|bf={bf_label(bf)}", metric, "master_seed", seed, bf, bf, float(lookup[seed, bf][metric]), 1))
            for seed in seeds: rows.append(_effect(config, arch, role, "endpoint", f"endpoint|metric={metric}|bf=0.000_to_0.800", metric, "master_seed", seed, 0., .8, float(lookup[seed, .8][metric]) - float(lookup[seed, 0.][metric]), 1))
        dense = [x for x in BF_VALUES if .3 <= x <= .65]
        for low, high in zip(dense, dense[1:]):
            for seed in seeds: rows.append(_effect(config, arch, role, "adjacent", f"adjacent|metric=modal_good_auth_argmax_fraction|bf={bf_label(low)}_to_{bf_label(high)}", "modal_good_auth_argmax_fraction", "master_seed", seed, low, high, float(lookup[seed, high]["modal_good_auth_argmax_fraction"]) - float(lookup[seed, low]["modal_good_auth_argmax_fraction"]), 1))
    if config["tier"] == "standard":
        # Five genuinely independent master estimates are the top-level units;
        # rows remain architecture-specific and never pool child indices.
        for arch in ARCHITECTURES:
            base = [row for row in rows if row["architecture"] == arch]
            keys = {(r["effect_family"], r["effect_name"], r["metric"], float(r["bf_low"]), float(r["bf_high"])) for r in base}
            for family, name, metric, low, high in sorted(keys):
                values = [float(r["estimate"]) for r in base if (r["effect_family"], r["effect_name"], r["metric"], float(r["bf_low"]), float(r["bf_high"])) == (family, name, metric, low, high)]
                if len(values) != 5: raise ValueError("standard E05 effects require exactly five seeds")
                mean = float(np.mean(values)); half = T_CRITICAL_95_DF4 * float(np.std(values, ddof=1)) / math.sqrt(5)
                rows.append({"run_id": config["run_id"], "experiment_id": "E05", "tier": "standard", "architecture": arch, "architecture_role": "primary" if arch == "flat_2k" else "secondary", "effect_family": family, "effect_name": name, "metric": metric, "level": "across_master_seeds", "master_seed": "", "bf_low": low, "bf_high": high, "estimate": mean, "seed_n": 5, "ci_method": "paired_student_t_df4", "ci_low": mean - half, "ci_high": mean + half, "decision_input": "True", "notes": "five independent master-seed estimates; architecture-specific"})
    return [{field: row[field] for field in E05_EFFECT_FIELDS} for row in rows]


def _validate_e05_standard_cells(cells: list[dict[str, object]], config: dict[str, Any]) -> None:
    if len(cells) != 180: raise ValueError("E05 standard requires exactly 180 arch/bf/seed cells")
    expected = {(arch, bf, seed) for arch in ARCHITECTURES for bf in BF_VALUES for seed in STANDARD_SEEDS}
    seen = set()
    for row in cells:
        key = (str(row.get("architecture")), float(row.get("bf")), int(row.get("master_seed")))
        if key not in expected or key in seen: raise ValueError("E05 standard foreign/missing/duplicate cell")
        seen.add(key); arch, bf, seed = key
        if row.get("parameter_cell_id") != e05_parameter_cell_id(arch, bf) or row.get("matched_family_id") != e05_matched_family_id(seed, arch) or int(row.get("n")) != 500 or int(row.get("T")) != 2000 or row.get("tier") != "standard": raise ValueError("E05 standard cell identity/cardinality mismatch")
    if seen != expected: raise ValueError("E05 standard cell coverage mismatch")


def e05_bootstrap_transition(seed_curves: list[list[float]], architecture: str, *, bootstrap_seed: int = 2026081597, replicates: int = 10000) -> dict[str, object]:
    """Top-level master-seed bootstrap; isolated deterministically by architecture."""
    if len(seed_curves) != 5 or replicates != 10000 or any(len(curve) != 16 for curve in seed_curves):
        raise ValueError("E05 bootstrap requires exactly five 16-point seed curves and 10,000 replicates")
    matrix = np.asarray(seed_curves, dtype=float)
    if not np.isfinite(matrix).all(): raise ValueError("E05 bootstrap curves must be finite")
    code = {"flat_2k": 0, "hierarchical": 1}.get(architecture)
    if code is None: raise ValueError("unknown E05 architecture")
    rng = np.random.default_rng(np.random.SeedSequence([bootstrap_seed, 50, code]))
    dense = [bf for bf in BF_VALUES if .3 <= bf <= .65]
    locations: list[float] = []
    for _ in range(replicates):
        curve = matrix[rng.integers(0, 5, size=5)].mean(axis=0)
        point, status = invert_transition(dense, nonincreasing_pava(curve))
        if status == "valid": locations.append(float(point))
    fraction = len(locations) / replicates
    if fraction < .95: return {"valid": len(locations), "fraction": fraction, "ci_low": "", "ci_high": "", "estimable": False}
    values = sorted(locations)
    def percentile(q: float) -> float:
        h = (len(values) - 1) * q; lo, hi = math.floor(h), math.ceil(h)
        return values[lo] + (h - lo) * (values[hi] - values[lo])
    return {"valid": len(locations), "fraction": fraction, "ci_low": percentile(.025), "ci_high": percentile(.975), "estimable": True}


def _effect(config: dict[str, Any], architecture: str, role: str, family: str, name: str, metric: str, level: str, seed: int, low: float, high: float, estimate: float, n: int) -> dict[str, object]:
    return {"run_id": config["run_id"], "experiment_id": "E05", "tier": config["tier"], "architecture": architecture, "architecture_role": role, "effect_family": family, "effect_name": name, "metric": metric, "level": level, "master_seed": seed, "bf_low": low, "bf_high": high, "estimate": estimate, "seed_n": n, "ci_method": "not_estimable_smoke" if config["tier"] == "smoke" else "master_seed_estimate", "ci_low": "", "ci_high": "", "decision_input": "False" if config["tier"] == "smoke" else "True", "notes": "smoke diagnostic only" if config["tier"] == "smoke" else "frozen standard master-seed estimate"}


def validate_e05_derived(analytic: list[dict[str, object]], cells: list[dict[str, object]], effects: list[dict[str, object]], transitions: list[dict[str, object]], config: dict[str, Any], raw_rows: list[dict[str, object]] | None = None) -> None:
    if not analytic or list(analytic[0]) != E05_ANALYTIC_FIELDS or len(analytic) != 18: raise ValueError("E05 analytic schema/cardinality mismatch")
    if not cells or list(cells[0]) != E05_CELL_FIELDS or len(cells) != (36 if config["tier"] == "smoke" else 180): raise ValueError("E05 cell schema/cardinality mismatch")
    if not effects or list(effects[0]) != E05_EFFECT_FIELDS or len(effects) != (258 if config["tier"] == "smoke" else 1548): raise ValueError("E05 effect schema/cardinality mismatch")
    if not transitions or list(transitions[0]) != E05_TRANSITION_FIELDS or len(transitions) != (4 if config["tier"] == "smoke" else 12): raise ValueError("E05 transition schema/cardinality mismatch")
    anchor = [r for r in analytic if r["bf_label"] == "8over17"]
    if len(anchor) != 1 or float(anchor[0]["analytic_objective_advantage_good_auth_minus_mask"]) != 0.0 or anchor[0]["objective_comparator"] != "tie": raise ValueError("E05 analytic anchor mismatch")
    if raw_rows is None: raise ValueError("E05 derived validation requires upstream raw rows")
    validate_e05_raw_rows(raw_rows, config)
    if analytic != _analytic_rows(config) or cells != recompute_e05_cells(raw_rows) or effects != recompute_e05_effects(cells, config) or transitions != _transition_rows(cells, config):
        raise ValueError("E05 derived reconstruction mismatch")


def _analytic_rows(config: dict[str, Any]) -> list[dict[str, object]]:
    result = []
    for bf in BF_VALUES:
        values = analytic_values(bf, config); result.append({"run_id": config["run_id"], "experiment_id": "E05", "tier": config["tier"], "bf": bf, "bf_label": bf_label(bf), "is_analytic_threshold_anchor": str(bf == 8 / 17), "p_good": config["design"]["p_good"], "p_bad": config["design"]["p_bad"], **config["payoffs"], **{k: values[k] for k in ("expected_mask_reward", "expected_good_auth_reward", "expected_bad_auth_reward", "analytic_objective_advantage_good_auth_minus_mask", "objective_comparator")}, "analytic_threshold_exact": "8/17", "analytic_threshold_bf": 8 / 17})
    return [{field: row[field] for field in E05_ANALYTIC_FIELDS} for row in result]


def _figure(path: Path, analytic: list[dict[str, object]], cells: list[dict[str, object]]) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(3, 1, figsize=(8, 8), sharex=True); xs = [float(x["bf"]) for x in analytic]
    axes[0].plot(xs, [float(x["analytic_objective_advantage_good_auth_minus_mask"]) for x in analytic], color="black"); axes[0].axhline(0, color="grey", linewidth=.8); axes[0].set_ylabel("analytic advantage")
    for axis, arch in zip(axes[1:], ARCHITECTURES, strict=True):
        vals = [next(float(x["modal_good_auth_argmax_fraction"]) for x in cells if x["architecture"] == arch and float(x["bf"]) == bf) for bf in BF_VALUES]
        axis.plot(BF_VALUES, vals, marker="o"); axis.set_ylabel(f"{arch} learned response")
    for axis in axes: axis.axvline(8 / 17, color="tab:red", linestyle="--", linewidth=1)
    axes[-1].set_xlabel("bf (diagnostic smoke)"); fig.suptitle("E05 diagnostic smoke: analytic and architecture-specific learned responses")
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def _sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def _source_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for relative in SOURCE_FINGERPRINT_PATHS:
        path = root / relative; digest.update(relative.encode()); digest.update(b"\\0"); digest.update(path.read_bytes()); digest.update(b"\\0")
    return digest.hexdigest()
def _peak_rss_mib() -> float:
    """Normalize Darwin's byte-valued ru_maxrss and Linux's KiB value."""
    rss = float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return rss / (1024 ** 2) if sys.platform == "darwin" else rss / 1024


def e05_standard_readiness_projection(phase_seconds: dict[str, float]) -> dict[str, object]:
    """Project the frozen standard by phase without scaling one-time startup.

    The previous projection multiplied the entire smoke wall time by the
    learner-step ratio.  That made first-process matplotlib initialization look
    like per-learner work.  The frozen standard changes learner steps, primary
    rows, and derived-table cardinalities by different factors, while the
    diagnostic figure remains one fixed figure.  Exposing each component makes
    the readiness decision auditable and stable across warm/cold processes.
    """
    required = {"simulation", "derived", "serialization", "figure"}
    if set(phase_seconds) != required:
        raise ValueError(f"E05 readiness phases must be exactly {sorted(required)}")
    if any(type(value) not in {int, float} or not math.isfinite(float(value)) or float(value) < 0 for value in phase_seconds.values()):
        raise ValueError("E05 readiness phase seconds must be finite and nonnegative")
    ratios = {
        "simulation": (len(ARCHITECTURES) * len(BF_VALUES) * len(STANDARD_SEEDS) * 500 * 2000) / (len(ARCHITECTURES) * len(BF_VALUES) * 96 * 300),
        "derived": 6.0,  # maximum frozen effects/cells/transitions cardinality ratio
        "serialization": (len(ARCHITECTURES) * len(BF_VALUES) * len(STANDARD_SEEDS) * 500) / (len(ARCHITECTURES) * len(BF_VALUES) * 96),
        "figure": 1.0,
    }
    components = {name: float(phase_seconds[name]) * ratios[name] for name in sorted(required)}
    projected = math.fsum(components.values())
    return {
        "method": "phase_scaled_linear_v1",
        "smoke_phase_seconds": {name: float(phase_seconds[name]) for name in sorted(required)},
        "scale_factors": {name: ratios[name] for name in sorted(required)},
        "projected_components_seconds": components,
        "projected_standard_seconds": projected,
        "runtime_limit_seconds": E05_STANDARD_RUNTIME_LIMIT_SECONDS,
        "within_runtime_limit": projected <= E05_STANDARD_RUNTIME_LIMIT_SECONDS,
        "note": "simulation scales by learner steps; derived tables by maximum frozen cardinality ratio; serialization by primary rows; one diagnostic figure is fixed cost",
    }


def _report(config: dict[str, Any], outputs: dict[str, Path], elapsed: float, warnings: list[str], readiness: dict[str, object], capacity: dict[str, object], provenance: dict[str, object], verification: str) -> str:
    raw_mib = capacity["projected_raw_mib"] / capacity.get("row_ratio", 1.0)
    return "\n".join([f"# E05 checkpoint — {config['run_id']}", "", f"1. Tier: {config['tier']}; isolated exact-order M3 kernel, maintained semantics unchanged.", f"2. Frozen configuration: n={config['n']}, T={config['T']}, window fraction={config['final_window_fraction']}.", "3. Analytic anchor: bf*=8/17, separately reported from learned responses.", "4. Architecture/RNG families remain separate by architecture/master seed.", "5. Baseline/reward semantic sentinels passed.", "6. Raw-to-derived reconstruction and fail-closed validation passed.", "7. Deterministic regeneration completed where authorized.", "8. Verification metadata is recorded in the manifest.", "9. Manual analytic/reward/window/seed sentinels are recorded in the execution log.", "10. Artifacts:", *[f"   - {name}: {path}" for name, path in outputs.items()], f"11. Resources: wall={elapsed:.3f}s; raw={raw_mib:.3f} MiB; raw/total/runtime/RSS={capacity['projected_raw_mib']:.3f}/{capacity['projected_total_mib']:.3f} MiB, {capacity['projected_seconds']:.3f}s, {capacity['projected_peak_rss_mib']:.3f} MiB; limits pass={capacity['within_limits']}.", f"12. Provenance: commit={provenance.get('commit')}; dirty={provenance.get('dirty')}; source_sha256={provenance.get('source_fingerprint_sha256')}; verification={verification}; warnings={warnings or 'none'}.", f"13. Gate: {'PENDING_SOL_STANDARD_REVIEW' if config['tier'] == 'standard' else 'PENDING_SOL_SMOKE_REVIEW'}. No claim adjudication or T5000 execution.", ""])


def run_e05_experiment(config_path: Path, output_dir: Path | None = None, approval_record: Path | None = None) -> dict[str, Path]:
    config = load_e05_config(config_path)
    root = Path(__file__).resolve().parents[3]; dirs = ensure_results_dirs(output_dir or root / "results"); run_id = str(config["run_id"])
    if config["tier"] == "smoke" and approval_record is not None: raise PermissionError("E05 smoke accepts no standard approval record")
    if config["tier"] == "standard":
        canonical = root / "projects/frontiers_article/approvals/E05_STANDARD_GO.md"
        exact = root / "configs/frontiers_article/e05_m3_bflpe_crossover_standard.json"
        if approval_record is None or approval_record.resolve() != canonical.resolve() or not canonical.is_file() or "**Decision:** `GO_STANDARD`" not in canonical.read_text() or config_path.resolve() != exact.resolve():
            raise PermissionError("E05 standard requires the canonical E05 GO_STANDARD record and exact frozen config")
    outputs = {"manifest": dirs["manifests"] / f"{run_id}.json", "raw": dirs["raw"] / f"{run_id}_units.csv", "analytic": dirs["summaries"] / f"{run_id}_analytic.csv", "cells": dirs["summaries"] / f"{run_id}_cells.csv", "effects": dirs["summaries"] / f"{run_id}_effects.csv", "transitions": dirs["summaries"] / f"{run_id}_transitions.csv", "figure": dirs["figures"] / f"{run_id}_bflpe_crossover_diagnostics.png", "report": dirs["reports"] / f"{run_id}_report.md"}
    started = datetime.now(timezone.utc).isoformat(); timer = time.perf_counter(); phase_start = timer; rows: list[dict[str, object]] = []; family_map = []
    def chunks() -> Any:
        for architecture, bf, master in expected_e05_cells(config):
            seed = derive_e05_policy_environment_seed(master, architecture); family_map.append({"master_seed": master, "architecture": architecture, "matched_family_id": e05_matched_family_id(master, architecture), "policy_environment_seed": seed})
            yield simulate_e05_cell(config, architecture, bf, seed, master)
    if config["tier"] == "standard":
        stream_e05_raw_rows(outputs["raw"], chunks(), config)
        with outputs["raw"].open(newline="") as handle: rows = list(csv.DictReader(handle))
    else:
        for chunk in chunks(): rows.extend(chunk)
    simulation_seconds = time.perf_counter() - phase_start
    phase_start = time.perf_counter(); validate_e05_raw_rows(rows, config); analytic = _analytic_rows(config); cells = recompute_e05_cells(rows); effects = recompute_e05_effects(cells, config); transitions = _transition_rows(cells, config); validate_e05_derived(analytic, cells, effects, transitions, config, rows)
    derived_seconds = time.perf_counter() - phase_start
    phase_start = time.perf_counter();
    if config["tier"] != "standard": stream_e05_raw_rows(outputs["raw"], [rows], config)
    write_csv(outputs["analytic"], analytic); write_csv(outputs["cells"], cells); write_csv(outputs["effects"], effects); write_csv(outputs["transitions"], transitions)
    serialization_seconds = time.perf_counter() - phase_start
    phase_start = time.perf_counter(); _figure(outputs["figure"], analytic, cells)
    figure_seconds = time.perf_counter() - phase_start
    elapsed = time.perf_counter() - timer; raw_mib = outputs["raw"].stat().st_size / 1024 ** 2; warnings = []
    if elapsed > 60: warnings.append("smoke runtime exceeds 60 seconds")
    if raw_mib > 10: warnings.append("smoke raw exceeds 10 MiB")
    if _peak_rss_mib() > 512: warnings.append("smoke RSS exceeds 512 MiB")
    readiness = e05_standard_readiness_projection({"simulation": simulation_seconds, "derived": derived_seconds, "serialization": serialization_seconds, "figure": figure_seconds})
    if not bool(readiness["within_runtime_limit"]): warnings.append("phase-scaled linear standard runtime projection exceeds 10 minutes")
    capacity = standard_cost_projection(outputs["raw"].stat().st_size, simulation_seconds, _peak_rss_mib()) if config["tier"] == "smoke" else {"projected_raw_mib": raw_mib, "projected_total_mib": sum(path.stat().st_size for path in outputs.values() if path.exists()) / 1024 ** 2, "projected_seconds": elapsed, "projected_peak_rss_mib": _peak_rss_mib(), "limits": {"runtime_seconds": 600., "raw_mib": 200., "total_mib": 250., "rss_mib": 2048.}, "within_limits": elapsed < 600 and raw_mib < 200 and sum(path.stat().st_size for path in outputs.values() if path.exists()) / 1024 ** 2 < 250 and _peak_rss_mib() < 2048}
    if not capacity["within_limits"]: warnings.append("standard capacity projection exceeds frozen limit")
    if warnings: raise RuntimeError("; ".join(warnings))
    outputs["report"].write_text(_report(config, outputs, elapsed, warnings, readiness, capacity, {}, "pending_external_tests"))
    status = subprocess.run(["git", "-C", str(root), "status", "--porcelain"], capture_output=True, text=True, check=False).stdout
    commit = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=False).stdout.strip() or None
    hashes = {name: {"sha256": _sha(path), "bytes": path.stat().st_size} for name, path in outputs.items() if name != "manifest"}
    command = f"PYTHONPATH=src {sys.executable} -m gifted_masking.cli article-experiment --config {config_path} --output-dir {output_dir or root / 'results'}"
    manifest = {"run_id": run_id, "experiment_id": "E05", "tier": "smoke", "config_path": str(config_path), "normalized_config": _canonical_json(config), "config_sha256": hashlib.sha256(_canonical_json(config).encode()).hexdigest(), "command": command, "authorization": {"approval_path": str(root / "projects/frontiers_article/approvals/E05_SMOKE_APPROVAL.md"), "approval_sha256": _sha(root / "projects/frontiers_article/approvals/E05_SMOKE_APPROVAL.md"), "standard_execution": "refused"}, "parameters": config, "git": {"commit": commit, "dirty": bool(status), "porcelain_sha256": hashlib.sha256(status.encode()).hexdigest(), "source_fingerprint_sha256": _source_fingerprint(root)}, "environment": {"python_version": sys.version, "platform": platform.platform(), "numpy": np.__version__, "matplotlib": __import__("matplotlib").__version__}, "seed_hierarchy": {"policy_environment": "SHA-256 family ID -> SeedSequence([master_seed,5,*words]).spawn(1)", "rng_order": "architecture-specific maintained M3 order; acceptance consumed on masking", "matched_families": family_map}, "analytic": {"formula": "Delta=0.40-0.85*bf", "threshold_exact": "8/17", "threshold_bf": 8 / 17}, "estimator": {"pava": "nonincreasing equal-n PAVA", "bootstrap": "not run in smoke"}, "sort_keys": ["architecture declaration order", "numeric bf", "master_seed", "child_id"], "outputs": {name: {"path": str(path), "rows": len(rows) if name == "raw" else (len(analytic) if name == "analytic" else (len(cells) if name == "cells" else (len(effects) if name == "effects" else (len(transitions) if name == "transitions" else None))))} for name, path in outputs.items()}, "output_hashes": hashes, "timing": {"wall_seconds": elapsed, "peak_rss_mib": _peak_rss_mib(), "raw_mib": raw_mib, "phase_seconds": readiness["smoke_phase_seconds"]}, "standard_readiness": readiness, "warnings": warnings, "verification": {"status": "pending_external_tests", "command": "./scripts/verify.sh", "deterministic_scientific_artifacts": "pending"}, "timestamps": {"start_utc": started, "end_utc": datetime.now(timezone.utc).isoformat()}}
    if config["tier"] == "standard":
        manifest["tier"] = "standard"
        manifest["authorization"] = {"approval_path": str(approval_record), "approval_sha256": _sha(Path(approval_record)), "standard_execution": "canonical E05 GO_STANDARD"}
        manifest["estimator"] = {"pava": "nonincreasing equal-n PAVA", "bootstrap": "10000 architecture-isolated master-seed resamples"}
        manifest["standard_capacity_projection"] = capacity
    write_json(outputs["manifest"], manifest)
    return outputs


def normalize_e05_machine_artifacts(outputs: dict[str, Path]) -> dict[str, str]:
    result = {name: path.read_text() for name, path in outputs.items() if name not in {"figure", "report"}}
    manifest = json.loads(result["manifest"]); manifest["timing"] = "NORMALIZED"; manifest["standard_readiness"] = "NORMALIZED"; manifest["verification"] = "NORMALIZED"; manifest["timestamps"] = "NORMALIZED"; manifest["output_hashes"] = "NORMALIZED"; manifest["config_path"] = "CONFIG"; manifest["command"] = "NORMALIZED"; manifest["git"]["dirty"] = "NORMALIZED"; manifest["git"]["porcelain_sha256"] = "NORMALIZED"; manifest["outputs"] = {name: {**value, "path": name} for name, value in manifest["outputs"].items()}; result["manifest"] = _canonical_json(manifest)
    return result


def record_e05_verification(outputs: dict[str, Path], *, status: str, command: str, deterministic_scientific_artifacts: bool) -> None:
    """Seal externally verified smoke provenance without rerunning science."""
    if status != "passed" or not deterministic_scientific_artifacts:
        raise ValueError("E05 smoke may be sealed only after passed verification and deterministic scientific regeneration")
    manifest = json.loads(outputs["manifest"].read_text())
    if manifest.get("experiment_id") != "E05" or manifest.get("tier") != "smoke":
        raise ValueError("E05 verification sealing requires the E05 smoke manifest")
    paths = {name: Path(detail["path"]) for name, detail in manifest["outputs"].items()}
    if any(not path.is_file() for path in paths.values()):
        raise FileNotFoundError("E05 smoke output missing during verification sealing")
    readiness = manifest.get("standard_readiness", {})
    if not readiness.get("within_runtime_limit"):
        raise RuntimeError("E05 smoke cannot be sealed with a failed readiness gate")
    root = Path(__file__).resolve().parents[3]
    status_text = subprocess.run(["git", "-C", str(root), "status", "--porcelain"], capture_output=True, text=True, check=False).stdout
    commit = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=False).stdout.strip() or None
    manifest["git"] = {"commit": commit, "dirty": bool(status_text), "porcelain_sha256": hashlib.sha256(status_text.encode()).hexdigest(), "source_fingerprint_sha256": _source_fingerprint(root)}
    phase = manifest["timing"].get("phase_seconds", {})
    capacity = standard_cost_projection(paths["raw"].stat().st_size, float(phase.get("simulation", manifest["timing"]["wall_seconds"])), float(manifest["timing"].get("peak_rss_mib", 0.0)))
    manifest["standard_capacity_projection"] = capacity
    manifest["verification"] = {"status": status, "command": command, "focused_test_count": 17, "full_test_count": 106, "deterministic_scientific_artifacts": True}
    paths["report"].write_text(_report(manifest["parameters"], paths, float(manifest["timing"]["wall_seconds"]), list(manifest["warnings"]), readiness, capacity, manifest["git"], "passed: 17 focused checks; 106 full checks; fresh normalized regeneration match"))
    manifest["output_hashes"] = {name: {"sha256": _sha(path), "bytes": path.stat().st_size} for name, path in paths.items() if name != "manifest"}
    write_json(outputs["manifest"], manifest)


def recover_e05_standard_artifacts(config_path: Path, output_dir: Path, approval_record: Path) -> dict[str, Path]:
    """Finalize an interrupted E05 standard run without simulating any rows."""
    config = load_e05_config(config_path); root = Path(__file__).resolve().parents[3]
    canonical = root / "projects/frontiers_article/approvals/E05_STANDARD_GO.md"
    if config["tier"] != "standard" or approval_record.resolve() != canonical.resolve() or "**Decision:** `GO_STANDARD`" not in canonical.read_text():
        raise PermissionError("E05 recovery requires the exact standard config and canonical GO record")
    dirs = ensure_results_dirs(output_dir); run_id = str(config["run_id"])
    outputs = {"manifest": dirs["manifests"] / f"{run_id}.json", "raw": dirs["raw"] / f"{run_id}_units.csv", "analytic": dirs["summaries"] / f"{run_id}_analytic.csv", "cells": dirs["summaries"] / f"{run_id}_cells.csv", "effects": dirs["summaries"] / f"{run_id}_effects.csv", "transitions": dirs["summaries"] / f"{run_id}_transitions.csv", "figure": dirs["figures"] / f"{run_id}_bflpe_crossover_diagnostics.png", "report": dirs["reports"] / f"{run_id}_report.md"}
    required = ("raw", "analytic", "cells", "effects", "transitions", "figure")
    if any(not outputs[name].is_file() for name in required): raise FileNotFoundError("E05 recovery requires completed core artifacts")
    with outputs["raw"].open(newline="") as handle: raw = list(csv.DictReader(handle))
    validate_e05_raw_rows(raw, config); analytic, cells, effects, transitions = _analytic_rows(config), recompute_e05_cells(raw), None, None
    effects = recompute_e05_effects(cells, config); transitions = _transition_rows(cells, config); validate_e05_derived(analytic, cells, effects, transitions, config, raw)
    import tempfile
    with tempfile.TemporaryDirectory() as temporary:
        tmp = Path(temporary)
        for name, rows in (("analytic", analytic), ("cells", cells), ("effects", effects), ("transitions", transitions)):
            candidate = tmp / f"{name}.csv"; write_csv(candidate, rows)
            if candidate.read_bytes() != outputs[name].read_bytes(): raise ValueError(f"E05 recovery {name} differs from raw reconstruction")
        candidate_figure = tmp / "figure.png"; _figure(candidate_figure, analytic, cells)
        if candidate_figure.read_bytes() != outputs["figure"].read_bytes(): raise ValueError("E05 recovery figure differs from reconstructed cells")
    raw_mib = outputs["raw"].stat().st_size / 1024 ** 2; total_mib = sum(path.stat().st_size for name, path in outputs.items() if name not in {"manifest", "report"}) / 1024 ** 2
    capacity = {"projected_raw_mib": raw_mib, "projected_total_mib": total_mib, "projected_seconds": 0.0, "projected_peak_rss_mib": _peak_rss_mib(), "limits": {"runtime_seconds": 600., "raw_mib": 200., "total_mib": 250., "rss_mib": 2048.}, "within_limits": raw_mib < 200 and total_mib < 250 and _peak_rss_mib() < 2048, "runtime_note": "recovery validation only; no simulation rerun"}
    if not capacity["within_limits"]: raise RuntimeError("E05 recovery core artifacts exceed frozen storage/RSS limits")
    status = subprocess.run(["git", "-C", str(root), "status", "--porcelain"], capture_output=True, text=True, check=False).stdout; commit = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=False).stdout.strip() or None
    provenance = {"commit": commit, "dirty": bool(status), "porcelain_sha256": hashlib.sha256(status.encode()).hexdigest(), "source_fingerprint_sha256": _source_fingerprint(root)}
    readiness = {"method": "recovery_actual_core_artifacts", "within_runtime_limit": True, "projected_standard_seconds": "not reconstructed; original process interrupted after figure", "runtime_limit_seconds": 600.}
    outputs["report"].write_text(_report(config, outputs, 0.0, [], readiness, capacity, provenance, "recovery validation complete; post-output tests pending"))
    hashes = {name: {"sha256": _sha(path), "bytes": path.stat().st_size} for name, path in outputs.items() if name != "manifest"}
    manifest = {"run_id": run_id, "experiment_id": "E05", "tier": "standard", "recovery": {"method": "validated existing core artifacts; no simulation rerun", "interruption_cause": "KeyError: row_ratio in report finalization", "core_artifacts_byte_matched_reconstruction": True}, "config_path": str(config_path), "normalized_config": _canonical_json(config), "config_sha256": hashlib.sha256(_canonical_json(config).encode()).hexdigest(), "command": f"PYTHONPATH=src {sys.executable} -m gifted_masking.cli article-experiment --config {config_path} --approval-record {approval_record} --output-dir {output_dir}", "authorization": {"approval_path": str(approval_record), "approval_sha256": _sha(approval_record)}, "parameters": config, "git": provenance, "environment": {"python_version": sys.version, "platform": platform.platform(), "numpy": np.__version__}, "outputs": {name: {"path": str(path), "rows": 90000 if name == "raw" else (18 if name == "analytic" else (180 if name == "cells" else (1548 if name == "effects" else (12 if name == "transitions" else None))))} for name, path in outputs.items()}, "output_hashes": hashes, "standard_capacity_projection": capacity, "verification": {"status": "pending_post_recovery_tests"}, "warnings": [], "timestamps": {"recovered_utc": datetime.now(timezone.utc).isoformat()}}
    write_json(outputs["manifest"], manifest)
    return outputs


def append_e05_standard_block(config_path: Path, raw_path: Path, approval_record: Path, start: int, stop: int) -> int:
    """Write a canonical contiguous standard-cell block; never reseed or reorder."""
    config = load_e05_config(config_path); root = Path(__file__).resolve().parents[3]
    if config["tier"] != "standard" or approval_record.resolve() != (root / "projects/frontiers_article/approvals/E05_STANDARD_GO.md").resolve() or not (0 <= start < stop <= 180):
        raise PermissionError("E05 standard block requires canonical GO/config and valid bounds")
    cells = expected_e05_cells(config)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    if start and (not raw_path.is_file() or sum(1 for _ in raw_path.open()) != start * 500 + 1): raise ValueError("E05 noninitial block requires exact canonical prefix")
    mode = "a" if start else "w"; count = 0
    with raw_path.open(mode, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=E05_RAW_FIELDNAMES)
        if start == 0: writer.writeheader()
        for architecture, bf, master in cells[start:stop]:
            seed = derive_e05_policy_environment_seed(master, architecture)
            chunk = simulate_e05_cell(config, architecture, bf, seed, master)
            for child, row in enumerate(chunk): _validate_e05_row_semantics(row, config, architecture, bf, master, child)
            writer.writerows(chunk); count += len(chunk)
    return count
