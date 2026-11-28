"""Referee 1, independent check of census/round5/funcfield (written from scratch; imports
nothing from the prover's files).  Exits 1 on any failure.

Checks:
 1. Horizon lemma (exact): own enumeration of N_D(b) for A3 (D<=8), S2c (D<=12), Q4b (D<=5)
    against (q-1) q^D P(b) with an own exact P(b); also confirms that beyond the horizon the
    equality does FAIL somewhere (so the test can fail).
 2. Lemma T / T1 on random (f, n), not only on cycles: deg(t^L T^n f - G_w f) <= L+kappa+R.
 3. Theorem F: every zero-slope word of A3 (L=6), Q4b (L=6), S2c (L=8) gives a periodic
    polynomial point with the right word; random words at A3 L=18, S2c L=16; distinct-cycle
    count >= |W_L|/L; the never-dropping count found by enumeration of deg <= L+kappa is
    >= #cycles - 1.
 4. Theorem A arithmetic: exact integer inequality
       C(L,N) 2^N/(L(L+1)) >= 8^{(L+2)/2}/(9 (L+2)^2)  for L = 2*3^k, k<=8,
    exact Chernoff P(b)^2 <= (8/9)^b (A3), P(b)^3 <= (243/256)^b (Q4b), b<=200,
    and the 'L = 486 is the first crossing' claim, exactly.
 5. S2c: own Z_L (zero-slope words of digit length L) by the multinomial formula; rates
    log2(Z_L)/L; Chernoff rate h for S2c; exact P(b) <= 2 rho^(b-1) numerically.
 6. Generic control B3/G3: no zero-slope word with G_w = t^L + c for L <= 40 (by counts).
 7. Integer side: |2^L - 3^a| = 1 solutions (including a = 0); the cycles they give; and the
    3x+1 negative cycle through -17 and the 3x+5 cycles through 187, 347 have
    |2^L - 3^a| != 1 (so G's exceptional set is strictly larger than the 'Catalan' set).
"""
import sys, random, itertools
from fractions import Fraction
from math import comb, log, log2, sqrt

FAILS = []
CLAIMS = []   # (prover claim, holds?, detail)


def need(cond, *msg):
    if not cond:
        FAILS.append(msg)
        print('FAIL', *msg)


# ---------------- field arithmetic ----------------
class Field:
    def __init__(self, q):
        self.q = q
        if q == 4:
            # codes 0,1,2=w,3=w^2 ; w^2 = w+1 ; addition = XOR
            self.add = lambda a, b: a ^ b
            self.neg = lambda a: a
            exp = [1, 2, 3]
            lg = {1: 0, 2: 1, 3: 2}
            self.mul = lambda a, b: 0 if a == 0 or b == 0 else exp[(lg[a] + lg[b]) % 3]
        else:
            self.add = lambda a, b: (a + b) % q
            self.neg = lambda a: (-a) % q
            self.mul = lambda a, b: (a * b) % q
        self.inv = {a: next(b for b in range(1, q) if self.mul(a, b) == 1) for a in range(1, q)}


def tr(f):
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    return f


def pad(F, f, g):
    n = max(len(f), len(g))
    return tr([F.add(f[i] if i < len(f) else 0, g[i] if i < len(g) else 0) for i in range(n)])


def pmul(F, f, g):
    if not f or not g:
        return []
    o = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                if b:
                    o[i + j] = F.add(o[i + j], F.mul(a, b))
    return tr(o)


def pscal(F, c, f):
    return tr([F.mul(c, a) for a in f])


def dg(f):
    return len(f) - 1 if f else -1


def shift(f, k):
    return [0] * k + list(f) if f else []


# system: (F, [(r digits list, g, c)])
def mk(q, brs):
    return (Field(q), [(list(r), tr(g), tr(c)) for r, g, c in brs])


