#!/usr/bin/env python3
"""Referee's independent check for CLS-057.md (Theorem F). Exact integers; exit 0 iff all pass.
Independent T (brute-force digit), agreement with census/round2/qr/systems.py, smallest-q table,
shared-coset list for m=3, and finite evidence that every in-coset class mod M meets every basin."""
import sys, os
from math import gcd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'round2', 'qr'))
from systems import get
bad = []
def T(q, m):
    def f(n):
        if n % 2 == 0: return n // 2
        c = next(c for c in range(m) if (n + c * q) % m == 0)
        return (n + c * q) // m
    return f
def info(q, m):
    t = T(q, m); cyc = {}
    for n in range(1, q + 1):
        seen = []; x = n
        while x not in seen: seen.append(x); x = t(x)
        c = tuple(seen[seen.index(x):]); cyc[min(c)] = c
    H = {1}; fr = [1]
    while fr:
        x = fr.pop()
        for g in (2 % q, m % q):
            y = x * g % q
            if y not in H: H.add(y); fr.append(y)
    by = {}
    for k in cyc:
        if gcd(k, q) == 1: by.setdefault(min(k * h % q for h in H), []).append(k)
    return t, cyc, {a: b for a, b in by.items() if len(b) > 1}
step = get("qrA3_q17")["step"]; t = T(17, 3)
if any(step(n) != t(n) for n in range(1, 100000)): bad.append("step mismatch")
exp = {3: 17, 5: 19, 7: 13, 9: 17, 11: 5, 13: 21, 15: 7, 17: 11, 19: 9, 21: 5}
for m, q0 in exp.items():
    q = next(q for q in range(2, 200) if gcd(q, 2 * m) == 1 and info(q, m)[2])
    if q != q0: bad.append(f"smallest q m={m}")
if not all(not info(q, m)[2] for q in range(3, 5) for m in range(3, 60, 2) if gcd(q, 2 * m) == 1):
    bad.append("q<5 member")
if [q for q in range(5, 200) if all(q % p for p in range(2, q)) and info(q, 3)[2]] != [17, 53, 67, 71, 97, 107, 109, 157]:
    bad.append("m=3 prime list")
for q, m, M, N in ((19, 5, 4 * 25 * 19, 10**6), (5, 11, 8 * 11 * 5 * 3, 10**6), (17, 3, 16 * 27 * 17, 10**6)):
    t, cyc, sh = info(q, m); cof = {x: k for k, c in cyc.items() for x in c}; memo = {}
    def b(n):
        p = []; x = n
        while x not in cof and x not in memo: p.append(x); x = t(x)
        r = cof[x] if x in cof else memo[x]
        for y in p: memo[y] = r
        return r
    hit = {}
    for n in range(1, N):
        if gcd(n, q) == 1: hit.setdefault(n % M, set()).add(b(n))
    G = set(list(sh.values())[0])
    if any(not G <= hit.get(r, set()) for r in range(M) if gcd(r, q) == 1): bad.append(f"class {q},{m}")
print("failures:", bad)
sys.exit(1 if bad else 0)
