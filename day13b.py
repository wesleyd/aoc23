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

def dist1(lines, n):
    m = n-1
    dist = 0
    while m >= 0 and n < len(lines):
        for c1, c2 in zip(lines[m], lines[n]):
            if c1 != c2: 
                dist += 1
        m -= 1
        n += 1
    return dist

def invert(lines):
    ll = [""] * len(lines[0])
    for col in range(len(lines[0])):
        for row in range(len(lines)):
            ll[col] += lines[row][col]
    return ll

def find_reflection(section, delta=0):
    for n in range(1, len(section)):
        d = dist1(section, n)
        if d == delta:
            return n*100
    vert = invert(section)
    for n in range(1, len(vert)):
        d = dist1(vert, n)
        if d == delta:
            return n
    return 0

def run(inp, delta=1):
    sections = parse(inp)
    tot = 0
    for i, section in enumerate(sections):
        n = find_reflection(section, delta)
        tot += n
    return tot

assert run(example_input, 0) == 405
assert run(example_input, 1) == 400

real_input = open("inputs/day13.input.txt").read()

#assert run(real_input, 0) == 43614

print(run(real_input, 1)) # => 36771
