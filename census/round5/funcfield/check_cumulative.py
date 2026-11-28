"""Proposition H' (cumulative count inside the horizon), checked exactly on all data.

For a system with e = e_max, D_0 as in theory sec. 1, D_1 = max(D_0, 2e - 2), X = q^{D+1},
B = max(D_0, b + e - 1) and 0 <= b <= D + 2 - e, Proposition H' says

    0 <= N(X, b) - (X - q^B) P(b) <= Gamma (q - 1) q^{b + 2e - 2} P(b) + q^{D_1},

where Gamma = sum_{j >= 0} 1/(q^j P(j)).  Here Gamma is bounded from above by the exact sum for
j <= J plus the tail of the proved block bound G(j) = q^j P(j) >= c rho^j (theory sec. 1):
  step law of A3 (A3, B3, G3):  G(j) >= 2^{j/2} / 3
  step law of Q4b (Q4b, Q4):    G(j) >= 9^{j/3} / 16
  step law of S2c (S2c, S2):    G(j) >= c(n) 2^{j - n} for every n >= j, c(n) = number of
                                compositions of n into parts 3 and 4.
The script checks (1) the block bounds against the exact P(j) for j <= 400 (they are proofs,
this only guards against a wrong formula), (2) the supermultiplicativity
P(b) >= P(m + e - 1) P(b - m), 0 <= m <= b <= 200, exactly, (3) the two-sided inequality on
every (D, b) cell of the exhaustive data with D >= D_0 and b <= D + 2 - e.
Octave D' = 0 (the q - 1 nonzero constants) is not in the data files and is added by brute
force.  Exits 1 on any failure.
"""
import sys
from fractions import Fraction
from ffmap import load_spec, survivors_exact, step_law, sigma, deg
from analyse import load

fail = []
CAP = 400


def D0_of(S):
    q, brs = S
    out = 0
    for (r, g, c) in brs:
        e = len(r)
        s = deg(g) - e
        dc = deg(c) if c else -10**9
        out = max(out, e, dc - s + 1)
    return out


def comp34(nmax):
    c = [0] * (nmax + 1)
    c[0] = 1
    for n in range(1, nmax + 1):
        c[n] = (c[n - 3] if n >= 3 else 0) + (c[n - 4] if n >= 4 else 0)
    return c


C34 = comp34(CAP + 10)
LAWS = {}
for name in ['A3', 'B3', 'G3', 'S2', 'S2c', 'Q4', 'Q4b']:
    S = load_spec(f'specs/{name}.txt')
    LAWS[name] = sorted(step_law(S))
family = {'A3': 'A3', 'B3': 'A3', 'G3': 'A3', 'S2': 'S2c', 'S2c': 'S2c', 'Q4': 'Q4b', 'Q4b': 'Q4b'}
for n, f in family.items():
    if LAWS[n] != LAWS[f]:
        fail.append(('step law differs', n, f))


def block_bound(fam, j):
    """Proved lower bound for G(j) = q^j P(j), as an exact Fraction."""
    if fam == 'A3':
        m = -(-j // 2)
        return Fraction(3 ** j * 2 ** m, 9 ** m)
    if fam == 'Q4b':
        m = -(-j // 3)
        return Fraction(4 ** j * 9 ** m, 64 ** m)
    if fam == 'S2c':
        return max(Fraction(C34[n] * 2 ** j, 2 ** n) for n in range(j, j + 4))


# For S2c: c(n) >= alpha x^n on a window of 4 values implies it for all larger n.  We only need
# sum 1/G(j) over j > J; use G(j) >= max_n c(n)/8 and the exact recurrence for n <= J + 200,
# and beyond that the geometric bound with ratio x^{-1}, x = 1.2207 (x^4 = x + 1).
def gamma_upper(fam, P, q):
    J = 300
    tot = Fraction(0)
    for j in range(J + 1):
        G = q ** j * P[j]
        if G < block_bound(fam, j):
            fail.append(('block bound violated', fam, j))
        tot += 1 / G
    # tail j > J from the block bounds, in floats with a safety factor 2
    if fam == 'A3':
        tail = 3 * 2 ** (-(J + 1) / 2) / (1 - 2 ** -0.5)
    elif fam == 'Q4b':
        tail = 16 * 9 ** (-(J + 1) / 3) / (1 - 9 ** (-1 / 3))
    else:
        x = 1.2207440846057596  # real root of x^4 = x + 1, x > 1
        # window check: c(n) >= alpha x^n for n = J..J+3 implies for all n >= J
        alpha = min(C34[n] / x ** n for n in range(J, J + 4))
        if any(C34[n] < alpha * x ** n * (1 - 1e-12) for n in range(J, CAP + 10)):
            fail.append(('composition window', alpha))
        tail = 8 * x ** (-(J + 1)) / alpha / (1 - 1 / x)
    return (float(tot) + 2 * tail) * (1 + 1e-9)


report = []
for name in ['A3', 'B3', 'G3', 'S2', 'S2c', 'Q4', 'Q4b']:
    S = load_spec(f'specs/{name}.txt')
    q = S[0]
    law = step_law(S)
    e = max(x for _, _, x in law)
    D0 = D0_of(S)
    D1 = max(D0, 2 * e - 2)
    P = survivors_exact(S, CAP)
    fam = family[name]
    Gam = gamma_upper(fam, P, q)
    # supermultiplicativity
    for b in range(0, 201):
        for m in range(0, b + 1):
            if m + e - 1 <= CAP and P[b] < P[m + e - 1] * P[b - m]:
                fail.append(('supermult', name, b, m))
    N, cap = load(name)
    Ds = sorted({D for D, b in N})
    # octave 0 by brute force
    N0 = {}
    for b in range(0, 60):
        N0[b] = sum(1 for a in range(1, q) if sigma(S, (a,), b) > b)
    worst_rel = 0.0
    cells = 0
    for D in Ds:
        if D < D0:
            continue
        X = q ** (D + 1)
        for b in range(0, D + 3 - e):
            B = max(D0, b + e - 1)
            tot = N0.get(b, q - 1) + sum(N[(Dp, b)] for Dp in Ds if Dp <= D)
            if any((Dp, b) not in N for Dp in Ds if Dp <= D):
                fail.append(('missing cell', name, D, b))
                continue
            diff = tot - (X - q ** B) * P[b]
            upper = Fraction(Gam).limit_denominator(10**12) * (q - 1) * q ** (b + 2 * e - 2) * P[b] + q ** D1
            if diff < 0 or diff > upper:
                fail.append(('H-prime', name, D, b, float(diff), float(upper)))
            cells += 1
            rel = float(abs(tot - X * P[b]) / (X * P[b]))
            if b <= D - 4:
                worst_rel = max(worst_rel, rel * q ** (D - b))
    report.append((name, D0, Gam, cells, worst_rel))
    print(f'{name}: D_0 = {D0}, e_max = {e}, Gamma <= {Gam:.4f}; {cells} cells checked; '
          f'max over b <= D-4 of |N/(XP) - 1| * q^(D-b) = {worst_rel:.3f}')
if fail:
    print('FAIL', fail[:20])
    sys.exit(1)
print("Proposition H' check passed")
