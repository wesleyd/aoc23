#!/usr/bin/env python3

import re
import itertools

example_input1 = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

example_input2 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

def parse(inp):
    pieces = inp.lstrip().split("\n\n")
    instructions = pieces[0]
    network = {}
    for line in pieces[1].splitlines():
       start, left, right = re.findall("[A-Z]+", line)
       network[start] = {'L': left, 'R': right}
    return instructions, network

def walk(instructions, network):
    at = 'AAA'
    n = 0
    instrs = itertools.cycle(instructions)
    while at != 'ZZZ':
        move = instrs.__next__()
        at = network[at][move]
        n += 1
    return n

assert walk(*parse(example_input1)) == 2
assert walk(*parse(example_input2)) == 6

with open("inputs/day08.input.txt") as f:
    real_input = f.read()

print(walk(*parse(real_input))) # => 16531
