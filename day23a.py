#!/usr/bin/env python3

from collections import namedtuple

example_input = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

Point = namedtuple('Point', ['row', 'col'])

def parse(inp):
    return [list(line) for line in inp.strip().splitlines()]

def at(grid, p):
    if 0 <= p.row and p.row < len(grid) and 0 <= p.col and p.col < len(grid[0]):
        return grid[p.row][p.col]
    return '#'

def goal(grid):
    return Point(len(grid)-1, len(grid[0])-2)

def moves(grid, p, prev):
    """What moves can we make from p, given that we've been to prev?"""
    n = Point(p.row-1, p.col)
    if at(grid, n) in '^.' and n not in prev:
        yield n
    s = Point(p.row+1, p.col)
    if at(grid, s) in 'v.' and s not in prev:
        yield s
    w = Point(p.row, p.col-1)
    if at(grid, w) in '<.' and w not in prev:
        yield w
    e = Point(p.row, p.col+1)
    if at(grid, e) in '>.' and e not in prev:
        yield e

def walk(grid, p=Point(0,1), steps=0, prev=None):
    if prev is None:
        prev = {}
    while True:
        prev[p] = True
        if p == goal(grid):
            yield steps
            return
        mm = list(moves(grid, p, prev))
        steps += 1
        if not mm:
            return
        for q in mm[1:]:
            prev2 = dict(prev)
            yield from walk(grid, q, steps, prev2)
        p = mm[0]

def play(grid):
    return max(walk(grid))

assert play(parse(example_input)) == 94

real_input = open('inputs/day23.input.txt').read()
print(play(parse(real_input)))
