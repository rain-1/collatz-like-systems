"""Referee 2: independent check of census/round5/funcfield (written from scratch).

Imports nothing from the prover (ffmap, analyse, check_*) or from referee1_check.py.
Exact arithmetic (Fraction / int) wherever the claim is exact. Every section can fail and the
script exits 1 if any does. Run from any directory:  python referee2_check.py  (about 1-3 min).

Sections
 0. own field arithmetic F_2, F_3, F_4; own encoding of A3, Q4b, S2c, B3, G3; compared with the
    prover's spec files (parsed here independently).
 1. exact P(b) by a digit-position DP; Theorem A / A' Chernoff bounds exactly; Theorem A''(a)
    P(b) <= rho*^(b-1) exactly against a rational rho_lo < rho*.
 2. h for S2c computed independently (minimise the root rho(lambda) of F = 1), compared with the
    closed form 2 lambda = (lambda^2-1)^2 and with the tilt identity phi(theta*) = h.
 3. Lemma S (supermultiplicativity) and Lemma B (block bounds) exactly; Gamma upper bounds.
 4. own exhaustive enumeration of sigma: horizon lemma per octave (must match exactly in-horizon
    and must differ somewhere beyond, so the test discriminates); Proposition H' two-sided bound
    on every in-range cell; corrected-law upper bound N(X, D+1-e) / X^h bounded.
 5. Theorem F for S2c at L = 16 (all 1330 zero-slope words): G_w = 1 + t^16, x_w periodic with
    word w, deg <= L + kappa for nonneg-prefix words, cycle count >= Z_L/L - 1; random words at
    L = 32, 64; same for A3 (L = 6, 18 sampled) and Q4b (L = 6, 12 sampled).
 6. Theorem A''(b): exact big-integer Z_L >= 2^(h L - 4)/(L+1)^2 for L = 2^8 .. 2^13, and the
    chosen-type term alone for L = 2^8 .. 2^15 (exact integers); Z_L formula vs brute force.
 7. Lemma T on random orbits (A3, Q4b, S2c, G3); T1 and T2 on the A3 cycles found in section 4.
 8. Integer side: |2^L - 3^a| = 1 solutions; the -17 cycle; sibling sanity (3x-1, 3x+5).
 9. Spot checks of numbers quoted in README (Theorem A crossing at L = 486; K threshold at
    L = 2048 for S2c; Gamma constants).
"""
import sys, random, math, itertools, os
from fractions import Fraction as Fr
from math import comb
from decimal import Decimal as Dc, getcontext

getcontext().prec = 80
HERE = os.path.dirname(os.path.abspath(__file__))
FAIL = []


def bad(*a):
    FAIL.append(a)
    print('  FAIL', *a)


# ---------------------------------------------------------------- 0. arithmetic and systems
class Field:
    def __init__(self, q):
        self.q = q

    def add(self, a, b):
        return a ^ b if self.q in (2, 4) else (a + b) % self.q

    def neg(self, a):
        return a if self.q in (2, 4) else (-a) % self.q

    def mul(self, a, b):
        if self.q != 4:
            return a * b % self.q
        if a == 0 or b == 0:
            return 0
        # F_4 = {0,1,w,w+1}, codes 0,1,2,3, w^2 = w+1. log: 1->0, w(2)->1, w+1(3)->2
        lg = {1: 0, 2: 1, 3: 2}
        ex = [1, 2, 3]
        return ex[(lg[a] + lg[b]) % 3]

    def inv(self, a):
        for x in range(1, self.q):
            if self.mul(a, x) == 1:
                return x
        raise ZeroDivisionError


def norm(f):
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    return f


def dg(f):
    return len(f) - 1 if f else -1  # deg 0 = -1 here (only used with care)


def padd(F, a, b):
    n = max(len(a), len(b))
    return norm([F.add(a[i] if i < len(a) else 0, b[i] if i < len(b) else 0) for i in range(n)])


def psc(F, c, a):
    return norm([F.mul(c, x) for x in a])


def pmul(F, a, b):
    if not a or not b:
        return []
    o = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    o[i + j] = F.add(o[i + j], F.mul(x, y))
    return norm(o)


def shift(a, k):
    return norm([0] * k + list(a)) if a else []


