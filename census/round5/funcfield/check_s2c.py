"""Theorem A'' (S2c, all K > 1), finite and numerical parts, checked exactly or to 50 digits.

Checks:
 1. lambda* > 1 solves 2 lambda = (lambda^2 - 1)^2, rho* = (lambda*^2 - 1)/2; then
    F(lambda, rho) = (1/2)/(lambda rho) + (lambda + 1/lambda)/(4 rho^2) = 1 and dF/dlambda = 0
    (50-digit Decimal).  h = 1 + log2 rho* is printed (referee: 0.87585).
 2. The tilted law pi = (pi_0, pi_10, pi_11) sums to 1, has mean slope 0, and
    H(pi) = E_pi[e] (1 + log2 rho*) (the identity used in the proof), theta* = 2 pi_11.
 3. P(b) <= rho*^(b-1) exactly-in-Decimal for 1 <= b <= 400 (optional stopping bound).
 4. Z_L = sum_{3a + beta = L, 0 <= beta <= a} C(2a, a) C(a, beta) equals the brute-force number
    of zero-slope branch words of digit length L, L <= 16.
 5. The elementary binomial bound (n + 1) C(n, k) >= n^n / (k^k (n-k)^(n-k)), n <= 300, exact.
 6. For L = 2^k, 8 <= k <= 22: the beta chosen in the proof (nearest admissible integer to
    beta* = theta* L/(3 + theta*), beta = L mod 3) has theta = beta/a in [0.3, 0.4], and
    log2(C(2a,a) C(a,beta)) >= h L - 4 - log2((2a+1)(a+1)).
 7. sup |g'| <= 2 on theta in [0.3, 0.4] (the Lipschitz constant used in the proof), on a fine grid
    plus monotonicity of the two terms.
 8. Numerical illustration only (not a theorem): at L = 2048 the smallest K with
    Z_L/L - 1 > X rho*^(K log2 X - 1), X = 2^(L+3).
Exits 1 on any failure.
"""
import sys, math, itertools
from decimal import Decimal as Dm, getcontext
from fractions import Fraction
from math import comb
from ffmap import load_spec, survivors_exact

getcontext().prec = 60
fail = []

# 1. saddle point
lo, hi = Dm(1), Dm(3)
for _ in range(250):
    mid = (lo + hi) / 2
    if (mid * mid - 1) ** 2 - 2 * mid < 0:
        lo = mid
    else:
        hi = mid
lam = lo
rho = (lam * lam - 1) / 2
F = Dm(1) / (2 * lam * rho) + (lam + 1 / lam) / (4 * rho * rho)
dF = -Dm(1) / (2 * lam * lam * rho) + (1 - 1 / (lam * lam)) / (4 * rho * rho)
if abs(F - 1) > Dm('1e-45') or abs(dF) > Dm('1e-45') or not lam > 1:
    fail.append(('saddle', F, dF))
ln2 = Dm(2).ln()
h = 1 + rho.ln() / ln2
print(f'lambda* = {float(lam):.6f}, rho* = {float(rho):.6f}, h = 1 + log2 rho* = {float(h):.6f}, '
      f'C* = 1/(1-h) = {float(1 / (1 - h)):.4f}')
if abs(float(h) - 0.87585) > 5e-5:
    fail.append(('h value', h))

# 2. tilt identity
p0 = Dm(1) / (2 * lam * rho)
p10 = lam / (4 * rho * rho)
p11 = 1 / (4 * lam * rho * rho)
Ee = p0 + 2 * p10 + 2 * p11
Es = -p0 + p10 - p11
H = -(p0 * p0.ln() + p10 * p10.ln() + p11 * p11.ln()) / ln2
if abs(p0 + p10 + p11 - 1) > Dm('1e-45') or abs(Es) > Dm('1e-45') or abs(H - Ee * h) > Dm('1e-40'):
    fail.append(('tilt', p0 + p10 + p11, Es, H - Ee * h))
theta = 2 * p11
if abs(p10 - Dm('0.5')) > Dm('1e-45'):
    fail.append(('pi_10 != 1/2', p10))


def Hb(x):
    return 0.0 if x in (0, 1) else -(x * math.log2(x) + (1 - x) * math.log2(1 - x))


phi = (2 + Hb(float(theta))) / (3 + float(theta))
print(f'theta* = {float(theta):.6f}, phi(theta*) = {phi:.8f}')
if abs(phi - float(h)) > 1e-12:
    fail.append(('phi(theta*) != h', phi))

