"""Referee's independent check for the collatz3 claims (CLS-031,004..011).
Uses the census step functions (census/systems.py), not _common.py.
Exact integers. Exit 0 iff every computational part passes. Runs in a few seconds.

What it checks (finite statements only; none of this proves GLOBAL):
 1. The step functions in census/systems.py agree with F_d / G (6n+2) on 1..1e5.
 2. Lemma S / G / sublattice embedding: for n <= 3000, the first 300 orbit
    terms of n under F_d equal g times the orbit of m = n/g under F_{d/g}.
 3. Orbit embedding for 6n+2: the G-orbit with the inserted terms 2(3n+1) removed
    equals the Collatz orbit (first 500 terms, n <= 5000).
 4. 1-cycles by a second, independent route: for every k <= 400 and every
    l with |2^(k+l)-3^k| <= |d|(2^l-1), test x = d(3^k-2^k)/(2^K-3^k).
    (Only this finite set needs testing, by the divisibility step (ii).)
 5. Cross-check by brute force: all T_d cycles whose minimum is < 20000
    (each n tested for return to itself before exceeding 10^12 or 10^4 steps),
    their odd-run counts, and that the 1-run cycles among them are exactly the listed ones
    with min < 20000.
 6. Re-derivation of the bound k <= kE(d) under Ellison's inequality, in exact
    rational arithmetic with ln2 > 0.6931, log2(3) < 1.585, ln|d| upper bounds.
"""
import os, sys, math
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))
from systems import get

ok = True
def rep(name, c):
    global ok
    ok &= bool(c)
    print(("PASS " if c else "FAIL ") + name)

IDS = {1: "par_3_1_s27", -1: "par_3_m1_s27", 3: "par_3_3_s27", 5: "par_3_5_s27",
       7: "par_3_7_s27", 9: "par_3_9_s27", 13: "par_3_13_s27", 17: "par_3_17_s27"}
STEP = {d: get(k)["step"] for d, k in IDS.items()}
G = get("par_6_2_s27")["step"]

