"""Exhaustive census of the S-family (even -> n/2; odd n -> 3n+1 if n mod 2^m
in S, else n+1) for m = 2..5: every subset S of odd residues is classified as
CERT (minimal stopping-time certificate found, exact) or OBST (exact 2-adic
periodic point with multiplier > 1 verified, so no certificate exists by
Lemma B).  Any subset in neither class is reported as UNKNOWN.
Not a per-system check (m=5 takes ~1-2 min).  Usage: python3 family_scan.py [maxm]"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from descent_lib import *
from systems import s_table

maxm = int(sys.argv[1]) if len(sys.argv) > 1 else 5
for m in range(2, maxm + 1):
    odd = list(range(1, 2 ** m, 2))
    stat = collections.Counter()
    bysize = collections.Counter()
    periods = collections.Counter()
    deepest = []
    for mask in range(1 << len(odd)):
        S = tuple(odd[i] for i in range(len(odd)) if mask >> i & 1)
        t = s_table(m, S)
        c = certificate(2, m, t, maxK=80, maxnodes=20000)
        if not c["ok"]:
            g = growing_cycle(2, m, t, extra=4)
            if g["cycle"] and g["check"] and g["check"][1] > g["check"][2]:
                verify_obstruction(2, m, t, g["point"])
                stat["OBST"] += 1
                periods[g["check"][0]] += 1
                continue
            c = certificate(2, m, t, maxK=300, maxnodes=10 ** 6)
            if not c["ok"]:
                stat["UNKNOWN"] += 1
                continue
        stat["CERT"] += 1
        bysize[len(S)] += 1
        deepest.append((c["k"], c["K"], c["size"], S))
    deepest.sort(reverse=True)
    print(f"m={m}: {dict(stat)}  certifiable by |S|: {sorted(bysize.items())}")
    print(f"   max |S| = {max(bysize)} of {len(odd)}; obstruction periods {sorted(periods.items())}")
    for row in deepest[:3]:
        print("   deepest (k, K, size, S):", row)