# System: (F, [(r_digits_tuple, g_poly, c_poly)])
def system(q, brs):
    return (Field(q), [(tuple(r), norm(g), norm(c)) for r, g, c in brs])


# Own encoding from the README table / theory sec. 3 (NOT from specs; compared below).
SYS = {
    'A3': system(3, [((0,), [1], []), ((1,), [1, 0, 1], []), ((2,), [1], [1])]),
    'Q4b': system(4, [((0,), [1], []), ((1,), [1, 0, 0, 1], []), ((2,), [1], [1]), ((3,), [1], [])]),
    'S2c': system(2, [((0,), [1], []), ((1, 0), [1, 1, 1, 1], [1]), ((1, 1), [1, 1], [1])]),
    # B3 per README "g_1 = (1+t)^2" would be [1,2,1]; spec says 1+t+t^2. Encoded per spec, see sec 0.
    'B3': system(3, [((0,), [1], []), ((1,), [1, 1, 1], [1]), ((2,), [2], [])]),
    'G3': system(3, [((0,), [1], []), ((1,), [1, 1, 2], [1]), ((2,), [2], [])]),
}


def parse_spec(path):
    q, brs = None, []
    for line in open(path):
        p = line.split()
        if not p or p[0].startswith('#'):
            continue
        if p[0] == 'q':
            q = int(p[1])
            continue
        assert p[0] == 'B'
        e = int(p[1])
        r = tuple(int(x) for x in p[2:2 + e])
        i = 2 + e
        assert p[i] == 'G'
        gd = int(p[i + 1])
        g = [int(x) for x in p[i + 2:i + 3 + gd]]
        j = i + 3 + gd
        assert p[j] == 'C'
        cd = int(p[j + 1])
        c = [int(x) for x in p[j + 2:j + 3 + cd]]
        brs.append((r, norm(g), norm(c)))
    return q, brs


print('0. systems vs spec files')
for name, (F, brs) in SYS.items():
    q, sb = parse_spec(os.path.join(HERE, 'specs', name + '.txt'))
    if q != F.q or sorted(sb) != sorted(brs):
        bad('spec mismatch', name, sb, brs)
    else:
        print(f'  {name}: own encoding == specs/{name}.txt')
F3 = Field(3)
print('  B3: (1+t)^2 over F_3 =', pmul(F3, [1, 1], [1, 1]), ' spec g_1 =', SYS['B3'][1][1][1],
      ' (1-t)^2 =', pmul(F3, [1, 2], [1, 2]))


def branch(S, f):
    F, brs = S
    for i, (r, g, c) in enumerate(brs):
        if all((f[k] if k < len(f) else 0) == r[k] for k in range(len(r))):
            return i
    raise ValueError


def T(S, f):
    F, brs = S
    i = branch(S, f)
    r, g, c = brs[i]
    u = padd(F, f, [F.neg(x) for x in r])
    e = len(r)
    assert all((u[k] if k < len(u) else 0) == 0 for k in range(e))
    return padd(F, pmul(F, g, u[e:]), c), i


def sigma(S, f, cap):
    """digits consumed to end of first step with deg < deg f; cap+1 if none within cap digits."""
    d0 = dg(f)
    E = 0
    x = f
    while E <= cap:
        x, i = T(S, x)
        E += len(S[1][i][0])
        if dg(x) < d0:
            return E
    return cap + 1


def law(S):
    F, brs = S
    return [(Fr(1, F.q ** len(r)), dg(g) - len(r), len(r)) for r, g, c in brs]


# ---------------------------------------------------------------- 1. exact P(b)
def Pexact(S, bmax):
    L = law(S)
    emax = max(e for _, _, e in L)
    # prob[E] = dict slope -> prob, alive at a step end with digit count E
    prob = [dict() for _ in range(bmax + emax + 2)]
    prob[0][0] = Fr(1)
    P = [Fr(0)] * (bmax + 1)
    for E in range(0, bmax + 1):
        for s, pr in prob[E].items():
            for p, sl, e in L:
                ns = s + sl
                # this alive state at E straddles every b with E <= b < E + e
                for b in range(E, min(E + e, bmax + 1)):
                    P[b] += pr * p
                if ns >= 0 and E + e <= bmax + emax:
                    prob[E + e][ns] = prob[E + e].get(ns, 0) + pr * p
        prob[E] = None
    return P


