#!/usr/bin/env python3

from collections import defaultdict

example_input = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

tr = str.maketrans("J23456789TQKA", "*23456789:<>A")

def score(hand):
    """Returns a string-sortable score for hand."""
    cards = defaultdict(int)
    for c in hand:
        cards[c] += 1
    jokers = cards['J']
    del cards['J']
    counts = sorted(cards.values())
    if jokers == 5:
        counts = [5]
    else:
        counts[len(counts)-1] += jokers
    if counts == [5]:
        grade = "50"
    elif counts == [1, 4]:
        grade = "40"
    elif counts == [2, 3]:
        grade = "32"
    elif counts == [1, 1, 3]:
        grade = "30"
    elif counts == [1, 2, 2]:
        grade = "20"
    elif counts == [1, 1, 1, 2]:
        grade = "10"
    else:
        grade = "00"
    return grade + hand.translate(tr)

def rank(inp):
    camel = []
    for line in inp.splitlines():
        if not line:
            continue
        hand, bid = line.split(" ")
        camel.append((hand, int(bid), score(hand)))
    camel.sort(key=lambda t: t[2])
    winnings = 0
    for rank, c in enumerate(camel, start=1):
        winnings += rank * c[1]
    return winnings

assert rank(example_input) == 5905

with open("inputs/day07.input.txt") as f:
    real_input = f.read()

print(rank(real_input)) # => 251195607
