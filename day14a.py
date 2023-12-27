#!/usr/bin/env python3

example_input = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

def parse(inp):
    return [line for line in inp.splitlines() if line]

def roll1_north(lines, col):
    holes = []
    rocks = []
    for i in range(len(lines)):
        c = lines[i][col]
        n = len(lines) - i
        if c == 'O':
            if holes:
                hole = holes.pop(0)
                rocks.append(hole)
                holes.append(n)
            else:
                rocks.append(n)
        elif c == '.':
            holes.append(n)
        elif c == '#':
            holes = []
        else:
            raise(f'Bad rock {c} at row={i},col={col}')
    return sum(rocks)

def roll_north(lines):
    return sum(roll1_north(lines, col) for col in range(len(lines[0])))

assert roll_north(example_lines) == 135

real_input = open('inputs/day14.input.txt').read()
print(roll_north(parse(real_input))) # => 110565
