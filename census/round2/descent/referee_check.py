"""Referee check for the 'descent' lens (round 2).  Exit 0 iff all parts pass.

Uses only the step functions / residue tables in systems.py, not descent_lib.

1. An independent first-descent engine (steps through the real step function,
   refines whenever 2^m does not divide the slope) recomputes, for s8_35,
   s32_max, s32_d65: max steps k, and the exceptional set E.
2. One-step weighted potential V(n) = n * c(n mod 32) with 32 integer weights
   for s32_max and s32_d65 (lambda = 499/500): every edge of the mod-32
   transition graph satisfies q * c(target) <= lambda * c(source).  Hence
   V(T n) <= lambda V(n) + d * cmax, so V strictly drops while
   n > d * cmax / ((1 - lambda) * cmin) = B.  All n <= B are simulated.
3. s8_35: the two-block valuation argument (tier 1), checked symbolically.
4. Exact 2-adic growing cycles for split7_1, m3_4n5, s32_plus9 (all partial
   products > 1 from the stated starting point).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
import systems


def engine(s, maxK=60):
    T, p, Q = s['step'], s['p'], s['p'] ** s['m']
    leaves, stack = [], [(0, 0, 1, 0, 0)]
    while stack:
        K, r, P, R, j = stack.pop()
        M = p ** K
        if j > 0 and (P < M or (P == M and R < r)):
            leaves.append((K, r, j, P, R))
            continue
        if P % Q == 0:
            t0 = 0 if R > 0 else Q
            v0, v1 = T(P * t0 + R), T(P * (t0 + 1) + R)
            nP = v1 - v0
            nR = v0 - nP * t0
            assert T(P * (t0 + 7) + R) == nP * (t0 + 7) + nR
            stack.append((K, r, nP, nR, j + 1))
        else:
            assert K < maxK
            for x in range(p):
                stack.append((K + 1, r + x * M, p * P, R + x * P, j))
    assert sum(F(1, p ** l[0]) for l in leaves) == 1
    E = []
    for K, r, j, P, R in leaves:
        M = p ** K
        if P < M and R >= r:
            E += [M * t + r for t in range((R - r) // (M - P) + 1) if M * t + r > 0]
    return max(l[2] for l in leaves), sorted(E)


def cycle_of(T, n):
    seen = set()
    x = n
    while x not in seen:
        seen.add(x)
        x = T(x)
    c = [x]
    y = T(x)
    while y != x:
        c.append(y)
        y = T(y)
    return (min(c), len(c))


# 1. independent engine
for sid, k_exp, E_exp in [('desc_s8_35', 6, [1]), ('desc_s32_max', 44, [1]),
                          ('desc_s32_d65', 44, None)]:
    k, E = engine(systems.get(sid))
    assert k == k_exp, (sid, k)
    if E_exp is not None:
        assert E == E_exp, (sid, E)
    else:
        assert len(E) == 63 and max(E) == 1519
    print(sid, 'independent engine: k =', k, '|E| =', len(E))

# 2. weighted potential, one step
W = {0: 200, 1: 602, 2: 302, 3: 908, 4: 200, 5: 602, 6: 455, 7: 1370, 8: 200,
     9: 303, 10: 302, 11: 908, 12: 228, 13: 602, 14: 687, 15: 2068, 16: 200,
     17: 602, 18: 345, 19: 201, 20: 200, 21: 602, 22: 455, 23: 1370, 24: 261,
     25: 687, 26: 394, 27: 522, 28: 520, 29: 785, 30: 1037, 31: 201}
lam = F(499, 500)
for sid, expected in [('desc_s32_max', [(1, 3)]),
                      ('desc_s32_d65', [(1, 21), (5, 5), (7, 29), (13, 4), (39, 5),
                                        (65, 3), (299, 8), (1135, 13)])]:
    s = systems.get(sid)
    tab, T = s['table'], s['step']
    d = max(v for (u, v, w) in tab)
    for r in range(32):
        u, v, w = tab[r]
        tg = [((u * r + v) % 32, F(u))] if w == 1 else [(r // 2, F(1, 2)), (r // 2 + 16, F(1, 2))]
        for t, q in tg:
            assert q * W[t] <= lam * W[r], (sid, r, t)
    # transition graph is sound: T(n) mod 32 is one of the listed targets
    for n in range(1, 5000):
        r = n % 32
        u, v, w = tab[r]
        assert (T(n) % 32 == (u * r + v) % 32) if w == 1 else (T(n) % 16 == r // 2)
    B = (d * max(W.values()) * 500) // min(W.values())   # d*cmax/((1-lam)cmin)
    cyc = set(cycle_of(T, n) for n in range(1, B + 1))
    assert sorted(cyc) == expected, (sid, sorted(cyc))
    print(sid, 'one-step potential OK; all n <=', B, 'reach', sorted(cyc))

# 3. s8_35 two-block argument: odd n -> next odd value ("block")
#    n=8t+1 -> 4t+1 ; n=8t+7 -> <= t+1 ; n=8t+5 -> <= 3t+2 ; n=8t+3 -> 12t+5 (odd), then block again
T = systems.get('desc_s8_35')['step']
for n in range(1, 200001, 2):
    x = T(n)
    while x % 2 == 0:
        x = T(x)
    r = n % 8
    if r == 3:
        assert x == (3 * n + 1) // 2 and x % 8 in (1, 5)
        y = T(x)
        while y % 2 == 0:
            y = T(y)
        assert y < n
    elif n > 1:
        assert x < n
print('desc_s8_35 two-block argument consistent on odd n <= 2e5')

# 4. obstructions
def orbit(sid, x0):
    s = systems.get(sid)
    Q, tab = s['p'] ** s['m'], s['table']
    x, lam, mins = F(x0), F(1), []
    for i in range(100):
        r = (x.numerator * pow(x.denominator, -1, Q)) % Q
        u, v, w = tab[r]
        x = (u * x + v) / w
        lam *= F(u, w)
        mins.append(lam)
        if x == F(x0):
            return i + 1, lam, min(mins)
    raise AssertionError(sid)

for sid, x0, L, mult in [('desc_split7_1', F(-1, 3), 3, F(7, 4)),
                         ('desc_m3_4n5', F(-5), 2, F(4, 3)),
                         ('desc_s32_plus9', F(-227, 115), 12, F(243, 128))]:
    got = orbit(sid, x0)
    assert got[0] == L and got[1] == mult and got[2] > 1, (sid, got)
    print(sid, 'growing p-adic cycle through', x0, 'period', L, 'multiplier', mult)
print('PASS')