print('1. exact P(b) and Chernoff bounds')
BM = 300
PA = Pexact(SYS['A3'], BM)
PQ = Pexact(SYS['Q4b'], BM)
PS = Pexact(SYS['S2c'], 400)
# S2c: P(1) = 1/2 (first branch 10 or 11 ends at E=2 > 1), P(2) = 1/4 (only 10). A3: P(1)=P(2)=1/3.
if PS[1] != Fr(1, 2) or PS[2] != Fr(1, 4):
    bad('S2c P(1),P(2)', PS[1], PS[2])
if PA[1] != Fr(1, 3) or PA[2] != Fr(1, 3):
    bad('A3 P(1),P(2)', PA[1], PA[2])
for b in range(BM + 1):
    if PA[b] ** 2 > Fr(8, 9) ** b:
        bad('A3 Chernoff', b)
    if PQ[b] ** 3 > Fr(243, 256) ** b:
        bad('Q4b Chernoff', b)
# sharpness of A3 rate: ratio should not be uniformly tiny (rate is right, not just an upper bound)
r300 = float(PA[300] ** 2 / Fr(8, 9) ** 300)
print(f'  A3: P(b)^2 <= (8/9)^b for b <= {BM}; P(300)^2/(8/9)^300 = {r300:.3e} (poly factor only)')


# ---------------------------------------------------------------- 2. h for S2c
def rho_of(lam):
    # positive root of 4 lam rho^2 - 2 rho - (lam^2 + 1) = 0
    return (2 + (4 + 16 * lam * (lam * lam + 1)).sqrt()) / (8 * lam)


lo, hi = Dc(1), Dc(4)
for _ in range(300):
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    if rho_of(m1) < rho_of(m2):
        hi = m2
    else:
        lo = m1
lam_n = (lo + hi) / 2
rho_n = rho_of(lam_n)
# closed form
a, b_ = Dc(1), Dc(3)
for _ in range(300):
    mid = (a + b_) / 2
    if (mid * mid - 1) ** 2 < 2 * mid:
        a = mid
    else:
        b_ = mid
lam_c = a
rho_c = (lam_c ** 2 - 1) / 2
h = 1 + rho_c.ln() / Dc(2).ln()
print(f'2. S2c: numeric min rho(lambda) = {rho_n:.15f} at lambda = {lam_n:.10f}; closed form rho* = {rho_c:.15f}, '
      f'h = {h:.8f}, C* = {1 / (1 - h):.4f}')
if abs(rho_n - rho_c) > Dc('1e-30') or abs(lam_n - lam_c) > Dc('1e-12'):
    bad('S2c saddle')
if abs(float(h) - 0.875848) > 1e-6:
    bad('S2c h quoted', h)
th = 1 / lam_c ** 2
Hth = -(th * th.ln() + (1 - th) * (1 - th).ln()) / Dc(2).ln()
phi = (2 + Hth) / (3 + th)
print(f'  theta* = 1/lambda*^2 = {th:.6f}; phi(theta*) = {phi:.12f}')
if abs(phi - h) > Dc('1e-40') or abs(float(th) - 0.352723) > 1e-6:
    bad('tilt identity', phi, h)
# empirical decay with b^{-3/2} correction approaches rho*
est = (float(PS[400] / PS[360]) * (400 / 360) ** 1.5) ** (1 / 40)
raw = float(PS[400] / PS[360]) ** (1 / 40)
print(f'  (P(400)/P(360))^(1/40): raw {raw:.6f} (h_raw = {1 + math.log2(raw):.4f}), '
      f'with b^-3/2 correction {est:.6f} (h = {1 + math.log2(est):.5f})')
if abs(est - float(rho_c)) > 2e-4:
    bad('S2c empirical rate')
# Theorem A''(a), exact: P(b) <= rho_lo^(b-1) with rational rho_lo < rho*
rho_lo = Fr(str(rho_c - Dc('1e-40')))
assert Dc(rho_lo.numerator) / Dc(rho_lo.denominator) < rho_c
mx = Fr(0)
pw = Fr(1)
for bb in range(1, 401):
    if bb > 1:
        pw *= rho_lo
    if PS[bb] > pw:
        bad("A''(a)", bb)
    mx = max(mx, PS[bb] / pw)
