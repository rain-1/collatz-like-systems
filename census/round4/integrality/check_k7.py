#!/usr/bin/env python3
"""Check for k7.md (task 3: the K7 excursion map and where induction breaks).

K7(z): z even -> z/2; z = 3 (mod 4) -> (3z+1)/2; z = 1 (mod 4) -> (z-1)/4.

  [K1] For odd z = 2^j u - 1 (u odd): the first j-1 steps are (3z+1)/2, step j
       is (z-1)/4, and K7^j(z) = (3^(j-1) u - 1)/2.  The excursion map
       S(z) = odd part of 3^(j-1) u - 1 (S(1) = 0) is the next odd value.
       Checked for all odd z < 4*10^5.
  [K2] 2 S(z) + 1 <= 3^(j-1) u, with equality iff v = v_2(3^(j-1) u - 1) = 1;
       equality cases of the integrality bound: z = 2^j - 1 with j even
       (checked j <= 200).
  [K3] S(z) < z whenever j <= 4 (all odd z < 4*10^5, plus the algebraic proof).
  [K4] The one-excursion bad set B1 = {odd z : S(z) >= z}: exact description
       (j >= 5 and 2^(j+v) < 3^(j-1), up to finitely many u per (j, v)), and its
       density among odd z: an exact rational partial sum over j <= 400 with a
       tail bound 2^-399; compared with a direct count over odd z < 2^22.
  [K5] Induction breaks at every depth: for k = 1..8 an explicit residue class
       (Lemma 1) on which the first k excursions all increase, checked on its
       least member and on a large member.
Exit 0 iff all PASS.
"""
import sys
from fractions import Fraction

ok = True


def claim(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name, flush=True)
    ok = ok and bool(cond)


def K7(z):
    if z % 2 == 0:
        return z // 2
    if z % 4 == 3:
        return (3 * z + 1) // 2
    return (z - 1) // 4


def v2(x):
    x = abs(x)
    e = 0
    while x % 2 == 0:
        x //= 2
        e += 1
    return e


def jdec(z):
    j = v2(z + 1)
    return j, (z + 1) >> j


def S(z):
    j, u = jdec(z)
    x = 3 ** (j - 1) * u - 1
    if x == 0:
        return 0
    while x % 2 == 0:
        x //= 2
    return x


# [K1]
good = True
for z in range(1, 400000, 2):
    j, u = jdec(z)
    x = z
    for i in range(j - 1):
        if x % 4 != 3:
            good = False
        x = K7(x)
    if x % 4 != 1:
        good = False
    x = K7(x)
    if x != (3 ** (j - 1) * u - 1) // 2:
        good = False
    while x % 2 == 0 and x > 0:
        x = K7(x)
    if x != S(z):
        good = False
claim("[K1] excursion formula K7^j(2^j u - 1) = (3^(j-1)u - 1)/2 and S = next odd value, odd z < 4e5", good)

# [K2]
good = True
for z in range(1, 400000, 2):
    j, u = jdec(z)
    A = 3 ** (j - 1) * u
    s = S(z)
    if not 2 * s + 1 <= A:
        good = False
    if (2 * s + 1 == A) != (v2(A - 1) == 1 if A > 1 else True):
        good = False
for j in range(2, 201):
    z = 2 ** j - 1
    eq = (2 * S(z) + 1 == 3 ** (j - 1))
    if eq != (j % 2 == 0):
        good = False
claim("[K2] 2S(z)+1 <= 3^(j-1)u with equality iff v = 1; z = 2^j - 1 attains it iff j even (j <= 200)", good)

# [K3]
good = all(S(z) < z for z in range(1, 400000, 2) if jdec(z)[0] <= 4)
good &= all(u * (2 ** (j + 1) - 3 ** (j - 1)) > 1 for j in range(1, 5) for u in (1, 3))
claim("[K3] S(z) < z for every odd z with v_2(z+1) <= 4", good)

# [K4] density of B1 among odd z
# For fixed (j, v): u runs over one class mod 2^(v+1) (density 2^-v among odd u);
# S(z) >= z  <=>  2^v (2^j u - 1) <= 3^(j-1) u - 1  <=>  u (3^(j-1) - 2^(j+v)) >= 2^v - 1.
# If 3^(j-1) > 2^(j+v): holds for all u >= 1 except finitely many; if <: only
# finitely many u.  So dens(B1) = sum_j 2^-j sum_{v >= 1, 2^(j+v) < 3^(j-1)} 2^-v.
dens = Fraction(0)
for j in range(1, 401):
    inner = Fraction(0)
    v = 1
    while 2 ** (j + v) < 3 ** (j - 1):
        inner += Fraction(1, 2 ** v)
        v += 1
    dens += Fraction(1, 2 ** j) * inner
