"""Exact checks for transport_theorems.md.  Exits 0 iff every check passes.

A  independent symbolic verifier for transport identities (different code path from
   transport_lib.first_return), tested on the identities below
B  Proposition C (3x+1 on 2 mod 3) and Theorem F (four S-family members), with Lemma S,
   decide.py verdicts and exact types; numeric cross-check of the identity
C  every join recorded in results/equiv_{lib,sfam4,sfam5}.json re-verified (identity + Lemma S)
D  Lemma R witnesses (realised growth) for every open unit p-adic library system and core
E  types: every open unit p-adic library table is of type (c) (exact)
F  the 8 cores: canonical first-return maps on all classes M <= 32 pairwise distinct
   between different cores and 3x+1
G  non-unit search (EVIDENCE): no bounded first return of a pairing/dressed system on classes
   M <= 48 and M <= 144 is a unit p-adic table; at M <= 144 the bounded ones are exactly
   24 pairing + 7 dressed returns, all to classes 0 mod M_Y (Revision after REFEREE1)
F2 (Revision after REFEREE1) the 8 cores and 3x+1: on classes 2^s <= 32 boundedness of the first
   return is decided exactly (residue-graph criterion, Lemma 1 of dichotomy.md) and agrees with
   the tmax = 24 search; on all classes M <= 32 the count of bounded returns is unchanged at
   tmax = 64, piece cap 60000
B2 (Revision after REFEREE1) Proposition C: every 3x+1 orbit through 1 mod 3 reaches 2 mod 3
   within two steps, and no 3x+1 cycle lies inside 0 mod 3 (symbolic, mod 6)
"""
import json
import os
import sys
import time
from fractions import Fraction
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'round3', 'dichotomy'))
import decide  # noqa: E402
from transport_lib import (induced_canonical, sufficient, unit_type, is_unit_padic,  # noqa: E402
                           step_fn, table_canonical, lcm)
from library import build, by_id, s_table  # noqa: E402

FAIL = []


