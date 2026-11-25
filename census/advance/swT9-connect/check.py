#!/usr/bin/env python3
"""check.py for census/advance/swT9-connect (CLS-055, swT9_s8).

Verifies the finite facts F1-F4 used in theorem.md, then runs sanity checks
(not needed by the proof) that build G_K from real integers and also run
the constructive algorithm of the proof. Exact integer arithmetic only.
Exit code 0 iff everything passes.
"""
import random
import sys
from math import gcd

OK = True


def check(cond, msg):
    global OK
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        OK = False


def T(n):
    q, r = divmod(n, 3)
    return 2 * q if r == 0 else (4 * q + 1 if r == 1 else 4 * q + 3)


def Q(n):
    t = T(n)
    if t % 18 == 9:
        return t + 1
    if t % 18 == 10:
        return t - 1
    return t


# ---------------------------------------------------------------- F1: pieces
# Claimed: Q(n) = (alpha_r n + beta_r)/3 for n = r (mod 27), with
# T's pieces (2n/3, (4n-1)/3, (4n+1)/3 for r = 0,1,2 mod 3) except at r = 7, 15, 20.
PIECE = {}
for r in range(27):
    if r % 3 == 0:
        PIECE[r] = (2, 0)
    elif r % 3 == 1:
        PIECE[r] = (4, -1)
    else:
        PIECE[r] = (4, 1)
PIECE[15] = (2, -3)
PIECE[7] = (4, 2)
PIECE[20] = (4, 4)

N1 = 300000
good = all(3 * Q(n) == PIECE[n % 27][0] * n + PIECE[n % 27][1] for n in range(1, N1 + 1))
check(good, f"F1 sample: Q(n) = (alpha_r n + beta_r)/3 for all 1 <= n <= {N1} "
            "(T's pieces except r=15:(2n-3)/3, r=7:(4n+2)/3, r=20:(4n+4)/3)")
# Symbolic proof of F1 for all n: on n = 27t + r both sides are affine in t,
# so agreement at t = 0 and t = 1 for every r, plus the fact that T(n) mod 18
# depends only on n mod 27, gives all t.  Check the latter on t = 0..2.
good = True
for r in range(27):
    for t in range(3):
        n = 27 * t + r
        if n == 0:
            continue
        # T(27t + r) = T(r') + 18t or 36t with r' = r: T(n) mod 18 = T(r) mod 18
        good &= (T(n) - T(r if r else 27)) % 18 == 0
check(good, "F1 symbolic: T(n) mod 18 depends only on n mod 27 (slopes 18,36 on t)")

