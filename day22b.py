#!/usr/bin/env python3

import re

from collections import defaultdict, namedtuple
from functools import lru_cache

example_input = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

Brick = namedtuple('Brick', ['name', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2'])

def parse(inp):
    """Turns input into bricks, sorted by z, with the x's, y's and z's sorted."""
    bricks = []
    name = 'A'
    for line in inp.strip().splitlines():
        pp = [int(s) for s in re.split("[~,]", line)]
        if pp[0] > pp[3]:
            pp[0], pp[3] = pp[3], pp[0]
        if pp[1] > pp[4]:
            pp[1], pp[4] = pp[4], pp[1]
        if pp[2] > pp[5]:
            pp[2], pp[5] = pp[5], pp[2]
        bricks.append(Brick(name, *pp))
        name = chr(ord(name) + 1)
        bricks.sort(key=lambda br: br.z1)
    return bricks

def overlap_x(br1, br2):
    return br1.x1 <= br2.x2 and br2.x1 <= br1.x2

def overlap_y(br1, br2):
    return br1.y1 <= br2.y2 and br2.y1 <= br1.y2

def overlap_xy(br1, br2):
    return overlap_x(br1, br2) and overlap_y(br1, br2)

def dropped(br, dz):
    """Returns what br would look like if it dropped by dz."""
    return Brick(br.name, br.x1, br.y1, br.z1 - dz, br.x2, br.y2, br.z2 - dz)

def gravity_falls(bricks):
    """Enforces gravity on bricks. Returns how many bricks got dropped."""
    n = 0
    for i in range(len(bricks)):
        drop = bricks[i].z1 - 1
        for j in range(len(bricks)):
            if drop < 1:
                break
            if i == j:
                continue
            if not overlap_xy(bricks[i], bricks[j]):
                continue  # b can't support a ∵ they don't share a brick
            if bricks[j].z2 > bricks[i].z1:
                continue  # b can't support a ∵ b isn't below a
            drop_a_on_b = bricks[i].z1 - bricks[j].z2 - 1
            if drop_a_on_b < drop:
                drop = drop_a_on_b
        if drop > 0:
            bricks[i] = dropped(bricks[i], drop)
            n += 1
    return n

def supporters(bricks):
    """Returns which bricks are atop which other bricks."""
    supports = {}
    supported_by = defaultdict(set)
    for i in range(len(bricks)):
        supports[bricks[i]] = set()
        for j in range(len(bricks)):
            if i == j:
                continue
            if not overlap_xy(bricks[i], bricks[j]):
                continue
            if bricks[j].z1 - bricks[i].z2 == 1:
                supports[bricks[i]].add(bricks[j])
                supported_by[bricks[j]].add(bricks[i])
    return supports, supported_by

def run(inp):
    fallen = 0
    bricks = parse(inp)
    gravity_falls(bricks)
    for i in range(len(bricks)-1,-1,-1):
        almost = bricks[0:i] + bricks[i+1:]

        n = gravity_falls(almost)
        if n > 0:
            fallen += n
        print(f'Brick {i} {bricks[i]} => {n}')
    return fallen

assert run(example_input) == 7

real_input = open('inputs/day22.input.txt').read()
print(run(real_input)) # => 93292