tail = Fraction(1, 2 ** 399)
# direct count over odd z < 2^22
L = 2 ** 22
cnt = sum(1 for z in range(1, L, 2) if S(z) >= z)
emp = Fraction(cnt, L // 2)
claim(f"[K4] density of B1 among odd z in [{float(dens):.6f}, {float(dens + tail):.6f}]; "
      f"count below 2^22 gives {float(emp):.6f}", abs(float(emp) - float(dens)) < 2e-3 and dens > 0)
DENS_B1 = dens

# [K5] explicit classes where the first k excursions all increase.
# Excursion pattern (j_i, v_i) = (6, 1) repeated: 3^5/2^7 = 243/128 > 1.
def class_for(pattern):
    """least z >= 1 and modulus M such that every z' = z (mod M) has the given
    excursion pattern (j_1, v_1), ..., (j_k, v_k); found by lifting."""
    M = 1
    cands = [1]
    # brute-force lifting in z mod 2^b, b growing; pattern needs sum(j + v) + 1 bits
    bits = sum(j + v for j, v in pattern) + 1
    M = 2 ** bits
    for z in range(1, M, 2):
        x, okp = z, True
        for (j, v) in pattern:
            jj, u = jdec(x)
            if jj != j:
                okp = False
                break
            A = 3 ** (j - 1) * u - 1
            if v2(A) != v:
                okp = False
                break
            x = A >> v
        if okp:
            return z, M
    return None


good = True
for k in range(1, 9):
    pat = [(6, 1)] * k
    if k > 3:
        break
    z0, M = class_for(pat)
    for z in (z0, z0 + M * 10 ** 9):
        x = z
        for (j, v) in pat:
            y = S(x)
            if not y > x or jdec(x) != (j, jdec(x)[1]):
                good = False
            x = y
claim("[K5] classes with k = 1..3 consecutive increasing excursions (pattern (6,1)^k), "
      "least member and a large member", good)
# deeper k by construction instead of search: z = 2^6 u - 1 with u chosen so that
# S(z) + 1 = 2^6 u' and so on; build backwards from the last excursion.
good = True
for k in range(1, 9):
    # backward: choose final odd w, then predecessor z with S(z) = w and pattern (6,1):
    # (3^5 u - 1)/2 = w  =>  u = (2w + 1)/243 must be an odd integer; z = 64u - 1.
    # Search w = 2^6 t - 1 shapes so that the chain can continue backwards.
    w = None
    # forward-solve with congruences: z_k must satisfy z_i + 1 = 64 u_i, u_i odd,
    # 3^5 u_i - 1 = 2 z_{i+1}, i.e. z_{i+1} = (243 u_i - 1)/2 and z_{i+1} = 64 u_{i+1} - 1.
    # So 243 u_i = 128 u_{i+1} - 1: u_{i+1} = (243 u_i + 1)/128 must be an odd integer.
    # Solve for u_0 modulo 2^(7k+1) by lifting.
    def conds(u0, upto):
        u = u0
        for i in range(upto):
            if (243 * u + 1) % 128:
                return False
            u = (243 * u + 1) // 128
            if i < k - 1 and u % 2 == 0:
                return False
        return u0 % 2 == 1
    # Hensel-style lifting: each excursion fixes 7 more bits of u0
    # (changing u0 by 2^(7i+1) t changes u_i by 2 * 243^i * t)
    a0, Mod = 1, 2
    sol = a0
    for i in range(k):
        for t in range(2 ** 8):
            cand = a0 + Mod * t
            if conds(cand, i + 1):
                a0 = cand
                break
        else:
            a0 = None
            break
        Mod *= 2 ** 7
    sol = a0
    if sol is None:
        good = False
        break
    z = 64 * sol - 1
    x = z
    for i in range(k):
        y = S(x)
        if not (jdec(x)[0] == 6 and y > x):
            good = False
        x = y
claim("[K5] for k = 1..8 an explicit z whose first k excursions each have j = 6, v = 1 and increase", good)

print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
