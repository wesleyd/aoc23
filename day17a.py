#!/usr/bin/env python3

from collections import namedtuple
from heapdict import heapdict
import math

example_input = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
""".strip()

Node = namedtuple('Node', ['row', 'col', 'direction', 'nprev'])
opposites = { 'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

def parse(inp):
    grid = []
    for line in inp.splitlines():
        grid.append([int(c) for c in line])
    return grid

def neighbors(grid, node):
    directions = set(['N', 'S', 'E', 'W'])
    if node.direction in opposites:
        directions.remove(opposites[node.direction])  # Can't reverse
    for d in directions:
        if d == node.direction:
            nprev = node.nprev + 1
        else:
            nprev = 0
        if nprev > 2: # Can't go in the same direction more than three times
            continue
        if d == 'N':
            if node.row > 0:
                yield Node(node.row-1, node.col, d, nprev)
        elif d == 'S':
            if node.row < len(grid)-1:
                yield Node(node.row+1, node.col, d, nprev)
        elif d == 'E':
            if node.col < len(grid[0])-1:
                yield Node(node.row, node.col+1, d, nprev)
        elif d == 'W':
            if node.col > 0:
                yield Node(node.row, node.col-1, d, nprev)

def walk(grid, start=Node(0, 0, 'X', 0)):
    target = (len(grid)-1, len(grid[0])-1)
    q = heapdict()
    q[start] = 0
    dist = {}
    prev = {}
    dist[start] = 0
    while q:
        u, _ = q.popitem()
        for v in neighbors(grid, u):
            alt = dist.get(u, math.inf) + grid[v.row][v.col]
            if (v.row, v.col) == target:
                return alt
            if alt < dist.get(v, math.inf):
                dist[v] = alt
                prev[v] = u
                q[v] = alt
    return math.inf

assert walk(parse(example_input)) == 102

real_input = open('inputs/day17.input.txt').read().strip()
print(walk(parse(real_input))) # => 1023
