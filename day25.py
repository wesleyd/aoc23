#!/usr/bin/env python3

import copy
import math

from collections import defaultdict
from dataclasses import dataclass
from heapdict import heapdict
from typing import Any, Dict, Generator, Iterable, Iterator, List, Optional, Set, Tuple, TypeVar

example_input = """
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

@dataclass
class Apparatus:
    edges: Dict[str, Set[str]]
    vertices: Set[str]
    def all_edges(self) -> Set[Tuple[str, str]]:
        ee = set()
        for p in self.vertices:
            for q in self.edges.get(p, []):
                ee.add((p, q))
        return ee

def parse(inp):
    e = defaultdict(set)
    v = set()
    for line in inp.strip().splitlines():
        p, qq = line.split(":")
        v.add(p)
        for q in qq.strip().split():
            e[p].add(q)
            e[q].add(p)
            v.add(q)
    return Apparatus(edges=e, vertices=v)

example_apparatus = parse(example_input)

def reachable(a: Apparatus, o: str) -> Set[str]:
    """Returns all the vertices reachable from o in a."""
    visited = set()
    unvisited = [o]
    while unvisited:
        p = unvisited.pop()
        visited.add(p)
        for q in a.edges.get(p, []):
            if q in visited:
                continue
            unvisited.append(q)
    return visited

def without(a: Apparatus, edges: List[Tuple[str, str]]) -> Apparatus:
    """Returns a new Apparatus without edges."""
    b = copy.deepcopy(a)
    for p, q in edges:
        if p in b.edges:
            b.edges[p].discard(q)
        if q in b.edges:
            b.edges[q].discard(p)
    return b

def partitions(a: Apparatus) -> List[Set[str]]:
    """Returns a's partitions."""
    pp = []
    def known(v):
        for p in pp:
            if v in p:
                return True
        return False
    for v in a.vertices:
        if known(v):
            continue
        pp.append(reachable(a, v))
    return pp
assert len(partitions(without(example_apparatus, [('hfx', 'pzl'), ('bvb', 'cmg'), ('nvd', 'jqt')]))) == 2

def peek(it):
    """Return 'first' (or arbitrary, if no order) entry in it."""
    return iter(it).__next__()
assert peek(set((1,2,3))) in (1,2,3)

def shortest_paths(a: Apparatus, o: Optional[str] = None) -> Generator[List[str], None, None]:
    """Yields shortest paths to everywhere from somewhere (or o)."""
    o = peek(a.vertices)
    dist = {o: 0}
    prev = {}
    q = heapdict()
    q[o] = 0
    while q:
        u, _ = q.popitem()
        for v in a.edges[u]:
            alt = dist.get(u, math.inf) + 1
            if alt < dist.get(v, math.inf):
                dist[v] = alt
                q[v] = alt
                prev[v] = u
    for v in prev:
        path = [v]
        u = prev[v]
        while u:
            path.append(u)
            u = prev.get(u, None)
        path.reverse()
        yield path

def longest_shortest_path(a: Apparatus, o: Optional[str] = None) -> List[str]:
    lsp = []
    for p in shortest_paths(a):
        if len(p) > len(lsp):
            lsp = p
    return lsp

def pathify(lst: List[str]) -> List[Tuple[str, str]]:
    """Turns a list of points into a list of pairs of points."""
    ret = []
    for i in range(len(lst)-1):
        ret.append((lst[i], lst[i+1]))
    return ret

def cut3(a: Apparatus):
    """Find three weakest links, assuming they exist."""
    # Pick an arbitrary point to start with (and if it doesn't work, try the next one...)
    for o in a.vertices:
        # Big assumption: that one of the three weak links is in the longest shortest path...
        lsp1 = set(pathify(longest_shortest_path(a, o)))
        #print(f'o={o} : longest path has {len(lsp1)} elements: {lsp1}')
        for e1 in lsp1:
            b = without(a, [e1])
            # And let's assume that the longest path crosses one of the other two...
            lsp2 = set(pathify(longest_shortest_path(b, o)))
            # ...but that the first longest shortest path didn't...
            lsp2 -= lsp1
            #print(f'  Trying e1={e1}, lsp has{len(lsp2)} elements')
            for e2 in lsp2:
                c = without(b, [e2])
                lsp3 = set(pathify(longest_shortest_path(c, o)))
                # Again, let's assume that *this* LSP crosses the final link...
                lsp3 -= lsp2
                lsp3 -= lsp1
                #print(f'    e2={e2} : trying {len(lsp3)} elements')
                for e3 in lsp3 - lsp2 - lsp1:
                    # ...which we can test for by removing it...
                    d = without(c, [e3])
                    #print(f'      Removing e3={e3}...')
                    parts = partitions(d)
                    if len(parts) > 1:
                        lens = [len(part) for part in parts]
                        #print('      ', e1, e2, e3, lens)
                        return lens[0] * lens[1]
cut3(example_apparatus)

real_input = open('inputs/day25.input.txt').read()
real_apparatus = parse(real_input)
print(cut3(real_apparatus))
