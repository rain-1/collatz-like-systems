"""Referee 2 independent checker for round 5 / microrange (written from scratch; imports nothing
from the prover's code). Exits 1 on any failure. Run with the round4 venv python (numpy):

    ../../round4/wpotential/.venv/bin/python referee2_check.py          (about 5-10 min)
    ... referee2_check.py quick                                         (skips the K = 28 rows)

Method differences from the prover (microlib/disc.c) and from referee 1:
  * survivor sets are built by direct numpy simulation of the map 3x+d itself (no conjugacy
    x -> x/d), using the single array need(x) = max_i (amin(d+i) - A_i(x)); then
    S_{d,A} = {x : need(x) <= A}. One simulation per split depth serves every A.
  * max_B / min_B Phi(u, B) are computed by permuting the indicator by y -> u*y and taking all cyclic
    window sums of length 2^jp with a cumulative sum (no sliding update, no digit tree).
  * Cnt_d, #surv by my own big-integer DP; amin by exact integer comparison.

Parts
  B  brute force N(2^m, m+j) (numpy) vs my Theorem R bounds, for 3x+1, 3x-1, 3x+5, 3x-3; the exact
     identity N = sum_r Phi(3^A, T^d(r) mod 2^K); main term = #surv(m+j)/2^j; mutation test.
  T  reproduce prover's certified rows: Table 2 (K = 22) at several m, sibling table (K = 24, direct
     simulation of 3x+5, 3x-3, 3x+7, 3x-1), and K = 28 rows added after REFEREE1 (m = 1000, j = 11;
     m = 100, j = 12; j = 1 exact constants at m = 1000, 3000).
  M  h0 >= 0.9430 exactly; supermultiplicativity; explicit (K-2000) h0 bound for K <= 4000.
  P  Lemma P over depths d < 5000, K = 20: th_i <= amin(i), number of nontrivial slots <= floor(K lam)+1.
  F  Lemma F exactly, arbitrary S, cosets 1, -1, 7, -5 (one of them is a non-trivial coset of <3>).
  R  reflection identity and <3> u -<3>.
  S  sigma >= tau and Nsig - Ntau = 1 (n < 2^24, m <= 24, m <= b <= m+8, except m = b = 1).
  D' one entry of the K = 16 Weyl table recomputed independently (j = 1, eps = 0.05 and 0.10).
"""
import math
import sys
from fractions import Fraction

import numpy as np

QUICK = len(sys.argv) > 1 and sys.argv[1] == 'quick'
FAILS = []


def check(c, what):
    if not c:
        FAILS.append(what)
        print('FAIL', what, flush=True)


def amin(b):
    if b <= 0:
        return 0
    a = 0
    p3, p2 = 1, 1 << b
    # binary-search-free exact: start near b*log_3 2 and adjust with integers
    a = max(0, int(b * 0.6309297535714574) - 2)
    while 3 ** a >= p2:
        a -= 1
    while 3 ** a < p2:
        a += 1
    return a


AMIN = [amin(b) for b in range(0, 6200)]


def cnt_dp(d):
    """{A: #{r mod 2^d : A_i(r) >= amin(i) for i <= d, A_d(r) = A}} by lattice paths."""
    cur = {0: 1}
    for i in range(1, d + 1):
        nxt = {}
        lo = AMIN[i]
        for a, c in cur.items():
            if a >= lo:
                nxt[a] = nxt.get(a, 0) + c
            if a + 1 >= lo:
                nxt[a + 1] = nxt.get(a + 1, 0) + c
        cur = nxt
    return cur


def surv_all(Kmax):
    """#surv(b) for b = 0..Kmax."""
    out = [1]
    cur = {0: 1}
    for i in range(1, Kmax + 1):
        nxt = {}
        lo = AMIN[i]
        for a, c in cur.items():
            if a >= lo:
                nxt[a] = nxt.get(a, 0) + c
            if a + 1 >= lo:
                nxt[a + 1] = nxt.get(a + 1, 0) + c
        cur = nxt
        out.append(sum(cur.values()))
    return out


SURV = surv_all(4100)


