#!/usr/bin/env python3

import itertools
import math
import re

example_input = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

def parse(inp):
    pieces = inp.lstrip().split("\n\n")
    instructions = pieces[0]
    network = {}
    for line in pieces[1].splitlines():
       start, left, right = re.findall("[0-9A-Z]+", line)
       network[start] = {'L': left, 'R': right}
    return instructions, network

def walk1(instructions, network, at):
    n = 0
    instrs = itertools.cycle(instructions)
    while not at.endswith("Z"):
        move = instrs.__next__()
        at = network[at][move]
        n += 1
    return n

def lcm(nn):
    p = 1
    while nn:
        q = nn.pop()
        p = abs(p*q) // math.gcd(p,q)
    return p

def walk(instructions, network):
    starts = [x for x in network if x.endswith('A')]
    nn = [walk1(instructions, network, start) for start in starts]
    return lcm(nn)

assert walk(*parse(example_input)) == 6

with open("inputs/day08.input.txt") as f:
    real_input = f.read()

print(walk(*parse(real_input))) # => 24035773251517