A3 = mk(3, [([0], [1], []), ([1], [1, 0, 1], []), ([2], [1], [1])])
B3 = mk(3, [([0], [1], []), ([1], [1, 1, 1], [1]), ([2], [2], [])])
G3 = mk(3, [([0], [1], []), ([1], [1, 1, 2], [1]), ([2], [2], [])])
Q4b = mk(4, [([0], [1], []), ([1], [1, 0, 0, 1], []), ([2], [1], [1]), ([3], [1], [])])
S2c = mk(2, [([0], [1], []), ([1, 0], [1, 1, 1, 1], [1]), ([1, 1], [1, 1], [1])])


def branch(S, f):
    F, brs = S
    for i, (r, g, c) in enumerate(brs):
        if all((f[k] if k < len(f) else 0) == r[k] for k in range(len(r))):
            return i
    raise RuntimeError


def T(S, f):
    F, brs = S
    i = branch(S, f)
    r, g, c = brs[i]
    u = pad(F, f, [F.neg(a) for a in r])
    e = len(r)
    assert all(a == 0 for a in u[:e])
    return pad(F, pmul(F, g, u[e:]), c), i, e


def slope(S, i):
    r, g, c = S[1][i]
    return dg(g) - len(r)


def kappa(S):
    return max(max(dg(g) - 1, dg(c) if c else 0) for r, g, c in S[1])


def Pexact(S, bmax):
    """P(b): Haar measure of x with S_k >= 0 at every step end with E_k <= b. Own DP over
    (digits, height) of the mass alive at step ends."""
    F, brs = S
    q = F.q
    law = [(Fraction(1, q ** len(r)), slope(S, i), len(r)) for i, (r, g, c) in enumerate(brs)]
    emax = max(e for _, _, e in law)
    alive = [dict() for _ in range(bmax + emax + 2)]
    alive[0][0] = Fraction(1)
    for d in range(bmax + 1):
        for h, m in alive[d].items():
            for p, s, e in law:
                if h + s >= 0:
                    alive[d + e][h + s] = alive[d + e].get(h + s, 0) + m * p
    # survive(b) = mass at step ends d<=b whose next step ends beyond b (and is not yet judged)
    P = []
    for b in range(bmax + 1):
        tot = Fraction(0)
        for d in range(max(0, b - emax + 1), b + 1):
            md = sum(alive[d].values())
            tot += md * sum(p for p, s, e in law if d + e > b)
        P.append(tot)
    return P


def sigma(S, f, cap):
    D = dg(f)
    x, dig = f, 0
    while dig <= cap:
        x, i, e = T(S, x)
        dig += e
        if dg(x) < D:
            return dig
    return cap + 1


def all_polys(q, D):
    for low in itertools.product(range(q), repeat=D):
        for lead in range(1, q):
            yield list(low) + [lead]


# ---------------- 1. horizon lemma ----------------
def horizon(S, name, Dmax, cap):
    q = S[0].q
    emax = max(len(r) for r, g, c in S[1])
    P = Pexact(S, cap)
    inh_bad = 0
    beyond_diff = 0
    for D in range(1, Dmax + 1):
        cnt = [0] * (cap + 2)
        for f in all_polys(q, D):
            s = sigma(S, f, cap)
            for b in range(min(s, cap + 1)):
                cnt[b] += 1
        for b in range(cap + 1):
            pred = (q - 1) * q ** D * P[b]
            if b + emax - 1 <= D and D >= 2:
                if pred != cnt[b]:
                    inh_bad += 1
            elif b > D and pred != cnt[b]:
                beyond_diff += 1
    print(f'[1] {name}: in-horizon mismatches {inh_bad}; beyond-horizon cells differing {beyond_diff}')
    need(inh_bad == 0, 'horizon', name)
    need(beyond_diff > 0, 'beyond horizon never differs (test cannot fail?)', name)
    return P


# ---------------- 2. Lemma T on random orbits ----------------
def compose(S, word):
    F, brs = S
    G, H, E = [1], [], 0
    for i in word:
        r, g, c = brs[i]
        e = len(r)
        h = pad(F, shift(c, e), [F.neg(a) for a in pmul(F, g, r)])   # h_r = t^e c - g r
        H = pad(F, pmul(F, g, H), shift(h, E))
        G = pmul(F, g, G)
        E += e
    return G, H, E


