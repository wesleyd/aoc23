#!/usr/bin/env python3

from collections import deque, namedtuple
from functools import lru_cache
from heapdict import heapdict

import math

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

real_input = open('inputs/day21.input.txt').read()

Farm = namedtuple('Farm', ['r', 'moves'])


class Grid(object):
    def __init__(self, inp):
        self.g = [list(line) for line in inp.strip().splitlines()]
        assert len(g) == len(g[0]), f'map must be square: {len(g)}x{len(g[0])}'
        assert len(g) % 2 == 1, f'map size must be odd: {len(g)}'
        self.g = g
        self.h = len(g)
        self.r = len(g) // 2
        assert all('.' == self.at(x,y) for x,y in self.edges()), f'edge not empty'
    def at(self, x, y):
        y = -y
        row = (y + self.r) % self.h
        col = (x + self.r) % self.h
        c = self.g[row][col]
        return '#' if c == '#' else '.'


def peek_dict(d, n):
    """Return the nth key in d by insertion order."""
    if n < 0:
        d = reversed(d)
        n = -n - 1 
    for e in d:
        if not n:
            return e
        n -= 1
    raise IndexError(n)

def walk_grid(grid):
    visited = {}
    visited[(0, 0)] = 0
    while visited:
        p, d = visited.pop()
        n = 


class Farm(object):
    def __init__(self, inp):
        g = list(inp.strip().splitlines())
        assert len(g) == len(g[0]), f'map must be square: {len(g)}x{len(g[0])}'
        assert len(g) % 2 == 1, f'map size must be odd: {len(g)}'
        self.g = g
        self.h = len(g)
        self.r = len(g) // 2
        assert all('.' == self.at(x,y) for x,y in self.edges()), f'edge not empty'



class Garden(object):
    def __init__(self, inp):
        g = list(inp.strip().splitlines())
        assert len(g) == len(g[0]), f'map must be square: {len(g)}x{len(g[0])}'
        assert len(g) % 2 == 1, f'map size must be odd: {len(g)}'
        self.g = g
        self.h = len(g)
        self.r = len(g) // 2
        assert all('.' == self.at(x,y) for x,y in self.edges()), f'edge not empty'
    def edges(self):
        """Yields all the edge points of the garden."""
        for y in range(-self.r, self.r+1):
            yield(-self.r, y)
            yield(self.r, y)
        for x in range(-self.r+1, self.r):
            yield(x, -self.r)
            yield(x, self.r)
    def __str__(self):
        return f'Garden{{h={self.h}, r={self.r}}}'
    def at(self, x, y):
        y = -y
        row = (y + self.r) % self.h
        col = (x + self.r) % self.h
        c = self.g[row][col]
        return '#' if c == '#' else '.'
    def within_bounds(self, p):
        x, y = p
        r = self.r
        return -r <= x and x <= r and -r <= y and y <= r
    def moves1(self, x, y):
        """Yields all possible one-step moves from (x,y)."""
        for p in ((x, y+1), (x, y-1), (x-1, y), (x+1, y)):
            if self.at(*p) == '.':
                yield p
    def moves2(self, x, y):
        """Yields all possible two-step moves from (x,y)."""
        g = self.g
        yield (x, y)
        if self.at(x, y+2) != '#' and self.at(x, y+1) != '#':
            yield (x, y+2)
        if self.at(x, y-2) != '#' and self.at(x, y-1) != '#':
            yield (x, y-2)
        if self.at(x+2, y) != '#' and self.at(x+1, y) != '#':
            yield (x+2, y)
        if self.at(x-2, y) != '#' and self.at(x-1, y) != '#':
            yield (x-2, y)
        if self.at(x-1,y-1) != '#' and (self.at(x-1, y) != '#' or self.at(x,y-1) != '#'):
            yield (x-1,y-1)
        if self.at(x-1,y+1) != '#' and (self.at(x-1, y) != '#' or self.at(x,y+1) != '#'):
            yield (x-1,y+1)
        if self.at(x+1,y-1) != '#' and (self.at(x+1, y) != '#' or self.at(x,y-1) != '#'):
            yield (x+1,y-1)
        if self.at(x+1,y+1) != '#' and (self.at(x+1, y) != '#' or self.at(x,y+1) != '#'):
            yield (x+1,y+1)
    @lru_cache
    def notrocks(self, odd=None):
        """How many of the odd/even tiles are not rocks?"""
        assert odd is not None
        n = 0
        for x in range(-self.r, self.r+1):
            for y in range(-self.r, self.r+1):
                if self.at(x, y) != '.' and bool((x+y)%2) == odd:
                    n += 1
        return n
    @lru_cache
    def shortest_paths(self, p):
        """Returns shortest paths from p to all points in the containing g."""
        q = heapdict()
        q[p] = 0
        dist = {p: 0}
        while q:
            u, _ = q.popitem()
            for v in self.moves1(*u):
                if not self.within_bounds(v):
                    continue
                alt = dist.get(u, math.inf) + 1
                if alt < dist.get(v, math.inf):
                    dist[v] = alt
                    q[v] = alt
        return dist

