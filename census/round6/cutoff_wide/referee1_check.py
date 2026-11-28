"""Referee 1 independent check for round6/cutoff_wide.

Written from scratch; does NOT import cwlib or any prover script.  Exact
arithmetic (int, Fraction) wherever a claim is exact.  Float quantities (H
exponents) are EVIDENCE and are compared with a tolerance.  Exits 1 if any
assertion fails.

Sections
  A  obstruction cycles x*, lambda_C, W slopes and kappa values of the
     theorem_W.md instance table (exact rationals; kappa floats)
  B  exact non-descending counts N(E): own DP vs own brute force over residues,
     then H_fit at large E vs the theorem_P.md table (EVIDENCE, tolerance)
  C  Theorem P code for core13, core135 built independently (own cycle, own
     re-entry walk, own D), realization of random {U,V}^n words by integers
  D  Theorem W on random rotation schedules with two pieces and a jump, for
     3x+1, core13, m3_b: identity (1) exactly on integer orbits, pairing
     identity exactly, exception counts vs the Lemma R bound, Step 1 bound
  E  Lemma R window-count slip: ceil(|I'|/floor(delta|I'|)) can exceed 1/delta+2
  F  expanding integer cycles satisfy (H1)-(H4) with bounded start (3x-1: 5,7,10;
     3x+1: -5,-7,-10 and the -17 cycle): contradicts "cycles fail (H2)"
  G  Proposition B (mb_s3_27): skew product, code U,V, realizations, and which
     27-states can reach 22 avoiding 26
  H  Lemma Q sanity: number of distinct one-piece rotation words <= n+1
  I  split5_3 kappa for the exits y/2+3/2, y/2+3 (claimed 6.2126)
"""
import sys
import random
from fractions import Fraction as Fr
from math import log, floor, ceil

random.seed(20261128)
FAILS = []
NOTES = []


def check(name, cond):
    if not cond:
        FAILS.append(name)
        print('FAIL:', name)
    return cond


# ------------------------------------------------------------------ systems
# table: dict p, m, l, rows[r] = (u, v, w) meaning n = r mod p^m -> (u n + v)/w
def terras(a, b, l):
    return dict(p=2, m=1, l=l, rows=[(1, 0, 2), (a, b, 2)])


def core(S):
    rows = []
    for r in range(8):
        if r % 2 == 0:
            rows.append((1, 0, 2))
        elif r in S:
            rows.append((3, 1, 1))
        else:
            rows.append((1, 1, 1))
    return dict(p=2, m=3, l=3, rows=rows)


SYS = {
    '3x+1': terras(3, 1, 3), '3x-1': terras(3, -1, 3), '3x+5': terras(3, 5, 3),
    '5x+1': terras(5, 1, 5),
    'K7': core({7}), 'core13': core({1, 3}), 'core135': core({1, 3, 5}),
    'core57': core({5, 7}), 'core157': core({1, 5, 7}), 'core357': core({3, 5, 7}),
    'core17': core({1, 7}), 'coreW': core({1, 3, 7}),
    'split5_3': dict(p=2, m=2, l=5, rows=[(1, 0, 2), (5, 3, 1), (1, 0, 2), (1, 3, 1)]),
    'split5_1': dict(p=2, m=2, l=5, rows=[(1, 0, 2), (5, 1, 1), (1, 0, 2), (1, 1, 1)]),
    'm3_b': dict(p=3, m=1, l=2, rows=[(1, 0, 3), (4, -1, 3), (4, 1, 3)]),
}


def res(x, M):
    x = Fr(x)
    return (x.numerator * pow(x.denominator, -1, M)) % M


def T(sd, x):
    u, v, w = sd['rows'][res(x, sd['p'] ** sd['m'])]
    y = (u * Fr(x) + v) / w
    return y


def Tint(sd, n):
    u, v, w = sd['rows'][n % sd['p'] ** sd['m']]
    assert (u * n + v) % w == 0
    return (u * n + v) // w


def ve(n, q):
    k = 0
    while n % q == 0 and n:
        n //= q
        k += 1
    return k


def row_exps(sd, r):
    u, v, w = sd['rows'][r]
    return ve(u, sd['l']) if u > 1 else 0, ve(w, sd['p'])


def cyc_of(sd, x, maxlen=200):
    pts = [Fr(x)]
    y = T(sd, x)
    while y != pts[0]:
        pts.append(y)
        y = T(sd, y)
        assert len(pts) < maxlen
    return pts


