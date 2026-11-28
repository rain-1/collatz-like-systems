"""check_rings.py -- exact checks for rings.md (Eisenstein, Z[sqrt-2], Z[sqrt2],
and the Gaussian unit-multiplier maps).

Claims checked:
  R1  Theorem N' applies: every branch is u z + c with u a unit of absolute
      value 1 in every archimedean embedding, pi | u r + c on its class; the
      window of rings.window contains the bound C/(|pi|-1) in every embedding
      (exact integer comparison on the window's boundary).
  R2  complete cycle lists for the named systems (asserted), in particular
      the "complete number system" maps whose only cycle is {0}:
      Z[sqrt-2] z+1, Z[i] -z+1, Z[i] -iz+1.
  R3  table: for each ring and each listed c (and u = 1): number of cycles,
      number of orbits of multiplication by pi on O/(c) (canonical residues by
      Hermite normal form), and how many cycles each orbit carries (data;
      the bound "<= 2 per orbit" is PROVED only for Z[i], see gaussian.md).
Runs in about 30 s.
"""
import os
import sys
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rings as RG  # noqa: E402


def hnf_reducer(R, c):
    """Canonical reduction modulo the ideal cO, via the HNF of the lattice
    spanned by c and c*theta in Z^2."""
    v1, v2 = c, R.mul(c, (0, 1))
    # make first coordinate gcd in v1, zero in v2 (integer row ops)
    (a1, b1), (a2, b2) = v1, v2
    while a2 != 0:
        q = a1 // a2
        (a1, b1), (a2, b2) = (a2, b2), (a1 - q * a2, b1 - q * b2)
    if a1 < 0:
        a1, b1 = -a1, -b1
    D = abs(b2)
    assert a1 * D == abs(R.norm(c)), (c, a1, D)

    def red(z):
        x, y = z
        k = x // a1
        x, y = x - k * a1, y - k * b1
        return (x, y % D)
    return red, a1 * D


def orbits_pi(R, c):
    red, N = hnf_reducer(R, c)
    elems = {(x, y) for x in range(N) for y in range(N)}
    elems = {red(e) for e in elems}
    assert len(elems) == N
    seen, out = set(), []
    for e in sorted(elems):
        if e in seen:
            continue
        o, x = set(), e
        while x not in o:
            o.add(x)
            x = red(R.mul(x, R.pi))
        seen |= o
        out.append(frozenset(o))
    return out, red


NAMED = {
    # id: (ring, branches, expected sorted cycle lengths)
    'E_f': (RG.EIS, {1: ((1, 0), (2, 0)), 2: ((1, 0), (1, 0))}, [1, 2, 2]),
    'E_w': (RG.EIS, {1: ((0, 1), (-1, 0)), 2: ((0, 1), (1, 0))}, None),
    'ZM2_1': (RG.ZM2, {1: ((1, 0), (1, 0))}, [1]),
    'ZP2_1': (RG.ZP2, {1: ((1, 0), (1, 0))}, [1, 2, 3]),
    'G1_1': (RG.GAUSS, {1: ((1, 0), (1, 0))}, [1, 2]),
    'Gm1_1': (RG.GAUSS, {1: ((-1, 0), (1, 0))}, [1]),
    'Gmi_1': (RG.GAUSS, {1: ((0, -1), (1, 0))}, [1]),
    'Gi_1': (RG.GAUSS, {1: ((0, 1), (1, 0))}, [1, 2, 3]),
}


def R1_R2():
    for name, (R, br, want) in NAMED.items():
        T = RG.PiMap(R, br)
        for r, (u, c) in br.items():
            if R.imag:
                assert R.norm(u) == 1
            else:
                assert u in ((1, 0), (-1, 0))
        cyc = RG.all_cycles(T)
        for C in cyc:
            for i, z in enumerate(C):
                assert T(z) in C
        lens = sorted(len(C) for C in cyc)
        if want is not None:
            assert lens == want, (name, lens)
        print('   R2 %-6s %-10s cycles: %s' % (name, R.name, [list(C) for C in cyc]))
    print('R1, R2 OK')


