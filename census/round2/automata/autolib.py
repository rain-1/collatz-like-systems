"""Shared exact tools for the automata lens (round 2).

Conventions
-----------
A *branch* (u, r, v, s) means   u*q + r  ->  v*q + s   for every integer q >= 0
(u >= 1, 0 <= r < u, v >= 1, s >= 0).  A map is a list of branches whose
input classes partition the positive integers.

A *DFA* is dict(base=b, delta=[[...], ...], acc=set_of_states); state 0 is the
start state.  It reads the canonical base-b expansion of a positive integer,
most significant digit first.  Its behaviour on words with a leading zero is
irrelevant ("don't care"), and the number of states is len(delta).  A DFA
*certifies NONRETURN of seed s* when its accepted set C satisfies
    T(C) subset of C,   s not in C,   T(s) in C.
By induction every T^n(s), n >= 1, lies in C, so none equals s.

closure_violation() decides T(C) subset of C exactly (all q >= 0, no
sampling): it runs the synchronous least-significant-digit-first product of
the two affine maps q -> u q + r and q -> v q + s with the reversed (subset)
automaton of C, so the search space is finite (bounded carries, finitely
many state subsets).
"""

from collections import deque


# ---------------------------------------------------------------- maps ----
def suffix_branches(rules):
    """Binary suffix rules [(a, b), ...] (strings) -> affine branches."""
    return [(1 << len(a), int(a, 2), 1 << len(b), int(b, 2)) for a, b in rules]


def check_partition(branches):
    """Input classes partition the positive integers (exact: one period)."""
    from math import lcm
    L = 1
    for u, r, v, s in branches:
        assert u >= 1 and 0 <= r < u and v >= 1 and s >= 0
        L = lcm(L, u)
    for n in range(L, 2 * L):           # one full period of residues
        hits = [b for b in branches if n % b[0] == b[1]]
        assert len(hits) == 1, (n, hits)
    return True


