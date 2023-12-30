#!/usr/bin/env python3

from collections import defaultdict
from dataclasses import dataclass

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

@dataclass
class Module:
    typ: str
    state: str
    targets: list[str]

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
    for name, module in wiring.items():
        for target_name in module.targets:
            if target_name not in wiring:
                continue
            target = wiring[target_name]
            if target.typ == '&':
                target.state[name] = 'low'
    return wiring

def run(wiring, n=1):
    npulses = defaultdict(int)
    while n > 0:
        n -= 1
        messages = [('button', 'broadcaster', 'low')]
        while messages:
            message = messages.pop(0)
            source, target, pulse = message
            #print(f'{source} -{pulse}-> {target}')
            npulses[pulse] += 1
            if target not in wiring:
                continue
            module = wiring[target]
            assert module.typ in '*&%', f'bad module type {module}'
            if module.typ == '*':
                for t in module.targets:
                    messages.append((target, t, pulse))
            elif module.typ == '&':
                module.state[source] = pulse
                send = 'low' if all([x == 'high' for x in module.state.values()]) else 'high'
                for t in module.targets:
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
                for t in module.targets:
                    messages.append((target, t, pulse))
    return npulses

def product(npulses):
    return functools.reduce(operator.mul, npulses.values())

assert run(parse(example1)) == {'low': 8, 'high': 4}
assert run(parse(example2), 1000) == {'low': 4250, 'high': 2750}
assert product(run(parse(example2), 1000)) == 11687500

real_input = open('inputs/day20.input.txt').read()
print(product(run(parse(real_input), 1000))) # => 791120136
