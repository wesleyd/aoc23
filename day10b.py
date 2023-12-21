#!/usr/bin/env python3

example_input1 = """
.....
.S-7.
.|.|.
.L-J.
.....
"""

example_input2 = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

example_input3 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

example_input4 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

example_input5 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

def at(maze, p):
    row, col = p
    if row < 0 or len(maze) <= row or col < 0 or len(maze[row]) <= col:
        return '.'
    return maze[row][col]

def up(p):
    return (p[0]-1, p[1])
def down(p):
    return (p[0]+1, p[1])
def left(p):
    return (p[0], p[1]-1)
def right(p):
    return (p[0], p[1]+1)

def parse(inp):
    maze = [list(x) for x in inp.splitlines() if x]
    for row, line in enumerate(maze):
        col =-1 
        if 'S' in line:
            col = line.index('S')
        if col >= 0:
            fix_start(maze, (row, col))
            return maze, (row, col)

def fix_start(maze, start):
    row, col = start
    if at(maze, up(start)) in 'F7|' and at(maze, left(start)) in 'FL-':
        maze[row][col] = 'J'
    elif at(maze, up(start)) in 'F7|'and at(maze, down(start)) in 'LJ|':
        maze[row][col] = '|'
    elif at(maze, up(start)) in 'F7|'and at(maze, right(start)) in 'J7-':
        maze[row][col] = 'L'
    elif at(maze, left(start)) in 'FL-' and at(maze, down(start)) in 'LJ|':
        maze[row][col] = '7'
    elif at(maze, left(start)) in 'FL-' and at(maze, right(start)) in 'J7-':
        maze[row][col] = '-'
    elif at(maze, down(start)) in 'LJ|' and at(maze, right(start)) in 'J7-':
        maze[row][col] = 'F'
    else:
        raise Exception(f'No join at start={start}')

def find_loop(maze, start):
    """Returns all the points in maze on the loop."""
    prev = {}
    fut = [(start, 0)]
    while fut:
        p, dist = fut.pop()
        px = at(maze, p)
        if p in prev and dist >= prev[p]:
            continue
        prev[p] = dist
        dist += 1
        u, d, l, r = up(p), down(p), left(p), right(p)
        if px in '|JLS' and at(maze, u) in 'F7|':
            fut.append((u, dist))
        if px in '|F7S' and at(maze, d) in 'JL|':
            fut.append((d, dist))
        if px in '-J7S' and at(maze, l) in 'FL-':
            fut.append((l, dist))
        if px in '-FLS' and at(maze, r) in 'J7-':
            fut.append((r, dist))
    return prev.keys()

def inside(maze, p, loop):
    """Is p inside loop?"""
    walls, lefts, rights = 0, 0, 0
    if p in loop:
        return False
    while p[0] < len(maze) and p[1] < len(maze[0]):
        p = (p[0] + 1, p[1])
        if p in loop:
            if at(maze,p) in '-':
                walls += 1
            #elif at(maze,p) in 'FL':
            #    rights += 1
            elif at(maze,p) in 'J7':
                lefts += 1
    lefts %= 2
    #rights %= 2
    walls += lefts
    return walls % 2

def hunt(inp):
    ninside = 0
    maze, start = parse(inp)
    loop = find_loop(maze, start)
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            p = (row, col)
            if inside(maze, p, loop):
                ninside += 1
    return ninside

assert hunt(example_input1) == 1
assert hunt(example_input2) == 1
assert hunt(example_input3) == 4
assert hunt(example_input4) == 8
assert hunt(example_input5) == 10

real_input = open("inputs/day10.input.txt").read()
print(hunt(real_input)) # => 417
