from __future__ import annotations

import numpy as np

from gifted_masking.core import final_window_size, make_rng, softmax_sample, subjective_value


def update_receptivity(
    p_t: np.ndarray,
    authentic: np.ndarray,
    accepted: np.ndarray,
    *,
    km: float,
    ka: float,
    kr: float,
    p_min: float,
    p_max: float,
) -> np.ndarray:
    updated = p_t.copy()
    updated[authentic & accepted] += ka * (p_max - updated[authentic & accepted])
    updated[authentic & ~accepted] -= kr * (updated[authentic & ~accepted] - p_min)
    updated[~authentic] -= km * (updated[~authentic] - p_min)
    return np.clip(updated, p_min, p_max)


def simulate(
    p0: float,
    km: float,
    *,
    ka: float = 0.12,
    kr: float = 0.04,
    p_min: float = 0.05,
    p_max: float = 0.95,
    b: float = 1.0,
    a: float = 0.6,
    c: float = 0.25,
    r: float = 2.0,
    n: int = 300,
    horizon: int = 2000,
    alpha: float = 0.1,
    temp: float = 0.25,
    lam: float = 1.0,
    q0: float = 0.0,
    seed: int = 0,
    ntraj: int = 0,
    final_window_fraction: float = 0.2,
) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
    rng = make_rng(seed)
    q_values = np.full((n, 2), float(q0))
    p_t = np.clip(np.full(n, float(p0)), p_min, p_max)
    idx = np.arange(n)
    window = final_window_size(horizon, final_window_fraction)
    start = horizon - window
    mask_count = np.zeros(n)
    trajectories = np.empty((horizon, ntraj)) if ntraj else None
    for t in range(horizon):
        action = softmax_sample(q_values, temp, rng)
        authentic = action == 1
        accepted = rng.random(n) < p_t
        reward = np.where(~authentic, b - c, np.where(accepted, b + a, a - r))
        q_values[idx, action] += alpha * (subjective_value(reward, lam) - q_values[idx, action])
        p_t = update_receptivity(
            p_t,
            authentic,
            accepted,
            km=km,
            ka=ka,
            kr=kr,
            p_min=p_min,
            p_max=p_max,
        )
        if trajectories is not None:
            trajectories[t] = p_t[:ntraj]
        if t >= start:
            mask_count += ~authentic
    return mask_count / window, p_t, trajectories


def simulate_from_state(
    p_t: np.ndarray,
    q_values: np.ndarray,
    km: float,
    *,
    ka: float = 0.12,
    kr: float = 0.04,
    p_min: float = 0.05,
    p_max: float = 0.95,
    b: float = 1.0,
    a: float = 0.6,
    c: float = 0.25,
    r: float = 2.0,
    alpha: float = 0.1,
    temp: float = 0.25,
    lam: float = 1.0,
    seed: int = 0,
    ntraj: int = 0,
    horizon: int = 2000,
    final_window_fraction: float = 0.2,
) -> tuple[np.ndarray, np.ndarray, np.ndarray | None, np.ndarray]:
    rng = make_rng(seed)
    q_state = q_values.copy()
    p_state = np.clip(p_t.copy(), p_min, p_max)
    idx = np.arange(p_state.shape[0])
    window = final_window_size(horizon, final_window_fraction)
    start = horizon - window
    mask_count = np.zeros(p_state.shape[0])
    trajectories = np.empty((horizon, ntraj)) if ntraj else None
    for t in range(horizon):
        action = softmax_sample(q_state, temp, rng)
        authentic = action == 1
        accepted = rng.random(p_state.shape[0]) < p_state
        reward = np.where(~authentic, b - c, np.where(accepted, b + a, a - r))
        q_state[idx, action] += alpha * (subjective_value(reward, lam) - q_state[idx, action])
        p_state = update_receptivity(
            p_state,
            authentic,
            accepted,
            km=km,
            ka=ka,
            kr=kr,
            p_min=p_min,
            p_max=p_max,
        )
        if trajectories is not None:
            trajectories[t] = p_state[:ntraj]
        if t >= start:
            mask_count += ~authentic
    return mask_count / window, p_state, trajectories, q_state


def hysteresis_experiment(
    p0: float,
    km_values: np.ndarray,
    *,
    ka: float = 0.12,
    kr: float = 0.04,
    p_min: float = 0.05,
    p_max: float = 0.95,
    b: float = 1.0,
    a: float = 0.6,
    c: float = 0.25,
    r: float = 2.0,
    n: int = 300,
    horizon: int = 600,
    alpha: float = 0.1,
    temp: float = 0.25,
    lam: float = 1.0,
    q0: float = 0.0,
    seed: int = 0,
    final_window_fraction: float = 0.2,
) -> dict[str, np.ndarray]:
    q_state = np.full((n, 2), float(q0))
    p_state = np.clip(np.full(n, float(p0)), p_min, p_max)
    up_mask = []
    up_p = []
    down_mask = []
    down_p = []

    for offset, km in enumerate(km_values):
        mask_rate, p_state, _, q_state = simulate_from_state(
            p_state,
            q_state,
            km,
            ka=ka,
            kr=kr,
            p_min=p_min,
            p_max=p_max,
            b=b,
            a=a,
            c=c,
            r=r,
            alpha=alpha,
            temp=temp,
            lam=lam,
            seed=seed + offset,
            horizon=horizon,
            final_window_fraction=final_window_fraction,
        )
        up_mask.append(mask_rate.mean())
        up_p.append(p_state.mean())

    for offset, km in enumerate(km_values[::-1]):
        mask_rate, p_state, _, q_state = simulate_from_state(
            p_state,
            q_state,
            km,
            ka=ka,
            kr=kr,
            p_min=p_min,
            p_max=p_max,
            b=b,
            a=a,
            c=c,
            r=r,
            alpha=alpha,
            temp=temp,
            lam=lam,
            seed=seed + len(km_values) + offset,
            horizon=horizon,
            final_window_fraction=final_window_fraction,
        )
        down_mask.append(mask_rate.mean())
        down_p.append(p_state.mean())

    return {
        "km_up": km_values.copy(),
        "km_down": km_values[::-1].copy(),
        "mask_up": np.asarray(up_mask),
        "mask_down": np.asarray(down_mask),
        "p_up": np.asarray(up_p),
        "p_down": np.asarray(down_p),
    }
