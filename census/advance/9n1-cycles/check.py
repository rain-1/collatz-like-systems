"""Exact certificate for census/advance/9n1-cycles/theorem.md.

Theorem: every positive cycle of the 9n+1 map (n even -> n/2, n odd -> 9n+1)
has at least R+1 = 14 rising runs (strict local minima of the shortcut map
S(n) = (9n+1)/2 for odd n, n/2 for even n).  Equivalently, at least 14 of
its odd terms are = 3 (mod 4).  In particular there is no circuit.

Usage: python3 check.py [R]      (default R = 13; exit 0 iff all checks pass)
All arithmetic is with Python integers / Fractions; logarithms are enclosed
by the atanh series with an explicit tail bound.
"""
import sys
import time
from fractions import Fraction as F
from math import gcd
from multiprocessing import Pool, cpu_count

R = int(sys.argv[1]) if len(sys.argv) > 1 else 13


def atanh_bounds(d, terms=120):
    """Enclose log((d+1)/(d-1)) = 2 atanh(1/d), d >= 2."""
    z = F(1, d)
    lo = sum(2 * z**(2*j+1) / (2*j+1) for j in range(terms))
    tail = 2 * z**(2*terms+1) / ((2*terms+1) * (1 - z*z))
    return lo, lo + tail


# log 2 = 2atanh(1/3), log 3 = 2atanh(1/2), log(5/4) = 2atanh(1/9)
L2 = atanh_bounds(3)
L3 = atanh_bounds(2)
L54 = atanh_bounds(9)
L10_hi = 3 * L2[1] + L54[1]                       # log 10 = 3 log 2 + log(5/4)
ALO, AHI = 2 * L3[0] / L2[1], 2 * L3[1] / L2[0]   # alpha = log_2 9 in [ALO, AHI]
assert 3 < ALO < AHI < F(16, 5)
assert AHI - ALO < F(1, 10**60)


def continued_fraction(lo, hi):
    """Partial quotients shared by every real in [lo, hi] (hence true ones of alpha)."""
    out = []
    while True:
        a, b = lo.numerator // lo.denominator, hi.numerator // hi.denominator
        if a != b or lo == a:
            return out
        out.append(a)
        lo, hi = 1 / (hi - a), 1 / (lo - a)


def convergents(cf):
    p0, p1, q0, q1 = 1, cf[0], 0, 1
    res = [(p1, q1)]
    for a in cf[1:]:
        p0, p1, q0, q1 = p1, a*p1 + p0, q1, a*q1 + q0
        res.append((p1, q1))
    return res


CONV = convergents(continued_fraction(ALO, AHI))
assert CONV[:4] == [(3, 1), (16, 5), (19, 6), (149, 47)]
for (p, q), (p2, q2) in zip(CONV, CONV[1:]):
    assert p2*q - p*q2 in (1, -1)


def e_lower(n):
    """Rigorous lower bound for |q_n alpha - p_n| (sign must be certain)."""
    p, q = CONV[n]
    a, b = q*ALO - p, q*AHI - p
    assert a * b > 0, "enclosure too coarse"
    return min(abs(a), abs(b))


def index_for(kmax):
    """Least n with q_{n+1} > kmax; then |k alpha - K| >= |q_n alpha - p_n| for 0 < k <= kmax."""
    for n in range(len(CONV) - 1):
        if CONV[n+1][1] > kmax:
            return n
    raise AssertionError("need more partial quotients")


def log_upper(x):
    """log x <= log2 * bit_length(x) for integer x >= 1."""
    return L2[1] * x.bit_length()


# C_R >= sum_{i<R} alpha^i : odd steps k <= C_R * log_2(7m+1)
C_R = (AHI**R - 1) / (AHI - 1)

# ---- Step 1: Laurent (2008) Corollary 2, (m, C2) = (10, 25.2), gives k < K0 ----
K0 = 2 * 10**12
c_bp = 2 + L10_hi / (L2[0] * L3[0])        # b' = 2k + K/log3 <= c_bp * k   (K <= k log_2 10)
assert c_bp < F(503, 100)
Lt = log_upper(-(-K0 * c_bp.numerator // c_bp.denominator)) + F(38, 100)   # >= log(c_bp K0)+0.38
# For k >= K0: log(b')+0.38 <= Ltilde(k) := log(c_bp k)+0.38, and Ltilde(k) >= 28 log 2 + 0.38 >= 10,
# so max{log b'+0.38, 10, 1} <= Ltilde(k); also Ltilde > 2 gives f(k)/k decreasing on [K0, oo).
assert K0 >= 2**28 and 28 * L2[0] + F(38, 100) >= 10
f_K0 = C_R * (3 + ((F(R, 7) - 1 if R >= 7 else 0) + F(252, 10) * L3[1] * Lt * Lt) / L2[0])
assert f_K0 < K0, (float(f_K0), K0)
print(f"[LMN] R={R}: C_R < {float(C_R):.4g}; f(K0)={float(f_K0):.4g} < K0={K0}, so k < {K0}")

# ---- Step 2: continued-fraction reduction ----
kmax = K0
history = []
while True:
    n = index_for(kmax)
    e = e_lower(n)
    M = int(F(R) / (7 * L2[0] * e)) + 1          # every cycle minimum m satisfies m < M
    new_kmax = int(C_R * (7*M + 1).bit_length())  # k <= C_R log_2(7m+1)
    history.append((kmax, CONV[n][1], CONV[n+1][1], M))
    if new_kmax >= kmax:
        break
    kmax = new_kmax
for row in history:
    print(f"[CF] k <= {row[0]}: q_n={row[1]}, q_(n+1)={row[2]} -> m < {row[3]}")
M_FINAL = history[-1][3]
print(f"[CF] final: any cycle with at most {R} runs has minimum m < {M_FINAL}")

# ---- Step 3: exhaustive scan of odd m < M_FINAL ----
P9 = [9**a for a in range(64)]


def run(x):
    """Next valley after the rising run from odd x (shortcut map, closed form)."""
    t = 7*x + 1
    a = (t & -t).bit_length() - 1
    y = ((t >> a) * (P9[a] if a < 64 else 9**a) - 1) // 7
    return y >> ((y & -y).bit_length() - 1)


def run_slow(x):
    """Same, by iterating the original catalog map n->9n+1 / n->n/2."""
    assert x % 2
    n = x
    n = 9*n + 1
    while True:
        n //= 2
        if n % 2:           # odd after exactly one halving: still rising
            n = 9*n + 1
            continue
        while n % 2 == 0:
            n //= 2
        return n


for x in range(1, 20001, 2):
    assert run(x) == run_slow(x)


def chunk(bounds):
    lo, hi = bounds
    for m in range(lo | 1, hi, 2):
        x = m
        for _ in range(R):
            x = run(x)
            if x <= m:
                if x == m:
                    return m
                break
    return None


if __name__ == "__main__":
    t0 = time.time()
    step = 10**6
    jobs = [(i, min(i + step, M_FINAL)) for i in range(1, M_FINAL, step)]
    with Pool(cpu_count()) as pool:
        bad = [r for r in pool.imap_unordered(chunk, jobs) if r is not None]
    assert not bad, f"cycle found from {bad}"
    print(f"[scan] all {(M_FINAL)//2:,} odd m < {M_FINAL} excluded through {R} runs "
          f"({time.time()-t0:.0f}s, {cpu_count()} workers)")
    print(f"PASS: no positive 9n+1 cycle has <= {R} rising runs (no circuit in particular).")
