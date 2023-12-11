#!/usr/bin/env python3

example_input = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen """

numbers = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
}

def first_digit(line):
    while line:
        for name, digit in numbers.items():
            if line.startswith(name) or line.startswith(digit):
                return digit
        line = line[1:]
    return '0'

def last_digit(line):
    while line:
        for name, digit in numbers.items():
            if line.endswith(name) or line.endswith(digit):
                return digit
        line = line[:-1]
    return '0'

def sum_first_and_last_digits(s):
    tot = 0
    for line in s.splitlines():
        n = int(first_digit(line) + last_digit(line))
        tot += n
    return tot

assert sum_first_and_last_digits(example_input) == 281

with open('inputs/day01.input.txt', 'r') as f:
    full_input = f.read()

print(sum_first_and_last_digits(full_input)) # => 54110
