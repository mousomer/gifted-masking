from __future__ import annotations

from dataclasses import dataclass


DEFAULT_PAYOFFS = {
    "b": 1.0,
    "a": 0.6,
    "c": 0.25,
    "r": 2.0,
}


@dataclass(frozen=True)
class AgentParams:
    alpha: float = 0.1
    temp: float = 0.25
    lam: float = 1.0
    q0: float = 0.0
    gamma: float = 0.9

    def validate(self) -> "AgentParams":
        if not 0.0 < self.alpha <= 1.0:
            raise ValueError(f"alpha must be in (0, 1], got {self.alpha}")
        if self.temp <= 0.0:
            raise ValueError(f"temp must be > 0, got {self.temp}")
        if self.lam < 0.0:
            raise ValueError(f"lam must be >= 0, got {self.lam}")
        if not 0.0 <= self.gamma <= 1.0:
            raise ValueError(f"gamma must be in [0, 1], got {self.gamma}")
        return self


@dataclass(frozen=True)
class RunParams:
    n: int
    horizon: int
    final_window_fraction: float = 0.2
    seed: int = 0

    def validate(self) -> "RunParams":
        if self.n <= 0:
            raise ValueError(f"n must be > 0, got {self.n}")
        if self.horizon <= 0:
            raise ValueError(f"horizon must be > 0, got {self.horizon}")
        if not 0.0 < self.final_window_fraction <= 1.0:
            raise ValueError(
                "final_window_fraction must be in (0, 1], "
                f"got {self.final_window_fraction}"
            )
        return self
