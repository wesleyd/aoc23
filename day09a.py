#!/usr/bin/env python3

import operator

example_input = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

def parse(inp):
    for line in inp.splitlines():
        if not line:
            continue
        yield [int(x) for x in line.split()]

def extrapolate1(xx):
    yy = []
    while any(xx):
        yy.append(xx[len(xx)-1])
        xx = list(map(operator.sub, xx[1:], xx[0:-1]))
    return sum(yy)

def extrapolate(inp):
    return sum([extrapolate1(xx) for xx in parse(inp)])

assert extrapolate(example_input) == 114

real_input = open("inputs/day09.input.txt").read()

print(extrapolate(real_input)) # => 1995001648