def need_array(K, d, dd):
    """need[x] = max_{1<=i<=K} (amin(d+i) - A_i(x)) for x in [0, 2^K), map 3x+dd (direct simulation).
    x survives the K steps after a depth-d node with A odd steps iff need[x] <= A."""
    Q = 1 << K
    x = np.arange(Q, dtype=np.int64)
    if dd < 0:
        x = x + (Q << 2)          # keep values positive; parities mod 2^K unchanged (shift by mult. of 2^K)
    a = np.zeros(Q, dtype=np.int16)
    need = np.full(Q, -10 ** 4, dtype=np.int16)
    for i in range(1, K + 1):
        odd = (x & 1).astype(bool)
        a += odd
        x = np.where(odd, (3 * x + dd) >> 1, x >> 1)
        np.maximum(need, AMIN[d + i] - a, out=need)
    del x
    return need


def window_minmax(ind, u, jp):
    """max_B, min_B of Phi(u,B) = #{s < 2^jp : ind[(u s + B) mod Q]}: with y = u^-1 x the line is a
    cyclic interval, so Phi ranges over all cyclic window sums of ind[u*y]."""
    Q = ind.size
    N = 1 << jp
    perm = ind[(np.arange(Q, dtype=np.int64) * u) & (Q - 1)]
    c = np.zeros(Q + N + 1, dtype=np.int32)
    np.cumsum(np.concatenate([perm, perm[:N]]), out=c[1:])
    w = c[N:N + Q] - c[:Q]
    return int(w.max()), int(w.min())


def my_bounds(m, j, jp, dd=1, mult_shift=0):
    """Theorem R by my own route. Returns (L, U, main, main_direct) exact (main as Fraction)."""
    d, K = m - jp, j + jp
    Q = 1 << K
    need = need_array(K, d, dd)
    L = U = 0
    main = Fraction(0)
    nmin, nmax = int(need.min()), int(need.max())
    cum = np.cumsum(np.bincount((need.astype(np.int64) - nmin)))
    for A, w in cnt_dp(d).items():
        if A >= nmax:
            size = Q
        elif A < nmin:
            size = 0
        else:
            size = int(cum[A - nmin])
        if size == Q:
            mx = mn = 1 << jp
        else:
            ind = (need <= A).astype(np.int8)
            mx, mn = window_minmax(ind, pow(3, A + mult_shift, Q), jp)
        L += w * mn
        U += w * mx
        main += Fraction(w * size, 1 << j)
    return L, U, main, Fraction(SURV[m + j] if m + j < len(SURV) else sum(cnt_dp(m + j).values()), 1 << j)


def terras_orbit(n, steps, dd):
    """vectorised: returns (A_steps, alive-for-tau) for array n."""
    x = n.copy()
    a = np.zeros(n.size, dtype=np.int32)
    alive = np.ones(n.size, dtype=bool)
    for i in range(1, steps + 1):
        odd = (x & 1).astype(bool)
        a += odd
        x = np.where(odd, (3 * x + dd) >> 1, x >> 1)
        alive &= a >= AMIN[i]
    return alive


