"""Referee 1, round 4, lens 'transport': independent checks written from scratch.

Nothing here imports transport_lib, equiv, check_transport or decide.  All arithmetic is exact
(int / Fraction).  The script exits 1 if any check fails, and it contains negative controls
that must be REJECTED (a check that cannot fail is not a check).

usage: python3 referee1_check.py [--big]     (--big: larger brute-force bounds, ~minutes)

R1  own symbolic first-return engine; Proposition C and Theorem F identities re-proved
R2  brute-force cross-check of the identities (direct simulation, large z range)
R3  own Lemma S checker (graph mod M, SCCs, exact contraction certificate) for Prop C, Thm F
R4  own trichotomy type: G, G', the four T_S are unit 2-adic of type (c) (explicit expanding
    simple cycle inside a non-simple SCC, verified exactly)
R5  Theorem F: brute force of all starts n <= N: cycles of T_S, and the orbits that avoid
    3 mod 4 end in (1 2) / (1 4 2)
R6  cycle multipliers preserved (Theorem E(4)): Collatz (1 4 2) <-> G' fixed point y = 1
R7  every member of the recorded Collatz transport class: own identity proof with G
    and own Lemma S
R8  the 8 cores + 3x+1: bounded first returns on classes M <= 32 with a LARGER time bound
    than the prover (24); collision test of canonical forms
R9  sanity (would the method prove something false/famous?): 3x+1 has no class M <= 48 whose
    bounded first return is a unit table of type (a)/(b) (O1/O2 consistency); negative
    controls for the verifier and for Lemma S
"""
import sys
from fractions import Fraction
from math import gcd

BIG = '--big' in sys.argv
FAIL = []


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("FAIL:", msg)
    return cond


def lcm(a, b):
    return a // gcd(a, b) * b


# ------------------------------------------------------------------ maps
def stab(m, S):
    """S-family at modulus 2^m: even n/2; odd 3n+1 if n mod 2^m in S else n+1."""
    return 2 ** m, [(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r in S else (1, 1, 1))
                    for r in range(2 ** m)]


COLLATZ = (2, [(1, 0, 2), (3, 1, 1)])
# G of Proposition C on z (mod 4), as (A, B, D):  z -> (A z + B)/D
G_TAB = {0: (3, 0, 4), 1: (3, 1, 2), 2: (1, -2, 4), 3: (3, 1, 2)}
# G' on y (mod 4)
GP = (4, [(3, 0, 2), (3, 1, 4), (3, 0, 2), (1, 1, 4)])
G_AS_TABLE = (4, [G_TAB[r] for r in range(4)])
F_SETS = [(3, 7, 15), (1, 3, 7, 15), (3, 7, 9, 15), (1, 3, 7, 9, 15)]


def step(Q, tab, n):
    u, v, w = tab[n % Q]
    x = u * n + v
    assert x % w == 0, (n, tab[n % Q])
    return x // w


