from __future__ import annotations

import numpy as np

from gifted_masking.core import final_window_size, make_rng, softmax_sample, subjective_value


def group_probabilities(k_groups: int, p_good: float, p_bad: float, good_group: int = 0) -> np.ndarray:
    if k_groups <= 0:
        raise ValueError(f"k_groups must be > 0, got {k_groups}")
    if not 0 <= good_group < k_groups:
        raise ValueError(f"good_group must be in [0, {k_groups}), got {good_group}")
    probs = np.full(k_groups, p_bad)
    probs[good_group] = p_good
    return probs


def decode_action(action: np.ndarray | int) -> tuple[np.ndarray, np.ndarray]:
    action = np.asarray(action)
    group = action // 2
    authentic = (action % 2) == 1
    return group, authentic


def expected_reward_for_action(
    action: np.ndarray | int,
    *,
    k_groups: int,
    p_good: float = 0.85,
    p_bad: float = 0.2,
    bf: float = 0.0,
    b: float = 1.0,
    a: float = 0.6,
    c: float = 0.25,
    r: float = 2.0,
    good_group: int = 0,
) -> np.ndarray:
    group, authentic = decode_action(action)
    p_vec = group_probabilities(k_groups, p_good=p_good, p_bad=p_bad, good_group=good_group)
    group = np.asarray(group)
    authentic = np.asarray(authentic)
    reward = np.full(group.shape, b - c, dtype=float)
    auth_reward = p_vec[group] * (b + a - bf * (group == good_group)) + (1.0 - p_vec[group]) * (a - r)
    reward = np.where(authentic, auth_reward, reward)
    return reward


