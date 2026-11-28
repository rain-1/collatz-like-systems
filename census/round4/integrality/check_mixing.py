#!/usr/bin/env python3
"""Exact checks for mixing.md (Theorems M, Nhat; Theorem R is a proof only).

[M-run]  For three type-(c) examples and d = 0..8: the run map R = T^(d*l) sends
         the residues n mod p^(K+dE+J) with n = x* (mod p^(K+dE)) bijectively
         onto the residues s mod p^(K+J) with s = r0 (mod p^K).  So the
         distribution of the post-run value does not depend on d, whatever the
         congruence properties of the multiplier (u = 3, 4, 5 below; 4 = 1 mod 3,
         5 = 1 mod 4).
[M-walk] The same full-branch property for 300 random closed walks of G_K
         through r0 (Lemma 1 / Markov property, restated as an exact count).
[M-iid]  Exact joint count: for the first two excursion depths (d1, d2) of
         n mod p^J, the number of residues with (d1, d2) equals
         count(d1) * count(d2) / (number of residues), for all pairs that are
         decided at level J.
[Nhat]   Theorem N over Zhat: for the expanding periodic points y_d of C^d W
         (d = 0..16) and for integers n = y_d (mod p^N) with ARBITRARY residues
         modulo M' = 3^4 5^3 7^2 (p = 2) or 2^6 5^3 7^2 (p = 3), the orbit
         satisfies T^j(n) > n for all 1 <= j <= J0 (along the rotated walk).
         So cylinders of any modulus (not only p-adic ones) cannot separate.
Exit 0 iff all PASS.
"""
import sys, os, random
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import intlib as IL
AL = IL.AL

ok = True


