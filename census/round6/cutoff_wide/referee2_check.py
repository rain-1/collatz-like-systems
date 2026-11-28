"""Referee 2: independent check for round6/cutoff_wide.

Written from scratch.  It imports nothing from the prover's files (cwlib,
check_*.py, count_nondesc.py) or from referee1_check.py.  Exact integers and
Fractions wherever a claim is exact; the entropy exponents are floats and only
compared against the stated EVIDENCE values with a tolerance.

Sections
  A  systems from the census rules; cylinder graph G_m; Markov property (M)
     by exhaustive lifting; standing hypothesis; SCC types (trichotomy.md)
  B  Theorem P witnesses (own construction): rotation, re-entry, U, V, prefix
     slopes, realization of random {U,V}^n words by integers via lifting and
     direct iteration, disjointness; dimension bound s; item 4 count in
     random intervals (brute force over integers)
  C  exact non-descending counts N(E): DP against direct integer iteration,
     and long-range fits against the stated H table (EVIDENCE)
  D  Theorem W: whole-prefix identity on actual integer orbits of rigid
     two-piece schedules with a jump (3x+1, m3_b, core13), pairing identity
     with exceptions, |1 - gamma| lower bound; Lemma R exception counts on
     random step functions (exact rational phases)
  E  expanding integer cycles of 3x-1 and 3x+1 satisfy (H0)-(H4) from bounded
     starts (withdrawn claim "cycles fail (H2)")
  F  Proposition B (mb_s3_27): skew product, classes s = 2 mod 3, entry
     words for s = 0, 1 mod 3, the code U, V, never-blocked counts
  G  numbers quoted in the README (kappa values, 0.0366)

Run: python3 referee2_check.py     exits 0 iff every assertion holds.
"""
import sys
import random
from fractions import Fraction as Fr
from math import log, ceil, floor
from collections import deque

random.seed(20261128)
FAILS = []
RIGID_RUNS = []


def check(name, cond, info=''):
    if not cond:
        FAILS.append(name)
        print('FAIL:', name, info)
    return cond


# ------------------------------------------------------------------ A systems
def mk(p, m, rule, l):
    """rule(r) -> (u, v, e): n = r (mod p^m) -> (u n + v)/p^e."""
    br = [rule(r) for r in range(p ** m)]
    for r, (u, v, e) in enumerate(br):
        assert u % p != 0
        # exactness on the whole class
        for z in range(p ** (e + 1)):
            assert (u * (r + p ** m * z) + v) % p ** e == 0
    return dict(p=p, m=m, br=br, l=l)


def terras(a, b):
    return lambda r: (1, 0, 1) if r % 2 == 0 else (a, b, 1)


def sfam(S):
    def rule(r):
        if r % 2 == 0:
            return (1, 0, 1)
        return (3, 1, 0) if r in S else (1, 1, 0)
    return rule


SYS = {
    '3x+1': mk(2, 1, terras(3, 1), 3),
    '3x-1': mk(2, 1, terras(3, -1), 3),
    '3x+5': mk(2, 1, terras(3, 5), 3),
    '5x+1': mk(2, 1, terras(5, 1), 5),
    'K7': mk(2, 3, sfam({7}), 3),
    'core13': mk(2, 3, sfam({1, 3}), 3),
    'core135': mk(2, 3, sfam({1, 3, 5}), 3),
    'core57': mk(2, 3, sfam({5, 7}), 3),
    'core157': mk(2, 3, sfam({1, 5, 7}), 3),
    'core357': mk(2, 3, sfam({3, 5, 7}), 3),
    'core17': mk(2, 3, sfam({1, 7}), 3),
    'coreW': mk(2, 3, sfam({1, 3, 7}), 3),
    # CLS-049: even n/2; 1 mod 4 -> 5n+3; 3 mod 4 -> n+3
    'split5_3': mk(2, 2, lambda r: (1, 0, 1) if r % 2 == 0 else ((5, 3, 0) if r == 1 else (1, 3, 0)), 5),
    # CLS-048: even n/2; 1 mod 4 -> 5n+1; 3 mod 4 -> n+1
    'split5_1': mk(2, 2, lambda r: (1, 0, 1) if r % 2 == 0 else ((5, 1, 0) if r == 1 else (1, 1, 0)), 5),
    # CLS-004: 3|n -> n/3; 1 mod 3 -> (4n-1)/3; 2 mod 3 -> (4n+1)/3
    'm3_b': mk(3, 1, lambda r: [(1, 0, 1), (4, -1, 1), (4, 1, 1)][r], 2),
}


def T(sy, n):
    u, v, e = sy['br'][n % sy['p'] ** sy['m']]
    x = u * n + v
    assert x % sy['p'] ** e == 0
    return x // sy['p'] ** e


def lexp(u, l):
    a = 0
    while u % l == 0:
        u //= l
        a += 1
    assert u == 1
    return a


