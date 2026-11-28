#!/usr/bin/env python3
"""Checks for basins.md.

Claims tested (exact integer arithmetic):
  B1  X_d = SPLIT(1,1,d), every odd d <= 301: the cycles are exactly C(K) for the cosets K of <2>
      in Z/d (formula for elements and length), their number is sum_{e|d} phi(e)/ord_e(2), and
      every n <= 4000 reaches the cycle of its coset
  B0  Sigma_d: the rule 'whichever of n+d, 3n+d is divisible by 4' equals SPLIT(3,1,d) for
      d = 1 mod 4 and SPLIT(1,3,d) for d = 3 mod 4; T(n) = n*{1,3,1/2} mod d (invariance);
      the shared-class table for d < 200 with gcd(d,6)=1 and for the catalog values 5,7,13,71,73,97,7081
  B3a for every class with a single cycle, all n <= 3000 (and random 120-bit n) of that class reach it
  B2  the constructive accessibility proof (access_lib.construct) on random targets, verified by
      forward iteration; identities used in Steps 1-2 (L2U2 vs U2L2 translation, 2 primitive root
      mod 3^j, U2(x) - d = (4/3)(x - d))
  B4  the identity f(4m+d) = f(3m+d) (three raw steps 4m+d -> 12m+4d -> 6m+2d -> 3m+d)
  E   EVIDENCE: for split_13 every unit residue r mod 936 contains members of both basins 1 and 5
Exit 0 iff all pass.  Runtime about 1 minute.
"""
import os
import random
import sys
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from basins_lib import sigma_step, x_step, all_cycles, orbit_classes, sigma_table, cycle_of
from systems import split_step
import access_lib as A

random.seed(7081)
FAIL = []


