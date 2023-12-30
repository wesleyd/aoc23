#!/usr/bin/env python3

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

def parse(inp):
    return [list(line) for line in inp.strip().splitlines()]

example_garden = parse(example_input)

real_input = open('inputs/day21.input.txt').read()
real_garden = parse(real_input)

def empty_garden(g):
    g2 = []
    for line in g:
        g2.append(['.' if c in '.OS' else '#' for c in line])
    return g2

def find_start(g):
    for row, line in enumerate(garden):
        for col, c in enumerate(line):
            if c == 'S':
                return (row, col)

def moves(g, row, col):
    if row >= 0 and g[row-1][col] in '.OS':
        yield(row-1, col)
    if col >= 0 and g[row][col-1] in '.OS':
        yield(row, col-1)
    if row+1 < len(g) and g[row+1][col] in '.OS':
        yield(row+1, col)
    if col+1 < len(g) and g[row][col+1] in '.OS':
        yield(row, col+1)

def print_garden(g):
    for line in g:
        print(''.join(line))

def walk(g, n):
    while n:
        n -= 1
        g2 = empty_garden(g)
        for row, line in enumerate(g):
            for col, c in enumerate(line):
                if c in 'OS':
                    for move in moves(g, row, col):
                        g2[move[0]][move[1]] = 'O'
        g = g2
    return sum(line.count('O') for line in g2)

assert walk(example_garden, 6) == 16

print(walk(real_garden, 64)) # => 3751
