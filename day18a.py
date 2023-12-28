#!/usr/bin/env python3

import math
from collections import defaultdict

example_input = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

def parse(inp):
    for line in inp.splitlines():
        if not line:
            continue
        pieces = line.split(" ")
        yield (pieces[0], int(pieces[1]))

def dig(inp):
    grid = {}
    p = (0, 0)
    for direction, distance in parse(inp):
        grid[p] = '#'
        while distance:
            assert direction in 'UDLR', f'Bad direction={direction}.'
            if direction == 'U':
                p = (p[0]-1, p[1])
                c = '|'
            elif direction == 'D':
                p = (p[0]+1, p[1])
                c = '|'
            elif direction == 'L':
                p = (p[0], p[1]-1)
                c = '-'
            elif direction == 'R':
                p = (p[0], p[1]+1)
                c = '-'
            if p in grid:
                c = '#'
            grid[p] = c
            distance -= 1
    min_row, max_row = math.inf, -math.inf
    min_col, max_col = math.inf, -math.inf
    for p in grid:
        if p[0] < min_row:
            min_row = p[0]
        if p[0] > max_row:
            max_row = p[0]
        if p[1] < min_col:
            min_col = p[1]
        if p[1] > max_col:
            max_col = p[1]
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    lagoon = []
    for row in range(height):
        line = []
        for col in range(width):
            line.append(grid.get((min_row+row, min_col+col), '.'))
        lagoon.append(line)
    return lagoon

#def draw(lagoon):
#    for line in lagoon:
#        print(''.join(line))

def at(lagoon, row, col):
    if row < 0 or col < 0 or row >= len(lagoon) or col >= len(lagoon[0]):
        return '.'
    return lagoon[row][col]

def fill(lagoon):
    for row in range(len(lagoon)):
        nwalls = 0
        col = 0
        while col < len(lagoon[0]):
            if lagoon[row][col] == '|':
                nwalls += 1
            elif lagoon[row][col] == '#':
                start = col
                col += 1
                while at(lagoon, row, col) != '#':
                    col += 1
                if not(at(lagoon, row+1, start) == '|' and at(lagoon, row+1, col) == '|' or at(lagoon, row-1, start) == '|' and at(lagoon, row-1, col) == '|'):
                    nwalls += 1
            elif lagoon[row][col] == '.' and nwalls % 2 == 1:
                lagoon[row][col] = '*'
            col += 1
    return lagoon

def volume(lagoon):
    vol = 0
    for line in lagoon:
        for c in line:
            if c != '.':
                vol += 1
    return vol

assert volume(fill(dig(example_input))) == 62

real_input = open('inputs/day18.input.txt').read().strip()
#draw(fill(dig(real_input)))
print(volume(fill(dig(real_input))))

