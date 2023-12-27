#!/usr/bin/env python3

def hash(s):
    curr = 0
    for c in s:
        n = ord(c)
        curr += n
        curr *= 17
        curr %= 256
    return curr

assert hash("HASH") == 52

example_input = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

def run(inp):
    return sum(hash(s) for s in inp.strip().split(','))

assert run("HASH") == 52
assert run(example_input) == 1320

real_input = open('inputs/day15.input.txt').read()
print(run(real_input))  # => 515210
