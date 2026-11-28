#!/usr/bin/env python3
"""Referee 1, round 4, lens "integrality": independent check script.

Written from scratch (does not import any prover module).  Exact integer /
Fraction arithmetic throughout.  Every check prints PASS or FAIL; the script
exits 1 if any check fails.  Several checks are negative controls that must
detect a planted error (so the script is able to fail).

usage: python3 referee1_check.py [N]      (N = brute-force bound, default 2*10^6)
"""
import sys
from fractions import Fraction
from math import log
from collections import Counter

N_BF = int(sys.argv[1]) if len(sys.argv) > 1 else 2 * 10 ** 6
FAILS = []


def claim(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + ((" -- " + info) if info else ""), flush=True)
    if not ok:
        FAILS.append(name)


# ---------------------------------------------------------------- systems
def sfam(S):
    S = frozenset(S)

    def T(n):
        if n % 2 == 0:
            return n // 2
        return 3 * n + 1 if n % 8 in S else n + 1
    return T


def G3(n):
    if n % 9 == 8:
        assert (4 * n + 1) % 3 == 0
        return (4 * n + 1) // 3
    return -((-n) // 3)          # ceil(n/3)


def K7(z):
    if z % 2 == 0:
        return z // 2
    if z % 4 == 3:
        return (3 * z + 1) // 2
    return (z - 1) // 4


CORES = {
    "sf3_7": ({7}, [(1, 2)]),
    "sf3_17": ({1, 7}, [(1, 4, 2)]),
    "sf3_57": ({5, 7}, [(1, 2)]),
    "sf3_157": ({1, 5, 7}, [(1, 4, 2)]),
    "sf3_357": ({3, 5, 7}, [(1, 2)]),
    "sf3_13": ({1, 3}, [(1, 4, 2), (3, 10, 5, 6)]),
    "sf3_135": ({1, 3, 5}, [(1, 4, 2)]),
}


def is_cycle(T, cyc):
    return all(T(cyc[i]) == cyc[(i + 1) % len(cyc)] for i in range(len(cyc)))


def drop_verify(T, N, known, cap=10 ** 6, big=10 ** 60):
    """Every n <= N not in known must reach a value < n.  Returns (ok, bad n)."""
    for n in range(1, N + 1):
        if n in known:
            continue
        x, s = T(n), 1
        while x >= n:
            x = T(x)
            s += 1
            if s > cap or x > big:
                return False, n
    return True, None


def cycles_by_min(T, N, cap=10 ** 5):
    """Independent cycle enumeration: for each n <= N iterate until a repeat;
    record every cycle found whose minimum is <= N.  Orbits leaving 10^40 or
    exceeding cap steps are reported as unresolved."""
    found, unresolved = set(), []
    settled = {}
    for n in range(1, N + 1):
        if n in settled:
            continue
        seen, path, x = {}, [], n
        while x not in seen and x not in settled:
            seen[x] = len(path)
            path.append(x)
            x = T(x)
            if len(path) > cap or x > 10 ** 40:
                unresolved.append(n)
                break
        else:
            if x in seen:
                cyc = path[seen[x]:]
                m = min(cyc)
                i = cyc.index(m)
                found.add(tuple(cyc[i:] + cyc[:i]))
        for y in path:
            if y <= N:
                settled[y] = 1
    return found, unresolved


def canon(c):
    i = c.index(min(c))
    return tuple(c[i:] + c[:i])


# ---------------------------------------------------------------- 1. cycles
print("== 1. cycle lists, brute force to N =", N_BF)
for name, (S, cyc) in CORES.items():
    T = sfam(S)
    claim(f"[cyc-list] {name}: listed cycles are cycles", all(is_cycle(T, c) for c in cyc))
    known = {x for c in cyc for x in c}
    ok, bad = drop_verify(T, N_BF, known)
    claim(f"[drop] {name}: every n <= {N_BF} off listed cycles drops below itself", ok, str(bad))
for nm, T, cyc in [("G3", G3, [(1,)])]:
    claim(f"[cyc-list] {nm}: 1 is a fixed point", is_cycle(T, cyc[0]))
    ok, bad = drop_verify(T, N_BF, {1})
    claim(f"[drop] {nm}: every n <= {N_BF} except 1 drops below itself", ok, str(bad))

# independent enumeration of cycles (smaller bound)
NE = min(N_BF, 3 * 10 ** 5)
for name, (S, cyc) in CORES.items():
    found, unres = cycles_by_min(sfam(S), NE)
    claim(f"[enum] {name}: cycles with min <= {NE} are exactly the listed ones",
          found == {canon(list(c)) for c in cyc} and not unres, f"{sorted(found)} unresolved={unres[:3]}")
found, unres = cycles_by_min(G3, NE)
claim(f"[enum] G3: only cycle with min <= {NE} is (1)", found == {(1,)} and not unres, str(found))
found, unres = cycles_by_min(K7, NE)
claim(f"[enum] K7: the only cycle reached from z in 1..{NE} is the fixed point 0", found == {(0,)} and not unres, str(found))

# negative controls: must fail
ok, bad = drop_verify(sfam({1, 3}), 10 ** 4, {1, 4, 2})
claim("[neg] drop verifier REJECTS sf3_13 without (3 10 5 6)", (not ok) and bad == 3, str(bad))
ok, bad = drop_verify(sfam({1, 3, 7}), 100, {1, 4, 2, 3, 10, 5, 6}, cap=10 ** 5, big=10 ** 40)
claim("[neg] drop verifier REJECTS core W = sf3_137 (some n <= 100)", not ok, f"first bad n = {bad}")

# K7 <-> sf3_7 odd-to-odd correspondence
T7 = sfam({7})


def next_odd(n):
    x = T7(n)
    while x % 2 == 0:
        x = T7(x)
    return x


claim("[K7-z] K7(z) = (g(2z+1)-1)/2 for z <= 2*10^5",
      all(K7(z) == (next_odd(2 * z + 1) - 1) // 2 for z in range(0, 2 * 10 ** 5)))


# ---------------------------------------------------------------- 2. Theorem C
print("== 2. Theorem C: independent (Y_fail, X_fail), full scan")


def least_X(p, a, Y):
    # exact least X with p^X > a^Y, via float guess then integer correction
    X = int(Y * log(a) / log(p)) + 1
    A = a ** Y
    while p ** X <= A:
        X += 1
    while X > 0 and p ** (X - 1) > A:
        X -= 1
    return X


def scan(Z0, p, a, c_num, c_den, Ymax):
    """c = c_num/c_den. Return first Y>=0 with Z0*(p^X-a^Y) < c*X*a^Y (not excluded)."""
    PA = 1
    X = 0
    PX = 1
    for Y in range(0, Ymax + 1):
        if Y:
            PA *= a
        while PX <= PA:
            PX *= p
            X += 1
        if Z0 * (PX - PA) * c_den < c_num * X * PA:
            return Y, X
    return None


# spot-check the incremental X against least_X
for Z0, p, a, c, exp in [(10 ** 9, 2, 3, 2, (15601, 24727)), (10 ** 11, 2, 3, 2, (190537, 301994)),
                        (10 ** 9, 3, 4, 4, (25254, 31867)), (10 ** 11, 3, 4, 4, (176251, 222404))]:
    r = scan(Z0, p, a, c, 1, 400000)
    claim(f"[C-bd] Z0={Z0:.0e} p={p} a={a} c={c}: first non-excluded (Y,X) = {r}", r == exp, f"prover {exp}")
    if r:
        claim(f"[C-bd] least_X({p},{a},{r[0]}) == {r[1]}", least_X(p, a, r[0]) == r[1])
    # cross-check: the failure Y must be a near-convergent (|X log p - Y log a| tiny)
    if r:
        gap = r[1] * log(p) - r[0] * log(a)
        claim(f"[C-cf] at Y_fail the gap X log p - Y log a = {gap:.3e} <= c X / Z0 = {c * r[1] / Z0:.3e}",
              0 < gap <= 1.01 * c * r[1] / Z0)
# hypothesis X < Z0 ln2/(beta gamma) holds at X_fail
claim("[C-hyp] X_fail=301994 < 10^11 ln 2 and 222404 <= 10^11/2", 301994 < 10 ** 11 * log(2) and 222404 <= 10 ** 11 / 2)

# falsification: Theorem C must hold for EVERY real cycle of maps in its class.
# 3x+k (k odd, 3 not | k): even n -> n/2, odd n -> 3n+k.  u in {1,3}, v=k <= beta*3, beta=k/3,
# P+ = #odd steps <= X (gamma=1), c = 2k/3.  Z0 = min(cycle)-1.
print("== 3. falsification tests of Theorem C on real cycles (3x+k, 5x+1)")
viol, tested = [], 0
for k in range(1, 400, 2):
    if k % 3 == 0:
        continue
    T = lambda n, k=k: n // 2 if n % 2 == 0 else 3 * n + k
    found, _ = cycles_by_min(T, 3000, cap=10 ** 4)
    for cyc in found:
        X = sum(1 for x in cyc if x % 2 == 0)
        Y = len(cyc) - X
        Z0 = min(cyc) - 1
        if Z0 < 1:
            continue
        tested += 1
        lhs = 3 * Z0 * (2 ** X - 3 ** Y)            # times 3 to clear c = 2k/3
        rhs = 2 * k * X * 3 ** Y
        hyp = X < Z0 * log(2) / (k / 3)
        if hyp and not (2 ** X > 3 ** Y and lhs < rhs and 2 ** (X - 1) < 3 ** Y):
            viol.append((k, cyc[:4], X, Y))
claim(f"[C-false] Theorem C holds on all {tested} cycles of 3x+k (k<400) with min <= 3000", not viol and tested > 100, str(viol[:3]))
T51 = lambda n: n // 2 if n % 2 == 0 else 5 * n + 1
found, _ = cycles_by_min(T51, 200, cap=10 ** 4)
ok = True
for cyc in found:
    X = sum(1 for x in cyc if x % 2 == 0)
    Y = len(cyc) - X
    Z0 = min(cyc) - 1
    # beta = 1/5, gamma = 1, c = 2/5:  Z0 (2^X - 5^Y) < (2/5) X 5^Y
    if not (2 ** X > 5 ** Y and 5 * Z0 * (2 ** X - 5 ** Y) < 2 * X * 5 ** Y):
        ok = False
claim(f"[C-false] Theorem C holds on the 5x+1 cycles {sorted(min(c) for c in found)}", ok and len(found) >= 2)
# negative control: with a planted error (c halved, c = k/3) at least one real cycle violates (★)
bad = 0
for k in range(1, 400, 2):
    if k % 3 == 0:
        continue
    T = lambda n, k=k: n // 2 if n % 2 == 0 else 3 * n + k
    for cyc in cycles_by_min(T, 3000, cap=10 ** 4)[0]:
        X = sum(1 for x in cyc if x % 2 == 0); Y = len(cyc) - X; Z0 = min(cyc) - 1
        if Z0 >= 1 and not (3 * Z0 * (2 ** X - 3 ** Y) < k * X * 3 ** Y // 4):
            bad += 1
claim("[neg] a planted weaker constant (c/8) is violated by real 3x+k cycles", bad > 0, f"{bad} violations")

# ---------------------------------------------------------------- 4. G3 type
print("== 4. G3 residue graph, type (c)")


def graph(T_aff, p, K, m):
    """T_aff(r) -> (u, v, e) for r mod p^m; edges of G_K."""
    E = {}
    for r in range(p ** K):
        u, v, e = T_aff(r % p ** m)
        num = u * r + v
        assert num % p ** e == 0
        s0 = (num // p ** e) % p ** (K - e)
        E[r] = [(s0 + t * p ** (K - e)) % p ** K for t in range(p ** e)], Fraction(u, p ** e)
    return E


def G3aff(r):
    if r == 8:
        return 4, 1, 1
    return 1, (-r) % 3, 1


def reach(E, a):
    st, seen = [a], {a}
    while st:
        x = st.pop()
        for y in E[x][0]:
            if y not in seen:
                seen.add(y)
                st.append(y)
    return seen


for K in (2, 3):
    E = graph(G3aff, 3, K, 2)
    xs = (-1) % 3 ** K
    one = 1
    same = (one in reach(E, xs)) and (xs in reach(E, one))
    loop_exp = xs in E[xs][0] and E[xs][1] == Fraction(4, 3)
    loop_con = one in E[one][0] and E[one][1] == Fraction(1, 3)
    claim(f"[G3-c] level {K}: -1 (self-loop 4/3) and 1 (self-loop 1/3) in one SCC => type (c), not (b)",
          same and loop_exp and loop_con)
# G3 integer check of branch formulas
claim("[G3-def] G3 = (u n + v)/3 with u in {1,4}, 0 <= v <= 2u, all n < 10^5",
      all(G3(n) * 3 in (n, n + 1, n + 2, 4 * n + 1) and (G3(n) * 3 == 4 * n + 1) == (n % 9 == 8) for n in range(1, 10 ** 5)))

# ---------------------------------------------------------------- 5. Theorem M (G3, exact counts)
print("== 5. Theorem M: independence of (d1, return time, d2) for G3, exact residue counts")
# G3 consumes exactly one ternary digit per step: T^t(n) mod 9 depends on n mod 3^(t+2).
NP = 13
MOD = 3 ** NP
cnt3 = Counter()   # (d1, tau, d2)
cnt2 = Counter()   # (d1, tau) with return decided
for n in range(8, MOD, 9):
    # d1: largest d with n = -1 mod 3^(2+d)
    d1 = 0
    while (n + 1) % 3 ** (3 + d1) == 0:
        d1 += 1
    if 3 + d1 > NP:
        continue
    x = n
    for _ in range(d1):
        x = G3(x)
    # x is the post-run point: in [8]_9 but not -1 mod 27.  Move one step, then wait for next visit to 8 mod 9.
    tau = d1
    while True:
        x = G3(x)
        tau += 1
        if tau + 2 > NP:
            x = None
            break
        if x % 9 == 8:
            break
    if x is None:
        continue
    cnt2[(d1, tau)] += 1
    d2 = 0
    while (x + 1) % 3 ** (3 + d2) == 0:
        d2 += 1
    if tau + 3 + d2 <= NP:
        cnt3[(d1, tau, d2)] += 1
ok, ntest = True, 0
for (d1, tau, d2), c in cnt3.items():
    if tau + 3 + d2 <= NP:
        ntest += 1
        # predicted: P(d2 | history) = (2/3) 3^(-d2)
        if 3 * c * 3 ** d2 != 2 * cnt2[(d1, tau)]:
            ok = False
claim(f"[M-iid] G3: P(d2 = j | d1, return time) = (2/3)3^-j exactly on {ntest} decided events (mod 3^{NP})", ok and ntest > 20)
# d1 law: count of n = 8 mod 9 with d1 = i, mod 3^NP: should be 2*3^(NP-3-i)
ok = all(sum(1 for n in range(8, 3 ** 9, 9) if (n + 1) % 3 ** (3 + i) != 0 and (n + 1) % 3 ** (2 + i) == 0) == 2 * 3 ** (9 - 3 - i) for i in range(0, 5))
claim("[M-d1] G3: d1 is geometric, #{n mod 3^9: d1 = i} = 2*3^(6-i)", ok)
# run map on D_d: R(x) = -1 + (4/3)^d (x+1), exact
ok = True
for d in range(0, 9):
    for t in (1, 2, 4, 5, 7, 8, 10, 11):
        x = -1 + 3 ** (2 + d) * t     # in D_d (t not divisible by 3)
        y = x
        for _ in range(d):
            y = G3(y)
        if Fraction(y) != -1 + Fraction(4, 3) ** d * (x + 1) or (y + 1) % 27 == 0 or (y + 1) % 9 != 0:
            ok = False
claim("[M-run] G3: on D_d the run map is x -> x* + (4/3)^d (x - x*) and lands in D_0, d <= 8", ok)
# off-by-one wording check: n = 8 has first residue 8 but G3(8) = 11 not = 8 mod 9, and 8 is in D_0
claim("[M-word] n = 8: residue at time 0 is that of C but n lies in D_0 (wording 'first d*l residues' is off by one)",
      8 % 9 == 8 and G3(8) % 9 != 8 and (8 + 1) % 27 != 0)

# ---------------------------------------------------------------- 6. Theorem R (F5 family n_d)
print("== 6. Theorem R: explicit n_d for F5")


def F5(n):
    if n % 2 == 0:
        return n // 2
    if n % 4 == 1:
        return n + 1
    return (5 * n - 1) // 2


# x* = 1/3 = -a/b with a = -1, b = 3; K = 2, E = 1, U = 5, F = ord_3(2) = 2, c' = 5 (4*5 = -1 mod 3)
ok = True
for d in range(0, 12):
    nd = (2 ** (2 + 2 * d) * 5 + 1) // 3
    assert 3 * nd - 1 == 2 ** (2 + 2 * d) * 5
    x = nd
    laps = 0
    # lap count: largest d' with nd = 1/3 mod 2^(2+d')
    while (3 * nd - 1) % 2 ** (3 + laps) == 0:
        laps += 1
    for _ in range(laps):
        x = F5(x)
    if laps != 2 * d or 3 * x - 1 != 5 ** (2 * d) * 4 * 5:
        ok = False
claim("[R-nd] F5: d(n_d) = dF and b R(n_d) + a = U^(dF) p^K c' exactly, d < 12", ok)

# ---------------------------------------------------------------- 7. K7 claims
print("== 7. K1-K3")


def v2(x):
    e = 0
    while x % 2 == 0:
        x //= 2
        e += 1
    return e


ok1 = ok2 = ok3 = True
for z in range(1, 2 * 10 ** 5, 2):
    j = v2(z + 1)
    u = (z + 1) >> j
    x = z
    for _ in range(j):
        x = K7(x)
    if x != (3 ** (j - 1) * u - 1) // 2:
        ok1 = False
    w = 3 ** (j - 1) * u - 1
    S = 0 if w == 0 else w >> v2(w)
    y = K7(z) if j == 0 else x
    while y % 2 == 0 and y != 0:
        y = K7(y)
    if y != S:
        ok1 = False
    if not (2 * S + 1 <= 3 ** (j - 1) * u):
        ok2 = False
    if S > ((z + 1) ** log(3, 2) - 3) / 6 * (1 + 1e-12) + 1e-9:
        ok2 = False
    if j <= 4 and not S < z:
        ok3 = False
claim("[K1] excursion formula and S(z) for odd z < 2*10^5", ok1)
claim("[K2] 2S+1 <= 3^(j-1)u and S <= ((z+1)^log2(3) - 3)/6", ok2)
claim("[K3a] S(z) < z whenever v2(z+1) <= 4", ok3)
claim("[K2-eq] equality at z = 2^j - 1 iff j even (j <= 60)",
      all(((2 * ((3 ** (j - 1) - 1) >> v2(3 ** (j - 1) - 1)) + 1) == 3 ** (j - 1)) == (j % 2 == 0) for j in range(2, 61)))
# density of B1
dens = Fraction(0)
for j in range(5, 401):
    for v in range(1, 2 * j):
        if 2 ** (j + v) < 3 ** (j - 1):
            dens += Fraction(1, 2 ** (j + v))
cnt = 0
tot = 0
LIM = 2 ** 22
for z in range(1, LIM, 2):
    tot += 1
    j = v2(z + 1)
    if j < 5:
        continue
    u = (z + 1) >> j
    w = 3 ** (j - 1) * u - 1
    S = w >> v2(w)
    if S >= z:
        cnt += 1
claim(f"[K3-dens] delta1 partial sum = {float(dens):.10f}, count below 2^22 = {cnt / tot:.7f}; both round to 0.036275",
      abs(float(dens) - 0.036275) < 5e-7 and abs(cnt / tot - 0.036275) < 5e-6)
# explicit z with k rising excursions, each (j,v) = (6,1), by 2-adic lifting.
# (j,v) of the excursion at z is decided by z mod 2^8, and S is affine with slope
# 243/128 there, so the first i+1 excursions are decided by z mod 2^(7i+8).
def excursion(z):
    j = v2(z + 1)
    u = (z + 1) >> j
    w = 3 ** (j - 1) * u - 1
    if w == 0:                      # z = 1 -> 0
        return j, 0, 0
    v = v2(w)
    return j, v, w >> v


def pattern_ok(z, k):
    y = z
    for _ in range(k):
        j, v, y2 = excursion(y)
        if (j, v) != (6, 1) or y2 <= y:
            return False
        y = y2
    return True


cls = [r for r in range(1, 2 ** 8, 2) if pattern_ok(r, 1)]
ok = cls == [63]
for i in range(1, 8):
    mod = 2 ** (7 * (i - 1) + 8)
    cls = [r + t * mod for r in cls for t in range(2 ** 7) if pattern_ok(r + t * mod, i + 1)]
    ok = ok and len(cls) == 1          # Theorem M: exactly one class per word
claim("[K3-rise] for k = 1..8 exactly one class mod 2^(7k+1) gives k rising (6,1) excursions",
      ok and pattern_ok(cls[0], 8) and pattern_ok(cls[0] + 2 ** 57 * 12345, 8), f"z = {cls[0]}")

print()
if FAILS:
    print("FAILED:", FAILS)
    sys.exit(1)
print("ALL PASS")