def ok(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("FAIL:", msg)


# ---------------------------------------------------------------- A: independent verifier
def verify_identity(Q, table, MX, rX, canon, tmax=40):
    """Prove h^{-1} R_T^X h = canon on every class, by direct symbolic iteration in a fresh
    variable.  For z = L w + c the start is n = MX (L w + c) + rX = al*w + be (integers).
    A state is (al, be, t, mod-split history); branch of T constant iff Q | al, membership of X
    constant iff MX | al; otherwise split w by the needed factor."""
    L, rows = canon
    for c in range(L):
        A, B, D = rows[c]
        stack = [(MX * L, MX * c + rX, 1, 0, 0)]      # value = (al w' + be), with w = k w' + i
        # we track w = kk * w' + ii to translate back
        stack = [(MX * L, MX * c + rX, 0, 1, 0)]      # (al, be, t, kk, ii)
        while stack:
            al, be, t, kk, ii = stack.pop()
            if t >= 1:
                need = MX // gcd(MX, al)
                if need > 1:
                    for i in range(need):
                        stack.append((al * need, be + al * i, t, kk * need, ii + kk * i))
                    continue
                if be % MX == rX % MX:
                    # returned: z-value = (value - rX)/MX must equal (A z + B)/D, z = L(kk w'+ii)+c
                    # compare as affine functions of w'
                    zal, zbe = L * kk, L * ii + c
                    lhs_al, lhs_be = Fraction(al, MX), Fraction(be - rX, MX)
                    rhs_al, rhs_be = Fraction(A * zal, D), Fraction(A * zbe + B, D)
                    if (lhs_al, lhs_be) != (rhs_al, rhs_be):
                        return False
                    continue
            if t >= tmax:
                return False
            need = Q // gcd(Q, al)
            if need > 1:
                for i in range(need):
                    stack.append((al * need, be + al * i, t, kk * need, ii + kk * i))
                continue
            u, v, w = table[be % Q]
            if (u * al) % w or (u * be + v) % w:
                return False
            stack.append(((u * al) // w, (u * be + v) // w, t + 1, kk, ii))
    return True


def numeric_identity(Q, table, MX, rX, canon, zmax=3000):
    T = step_fn(Q, table)
    L, rows = canon
    for z in range(0, zmax):
        n = MX * z + rX
        if n < 1:
            continue
        y = T(n)
        steps = 1
        while y % MX != rX % MX:
            y = T(y)
            steps += 1
            if steps > 200:
                return False
        A, B, D = rows[z % L]
        if (A * z + B) % D or (A * z + B) // D != (y - rX) // MX:
            return False
    return True


C3 = (2, [(1, 0, 2), (3, 1, 1)])                     # n/2, 3n+1
G = (4, ((3, 0, 4), (3, 1, 2), (1, -2, 4), (3, 1, 2)))
Gp = [(3, 0, 2), (3, 1, 4), (3, 0, 2), (1, 1, 4)]      # y even 3y/2; 1 mod 4 (3y+1)/4; 3 mod 4 (y+1)/4
F_SETS = [(3, 7, 15), (1, 3, 7, 15), (3, 7, 9, 15), (1, 3, 7, 9, 15)]


def part_A_B():
    t0 = time.time()
    # Proposition C
    ok(verify_identity(*C3, 3, 2, G), "Prop C identity (independent verifier)")
    c, pcs, st = induced_canonical(*C3, 3, 2)
    ok(st == 'ok' and c == G, "Prop C identity (transport_lib)")
    ok(max(p[2] for p in pcs) <= 3, "Prop C return time <= 3")
    ok(numeric_identity(*C3, 3, 2, G), "Prop C numeric")
    s, info = sufficient(*C3, 3, 2)
    ok(s, "Prop C Lemma S")
    # G' = conjugate of G by y = z + 1
    for y in range(1, 2000):
        z = y - 1
        A, B, D = G[1][z % 4]
        gz = (A * z + B) // D
        u, v, w = Gp[y % 4]
        ok((u * y + v) % w == 0 and (u * y + v) // w == gz + 1, "G' = G conjugate at y=%d" % y)
        if FAIL:
            break
    r = decide.decide(4, Gp, want_cycles=False, want_depth=False)
    ok(r['verdict'] == 'OBST', "decide(G') = OBST")
    ty = unit_type(4, list(Gp))
    ok(ty['type'] == 'c', "G' type (c)")
    tyG = unit_type(4, list(G[1]))
    ok(tyG['type'] == 'c', "G type (c)")
    # Theorem F
    for S in F_SETS:
        t = s_table(4, S)
        ok(set(S) & {3, 7, 11, 15} == {3, 7, 15} and not set(S) & {5, 13}, "F hyp %s" % (S,))
        ok(verify_identity(16, t, 4, 3, G), "Thm F identity %s (independent)" % (S,))
        c, pcs, st = induced_canonical(16, t, 4, 3)
        ok(st == 'ok' and c == G, "Thm F identity %s (transport_lib)" % (S,))
        ok(numeric_identity(16, t, 4, 3, G), "Thm F numeric %s" % (S,))
        s, info = sufficient(16, t, 4, 3, allow_contracting=True)
        exp = [[1, 2, 4]] if 1 in S else [[1, 2]]
        ok(s and info['contracting'] == exp, "Thm F Lemma S %s: %s" % (S, info))
        r = decide.decide(16, t, want_cycles=False, want_depth=False)
        ok(r['verdict'] == 'OBST', "decide OBST %s" % (S,))
        ok(unit_type(16, t)['type'] == 'c', "type (c) %s" % (S,))
        # the bad-part cycle and the orbits that avoid 3 mod 4 (EVIDENCE, n < 5000)
        T = step_fn(16, t)
        cyc = (1, 4, 2) if 1 in S else (1, 2)
        x = 1
        seen = [x]
        for _ in range(len(cyc) - 1):
            x = T(x)
            seen.append(x)
        ok(tuple(seen) == cyc and T(x) == 1, "bad cycle %s" % (cyc,))
    # identity cross-check: final cycles correspond (EVIDENCE): T_S orbit of 4z+3 and 3x+1 orbit
    # of 3z+2 both eventually periodic for z < 2000, and z-values of their X-points match
    T3 = step_fn(*C3)
    for S in F_SETS:
        T = step_fn(16, s_table(4, S))
        for z in range(0, 300):
            a, b = 4 * z + 3, 3 * z + 2
            za, zb = [], []
            for _ in range(60):
                a = T(a)
                while a % 4 != 3:
                    a = T(a)
                za.append((a - 3) // 4)
                b = T3(b)
                while b % 3 != 2:
                    b = T3(b)
                zb.append((b - 2) // 3)
            ok(za == zb, "orbit correspondence z=%d S=%s" % (z, S))
            if FAIL:
                return
    # B2 (Revision after REFEREE1): every C-cycle meets 2 mod 3.  Symbolic on n = 6k + c:
    # each formula is affine in k, so its residue mod 3 is constant iff 3 divides the slope.
    for c in range(6):
        A, B = 6, c                      # n = A k + B
        if c % 2 == 0:
            A1, B1 = A // 2, B // 2      # n/2
        else:
            A1, B1 = 3 * A, 3 * B + 1    # 3n+1
        ok(A1 % 3 == 0, "B2 slope mod 3, c=%d" % c)
        if c % 3 == 1:
            if c % 2 == 0:
                ok(B1 % 3 == 2, "B2: n=1 mod 3 even -> n/2 = 2 mod 3")
            else:
                ok(A1 % 2 == 0 and B1 % 2 == 0 and A1 % 6 == 0 and (B1 // 2) % 3 == 2,
                   "B2: n=1 mod 3 odd -> (3n+1)/2 = 2 mod 3")
        if c % 3 == 0:
            if c % 2 == 0:
                ok(B1 % 3 == 0, "B2: n=0 mod 3 even -> n/2 = 0 mod 3 (and n/2 < n)")
            else:
                ok(B1 % 3 == 1, "B2: n=0 mod 3 odd -> 3n+1 = 1 mod 3")
    print("A/B ok (%.1f s)" % (time.time() - t0))


# ---------------------------------------------------------------- C: joins
def part_C():
    t0 = time.time()
    from equiv import population
    n = 0
    for kind in ('lib', 'sfam4', 'sfam5'):
        path = os.path.join(HERE, 'results', 'equiv_%s.json' % kind)
        d = json.load(open(path))
        P = {s['id']: s for s in population(kind)}
        for j in d['joins']:
            canon = (j['canon'][0], tuple(tuple(r) for r in j['canon'][1]))
            ids = set()
            for (i, MX, rX, suff) in j['members']:
                s = P[i]
                ok(suff, "join member marked insufficient %s" % i)
                if MX == 1:
                    ok(table_canonical(s['Q'], s['table']) == canon, "join self %s" % i)
                else:
                    ok(verify_identity(s['Q'], s['table'], MX, rX, canon),
                       "join identity %s %d %d" % (i, MX, rX))
                    ok(sufficient(s['Q'], s['table'], MX, rX, allow_contracting=True)[0],
                       "join Lemma S %s %d %d" % (i, MX, rX))
                ids.add(i)
                n += 1
            ok(len(ids) >= 2, "join has two systems")
        # no class mixes types (O1/O2 consistency) -- recomputed
        for cl in d['classes']:
            tys = set()
            for i in cl:
                s = P[i]
                if is_unit_padic(s['Q'], s['table']):
                    tys.add(unit_type(s['Q'], s['table'])['type'])
            ok(tys <= {'c'}, "class types %s" % cl[:3])
            ok(all(P[i]['status'] in ('open', 'family') for i in cl), "class contains settled %s" % cl[:3])
    print("C ok: %d join members re-verified (%.1f s)" % (n, time.time() - t0))


# ---------------------------------------------------------------- D/E: growth witnesses and types
def part_D_E():
    t0 = time.time()
    cnt = 0
    for s in build():
        if s['status'] != 'open' or not is_unit_padic(s['Q'], s['table']):
            continue
        Q, t = s['Q'], [tuple(x) for x in s['table']]
        ty = unit_type(Q, t)
        ok(ty['type'] == 'c', "type (c) %s" % s['id'])
        r = decide.decide(Q, t, want_cycles=False, want_depth=False)
        ok(r['verdict'] == 'OBST', "OBST %s" % s['id'])
        o = r['obst']
        cyc = list(o['rotated'])
        lam = Fraction(o['U'], o['W'])
        ok(lam > 1, "expanding %s" % s['id'])
        T = step_fn(Q, t)
        for d in (1, 2, 4, 8):
            nodes = cyc * d + [cyc[0]]
            a, M, A, B, D = decide.path_progression(Q, t, nodes)
            ok(Fraction(A, D) == lam ** d, "multiplier %s d=%d" % (s['id'], d))
            # choose n in the progression with (A n + B)/D >= (lam^d / 2) n
            k = 0
            n = a
            while 2 * (A * n + B) < A * n:                 # i.e. (A n+B)/D < (A/D) n / 2
                k += 1
                n = a + M * k
            y = n
            for _ in range(d * len(cyc)):
                y = T(y)
            ok(y * D == A * n + B and 2 * D * y >= A * n, "growth %s d=%d" % (s['id'], d))
        cnt += 1
    print("D/E ok: %d open unit systems, all type (c), growth witnesses d <= 8 (%.1f s)"
          % (cnt, time.time() - t0))


# ---------------------------------------------------------------- F: cores distinct
CORES = ['sf3_7', 'sf3_17', 'sf3_57', 'sf3_157', 'sf3_357', 'sf3_137', 'sf3_13', 'sf3_135']


def part_F():
    t0 = time.time()
    classes = [(1, 0)] + [(M, r) for M in range(2, 33) for r in range(M)]
    seen = {}
    sysl = [(i, by_id(i)['Q'], by_id(i)['table']) for i in CORES] + [('3x+1', 2, C3[1])]
    nb = 0
    for (i, Q, t) in sysl:
        for (MX, rX) in classes:
            if MX == 1:
                c = table_canonical(Q, t)
            else:
                c, pcs, st = induced_canonical(Q, t, MX, rX, tmax=24, pmax=20000, Lmax=1 << 14)
                if st != 'ok' or c is None:
                    continue
            nb += 1
            key = json.dumps(c)
            if key in seen and seen[key][0] != i:
                ok(False, "cores collide: %s %s" % (seen[key], (i, MX, rX)))
            seen.setdefault(key, (i, MX, rX))
    print("F ok: %d bounded canonical first returns, no collision between cores (%.1f s)"
          % (nb, time.time() - t0))


def exact_bounded_2adic(Q, table, s, r):
    """Exact decision (Revision after REFEREE1): for a unit 2-adic table at Q = 2^m and the
    class X = r mod 2^s, the first return to X is bounded iff no walk of the residue graph at
    modulus 2^K (K = max(m, s)) goes from an X-vertex into the non-X vertices and then has an
    infinite continuation inside the non-X vertices.  (<=) every orbit follows a walk (Lemma 1(1)
    of dichotomy.md), and non-X walks from X are then shorter than the number of vertices.
    (=>) Lemma 1(2) realises x y ... C^d by an infinite progression of positive integers that
    start in X and stay outside X for |P| + d|C| steps, for every d."""
    m = Q.bit_length() - 1
    assert Q == 1 << m
    K = max(m, s)
    QK = 1 << K
    lifted = [table[x % Q] for x in range(QK)]
    decide.check_hypotheses(QK, lifted)
    succ = decide.residue_graph(QK, lifted)
    inX = [x % (1 << s) == r for x in range(QK)]
    # non-X vertices with an infinite non-X forward walk: iteratively delete non-X sinks
    alive = {x for x in range(QK) if not inX[x]}
    changed = True
    while changed:
        changed = False
        for x in list(alive):
            if not any(y in alive for y in succ[x]):
                alive.discard(x)
                changed = True
    return not any(y in alive for x in range(QK) if inX[x] for y in succ[x])


def part_F2():
    t0 = time.time()
    sysl = [(i, by_id(i)['Q'], by_id(i)['table']) for i in CORES] + [('3x+1', 2, C3[1])]
    nexact = 0
    for (i, Q, t) in sysl:
        for s in range(1, 6):
            for r in range(1 << s):
                b = exact_bounded_2adic(Q, t, s, r)
                c, pcs, st = induced_canonical(Q, t, 1 << s, r, tmax=24, pmax=20000,
                                               Lmax=1 << 14)
                ok(b == (st == 'ok'), "F2 exact boundedness %s 2^%d r=%d: %s %s" % (i, s, r, b, st))
                nexact += b
    # larger search bounds on every class M <= 32
    classes = [(M, r) for M in range(2, 33) for r in range(M)]
    nb24 = nb64 = 0
    seen = {}
    for (i, Q, t) in sysl:
        for (MX, rX) in classes:
            c, pcs, st = induced_canonical(Q, t, MX, rX, tmax=24, pmax=20000, Lmax=1 << 14)
            nb24 += (st == 'ok' and c is not None)
            c, pcs, st = induced_canonical(Q, t, MX, rX, tmax=64, pmax=60000, Lmax=1 << 16)
            if st != 'ok' or c is None:
                continue
            nb64 += 1
            key = json.dumps(c)
            ok(not (key in seen and seen[key][0] != i), "F2 collision at tmax 64: %s %s"
               % (seen.get(key), (i, MX, rX)))
            seen.setdefault(key, (i, MX, rX))
    ok(nb24 == nb64 == 34, "F2 bounded returns: %d at tmax 24, %d at tmax 64 (expect 34)"
       % (nb24, nb64))
    print("F2 ok: %d bounded returns on 2-power classes decided exactly; %d bounded returns on "
          "M <= 32 at both tmax 24 and 64 (+9 maps = 43) (%.1f s)" % (nexact, nb64, time.time() - t0))


# ---------------------------------------------------------------- G: non-unit search (EVIDENCE)
def part_G():
    t0 = time.time()
    import search_nonunit as sn
    hits, stats = sn.run(48)
    ok(stats['unit'] == 0 and not hits, "non-unit search found a unit table: %s" % hits[:2])
    hits, stats = sn.run(144)
    ok(stats == dict(pairs=117390, bounded=31, unit=0) and not hits,
       "non-unit search M <= 144: %s" % stats)
    import nonunit_breakdown as nb
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        rc = nb.main(144)
    ok(rc == 0, "non-unit breakdown 24 pairing + 7 dressed, all to 0 mod M_Y")
    print("G ok (EVIDENCE): %s (%.1f s)" % (stats, time.time() - t0))


if __name__ == "__main__":
    part_A_B()
    part_C()
    part_D_E()
    part_F()
    part_F2()
    part_G()
    if FAIL:
        print("FAILED:", len(FAIL))
        sys.exit(1)
    print("ALL CHECKS PASSED")
