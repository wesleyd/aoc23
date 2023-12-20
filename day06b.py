#!/usr/bin/env python3

import re

example_input = """
Time:      7  15   30
Distance:  9  40  200
"""

def parse(inp):
    for line in inp.splitlines():
        if line.startswith("Time:"):
            time = int("".join(re.findall(r"\d+", line)))
        if line.startswith("Distance:"):
            record = int("".join(re.findall(r"\d+", line)))
    return time, record

def race(time, record):
    n = 0
    for t in range(1, time):
        s = (time - t) * t
        if s > record:
            n += 1
    return n
assert(race(7, 9)) == 4

assert race(*parse(example_input)) == 71503

with open("inputs/day06.input.txt") as f:
    real_input = f.read()

print(race(*parse(real_input))) # => 449550
