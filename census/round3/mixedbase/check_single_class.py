"""Check for single_class.md (Theorems S3, S5, S7).

T_{m,r,c}(n) = (n + c)/m if n = r (mod m)  [c = -r mod m, priority];  n/2 if n even;
               (a n + 1)/2 otherwise.            (a = 3, 5, 7; m odd >= 3)

For every odd m in [3, 301] and every residue r, an exact witness that no descent certificate
exists is produced and verified (fixed point / explicit cycle / run identity / Lemma D'' word),
except for the classes of the theorems, where a certificate is built, verified, and Lemma A'
gives the cycle list.  Witnesses do not depend on c; they are verified for two values of c.
For a = 7 the classification is checked for odd m <= 199 by hitting constraints (exact
expanding cycles of the plain map, Lyndon words of length <= 14).
Runs in ~60 s.
"""
import sys, os, math, random
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mixedlib import (verify_periodic, rat_mod, prove_global, lyndon_words, certificate)

random.seed(5)


def table(m, r, c, a):
    tab = {}
    for rho in range(2 * m):
        if rho % m == r:
            tab[rho] = (1, c, m)
        elif rho % 2 == 0:
            tab[rho] = (1, 0, 2)
        else:
            tab[rho] = (a, 1, 2)
    return 2 * m, tab


def T(m, r, c, a, n):
    if n % m == r:
        assert (n + c) % m == 0
        return (n + c) // m
    if n % 2 == 0:
        return n // 2
    return (a * n + 1) // 2


def crt(r1, m1, r2, m2):
    g = math.gcd(m1, m2)
    assert g == 1
    return (r1 + m1 * ((r2 - r1) * pow(m1, -1, m2) % m2)) % (m1 * m2)


def run_witness(m, r, c, a, n_mod, mod, N=48):
    """Lemma R: n = x* (mod 2^N) and n = n_mod (mod mod) (mod | m); check
    T^i(n) = x* + (a/2)^i (n - x*) for 1 <= i <= N-1 on several such n, and that the
    residue mod `mod` of every run value differs from r mod `mod`."""
    xs = Fraction(1, 2 - a)
    x2 = rat_mod(xs, 2 ** N)
    base = crt(x2, 2 ** N, n_mod % mod, mod) if mod > 1 else x2
    step = 2 ** N * mod
    for t in [1, 7, random.getrandbits(64)]:
        n = base + step * t
        y = n
        for i in range(1, N):
            y = T(m, r, c, a, y)
            assert y == xs + Fraction(a, 2) ** i * (n - xs)
            assert (y - r) % mod != 0
        assert y > n
    return True


def word_witness(m, r, c, a, L):
    """Lemma D'': the word U^L Q; its rational fixed point must be verified periodic."""
    A, B = Fraction(1), Fraction(0)
    for _ in range(L):
        A, B = A * Fraction(a, 2), (a * B + 1) / 2
    A, B = A / m, (B + c) / m
    y = B / (1 - A)
    M0, tab = table(m, r, c, a)
    lam, orb = verify_periodic(M0, tab, y, L + 1)
    assert lam == A and lam > 1
    return y


def cycle_witness(m, r, c, a, cyc):
    M0, tab = table(m, r, c, a)
    lam, orb = verify_periodic(M0, tab, Fraction(cyc[0]), len(cyc))
    assert lam > 1
    return True


def fixed_witness(m, r, c, a):
    xs = Fraction(1, 2 - a)
    M0, tab = table(m, r, c, a)
    lam, _ = verify_periodic(M0, tab, xs, 1)
    assert lam == Fraction(a, 2)


def factor_out(m, p):
    k = 0
    while m % p == 0:
        m //= p
        k += 1
    return k, m


def classify3(m, r, c):
    a = 3
    if r != m - 1:
        fixed_witness(m, r, c, a)
        return 'fixed -1'
    if m % 3:
        run_witness(m, r, c, a, 0, m)
        return 'run'
    if m in (3, 9):
        return 'CERT'
    assert all((y - r) % m for y in (-5, -7, -10))
    cycle_witness(m, r, c, a, [-5, -7, -10])
    return 'cycle -5'


