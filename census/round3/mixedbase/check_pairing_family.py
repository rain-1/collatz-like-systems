"""Check for pairing_family.md (Theorems P1-P5).  Exact integer / Fraction arithmetic.

P1 block lemma            : exhaustive |n| <= 6000 and 300 random 200-bit n (both signs) for
                            a in {3,5,7,9,11,13}, K in {1,2,3,4}, x* in {1,-1,5,-7,11,13,-25};
P2 symmetry / scaling     : T_{-x}(-n) = -T_x(n), T_x(x n) = x T_1(n) on |n| <= 3000;
P3 GLOBAL (K=1, (3,2))    : the |.|-descent inequality of the proof on 5|x*| < |n| <= 20000, and
                            the cycle lists of the theorem (all n with |n| <= 5|x*| simulated);
                            plus the run-accelerated certificates (pairlib) for x* = +-1;
P4 no plain certificate   : x* is an exact T^-fixed point, multiplier a/2, for all tested params;
P5 no accelerated cert.   : the explicit expanding cycles for a >= 5, K >= 2 and a = 3, K >= 3.
Runs in ~20 s.  Exits non-zero on any failure.
"""
import random
import sys
import os
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pairlib import Pairing, v2
from mixedlib import verify_periodic, rat_mod

random.seed(20261127)
XS = [1, -1, 5, -7, 11, 13, -25]


def table(P):
    m = P.m
    tab = {}
    for rho in range(2 * m):
        if rho % m == P.r:
            tab[rho] = (1, P.c, m)
        elif rho % 2 == 0:
            tab[rho] = (1, 0, 2)
        else:
            tab[rho] = (P.a, P.b, 2)
    return 2 * m, tab


def block_check(P, n):
    """P1: T^(j+1+q)(n) = (x* + a^l u)/2 and every intermediate value is as claimed."""
    a, K, xs, m = P.a, P.K, P.xs, P.m
    d = n - xs
    j = v2(d)
    u = d >> j
    assert u % 2 == 1
    q, l = divmod(j, K)
    y = n
    for i in range(j):                        # up-run
        assert y == xs + a ** i * 2 ** (j - i) * u and y % 2 == 1 and y % m != P.r
        y = P.T(y)
    assert y == xs + a ** j * u and y % 2 == 0 and y % m != P.r
    y = P.T(y)                                # one halving
    k = j
    assert 2 * y == xs + a ** k * u
    for _ in range(q):                        # down-run
        assert y % m == P.r
        y = P.T(y)
        k -= K
        assert 2 * y == xs + a ** k * u
    assert k == l
    z, s = P.S(n)
    assert z == y and s == j + 1 + q


