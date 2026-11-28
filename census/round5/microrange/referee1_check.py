"""Referee 1, independent checks for census/round5/microrange (written from scratch).

Run:  /home/riv/Code/collatz/census/round4/wpotential/.venv/bin/python referee1_check.py
Exits 1 if any exact check fails.  Nothing here reuses the prover's code except in part X, where
the prover's bounds are compared against this file's own implementation.

  T. Terras identity and the 3x+d conjugacy, exact (Python ints, negative values included).
  R. Theorem R from scratch: own survivor sets (direct simulation of 3x+d, NOT via conjugacy), own
     Cnt_d (direct enumeration of residues), own Phi (cyclic window sums), own brute force N(2^m, m+j).
     Checks (a) the exact middle step N = sum_r Phi(3^A, T^d(r)); (b) L <= N <= U; (c) the identity
     sum Cnt * |S| / 2^j = 2^m P(m+j); for 3x+1, 3x-1, 3x+5.  A mutation test (multiplier 3^(A+1))
     must make (a) fail, showing the check is able to fail.
  X. Large-m cross-check: own Theorem R bounds at m = 101, 290, 751 (j = 4, j' = 18, K = 22) against
     README Table 2, and at m = 1000 (j = 8, j' = 12) against the prover's microlib.
  F. Lemma F exactly (Fractions) for RANDOM sets S (the lemma claims every S), and survivor sets,
     cosets 1, -1, 5^-1.
  P. Lemma P exactly for every depth d < 6000 at K = 8, 16, 24.
  M. Lemma M: own DP, supermultiplicativity, h0 at K0 = 2000.
  S. sigma >= tau for 3x+1 (exact, n < 2^20); for 3x-1 the README's one-line proof does not apply
     (negative constant term), the count of sigma < tau is only reported.
  G. Coset (in)dependence: (i) D'-type worst-slot densities at K = 12, j = 1 for cosets 1, -1, 5^-1
     (they coincide, because Phi(-u, B) = Phi(u, B - u(N-1)) and the units are <3> u -<3>);
     (ii) Theorem C-type certificates are NOT coset-invariant: 3x+5 bounds differ from 3x+1, 3x-1 equal.
  E. Bad-multiplier evidence at K = 16, j = 2, slot 0.
"""
import math
import os
import random
import sys
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FAILS = 0


def check(cond, msg):
    global FAILS
    if not cond:
        FAILS += 1
        print('  FAIL', msg)


def amin(b):
    a = 0
    while 3 ** a < 2 ** b:
        a += 1
    return a


AMIN = [amin(b) for b in range(0, 6100)]
LAM = math.log(2) / math.log(3)


def Tstep(x, dd):
    return (3 * x + dd) // 2 if x % 2 else x // 2      # exact for negative x too (x odd => 3x+dd even)


# ------------------------------------------------------------------ T
random.seed(1)
for dd in (1, -1, 5, -3, 7):
    for _ in range(400):
        d = random.randint(0, 50)
        r = random.randrange(-(1 << d), 1 << d) if d else 0
        s = random.randrange(-(1 << 60), 1 << 60)
        x, y, A, ok = r, r + (s << d), 0, True
        for _ in range(d):
            ok &= (x % 2) == (y % 2)
            A += x % 2
            x, y = Tstep(x, dd), Tstep(y, dd)
        check(ok and y == 3 ** A * s + x, ('terras', dd, d, r, s))
    # conjugacy over Z_2 modulo 2^K: parity words of x under 3x+dd = those of x/dd under 3x+1
    K, Q = 14, 1 << 14
    inv = pow(dd % Q, -1, Q)
    for x0 in random.sample(range(Q), 300):
        x, y, ok = x0, x0 * inv % Q, True
        for _ in range(K):
            ok &= (x % 2) == (y % 2)
            x, y = Tstep(x, dd), Tstep(y, 1)
        check(ok, ('conj', dd, x0))
print('T. Terras identity (incl. negative r, s) and conjugacy: done')


# ------------------------------------------------------------------ own primitives
def odd_counts(x0, steps, dd):
    """numpy: A_i for i = 1..steps for int64 starts x0 (values must stay in range)."""
    x = x0.astype(np.int64).copy()
    out = np.zeros((steps, len(x)), dtype=np.int16)
    a = np.zeros(len(x), dtype=np.int16)
    for i in range(steps):
        o = (x & 1).astype(bool)
        a = a + o
        out[i] = a
        x = np.where(o, (3 * x + dd) >> 1, x >> 1)
    return out


