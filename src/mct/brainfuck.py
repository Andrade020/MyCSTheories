"""Brainfuck interpreter with a precomputed jump table and bounded execution.

Brainfuck is Turing-complete (given an unbounded tape), which makes it a compact
playground for universality arguments.
"""
from __future__ import annotations


class BrainfuckError(Exception):
    pass


def _jump_table(code: str) -> dict[int, int]:
    table: dict[int, int] = {}
    stack: list[int] = []
    for i, c in enumerate(code):
        if c == "[":
            stack.append(i)
        elif c == "]":
            if not stack:
                raise BrainfuckError(f"unmatched ']' at {i}")
            j = stack.pop()
            table[i], table[j] = j, i
    if stack:
        raise BrainfuckError(f"unmatched '[' at {stack[-1]}")
    return table


def run(program: str, stdin: str = "", max_steps: int = 10_000_000, tape_size: int = 30_000) -> str:
    """Runs ``program`` and returns its output. Cells wrap modulo 256."""
    code = "".join(c for c in program if c in "><+-.,[]")
    jumps = _jump_table(code)
    tape, ptr, pc, steps = [0] * tape_size, 0, 0, 0
    ip, out = 0, []
    while pc < len(code):
        steps += 1
        if steps > max_steps:
            raise BrainfuckError(f"step limit ({max_steps}) exceeded")
        c = code[pc]
        if c == ">":
            ptr += 1
            if ptr >= tape_size:
                raise BrainfuckError("tape pointer past the right end")
        elif c == "<":
            ptr -= 1
            if ptr < 0:
                raise BrainfuckError("tape pointer before the left end")
        elif c == "+":
            tape[ptr] = (tape[ptr] + 1) & 255
        elif c == "-":
            tape[ptr] = (tape[ptr] - 1) & 255
        elif c == ".":
            out.append(chr(tape[ptr]))
        elif c == ",":
            tape[ptr] = ord(stdin[ip]) if ip < len(stdin) else 0
            ip += 1
        elif (c == "[" and tape[ptr] == 0) or (c == "]" and tape[ptr] != 0):
            pc = jumps[pc]
        pc += 1
    return "".join(out)
