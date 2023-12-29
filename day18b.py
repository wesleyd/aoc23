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

my_example = """
R 12 (#C0)
D 3 (#31)
L 3 (#32)
D 2 (#21)
R 2 (#20)
D 6 (#61)
L 2 (#22)
U 3 (#33)
L 1 (#12)
D 3 (#31)
L 4 (#42)
U 2 (#23)
L 2 (#22)
U 2 (#23)
L 2 (#22)
U 7 (#73)
"""

def parse(inp):
    for line in inp.splitlines():
        if not line:
            continue
        pieces = line.split("#")
        piece = pieces[1].rstrip(')')
        direction = ['R', 'D', 'L', 'U'][int(piece[-1])]
        distance = int(piece[:-1], 16)
        yield direction, distance

def dig(inp):
    walls = []
    p = (0, 0)
    for direction, distance in parse(inp):
        assert direction in 'UDLR', f'Bad direction={direction}.'
        if direction == 'U':
            q = (p[0]-distance, p[1])
        elif direction == 'D':
            q = (p[0]+distance, p[1])
        elif direction == 'L':
            q = (p[0], p[1]-distance)
        elif direction == 'R':
            q = (p[0], p[1]+distance)
        walls.append((p, q))
        p = q
    walls.append((p, (0, 0)))
    return walls

def wallrows(walls):
    rows = set()
    for w in walls:
        for p in w:
            rows.add(p[0])
    return sorted(rows)

def wallcols(walls):
    cols = set()
    for w in walls:
        for p in w:
            cols.add(p[1])
    return sorted(cols)

def minmax(a, b):
    return min(a,b), max(a,b)

def shrink(walls, thickness=1):
    """Like build, but at a tiny scale."""
    rows = {}
    cols = {}
    if thickness > 0:
        rows = {r: i*thickness for i, r in enumerate(wallrows(walls))}
        cols = {c: i*thickness for i, c in enumerate(wallcols(walls))}
    else:  # Don't shrink if thickness == 0
        rows = {r: r for r in wallrows(walls)}
        cols = {c: c for c in wallcols(walls)}
    nrows = max(rows.values())+1 #len(rows)
    ncols = max(cols.values())+1 # len(cols)
    grid = [[' '] * ncols for _ in range(nrows)]
    for w in walls:
        p, q = w
        if p[0] == q[0]:
            irow = rows[p[0]]
            l, r = cols[p[1]], cols[q[1]]
            if l > r:
                l, r = r, l
            for icol in range(l, r+1):
                if grid[irow][icol] != ' ':
                    grid[irow][icol] = '#'
                else:
                    grid[irow][icol] = '-'
        if p[1] == q[1]:
            icol = cols[p[1]]
            u, d = rows[p[0]], rows[q[0]]
            if u > d:
                u, d = d, u
            for irow in range(u, d+1):
                if grid[irow][icol] != ' ':
                    grid[irow][icol] = '#'
                else:
                    grid[irow][icol] = '|'
    return grid

def draw(grid):
    for row in grid:
        print(''.join(row))

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
                up1 = at(lagoon, row-1, start) 
                up2 = at(lagoon, row-1, col)
                down1 = at(lagoon, row+1, start) 
                down2 = at(lagoon, row+1, col)
                if (up1 not in '|#' or up2 not in '|#') and (down1 not in '|#' or down2 not in '|#'):
                    nwalls += 1
            elif lagoon[row][col] == ' ' and nwalls % 2 == 1:
                lagoon[row][col] = '*'
            col += 1
    return lagoon

def area(walls, thickness=2):
    assert thickness in [0, 2], f'bad thickness={thickness}'
    if thickness == 2:
        lagoon = shrink(walls, thickness=2)
        rows = wallrows(walls)
        cols = wallcols(walls)
        heights = [1]*(2*len(rows)-1)
        widths = [1]*(2*len(cols)-1)
        for i in range(len(rows)-1):
            heights[2*i+1] = rows[i+1] - rows[i] - 1
            assert heights[2*i-1] >= 0
        for i in range(len(cols)-1):
            widths[2*i+1] = cols[i+1] - cols[i] - 1
            assert widths[2*i-1] >= 0
    elif thickness == 0:
        lagoon = shrink(walls, thickness=0)
        heights = [1] * len(lagoon)
        widths = [1] * len(lagoon[0])
    fill(lagoon)
    area = 0
    assert len(lagoon) == len(heights), f'{len(lagoon)} != {len(heights)}'
    assert len(lagoon[0]) == len(widths), f'{len(lagoon[0])} != {len(widths)}'
    for row, line in enumerate(lagoon):
        arow = 0
        for col, c in enumerate(lagoon[row]):
            if c == ' ':
                continue
            area += widths[col] * heights[row]
    return area

assert area(dig(my_example)) == 134
assert area(dig(example_input)) == 952408144115

real_input = open('inputs/day18.input.txt').read().strip()

# draw(fill(shrink(dig(real_input))))

print(area(dig(real_input))) # => 62762509300678
