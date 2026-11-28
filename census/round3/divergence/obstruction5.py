"""Precision lemma (theorem_precision.md) applied to single-class modifications
of the 5x+1 map  B(n) = n/2 (n even), 5n+1 (n odd).

For a modification T = B except on the class c mod 2^m, where T(n) = (a n + b)/d
with a odd and d a power of 2, the precision lemma says: if the no-halving
subgraph G1 (classes with d = 1) of the residue graph mod 2^m is acyclic, then
every nonempty forward-closed union of residue classes, at ANY modulus 2^K,
contains a nonempty forward-closed union of classes mod 2^m.  So if every sink
strongly connected component of the residue graph mod 2^m contains the class of
a periodic point, no congruence certificate of divergence (cycle-free trap)
exists at any modulus, for any seed.

classify(m, c, rule) returns one of
  'G1-cycle'    : c lies on a no-halving cycle (lemma does not apply),
  'obstructed'  : lemma applies and every sink SCC holds a periodic point,
  'open'        : lemma applies, some sink SCC has no known periodic point.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from divlib import RCWA, modify, images  # noqa: E402

B5 = RCWA(2, [(1, 0, 2), (5, 1, 1)], "5x+1")


def sccs(nodes, adj):
    """Tarjan (iterative). Returns list of components."""
    index = {}
    low = {}
    onst = set()
    st = []
    comps = []
    counter = [0]
    for s in nodes:
        if s in index:
            continue
        work = [(s, iter(adj[s]))]
        index[s] = low[s] = counter[0]
        counter[0] += 1
        st.append(s)
        onst.add(s)
        while work:
            v, it = work[-1]
            w = next(it, None)
            if w is not None:
                if w not in index:
                    index[w] = low[w] = counter[0]
                    counter[0] += 1
                    st.append(w)
                    onst.add(w)
                    work.append((w, iter(adj[w])))
                elif w in onst:
                    low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        w = st.pop()
                        onst.discard(w)
                        comp.append(w)
                        if w == v:
                            break
                    comps.append(comp)
    return comps


def sink_sccs(T, K):
    nodes = list(range(K))
    adj = {u: sorted(set(images(T, K, u))) for u in nodes}
    comps = sccs(nodes, adj)
    where = {}
    for i, cp in enumerate(comps):
        for u in cp:
            where[u] = i
    sinks = []
    for i, cp in enumerate(comps):
        if all(where[v] == i for u in cp for v in adj[u]):
            sinks.append(cp)
    return sinks, adj


def g1_acyclic(T, K, adj):
    nodes = [u for u in range(K) if T.rules[u % T.L][2] == 1]
    ns = set(nodes)
    sub = {u: [v for v in adj[u] if v in ns] for u in nodes}
    comps = sccs(nodes, sub)
    for cp in comps:
        if len(cp) > 1 or cp[0] in sub[cp[0]]:
            return False
    return True


def periodic_points(T, upto=600, cap=4000):
    pts = set()
    for n in range(1, upto):
        seen = {}
        x = n
        for i in range(cap):
            if x in seen:
                y = x
                while True:
                    pts.add(y)
                    y = T(y)
                    if y == x:
                        break
                break
            seen[x] = i
            x = T(x)
            if x > 10 ** 25:
                break
    return pts


def classify(m, c, rule, per_upto=600):
    M = 2 ** m
    T = modify(B5, M, {c: rule})
    sinks, adj = sink_sccs(T, M)
    if not g1_acyclic(T, M, adj):
        return "G1-cycle", T, None
    pts = periodic_points(T, per_upto)
    cls = {p % M for p in pts}
    bad = [cp for cp in sinks if not (set(cp) & cls)]
    if not bad:
        return "obstructed", T, pts
    return "open", T, bad
