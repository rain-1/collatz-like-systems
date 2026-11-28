#!/usr/bin/env python3
"""Checks for family.md (classification of SPLIT(a,b,d)).

Claims tested (exact integer arithmetic):
  T1  the classification table (a,b <= 7, d <= 15) and its class counts
  T2  Lemma V (valuations) on all residues needed, ranges and random 256-bit inputs
  T3  Lemma C (class C descent and invariance of [1,d]) for every class-C member and for
      SPLIT(1,1,d), d <= 199; cycle minima <= d
  T4  Theorem D (every odd value strictly increases, stays odd) for all class-D members
  T5  Theorem K (phi(S(n)) = P_c(phi(n)), exactly two raw steps per S-step) for all class-K members
      in the table and for c = 3, 7 with d up to 99; the corollary cycle correspondence for
      SPLIT(1,3,1) <-> Collatz and SPLIT(3,1,3) <-> 3x+3 (small cycles)
  T6  Lemma S (scaling conjugacy) and Lemma R (a-branch lands in eZ; b-branch contracts)
  E1  EVIDENCE only: the cycle lists quoted for class O members (starts <= 3000, cap 10^40)
Exit 0 iff all pass.  Runtime about 20 s.
"""
import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from family_lib import vals, classify, canonical, certifiable, drift, scale
from systems import split_step, par_step

random.seed(20261127)
FAIL = []


