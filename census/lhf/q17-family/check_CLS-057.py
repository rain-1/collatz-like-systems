#!/usr/bin/env python3
"""Check for census/lhf/q17-family/CLS-057.md (family theorem for A_m(q)).

Map T_{q,m}: n even -> n/2; n odd -> (n + c q)/m, c in [0,m-1] with m | n + c q.
Exact integers only. Exit 0 iff every check passes.
"""
import sys, random
from math import gcd
from collections import deque

def make_T(q, m):
    qi = pow(q, -1, m)
    def T(n):
        if n % 2 == 0:
            return n // 2
        return (n + ((-n * qi) % m) * q) // m
    return T

def subgroup(gens, q):
    H, fr = {1 % q}, [1 % q]
    while fr:
        x = fr.pop()
        for g in gens:
            y = x * g % q
            if y not in H:
                H.add(y); fr.append(y)
    return H

FAIL = []
def ok(cond, msg):
    if not cond:
        FAIL.append(msg); print("FAIL:", msg)

class Sys:
    def __init__(self, q, m):
        self.q, self.m, self.T = q, m, make_T(q, m)
        T = self.T
        # [1,q] invariant
        ok(all(1 <= T(n) <= q for n in range(1, q + 1)), f"{q},{m}: [1,q] invariant")
        # cycles in [1,q]
        seen, cyc = set(), []
        for n in range(1, q + 1):
            x, path = n, []
            while x not in seen and x not in path:
                path.append(x); x = T(x)
            if x in path:
                cyc.append(path[path.index(x):])
            seen |= set(path)
        self.cycles = cyc
        self.cyc_of = {x: i for i, c in enumerate(cyc) for x in c}
        self.H = subgroup([2 % q, m % q], q)
        self.memo = {}
    def basin(self, n):
        T, path, x = self.T, [], n
        while x not in self.cyc_of:
            if x in self.memo:
                r = self.memo[x]; break
            path.append(x); x = T(x)
        else:
            r = self.cyc_of[x]
        if n < 10**6:
            for y in path:
                if y < 10**6: self.memo[y] = r
        return r
    def coset(self, u):
        return min(u * h % self.q for h in self.H)
    def shared(self):
        by = {}
        for i, c in enumerate(self.cycles):
            if gcd(c[0], self.q) == 1:
                by.setdefault(self.coset(c[0]), []).append(i)
        return {k: v for k, v in by.items() if len(v) > 1}

def check_basic(S, N):
    q, m, T = S.q, S.m, S.T
    for n in range(q + 1, N):
        ok(T(n) < n, f"descent {q},{m},{n}") if T(n) >= n else None
    for n in range(1, N):
        b = S.basin(n)
        if S.basin(2 * n) != b or S.basin(m * n) != b:
            ok(False, f"dilation {q},{m},{n}"); break
        # gcd(n,q) and unit coset invariant under T
        t = T(n)
        if gcd(t, q) != gcd(n, q):
            ok(False, f"gcd invariant {q},{m},{n}"); break
        if gcd(n, q) == 1 and S.coset(t % q) != S.coset(n % q):
            ok(False, f"coset invariant {q},{m},{n}"); break
    for y in range(1, 4000, 2):
        L, R, Sx = m * y, m * y - 2 * q, 2 * m * y - q
        ok(T(L) == y and L % 2 == 1, "L")
        if R > 0: ok(T(R) == y and R % 2 == 1, "R")
        if Sx > 0: ok(T(T(Sx)) == y and Sx % 2 == 1, "S")

def lemma_rough_residues(S, b, Q):
    """Residues mod Q reachable from odd b by words in L,R,S; compare to the predicted set."""
    q, m = S.q, S.m
    start = b % Q
    seen = {start}; dq = deque([start])
    while dq:
        y = dq.popleft()
        for z in ((m * y) % Q, (m * y - 2 * q) % Q, (2 * m * y - q) % Q):
            if z not in seen:
                seen.add(z); dq.append(z)
    g = gcd(q, Q)
    Hb = {h * b % q for h in S.H}
    pred = set()
    for y in range(Q):
        if Q % 2 == 0 and y % 2 == 0: continue
        if any((y - hb) % g == 0 for hb in Hb):
            pred.add(y)
    return seen == pred

def rough_witness(S, b, c, Q, lo):
    """Odd z >= lo, z = c (mod Q), z in basin of b's cycle, by BFS over L,R,S words from m^N b."""
    q, m = S.q, S.m
    o = 1
    while pow(m, o, Q) != 1 % Q: o += 1
    y0 = b
    while y0 < max(lo, q): y0 *= m ** o
    dq = deque([y0]); seen = {y0 % Q}
    while dq:
        y = dq.popleft()
        if y % Q == c % Q and y >= lo:
            return y
        for z in (m * y, m * y - 2 * q, 2 * m * y - q):
            if z % Q not in seen:
                seen.add(z % Q); dq.append(z)
    return None

