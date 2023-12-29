#!/usr/bin/env python3

example_input = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

def parse(inp):
    paragraphs = inp.split("\n\n")
    workflows = {}
    for line in paragraphs[0].strip().splitlines():
        name, rest = line.split("{")
        workflows[name] = rest.strip("}").split(",")
    ratings = []
    for line in paragraphs[1].strip().splitlines():
        rating = {}
        for piece in line.strip("{}").split(","):
            v, x = piece.split("=")
            rating[v] = int(x)
        ratings.append(rating)
    return workflows, ratings

def apply1(workflow, rating):
    for rule in workflow:
        if ":" not in rule:
            return rule
        l, outcome = rule.split(':')
        v = l[0]
        op = l[1]
        x = int(l[2:])
        if op == '<':
            if rating[v] < x:
                return outcome
        elif op == '>':
            if rating[v] > x:
                return outcome
    assert False, f'Fell off end of apply1({workflow}, {rating})'

def run1(workflows, rating):
    wf_name = "in"
    while wf_name not in "AR":
        wf_name = apply1(workflows[wf_name], rating)
    if wf_name == 'A':
        return sum(rating.values())
    return 0

def run(workflows, ratings):
    tot = 0
    for rating in ratings:
        tot += run1(workflows, rating)
    return tot

assert run(*parse(example_input)) == 19114

real_input = open('inputs/day19.input.txt').read().strip()
print(run(*parse(real_input))) # => 319062
