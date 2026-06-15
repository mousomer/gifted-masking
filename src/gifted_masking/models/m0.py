from __future__ import annotations

import numpy as np

from gifted_masking.core import final_window_size, make_rng, softmax_sample, subjective_value


def expected_rewards(p: float, b: float = 1.0, a: float = 0.6, c: float = 0.25, r: float = 2.0) -> tuple[float, float]:
    mask = b - c
    authentic = p * (b + a) + (1.0 - p) * (a - r)
    return mask, authentic


def expected_gap(p: float, b: float, a: float, c: float, r: float) -> float:
    mask, authentic = expected_rewards(p, b=b, a=a, c=c, r=r)
    return authentic - mask


def objective_indifference_r(p: np.ndarray | float, b: float = 1.0, a: float = 0.6, c: float = 0.25) -> np.ndarray | float:
    return (a + c) / (1.0 - p) - b


def subjective_indifference_r(
    p: np.ndarray | float,
    lam: float,
    b: float = 1.0,
    a: float = 0.6,
    c: float = 0.25,
) -> np.ndarray | float:
    return a - ((b - c) - p * (b + a)) / (lam * (1.0 - p))


def simulate(
    p: float,
    *,
    b: float = 1.0,
    a: float = 0.6,
    c: float = 0.25,
    r: float = 2.0,
    n: int = 300,
    horizon: int = 1500,
    alpha: float = 0.1,
    temp: float = 0.25,
    lam: float = 1.0,
    q0: float = 0.0,
    seed: int = 0,
    final_window_fraction: float = 0.2,
) -> np.ndarray:
    rng = make_rng(seed)
    q_values = np.full((n, 2), float(q0))
    idx = np.arange(n)
    window = final_window_size(horizon, final_window_fraction)
    start = horizon - window
    mask_count = np.zeros(n)
    for t in range(horizon):
        action = softmax_sample(q_values, temp, rng)
        accept = rng.random(n) < p
        reward = np.where(action == 0, b - c, np.where(accept, b + a, a - r))
        q_values[idx, action] += alpha * (subjective_value(reward, lam) - q_values[idx, action])
        if t >= start:
            mask_count += action == 0
    return mask_count / window
