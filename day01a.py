#!/usr/bin/env python3

example_input = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

def first_digit(line):
    for c in line:
        if c.isdigit():
            return c
    return 0

def last_digit(line):
    return first_digit(reversed(line))

def sum_first_and_last_digits(s):
    tot = 0
    for line in s.splitlines():
        tot += int(first_digit(line) + last_digit(line))
    return tot

assert sum_first_and_last_digits(example_input) == 142

with open('inputs/day01.input.txt', 'r') as f:
    full_input = f.read()

print(sum_first_and_last_digits(full_input)) # => 54968
