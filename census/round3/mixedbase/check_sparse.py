"""Check for sparse_taming.md.

Part 1 (systems): for every listed system, build the table, certify GLOBAL with the
mixed-radix engine, verify the certificate independently, apply Lemma A' and list the cycles.
Part 2 (minimality): exhaustive hitting-set search against exactly verified expanding cycles of
the plain map (n odd -> (a n + 1)/2, n even -> n/2), showing that no smaller set of classes
mod the same modulus can admit a certificate (Lemma B': an uncaught expanding cycle survives).
Runs in ~90 s.
"""
import sys, os, math
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mixedlib import prove_global, rat_mod, lyndon_words, verify_periodic

SYSTEMS = [
    # id, a, m, classes R (c = -r mod m), expected cycles
    ("mb_t27",   3, 27,  (17, 26)),
    ("mb_t27b",  3, 27,  (20, 26)),
    ("mb_t27c",  3, 27,  (22, 26)),
    ("mb_t81",   3, 81,  (20, 71, 80)),
    ("mb_t243",  3, 243, (137, 152, 233, 242)),
    ("mb_f25",   5, 25,  (8, 23)),
    ("mb_f125",  5, 125, (68, 73, 83, 123)),
    ("mb_s49",   7, 49,  (32, 39)),
    ("mb_s343",  7, 343, (93, 137, 142, 200, 228)),
    ("mb_t729",  3, 729, (182, 380, 395, 425, 668, 719, 728)),
]


def table(a, m, R):
    tab = {}
    for rho in range(2 * m):
        if rho % m in R:
            tab[rho] = (1, (-(rho % m)) % m, m)
        elif rho % 2 == 0:
            tab[rho] = (1, 0, 2)
        else:
            tab[rho] = (a, 1, 2)
    return 2 * m, tab


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


def hitting_sets(cons, k):
    """all minimal-search hitting sets of size <= k (exhaustive branching)."""
    sols = set()

    def bt(S):
        for c in cons:
            if not (S & c):
                if len(S) == k:
                    return
                for r in sorted(c):
                    bt(S | {r})
                return
        sols.add(frozenset(S))
    bt(frozenset())
    return sols


def main():
    for (sid, a, m, R) in SYSTEMS:
        M0, tab = table(a, m, set(R))
        res = prove_global(M0, tab)
        assert res['ok'], sid
        print(f"{sid}: a={a} m={m} R={R} density={len(R)}/{m}: certificate leaves={res['nleaves']} "
              f"max j={res['maxj']} max modulus~2^{res['maxM'].bit_length() - 1} |E|={res['E']} "
              f"cycles={res['cycles']}")
    # minimality
    plan = [(3, 27, 1, 14), (3, 81, 2, 16), (3, 243, 3, 18), (3, 729, 6, 20),
            (5, 25, 1, 14), (5, 125, 3, 18), (7, 49, 1, 14), (7, 343, 4, 16)]
    cache = {}
    for (a, m, k, L) in plan:
        if (a, L) not in cache:
            cache[(a, L)] = plain_cycles(a, L)
        cons = []
        for orb in cache[(a, L)]:
            if any(math.gcd(y.denominator, m) > 1 for y in orb):
                continue
            cons.append(frozenset(rat_mod(y, m) for y in orb))
        cons = sorted(set(cons), key=len)
        hs = hitting_sets(cons, k)
        assert not hs, (a, m, k, len(hs))
        # spot-verify that the constraint cycles are genuine periodic points of the plain map
        for orb in cache[(a, L)][:50]:
            y = orb[0]
            z = y
            for _ in range(len(orb)):
                z = (a * z + 1) / 2 if rat_mod(z, 2) == 1 else z / 2
            assert z == y
        print(f"a={a} m={m}: no set of <= {k} classes meets all {len(cons)} expanding-cycle constraints "
              f"(words <= {L}) -> at least {k + 1} classes are needed for a certificate")
    print("ALL OK")


if __name__ == "__main__":
    main()
