"""Kolmogorov-complexity-flavoured randomness check via compression.

K(x) is uncomputable, but a compressor gives an upper bound: random data is
incompressible, structured data is not. A cheap sanity check for sequences such
as lottery draws or the output of a PRNG.
"""
from __future__ import annotations

import zlib


def compression_ratio(data: bytes, level: int = 9) -> float:
    """len(compressed) / len(original); ~1 (or above) means no detectable structure."""
    if not data:
        raise ValueError("empty input")
    return len(zlib.compress(data, level)) / len(data)


def lcg(seed: int, n: int, a: int = 1103515245, c: int = 12345, m: int = 2**31) -> bytes:
    """A deliberately weak PRNG: the low byte of this LCG has period 256."""
    out, x = bytearray(), seed
    for _ in range(n):
        x = (a * x + c) % m
        out.append(x & 0xFF)
    return bytes(out)
