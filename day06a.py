#!/usr/bin/env python3

import re

example_input = """
Time:      7  15   30
Distance:  9  40  200
"""

def parse(inp):
    for line in inp.splitlines():
        if line.startswith("Time:"):
            times = [int(s) for s in re.findall(r"\d+", line)]
        if line.startswith("Distance:"):
            records = [int(s) for s in re.findall(r"\d+", line)]
    return times, records

def race(time, record):
    n = 0
    for t in range(1, time):
        s = (time - t) * t
        if s > record:
            n += 1
    return n
assert(race(7, 9)) == 4

def play(times, records):
    p = 1
    for time, record in zip(times, records):
        p *= race(time, record)
    return p

assert play(*parse(example_input)) == 288

with open("inputs/day06.input.txt") as f:
    real_input = f.read()

print(play(*parse(real_input))) # => 449550
