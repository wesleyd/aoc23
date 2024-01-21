#!/usr/bin/env python3

# Following clever algebra at...
#   https://github.com/jmd-dk/advent-of-code/blob/main/2023/solution/24/solve.py
# ...where he elminates t, leaving only the position-momentum sixtuple of the
# rock unknown, but the equations are nonlinear. Then he separates out the
# onlinear terms, which _don't depend on the hailstone_, and equates them with
# same from another pair of axes. Brilliant.  But that's only three equations ...
# with six unknowns! So he adds another hailstone - this doesn't add new unknows,
# but it _does_ give us more equations. Three more, in fact. I assume this only
# works because the hailstones were carefully chosen to only offer six degrees
# of freedom.

import re

from collections import namedtuple
from fractions import Fraction

example_input = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

PV = namedtuple('PV', ['x', 'y', 'z', 'vx', 'vy', 'vz'])

def parse(inp):
    return [PV(*[int(s) for s in re.findall(r'-?\d+', line)]) for line in inp.strip().splitlines()]

def det(A):
    """Determinant of square matrix A."""
    if len(A) == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]
    d = 0
    for c in range(len(A[0])):
        sub = [ row[:c] + row[c+1:] for row in A[1:] ]
        d += [1, -1][c%2] * A[0][c] * det(sub)
    return d

M = [ [ 1, 2, 3 ], [ 0, 1, 4 ], [ 5, 6, 0 ] ]
assert det(M) == 1

def replace_col(A, b, i):
    """Return a copy of A with the ith col replaced with b."""
    R = []
    for r in range(len(A)):
        R.append(A[r][:i] + [b[r]] + A[r][i+1:])
    return R

def cramer(A, b):
    """Solve A*x=b with cramer's rule."""
    d = det(A)
    x = []
    for i in range(len(b)):
        A_i = replace_col(A, b, i)
        d_i = det(A_i)
        if d_i % d == 0:
            x_i = d_i // d
        else:
            x_i = d_i / d
        x.append(x_i)
    return x

assert cramer([[1,1,1],[2,1,3],[1,-3,1]], [2, 9, 10]) == [1,-2,3]

def solve(inp, first=0):
  pp = parse(inp)
  p0, p1, p2 = pp[first:first+3]
  A = [
          [ p0.vy - p1.vy, p1.vx - p0.vx, 0, p1.y - p0.y, p0.x - p1.x, 0 ],
          [ 0, p0.vz - p1.vz, p1.vy - p0.vy, 0, p1.z - p0.z, p0.y - p1.y ],
          [ p1.vz - p0.vz, 0, p0.vx - p1.vx, p0.z - p1.z, 0, p1.x - p0.x ],
          [ p0.vy - p2.vy, p2.vx - p0.vx, 0, p2.y - p0.y, p0.x - p2.x, 0 ],
          [ 0, p0.vz - p2.vz, p2.vy - p0.vy, 0, p2.z - p0.z, p0.y - p2.y ],
          [ p2.vz - p0.vz, 0, p0.vx - p2.vx, p0.z - p2.z, 0, p2.x - p0.x ],
      ]
  b = [
          -p0.vx * p0.y + p0.x * p0.vy + p1.vx * p1.y - p1.x * p1.vy,
          -p0.vy * p0.z + p0.y * p0.vz + p1.vy * p1.z - p1.y * p1.vz,
          -p0.vz * p0.x + p0.z * p0.vx + p1.vz * p1.x - p1.z * p1.vx,
          #
          -p0.vx * p0.y + p0.x * p0.vy + p2.vx * p2.y - p2.x * p2.vy,
          -p0.vy * p0.z + p0.y * p0.vz + p2.vy * p2.z - p2.y * p2.vz,
          -p0.vz * p0.x + p0.z * p0.vx + p2.vz * p2.x - p2.z * p2.vx,
      ]
  pv = PV(*cramer(A, b))
  return pv.x + pv.y + pv.z

assert solve(example_input) == 47

real_input = open('inputs/day24.input.txt').read()
print(solve(real_input)) # => 695832176624149
