from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

import numpy as np

from gifted_masking.core import subjective_value
from gifted_masking.models import m2


STATE_NAMES = ("neutral", "accepted", "stigmatized")
ACTION_NAMES = ("mask", "authentic")
TRANSITION_ORDERING = "reward_first_then_delta_turnover_or_eta_escape_on_next_state"


@dataclass(frozen=True)
class M2Params:
    p: float
    eta: float
    b: float = 1.0
    a: float = 0.6
    c: float = 0.25
    r: float = 2.0
    b2: float = 0.5
    r2: float = 2.5
    delta: float = 0.02
    gamma: float = 0.9
    lam: float = 1.0


def _reward(reward: float, reward_mode: str, lam: float) -> float:
    if reward_mode == "objective":
        return float(reward)
    if reward_mode == "subjective":
        return float(subjective_value(np.asarray([reward], dtype=float), lam)[0])
    raise ValueError(f"unknown reward_mode: {reward_mode}")


def build_m2_transition_table(params: M2Params, reward_mode: str = "objective") -> list[list[list[dict[str, float]]]]:
    p = params.p
    eta = params.eta
    b = params.b
    a = params.a
    c = params.c
    r = params.r
    b2 = params.b2
    r2 = params.r2
    delta = params.delta
    lam = params.lam
    table: list[list[list[dict[str, float]]]] = [[[] for _ in ACTION_NAMES] for _ in STATE_NAMES]

    table[m2.STATE_NEUTRAL][0] = [{"probability": 1.0, "next_state": m2.STATE_NEUTRAL, "reward": _reward(b - c, reward_mode, lam)}]
    table[m2.STATE_NEUTRAL][1] = [
        {"probability": p, "next_state": m2.STATE_ACCEPTED, "reward": _reward(b + a, reward_mode, lam)},
        {"probability": 1.0 - p, "next_state": m2.STATE_STIGMATIZED, "reward": _reward(a - r, reward_mode, lam)},
    ]
    table[m2.STATE_ACCEPTED][0] = [
        {"probability": delta, "next_state": m2.STATE_NEUTRAL, "reward": _reward(b - c, reward_mode, lam)},
        {"probability": 1.0 - delta, "next_state": m2.STATE_ACCEPTED, "reward": _reward(b - c, reward_mode, lam)},
    ]
    table[m2.STATE_ACCEPTED][1] = [
        {"probability": delta, "next_state": m2.STATE_NEUTRAL, "reward": _reward(b + a, reward_mode, lam)},
        {"probability": 1.0 - delta, "next_state": m2.STATE_ACCEPTED, "reward": _reward(b + a, reward_mode, lam)},
    ]
    table[m2.STATE_STIGMATIZED][0] = [
        {"probability": eta, "next_state": m2.STATE_NEUTRAL, "reward": _reward(b2 - c, reward_mode, lam)},
        {"probability": 1.0 - eta, "next_state": m2.STATE_STIGMATIZED, "reward": _reward(b2 - c, reward_mode, lam)},
    ]
    redemption = p / 2.0
    failed = 1.0 - redemption
    table[m2.STATE_STIGMATIZED][1] = [
        {"probability": redemption, "next_state": m2.STATE_ACCEPTED, "reward": _reward(b + a, reward_mode, lam)},
        {"probability": failed * eta, "next_state": m2.STATE_NEUTRAL, "reward": _reward(a - r2, reward_mode, lam)},
        {"probability": failed * (1.0 - eta), "next_state": m2.STATE_STIGMATIZED, "reward": _reward(a - r2, reward_mode, lam)},
    ]
    return table


def transition_arrays(table: list[list[list[dict[str, float]]]]) -> tuple[np.ndarray, np.ndarray]:
    probabilities = np.zeros((len(STATE_NAMES), len(ACTION_NAMES), len(STATE_NAMES)), dtype=float)
    rewards = np.zeros_like(probabilities)
    for state, action_rows in enumerate(table):
        for action, outcomes in enumerate(action_rows):
            for outcome in outcomes:
                next_state = int(outcome["next_state"])
                probability = float(outcome["probability"])
                probabilities[state, action, next_state] += probability
                rewards[state, action, next_state] += probability * float(outcome["reward"])
    return probabilities, rewards