# 3. P(b) <= rho^(b-1)
S = load_spec('specs/S2c.txt')
P = survivors_exact(S, 400)
worst = Dm(0)
for b in range(1, 401):
    pb = Dm(P[b].numerator) / Dm(P[b].denominator)
    r = pb / rho ** (b - 1)
    worst = max(worst, r)
    if r > 1:
        fail.append(('P(b) > rho^(b-1)', b, r))
print(f'max_b<=400 P(b)/rho*^(b-1) = {float(worst):.5f} (must be <= 1)')

# 4. Z_L vs brute force
BR = [((0,), -1), ((1, 0), +1), ((1, 1), -1)]


def Z(L):
    return sum(comb(2 * a, a) * comb(a, L - 3 * a) for a in range(0, L // 3 + 1) if 0 <= L - 3 * a <= a)


def Z_brute(L):
    # count words (sequences of branches) of digit length exactly L and total slope 0
    from functools import lru_cache

    @lru_cache(None)
    def cnt(rem, s):
        if rem == 0:
            return 1 if s == 0 else 0
        return sum(cnt(rem - len(r), s + sl) for r, sl in BR if len(r) <= rem)
    return cnt(L, 0)


for L in range(1, 17):
    if Z(L) != Z_brute(L):
        fail.append(('Z_L', L, Z(L), Z_brute(L)))

# 5. binomial bound, exact integers
for n in range(1, 301):
    for k in range(0, n + 1):
        lhs = (n + 1) * comb(n, k) * (k ** k) * ((n - k) ** (n - k))
        if lhs < n ** n:
            fail.append(('binomial bound', n, k))

# 6. chosen beta for L = 2^k
th = float(theta)
hf = float(h)
for k in range(8, 23):
    L = 2 ** k
    bstar = th * L / (3 + th)
    cands = [bb for bb in range(int(bstar) - 3, int(bstar) + 4) if bb % 3 == L % 3]
    beta = min(cands, key=lambda bb: abs(bb - bstar))
    if abs(beta - bstar) > 1.5:
        fail.append(('beta distance', L))
    a = (L - beta) // 3
    if 3 * a + beta != L or not (0.3 <= beta / a <= 0.4):
        fail.append(('theta range', L, beta / a))
    # also the whole segment between beta and bstar stays in [0.3, 0.4]
    for bb in (bstar - 2, bstar + 2):
        aa = (L - bb) / 3
        if not (0.3 <= bb / aa <= 0.4):
            fail.append(('segment theta', L))
    val = (math.lgamma(2 * a + 1) - 2 * math.lgamma(a + 1) + math.lgamma(a + 1) - math.lgamma(beta + 1)
           - math.lgamma(a - beta + 1)) / math.log(2)
    bound = hf * L - 4 - math.log2((2 * a + 1) * (a + 1))
    if val < bound:
        fail.append(('rate bound', L, val, bound))
    if k in (8, 11, 16, 22):
        print(f'L = 2^{k}: log2(max term)/L = {val / L:.6f}, proved lower bound / L = {bound / L:.6f}, h = {hf:.6f}')

# 7. Lipschitz constant of g(beta) = 2a + a H(beta/a), a = (L - beta)/3:
#    g'(beta) = -(2 - log2(1 - theta))/3 + log2((1 - theta)/theta)
for i in range(0, 100001):
    t = 0.3 + 0.1 * i / 100000
    gp = -(2 - math.log2(1 - t)) / 3 + math.log2((1 - t) / t)
    if abs(gp) > 2:
        fail.append(('lipschitz', t, gp))
        break
# g' is decreasing in theta (both log terms decrease), so its range on [0.3, 0.4] is [g'(0.4), g'(0.3)]
g03 = -(2 - math.log2(0.7)) / 3 + math.log2(0.7 / 0.3)
g04 = -(2 - math.log2(0.6)) / 3 + math.log2(0.6 / 0.4)
print(f"g'(0.3) = {g03:.4f}, g'(0.4) = {g04:.4f} (|g'| <= 2 required)")

# 8. single-X illustration
L = 2048
ZL = Z(L)
lhs = math.log2(ZL // L - 1)
X2 = L + 3
# need lhs > X2 + (K X2 - 1) log2 rho
lr = math.log2(float(rho))
Kthr = ((lhs - X2) / lr + 1) / X2
print(f'L = 2048: Z_L/L - 1 > X P(K log2 X) is guaranteed by the proved bounds once K > {Kthr:.4f} '
      f'(a statement about this one X only)')

if fail:
    print('FAIL', fail[:10])
    sys.exit(1)
print('S2c check passed')
