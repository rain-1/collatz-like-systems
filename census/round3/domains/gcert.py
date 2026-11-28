"""Norm-descent certificates for Collatz-type maps on an imaginary quadratic
order, dividing by a prime pi (used here for Z[i], pi = 1+i).

Map: T(z) = z/pi if pi | z; else u_r z + c_r where r = z mod pi^m (table over
canonical residues mod pi^m, odd residues only).  Classes are z = pi^K t + r
(t ranges over the whole order).  On a class, T^j(z) = P t + R exactly.
A node closes at the first j >= 1 with N(P) < N(pi)^K: then |T^j z| < |z| for
all t outside a finite disc (norm descent).  Lemma A then gives GLOBAL plus the
complete cycle list from the finite exceptional set (cycles_from_E).
All arithmetic exact (Python ints).
"""
from math import isqrt
import rings as RG


class GaussMap:
    def __init__(self, R, m, rule):
        """rule(r) -> (u, c) for odd canonical residues r mod pi^m."""
        self.R, self.m = R, m
        self.pim = (1, 0)
        for _ in range(m):
            self.pim = R.mul(self.pim, R.pi)
        from check_rings import hnf_reducer
        self.red, self.Nm = hnf_reducer(R, self.pim)
        self.table = {}
        for a in range(self.Nm):
            for b in range(self.Nm):
                r = self.red((a, b))
                if r in self.table:
                    continue
                if R.divides(R.pi, r):
                    self.table[r] = None
                else:
                    u, c = rule(r)
                    assert R.divides(R.pi, R.add(R.mul(u, r), c))
                    self.table[r] = (u, c)
        assert len(self.table) == self.Nm

    def __call__(self, z):
        R = self.R
        if R.divides(R.pi, z):
            return R.div(z, R.pi)
        u, c = self.table[self.red(z)]
        return R.add(R.mul(u, z), c)


def reps(R, K):
    """A complete residue system mod pi^K built from pi-adic digits {0,1}."""
    out = [(0, 0)]
    pk = (1, 0)
    for _ in range(K):
        out = out + [R.add(x, pk) for x in out]
        pk = R.mul(pk, R.pi)
    return out


def certificate(Tm, maxK=60, maxnodes=400000):
    R, m = Tm.R, Tm.m
    Rm = reps(R, m)
    leaves = []
    # node: (K, r, P, R0, j); z = pi^K t + r ; T^j z = P t + R0
    stack = [(0, (0, 0), (1, 0), (0, 0), 0)]
    nodes = 0
    q = R.Npi
    while stack:
        K, r, P, R0, j = stack.pop()
        nodes += 1
        if nodes > maxnodes:
            return dict(ok=False, reason='nodes', open=(K, r, j))
        if j > 0 and R.norm(P) < q ** K:
            leaves.append((K, r, j, P, R0))
            continue
        # residues of P t + R0 mod pi^m over all t
        res = {Tm.red(R.add(R0, R.mul(P, s))) for s in Rm}
        rows = {Tm.table[x] for x in res}
        if len(rows) == 1:
            row = rows.pop()
            if row is None:            # all divisible by pi: need pi | P and pi | R0
                if R.divides(R.pi, P) and R.divides(R.pi, R0):
                    stack.append((K, r, R.div(P, R.pi), R.div(R0, R.pi), j + 1))
                    continue
            else:
                u, c = row
                stack.append((K, r, R.mul(u, P), R.add(R.mul(u, R0), c), j + 1))
                continue
        if K >= maxK:
            return dict(ok=False, reason='depth', open=(K, r, j))
        pk = (1, 0)
        for _ in range(K):
            pk = R.mul(pk, R.pi)
        for s in ((0, 0), (1, 0)):
            # t = pi t' + s:  z = pi^(K+1) t' + (r + pi^K s); P t + R0 = (P pi) t' + (R0 + P s)
            stack.append((K + 1, R.add(r, R.mul(pk, s)), R.mul(P, R.pi), R.add(R0, R.mul(P, s)), j))
    return dict(ok=True, leaves=leaves, k=max(l[2] for l in leaves),
                K=max(l[0] for l in leaves), size=len(leaves))