print(f"  A''(a): P(b) <= rho*^(b-1) for 1 <= b <= 400; max ratio {float(mx):.4f}")
# the same martingale bound must FAIL with a smaller rho (discrimination)
rho_small = Fr(9, 10)
if all(PS[bb] <= rho_small ** (bb - 1) for bb in range(1, 401)):
    bad('rho=0.9 not refuted: check cannot discriminate')

# ---------------------------------------------------------------- 3. Lemma S, Lemma B, Gamma
print('3. Lemma S, Lemma B, Gamma')
for name, P, q, e in (('A3', PA, 3, 1), ('Q4b', PQ, 4, 1), ('S2c', PS, 2, 2)):
    for b in range(0, 151):
        for m in range(0, b + 1):
            if P[b] < P[m + e - 1] * P[b - m]:
                bad('Lemma S', name, b, m)
    # Lemma S needs the e-1 slack: without it it must fail for S2c somewhere (discrimination)
    if e == 2:
        viol = sum(1 for b in range(0, 60) for m in range(0, b + 1) if P[b] < P[m] * P[b - m])
        print(f'  S2c: P(b) >= P(m)P(b-m) (no slack) fails in {viol} cells b<60 -- the slack e-1 is needed'
              if viol else '  S2c: no-slack version also holds for b<60')
c34 = [0] * 520
c34[0] = 1
for n in range(1, 520):
    c34[n] = (c34[n - 3] if n >= 3 else 0) + (c34[n - 4] if n >= 4 else 0)
for j in range(0, 301):
    if (3 ** j * PA[j]) ** 2 * 9 < 2 ** j:
        bad('Lemma B A3 exact', j)
    if (4 ** j * PQ[j]) ** 3 * 16 ** 3 < 9 ** j:
        bad('Lemma B Q4b', j)
    for n in range(j, j + 4):
        if 2 ** j * PS[j] < Fr(c34[n] * 2 ** j, 2 ** n):
            bad('Lemma B S2c', j, n)


def gamma(P, q, J, tail):
    return float(sum(1 / (q ** j * P[j]) for j in range(J + 1))) + tail


x434 = 1.2207440846057596
assert abs(x434 ** 4 - x434 - 1) < 1e-12
GA = gamma(PA, 3, 300, 3 * 2 ** (-301 / 2) / (1 - 2 ** -0.5))
GQ = gamma(PQ, 4, 300, 16 * 9 ** (-301 / 3) / (1 - 9 ** (-1 / 3)))
alpha = min(c34[n] / x434 ** n for n in range(300, 304))
GS = gamma(PS, 2, 400, 8 * x434 ** (-401) / alpha / (1 - 1 / x434))
print(f'  Gamma: A3 {GA:.4f} (quoted <= 2.655), Q4b {GQ:.4f} (<= 2.349), S2c {GS:.4f} (<= 4.446)')
for g_, qu in ((GA, 2.655), (GQ, 2.349), (GS, 4.446)):
    if g_ > qu:
        bad('Gamma quoted', g_, qu)


# ---------------------------------------------------------------- 4. enumeration
def allpolys(q, D):
    """all polys of degree exactly D (as lists)"""
    for low in itertools.product(range(q), repeat=D):
        for lead in range(1, q):
            yield list(low) + [lead]


def D0(S):
    F, brs = S
    out = 0
    for r, g, c in brs:
        e = len(r)
        s = dg(g) - e
        out = max(out, e, (dg(c) - s + 1) if c else 0)
    return out