def simulate(
    k_groups: int,
    *,
    p_good: float = 0.85,
    p_bad: float = 0.2,
    bf: float = 0.0,
    b: float = 1.0,
    a: float = 0.6,
    c: float = 0.25,
    r: float = 2.0,
    n: int = 400,
    horizon: int = 2000,
    alpha: float = 0.1,
    temp: float = 0.25,
    lam: float = 1.0,
    q0: float = 0.0,
    seed: int = 0,
    final_window_fraction: float = 0.2,
    good_group: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = make_rng(seed)
    p_vec = group_probabilities(k_groups, p_good=p_good, p_bad=p_bad, good_group=good_group)
    q_values = np.full((n, 2 * k_groups), float(q0))
    idx = np.arange(n)
    window = final_window_size(horizon, final_window_fraction)
    start = horizon - window
    arm_count = np.zeros((n, 2 * k_groups))
    mask_count = np.zeros(n)
    optimal_action = 2 * good_group + 1
    for t in range(horizon):
        action = softmax_sample(q_values, temp, rng)
        group, authentic = decode_action(action)
        accept = rng.random(n) < p_vec[group]
        reward = np.where(
            ~authentic,
            b - c,
            np.where(accept, b + a - bf * (group == good_group), a - r),
        )
        q_values[idx, action] += alpha * (subjective_value(reward, lam) - q_values[idx, action])
        if t >= start:
            arm_count[idx, action] += 1
            mask_count += ~authentic
    modal = arm_count.argmax(axis=1)
    return modal == optimal_action, mask_count / window, modal


def simulate_hierarchical(
    k_groups: int,
    *,
    p_good: float = 0.85,
    p_bad: float = 0.2,
    bf: float = 0.0,
    b: float = 1.0,
    a: float = 0.6,
    c: float = 0.25,
    r: float = 2.0,
    n: int = 400,
    horizon: int = 2000,
    alpha: float = 0.1,
    temp: float = 0.25,
    lam: float = 1.0,
    q0: float = 0.0,
    seed: int = 0,
    final_window_fraction: float = 0.2,
    good_group: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = make_rng(seed)
    p_vec = group_probabilities(k_groups, p_good=p_good, p_bad=p_bad, good_group=good_group)
    q_groups = np.full((n, k_groups), float(q0))
    q_behaviors = np.full((n, k_groups, 2), float(q0))
    idx = np.arange(n)
    window = final_window_size(horizon, final_window_fraction)
    start = horizon - window
    pair_count = np.zeros((n, 2 * k_groups))
    mask_count = np.zeros(n)
    optimal_action = 2 * good_group + 1
    for t in range(horizon):
        group = softmax_sample(q_groups, temp, rng)
        behavior = softmax_sample(q_behaviors[idx, group], temp, rng)
        authentic = behavior == 1
        accept = rng.random(n) < p_vec[group]
        reward = np.where(
            ~authentic,
            b - c,
            np.where(accept, b + a - bf * (group == good_group), a - r),
        )
        subjective = subjective_value(reward, lam)
        q_groups[idx, group] += alpha * (subjective - q_groups[idx, group])
        q_behaviors[idx, group, behavior] += (
            alpha * (subjective - q_behaviors[idx, group, behavior])
        )
        if t >= start:
            action = 2 * group + behavior
            pair_count[idx, action] += 1
            mask_count += ~authentic
    modal = pair_count.argmax(axis=1)
    return modal == optimal_action, mask_count / window, modal


def simulate_global_mask(
    k_groups: int,
    *,
    p_good: float = 0.85,
    p_bad: float = 0.2,
    bf: float = 0.0,
    b: float = 1.0,
    a: float = 0.6,
    c: float = 0.25,
    r: float = 2.0,
    n: int = 400,
    horizon: int = 2000,
    alpha: float = 0.1,
    temp: float = 0.25,
    lam: float = 1.0,
    q0: float = 0.0,
    seed: int = 0,
    final_window_fraction: float = 0.2,
    good_group: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = make_rng(seed)
    p_vec = group_probabilities(k_groups, p_good=p_good, p_bad=p_bad, good_group=good_group)
    q_values = np.full((n, k_groups + 1), float(q0))
    idx = np.arange(n)
    window = final_window_size(horizon, final_window_fraction)
    start = horizon - window
    action_count = np.zeros((n, k_groups + 1))
    mask_count = np.zeros(n)
    optimal_action = 1 + good_group
    for t in range(horizon):
        action = softmax_sample(q_values, temp, rng)
        authentic = action != 0
        group = np.maximum(action - 1, 0)
        accept = rng.random(n) < p_vec[group]
        reward = np.where(
            ~authentic,
            b - c,
            np.where(accept, b + a - bf * (group == good_group), a - r),
        )
        q_values[idx, action] += alpha * (subjective_value(reward, lam) - q_values[idx, action])
        if t >= start:
            action_count[idx, action] += 1
            mask_count += ~authentic
    modal = action_count.argmax(axis=1)
    return modal == optimal_action, mask_count / window, modal


def simulate_fixed_good_pond(
    *,
    p_good: float = 0.85,
    bf: float = 0.0,
    b: float = 1.0,
    a: float = 0.6,
    c: float = 0.25,
    r: float = 2.0,
    n: int = 400,
    horizon: int = 2000,
    alpha: float = 0.1,
    temp: float = 0.25,
    lam: float = 1.0,
    q0: float = 0.0,
    seed: int = 0,
    final_window_fraction: float = 0.2,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = make_rng(seed)
    q_values = np.full((n, 2), float(q0))
    idx = np.arange(n)
    window = final_window_size(horizon, final_window_fraction)
    start = horizon - window
    action_count = np.zeros((n, 2))
    mask_count = np.zeros(n)
    optimal_action = 1
    for t in range(horizon):
        action = softmax_sample(q_values, temp, rng)
        authentic = action == 1
        accept = rng.random(n) < p_good
        reward = np.where(
            ~authentic,
            b - c,
            np.where(accept, b + a - bf, a - r),
        )
        q_values[idx, action] += alpha * (subjective_value(reward, lam) - q_values[idx, action])
        if t >= start:
            action_count[idx, action] += 1
            mask_count += ~authentic
    modal = action_count.argmax(axis=1)
    return modal == optimal_action, mask_count / window, modal
