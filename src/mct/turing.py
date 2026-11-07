"""Deterministic single-tape Turing machine simulator.

A machine is a transition table ``{(state, symbol): (new_state, write, move)}``
with ``move`` in ``{"L", "R", "N"}``. The tape is unbounded in both directions
(stored sparsely) and blank cells read as ``blank``.
"""
from __future__ import annotations

from dataclasses import dataclass, field

Table = dict[tuple[str, str], tuple[str, str, str]]


@dataclass
class Result:
    state: str
    tape: dict[int, str]
    head: int
    steps: int
    halted: bool
    blank: str = "_"

    def tape_str(self) -> str:
        """Tape contents from the leftmost to the rightmost non-blank cell."""
        cells = {i: s for i, s in self.tape.items() if s != self.blank}
        if not cells:
            return ""
        return "".join(cells.get(i, self.blank) for i in range(min(cells), max(cells) + 1))

    def count(self, symbol: str) -> int:
        return sum(1 for s in self.tape.values() if s == symbol)


@dataclass
class TuringMachine:
    table: Table
    start: str = "q0"
    halt_states: frozenset[str] = field(default_factory=lambda: frozenset({"halt"}))
    blank: str = "_"

    def run(self, tape: str = "", max_steps: int = 1_000_000) -> Result:
        cells = {i: s for i, s in enumerate(tape) if s != self.blank}
        state, head, steps = self.start, 0, 0
        while state not in self.halt_states and steps < max_steps:
            key = (state, cells.get(head, self.blank))
            if key not in self.table:  # no rule applies: halt in place
                return Result(state, cells, head, steps, True, self.blank)
            state, write, move = self.table[key]
            if write == self.blank:
                cells.pop(head, None)
            else:
                cells[head] = write
            head += {"L": -1, "R": 1, "N": 0}[move]
            steps += 1
        return Result(state, cells, head, steps, state in self.halt_states, self.blank)


# --- example machines -------------------------------------------------------

def binary_increment() -> TuringMachine:
    """Adds 1 to a binary number written MSB-first; head starts on the first digit."""
    t: Table = {}
    for s in "01":
        t[("q0", s)] = ("q0", s, "R")          # run to the right end
    t[("q0", "_")] = ("q1", "_", "L")
    t[("q1", "1")] = ("q1", "0", "L")          # carry propagates
    t[("q1", "0")] = ("halt", "1", "N")
    t[("q1", "_")] = ("halt", "1", "N")        # overflow: new leading 1
    return TuringMachine(t)


def palindrome_checker() -> TuringMachine:
    """Accepts palindromes over {a, b}: ends in ``accept`` or ``reject``."""
    t: Table = {("q0", "_"): ("accept", "_", "N")}
    for c, seek, check in (("a", "seek_a", "check_a"), ("b", "seek_b", "check_b")):
        t[("q0", c)] = (seek, "_", "R")            # erase leftmost, remember it
        t[(seek, "a")] = (seek, "a", "R")
        t[(seek, "b")] = (seek, "b", "R")
        t[(seek, "_")] = (check, "_", "L")         # reached right end
        t[(check, c)] = ("back", "_", "L")         # matches: erase rightmost
        t[(check, "_")] = ("accept", "_", "N")     # nothing left to compare
        other = "b" if c == "a" else "a"
        t[(check, other)] = ("reject", other, "N")
    t[("back", "a")] = ("back", "a", "L")
    t[("back", "b")] = ("back", "b", "L")
    t[("back", "_")] = ("q0", "_", "R")
    return TuringMachine(t, halt_states=frozenset({"accept", "reject"}))


def busy_beaver_3() -> TuringMachine:
    """The 3-state, 2-symbol busy beaver: 6 ones in 14 steps."""
    t: Table = {
        ("A", "_"): ("B", "1", "R"), ("A", "1"): ("halt", "1", "R"),
        ("B", "_"): ("C", "_", "R"), ("B", "1"): ("B", "1", "R"),
        ("C", "_"): ("C", "1", "L"), ("C", "1"): ("A", "1", "L"),
    }
    return TuringMachine(t, start="A")
