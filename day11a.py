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
    empty_cols = []
    row = 0
    while row < len(maze):
        if '#' not in maze[row]:
            maze.insert(row, maze[row][:])
            row += 1
        row += 1
    for col in range(len(maze[0])):
        if empty_col(maze, col):
            empty_cols.append(col)
    empty_cols.reverse()
    for col in empty_cols:
        for row in range(len(maze)):
            maze[row].insert(col, '.')
    galaxies = []
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == '#':
                galaxies.append((row, col))
    return galaxies

def sum_distances(galaxies):
    dist = 0
    for n, g1 in enumerate(galaxies[:-1]):
        for g2 in galaxies[n+1:]:
            dist += abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
    return dist
  
assert sum_distances(parse(example_input)) == 374

real_input = open('inputs/day11.input.txt').read()
print(sum_distances(parse(real_input))) # => 9693756
