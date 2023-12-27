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
    dish = [list(line) for line in inp.splitlines() if line]
    return dish

def printable(dish):
    return '\n'.join(''.join(line) for line in dish)

def north_load(dish):
    load = 0
    for row in range(len(dish)):
        for col in range(len(dish[0])):
            if dish[row][col] == 'O':
                load += len(dish) - row
    return load

def roll_north(dish):
    for col in range(len(dish[0])):
        holes = []
        rocks = []
        for row in range(len(dish)):
            c = dish[row][col]
            if c == 'O' and holes:
                hole = holes.pop(0)
                dish[hole][col] = 'O'
                dish[row][col] = '.'
                holes.append(row)
            elif c == '.':
                holes.append(row)
            elif c == '#':
                holes = []
            else:
                assert f'Bad rock {c} at row={row},col={col}'
    pass

dish = parse(example_input)
roll_north(dish)
assert north_load(dish) == 136

real_input = open('inputs/day14.input.txt').read()
dish = parse(real_input)
roll_north(dish)
assert north_load(dish) == 110565

def roll_south(dish):
    for col in range(len(dish[0])):
        holes = []
        rocks = []
        for row in reversed(range(len(dish))):
            c = dish[row][col]
            if c == 'O' and holes:
                hole = holes.pop(0)
                dish[hole][col] = 'O'
                dish[row][col] = '.'
                holes.append(row)
            elif c == '.':
                holes.append(row)
            elif c == '#':
                holes = []
            else:
                assert f'Bad rock {c} at row={row},col={col}'
    pass

def roll_west(dish):
    for row in range(len(dish)):
        holes = []
        rocks = []
        for col in range(len(dish[0])):
            c = dish[row][col]
            if c == 'O' and holes:
                hole = holes.pop(0)
                dish[row][hole] = 'O'
                dish[row][col] = '.'
                holes.append(col)
            elif c == '.':
                holes.append(col)
            elif c == '#':
                holes = []
            else:
                assert f'Bad rock {c} at row={row},col={col}'
    pass

def roll_east(dish):
    for row in range(len(dish)):
        holes = []
        rocks = []
        for col in reversed(range(len(dish[0]))):
            c = dish[row][col]
            if c == 'O' and holes:
                hole = holes.pop(0)
                dish[row][hole] = 'O'
                dish[row][col] = '.'
                holes.append(col)
            elif c == '.':
                holes.append(col)
            elif c == '#':
                holes = []
            else:
                assert f'Bad rock {c} at row={row},col={col}'
    pass

def roll(dish):
    roll_north(dish)
    roll_west(dish)
    roll_south(dish)
    roll_east(dish)

dish = parse(example_input)
roll(dish)
assert printable(dish) == """
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....
""".strip()
roll(dish)
assert printable(dish) == """
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O
""".strip()
roll(dish)
assert printable(dish) == """
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
""".strip()

class SequenceFinder(object):
    def __init__(self, min_length=1):
        self.count = 0
        self.seq = []
        self.period = 0
        self.min_length = min_length
    def look_back(self, n):
        assert n>0, f'non-positive n={n}'
        if len(self.seq) < 2*self.min_length:
            return False
        for i in range(n, 0, -1):
            if self.seq[-i] != self.seq[-n-i]:
                return False
        return True
    def add(self, x):
        self.count += 1
        if self.period:
            period_start = len(self.seq) - self.period
            index = period_start + (self.count - 1 - period_start) % self.period
            predicted = self.seq[index]
            if x != predicted:
                assert False, f'Sequence violation predicted {predicted}@{index}; got {x}!'
            return True
        else:
            self.seq.append(x)
            if len(self.seq) < 2:
                return False
            for n in range(len(self.seq)//2, 0, -1):
                if self.look_back(n):
                    self.period = n
                    self.seq[-n:] = []
                    return True
            return False
    def goto(self, n):
        assert self.period > 0, 'no period found'
        if n < len(self.seq):
            return self.seq[n]
        period_start = len(self.seq) - self.period
        index = period_start + (n - period_start)%self.period
        return self.seq[index]

def rolln(dish, n):
    sf = SequenceFinder()
    for i in range(n):
        if sf.add(printable(dish)):
            dish = parse(sf.goto(n))
            break
        roll(dish)
    return north_load(dish)

dish = parse(example_input)
assert rolln(dish, 1000000000) == 64

real_input = open('inputs/day14.input.txt').read()
dish = parse(real_input)
print(rolln(dish, 1000000000)) # => 89845
