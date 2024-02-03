#!/usr/bin/env python3

# I gave up on this one and used the quadratic fitting idea from:
#   https://github.com/derailed-dash/Advent-of-Code/blob/master/src/AoC_2023/Dazbo's_Advent_of_Code_2023.ipynb
# Brilliant insight.
# This only works when one is walking r=65 plus an exact multiple of h=131. Which we are.

import math

from collections import namedtuple
from heapdict import heapdict
from typing import Dict, Iterator, Tuple


example_input = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

Point = namedtuple('Point', ['x', 'y'])
def up(p: Point) -> Point:
    return Point(p.x, p.y+1)
def down(p: Point) -> Point:
    return Point(p.x, p.y-1)
def left(p: Point) -> Point:
    return Point(p.x-1, p.y)
def right(p: Point) -> Point:
    return Point(p.x+1, p.y)

class Grid(object):
    def __init__(self, inp: str):
        g = list(inp.strip().splitlines())
        assert len(g) == len(g[0]), f'map must be square: {len(g)}x{len(g[0])}'
        assert len(g) % 2 == 1, f'map size must be odd: {len(g)}'
        self.g = g
        self.h = len(g)
        self.r = len(g) // 2
    def at(self, p: Point) -> str:
        """Returns the character at p."""
        row = (-p.y + self.r) % self.h
        col = (p.x + self.r) % self.h
        c = self.g[row][col]
        return '#' if c == '#' else '.'  # return '.' for 'S'
    def atxy(self, x: int, y: int) -> str:
        return self.at(Point(x,y))

example_grid = Grid(example_input)
assert example_grid.at(Point( 0, 0)) == '.'
assert example_grid.at(Point( 0,+1)) == '.'
assert example_grid.at(Point(-1, 0)) == '.'
assert example_grid.at(Point(+1, 0)) == '#'
assert example_grid.at(Point( 0,-1)) == '#'
assert example_grid.at(Point( 0,+1)) == '.'

def move1(g: Grid, p: Point) -> Iterator[Point]:
    """Yields all possible one-step moves in g from p."""
    for q in up(p), down(p), left(p), right(p):
        if g.at(q) == '.':
            yield q

def move2(g: Grid, p: Point) -> Iterator[Point]:
    """Yields all possible two-step moves in g from p."""
    moved = set()
    for q in move1(g, p):
        for r in move1(g, q):
            if r in moved:
                continue
            yield r
            moved.add(r)

def move(g: Grid, steps: int, o: Point = Point(0,0)) -> int:
    """Returns num reachable points from p in g in exactly steps."""
    q = heapdict()
    dist = {}
    if steps % 2 == 1:
        for p in move1(g, o):
            q[p] = 1
            dist[p] = 1
    else:
        q[o] = 0
        dist[o] = 0
    while q:
        u, d = q.popitem()
        assert d <= steps, (u, d)
        for v in move2(g, u):
            alt = dist.get(u, math.inf) + 2
            if alt > steps:
                continue
            if alt < dist.get(v, math.inf):
                dist[v] = alt
                q[v] = alt
    return len(dist)


assert move(example_grid, 6) == 16
assert move(example_grid, 10) == 50
assert move(example_grid, 50) == 1594
#assert move(example_grid, 100) == 6536
#assert move(example_grid, 500) == 167004
#assert move(example_grid, 1000) == 668697

real_input = open('inputs/day21.input.txt').read()
real_grid = Grid(real_input)

# Fit to
#  a*n^2 + b*n + c = ?
# where we move 65 + n*131 steps...

def moveN(g: Grid, n: int) -> int:
    """Returns how many points are reachable from origin within 65+n*131 steps.
       Requires g have highways around edges and along axes."""
    x0 = move(real_grid, 65)
    x1 = move(real_grid, 65 + 131)
    x2 = move(real_grid, 65 + 131 * 2)
    c = x0
    a = ( x2 - 2*x1 + c ) // 2
    b = x1 -c - a
    return a*n*n + b*n + c

assert moveN(real_grid, 4) == move(real_grid, 65+4*131)

N = ( 26501365 - 65 ) // 131
print(moveN(real_grid, N))
