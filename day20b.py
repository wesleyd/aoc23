#!/usr/bin/env python3

from collections import defaultdict
from dataclasses import dataclass, field

import math
import operator
import functools

example1 = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

example2 = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""

real_input = open('inputs/day20.input.txt').read()

@dataclass
class Module:
    typ: str
    state: str
    targets: list[str]
    received: dict[int] = field(default_factory=lambda: {'low': 0, 'high': 0})
    sent: dict[int] = field(default_factory=lambda: {'low': 0, 'high': 0})

def parse(inp):
    wiring = {}
    for line in inp.strip().splitlines():
        l, r = line.split(" -> ")
        targets = r.split(", ")
        if l[0] == '%':
            wiring[l[1:]] = Module(l[0], 'off', targets)
        elif l[0] == '&':
            wiring[l[1:]] = Module(l[0], {}, targets)
        else:
            wiring[l] = Module('*', None, targets)
    all_targets = set()
    for name, module in wiring.items():
        for target_name in module.targets:
            all_targets.add(target_name)
            if target_name not in wiring:
                continue
            target = wiring[target_name]
            if target.typ == '&':
                target.state[name] = 'low'
    for name in all_targets:
        if name not in wiring:
            wiring[name] = Module('=', '', [])
    return wiring

def run(wiring, goal='rx', goal_state=''):
    n = 0
    while True:
        n += 1
        messages = [('button', 'broadcaster', 'low')]
        while messages:
            message = messages.pop(0)
            source, target, pulse = message
            #print(f'{source} -{pulse}-> {target}')
            if target not in wiring:
                continue
            module = wiring[target]
            module.received[pulse] += 1
            assert module.typ in '=*&%', f'bad module type {module}'
            if module.typ == '*':
                for t in module.targets:
                    module.sent[pulse] += 1
                    messages.append((target, t, pulse))
            elif module.typ == '&':
                module.state[source] = pulse
                send = 'low' if all([x == 'high' for x in module.state.values()]) else 'high'
                if target == goal and (not goal_state or send == goal_state):
                    #print(f'{module.typ}{target} is about to send {goal_state} to {module.targets}, after {n} button pushes')
                    return n
                for t in module.targets:
                    module.sent[pulse] += 1
                    messages.append((target, t, send))
            elif module.typ == '%':
                if pulse == 'high':
                    continue
                assert pulse == 'low'
                assert module.state in ['on', 'off']
                if module.state == 'off':
                    module.state = 'on'
                    pulse = 'high'
                else:
                    module.state = 'off'
                    pulse = 'low'
                if target == goal and (not goal_state or module.state == goal_state):
                    #print(f'{module.typ}{target} just went {module.state}, after {n} button pushes')
                    return n
                for t in module.targets:
                    module.sent[pulse] += 1
                    messages.append((target, t, pulse))

def print_wiring(wiring, start="broadcaster", skip_inactive=True, include_state=True):
    printed = set()
    to_print = [start]
    while to_print:
        name = to_print.pop(0)
        if name in printed:
            continue
        m = wiring[name]
        if skip_inactive and sum(m.received.values()) == 0:
            continue
        print(f'{m.typ}{name} -> {", ".join(m.targets)}', end='')
        if include_state:
            print(f': {m.state} received={m.received} sent={m.sent}', end='')
        print()
        printed.add(name)
        for target in m.targets:
            to_print.append(target)

def invert(w):
    inv = defaultdict(list)
    for name, m in w.items():
        for t in m.targets:
            inv[t].append(name)
    return inv

def lcm(mm):
    if len(mm) > 2:
        return lcm([lcm([mm[0], mm[1]])] + mm[2:])
    else:
        return abs(mm[0]*mm[1]) // math.gcd(mm[0], mm[1])

def play(inp):
    p = parse(real_input)
    inv = invert(p)
    assert len(inv['rx']) == 1
    mm = []
    for x in inv[inv['rx'][0]]:
        mm.append(run(parse(real_input), goal=x, goal_state='high'))
    return lcm(mm)

print(play(real_input)) # => 215252378794009

