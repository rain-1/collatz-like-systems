"""Mixed-radix tools for residue-class affine maps (round 3, lens "mixedbase").

A *table map* is (M0, table) with table[r] = (u, v, w) meaning

    n = r (mod M0)   ->   T(n) = (u*n + v) / w        (exact division on the class).

M0 may have several prime factors (e.g. 2*5 = 10), so the map is continuous on
the product  Z_S = prod_{p | M0} Z_p  but in general on no single Z_p.  This is
exactly the situation of Farkas-type maps, which the one-prime engine of
round2/descent cannot see.

Contents
  * step_fn / check_table                      -- the map itself
  * certificate(...)                            -- mixed-radix minimal descent certificate
  * verify_certificate(...)                     -- independent exact re-verification
  * lemma_A(...)                                -- finite exceptional set E and the cycle list
  * growing_cycle(...)                          -- search (floats) + exact verification of an
                                                   expanding periodic point of T^ in Z_S
                                                   (kills every certificate, Lemma B')
All proofs use exact integer / Fraction arithmetic.  Floats only steer searches.
"""
from fractions import Fraction
import math
import random


def primes_of(n):
    out, p = [], 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def step_fn(M0, table):
    def T(n):
        u, v, w = table[n % M0]
        x = u * n + v
        assert x % w == 0, (n, M0)
        return x // w
    return T


def check_table(M0, table, step=None, upto=5000, positive=True):
    """Exact division on every class (checked on a full period of each class via
    the affine identity) and agreement with an independent step function."""
    for r in range(M0):
        u, v, w = table[r]
        # u*(r + M0 t) + v divisible by w for all t  <=>  w | u*r+v and w | u*M0
        assert (u * r + v) % w == 0 and (u * M0) % w == 0, ("inexact class", r)
    T = step_fn(M0, table)
    for n in range(1, upto):
        x = T(n)
        if positive:
            assert x >= 1, ("not positive", n)
        if step is not None:
            assert step(n) == x, ("table != step", n, step(n), x)
    return True


# ----------------------------------------------------------------------------
# mixed-radix descent certificate (Lemma C of round2/descent, several primes)
# ----------------------------------------------------------------------------

