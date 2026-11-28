"""Lemma P3 (theorem5_precision3.md): the full-class graph of Q = sigma o G mod 2^i * 9.

G(3q) = 2q, G(3q+1) = 4q+1, G(3q+2) = 4q+3 (the 1932 permutation) and sigma is
any map n -> n + delta(n mod 18) with delta in {-1, 0, 1}, positive on positive
integers (e.g. the swaps sigma_A of round2/downfrom5).

Node y (mod 2^i*9).  Its three subclasses y + 2^i*9*k (k = 0,1,2) mod 2^i*27 each
have a well-defined G-branch and G(n) mod 2^i*18 (difference a*2^i*9 with a in
{2,4}), hence a well-defined Q(n) mod 2^i*9.  Edge y -> Q(y_k) mod 2^i*9.
"""
from math import gcd


def G(n):
    q, r = divmod(n, 3)
    return (2 * q, 4 * q + 1, 4 * q + 3)[r]


def make_sigma(A, M=18):
    up = {a % M for a in A}
    down = {(a + 1) % M for a in A}
    assert not (up & down)

    def s(n):
        r = n % M
        return n + 1 if r in up else (n - 1 if r in down else n)
    return s


def full_class_graph(sig, i):
    N = 2 ** i * 9
    adj = []
    for y in range(N):
        outs = set()
        for k in range(3):
            n = y + N * k
            n = n if n > 0 else 3 * N        # positive representative of the class mod 2^i*27
            outs.add(sig(G(n)) % N)
        adj.append(sorted(outs))
    return adj


def sink_components(adj):
    import sys
    sys.setrecursionlimit(10000)
    N = len(adj)
    index = [None] * N
    low = [0] * N
    onst = [False] * N
    st = []
    comps = []
    c = 0
    for s0 in range(N):
        if index[s0] is not None:
            continue
        work = [(s0, 0)]
        index[s0] = low[s0] = c
        c += 1
        st.append(s0)
        onst[s0] = True
        while work:
            v, pi = work[-1]
            if pi < len(adj[v]):
                work[-1] = (v, pi + 1)
                w = adj[v][pi]
                if index[w] is None:
                    index[w] = low[w] = c
                    c += 1
                    st.append(w)
                    onst[w] = True
                    work.append((w, 0))
                elif onst[w]:
                    low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        w = st.pop()
                        onst[w] = False
                        comp.append(w)
                        if w == v:
                            break
                    comps.append(comp)
    where = [0] * N
    for ci, cp in enumerate(comps):
        for u in cp:
            where[u] = ci
    sinks = [cp for ci, cp in enumerate(comps) if all(where[w] == ci for u in cp for w in adj[u])]
    return sinks


def obstructed(sig, i, seed=8):
    """True iff every sink component of the full-class graph mod 2^i*9 contains
    the class of `seed` (then no separator exists at any modulus 2^i*3^j)."""
    N = 2 ** i * 9
    sinks = sink_components(full_class_graph(sig, i))
    return all(seed % N in set(cp) for cp in sinks), sinks
