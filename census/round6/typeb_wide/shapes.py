"""Minimal modulus for type (b): exhaustive enumeration of cylinder-graph shapes.

For a unit-multiplier p-adic table at modulus p^m, the graph G_m and the edge multipliers
depend only on, per class r: the division exponent e_r, the target t_r mod p^(m-e_r)
(the edges are r -> t_r + i p^(m-e_r)), and the multiplier u_r.  Every shape (e_r, t_r)
is realised by a genuine table with any unit u_r >= 1 (choose v_r = w t_r - u_r r plus a
large multiple of p^m for positivity).

Claims checked here (exact, finite):
  [M1] for (p, m) = (2, 1), (3, 1), (5, 1), (7, 1) no shape admits type (b): no unit table
       at modulus p has a type-(b) system;
  [M2] at modulus 4 there are shapes admitting type (b) (128 of 2401), and the explicit
       table sh4 below is a type-(b) system (settled in check_examples.py);
  [M3] with the Collatz convention "n/2 on every even class", no table at modulus 4 is of
       type (b), while sh8 (modulus 8) is; with "n/3 on every class 0 mod 3", modulus 3 is
       impossible by [M1] and acc_h9 (modulus 9) exists.

Reduction used (proved in README, Prop. M): a shape admits a type-(b) table iff
  (i)  G_m has no cycle all of whose edges have e = 0 (else the standing hypothesis fails),
  (ii) some SCC is a simple cycle containing an edge with e >= 1,
  (iii) with u_r = 1 on all classes outside the simple-cycle SCCs, every non-simple SCC
       contracts - automatic under (i): with u = 1 every cycle has multiplier p^-(#div) < 1.
Then u_r = large on that simple cycle makes it expanding.  So only (i) and (ii) are tested.
Exit status 0 iff no such shape exists for the listed (p, m), and some shape exists at
(2, 3) and (3, 2) (sanity: the mod-8 and mod-9 examples of this folder / round 3).
"""
import itertools, sys
sys.setrecursionlimit(10000)


def sccs(N, succ):
    idx, low, on, st, out, c = {}, {}, set(), [], [], [0]

    def go(v):
        idx[v] = low[v] = c[0]
        c[0] += 1
        st.append(v)
        on.add(v)
        for w in succ[v]:
            if w not in idx:
                go(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = st.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            out.append(comp)
    for v in range(N):
        if v not in idx:
            go(v)
    return out


def shapes(p, m):
    Q = p ** m
    per = []
    for r in range(Q):
        o = []
        for e in range(m + 1):
            for t in range(p ** (m - e)):
                o.append((e, t))
        per.append(o)
    return Q, per


def admits_b(p, m, shape, free=None):
    """free: classes whose multiplier u may be chosen (default all); the expanding
    simple cycle must contain a free class, since the others keep u = 1."""
    Q = p ** m
    succ, div = [], []
    for r, (e, t) in enumerate(shape):
        step = p ** (m - e)
        succ.append([t + i * step for i in range(p ** e)])
        div.append(e)
    # (i) no division-free cycle
    z = [succ[r] if div[r] == 0 else [] for r in range(Q)]
    for c in sccs(Q, z):
        if len(c) > 1 or c[0] in z[c[0]]:
            return False
    # (ii) a simple-cycle SCC containing a division
    for c in sccs(Q, succ):
        cs = set(c)
        ed = [(a, b) for a in c for b in succ[a] if b in cs]
        if ed and len(ed) == len(c) and any(div[a] for a in c) and \
                (free is None or any(a in free for a in c)):
            return True
    return False


def count(p, m, stop_first=False):
    Q, per = shapes(p, m)
    n = 0
    ex = None
    for sh in itertools.product(*per):
        if admits_b(p, m, sh):
            n += 1
            ex = ex or sh
            if stop_first:
                break
    return n, ex


ok = True
for p, m in ((2, 1), (3, 1), (5, 1), (7, 1)):
    n, ex = count(p, m)
    print(f"[M1] p={p} m={m}: shapes admitting type (b): {n}")
    ok &= n == 0
n, ex = count(2, 2)
print(f"[M2] p=2 m=2: shapes admitting type (b): {n}, e.g. {ex}")
ok &= n == 128


def shape_of(p, m, tab):
    sh = []
    for r, (u, v, w) in enumerate(tab):
        e = 0
        while w % p ** (e + 1) == 0:
            e += 1
        sh.append((e, ((u * r + v) // w) % p ** (m - e)))
    return sh


SH4 = [(1, 1, 1), (1, 1, 1), (1, 2, 2), (3, 1, 2)]   # n+1, n+1, (n+2)/2, (3n+1)/2 mod 4
ok &= admits_b(2, 2, shape_of(2, 2, SH4))
print("[M2] sh4 admits type (b):", admits_b(2, 2, shape_of(2, 2, SH4)))
# [M3] n/2 on even classes, any shape on the odd classes, modulus 4
Q, per = shapes(2, 2)
per = [[(1, (r // 2) % 2)] if r % 2 == 0 else per[r] for r in range(4)]
n3 = sum(admits_b(2, 2, sh, free={1, 3}) for sh in itertools.product(*per))
print(f"[M3] modulus 4 with n/2 on even classes: shapes admitting type (b): {n3}")
ok &= n3 == 0
SH8 = [(1, 0, 2), (1, 1, 1), (1, 0, 2), (3, 1, 1), (1, 0, 2), (1, 5, 1), (1, 0, 2), (3, 1, 1)]
H9 = [(1, 0, 3), (2, 1, 3), (4, 4, 3), (1, 0, 3), (2, 4, 3), (4, 1, 3), (1, 0, 3), (2, 7, 3), (4, 1, 3)]
a8 = admits_b(2, 3, shape_of(2, 3, SH8), free={1, 3, 5, 7})
a9 = admits_b(3, 2, shape_of(3, 2, H9), free={1, 2, 4, 5, 7, 8})
print("[M3] sh8 admits type (b):", a8, "; acc_h9 admits type (b):", a9)
ok &= a8 and a9
print("ALL PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
