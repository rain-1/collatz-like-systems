"""Checks for the analytic part (Lemma F, Lemma P, Lemma M, Theorem D) and the explicit density
numbers. Exits 0 only if every exact check passes.

  F. Lemma F (averaged uniform discrepancy): for u uniform on a coset c<3> of the units mod 2^K,
       E_u max_B |Phi(u,B) - Phi_bar| <= g_K sqrt(|S| (1 - |S|/2^K)),  g_K = 4 (1 + 0.3466 (K-1)),
     checked exactly (all u, all B) for survivor sets of many patterns, K = 8..14, cosets c = 1, 5^-1, -1.
     Also the pointwise Fourier bound max_B |Phi - Phi_bar| <= 2^-K sum_{xi != 0} |S^(xi)| |G(u xi)|
     (floating point, numpy; reported, tolerance 1e-6).
  P. Lemma P: every slot pattern th_i = ceil(phi + i lambda), phi < 0, satisfies th_i <= amin(i), hence
     |S| >= #surv(K); checked over all slot patterns for K <= 24.
  M. Lemma M: #surv(a + b) >= #surv(a) #surv(b) (a, b <= 80); certified exponent
     h0 = log2 #surv(K0) / K0 at K0 = 2000 (lower bound for lim (1/K) log2 #surv(K)).
  D. Theorem D constants: the explicit bound on the fraction of bad m, and the exact (Weyl) density
     bound at K = 16 computed from every multiplier and every slot pattern.
"""
import math
import os
import subprocess
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from microlib import HERE, amin, survivors

LAM = math.log(2) / math.log(3)
fails = 0


def check(cond, msg):
    global fails
    if not cond:
        fails += 1
        print('FAIL', msg)


def gK(K):
    return Fraction(4) * (1 + Fraction(3466, 10000) * (K - 1))


def allu(K, jp, th, coset=1):
    """exact (|S|, [(mx, mn)] for u = coset * 3^a, a = 0..2^(K-2)-1). coset != 1 is done by passing the
    thresholds unchanged and rescaling: Phi for multiplier c*3^a is computed by the job interface."""
    if coset == 1:
        out = subprocess.run(['nice', os.path.join(HERE, 'disc'), 'allu', str(K), str(jp)] + list(map(str, th)),
                             capture_output=True, text=True, check=True).stdout.split('\n')
        size = int(out[0].split()[1])
        rows = [tuple(map(int, l.split()[1:])) for l in out[1:] if l]
        return size, rows
    Q = 1 << K
    inp = ''.join('%d %d %d %s\n' % (K, jp, coset * pow(3, a, Q) % Q, ' '.join(map(str, th)))
                  for a in range(Q >> 2))
    out = subprocess.run(['nice', os.path.join(HERE, 'disc'), 'batch'], input=inp, capture_output=True,
                         text=True, check=True).stdout.split('\n')
    rows = [tuple(map(int, l.split())) for l in out if l]
    return rows[0][0], [(r[1], r[2]) for r in rows]


def slot_patterns(K):
    """all distinct nontrivial threshold patterns th_i = ceil(phi + i lam) (i = 1..K) for phi < 0,
    as (k, f-interval length, pattern): phi = f - 1 - k, f in (0, 1). Breakpoints f = 1 - {i lam}.
    Uses exact integer comparisons: ceil(phi + i lam) is computed as amin(d + i) - A for a real
    depth d with {d lam} in the interval, so no floating point decides a threshold."""
    bps = sorted(set([0.0, 1.0] + [1 - (i * LAM - math.floor(i * LAM)) for i in range(1, K + 1)]))
    res = []
    for lo, hi in zip(bps, bps[1:]):
        if hi - lo < 1e-12:
            continue
        fm = (lo + hi) / 2
        # find an integer depth d with {d lam} close to fm (only the pattern matters, and the pattern is
        # constant on the open interval, so any d with {d lam} strictly inside works); verify exactly below
        d = next(d for d in range(1, 10 ** 6) if lo + 1e-9 < d * LAM - math.floor(d * LAM) < hi - 1e-9)
        for k in range(0, K + 2):
            A = amin(d) + k
            th = [amin(d + i) - A for i in range(1, K + 1)]
            if max(th) <= 0:
                continue
            res.append((k, hi - lo, tuple(th), d))
    return res


# ---------------- Lemma P
for K in range(2, 25):
    for k, w, th, d in slot_patterns(K):
        check(all(th[i - 1] <= amin(i) for i in range(1, K + 1)), ('P', K, k, th))
print('P. all slot patterns have th_i <= amin(i), K <= 24  =>  |S| >= #surv(K)')

# ---------------- Lemma M
s = [survivors(i) for i in range(0, 161)]
for a in range(1, 81):
    for b in range(1, 81):
        check(s[a + b] >= s[a] * s[b], ('M', a, b))
K0 = 2000
sK0 = survivors(K0)
h0 = Fraction(sK0.bit_length() - 1, K0)          # log2 #surv(K0) >= bit_length - 1
print('M. #surv supermultiplicative (a, b <= 80); h0 = log2 #surv(%d)/%d >= %.5f' % (K0, K0, float(h0)))

