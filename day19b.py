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
    return workflows

def apply1(workflow, rating):
    for rule in workflow:
        if ":" not in rule:
            yield (rating, rule)
            return
        blah, outcome = rule.split(':')
        v = blah[0]
        op = blah[1]
        x = int(blah[2:])
        if op == '<':
            if rating[v][1] < x:
                yield (rating, outcome)
                continue
            elif rating[v][0] < x and x <= rating[v][1]:
                r2 = dict(rating)
                r2[v] = (rating[v][0], x-1)
                yield(r2, outcome)
                rating[v] = (x, rating[v][1])
            elif x <= rating[v][0]:
                continue
            elif rating[v][0] == rating[v][1]:
                assert x == rating[v][0], f'{x}, {rating}'
                continue
        elif op == '>':
            if rating[v][0] > x:
                yield (rating, outcome)
                continue
            elif rating[v][1] <= x:
                continue
            elif rating[v][0] <= x and x < rating[v][1]:
                r2 = dict(rating)
                r2[v] = (x+1, rating[v][1])
                yield (r2, outcome)
                rating[v] = (rating[v][0], x)
            elif rating[v][0] == rating[v][1]:
                assert x == rating[v][0], f'{x}, {rating}'
    yield (rating, outcome)
    assert False, f'Fell off end of apply1({workflow}, {rating})'

def score(rating):
    return (
        (rating['x'][1] - rating['x'][0] + 1) *
        (rating['m'][1] - rating['m'][0] + 1) *
        (rating['a'][1] - rating['a'][0] + 1) *
        (rating['s'][1] - rating['s'][0] + 1)
    )

def run(workflows):
    tot = 0
    rating = { 'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000) }
    bundles = [(rating, 'in')]
    while bundles:
        rating, workflow_name = bundles.pop()
        workflow = workflows[workflow_name]
        bb = list(apply1(workflow, rating))
        for b in bb:
            if b[1] == 'A':
                tot += score(b[0])
            elif b[1] == 'R':
                pass
            else:
                bundles.append(b)
    return tot

assert run(parse(example_input)) == 167409079868000

real_input = open('inputs/day19.input.txt').read().strip()
print(run(parse(real_input))) # => 118638369682135
