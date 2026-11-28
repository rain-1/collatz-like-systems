#!/usr/bin/env python3
"""classify6.py -- complete certificate classification of the family

   D6(u1, v1, u5, v5):  2|n -> n/2;  else 3|n -> n/3;  n = 1 (mod 6) -> u1 n + v1;
                        n = 5 (mod 6) -> u5 n + v5,       gcd(u1, 6) = gcd(u5, 6) = 1,

which contains div23_5n1 (u1 = u5 = 5, v1 = v5 = 1) and every table of the M_6 scan.
The residue graph G_6 depends only on the successor pattern s1 = u1 + v1, s5 = 5 u5 + v5
(mod 6); its simple cycles are enumerated per pattern, each with its multiplier
u1^a u5^b / (2^c 3^d).  By the dichotomy theorem (round 3), D6 has a descent certificate iff
there is no division-free cycle and every simple cycle contracts.  Output: the table of
conditions per pattern (out/classify6.md).  Run with `check` to compare against decide.py on a
grid (exits 1 on a mismatch).
"""
import itertools
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def graph(s1, s5):
    return {0: [0, 3], 2: [1, 4], 4: [2, 5], 3: [1, 3, 5], 1: [s1], 5: [s5]}


MULT = {0: (0, 0, 1, 0), 2: (0, 0, 1, 0), 4: (0, 0, 1, 0), 3: (0, 0, 0, 1),
        1: (1, 0, 0, 0), 5: (0, 1, 0, 0)}          # exponents of (u1, u5, 2, 3) (sign: 2,3 divide)


def simple_cycles(G):
    out = []
    nodes = sorted(G)
    for start in nodes:
        stack = [(start, [start])]
        while stack:
            v, path = stack.pop()
            for s in G[v]:
                if s == start:
                    out.append(list(path))
                elif s > start and s not in path:
                    stack.append((s, path + [s]))
    return out


def monomial(cyc):
    a = b = c = d = 0
    for r in cyc:
        x = MULT[r]
        a += x[0]
        b += x[1]
        c += x[2]
        d += x[3]
    return (a, b, c, d)


def conditions(s1, s5):
    """None if a division-free cycle exists (1 -> 1, 5 -> 5 or 1 <-> 5); else the set of
    monomials (a, b, c, d) with a + b > 0 that must satisfy u1^a u5^b < 2^c 3^d."""
    if s1 == 1 or s5 == 5 or (s1 == 5 and s5 == 1):
        return None
    mons = set()
    for cyc in simple_cycles(graph(s1, s5)):
        m = monomial(cyc)
        if m[0] + m[1] > 0:
            mons.add(m)
    # drop monomials implied by others (m implied by m' if m = m' + (pure division cycle) ...):
    # keep it simple and exact: drop m if some other m' has the same (a, b) and smaller (c, d)
    keep = set()
    for m in mons:
        if not any(m2 != m and m2[0] == m[0] and m2[1] == m[1] and m2[2] <= m[2] and m2[3] <= m[3]
                   for m2 in mons):
            keep.add(m)
    return sorted(keep)


def cert(u1, u5, s1, s5):
    cs = conditions(s1, s5)
    if cs is None:
        return None
    return all(u1 ** a * u5 ** b < 2 ** c * 3 ** d for (a, b, c, d) in cs)


def fmt(m):
    a, b, c, d = m
    lhs = "*".join(([f"u1^{a}" if a > 1 else "u1"] if a else []) + ([f"u5^{b}" if b > 1 else "u5"] if b else []))
    return f"{lhs} < {2 ** c * 3 ** d}"


def table():
    L = ["| s1 = u1+v1 mod 6 | s5 = 5u5+v5 mod 6 | certificate exists iff |", "|---|---|---|"]
    for s1 in range(6):
        for s5 in range(6):
            cs = conditions(s1, s5)
            if cs is None:
                txt = "never (division-free cycle)"
            elif not cs:
                txt = "always"
            else:
                txt = " and ".join(fmt(m) for m in cs)
            L.append(f"| {s1} | {s5} | {txt} |")
    return "\n".join(L)


def check():
    import twlib
    bad = n = 0
    us = [1, 5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35, 37]
    for u1 in us:
        for u5 in us:
            for v1 in range(-6, 7):
                for v5 in range(-6, 7):
                    tab = [(1, 0, 2), (u1, v1, 1), (1, 0, 2), (1, 0, 3), (1, 0, 2), (u5, v5, 1)]
                    if u1 + v1 < 1 or 5 * u5 + v5 < 1:
                        continue
                    s1, s5 = (u1 + v1) % 6, (5 * u5 + v5) % 6
                    c = cert(u1, u5, s1, s5)
                    if c is None:
                        lev = twlib.classify_level(6, tab, 6)
                        ok = "z" in lev["types"]
                    else:
                        d = twlib.D.decide(6, tab, want_cycles=False, want_depth=False)
                        ok = (d["verdict"] == "CERT") == c
                    n += 1
                    if not ok:
                        bad += 1
                        print("MISMATCH", u1, v1, u5, v5)
    print(f"classify6: {n} tables compared with decide.py, {bad} mismatches")
    return bad == 0


if __name__ == "__main__":
    open(os.path.join(HERE, "out", "classify6.md"), "w").write(table() + "\n")
    print(table())
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        sys.exit(0 if check() else 1)