def survivor_set(K, th, dd):
    """S = {x mod 2^K : A_i(x) >= th_i, i = 1..K} for the map 3x+dd, by direct simulation.
    Starts x0 in [2^K, 2^(K+1)) represent the residues (keeps 3x+dd positive for dd >= -1)."""
    Q = 1 << K
    x0 = np.arange(Q, 2 * Q, dtype=np.int64)
    ok = np.ones(Q, dtype=bool)
    x = x0.copy()
    a = np.zeros(Q, dtype=np.int64)
    for i in range(K):
        o = (x & 1).astype(bool)
        a += o
        ok &= a >= th[i]
        x = np.where(o, (3 * x + dd) >> 1, x >> 1)
    S = np.zeros(Q, dtype=np.int8)
    S[(x0 - Q)] = ok
    return S


def window_minmax(S, u, jp):
    """max_B and min_B of Phi(u, B) = #{0 <= s < 2^jp : S[(u s + B) mod Q]} by cyclic window sums of
    g[y] = S[u y], since u s + B = u (s + B') with B' = u^-1 B."""
    Q = len(S)
    y = np.arange(Q, dtype=np.int64)
    g = S[(u * y) % Q].astype(np.int64)
    N = 1 << jp
    c = np.concatenate([[0], np.cumsum(np.concatenate([g, g[:N]]))])
    w = c[N:N + Q] - c[:Q]
    return int(w.max()), int(w.min()), int(g.sum())


def window_all(S, u, jp):
    """Phi(u, B) for every B (array indexed by B)."""
    Q = len(S)
    y = np.arange(Q, dtype=np.int64)
    g = S[(u * y) % Q].astype(np.int64)
    N = 1 << jp
    c = np.concatenate([[0], np.cumsum(np.concatenate([g, g[:N]]))])
    w = c[N:N + Q] - c[:Q]                      # w[B'] = Phi(u, u B')
    out = np.empty(Q, dtype=np.int64)
    out[(u * y) % Q] = w
    return out


def phi_at(S, u, jp, B):
    Q = len(S)
    s = np.arange(1 << jp, dtype=np.int64)
    return int(S[(u * s + B) % Q].sum())


# ------------------------------------------------------------------ R (small m, brute force)
def brute_tau(m, b, dd):
    """N(2^m, b) = #{0 <= n < 2^m : A_i(n) >= amin(i), i <= b}."""
    n = np.arange(0, 1 << m, dtype=np.int64)
    x = n.copy()
    a = np.zeros(len(n), dtype=np.int64)
    alive = np.ones(len(n), dtype=bool)
    for i in range(1, b + 1):
        o = (x & 1).astype(bool)
        a += o
        alive &= a >= AMIN[i]
        x = np.where(o, (3 * x + dd) >> 1, x >> 1)
    return int(alive.sum())


def residues_depth(d, dd):
    """for r < 2^d: survives d steps?, A_d(r), T^d(r) (exact; numpy int64)."""
    r = np.arange(0, 1 << d, dtype=np.int64)
    x = r.copy()
    a = np.zeros(len(r), dtype=np.int64)
    alive = np.ones(len(r), dtype=bool)
    for i in range(1, d + 1):
        o = (x & 1).astype(bool)
        a += o
        alive &= a >= AMIN[i]
        x = np.where(o, (3 * x + dd) >> 1, x >> 1)
    return alive, a, x


def surv_count(b):
    """#surv(b) by own DP over parity words (dict A -> count)."""
    cur = {0: 1}
    for i in range(1, b + 1):
        nx = {}
        for a, c in cur.items():
            for a2 in (a, a + 1):
                if a2 >= AMIN[i]:
                    nx[a2] = nx.get(a2, 0) + c
        cur = nx
    return cur


