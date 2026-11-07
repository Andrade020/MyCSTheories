"""Floating-point pitfalls that matter in finance, and their fixes."""
from __future__ import annotations

import math
from collections.abc import Iterable


def naive_sum(xs: Iterable[float]) -> float:
    total = 0.0
    for x in xs:
        total += x
    return total


def kahan_sum(xs: Iterable[float]) -> float:
    """Compensated summation: error O(eps) independent of n (vs O(n*eps) naive)."""
    total = comp = 0.0
    for x in xs:
        y = x - comp
        t = total + y
        comp = (t - total) - y
        total = t
    return total


def pairwise_sum(xs: list[float]) -> float:
    """Divide-and-conquer summation (what NumPy uses): error O(eps * log n)."""
    n = len(xs)
    if n <= 8:
        return naive_sum(xs)
    mid = n // 2
    return pairwise_sum(xs[:mid]) + pairwise_sum(xs[mid:])


def exact_sum(xs: Iterable[float]) -> float:
    """Correctly rounded sum, used as ground truth."""
    return math.fsum(xs)


def welford_variance(xs: Iterable[float]) -> float:
    """Single-pass, numerically stable sample variance."""
    n, mean, m2 = 0, 0.0, 0.0
    for x in xs:
        n += 1
        d = x - mean
        mean += d / n
        m2 += d * (x - mean)
    if n < 2:
        raise ValueError("need at least two observations")
    return m2 / (n - 1)


def naive_variance(xs: list[float]) -> float:
    """E[X^2] - E[X]^2: suffers catastrophic cancellation when mean >> std."""
    n = len(xs)
    s, s2 = sum(xs), sum(x * x for x in xs)
    return (s2 - s * s / n) / (n - 1)