print('4. enumeration: horizon lemma, Proposition H\', corrected-law upper bound')
ENUM = {'A3': 9, 'Q4b': 6, 'S2c': 14, 'G3': 8, 'B3': 8}
CAP = 40
NOCT = {}
CYC_A3 = []
for name, Dmax in ENUM.items():
    S = SYS[name]
    q = S[0].q
    P = Pexact(S, CAP + 2)
    e = max(len(r) for r, _, _ in S[1])
    d0 = D0(S)
    cnt = {}
    for D in range(0, Dmax + 1):
        hist = [0] * (CAP + 3)
        for f in allpolys(q, D):
            s = sigma(S, f, CAP)
            hist[min(s, CAP + 1)] += 1
            if name == 'A3' and s > CAP and D >= 3:
                CYC_A3.append(f)
        # N_D(b) = #{sigma > b}
        tail = 0
        Nb = [0] * (CAP + 2)
        for b in range(CAP + 1, -1, -1):
            Nb[b] = tail if b <= CAP else hist[CAP + 1]
            tail += hist[b]
        # recompute cleanly
        for b in range(0, CAP + 1):
            Nb[b] = sum(hist[k] for k in range(b + 1, CAP + 2))
        cnt[D] = Nb
    NOCT[name] = cnt
    inh = mism = beyond_diff = 0
    for D in range(d0, Dmax + 1):
        for b in range(0, CAP + 1):
            pred = (q - 1) * q ** D * P[b]
            if b + e - 1 <= D:
                inh += 1
                if cnt[D][b] != pred:
                    mism += 1
                    bad('horizon lemma', name, D, b, cnt[D][b], pred)
            elif cnt[D][b] != pred:
                beyond_diff += 1
    print(f'  {name}: D_0 = {d0}, in-horizon cells {inh}, mismatches {mism}; beyond-horizon cells differing {beyond_diff}')
    if beyond_diff == 0:
        bad('horizon test cannot discriminate', name)
    # Proposition H'
    Gam = {'A3': GA, 'B3': GA, 'G3': GA, 'Q4b': GQ, 'S2c': GS}[name]
    D1 = max(d0, 2 * e - 2)
    cells = 0
    for D in range(d0, Dmax + 1):
        X = q ** (D + 1)
        for b in range(0, D + 3 - e):
            if b > CAP:
                continue
            B = max(d0, b + e - 1)
            N = sum(cnt[Dp][b] for Dp in range(0, D + 1))
            diff = N - (X - q ** B) * P[b]
            up = Fr(Gam) * (q - 1) * q ** (b + 2 * e - 2) * P[b] + q ** D1
            cells += 1
            if diff < 0 or diff > up:
                bad("H'", name, D, b, float(diff), float(up))
            # discrimination: the naive "N(X,b) = X P(b) exactly" must fail somewhere
    naive_fail = sum(1 for D in range(d0, Dmax + 1) for b in range(0, D + 3 - e)
                     if sum(cnt[Dp][b] for Dp in range(D + 1)) != q ** (D + 1) * P[b])
    print(f"    H' two-sided bound on {cells} cells OK unless FAIL above; naive cumulative equality fails in {naive_fail} cells")
    if naive_fail == 0:
        bad('H naive equality never fails?', name)
# corrected law upper bound: N(X, D+1-e)/X^h bounded (A3, S2c)
for name, hh in (('A3', math.log(2 * math.sqrt(2), 3)), ('S2c', float(h)), ('Q4b', math.log(60.75, 4) / 3)):
    cnt = NOCT[name]
    S = SYS[name]
    q = S[0].q
    e = max(len(r) for r, _, _ in S[1])
    rat = []
    for D in range(D0(S), ENUM[name] + 1):
        b = D + 1 - e
        N = sum(cnt[Dp][b] for Dp in range(D + 1))
        rat.append(round(N / q ** ((D + 1) * hh), 3))
    print(f'  corrected law {name}: N(X, D+1-e)/X^h = {rat}')
    if max(rat) > 10:
        bad('corrected law constant large', name, rat)


# ---------------------------------------------------------------- 5. Theorem F
def compose(S, word):
    """G_w, H_w, L, slopes; H <- g H + t^E h_r, h_r = t^e c - g r"""
    F, brs = S
    G, H, E = [1], [], 0
    pref = []
    s = 0
    for i in word:
        r, g, c = brs[i]
        e = len(r)
        hr = padd(F, shift(c, e), [F.neg(x) for x in pmul(F, g, norm(list(r)))])
        G = pmul(F, g, G)
        H = padd(F, pmul(F, g, H), shift(hr, E))
        E += e
        s += dg(g) - e
        pref.append(s)
    return G, H, E, pref


def kappa(S):
    F, brs = S
    return max(max(dg(g) - 1, dg(c) if c else -1) for r, g, c in brs)


def words_of_length(S, L):
    brs = S[1]
    out = []

    def rec(rem, w):
        if rem == 0:
            out.append(tuple(w))
            return
        for i, (r, g, c) in enumerate(brs):
            if len(r) <= rem:
                w.append(i)
                rec(rem - len(r), w)
                w.pop()
    rec(L, [])
    return out