ncase = 0
mutation_caught = 0
widths = []
for dd in (1, -1, 5):
    for m in range(12, 21):
        for j in (1, 2, 3, 5):
            Nb = brute_tau(m, m + j, dd)
            for jp in (j, j + 3, j + 7):
                if jp > m:
                    continue
                d, K = m - jp, j + jp
                Q = 1 << K
                alive, Ad, Bd = residues_depth(d, dd)
                L = U = exact = mut = 0
                main = Fraction(0)
                Scache = {}
                for A in sorted(set(Ad[alive].tolist())):
                    sel = alive & (Ad == A)
                    w = int(sel.sum())
                    th = [AMIN[d + i] - A for i in range(1, K + 1)]
                    if A not in Scache:
                        Scache[A] = survivor_set(K, th, dd)
                    S = Scache[A]
                    u = pow(3, A, Q)
                    mx, mn, size = window_minmax(S, u, jp)
                    L += w * mn
                    U += w * mx
                    main += Fraction(w * size, 1 << j)
                    Bs = Bd[sel] % Q
                    ph = window_all(S, u, jp)
                    exact += int(ph[Bs].sum())
                    mut += int(window_all(S, u * 3 % Q, jp)[Bs].sum())
                    # spot-check window_all against the naive definition
                    for B in Bs[:3].tolist():
                        check(ph[B] == phi_at(S, u, jp, B), ('window_all', B))
                check(exact == Nb, ('R exact middle step', dd, m, j, jp, exact, Nb))
                check(L <= Nb <= U, ('R bounds', dd, m, j, jp, L, Nb, U))
                # 2^m P(m+j) computed by own DP: #surv(m+j) / 2^j
                P_direct = Fraction(sum(surv_count(m + j).values()), 1 << j)
                check(main == P_direct, ('R identity', dd, m, j, jp))
                if mut != Nb:
                    mutation_caught += 1
                widths.append(float(Fraction(U - L, 1) / P_direct))
                ncase += 1
print('R. Theorem R from scratch: %d cases (3x+1, 3x-1, 3x+5; m = 12..20; j in 1,2,3,5): exact middle step,'
      ' L <= N <= U, identity; mutation 3^(A+1) changed the count in %d cases' % (ncase, mutation_caught))
