"""Exact p-adic descent-certificate engine for residue-class affine maps.

A map is given by (p, m, table): Q = p**m, and table[r] = (u, v, w) means
    n = r (mod Q)  ->  (u*n + v) // w      (exact division, w a power of p).

1. certificate(...)  -- exhaustive search for the minimal descent certificate.
   A class n = p^K t + r (t >= 0) carries T^j(n) = P t + R with integers
   P, R, valid for every t >= 0.  The class is *closed* at the first j with
   P < p^K, or P == p^K and R < r: then T^j(n) < n for all large n in the
   class.  If the values P t + R (t >= 0) do not all use the same branch
   (i.e. the residues R + gcd(P,Q) i mod Q hit different table rows), t is
   split p ways; otherwise one step is applied.  Each p-adic integer is closed at its own first
   descent time, so the leaves form the unique minimal certificate: no
   certificate can use fewer steps on any class.

2. growing_cycle(...) -- searches the p-adic cylinder graph for a cycle with
   multiplier > 1, then returns the exact rational p-adic periodic point,
   verified with Fractions.  Such a point kills every certificate (see
   lemmas.md, Lemma B).

All integer arithmetic is exact; floats are only used to *find* candidate
cycles, which are then verified exactly.
"""
from fractions import Fraction
import math


def vp(x, p):
    if x == 0:
        return 10 ** 9
    c = 0
    while x % p == 0:
        x //= p
        c += 1
    return c


def check_table(p, m, table, upto=2000):
    Q = p ** m
    for n in range(1, upto):
        u, v, w = table[n % Q]
        assert (u * n + v) % w == 0 and (u * n + v) // w > 0, n


def step_fn(p, m, table):
    Q = p ** m

    def T(n):
        u, v, w = table[n % Q]
        x = u * n + v
        assert x % w == 0
        return x // w
    return T