def verify(Tm, leaves):
    """Independent check: measure sums to 1, prefix code (no leaf class contains
    another), descent condition, and each affine form equals the true iterate at
    several t (including large ones)."""
    from fractions import Fraction
    R = Tm.R
    q = R.Npi
    assert sum(Fraction(1, q ** K) for K, *_ in leaves) == 1

    def pipow(K):
        x = (1, 0)
        for _ in range(K):
            x = R.mul(x, R.pi)
        return x
    from check_rings import hnf_reducer
    reds = {}
    keys = set()
    for K, r, *_ in leaves:
        if K not in reds:
            reds[K] = hnf_reducer(R, pipow(K))[0]
        keys.add((K, reds[K](r)))
    assert len(keys) == len(leaves)
    for K, r, *_ in leaves:
        for K2 in range(K):
            if K2 not in reds:
                reds[K2] = hnf_reducer(R, pipow(K2))[0] if K2 > 0 else (lambda z: (0, 0))
            assert (K2, reds[K2](r)) not in keys, (K, r, K2)
    for K, r, j, P, R0 in leaves:
        assert R.norm(P) < q ** K
        pk = pipow(K)
        for t in [(0, 0), (1, 0), (0, 1), (-3, 2), (10 ** 12 + 7, -(10 ** 11) + 3)]:
            z = R.add(R.mul(pk, t), r)
            x = z
            for _ in range(j):
                x = Tm(x)
            assert x == R.add(R.mul(P, t), R0), (K, r, j, t)
    return True


def exceptional(Tm, leaves):
    """All z = pi^K t + r in a leaf with N(P t + R0) >= N(pi^K t + r).
    Superset bound for |t| (exact): with A = sqrt(2^K) and p = sqrt(N(P)),
    |t| (A - p) <= |R0| + |r|, and A - p = (2^K - N(P))/(A + p) >= (2^K - N(P))/(2*(isqrt(2^K)+1))."""
    R = Tm.R
    q = R.Npi
    E = set()

    def pipow(K):
        x = (1, 0)
        for _ in range(K):
            x = R.mul(x, R.pi)
        return x
    for K, r, j, P, R0 in leaves:
        num = (isqrt(R.norm(R0)) + 1 + isqrt(R.norm(r)) + 1) * 2 * (isqrt(q ** K) + 1)
        den = q ** K - R.norm(P)
        B = num // den + 1                  # |t| <= B ; coordinates of t bounded by 2B
        pk = pipow(K)
        L = 2 * B + 1
        for a in range(-L, L + 1):
            for b in range(-L, L + 1):
                t = (a, b)
                if R.norm(t) > 4 * B * B:
                    continue
                z = R.add(R.mul(pk, t), r)
                if R.norm(R.add(R.mul(P, t), R0)) >= R.norm(z):
                    E.add(z)
    return sorted(E)


# ---------------------------------------------------------------- obstructions
def residue_graph(Tm):
    """Nodes: canonical residues mod pi^m.  Odd r -> (u r + c) mod pi^m with
    weight log|u|; even s -> the residues mod pi^m of s/pi (two of them), weight
    -log|pi|.  (Weights in floats for the search only.)"""
    import math
    R = Tm.R
    edges = {}
    pim1 = (1, 0)
    for _ in range(Tm.m - 1):
        pim1 = R.mul(pim1, R.pi)
    for r, row in Tm.table.items():
        if row is None:
            h = R.div(r, R.pi)
            tg = {Tm.red(h), Tm.red(R.add(h, pim1))}
            edges[r] = [(t, -0.5 * math.log(R.Npi), ('H',)) for t in tg]
        else:
            u, c = row
            edges[r] = [(Tm.red(R.add(R.mul(u, r), c)), 0.5 * math.log(R.norm(u)), ('B', r))]
    return edges


