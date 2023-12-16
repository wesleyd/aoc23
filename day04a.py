#!/usr/bin/env python3

import re

example_input = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

numbers_re = re.compile(r"\d+")

def parse(inp):
    for line in inp.splitlines():
        if not line:
            continue
        _, numbers = line.split(":")
        left, right = numbers.split("|")
        winners = set(numbers_re.findall(left))
        ours = numbers_re.findall(right)
        yield (winners, ours)

def points(inp):
    summand = 0
    for winners, ours in parse(inp):
        points = 0
        for our in ours:
            if our in winners:
                points = 2*points if points else 1
        summand = summand + points
    return summand

assert points(example_input) == 13

with open('inputs/day04.input.txt') as f:
    real_input = f.read()

print(points(real_input)) # => 25004
