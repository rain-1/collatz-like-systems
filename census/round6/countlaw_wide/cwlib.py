"""cwlib: the count law for general unit-multiplier p-adic table maps (round 6, lens countlaw_wide).

A system is a table on residues mod Q = p^k: n = r mod Q  ->  (u_r n + v_r) / p^{e_r}, exact division,
with u_r = g^{a_r} for one integer g >= 2 coprime to p ("single generator", hypothesis SG).

Digit tree (round3/density/theory.md Lemma 1; round5/fourier rb.c): with s known low digits of the current
value x, a step is applied iff every residue mod Q congruent to x mod p^min(s,k) uses the same row; it
consumes e digits.  A node state is sigma = (s, c), c = x mod p^s.  The slope after t steps is
g^{A_t} / p^{E_t}; a residue r mod p^b "survives b digits" (slope sense) iff every decided step has
g^{A_t} >= p^{E_t}.  R_b = set of survivors, P(b) = |R_b| / p^b, N(X, b) = #{0 <= n < X : n mod p^b in R_b}.

Everything here is exact integer arithmetic unless a function name says "float".
"""
from fractions import Fraction
from functools import lru_cache
import math

# ----------------------------------------------------------------------------------------------------------
# systems


def s_family(S, m=3, d=1):
    Q = 2 ** m
    return [(1, 0, 1) if r % 2 == 0 else ((3, d, 0) if r in S else (1, d, 0)) for r in range(Q)]


SYS = {
    # 3x+d controls (Terras n-form; one digit = one halving)
    "3x+1": dict(p=2, k=1, g=3, rows=[(1, 0, 1), (3, 1, 0)]),
    "3x-1": dict(p=2, k=1, g=3, rows=[(1, 0, 1), (3, -1, 0)]),
    "3x+5": dict(p=2, k=1, g=3, rows=[(1, 0, 1), (3, 5, 0)]),
    "5x+1": dict(p=2, k=1, g=5, rows=[(1, 0, 1), (5, 1, 0)]),
    # K7 in z-form (round4/integrality/k7.md; round5/fourier rb.c system 2)
    "K7": dict(p=2, k=2, g=3, rows=[(1, 0, 1), (1, -1, 2), (1, 0, 1), (3, 1, 1)]),
    # S-family cores in n-form: odd n -> 3n+1 if n mod 8 in S else n+1 (round3/accel/sfamily_obst.md)
    "sf3_7": dict(p=2, k=3, g=3, rows=s_family({7})),
    "sf3_17": dict(p=2, k=3, g=3, rows=s_family({1, 7})),
    "sf3_57": dict(p=2, k=3, g=3, rows=s_family({5, 7})),
    "sf3_157": dict(p=2, k=3, g=3, rows=s_family({1, 5, 7})),
    "sf3_357": dict(p=2, k=3, g=3, rows=s_family({3, 5, 7})),
    "sf3_137": dict(p=2, k=3, g=3, rows=s_family({1, 3, 7})),
    "sf3_13": dict(p=2, k=3, g=3, rows=s_family({1, 3})),
    "sf3_135": dict(p=2, k=3, g=3, rows=s_family({1, 3, 5})),
    # split maps
    "split5_1": dict(p=2, k=2, g=5, rows=[(1, 0, 1), (5, 1, 0), (1, 0, 1), (1, 1, 0)]),
    "split5_3": dict(p=2, k=2, g=5, rows=[(1, 0, 1), (5, 3, 0), (1, 0, 1), (1, 3, 0)]),
    "desc_split7_1": dict(p=2, k=2, g=7, rows=[(1, 0, 1), (7, 1, 0), (1, 0, 1), (1, 1, 0)]),
    "desc_s32_plus9": dict(p=2, k=5, g=3,
                           rows=s_family({1, 3, 5, 7, 9, 11, 13, 15, 17, 21, 23, 25, 29}, m=5)),
    # base 3
    "m3_b": dict(p=3, k=1, g=4, rows=[(1, 0, 1), (4, -1, 1), (4, 1, 1)]),
    "m3_d": dict(p=3, k=1, g=4, rows=[(1, 0, 1), (4, 2, 0), (4, 1, 0)]),
    "m3_g": dict(p=3, k=1, g=5, rows=[(1, 0, 1), (5, 1, 0), (5, 2, 0)]),
    "m3_e": dict(p=3, k=1, g=7, rows=[(1, 0, 1), (7, 2, 0), (7, 1, 0)]),
    "desc_m3_4n5": dict(p=3, k=1, g=2, rows=[(1, 0, 1), (4, 5, 0), (2, 2, 0)]),
    # a permutation (positive log-drift), base 3: 3q->2q, 3q+1->4q+1, 3q+2->4q+3
    "perm_1932": dict(p=3, k=1, g=2, rows=[(2, 0, 1), (4, -1, 1), (4, 1, 1)]),
}


def log_exact(g, u):
    a = 0
    x = 1
    while x < u:
        x *= g
        a += 1
    assert x == u, (g, u)
    return a


