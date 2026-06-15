from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def make_rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def final_window_size(horizon: int, fraction: float) -> int:
    if horizon <= 0:
        raise ValueError(f"horizon must be > 0, got {horizon}")
    if not 0.0 < fraction <= 1.0:
        raise ValueError(f"fraction must be in (0, 1], got {fraction}")
    return max(1, int(math.ceil(horizon * fraction)))


def subjective_value(reward: np.ndarray, lam: float) -> np.ndarray:
    if lam < 0.0:
        raise ValueError(f"lam must be >= 0, got {lam}")
    return np.where(reward < 0.0, lam * reward, reward)


def softmax_probabilities(q_values: np.ndarray, temp: float) -> np.ndarray:
    if temp <= 0.0:
        raise ValueError(f"temp must be > 0, got {temp}")
    z = q_values / temp
    z = z - z.max(axis=1, keepdims=True)
    probs = np.exp(z)
    probs /= probs.sum(axis=1, keepdims=True)
    return probs


def softmax_sample(q_values: np.ndarray, temp: float, rng: np.random.Generator) -> np.ndarray:
    probs = softmax_probabilities(q_values, temp)
    u = rng.random((q_values.shape[0], 1))
    return (u > probs.cumsum(axis=1)).sum(axis=1)


def standard_error(values: np.ndarray) -> float:
    if values.size < 2:
        return 0.0
    return float(values.std(ddof=1) / math.sqrt(values.size))


def bootstrap_ci(
    values: np.ndarray,
    rng: np.random.Generator,
    draws: int = 500,
    alpha: float = 0.05,
) -> tuple[float, float]:
    if values.size == 0:
        raise ValueError("values must not be empty")
    samples = rng.choice(values, size=(draws, values.size), replace=True).mean(axis=1)
    lo = float(np.quantile(samples, alpha / 2.0))
    hi = float(np.quantile(samples, 1.0 - alpha / 2.0))
    return lo, hi


@dataclass(frozen=True)
class EstimateSummary:
    estimate: float
    standard_error: float
    ci_low: float
    ci_high: float


def summarize_mean(values: np.ndarray, seed: int) -> EstimateSummary:
    rng = make_rng(seed)
    estimate = float(values.mean())
    stderr = standard_error(values)
    ci_low, ci_high = bootstrap_ci(values, rng=rng)
    return EstimateSummary(
        estimate=estimate,
        standard_error=stderr,
        ci_low=ci_low,
        ci_high=ci_high,
    )
