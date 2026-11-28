"""check_gaussian.py -- exact checks for gaussian.md.

Claims checked:
  G0  basic facts: V(z) = z/pi or (z+c)/pi satisfies V(z) = pi^{-1} z (mod c);
      the c = 1 map has exactly the cycles {0} and {-i} (window enumeration).
  G1  the finite-graph lemmas of Theorem G:
      (a) difference graph Gamma on {q : 1 <= N(q) <= 5}: the nodes lying on
          closed walks are exactly the hexagon {-1,-1+i,i,1,1-i,-i};
      (b) the triple product graph: every node on a closed walk has exactly one
          outgoing edge inside the closed-walk part, the closed walks are two
          6-cycles, and along each the three parity words are rotations of a
          single word (000111).
  G2  for every odd c with |Re c|, |Im c| <= 9 (Im c >= 0): the complete cycle list
      of T_c (window of Theorem N'), the zero orbit carries exactly the cycles
      {0} and {-ic}, every nonzero <pi>-orbit of Z[i]/(c) carries 1 or 2 cycles,
      and for z in a box the basin follows the residue orbit whenever that orbit
      carries one cycle.  Prints the statistics.
  G3  other unit multipliers u in {i, -1, -i}: complete cycle lists (Theorem N').
  G4  Gaussian 5x+1 (u = 1+2i, c = 1): z = i is a fixed point of the block
      (u z + 1)/pi with archimedean multiplier |u/pi| = sqrt(5/2) > 1 (Lemma B
      obstruction, exact); evidence: orbit sizes of a few seeds after 20000 steps.
  G5  the naive lift z/2 or z+1: z = i (mod 2) or 1+i (mod 2) never becomes
      divisible by 2 and Re z increases by 1 per step (exact on a box).
Runs in about 60 s.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rings as RG  # noqa: E402

G = RG.GAUSS
PI = (1, 1)


def V(z, c):
    if G.divides(PI, z):
        return G.div(z, PI)
    return G.div(G.add(z, c), PI)


def red(z, c):
    """canonical representative of z mod c: z - c*round(z/c)"""
    N = G.norm(c)
    num = G.mul(z, G.conj(c))
    q = ((2 * num[0] + N) // (2 * N), (2 * num[1] + N) // (2 * N))
    return G.add(z, G.neg(G.mul(q, c)))


def residues(c):
    N = G.norm(c)
    L = int(N ** 0.5) + 2
    S = {red((a, b), c) for a in range(-2 * L, 2 * L + 1) for b in range(-2 * L, 2 * L + 1)}
    assert len(S) == N
    return S


def orbits(c):
    S = residues(c)
    seen, out = set(), []
    for r in sorted(S):
        if r in seen:
            continue
        o, x = set(), r
        while x not in o:
            o.add(x)
            x = red(G.mul(x, PI), c)
        seen |= o
        out.append(frozenset(o))
    return out


def G0():
    for c in [(1, 0), (3, 0), (2, 1), (5, 4), (-7, 2)]:
        for a in range(-20, 21):
            for b in range(-20, 21):
                z = (a, b)
                # pi * V(z) = z (mod c)
                assert red(G.add(G.mul(PI, V(z, c)), G.neg(z)), c) == (0, 0)
    T1 = RG.PiMap(G, {1: ((1, 0), (1, 0))})
    cyc = RG.all_cycles(T1)
    assert [tuple(sorted(c)) for c in cyc] == [((0, 0),), ((0, -1), (1, -1))], cyc
    print('G0 OK')


def divpi(q):
    a, b = q
    if (a + b) % 2:
        return None
    return ((a + b) // 2, (b - a) // 2)


def closed_walk_nodes(nodes, succ):
    """Nodes lying on some closed walk: nodes in a nontrivial SCC (Tarjan-free:
    v is on a closed walk iff v is reachable from one of its successors)."""
    out = set()
    for v in nodes:
        st, seen = [w for w in succ(v) if w in nodes], set()
        while st:
            x = st.pop()
            if x in seen:
                continue
            seen.add(x)
            st += [w for w in succ(x) if w in nodes]
        if v in seen:
            out.add(v)
    return out


HEX = [(-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1), (0, -1)]


def G1():
    Q0 = {(a, b) for a in range(-3, 4) for b in range(-3, 4) if 1 <= a * a + b * b <= 5}

    def succ(q):
        out = []
        for d in (-1, 0, 1):
            n = divpi((q[0] + d, q[1]))
            if n is not None:
                out.append(n)
        return out
    cw = closed_walk_nodes(Q0, succ)
    assert cw == set(HEX), cw
    # self loops at +-i, hexagon edges
    assert (0, 1) in succ((0, 1)) and (0, -1) in succ((0, -1))
    # triple product graph
    states = {(x, y) for x in Q0 for y in Q0
              if x != y and (y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2 <= 5}

    def trans(s):
        x, y = s
        out = []
        for e1 in (0, 1):
            for e2 in (0, 1):
                for e3 in (0, 1):
                    nx = divpi((x[0] + e1 - e2, x[1]))
                    ny = divpi((y[0] + e1 - e3, y[1]))
                    if nx is not None and ny is not None and (nx, ny) in states:
                        out.append(((nx, ny), (e1, e2, e3)))
        return out
    cw3 = closed_walk_nodes(states, lambda s: [t for t, _ in trans(s)])
    assert len(cw3) == 12
    for s in cw3:
        inside = [(t, l) for t, l in trans(s) if t in cw3]
        assert len(inside) == 1, (s, inside)
    # follow each 6-cycle and read the three parity words
    done = set()
    for s0 in sorted(cw3):
        if s0 in done:
            continue
        s, words = s0, ([], [], [])
        for _ in range(6):
            done.add(s)
            (t, (e1, e2, e3)), = [(t, l) for t, l in trans(s) if t in cw3]
            for w, e in zip(words, (e1, e2, e3)):
                w.append(e)
            s = t
        assert s == s0
        rots = {tuple(words[0][i:] + words[0][:i]) for i in range(6)}
        assert tuple(words[1]) in rots and tuple(words[2]) in rots
        assert sorted(words[0]) == [0, 0, 0, 1, 1, 1]
    print('G1 OK: closed-walk part of Gamma = hexagon (+ loops at +-i); triple graph forces'
          ' rotations of 000111')


def G2(B=9):
    stats = dict(c=0, orbits=0, two=0)
    examples = []
    for ca in range(-B, B + 1):
        for cb in range(0, B + 1):
            c = (ca, cb)
            if (ca + cb) % 2 == 0:
                continue
            T = RG.PiMap(G, {1: ((1, 0), c)})
            cyc = RG.all_cycles(T)
            orbs = orbits(c)
            # V-cycles <-> T-cycles: T-cycle odd points z; V-cycle = T-cycle minus
            # the intermediate values z + c.  residues of a T-cycle's even points
            # that are values V(...) -- simply use all points z of the T-cycle that
            # are pi^{-1}-images, i.e. all even points and odd points alike have
            # residues in one orbit (z + c = z mod c).
            per = {o: [] for o in orbs}
            for C in cyc:
                rs = {red(z, c) for z in C}
                o = [o for o in orbs if rs <= o]
                assert len(o) == 1
                assert rs == o[0]
                per[o[0]].append(C)
            zero = [o for o in orbs if (0, 0) in o][0]
            want = {((0, 0),), tuple(sorted([G.mul((0, -1), c), G.mul((1, -1), c)]))}
            assert {tuple(sorted(C)) for C in per[zero]} == want, c
            for o in orbs:
                if o is zero:
                    continue
                assert 1 <= len(per[o]) <= 2, (c, len(per[o]))
                stats['orbits'] += 1
                if len(per[o]) == 2:
                    stats['two'] += 1
                    if len(examples) < 6:
                        examples.append((c, sorted(len(C) for C in per[o])))
            stats['c'] += 1
            # basin rule on a box for single-cycle orbits
            lab = {}
            for C in cyc:
                for z in C:
                    lab[z] = C
            single = {o: per[o][0] for o in orbs if len(per[o]) == 1 and o is not zero}
            for a in range(-12, 13, 3):
                for b in range(-12, 13, 3):
                    z = (a, b)
                    r = red(z, c)
                    o = [o for o in orbs if r in o][0]
                    if o in single:
                        x = z
                        while x not in lab:
                            x = T(x)
                        assert lab[x] == single[o], (c, z)
    print(f"G2 OK: {stats['c']} values of c, {stats['orbits']} nonzero <pi>-orbits,"
          f" {stats['two']} of them carry two cycles; examples (c, T-cycle lengths): {examples}")


def G3():
    out = {}
    for u in [(0, 1), (-1, 0), (0, -1)]:
        for c in [(1, 0), (0, 1), (2, 1), (1, 2), (3, 0)]:
            T = RG.PiMap(G, {1: (u, c)})
            cyc = RG.all_cycles(T)
            out[(u, c)] = sorted(len(C) for C in cyc)
            for C in cyc:      # each is really a cycle
                assert T(C[-1]) == C[0] or len(C) == 1 or all(T(C[i]) in C for i in range(len(C)))
    for k, v in out.items():
        print('   G3 u=%s c=%s: %d cycles, lengths %s' % (k[0], k[1], len(v), v))
    print('G3 OK')
    return out


def G4():
    u, c = (1, 2), (1, 0)
    T = RG.PiMap(G, {1: (u, c)})
    z = (0, 1)
    y = G.add(G.mul(u, z), c)                      # -1 + i
    assert G.vpi(y) == 1 and G.div(y, PI) == z     # exact fixed point of the k=1 block
    # archimedean multiplier |u/pi|^2 = 5/2 > 1 (norms are exact integers)
    assert G.norm(u) * 1 > G.norm(PI) * 1 and 2 * G.norm(u) == 5 * G.norm(PI)
    assert T(T(z)) == z
    # evidence: growth of a few orbits
    for z0 in [(1, 0), (2, 1), (3, 0), (1, 3)]:
        x = z0
        for _ in range(20000):
            x = T(x)
        print('   G4 evidence: seed %s after 20000 steps has |z|^2 with %d bits' % (z0, G.norm(x).bit_length()))
    print('G4 OK (Lemma B obstruction exact; divergence EVIDENCE only)')


def G5():
    import systems as SY
    T = SY.gauss_naive_x1
    for a in range(-30, 31):
        for b in range(-30, 31):
            if b % 2 == 1:           # z = i or 1+i (mod 2)
                z = (a, b)
                for k in range(50):
                    assert z == (a + k, b)
                    z = T(z)
    print('G5 OK: z with odd imaginary part runs z, z+1, z+2, ... forever')


if __name__ == '__main__':
    G0()
    G1()
    G2()
    G3()
    G4()
    G5()
    print('ALL OK')
