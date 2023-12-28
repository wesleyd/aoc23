#!/usr/bin/env python3

from collections import defaultdict

example_input = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""".strip()

def move1(beam):
    return (beam[0] + beam[2], beam[1] + beam[3], beam[2], beam[3])

def print_map(lines, energized):
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if (row, col) in energized:
                c = '#'
            print(c, end='')
        print()
    print()

def play(lines, pilot=(0, -1, 0, 1)):
    beams = [pilot]   # (row, col, row-v, col-v)
    energized = defaultdict(set)
    while True:
        if not beams:
            break
        beam = move1(beams.pop())
        if beam[0] < 0 or len(lines) <= beam[0]:
            continue
        if beam[1] < 0 or len(lines[0]) <= beam[1]:
            continue
        if (beam[2], beam[3]) in energized[(beam[0],beam[1])]:
            continue
        energized[(beam[0], beam[1])].add((beam[2], beam[3]))
        c = lines[beam[0]][beam[1]]
        if c == '/':
            if beam[2] != 0:
                beams.append((beam[0], beam[1], 0, -beam[2]))
            elif beam[3] != 0:
                beams.append((beam[0], beam[1], -beam[3], 0))
            else:
                assert False, f'Bad beam {beam}'
        elif c == '\\':
            if beam[2] != 0:
                beams.append((beam[0], beam[1], 0, beam[2]))
            elif beam[3] != 0:
                beams.append((beam[0], beam[1], beam[3], 0))
        elif c == '|' and beam[3] != 0:
            beams.append((beam[0], beam[1], beam[3], 0))
            beams.append((beam[0], beam[1], -beam[3], 0))
        elif c == '-' and beam[2] != 0:
            beams.append((beam[0], beam[1], 0, beam[2]))
            beams.append((beam[0], beam[1], 0, -beam[2]))
        else:
            beams.append(beam)
        #print_map(lines, energized)
    return len(energized)

assert play(example_input.splitlines()) == 46

def optimize(lines):
    ee = []
    for row in range(len(lines)):
        ee.append(play(lines, pilot=(row, -1, 0, 1)))
        ee.append(play(lines, pilot=(row, len(lines[0]), 0, -1)))
    for col in range(len(lines[0])):
        ee.append(play(lines, pilot=(-1, col, 1, 0)))
        ee.append(play(lines, pilot=(len(lines), col, -1, 0)))
    return max(ee)
                  
assert optimize(example_input.splitlines()) == 51

real_input = open('inputs/day16.input.txt').read().strip()
print(optimize(real_input.splitlines())) # =>  8239
