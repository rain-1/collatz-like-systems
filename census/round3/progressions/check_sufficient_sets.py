"""Check for sufficient_sets.md. Exact; exits 0 iff all checks pass."""

import itertools
import math
import os
import random
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plib
import systems
import construct

FAIL = []
rng = random.Random(3)


def ok(c, m):
    if not c:
        FAIL.append(m)
        print("FAIL:", m, flush=True)


# ---- Theorem D: the construction with N = p^k, x = least x = 1 mod p^k in the class of y
for sid in ["par_5_1", "split5_3", "par_7_1"]:
    S = systems.get(sid)["sys"]
    info = construct.prepare(S)
    L_U = plib.L_U(S)
    A = 2 * math.log(L_U)
    y = systems.get(sid)["cycles"][0]
    out = []
    for k in range(1, 9):
        N = S.p ** k
        x = next(1 + N * j for j in range(info["dstar"] + 1)
                 if construct.g(S, info, 1 + N * j) == construct.g(S, info, y))
        n, data = construct.construct(S, info, y, x, N)
        construct.verify(S, y, x, N, n, data)
        ok(n % N == 1, f"n = 1 mod p^k {sid}")
        ll = math.log(max(math.log(n), 1.0001))
        out.append((k, round(ll / k, 2), math.floor(ll / A) <= k))
    print(sid, "k, loglog(n_k)/k, k(n_k)<=k :", out, flush=True)
    ok(all(t[2] for t in out), f"n_k in S_T for k <= 8 ({sid}) [illustration]")

# S_T(5x+1) starts thinning only at exp(exp(A j)): print the first thresholds (illustration)
A = 2 * math.log(5)
print("S_T(5x+1): members above exp(exp(A j)) are = 1 mod 2^j; log10 thresholds j=1,2:",
      [round(math.exp(A * j) / math.log(10), 1) for j in (1, 2)])

# ---- forward-invariant good-modulus sets are unions of classes (kappa = 1 systems)
for sid in ["par_5_1", "par_3_5", "par_5_7", "m3_e", "par_3_13"]:
    S = systems.get(sid)["sys"]
    for q in [5, 7, 11, 13]:
        if any(q % b == 0 for b in S.bad):
            continue
        phis = [(u, v) for (u, v) in S.table.values()]
        cls = plib.groupoid_classes(S, q)
        for bits in range(1, 2 ** q):
            Aset = {z for z in range(q) if bits >> z & 1}
            inv = all(((u * z + v) * pow(S.p, -1, q)) % q in Aset for z in Aset for (u, v) in phis)
            if inv:
                ok(all(cls[(0, z)] != cls[(0, w)] or (w in Aset) for z in Aset for w in range(q)),
                   f"forward-invariant set not a union of classes {sid} q={q}")
print("forward-invariant good-modulus sets are unions of invariant classes (all subsets, q<=13)")

# 7x+1: squares mod 7 are forward invariant (a U-adic forward-invariant set)
S = systems.get("par_7_1")["sys"]
ok(all(S.T(n) % 7 in (1, 2, 4) for n in range(1, 50000) if n % 7 in (1, 2, 4)), "7x+1 squares invariant")

# ---- cylinder certificates: a descent word valid on P (p not dividing N) is valid everywhere
S = systems.get("par_3_1")["sys"]
for N in [3, 5, 7, 9, 15]:
    for m in range(1, 9):
        for res in range(2 ** m):
            # cylinder class res mod 2^m meets x mod N for every x
            ok(all(any((res + 2 ** m * j - x) % N == 0 for j in range(N)) for x in range(N)),
               "cylinder meets every class mod odd N")

# ---- Proposition P for the 1932 map
P = systems.get("perm_1932")["sys"]
for k in range(1, 8):
    seen = {}
    for n in range(3 ** k, 2 * 3 ** k):
        x, w = n, []
        for _ in range(k):
            w.append(x % 3)
            x = P.T(x)
        seen.setdefault(tuple(w), set()).add(n % 3 ** k)
    ok(len(seen) == 3 ** k and all(len(v) == 1 for v in seen.values()),
       f"1932 itinerary blocks <-> classes mod 3^k (k={k})")