def lemmaT(S, name, trials=300):
    F = S[0]
    rng = random.Random(1)
    kap = kappa(S)
    for _ in range(trials):
        D = rng.randint(1, 30)
        f = [rng.randrange(F.q) for _ in range(D)] + [rng.randrange(1, F.q)]
        n = rng.randint(1, 40)
        x, w = f, []
        for _ in range(n):
            x, i, e = T(S, x)
            w.append(i)
        G, H, L = compose(S, w)
        # exact affine form
        lhs = shift(x, L)
        rhs = pad(F, pmul(F, G, f), H)
        need(lhs == rhs, 'affine form', name, f, w)
        Sp = list(itertools.accumulate(slope(S, i) for i in w))
        R = max(Sp[-1] - s for s in Sp)
        need(dg(H) <= L + kap + R, 'deg H', name, dg(H), L + kap + R)
    print(f'[2] {name}: Lemma T affine form and deg H bound on {trials} random (f, n)')


# ---------------- 3. Theorem F ----------------
def is_frob(S, G, L):
    return len(G) == L + 1 and G[L] == 1 and all(a == 0 for a in G[1:L]) and G[0] != 0


def word_from(S, x, L):
    w, dig = [], 0
    while dig < L:
        x, i, e = T(S, x)
        w.append(i)
        dig += e
    return w, x, dig


def zero_slope_words(S, L):
    """all words of digit length exactly L and total slope 0"""
    F, brs = S
    out = []

    def rec(w, dig, s):
        if dig == L:
            if s == 0:
                out.append(list(w))
            return
        for i, (r, g, c) in enumerate(brs):
            if dig + len(r) <= L:
                w.append(i)
                rec(w, dig + len(r), s + slope(S, i))
                w.pop()
    rec([], 0, 0)
    return out


def frob_point(S, w):
    F = S[0]
    G, H, L = compose(S, w)
    if not is_frob(S, G, L):
        return None, L
    c = G[0]
    x = pscal(F, F.neg(F.inv[c]), H)
    return x, L


def theoremF(S, name, L, sample=None, enum=True):
    F = S[0]
    kap = kappa(S)
    if sample is None:
        words = zero_slope_words(S, L)
    else:
        rng = random.Random(7)
        # random zero-slope words: random permutations of a fixed admissible multiset
        base = zero_slope_words(S, L) if L <= 10 else None
        words = []
        brs = S[1]
        while len(words) < sample:
            w, dig, s = [], 0, 0
            while dig < L:
                i = rng.randrange(len(brs))
                if dig + len(brs[i][0]) <= L:
                    w.append(i); dig += len(brs[i][0]); s += slope(S, i)
            if s == 0 and w not in words:
                words.append(w)
    pts = {}
    nonfrob = 0
    for w in words:
        x, L2 = frob_point(S, w)
        if x is None:
            nonfrob += 1
            continue
        w2, y, dig = word_from(S, x, L)
        need(w2 == w and y == x and dig == L, 'F periodic', name, w)
        Sp = list(itertools.accumulate(slope(S, i) for i in w))
        if min(Sp) >= 0:
            need(dg(x) <= L + kap, 'F degree', name, w, dg(x))
        pts[tuple(x)] = tuple(w)
    need(len(pts) == len(words) - nonfrob, 'F distinct', name)
    if sample is None:
        need(nonfrob == 0, 'binomial: some zero-slope word not Frobenius', name, nonfrob)
    # cycles
    cyc = set()
    for x in pts:
        orb, y = [], list(x)
        for _ in range(4 * L + 4):
            orb.append(tuple(y))
            y = T(S, y)[0]
            if tuple(y) == x:
                break
        cyc.add(min(orb))
    mins = []
    for c in cyc:
        orb, y = [], list(c)
        while True:
            orb.append(y)
            y = T(S, y)[0]
            if y == list(c):
                break
        mins.append(min(dg(z) for z in orb))
    nz = [m for m in mins if m >= 0]
    msg = f'[3] {name} L={L}: words {len(words)} (non-Frobenius {nonfrob}), distinct points {len(pts)}, cycles {len(cyc)}, bound |W|/L = {len(pts)/L:.1f}; max min-degree {max(mins)} <= L+kappa = {L+kap}'
    print(msg)
    need(len(cyc) >= len(pts) / L, 'cycle count bound', name)
    need(max(mins) <= L + kap, 'min degree', name)
    if enum and sample is None:
        # independent enumeration of never-dropping polys of deg <= L + kappa (certified by repeat)
        q = F.q
        never = 0
        unres = 0
        for D in range(0, L + kap + 1):
            for f in all_polys(q, D):
                x, seen, dropped = f, {tuple(f)}, False
                for _ in range(3000):
                    x = T(S, x)[0]
                    if dg(x) < D:
                        dropped = True; break
                    if tuple(x) in seen:
                        break
                    seen.add(tuple(x))
                    if dg(x) > D + 300:
                        unres += 1; dropped = True; break
                if not dropped:
                    never += 1
        print(f'    enumeration deg <= {L+kap}: certified never-dropping {never} (unresolved {unres}); need >= {len(nz)}')
        need(never >= len(nz), 'never-dropping count', name)