check(mutation_caught > ncase // 2, 'mutation test did not bite: checker cannot fail')
print('   median relative width (U-L)/2^mP = %.4f' % sorted(widths)[len(widths) // 2])


# ------------------------------------------------------------------ X (large m, own implementation)
def cnt_dp(d):
    cur = {0: 1}
    for i in range(1, d + 1):
        nx = {}
        lo = AMIN[i]
        for a, c in cur.items():
            if a >= lo:
                nx[a] = nx.get(a, 0) + c
            if a + 1 >= lo:
                nx[a + 1] = nx.get(a + 1, 0) + c
        cur = nx
    return cur


def own_bounds(m, j, jp, dd=1):
    d, K = m - jp, j + jp
    Q = 1 << K
    inv = pow(dd % Q, -1, Q)
    L = U = 0
    main = Fraction(0)
    for A, w in cnt_dp(d).items():
        th = [AMIN[d + i] - A for i in range(1, K + 1)]
        if max(th) <= 0:
            L += w << jp
            U += w << jp
            main += Fraction(w << K, 1 << j)
            continue
        S = survivor_set(K, th, 1)
        mx, mn, size = window_minmax(S, pow(3, A, Q) * inv % Q, jp)
        L += w * mn
        U += w * mx
        main += Fraction(w * size, 1 << j)
    return L, U, main


for m, claim in ((290, 0.00617), (751, 0.0055), (101, 0.0051)):
    L, U, main = own_bounds(m, 4, 18)
    check(main == Fraction(sum(cnt_dp(m + 4).values()), 16), ('X identity', m))
    hw = max(float(1 - Fraction(L) / main), float(Fraction(U) / main - 1))
    print('X. m = %d, j = 4, j\' = 18: own half-width %.5f (README Table 2: %.4f)' % (m, hw, claim))
    check(abs(hw - claim) < 6e-5, ('X table2', m, hw, claim))
try:
    sys.path.insert(0, HERE)
    import microlib
    r = microlib.bounds(1000, 8, 12, microlib.Disc())
    L, U, main = own_bounds(1000, 8, 12)
    check((L, U, main) == (r['lower'], r['upper'], r['main']), 'X microlib m=1000')
    print('X. m = 1000, j = 8, j\' = 12: own (L, U, main) == prover microlib exactly: %s; rel [%+.5f, %+.5f]'
          % ((L, U, main) == (r['lower'], r['upper'], r['main']), float(Fraction(L) / main - 1),
             float(Fraction(U) / main - 1)))
    L, U, main = own_bounds(200, 3, 12, dd=-1)
    r = microlib.bounds(200, 3, 12, microlib.Disc(), dd=-1)
    check((L, U, main) == (r['lower'], r['upper'], r['main']), 'X microlib 3x-1')
    print('X. 3x-1, m = 200, j = 3, j\' = 12: own == prover: %s' % ((L, U, main) == (r['lower'], r['upper'], r['main'])))
except Exception as e:  # pragma: no cover
    check(False, ('X microlib unavailable', e))


# ------------------------------------------------------------------ F
def gK(K):
    return 4 * (1 + Fraction(3466, 10000) * (K - 1))


def lemmaF_case(S, K, j, coset):
    Q = 1 << K
    jp = K - j
    size = int(S.sum())
    q = Q >> 2
    tot = Fraction(0)
    for a in range(q):
        u = coset * pow(3, a, Q) % Q
        mx, mn, _ = window_minmax(S, u, jp)
        tot += max(Fraction(mx) - Fraction(size, 1 << j), Fraction(size, 1 << j) - mn)
    lhs = tot / q
    rhs2 = gK(K) ** 2 * Fraction(size * (Q - size), Q)
    return lhs, rhs2


worstF = 0.0
nF = 0
rng = np.random.default_rng(5)
for K in (8, 9, 10):
    Q = 1 << K
    for j in (1, 2, 3):
        for kind in range(6):
            if kind < 3:
                dens = (0.03, 0.3, 0.7)[kind]
                S = (rng.random(Q) < dens).astype(np.int8)
            elif kind == 3:
                S = np.zeros(Q, dtype=np.int8)
                S[:Q // 3] = 1                       # an interval: adversarial for lines with u near 1
            elif kind == 4:
                S = (np.arange(Q) % 4 == 1).astype(np.int8)   # a 2-adic ball
            else:
                th = [AMIN[i] for i in range(1, K + 1)]
                S = survivor_set(K, th, 1)
            for coset in (1, Q - 1, pow(5, -1, Q)):
                lhs, rhs2 = lemmaF_case(S, K, j, coset)
                check(lhs * lhs <= rhs2, ('F', K, j, kind, coset, float(lhs), float(rhs2) ** .5))
                if rhs2:
                    worstF = max(worstF, float(lhs) / float(rhs2) ** .5)
                nF += 1
print('F. Lemma F exact on %d cases incl. random sets, intervals, balls: max LHS/RHS = %.4f' % (nF, worstF))

# ------------------------------------------------------------------ P
for K in (8, 16, 24):
    pats = {}
    nontriv_max = 0
    for d in range(0, 6000 - K):
        nt = 0
        for k in range(0, K + 3):
            A = AMIN[d] + k
            th = tuple(AMIN[d + i] - A for i in range(1, K + 1))
            check(all(th[i - 1] <= AMIN[i] for i in range(1, K + 1)), ('P th<=amin', K, d, k))
            if max(th) > 0:
                nt += 1
                pats.setdefault(k, set()).add(th)
        nontriv_max = max(nontriv_max, nt)
    check(nontriv_max <= math.floor(K * LAM) + 1, ('P n_s', K, nontriv_max))
    mp = max(len(v) for v in pats.values())
    check(mp <= K + 1, ('P patterns', K, mp))
    print('P. K = %d: th <= amin for all d < %d; nontrivial slots <= %d (bound %d); patterns/slot <= %d (bound %d)'
          % (K, 6000 - K, nontriv_max, math.floor(K * LAM) + 1, mp, K + 1))

# ------------------------------------------------------------------ M
sv = [1]
cur = {0: 1}
for i in range(1, 2001):
    nx = {}
    for a, c in cur.items():
        for a2 in (a, a + 1):
            if a2 >= AMIN[i]:
                nx[a2] = nx.get(a2, 0) + c
    cur = nx
    sv.append(sum(cur.values()))
for a in range(1, 70):
    for b in range(1, 70):
        check(sv[a + b] >= sv[a] * sv[b], ('M', a, b))
h0 = (sv[2000].bit_length() - 1) / 2000
check(h0 >= 0.9430, ('h0', h0))
print('M. supermultiplicative for a, b < 70; log2 #surv(2000)/2000 >= %.5f' % h0)

# ------------------------------------------------------------------ S
n = np.arange(1, 1 << 20, dtype=np.int64)
for dd in (1, -1):
    x = n.copy()
    a = np.zeros(len(n), dtype=np.int64)
    tau = np.full(len(n), 10 ** 6)
    sig = np.full(len(n), 10 ** 6)
    for i in range(1, 200):
        o = (x & 1).astype(bool)
        a += o
        x = np.where(o, (3 * x + dd) >> 1, x >> 1)
        tau = np.where((tau == 10 ** 6) & (a < AMIN[i]), i, tau)
        sig = np.where((sig == 10 ** 6) & (x < n), i, sig)
    bad = int((sig < tau).sum())
    if dd == 1:
        check(bad == 0, ('sigma>=tau', bad))
    print('S. 3x%+d, n < 2^20: #{sigma < tau} = %d' % (dd, bad))

# ------------------------------------------------------------------ G (coset dependence of D'-type densities)
K, j = 12, 1
Q, q, jp = 1 << K, 1 << 10, K - 1
bps = sorted(set([0.0, 1.0] + [1 - (i * LAM % 1) for i in range(1, K + 1)]))
res = {}
for coset_name, coset in (('1', 1), ('-1', Q - 1), ('5^-1', pow(5, -1, Q))):
    dens = 0.0
    for lo, hi in zip(bps, bps[1:]):
        f = (lo + hi) / 2
        for k in range(0, K + 2):
            th = [math.ceil(f - 1 - k + i * LAM) for i in range(1, K + 1)]
            if max(th) <= 0:
                continue
            S = survivor_set(K, th, 1)
            size = int(S.sum())
            nb = 0
            for a in range(q):
                mx, mn, _ = window_minmax(S, coset * pow(3, a, Q) % Q, jp)
                if max(mx * 2 - size, size - 2 * mn) > 0.05 * size:
                    nb += 1
            dens += (hi - lo) * nb / q
    res[coset_name] = dens
print('G. K = 12, j = 1, eps = 0.05, worst-slot density bound by coset: %s'
      % ', '.join('%s: %.4f' % kv for kv in res.items()))
check(abs(res['1'] - res['-1']) < 1e-12 and abs(res['1'] - res['5^-1']) < 1e-12, ('G coset invariance', res))
# reflection identity, exact, random S
Q, jp = 1 << 10, 7
S = (rng.random(Q) < 0.4).astype(np.int8)
for u in (3, 27, 1001, 5):
    a1, a2 = window_all(S, u, jp), window_all(S, Q - u, jp)
    N = 1 << jp
    check(all(a2[B] == a1[(B - u * (N - 1)) % Q] for B in range(Q)), ('reflection', u))
b1, b5, bm = own_bounds(120, 3, 10, 1), own_bounds(120, 3, 10, 5), own_bounds(120, 3, 10, -1)
check(b1 == bm, 'G: 3x-1 certificate should equal 3x+1')
print('G. reflection identity exact; m = 120, j = 3: 3x-1 certificate == 3x+1: %s; 3x+5 == 3x+1: %s'
      % (b1 == bm, b1 == b5))

# ------------------------------------------------------------------ E (bad multipliers, evidence)
K, j = 16, 2
Q, q, jp = 1 << K, 1 << 14, K - 2
bps = sorted(set([0.0, 1.0] + [1 - (i * LAM % 1) for i in range(1, K + 1)]))
best = (0, None)
means = []
samp = random.Random(3).sample(range(q), 200)
for lo, hi in zip(bps, bps[1:]):
    f = (lo + hi) / 2
    th = [math.ceil(f - 1 + i * LAM) for i in range(1, K + 1)]     # slot k = 0
    S = survivor_set(K, th, 1)
    size = int(S.sum())
    phib = size / 4

    def r_of(a):
        mx, mn, _ = window_minmax(S, pow(3, a, Q), jp)
        return max(mx - phib, phib - mn) / phib
    for t in range(4):
        a = (-8 + 4096 * t) % q
        best = max(best, (r_of(a), (a, round(f, 3))))
    means.append(sum(r_of(a) for a in samp) / len(samp))
print('E. K = 16, j = 2, slot 0: max r over a = -8 mod 2^12 is %.3f at %s; mean r over random a, by pattern:'
      ' %.3f .. %.3f' % (best[0], best[1], min(means), max(means)))

print('FAILS: %d' % FAILS)
sys.exit(1 if FAILS else 0)
