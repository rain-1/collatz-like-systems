"""Check for relatives.md: sparse taming of the open entries div23_5n1 (CLS-002/059) and
m3_b (CLS-004/061) by added residue classes.  (Repaired after the referee report.)

1. certify the named systems (engine + verification + Lemma A' + complete cycle list);
2. exact expanding rational cycles of the *base* maps (Lyndon words <= 11 over their rows),
   plus exact verification of the specific integer / rational cycles used in the bounds;
3. Theorem D(1): the bound q <= 83 from the two INTEGER cycles (-1 -4 -2) and
   (-84 -42 -21 -7 -34 -17) (valid for every q, either priority); then the exhaustive
   (q, r) scan for q <= 83 with the refined Lemma B' (a cycle whose denominator shares primes
   with q only constrains r modulo the part q1 of q prime to that denominator);
   (the old scan over q <= 3000 is also kept as a consistency check);
4. Theorem D(2): every survivor except 'first' (2,0) and (4,2) is certified, and its COMPLETE
   cycle list is computed and asserted against the table in relatives.md;
5. Theorem M: one class -> q | 2 and the system odd -> (n+1)/2 has cycles (1), (2 3);
   two classes -> {1,-1} mod q; refined Lemma B' with (1/7, -1/7) gives q = 7^e q1, q1 | 6 or 8;
   the cycle (7/25, 1/25, -7/25, -1/25) (denominator prime to 42) gives q <= 32; scan q <= 32
   with the refined criterion -> {3, 4, 6, 8}; each certified with cycle list [(1,)].
Runs in ~10 s.
"""
import sys, os, math
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mixedlib import prove_global, rat_mod, word_cycles, table_rows, certificate


def lcm(a, b):
    return a * b // math.gcd(a, b)


def div23_row(rho):
    if rho % 2 == 0:
        return (1, 0, 2)
    if rho % 3 == 0:
        return (1, 0, 3)
    return (5, 1, 1)


def m3b_row(rho):
    return [(1, 0, 3), (4, -1, 3), (4, 1, 3)][rho % 3]


def build(base_M, row, q, R, prio='first'):
    M0 = lcm(base_M, q)
    tab = {}
    for rho in range(M0):
        b = row(rho)
        if rho % q in R and (prio == 'first' or b[0] > 1):
            tab[rho] = (1, (-(rho % q)) % q, q)
        else:
            tab[rho] = b
    return M0, tab


def base_step_rat(base_M, row, y):
    u, v, w = row(rat_mod(y, base_M))
    return (u * y + v) / w


def verify_cycle(base_M, row, orb):
    """exact: orb is a cycle of the base map T^ (on Z_S, rational points); return multiplier."""
    lam = F(1)
    for i, y in enumerate(orb):
        assert base_step_rat(base_M, row, y) == orb[(i + 1) % len(orb)], orb
        u, v, w = row(rat_mod(y, base_M))
        lam *= F(u, w)
    return lam


def coprime_part(q, d):
    """part of q prime to d"""
    g = math.gcd(q, d)
    while g > 1:
        q //= g
        g = math.gcd(q, d)
    return q


def survives(q, R, cycles, ok_point):
    """refined Lemma B': for every base cycle, with q1 = part of q prime to the cycle's
    denominators, some admissible point y must satisfy y mod q1 in R mod q1."""
    for orb in cycles:
        d = 1
        for y in orb:
            d = lcm(d, y.denominator)
        q1 = coprime_part(q, d)
        if q1 == 1:
            continue
        R1 = {r % q1 for r in R}
        if not any(ok_point(y) and rat_mod(y, q1) in R1 for y in orb):
            return False
    return True


NAMED = [
    ("mb_d23_8",  6, div23_row, 8, {7}),
    ("mb_d23_4",  6, div23_row, 4, {3}),
    ("mb_d23_30", 6, div23_row, 30, {26}),
    ("mb_m3b_8",  3, m3b_row, 8, {1, 7}),
]