def certificate(p, m, table, maxK=40, maxnodes=2_000_000):
    """Return dict with leaves [(K, r, j, P, R)], or None if maxK/maxnodes hit
    (then 'open' lists an unresolved class)."""
    Q = p ** m
    leaves = []
    stack = [(0, 0, 1, 0, 0)]       # (K, r, P, R, j): n = p^K t + r, value P t + R
    nodes = 0
    while stack:
        K, r, P, R, j = stack.pop()
        nodes += 1
        if nodes > maxnodes:
            return dict(ok=False, open=(K, r, j), reason="nodes")
        pk = p ** K
        if j > 0 and (P < pk or (P == pk and R < r)):
            leaves.append((K, r, j, P, R))
            continue
        g = math.gcd(P, Q)
        ent = {table[(R + g * i) % Q] for i in range(Q // g)}
        u, v, w = next(iter(ent))
        if len(ent) == 1 and (u * P) % w == 0:
            # branch (and exact division) determined for every t >= 0
            nP, nR = u * P, u * R + v
            assert nP % w == 0 and nR % w == 0
            stack.append((K, r, nP // w, nR // w, j + 1))
        else:
            if K >= maxK:
                return dict(ok=False, open=(K, r, j), reason="depth")
            for s in range(p):
                stack.append((K + 1, r + s * pk, p * P, R + s * P, j))
    # threshold: largest n in a leaf class that is not yet known to descend
    N0 = 0
    for K, r, j, P, R in leaves:
        pk = p ** K
        if P < pk:
            if R >= r:
                tmax = (R - r) // (pk - P)
                N0 = max(N0, pk * tmax + r)
        else:  # P == pk, R < r: descends for every t
            pass
    return dict(ok=True, leaves=leaves, N0=N0,
                K=max(l[0] for l in leaves), k=max(l[2] for l in leaves),
                size=len(leaves))


def verify_certificate(p, m, table, leaves):
    """Independent check: leaves partition Z_p (measure sums to 1, pairwise
    disjoint as a prefix code) and the affine form of each leaf is recomputed
    by direct substitution at several t and checked to descend."""
    Q = p ** m
    T = step_fn(p, m, table)
    tot = Fraction(0)
    seen = set()
    for K, r, j, P, R in leaves:
        tot += Fraction(1, p ** K)
        seen.add((K, r))
    assert tot == 1, tot
    # prefix-code disjointness: no leaf class contains another leaf's class
    for K, r, j, P, R in leaves:
        for K2 in range(K):
            assert (K2, r % p ** K2) not in seen
    for K, r, j, P, R in leaves:
        pk = p ** K
        assert P < pk or (P == pk and R < r)
        # affine form must equal the true iterate for several t
        for t in (1, 2, 3, 7, 1000003):
            n = pk * t + r
            x = n
            for _ in range(j):
                x = T(x)
            assert x == P * t + R, (K, r, j, t)
    return True


def apply_frac(x, p, m, table):
    Q = p ** m
    a, b = x.numerator, x.denominator
    assert b % p != 0
    r = (a * pow(b, -1, Q)) % Q
    u, v, w = table[r]
    y = (u * x + v) / w
    assert y.denominator % p != 0
    return y, r


def padic_cycle_check(x0, p, m, table, maxlen=500):
    """Follow the exact rational p-adic orbit of x0; return (period, A, D)
    where the composed slope over one period is A/D (A = prod u, D = prod w),
    or None if no return within maxlen."""
    x = Fraction(x0)
    A, D = 1, 1
    for L in range(1, maxlen + 1):
        y, r = apply_frac(x, p, m, table)
        u, v, w = table[r]
        A *= u
        D *= w
        x = y
        if x == x0:
            return L, A, D
    return None


def cylinder_graph(p, m, table, extra=2):
    """Nodes: classes (c, l) mod p^l, l <= m+extra.  'Determined' nodes apply
    one step; others split.  Returns step graph among determined nodes."""
    Q = p ** m
    Lmax = m + extra

    def determined(c, l):
        if l >= m:
            return True
        rs = {table[(c + k * p ** l) % Q] for k in range(p ** (m - l))}
        return len(rs) == 1

    def leaves_below(c, l):
        if determined(c, l):
            return [(c, l)]
        out = []
        for s in range(p):
            out += leaves_below(c + s * p ** l, l + 1)
        return out

    det = leaves_below(0, 0)
    seen = set(det)
    work = list(det)
    edges = {}
    while work:
        c, l = work.pop()
        u, v, w = table[c % Q]
        nl = l + vp(u, p) - vp(w, p)
        assert nl >= 0
        img = ((u * c + v) // w) if (u * c + v) % w == 0 else None
        assert img is not None
        nl = min(nl, Lmax)
        img %= p ** nl
        tg = leaves_below(img, nl)
        edges[(c, l)] = [(t, math.log(u / w)) for t in tg]
        for t in tg:
            if t not in seen:
                seen.add(t)
                work.append(t)
    return edges


def max_mean_cycle(edges):
    """Karp's algorithm per strongly connected piece (just run on all nodes
    from a virtual source).  Returns (mean, cycle_nodes)."""
    nodes = list(edges)
    idx = {v: i for i, v in enumerate(nodes)}
    n = len(nodes)
    NEG = -1e300
    D = [[NEG] * n for _ in range(n + 1)]
    par = [[None] * n for _ in range(n + 1)]
    for i in range(n):
        D[0][i] = 0.0
    for k in range(1, n + 1):
        for v in nodes:
            i = idx[v]
            if D[k - 1][i] == NEG:
                continue
            for t, wgt in edges[v]:
                if t not in idx:
                    continue
                j = idx[t]
                val = D[k - 1][i] + wgt
                if val > D[k][j]:
                    D[k][j] = val
                    par[k][j] = i
    best, bv = NEG, None
    for v in range(n):
        if D[n][v] == NEG:
            continue
        worst = min((D[n][v] - D[k][v]) / (n - k) for k in range(n)
                    if D[k][v] != NEG)
        if worst > best:
            best, bv = worst, v
    # recover a cycle by walking parents from (n, bv)
    walk = []
    k, v = n, bv
    while k > 0:
        walk.append(v)
        v = par[k][v]
        k -= 1
    walk.append(v)
    walk.reverse()
    pos = {}
    for i, v in enumerate(walk):
        if v in pos:
            cyc = walk[pos[v]:i]
            return best, [nodes[c] for c in cyc]
        pos[v] = i
    return best, None


def cycle_fixed_point(p, m, table, cyc):
    """Compose the affine steps along a node cycle and return the fixed point."""
    Q = p ** m
    A, B, D = 1, 0, 1   # current map x -> (A x + B)/D
    for (c, l) in cyc:
        u, v, w = table[c % Q]
        # x -> (u*(A x + B)/D + v)/w = (uA x + uB + vD)/(D w)
        A, B, D = u * A, u * B + v * D, D * w
    # fixed point: D x = A x + B  -> x = B/(D - A)
    return Fraction(B, D - A)


def growing_cycle(p, m, table, extra=3):
    edges = cylinder_graph(p, m, table, extra)
    mean, cyc = max_mean_cycle(edges)
    if cyc is None or mean <= 0:
        return dict(mean=mean, cycle=None)
    x = cycle_fixed_point(p, m, table, cyc)
    res = padic_cycle_check(x, p, m, table)
    return dict(mean=mean, cycle=cyc, point=x, check=res)


def odd_markov_drift(m, mult, add=1):
    """Random-model drift per odd step for T(n)=n/2 (even), mult[r]*n+add (odd
    n = r mod 2^m).  Markov chain on odd classes mod 2^m (see lemmas.md, Heuristic)."""
    Q = 2 ** m
    odd = list(range(1, Q, 2))
    P = {r: {} for r in odd}
    W = {}
    for r in odd:
        a = mult[r]
        x = a * r + add
        v = vp(x % Q, 2) if x % Q else m
        if x % Q:
            img = (x >> v) % (Q >> v)          # known mod 2^(m-v)
            lifts = [s for s in odd if s % (Q >> v) == img]
            for s in lifts:
                P[r][s] = 1 / len(lifts)
            W[r] = math.log(a) - v * math.log(2)
        else:
            for s in odd:
                P[r][s] = 1 / len(odd)
            W[r] = math.log(a) - (m + 1) * math.log(2)
    pi = {r: 1 / len(odd) for r in odd}
    for _ in range(5000):
        new = {r: 0.5 * pi[r] for r in odd}
        for r in odd:
            for s, pr in P[r].items():
                new[s] += 0.5 * pi[r] * pr
        pi = new
    return sum(pi[r] * W[r] for r in odd)


def verify_obstruction(p, m, table, x0, maxlen=1000):
    """Exact proof data for Lemma B.  x0 must be a rational with denominator
    prime to p lying on a periodic orbit of the p-adic extension.  Returns
    (L, A, D, y) where A/D > 1 is the multiplier over one period and y is the
    point of the orbit from which every partial multiplier is > 1 (cycle
    lemma), all checked with exact Fractions.  Raises AssertionError
    otherwise."""
    Q = p ** m
    orbit, mults = [Fraction(x0)], []
    x = Fraction(x0)
    for _ in range(maxlen):
        y, r = apply_frac(x, p, m, table)
        u, v, w = table[r]
        mults.append(Fraction(u, w))
        x = y
        if x == orbit[0]:
            break
        orbit.append(x)
    else:
        raise AssertionError("not periodic")
    L = len(mults)
    lam = math.prod(mults)
    assert lam > 1, lam
    # cycle lemma: start just after the LAST minimum of the prefix products
    pref = [Fraction(1)]
    for q in mults:
        pref.append(pref[-1] * q)
    mn = min(pref[:L])
    i0 = max(i for i in range(L) if pref[i] == mn)
    rot = mults[i0:] + mults[:i0]
    acc = Fraction(1)
    for j in range(3 * L):
        acc *= rot[j % L]
        assert acc > 1, (j, acc)
    return L, lam.numerator, lam.denominator, orbit[i0]


def exceptional_set(p, leaves):
    """Positive n not covered by a descent inequality: n = p^K t + r with
    t <= (R - r) // (p^K - P) in a leaf with P < p^K and R >= r."""
    E = []
    for K, r, j, P, R in leaves:
        M = p ** K
        if P < M and R >= r:
            E += [M * t + r for t in range((R - r) // (M - P) + 1) if M * t + r > 0]
    return sorted(E)


def cycles_from(T, starts, cap=10 ** 6):
    """Simulate each start until a value repeats; return the set of cycles
    (as tuples starting at their minimum) and confirm every start ends in one."""
    cycles = set()
    for e in starts:
        seen = {}
        x = e
        i = 0
        while x not in seen:
            seen[x] = i
            x = T(x)
            i += 1
            assert i < cap, e
        c = [x]
        y = T(x)
        while y != x:
            c.append(y)
            y = T(y)
        k = c.index(min(c))
        cycles.add(tuple(c[k:] + c[:k]))
    return cycles


def deepest_leaf_witness(p, m, table, leaf, t=10 ** 12):
    """For the deepest leaf, exhibit n in its class with T^i(n) >= n for every
    i < j (so no shorter descent works on that class)."""
    K, r, j, P, R = leaf
    T = step_fn(p, m, table)
    n = p ** K * t + r
    x = n
    for i in range(1, j):
        x = T(x)
        assert x >= n, (i, x, n)
    x = T(x)
    assert x < n
    return True


def full_certificate_check(sysdict, expect):
    """Shared body of the tier-2 checks: build the minimal stopping-time
    certificate, verify it independently, compute the exceptional set E and
    the cycles reached from E, and compare with `expect`."""
    p, m, tab = sysdict["p"], sysdict["m"], sysdict["table"]
    check_table(p, m, tab)
    c = certificate(p, m, tab, maxK=80)
    assert c["ok"]
    verify_certificate(p, m, tab, c["leaves"])
    got = dict(K=c["K"], k=c["k"], size=c["size"])
    E = exceptional_set(p, c["leaves"])
    cyc = cycles_from(sysdict["step"], E)
    got["E"] = E
    got["cycle_mins"] = sorted(min(x) for x in cyc)
    deep = max(c["leaves"], key=lambda l: l[2])
    deepest_leaf_witness(p, m, tab, deep)
    for key, val in expect.items():
        assert got[key] == val, (key, got[key], val)
    return c, got, cyc, deep