def G(sy):
    """cylinder graph at K = m: node r -> list of (s, slope)."""
    p, m, br = sy['p'], sy['m'], sy['br']
    M = p ** m
    g = {}
    for r in range(M):
        u, v, e = br[r]
        outs = []
        for j in range(p ** e):
            x = u * (r + M * j) + v
            outs.append(((x // p ** e) % M, Fr(u, p ** e)))
        g[r] = outs
    return g


def markov_check(sy, g, depth=4):
    """(M): every walk of length <= depth of G is followed by exactly one class
    mod p^(m + divisions); tested by enumerating all residues."""
    p, m = sy['p'], sy['m']
    ok = True
    for L_ in range(1, depth + 1):
        # count walks by enumerating residues mod p^(m + e_max*L)
        emax = max(e for (_, _, e) in sy['br'])
        Mod = p ** (m + emax * L_)
        seen = {}
        for r in range(Mod):
            n = r + Mod * 10 ** 6
            w = [n % p ** m]
            divs = 0
            for _ in range(L_):
                divs += sy['br'][n % p ** m][2]
                n = T(sy, n)
                w.append(n % p ** m)
            seen.setdefault(tuple(w), set()).add((r % p ** (m + divs), divs))
        for w, cls in seen.items():
            divs = {d for (_, d) in cls}
            ok &= len(divs) == 1 and len({c for (c, _) in cls}) == 1
        # every walk of G of length L_ is realized
        walks = [[r] for r in g]
        for _ in range(L_):
            walks = [w + [s] for w in walks for (s, _) in g[w[-1]]]
        ok &= len({tuple(w) for w in walks}) == len(seen)
    return ok


def sccs(g):
    idx, low, on, st, out, c = {}, {}, set(), [], [], [0]

    def strong(v):
        idx[v] = low[v] = c[0]
        c[0] += 1
        st.append(v)
        on.add(v)
        for (w, _) in g[v]:
            if w not in idx:
                strong(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = st.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            out.append(comp)
    for v in g:
        if v not in idx:
            strong(v)
    return out


def simple_cycles(g, comp):
    """all simple cycles inside comp, as edge lists [(r, s, slope)], with
    parallel edges distinguished."""
    comp = set(comp)
    res = []
    nodes = sorted(comp)
    for s0 in nodes:
        stack = [(s0, [], {s0})]
        while stack:
            r, path, vis = stack.pop()
            for k, (t, q) in enumerate(g[r]):
                if t not in comp or t < s0:
                    continue
                e = (r, t, k, q)
                if t == s0:
                    res.append(path + [e])
                elif t not in vis:
                    stack.append((t, path + [e], vis | {t}))
    return res


def prod(xs):
    out = Fr(1)
    for x in xs:
        out *= x
    return out


def scc_types(g):
    types = []
    for comp in sccs(g):
        cs = set(comp)
        internal = [(r, k) for r in comp for k, (t, _) in enumerate(g[r]) if t in cs]
        if not internal:
            continue
        cyc = simple_cycles(g, comp)
        sl = [prod(e[3] for e in c) for c in cyc]
        assert all(s != 1 for s in sl)
        if len(cyc) == 1:
            types.append('b' if sl[0] > 1 else 'a')
        elif any(s > 1 for s in sl):
            types.append('c')
        else:
            types.append('a')
    return types


def standing(sy, g):
    """no division-free cycle: the subgraph of e = 0 edges is acyclic."""
    br, p, m = sy['br'], sy['p'], sy['m']
    sub = {r: ([(t, q) for (t, q) in g[r]] if br[r][2] == 0 else []) for r in g}
    for comp in sccs(sub):
        cs = set(comp)
        if any(t in cs for r in comp for (t, _) in sub[r]):
            return False
    return True


# ------------------------------------------------------- B Theorem P witness
def lift_walk(sy, nodes):
    """nodes = r_0, ..., r_L (residues mod p^m).  Returns (rho, Mod, divs): the
    class of integers whose first L iterates visit these nodes, found by
    p-adic lifting with an exhaustive uniqueness test at each step."""
    p, m = sy['p'], sy['m']
    M = p ** m
    rho, Mod = nodes[0] % M, M
    divs = 0
    for j in range(1, len(nodes)):
        e = sy['br'][nodes[j - 1]][2]
        hits = []
        for t in range(p ** e):
            n = rho + Mod * t
            x = n
            for k in range(j):
                x = T(sy, x)
            if x % M == nodes[j]:
                hits.append(n)
        assert len(hits) == 1, (len(hits), j)
        rho, Mod = hits[0], Mod * p ** e
        divs += e
    return rho, Mod, divs


def follows(sy, n, nodes):
    M = sy['p'] ** sy['m']
    for j, r in enumerate(nodes):
        if n % M != r:
            return False
        if j < len(nodes) - 1:
            n = T(sy, n)
    return True


def slopes_of(sy, walk):
    """prefix slopes along a node walk r_0..r_{L-1} (the L steps)."""
    s, out = Fr(1), []
    for r in walk:
        u, v, e = sy['br'][r]
        s *= Fr(u, sy['p'] ** e)
        out.append(s)
    return out


def own_witness(sy, g):
    """Shortest expanding simple cycle C (largest slope on ties), cycle-lemma
    rotation, shortest closed walk at r_0 through an edge off C, U and V."""
    best = None
    for comp in sccs(g):
        for c in simple_cycles(g, comp):
            s = prod(e[3] for e in c)
            if s > 1 and (best is None or len(c) < len(best[0]) or
                          (len(c) == len(best[0]) and s > best[1])):
                best = (c, s)
    c, lam = best
    L_ = len(c)
    logs = [log(float(e[3])) for e in c]
    # rotation: start after the last minimum of the partial sums S_0..S_{L-1}
    S = [0.0]
    for x in logs[:-1]:
        S.append(S[-1] + x)
    mn = min(S)
    start = max(i for i, x in enumerate(S) if abs(x - mn) < 1e-12)
    c = c[start:] + c[:start]
    Cn = [e[0] for e in c]
    r0 = Cn[0]
    assert all(x > 1 for x in slopes_of(sy, Cn))
    cedges = {(e[0], e[2]) for e in c}
    # BFS over (node, used_off_edge) to return to r0 having used an edge off C
    dq = deque([(r0, False, [])])
    seen = {(r0, False)}
    W = None
    while dq:
        r, used, path = dq.popleft()
        for k, (t, _) in enumerate(g[r]):
            u2 = used or ((r, k) not in cedges)
            if t == r0 and u2:
                W = path + [r]
                break
            if (t, u2) not in seen:
                seen.add((t, u2))
                dq.append((t, u2, path + [r]))
        if W:
            break
    Wp = W * L_
    mm = len(Wp) // L_
    D = 0
    while True:
        U, V = Cn * D + Wp, Cn * (D + mm)
        if all(x > 1 for x in slopes_of(sy, U)) and all(x > 1 for x in slopes_of(sy, V)):
            break
        D += 1
    return dict(C=Cn, lam=lam, W=W, D=D, U=U, V=V, r0=r0)


def divs_of(sy, walk):
    return sum(sy['br'][r][2] for r in walk)


def dim_s(p, a, b):
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if p ** (-mid * a) + p ** (-mid * b) > 1:
            lo = mid
        else:
            hi = mid
    return lo


def section_A_B():
    print('== A/B: SCC types, (M), Theorem P witnesses')
    print('%-9s %-6s %-5s %-4s %-4s %-5s %-9s %s' % ('system', 'types', '|C|', '|W|', 'D', '|U|', 'eU/eV', 's'))
    res = {}
    for nm, sy in SYS.items():
        g = G(sy)
        check(nm + ' standing hypothesis', standing(sy, g))
        check(nm + ' Markov property (M)', markov_check(sy, g, depth=3 if sy['m'] > 1 else 5))
        ty = scc_types(g)
        check(nm + ' has a type-(c) SCC', 'c' in ty, ty)
        wt = own_witness(sy, g)
        U, V, r0 = wt['U'], wt['V'], wt['r0']
        check(nm + ' U != V, equal length', U != V and len(U) == len(V))
        check(nm + ' U, V closed at r0', U[0] == r0 and V[0] == r0)
        # closedness: last node -> r0 is an edge
        for X in (U, V):
            seq = X + [r0]
            check(nm + ' walk is a walk of G', all(any(t == seq[i + 1] for (t, _) in g[seq[i]])
                                                   for i in range(len(X))))
        eU, eV = divs_of(sy, U), divs_of(sy, V)
        # random words: realized, prefix slopes > 1, disjoint classes
        cls = set()
        ok_real = ok_sl = True
        for n_bl in (1, 2, 3, 4):
            words = set()
            for _ in range(6):
                words.add(tuple(random.choice('UV') for _ in range(n_bl)))
            for wd in words:
                walk = []
                for ch in wd:
                    walk += U if ch == 'U' else V
                rho, Mod, dv = lift_walk(sy, walk + [r0])
                ok_real &= follows(sy, rho + Mod * 3, walk + [r0]) and follows(sy, rho - Mod * 5, walk + [r0])
                ok_sl &= all(x > 1 for x in slopes_of(sy, walk))
                cls.add((n_bl, wd, rho % Mod, Mod))
        check(nm + ' {U,V}^n realized by integers', ok_real)
        check(nm + ' {U,V}^n prefix slopes > 1', ok_sl)
        # disjointness: same-length words give different classes with same modulus? (classes mod
        # their own modulus must be pairwise disjoint: one residue of the other is not congruent)
        by = {}
        for (nb, wd, r, M) in cls:
            by.setdefault(nb, []).append((r, M))
        ok_dis = True
        for nb, lst in by.items():
            for i in range(len(lst)):
                for j in range(i + 1, len(lst)):
                    (r1, M1), (r2, M2) = lst[i], lst[j]
                    Mm = min(M1, M2)
                    ok_dis &= (r1 - r2) % Mm != 0
        check(nm + ' distinct words give disjoint classes', ok_dis)
        s = dim_s(sy['p'], eU, eV)
        res[nm] = (wt, eU, eV, s)
        print('%-9s %-6s %-5d %-4d %-4d %-5d %-9s %.5f' % (nm, ''.join(sorted(ty)), len(wt['C']), len(wt['W']),
                                                          wt['D'], len(U), '%d/%d' % (eU, eV), s))
    # item 4 by brute force: in random intervals of p^(m+E) integers, at least
    # 2^floor((E-1)/e*) integers keep all prefix slopes > 1 through E divisions
    for nm in ('3x+1', '5x+1', 'm3_b', 'split5_1', 'K7'):
        sy = SYS[nm]
        wt, eU, eV, s = res[nm]
        es = max(eU, eV)
        p, m, l = sy['p'], sy['m'], sy['l']
        for E in range(1, 9 if p == 3 else 13):
            Lint = p ** (m + E)
            a0 = random.randrange(-10 ** 9, 10 ** 9)
            cnt = 0
            for n in range(a0, a0 + Lint):
                x, sl, d, good = n, Fr(1), 0, True
                while d < E:
                    u, v, e = sy['br'][x % p ** m]
                    sl *= Fr(u, p ** e)
                    d += e
                    x = T(sy, x)
                    if sl <= 1:
                        good = False
                        break
                cnt += good
            check('%s item 4 E=%d' % (nm, E), cnt >= 2 ** ((E - 1) // es), (cnt, es))
    return res


# ------------------------------------------------------- C exact counts
def counts(sy, Emax):
    """N(E) = number of walks (from any node) reaching E divisions with every
    prefix slope >= 1 at every division.  State (node, a) per division depth."""
    p, m, l, br = sy['p'], sy['m'], sy['l'], sy['br']
    g = G(sy)
    amin = [0] * (Emax + 3)
    a = 0
    for d in range(Emax + 3):
        while l ** a < p ** d:
            a += 1
        amin[d] = a
    layers = {0: {}}
    for r in g:
        layers[0][(r, 0)] = layers[0].get((r, 0), 0) + 1
    N = [len(g)]
    for d in range(Emax):
        cur = layers.pop(d, {})
        stack = list(cur.items())
        while stack:
            (r, a), c = stack.pop()
            u, v, e = br[r]
            a2 = a + lexp(u, l)
            for (t, _) in g[r]:
                if e == 0:
                    stack.append(((t, a2), c))
                else:
                    d2 = d + e
                    if a2 < amin[d2]:
                        continue
                    lay = layers.setdefault(d2, {})
                    lay[(t, a2)] = lay.get((t, a2), 0) + c
        N.append(sum(layers.get(d + 1, {}).values()))
    return N


def brute_counts(sy, E):
    p, m, l = sy['p'], sy['m'], sy['l']
    Mod = p ** (m + E)
    cnt = 0
    for r in range(Mod):
        x, A, d, good = r + Mod * 777, 0, 0, True
        while d < E:
            u, v, e = sy['br'][x % p ** m]
            A += lexp(u, l)
            d += e
            x = T(sy, x)
            if e and l ** A < p ** d:
                good = False
                break
        cnt += good
    return cnt


STATED_H = {'3x+1': 0.9500, 'K7': 0.7491, 'core13': 0.4281, 'core135': 0.3593,
            'core57': 0.7193, 'core157': 0.774, 'core357': 0.788, 'core17': 0.790,
            'split5_3': 0.5807, 'split5_1': 0.9369, 'm3_b': 0.9648}


def section_C():
    print('== C: exact non-descending counts and H (EVIDENCE)')
    for nm in ('3x+1', 'core13', 'core135', 'split5_3', 'm3_b', 'K7'):
        sy = SYS[nm]
        Em = 11 if sy['p'] == 2 else 6
        N = counts(sy, Em)
        ok = all(N[E] == brute_counts(sy, E) for E in range(1, Em + 1))
        check(nm + ' DP = direct counts', ok)
    sample = ['core13', 'core135'] + random.sample([k for k in STATED_H if k not in ('core13', 'core135')], 5)
    for nm in sample:
        sy = SYS[nm]
        E2 = 1600
        N = counts(sy, E2)
        p = sy['p']
        fit = (log(N[E2]) - log(N[E2 // 2])) / ((E2 - E2 // 2) * log(p))
        H = STATED_H[nm]
        print('  %-9s stated H %.4f  own fit [%d,%d] %.4f' % (nm, H, E2 // 2, E2, fit))
        check(nm + ' H fit consistent', -0.008 < fit - H < 0.002, (fit, H))
    # the old core13/core135 values must be rejected by the same test
    for nm, old in (('core13', 0.4565), ('core135', 0.3755)):
        N = counts(SYS[nm], 1600)
        fit = (log(N[1600]) - log(N[800])) / (800 * log(2))
        check(nm + ' old value rejected', not (-0.008 < fit - old < 0.002))
    # 5x+1 and coreW: H = 1 (positive drift): fit close to 1
    for nm in ('5x+1', 'coreW'):
        N = counts(SYS[nm], 600)
        fit = (log(N[600]) - log(N[300])) / (300 * log(2))
        check(nm + ' H ~ 1', fit > 0.995, fit)


# ------------------------------------------------------- D Theorem W
def shifted(sy, walk, xs):
    """affine action of a node walk on y = n - x*: y -> lam y + c."""
    def act(x):
        for r in walk:
            u, v, e = sy['br'][r]
            x = (u * x + v) / Fr(sy['p'] ** e)
        return x
    lam = act(xs + 1) - act(xs)
    c = act(xs) - xs
    return lam, c


def periodic_point(sy, walk):
    A, B, Dd = Fr(1), Fr(0), Fr(1)
    x0 = Fr(0)
    # composed map x -> a x + b
    a, b = Fr(1), Fr(0)
    for r in walk:
        u, v, e = sy['br'][r]
        q = Fr(sy['p'] ** e)
        a, b = a * u / q, (b * u + v) / q
    return b / (1 - a)


def rigid_check(nm, cyc_nodes, exits, kap_fun, n_pieces=2, nblocks=40):
    """Rigid schedule: C^{k_1} X_{lambda_1} ... in two pieces with an arbitrary
    jump; checks the whole-prefix identity on the integer orbit and the
    pairing identity with exceptions, exactly."""
    sy = SYS[nm]
    p, l = sy['p'], sy['l']
    xs = periodic_point(sy, cyc_nodes)
    lamC, c0 = shifted(sy, cyc_nodes, xs)
    check(nm + ' C fixes x*', c0 == 0 and lamC > 1)
    acts = [shifted(sy, X, xs) for X in exits]
    mus = {a[0] for a in acts}
    check(nm + ' exits: equal slope, nonzero distinct labels', len(mus) == 1 and all(a[1] != 0 for a in acts)
          and len({a[1] for a in acts}) == len(acts))
    mu = acts[0][0]
    kappa = -log(float(mu)) / log(float(lamC))
    # schedule: piece 1 rotation with t1, piece 2 rotation with t2 and jump
    t1, t2 = random.random(), random.random()
    jump = random.randint(5, 30)
    half = nblocks // 2
    Ks, labs = [0], []
    for i in range(1, nblocks + 1):
        t = t1 if i <= half else t2
        base = floor(kappa * i + t) + (jump if i > half else 0)
        ph = (kappa * i + t) % 1
        Ks.append(base + 1)
        labs.append(0 if ph < 0.5 or len(exits) == 1 else 1)
    ks = [Ks[i] - Ks[i - 1] for i in range(1, nblocks + 1)]
    if min(ks) < 0:
        RIGID_RUNS.append((nm, 'skipped'))
        return
    walk = []
    for i in range(nblocks):
        walk += cyc_nodes * ks[i] + exits[labs[i]]
    rho, Mod, dv = lift_walk(sy, walk + [cyc_nodes[0]])
    n = rho + Mod
    check(nm + ' rigid word followed', follows(sy, n, walk + [cyc_nodes[0]]))
    x = n
    for r in walk:
        x = T(sy, x)
    y0, yn = Fr(n) - xs, Fr(x) - xs
    # events, exactly as in theorem_W.md: tau_i = c_i / P_i where P_i is the
    # prefix slope after the event (exit block acts as y -> mu y + c)
    P, taus, data = Fr(1), [], []
    y = y0
    for i in range(nblocks):
        P *= lamC ** ks[i]
        y = lamC ** ks[i] * y
        lam_, c = acts[labs[i]]
        P *= lam_
        y = lam_ * y + c
        taus.append(c / P)
        data.append((labs[i], P))
    check(nm + ' shifted values match orbit', y == yn)
    check(nm + ' whole-prefix identity (1)', y0 + sum(taus) == yn / P)
    # tau_i = c p^{E'} / l^{A} with the prefix slope BEFORE the exit
    # pairing in piece 2 (indices half..nblocks-1, 0-based), Q = floor(n/4)
    I = list(range(half, nblocks))
    n_I = len(I)
    Q = n_I // 4
    q = min(range(1, Q + 1), key=lambda j: abs(kappa * j - round(kappa * j)))
    k = round(kappa * q)
    gamma = lamC ** k * mu ** q
    Xc = [i for i in I if i + q in I and not (Ks[i + q + 1] - Ks[i + 1] == k and labs[i + q] == labs[i])]
    ok = all(taus[i] == gamma * taus[i + q] for i in I if i + q in I and i not in Xc)
    check(nm + ' tau_i = gamma tau_{i+q} off exceptions', ok)
    u_, v_ = I[0], I[-1]
    S = sum(taus[i] for i in I)
    rhs = sum(taus[i] for i in range(v_ - q + 1, v_ + 1)) - gamma * sum(taus[i] for i in range(u_, u_ + q)) \
        + sum(taus[i] - gamma * taus[i + q] for i in Xc)
    check(nm + ' pairing identity', (1 - gamma) * S == rhs)
    # |1 - gamma| >= p^{-k_E} l^{-max(0,-k_A)}
    num, den = (1 - gamma).numerator, (1 - gamma).denominator
    dd = den
    for pr in (p, l):
        while dd % pr == 0:
            dd //= pr
    check(nm + ' 1 - gamma != 0, denominator an {p,l}-unit', num != 0 and dd == 1)
    RIGID_RUNS.append((nm, len(walk), q, k, len(Xc)))
    # (H2): every prefix slope at an exit >= 1 for this near-critical schedule?  report only
    return len(Xc)


def lemma_R_random(trials=400):
    """Exceptional indices of Lemma R with exact rational phases."""
    worst = 0
    for _ in range(trials):
        den = random.randint(10 ** 6, 10 ** 7)
        kappa = Fr(random.randint(den // 3, 5 * den), den)
        t = Fr(random.randint(0, 10 ** 6), 10 ** 6)
        J = random.randint(1, 4)
        B = 3
        cw = sorted(Fr(random.randint(0, 10 ** 5), 10 ** 5) for _ in range(J - 1)) if J > 1 else []
        cl = sorted(Fr(random.randint(0, 10 ** 5), 10 ** 5) for _ in range(J - 1)) if J > 1 else []
        wv = [random.randint(-B, B) for _ in range(J)]
        lv = [random.randint(0, 2) for _ in range(J)]

        def arc(cuts, x):
            k = 0
            while k < len(cuts) and x >= cuts[k]:
                k += 1
            return k  # left-closed arcs [c_k, c_{k+1})
        d = random.choice([5, 6, 8, 10, 13, 20])
        delta = Fr(1, d)
        nI = random.randint(2 * d, 400)
        i0 = random.randint(0, 50)

        def phase(i):
            x = kappa * i + t
            return x - (x.numerator // x.denominator)

        def K(i):
            x = kappa * i + t
            return (x.numerator // x.denominator) + wv[arc(cw, phase(i))]

        def lab(i):
            return lv[arc(cl, phase(i))]
        Q = int(delta * nI)
        q = min(range(1, Q + 1), key=lambda j: (abs(kappa * j - round(kappa * j)), j))
        k = round(kappa * q)
        idx = list(range(i0, i0 + nI))
        X = [i for i in idx if i + q <= idx[-1] and not (K(i + q) - K(i) == k and lab(i + q) == lab(i))]
        M = 2 * (2 * J + 1) * (Fr(1) / delta + 2)
        check('Lemma R total exceptions <= M(delta)', len(X) <= M, (len(X), M))
        # per window of Q consecutive indices at most 2J+1
        for w0 in range(0, nI, Q):
            win = set(idx[w0:w0 + Q])
            check('Lemma R per-window <= 2J+1', len([i for i in X if i in win]) <= 2 * J + 1)
        worst = max(worst, len(X))
    return worst


def section_D():
    print('== D: Theorem W identities and Lemma R')
    # 3x+1: C = odd node 1 (y -> 3/2 y around -1), exit X = node 0 (y -> (y+1)/2)
    for _ in range(5):
        rigid_check('3x+1', [1], [[0]], None)
    # m3_b: C = node 1 (fixed point 1, slope 4/3), exit node 0 (y -> (y-2)/3)
    for _ in range(5):
        rigid_check('m3_b', [1], [[0]], None)
    # 3x+1 with two equal-slope exits of different labels: X1 = 0, X2 = 0 0 1 ... need same slope;
    # use exits '0' (slope 1/2) and '1 0 0' (slope 3/8)?  different slopes -> not Lemma R.
    # core13: C is the 5-cycle -5,-14,-7,-20,-10 rotated; exit: a contracting re-entry
    sy = SYS['core13']
    g = G(sy)
    pts = [-5]
    while True:
        x = T(sy, pts[-1])
        if x == -5:
            break
        pts.append(x)
    Cn = [x % 8 for x in pts]
    # rotate so prefix slopes > 1
    for st in range(len(Cn)):
        R = Cn[st:] + Cn[:st]
        if all(s > 1 for s in slopes_of(sy, R)):
            Cn = R
            break
    # contracting closed walk at Cn[0] using an off-cycle edge (BFS, small)
    r0 = Cn[0]
    best = None
    dq = deque([[r0]])
    while dq and best is None:
        w = dq.popleft()
        if len(w) > 9:
            break
        for (t, _) in g[w[-1]]:
            w2 = w + [t]
            if t == r0:
                cand = w2[:-1]
                if cand != Cn[:len(cand)] or len(cand) % len(Cn):
                    s = prod(slopes_of(sy, cand)[-1:])
                    if s < 1 and not all(cand[i] == Cn[i % len(Cn)] for i in range(len(cand))):
                        best = cand
                        break
            dq.append(w2)
    check('core13 contracting re-entry found', best is not None)
    for _ in range(3):
        rigid_check('core13', Cn, [best], None)
    done = [r for r in RIGID_RUNS if r[1] != 'skipped']
    check('rigid schedules exercised', len(done) >= 10, RIGID_RUNS)
    print('  rigid two-piece schedules checked (system, steps, q, k, |X|):', done)
    worst = lemma_R_random()
    print('  Lemma R random tests: max exceptions', worst)


# ------------------------------------------------------- E cycles
def section_E():
    print('== E: expanding cycles satisfy (H0)-(H4) from bounded starts')
    for (nm, n0, xs) in (('3x-1', 5, 1), ('3x-1', 17, 1), ('3x+1', -5, -1), ('3x+1', -17, -1)):
        sy = SYS[nm]
        cyc = [n0]
        while True:
            x = T(sy, cyc[-1])
            if x == n0:
                break
            cyc.append(x)
        nodes = [x % 2 for x in cyc]
        lam = prod(slopes_of(sy, nodes)[-1:])
        check(nm + ' cycle expands', lam > 1)
        y0 = Fr(n0 - xs)
        laps = 40
        P, taus, y, A, Ecount = Fr(1), [], y0, 0, 0
        n = n0
        for _ in range(laps):
            for r in nodes:
                u, v, e = sy['br'][r]
                slope = Fr(u, 2 ** e)
                c = (u * Fr(xs) + v) / Fr(2 ** e) - Fr(xs)
                P *= slope
                y = slope * y + c
                n = T(sy, n)
                if c != 0:
                    taus.append(c / P)
        check(nm + ' cycle identity', y0 + sum(taus) == y / P and y == Fr(n - xs))
        check(nm + ' |tau| bounded', max(abs(t) for t in taus) <= 1)
        print('  %s cycle from %d: |y0| = %s, divisions after %d laps = %d, max|tau| = %s'
              % (nm, n0, abs(y0), laps, laps * sum(1 for r in nodes), max(abs(t) for t in taus)))


# ------------------------------------------------------- F Proposition B
def Tb(n):
    if n % 27 == 26:
        return (n + 1) // 27
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def section_F():
    print('== F: Proposition B (mb_s3_27)')
    inv2 = 14
    ok = True
    for n in range(-5000, 5000):
        if n % 27 == 26:
            continue
        b = n % 2
        s = n % 27
        ok &= Tb(n) % 27 == ((s * inv2) % 27 if b == 0 else ((3 * s + 1) * inv2) % 27)
    check('mb skew product', ok)
    # classes s = 2 mod 3: some prefix slope < 1 within 3 steps, all |n| < 10^6
    ok = True
    for n in range(-10 ** 6, 10 ** 6):
        if (n % 27) % 3 != 2:
            continue
        x, sl, dead = n, Fr(1), False
        for _ in range(3):
            sl *= Fr(1, 27) if x % 27 == 26 else (Fr(3, 2) if x % 2 else Fr(1, 2))
            x = Tb(x)
            if sl < 1:
                dead = True
                break
        ok &= dead
        if not ok:
            break
    check('mb classes 2 mod 3 descend within 3 steps', ok)
    # code: C = 110 from state 22; W shortest parity word 22 -> 22 avoiding 26, not power of C
    def f(s, b):
        return (s * inv2) % 27 if b == 0 else ((3 * s + 1) * inv2) % 27

    def path(bits, s):
        for b in bits:
            if s == 26:
                return None
            s = f(s, b)
        return None if s == 26 else s
    C = [1, 1, 0]
    check('mb C cycle at 22', path(C, 22) == 22)
    W = None
    for L_ in range(1, 12):
        for x in range(2 ** L_):
            bits = [(x >> i) & 1 for i in range(L_)]
            if L_ % 3 == 0 and bits == C * (L_ // 3):
                continue
            if path(bits, 22) == 22:
                W = bits
                break
        if W:
            break
    check('mb W = 010', W == [0, 1, 0], W)

    def psl(bits):
        s, out = Fr(1), []
        for b in bits:
            s *= Fr(3, 2) if b else Fr(1, 2)
            out.append(s)
        return out
    D = 0
    while True:
        U, V = C * D + W * 3, C * (D + len(W))
        if all(x > 1 for x in psl(U)) and all(x > 1 for x in psl(V)):
            break
        D += 1
    check('mb D = 25, |U| = 84', D == 25 and len(U) == 84 and len(V) == 84)
    check('mb U, V return to 22 avoiding 26', path(U, 22) == 22 and path(V, 22) == 22)

    def realize(bits, s0):
        # integers n = s0 mod 27 with Terras parity vector bits: lift 2-adically
        Mod2 = 1
        rho = 0
        for j in range(len(bits)):
            # choose rho mod 2^(j+1) so that the j-th iterate (Terras) has parity bits[j]
            for t in (0, 1):
                cand = rho + Mod2 * t
                x = cand
                okp = True
                for k in range(j + 1):
                    if x % 2 != bits[k]:
                        okp = False
                        break
                    x = x // 2 if x % 2 == 0 else (3 * x + 1) // 2
                if okp:
                    rho = cand
                    break
            Mod2 *= 2
        n = (rho + Mod2 * (((s0 - rho) * pow(Mod2, -1, 27)) % 27)) % (Mod2 * 27)
        return n, Mod2 * 27

    def follows_b(n, bits):
        for b in bits:
            if n % 27 == 26 or n % 2 != b:
                return False
            n = Tb(n)
        return True
    ok = True
    for _ in range(8):
        wd = []
        for _ in range(3):
            wd += random.choice([U, V])
        n, M = realize(wd, 22)
        ok &= follows_b(n + 2 * M, wd) and follows_b(n - 3 * M, wd)
    check('mb {U,V}^3 realized, never blocked', ok)
    # entry words: own exhaustive search, length <= 8, exact slopes > 1
    okE, mx = True, 0
    for s0 in range(27):
        if s0 % 3 == 2:
            continue
        found = None
        for L_ in range(0, 9):
            for x in range(2 ** L_):
                bits = [(x >> i) & 1 for i in range(L_)]
                if path(bits, s0) == 22 and all(y > 1 for y in psl(bits)):
                    found = bits
                    break
            if found is not None:
                break
        if found is None:
            okE = False
            print('  no entry word from', s0)
            continue
        mx = max(mx, len(found))
        n, M = realize(found + U + V, s0)
        okE &= n % 27 == s0 and follows_b(n + M, found + U + V)
    check('mb entry words for s = 0, 1 mod 3', okE)
    bad2 = [s0 for s0 in range(27) if s0 % 3 == 2 and any(
        path(b, s0) == 22 and all(y > 1 for y in psl(b))
        for L_ in range(0, 9) for b in ([(x >> i) & 1 for i in range(L_)] for x in range(2 ** L_)))]
    check('mb negative control: no entry word from s = 2 mod 3', bad2 == [], bad2)
    print('  entry words found for all 18 classes, max length', mx)
    # never-blocked non-descending counts, fit at [240, 480] (EVIDENCE)
    layer = {(s, 0): 1 for s in range(27) if s != 26}
    Ns = [sum(layer.values())]
    for j in range(1, 481):
        nxt = {}
        for (s, a), c in layer.items():
            for b in (0, 1):
                a2 = a + b
                s2 = f(s, b)
                if s2 == 26 or 3 ** a2 < 2 ** j:
                    continue
                nxt[(s2, a2)] = nxt.get((s2, a2), 0) + c
        layer = nxt
        Ns.append(sum(layer.values()))
    fit = (log(Ns[480]) - log(Ns[240])) / (240 * log(2))
    print('  never-blocked non-descending exponent, fit [240, 480]: %.4f' % fit)
    check('mb never-blocked exponent ~ 0.32', 0.30 < fit < 0.34, fit)
    # direct check of the count at j = 12 by brute force on residues mod 2^12 * 27
    j = 12
    Mod = 2 ** j * 27
    cnt = 0
    for r in range(Mod):
        x, A, good = r + Mod * 1000, 0, True
        for k in range(1, j + 1):
            if x % 27 == 26:
                good = False
                break
            A += x % 2
            x = Tb(x)
            if 3 ** A < 2 ** k:
                good = False
                break
        # also the state after j steps must not be 26 (the DP excludes s2 == 26)
        if good and x % 27 == 26:
            good = False
        cnt += good
    check('mb never-blocked DP = direct count at j=12', cnt == Ns[12], (cnt, Ns[12]))


# ------------------------------------------------------- G quoted numbers
def section_G():
    print('== G: quoted numbers')
    def kap(mu, lam):
        return log(1 / mu) / log(lam)
    tab = [(3 / 4, 3 / 2, 0.7095), (1 / 2, 3 / 2, 1.7095), (5 / 8, 5 / 2, 0.5129), (1 / 2, 5 / 2, 0.7565),
           (3 / 8, 3 / 2, 2.4190), (3 / 4, 9 / 8, 2.4425), (9 / 16, 9 / 8, 4.8849), (27 / 32, 3 / 2, 0.4190),
           (5 / 8, 5 / 4, 2.1063), (1 / 2, 5 / 4, 3.1063), (4 / 9, 4 / 3, 2.8188), (1 / 3, 4 / 3, 3.8188),
           (3 / 8, 9 / 8, 8.3274)]
    for mu, lam, v in tab:
        check('kappa %s %s' % (mu, lam), abs(kap(mu, lam) - v) < 6e-5, kap(mu, lam))
    Tm = 2 * log(2) / log(5 / 4) + 1
    check('T = 7.2126', abs(Tm - 7.2126) < 1e-4)
    check('log2(3)/(6T) = 0.0366', abs(log(3, 2) / (6 * Tm) - 0.0366) < 1e-4)
    for H, cr in ((0.4281, 1.75), (0.3593, 1.56), (0.5807, 2.38), (0.9500, 20.0), (0.9648, 28.4)):
        check('crit %s' % H, abs(1 / (1 - H) - cr) < 0.01, 1 / (1 - H))


if __name__ == '__main__':
    section_A_B()
    section_C()
    section_D()
    section_E()
    section_F()
    section_G()
    if FAILS:
        print('FAILURES (%d):' % len(FAILS), FAILS[:20])
        sys.exit(1)
    print('referee 2: all checks passed')
