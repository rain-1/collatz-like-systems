"""Referee: independent period<=26 cycle enumeration for the 6 S-family systems
not covered in referee_check.py [CYC].  Same algorithm as referee_check.cycles_upto
(pruned DFS over closed walks of G_m with exact integer composition);
duplicated here. Runtime: about 5 s."""
import sys
from fractions import Fraction

def r_sf(m, S):
    S = set(S)
    def T(n):
        if n % 2 == 0:
            return n // 2
        return 3 * n + 1 if n % (2 ** m) in S else n + 1
    return T

def cycle_from(f, n, cap=10 ** 6):
    seen = {}
    while n not in seen:
        seen[n] = 1
        n = f(n)
    c, z = [n], f(n)
    while z != n:
        c.append(z); z = f(z)
    return c

def cycles_upto(m, S, L):
    Q = 2 ** m
    E = {}
    for r in range(Q):
        if r % 2 == 0:
            E[r] = [(r // 2, 0), (r // 2 + Q // 2, 0)]
        else:
            E[r] = [((3 * r + 1) % Q, 1)] if r in S else [((r + 1) % Q, 2)]
    T = r_sf(m, S)
    found = set()
    for r0 in range(Q):
        can = [set([r0])]
        for t in range(1, L + 1):
            can.append({s for s in range(Q) if any(b in can[t - 1] for b, _ in E[s])})
        reach = [set().union(*can[:k + 1]) for k in range(L + 1)]
        stack = [(r0, 0, 1, 0, 0)]
        while stack:
            s, l, A, B, b = stack.pop()
            if l > 0 and s == r0 and b > 0:
                den = 2 ** b - A
                if den != 0 and B % den == 0:
                    x = B // den
                    if x > 0 and x % Q == r0:
                        found.add(min(cycle_from(T, x)))
            if l == L:
                continue
            for nb, kind in E[s]:
                if nb in reach[L - l - 1]:
                    if s % 2 == 0:
                        stack.append((nb, l + 1, A, B, b + 1))
                    elif kind == 1:
                        stack.append((nb, l + 1, 3 * A, 3 * B + 2 ** b, b))
                    else:
                        stack.append((nb, l + 1, A, B + 2 ** b, b))
    return sorted(found)

EXP = {(2, (1, 3)): [1], (3, (1, 3, 5)): [1], (3, (5, 7)): [1], (3, (1, 5, 7)): [1],
       (3, (3, 5, 7)): [1], (3, (1, 3, 5, 7)): [1]}
ok = True
for (m, S), e in EXP.items():
    g = cycles_upto(m, set(S), 26)
    print(("PASS" if g == e else "FAIL"), m, S, g, flush=True)
    ok &= g == e
sys.exit(0 if ok else 1)
