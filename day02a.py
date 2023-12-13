#!/usr/bin/env python3

from collections import defaultdict
import re

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
    g = int(m.group(1))
    line = line[m.end():]
    for reveal in line.split(";"):
        draw = defaultdict(int)
        for m in dice_re.findall(reveal):
            draw[m[1]] = int(m[0])
        if draw['red'] > 12 or draw['green'] > 13 or draw['blue'] > 14:
            return 0
    return g

def play(inp):
    return sum(map(play1, inp.splitlines()))

assert play(example_input) == 8

with open("inputs/day02.input.txt") as f:
    real_input = f.read()
    
play(real_input) # => 2776
