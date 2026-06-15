from __future__ import annotations

import numpy as np

from gifted_masking.core import final_window_size, make_rng, softmax_sample, subjective_value


STATE_NEUTRAL = 0
STATE_ACCEPTED = 1
STATE_STIGMATIZED = 2


def transition_step(
    state: np.ndarray,
    action: np.ndarray,
    *,
    p: float,
    eta: float,
    b: float = 1.0,
    a: float = 0.6,
    c: float = 0.25,
    r: float = 2.0,
    b2: float = 0.5,
    r2: float = 2.5,
    delta: float = 0.02,
    outcome_uniform: np.ndarray,
    turnover_uniform: np.ndarray,
    escape_uniform: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    reward = np.empty(state.shape[0])
    next_state = state.copy()
    authentic = action == 1

    neutral = state == STATE_NEUTRAL
    reward[neutral & ~authentic] = b - c
    accepted = neutral & authentic & (outcome_uniform < p)
    rejected = neutral & authentic & (outcome_uniform >= p)
    reward[accepted] = b + a
    next_state[accepted] = STATE_ACCEPTED
    reward[rejected] = a - r
    next_state[rejected] = STATE_STIGMATIZED

    accepted_state = state == STATE_ACCEPTED
    reward[accepted_state & ~authentic] = b - c
    reward[accepted_state & authentic] = b + a
    turnover = accepted_state & (turnover_uniform < delta)
    next_state[turnover & (next_state == STATE_ACCEPTED)] = STATE_NEUTRAL

    stigmatized = state == STATE_STIGMATIZED
    reward[stigmatized & ~authentic] = b2 - c
    redeemed = stigmatized & authentic & (outcome_uniform < p / 2.0)
    failed = stigmatized & authentic & (outcome_uniform >= p / 2.0)
    reward[redeemed] = b + a
    next_state[redeemed] = STATE_ACCEPTED
    reward[failed] = a - r2
    escaped = stigmatized & (escape_uniform < eta)
    next_state[escaped & (next_state == STATE_STIGMATIZED)] = STATE_NEUTRAL
    return reward, next_state


def simulate(
    p: float,
    eta: float,
    *,
    b: float = 1.0,
    a: float = 0.6,
    c: float = 0.25,
    r: float = 2.0,
    b2: float = 0.5,
    r2: float = 2.5,
    delta: float = 0.02,
    n: int = 300,
    horizon: int = 2000,
    alpha: float = 0.1,
    temp: float = 0.25,
    lam: float = 1.0,
    q0: float = 0.0,
    gamma: float = 0.9,
    seed: int = 0,
    final_window_fraction: float = 0.2,
) -> np.ndarray:
    rng = make_rng(seed)
    q_values = np.full((n, 3, 2), float(q0))
    state = np.zeros(n, dtype=int)
    idx = np.arange(n)
    window = final_window_size(horizon, final_window_fraction)
    start = horizon - window
    mask_count = np.zeros(n)
    for t in range(horizon):
        action = softmax_sample(q_values[idx, state], temp, rng)
        reward, next_state = transition_step(
            state,
            action,
            p=p,
            eta=eta,
            b=b,
            a=a,
            c=c,
            r=r,
            b2=b2,
            r2=r2,
            delta=delta,
            outcome_uniform=rng.random(n),
            turnover_uniform=rng.random(n),
            escape_uniform=rng.random(n),
        )
        target = subjective_value(reward, lam) + gamma * q_values[idx, next_state].max(axis=1)
        q_values[idx, state, action] += alpha * (target - q_values[idx, state, action])
        state = next_state
        if t >= start:
            mask_count += action == 0
    return mask_count / window


def simulate_with_diagnostics(
    p: float,
    eta: float,
    *,
    b: float = 1.0,
    a: float = 0.6,
    c: float = 0.25,
    r: float = 2.0,
    b2: float = 0.5,
    r2: float = 2.5,
    delta: float = 0.02,
    n: int = 300,
    horizon: int = 2000,
    alpha: float = 0.1,
    temp: float = 0.25,
    lam: float = 1.0,
    q0: float = 0.0,
    gamma: float = 0.9,
    seed: int = 0,
    final_window_fraction: float = 0.2,
) -> dict[str, np.ndarray]:
    rng = make_rng(seed)
    q_values = np.full((n, 3, 2), float(q0))
    state = np.zeros(n, dtype=int)
    idx = np.arange(n)
    window = final_window_size(horizon, final_window_fraction)
    start = horizon - window
    mask_count = np.zeros(n)
    state_action_counts = np.zeros((n, 3, 2), dtype=int)
    state_visit_counts = np.zeros((n, 3), dtype=int)
    reward_sum = np.zeros(n)
    for t in range(horizon):
        current_state = state.copy()
        action = softmax_sample(q_values[idx, current_state], temp, rng)
        reward, next_state = transition_step(
            current_state,
            action,
            p=p,
            eta=eta,
            b=b,
            a=a,
            c=c,
            r=r,
            b2=b2,
            r2=r2,
            delta=delta,
            outcome_uniform=rng.random(n),
            turnover_uniform=rng.random(n),
            escape_uniform=rng.random(n),
        )
        target = subjective_value(reward, lam) + gamma * q_values[idx, next_state].max(axis=1)
        q_values[idx, current_state, action] += alpha * (target - q_values[idx, current_state, action])
        if t >= start:
            mask_count += action == 0
            reward_sum += reward
            for state_id in (STATE_NEUTRAL, STATE_ACCEPTED, STATE_STIGMATIZED):
                in_state = current_state == state_id
                state_visit_counts[in_state, state_id] += 1
                state_action_counts[in_state & (action == 0), state_id, 0] += 1
                state_action_counts[in_state & (action == 1), state_id, 1] += 1
        state = next_state
    return {
        "mask_rate_final": mask_count / window,
        "state_action_counts_final": state_action_counts,
        "state_visit_counts_final": state_visit_counts,
        "final_state": state.copy(),
        "reward_mean_final": reward_sum / window,
    }