def claim(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok = ok and bool(cond)


SF7 = [(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r == 7 else (1, 1, 1)) for r in range(8)]
G3 = [(1, 0, 3), (1, 2, 3), (1, 1, 3), (1, 0, 3), (1, 2, 3), (1, 1, 3), (1, 0, 3), (1, 2, 3), (4, 1, 3)]
F5 = [(1, 0, 2), (1, 1, 1), (1, 0, 2), (5, -1, 2)]
EXAMPLES = [
    # name, p, m, table, K, x*
    ("sf3_7 (K7, u=3)", 2, 3, SF7, 3, Fraction(-1)),
    ("G3 (u=4=1 mod 3)", 3, 2, G3, 2, Fraction(-1)),
    ("F5 (u=5=1 mod 4)", 2, 2, F5, 2, Fraction(1, 3)),
]


def nres(x, mod):
    return (x.numerator * pow(x.denominator, -1, mod)) % mod


for name, p, m, table, K, xs in EXAMPLES:
    IL.positivity_ok(p, m, table)
    kind, _ = IL.system_type(p, m, table, K)
    claim(f"[type] {name}: type c_mixed and decide.py says OBST",
          kind == "c_mixed" and IL.decide_verdict(p, m, table) == "OBST")
    T = IL.step_fn(p, m, table)
    C, lamC = AL.orbit_residues(xs, p, m, table, K)
    ell = len(C)
    # number of divisions by p along one lap (exponents)
    E = 0
    for r in C:
        w = table[r % p ** m][2]
        while w % p == 0:
            w //= p
            E += 1
    r0 = C[0]
    J = 4
    good = True
    for d in range(0, 9):
        N = K + d * E
        base = nres(xs, p ** N)
        img = set()
        for t in range(p ** J):
            n = base + t * p ** N
            if n == 0:
                n += p ** (N + J + 2)
            n2 = n + 7 * p ** (N + J + 3)
            x, x2 = n, n2
            for _ in range(d * ell):
                x, x2 = T(x), T(x2)
            s = x % p ** (K + J)
            if s != x2 % p ** (K + J) or s % p ** K != r0:
                good = False
            img.add(s)
        if len(img) != p ** J:
            good = False
    claim(f"[M-run] {name}: run map is a bijection onto the cylinder of r0, d = 0..8", good)

    # [M-walk] random closed walks through r0
    G = AL.graph(p, m, table, K)
    random.seed(7)
    good = True
    tested = 0
    for _ in range(300):
        walk = [r0]
        for _ in range(random.randint(1, 7)):
            walk.append(random.choice(G[walk[-1]])[0])
        # close it with a BFS path back to r0
        comp = next(c for c in AL.tarjan(list(range(p ** K)), G) if r0 in c)
        if walk[-1] not in comp:
            continue
        back = AL.bfs_path(G, set(comp), walk[-1], r0) if walk[-1] != r0 else [r0]
        walk = walk + back[1:]
        L = len(walk) - 1
        Ew = 0
        for r in walk[:-1]:
            w = table[r % p ** m][2]
            while w % p == 0:
                w //= p
                Ew += 1
        # the integers following the walk form one progression a + M t (Lemma 1);
        # its first p^J members must map onto all residues mod p^(K+J) above walk[-1]
        assert K == m
        a, M, A_, B_, D_ = IL.DC.path_progression(p ** m, table, walk)
        img = set()
        cnt = 0
        for t in range(p ** J):
            x = a + M * t
            for i in range(L):
                assert x % p ** K == walk[i]
                x = T(x)
            cnt += 1
            img.add(x % p ** (K + J))
        if M != p ** (K + Ew) or any(s_ % p ** K != walk[-1] for s_ in img):
            good = False
        tested += 1
        if cnt != p ** J or len(img) != p ** J:
            good = False
    claim(f"[M-walk] {name}: {tested} closed walks, each cylinder maps onto the cylinder of r0", good and tested > 50)

    # [M-iid] exact joint law of the first two lap counts.  Events: d1 = a,
    # return walk (r0 -> ... -> r0, not a lap of C) with at most RMAX divisions,
    # d2 = b, for a, b <= 2.  With Jt = K + 5E + RMAX every such event is decided
    # by n mod p^Jt, so residue counts are exact Haar masses (times p^Jt).
    from collections import Counter
    RMAX = 3
    Jt = K + 5 * E + RMAX
    Mt = p ** Jt
    Qm = p ** m

    def ediv(r):
        w, e = table[r % Qm][2], 0
        while w % p == 0:
            w //= p
            e += 1
        return e

    def run(x, known, cap):
        """laps of C from x (x = r0 mod p^K, known mod p^known); returns
        (d, x_after, known_after) with d < cap, or None if d >= cap."""
        d = 0
        while True:
            assert known >= K + E
            if (Fraction(x) - xs).numerator % p ** (K + E) == 0:
                d += 1
                if d >= cap:
                    return None
                for _ in range(ell):
                    x = T(x)
                known -= E
            else:
                return d, x, known

    joint = Counter()
    for n in range(Mt, 2 * Mt):
        if n % p ** K != r0:
            continue
        r1 = run(n, Jt, 3)
        if r1 is None:
            continue
        d1, x, known = r1
        used = 0
        first = True
        while first or x % p ** K != r0:
            first = False
            assert known >= K
            e = ediv(x)
            x = T(x)
            known -= e
            used += e
            if used > RMAX:
                x = None
                break
        if x is None:
            continue
        r2 = run(x, known, 3)
        if r2 is None:
            continue
        joint[(d1, r2[0])] += 1
    good = joint[(0, 0)] > 0
    for d1 in range(0, 3):
        for d2 in range(0, 3):
            if joint[(d1, d2)] * joint[(0, 0)] != joint[(d1, 0)] * joint[(0, d2)]:
                good = False
    claim(f"[M-iid] {name}: (d1, d2) counts factor exactly on residues mod p^{Jt} "
          f"(table {[joint[(i, j)] for i in range(3) for j in range(3)]})", good)

    # [Nhat] Theorem N over Zhat
    Cw, lamC2, W, rows = AL.barrier_witness(p, m, table, K, xs, dmax=16)
    Mp = (3 ** 4 * 5 ** 3 * 7 ** 2) if p == 2 else (2 ** 6 * 5 ** 3 * 7 ** 2)
    good = True
    nexp = 0
    for d, y, lam in rows:
        if not lam > 1:
            continue
        nexp += 1
        walk = Cw * d + W
        # rotate the walk (cycle lemma) so every partial multiplier is > 1
        Q = p ** m
        mults = [Fraction(table[r % Q][0], table[r % Q][2]) for r in walk]
        L = len(walk)
        pref = [Fraction(1)]
        for q in mults:
            pref.append(pref[-1] * q)
        i0 = max(i for i in range(L) if pref[i] == min(pref[:L]))
        # the rotated periodic point: iterate y i0 steps
        yy = y
        for r in walk[:i0]:
            u, v, w = table[r % Q]
            yy = (u * yy + v) / w
        laps_ = 3
        N = K + 8 * laps_ * (sum(1 for r in walk if table[r % Q][2] > 1) + 2)
        base = nres(yy, p ** N)
        for c in (0, 1, 17, Mp - 1, 12345 % Mp):
            # n = yy mod p^N and n = c mod Mp (CRT), n > 0
            n = base + p ** N * (((c - base) * pow(p ** N, -1, Mp)) % Mp)
            assert n % Mp == c and (n - base) % p ** N == 0
            n += p ** N * Mp * 10 ** 6           # make it large
            x = n
            for j in range(1, laps_ * L + 1):
                x = T(x)
                if not x > n:
                    good = False
    claim(f"[Nhat] {name}: {nexp} expanding witnesses y_d; integers near y_d with arbitrary "
          f"residues mod {Mp} rise for 3 full laps", good and nexp >= 3)

print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