def check_F(name, word, L, cycles=None):
    S = SYS[name]
    F = S[0]
    G, H, E, pref = compose(S, word)
    assert E == L
    if pref[-1] != 0:
        return None
    tl = [0] * L + [1]
    diff = padd(F, G, [F.neg(x) for x in tl])
    if dg(diff) > 0:
        return False  # not a Frobenius word
    cw = diff[0] if diff else 0
    if cw == 0:
        bad('c_w = 0', name, word)
        return False
    x = psc(F, F.neg(F.inv(cw)), H)
    y = x
    orb = []
    for i in word:
        orb.append(tuple(y))
        y, j = T(S, y)
        if j != i:
            bad('Theorem F: wrong branch', name, word)
            return True
    if y != x:
        bad('Theorem F: not periodic', name, word)
    if min(pref) >= 0 and dg(x) > L + kappa(S):
        bad('Theorem F degree', name, word, dg(x))
    if cycles is not None:
        cycles.add(frozenset(orb))
    return True


print('5. Theorem F')
# S2c, L = 16: all words
cyc = set()
nF = nz = 0
for w in words_of_length(SYS['S2c'], 16):
    r = check_F('S2c', w, 16, cyc)
    if r is None:
        continue
    nz += 1
    if r:
        nF += 1
ZL16 = sum(comb(2 * a, a) * comb(a, 16 - 3 * a) for a in range(0, 6) if 0 <= 16 - 3 * a <= a)
nonzero_cycles = [c for c in cyc if c != frozenset({()})]
mindeg = [min(dg(list(p)) for p in c) for c in nonzero_cycles]
print(f'  S2c L=16: zero-slope words {nz} (Z_16 = {ZL16}), Frobenius {nF}, distinct cycles {len(cyc)}, '
      f'bound Z/L - 1 = {ZL16 / 16 - 1:.2f}, max min-degree {max(mindeg)} (<= 18)')
if nz != ZL16 or nF != nz or len(nonzero_cycles) < ZL16 / 16 - 1 or max(mindeg) > 18:
    bad('S2c Theorem F L=16')
# each min-degree point really never drops (check sigma > 300 directly)
for c in list(nonzero_cycles)[:40]:
    p = min(c, key=lambda z: dg(list(z)))
    if sigma(SYS['S2c'], list(p), 300) <= 300:
        bad('cycle min point drops', p)
# also: L = 12 is NOT a Frobenius length for S2c ((1+t)^12 not binomial) -> must find non-Frobenius words
nonF12 = sum(1 for w in words_of_length(SYS['S2c'], 12) if check_F('S2c', w, 12) is False)
print(f'  S2c L=12 (not 2^k): non-Frobenius zero-slope words {nonF12} (must be > 0)')
if nonF12 == 0:
    bad('discrimination L=12')
rng = random.Random(7)


def random_zero_slope(name, L, tries=200000):
    S = SYS[name]
    brs = S[1]
    for _ in range(tries):
        w, E, s = [], 0, 0
        while E < L:
            i = rng.randrange(len(brs))
            e = len(brs[i][0])
            if E + e > L:
                continue
            w.append(i)
            E += e
            s += dg(brs[i][1]) - e
        if s == 0:
            return tuple(w)
    return None


for name, Ls in (('S2c', (32, 64)), ('A3', (6, 18, 54)), ('Q4b', (6, 12, 24))):
    for L in Ls:
        ok = 0
        for _ in range(15):
            w = random_zero_slope(name, L)
            if w is None:
                continue
            r = check_F(name, w, L)
            if r is not True:
                bad('random Frobenius word not Frobenius', name, L, w)
            else:
                ok += 1
        print(f'  {name} L={L}: {ok} random zero-slope words are Frobenius and periodic')
# A3 L = 6: count cycles vs |W_L|/L - 1
cycA = set()
WA = [w for w in words_of_length(SYS['A3'], 6) if check_F('A3', w, 6, cycA)]
print(f'  A3 L=6: |W_6| = {len(WA)} (C(6,3)2^3 = {comb(6, 3) * 8}), cycles {len(cycA)} >= {len(WA) / 6 - 1:.1f}')
if len(WA) != comb(6, 3) * 8 or len(cycA) < len(WA) / 6 - 1:
    bad('A3 L=6')