def mix_witness(S, x, M, tgt_cycle):
    """Construct x' = x (mod M), x' > x, basin(x') = tgt_cycle, following the proof."""
    q, m, T = S.q, S.m, S.T
    # path x -> first odd point c of its cycle; A = product of denominators
    path, y = [x], x
    while not (y in S.cyc_of and y % 2 == 1):
        y = T(y); path.append(y)
    c = y; A = 1
    for v in path[:-1]:
        A *= 2 if v % 2 == 0 else m
    Cx = S.cycles[S.cyc_of[c]]
    a = sum(1 for v in Cx if v % 2 == 0); bb = len(Cx) - a
    Lam = 2 ** a * m ** bb
    Mm, Q = 1, M
    for p in range(2, m + 1):
        if m % p == 0 and all(p % r for r in range(2, p)):
            while Q % p == 0: Q //= p; Mm *= p
    b = next(v for v in S.cycles[tgt_cycle] if v % 2 == 1)
    z = rough_witness(S, b, c, Q, c + 1)
    if z is None: return None
    t = 0
    while (Lam ** t) % Mm: t += 1
    y = c + Lam ** t * (z - c)
    return x + A * (y - c)

def main():
    random.seed(1)
    systems = [(17, 3), (53, 3), (13, 7), (19, 5), (5, 11), (11, 17), (121, 3), (9, 19)]
    # the four smallest-q records quoted in the note
    for q, m in systems:
        S = Sys(q, m)
        sh = S.shared()
        ok(len(sh) > 0, f"{q},{m}: some coset holds >=2 cycles")
        check_basic(S, 60000 if q < 60 else 20000)
        for key, idx in sh.items():
            bs = [next(v for v in S.cycles[i] if v % 2 == 1) for i in idx]
            for Q in (1, 2, 4, 5, 7, 8, 12 if m % 3 else 10, q, 2 * q, q * q, 11 * q):
                if gcd(Q, m) != 1: continue
                ok(lemma_rough_residues(S, bs[0], Q), f"rough residues {q},{m},Q={Q}")
            units = [u for u in range(1, 2000) if gcd(u, q) == 1 and S.coset(u % q) == key]
            for M in (1, 2, 8, m, m * m * 4, q, q * q, 2 * m * q, 7 * 8 * q if q % 7 else 5 * 8 * q):
                for x in random.sample(units, 4):
                    for i in idx:
                        xp = mix_witness(S, x, M, i)
                        ok(xp is not None and xp % M == x % M and xp > x and S.basin(xp) == i,
                           f"mix {q},{m}: x={x} M={M} target={i}")
        print(f"q={q} m={m}: cycles={[min(c) for c in S.cycles]} shared cosets={sh}")
    # q=17 corollary: every unit class mod 17^2 and mod 2^4*3^3*17 contains both basins
    S = Sys(17, 3)
    A, B = S.cyc_of[1], S.cyc_of[5]
    for M in (289, 16 * 27 * 17):
        hit = {}
        for n in range(1, 400000):
            if n % 17: hit.setdefault(n % M, set()).add(S.basin(n))
        ok(all(hit.get(r) == {A, B} for r in range(M) if r % 17), f"q17 both basins in every unit class mod {M}")
    # section identity for the kernel step, (k,p) pairs
    S = Sys(13, 7); f = lambda n: 0 if n == 0 else int(S.basin(n) == S.cyc_of[1])
    for k, p in ((2, 7), (3, 2), (6, 2), (10, 2), (13, 2), (4, 7)):
        e = 3
        a = 1
        while k ** a <= 2 * 13 * p ** e: a += 1
        D = k ** a
        for d in range(p ** e):
            r0 = (-D * d) % p ** e
            r = next(r0 + p ** e * j for j in range(13) if gcd(r0 + p ** e * j, 13) == 1)
            ok(r < D, "r<D")
            for j in range(e + 1):
                dj = d % p ** j
                rj = (D * dj + r) // p ** j
                ok((D * dj + r) % p ** j == 0 and 0 <= rj < D and any(gcd(D * n + rj, 13) == 1 for n in range(13)), "rj")
                for n in range(30):
                    ok(f(D * (p ** j * n + dj) + r) == f(D * n + rj), "section")
    print("FAILURES:", len(FAIL))
    sys.exit(1 if FAIL else 0)

main()