def q_from_v(probabilities: np.ndarray, rewards: np.ndarray, values: np.ndarray, gamma: float) -> np.ndarray:
    return rewards.sum(axis=2) + gamma * np.einsum("san,n->sa", probabilities, values)


def solve_m2_value_iteration(
    params: M2Params,
    reward_mode: str = "objective",
    gamma: float | None = None,
    tol: float = 1e-10,
    max_iter: int = 100_000,
) -> dict[str, object]:
    gamma_value = params.gamma if gamma is None else float(gamma)
    table = build_m2_transition_table(params, reward_mode=reward_mode)
    probabilities, rewards = transition_arrays(table)
    values = np.zeros(len(STATE_NAMES), dtype=float)
    residual = float("inf")
    converged = False
    iterations = 0
    for iteration in range(1, max_iter + 1):
        q_values = q_from_v(probabilities, rewards, values, gamma_value)
        next_values = q_values.max(axis=1)
        residual = float(np.max(np.abs(next_values - values)))
        values = next_values
        iterations = iteration
        if residual <= tol:
            converged = True
            break
    q_values = q_from_v(probabilities, rewards, values, gamma_value)
    max_q = q_values.max(axis=1)
    optimal_actions_all = {
        STATE_NAMES[state]: [ACTION_NAMES[action] for action in range(len(ACTION_NAMES)) if abs(q_values[state, action] - max_q[state]) <= tol]
        for state in range(len(STATE_NAMES))
    }
    chosen_actions = {state: actions[0] for state, actions in optimal_actions_all.items()}
    return {
        "states": STATE_NAMES,
        "actions": ACTION_NAMES,
        "transition_table": table,
        "transition_probabilities": probabilities,
        "expected_rewards": rewards,
        "V": values,
        "Q": q_values,
        "optimal_actions_all": optimal_actions_all,
        "chosen_actions": chosen_actions,
        "iterations": iterations,
        "residual": residual,
        "converged": converged,
        "gamma": gamma_value,
        "reward_mode": reward_mode,
        "transition_ordering": TRANSITION_ORDERING,
        "params": asdict(params),
    }


def evaluate_policy_value(
    params: M2Params,
    action_probabilities: np.ndarray,
    reward_mode: str = "objective",
    gamma: float | None = None,
) -> np.ndarray:
    gamma_value = params.gamma if gamma is None else float(gamma)
    table = build_m2_transition_table(params, reward_mode=reward_mode)
    probabilities, rewards = transition_arrays(table)
    policy_p = np.einsum("sa,san->sn", action_probabilities, probabilities)
    policy_r = np.einsum("sa,san->s", action_probabilities, rewards)
    system = np.eye(len(STATE_NAMES)) - gamma_value * policy_p
    return np.linalg.solve(system, policy_r)


def static_m0_comparator(params: M2Params) -> dict[str, float | str]:
    e_mask = params.b - params.c
    e_auth = params.p * (params.b + params.a) + (1.0 - params.p) * (params.a - params.r)
    if abs(e_mask - e_auth) <= 1e-12:
        optimal = "tie"
    elif e_auth > e_mask:
        optimal = "authentic"
    else:
        optimal = "mask"
    return {
        "E_mask": e_mask,
        "E_auth": e_auth,
        "auth_advantage": e_auth - e_mask,
        "optimal_action": optimal,
    }


def policy_from_mask_probabilities(mask_probabilities: Iterable[float]) -> np.ndarray:
    mask = np.asarray(list(mask_probabilities), dtype=float)
    if mask.shape != (len(STATE_NAMES),):
        raise ValueError("mask_probabilities must have one value per M2 state")
    if np.any(mask < 0.0) or np.any(mask > 1.0):
        raise ValueError("mask probabilities must be in [0, 1]")
    return np.column_stack([mask, 1.0 - mask])


