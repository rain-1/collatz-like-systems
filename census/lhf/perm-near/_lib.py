"""Shared exact-integer helpers for the perm-near checks (no floats)."""
import os
import sys
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.abspath(os.path.join(HERE, "..", ".."))
DOWN = os.path.join(CENSUS, "round2", "downfrom5")


def catalog(id):
    """Step function from the round-1 catalog (census/systems.py) or downfrom5."""
    sys.path.insert(0, CENSUS)
    try:
        import systems as s1
        try:
            return s1.get(id)
        except KeyError:
            pass
    finally:
        sys.path.pop(0)
    import importlib.util
    spec = importlib.util.spec_from_file_location("down_systems", os.path.join(DOWN, "systems.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.get(id)


def T(n):
    q, r = divmod(n, 3)
    return 2 * q if r == 0 else (4 * q + 1 if r == 1 else 4 * q + 3)


def Tinv(m):
    if m % 2 == 0:
        return 3 * (m // 2)
    q, r = divmod(m, 4)
    return 3 * q + 1 if r == 1 else 3 * q + 2


def Q(n):
    """swT9_s8: sigma_9 o T, sigma_9 swaps 9 <-> 10 (mod 18)."""
    m = T(n)
    r = m % 18
    return m + 1 if r == 9 else (m - 1 if r == 10 else m)


def residue_graph(P, K, L):
    """Exact successor sets mod K of a map P affine on classes mod L.
    Every edge x -> y is realised by a positive n = x (mod K) with P(n) = y (mod K)."""
    L1 = L // gcd(K, L)
    succ = []
    for x in range(K):
        x0 = x if x > 0 else K
        out = set()
        for t0 in range(L1):
            n0 = x0 + K * t0
            base = P(n0)
            step = P(n0 + K * L1) - base
            g = gcd(K, step)
            out.update(range(base % g, K, g))
        succ.append(out)
    return succ


def reach(adj, s):
    seen = [False] * len(adj)
    seen[s] = True
    st = [s]
    while st:
        v = st.pop()
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True
                st.append(w)
    return all(seen)


def strongly_connected(P, K, L):
    succ = residue_graph(P, K, L)
    if not reach(succ, 0):
        return False
    pred = [[] for _ in range(K)]
    for x, o in enumerate(succ):
        for y in o:
            pred[y].append(x)
    return reach(pred, 0)


def affine_on_classes(P, L, reps=8):
    for r in range(1, L + 1):
        d = P(r + L) - P(r)
        for k in range(1, reps):
            if P(r + (k + 1) * L) - P(r + k * L) != d:
                return False
    return True


def digits(n, b, msd):
    d = []
    while n:
        d.append(n % b)
        n //= b
    return d[::-1] if msd else d


def dfa_search(P, seed, b, s, msd, N=3000, orbitlen=26):
    """Exhaustive (with state-relabelling symmetry breaking) search for a DFA
    with <= s states over base b (MSD- or LSD-first on the canonical digit
    string) whose language rejects seed, accepts P^1..P^orbitlen(seed), and
    satisfies n in L => P(n) in L for all 1 <= n <= N.  Returns a DFA or None.
    None is a proof that no DFA certificate of this size exists."""
    orb, x = [], seed
    for _ in range(orbitlen):
        x = P(x)
        orb.append(x)
    cons = [("rej", digits(seed, b, msd))] + [("acc", digits(y, b, msd)) for y in orb]
    for n in range(1, N + 1):
        cons.append(("imp", digits(n, b, msd), digits(P(n), b, msd)))
    delta = [[None] * b for _ in range(s)]
    sol = []

    def run(ds):
        st = 0
        for d in ds:
            nx = delta[st][d]
            if nx is None:
                return ("need", st, d)
            st = nx
        return ("ok", st)

    def rec(i, acc, used):
        while i < len(cons):
            c = cons[i]
            r = run(c[1])
            if r[0] == "need":
                return branch(i, acc, used, r)
            if c[0] == "imp":
                if acc[r[1]]:
                    r2 = run(c[2])
                    if r2[0] == "need":
                        return branch(i, acc, used, r2)
                    if not acc[r2[1]]:
                        return False
            elif acc[r[1]] != (c[0] == "acc"):
                return False
            i += 1
        sol.append(([row[:] for row in delta], acc))
        return True

    def branch(i, acc, used, r):
        _, st, d = r
        for nx in range(min(used + 1, s)):
            delta[st][d] = nx
            if rec(i, acc, max(used, nx + 1)):
                return True
        delta[st][d] = None
        return False

    for mask in range(2 ** s):
        acc = [(mask >> k) & 1 == 1 for k in range(s)]
        if rec(0, acc, 1):
            return sol[0]
    return None
