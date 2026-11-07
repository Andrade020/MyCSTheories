"""European call pricing three ways, to study convergence rates.

* Black-Scholes closed form (ground truth)
* Cox-Ross-Rubinstein binomial tree: O(n^2) work, error ~ O(1/n) (oscillating)
* Monte Carlo: O(N) work, error ~ O(1/sqrt(N)); antithetic variates cut variance
"""
from __future__ import annotations

import math

import numpy as np


def _ncdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2))


def bs_call(s: float, k: float, r: float, sigma: float, t: float) -> float:
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    return s * _ncdf(d1) - k * math.exp(-r * t) * _ncdf(d2)


def crr_call(s: float, k: float, r: float, sigma: float, t: float, n: int) -> float:
    dt = t / n
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)
    disc = math.exp(-r * dt)
    j = np.arange(n + 1)
    values = np.maximum(s * u**j * d ** (n - j) - k, 0.0)
    for _ in range(n):
        values = disc * (p * values[1:] + (1 - p) * values[:-1])
    return float(values[0])


def mc_call(s: float, k: float, r: float, sigma: float, t: float, n: int,
            antithetic: bool = False, seed: int = 0) -> tuple[float, float]:
    """Returns (price, standard error)."""
    rng = np.random.default_rng(seed)
    z = rng.standard_normal(n)
    drift, vol = (r - 0.5 * sigma**2) * t, sigma * math.sqrt(t)
    pay = np.maximum(s * np.exp(drift + vol * z) - k, 0.0)
    if antithetic:
        pay = 0.5 * (pay + np.maximum(s * np.exp(drift - vol * z) - k, 0.0))
    disc = math.exp(-r * t)
    return float(disc * pay.mean()), float(disc * pay.std(ddof=1) / math.sqrt(n))