# 1
rep("systems.py steps match F_d", all(STEP[d](n) == (n // 2 if n % 2 == 0 else 3 * n + d)
                                       for d in STEP for n in range(1, 100001)))
rep("systems.py step matches 6n+2", all(G(n) == (n // 2 if n % 2 == 0 else 6 * n + 2) for n in range(1, 100001)))

def orbit(f, n, L):
    o = [n]
    for _ in range(L):
        n = f(n); o.append(n)
    return o

# 2: scaling with census steps; g = gcd(n, d) (d=9: g = the 3-part reached later, test g|d directly)
good = True
for d in (3, 5, 7, 9, 13, 17):
    for g in [g for g in range(1, d + 1) if d % g == 0]:
        e = d // g
        if e not in STEP:
            continue
        for m in range(1, 3001):
            if [g * y for y in orbit(STEP[e], m, 300)] != orbit(STEP[d], g * m, 300):
                good = False
rep("F_d-orbit of g*m == g * F_{d/g}-orbit of m (g|d, m<=3000, 300 steps)", good)
# gcd invariance for gcd(d,6)=1
rep("gcd(n,d) invariant along orbits, d in {5,7,13,17}, n<=3000",
    all(len({math.gcd(y, d) for y in orbit(STEP[d], n, 300)}) == 1
        for d in (5, 7, 13, 17) for n in range(1, 3001)))
# every orbit enters 3Z (d=3) / 9Z (d=9) within a few odd steps
def enters(d, mod, n, L=2000):
    for _ in range(L):
        if n % mod == 0:
            return True
        n = STEP[d](n)
    return False
rep("3n+3: orbits of n<=20000 enter 3Z", all(enters(3, 3, n) for n in range(1, 20001)))
rep("3n+9: orbits of n<=20000 enter 9Z", all(enters(9, 9, n) for n in range(1, 20001)))

# 3
good = True
for n in range(1, 5001):
    o = orbit(G, n, 500)
    filt = [o[0]]
    i = 0
    while i + 1 < len(o):
        if o[i] % 2 == 1:
            if i + 2 >= len(o):
                break
            assert o[i + 1] == 2 * (3 * o[i] + 1)
            filt.append(o[i + 2]); i += 2
        else:
            filt.append(o[i + 1]); i += 1
    c = orbit(STEP[1], n, len(filt) - 1)
    good &= (c == filt)
rep("6n+2 orbit minus inserted 2(3n+1) terms == Collatz orbit (n<=5000)", good)

# 4
def T(d, n):
    return n // 2 if n % 2 == 0 else (3 * n + d) // 2
def one_cycles_indep(d, kmax):
    res = set()
    if d < 0:
        res.add(-d)  # l=0 fixed point
    for k in range(1, kmax + 1):
        A, B = 3 ** k, 2 ** k
        l = 1
        while True:
            K = k + l
            D = 2 ** K - A
            if (d < 0 and D > 0) or (d > 0 and D > d * (A - B)):
                break      # x < 1 for this and all larger l (D increasing in l)
            if abs(D) > abs(d) * (2 ** l - 1):
                l += 1
                continue
            num = d * (A - B)
            if D != 0 and num % D == 0 and num // D > 0:
                x = num // D
                # verify parity block 1^k 0^l by simulation
                y, okc = x, True
                for i in range(K):
                    if (y % 2) != (1 if i < k else 0):
                        okc = False
                    y = T(d, y)
                if okc and y == x:
                    res.add(x)
            l += 1
    return sorted(res)

EXPECT = {1: [1], -1: [1, 5], 3: [3], 5: [1, 5, 19], 7: [5, 7], 9: [9],
          13: [1, 13, 211], 17: [17]}
for d in EXPECT:
    got = one_cycles_indep(d, 400)
    rep(f"d={d}: 1-cycle minima for k<=400 == {EXPECT[d]} (got {got})", got == EXPECT[d])

# 5
def cycles_with_min_below(d, N, cap=10 ** 12, L=10000):
    out = {}
    for n in range(1, N):
        y = n
        for _ in range(L):
            y = T(d, y)
            if y == n or y < n or y > cap:
                break
        if y == n:  # n is the minimum of its cycle (we stopped at first value < n otherwise)
            cyc = [n]; y = T(d, n)
            while y != n:
                cyc.append(y); y = T(d, y)
            par = [v % 2 for v in cyc]
            runs = sum(1 for i in range(len(par)) if par[i] == 1 and par[i - 1] == 0)
            if all(par):
                runs = 1
            out[n] = runs
    return out
good = True
for d in EXPECT:
    cs = cycles_with_min_below(d, 20000)
    ones = sorted(m for m, r in cs.items() if r == 1)
    exp = [m for m in EXPECT[d] if m < 20000]
    print(f"   d={d}: cycles with min<20000 (min:runs) {cs}")
    good &= (ones == exp)
rep("brute-force 1-run cycles (min<20000) agree with the formula list", good)

# 6: under (E) |2^K-3^k| > 2^K e^{-K/10} (K>=28) and |D| < |d| 2^l:
#    k ln2 < ln|d| + K/10, with K < k log2 3 + log2(|d|+1).
#    So k (ln2 - log2(3)/10) < ln|d| + log2(|d|+1)/10. Rational upper/lower bounds.
LN2_LO = Fr(6931, 10000); L3_HI = Fr(1585, 1000)
def ln_hi(x):   # crude upper bound for ln x, x >= 1 integer: ln x <= log2(x)*0.6932
    return Fr(int(math.ceil(math.log2(x) * 10 ** 6)) + 1, 10 ** 6) * Fr(6932, 10000)
def log2_hi(x):
    return Fr(int(math.ceil(math.log2(x) * 10 ** 6)) + 1, 10 ** 6)
CLAIM_KE = {1: 0, -1: 0, 3: 2, 5: 3, 7: 4, 9: 4, 13: 5, 17: 6}
good = True
for d, kE in CLAIM_KE.items():
    ad = abs(d)
    rhs = (ln_hi(ad) if ad > 1 else Fr(0)) + log2_hi(ad + 1) / 10
    coef = LN2_LO - L3_HI / 10
    kmax = math.floor(rhs / coef)
    Kmax = kmax * L3_HI + log2_hi(ad + 1)
    good &= (kmax <= kE + 0) and Kmax < 28
    print(f"   d={d}: k < {float(rhs/coef):.3f} so k<={kmax} (claimed {kE}); K < {float(Kmax):.2f} < 28")
rep("Ellison route: k bounded by kE(d) and then K < 28 (contradiction), so K <= 27", good)

print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
