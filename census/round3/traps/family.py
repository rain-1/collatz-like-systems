"""Theorem F census: trap sets that work for a whole congruence family.

For odd a0, b0 mod 2^k, the avoider graph G_k^A of C_{a,b} (n/2 on evens,
a n + b on odds) depends only on (a mod 2^k, b mod 2^k).  If every SCC of
G_k^A is trivial or a simple cycle (type F), Theorem F gives, for EVERY
odd a, b >= 1 in the class, the statement: every positive orbit of C_{a,b}
meets A or ends in a positive-integer lift of one of the simple cycles.
This script lists the minimal type-F sets for every class (a0, b0).
Usage: python3 family.py k odd|all
"""
import sys, json
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
from traps_lib import *


def is_typeF(T, A, k):
    adj = build_graph(T, k, A, k)
    for comp in tarjan(adj):
        ie = internal_edges(adj, comp)
        if not ie:
            continue
        out = {}
        for (u, s, i) in ie:
            out[u] = out.get(u, 0) + 1
        if any(d != 1 for d in out.values()) or len(out) != len(comp):
            return False
    return True


def simple_cycles_of(T, A, k):
    adj = build_graph(T, k, A, k)
    cyc = []
    for comp in tarjan(adj):
        ie = internal_edges(adj, comp)
        if not ie:
            continue
        nxt = {u: s for (u, s, i) in ie}
        c0 = comp[0]; c = [c0]; y = nxt[c0]
        while y != c0:
            c.append(y); y = nxt[y]
        o = sum(1 for r in c if r % 2 == 1)
        E = sum(1 for r in c if r % 2 == 0)
        cyc.append({"nodes": c, "odd_steps": o, "halvings": E})
    return cyc


def run(k, universe):
    K = 1 << k
    U = [r for r in range(K) if universe == 'all' or r % 2]
    n = len(U)
    out = {}
    for a0 in range(1, K, 2):
        for b0 in range(1, K, 2):
            T = collatz_a(a0, b=b0)
            mins = []
            for s in sorted(range(1 << n), key=lambda s: (bin(s).count('1'), s)):
                if any(s & m == m for m in mins):
                    continue
                A = {U[j] for j in range(n) if s >> j & 1}
                if is_typeF(T, A, k):
                    mins.append(s)
            out[f"{a0},{b0}"] = [[U[j] for j in range(n) if s >> j & 1] for s in mins]
    return out


if __name__ == "__main__":
    k, uni = int(sys.argv[1]), sys.argv[2]
    out = run(k, uni)
    json.dump(out, open(f"family_k{k}_{uni}.json", "w"), indent=1)
    for key, v in out.items():
        print(key, "min size", min(map(len, v)) if v else None, "count", len(v),
              [x for x in v if len(x) == min(map(len, v))][:6])