# ------------------------------------------------------- F2: G_27 strongly conn
def qmod9(r):
    a, b = PIECE[r]
    return ((a * r + b) // 3) % 9 if r else 0


# Q(r) mod 9 computed from the piece at a positive representative
OUT27 = {}
for r in range(27):
    rep = r if r else 27
    OUT27[r] = [s for s in range(27) if s % 9 == Q(rep) % 9]


def strongly_connected(adj, V):
    V = list(V)
    s0 = V[0]

    def reach(g):
        seen = {s0}
        st = [s0]
        while st:
            v = st.pop()
            for w in g[v]:
                if w not in seen:
                    seen.add(w)
                    st.append(w)
        return seen
    rev = {v: [] for v in V}
    for v in V:
        for w in adj[v]:
            rev[w].append(v)
    return len(reach(adj)) == len(V) and len(reach(rev)) == len(V)


check(strongly_connected(OUT27, range(27)),
      "F2: H = G_27 (r -> r' iff r' = Q(r) mod 9) is strongly connected")

# --------------------------------------------- F3: 2-adic covering of in-pieces
# For each class c mod 9, the in-neighbours r (Q(r) = c mod 9) have 2-adic
# images beta_r/3 + alpha_r Z_2 ; check they cover Z_2 (alpha_r | 4, so mod 4).
inv3_mod4 = 3  # 3*3 = 9 = 1 mod 4
good = True
for c in range(9):
    ins = [r for r in range(27) if Q(r if r else 27) % 9 == c]
    covered = set()
    for r in ins:
        a, b = PIECE[r]
        base = (b * inv3_mod4) % 4
        covered |= {y for y in range(4) if (y - base) % a == 0}
    good &= covered == {0, 1, 2, 3}
check(good, "F3: for every class c mod 9 the images beta_r/3 + alpha_r Z_2 over "
            "in-neighbours r of c cover Z_2")

# --------------------------------------------- F4: the two closed walks at 0
def compose_walk(walk):
    """walk = list of vertices v0..vN; returns (A, B, N) with map u -> (A u + B)/3^N."""
    A, B, N = 1, 0, 0
    for v, w in zip(walk, walk[1:]):
        assert w in OUT27[v], (v, w)
        a, b = PIECE[v]
        A, B, N = a * A, a * B + b * 3 ** N, N + 1
    return A, B, N


W1 = [0, 0, 0, 0]
W2 = [0, 9, 15, 0]
check(compose_walk(W1) == (8, 0, 3) and compose_walk(W2) == (8, -27, 3),
      "F4: closed walks W1 = 0>0>0>0 (map 8u/27) and W2 = 0>9>15>0 (map (8u-27)/27) exist in H")

# ------------------------------------------------- sanity: G_K from integers
def G_from_integers(K):
    """Subgraph of G_K realised by integers n in [1, 3*27*K]; a subgraph, so
    strong connectivity of it implies strong connectivity of G_K."""
    adj = {x: set() for x in range(K)}
    for n in range(1, 3 * 27 * K + 1):
        adj[n % K].add(Q(n) % K)
    return adj


Ks = [81, 162, 243, 324, 405, 486, 567, 729, 810, 1215, 1458, 2187, 2430, 3*3**5*7, 3**4*11, 3**4*16]
good = True
for K in Ks:
    good &= strongly_connected(G_from_integers(K), range(K))
check(good, f"sanity: G_K (built from actual integers) strongly connected for K in {Ks}")


# ---------------------------- sanity: run the constructive proof on G_{27L}
def steer(rp, y, a):
    """Walk (vertex list) ending at rp whose map is constant = y mod 2^a."""
    if a == 0:
        return [rp]
    for r in range(27):
        if rp not in OUT27[r]:
            continue
        al, be = PIECE[r]
        # need y = f_r(z) mod 2^a for some z: 3y - be = al*z  (2-adically)
        if (3 * y - be) % gcd(al, 2 ** a) == 0:
            v = {2: 1, 4: 2}[al]
            ap = max(a - v, 0)
            z = ((3 * y - be) // al) % (2 ** ap) if ap else 0
            return steer(r, z, ap) + [rp]
    raise AssertionError("covering failed")


def apply_walk(walk, u, M):
    for v in walk[:-1]:
        a, b = PIECE[v]
        u = (a * u + b) * pow(3, -1, M) % M
    return u


def path27(s, t):
    from collections import deque
    prev = {s: None}
    dq = deque([s])
    while dq:
        v = dq.popleft()
        if v == t:
            break
        for w in OUT27[v]:
            if w not in prev:
                prev[w] = v
                dq.append(w)
    p = [t]
    while p[-1] != s:
        p.append(prev[p[-1]])
    return p[::-1]


def construct(r0, u0, rp, y, a, m):
    L = 2 ** a * m
    W = steer(rp, y % 2 ** a, a)
    sW = W[0]
    A1 = path27(r0, 0)
    A2 = path27(0, sW)
    # order of W1-map on Z/m, and target
    if m > 1:
        # order k of the multiplier 8/27 mod m (W1 acts as u -> 8u/27)
        lam = 8 * pow(27, -1, m) % m
        k, p = 1, lam
        while p != 1:
            p, k = p * lam % m, k + 1
        tau = W1[:-1] * (k - 1) + W2  # map u -> u - 1 on Z/m
        # target v with g_W(g_A2(v')) = y mod m ; solve by search (m small)
        start = apply_walk(A1, u0, m)
        want = [v for v in range(m) if apply_walk(W, apply_walk(A2, v, m), m) == y % m]
        assert len(want) == 1
        j = (start - want[0]) % m
        mid = A1[:-1] + (tau[:-1] * j) + A2
    else:
        mid = A1[:-1] + A2
    walk = mid[:-1] + W
    assert walk[0] == r0 and walk[-1] == rp
    for v, w in zip(walk, walk[1:]):
        assert w in OUT27[v]
    return apply_walk(walk, u0, L) == y % L


random.seed(1)
good = True
cnt = 0
for (a, m) in [(0, 5), (3, 1), (5, 7), (4, 11), (7, 13), (10, 25), (2, 35)]:
    L = 2 ** a * m
    for _ in range(40):
        r0, rp = random.randrange(27), random.randrange(27)
        u0, y = random.randrange(L), random.randrange(L)
        good &= construct(r0, u0, rp, y, a, m)
        cnt += 1
check(good, f"sanity: constructive proof produced a correct walk in G_27L for {cnt} random (start,target) pairs")

print("ALL PASS" if OK else "SOME CHECK FAILED")
sys.exit(0 if OK else 1)
