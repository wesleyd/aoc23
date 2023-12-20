#!/usr/bin/env python3

import math

example_input1 = """
.....
.S-7.
.|.|.
.L-J.
.....
"""

example_input2 = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

def parse(inp):
    maze = [x for x in inp.splitlines() if x]
    for row, line in enumerate(maze):
        col = line.find('S')
        if col >= 0:
            return maze, (row, col)

def at(maze, p):
    row, col = p
    if row < 0 or len(maze) <= row or col < 0 or len(maze[row]) <= col:
        return '.'
    return maze[row][col]

def up(p):
    return (p[0]-1, p[1])
def down(p):
    return (p[0]+1, p[1])
def left(p):
    return (p[0], p[1]-1)
def right(p):
    return (p[0], p[1]+1)

def explore(inp):
    maze, start = parse(inp)
    prev = {}
    fut = [(start, 0)]
    while fut:
        p, dist = fut.pop()
        px = at(maze, p)
        if p in prev and dist >= prev[p]:
            continue
        prev[p] = dist
        dist += 1
        u, d, l, r = up(p), down(p), left(p), right(p)
        if px in '|JLS' and at(maze, u) in 'F7|':
            fut.append((u, dist))
        if px in '|F7S' and at(maze, d) in 'JL|':
            fut.append((d, dist))
        if px in '-J7S' and at(maze, l) in 'FL-':
            fut.append((l, dist))
        if px in '-FLS' and at(maze, r) in 'J7-':
            fut.append((r, dist))
    return max(prev.values())

assert explore(example_input1) == 4
assert explore(example_input2) == 8

real_input = open("inputs/day10.input.txt").read()
print(explore(real_input)) # => 7005
