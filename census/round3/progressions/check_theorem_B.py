"""Check for Theorem B (theorem_B_automatic_labels.md). Exact arithmetic; exits 0 iff all pass."""

import os
import random
import sys
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plib
import systems
import construct
from certify import certify

FAIL = []
rng = random.Random(7)


def ok(c, m):
    if not c:
        FAIL.append(m)
        print("FAIL:", m, flush=True)


def label_fn(S, cycles, cap=4000, big=10 ** 80):
    """Basin label: index of the known cycle reached within cap steps, else None (unknown)."""
    where = {}
    for i, c in enumerate(cycles):
        x = c
        while True:
            where[x] = i
            x = S.T(x)
            if x == c:
                break
    memo = {}

    def f(n):
        if n in memo:
            return memo[n]
        x, path = n, []
        for _ in range(cap):
            if x in where:
                res = where[x]
                break
            if x in memo:
                res = memo[x]
                break
            path.append(x)
            x = S.T(x)
            if x > big:
                res = None
                break
        else:
            res = None
        for y in path:
            memo[y] = res
        memo[n] = res
        return res
    return f


count_B = 0
for e in systems.SYSTEMS:
    c = certify(e)
    if not c.get("theorem_B"):
        continue
    count_B += 1
    S = e["sys"]
    sid = e["id"]
    ok(c["state_free"] and c["theorem_A"], f"hyp {sid}")
    ok(gcd(c["invariant_modulus"], S.p * max(1, *(u for u, v in S.table.values()))) == 1
       or all(c["invariant_modulus"] % q for q in S.bad), f"d* coprime to bad primes {sid}")
    f = label_fn(S, e["cycles"])
    # dilation identity f(pn) = f(n), and T(pn) = n
    for n in range(1, 3000):
        ok(S.T(S.p * n) == n, f"T(pn)=n {sid}")
        a, b = f(S.p * n), f(n)
        if a is not None and b is not None:
            ok(a == b, f"f(pn)=f(n) {sid} {n}")
    # lap identity for the expanding cycle: T^L(c + mu p^L j) = c + mu a j, exactly
    cc = c["expanding_cycle"]
    a, L, x = 1, 0, cc
    while True:
        a *= S.table[x % S.P][0]
        x = S.T(x)
        L += 1
        if x == cc:
            break
    ok(a > 1 and a % S.p != 0, f"lap numerator {sid}")
    ok(all(q in S.U for q in plib.primes_of(a)), f"lap primes in U {sid}")
    mu = S.S
    for j in list(range(0, 400)) + [rng.randrange(1, 10 ** 30) for _ in range(300)]:
        z = cc + mu * S.p ** L * j
        for _ in range(L):
            z = S.T(z)
        ok(z == cc + mu * a * j, f"lap identity {sid} j={j}")
    # Lemma B0 digit arithmetic, both cases, with the system's invariant modulus as q'
    q = c["invariant_modulus"]
    for (P, K, k0) in [(S.p, 1, 10 if S.p != 10 else 3), (a, S.p ** L, S.p)]:
        for _ in range(30):
            E = rng.randrange(1, 5)
            d = rng.randrange(0, P ** E)
            A = 1
            while k0 ** A < P ** E * q:
                A += 1
            D = k0 ** A
            G = gcd(D, q)
            z0 = rng.randrange(0, q)
            r = plib.crt_pair((-D * d) % P ** E, P ** E, (z0 - D * d) % G, G)
            ok(r is not None and r[0] < D, f"CRT choice {sid}")
            r = r[0]
            # progression D P^E n + D d + r meets z0 mod q
            ok(any((D * P ** E * n + D * d + r - z0) % q == 0 for n in range(q)), f"meets C' {sid}")
            for jj in range(E + 1):
                dj = d % P ** jj
                ok((D * dj + r) % P ** jj == 0, f"s_j integral {sid}")
                sj = (D * dj + r) // P ** jj
                ok(0 <= sj < D and 0 <= K ** jj * sj < K ** jj * D, f"s_j range {sid}")
print(f"Theorem B data checked for {count_B} systems", flush=True)
ok(count_B >= 25, "number of Theorem B systems")

# qrB7_c53: no expanding cycle (all numerators 1), so Theorem B does not apply
qb = systems.get("qrB7_c53")["sys"]
ok(all(u == 1 for (u, v) in qb.table.values()), "qrB7_c53 has only u = 1")
NEVID = [0]
# shared-class basins meet small progressions (EVIDENCE illustration, settled systems)
for sid in ["m3_a", "desc_s32_d65", "split_13"]:
    e = systems.get(sid)
    S = e["sys"]
    f = label_fn(S, e["cycles"])
    cert = certify(e)
    for cls, reps in cert["shared_classes"].items():
        idx = [e["cycles"].index(r) for r in reps]
        info = construct.prepare(S)
        for N in (8, 9, 25, 49):
            for res in range(N):
                xs = [n for n in range(res if res else N, 400000, N)
                      if construct.g(S, info, n) == int(cls)]
                if not xs:
                    continue
                labs = {f(n) for n in xs[:3000]}
                NEVID[0] += 1
                ok(all(i in labs for i in idx), f"evidence {sid} class {cls} N={N} r={res}")
print(f"evidence: shared-class basins present in all {NEVID[0]} compatible classes mod 8, 9, 25, 49 tested", flush=True)
ok(NEVID[0] > 100, "evidence loop ran")

if FAIL:
    print(len(FAIL), "FAILURES")
    sys.exit(1)
print("ALL CHECKS PASSED")