def main():
    t_count = 0
    # ---- P1 ---------------------------------------------------------------
    for a in [3, 5, 7, 9, 11, 13]:
        for K in [1, 2, 3, 4]:
            if a ** K > 10 ** 5:
                continue
            for xs in XS:
                if xs % a == 0 or xs % 3 == 0 and a % 3 == 0:
                    continue
                from math import gcd
                if gcd(a, xs) != 1:
                    continue
                P = Pairing(a, K, xs)
                rng = range(-6000, 6001) if (a, K) in [(3, 1), (3, 2), (5, 1), (3, 3)] else range(-800, 801)
                for n in list(rng) + [random.choice([-1, 1]) * random.getrandbits(200) for _ in range(300)]:
                    if n % 2 == 1 and n % P.m != P.r and n != xs:
                        block_check(P, n)
                        t_count += 1
    print("P1 block lemma: ok,", t_count, "instances")
    # ---- P2 ---------------------------------------------------------------
    for a in [3, 5, 7]:
        for K in [1, 2, 3]:
            for xs in [1, 5, 7, 11, 13]:
                if xs % a == 0:
                    continue
                Pp, Pm, P1 = Pairing(a, K, xs), Pairing(a, K, -xs), Pairing(a, K, 1)
                for n in range(-3000, 3001):
                    assert Pm.T(-n) == -Pp.T(n)
                    assert Pp.T(xs * n) == xs * P1.T(n)
    print("P2 symmetry and scaling: ok")
    # ---- P3 ---------------------------------------------------------------
    expected = {}
    ndesc = 0
    for (a, K) in [(3, 1), (5, 1), (7, 1), (9, 1), (11, 1), (13, 1), (3, 2)]:
        B = 5 if (a, K) == (3, 2) else 1
        for xs in [1, -1, 5, -5, 7, -7, 11, 13, 17, 19, -23, 25, 29, 31, 35, 37, 41, 43]:
            from math import gcd
            if gcd(a, xs) != 1:
                continue
            P = Pairing(a, K, xs)
            X = abs(xs)
            # descent inequality of the proof: every |n| > B|x*| has a later iterate of smaller |.|
            for n in range(-20000, 20001):
                if abs(n) <= B * X:
                    continue
                if n % P.m == P.r or n % 2 == 0:
                    y = P.T(n)
                else:
                    y, _ = P.S(n)
                assert abs(y) < abs(n), (a, K, xs, n, y)
                ndesc += 1
            # cycles: simulate every n with |n| <= B|x*|
            cycs = set()
            for n0 in range(-B * X, B * X + 1):
                seen = []
                y = n0
                pos = {}
                while y not in pos:
                    pos[y] = len(seen)
                    seen.append(y)
                    y = P.T(y)
                cyc = seen[pos[y]:]
                i = cyc.index(min(cyc))
                cycs.add(tuple(cyc[i:] + cyc[:i]))
            expected[(a, K, xs)] = sorted(cycs)
    # the cycle lists quoted in pairing_family.md
    assert expected[(3, 2, 1)] == [(-2, -1), (0,), (1,)], expected[(3, 2, 1)]
    assert expected[(3, 2, -1)] == [(-1,), (0,), (1, 2)], expected[(3, 2, -1)]
    for a in [3, 5, 7, 9, 11, 13]:
        assert expected[(a, 1, 1)] == [(0,), (1,)], (a, expected[(a, 1, 1)])
    for k in sorted(expected):
        if abs(k[2]) > 1:
            assert all(min(abs(z) for z in c) <= (5 if k[:2] == (3, 2) else 1) * abs(k[2]) for c in expected[k])
    print("P3 descent inequality + cycle lists: ok,", ndesc, "descent instances")
    if '-v' in sys.argv:
        for k in sorted(expected):
            print("   ", k, expected[k])
    for key in [(3, 1, 1), (5, 1, 1), (7, 1, 1), (3, 2, 1), (3, 2, -1), (7, 1, -1), (5, 1, -1)]:
        print("   cycles on Z of P%s:" % (key,), expected[key])
    # accelerated certificates for x* = +-1 (independent of the hand proof)
    for (a, K) in [(3, 1), (5, 1), (7, 1), (9, 1), (11, 1), (13, 1), (3, 2)]:
        for xs in [1, -1]:
            P = Pairing(a, K, xs)
            res = P.prove(maxnodes=200000)
            assert res['ok']
            cyc_pos = sorted(c for c in res['cycles'])
            if xs == 1:
                assert cyc_pos == [(1,)], cyc_pos
            else:
                assert cyc_pos == ([(0,), (1, 2)] if (a, K) == (3, 2) else [(0,)]), cyc_pos
    print("P3 run-accelerated certificates (N+ for x*=1, N0 for x*=-1): ok")
    # ---- P4 ---------------------------------------------------------------
    for a in [3, 5, 7, 9, 11, 13]:
        for K in [1, 2, 3]:
            for xs in [1, -1, 5, 7, -11]:
                from math import gcd
                if gcd(a, xs) != 1:
                    continue
                P = Pairing(a, K, xs)
                M0, tab = table(P)
                lam, orb = verify_periodic(M0, tab, Fraction(xs), 1)
                assert lam == Fraction(a, 2)
    print("P4 x* is an expanding fixed point of T^ (no plain certificate): ok")
    # ---- P5 ---------------------------------------------------------------
    for a in [5, 7, 9, 11, 13, 15, 17]:
        for K in [2, 3, 4]:
            if a ** K > 10 ** 5:
                continue
            for xs in [1, -1, 7, -11, 13]:
                from math import gcd
                if gcd(a, xs) != 1:
                    continue
                P = Pairing(a, K, xs)
                M0, tab = table(P)
                y = Fraction((2 - a) * xs, 4 - a)
                lam, orb = verify_periodic(M0, tab, y, 2)
                assert lam == Fraction(a, 4) and orb[1] == 2 * y
    for K in [3, 4, 5, 6, 7]:
        for xs in [1, -1, 5, -7, 11, 13]:
            P = Pairing(3, K, xs)
            M0, tab = table(P)
            lam, orb = verify_periodic(M0, tab, Fraction(5 * xs), 3)
            assert lam == Fraction(9, 8) and orb == [5 * xs, 7 * xs, 10 * xs]
    # and for K <= 2 / K = 1 these cycles are caught (sanity: the theorem is sharp)
    P = Pairing(3, 2, 1)
    assert 5 % 9 == P.r
    P = Pairing(5, 1, 1)
    assert 3 % 5 == P.r
    print("P5 explicit expanding cycles (no accelerated certificate): ok")
    print("ALL OK")


if __name__ == "__main__":
    main()
