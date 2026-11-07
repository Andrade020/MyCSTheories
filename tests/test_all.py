import math
import os

import numpy as np
import pytest

from mct import automata, brainfuck, numerics, pricing, randomness
from mct.turing import TuringMachine, binary_increment, busy_beaver_3, palindrome_checker


@pytest.mark.parametrize("n", [0, 1, 5, 7, 255, 1023])
def test_binary_increment(n):
    assert binary_increment().run(format(n, "b")).tape_str() == format(n + 1, "b")


@pytest.mark.parametrize("word,ok", [("", True), ("a", True), ("abba", True), ("ababa", True),
                                     ("ab", False), ("aab", False), ("abab", False)])
def test_palindrome(word, ok):
    assert palindrome_checker().run(word).state == ("accept" if ok else "reject")


def test_busy_beaver_3():
    res = busy_beaver_3().run("")
    assert res.halted and res.count("1") == 6 and res.steps == 14


def test_step_limit_marks_not_halted():
    loop = TuringMachine({("q0", "_"): ("q0", "_", "R")})
    assert not loop.run("", max_steps=100).halted


HELLO = ("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++."
         ">>.<-.<.+++.------.--------.>>+.")


def test_brainfuck_hello():
    assert brainfuck.run(HELLO).startswith("Hello World")


def test_brainfuck_cat_and_errors():
    assert brainfuck.run(",[.,]", stdin="abc") == "abc"
    with pytest.raises(brainfuck.BrainfuckError):
        brainfuck.run("[")
    with pytest.raises(brainfuck.BrainfuckError):
        brainfuck.run("+[]", max_steps=1000)


def test_rule_90_is_sierpinski():
    grid = automata.evolve(90, 65, 31)
    assert grid[1].sum() == 2 and grid[3].sum() == 4 and grid[7].sum() == 8
    assert grid[15].sum() == 16  # row 2^k - 1 has 2^k live cells


def test_rule_110_known_row():
    seed = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=np.uint8)
    assert automata.evolve(110, 9, 1, seed=seed)[1].tolist() == [0, 0, 0, 0, 0, 0, 0, 1, 1]


def test_summation_accuracy():
    xs = [0.1] * 1_000_000
    truth = numerics.exact_sum(xs)
    err_naive = abs(numerics.naive_sum(xs) - truth)
    assert abs(numerics.kahan_sum(xs) - truth) < err_naive / 1000
    assert abs(numerics.pairwise_sum(xs) - truth) < err_naive


def test_variance_cancellation():
    rng = np.random.default_rng(0)
    xs = (1e9 + rng.standard_normal(10_000)).tolist()
    true = float(np.var(np.array(xs) - 1e9, ddof=1))
    assert numerics.welford_variance(xs) == pytest.approx(true, rel=1e-6)
    assert abs(numerics.naive_variance(xs) - true) / true > 1e-3  # naive formula breaks


def test_bs_value():
    assert pricing.bs_call(100, 100, 0.05, 0.2, 1) == pytest.approx(10.4506, abs=1e-4)


def test_binomial_converges():
    exact = pricing.bs_call(100, 100, 0.05, 0.2, 1)
    e_small = abs(pricing.crr_call(100, 100, 0.05, 0.2, 1, 50) - exact)
    e_big = abs(pricing.crr_call(100, 100, 0.05, 0.2, 1, 800) - exact)
    assert e_big < e_small and e_big < 0.01


def test_mc_within_error_and_antithetic_helps():
    exact = pricing.bs_call(100, 100, 0.05, 0.2, 1)
    p, se = pricing.mc_call(100, 100, 0.05, 0.2, 1, 200_000)
    assert abs(p - exact) < 4 * se
    _, se_a = pricing.mc_call(100, 100, 0.05, 0.2, 1, 200_000, antithetic=True)
    assert se_a < se and math.isfinite(se_a)


def test_compression_detects_structure():
    assert randomness.compression_ratio(os.urandom(5000)) > 0.99
    assert randomness.compression_ratio(randomness.lcg(1, 5000)) < 0.5