def _branch(M0, table, P, Q):
    """If every value P t + Q (t integer) lies in one table row with exact
    division uniform in t, return that row, else None and a prime to split by."""
    g = math.gcd(P, M0)
    rows = {table[(Q + g * i) % M0] for i in range(M0 // g)}
    if len(rows) == 1:
        u, v, w = next(iter(rows))
        if (u * P) % w == 0 and (u * Q + v) % w == 0:
            return (u, v, w), None
    # split t by the smallest prime p dividing M0/g (or M0 if g == M0 but inexact)
    h = M0 // g if g < M0 else M0
    return None, primes_of(h)[0]


def certificate(M0, table, maxnodes=2_000_000, maxdepth=400):
    """Minimal stopping-time certificate in mixed radix.

    Node: n = M t + r (t >= 0) with path = digits [(p, s), ...]; T^j(n) = P t + Q.
    Closed at the first j >= 1 with P < M, or P == M and Q < r.
    Returns dict(ok=True, leaves=[(M, r, j, P, Q, path)]) or dict(ok=False, open=...).
    """
    leaves = []
    stack = [(1, 0, 1, 0, 0, ())]
    nodes = 0
    while stack:
        M, r, P, Q, j, path = stack.pop()
        nodes += 1
        if nodes > maxnodes or j > maxdepth:
            return dict(ok=False, open=(M, r, j, P, Q), nodes=nodes,
                        reason="nodes" if nodes > maxnodes else "depth")
        if j > 0 and (P < M or (P == M and Q < r)):
            leaves.append((M, r, j, P, Q, path))
            continue
        row, p = _branch(M0, table, P, Q)
        if row is not None:
            u, v, w = row
            stack.append((M, r, u * P // w, (u * Q + v) // w, j + 1, path))
        else:
            for s in range(p):
                stack.append((p * M, r + M * s, p * P, Q + P * s, j,
                              path + ((p, s),)))
    return dict(ok=True, leaves=leaves, nodes=nodes)


def verify_certificate(M0, table, leaves, T=None, trials=4):
    """Independent check:
    (1) the digit paths form a complete prefix code (a full trie: every internal
        node has all p children for one prime p), and each leaf's (M, r) is the
        one its path encodes  ==> the leaf classes partition the integers;
    (2) re-derive T^j on each leaf class symbolically, asserting at every step
        that the branch is uniform on the class (so the affine form is valid
        for every t), and compare with the stored (P, Q);
    (3) numeric spot checks of T^j(M t + r) = P t + Q, incl. large t.
    """
    if T is None:
        T = step_fn(M0, table)
    # (1) trie
    children = {}
    leafset = set()
    for (M, r, j, P, Q, path) in leaves:
        MM, rr = 1, 0
        for i, (p, s) in enumerate(path):
            pre = path[:i]
            d = children.setdefault(pre, {})
            d.setdefault(p, set()).add(s)
            assert 0 <= s < p
            rr += MM * s
            MM *= p
        assert (MM, rr) == (M, r), "path does not encode the leaf"
        assert path not in leafset, "duplicate leaf"
        leafset.add(path)
    for pre, d in children.items():
        assert len(d) == 1, "two split primes at one node"
        (p, ss), = d.items()
        assert ss == set(range(p)), "incomplete split"
        assert pre not in leafset, "leaf is also internal"
    if not leaves:
        return False
    # a full trie whose leaves are exactly leafset: every child of an internal
    # node is either internal or a leaf
    internal = set(children)
    for pre, d in children.items():
        (p, ss), = d.items()
        for s in ss:
            c = pre + ((p, s),)
            assert c in internal or c in leafset, "dangling child"
    assert () in internal or () in leafset
    dens = sum(Fraction(1, L[0]) for L in leaves)
    assert dens == 1, dens
    # (2) + (3)
    for (M, r, j, P, Q, path) in leaves:
        PP, QQ = M, r
        for _ in range(j):
            g = math.gcd(PP, M0)
            rows = {table[(QQ + g * i) % M0] for i in range(M0 // g)}
            assert len(rows) == 1
            u, v, w = next(iter(rows))
            assert (u * PP) % w == 0 and (u * QQ + v) % w == 0
            PP, QQ = u * PP // w, (u * QQ + v) // w
        assert (PP, QQ) == (P, Q)
        assert P < M or (P == M and Q < r)
        for t in [0, 1, 2, 7, 1000003] + [random.getrandbits(80) for _ in range(trials)]:
            n = M * t + r
            if n <= 0:
                continue
            x = n
            for _ in range(j):
                x = T(x)
            assert x == P * t + Q, (M, r, t)
    return True


def lemma_A(leaves, positive_start=1):
    """Exceptional set E of Lemma A: all n >= positive_start lying in a leaf with
    t <= floor((Q - r)/(M - P)) (leaves with P < M); leaves with P == M, Q < r
    descend for every t.  Returns sorted list E (may be large; caller checks size)."""
    E = []
    for (M, r, j, P, Q, path) in leaves:
        if P < M:
            tmax = (Q - r) // (M - P) if Q - r >= 0 else -1
            for t in range(0, tmax + 1):
                n = M * t + r
                if n >= positive_start:
                    E.append(n)
    return sorted(set(E))


def cycles_from(T, starts, limit=10 ** 7):
    """Simulate each start until a repeat; return the set of cycles (as tuples
    rotated to start at their minimum).  Raises if an orbit exceeds limit steps."""
    known = {}      # value -> cycle id
    cycles = []
    for s in starts:
        seen = {}
        x = s
        k = 0
        while x not in seen and x not in known:
            seen[x] = k
            x = T(x)
            k += 1
            assert k < limit
        if x in known:
            cid = known[x]
        else:
            cyc = [x]
            y = T(x)
            while y != x:
                cyc.append(y)
                y = T(y)
            i = cyc.index(min(cyc))
            cyc = tuple(cyc[i:] + cyc[:i])
            cid = len(cycles)
            cycles.append(cyc)
            for y in cyc:
                known[y] = cid
        for y in seen:
            known[y] = cid
    return cycles


def prove_global(M0, table, step=None, maxnodes=2_000_000, maxE=10 ** 6):
    """certificate + verification + Lemma A.  Returns a summary dict."""
    check_table(M0, table, step)
    res = certificate(M0, table, maxnodes=maxnodes)
    if not res["ok"]:
        return dict(ok=False, open=res["open"], nodes=res["nodes"], reason=res["reason"])
    leaves = res["leaves"]
    verify_certificate(M0, table, leaves)
    E = lemma_A(leaves)
    assert len(E) <= maxE, len(E)
    T = step_fn(M0, table)
    cyc = cycles_from(T, E)
    return dict(ok=True, nleaves=len(leaves), maxj=max(L[2] for L in leaves),
                maxM=max(L[0] for L in leaves), E=len(E), Emax=max(E) if E else 0,
                cycles=cyc, leaves=leaves)


# ----------------------------------------------------------------------------
# expanding periodic points of T^ on Z_S (obstructions, Lemma B')
# ----------------------------------------------------------------------------

def rat_mod(x, M):
    """x mod M for a rational x whose denominator is coprime to M."""
    x = Fraction(x)
    d = x.denominator
    assert math.gcd(d, M) == 1
    return (x.numerator * pow(d, -1, M)) % M


def verify_periodic(M0, table, x, L):
    """Exactly check that the rational x (denominator coprime to M0) is a
    T^-periodic point of period dividing L; return the multiplier over L steps
    (a Fraction) and the orbit."""
    x = Fraction(x)
    orb = [x]
    lam = Fraction(1)
    y = x
    for _ in range(L):
        u, v, w = table[rat_mod(y, M0)]
        y = (u * y + v) / w
        lam *= Fraction(u, w)
        orb.append(y)
    assert y == x, "not periodic"
    return lam, orb[:-1]


def residue_graph(M0, table, N):
    """Edges of the residue graph mod N (M0 | N): rho -> sigma whenever some
    n = rho (mod N) has T(n) = sigma (mod N); weight log(u/w)."""
    assert N % M0 == 0
    src, dst, wt, row = [], [], [], []
    for rho in range(N):
        u, v, w = table[rho % M0]
        base = (u * rho + v)
        assert base % w == 0
        base //= w
        stepN = u * N // w if (u * N) % w == 0 else None
        assert stepN is not None
        g = math.gcd(stepN, N)
        for i in range(N // g):
            src.append(rho)
            dst.append((base + g * i) % N)
            wt.append(math.log(u / w))
            row.append(rho % M0)
    return src, dst, wt


def growing_cycle(M0, table, N, iters=None, seed_tries=1, exclude=()):
    """Search the residue graph mod N for a cycle of positive log-weight by max-plus
    value iteration with predecessor tracking (floats; search only).  Each
    candidate cycle is turned into the word of branches it follows, the rational
    fixed point of the composed affine map is computed and verify_periodic checks
    it exactly.  Returns (x, L, multiplier) or None."""
    import numpy as np
    src, dst, wt = residue_graph(M0, table, N)
    src = np.array(src); dst = np.array(dst); wt = np.array(wt)
    if iters is None:
        iters = min(4 * N, 3000)
    D = np.zeros(N)
    pred = np.full(N, -1)
    order = np.lexsort((-(D[src] + wt), dst))
    best = None
    for it in range(iters):
        val = D[src] + wt
        # per-destination max
        order = np.lexsort((-val, dst))
        d_sorted = dst[order]
        first = np.ones(len(order), bool)
        first[1:] = d_sorted[1:] != d_sorted[:-1]
        sel = order[first]
        Dn = np.full(N, -np.inf)
        Dn[dst[sel]] = val[sel]
        pred = np.full(N, -1)
        pred[dst[sel]] = src[sel]
        D = Dn - Dn.max()          # normalise
        if it in (iters // 4, iters // 2, iters - 1):
            # find cycles in the predecessor graph
            cand = _pred_cycles(pred)
            for cyc in cand:
                r = _exact_from_residue_cycle(M0, table, N, cyc)
                if r is not None and r[0] in exclude:
                    r = None
                if r is not None and (best is None or r[2] > best[2]):
                    best = r
            if best is not None:
                return best
    return best


def _pred_cycles(pred):
    N = len(pred)
    color = [0] * N
    out = []
    for s in range(N):
        if color[s] or pred[s] < 0:
            continue
        path = []
        x = s
        while x >= 0 and color[x] == 0:
            color[x] = 1
            path.append(x)
            x = pred[x]
        if x >= 0 and color[x] == 1:
            i = path.index(x)
            out.append(path[i:][::-1])     # forward order (pred reversed)
        for y in path:
            color[y] = 2
    return out


def _exact_from_residue_cycle(M0, table, N, cyc):
    """cyc: residues rho_0 -> rho_1 -> ... (forward).  Compose the branches; take
    the rational fixed point; verify exactly; return (x, L, lam) if lam > 1."""
    A, B = Fraction(1), Fraction(0)
    for rho in cyc:
        u, v, w = table[rho % M0]
        A, B = A * Fraction(u, w), (B * u + v) / w
    if A <= 1:
        return None
    x = B / (1 - A)
    if any(x.denominator % p == 0 for p in primes_of(M0)):
        return None
    try:
        lam, orb = verify_periodic(M0, table, x, len(cyc))
    except AssertionError:
        return None
    if lam <= 1:
        return None
    return (x, len(cyc), lam)


def lyndon_words(k, n):
    """Lyndon words over {0..k-1} of length 1..n (Duval's algorithm)."""
    w = [-1]
    while w:
        w[-1] += 1
        yield tuple(w)
        m = len(w)
        while len(w) < n:
            w.append(w[len(w) - m])
        while w and w[-1] == k - 1:
            w.pop()


def word_cycles(M0, rows, maxlen, exclude=(), only_expanding=True):
    """Exact search for T^-periodic points following a word over the distinct
    affine rows.  rows: dict row_id -> (u, v, w, predicate) where predicate(x mod M0)
    says whether that row applies at residue x mod M0.  For each Lyndon word the
    fixed point of the composition is computed and verified by verify-like exact
    simulation.  Returns list of (x, L, lam, orbit)."""
    ids = sorted(rows)
    out = []
    seen = set()
    for wd in lyndon_words(len(ids), maxlen):
        A, B = Fraction(1), Fraction(0)
        for i in wd:
            u, v, w, _ = rows[ids[i]]
            A, B = A * Fraction(u, w), (B * u + v) / w
        if A == 1:
            continue
        if only_expanding and A < 1:
            continue
        x = B / (1 - A)
        if any(x.denominator % p == 0 for p in primes_of(M0)):
            continue
        y = x
        ok = True
        orb = []
        for i in wd:
            u, v, w, pred = rows[ids[i]]
            if not pred(rat_mod(y, M0)):
                ok = False
                break
            orb.append(y)
            y = (u * y + v) / w
        if not ok or y != x:
            continue
        if any(z in exclude for z in orb):
            continue
        key = min(orb)
        if key in seen:
            continue
        seen.add(key)
        out.append((x, len(wd), A, orb))
    return out


def table_rows(M0, table):
    """rows for word_cycles: one row per distinct affine triple of the table."""
    rows = {}
    for i, trip in enumerate(sorted(set(table.values()))):
        rows[i] = trip + ((lambda y, trip=trip: table[y % M0] == trip),)
    return rows