def ok(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("FAIL:", msg)


def S(step, n):
    """first odd value after odd n, and the number of raw steps used"""
    x = step(n)
    k = 1
    while x % 2 == 0:
        x = step(x)
        k += 1
    return x, k


# T1 ------------------------------------------------------------------------
TABLE = """\
1 1 | P P P P P P P P
1 3 | K C K C K C K C
1 5 | O O R O O O O R
1 7 | K O K R K O K O
3 1 | C K C K C K C K
3 3 | P P P P P P P P
3 5 | O D R D O D O D
3 7 | O O O O O O O O
5 1 | O O R O O O O R
5 3 | D O D O D O D R
5 5 | P P P P P P P P
5 7 | D O D O D O D O
7 1 | O K O K O K O K
7 3 | O O O R O O O O
7 5 | O D O D O D O D
7 7 | P P P P P P P P"""
counts = {}
for line in TABLE.splitlines():
    ab, cl = line.split('|')
    a, b = map(int, ab.split())
    for d, c in zip(range(1, 16, 2), cl.split()):
        got = classify(a, b, d)[0]
        ok(got == c, f"T1 table {a,b,d}: {got} != {c}")
        counts[c] = counts.get(c, 0) + 1
ok(counts == {'P': 32, 'C': 8, 'K': 16, 'D': 16, 'R': 8, 'O': 48}, f"T1 counts {counts}")
# reductions quoted in family.md
for (a, b, d), tgt in {(1, 5, 5): (1, 5, 1), (1, 5, 15): (1, 5, 3), (1, 7, 7): (7, 1, 1),
                       (3, 5, 5): (3, 5, 1), (5, 1, 5): (5, 1, 1), (5, 1, 15): (5, 1, 3),
                       (5, 3, 15): (5, 3, 3), (7, 3, 7): (3, 7, 1)}.items():
    c = canonical(a, b, d)
    ok(c[0] == tgt and c[1] == 'O', f"T1 reduction {a,b,d} -> {c}")
print("T1 table and counts:", counts)

# T2 Lemma V ----------------------------------------------------------------
for a in range(1, 33, 2):
    for b in range(1, 33, 2):
        for d in range(1, 33, 2):
            va, vb = vals(a, b, d)
            for n in list(range(1, 400, 2)) + [random.getrandbits(256) | 1 for _ in range(4)]:
                if n % 4 == 1:
                    x, v = a * n + d, va
                else:
                    x, v = b * n + d, vb
                ok(x % (2 ** v) == 0, f"T2 {a,b,d,n}")
                if v == 1:
                    ok((x // 2) % 2 == 1, f"T2 exact {a,b,d,n}")
print("T2 Lemma V done")

# T3 Lemma C ----------------------------------------------------------------
cmembers = [(a, b, d) for (a, b) in [(1, 1), (3, 1), (1, 3)] for d in range(1, 200, 2)
            if certifiable(a, b, d)]
ok(len(cmembers) == 200, f"T3 count {len(cmembers)}")
for (a, b, d) in cmembers:
    st = split_step(a, b, d)
    tests = list(range(d + 2, d + 3000, 2)) + [random.getrandbits(200) | 1 for _ in range(20)]
    for n in tests:
        if n % 2 == 1:
            ok(S(st, n)[0] < n, f"T3 descent {a,b,d,n}")
    for n in range(1, d + 1, 2):
        ok(1 <= S(st, n)[0] <= d, f"T3 invariance {a,b,d,n}")
print("T3 Lemma C done for", len(cmembers), "members")

# T4 Theorem D --------------------------------------------------------------
dm = [(a, b, d) for a in (1, 3, 5, 7) for b in (1, 3, 5, 7) for d in range(1, 16, 2)
      if classify(a, b, d)[0] == 'D']
ok(len(dm) == 16, "T4 count")
for (a, b, d) in dm:
    st = split_step(a, b, d)
    for n in list(range(1, 20001, 2)) + [random.getrandbits(256) | 1 for _ in range(50)]:
        y, k = S(st, n)
        ok(y > n and k == 2, f"T4 {a,b,d,n}")
print("T4 Theorem D done:", dm)

# T5 Theorem K --------------------------------------------------------------
km = [(a, b, d) for a in (1, 3, 5, 7) for b in (1, 3, 5, 7) for d in range(1, 16, 2)
      if classify(a, b, d)[0] == 'K']
ok(len(km) == 16, "T5 count")
extra = [(1, c, d) for c in (3, 7) for d in range(1, 100, 4)] + \
        [(c, 1, d) for c in (3, 7) for d in range(3, 100, 4)]
for (a, b, d) in km + extra:
    va, vb = vals(a, b, d)
    assert va == 1 and vb == 1 and min(a, b) == 1
    c = max(a, b)
    st = split_step(a, b, d)
    P = par_step(c, d * (c - 1) // 2)
    for n in list(range(1, 6001, 2)) + [random.getrandbits(300) | 1 for _ in range(30)]:
        y, k = S(st, n)
        ok(k == 2, f"T5 two steps {a,b,d,n}")
        x = (n - d) // 2
        ok((n - d) % 2 == 0 and (y - d) // 2 == P(x), f"T5 conj {a,b,d,n}")
# corollary: SPLIT(1,3,1): cycles through 1 and 3 <-> Collatz {0}, {1,2}
st = split_step(1, 3, 1)
C = par_step(3, 1)
for n in (1, 3):
    x = (n - 1) // 2
    orb, y = [n], S(st, n)[0]
    while y != n:
        orb.append(y)
        y = S(st, y)[0]
    xo = [(m - 1) // 2 for m in orb]
    ok(all(C(xo[i]) == xo[(i + 1) % len(xo)] for i in range(len(xo))), f"T5 cycle {n}")
# SPLIT(3,1,3) <-> x/2,(3x+3)/2 on x >= -1
st = split_step(3, 1, 3)
P = par_step(3, 3)
for n in range(1, 4001, 2):
    ok((S(st, n)[0] - 3) // 2 == P((n - 3) // 2), f"T5 split_3 {n}")
print("T5 Theorem K done for", len(km) + len(extra), "members")

# T6 Lemma S and R ------------------------------------------------------------
for a in (1, 3, 5, 7):
    for b in (1, 3, 5, 7):
        for d in (3, 5, 7, 9, 15, 21, 25, 45):
            for e in [e for e in range(3, d + 1, 2) if d % e == 0]:
                a2, b2, d2 = scale(a, b, d, e)
                T, T2 = split_step(a, b, d), split_step(a2, b2, d2)
                for m in list(range(1, 3000)) + [random.getrandbits(150) for _ in range(10)]:
                    if m > 0:
                        ok(T(e * m) == e * T2(m), f"T6 S {a,b,d,e,m}")
for a in (1, 3, 5, 7):
    for b in (1, 3, 5, 7):
        for d in range(1, 16, 2):
            cls, info = classify(a, b, d)
            if cls != 'R':
                continue
            from math import gcd
            va, vb = vals(a, b, d)
            if gcd(d, a) > 1 and b < 2 ** vb:
                e, mult, other, vo, cls1 = gcd(d, a), a, b, vb, 1
            else:
                e, mult, other, vo, cls1 = gcd(d, b), b, a, va, 3
            ok(other < 2 ** vo, f"T6 R contract {a,b,d}")
            for n in range(cls1, 20000, 4):
                ok((mult * n + d) % e == 0, f"T6 R lands {a,b,d,n}")
print("T6 Lemmas S, R done")

# E1 evidence -----------------------------------------------------------------
def cycles(a, b, d, N=3000, cap=10 ** 40):
    st = split_step(a, b, d)
    cyc, esc = {}, 0
    for n0 in range(1, N + 1):
        seen, x = set(), n0
        while x not in seen and x < cap:
            seen.add(x)
            x = st(x)
        if x >= cap:
            esc += 1
            continue
        c, y = [x], st(x)
        while y != x:
            c.append(y)
            y = st(y)
        cyc[min(c)] = len(c)
    return cyc, esc

QUOTED = {(5, 1, 3): {1: 4, 3: 2, 5: 5, 61: 10, 125: 11}, (5, 1, 7): {1: 11, 7: 2, 9: 7, 25: 8},
          (5, 1, 1): {1: 5, 13: 35}, (1, 5, 1): {1: 2},
          (1, 5, 3): {1: 3, 3: 5, 39: 35, 47: 11, 79: 12, 103: 12},
          (7, 1, 1): {1: 4}, (7, 1, 5): {1: 7, 5: 4, 9: 9}, (1, 7, 3): {1: 3, 3: 4},
          (5, 3, 3): {1: 4, 3: 3, 21: 6, 61: 10}, (5, 7, 3): {1: 4, 3: 4, 5: 18, 61: 10, 181: 68}}
for key, want in QUOTED.items():
    got, esc = cycles(*key)
    ok(got == want and esc == 0, f"E1 {key}: {got} {esc}")
got, esc = cycles(3, 7, 1)
ok(got == {1: 3, 19: 23, 23: 9, 31: 9} and 500 < esc < 700, f"E1 (3,7,1) {got} {esc}")
print("E1 evidence cycle lists reproduced")

print("drift (5,1,3) %.3f, (3,7,1) %.3f" % (drift(5, 1, 3), drift(3, 7, 1)))
if FAIL:
    print(len(FAIL), "FAILURES")
    sys.exit(1)
print("ALL PASS")