def make_step(branches):
    def step(n):
        for u, r, v, s in branches:
            if n % u == r:
                return v * ((n - r) // u) + s
        raise AssertionError(n)
    return step


# ---------------------------------------------------------------- DFAs ----
def digits(n, base):
    out = []
    while n:
        n, d = divmod(n, base)
        out.append(d)
    return out[::-1]


def run(dfa, n, state=0):
    for d in digits(n, dfa["base"]):
        state = dfa["delta"][state][d]
    return state


def accepts(dfa, n):
    return n > 0 and run(dfa, n) in dfa["acc"]


def run_word(dfa, word, state=0):
    for ch in word:
        state = dfa["delta"][state][int(ch, 36)]
    return state


def _zero_tolerant(dfa):
    """Add a fresh start S looping on 0, so padded words read like canonical ones."""
    b = dfa["base"]
    delta = [list(row) for row in dfa["delta"]]
    S = len(delta)
    delta.append([S] + [dfa["delta"][0][d] for d in range(1, b)])
    return delta, set(dfa["acc"]), S


def closure_violation(dfa, branches, max_states=2_000_000):
    """Return (x, y) with x in C, y = T(x) not in C, or None if T(C) <= C.

    Exact for every q >= 0.  Explores (carry_x, carry_y, Rx, Ry) where Rx is the
    set of states p of the zero-tolerant DFA such that reading the low digits
    already produced (in MSB order) from p ends in an accepting state.
    """
    b = dfa["base"]
    delta, acc, S = _zero_tolerant(dfa)
    nst = len(delta)
    pre = [[[p for p in range(nst) if delta[p][d] == t] for t in range(nst)]
           for d in range(b)]

    def back(R, d):
        out = set()
        for t in R:
            out.update(pre[d][t])
        return frozenset(out)

    F = frozenset(acc)
    for (u, r, v, s) in branches:
        start = (r, s, F, F)
        parent = {start: None}
        queue = deque([start])
        while queue:
            st = queue.popleft()
            cx, cy, X, Y = st
            if cx == 0 and cy == 0 and S in X and S not in Y:
                # rebuild q (digits LSB first along parents)
                qd = []
                node = st
                while parent[node] is not None:
                    node, e = parent[node]
                    qd.append(e)
                q = 0
                for e in reversed(qd):
                    q = q * b + e
                x, y = u * q + r, v * q + s
                if x > 0:
                    return x, y
            for e in range(b):
                tx, ty = u * e + cx, v * e + cy
                nxt = (tx // b, ty // b, back(X, tx % b), back(Y, ty % b))
                if nxt not in parent:
                    parent[nxt] = (st, e)
                    if len(parent) > max_states:
                        raise RuntimeError("state budget exceeded")
                    queue.append(nxt)
    return None


def certifies(dfa, branches, seed):
    step = make_step(branches)
    if accepts(dfa, seed):
        return "seed accepted"
    if not accepts(dfa, step(seed)):
        return "T(seed) rejected"
    v = closure_violation(dfa, branches)
    if v is not None:
        return f"closure fails at {v[0]} -> {v[1]}"
    return None


def minimize(dfa):
    """Moore minimisation of the reachable part (language on all words)."""
    b, delta, acc = dfa["base"], dfa["delta"], dfa["acc"]
    reach, todo = {0}, [0]
    while todo:
        p = todo.pop()
        for q in delta[p]:
            if q not in reach:
                reach.add(q)
                todo.append(q)
    states = sorted(reach)
    cls = {p: int(p in acc) for p in states}
    while True:
        sig = {p: (cls[p],) + tuple(cls[delta[p][d]] for d in range(b)) for p in states}
        ids = {}
        new = {}
        for p in states:
            new[p] = ids.setdefault(sig[p], len(ids))
        if len(ids) == len(set(cls.values())):
            cls = new
            break
        cls = new
    # renumber so start is 0
    order = {cls[0]: 0}
    for p in states:
        order.setdefault(cls[p], len(order))
    n = len(order)
    nd = [[0] * b for _ in range(n)]
    nacc = set()
    for p in states:
        i = order[cls[p]]
        nd[i] = [order[cls[delta[p][d]]] for d in range(b)]
        if p in acc:
            nacc.add(i)
    return dict(base=b, delta=nd, acc=nacc)


# ------------------------------------------------------ lower bounds -------
def check_fooling_set(base, words, witnesses, in_fwd, in_bwd):
    """Verify a fooling set: words pairwise separated.

    witnesses[(i, j)] = (z, which) where `which` in {0, 1}: 0 means
    words[i]+z is forced IN (in_fwd) and words[j]+z forced OUT (in_bwd);
    1 means the reverse.  Words are digit strings, empty or not starting
    with '0'.  Any certificate DFA then needs >= len(words) states.
    """
    for w in words:
        assert w == "" or w[0] != "0"
    m = len(words)
    for i in range(m):
        for j in range(i + 1, m):
            z, which = witnesses[(i, j)]
            a, c = words[i] + z, words[j] + z
            assert a and a[0] != "0" and c and c[0] != "0", (i, j)
            na, nc = int(a, base), int(c, base)
            if which == 0:
                assert in_fwd(na) and in_bwd(nc), (i, j, z)
            else:
                assert in_bwd(na) and in_fwd(nc), (i, j, z)
    return m


# ------------------------------------------- exhaustive small-k refutation --
def exhaust(base, branches, seed, k, N, fwd=(), bwd=(), want_all=False):
    """Decide whether some DFA with <= k states certifies NONRETURN of seed.

    Complete backtracking over transition tables (states numbered in order of
    first use, which loses no generality), driven by the trie of the sample
    S = {1..N} u fwd u bwd u {seed, T seed}.  Pruning uses only necessary
    conditions: n in C => T(n) in C for n, T(n) in S; fwd forced in, bwd and
    seed forced out, T(seed) forced in.  Every surviving complete table and
    every consistent choice of accepting states is then checked EXACTLY with
    closure_violation.  Returns a certificate DFA, or None if none exists
    (then no certificate with <= k states exists at all).
    """
    step = make_step(branches)
    sample = set(range(1, N + 1)) | set(fwd) | set(bwd) | {seed, step(seed)}
    words = {n: digits(n, base) for n in sample}
    # trie
    node_of = {}
    children = [{}]
    parent = [None]
    pdigit = [None]
    for n in sorted(sample, key=lambda m: (len(words[m]), m)):
        v = 0
        for d in words[n]:
            if d not in children[v]:
                children[v][d] = len(children)
                children.append({})
                parent.append(v)
                pdigit.append(d)
            v = children[v][d]
        node_of[n] = v
    order = list(range(1, len(children)))
    order.sort(key=lambda v: (_depth(parent, v), v))
    pairs = [(node_of[n], node_of[step(n)]) for n in sample if step(n) in sample]
    force1 = [node_of[step(seed)]] + [node_of[n] for n in fwd]
    force0 = [node_of[seed]] + [node_of[n] for n in bwd]
    # constraints indexed by node, applied once both ends have states
    cons_at = {}
    for a, b in pairs:
        cons_at.setdefault(a, []).append((a, b))
        cons_at.setdefault(b, []).append((a, b))
    f1_at, f0_at = {}, {}
    for v in force1:
        f1_at.setdefault(v, []).append(v)
    for v in force0:
        f0_at.setdefault(v, []).append(v)

    delta = [[None] * base for _ in range(k)]
    st = [None] * len(children)
    st[0] = 0
    imp = [set() for _ in range(k)]     # imp[p] : p accepting => q accepting
    must1, must0 = set(), set()

    def consistent():
        # propagate from must1 along imp; must not hit must0
        seen = set(must1)
        todo = list(must1)
        while todo:
            p = todo.pop()
            if p in must0:
                return False
            for q in imp[p]:
                if q not in seen:
                    seen.add(q)
                    todo.append(q)
        return True

    results = []

    def finish(used):
        # complete every unassigned transition of a k-state table, then try
        # every accepting set compatible with the forced labels
        free = [(p, d) for p in range(k) for d in range(base) if delta[p][d] is None]

        def comp(i):
            if i == len(free):
                yield
                return
            p, d = free[i]
            for q in range(k):
                delta[p][d] = q
                yield from comp(i + 1)
            delta[p][d] = None

        for _ in comp(0):
            for mask in range(1 << k):
                acc = {p for p in range(k) if mask >> p & 1}
                if not must1 <= acc or acc & must0:
                    continue
                if any(p in acc and not imp[p] <= acc for p in range(k)):
                    continue
                dfa = dict(base=base, delta=[list(delta[p]) for p in range(k)], acc=acc)
                if certifies(dfa, branches, seed) is None:
                    results.append(dfa)
                    return True
        return False

    def rec(i, used):
        if i == len(order):
            return finish(used)
        v = order[i]
        p, d = st[parent[v]], pdigit[v]
        choices = [delta[p][d]] if delta[p][d] is not None else range(min(used + 1, k))
        for q in choices:
            newly = delta[p][d] is None
            if newly:
                delta[p][d] = q
            st[v] = q
            added = []
            ok = True
            for a, b in cons_at.get(v, ()):
                if st[a] is not None and st[b] is not None and st[b] not in imp[st[a]]:
                    imp[st[a]].add(st[b])
                    added.append((st[a], st[b]))
            m1 = [st[v]] if v in f1_at and st[v] not in must1 else []
            m0 = [st[v]] if v in f0_at and st[v] not in must0 else []
            must1.update(m1)
            must0.update(m0)
            if consistent():
                if rec(i + 1, max(used, q + 1)):
                    return True
            for a, b in added:
                imp[a].discard(b)
            must1.difference_update(m1)
            must0.difference_update(m0)
            st[v] = None
            if newly:
                delta[p][d] = None
        return False

    rec(0, 1)
    return results[0] if results else None


def _depth(parent, v):
    d = 0
    while parent[v] is not None:
        v = parent[v]
        d += 1
    return d
