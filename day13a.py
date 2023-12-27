#!/usr/bin/env python3

example_input = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

def parse1(para):
    lines = []
    for line in para.splitlines():
        if line:
            lines.append(line)
    return lines

def parse(inp):
    sections = []
    for para in inp.split("\n\n"):
        sections.append(parse1(para))
    return sections

def is_reflection(lines, i):
    j = i+1
    while 0 <= i and i < len(lines) and 0 <= j and j < len(lines):
        if lines[i] != lines[j]:
            return False
        i += 1
        j -= 1
    return True

def reflect(lines):
    for i in range(len(lines)-1):
        if lines[i] == lines[i+1]:
            if is_reflection(lines, i):
                return i+1
    return 0

def invert(lines):
    ll = [""] * len(lines[0])
    for col in range(len(lines[0])):
        for row in range(len(lines)):
            ll[col] += lines[row][col]
    return ll

def run(inp):
    sections = parse(inp)
    tot = 0
    for section in sections:
        tot += 100 * reflect(section) + reflect(invert(section))
    return tot

assert run(example_input) == 405

real_input = open("inputs/day13.input.txt").read()

print(run(real_input)) # => 43614