example_garden = Garden(example_input)

max(example_garden.shortest_paths((0,0)).values())

example_garden.shortest_paths((0,0)).values())









dijkstra(example_garden, (0,0))


real_garden = Garden(real_input)
rp = dijkstra(real_garden, (0,0))

def nearest(shortest_paths, f):
    nearest = None
    nearest_distance = math.inf
    for p, d in shortest_paths.items():
        if not f(p):
            continue
        if d < nearest_distance:
            nearest = p
            nearest_distance = d
    return nearest, nearest_distance

nearest(dijkstra(real_garden, (0, -65)), lambda p: p[1] == +65)



assert example_garden.h == 11
assert example_garden.r == 5
assert real_garden.h == 131
assert real_garden.r == 65

# Let's assume that:
# (i) all garden tiles are reachable from all other garden tiles...
# (ii) ... within at most 2*h steps.

def explore(garden, nsteps):
    nreachable = 0
    nstrides = 0
    if nsteps > garden.h:
        nsteps -= garden.h

    while nsteps > garden.h + garden.r:
        nstrides += 1
        nreachable += garden.notrocks(odd=bool(nsteps%2))
        nsteps -= garden.h

    while nsteps > garden.h:
        nreachable += 4*nstrides*garden.notrocks(odd=bool(nsteps%2))
        nstrides += 1
        nsteps -= garden.h
    return nreachable, nsteps


explore(example_garden, 10)

# .1, #4, o8, x12, .16
#     .
#    .x.
#   .xox.
#  .xo#ox.
# .xo#.#ox.
#  .xo#ox.
#   .xox.
#    .x.
#     .


class Walker(object):
    def __init__(self, garden, odd=False):
        self.garden = garden
        self.n = 0
        self.edge = set()
        self.prev = set()
        if odd:
            self.n += 1
            for p in self.garden.moves1((0,0)):
                self.edge.append(p)
                self.visited.add(p)
        else:
            self.edge.append((0, 0))
            self.visited.add((0,0))
        print(f'self.visited={self.visited}')
        print(f'self.edge={self.edge}')
    def walk2(self, i):
        """Takes two steps."""
        while i > 0:
            self.n += 2
            i -= 2
            edge = deque()
            for f in self.edge:
                for p in self.garden.moves2(*f):
                    if p not in self.visited:
                        edge.append(p)
                        self.visited.add(p)
            self.edge = edge
    def print(self, draw=False):
        minx, maxx = math.inf, -math.inf
        miny, maxy = math.inf, -math.inf
        for p in self.visited:
            x, y = p
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x
            if y < miny:
                miny = y
            if y > maxy:
                maxy = y
        if draw:
            y = miny
            while y <= maxy:
                line = []
                x = minx
                while x <= maxx:
                    p = (x, y)
                    if p in self.visited:
                        line.append('O')
                    elif p == (0, 0):
                        line.append('S')
                    else:
                        line.append(self.garden.at(x, y))
                    x += 1
                print(''.join(line))
                y += 1
        print(f'After {self.n} steps could reach {len(self.visited)} tiles. x ∈ [{minx}, {maxx}], y ∈ [{miny}, {maxy}]')

o = Garden(example_input)
w = Walker(g, odd=False)
w.walk2(6)
w.print()
w.walk2(4)
w.print()
w.walk2(40)
w.print()
w.walk2(450)
w.print()
w.walk2(500)
w.print()

w.print(True)
w.walk2(6)

w.walk2(50)

w.print(True)


p = walk(g, 3)

walk(g, 2, p)

list(g.moves2(0, 0))

print(g)
for y in range(16, -(16+1), -1):
    print(''.join(g.at(x,y) for x in range(-16, 16+1)))





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
