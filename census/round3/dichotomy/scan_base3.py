#!/usr/bin/env python3
"""Phase diagram of base-3 families (application (3a)).  Exhaustive; every verdict is
exactly verified by decide.py (integer potential or exact expanding/critical cycle).

Family B(Q, a, S):  3|n -> n/3;  n mod Q in S -> a n + 1;  other 3 not| n -> n + 1,
    Q in {9, 27},  a in {2, 4, 5, 7, 8, 10, 11, 13},  S any subset of the units mod Q.
Family C9(choice):  3|n -> n/3;  n = r (mod 9), 3 not| r -> one of the 8 maps
    n+1, n+2, 2n+1, 2n-1, 4n+1, 4n-1, 5n+1, 5n-1   (8^6 = 262144 systems).

Output: scan_base3.out (summary) and scratch/base3_cert.txt (all CERT systems with
k*, so that the deep ones can be re-run with full cycle lists).
Runtime: about 10 minutes in total (use `nice`).  Usage: python3 scan_base3.py [B9|B27|C9]...
"""
import sys, os, collections, itertools, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decide import decide, residue_graph, stopping_depth
from families import base3_S, base3_table

HERE = os.path.dirname(os.path.abspath(__file__))
which = sys.argv[1:] or ["B9", "B27", "C9"]
out = open(os.path.join(HERE, "scan_base3.out"), "a")
certf = open(os.path.join(HERE, "scratch", "base3_cert.txt"), "a")


def emit(s):
    print(s)
    out.write(s + "\n")
    out.flush()


def scanB(Q):
    units = [r for r in range(Q) if r % 3]
    for a in (2, 4, 5, 7, 8, 10, 11, 13):
        t0 = time.time()
        stat = collections.Counter()
        bysize = collections.Counter()
        total_by_size = collections.Counter()
        deep = []
        for mask in range(1 << len(units)):
            S = frozenset(units[i] for i in range(len(units)) if mask >> i & 1)
            tab = base3_S(Q, a, S)
            res = decide(Q, tab, want_cycles=False, want_depth=False)
            total_by_size[len(S)] += 1
            if res["verdict"] == "OBST":
                stat["OBST-" + res["obst"]["kind"]] += 1
                continue
            stat["CERT"] += 1
            bysize[len(S)] += 1
            k, nl = stopping_depth(Q, tab, residue_graph(Q, tab))
            deep.append((k, sorted(S)))
            certf.write(json.dumps(dict(fam=f"B{Q}", a=a, S=sorted(S), k=k, leaves=nl)) + "\n")
        deep.sort(reverse=True)
        mx = max(bysize) if bysize else None
        emit(f"B(Q={Q}, a={a}): {dict(stat)}  max|S| certifiable = {mx} of {len(units)} "
             f"(# at max = {bysize.get(mx)})  [{time.time()-t0:.0f}s]")
        emit(f"   CERT by |S|: {[(s, bysize[s], total_by_size[s]) for s in sorted(total_by_size)]}")
        for k, S in deep[:3]:
            emit(f"   deep: k*={k} S={S}")


C8 = [(1, 1), (1, 2), (2, 1), (2, -1), (4, 1), (4, -1), (5, 1), (5, -1)]


def scanC9():
    Q = 9
    units = [r for r in range(Q) if r % 3]
    t0 = time.time()
    stat = collections.Counter()
    by_logsum = collections.Counter()
    deep = []
    maxprod = []
    for combo in itertools.product(range(8), repeat=6):
        choice = {r: C8[c] for r, c in zip(units, combo)}
        tab = base3_table(Q, choice)
        res = decide(Q, tab, want_cycles=False, want_depth=False)
        if res["verdict"] == "OBST":
            stat["OBST-" + res["obst"]["kind"]] += 1
            continue
        stat["CERT"] += 1
        prod = 1
        for r in units:
            prod *= choice[r][0]
        k, nl = stopping_depth(Q, tab, residue_graph(Q, tab))
        deep.append((k, prod, combo))
        maxprod.append((prod, k, combo))
        certf.write(json.dumps(dict(fam="C9", combo=combo, k=k, leaves=nl)) + "\n")
    deep.sort(reverse=True)
    maxprod.sort(reverse=True)
    emit(f"C9 (8^6 systems): {dict(stat)}  [{time.time()-t0:.0f}s]")
    kdist = collections.Counter(d[0] for d in deep)
    emit(f"   k* distribution among CERT: {sorted(kdist.items())}")
    for k, prod, combo in deep[:5]:
        emit(f"   deep: k*={k} prod(a)={prod} maps={[C8[c] for c in combo]} on r={units}")
    for prod, k, combo in maxprod[:5]:
        emit(f"   largest prod(a): {prod} k*={k} maps={[C8[c] for c in combo]}")


for w in which:
    if w == "B9":
        scanB(9)
    elif w == "B27":
        scanB(27)
    elif w == "C9":
        scanC9()
