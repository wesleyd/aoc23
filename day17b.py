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
    if node.direction in directions and node.nprev < 3:  # Can't change direction until four moves
        directions = set([node.direction])
    if node.direction in opposites:
        directions.discard(opposites[node.direction])  # Can't reverse
    for d in directions:
        if d == node.direction:
            nprev = node.nprev + 1
        else:
            nprev = 0
        if nprev > 9: # Can't go in the same direction more than ten times
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
    #prev = {}
    dist[start] = 0
    while q:
        u, _ = q.popitem()
        for v in neighbors(grid, u):
            alt = dist.get(u, math.inf) + grid[v.row][v.col]
            if alt < dist.get(v, math.inf):
                dist[v] = alt
                #prev[v] = u
                q[v] = alt
            if (v.row, v.col) == target and v.nprev >= 3:  # Can't even stop until four moves
                return alt #, prev

#def print_path(grid, prev):
#    for p in prev:
#        if p.row == len(grid)-1 and p.col == len(grid[0])-1:
#            break
#    path = set()
#    while p:
#        path.add((p.row, p.col))
#        p = prev.get(p, None)
#    for row in range(len(grid)):
#        for col, c in enumerate(grid[row]):
#            if (row, col) in path:
#             c = 'X'
#            print(c, end='')
#        print()

assert walk(parse(example_input)) == 94

example_input2 = """
111111111111
999999999991
999999999991
999999999991
999999999991
""".strip()
assert walk(parse(example_input2)) == 71

real_input = open('inputs/day17.input.txt').read().strip()
print(walk(parse(real_input))) # => 1165
