#!/usr/bin/env python3

from collections import defaultdict
from functools import reduce
import operator

example_input = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

def numbers(lines):
    """Yields (n,row,col) of every number; (row,col) is of first digit."""
    row, col = 0, 0
    n = 0
    for r, line in enumerate(lines):
        for c, ch in enumerate(line+'.'):
            if ch.isdigit():
                if n == 0:
                    row, col = r, c
                n = 10 * n + int(ch)
            elif n:
                yield (n, row, col)
                n = 0

def neighbors(n, row, col):
    """Yields all the (row,col) neighbors of the number n beginning at (r,c)."""
    for r in [row-1,row,row+1]:
        for c in range(col-1, col+len(str(n))+1):
            yield (r,c)


def sum_gear_ratios(inp):
    """Return the numbers around every gear in inp."""
    lines = inp.splitlines()
    gg = defaultdict(list)
    for n, r, c in numbers(lines):
        for row, col in neighbors(n, r, c):
            try:
                ch = lines[row][col]
            except IndexError:
                ch = '.'
            if ch == '*':
                gg[(row,col)].append(n)
    summand = 0
    for gears in gg.values():
        if len(gears) < 2:
            continue
        gear_ratio = reduce(operator.mul, gears)
        summand += gear_ratio
    return summand

assert sum_gear_ratios(example_input) == 467835


with open("inputs/day03.input.txt") as f:
    real_input = f.read()

print(sum_gear_ratios(real_input)) # => 82301120
