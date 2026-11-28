"""Exact check of Theorem F (Frobenius cycles) for the binomial systems A3, S2c, Q4b.

For a branch word w of digit-length L, T^{(w)}(x) = (G_w x + H_w)/t^L on the cylinder of w.
Theorem F: if G_w = t^L + c with c a nonzero constant, then x_w = -H_w/c is a polynomial,
T^{(w)}(x_w) = x_w, its branch word over L digits is w, and deg x_w <= L + kappa when every
prefix slope of w is >= 0 (kappa = max_r max(deg g_r - 1, deg c_r)).

Checks (all exact; the script exits 1 on any failure):
  * every word in the Frobenius class for the smallest level (all of them), and a random
    sample at the next level, for each system;
  * the number of distinct cycles formed, against the lower bound #words / L;
  * the count of never-dropping polynomials of degree <= L + kappa found by direct
    enumeration (data/*.txt from survive.c) is at least the number of cycles.
"""
import sys, itertools, random
from math import comb
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
from ffmap import *

FAIL = []


def compose(system, word):
    q, brs = system
    G, H, E = (1,), (), 0
    for i in word:
        r, g, c = brs[i]
        e = len(r)
        h = padd(q, pneg(q, pmul(q, g, trim(r))), (0,) * e + tuple(c) if trim(c) else ())
        H = padd(q, pmul(q, g, H), (0,) * E + h if h else ())
        G = pmul(q, g, G)
        E += e
    return G, H, E


def finv(q, a):
    for b in range(1, q):
        if fmul(q, a, b) == 1:
            return b
    raise ZeroDivisionError


def word_of(system, x, L):
    w, dig = [], 0
    while dig < L:
        x, i, e = step(system, x)
        w.append(i)
        dig += e
    return tuple(w), x, dig


def check_word(system, word, kappa):
    q = system[0]
    G, H, L = compose(system, word)
    # G = t^L + c ?
    if len(G) != L + 1 or G[L] != 1 or any(G[1:L]) or G[0] == 0:
        return None
    c = G[0]
    ci = finv(q, fneg(q, c))
    x = trim(tuple(fmul(q, ci, a) for a in H))  # x = -H/c
    w2, y, dig = word_of(system, x, L)
    if w2 != tuple(word) or y != x or dig != L:
        FAIL.append(('not periodic', word))
        return x
    # prefix slopes
    slopes = [deg(trim(system[1][i][1])) - len(system[1][i][0]) for i in word]
    S, ok = 0, True
    for s in slopes:
        S += s
        ok = ok and S >= 0
    if S != 0:
        FAIL.append(('nonzero total slope', word))
    if ok and deg(x) > L + kappa:
        FAIL.append(('degree bound', word, deg(x)))
    return x


def kappa_of(system):
    return max(max(deg(trim(g)) - 1, deg(trim(c)) if trim(c) else 0) for (r, g, c) in system[1])


def frob_words(system, counts):
    """All words with the given branch counts (dict branch -> count)."""
    items = []
    for b, n in counts.items():
        items += [b] * n
    seen = set()
    for perm in set(itertools.permutations(items)):
        yield perm


def cycles_of(system, pts, L):
    """Group periodic points into cycles; return list of (min degree point)."""
    pts = set(pts)
    cyc_min = []
    done = set()
    for x in pts:
        if x in done:
            continue
        orbit = [x]
        y = step(system, x)[0]
        while y != x:
            orbit.append(y)
            y = step(system, y)[0]
            if len(orbit) > 10 * L:
                FAIL.append(('cycle too long', x))
                break
        for z in orbit:
            done.add(z)
        cyc_min.append(min(deg(z) for z in orbit))
    return cyc_min


