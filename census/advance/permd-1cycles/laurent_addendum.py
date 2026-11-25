"""Re-derive the perm_d cutoff from Laurent (2008), Acta Arith. 133, Corollary 2.

Statement used (read in the primary source by the constants-audit cohort and its
referee; see ../constants-audit/theorem.md): for alpha1, alpha2 multiplicatively
independent with alpha_i and log alpha_i real and positive, b1, b2 positive
integers, Lambda = b2 log alpha2 - b1 log alpha1, D = 1 here,
  log|Lambda| >= -C2 * max(log b' + 0.38, m, 1)^2 * log A1 * log A2
with (m, C2) from Table 1, log A_i >= max(h(alpha_i), |log alpha_i|, 1),
b' = b1/log A2 + b2/log A1.

Application (theorem.md Steps 3-4): alpha1 = 2, b1 = 3l+k, log A1 = 1;
alpha2 = 5, b2 = k+l, log A2 = log 5; so b' = (3l+k)/log 5 + (k+l) and
Step 3 gives b' < 7.204826 k + 6.093580 together with |Lambda| < 2^(1-k).
A solution needs (k-1) log 2 < C2 log 5 max(log b' + 0.38, m)^2.
G(k) := (k-1) log 2 - C2 log 5 max(log(7.204826k+6.093580)+0.38, m)^2.
G' >= log 2 - 2 C2 log 5 (log(..)+0.38)/k, which increases with k once the
argument exceeds e^0.62, so G(k0) > 0 and G'(k0) > 0 give G > 0 on [k0, inf).
The exact scan in check.py covers every k <= 24924; this script asserts k0 <= 24925.
"""
from decimal import Decimal as Dm, getcontext
getcontext().prec = 60
L2, L5 = Dm(2).ln(), Dm(5).ln()
TABLE = [(10, '25.2'), (12, '23.4'), (14, '22.1'), (16, '21.1'), (18, '20.3'), (20, '19.7'),
         (22, '19.2'), (24, '18.8'), (26, '18.4'), (28, '18.1'), (30, '17.9')]
best = None
for m, c in TABLE:
    C2 = Dm(c)
    def u(k): return max((Dm('7.204826') * k + Dm('6.093580')).ln() + Dm('0.38'), Dm(m))
    def G(k): return (k - 1) * L2 - C2 * L5 * u(k) ** 2
    def dG(k): return L2 - 2 * C2 * L5 * u(k) / k
    k = 2
    while not (G(k) > 0 and dG(k) > 0):
        k += 1
    if best is None or k < best[0]:
        best = (k, m, c)
    print(f"m={m:2d} C2={c}: G>0 and G'>0 from k0={k}")
k0, m, c = best
print(f"best cutoff: every solution has k < {k0} (m={m}, C2={c})")
assert k0 <= 24925, "existing exact scan (k <= 24924) would not cover the Laurent cutoff"
print("OK: the exact scan in check.py (k <= 24924) covers the Laurent 2008 cutoff")
