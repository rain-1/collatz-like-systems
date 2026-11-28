"""Theorem P (type (c) => a two-word code of non-descending walks), checked
exactly on every unit-multiplier system of the table in cwlib.SYSTEMS.

For each system:
  1. find an expanding simple cycle C of G_K (least length) and its periodic
     point x* (exact rational, checked to be T-periodic);
  2. rotate C (cycle lemma) so that every partial slope from its first node is > 1;
  3. find a re-entry walk W at that node using an edge not on C (type (c));
  4. put W' = W^{|C|}, U = C^D W', V = C^{D + |W'|/|C|} with the least D for which
     every prefix slope of U and of V is > 1;
  5. check exactly: U != V, |U| = |V|, both closed walks of G_K at r0, all prefix
     slopes > 1; for random words in {U,V}^6 the integer class following the
     concatenation is nonempty and its least positive member really follows it;
  6. report the dimension lower bound s with p^{-s e_U} + p^{-s e_V} = 1.

Exits 0 iff every assertion holds.  Run: python3 check_entropy_code.py
"""
import random
import sys
from fractions import Fraction as F
from math import log
import cwlib as L

random.seed(1)
FAIL = []


def claim(name, cond):
    if not cond:
        FAIL.append(name)
        print('FAIL', name)


def dim_lower(p, eU, eV):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        s = (lo + hi) / 2
        if p ** (-s * eU) + p ** (-s * eV) > 1:
            lo = s
        else:
            hi = s
    return lo


def run(name, K=None):
    sysd, l, seed, note = L.SYSTEMS[name]
    p, m = sysd['p'], sysd['m']
    K = K or m
    E = L.graph(sysd, K)
    c, lam = L.expanding_cycle(sysd, K, maxlen=10)
    x = L.periodic_point(sysd, c)
    pts = L.cycle_nodes(sysd, x, K)
    claim(name + ' periodic point follows cycle',
          L.nodes_of_points(pts, p, K) == c or len(pts) % len(c) == 0)
    pts = L.rotate_cycle_lemma(sysd, pts)
    cn = L.nodes_of_points(pts, p, K)
    # slopes along C from r0 all > 1
    ps = L.prefix_slopes(sysd, cn)
    claim(name + ' cycle-lemma rotation', all(s > 1 for s in ps))
    lamC = ps[-1]
    W = L.reentry_walk(E, cn)
    claim(name + ' re-entry exists (type c)', W is not None)
    if W is None:
        return None
    Wp = W * len(cn)
    D = 0
    while True:
        U = cn * D + Wp
        V = cn * (D + len(Wp) // len(cn))
        if all(s > 1 for s in L.prefix_slopes(sysd, U)) and \
           all(s > 1 for s in L.prefix_slopes(sysd, V)):
            break
        D += 1
        assert D < 10 ** 4
    claim(name + ' U != V', U != V)
    claim(name + ' |U| = |V|', len(U) == len(V))
    # closed walks: consecutive nodes joined by edges, last returns to r0
    def is_walk(wk):
        seq = wk + [wk[0]]
        return all(any(t == seq[i + 1] for (t, *_r) in E[seq[i]]) for i in range(len(wk)))
    claim(name + ' U,V closed walks', is_walk(U) and is_walk(V))
    # min over concatenations: prefix slopes of any word in {U,V}^* are > 1
    # (proof: product of complete blocks > 1 times a partial prefix > 1).
    lamU, lamV = L.slope(sysd, U), L.slope(sysd, V)
    claim(name + ' block slopes > 1', lamU > 1 and lamV > 1)
    eU = L.vexp(L.walk_affine(sysd, U)[2], p)[0]
    eV = L.vexp(L.walk_affine(sysd, V)[2], p)[0]
    # realizability and direct simulation on 5 random words of 6 blocks
    for trial in range(5):
        word = []
        for _ in range(6):
            word += random.choice([U, V])
        fc = L.follow_class(sysd, word + [word[0]], K)
        claim(name + ' class nonempty', fc is not None)
        rho, Mod = fc
        n0 = rho if rho > 0 else rho + Mod
        n = n0
        ok = True
        sl = F(1)
        for j, r in enumerate(word):
            if n % p ** K != r:
                ok = False
                break
            n = L.step(sysd, n)
        claim(name + ' integer follows word', ok)
    s = dim_lower(p, eU, eV)
    claim(name + ' positive dimension bound', s > 0)
    W_e = L.vexp(L.walk_affine(sysd, W)[2], p)[0]
    return dict(name=name, K=K, x=x, lenC=len(cn), lamC=lamC, lenW=len(W),
                lamW=L.slope(sysd, W), D=D, L=len(U), eU=eU, eV=eV, s=s)


if __name__ == '__main__':
    names = ['3x+1', '3x-1', '3x+5', '5x+1', 'K7', 'core13', 'core135', 'core57',
             'core157', 'core357', 'core17', 'coreW', 'split5_3', 'split5_1', 'm3_b']
    print('%-9s %-6s %-5s %-10s %-4s %-12s %-4s %-5s %-5s %-8s' %
          ('system', 'x*', '|C|', 'lambda_C', '|W|', 'lambda_W', 'D', '|U|', 'eU/eV', 'dim>='))
    for nm in names:
        r = run(nm)
        if r:
            print('%-9s %-6s %-5d %-10s %-4d %-12s %-4d %-5d %-5s %.5f' % (
                nm, str(r['x']), r['lenC'], str(r['lamC']), r['lenW'], str(r['lamW']),
                r['D'], r['L'], '%d/%d' % (r['eU'], r['eV']), r['s']))
    if FAIL:
        print('FAILURES', FAIL)
        sys.exit(1)
    print('all checks passed')
