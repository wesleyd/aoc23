#!/usr/bin/env python3

import math

from collections import defaultdict, namedtuple
from heapdict import heapdict

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

def moves(grid, p, path):
    """What moves not in path can we make from p?"""
    n = Point(p.row-1, p.col)
    s = Point(p.row+1, p.col)
    w = Point(p.row, p.col-1)
    e = Point(p.row, p.col+1)
    for q in (n, s, e, w):
        if at(grid, q) in '^v<>.' and q not in path:
            yield q

def survey(grid):
    """Yields all direct connections in grid."""
    maze = defaultdict(dict)
    x = goal(grid)
    path = [Point(0,1), Point(1,1)]
    paths = [path]
    while paths:
        path = paths.pop()
        p = path[-1]
        mm = list(moves(grid, p, path))
        while len(mm) == 1:
            p = mm[0]
            path.append(p)
            mm = list(moves(grid, p, path))
        if p == x:
            maze[path[0]][path[-1]] = len(path)-1
            continue
        if len(mm) == 0:
            continue # Dead end
        maze[path[0]][path[-1]] =  len(path)-1
        if p in maze:
            continue
        for m in mm:
            paths.append([p, m])
    for p in list(maze.keys()):
        for q in maze[p]:
            maze[q][p] = maze[p][q]
    return maze

def dict_peek(d, n):
    if n < 0:
        n = -1-n
        d = reversed(d)
    for x in d:
        if n == 0:
            return x
        n -= 1

def walk(inp, p=Point(0,1), path=None):
    grid = parse(inp)
    x = goal(grid)
    maze = survey(grid)
    if path is None:
        path = {p: 0}
    paths = [path]
    while paths:
        path = paths.pop()
        p = dict_peek(path,-1)
        for q in maze[p]:
            if q in path:
                continue
            path2 = dict(path)
            path2[q] = maze[p][q]
            if q == x:
                yield sum(path2.values())
            paths.append(path2)

assert max(walk(example_input)) == 154

real_input = open('inputs/day23.input.txt').read()
print(max(walk(real_input)))  # => 6350 is the right answer!!