class System:
    def __init__(self, name, maxchain=10000):
        d = SYS[name]
        self.name = name
        self.p, self.k, self.g = d["p"], d["k"], d["g"]
        self.Q = self.p ** self.k
        self.rows = d["rows"]
        assert len(self.rows) == self.Q and math.gcd(self.g, self.p) == 1
        for r, (u, v, e) in enumerate(self.rows):
            assert u >= 1 and math.gcd(u, self.p) == 1
            for n in range(r, r + 3 * self.Q, self.Q):          # exactness on the class
                assert (u * n + v) % self.p ** e == 0, (name, r)
            assert (u * self.Q) % self.p ** e == 0
        self.arow = [log_exact(self.g, u) for (u, v, e) in self.rows]
        # H0: rows with a = e = 0 have v >= 0
        self.H0 = all(v >= 0 for (u, v, e), a in zip(self.rows, self.arow) if a == 0 and e == 0)
        self.V = max(abs(v) for (u, v, e) in self.rows)
        self.maxchain = maxchain
        self._build()

    # decided row for (s, c) or None
    def decide(self, s, c):
        p, k = self.p, self.k
        if s >= k:
            return c % self.Q
        ps = p ** s
        rr = None
        for r in range(c % ps, self.Q, ps):
            if rr is None:
                rr = r
            elif self.rows[r] != self.rows[rr]:
                return None
        return rr

    def chain(self, s, c):
        """apply decided steps to value known mod p^s (= c); return (steps, s', c') with steps a list of
        cumulative (a, e) after each step"""
        steps = []
        A = E = 0
        while True:
            r = self.decide(s, c)
            if r is None:
                return steps, s, c
            u, v, e = self.rows[r]
            x = u * c + v
            assert x % self.p ** e == 0
            x //= self.p ** e
            s -= e
            c = x % self.p ** s
            A += self.arow[r]
            E += e
            steps.append((A, E))
            if len(steps) > self.maxchain:
                raise RuntimeError("infinite chain of decided steps")

    def _build(self):
        p = self.p
        root = (0, 0)
        steps0, s0, c0 = self.chain(0, 0)
        assert not steps0
        self.root = root
        self.trans = {}
        todo = [root]
        seen = {root}
        while todo:
            st = todo.pop()
            s, c = st
            out = []
            for dg in range(p):
                steps, s1, c1 = self.chain(s + 1, c + dg * p ** s)
                out.append(((s1, c1), steps))
                if (s1, c1) not in seen:
                    seen.add((s1, c1))
                    todo.append((s1, c1))
            self.trans[st] = out
        self.states = sorted(seen)
        # states reachable from the root in >= 1 digit (closed under transitions)
        rec = set()
        frontier = {t[0] for t in self.trans[root]}
        while frontier:
            rec |= frontier
            frontier = {t[0] for st in frontier for t in self.trans[st]} - rec
        self.states1 = sorted(rec)

    # ---------------------------------------------------------------------------------------------- thresholds
    @lru_cache(maxsize=None)
    def amin(self, E):
        """least A >= 0 with g^A >= p^E"""
        if E <= 0:
            return 0
        A = int(E * math.log(self.p) / math.log(self.g))
        A = max(A - 2, 0)
        pe = self.p ** E
        x = self.g ** A
        while x < pe:
            x *= self.g
            A += 1
        while A > 0 and x // self.g >= pe:
            x //= self.g
            A -= 1
        return A

    def passes(self, A, E, steps):
        return all(A + a >= self.amin(E + e) for (a, e) in steps)

    # ---------------------------------------------------------------------------------------------- DP counts
    def dp(self, depth, start=None, A0=0, E0=0, keep=None):
        """counts of alive nodes after j digits, keyed (state, A); E = E0 + j - s + s_start.
        start: start state (default root).  Returns list of dicts for j = 0..depth if keep is None,
        else only the depths in keep (dict depth -> counts)."""
        st0 = self.root if start is None else start
        cur = {(st0, A0): 1}
        s_start = st0[0]
        res = {} if keep is not None else []
        if keep is None:
            res.append(dict(cur))
        elif 0 in keep:
            res[0] = dict(cur)
        for j in range(depth):
            nxt = {}
            for (st, A), cnt in cur.items():
                E = E0 + j + s_start - st[0]
                for (st1, steps) in self.trans[st]:
                    if steps:
                        if not self.passes(A, E, steps):
                            continue
                        a, e = steps[-1]
                    else:
                        a, e = 0, 0
                    key = (st1, A + a)
                    assert E + e == E0 + (j + 1) + s_start - st1[0]
                    nxt[key] = nxt.get(key, 0) + cnt
            cur = nxt
            if keep is None:
                res.append(dict(cur))
            elif j + 1 in keep:
                res[j + 1] = dict(cur)
        return res

    def surv_counts(self, depth):
        """|R_b| for b = 0..depth (exact)"""
        return [sum(c.values()) for c in self.dp(depth)]

    # ---------------------------------------------------------------------------------------------- brute force
    def node_survives(self, r, b):
        """slope survival of residue r mod p^b (b known digits): all decided steps g^A >= p^E"""
        steps, s, c = self.chain(b, r % self.p ** b)
        return all(a_ >= 0 for a_ in [0]) and self.passes(0, 0, steps)

    def node_survives_actual(self, n, b):
        """actual survival of the integer n >= 1 over the steps decided by its b low digits:
        T^i(n) >= n for every decided step i"""
        steps, s, c = self.chain(b, n % self.p ** b)
        x = n
        for _ in steps:
            u, v, e = self.rows[x % self.Q]
            x = (u * x + v) // self.p ** e
            if x < n:
                return False
        return True

    # ---------------------------------------------------------------------------------------------- pressure
    def digit_moves(self):
        """per state: list of (next state, a, e) for each digit (total over the chain)"""
        out = {}
        for st in self.states:
            out[st] = [(st1, steps[-1][0] if steps else 0, steps[-1][1] if steps else 0)
                       for (st1, steps) in self.trans[st]]
        return out


def index_of_g(p, g, L):
    """[(Z/p^L)^* : <g mod p^L>]"""
    P = p ** L
    o = 1
    x = g % P
    while x != 1:
        x = x * g % P
        o += 1
    phi = P - P // p
    assert phi % o == 0
    return phi // o, o


def order_mod(g, P):
    o = 1
    x = g % P
    while x != 1:
        x = x * g % P
        o += 1
    return o
