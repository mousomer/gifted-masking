from __future__ import annotations

import numpy as np

from gifted_masking.core import final_window_size, make_rng, softmax_sample, subjective_value


def disclosure_levels(levels: int) -> np.ndarray:
    if levels < 2:
        raise ValueError(f"levels must be >= 2, got {levels}")
    grid = np.linspace(0.0, 1.0, levels)
    if grid[0] != 0.0 or grid[-1] != 1.0:
        raise AssertionError("disclosure grid must include exactly 0 and 1")
    return grid


def acceptance_probability(p: float, disclosure: np.ndarray) -> np.ndarray:
    prob = 1.0 - (1.0 - p) * disclosure
    if np.any(prob < 0.0) or np.any(prob > 1.0):
        raise ValueError("acceptance probabilities must stay in [0, 1]")
    return prob


def expected_reward(disclosure: np.ndarray | float, p: float, b: float = 1.0, a: float = 0.6, c: float = 0.25, r: float = 2.0) -> np.ndarray | float:
    disclosure = np.asarray(disclosure)
    return b - c + disclosure * (a + c - (1.0 - p) * (b + r))


def simulate(
    p: float,
    *,
    levels: int = 5,
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
    grid = disclosure_levels(levels)
    q_values = np.full((n, levels), float(q0))
    idx = np.arange(n)
    window = final_window_size(horizon, final_window_fraction)
    start = horizon - window
    disclosure_sum = np.zeros(n)
    for t in range(horizon):
        action = softmax_sample(q_values, temp, rng)
        disclosure = grid[action]
        accept = rng.random(n) < acceptance_probability(p, disclosure)
        base = a * disclosure - c * (1.0 - disclosure)
        reward = np.where(accept, base + b, base - r)
        q_values[idx, action] += alpha * (subjective_value(reward, lam) - q_values[idx, action])
        if t >= start:
            disclosure_sum += disclosure
    return disclosure_sum / window
