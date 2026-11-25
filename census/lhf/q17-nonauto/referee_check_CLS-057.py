"""Referee's independent check for CLS-057 (qrA3_q17).

Uses the repository step function (census/round2/qr/systems.py, via qrlib.famA)
rather than a local copy. Rebuilds the Theorem-mix witnesses with a different
implementation (BFS over words in L,R mod Q; explicit reverse paths), verifies
each by forward iteration with the repo step, and checks the kernel-section
identity used in the Cobham step on random words. Exact integers; exit 0 iff all pass.
"""
import os, sys, random
from collections import deque
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "round2", "qr"))
from systems import get
step = get("qrA3_q17")["step"]
random.seed(51)
bad = []
def need(c, m):
    if not c: bad.append(m); print("FAIL", m)

def rep(n):
    seen = set()
    while n not in seen:
        seen.add(n); n = step(n)
    while True:                      # n is on the cycle; return its minimum
        cyc = [n]; m = step(n)
        while m != n: cyc.append(m); m = step(m)
        return min(cyc)

# 0. repo step agrees with the stated rule; branch digits
for n in range(1, 300000):
    exp = n // 2 if n % 2 == 0 else (n + 17 * (n % 3)) // 3
    need(step(n) == exp, ("rule", n)) if step(n) != exp else None
need(sorted({rep(n) for n in range(1, 18)}) == [1, 5, 17], "cycle reps")
need(all((rep(n) == 17) == (n % 17 == 0) for n in range(1, 50000)), "B17 = 17N")

def path_to_rep(x):
    """forward path x -> c in {1,5}; returns c and list of predecessor values."""
    p = [x]
    while p[-1] not in (1, 5):
        p.append(step(p[-1]))
        assert len(p) < 10**5 and p[-1] != 17
    return p[-1], p[:-1]

def reverse(path_preds, y):
    """Re-apply the inverse branches of a recorded forward path to new endpoint y."""
    for u in reversed(path_preds):
        y = 2 * y if u % 2 == 0 else 3 * y - 17 * (u % 3)
    return y

def rough(b, c, Q, extra):
    """odd z in B_b with z = c mod Q, built by BFS on words in L(y)=3y, R(y)=3y-34."""
    if Q == 1:
        return 3 ** extra * b
    prev = {b % Q: None}; dq = deque([b % Q])
    while dq:
        r = dq.popleft()
        for s, g in (("L", (3 * r) % Q), ("R", (3 * r - 34) % Q)):
            if g not in prev: prev[g] = (r, s); dq.append(g)
    need(c % Q in prev, ("unreachable", b, c, Q))
    word = []; r = c % Q
    while prev[r] is not None: r, s = prev[r]; word.append(s)
    word.reverse()
    o = 1
    while pow(3, o, Q) != 1: o += 1
    h = o * extra
    while True:
        y = 3 ** h * b; ys = [y]
        for s in word:
            y = 3 * y if s == "L" else 3 * y - 34; ys.append(y)
        if all(v > 0 for v in ys): return y
        h += o

def basin(n):
    return rep(n)

count = 0
mods = [1, 2, 3, 4, 9, 17, 34, 51, 72, 85, 119, 289, 1155, 2023, 4913, 9792, 30030 // 2, 6 * 17 * 13]
for M in mods + [random.randint(2, 20000) for _ in range(25)]:
    u = v = 0; Q = M
    while Q % 2 == 0: Q //= 2; u += 1
    while Q % 3 == 0: Q //= 3; v += 1
    xs = [x for x in range(1, M + 1) if x % 17][:6] + [random.randrange(1, 10**6) for _ in range(3)]
    for x in xs:
        if x % 17 == 0: continue
        c, preds = path_to_rep(x)
        for b in (1, 5):
            for extra in (1, 3):
                z = rough(b, c, Q, extra)
                e2 = extra
                while z < c:            # Theorem mix needs z >= c
                    e2 += 1; z = rough(b, c, Q, e2)
                need(z % 2 == 1 and (z - c) % Q == 0 and basin(z) == b, ("rough", M, x, b))
                t = max(u, (v + 1) // 2)
                lap = [c, step(c), step(step(c))]
                y = z
                for _ in range(t): y = reverse(lap, y)
                need(y == c + 18 ** t * (z - c), ("lap", c))
                w = reverse(preds, y)
                need(w % M == x % M and w > x and basin(w) == b, ("mix", M, x, b))
                count += 1

# Kernel-section identity f(D(p^j n + d_j) + r) = f(D n + r_j) on random words.
for k, p in [(2, 3), (3, 2), (5, 2), (7, 2), (10, 2), (12, 2), (16, 3), (17, 2), (34, 2), (51, 2)]:
    for _ in range(6):
        e = random.randint(1, 5); digs = [random.randrange(p) for _ in range(e)]
        d = sum(di * p ** i for i, di in enumerate(digs))
        a = 1
        while k ** a <= 2 * p ** e: a += 1
        D = k ** a
        r0 = (-D * d) % p ** e
        r = r0 if r0 % 17 else r0 + p ** e
        need(r % 17 and r < D, "r choice")
        for j in range(e + 1):
            dj = d % p ** j
            need((D * dj + r) % p ** j == 0, "integral")
            rj = (D * dj + r) // p ** j
            need(0 <= rj < D and (D % 17 or rj % 17), "rj range/unit")
            for n in range(0, 40):
                lhs = D * (p ** j * n + dj) + r
                rhs = D * n + rj
                if lhs == 0 or rhs == 0: continue
                need(basin(lhs) == basin(rhs), ("section", k, p, j, n))

print("referee witnesses:", count)
print("PASS" if not bad else "FAIL %d" % len(bad))
sys.exit(1 if bad else 0)
