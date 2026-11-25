"""Shared exact-integer routines for the seven-nine low-hanging-fruit checks.

Maps (accelerated forms used for cycle enumeration):
  P7 : even n -> n/2, odd n -> 7n+1        acc(n) = (7n+1)/2^v   on odd n
  P9 : even n -> n/2, odd n -> 9n+1        acc(n) = (9n+1)/2^v   on odd n
  P77: even n -> n/2, odd n -> 7n+7        (reduced to P7 on 7Z)
  M3E: 3|n -> n/3, n=1 (3) -> 7n+2, n=2 (3) -> 7n+1
                                           acc(n) = (7n+r)/3^v  on n not = 0 (3)
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
import systems as census_systems  # noqa: E402


def step_p(q, c):
    return lambda n: n // 2 if n % 2 == 0 else q * n + c


def step_m3e(n):
    r = n % 3
    if r == 0:
        return n // 3
    return 7 * n + 2 if r == 1 else 7 * n + 1


STEPS = {
    'P7': step_p(7, 1),
    'P9': step_p(9, 1),
    'P77': step_p(7, 7),
    'M3E': step_m3e,
}
CENSUS_ID = {'P7': 'par_7_1_s3', 'P9': 'par_9_1_s5', 'P77': 'par_7_7_s9', 'M3E': 'm3_e_s7'}


def agree_with_census(name, N=5000):
    f = STEPS[name]
    g = census_systems.get(CENSUS_ID[name])['step']
    return all(f(n) == g(n) for n in range(1, N))


# ---------------------------------------------------------------------------
# (1) Congruence obstruction: every nonempty forward-closed union of residue
#     classes mod M contains the class of 1 (of 7 for P77).  Equivalently, in the residue
#     graph mod M (edges r -> class of T(n) for every n = r mod M), the class
#     of 1 is reachable from every class.  We check this for M <= bound with
#     M divisible by the "division" base (2 or 3); other moduli are covered
#     by refining M to 2M or 3M (a union of classes mod M is also one mod 2M).
# ---------------------------------------------------------------------------

def residue_edges(name, M):
    """Successor classes of each residue r mod M (exact: images of r+M t)."""
    succ = []
    if name in ('P7', 'P9', 'P77'):
        q, c = {'P7': (7, 1), 'P9': (9, 1), 'P77': (7, 7)}[name]
        assert M % 2 == 0
        for r in range(M):
            if r % 2 == 0:
                h = r // 2           # (r + M t)/2 = h + (M/2) t
                succ.append((h % M, (h + M // 2) % M))
            else:
                succ.append(((q * r + c) % M,))  # q(r+Mt)+c = qr+c mod M
    else:
        assert M % 3 == 0
        for r in range(M):
            if r % 3 == 0:
                h = r // 3
                succ.append(tuple((h + j * (M // 3)) % M for j in range(3)))
            else:
                succ.append((step_m3e(r) % M,))  # 7(r+Mt)+c = 7r+c mod M
    return succ


def all_reach_one(name, M):
    succ = residue_edges(name, M)
    pred = [[] for _ in range(M)]
    for r, ss in enumerate(succ):
        for s in ss:
            pred[s].append(r)
    seen = [False] * M
    target = (7 if name == 'P77' else 1) % M
    seen[target] = True
    stack = [target]
    while stack:
        x = stack.pop()
        for y in pred[x]:
            if not seen[y]:
                seen[y] = True
                stack.append(y)
    return all(seen)


def check_obstruction(name, Mmax):
    base = 3 if name == 'M3E' else 2
    bad = [M for M in range(base, Mmax + 1, base) if not all_reach_one(name, M)]
    return bad


# ---------------------------------------------------------------------------
# (2) Cycles with few "expanding" terms.
#   For a cycle with k expanding terms n_1..n_k (odd terms for P7/P9, terms
#   not divisible by 3 for M3E), multiplying the ratios gives
#       prod_i (q + r_i/n_i) = base^K,   K = total number of divisions,
#   with q = 7 or 9, r_i <= rmax (1, or 2 for M3E), base = 2 or 3.
#   If n_1 = min n_i then q^k < base^K <= (q + rmax/n_1)^k, so with K0 the
#   least K having base^K > q^k:  (q n_1 + rmax)^k >= base^K0 n_1^k.
#   B_k = the largest n with that inequality (exact integer test).
# ---------------------------------------------------------------------------

PARAMS = {'P7': (7, 1, 2), 'P9': (9, 1, 2), 'M3E': (7, 2, 3)}


def _ok(q, rmax, k, BK, n):
    return (q * n + rmax) ** k >= BK * n ** k


def min_bound(name, k):
    q, rmax, base = PARAMS[name]
    K = math.floor(k * math.log(q, base)) - 2
    while base ** K <= q ** k:
        K += 1
    BK = base ** K
    if not _ok(q, rmax, k, BK, 1):
        return 0
    # float estimate n ~ rmax / (base^(K/k) - q), then exact correction
    d = base ** (K / k) - q
    est = int(rmax / d) if d > 0 else 1
    n = max(1, est)
    while n > 1 and not _ok(q, rmax, k, BK, n):
        n -= 1
    while _ok(q, rmax, k, BK, n + 1):
        n += 1
    assert _ok(q, rmax, k, BK, n) and not _ok(q, rmax, k, BK, n + 1)
    return n


def acc(name):
    if name == 'M3E':
        def f(n):
            m = 7 * n + (2 if n % 3 == 1 else 1)
            while m % 3 == 0:
                m //= 3
            return m
        return f, (lambda n: n % 3 != 0)
    q = PARAMS[name][0]

    def g(n):
        m = q * n + 1
        m >>= (m & -m).bit_length() - 1
        return m
    return g, (lambda n: n % 2 == 1)


def cycles_up_to(name, L):
    """Return list of (k, min element) of all cycles with k <= L expanding terms.
    Exact: n is tested as the minimum expanding element for every k with B_k >= n."""
    B = [0] + [min_bound(name, k) for k in range(1, L + 1)]
    X = max(B)
    # need[n] = largest k with B_k >= n
    need = [0] * (X + 2)
    for k in range(1, L + 1):
        if B[k] >= 1:
            need[B[k]] = max(need[B[k]], k)
    for n in range(X - 1, 0, -1):
        need[n] = max(need[n], need[n + 1])
    f, is_exp = acc(name)
    found = []
    for n in range(1, X + 1):
        if not is_exp(n):
            continue
        x = n
        for i in range(1, need[n] + 1):
            x = f(x)
            if x <= n:
                if x == n:
                    found.append((i, n))
                break
    return found, X


# ---------------------------------------------------------------------------
# common driver for the per-item check scripts
# ---------------------------------------------------------------------------
EXPECTED_CYCLES = {'P7': [(1, 1)], 'P9': [], 'M3E': [(1, 1), (5, 4)]}


def run_standard(name, L=1000, Mmax=1000):
    ok = True
    if not agree_with_census(name):
        print(name, 'step disagrees with census/systems.py'); ok = False
    bad = check_obstruction(name, Mmax)
    print(f'{name}: residue graph mod M, M<={Mmax}: class of target reachable from every class:', not bad)
    ok &= not bad
    if name in EXPECTED_CYCLES:
        found, X = cycles_up_to(name, L)
        print(f'{name}: cycles with <= {L} expanding terms (min element <= {X} tested):', found)
        ok &= (found == EXPECTED_CYCLES[name])
    return ok