def R3():
    table = {
        RG.GAUSS: [(1, 0), (3, 0), (2, 1), (1, 2), (5, 0), (3, 2), (4, 1), (7, 0)],
        RG.EIS: [(1, 0), (2, 0), (4, 0), (5, 0), (3, 1), (7, 0), (4, 3), (8, 0)],
        RG.ZM2: [(1, 0), (3, 0), (5, 0), (1, 1), (3, 1), (5, 2), (7, 0), (1, 3)],
        RG.ZP2: [(1, 0), (3, 0), (5, 0), (3, 1), (7, 0), (5, 2), (9, 0), (1, 2)],
    }
    for R, cs in table.items():
        for c in cs:
            if R.residue_pi(c) == 0:
                continue
            if R.Npi == 2:
                br = {1: ((1, 0), c)}
            else:      # Eisenstein: residue 1 -> z + c1, residue 2 -> z + c2 with pi | r + c_r
                c1 = c if R.residue_pi(c) == 2 else R.neg(c)
                c2 = R.neg(c1)
                br = {1: ((1, 0), c1), 2: ((1, 0), c2)}
            T = RG.PiMap(R, br)
            cyc = RG.all_cycles(T)
            orbs, red = orbits_pi(R, c)
            per = {o: 0 for o in orbs}
            for C in cyc:
                rs = {red(z) for z in C}
                o = [o for o in orbs if rs <= o]
                assert len(o) == 1, (R.name, c)
                per[o[0]] += 1
            dist = {}
            for o, k in per.items():
                dist[k] = dist.get(k, 0) + 1
            assert min(per.values()) >= 1
            print('   R3 %-10s c=%-8s N(c)=%4d cycles=%3d  pi-orbits=%3d  cycles-per-orbit histogram=%s'
                  % (R.name, c, abs(R.norm(c)), len(cyc), len(orbs), dict(sorted(dist.items()))))
    print('R3 OK')


def R4():
    """Z[sqrt-2]: the Theorem G argument goes through: the closed-walk part of the
    triple product graph has unique transitions and its parity words are
    rotations of one word, so at most 2 cycles per xpi-orbit; the zero orbit
    carries only {0} (c = 1 map has the single cycle {0}, R2)."""
    from check_gaussian import closed_walk_nodes
    R = RG.ZM2
    Q0 = {(a, b) for a in range(-3, 4) for b in range(-3, 4) if 1 <= R.norm((a, b)) <= 5}
    # |q| <= 1/(sqrt2 - 1) < sqrt 6 gives N(q) <= 5; coordinates: a^2 + 2b^2 <= 5

    def dv(x):
        return R.div(x, R.pi) if R.divides(R.pi, x) else None
    states = {(x, y) for x in Q0 for y in Q0
              if x != y and 1 <= R.norm((y[0] - x[0], y[1] - x[1])) <= 5}

    def trans(s):
        x, y = s
        out = []
        for e1 in (0, 1):
            for e2 in (0, 1):
                for e3 in (0, 1):
                    nx, ny = dv((x[0] + e1 - e2, x[1])), dv((y[0] + e1 - e3, y[1]))
                    if nx is not None and ny is not None and (nx, ny) in states:
                        out.append(((nx, ny), (e1, e2, e3)))
        return out
    cw = closed_walk_nodes(states, lambda s: [t for t, _ in trans(s)])
    assert len(cw) == 24
    done = set()
    ncyc = 0
    for s0 in sorted(cw):
        if s0 in done:
            continue
        s, words = s0, ([], [], [])
        while True:
            done.add(s)
            inside = [(t, l) for t, l in trans(s) if t in cw]
            assert len(inside) == 1
            (t, l), = inside
            for w, e in zip(words, l):
                w.append(e)
            s = t
            if s == s0:
                break
            assert s not in done
        ncyc += 1
        L = len(words[0])
        rots = {tuple(words[0][i:] + words[0][:i]) for i in range(L)}
        assert tuple(words[1]) in rots and tuple(words[2]) in rots, words
    print(f'R4 OK: Z[sqrt-2] triple graph has {ncyc} closed cycles, all with rotated parity words'
          ' => at most 2 cycles per xpi-orbit')


if __name__ == '__main__':
    R1_R2()
    R3()
    R4()
    print('ALL OK')