def run(name, word_sets, Lsmall):
    S = load_spec(f'specs/{name}.txt')
    kap = kappa_of(S)
    pts = []
    nwords = 0
    for counts in word_sets:
        items = []
        for b, n in counts.items():
            items += [b] * n
        for perm in set(itertools.permutations(items)):
            nwords += 1
            x = check_word(S, perm, kap)
            if x is None:
                FAIL.append(('G_w not binomial', name, perm))
            else:
                pts.append(x)
    distinct = len(set(pts))
    if distinct != nwords:
        FAIL.append(('points not distinct', name, distinct, nwords))
    cm = cycles_of(S, pts, Lsmall)
    nonzero = [d for d in cm if d >= 0]
    print(f'{name}: L = {Lsmall}, Frobenius words {nwords}, distinct periodic polynomials {distinct}, '
          f'cycles {len(cm)} (bound words/L = {nwords / Lsmall:.1f}), max min-degree {max(nonzero)} '
          f'(bound L+kappa = {Lsmall + kap})')
    if len(cm) < nwords / Lsmall:
        FAIL.append(('too few cycles', name))
    if max(nonzero) > Lsmall + kap:
        FAIL.append(('cycle min degree above bound', name))
    return S, kap, cm


def sample_level(name, counts, nsample, seed):
    S = load_spec(f'specs/{name}.txt')
    kap = kappa_of(S)
    rnd = random.Random(seed)
    items = []
    for b, n in counts.items():
        items += [b] * n
    L = None
    for _ in range(nsample):
        rnd.shuffle(items)
        x = check_word(S, tuple(items), kap)
        if x is None:
            FAIL.append(('G_w not binomial (sample)', name))
        G, H, L = compose(S, tuple(items))
    print(f'{name}: level L = {L}: {nsample} random Frobenius words verified periodic')


def enum_check(name, cm, Lsmall, kap):
    """Never-dropping counts from the exhaustive enumeration must cover one point per cycle."""
    try:
        lines = open(f'data/{name}.txt').read().split('\n')
    except OSError:
        print(f'  (data/{name}.txt missing; enumeration cross-check skipped)')
        return
    cap = max(int(l.split()[2]) for l in lines if l.startswith('S '))
    never = {}
    for l in lines:
        if l.startswith('S '):
            _, D, b, N = l.split()
            if int(b) == cap:
                never[int(D)] = int(N)
    tot = sum(v for D, v in never.items() if D <= Lsmall + kap)
    need = sum(1 for d in cm if d >= 1)
    print(f'  enumeration: never-dropping (sigma > {cap}) polynomials of degree 1..{Lsmall + kap}: {tot} '
          f'>= cycles with min degree >= 1: {need}')
    if tot < need:
        FAIL.append(('enumeration below cycle count', name))


if __name__ == '__main__':
    # A3: branches 0 (g=1), 1 (g=1+t^2), 2 (g=1). Level k: n_1 = 3^k, n_0 + n_2 = 3^k.
    k = 1
    ws = [{1: 3, 0: j, 2: 3 - j} for j in range(4)]
    S, kap, cm = run('A3', ws, 6)
    enum_check('A3', cm, 6, kap)
    sample_level('A3', {1: 9, 0: 5, 2: 4}, 300, 1)
    sample_level('A3', {1: 27, 0: 13, 2: 14}, 40, 2)
    # S2c: branches 0 ('0', g=1, e=1), 1 ('10', g=(1+t)^3, e=2), 2 ('11', g=1+t, e=2).
    # G_w = (1+t)^{3a+b}, digits L = n0 + 2a + 2b, zero slope n0 = a - b. Need 3a + b = 2^k.
    ws = []
    Ls = 8
    for a in range(0, 9):
        for b in range(0, 9):
            if 3 * a + b == 8 and a - b >= 0:
                ws.append({1: a, 2: b, 0: a - b})
    S, kap, cm = run('S2c', ws, Ls)
    enum_check('S2c', cm, Ls, kap)
    sample_level('S2c', {1: 10, 2: 2, 0: 8}, 200, 3)    # 3*10+2 = 32
    # Q4b: branches 0 (1), 1 (1+t^3), 2 (1), 3 (1); n_1 = 2^k, others sum 2^{k+1}, L = 3*2^k.
    ws = []
    for i in range(5):
        for j in range(5 - i):
            ws.append({1: 2, 0: i, 2: j, 3: 4 - i - j})
    S, kap, cm = run('Q4b', ws, 6)
    enum_check('Q4b', cm, 6, kap)
    sample_level('Q4b', {1: 8, 0: 5, 2: 6, 3: 5}, 200, 4)
    if FAIL:
        print('FAIL', FAIL[:10])
        sys.exit(1)
    print('all Frobenius-cycle checks passed')
