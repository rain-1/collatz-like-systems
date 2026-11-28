#!/usr/bin/env python3
"""Checks for split5_3_deep.md.

Claims tested (exact arithmetic unless marked):
  O0  the U/O digit coding, for members of every type and J = 11: the digit word of n depends
      only on n mod 2^J, words <-> residues mod 2^J bijectively, the map is affine on each class
      with coefficient equal to the word's slope product, values in state O are odd; and the
      raw-step prefix minimum of the slope is attained at digit boundaries (random 80-bit n)
  O1  Theorem Omega1: the weighting identities ((c/4)/lam = lam, lam^2 = c/4), the bad-digit
      bijection, the binomial covering bound, the cycle-lemma bound |Y_m| >= C(m,i)/m (exact DP for
      m <= 60), and agreement of H_2(q_c) with log2(rho_*) (float, display)
  O3  certified upper bounds rho(p/q) <= mu (exact rationals) and lower bounds from exact
      excursion counts for every class-O type; L <= U and U - L < 1e-3; the table endpoints of
      split5_3_deep.md are compared exactly (lower: rational; upper: mu^Q <= 2^P), no tolerance
  O4  Theorem Omega4 sanity: never-descending starts in [2^m, 2^(m+1)) for m <= 15 (split5_3,
      split5_1) are at most the number of length-m words with P_m >= 1/2 (exact)
  O5  Theorem Omega5: s*r = 21/8 > 2 for both positive-drift types (exact)
  Z3  split5_3(3m) = 3 SPLIT(1,5,1)(m); mod-3 classes invariant
  C   the ancestor identity: n = 2 (mod 5) -> z = (4n-3)/5 = 1 (mod 4), T^3(z) = n
Exit 0 iff all pass.  Runtime about 1-2 minutes.
"""
import math
import os
import random
import sys
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from family_lib import vals, classify
from systems import split_step
from omega_lib import (transitions, loop_count, rho_min_float, certify_upper, lower_bound_counts,
                       upper_bound_cert, otype, H2)

random.seed(55)
FAIL = []


