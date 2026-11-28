"""Compare exhaustive counts N(D, b) = #{deg f = D : sigma(f) > b} with the Haar prediction
(q-1) q^D P(b), inside and beyond the horizon, and report the never-dropping counts.

usage: python3 analyse.py NAME [NAME ...]      (reads specs/NAME.txt, data/NAME.txt)
"""
import sys, math
from fractions import Fraction
from ffmap import load_spec, survivors_exact, step_law


def load(name):
    N, cap = {}, 0
    for l in open(f'data/{name}.txt'):
        p = l.split()
        if p and p[0] == 'S':
            D, b, v = int(p[1]), int(p[2]), int(p[3])
            N[(D, b)] = v
            cap = max(cap, b)
    return N, cap


def table(name):
    S = load_spec(f'specs/{name}.txt')
    q = S[0]
    law = step_law(S)
    emax = max(e for _, _, e in law)
    drift = sum(p * s for p, s, e in law) / sum(p * e for p, s, e in law)
    N, cap = load(name)
    Ds = sorted({D for D, b in N})
    P = survivors_exact(S, cap)
    print(f'== {name}: q = {q}, drift per digit = {float(drift):.4f}, cap = {cap}')
    # in-horizon exactness: b + emax - 1 <= D
    bad = 0
    for (D, b), v in N.items():
        if b + emax - 1 <= D and b >= 1:
            pred = (q - 1) * q ** D * P[b]
            if pred != v:
                bad += 1
    print(f'  in-horizon cells (b + emax - 1 <= D) with N != (q-1)q^D P(b) exactly: {bad}')
    # decay rate of P
    bb = cap - (cap % 2)
    rate = (P[bb] / P[bb - 40]) if P[bb - 40] else 0
    r = float(rate) ** (1 / 40)
    h = 1 + math.log(r) / math.log(q)
    print(f'  P(b) decay per digit near b = {bb}: {r:.5f}; finite-b estimate of h = {h:.4f} (biased low by the b^(-3/2) factor; exact h in theory.md) ')
    print('  D | N(D,D) pred | N(D,2D) obs / pred | N(D,3D) obs / pred | never (sigma>cap) | never/((q-1)q^D)')
    for D in Ds:
        if D < 4:
            continue
        tot = (q - 1) * q ** D
        cells = []
        for mult in (1, 2, 3):
            b = mult * D
            if b <= cap:
                cells.append((N[(D, b)], float(tot * P[b])))
            else:
                cells.append((None, None))
        nev = N[(D, cap)]
        s = f'  {D:2d} | {cells[0][0]:9d} {cells[0][1]:11.1f} |'
        for o, p in cells[1:]:
            s += f' {o:9d} / {p:11.2f} |' if o is not None else '   -   |'
        s += f' {nev:9d} | {nev / tot:.3e}'
        print(s)
    return S, N, P, cap


if __name__ == '__main__':
    for name in sys.argv[1:]:
        table(name)


def bins(name, Dmin=8, bnds=((1.0, 1.5), (1.5, 2.0), (2.0, 3.0), (3.0, 4.0), (4.0, 6.0), (6.0, 10.0))):
    """Beyond-horizon comparison by ranges of b/D, cells with expected >= 5.
    'never' = N(D, cap): starts that did not drop within cap digits."""
    S = load_spec(f'specs/{name}.txt')
    q = S[0]
    N, cap = load(name)
    P = survivors_exact(S, cap)
    Ds = sorted({D for D, b in N})
    print(f'== {name}: beyond the horizon, D >= {Dmin}, cells with expected >= 5')
    print('  b/D range | cells | observed | of which never-dropping | expected | obs/exp | (obs-never)/exp | chi2/cell')
    for lo, hi in bnds:
        no = nn = 0
        ne = 0.0
        chi = 0.0
        cells = 0
        for D in Ds:
            if D < Dmin:
                continue
            for b in range(D + 1, cap):
                if lo * D < b <= hi * D:
                    e = float((q - 1) * q ** D * P[b])
                    if e < 5:
                        continue
                    o = N[(D, b)]
                    no += o
                    nn += N[(D, cap)]
                    ne += e
                    chi += (o - e) ** 2 / e
                    cells += 1
        if cells:
            print(f'  {lo:.1f}-{hi:.1f} | {cells:4d} | {no:10d} | {nn:10d} | {ne:12.1f} | {no / ne:7.4f} | {(no - nn) / ne:7.4f} | {chi / cells:8.2f}')
        else:
            print(f'  {lo:.1f}-{hi:.1f} | no cells with expected >= 5')