def ok(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("FAIL:", msg)


def phi(n):
    r, m, p = n, n, 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            r -= r // p
        p += 1
    if m > 1:
        r -= r // m
    return r


def ordmod(g, e):
    if e == 1:
        return 1
    k, x = 1, g % e
    while x != 1:
        x = x * g % e
        k += 1
    return k


# B1 ---------------------------------------------------------------------------
for d in range(1, 302, 2):
    st = x_step(d)
    cyc = all_cycles(st, d)
    lab, k = orbit_classes(d, [2])
    ok(len(cyc) == k == sum(phi(e) // ordmod(2, e) for e in range(1, d + 1) if d % e == 0),
       f"B1 count d={d}")
    pred = {}
    for r in range(1, d + 1):
        pred.setdefault(lab[r % d], set()).add(r)
    for K, Kh in pred.items():
        CK = Kh | {r + d for r in Kh if r % 2 == 1}
        c = cycle_of(st, min(Kh))
        ok(set(c) == CK and len(c) == len(Kh) + sum(1 for r in Kh if r % 2), f"B1 cycle d={d}")
    if d <= 99:
        for n in range(1, 4001):
            c = cycle_of(st, n)
            ok(lab[c[0] % d] == lab[n % d], f"B1 basin d={d} n={n}")
print("B1 done (d <= 301)")

# B0 ---------------------------------------------------------------------------
for d in range(1, 200, 2):
    st = sigma_step(d)
    ref = split_step(3, 1, d) if d % 4 == 1 else split_step(1, 3, d)
    for n in list(range(1, 3000)) + [random.getrandbits(120) for _ in range(20)]:
        ok(st(n) == ref(n), f"B0 rule d={d} n={n}")
        if gcd(d, 6) == 1:
            t = st(n) % d
            ok(t in (n % d, 3 * n % d, n * pow(2, -1, d) % d) or d == 1, f"B0 inv d={d} n={n}")

SHARED = {13: [[1, 5]], 29: [[1, 5, 7]], 31: [[1, 5]], 55: [[7, 23]], 61: [[1, 5, 7, 9, 21]],
          65: [[5, 25]], 67: [[5, 11]], 85: [[3, 7]], 91: [[7, 35]], 109: [[1, 5]], 113: [[1, 17]],
          119: [[11, 23, 37]], 125: [[1, 7, 9, 11, 21, 23, 31]], 127: [[1, 5, 9, 21]],
          131: [[9, 11, 17]], 139: [[5, 13]], 143: [[11, 55]], 145: [[1, 49], [5, 25, 35], [13, 19]],
          155: [[5, 25]], 161: [[3, 13]], 167: [[3, 7, 27], [5, 13]], 169: [[3, 11], [13, 65]],
          187: [[3, 15, 31]], 7081: [[569, 713]]}
CATALOG = {5: (2, [1, 5]), 7: (2, [1, 7]), 13: (2, [1, 5, 13]), 71: (3, None), 73: (3, None),
           97: (3, None), 7081: (9, None)}
nd = ne = 0
for d in list(range(1, 200, 2)) + [7081]:
    if gcd(d, 6) != 1:
        continue
    cyc, lab, k, per = sigma_table(d)
    shared = sorted(sorted(v) for v in per.values() if len(v) > 1)
    ok(shared == sorted(sorted(v) for v in SHARED.get(d, [])), f"B0 shared d={d}: {shared}")
    ok(all(min(c) <= d for c in cyc.values()), f"B0 minima d={d}")
    if d < 200:
        nd += 1
        ne += bool(shared)
    if d in CATALOG:
        kk, cl = CATALOG[d]
        ok(k == kk and (cl is None or sorted(cyc) == cl), f"B0 catalog d={d}: {k} {sorted(cyc)}")
    if d == 7081:
        ok(len(cyc) == 10, "B0 7081 cycles")
    # B3a: unique-cycle classes are basins
    if d < 200:
        st = sigma_step(d)
        target = {cls: v[0] for cls, v in per.items() if len(v) == 1}
        for n in list(range(1, 3001)) + [random.getrandbits(120) for _ in range(10)]:
            cls = lab[n % d]
            if cls in target:
                c = cycle_of(st, n)
                ok(min(c) == target[cls], f"B3a d={d} n={n}")
ok((nd, ne) == (67, 23), f"B0 counts {nd},{ne}")
print("B0, B3a done:", nd, "values,", ne, "with shared classes")

# B2 identities ------------------------------------------------------------------
for j in range(1, 13):
    m = 3 ** j
    ok(A.ord_mod(2, m) == 2 * 3 ** (j - 1), f"B2 primitive root 3^{j}")
for d in (5, 7, 13, 29, 31, 55, 7081):
    for Q in (d, 5 * d, 7 * d, 11 * d):
        if Q % 3 == 0:
            continue
        i3 = pow(3, -1, Q)
        for r in range(0, Q, max(1, Q // 200)):
            lu = (4 * ((4 * r - d) * i3) - d) % Q
            ul = ((4 * (4 * r - d) - d) * i3) % Q
            ok((lu - ul - (-2 * d) * i3) % Q == 0, f"B2 translation d={d} Q={Q}")
    for x in range(d % 3, 3000, 3):
        if x % 2 == 1 and (4 * x - d) % 3 == 0:
            ok((4 * x - d) // 3 - d == 4 * (x - d) // 3 and (x - d) % 3 == 0, f"B2 U2 d={d} x={x}")

# B2 constructive runs -----------------------------------------------------------
runs = 0
for d in (5, 13, 29, 31, 55, 67):
    lab, _ = orbit_classes(d, [2, 3])
    st = sigma_step(d)
    cyc = sorted(all_cycles(st, d))
    for _ in range(12):
        y = random.choice(cyc + [random.randrange(1, 10 ** 6) for _ in range(3)])
        M = random.choice([1, 2, 4, 8]) * random.choice([1, 3, 9]) * random.choice([1, 5, 7, 11])
        while True:
            x = random.randrange(1, 10 ** 7)
            if lab[x % d] == lab[y % d]:
                break
        w, cp = A.construct(d, y, M, x)
        ok((w - x) % M == 0 and w > x, f"B2 residue d={d}")
        yo = y
        while yo % 2 == 0:
            yo //= 2          # forward iterate of y, so reaching yo means merging with y
        ok(A.reaches(st, w, cp, 10 ** 5) and A.reaches(st, cp, yo, 10 ** 6), f"B2 merge d={d} y={y} M={M} x={x}")
        runs += 1
print("B2 constructive accessibility verified on", runs, "random targets")

# B4 identity --------------------------------------------------------------------
for d in range(1, 200, 2):
    st = sigma_step(d)
    for m in list(range(0, 3000)) + [random.getrandbits(100) for _ in range(10)]:
        ok(st(st(st(4 * m + d))) == 3 * m + d, f"B4 d={d} m={m}")
print("B4 identity done")

# E: split_13 evidence ----------------------------------------------------------
d, M = 13, 8 * 9 * 13
st = sigma_step(d)
memo = {}


def basin(n):
    path = []
    while n not in memo:
        path.append(n)
        if n <= d:
            c = cycle_of(st, n)
            memo[n] = min(c)
            break
        n = st(n)
    v = memo[n]
    for p in path:
        memo[p] = v
    return v


seen = {}
for n in range(1, 400 * M):
    if n % d:
        seen.setdefault(n % M, set()).add(basin(n))
units = [r for r in range(M) if r % 13]
ok(all(seen.get(r) == {1, 5} for r in units), "E split_13 both basins in every unit class mod 936")
print("E: split_13, every one of", len(units), "classes mod 936 coprime-to-13 meets both basins")

if FAIL:
    print(len(FAIL), "FAILURES")
    sys.exit(1)
print("ALL PASS")
