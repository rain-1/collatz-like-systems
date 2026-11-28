#!/usr/bin/env python3
"""Mixed-modulus family (Theorem 1 with Q = 2^a 3^b).  Exhaustive, exact verdicts.

D(Q, a, S):  2|n -> n/2;  else 3|n -> n/3;  else n -> a n + 1 if n mod Q in S, else n + 1,
for Q in {36, 72} restricted to S within the units mod Q, a in {5, 7}  (the census open maps
div23_5n1 / div23_7n1 have S = all units).
Q = 36: 2^12 subsets;  Q = 72: 2^24 is too many, so only |S| >= 20 is scanned there
(to locate the certifiability frontier near the open maps).
Output: scan_mixed.out.  Runtime ~3 minutes.
"""
import sys, os, collections, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decide import decide, residue_graph, stopping_depth

HERE = os.path.dirname(os.path.abspath(__file__))


def D_table(Q, a, S):
    t = []
    for r in range(Q):
        if r % 2 == 0:
            t.append((1, 0, 2))
        elif r % 3 == 0:
            t.append((1, 0, 3))
        else:
            t.append((a, 1, 1) if r in S else (1, 1, 1))
    return t


out = open(os.path.join(HERE, "scan_mixed.out"), "w")


def emit(s):
    print(s, flush=True)
    out.write(s + "\n")


for a in (5, 7):
    Q = 36
    units = [r for r in range(Q) if r % 2 and r % 3]
    stat = collections.Counter()
    bysize = collections.Counter()
    deep = []
    for mask in range(1 << len(units)):
        S = {units[i] for i in range(len(units)) if mask >> i & 1}
        t = D_table(Q, a, S)
        res = decide(Q, t, want_cycles=False, want_depth=False)
        stat[res["verdict"]] += 1
        if res["verdict"] == "CERT":
            bysize[len(S)] += 1
            k, _ = stopping_depth(Q, t, residue_graph(Q, t))
            deep.append((k, sorted(S)))
    deep.sort(reverse=True)
    emit(f"D(36,{a}): {dict(stat)}; CERT by |S|: {sorted(bysize.items())}; deepest {deep[:2]}")
    Q = 72
    units = [r for r in range(Q) if r % 2 and r % 3]
    best = collections.Counter()
    ex = {}
    for k in (24, 23, 22, 21, 20):
        for drop in itertools.combinations(units, 24 - k):
            S = set(units) - set(drop)
            res = decide(Q, D_table(Q, a, S), want_cycles=False, want_depth=False)
            if res["verdict"] == "CERT":
                best[k] += 1
                ex.setdefault(k, sorted(drop))
        if best[k]:
            break
    emit(f"D(72,{a}): largest certifiable |S| among 20..24: {dict(best)}; e.g. n+1 on {ex}")