def classify5(m, r, c):
    a = 5
    xs = Fraction(-1, 3)
    if m % 3:
        if (3 * r + 1) % m:
            fixed_witness(m, r, c, a)
            return 'fixed -1/3'
        l, mm = factor_out(m, 5)
        if mm > 1:
            run_witness(m, r, c, a, 0, mm)
            return 'run'
        if (m, r) == (5, 3):
            return 'CERT'
        assert all((y - r) % m for y in (-1, -2))
        cycle_witness(m, r, c, a, [-1, -2])
        return 'cycle -1'
    k, rest = factor_out(m, 3)
    l, mm = factor_out(rest, 5)
    if mm > 1:
        x_mm = rat_mod(xs, mm)
        if r % mm == x_mm:
            run_witness(m, r, c, a, 0, mm)
        else:
            run_witness(m, r, c, a, x_mm, mm)
        return 'run'
    if l == 0:
        word_witness(m, r, c, a, m - 1)
        return 'word U^(m-1)Q'
    if r % 5 ** l != rat_mod(xs, 5 ** l):
        run_witness(m, r, c, a, rat_mod(xs, 5 ** l), 5 ** l)
        return 'run'
    if (r + 1) % m and (r + 2) % m:
        cycle_witness(m, r, c, a, [-1, -2])
        return 'cycle -1'
    # here l = 1 and r = -2 (mod m): the plain cycle through -14/17 is uncaught
    y = Fraction(-14, 17)
    M0, tab = table(m, r, c, a)
    lam, orb = verify_periodic(M0, tab, y, 3)
    assert lam == Fraction(25, 8)
    return 'cycle -14/17'


def plain_cycles(a, maxlen):
    out = []
    for wd in lyndon_words(2, maxlen):
        A, B = Fraction(1), Fraction(0)
        for i in wd:
            A, B = (A * Fraction(a, 2), (a * B + 1) / 2) if i == 0 else (A / 2, B / 2)
        if A <= 1:
            continue
        x = B / (1 - A)
        if x.denominator % 2 == 0:
            continue
        y, ok, orb = x, True, []
        for i in wd:
            if (i == 0) != (rat_mod(y, 2) == 1):
                ok = False
                break
            orb.append(y)
            y = (a * y + 1) / 2 if i == 0 else y / 2
        if ok and y == x:
            out.append(orb)
    return out


def main():
    stats = {}
    for m in range(3, 302, 2):
        for r in range(m):
            for c in {(-r) % m, (-r) % m - m}:
                k3 = classify3(m, r, c)
                k5 = classify5(m, r, c)
                stats[('3', k3)] = stats.get(('3', k3), 0) + 1
                stats[('5', k5)] = stats.get(('5', k5), 0) + 1
    print("witness counts:", sorted(stats.items()))
    # the certified classes
    for (m, r, c, a, cyc) in [(3, 2, 1, 3, [(1, 2)]), (9, 8, 1, 3, [(1, 2)]), (5, 3, 2, 5, [(1, 3)])]:
        M0, tab = table(m, r, c, a)
        res = prove_global(M0, tab)
        assert res['ok'] and sorted(res['cycles']) == cyc, res.get('cycles')
        print("certificate (m,r,c,a) =", (m, r, c, a), "leaves", res['nleaves'], "max j", res['maxj'],
              "|E|", res['E'], "cycles", res['cycles'])
    # consistency with the engine on small m (no certificate where a witness exists)
    for a, cls in [(3, classify3), (5, classify5)]:
        for m in range(3, 28, 2):
            for r in range(m):
                c = (-r) % m
                M0, tab = table(m, r, c, a)
                ok = certificate(M0, tab, maxnodes=20000, maxdepth=150)['ok']
                assert ok == (cls(m, r, c) == 'CERT'), (a, m, r)
    print("engine agrees with the classification for m <= 27")
    # a = 7 by hitting constraints
    cyc7 = plain_cycles(7, 14)
    certs = []
    for m in range(3, 200, 2):
        cons = []
        for orb in cyc7:
            if any(math.gcd(y.denominator, m) > 1 for y in orb):
                continue
            cons.append({rat_mod(y, m) for y in orb})
        for r in range(m):
            if all(r in s for s in cons):
                certs.append((m, r))
    assert certs == [(7, 4)], certs
    M0, tab = table(7, 4, 3, 7)
    res = prove_global(M0, tab)
    assert res['ok'] and res['cycles'] == [(1, 4)]
    print("a = 7: the only single class mod odd m <= 199 meeting every expanding plain cycle is 4 mod 7;"
          " certified, cycles", res['cycles'])
    print("ALL OK")


if __name__ == "__main__":
    main()