# ---------------------------------------------------------------- 6. Theorem A''(b)
print("6. Theorem A''(b) exact")


def Z(L):
    return sum(comb(2 * a, a) * comb(a, L - 3 * a) for a in range(0, L // 3 + 1) if 0 <= L - 3 * a <= a)


for L in range(1, 19):
    brute = sum(1 for w in words_of_length(SYS['S2c'], L) if compose(SYS['S2c'], w)[3][-1] == 0)
    if brute != Z(L):
        bad('Z_L formula', L, brute, Z(L))
h_hi = Fr(str(h + Dc('1e-30')))  # rational > h: makes the check stricter


def ge_pow2(N, expo):
    """N >= 2^expo: integer test 2^ceil(expo) <= N (sufficient), else 80-digit Decimal log."""
    c = math.ceil(Fr(expo))
    if N >= 2 ** max(c, 0):
        return True
    return Dc(N).ln() / Dc(2).ln() >= Dc(Fr(expo).numerator) / Dc(Fr(expo).denominator) + Dc('1e-50')


for k in range(8, 14):
    L = 2 ** k
    ZL = Z(L)
    # Z_L (L+1)^2 >= 2^(hL - 4)
    if not ge_pow2(ZL * (L + 1) ** 2, h_hi * L - 4):
        bad("A''(b) Z_L", L)
    print(f'  L=2^{k}: log2(Z_L)/L = {math.log2(ZL) / L:.6f}; Z_L (L+1)^2 >= 2^(hL-4) exactly')
thf = float(th)
for k in range(8, 16):
    L = 2 ** k
    bstar = thf * L / (3 + thf)
    beta = min((bb for bb in range(int(bstar) - 3, int(bstar) + 5) if (bb - L) % 3 == 0),
               key=lambda bb: abs(bb - bstar))
    a = (L - beta) // 3
    term = comb(2 * a, a) * comb(a, beta)
    if not ge_pow2(term * (2 * a + 1) * (a + 1), h_hi * L - 4):
        bad("A''(b) chosen type term", L)
    # direct sanity of the slack: how far below hL is the bound actually used?
    slack = h_hi * L - (math.log2(term) + math.log2((2 * a + 1) * (a + 1)))
    if k in (8, 15):
        print(f'  L=2^{k}: chosen beta={beta}, theta={beta / a:.4f}; hL - log2(term*(2a+1)(a+1)) = {float(slack):.3f} (<= 4 needed)')
# monotone segment claim: theta(beta*+-2) moves toward theta* with L (analytic: sign of derivative = -delta)
prev = None
for L in range(256, 5000, 37):
    c = thf / (3 + thf)
    tp = (c * L + 2) / (((1 - c) * L - 2) / 3)
    tm = (c * L - 2) / (((1 - c) * L + 2) / 3)
    if prev and not (tp <= prev[0] + 1e-15 and tm >= prev[1] - 1e-15):
        bad('segment monotone', L)
    if not (0.3 <= tm <= tp <= 0.4):
        bad('segment in [0.3,0.4]', L)
    prev = (tp, tm)

# ---------------------------------------------------------------- 7. Lemma T, T1, T2
print('7. Lemma T, T1, T2')
for name in ('A3', 'Q4b', 'S2c', 'G3'):
    S = SYS[name]
    F = S[0]
    q = F.q
    kap = kappa(S)
    for _ in range(150):
        D = rng.randrange(3, 30)
        f = [rng.randrange(q) for _ in range(D)] + [rng.randrange(1, q)]
        n = rng.randrange(1, 40)
        y, w = f, []
        for _ in range(n):
            y, i = T(S, y)
            w.append(i)
        G, H, L, pref = compose(S, w)
        lhs = shift(y, L)
        rhs = padd(F, pmul(F, G, f), H)
        if lhs != rhs:
            bad('Lemma T affine', name)
        R = max(pref[-1] - p for p in pref)
        if H and dg(H) > L + kap + R:
            bad('Lemma T degree', name, dg(H), L + kap + R)
    print(f'  {name}: affine form and deg H_w <= L + kappa + R on 150 random (f, n)')
# T1/T2 on A3 cycles (one nonconstant multiplier 1+t^2: u = 1 + s^2, nu = 2, p = 3)
S = SYS['A3']
F = S[0]
seen = set()
nT2 = 0
for f in CYC_A3:
    y = f
    orbit = [tuple(y)]
    w = []
    for _ in range(2000):
        y, i = T(S, y)
        w.append(i)
        if tuple(y) == tuple(f):
            break
        orbit.append(tuple(y))
    if tuple(y) != tuple(f):
        continue  # not periodic itself (preperiodic or long)
    key = frozenset(orbit)
    if key in seen:
        continue
    seen.add(key)
    G, H, L, pref = compose(S, w)
    R = max(pref[-1] - p for p in pref)
    D = dg(f)
    diff = padd(F, [0] * L + [1], [F.neg(x) for x in G])
    if dg(diff) > L + 1 + R - D:
        bad('T1', f)
    Dp = D - 1 - R
    n1 = w.count(1)
    v = 0
    while n1 % 3 ** (v + 1) == 0:
        v += 1
    if Dp >= 1:
        nT2 += 1
        if 2 * 3 ** v < Dp:
            bad('T2', f, n1, D, R)
print(f'  A3: {len(seen)} distinct cycles through enumerated never-dropping polys; T1 OK; T2 tested on {nT2}')
if len(seen) == 0:
    bad('no A3 cycles found')

# ---------------------------------------------------------------- 8. integer side
print('8. integer side')
sols = [(L, a) for L in range(1, 400) for a in range(0, 260) if abs(2 ** L - 3 ** a) == 1]
print('  |2^L - 3^a| = 1:', sols)
if sols != [(1, 0), (1, 1), (2, 1), (3, 2)]:
    bad('catalan', sols)


def Ti(x, d):
    return x // 2 if x % 2 == 0 else (3 * x + d) // 2


for d, start in ((1, -17), (-1, 17), (5, 187), (5, 347), (-1, 1), (-1, 5)):
    y, L, a = start, 0, 0
    while True:
        a += y & 1
        y = Ti(y, d)
        L += 1
        if y == start or L > 500:
            break
    print(f'  3x{d:+d}: cycle through {start}: L={L}, a={a}, 2^L-3^a = {2 ** L - 3 ** a}')
    if y != start:
        bad('integer cycle', d, start)
# unit-denominator words for 3x-1 give the negatives of the 3x+1 set; the 17-cycle of 3x-1
# (denominator -139) is NOT of this type: the integer Theorem F does not 'explain' all cycles.
# Baker-type sanity (not a proof): min_a |2^L - 3^a| / 2^L over L <= 3000, times L^14
worst = min(abs(Fr(2 ** L - 3 ** round(L * math.log(2) / math.log(3) + s), 2 ** L)) * L ** 14
            for L in range(2, 3001) for s in (-1, 0, 1)
            if round(L * math.log(2) / math.log(3) + s) >= 0)
print(f'  min_L<=3000 |1 - 3^a/2^L| * L^14 = {float(worst):.3g} (Baker-shape sanity only)')

# ---------------------------------------------------------------- 9. quoted numbers
print('9. quoted numbers')
hA = math.log(2 * math.sqrt(2), 3)
cross = None
for k in range(1, 12):
    L = 2 * 3 ** k
    lhs = L * math.log(2 * math.sqrt(2), 3) - math.log(L * (L + 1), 3)  # log3 of main term
    rhs = (L + 2) - (1 - hA) * 2 * (L + 2)
    if lhs > rhs + 1e-9 and cross is None:
        cross = L
print(f'  Theorem A: explicit lower bound first beats X 3^-(1-h)b at b = 2 log_3 X for L = {cross} (quoted 486)')
if cross != 486:
    bad('crossing', cross)
L = 2048
lz = math.log2(Z(L) // L - 1)
lr = math.log2(float(rho_c))
Kthr = ((lz - (L + 3)) / lr + 1) / (L + 3)
print(f'  S2c L=2048 single-X threshold K = {Kthr:.4f} (quoted 1.083; referee 1 quoted 1.087)')
if abs(Kthr - 1.083) > 0.001:
    bad('K threshold', Kthr)

print()
if FAIL:
    print(f'REFEREE2 CHECK: {len(FAIL)} FAILURES')
    sys.exit(1)
print('REFEREE2 CHECK: all sections passed')