# ---------------- Lemma F (exact)
worst = 0.0
nF = 0
for K in range(8, 15):
    pats = slot_patterns(K)
    sel = pats[:: max(1, len(pats) // 6)]
    for j in (1, 2, 3):
        jp = K - j
        if jp < j:
            continue
        for k, w, th, d in sel:
            for coset in (1, pow(5, -1, 1 << K), (1 << K) - 1):
                size, rows = allu(K, jp, list(th), coset)
                Q = 1 << K
                # D(u) = max(mx - size/2^j, size/2^j - mn); mean over u
                tot = sum(max(Fraction(mx) - Fraction(size, 1 << j), Fraction(size, 1 << j) - mn) for mx, mn in rows)
                mean = tot / len(rows)
                rhs2 = gK(K) ** 2 * Fraction(size) * (Q - size) / Q
                check(mean * mean <= rhs2, ('F', K, j, th, coset, float(mean), float(rhs2) ** 0.5))
                worst = max(worst, float(mean) / float(rhs2) ** 0.5 if rhs2 else 0)
                nF += 1
print('F. Lemma F holds exactly in %d cases (K = 8..14, j = 1..3, three cosets); max ratio LHS/RHS = %.4f'
      % (nF, worst))

# pointwise Fourier bound (floating point, EVIDENCE-level sanity of the derivation)
try:
    import numpy as np
    K, j = 12, 2
    jp = K - j
    Q = 1 << K
    k, w, th, d = slot_patterns(K)[3]
    size, rows = allu(K, jp, list(th))
    # rebuild S by direct simulation
    Sx = np.zeros(Q)
    for x0 in range(Q):
        x, a, okk = x0, 0, True
        for i in range(1, K + 1):
            if x & 1:
                x = (3 * x + 1) // 2
                a += 1
            else:
                x //= 2
            if a < th[i - 1]:
                okk = False
                break
        Sx[x0] = okk
    Sh = np.abs(np.fft.fft(Sx))
    xi = np.arange(Q)
    viol = 0
    for a in range(0, Q >> 2, 7):
        u = pow(3, a, Q)
        eta = (u * xi) % Q
        th_ = eta / Q
        with np.errstate(divide='ignore', invalid='ignore'):
            Gm = np.abs(np.sin(np.pi * (1 << jp) * th_) / np.sin(np.pi * th_))
        Gm[0] = 1 << jp
        bound = (Sh[1:] * Gm[1:]).sum() / Q
        mx, mn = rows[a]
        Dv = max(mx - size / 2 ** j, size / 2 ** j - mn)
        if Dv > bound + 1e-6:
            viol += 1
    print('F\'. pointwise Fourier bound (floats, K = 12): %d violations (expected 0)' % viol)
    check(viol == 0, 'Fourier pointwise')
except ImportError:
    print("F'. numpy not available; pointwise Fourier check skipped (run with the round4 venv python)")

# ---------------- Theorem D: explicit fraction bound
print('D. explicit bound on the fraction of bad m in [M, 2M) (Theorem D, q = 2^(K-2) <= M):')
print('   frac <= 2 n_s (lam + 3) (K + 1) g_K 2^j / (eps sqrt(#surv(K))),  n_s = floor(K lam) + 1')
for j in (1, 4, 10):
    for eps in (Fraction(1, 10), Fraction(1, 100)):
        Kmin = None
        for K in range(max(2 * j, 3), 400):
            ns = math.floor(K * LAM) + 1
            num = 2 * ns * (LAM + 3) * (K + 1) * float(gK(K)) * 2 ** j
            val = num / (float(eps) * math.sqrt(float(survivors(K))))
            if val < 0.1:
                Kmin = K
                break
        print('   j = %2d, eps = %.2f: bound < 0.1 from K = %s, i.e. for M >= 2^%s'
              % (j, float(eps), Kmin, Kmin - 2 if Kmin else None))

# ---------------- exact density at K = 16 (Weyl version)
K = 16
q = 1 << (K - 2)
pats = slot_patterns(K)
print('D\'. exact density bound at K = 16 from all %d slot patterns x %d multipliers' % (len(pats), q))
for j in (1, 2, 4):
    jp = K - j
    data = []
    for k, w, th, d in pats:
        size, rows = allu(K, jp, list(th))
        data.append((w, size, rows))
    for eps in (Fraction(1, 100), Fraction(2, 100), Fraction(5, 100), Fraction(1, 10)):
        dens = 0.0
        for w, size, rows in data:
            nb = sum(1 for mx, mn in rows if max(mx * (1 << j) - size, size - mn * (1 << j)) > eps * size)
            dens += w * nb / q
        print('   j = %d, eps = %.2f: upper density of {m : |N/2^mP - 1| > eps} <= %.4f' % (j, float(eps), dens))

if fails:
    print('%d FAILURES' % fails)
    sys.exit(1)
print('all checks passed')
