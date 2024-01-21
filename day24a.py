#!/usr/bin/env python3

import math
import re

from collections import namedtuple

example_input = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

PV = namedtuple('PV', ['x', 'y', 'z', 'vx', 'vy', 'vz'])

def parse(inp):
    return [PV(*[int(s) for s in re.findall(r'-?\d+', line)]) for line in inp.strip().splitlines()]

example = parse(example_input)

def det(pv1, pv2):
    return pv1.vx*(-pv2.vy) + pv2.vx*pv1.vy

assert det(example[0], example[1]) == -3

def solve(p, q):
    d = det(p, q)
    #print(f'd={d}')
    if not d:
        return None  # Parallel
    t1 = ( -q.vy*(q.x-p.x) + q.vx*(q.y-p.y) )/ d
    t2 = ( -p.vy*(q.x-p.x) + p.vx*(q.y-p.y) )/ d
    if t1 < 0 or t2 < 0:
        return None  # In the past
    return (p.vx * t1 + p.x, p.vy * t1 + p.y)

def run(inp, low, high):
    n = 0
    pp = parse(inp)
    for i in range(len(pp)):
        for j in range(i+1, len(pp)):
            q = solve(pp[i], pp[j])
            if not q:
                continue
            x, y = q
            if low <= x <= high and low <= y <= high:
                n += 1
    return n

assert run(example_input, 7, 27) == 2

real_input = open('inputs/day24.input.txt').read()
print(run(real_input, 200000000000000, 400000000000000)) # => 15262
