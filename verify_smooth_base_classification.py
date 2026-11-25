"""Checks for the base-2^x*3^y classification of forward-closed automatic sets.

The note output/pdf/smooth_base_invariants.pdf proves: if S is b-automatic
for b = 2**x * 3**y (x, y >= 1) and G(S) is inside S for the 1932 permutation
G, then S or its complement has density zero. This script tests every exact
identity that proof uses, on finite ranges, and then measures which base-6
digit blocks occur on the two half-orbits of 8. Nothing here is a proof of
an all-n statement; the identities are proved in the note by induction.

Run: python3 verify_smooth_base_classification.py [--steps 30000] [--block 7]
"""
import argparse
from fractions import Fraction
from itertools import product


def G(n):
    q, r = divmod(n, 3)
    return (2 * q, 4 * q + 1, 4 * q + 3)[r]


def Ginv(n):
    if n % 2 == 0:
        return 3 * n // 2
    return (3 * n + 1) // 4 if n % 4 == 1 else (3 * n - 1) // 4


def iterate(f, n, k):
    for _ in range(k):
        n = f(n)
    return n


def check_inverse(limit=5000):
    for n in range(limit):
        assert Ginv(G(n)) == n and G(Ginv(n)) == n


def forward_classes(k):
    """Map r mod 3**k -> (e, beta) with G**k(3**k q + r) = 2**e q + beta."""
    out = {}
    for r in range(3 ** k):
        beta = iterate(G, r, k)
        e, n = 0, r
        for _ in range(k):
            e += 1 if n % 3 == 0 else 2
            n = G(n)
        for q in (1, 2, 5, 11):
            assert iterate(G, 3 ** k * q + r, k) == 2 ** e * q + beta
        assert 0 <= beta < 2 ** e
        out[r] = (e, beta)
    return out


def check_forward_weights(kmax=7):
    """Sum of 2**-e over the lifts of a class mod 3**k0 is 2**-e(k0 class)."""
    tables = [forward_classes(k) for k in range(kmax + 1)]
    for k0 in range(kmax + 1):
        for k in range(k0, kmax + 1):
            for r0 in range(3 ** k0):
                total = sum(Fraction(1, 2 ** tables[k][r][0])
                            for r in range(r0, 3 ** k, 3 ** k0))
                assert total == Fraction(1, 2 ** tables[k0][r0][0])
    # images of the classes mod 3**k partition the integers
    for k in range(kmax + 1):
        assert sum(Fraction(1, 2 ** e) for e, _ in tables[k].values()) == 1


def backward_class(n, i):
    """Return (ell, beta, rho): n = beta mod 2**ell fixes i backward branches
    and G**-i(2**ell m + beta) = 3**i m + rho."""
    ell, cur = 0, n
    for _ in range(i):
        ell += 1 if cur % 2 == 0 else 2
        cur = Ginv(cur)
    beta = n % 2 ** ell
    rho = iterate(Ginv, beta, i)
    return ell, beta, rho


def check_backward_classes(imax=7):
    for i in range(imax + 1):
        weight = Fraction(0)
        seen = set()
        for n in range(4 ** i):
            ell, beta, rho = backward_class(n, i)
            assert i <= ell <= 2 * i and 0 <= rho < 3 ** i
            for m in (0, 1, 2, 7, 12):
                assert iterate(Ginv, 2 ** ell * m + beta, i) == 3 ** i * m + rho
            if (ell, beta) not in seen:
                seen.add((ell, beta))
                weight += Fraction(1, 2 ** ell)
        assert weight == 1  # the classes partition the nonnegative integers


def check_kernel_bridge(x, y, jmax=11):
    """Every f(2**J q + B) equals K(2**t q + c) composed with G**-i, where K
    is a b-kernel restriction n -> f(b**a n + R) and t < x + 2*y."""
    b = 2 ** x * 3 ** y
    tmax = 0
    for J in range(jmax + 1):
        for B in range(2 ** J):
            a = 0
            while True:
                ell_next = backward_class(B, y * (a + 1))[0]
                if ell_next + x * (a + 1) > J:
                    break
                a += 1
            i = y * a
            ell, beta, rho = backward_class(B, i)
            t = J - ell - x * a
            assert 0 <= t < x + 2 * y
            tmax = max(tmax, t)
            Bp = B >> ell
            R = 3 ** i * Bp + rho
            assert R < 2 ** t * b ** a
            c, Rp = divmod(R, b ** a)
            for q in (0, 1, 2, 3, 10, 37):
                lhs = iterate(Ginv, 2 ** J * q + B, i)
                assert lhs == b ** a * (2 ** t * q + c) + Rp
    return tmax


def check_periodic_invariants(mmax=80):
    """p o G = p with p periodic mod m forces p constant."""
    for m in range(1, mmax + 1):
        parent = list(range(m))

        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v

        for n in range(3 * m):
            parent[find(n % m)] = find(G(n) % m)
        assert len({find(v) for v in range(m)}) == 1, m


def digits(n, base):
    out = []
    while n:
        n, d = divmod(n, base)
        out.append(d)
    return out[::-1]


def block_census(step, start, steps, base, length, skip_first):
    """Blocks of the given length occurring after the leading digit."""
    seen = bytearray(base ** length)
    count, n = 0, start
    mod = base ** length
    first_full = None
    for j in range(steps + 1):
        if j >= skip_first:
            ds = digits(n, base)[1:]
            if len(ds) >= length:
                code = 0
                for pos, d in enumerate(ds):
                    code = (code * base + d) % mod
                    if pos >= length - 1 and not seen[code]:
                        seen[code] = 1
                        count += 1
                if count == mod and first_full is None:
                    first_full = j
                    break
        n = step(n)
    return count, mod, first_full


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=30000)
    ap.add_argument("--block", type=int, default=7)
    ap.add_argument("--base", type=int, default=6)
    args = ap.parse_args()

    check_inverse()
    check_forward_weights()
    check_backward_classes()
    print("forward weight identity and backward class formula: ok")
    for x, y in product((1, 2, 3), (1, 2)):
        tmax = check_kernel_bridge(x, y)
        print(f"kernel bridge, base {2**x * 3**y}: ok (largest t seen {tmax},"
              f" bound {x + 2*y - 1})")
    check_periodic_invariants()
    print("periodic G-invariant functions are constant for moduli <= 80: ok")

    L = args.block
    fwd = block_census(G, 8, args.steps, args.base, L, skip_first=1)
    bwd = block_census(Ginv, 8, args.steps, args.base, L, skip_first=0)
    for name, (count, total, first) in (("forward", fwd), ("backward", bwd)):
        where = f"complete at step {first}" if first is not None else "incomplete"
        print(f"{name} half-orbit of 8, base {args.base}, blocks of length {L}: "
              f"{count}/{total} seen, {where}")
    if fwd[2] is not None and bwd[2] is not None:
        r = 1
        while (r - 1) ** 2 <= L:
            r += 1
        print(f"consequence: a base-{args.base} separator for 8 needs an "
              f"avoided block longer than {L}, hence at least {r} states")


if __name__ == "__main__":
    main()