def max_mean_cycle(edges):
    """Karp's algorithm (floats; search only).  Returns (mean, list of edges)."""
    nodes = list(edges)
    idx = {v: i for i, v in enumerate(nodes)}
    n = len(nodes)
    NEG = float('-inf')
    D = [[NEG] * n for _ in range(n + 1)]
    par = [[None] * n for _ in range(n + 1)]
    for i in range(n):
        D[0][i] = 0.0
    for k in range(1, n + 1):
        for v in nodes:
            i = idx[v]
            if D[k - 1][i] == NEG:
                continue
            for t, wgt, lab in edges[v]:
                j = idx[t]
                if D[k - 1][i] + wgt > D[k][j]:
                    D[k][j] = D[k - 1][i] + wgt
                    par[k][j] = (i, lab)
    best, bv = NEG, None
    for v in range(n):
        if D[n][v] == NEG:
            continue
        worst = min((D[n][v] - D[k][v]) / (n - k) for k in range(n) if D[k][v] != NEG)
        if worst > best:
            best, bv = worst, v
    walk, k, v = [], n, bv
    while k > 0:
        i, lab = par[k][v]
        walk.append((nodes[i], nodes[v], lab))
        v, k = i, k - 1
    walk.reverse()
    seen = {}
    for pos, (a, b, lab) in enumerate(walk):
        if a in seen:
            return best, walk[seen[a]:pos]
        seen[a] = pos
    return best, walk


def verify_obstruction(Tm, cyc_edges, maxlen=10000):
    """Exact: compose the cycle's affine steps (z -> u z + c or z -> z/pi),
    take the fixed point x in Q(i) (as a pair numerator/denominator in Z[i]),
    check that the true pi-adic T-orbit of x is periodic with that itinerary,
    that |multiplier|^2 = prod N(u) / 2^h > 1, and that some rotation has all
    partial products > 1 (cycle lemma; Lemma B then kills every certificate)."""
    from fractions import Fraction
    R = Tm.R
    # composite z -> (A z + B)/D, D = pi^h (as ring elements)
    A, B, D = (1, 0), (0, 0), (1, 0)
    mults = []
    for (a, b, lab) in cyc_edges:
        if lab[0] == 'H':
            D = R.mul(D, R.pi)
            mults.append(Fraction(1, R.Npi))
        else:
            u, c = Tm.table[lab[1]]
            A, B = R.mul(u, A), R.add(R.mul(u, B), R.mul(c, D))
            mults.append(Fraction(R.norm(u)))
    # x = B/(D - A)
    num, den = B, R.add(D, R.neg(A))
    # follow T on x = num/den pi-adically: residue of x mod pi^m via den^{-1}
    reps_m = reps(R, Tm.m)

    def res(nm, dn):
        for s in reps_m:            # s with dn*s = nm (mod pi^m)
            if Tm.red(R.add(R.mul(dn, s), R.neg(nm))) == (0, 0):
                return Tm.red(s)
        raise AssertionError('denominator not a pi-unit')

    def step(nm, dn):
        r = res(nm, dn)
        row = Tm.table[r]
        if row is None:
            # nm/dn divisible by pi: divide numerator (dn is a pi-unit)
            return R.div(nm, R.pi) if R.divides(R.pi, nm) else _div_frac(R, nm, dn), dn
        u, c = row
        return R.add(R.mul(u, nm), R.mul(c, dn)), dn

    def eq(n1, d1, n2, d2):
        return R.mul(n1, d2) == R.mul(n2, d1)
    nm, dn = num, den
    for (a, b, lab) in cyc_edges:
        r = res(nm, dn)
        assert r == a, 'itinerary mismatch'
        nm, dn = step(nm, dn)
    assert eq(nm, dn, num, den), 'not periodic'
    lam = 1
    for q in mults:
        lam *= q
    assert lam > 1
    L = len(mults)
    pref = [Fraction(1)]
    for q in mults:
        pref.append(pref[-1] * q)
    mn = min(pref[:L])
    i0 = max(i for i in range(L) if pref[i] == mn)
    rot = mults[i0:] + mults[:i0]
    acc = Fraction(1)
    for j in range(2 * L):
        acc *= rot[j % L]
        assert acc > 1
    return dict(period=L, mult2=lam, point=(num, den))


def _div_frac(R, nm, dn):
    # nm/dn is pi-divisible with dn a pi-unit but nm not divisible as written:
    # rewrite x = (nm * conj(dn)) / N(dn) and divide the new numerator.
    raise AssertionError('unexpected')