def aggregate_learned_policy_from_diagnostics(diagnostics: dict[str, np.ndarray]) -> dict[str, object]:
    state_action_counts = np.asarray(diagnostics["state_action_counts_final"], dtype=float)
    state_visit_counts = np.asarray(diagnostics["state_visit_counts_final"], dtype=float)
    total_state_action_counts = state_action_counts.sum(axis=0)
    total_state_visit_counts = state_visit_counts.sum(axis=0)
    learned_mask_probabilities: dict[str, float | None] = {}
    learned_actions: dict[str, str | None] = {}
    for state_index, state_name in enumerate(STATE_NAMES):
        visits = float(total_state_visit_counts[state_index])
        if visits <= 0.0:
            learned_mask_probabilities[state_name] = None
            learned_actions[state_name] = None
            continue
        mask_probability = float(total_state_action_counts[state_index, 0] / visits)
        learned_mask_probabilities[state_name] = mask_probability
        learned_actions[state_name] = "mask" if mask_probability >= 0.5 else "authentic"
    return {
        "state_action_counts_total": total_state_action_counts,
        "state_visit_counts_total": total_state_visit_counts,
        "learned_mask_probabilities": learned_mask_probabilities,
        "learned_actions": learned_actions,
        "learned_mean_mask_rate_final": float(np.asarray(diagnostics["mask_rate_final"], dtype=float).mean()),
        "learned_mean_reward_final": float(np.asarray(diagnostics["reward_mean_final"], dtype=float).mean()),
    }


def classify_m2_cell(
    params: M2Params,
    diagnostics: dict[str, np.ndarray],
    *,
    reward_mode: str = "objective",
    regret_tol: float = 1e-9,
) -> dict[str, object]:
    solution = solve_m2_value_iteration(params, reward_mode=reward_mode)
    static = static_m0_comparator(params)
    learned = aggregate_learned_policy_from_diagnostics(diagnostics)
    mask_probabilities = learned["learned_mask_probabilities"]
    if any(mask_probabilities[state] is None for state in STATE_NAMES):
        learned_policy_value_neutral = None
        regret_neutral = None
        regret_available = False
    else:
        policy = policy_from_mask_probabilities(mask_probabilities[state] for state in STATE_NAMES)
        learned_policy_value_neutral = float(evaluate_policy_value(params, policy, reward_mode=reward_mode)[0])
        regret_neutral = float(solution["V"][0] - learned_policy_value_neutral)
        regret_available = True

    static_action = str(static["optimal_action"])
    dynamic_action = str(solution["chosen_actions"]["neutral"])
    learned_action = learned["learned_actions"]["neutral"]
    if static_action == "authentic" and dynamic_action == "mask":
        region = "optimal_learner_lock_in"
    elif learned_action == "mask" and dynamic_action == "authentic" and regret_available and regret_neutral is not None and regret_neutral > regret_tol:
        region = "learned_suboptimal_lock_in"
    elif static_action == "mask" and dynamic_action == "authentic":
        region = "dynamic_authenticity_overrides_static_masking"
    elif dynamic_action == "mask":
        region = "masking_optimal_and_learned_not_proven_suboptimal"
    else:
        region = "authenticity_optimal_or_learned_matches"

    return {
        "solution": solution,
        "static": static,
        "learned": learned,
        "learned_policy_value_neutral": learned_policy_value_neutral,
        "regret_neutral": regret_neutral,
        "regret_available": regret_available,
        "region": region,
        "static_neutral_action": static_action,
        "dynamic_neutral_action": dynamic_action,
        "learned_neutral_action": learned_action,
    }


def dynamic_authenticity_threshold(
    params: M2Params,
    *,
    reward_mode: str = "objective",
    state: str = "neutral",
    tol: float = 1e-8,
) -> float | None:
    state_index = STATE_NAMES.index(state)

    def q_gap(p_value: float) -> float:
        candidate = M2Params(
            p=p_value,
            eta=params.eta,
            b=params.b,
            a=params.a,
            c=params.c,
            r=params.r,
            b2=params.b2,
            r2=params.r2,
            delta=params.delta,
            gamma=params.gamma,
            lam=params.lam,
        )
        solution = solve_m2_value_iteration(candidate, reward_mode=reward_mode)
        return float(solution["Q"][state_index, 1] - solution["Q"][state_index, 0])

    low_gap = q_gap(0.0)
    high_gap = q_gap(1.0)
    if low_gap >= 0.0:
        return 0.0
    if high_gap < 0.0:
        return None
    low = 0.0
    high = 1.0
    while high - low > tol:
        midpoint = (low + high) / 2.0
        if q_gap(midpoint) >= 0.0:
            high = midpoint
        else:
            low = midpoint
    return high
