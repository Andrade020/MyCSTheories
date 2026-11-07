"""Elementary cellular automata. Rule 110 is Turing-complete (Cook, 2004)."""
from __future__ import annotations

import numpy as np


def step(cells: np.ndarray, rule: int) -> np.ndarray:
    """One update with periodic boundary conditions."""
    table = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    idx = (np.roll(cells, 1) << 2) | (cells << 1) | np.roll(cells, -1)
    return table[idx]


def evolve(rule: int, width: int, steps: int, seed: np.ndarray | None = None) -> np.ndarray:
    """Returns a (steps+1, width) array; default seed is a single live cell."""
    if seed is None:
        seed = np.zeros(width, dtype=np.uint8)
        seed[width // 2] = 1
    rows = [seed.astype(np.uint8)]
    for _ in range(steps):
        rows.append(step(rows[-1], rule))
    return np.array(rows)


def render(grid: np.ndarray) -> str:
    return "\n".join("".join("#" if c else "." for c in row) for row in grid)