# Theorem D(2): complete cycle lists of the certified survivors (relatives.md table)
D_CYCLES = {
    ('first', 2, 1): [(1,)],
    ('first', 3, 1): [(1,), (5, 26, 13)],
    ('first', 5, 1): [(1,)],
    ('first', 6, 2): [(1, 6, 3), (5, 26)],
    ('first', 10, 6): [(1, 6)],
    ('last', 2, 1): [(1,)],
}
D_DEFAULT = [(1, 6, 3)]
D_LIST = {'first': [(2, 0), (2, 1), (3, 1), (3, 2), (4, 2), (4, 3), (5, 1), (5, 3), (6, 2), (6, 5),
                    (8, 7), (10, 6), (15, 11), (15, 13), (30, 26)],
          'last': [(2, 1), (3, 2), (6, 5)]}
D_UNCERT = {('first', 2, 0), ('first', 4, 2)}


def canon(cycles):
    out = []
    for c in cycles:
        c = list(c)
        i = c.index(min(c))
        out.append(tuple(c[i:] + c[:i]))
    return sorted(out)


def main():
    for sid, bM, row, q, R in NAMED:
        M0, tab = build(bM, row, q, R)
        res = prove_global(M0, tab)
        assert res['ok'], sid
        print(f"{sid}: q={q} R={sorted(R)}: leaves={res['nleaves']} max j={res['maxj']} |E|={res['E']} "
              f"cycles={res['cycles']}")
        assert canon(res['cycles']) == ([(1,)] if sid == 'mb_m3b_8' else [(1, 6, 3)]), sid

    # ---- div23_5n1 -------------------------------------------------------------
    cyc, tab6 = (lambda M0: (word_cycles(M0, table_rows(M0, {r: div23_row(r) for r in range(M0)}), 11),
                             {r: div23_row(r) for r in range(M0)}))(6)
    orbs = [o for x, L, l, o in cyc]
    print("div23_5n1: expanding rational cycles found (words <= 11):", len(cyc))
    A = [F(-1), F(-4), F(-2)]
    B = [F(-84), F(-42), F(-21), F(-7), F(-34), F(-17)]
    lamA, lamB = verify_cycle(6, div23_row, A), verify_cycle(6, div23_row, B)
    assert lamA == F(5, 4) and lamB == F(25, 24), (lamA, lamB)
    assert any(set(o) == set(A) for o in orbs) and any(set(o) == set(B) for o in orbs)
    # 'last'-admissible points (those in the 5n+1 branch) on each cycle are a subset; the bound
    # uses all points, so it holds for both priorities.  Both cycles are integral, so they lie in
    # every Z_q and Lemma B' applies to them for every q.
    bound = int(max(abs(y - z) for y in A for z in B))
    assert all(y != z for y in A for z in B)
    print("div23: q | (y - z), y on (-1 -4 -2), z on (-84 ... -17), all integers; max |y-z| =", bound)
    assert bound == 83
    ok_pt = {'first': lambda y: True, 'last': lambda y: div23_row(rat_mod(y, 6))[0] > 1}
    surv = {p: [(q, r) for q in range(2, bound + 1) for r in range(q)
                if survives(q, {r}, orbs, ok_pt[p])] for p in ('first', 'last')}
    print("div23 + one class, refined Lemma B', q <= 83:", surv)
    assert surv == D_LIST, surv
    # consistency: the older coarse scan (skip cycles not coprime to q) up to 3000 gives the same
    surv_old = {'first': [], 'last': []}
    for q in range(2, 3001):
        for prio in ('first', 'last'):
            cons = [{rat_mod(y, q) for y in o if ok_pt[prio](y)} for o in orbs
                    if all(math.gcd(y.denominator, q) == 1 for y in o)]
            surv_old[prio] += [(q, r) for r in range(q) if all(r in s for s in cons)]
    assert surv_old == D_LIST, surv_old
    for prio in ('first', 'last'):
        for q, r in surv[prio]:
            M0, tab = build(6, div23_row, q, {r}, prio)
            if (prio, q, r) in D_UNCERT:
                ok = certificate(M0, tab, maxnodes=200000, maxdepth=300)['ok']
                assert not ok
                print("   engine", prio, "q=%d r=%d:" % (q, r), "no certificate within budget"
                      + (" (the open map itself)" if q == 2 else " (UNRESOLVED)"))
                continue
            res = prove_global(M0, tab)
            assert res['ok'], (prio, q, r)
            cl = canon(res['cycles'])
            want = canon(D_CYCLES.get((prio, q, r), D_DEFAULT))
            assert cl == want, (prio, q, r, cl, want)
            print("   engine", prio, "q=%d r=%d: CERT, leaves=%d, cycles=%s" % (q, r, res['nleaves'], cl))

    # ---- m3_b --------------------------------------------------------------------
    cyc3 = word_cycles(3, table_rows(3, {r: m3b_row(r) for r in range(3)}), 11)
    orbs3 = [o for x, L, l, o in cyc3]
    print("m3_b: expanding rational cycles (words <= 11):", len(cyc3))
    for fp in (F(1), F(-1)):
        assert verify_cycle(3, m3b_row, [fp]) == F(4, 3)
    C1 = [F(1, 7), F(-1, 7)]
    C2 = [F(7, 25), F(1, 25), F(-7, 25), F(-1, 25)]
    print("   (1/7, -1/7) multiplier", verify_cycle(3, m3b_row, C1),
          "; (7/25, 1/25, -7/25, -1/25) multiplier", verify_cycle(3, m3b_row, C2))
    assert verify_cycle(3, m3b_row, C1) > 1 and verify_cycle(3, m3b_row, C2) > 1
    # one class r mod q must contain 1 and -1 (integers): q | 2
    one = [(q, r) for q in range(2, 200) for r in range(q) if (1 - r) % q == 0 and (-1 - r) % q == 0]
    assert one == [(2, 1)]
    M0, tab = build(3, m3b_row, 2, {1})
    res = prove_global(M0, tab)
    assert res['ok'] and canon(res['cycles']) == [(1,), (2, 3)], res.get('cycles')
    print("m3_b + (odd -> (n+1)/2): CERT, leaves=%d, cycles=%s" % (res['nleaves'], canon(res['cycles'])))
    # two classes {1,-1} mod q (q >= 3).  Refined Lemma B' with C1: q = 7^e q1, q1 | 6 or 8.
    nums1 = {abs((y - e).numerator) for y in C1 for e in (1, -1)}
    assert nums1 == {6, 8}
    # C2 has denominator 25, prime to 2, 3, 7, so for every q whose primes lie in {2,3,7}
    # (forced by C1 and the refined lemma) q | numerator of y -+ 1 for some y on C2.
    nums2 = {abs((y - e).numerator) for y in C2 for e in (1, -1)}
    bound_m = int(max(nums2))
    print("m3_b: C1 numerators", sorted(nums1), "; C2 numerators", sorted(nums2), "-> q <=", bound_m)
    assert bound_m == 32
    # sanity: the reduction "primes of q in {2,3,7}" from C1 on a wide range
    for q in range(3, 5000):
        R = {1 % q, (-1) % q}
        if survives(q, R, [C1], lambda y: True):
            assert set(p for p in range(2, q + 1) if q % p == 0 and all(p % s for s in range(2, p))) <= {2, 3, 7}, q
            q7 = coprime_part(q, 7)
            assert 6 % q7 == 0 or 8 % q7 == 0, q
    survm = [q for q in range(3, bound_m + 1)
             if survives(q, {1 % q, (-1) % q}, orbs3 + [C1, C2], lambda y: True)]
    print("m3_b + {1,-1} mod q, refined Lemma B', q <= 32:", survm)
    assert survm == [3, 4, 6, 8]
    for q in survm:
        M0, tab = build(3, m3b_row, q, {1 % q, (-1) % q})
        res = prove_global(M0, tab)
        assert res['ok'] and canon(res['cycles']) == [(1,)], (q, res.get('cycles'))
        print("   q=%d: CERT, leaves=%d, cycles=%s" % (q, res['nleaves'], canon(res['cycles'])))
    print("ALL OK")


if __name__ == "__main__":
    main()
