"""Core library for the progression (sufficiency) theory of p-shift maps.

A *p-shift map* is given by a prime p, an integer kappa >= 1 and, for every residue
r mod p^kappa, a pair (u_r, v_r) of integers with u_r >= 1, p not dividing u_r and
p | u_r*r + v_r.  It acts on positive integers by

        T(n) = (u_r n + v_r) / p      for n = r (mod p^kappa).

Everything here is exact (Python integers and fractions.Fraction).  See
theorem_A_sufficiency.md for the mathematics; function names follow that file.
"""

from fractions import Fraction as Fr
from math import gcd
from collections import deque
from functools import reduce


# ---------------------------------------------------------------- arithmetic
def lcm(a, b):
    return a // gcd(a, b) * b


def primes_of(n):
    n = abs(n)
    out, q = [], 2
    while q * q <= n:
        if n % q == 0:
            out.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        out.append(n)
    return out


def vp(n, q):
    if n == 0:
        return 10 ** 9
    n, k = abs(n), 0
    while n % q == 0:
        n //= q
        k += 1
    return k


def strip(n, primes):
    """Remove all factors of the given primes from |n|."""
    n = abs(n)
    for q in primes:
        while n and n % q == 0:
            n //= q
    return n


def mult_order(a, m):
    """Multiplicative order of a modulo m (gcd(a, m) = 1); 1 when m = 1."""
    if m == 1:
        return 1
    a %= m
    assert gcd(a, m) == 1
    # order divides lambda(m); compute via factorisation of the group exponent
    lam = carmichael(m)
    o = lam
    for q in primes_of(lam):
        while o % q == 0 and pow(a, o // q, m) == 1:
            o //= q
    return o


def carmichael(m):
    res = 1
    for q in primes_of(m):
        e = vp(m, q)
        if q == 2:
            lam = 1 if e == 1 else (2 if e == 2 else 2 ** (e - 2))
        else:
            lam = (q - 1) * q ** (e - 1)
        res = lcm(res, lam)
    return res


def crt_pair(a1, m1, a2, m2):
    """Solve x = a1 (m1), x = a2 (m2); return (x, lcm) or None."""
    g = gcd(m1, m2)
    if (a2 - a1) % g:
        return None
    l = m1 // g * m2
    k = ((a2 - a1) // g) * pow(m1 // g, -1, m2 // g) % (m2 // g) if m2 // g > 1 else 0
    return (a1 + m1 * k) % l, l


def dlog(base, target, m):
    """Some h >= 0 with base^h = target (mod m), together with ord_m(base); None if none.
    Pohlig-Hellman over the (smooth) group order; exact."""
    base %= m
    target %= m
    if m == 1:
        return 0, 1
    o = mult_order(base, m)
    h, mod = 0, 1
    for q in primes_of(o):
        e = vp(o, q)
        # solve base^(x) = target in the subgroup of order q^e
        oq = o // q ** e
        gq = pow(base, oq, m)       # order q^e
        tq = pow(target, oq, m)
        x = 0
        gamma = pow(gq, q ** (e - 1), m)   # order q
        for k in range(e):
            hk = pow(pow(gq, -x, m) * tq % m, q ** (e - 1 - k), m)
            # find d in [0, q) with gamma^d = hk
            d, acc = None, 1
            for dd in range(q):
                if acc == hk:
                    d = dd
                    break
                acc = acc * gamma % m
            if d is None:
                return None
            x += d * q ** k
        r = crt_pair(h, mod, x, q ** e)
        h, mod = r
    if pow(base, h, m) != target:
        return None
    return h, o


# ---------------------------------------------------------------- affine maps
class Aff:
    """x -> a x + b over Q."""
    __slots__ = ("a", "b")

    def __init__(self, a, b):
        self.a, self.b = Fr(a), Fr(b)

    def __call__(self, x):
        return self.a * x + self.b

    def __matmul__(self, other):          # (self o other)(x) = self(other(x))
        return Aff(self.a * other.a, self.a * other.b + self.b)

    def inv(self):
        return Aff(1 / self.a, -self.b / self.a)

    def __eq__(self, o):
        return self.a == o.a and self.b == o.b

    def __repr__(self):
        return f"x -> {self.a} x + {self.b}"


ID = Aff(1, 0)


def mod_eval(aff, x, m):
    """Evaluate a rational affine map modulo m (denominators must be units mod m)."""
    a = aff.a.numerator * pow(aff.a.denominator, -1, m) % m if m > 1 else 0
    b = aff.b.numerator * pow(aff.b.denominator, -1, m) % m if m > 1 else 0
    return (a * x + b) % m if m > 1 else 0


# ---------------------------------------------------------------- the map class
class PShift:
    def __init__(self, name, p, kappa, table, note=""):
        self.name, self.p, self.kappa = name, p, kappa
        self.P = p ** kappa
        self.S = p ** (kappa - 1)                # number of states
        self.table = {r: (int(table[r][0]), int(table[r][1])) for r in range(self.P)}
        self.note = note
        self.U = sorted({q for (u, v) in self.table.values() for q in primes_of(u)})
        self.bad = sorted(set([p] + self.U))

    # --- the map
    def T(self, n):
        u, v = self.table[n % self.P]
        x = u * n + v
        assert x % self.p == 0
        return x // self.p

    def B(self, r):
        u, v = self.table[r]
        return (u * r + v) // self.p

    # --- validity and hypothesis (A1)
    def validate(self):
        errs = []
        for r, (u, v) in self.table.items():
            if u < 1 or u % self.p == 0:
                errs.append(f"r={r}: u={u} not a positive unit mod p")
            if (u * r + v) % self.p:
                errs.append(f"r={r}: p does not divide u r + v")
            nmin = r if r > 0 else self.P
            if u * nmin + v <= 0:
                errs.append(f"r={r}: T not positive on the class")
        return errs

    def has_dilation(self):
        """(A1): every r = 0 mod p has (u, v) = (1, 0), i.e. T(pn) = n."""
        return all(self.table[r] == (1, 0) for r in range(0, self.P, self.p))

    # --- moves (inverse branches)
    def moves(self):
        if getattr(self, "_moves", None) is not None:
            return self._moves
        out = []
        rad = 1
        for q in self.U:
            rad *= q
        for r in range(self.P):
            u, v = self.table[r]
            src = self.B(r) % self.S
            dst = r % self.S
            if r % self.p == 0:
                kind = "D"
            elif u == 1:
                kind = "I"
            elif rad > 1 and u % rad == 0:
                kind = "E"
            else:
                kind = "X"
            out.append(dict(r=r, u=u, v=v, src=src, dst=dst, kind=kind,
                            aff=Aff(Fr(self.p, u), Fr(-v, u))))
        self._moves = out
        return out

    def move_int(self, m, z):
        """Apply move m to an integer z; None if not admissible."""
        if z % self.S != m["src"]:
            return None
        x = self.p * z - m["v"]
        if x % m["u"]:
            return None
        w = x // m["u"]
        assert w % self.P == m["r"]
        return w

    # --- (A0)
    def state_graph_strongly_connected(self):
        mv = self.moves()
        adj = {s: set() for s in range(self.S)}
        radj = {s: set() for s in range(self.S)}
        for m in mv:
            adj[m["src"]].add(m["dst"])
            radj[m["dst"]].add(m["src"])

        def reach(start, g):
            seen, st = {start}, [start]
            while st:
                x = st.pop()
                for y in g[x]:
                    if y not in seen:
                        seen.add(y)
                        st.append(y)
            return seen
        return len(reach(0, adj)) == self.S and len(reach(0, radj)) == self.S


# ---------------------------------------------------------------- loops and translations
def word_aff(sys_, word):
    """Affine map of a word of moves, applied left to right (first move first)."""
    mv = sys_.moves()
    f = ID
    for i in word:
        f = mv[i]["aff"] @ f
    return f


def fundamental_loops(sys_):
    """For every move e: s_{dst(e)} . e . t_{src(e)}, an actual loop at state 0
    (t_s: BFS path 0 -> s, s_s: BFS path s -> 0). Returns list of (word, Aff)."""
    mv = sys_.moves()
    S = sys_.S
    # forward BFS tree from 0
    tpath = {0: []}
    dq = deque([0])
    while dq:
        s = dq.popleft()
        for i, m in enumerate(mv):
            if m["src"] == s and m["dst"] not in tpath:
                tpath[m["dst"]] = tpath[s] + [i]
                dq.append(m["dst"])
    # backward BFS tree to 0: spath[s] = word from s to 0
    spath = {0: []}
    dq = deque([0])
    while dq:
        s = dq.popleft()
        for i, m in enumerate(mv):
            if m["dst"] == s and m["src"] not in spath:
                spath[m["src"]] = [i] + spath[s]
                dq.append(m["src"])
    assert len(tpath) == S and len(spath) == S
    loops = []
    for i, m in enumerate(mv):
        w = tpath[m["src"]] + [i] + spath[m["dst"]]
        loops.append((w, word_aff(sys_, w)))
    return loops


def translations(sys_, loops, limit=60):
    """Commutators [g, h] = g h g^-1 h^-1 of loops; each is a translation x -> x + t."""
    out = []
    L = loops[:limit]
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            g, h = L[i][1], L[j][1]
            c = g @ h @ g.inv() @ h.inv()
            assert c.a == 1
            if c.b != 0:
                out.append((i, j, c.b))
    # loops of slope one are translations themselves
    for i, (w, f) in enumerate(L):
        if f.a == 1 and f.b != 0:
            out.append((i, i, f.b))
    return out


def delta_from_translations(sys_, trans):
    """gcd of the good parts of the numerators of the translation amounts (0 if none)."""
    d = 0
    for (_, _, t) in trans:
        d = gcd(d, strip(t.numerator, sys_.bad))
    return d


# ---------------------------------------------------------------- the groupoid and the invariant
def groupoid_classes(sys_, Q):
    """Reachability classes of states x Z/Q under all moves (Q coprime to p and U).
    Returns dict (state, residue) -> class id."""
    assert all(Q % q for q in sys_.bad)
    mv = sys_.moves()
    cls = {}
    cid = 0
    maps = []
    for m in mv:
        uinv = pow(m["u"], -1, Q) if Q > 1 else 0
        maps.append((m["src"], m["dst"], uinv, m["v"]))
    adj_cache = {}
    for s in range(sys_.S):
        for z in range(Q):
            if (s, z) in cls:
                continue
            # BFS (reachability is symmetric, see theorem_A_sufficiency.md, Lemma 4)
            cls[(s, z)] = cid
            dq = deque([(s, z)])
            while dq:
                (a, x) = dq.popleft()
                for (src, dst, uinv, v) in maps:
                    if src != a:
                        continue
                    y = ((sys_.p * x - v) * uinv) % Q if Q > 1 else 0
                    if (dst, y) not in cls:
                        cls[(dst, y)] = cid
                        dq.append((dst, y))
            cid += 1
    return cls


def check_symmetric(sys_, Q, cls):
    """Verify that every move maps a class into itself (so classes = weak = strong comps)."""
    mv = sys_.moves()
    for (s, z), c in cls.items():
        for m in mv:
            if m["src"] != s:
                continue
            y = ((sys_.p * z - m["v"]) * pow(m["u"], -1, Q)) % Q if Q > 1 else 0
            if cls[(m["dst"], y)] != c:
                return False
    return True


def divisors(n):
    ds = [1]
    for q in primes_of(n):
        e = vp(n, q)
        ds = [d * q ** k for d in ds for k in range(e + 1)]
    return sorted(ds)


def minimal_invariant(sys_, delta, cls):
    """Smallest divisor d of delta such that the class of (state, z mod delta) depends only on
    (state, z mod d); also whether the state matters at that level."""
    for d in divisors(delta):
        ok = True
        rep = {}
        for (s, z), c in cls.items():
            key = (s, z % d)
            if rep.setdefault(key, c) != c:
                ok = False
                break
        if ok:
            # does the state matter?
            state_free = all(rep[(s, x)] == rep[(0, x)] for (s, x) in rep)
            return d, state_free, rep
    raise AssertionError


# ---------------------------------------------------------------- initial accessibility (IA-cover)
def L_U(sys_):
    L = 1
    for q in sys_.U:
        L *= q ** max(vp(u, q) for (u, v) in sys_.table.values())
    return L


def ia_game(sys_):
    """The finite IA game of theorem_A_sufficiency.md (Section 4).

    Nodes: (state, z mod L2) with L2 = L_U^2.  An *option* at a node is an admissible word
    (I or D moves)* followed by one E move whose U-domain condition holds; its *outcome* is the
    set of nodes (dst, z') with z' = P_E(z1) mod L2/u (all lifts of the known residue).
    Live = greatest set of nodes each having an option whose outcome lies inside Live.
    Returns dict(L, L2, live=set of nodes, enter=set of residues z mod L2 such that
    (0, p^h z) is live for some h >= kappa-1)."""
    L = L_U(sys_)
    L2 = L * L
    mv = sys_.moves()
    iso = [m for m in mv if m["kind"] in ("I", "D")]
    exps = [m for m in mv if m["kind"] == "E"]
    S = sys_.S
    nodes = [(s, z) for s in range(S) for z in range(L2)]
    options = {}
    for nd in nodes:
        seen = {nd}
        st = [nd]
        while st:
            (a, x) = st.pop()
            for m in iso:
                if m["src"] == a:
                    y = (m["dst"], (sys_.p * x - m["v"]) % L2)
                    if y not in seen:
                        seen.add(y)
                        st.append(y)
        opts = set()
        for (a, x) in seen:
            for m in exps:
                if m["src"] == a and (sys_.p * x - m["v"]) % m["u"] == 0:
                    mod = L2 // m["u"]
                    w = ((sys_.p * x - m["v"]) // m["u"]) % mod
                    outcome = frozenset((m["dst"], w + mod * k) for k in range(m["u"]))
                    opts.add(outcome)
        options[nd] = opts
    live = set(nodes)
    while True:
        new = {nd for nd in live if any(o <= live for o in options[nd])}
        if new == live:
            break
        live = new
    enter = set()
    for z in range(L2):
        x = z * pow(sys_.p, sys_.kappa - 1, L2) % L2
        for h in range(L2 + 1):
            if (0, x) in live:
                enter.add(z)
                break
            x = x * sys_.p % L2
    return dict(L=L, L2=L2, live=live, enter=enter)


def find_ia_word(sys_, s, z, L2, live):
    """BFS for a word (I/D moves)* E-move from (s, z mod L2) whose outcome lies in live.
    Returns list of move indices (first move first)."""
    mv = sys_.moves()
    start = (s, z % L2)
    prev = {start: None}
    dq = deque([start])
    while dq:
        nd = dq.popleft()
        (a, x) = nd
        for i, m in enumerate(mv):
            if m["src"] != a or m["kind"] != "E" or (sys_.p * x - m["v"]) % m["u"]:
                continue
            mod = L2 // m["u"]
            w = ((sys_.p * x - m["v"]) // m["u"]) % mod
            if all((m["dst"], w + mod * k) in live for k in range(m["u"])):
                word = [i]
                cur = nd
                while prev[cur] is not None:
                    cur, j = prev[cur]
                    word.append(j)
                return word[::-1]
        for i, m in enumerate(mv):
            if m["src"] != a or m["kind"] not in ("I", "D"):
                continue
            y = (m["dst"], (sys_.p * x - m["v"]) % L2)
            if y not in prev:
                prev[y] = (nd, i)
                dq.append(y)
    return None


def e_image_residues(sys_, m, mod):
    """Residues mod `mod` of B_r(n), n = r (mod p^kappa), for the branch of move m."""
    r, u, v = m["r"], m["u"], m["v"]
    base = (u * r + v) // sys_.p
    step = u * sys_.S
    return {(base + step * k) % mod for k in range(mod)}


def non_E_cycles(sys_):
    """All cycles of T that use no E or X branch.  Requires u_r < p for every I/D branch.
    Such orbits decrease above Bnd = max v_r/(p-u_r), and [1, Bnd] is invariant under them."""
    Bnd = 0
    for r, (u, v) in sys_.table.items():
        m_kind = "D" if r % sys_.p == 0 else ("I" if u == 1 else "EX")
        if m_kind == "EX":
            continue
        assert u < sys_.p
        Bnd = max(Bnd, v // (sys_.p - u))
    cycles = []
    seen = set()
    for n in range(1, Bnd + 1):
        x, path = n, []
        ok = True
        visited = {}
        while x not in visited:
            visited[x] = len(path)
            path.append(x)
            r = x % sys_.P
            u, v = sys_.table[r]
            if r % sys_.p != 0 and u != 1:
                ok = False
                break
            x = sys_.T(x)
            if x > Bnd:
                ok = False
                break
        if ok:
            cyc = path[visited[x]:]
            key = min(cyc)
            if key not in seen:
                seen.add(key)
                cycles.append(cyc)
    return Bnd, cycles


def is_U_unit(sys_, n):
    return all(n % q for q in sys_.U)


# ---------------------------------------------------------------- cycles
def cycle_of(sys_, n, limit=10 ** 6, cap=10 ** 30):
    seen = {}
    x = n
    for k in range(limit):
        if x in seen:
            i = seen[x]
            orb = list(seen.keys())
            return orb[i:]
        seen[x] = k
        x = sys_.T(x)
        if x > cap:
            return None
    return None


def find_cycles(sys_, upto, limit=10 ** 5, cap=10 ** 40):
    cyc = {}
    for n in range(1, upto + 1):
        c = cycle_of(sys_, n, limit, cap)
        if c:
            cyc.setdefault(min(c), c)
    return [cyc[k] for k in sorted(cyc)]