for L in range(1, 9):
    for W in itertools.product(range(3), repeat=L):
        # composite on the cylinder: n -> (a n + b)/3^L
        a, b = Fr(1), Fr(0)
        for r in W:
            u, v = P.table[r]
            a, b = a * Fr(u, 3), b * Fr(u, 3) + Fr(v, 3)
        cstar = b / (1 - a)
        if cstar.denominator == 1 and cstar > 0:
            n = int(cstar)
            x, ww = n, []
            for _ in range(L):
                ww.append(x % 3)
                x = P.T(x)
            if tuple(ww) == W:
                ok(x == n, "periodic itinerary at integer fixed point gives a cycle")
for c0 in [1, 2, 4, 44]:
    cyc = plib.cycle_of(P, c0)
    for k in range(1, 8):
        ok(len({x % 3 ** k for x in cyc}) <= len(cyc), "cycle meets at most its length classes")
print("Proposition P data checked")

# ---- Proposition P0 (correction after REFEREE1): the sufficient progressions of the 1932 map
# are exactly Z>=1 and 1 mod 2.
# Exact finite content: T(3q+1) = 4q+1, T(3q+2) = 4q+3, T(3q) = 2q as affine identities in q
# (two points determine an affine map; T is affine on each class), parity of 4q+1, 4q+3, and
# 2q < 3q for q >= 1; the cycles (1), (2 3); the divisibility argument N | 1 or N | 2.
for r, (A, B) in {0: (2, 0), 1: (4, 1), 2: (4, 3)}.items():
    ok(all(P.T(3 * q + r) == A * q + B for q in (1, 2)), f"1932 branch {r} affine identity")
    ok(P.table[r] == {0: (2, 0), 1: (4, -1), 2: (4, 1)}[r], "1932 table")
for q in list(range(0, 3000)) + [rng.randrange(1, 10 ** 40) for _ in range(3000)]:
    ok(P.T(3 * q + 1) % 2 == 1 and P.T(3 * q + 2) % 2 == 1, "1932 nonzero branches odd")
    if q >= 1:
        ok(P.T(3 * q) == 2 * q < 3 * q, "1932 zero branch decreases")
ok(P.T(1) == 1 and P.T(2) == 3 and P.T(3) == 2, "1932 cycles (1), (2 3)")
suff = [(x, N) for N in range(1, 300) for x in range(N)
        if 1 % N == x and (2 % N == x or 3 % N == x)]
ok(suff == [(0, 1), (1, 2)], f"progressions meeting (1) and (2 3): {suff}")
for n in range(1, 10 ** 5):
    x, k = n, 0
    while x % 2 == 0:
        ok(x % 3 == 0 or P.T(x) % 2 == 1, "even non-multiple of 3 maps to odd")
        x = P.T(x)
        k += 1
    ok(k <= 40, "odd value reached")
print("Proposition P0: sufficient progressions of the 1932 map are exactly Z and 1 mod 2")

# ---- Theorem A item 3 (corrected example): every progression x + N Z with
# gcd(N, p^(kappa-1) d*) = 1 meets every g-class (CRT); tested on every system where Theorem A
# applies, for several N and x.
from certify import certify
nsys = 0
for e in systems.SYSTEMS:
    c = certify(e)
    if not c.get("theorem_A"):
        continue
    S = e["sys"]
    info = construct.prepare(S)
    allg = {construct.g(S, info, n) for n in range(1, S.S * info["dstar"] * S.p + 1)}
    M = S.S * info["dstar"]
    for N in [7, 10, 11, 12, 100, 1001, 2 ** 5, 3 ** 4]:
        if math.gcd(N, M) != 1:
            continue
        for x in [1, 2, rng.randrange(1, 10 ** 6)]:
            got = {construct.g(S, info, x + N * j) for j in range(M + 1)}
            ok(got == allg, f"item 3: {x} mod {N} meets every g-class ({e['id']})")
    nsys += 1
print(f"Theorem A item 3 example: checked on {nsys} systems")

if FAIL:
    print(len(FAIL), "FAILURES")
    sys.exit(1)
print("ALL CHECKS PASSED")
