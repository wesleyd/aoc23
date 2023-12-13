#!/usr/bin/env python3

from collections import defaultdict
import re

from functools import reduce
import operator

reduce(operator.mul, (3, 4, 5), 1)

example_input = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

game_re = re.compile(r"Game (\d+):")
dice_re = re.compile(r" (\d+) (red|green|blue)")

def play1(line):
    m = game_re.match(line)
    if not m:
        return 0
    line = line[m.end():]
    power = defaultdict(int)
    for reveal in line.split(";"):
        for m in dice_re.findall(reveal):
            color, n = m[1], int(m[0])
            if power[color] < n:
                power[color] = n
    return reduce(operator.mul, power.values())

def play(inp):
    return sum(map(play1, inp.splitlines()))

assert play(example_input) == 2286

with open("inputs/day02.input.txt") as f:
    real_input = f.read()
    
play(real_input) # => 68638