def slope_of_points(sd, pts):
    s = Fr(1)
    for x in pts:
        u, v, w = sd['rows'][res(x, sd['p'] ** sd['m'])]
        s *= Fr(u, w)
    return s


# ------------------------------------------------------------- section A
print('== A: instance table (theorem_W.md section 6)')
# claimed: system -> (x*, lambda_C, W slope, kappa_W)
claimedA = {
    '3x+1': (-1, Fr(3, 2), Fr(3, 4), 0.7095), '3x-1': (1, Fr(3, 2), Fr(3, 4), 0.7095),
    '3x+5': (-5, Fr(3, 2), Fr(3, 4), 0.7095), '5x+1': (Fr(-1, 3), Fr(5, 2), Fr(5, 8), 0.5129),
    'K7': (-1, Fr(3, 2), Fr(3, 8), 2.4190), 'core13': (-5, Fr(9, 8), Fr(3, 4), 2.4425),
    'core135': (-5, Fr(9, 8), Fr(9, 16), 4.8849), 'core57': (-1, Fr(3, 2), Fr(3, 8), 2.4190),
    'core157': (-1, Fr(3, 2), Fr(3, 8), 2.4190), 'core17': (-1, Fr(3, 2), Fr(3, 8), 2.4190),
    'core357': (-1, Fr(3, 2), Fr(27, 32), 0.4190), 'coreW': (-1, Fr(3, 2), Fr(27, 32), 0.4190),
    'split5_3': (-3, Fr(5, 4), Fr(5, 8), 2.1063), 'split5_1': (Fr(-1, 3), Fr(5, 2), Fr(5, 8), 0.5129),
    'm3_b': (1, Fr(4, 3), Fr(4, 9), 2.8188),
}
for nm, (xs, lamC, lamW, kap) in claimedA.items():
    sd = SYS[nm]
    pts = cyc_of(sd, xs)
    check(nm + ' x* periodic with lambda_C', slope_of_points(sd, pts) == lamC)
    k2 = log(1 / lamW) / log(lamC)
    check(nm + ' kappa_W value', abs(k2 - kap) < 6e-5)
    # W slope must be the slope of SOME closed walk of G_m through x*'s node that
    # leaves the cycle: search closed walks of length <= 10 at the node of x*.
    p, m = sd['p'], sd['m']
    M = p ** m
    r0 = res(xs, M)
    cyc_edges = set()
    cn = [res(x, M) for x in pts]
    for i in range(len(cn)):
        cyc_edges.add((cn[i], cn[(i + 1) % len(cn)]))

    def succ(r):
        u, v, w = sd['rows'][r]
        e = ve(w, p)
        return sorted({((u * (r + M * j) + v) // w) % M for j in range(p ** e)})
    found = False
    stack = [(r0, [r0], Fr(1), False)]
    while stack and not found:
        r, path, s, off = stack.pop()
        u, v, w = sd['rows'][r]
        s2 = s * Fr(u, w)
        for t in succ(r):
            off2 = off or ((r, t) not in cyc_edges)
            if t == r0 and off2 and s2 == lamW:
                found = True
            if len(path) < 10:
                stack.append((t, path + [t], s2, off2))
    check(nm + ' W slope realized by an off-cycle closed walk', found)

# ------------------------------------------------------------- section B
print('== B: exact non-descending counts and H (EVIDENCE)')


def brute_count(sd, E):
    p, m, l = sd['p'], sd['m'], sd['l']
    Mod = p ** (m + E)
    cnt = 0
    for r in range(Mod):
        n = r + Mod * 7919
        a = d = 0
        ok = True
        while d < E:
            ra, rd = row_exps(sd, n % p ** m)
            n = Tint(sd, n)
            a += ra
            d += rd
            if rd and l ** a < p ** d:
                ok = False
                break
        cnt += ok
    return cnt


def dp_counts(sd, Emax):
    """N[E] = # residues mod p^(m+E) whose first E divisions are non-descending.
    = # walks of G_m (start node, edges) ending at the E-th division edge."""
    p, m, l = sd['p'], sd['m'], sd['l']
    M = p ** m
    # macro edges: from node r, follow division-free steps then one dividing
    # step; returns list of (da, target) (each dividing step has e = 1 here)
    mac = {}
    for r in range(M):
        a, cur, guard = 0, r, 0
        while True:
            u, v, w = sd['rows'][cur]
            ra, rd = row_exps(sd, cur)
            if rd == 0:
                a += ra
                cur = ((u * cur + v) // w) % M
                guard += 1
                assert guard < 50
                continue
            assert rd == 1
            mac[r] = [(a + ra, ((u * (cur + M * j) + v) // w) % M) for j in range(p)]
            break
    layer = {(r, 0): 1 for r in range(M)}
    N = [M]
    for d in range(1, Emax + 1):
        nxt = {}
        for (r, a), c in layer.items():
            for (da, t) in mac[r]:
                a2 = a + da
                if l ** a2 < p ** d:
                    continue
                nxt[(t, a2)] = nxt.get((t, a2), 0) + c
        layer = nxt
        N.append(sum(layer.values()))
    return N


# core13/core135: CORRECTED values (prover: 0.4565, 0.3755); others as claimed
claimedH = {'core135': 0.3593, 'core13': 0.4281, 'split5_3': 0.5807, 'core57': 0.7193,
            'K7': 0.7491, 'core157': 0.774, 'core357': 0.788, 'core17': 0.790,
            'split5_1': 0.9369, '3x+1': 0.9500, 'm3_b': 0.9648}
for nm in ['3x+1', '3x-1', '5x+1', 'core13', 'core135', 'split5_3', 'm3_b', 'K7']:
    sd = SYS[nm]
    Eb = 11 if sd['p'] == 2 else 6
    N = dp_counts(sd, Eb)
    ok = all(brute_count(sd, E) == N[E] for E in range(1, Eb + 1))
    check(nm + ' DP equals brute residue count', ok)
Hfit = {}
for nm, Hc in claimedH.items():
    sd = SYS[nm]
    E1, E2 = 300, 600
    N = dp_counts(sd, E2)
    H = log(N[E2] / N[E1]) / ((E2 - E1) * log(sd['p']))
    Hfit[nm] = H
    print('   %-9s H_fit(300->600) = %.4f   claimed %.4f' % (nm, H, Hc))
    check(nm + ' H within 0.02 of claim (EVIDENCE)', abs(H - Hc) < 0.02)
# own variational value H = min_theta s(theta), rho(M_{theta,s}) = 1, theta in [0, 12]
def var_H(sd, thmax=12.0, steps=241):
    p, m, l = sd['p'], sd['m'], sd['l']
    M = p ** m
    mac = {}
    for r in range(M):
        a, cur = 0, r
        while True:
            u, v, w = sd['rows'][cur]
            ra, rd = row_exps(sd, cur)
            if rd == 0:
                a += ra
                cur = ((u * cur + v) // w) % M
                continue
            mac[r] = [(a + ra, ((u * (cur + M * j) + v) // w) % M) for j in range(p)]
            break

    def rho(th, s_):
        vec = [1.0] * M
        lam = 1.0
        for _ in range(400):
            nv = [0.0] * M
            for r in range(M):
                for (da, t) in mac[r]:
                    nv[r] += p ** (-s_) * (l ** da / p) ** th * vec[t]
            lam = max(nv)
            vec = [x / lam for x in nv]
        return lam

    def s_of(th):
        if rho(th, 1.0) >= 1:
            return 1.0
        lo, hi = 0.0, 1.0
        for _ in range(40):
            mid = (lo + hi) / 2
            if rho(th, mid) > 1:
                lo = mid
            else:
                hi = mid
        return hi
    best = min((s_of(thmax * j / (steps - 1)), thmax * j / (steps - 1)) for j in range(steps))
    return best, s_of(3.0)


for nm, old in (('core13', 0.4565), ('core135', 0.3755)):
    (h, th), s3 = var_H(SYS[nm])
    print('   %-8s own variational H = %.4f at theta = %.2f; s(3) = %.4f (prover grid stops at theta = 3: %.4f)'
          % (nm, h, th, s3, old))
    check(nm + ' minimizer beyond theta = 3 explains prover value', th > 3 and abs(s3 - old) < 2e-3)
    check(nm + ' corrected H agrees with fit', abs(h - Hfit[nm]) < 0.01)
NOTES.append('H for core13/core135 is 0.428/0.359, not 0.4565/0.3755: count_nondesc.H_variational '
             'searches theta in [0,3] but the minimizer is at theta ~ 4.6 / 4.0')
for nm in ['5x+1', 'coreW']:
    sd = SYS[nm]
    N = dp_counts(sd, 400)
    H = log(N[400] / N[200]) / (200 * log(sd['p']))
    print('   %-9s H_fit(200->400) = %.4f   claimed 1' % (nm, H))
    check(nm + ' H near 1 (EVIDENCE)', H > 0.97)

# ------------------------------------------------------------- section C
print('== C: Theorem P code, independent construction')


def walk_class(sd, nodes):
    """Integers following node sequence nodes[0..L] (mod p^m) for L steps
    (nodes[L] is the node after the last step).  Returns (rho, Mod)."""
    p, m = sd['p'], sd['m']
    M = p ** m
    rho, Mod = nodes[0] % M, M
    A, B, D = 1, 0, 1
    for j in range(1, len(nodes)):
        u, v, w = sd['rows'][nodes[j - 1]]
        A, B, D = A * u, B * u + v * D, D * w
        e = ve(w, p)
        if e == 0:
            val = (A * rho + B) // D
            assert (A * rho + B) % D == 0
            if val % M != nodes[j]:
                return None
            continue
        hits = []
        for t in range(p ** e):
            n2 = rho + Mod * t
            if (A * n2 + B) % D == 0 and ((A * n2 + B) // D) % M == nodes[j]:
                hits.append(n2)
        if len(hits) != 1:
            return None
        rho, Mod = hits[0], Mod * p ** e
    return rho, Mod


def follows(sd, n, nodes):
    M = sd['p'] ** sd['m']
    for j in range(len(nodes) - 1):
        if n % M != nodes[j]:
            return False
        n = Tint(sd, n)
    return n % M == nodes[-1]


def code_for(nm, xs):
    sd = SYS[nm]
    p, m = sd['p'], sd['m']
    M = p ** m
    pts = cyc_of(sd, xs)
    # cycle lemma rotation: start after the last minimum of partial log sums
    sl = [Fr(sd['rows'][res(x, M)][0], sd['rows'][res(x, M)][2]) for x in pts]
    L = len(pts)
    part, s = [], Fr(1)
    for x in sl:
        s *= x
        part.append(s)
    mn = min([Fr(1)] + part)
    idx = max(i for i, v in enumerate([Fr(1)] + part) if v == mn)
    start = idx % L
    pts = pts[start:] + pts[:start]
    cn = [res(x, M) for x in pts]
    ps, s = [], Fr(1)
    for r in cn:
        s *= Fr(sd['rows'][r][0], sd['rows'][r][2])
        ps.append(s)
    check(nm + ' own cycle-lemma rotation all partial slopes > 1', all(v > 1 for v in ps))
    # re-entry: BFS for shortest closed walk at cn[0] using a non-cycle edge
    cedges = {(cn[i], cn[(i + 1) % L]) for i in range(L)}

    def succ(r):
        u, v, w = sd['rows'][r]
        return sorted({((u * (r + M * j) + v) // w) % M for j in range(p ** ve(w, p))})
    from collections import deque
    q = deque([(cn[0], (cn[0],), False)])
    W = None
    while q:
        r, path, off = q.popleft()
        for t in succ(r):
            o2 = off or (r, t) not in cedges
            if t == cn[0] and o2:
                W = list(path)
                break
            if len(path) < 14:
                q.append((t, path + (t,), o2))
        if W:
            break
    check(nm + ' own re-entry found', W is not None)
    Wp = W * L

    def pslopes(word):
        out, s = [], Fr(1)
        for r in word:
            s *= Fr(sd['rows'][r][0], sd['rows'][r][2])
            out.append(s)
        return out
    D = 0
    while True:
        U = cn * D + Wp
        V = cn * (D + len(Wp) // L)
        if all(v > 1 for v in pslopes(U)) and all(v > 1 for v in pslopes(V)):
            break
        D += 1
    check(nm + ' U != V, equal length', U != V and len(U) == len(V))
    eU = sum(ve(sd['rows'][r][2], p) for r in U)
    eV = sum(ve(sd['rows'][r][2], p) for r in V)
    # realize random words of 5 blocks by integers, by direct iteration
    ok = True
    for _ in range(6):
        word = []
        for _ in range(5):
            word += random.choice([U, V])
        assert all(v > 1 for v in pslopes(word))
        c = walk_class(sd, word + [word[0]])
        if c is None:
            ok = False
            break
        rho, Mod = c
        for n in (rho, rho + Mod * random.randint(1, 10 ** 6), rho - Mod * random.randint(1, 10 ** 6)):
            ok &= follows(sd, n, word + [word[0]])
    check(nm + ' random {U,V}^5 words realized by integers', ok)
    # dimension bound: solve p^(-s eU) + p^(-s eV) = 1
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if p ** (-mid * eU) + p ** (-mid * eV) > 1:
            lo = mid
        else:
            hi = mid
    print('   %-8s |C|=%d |W|=%d D=%d |U|=%d eU/eV=%d/%d s>=%.4f' % (nm, L, len(W), D, len(U), eU, eV, lo))
    return lo


s13 = code_for('core13', -5)
s135 = code_for('core135', -5)
check('core13/core135 dimension bounds positive', s13 > 0 and s135 > 0)

# ------------------------------------------------------------- section D
print('== D: Theorem W identity, pairing, exceptions on random two-piece rotation schedules')


def blocks_word(cn, X, ks):
    w = []
    for k in ks:
        w += cn * k + X
    return w


def schedule_piece(kappa, n, t, c0, cuts, vals):
    """K_i = c0 + floor(kappa i + t) + w(phi_i), phi_i = {kappa i + t},
    w = vals[j] on [cuts[j], cuts[j+1]) (cuts[0] = 0)."""
    Ks, phis = [], []
    for i in range(1, n + 1):
        x = kappa * i + t
        phi = x - floor(x)
        j = max(jj for jj in range(len(cuts)) if cuts[jj] <= phi)
        Ks.append(c0 + floor(x) + vals[j])
        phis.append(phi)
    return Ks, phis


def test_W(nm, xs, Cnodes, Xnodes, trials=4, J=2, delta=0.2):
    sd = SYS[nm]
    p, l, m = sd['p'], sd['l'], sd['m']
    M = p ** m
    lamC = Fr(1)
    aC = eC = aX = eX = 0
    for r in Cnodes:
        lamC *= Fr(sd['rows'][r][0], sd['rows'][r][2])
        ra, rd = row_exps(sd, r)
        aC += ra
        eC += rd
    lamX = Fr(1)
    for r in Xnodes:
        lamX *= Fr(sd['rows'][r][0], sd['rows'][r][2])
        ra, rd = row_exps(sd, r)
        aX += ra
        eX += rd
    kappa = log(1 / lamX) / log(lamC)
    # shifted constant of X around xs
    y = Fr(xs)
    for r in Xnodes:  # the affine branches named by the nodes (x* itself does not follow X)
        u, v, w = sd['rows'][r]
        y = (u * y + v) / w
    yC = Fr(xs)
    for r in Cnodes:
        u, v, w = sd['rows'][r]
        yC = (u * yC + v) / w
    check(nm + ' C fixes x*', yC == xs)
    # X maps xs + y to xs + lamX y + cX
    cX = y - xs
    check(nm + ' exit constant nonzero', cX != 0)
    worst = 0
    for tr in range(trials):
        n1, n2 = random.randint(25, 45), random.randint(25, 45)
        pieces = []
        Kall = []
        base = 0
        for n_ in (n1, n2):
            t = random.random()
            cuts = [0.0] + sorted(random.random() for _ in range(J - 1))
            vals = [random.randint(0, 1) for _ in cuts]
            Ks, phis = schedule_piece(kappa, n_, t, 0, cuts, vals)
            off = base + random.randint(3, 25) - Ks[0]  # jump at the piece start
            Ks = [k + off for k in Ks]
            pieces.append((len(Kall), len(Kall) + n_))
            Kall += Ks
            base = Ks[-1]
        ks = [Kall[0]] + [Kall[i] - Kall[i - 1] for i in range(1, len(Kall))]
        if min(ks) < 0:
            continue
        word = blocks_word(Cnodes, Xnodes, ks)
        nodes = word + [Cnodes[0]]
        c = walk_class(sd, nodes)
        check(nm + ' rigid word realizable', c is not None)
        rho, Mod = c
        n0 = rho + Mod * random.randint(1, 1000)
        check(nm + ' integer follows rigid word', follows(sd, n0, nodes))
        # orbit and identity (1)
        cur = n0
        A = E = 0
        taus = []
        Ep, Ap = [], []
        for bi, k in enumerate(ks):
            for _ in range(k):
                for r in Cnodes:
                    cur = Tint(sd, cur)
                A += aC * k * 0  # placeholder (exponents tracked below)
            A_before = (aC * sum(ks[:bi + 1])) + aX * bi
            E_before = (eC * sum(ks[:bi + 1])) + eX * bi
            for r in Xnodes:
                cur = Tint(sd, cur)
            # event: the whole exit block X, c = cX, a = aX, e = eX
            Aev = A_before + aX
            Eprime = E_before
            Ep.append(Eprime)
            Ap.append(Aev)
            # W convention phi(y) = (l^a y + c)/p^e with c = cX p^eX, so
            # tau = c/(l^a P_{j-1}) = cX p^(E'+eX)/l^A
            taus.append(cX * Fr(p ** (Eprime + eX), l ** Aev))
        Etot = eC * sum(ks) + eX * len(ks)
        Atot = aC * sum(ks) + aX * len(ks)
        y0 = Fr(n0) - xs
        yn = Fr(cur) - xs
        check(nm + ' whole-prefix identity (1)', y0 + sum(taus) == Fr(p ** Etot, l ** Atot) * yn)
        # prefix slopes at events >= 1 (non-descending family)
        check(nm + ' |tau_i| <= |cX| p^eX (H2 from slopes >= 1)',
              all(abs(tt) <= abs(cX) * p ** eX for tt in taus))
        # pairing on each piece with Dirichlet q
        for (u, v) in pieces:
            n_ = v - u
            Q = int(delta * n_)
            q = min(range(1, Q + 1), key=lambda j: abs(kappa * j - round(kappa * j)))
            k = round(kappa * q)
            kA, kE = aC * k + aX * q, eC * k + eX * q
            gamma = Fr(l ** kA, p ** kE) if kA >= 0 else Fr(1, p ** kE * l ** (-kA))
            check(nm + ' k_E >= 1', kE >= 1)
            # Step 1 bound |1 - gamma| >= p^-kE l^-max(0,-kA)
            check(nm + ' Step 1 bound', abs(1 - gamma) >= Fr(1, p ** kE * l ** max(0, -kA)))
            tau = taus[u:v]
            exc = [i for i in range(n_ - q) if tau[i] != gamma * tau[i + q]]
            lhs = (1 - gamma) * sum(tau)
            rhs = sum(tau[n_ - q:]) - gamma * sum(tau[:q]) + sum(tau[i] - gamma * tau[i + q] for i in exc)
            check(nm + ' pairing identity (Step 2)', lhs == rhs)
            # exceptions: half-open arcs of length Delta, (J cuts + point 0) per window
            windows = ceil(n_ / Q)
            check(nm + ' exceptions <= (J+1)*windows', len(exc) <= (J + 1) * windows)
            Mstated = 2 * (2 * J + 1) * (1 / delta + 2)
            check(nm + ' exceptions <= stated M(delta)', len(exc) <= Mstated)
            worst = max(worst, len(exc))
    print('   %-8s kappa=%.4f  max exceptions per piece %d' % (nm, kappa, worst))


test_W('3x+1', -1, [1], [0])
# core13: rotated cycle point; take the C node list from the cycle at x* = -5 rotated
sd = SYS['core13']
pts = cyc_of(sd, -5)
# rotation with all partial slopes > 1
for st in range(len(pts)):
    rot = pts[st:] + pts[:st]
    s, ok = Fr(1), True
    for x in rot:
        r = res(x, 8)
        s *= Fr(sd['rows'][r][0], sd['rows'][r][2])
        ok &= s > 1
    if ok:
        break
xs13 = rot[0]
Cn13 = [res(x, 8) for x in rot]
# contracting exit: find a closed walk at Cn13[0] of slope 3/4 using a non-cycle edge
test_W_ok = False


def find_exit(nm, r0, Cn, target_slope, maxlen=8):
    sd = SYS[nm]
    p, m = sd['p'], sd['m']
    M = p ** m
    ced = {(Cn[i], Cn[(i + 1) % len(Cn)]) for i in range(len(Cn))}
    stack = [(r0, [r0], Fr(1), False)]
    while stack:
        r, path, s, off = stack.pop()
        u, v, w = sd['rows'][r]
        s2 = s * Fr(u, w)
        for t in sorted({((u * (r + M * j) + v) // w) % M for j in range(p ** ve(w, p))}):
            o2 = off or (r, t) not in ced
            if t == r0 and o2 and s2 == target_slope:
                return path
            if len(path) < maxlen:
                stack.append((t, path + [t], s2, o2))
    return None


X13 = find_exit('core13', Cn13[0], Cn13, Fr(3, 4))
check('core13 exit of slope 3/4 exists', X13 is not None)
test_W('core13', xs13, Cn13, X13, trials=3)
test_W('m3_b', 1, [1], [0], trials=3)

# ------------------------------------------------------------- section E
print('== E: Lemma R window count')
bad = []
for den in range(5, 41):
    delta = 1 / den
    for I in range(2 * den, 6 * den):
        Q = floor(delta * I)
        if ceil(I / Q) > 1 / delta + 2 + 1e-12:
            bad.append((den, I, ceil(I / Q)))
print('   instances with ceil(|I|/Q) > 1/delta + 2: %d, e.g. delta=1/%d |I|=%d windows=%d'
      % (len(bad), *bad[0]) if bad else '   none')
NOTES.append('Lemma R: window bound 1/delta+2 false (%d cases); true bound 2/delta+1' % len(bad))
check('Lemma R corrected window bound 2/delta + 1 always holds',
      all(ceil(I / floor(I / den)) <= 2 * den + 1 for den in range(5, 41) for I in range(2 * den, 6 * den)))
# with half-open arcs (<= 1 point per arc per window) M = (2J+1)(2/delta+1) <= 2(2J+1)(1/delta+2)
check('corrected M <= stated M', all((2 * J + 1) * (2 * d + 1) <= 2 * (2 * J + 1) * (d + 2)
                                     for J in range(1, 6) for d in range(4, 100)))

# ------------------------------------------------------------- section F
print('== F: expanding integer cycles are bounded-start paths satisfying (H1)-(H4)')


def cycle_path_test(nm, xs, n0, laps=40):
    sd = SYS[nm]
    p, l, m = sd['p'], sd['l'], sd['m']
    M = p ** m
    pts = cyc_of(sd, n0)
    lam = slope_of_points(sd, pts)
    # rotate so every prefix slope > 1
    for st in range(len(pts)):
        rot = pts[st:] + pts[:st]
        s, ok = Fr(1), True
        for x in rot:
            u, v, w = sd['rows'][res(x, M)]
            s *= Fr(u, w)
            ok &= s > 1
        if ok:
            break
    assert ok
    # shifted labels around xs: step x -> (u x + v)/w acts on y = x - xs as
    # y -> (u y + c)/w with c = u xs + v - w xs
    y0 = rot[0] - xs
    y = y0
    P = Fr(1)
    A = E = 0
    taus = []
    labels = set()
    cur = rot[0]
    for _ in range(laps):
        for x in rot:
            u, v, w = sd['rows'][res(cur, M)]
            c = u * Fr(xs) + v - w * Fr(xs)
            a, e = row_exps(sd, res(cur, M))
            if c != 0:
                labels.add(c)
                taus.append(c * Fr(p ** E, l ** (A + a)))
            A += a
            E += e
            cur = (u * cur + v) / w
    yn = cur - xs
    ident = y0 + sum(taus) == Fr(p ** E, l ** A) * yn
    tmax = max(abs(t) for t in taus)
    print('   %-5s cycle from %s (lap slope %s), shifted start |y0| = %s, labels %s, E = %d, max|tau| = %s'
          % (nm, rot[0], lam, abs(y0), sorted(labels), E, float(tmax)))
    check(nm + ' cycle identity (1)', ident)
    check(nm + ' expanding cycle path has bounded tau (H2 holds)', lam > 1 and tmax <= 2)
    return E, abs(y0)


cycle_path_test('3x-1', 1, 5)
cycle_path_test('3x-1', 1, 17)
cycle_path_test('3x+1', -1, -5)
cycle_path_test('3x+1', -1, -17)
NOTES.append('Expanding integer cycles satisfy (H1)-(H4) with |y0| bounded and E unbounded; '
             '"cycles fail (H2)" is false for them; y_* must exceed their shifted starts')

# ------------------------------------------------------------- section G
print('== G: Proposition B (mb_s3_27)')


def Tmb(n):
    if n % 27 == 26:
        return (n + 1) // 27
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def fmb(s, b):
    return (s * 14) % 27 if b == 0 else ((3 * s + 1) * 14) % 27  # 14 = 1/2 mod 27


ok = True
for n in range(-3000, 3000):
    if n % 27 != 26:
        ok &= Tmb(n) % 27 == fmb(n % 27, n % 2)
check('mb skew product', ok)
check('mb -5,-7,-10 cycle', [Tmb(-5), Tmb(-7), Tmb(-10)] == [-7, -10, -5])
Cb = [1, 1, 0]
Wb = [0, 1, 0]


def fpath(bits, s):
    for b in bits:
        if s == 26:
            return None
        s = fmb(s, b)
    return None if s == 26 else s


check('mb C returns 22', fpath(Cb, 22) == 22)
check('mb W=010 returns 22', fpath(Wb, 22) == 22)
Ub = Cb * 25 + Wb * 3
Vb = Cb * 28


def pslope_bits(bits):
    s, out = Fr(1), []
    for b in bits:
        s *= Fr(3, 2) if b else Fr(1, 2)
        out.append(s)
    return out


check('mb U,V length 84, prefix slopes > 1', len(Ub) == len(Vb) == 84 and
      all(v > 1 for v in pslope_bits(Ub)) and all(v > 1 for v in pslope_bits(Vb)))
check('mb D=25 minimal', not all(v > 1 for v in pslope_bits(Cb * 24 + Wb * 3)))


def mb_class(bits, s0):
    # own lifting: residues mod 2^j * 27 with n = s0 mod 27, parity word bits
    rho, Mod = s0 % 27, 27
    for j, b in enumerate(bits):
        good = []
        for t in range(2):
            n = rho + Mod * t
            m_ = n
            okk = True
            for bb in bits[:j]:
                m_ = Tmb(m_)
            if m_ % 2 == b:
                good.append(n)
        assert len(good) == 1
        rho, Mod = good[0], Mod * 2
    return rho, Mod


ok = True
for _ in range(8):
    word = []
    for _ in range(3):
        word += random.choice([Ub, Vb])
    rho, Mod = mb_class(word, 22)
    for n in (rho, rho + Mod * random.randint(1, 10 ** 9)):
        m_ = n
        for b in word:
            if m_ % 27 == 26 or m_ % 2 != b:
                ok = False
            m_ = Tmb(m_)
check('mb random {U,V}^3 words realized, never blocked', ok)
# which states reach 22 avoiding 26
reach = {22}
changed = True
while changed:
    changed = False
    for s in range(27):
        if s in reach or s == 26:
            continue
        if any(fmb(s, b) in reach for b in (0, 1)):
            reach.add(s)
            changed = True
print('   states that reach 22 avoiding 26: %d of 27 (missing %s)' % (len(reach), sorted(set(range(27)) - reach)))
NOTES.append('Prop B "inside each 27-class": false for s = 26 (blocked immediately); holds for %d states' % len(reach))

# ------------------------------------------------------------- section H
print('== H: Lemma Q sanity (one rotation piece, no w)')
kappa = log(2) / log(1.5)
for n in (10, 20, 40):
    words = set()
    for j in range(4000):
        t = j / 4000 + 1 / 8000
        Ks = [floor(kappa * i + t) for i in range(0, n + 1)]
        words.add(tuple(Ks[i] - Ks[i - 1] for i in range(1, n + 1)))
    check('Lemma Q: <= n+1 words for n=%d' % n, len(words) <= n + 1)
    print('   n=%d distinct rotation words %d (bound n+1 = %d)' % (n, len(words), n + 1))

# ------------------------------------------------------------- section I
print('== I: split5_3 kappa for exits of slope 1/2')
sd = SYS['split5_3']
xs = -3
# exits y/2 + 3/2 and y/2 + 3: slope 1/2; lambda_C = 5/4
kap = log(2) / log(1.25)
print('   log 2 / log(5/4) = %.4f  (theorem_W table says 6.2126)' % kap)
check('split5_3 standard kappa = 3.1063', abs(kap - 3.1063) < 1e-4)
NOTES.append('split5_3 kappa: 3.1063 = 1/log2(5/4) (repo), not 6.2126 as in theorem_W table')

print()
for nt in NOTES:
    print('NOTE:', nt)
if FAILS:
    print('FAILURES (%d):' % len(FAILS), FAILS)
    sys.exit(1)
print('referee1_check: all assertions passed')
