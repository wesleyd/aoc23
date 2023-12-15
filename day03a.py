#!/usr/bin/env python3

import re

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

def issymbol(c):
    return not re.search('[0123456789.]', c)
assert not issymbol('9')
assert not issymbol('.')
assert issymbol('+')
assert issymbol('#')

def neighbors(row, col):
    for r in [row-1, row, row+1]:
        for c in [col-1, col, col+1]:
            yield(r,c)

def parse(inp):
    summand = 0
    lines = inp.splitlines()
    n = 0
    ispartnum = False
    def kerching():
        nonlocal n, ispartnum, summand
        if not n:
            return
        if ispartnum:
            summand += n
        n = 0
        ispartnum = False
    def adjacent(row,col):
        for r, c in neighbors(row, col):
            try:
                if issymbol(lines[r][c]):
                    return True
            except IndexError:
                continue
        return False
    for row, line in enumerate(lines):
        line = lines[row]
        for col, ch in enumerate(line):
            if ch.isdigit():
                n = 10*n + int(ch)
                ispartnum = ispartnum or adjacent(row,col)
            else:
                kerching()
        kerching()
    return summand

assert parse(example_input) == 4361

with open('inputs/day03.input.txt') as f:
    real_input = f.read()

parse(real_input) # => 532331
