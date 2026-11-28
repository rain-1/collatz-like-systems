"""schemalib.py -- shared exact tools for part B (approximants), lens 'schema', round 4.

Tables use the round-3 format: modulus Q, table[r] = (u, v, w), n = r (mod Q) ->
(u n + v)/w.  Everything used as proof data is exact (ints / Fractions).
"""
import sys, os, math
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "round3", "dichotomy"))
import decide as DC  # noqa: E402


# ----------------------------------------------------------------- systems

def collatz_table():
    """accelerated 3x+1 on n >= 1: n even -> n/2, n odd -> (3n+1)/2 (Q = 2)."""
    return 2, [(1, 0, 2), (3, 1, 2)]


def k7_table():
    """core K7 of round3/accel/sfamily_obst.md in the coordinate n = z + 1 >= 1:
    n odd -> (n+1)/2  (z even -> z/2);  n = 0 mod 4 -> 3n/2  (z = 3 mod 4 -> (3z+1)/2);
    n = 2 mod 4 -> (n+2)/4  (z = 1 mod 4 -> (z-1)/4).  Q = 4.  Expanding fixed point
    n = 0 (z = -1), multiplier 3/2."""
    return 4, [(3, 0, 2), (1, 1, 2), (1, 2, 4), (1, 1, 2)]


def k7_z(z):
    if z % 2 == 0:
        return z // 2
    if z % 4 == 3:
        return (3 * z + 1) // 2
    return (z - 1) // 4


def lift(Q, table, Q2):
    assert Q2 % Q == 0
    return [table[r % Q] for r in range(Q2)]


def reset(Q, r):
    """n -> floor(n/Q) + 1 on the class r mod Q, as (u, v, w)."""
    return (1, (Q - r) % Q if r else 0, Q) if r else (1, 0, Q)


def step(Q, table):
    return DC.step_fn(Q, table)


# ----------------------------------------------------------------- SCC tools

def sccs(Q, succ):
    """Iterative Tarjan on nodes 0..Q-1 with successor lists succ."""
    index, low, onst, st, out = {}, {}, set(), [], []
    counter = 0
    for root in range(Q):
        if root in index:
            continue
        stack = [(root, iter(succ[root]))]
        index[root] = low[root] = counter
        counter += 1
        st.append(root)
        onst.add(root)
        while stack:
            v, it = stack[-1]
            pushed = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    st.append(w)
                    onst.add(w)
                    stack.append((w, iter(succ[w])))
                    pushed = True
                    break
                elif w in onst:
                    low[v] = min(low[v], index[w])
            if pushed:
                continue
            stack.pop()
            if stack:
                low[stack[-1][0]] = min(low[stack[-1][0]], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = st.pop()
                    onst.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                out.append(comp)
    return out


def type_c_witness(Q, table, cyc):
    """Exact check that the closed walk `cyc` of G_T (level Q) is a cycle with
    multiplier > 1 lying in an SCC that has an internal edge not on the cycle,
    i.e. the SCC is of type (c) (accel/trichotomy.md).  Returns (U, W, size of SCC,
    extra edge) or raises."""
    succ = DC.residue_graph(Q, table)
    assert DC.is_graph_cycle(succ, cyc)
    U, W = DC.cycle_multiplier(table, cyc)
    assert U > W, "cycle does not expand"
    comp = next(c for c in sccs(Q, succ) if cyc[0] in c)
    cs = set(comp)
    assert set(cyc) <= cs
    cedges = set(zip(cyc, cyc[1:] + cyc[:1]))
    extra = [(a, b) for a in comp for b in succ[a] if b in cs and (a, b) not in cedges]
    assert extra, "SCC is the single cycle (type b)"
    return U, W, len(comp), extra[0]


def no_division_free_cycle(Q, table):
    """Standing hypothesis of trichotomy.md: every cycle of G_T contains a division
    (w > 1).  Exact: the nodes with w = 1 have out-degree 1; check that following
    them never closes a loop."""
    succ = DC.residue_graph(Q, table)
    for r in range(Q):
        seen, x = set(), r
        while table[x][2] == 1:
            if x in seen:
                return False
            seen.add(x)
            x = succ[x][0]
    return True