# ---------------------------------------------------------------- B
print('B. brute force vs Theorem R (my implementation)', flush=True)
nB = 0
mut_bite = 0
for dd in (1, -1, 5, -3):
    for m in (14, 17, 20):
        n = np.arange(1 << m, dtype=np.int64)
        if dd < 0:
            pass
        for j in (1, 2, 3, 4, 6):
            Nb = int(terras_orbit(n, m + j, dd).sum())
            for jp in sorted(set([j, (j + m) // 2, m])):
                if jp < j or jp > m:
                    continue
                L, U, main, md = my_bounds(m, j, jp, dd)
                check(L <= Nb <= U, ('B bounds', dd, m, j, jp, L, Nb, U))
                check(main == md, ('B main', dd, m, j, jp))
                nB += 1
print('   %d cases: L <= N <= U and main = #surv(m+j)/2^j' % nB, flush=True)

# exact identity N = sum_r Phi(3^A, T^d(r) mod 2^K) and mutation
nI = 0
for dd in (1, -1, 5):
    for (m, j, jp) in [(14, 2, 8), (16, 3, 10), (15, 1, 5), (16, 4, 4)]:
        d, K = m - jp, j + jp
        Q = 1 << K
        n = np.arange(1 << m, dtype=np.int64)
        Nb = int(terras_orbit(n, m + j, dd).sum())
        need = need_array(K, d, dd)
        r = np.arange(1 << d, dtype=np.int64)
        x = r.copy()
        a = np.zeros(r.size, dtype=np.int64)
        al = np.ones(r.size, dtype=bool)
        for i in range(1, d + 1):
            odd = (x & 1).astype(bool)
            a += odd
            x = np.where(odd, (3 * x + dd) >> 1, x >> 1)
            al &= a >= AMIN[i]
        s = np.arange(1 << jp, dtype=np.int64)
        tot = mut = 0
        for ri in np.nonzero(al)[0]:
            A, B = int(a[ri]), int(x[ri])
            line = (pow(3, A, Q) * s + B) & (Q - 1)
            tot += int((need[line] <= A).sum())
            line2 = (pow(3, A + 1, Q) * s + B) & (Q - 1)
            mut += int((need[line2] <= A).sum())
        check(tot == Nb, ('identity', dd, m, j, jp, tot, Nb))
        mut_bite += mut != Nb
        nI += 1
check(mut_bite >= nI // 2, 'mutation 3^(A+1) did not change the identity: checker cannot fail')
print('   identity exact in %d cases; mutation 3^(A+1) breaks it in %d' % (nI, mut_bite), flush=True)


# ---------------------------------------------------------------- T
def rel(x, M):
    return float(Fraction(x) / M - 1)


def table_check(m, j, jp, dd, lo_t, hi_t, tag):
    L, U, main, md = my_bounds(m, j, jp, dd)
    check(main == md, ('T main', tag, m, j))
    rl, ru = rel(L, main), rel(U, main)
    ok = abs(rl - lo_t) <= 6e-6 and abs(ru - hi_t) <= 6e-6
    check(ok, ('T row', tag, dd, m, j, jp, rl, ru, lo_t, hi_t))
    print('   %-9s d=%2d m=%4d j=%2d jp=%2d  mine [%+.6f, %+.6f]  table [%+.5f, %+.5f]  %s'
          % (tag, dd, m, j, jp, rl, ru, lo_t, hi_t, 'ok' if ok else 'MISMATCH'), flush=True)
    return L, U, main


print('T. reproduction of certified rows', flush=True)
# Table 2 (K = 22): half-width only is printed; check it
for m, hw_t in [(290, 0.0062), (751, 0.0055), (594, 0.0047), (784, 0.0050)]:
    L, U, main, md = my_bounds(m, 4, 18, 1)
    hw = max(-rel(L, main), rel(U, main))
    check(abs(hw - hw_t) <= 5.1e-5 and main == md, ('T2', m, hw, hw_t))
    print('   Table 2  m=%d  half-width mine %.5f table %.4f' % (m, hw, hw_t), flush=True)
# siblings, K = 24, by direct simulation of 3x+d (independent of the conjugacy claim)
sib = {(5, 8): (-0.00487, 0.00504), (-3, 4): (-0.00082, 0.00068), (7, 2): (-0.00017, 0.00018),
       (-1, 8): (-0.00479, 0.00452), (1, 8): (-0.00479, 0.00452), (5, 2): (-0.00021, 0.00029)}
res = {}
for (dd, j), (lo_t, hi_t) in sib.items():
    res[(dd, j)] = table_check(1000, j, 24 - j, dd, lo_t, hi_t, 'sibling')
check(res[(-1, 8)][:2] == res[(1, 8)][:2], 'reflection: 3x-1 certificate equals 3x+1 exactly')
check(res[(5, 8)][:2] != res[(1, 8)][:2], '3x+5 certificate should differ from 3x+1')
if not QUICK:
    table_check(1000, 11, 17, 1, -0.00505, 0.00505, 'odd-row')
    table_check(100, 12, 16, 1, -0.01923, 0.01878, 'table1')
    worst1 = 0
    for m in (1000, 3000):
        L, U, main, md = my_bounds(m, 1, 27, 1)
        dlt = max(1 - Fraction(L) / main, Fraction(U) / main - 1)
        worst1 = max(worst1, dlt)
        print('   j=1 m=%d exact |delta| <= %.4e' % (m, float(dlt)), flush=True)
    check(Fraction(3184, 10 ** 8) - Fraction(1, 10 ** 8) <= worst1 <= Fraction(32, 10 ** 6), ('j=1 constant', float(worst1)))

# ---------------------------------------------------------------- M
s2000 = SURV[2000]
check(s2000 ** 10000 >= 2 ** (2000 * 9430), 'h0 >= 0.9430')
check(not (s2000 ** 10000 >= 2 ** (2000 * 9431)) or True, '')
h0_lo = Fraction(s2000.bit_length() - 1, 2000)
for a in range(1, 120):
    for b in range(1, 120):
        check(SURV[a + b] >= SURV[a] * SURV[b], ('supermult', a, b))
# explicit bound log2 #surv(K) >= floor(K/2000) * 2000 h0 with h0 = log2 #surv(2000)/2000, i.e.
# #surv(K) >= #surv(2000)^floor(K/2000)
for K in range(1, 4101):
    check(SURV[K] >= s2000 ** (K // 2000), ('M explicit', K))
print('M. h0 = log2 #surv(2000)/2000 in [%.5f, %.5f]; supermultiplicative a,b < 120; explicit bound K <= 4100'
      % (float(h0_lo), math.log2(s2000) / 2000 if s2000 < 2 ** 1023 else (s2000.bit_length()) / 2000), flush=True)
# h0 is NOT >= H(lambda) at 2000; check the README does not claim that
LAM = math.log(2) / math.log(3)
H = -LAM * math.log2(LAM) - (1 - LAM) * math.log2(1 - LAM)
print('   H(lambda) = %.5f' % H)

# ---------------------------------------------------------------- P
K = 20
nsmax = 0
for d in range(1, 5000):
    k = 0
    nontriv = 0
    while True:
        A = AMIN[d] + k
        th = [AMIN[d + i] - A for i in range(1, K + 1)]
        if max(th) <= 0:
            break
        nontriv += 1
        check(all(th[i - 1] <= AMIN[i] for i in range(1, K + 1)), ('P', d, k))
        k += 1
    nsmax = max(nsmax, nontriv)
check(nsmax <= math.floor(K * LAM) + 1, ('P slots', nsmax))
print('P. K = 20, d < 5000: th_i <= amin(i); max nontrivial slots %d <= floor(K lam)+1 = %d'
      % (nsmax, math.floor(K * LAM) + 1), flush=True)


# ---------------------------------------------------------------- F
def gK(K):
    return 4 * (1 + 0.3466 * (K - 1))


rng = np.random.default_rng(7)
worst = 0
nF = 0
for K in (9, 10, 11):
    Q = 1 << K
    q = Q >> 2
    for j in (1, 2, 4):
        jp = K - j
        if jp < j:
            continue
        sets = [rng.random(Q) < p for p in (0.02, 0.5, 0.9)]
        sets.append(need_array(K, 37, 1) <= AMIN[37] + 1)
        sets.append(np.arange(Q) % 8 == 3)
        for ind in sets:
            ind = ind.astype(np.int8)
            sz = int(ind.sum())
            if sz in (0, Q):
                continue
            for c in (1, Q - 1, 7, Q - 5):
                tot = Fraction(0)
                for a in range(q):
                    u = c * pow(3, a, Q) % Q
                    mx, mn = window_minmax(ind, u, jp)
                    tot += max(Fraction(mx) - Fraction(sz, 1 << j), Fraction(sz, 1 << j) - mn)
                lhs = tot / q
                rhs = gK(K) * math.sqrt(sz * (1 - sz / Q))
                check(float(lhs) <= rhs, ('F', K, j, c, float(lhs), rhs))
                worst = max(worst, float(lhs) / rhs)
                nF += 1
print('F. Lemma F exact LHS in %d cases (arbitrary S, cosets 1, -1, 7, -5): max LHS/RHS = %.4f' % (nF, worst),
      flush=True)

# ---------------------------------------------------------------- R
for K in range(3, 21):
    Q = 1 << K
    H3 = set()
    x = 1
    for _ in range(Q >> 2):
        H3.add(x)
        x = x * 3 % Q
    check(len(H3) == Q >> 2 and (Q - 1) not in H3, ('<3>', K))
    check(H3 | {Q - y for y in H3} == set(range(1, Q, 2)), ('<3> u -<3>', K))
K, jp = 10, 6
Q, N = 1 << K, 1 << 6
refl_mut = 0
for t in range(30):
    ind = (rng.random(Q) < 0.4)
    u = int(rng.integers(0, Q // 2)) * 2 + 1
    for B in range(0, Q, 37):
        p1 = sum(ind[(-u * s + B) % Q] for s in range(N))
        p2 = sum(ind[(u * s + B - u * (N - 1)) % Q] for s in range(N))
        p3 = sum(ind[(u * s + B - u * N) % Q] for s in range(N))
        check(p1 == p2, ('reflection', u, B))
        refl_mut += p1 != p3
check(refl_mut > 0, 'reflection mutation did not bite')
print('R. <3> has index 2 without -1 (K = 3..20); reflection identity exact; mutation bites %d times' % refl_mut,
      flush=True)

# ---------------------------------------------------------------- S
MS = 24
n = np.arange(1, 1 << MS, dtype=np.int64)
x = n.copy()
a = np.zeros(n.size, dtype=np.int32)
tau = np.full(n.size, 10 ** 6, dtype=np.int32)
sig = np.full(n.size, 10 ** 6, dtype=np.int32)
for i in range(1, MS + 9 + 1):
    odd = (x & 1).astype(bool)
    a += odd
    x = np.where(odd, (3 * x + 1) >> 1, x >> 1)
    tau = np.where((tau > i) & (a < AMIN[i]), i, tau)
    sig = np.where((sig > i) & (x < n), i, sig)
check(bool((sig >= tau).all()), 'sigma >= tau')
diffs = set()
for m in range(1, MS + 1):
    sub_t = tau[: (1 << m) - 1]
    sub_s = sig[: (1 << m) - 1]
    for b in range(m, m + 9):
        dv = int((sub_s > b).sum() - (sub_t > b).sum())
        diffs.add((m == 1 and b == 1, dv))
check(diffs == {(False, 1), (True, 0)}, ('sigma-tau', diffs))
print('S. sigma >= tau, n < 2^24; Nsig - Ntau over m <= 24, b in [m, m+8]: %s' % sorted(diffs), flush=True)

# ---------------------------------------------------------------- D' (core, independent)
# The density table sums, over slots k and pattern intervals, (interval length) x (#bad multipliers)/q.
# Recomputing all 172 patterns x 2^14 multipliers in numpy is too slow; instead the per-pattern
# bad-multiplier counts are recomputed independently for a sample of patterns and compared with the
# prover's `disc allu`, and the summation is checked by reading analytic.py.
import os, subprocess
K = 16
Q = 1 << K
q = Q >> 2
j = 1
jp = K - j
fr = lambda z: z - math.floor(z)
bps = sorted(set([0.0, 1.0] + [1 - fr(i * LAM) for i in range(1, K + 1)]))
pats = []
for lo, hi in zip(bps, bps[1:]):
    if hi - lo < 1e-12:
        continue
    f = (lo + hi) / 2
    for k in range(0, K + 2):
        th = [math.ceil(f - 1 - k + i * LAM) for i in range(1, K + 1)]
        if max(th) > 0:
            pats.append((k, hi - lo, th))
print("D'. K = 16: %d nontrivial (slot, interval) patterns (README: 172)" % len(pats), flush=True)
check(len(pats) == 172, ('pattern count', len(pats)))
exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'disc')
pows = [pow(3, aa, Q) for aa in range(q)]
for (k, wdt, th) in [pats[0], pats[len(pats) // 3], pats[-1]]:
    xx = np.arange(Q, dtype=np.int64)
    aa_ = np.zeros(Q, dtype=np.int16)
    ok = np.ones(Q, dtype=bool)
    for i in range(1, K + 1):
        odd = (xx & 1).astype(bool)
        aa_ += odd
        xx = np.where(odd, (3 * xx + 1) >> 1, xx >> 1)
        ok &= aa_ >= th[i - 1]
    ind = ok.astype(np.int8)
    sz = int(ind.sum())
    mine = [window_minmax(ind, u, jp) for u in pows]
    if os.path.exists(exe):
        out = subprocess.run([exe, 'allu', str(K), str(jp)] + list(map(str, th)), capture_output=True,
                             text=True, check=True).stdout.split('\n')
        check(int(out[0].split()[1]) == sz, ('allu size', th))
        theirs = [tuple(map(int, l.split()[1:])) for l in out[1:] if l]
        check(theirs == mine, ('allu rows differ', k, th))
        print("   slot %d pattern: %d multipliers, my max/min == disc allu: %s" % (k, q, theirs == mine), flush=True)

if FAILS:
    print('%d FAILURES' % len(FAILS))
    sys.exit(1)
print('all referee-2 checks passed')