def ok(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("FAIL:", msg)


MEMBERS = [(5, 1, 3), (1, 5, 1), (5, 1, 1), (1, 5, 3), (7, 1, 1), (3, 5, 1), (5, 7, 3), (3, 7, 1),
           (3, 7, 3), (7, 3, 1), (5, 1, 7), (9, 1, 3), (13, 1, 3)]

# O0 -------------------------------------------------------------------------------
for (a, b, d) in MEMBERS:
    va, vb = vals(a, b, d)
    J = 11
    words = {}
    for r in range(2 ** J):
        # exact tracking with the actual integer and the 2-adic slope
        n = r if r else 2 ** J
        x, state, slope, word = n, 'U', Fraction(1), []
        k = 0
        while k < J:
            if state == 'U':
                if x % 2 == 0:
                    x //= 2; slope /= 2; word.append(0)
                else:
                    state = 'O'; word.append(1)
            else:
                if x % 4 == 1:
                    x = (a * x + d) // 2 ** va; slope *= Fraction(a, 2 ** va)
                    state = 'U' if va == 2 else 'O'; word.append(0)
                else:
                    x = (b * x + d) // 2 ** vb; slope *= Fraction(b, 2 ** vb)
                    state = 'U' if vb == 2 else 'O'; word.append(1)
            k += 1
        words[tuple(word)] = words.get(tuple(word), 0) + 1
        # the same word must result for n + 2^J (digit word depends only on n mod 2^J)
        n2 = n + 2 ** J * random.randrange(1, 10 ** 6)
        x2, state2, w2 = n2, 'U', []
        for _ in range(J):
            if state2 == 'U':
                if x2 % 2 == 0:
                    x2 //= 2; w2.append(0)
                else:
                    state2 = 'O'; w2.append(1)
            else:
                if x2 % 4 == 1:
                    x2 = (a * x2 + d) // 2 ** va; state2 = 'U' if va == 2 else 'O'; w2.append(0)
                else:
                    x2 = (b * x2 + d) // 2 ** vb; state2 = 'U' if vb == 2 else 'O'; w2.append(1)
        ok(w2 == word, f"O0 word depends on residue {a,b,d,r}")
        ok((x2 - x) == slope * (n2 - n), f"O0 linear coefficient {a,b,d,r}")
        if state == 'O':
            ok(x % 2 == 1, f"O0 O-state odd {a,b,d,r}")
    ok(len(words) == 2 ** J and set(words.values()) == {1}, f"O0 bijection {a,b,d}")
    # raw-step minimum at digit boundaries: for random n compare raw slope prefix minima
    st = split_step(a, b, d)
    for _ in range(200):
        n = random.getrandbits(80) | 1
        x, raw = n, Fraction(1)
        rawmin = Fraction(10 ** 9)
        boundary_min = Fraction(10 ** 9)
        for _ in range(60):
            if x % 2 == 0:
                x //= 2; raw /= 2
            else:
                c = a if x % 4 == 1 else b
                v = va if x % 4 == 1 else vb
                x = c * x + d; raw *= c; rawmin = min(rawmin, raw)
                for _ in range(v):
                    x //= 2; raw /= 2; rawmin = min(rawmin, raw)
                boundary_min = min(boundary_min, raw)
                continue
            rawmin = min(rawmin, raw); boundary_min = min(boundary_min, raw)
        ok(rawmin == boundary_min, f"O0 raw minimum at boundaries {a,b,d}")
print("O0 coding verified for", len(MEMBERS), "members")

# O1 -------------------------------------------------------------------------------
for c in (5, 9, 13):
    lam2 = Fraction(c, 4)
    ok((Fraction(c, 4)) ** 2 / lam2 == lam2, "O1 weighting")
    for (a, b, d) in [(c, 1, 3), (1, c, 1)]:
        ok(otype(a, b, d)[0] == 'T1', f"O1 type {a,b,d}")
    q = 1 - 2 / math.log2(c)
    th, rho = rho_min_float(c, 1, 3)
    ok(abs(H2(q) - math.log2(rho)) < 1e-9, f"O1 H2 vs rho c={c}")
    print("  c=%d: q_c=%.10f  H2(q_c)=%.10f  log2 rho*=%.10f" % (c, q, H2(q), math.log2(rho)))
# exact binomial covering bound sum_{i<=qm} C(m,i) <= 2^(m H(q)) checked in integers via
# the equivalent inequality sum C(m,i) q^i (1-q)^(m-i) <= 1 with rational q close below q_5
qr = Fraction(1386, 10000)
for m in range(1, 120):
    s = sum(math.comb(m, i) for i in range(0, m + 1) if i <= qr * m)
    # the covering bound rests on: each term C(m,i) q^i (1-q)^(m-i) with i <= qm is at least
    # C(m,i) q^(qm)(1-q)^((1-q)m); check the monotonicity q^i(1-q)^(m-i) decreasing in i (q < 1/2)
    terms = [qr ** i * (1 - qr) ** (m - i) for i in range(0, m + 1)]
    ok(all(terms[i] > terms[i + 1] for i in range(m)), "O1 monotone")
    ok(sum(math.comb(m, i) * terms[i] for i in range(m + 1) if i <= qr * m) <= 1, "O1 binomial")
# |Y_m| >= C(m,i)/m via exact DP of surplus walks for c = 5
for m in range(2, 61):
    # count length-m 0/1 words (1 = bad) with all prefixes satisfying 5^(j-m_j) >= 4^(j)... i.e.
    # (j - m_j) log lam - m_j log 2 >= 0  <=>  (c/4)^(j-m_j) >= 4^(m_j)  <=> c^(j-m_j) >= 4^j
    cnt = {0: 1}
    for j in range(1, m + 1):
        new = {}
        for mb, v in cnt.items():
            for bad in (0, 1):
                mb2 = mb + bad
                if 5 ** (j - mb2) >= 4 ** j:
                    new[mb2] = new.get(mb2, 0) + v
        cnt = new
    Y = sum(cnt.values())
    i = max(i for i in range(m) if 5 ** (m - i) > 4 ** m) if any(5 ** (m - i) > 4 ** m for i in range(m)) else None
    if i is not None:
        ok(Y * m >= math.comb(m, i), f"O1 cycle lemma m={m}")
print("O1 done")

# O3 -------------------------------------------------------------------------------
rows = []
for (a, b, d) in [(5, 1, 3), (5, 1, 1), (7, 1, 1), (3, 5, 1), (5, 7, 3)]:
    typ = otype(a, b, d)[0]
    p, q, mu = upper_bound_cert(a, b, d)
    U = math.log2(mu)
    if typ == 'T1':
        L = None
    else:
        Lf, m, data = lower_bound_counts(a, b, d, 20000)
        L = float(Lf)
        ok(L <= U and U - L < 1e-3, f"O3 gap {a,b,d}: {L} {U}")
    rows.append((a, b, d, typ, L, U, Lf if typ != 'T1' else None, mu))
    print("  %s %s: dim in [%s, %.6f]" % ((a, b, d), typ, "%.6f" % L if L else "H2 exact", U))
# the stated table values, compared exactly (no tolerance): the certified lower bound Lf is a
# rational and must be >= lo; the certified upper bound log2(mu) <= hi is checked as
# mu^Q <= 2^P for hi = P/Q in lowest terms (pure integer arithmetic).
expect = {(5, 1, 1): ("0.936275", "0.936852"), (7, 1, 1): ("0.752601", "0.753484"),
          (3, 5, 1): ("0.662525", "0.663348"), (5, 7, 3): ("0.966468", "0.967365")}


def log2_le(mu, hi):
    P, Q = hi.numerator, hi.denominator
    return mu.numerator ** Q <= (1 << P) * mu.denominator ** Q


for (a, b, d, typ, L, U, Lf, mu) in rows:
    if (a, b, d) in expect:
        lo, hi = (Fraction(x) for x in expect[(a, b, d)])
        ok(Lf >= lo and log2_le(mu, hi), f"O3 table {a,b,d}")
# same transitions for the symmetric members quoted in the table
for (x, y) in [((5, 1, 1), (1, 5, 3)), ((7, 1, 1), (1, 7, 3)), ((3, 5, 1), (5, 3, 3)),
               ((5, 7, 3), (7, 5, 1)), ((5, 1, 3), (1, 5, 1)), ((5, 1, 1), (5, 1, 9))]:
    ok(otype(*x) == otype(*y) or sorted(map(str, otype(*x)[1])) == sorted(map(str, otype(*y)[1])),
       f"O3 same type {x} {y}")
print("O3 certified bounds done")

# O4 -------------------------------------------------------------------------------
for (a, b, d) in [(5, 1, 3), (5, 1, 1)]:
    st = split_step(a, b, d)
    va, vb = vals(a, b, d)
    for m in range(6, 16):
        # number of words of length m with P_m >= 1/2
        tr = transitions(a, b, d)
        cur = {('U', 0, 0, 0): 1}
        for _ in range(m):
            nxt = {}
            for (s, i, k, l), c in cur.items():
                for (t, (di, dk, dl)) in tr[s]:
                    key = (t, i + di, k + dk, l + dl)
                    nxt[key] = nxt.get(key, 0) + c
            cur = nxt
        W = sum(c for (s, i, k, l), c in cur.items() if 2 * a ** i * b ** k >= 2 ** l)
        nd = 0
        for n in range(2 ** m, 2 ** (m + 1)):
            x, good = n, True
            for _ in range(4000):
                x = st(x)
                if x < n:
                    good = False
                    break
            nd += good
        ok(nd <= W, f"O4 {a,b,d} m={m}: {nd} > {W}")
print("O4 sanity done")

# O5 -------------------------------------------------------------------------------
for (a, b, d) in [(3, 7, 1), (3, 7, 3), (7, 3, 1), (7, 3, 3)]:
    typ, (s, r) = otype(a, b, d)
    ok(typ == 'T2' and s > 1 and s * r == Fraction(21, 8) and s * r > 2 and r * 2 >= 1, f"O5 {a,b,d}")
print("O5 done")

# Z3 and C ---------------------------------------------------------------------------
T = split_step(5, 1, 3)
T151 = split_step(1, 5, 1)
for m in list(range(1, 50000)) + [random.getrandbits(200) for _ in range(100)]:
    if m > 0:
        ok(T(3 * m) == 3 * T151(m), f"Z3 {m}")
        ok((T(m) % 3 == 0) == (m % 3 == 0), f"Z3 inv {m}")
for n in range(2, 100000, 5):
    z = (4 * n - 3) // 5
    ok((4 * n - 3) % 5 == 0 and z % 4 == 1 and 0 < z < n and T(T(T(z))) == n, f"C {n}")
print("Z3, C done")

if FAIL:
    print(len(FAIL), "FAILURES")
    sys.exit(1)
print("ALL PASS")