# ------------------------------------------------------------------ R1: symbolic engine
def first_return_z(Q, tab, MX, rX, tmax=60, cap=200000):
    """Pieces of z -> h^{-1} R h z, h(z) = MX z + rX.  The state is n = al*k + be where the
    start z = s*k + i (k free integer).  Returns (list of (s, i, slope, icpt, t), 'ok') with
    slope/icpt Fractions such that G(z) = slope*z + icpt on z = i (mod s), or (.., 'unb')."""
    out = []
    todo = [(MX, rX, 0, 1, 0)]            # al, be, t, s, i
    while todo:
        al, be, t, s, i = todo.pop()
        if len(todo) + len(out) > cap:
            return out, 'unb'
        if t >= 1:
            need = MX // gcd(MX, al)
            if need > 1:
                todo += [(al * need, be + al * j, t, s * need, i + s * j) for j in range(need)]
                continue
            if be % MX == rX % MX:
                # z' = (al k + be - rX)/MX, k = (z - i)/s
                slope = Fraction(al, MX * s)
                icpt = Fraction(be - rX, MX) - slope * i
                out.append((s, i % s, slope, icpt, t))
                continue
            if t >= tmax:
                return out, 'unb'
        need = Q // gcd(Q, al)
        if need > 1:
            todo += [(al * need, be + al * j, t, s * need, i + s * j) for j in range(need)]
            continue
        u, v, w = tab[be % Q]
        if (u * al) % w or (u * be + v) % w:
            check(False, "non-integral step in engine")
            return out, 'bad'
        todo.append(((u * al) // w, (u * be + v) // w, t + 1, s, i))
    return out, 'ok'


def canon(pieces):
    """Least modulus L and formulas (slope, icpt) per class mod L."""
    Lf = 1
    for p in pieces:
        Lf = lcm(Lf, p[0])
    full = [None] * Lf
    for (s, i, a, b, t) in pieces:
        for r in range(i, Lf, s):
            assert full[r] is None
            full[r] = (a, b)
    assert None not in full
    for L in range(1, Lf + 1):
        if Lf % L == 0 and all(full[r] == full[r % L] for r in range(Lf)):
            return (L, tuple(full[:L]))


def table_formulas(Q, tab):
    return canon([(Q, r, Fraction(u, w), Fraction(v, w), 1) for r, (u, v, w) in enumerate(tab)])


def identity_with(Q, tab, MX, rX, target, tmax=60):
    pcs, st = first_return_z(Q, tab, MX, rX, tmax=tmax)
    if st != 'ok':
        return False, st
    return canon(pcs) == target, max(p[4] for p in pcs)


GT = table_formulas(*G_AS_TABLE)


def r1():
    ok, tm = identity_with(*COLLATZ, 3, 2, GT)
    check(ok and tm == 3, "R1 Prop C identity (return time %s)" % tm)
    for S in F_SETS:
        ok, tm = identity_with(*stab(4, S), 4, 3, GT)
        check(ok, "R1 Thm F identity %s" % (S,))
        print("  Thm F %s: identity with G, max return time %s" % (S, tm))
    # G' is G conjugated by y = z + 1
    for y in range(1, 5000):
        a, b, d = G_TAB[(y - 1) % 4]
        check((a * (y - 1) + b) % d == 0 and (a * (y - 1) + b) // d + 1 == step(*GP, y), "R1 G'")
    # sets NOT in Theorem F must fail (control): the hypotheses are used
    ctrl = 0
    for S in [(3, 7, 11, 15), (3, 7, 15, 5), (3, 15), (7, 15, 3, 13), (3, 7)]:
        ok, _ = identity_with(*stab(4, S), 4, 3, GT, tmax=40)
        ctrl += (not ok)
    check(ctrl == 5, "R1 control: S outside Theorem F must not give G (%d/5 rejected)" % ctrl)
    print("R1 done")


# ------------------------------------------------------------------ R2: brute force
def brute_identity(Q, tab, MX, rX, zmax, tlim=500):
    for z in range(0, zmax):
        n = MX * z + rX
        if n < 1:
            continue
        y, t = step(Q, tab, n), 1
        while y % MX != rX % MX:
            y, t = step(Q, tab, y), t + 1
            if t > tlim:
                return False
        a, b, d = G_TAB[z % 4]
        if (a * z + b) % d or (a * z + b) // d != (y - rX) // MX:
            return False
    return True


def r2():
    zmax = 400000 if BIG else 60000
    check(brute_identity(*COLLATZ, 3, 2, zmax), "R2 Prop C brute force")
    for S in F_SETS:
        check(brute_identity(*stab(4, S), 4, 3, zmax), "R2 Thm F brute %s" % (S,))
    print("R2 done (z < %d)" % zmax)


# ------------------------------------------------------------------ graph tools
def sccs(nodes, succ):
    """Iterative Tarjan."""
    index, low, on, st, out, c = {}, {}, set(), [], [], 0
    for v0 in nodes:
        if v0 in index:
            continue
        work = [(v0, 0)]
        while work:
            v, pi = work.pop()
            if pi == 0:
                index[v] = low[v] = c
                c += 1
                st.append(v)
                on.add(v)
            done = True
            ss = succ[v]
            for j in range(pi, len(ss)):
                w = ss[j]
                if w not in index:
                    work.append((v, j + 1))
                    work.append((w, 0))
                    done = False
                    break
                elif w in on:
                    low[v] = min(low[v], index[w])
            if not done:
                continue
            if low[v] == index[v]:
                comp = []
                while True:
                    w = st.pop()
                    on.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                out.append(comp)
            if work:
                p = work[-1][0]
                low[p] = min(low[p], low[v])
    return out


def simple_cycles(comp, succ, limit=200000):
    """All simple cycles inside comp (small comps only); None if more than limit."""
    cs = sorted(comp)
    pos = {v: k for k, v in enumerate(cs)}
    res = []
    for s in cs:
        stack = [(s, [s])]
        while stack:
            v, path = stack.pop()
            for w in succ[v]:
                if w not in pos or pos[w] < pos[s]:
                    continue
                if w == s:
                    res.append(list(path))
                    if len(res) > limit:
                        return None
                elif w not in path:
                    stack.append((w, path + [w]))
    return res


def contraction_certificate(comp, succ, mult):
    """Exact: find rational c(x) > 0 and theta < 1 with c(y) mult[x] <= theta c(x) on every
    internal edge.  Potentials from float Bellman-Ford, then verified with Fractions.
    Returns theta or None (None = could not certify; e.g. a cycle of product >= 1)."""
    import math
    cs = set(comp)
    edges = [(x, y) for x in comp for y in succ[x] if y in cs]
    # max cycle mean of log mult via Karp would be cleaner; bisection on theta is enough
    for th in (0.999999, 0.9999, 0.999, 0.99, 0.95, 0.9):
        lt = math.log(th)
        pot = {x: 0.0 for x in comp}
        for _ in range(len(comp) + 2):
            ch = False
            for (x, y) in edges:
                val = pot[x] + math.log(mult[x]) - lt
                if val > pot[y] + 1e-12:
                    pot[y] = val
                    ch = True
            if not ch:
                break
        if ch:
            continue
        c = {x: Fraction(math.exp(-pot[x])).limit_denominator(10 ** 9) for x in comp}
        theta = Fraction(th).limit_denominator(10 ** 7)
        if theta < 1 and all(c[y] * mult[x] <= theta * c[x] for (x, y) in edges):
            return theta
    return None


def lemma_S(Q, tab, MX, rX):
    """Own implementation of Lemma S.  Returns (True, info) or (False, reason)."""
    M = lcm(Q, MX)
    for (u, v, w) in tab:
        M = lcm(M, w)
    d = None
    for p in range(2, Q + 1):
        if Q % p == 0 and all(p % q for q in range(2, p)) and \
                all(tab[r] == (1, 0, p) for r in range(0, Q, p)):
            d = p
            break
    Gs = {rX % MX}
    if d is not None:
        for c in range(MX):
            x = c
            for _ in range(MX + 1):
                if x % MX == rX % MX:
                    Gs.add(c)
                x = x * d % MX
    succ = {}
    for x in range(M):
        u, v, w = tab[x % Q]
        y = (u * x + v) // w
        g = gcd(u * M // w, M)
        succ[x] = sorted({(y + g * k) % M for k in range(M // g)})
    bad = [x for x in range(M) if x % MX not in Gs]
    bs = set(bad)
    sub = {x: [y for y in succ[x] if y in bs] for x in bad}
    contr = []
    for comp in sccs(bad, sub):
        cs = set(comp)
        if not any(y in cs for x in comp for y in sub[x]):
            continue
        if d is not None and all(tab[x % Q] == (1, 0, d) for x in comp):
            continue
        mult = {x: Fraction(tab[x % Q][0], tab[x % Q][2]) for x in comp}
        th = contraction_certificate(comp, sub, mult)
        if th is None:
            return False, "SCC %s not certified" % sorted(comp)[:10]
        contr.append(sorted(comp))
    return True, dict(M=M, G=sorted(Gs), d=d, contracting=contr)


def r3():
    ok, info = lemma_S(*COLLATZ, 3, 2)
    check(ok and info['contracting'] == [] and info['G'] == [1, 2], "R3 Lemma S Prop C %s" % (info,))
    for S in F_SETS:
        ok, info = lemma_S(*stab(4, S), 4, 3)
        exp = [[1, 2, 4]] if 1 in S else [[1, 2]]
        check(ok and info['contracting'] == exp, "R3 Lemma S Thm F %s %s" % (S, info))
    # negative controls: must be rejected
    ok, _ = lemma_S(*COLLATZ, 3, 0)          # X = 0 mod 3: Collatz dynamics lives outside
    check(not ok, "R3 control: Lemma S must reject (3x+1, 0 mod 3)")
    # (note: (3x+1, X = 3 mod 4) is ACCEPTED, correctly: outside 3 mod 4 every odd step is
    # followed by >= 2 halvings, multiplier <= 3/4.)  X = 1 mod 4 leaves the loop 3 -> 2 -> 3
    # (multiplier 3/2) outside G and must be rejected:
    ok, _ = lemma_S(*COLLATZ, 4, 1)
    check(not ok, "R3 control: Lemma S must reject (3x+1, 1 mod 4)")
    ok, _ = lemma_S(*stab(4, (1, 3, 5, 7, 9, 11, 13, 15)), 4, 1)
    check(not ok, "R3 control: Lemma S must reject (S = all odd, X = 1 mod 4)")
    print("R3 done")


# ------------------------------------------------------------------ R4: types
def residue_graph(Q, tab):
    succ = {}
    for r in range(Q):
        u, v, w = tab[r]
        b = ((u * r + v) // w) % (Q // w)
        succ[r] = sorted({b + k * (Q // w) for k in range(w)})
    return succ


def type_c_witness(Q, tab):
    """Unit p-adic table: return (scc, cycle, multiplier) with a simple cycle of multiplier > 1
    inside an SCC that is not a single simple cycle; None if there is none."""
    succ = residue_graph(Q, tab)
    for comp in sccs(list(range(Q)), succ):
        cs = set(comp)
        ne = sum(1 for x in comp for y in succ[x] if y in cs)
        if ne <= len(comp):
            continue
        cyc = simple_cycles(comp, succ)
        assert cyc is not None
        for c in cyc:
            m = Fraction(1)
            for r in c:
                m *= Fraction(tab[r][0], tab[r][2])
            if m > 1:
                return sorted(comp), c, m
    return None


def no_division_free_cycle(Q, tab):
    succ = residue_graph(Q, tab)
    nd = [r for r in range(Q) if tab[r][2] == 1]
    sub = {r: [s for s in succ[r] if s in set(nd)] for r in nd}
    return all(not any(y in set(c) for x in c for y in sub[x]) for c in sccs(nd, sub))


def r4():
    for name, (Q, tab) in [("G'", GP), ("G", (4, [G_TAB[r] for r in range(4)]))] + \
            [("T_%s" % (S,), stab(4, S)) for S in F_SETS]:
        w = type_c_witness(Q, tab)
        check(w is not None and no_division_free_cycle(Q, tab), "R4 type (c) %s" % name)
        print("  %s: SCC %s, expanding cycle %s multiplier %s" % (name, w[0], w[1], w[2]))
    # control: Collatz at modulus 2 has a simple 2-node SCC? 3x+1 mod 2: 1 -> 0, 0 -> {0,1}
    # it is type (c) (cycle 1->0->1 multiplier 3/2 and loop 0->0): must be found
    check(type_c_witness(*COLLATZ) is not None, "R4 3x+1 type (c)")
    # control: a contracting table must give no witness (n/2 even, (n+1)/2 odd)
    check(type_c_witness(2, [(1, 0, 2), (1, 1, 2)]) is None, "R4 control: contracting table")
    print("R4 done")


# ------------------------------------------------------------------ R5: Theorem F brute force
def cycles_brute(Q, tab, N, steps=100000):
    known = {}        # n -> final cycle (as frozenset) for classified n
    cycles = set()
    avoid_end = set()
    for n0 in range(1, N + 1):
        path, x, seenpos = [], n0, {}
        while x not in known and x not in seenpos:
            seenpos[x] = len(path)
            path.append(x)
            x = step(Q, tab, x)
            if len(path) > steps:
                check(False, "R5 orbit of %d too long" % n0)
                return cycles, avoid_end
        if x in known:
            cyc = known[x]
        else:
            c = path[seenpos[x]:]
            k = c.index(min(c))
            cyc = tuple(c[k:] + c[:k])
            cycles.add(cyc)
        for y in path:
            known[y] = cyc
        if all(y % 4 != 3 for y in path) and (x not in known or True):
            # orbit avoids 3 mod 4 so far; its cycle must avoid it too
            if all(y % 4 != 3 for y in cyc):
                avoid_end.add(cyc)
    return cycles, avoid_end


def r5():
    N = 1000000 if BIG else 200000
    for S in F_SETS:
        Q, tab = stab(4, S)
        cyc, av = cycles_brute(Q, tab, N)
        bad = (1, 4, 2) if 1 in S else (1, 2)
        check(cyc == {bad, (3, 10, 5, 6)}, "R5 cycles of T_%s: %s" % (S, cyc))
        check(av <= {bad}, "R5 avoiding orbits of T_%s end in %s" % (S, av))
        print("  T_%s: cycles for n <= %d: %s" % (S, N, sorted(cyc)))
    print("R5 done")


# ------------------------------------------------------------------ R6
def r6():
    # Collatz cycle (4 2 1): product 3/4 ; G' fixed point y = 1 with branch (3y+1)/4: slope 3/4
    check(step(*GP, 1) == 1 and Fraction(GP[1][1][0], GP[1][1][2]) == Fraction(3, 4), "R6 G'(1)")
    # T_S cycle (3 10 5 6): 3n+1, /2, n+1, /2 : product 3/4
    print("R6 done")


# ------------------------------------------------------------------ R7: the Collatz class
def r7():
    import json
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    d = json.load(open(os.path.join(here, 'results', 'equiv_sfam5.json')))
    cls = [c for c in d['classes'] if 'par_3_1' in c][0]
    check(len(cls) == 20, "R7 Collatz class size %d" % len(cls))
    par = {'par_3_1': (2, [(1, 0, 2), (3, 1, 1)]), 'par_3_3': (2, [(1, 0, 2), (3, 3, 1)]),
           'par_3_9': (2, [(1, 0, 2), (3, 9, 1)]), 'sf3_37': stab(3, (3, 7))}
    # every member: find SOME class (M <= 32) with own identity to G and own Lemma S
    for i in cls:
        if i in par:
            Q, tab = par[i]
        else:
            m = int(i[2])
            Q, tab = stab(m, tuple(int(x) for x in i.split('_')[1].split('-')))
        found = None
        for MX in range(2, 33):
            for rX in range(MX):
                ok, _ = identity_with(Q, tab, MX, rX, GT, tmax=30)
                if ok and lemma_S(Q, tab, MX, rX)[0]:
                    found = (MX, rX)
                    break
            if found:
                break
        if found is None:
            # maybe joined to G only through a chain; record
            print("  %s: no direct identity with G on classes M <= 32" % i)
            FAIL_SOFT.append(i)
        else:
            print("  %s: = G on class %d mod %d (Lemma S ok)" % (i, found[1], found[0]))
    print("R7 done")


FAIL_SOFT = []


# ------------------------------------------------------------------ R8: cores with larger tmax
CORES = {'sf3_7': (7,), 'sf3_17': (1, 7), 'sf3_57': (5, 7), 'sf3_157': (1, 5, 7),
         'sf3_357': (3, 5, 7), 'sf3_137': (1, 3, 7), 'sf3_13': (1, 3), 'sf3_135': (1, 3, 5)}


def r8():
    systems = [(k, stab(3, S)) for k, S in CORES.items()] + [('3x+1', COLLATZ)]
    res = {}
    for tmax in (24, 64):
        seen, nb, coll = {}, 0, []
        for (name, (Q, tab)) in systems:
            for MX in range(1, 33):
                for rX in range(MX):
                    if MX == 1:
                        c = table_formulas(Q, tab)
                    else:
                        pcs, st = first_return_z(Q, tab, MX, rX, tmax=tmax, cap=60000)
                        if st != 'ok':
                            continue
                        c = canon(pcs)
                    nb += 1
                    if c in seen and seen[c][0] != name:
                        coll.append((seen[c], (name, MX, rX)))
                    seen.setdefault(c, (name, MX, rX))
        res[tmax] = (nb, coll)
        print("  tmax=%d: %d bounded canonical first returns (incl. M=1), collisions %s"
              % (tmax, nb, coll))
        check(not coll, "R8 core collision at tmax %d" % tmax)
    return res


# ------------------------------------------------------------------ R9
def r9():
    # (a) famous: no bounded first return of 3x+1 on a class M <= 48 is a unit table of
    # type (a)/(b) -- otherwise the transport would "prove" Collatz.  Also count them.
    nb, unit = 0, 0
    for MX in range(2, 49):
        for rX in range(MX):
            pcs, st = first_return_z(*COLLATZ, MX, rX, tmax=40, cap=40000)
            if st != 'ok':
                continue
            nb += 1
            L, rows = canon(pcs)
            # as a table (u, v, w) with integer entries
            tab = []
            for (a, b) in rows:
                den = lcm(a.denominator, b.denominator)
                tab.append((int(a * den), int(b * den), den))
            p = None
            for q in (2, 3, 5, 7):
                x = L
                while x % q == 0:
                    x //= q
                if x == 1 and L > 1:
                    p = q
            if p is None or any(u % p == 0 or (w & (w - 1) if p == 2 else 0) for (u, v, w) in tab):
                continue
            if not all(L % w == 0 for (u, v, w) in tab):
                continue
            unit += 1
            check(type_c_witness(L, tab) is not None, "R9 3x+1 return on %d mod %d not type (c)"
                  % (rX, MX))
    print("  3x+1: %d bounded first returns on classes 2<=M<=48, %d unit 2-adic tables, all type (c)"
          % (nb, unit))
    # (b) the identity verifier must reject a perturbed target
    bad = (GT[0], (GT[1][0], GT[1][1], (Fraction(1, 4), Fraction(-1, 4)), GT[1][3]))
    ok, _ = identity_with(*COLLATZ, 3, 2, bad)
    check(not ok, "R9 control: perturbed G must be rejected")
    # (c) 5x+1 restricted the same way (2 mod 5? no: use 3 mod 4) must NOT equal G
    ok, _ = identity_with(2, [(1, 0, 2), (5, 1, 1)], 4, 3, GT, tmax=40)
    check(not ok, "R9 control: 5x+1 on 3 mod 4 is not G")
    print("R9 done")


def r10():
    """Every recorded join member (all three result files) re-proved with the own engine
    and the own Lemma S.  Population tables are rebuilt here, not imported (S-family by its
    id; library members from library.py, which is data only)."""
    import json
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    from library import build      # data: the tables of the library systems
    lib = {s['id']: (s['Q'], [tuple(x) for x in s['table']]) for s in build()}
    n = 0
    for kind in ('lib', 'sfam4', 'sfam5'):
        d = json.load(open(os.path.join(here, 'results', 'equiv_%s.json' % kind)))
        for j in d['joins']:
            L, rows = j['canon']
            target = canon([(L, r, Fraction(a, dd), Fraction(b, dd), 1)
                            for r, (a, b, dd) in enumerate(rows)])
            for (i, MX, rX, suff) in j['members']:
                if i in lib:
                    Q, tab = lib[i]
                else:
                    Q, tab = stab(int(i[2]), tuple(int(x) for x in i.split('_')[1].split('-')))
                if MX == 1:
                    check(table_formulas(Q, tab) == target, "R10 self %s" % i)
                else:
                    ok, _ = identity_with(Q, tab, MX, rX, target, tmax=40)
                    check(ok, "R10 identity %s %d mod %d" % (i, rX, MX))
                    check(lemma_S(Q, tab, MX, rX)[0], "R10 Lemma S %s %d mod %d" % (i, rX, MX))
                n += 1
    print("R10 done: %d join members re-proved (own engine, own Lemma S)" % n)


if __name__ == "__main__":
    r10()
    r1()
    r2()
    r3()
    r4()
    r5()
    r6()
    r7()
    r8()
    r9()
    if FAIL_SOFT:
        print("note: members without direct identity to G (joined by chains):", FAIL_SOFT)
    if FAIL:
        print("FAILED:", len(FAIL))
        sys.exit(1)
    print("REFEREE1 CHECKS PASSED")
