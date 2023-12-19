#!/usr/bin/env python3

from collections import defaultdict

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
    seeds = [int(x) for x in seeds_str.split(" ")]
    needs = {}
    for piece in pieces:
        a, z, m = parse_map(piece)
        needs[a] = (z, m)
    almanac = (seeds, needs)
    return almanac

def translate(m, n):
    for d, s, l in m:
        if s <= n and n < s+l:
            return d + (n - s)
    return n

def find1(needs, want, a, an):
    if a == want:
        return an
    z, m = needs[a]
    return find1(needs, want, z, translate(m, an))

def find(inp):
    almanac = parse(inp)
    seeds, needs = almanac
    lowest = -1
    for seed in seeds:
        x = find1(needs, 'location', 'seed', seed)
        if lowest < 0 or x < lowest:
            lowest = x
    return lowest

assert find(example_input) == 35

with open("inputs/day05.input.txt") as f:
    real_input = f.read()

print(find(real_input)) # => 457535844
