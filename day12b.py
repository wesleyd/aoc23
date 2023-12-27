#!/usr/bin/env python3

import math

import re

example_input = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

def parse1(line, mult):
    pat, commas = line.split()
    nums = [int(x) for x in commas.split(',')] 
    pat = "?".join([pat]*mult)
    nums *= mult
    return pat, nums

def can_match_at(pat, num, start):
    """Returns true if num can match at start in pat. Inefficiently."""
    if start+num > len(pat):
        return False
    if start > 0 and pat[start-1] not in '?.':
        return False
    if start+num < len(pat) and pat[start+num] not in '?.':
        return False
    for i in range(num):
        if pat[start+i] not in '?#':
            return False
    return True

def match_at(pat, num, start):
    if start+num > len(pat):
        return False, "", ""
    if start > 0 and pat[start-1] not in '?.':
        return False, "", ""
    if start+num < len(pat) and pat[start+num] not in '?.':
        return False, "", ""
    if start < 0:
        return False, "", ""
    for i in range(num):
        if pat[start+i] not in '?#':
            return False, "", ""
    l = ""
    if start > 1:
        l = pat[:start-1]
    return True, l, pat[start+num+1:]

def match(pat, nums, indent=0):
    if sum(nums) + len(nums) - 1 > len(pat):
        return 0
    if not nums:
        if '#' in pat:
            return 0
        else:
            return 1
    pat = pat.strip('.')
    if not pat:
        return 0
    if len(nums) == 1:
        tot = 0
        for i in range(len(pat)):
            y, l, r = match_at(pat, nums[0], i)
            if y and '#' not in l and '#' not in r:
                tot += 1
        return tot
    if '.' in pat:
        l, r = re.split('[.]+', pat, maxsplit=1)
        tot = 0
        for i in range(len(nums)+1):
            a = match(l, nums[:i], indent+1) 
            if a:
                tot += a * match(r, nums[i:], indent+1)
        return tot
    elif '#' in pat: # Mixture of question marks and hashes
        n = pat.find('#')
        tot = 0
        for i in range(len(nums)):
            for j in range(nums[i]):
                y, l, r = match_at(pat, nums[i], n-j)
                if not y:
                    continue
                a = match(l, nums[:i], indent+1)
                if a:
                    a *= match(r, nums[i+1:], indent+1)
                tot += a
        return tot
    else:  # Only question marks!
        n = len(pat) - sum(nums) + 1
        k = len(nums)
        c = math.comb(n, k)
        return c

def run(lines, mult=1):
    tot = 0
    for line in lines.splitlines():
        if not line:
            continue
        pat, nums = parse1(line, mult)
        n = match(pat, nums)
        tot += n
    return tot

assert run("????? 1") == 5
assert run("????? 1,1") == 6
assert run("?????? 1,1") == 10
assert run("??????? 1,1") == 15
assert run("?????? 1,1,1") == 4
assert run("????????? 2,2,2") == 4
assert run("#.#.### 1,1,3") == 1
assert run(".??..??...?##. 1,1,3") == 4
assert run("?#?#?#?#?#?#?#? 1,3,1,6") == 1
assert run("????.#...#... 4,1,1") == 1
assert run("????.######..#####. 1,6,5") == 4
assert run("?###???????? 3,2,1") == 10

assert run(example_input) == 21

real_input = open('inputs/day12.input.txt').read()
#assert run(real_input) == 7718

assert run("???.### 1,1,3", 5) == 1
assert run(".??..??...?##. 1,1,3", 5) == 16384
assert run("?#?#?#?#?#?#?#? 1,3,1,6", 5) == 1
assert run("????.#...#... 4,1,1", 5) == 16
assert run("????.######..#####. 1,6,5", 5) == 2500
assert run("?###???????? 3,2,1", 5) == 506250

print(run(real_input, 5)) #  => 128741994134728
