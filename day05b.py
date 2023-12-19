#!/usr/bin/env python3

import math

example_input = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

def parse_map(piece):
    lines = piece.splitlines()
    name = lines[0].split(" ")[0]
    a, z = name.split("-to-")
    mappings = []
    for line in lines[1:]:
        mappings.append(tuple([int(x) for x in line.split(" ")]))
    return a,z,mappings

def parse(inp):
    pieces = inp.split("\n\n")
    seeds_str = pieces.pop(0).lstrip("\n").removeprefix("seeds: ")
    seeds_it = (int(x) for x in seeds_str.split(" "))
    seed_pairs = zip(seeds_it, seeds_it)
    almanac = {}
    for piece in pieces:
        a, z, m = parse_map(piece)
        almanac[a] = (z, m)
    return (seed_pairs, almanac)

def slice3(a, b, c, d):
    left = (min(a,c), min(b,c))
    middle = (max(a,c), min(b,d))
    right = (max(a,d), max(b, d))
    return left, middle, right
assert slice3(0, 1, 2, 3) == ((0, 1), (2,1), (3,3))
assert slice3(0, 2, 1, 3) == ((0, 1), (1,2), (3,3))
assert slice3(0, 3, 1, 2) == ((0, 1), (1, 2), (2, 3))
assert slice3(1, 2, 0, 3) == ((0,0), (1, 2), (3, 3))
assert slice3(1, 3, 0, 2) == ((0,0), (1, 2), (2, 3))
assert slice3(2, 3, 0, 1) == ((0,0), (2, 1), (2, 3))

def trisect(a, an, s, sn):
    left, middle, right = slice3(a, a+an, s, s+sn)
    l = (left[0], left[1]-left[0])
    m = (middle[0], middle[1]-middle[0])
    r = (right[0], right[1]-right[0])
    return (l, m, r)

def translate(mappings, point):
    if not mappings:
        yield point
        return
    d, s, sn = mappings[0]
    a, an = point
    l, m, r = trisect(a, an, s, sn)
    if l[1] > 0:
        yield from translate(mappings[1:], l)
    if m[1] > 0:
        yield (m[0]-s+d, m[1])
    if r[1] > 0:
        yield from translate(mappings[1:], r)

def find(inp):
    seed_pairs, almanac = parse(inp)
    lowest_location = math.inf
    for seed_pair in seed_pairs:
        have = 'seed'
        nxt = [seed_pair]
        while have != 'location':
            have, mappings = almanac[have]
            pairs = nxt[:]
            nxt = []
            for p in pairs:
                nxt.extend(translate(mappings, p))
        for p in nxt:
            if p[0] < lowest_location:
                lowest_location = p[0]
    return lowest_location

assert find(example_input) == 46


with open("inputs/day05.input.txt") as f:
    real_input = f.read()

print(find(real_input)) # => 41222968
