#!/usr/bin/env python3

example_input = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

def parse1(line):
    pat, commas = line.split()
    nums = [int(x) for x in commas.split(',')] 
    return pat, nums

def matches(nums, pat, prefix=''):
    if not nums:
        if '#' in pat:
            return # Can't match
        else:
            yield prefix + pat.replace('?', '.')
            return # Can't match anything else
    if not pat:
        return # Didn't match
    if nums[0] > len(pat):
        return # Can't match
    if pat[0] == '.' or pat[0] == '?':
        yield from matches(nums, pat[1:], prefix+'.')
    first, second = pat[:nums[0]], pat[nums[0]:]
    hashes =  "#" * nums[0]
    mfirst = first.replace("?", "#")
    if mfirst == hashes:
        if len(nums) == 1:  # Doesn't need a space
            yield from matches([], second, prefix+hashes)
        elif len(second) > 0 and second[0] in "?.":
                yield from matches(nums[1:], second[1:], prefix+hashes+".")

assert len(list(matches([1,1,3], "???.###"))) == 1
assert len(list(matches([1,1,3], ".??..??...?##."))) == 4
assert len(list(matches([1,3,1,6], "?#?#?#?#?#?#?#?"))) == 1
assert len(list(matches([4,1,1], "????.#...#..."))) == 1
assert len(list(matches([1,6,5], "????.######..#####."))) == 4
assert len(list(matches([3,2,1], "?###????????"))) == 10

def run(inp):
    tot = 0
    for line in inp.splitlines():
        if not line:
            continue
        pat, nums = parse1(line)
        n = sum(1 for _ in matches(nums, pat))
        print(f'"{line}" => {n}')
        tot += n
    return tot

assert run(example_input) == 21

real_input = open('inputs/day12.input.txt').read()
print(run(real_input)) # =>  7718