# ---------------- main ----------------
if __name__ == '__main__':
    PA3 = horizon(A3, 'A3', 8, 40)
    horizon(S2c, 'S2c', 12, 40)
    horizon(Q4b, 'Q4b', 5, 25)
    for S, n in ((A3, 'A3'), (B3, 'B3'), (G3, 'G3'), (Q4b, 'Q4b'), (S2c, 'S2c')):
        lemmaT(S, n)
    theoremF(A3, 'A3', 6)
    theoremF(Q4b, 'Q4b', 6)
    theoremF(S2c, 'S2c', 8)
    theoremF(A3, 'A3', 18, sample=300, enum=False)
    theoremF(S2c, 'S2c', 16, sample=300, enum=False)
    theoremF(Q4b, 'Q4b', 12, sample=200, enum=False)

    # ---- 4. Theorem A arithmetic, exact ----
    for k in range(1, 9):
        N = 3 ** k; L = 2 * N
        # chain: |W_L|/L = C(L,N) 2^N / L >= 8^N/(L(L+1)) >= 8^{N+1}/(9 (L+2)^2) = X^h/(9 log_3^2 X)
        need(comb(L, N) * (L + 1) >= 4 ** N, 'C(2N,N) >= 4^N/(2N+1)', k)
        need(9 * (L + 2) ** 2 >= 8 * L * (L + 1), 'Theorem A constant 9', k)
        need(comb(L, N) * 2 ** N * 9 * (L + 2) ** 2 >= 8 ** (N + 1) * L, 'Theorem A lower bound', k)
    P = Pexact(A3, 200)
    Q = Pexact(Q4b, 200)
    for b in range(201):
        need(P[b] ** 2 <= Fraction(8, 9) ** b, 'A3 Chernoff', b)
        need(Q[b] ** 3 <= Fraction(243, 256) ** b, 'Q4b Chernoff', b)
    # first L = 2*3^k at which lower bound > Chernoff bound for X P(2 log X): 3^{L+2} (8/9)^{L+2}
    first = None
    for k in range(1, 9):
        N = 3 ** k; L = 2 * N
        low = comb(L, N) * 2 ** N // (L * (L + 1)) - 1
        if low * 3 ** (L + 2) > 8 ** (L + 2):
            first = L; break
    print(f'[4] Theorem A exact inequalities ok; first crossing (C(L,N)2^N/(L(L+1)) - 1 vs Chernoff) at L = {first}')
    need(first == 486, 'crossing L', first)
    # same with the stated forms (2 sqrt2)^L/(L(L+1)) - 1 and X^h/(9 log^2 X) - 1  (X^h = 8^{N+1})
    for form in ('8^N/(L(L+1))', '8^(N+1)/(9(L+2)^2)'):
        fst = None
        for k in range(1, 9):
            N = 3 ** k; L = 2 * N
            num, den = (8 ** N, L * (L + 1)) if form[3] == 'N' and form[4] == '/' else (8 ** (N + 1), 9 * (L + 2) ** 2)
            if (num - den) * 3 ** (L + 2) > 8 ** (L + 2) * den:
                fst = L; break
        print(f'    first crossing with lower bound {form} - 1: L = {fst}')
        need(fst == 486, 'crossing (stated form)', form, fst)
    # ratio of the true exact P to the Chernoff bound (how loose is it?) at b = 200
    print(f'    A3: P(200) = 3^{log(P[200], 3):.2f}, Chernoff 3^{200*log(8/9,3)/2:.2f}')

    # ---- 5. S2c ----
    def ZL(L):
        z = 0
        for a in range(0, L // 3 + 1):
            b = L - 3 * a
            if 0 <= b <= a:
                n0 = a - b
                n = n0 + a + b
                z += comb(n, a) * comb(n - a, b)
        return z
    # brute check of ZL for small L against word enumeration
    for L in range(1, 15):
        need(ZL(L) == len(zero_slope_words(S2c, L)), 'Z_L formula', L)
    rates = [(L, log2(ZL(L)) / L) for L in (32, 64, 128, 256, 512, 1024, 2048)]
    print('[5] S2c log2(Z_L)/L:', ' '.join(f'{L}:{r:.3f}' for L, r in rates))
    # Chernoff rate: rho(lam) solves 4 lam rho^2 - 2 rho - (lam^2+1) = 0
    def rho(l):
        return (2 + sqrt(4 + 16 * l * (l * l + 1))) / (8 * l)
    lo, hi = 1.0, 4.0
    for _ in range(200):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if rho(m1) < rho(m2):
            hi = m2
        else:
            lo = m1
    lam = (lo + hi) / 2
    r = rho(lam)
    h = 1 + log2(r)
    print(f'    S2c Chernoff: lambda = {lam:.6f}, rho = {r:.6f}, h = {h:.5f}')
    need(abs(h - 0.87585) < 5e-5, 'S2c h (own value)', h)
    CLAIMS.append(('S2c Haar h = 0.8703 (README table, theory sec. 3)', abs(h - 0.8703) < 5e-4, f'own exact Chernoff/saddle rate {h:.5f}'))
    CLAIMS.append(('S2c: log2(Z_L)/L increases to h = 0.8703', rates[-1][1] <= 0.8703, f'already {rates[-1][1]:.4f} at L=2048'))
    # finite-b decay estimate as in analyse.py (ratio over 40 digits near b = 400): reproduces 0.870?
    PS4 = Pexact(S2c, 400)
    hemp = 1 + log2(float(PS4[400] / PS4[360]) ** (1 / 40))
    print(f'    S2c finite-b estimate from P(400)/P(360): h_emp = {hemp:.4f} (b^(-3/2) bias)')
    # K threshold at L = 2048 with the proved bounds N >= Z_L/L - 1, X P(b) <= X * 2 rho^(b-1), X = 2^(L+3)
    L = 2048; lx = L + 3
    lN = log2(ZL(L)) - log2(L)
    K = next(K / 1000 for K in range(1000, 3000) if lN > lx + 1 + log2(r) * (K / 1000 * lx - 1))
    print(f'    S2c L=2048: E_F inequality violated (proved bounds) for K >= {K:.3f}')
    PS = Pexact(S2c, 300)
    worst = max(float(PS[b]) / (2 * r ** (b - 1)) for b in range(1, 301))
    print(f'    S2c: max_b P(b) / (2 rho^(b-1)) = {worst:.4f} (must be <= 1)')
    need(worst <= 1.0, 'S2c Chernoff')
    # max multinomial term vs Z_L (elementary route to the asymptotic rate)
    L = 2048
    mx = max(comb(2 * a, a) * comb(a, L - 3 * a) for a in range(L // 4, L // 3 + 1) if 0 <= L - 3 * a <= a)
    print(f'    S2c L=2048: log2(max multinomial)/L = {log2(mx)/L:.4f}')

    # ---- 6. generic controls ----
    for S, n in ((B3, 'B3'), (G3, 'G3')):
        F = S[0]
        g1 = S[1][1][1]
        hit = 0
        for a in range(1, 21):            # n_1 = a uses, L = 2a, zero slope
            Gp = [1]
            for _ in range(2 * a if False else a):
                Gp = pmul(F, Gp, g1)
            # constants from branch 2 only rescale
            L = 2 * a
            Gm = pscal(F, F.inv[Gp[-1]], Gp)
            if all(x == 0 for x in Gm[1:L]) and len(Gm) == L + 1:
                hit += 1
        print(f'[6] {n}: zero-slope Frobenius words with L <= 40: {hit}')
        need(hit == 0, 'generic has Frobenius word', n)

    # ---- 7. integer side ----
    sols = [(L, a) for L in range(1, 300) for a in range(0, L + 1) if abs(2 ** L - 3 ** a) == 1]
    print('[7] |2^L - 3^a| = 1:', sols)
    need(sols == [(1, 0), (1, 1), (2, 1), (3, 2)], 'catalan list', sols)

    def Tz(x, d):
        return x // 2 if x % 2 == 0 else (3 * x + d) // 2

    def cyc_La(x, d):
        y, L, a = x, 0, 0
        while True:
            a += y % 2; L += 1
            y = Tz(y, d)
            if y == x:
                return L, a
    for x, d in ((-17, 1), (187, 5), (347, 5), (-1, 1), (1, 1), (-5, 1)):
        L, a = cyc_La(x, d)
        print(f'    3x+{d} cycle through {x}: L={L}, a={a}, 2^L-3^a = {2**L - 3**a}')
    need(abs(2 ** cyc_La(-17, 1)[0] - 3 ** cyc_La(-17, 1)[1]) != 1, '-17 cycle')

    # ---- control: Hicks-Mullen-Yucas-Zavislak F_2[t] map f/t, ((1+t)f+1)/t (all orbits reach 1)
    HM = mk(2, [([0], [1], []), ([1], [1, 1], [1])])
    for L in (4, 8, 16):          # zero_slope_words enumerates all 2^L words
        pts = set()
        for w in zero_slope_words(HM, L):
            x, _ = frob_point(HM, w)
            need(x is not None, 'HMYZ Frobenius', L)
            pts.add(tuple(x))
        need(pts == {(1,)}, 'HMYZ Frobenius points', L, pts)
    bad = 0
    for D in range(0, 13):
        for f in all_polys(2, D):
            x = f
            for _ in range(10 * (D + 2) ** 2):
                if x == [1]:
                    break
                x = T(HM, x)[0]
            bad += x != [1]
    print(f'[ctl] HMYZ map: Theorem F gives only the fixed point 1; all polys of deg <= 12 reach 1: {bad == 0}')
    need(bad == 0, 'HMYZ control')

    # ---- U: the A3 'growing' orbit (evidence) ----
    f = [1, 1, 1, 0, 2, 2, 0, 2]
    x = f
    for k in range(1, 6001):
        x = T(A3, x)[0]
    print(f'[U] A3 orbit of 1+t+t^2+2t^4+2t^5+2t^7 after 6000 steps: degree {dg(x)} ({dg(x)/6000:.3f}/step)')

    print('Prover claims tested numerically:')
    for c, ok, d in CLAIMS:
        print(f'   {"HOLDS " if ok else "REFUTED"}  {c}  [{d}]')
    if FAILS:
        print('REFEREE CHECK FAILED', len(FAILS))
        sys.exit(1)
    print('referee1 checks passed')
