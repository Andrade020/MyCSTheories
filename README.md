# MyCSTheories

[![CI](https://github.com/Andrade020/MyCSTheories/actions/workflows/ci.yml/badge.svg)](https://github.com/Andrade020/MyCSTheories/actions/workflows/ci.yml)

Experiments in the theory of computation and in numerical computing for finance. Every claim here is backed by a test: if a result is stated, `pytest` checks it.

```bash
pip install -e ".[dev]"
pytest -q
```

## Part I - Models of computation

| Module | What it shows |
| --- | --- |
| [`turing.py`](src/mct/turing.py) | A deterministic Turing machine simulator (sparse, two-way infinite tape) with three machines: binary increment, palindrome decider over `{a,b}`, and the 3-state busy beaver (6 ones in 14 steps, verified) |
| [`brainfuck.py`](src/mct/brainfuck.py) | A Brainfuck interpreter with a precomputed jump table, step limits and tape-bounds errors. Brainfuck is Turing-complete, so it is a compact universality playground |
| [`automata.py`](src/mct/automata.py) | Elementary cellular automata. Rule 90 draws the Sierpinski triangle (row `2^k - 1` has `2^k` live cells); Rule 110 is Turing-complete (Cook, 2004) |
| [`BF/`](BF) | Earlier Brainfuck experiments, including an approximate linear regression written in Brainfuck |

```python
from mct.turing import binary_increment
binary_increment().run("1011").tape_str()   # '1100'
```

Rule 90 after 15 steps:

```
...............#...............
..............#.#..............
.............#...#.............
............#.#.#.#............
...........#.......#...........
```

## Part II - Computing with numbers

Theory only matters when the machine disagrees with the maths. These modules are about *where it disagrees*.

**Floating-point summation** ([`numerics.py`](src/mct/numerics.py)). Summing `0.1` one million times: naive summation accumulates `O(n*eps)` error, pairwise (what NumPy does) `O(eps*log n)`, and Kahan compensated summation `O(eps)`. The tests assert Kahan is at least 1000x more accurate than the naive loop.

**Catastrophic cancellation.** For data with mean `1e9` and standard deviation 1, the textbook formula `E[X^2] - E[X]^2` is off by more than 0.1%, while Welford's one-pass algorithm matches the true variance to 6 digits.

**Option pricing and convergence rates** ([`pricing.py`](src/mct/pricing.py)). A European call (`S=K=100, r=5%, sigma=20%, T=1`, Black-Scholes price 10.4506) priced three ways:

| Method | Cost | Observed error |
| --- | --- | --- |
| Cox-Ross-Rubinstein tree | `O(n^2)` | `n=25: 0.070`, `n=100: 0.020`, `n=400: 0.0050`, `n=1600: 0.0013` (error ~ `1/n`) |
| Monte Carlo | `O(N)` | standard error `N=1e3: 0.44`, `1e4: 0.15`, `1e5: 0.047`, `1e6: 0.015` (~ `1/sqrt(N)`) |
| Monte Carlo + antithetic variates | `O(N)` | same rate, standard error roughly halved |

**Randomness as compressibility** ([`randomness.py`](src/mct/randomness.py)). Kolmogorov complexity is uncomputable, but a compressor gives an upper bound. Output of `os.urandom` does not compress (ratio > 0.99); a weak linear congruential generator compresses below 50%. A cheap first check for suspicious "random" sequences, such as lottery draws.

## Layout

```
src/mct/    the package (turing, brainfuck, automata, numerics, pricing, randomness)
tests/      pytest suite (25 tests), run in CI on Python 3.10 and 3.12
BF/         early Brainfuck scripts
```

## License

MIT
