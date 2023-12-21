#!/usr/bin/env python3

example_input = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

def empty_col(maze, col):
    for row in range(len(maze)):
        if maze[row][col] == '#':
            return False
    return True

def parse(inp):
    maze = [list(line) for line in inp.lstrip().splitlines()]
    galaxies = []
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == '#':
                galaxies.append((row, col))
    empty_rows = []
    empty_cols = []
    for row in range(len(maze)):
        if '#' not in maze[row]:
            empty_rows.append(row)
    for col in range(len(maze[0])):
        if empty_col(maze, col):
            empty_cols.append(col)
    return galaxies, empty_rows, empty_cols

def minmax(a, b):
    return min(a, b), max(a, b)

def dist(empty_rows, empty_cols, g1, g2, extra):
    row1, row2 = minmax(g1[0], g2[0])
    num_empty_rows = sum([1 for x in empty_rows if row1 < x and x < row2])
    col1, col2 = minmax(g1[1], g2[1])
    num_empty_cols = sum([1 for x in empty_cols if col1 < x and x < col2])
    return row2 - row1 + (extra-1)*num_empty_rows + col2 - col1 + (extra-1)*num_empty_cols

def sum_distances(inp, extra=2):
    galaxies, empty_rows, empty_cols = parse(inp)
    tot = 0
    for n, g1 in enumerate(galaxies[:-1]):
        for g2 in galaxies[n+1:]:
            tot += dist(empty_rows, empty_cols, g1, g2, extra)
    return tot

assert sum_distances(example_input) == 374
assert sum_distances(example_input, 10) == 1030
assert sum_distances(example_input, 100) == 8410

real_input = open('inputs/day11.input.txt').read()
print(sum_distances(real_input, 1000000)) # => 717878258016
