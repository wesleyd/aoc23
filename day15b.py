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

def make_boxes():
    return [[] for _ in range(256)]

def box_find(box, label):
    for i, lens in enumerate(box):
        if lens[0] == label:
            return i
    return -1

def apply(boxes, cmd):
    if cmd.endswith('-'):
        label = cmd[:-1]
        h = hash(label)
        box = boxes[h]
        i = box_find(box, label)
        if i != -1:
            boxes[h] = box[:i] + box[i+1:]
    elif '=' in cmd:
        label, r = cmd.split('=')
        h = hash(label)
        n = int(r)
        box = boxes[h]
        i = box_find(box, label)
        if i == -1:
            box.append((label, n))
        else:
            box[i] = (label, n)
    else:
        assert False, f'bad command {cmd!s}'

def focusing_power(boxes):
    tot = 0
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box):
            fp = i + 1
            fp *= j + 1
            fp *= lens[1]
            tot += fp
    return tot

def run(inp):
    boxes = make_boxes()
    cmds = inp.strip().split(',')
    for cmd in cmds:
        apply(boxes, cmd)
    return focusing_power(boxes)

assert run(example_input) == 145

real_input = open('inputs/day15.input.txt').read()
print(run(real_input))  # => 246762
