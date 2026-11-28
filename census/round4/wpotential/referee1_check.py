"""Referee 1, round 4, lens 'wpotential': independent checks, written from scratch.

Does not import wplib, accel_lib, decide or any prover file.  Exact arithmetic
(int / Fraction) everywhere except the rank computation, which is done modulo a
prime (a lower bound for the rank over Q) in numpy int64 with products < 2^61.

[TYPE]   own G_K, own SCCs: for the 8 cores (n-form), K7 z-form, 3x+1, 5x+1,
         acc_h16: the residue cycle of the claimed x* is expanding and its SCC
         is not a simple cycle (type (c)); acc_h16 must come out NOT type (c)
         (negative control).  Standing hypothesis (division-free subgraph
         acyclic) checked.  K7 z-form: G_2 is one SCC.
[SHADOW] Theorem W configuration, own construction: for x* and for periodic
         points of C^d W, an integer n with T^(kL) n = y + lam^k (n - y) >= 2n,
         n' = n mod 2^N, all intermediate iterates > n/8.  A potential
         V(n) = c(n mod 2^K) n (random c > 0) and V = bitlength must then fail
         descent somewhere on that orbit segment (checked: they do).
[DENSE]  Corollary W1(2): random walks of length 10/20/40 inside the type-(c)
         SCC of K7 z-form, sf3_13, 3x+1; an expanding rational periodic point
         is constructed and its orbit residues are compared with the walk by
         direct iteration of T-hat.
[BIJ]    Theorem A step 2: x -> y permutation for u = 3, 5, odd k <= 13;
         control: u = 3 at even k is NOT a bijection of closed walks.
[STEP3]  F(y) - F(x) = E_f(uh) - E_f(h) for padded words, random integer f.
[PUMP]   Theorem A step 1: V(T n_M) - V(n_M) - M Phi(x) independent of M, for
         3x+1 and the x5 branch of 5x+1, random f, every closed walk with k <= 5.
[RANK]   rank of f -> (E_f(uh) - E_f(h))_{h < 2^(s+2)} mod 1000000007 equals
         2^(s-1) (u=3, s<=10; u=5, s<=8); constants+coboundaries are in the
         kernel exactly and span dimension 2^(s-1).  Control: u = 1 gives 0.
[MB]     mb_s3_27: own enumeration of all rational periodic orbits of period
         <= 12 in Z_(2) cap Z_(3) (count and the expanding ones), and own
         homoclinic points following (-5,-7,-10)^d, d = 10, 20, 40.
[BRUTE]  the cores: every n < 2*10^5 reaches the expected cycle(s)
         (sanity of srs.md's stopping values; no claim of GLOBAL is made).
Exits 0 iff every check passes.
"""
import random
import sys
from fractions import Fraction
from itertools import product

import numpy as np

OK = True


def check(msg, cond):
    global OK
    print(("PASS " if cond else "FAIL ") + msg, flush=True)
    OK = OK and bool(cond)


# ---------------------------------------------------------------- systems
def stab(m, S):
    return {r: ((1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r in S else (1, 1, 1)))
            for r in range(2 ** m)}


SYS = {}
for nm, S in [("sf3_7", {7}), ("sf3_17", {1, 7}), ("sf3_57", {5, 7}), ("sf3_157", {1, 5, 7}),
              ("sf3_357", {3, 5, 7}), ("sf3_137", {1, 3, 7}), ("sf3_13", {1, 3}),
              ("sf3_135", {1, 3, 5})]:
    SYS[nm] = (3, stab(3, S), Fraction(-5) if nm in ("sf3_13", "sf3_135") else Fraction(-1))
SYS["K7z"] = (2, {0: (1, 0, 2), 1: (1, -1, 4), 2: (1, 0, 2), 3: (3, 1, 2)}, Fraction(-1))
SYS["3x+1"] = (1, {0: (1, 0, 2), 1: (3, 1, 2)}, Fraction(-1))
SYS["5x+1"] = (1, {0: (1, 0, 2), 1: (5, 1, 2)}, Fraction(-1, 3))
h16 = {}
for r in range(16):
    if r % 2 == 0:
        h16[r] = (1, 0, 2)
    elif r in (5, 9):
        h16[r] = (1, 1, 1)
    elif r == 13:
        h16[r] = (1, 5, 1)
    else:
        h16[r] = (3, 1, 1)
SYS["acc_h16"] = (4, h16, Fraction(-1))


def res(x, M):
    x = Fraction(x)
    return x.numerator * pow(x.denominator, -1, 2 ** M) % 2 ** M


def step(sysd, x):
    m, t, _ = sysd
    u, v, w = t[res(x, m)]
    y = (u * Fraction(x) + v) / w
    assert y.denominator % 2 == 1
    return y, Fraction(u, w)


def istep(sysd, n):
    m, t, _ = sysd
    u, v, w = t[n % 2 ** m]
    a = u * n + v
    assert a % w == 0
    return a // w


def edges(sysd, K):
    """G_K: r -> targets; each edge with its (u, e)."""
    m, t, _ = sysd
    E = {}
    for r in range(2 ** K):
        u, v, w = t[r % 2 ** m]
        e = w.bit_length() - 1
        assert w == 2 ** e and (u * r + v) % w == 0
        base = (u * r + v) // w
        E[r] = sorted({((base + j * u * 2 ** (K - e)) % 2 ** K, e) for j in range(2 ** e)})
        # targets: (u (r + 2^K z) + v)/2^e = base + u 2^(K-e) z, z mod 2^e
    return E


def sccs(nodes, E):
    idx, low, st, on, out, c = {}, {}, [], set(), [], [0]
    sys.setrecursionlimit(100000)

    def dfs(v):
        idx[v] = low[v] = c[0]; c[0] += 1; st.append(v); on.add(v)
        for w, _ in E[v]:
            if w not in idx:
                dfs(w); low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = st.pop(); on.discard(w); comp.append(w)
                if w == v:
                    break
            out.append(comp)
    for v in nodes:
        if v not in idx:
            dfs(v)
    return out


def periodic(sysd, y, cap=100000):
    x, lam, orb = Fraction(y), Fraction(1), []
    for _ in range(cap):
        orb.append(x)
        x, q = step(sysd, x)
        lam *= q
        if x == y:
            return orb, lam
    raise AssertionError("not periodic")


def walk_point(sysd, K, walk):
    """unique fixed point of the composed branch map along closed walk (residues mod 2^K)."""
    m, t, _ = sysd
    A, B = Fraction(1), Fraction(0)
    for r in walk:
        u, v, w = t[r % 2 ** m]
        A, B = A * u / w, (u * B + v) / w
    y = B / (1 - A)
    orb, lam = periodic(sysd, y)
    return y, A, orb


# ---------------------------------------------------------------- [TYPE]
TYPEC = {}
for nm, sysd in SYS.items():
    m, t, xs = sysd
    for K in (m, m + 2):
        E = edges(sysd, K)
        # standing hypothesis: division-free subgraph acyclic
        E0 = {r: [(s, e) for s, e in E[r] if e == 0] for r in E}
        hyp = all(len(c) == 1 and all(s != c[0] for s, _ in E0[c[0]]) for c in sccs(list(E), E0))
        orb, lam = periodic(sysd, xs)
        cyc = [res(x, K) for x in orb]
        comp = next(c for c in sccs(list(E), E) if cyc[0] in c)
        cs = set(comp)
        inner = sum(1 for a in comp for s, _ in E[a] if s in cs)
        # residue cycle may wrap several times; it is a closed walk in comp
        typec = lam > 1 and all(c in cs for c in cyc) and inner > len(comp)
        TYPEC[(nm, K)] = (typec, comp)
        exp = nm != "acc_h16"
        check(f"[TYPE] {nm} K={K}: standing hyp {hyp}; x*={xs} lam={lam}; SCC size {len(comp)}, "
              f"internal edges {inner}; type (c) = {typec} (expected {exp})", hyp and typec == exp)
check("[TYPE] K7z: G_2 is a single SCC (Lambda = Z_2)", len(TYPEC[("K7z", 2)][1]) == 4)

# ---------------------------------------------------------------- [SHADOW]
rnd = random.Random(1234)


def shadow(sysd, y, N=20, H=10 ** 12 + 39):
    orb, lam = periodic(sysd, y)
    L = len(orb)
    assert lam > 1
    k = 1
    while lam ** k < 4:
        k += 1
    D = 0
    for x in orb:
        D += (step(sysd, x)[1].denominator).bit_length() - 1
    M = N + k * D + 2
    n = res(y, M) + 2 ** M * H
    seq = [n]
    for _ in range(k * L):
        seq.append(istep(sysd, seq[-1]))
    n2 = seq[-1]
    ok = (Fraction(n2) == y + lam ** k * (n - y) and n2 % 2 ** N == n % 2 ** N
          and n2 >= 2 * n and min(seq) * 8 > n)
    return ok, seq


for nm in ["sf3_7", "sf3_137", "sf3_13", "K7z", "3x+1"]:
    sysd = SYS[nm]
    m = sysd[0]
    K = m
    E = edges(sysd, K)
    orb, lam = periodic(sysd, sysd[2])
    C = [res(x, K) for x in orb]
    typec, comp = TYPEC[(nm, K)]
    cs = set(comp)
    cedges = set(zip(C, C[1:] + C[:1]))
    a, b = next((a, s) for a in comp for s, _ in E[a] if s in cs and (a, s) not in cedges)

    def path(src, dst):
        prev, fr = {src: None}, [src]
        while fr:
            nx = []
            for v in fr:
                for w, _ in E[v]:
                    if w in cs and w not in prev:
                        prev[w] = v; nx.append(w)
            fr = nx
        p = [dst]
        while p[-1] != src:
            p.append(prev[p[-1]])
        return p[::-1]
    Wk = path(C[0], a) + path(b, C[0])[:-1] if b != C[0] else path(C[0], a)
    pts = [sysd[2]]
    for d in range(0, 60):
        y, A, o = walk_point(sysd, K, C * d + Wk)
        if A > 1 and y not in orb:
            pts.append(y)
        if len(pts) >= 5:
            break
    allok, fails = True, True
    for y in pts:
        ok, seq = shadow(sysd, y)
        allok = allok and ok
        c = {r: Fraction(rnd.randint(1, 50), rnd.randint(1, 50)) for r in range(2 ** (m + 2))}
        V1 = [c[n % 2 ** (m + 2)] * n for n in seq]
        V2 = [n.bit_length() for n in seq]
        # descent would demand V strictly decreasing along the whole segment
        fails = fails and not all(V1[i + 1] < V1[i] for i in range(len(seq) - 1)) \
            and not all(V2[i + 1] < V2[i] for i in range(len(seq) - 1))
    check(f"[SHADOW] {nm}: {len(pts)} expanding periodic points (x* and C^d W points), exact shadow "
          f"identity, growth >= 2, iterates > n/8", allok and len(pts) >= 3)
    check(f"[SHADOW] {nm}: random CM potentials c(r) n and bitlength fail descent on each shadow segment",
          fails)

# ---------------------------------------------------------------- [DENSE]
for nm in ["K7z", "sf3_13", "3x+1"]:
    sysd = SYS[nm]
    m = sysd[0]
    K = m
    E = edges(sysd, K)
    typec, comp = TYPEC[(nm, K)]
    cs = set(comp)
    orb, lam = periodic(sysd, sysd[2])
    C = [res(x, K) for x in orb]

    def path(src, dst):
        prev, fr = {src: None}, [src]
        while fr:
            nx = []
            for v in fr:
                for w, _ in E[v]:
                    if w in cs and w not in prev:
                        prev[w] = v; nx.append(w)
            fr = nx
        p = [dst]
        while p[-1] != src:
            p.append(prev[p[-1]])
        return p[::-1]
    good = True
    for tl in (10, 20, 40):
        for _ in range(4):
            wk = [rnd.choice(comp)]
            for _ in range(tl):
                wk.append(rnd.choice([s for s, _ in E[wk[-1]] if s in cs]))
            P = wk + path(wk[-1], C[0])[1:]
            tail = path(C[0], wk[0])[1:]
            for d in range(0, 500):
                closed = (P + (C[1:] + C[:1]) * d + tail)[:-1]
                A = Fraction(1)
                for r in closed:
                    u, v, w = sysd[1][r % 2 ** m]
                    A *= Fraction(u, w)
                if A > 1:
                    break
            y, A, o = walk_point(sysd, K, closed)
            # orbit of y must realise the walk exactly (residue by residue)
            x = y
            seq = []
            for _ in range(len(closed)):
                seq.append(res(x, K)); x = step(sysd, x)[0]
            good = good and seq == closed and x == y and A > 1 and seq[:tl + 1] == wk
    check(f"[DENSE] {nm}: random walks of length 10/20/40 in the type-(c) SCC are followed by an "
          f"expanding rational periodic point (direct iteration)", good)

# ---------------------------------------------------------------- [BIJ]
def closed_walks(u, k):
    out = {}
    for x in range(2 ** k):
        for c0 in range(u):
            c, y = c0, 0
            for i in range(k):
                t = u * ((x >> i) & 1) + c
                y |= (t & 1) << i
                c = t >> 1
            if c == c0:
                out.setdefault(x, []).append(y)
    return out


for u in (3, 5):
    g = True
    for k in range(1, 14, 2):
        cw = closed_walks(u, k)
        g = g and len(cw) == 2 ** k and all(len(v) == 1 for v in cw.values()) \
            and sorted(v[0] for v in cw.values()) == list(range(2 ** k))
    check(f"[BIJ] u={u}: odd k<=13, closed walks <-> words, x->y permutation", g)
cw = closed_walks(3, 4)
check("[BIJ] control u=3, k=4: closed walks NOT one per word (test can fail)",
      not (len(cw) == 16 and all(len(v) == 1 for v in cw.values())))


# ---------------------------------------------------------------- window sums
def bitsl(n):
    return [(n >> i) & 1 for i in range(n.bit_length())]


def win(bits, i, s):
    w = 0
    for j in range(s):
        p = i + j
        if 0 <= p < len(bits) and bits[p]:
            w |= 1 << j
    return w


def Ef(f, h, s):
    b = bitsl(h)
    return sum(f[win(b, i, s)] - f[0] for i in range(-(s - 1), len(b)))


def Fcyc(f, word, k, s):
    return sum(f[sum(((word >> ((i + j) % k)) & 1) << j for j in range(s))] for i in range(k))


def Vf(f, n, s):
    b = bitsl(n)
    return sum(f[win(b, i, s)] for i in range(len(b)))


g = True
for s in (2, 3, 5):
    f = [rnd.randint(-20, 20) for _ in range(2 ** s)]
    for u in (3, 5):
        for h in rnd.sample(range(1, 4000), 60):
            k = (u * h).bit_length() + s
            k += (k % 2 == 0)
            x, y = h, u * h
            g = g and Fcyc(f, y, k, s) - Fcyc(f, x, k, s) == Ef(f, u * h, s) - Ef(f, h, s)
check("[STEP3] F(y) - F(x) = E_f(uh) - E_f(h) for padded words (u=3,5; s=2,3,5)", g)

# ---------------------------------------------------------------- [PUMP]
g = True
for (u, v, e) in ((3, 1, 1), (5, 1, 1)):
    r, m = 1, 1
    for s in (2, 3):
        f = [rnd.randint(-9, 9) for _ in range(2 ** s)]
        for k in range(1, 6):
            for x in range(2 ** k):
                for c in range(u):
                    cc, y = c, 0
                    for i in range(k):
                        t = u * ((x >> i) & 1) + cc
                        y |= (t & 1) << i
                        cc = t >> 1
                    if cc != c:
                        continue
                    Phi = Fcyc(f, y, k, s) - Fcyc(f, x, k, s)
                    b = 12
                    beta = next(bb for bb in range(2 ** b)
                                if (u * (r + 2 ** m * bb) + v) >> (m + b) == c)
                    diffs = []
                    for M in range(4, 10):
                        XM = sum(x << (k * j) for j in range(M))
                        n = r + 2 ** m * (beta + 2 ** b * XM)
                        Tn = (u * n + v) // 2 ** e
                        assert (u * n + v) % 2 ** e == 0
                        diffs.append(Vf(f, Tn, s) - Vf(f, n, s) - M * Phi)
                    g = g and len(set(diffs)) == 1
check("[PUMP] V(T n_M) - V(n_M) = M Phi(x) + const for every closed walk (k<=5), 3x+1 and 5x+1 branches", g)

# ---------------------------------------------------------------- [RANK]
P = 1000000007


def rank_mod(rows):
    M = [list(r) for r in rows]
    A = np.array(M, dtype=np.int64) % P
    nr, nc = A.shape
    rk = 0
    for col in range(nc):
        if rk == nr:
            break
        piv = None
        nzs = np.nonzero(A[rk:, col])[0]
        if len(nzs) == 0:
            continue
        piv = rk + nzs[0]
        A[[rk, piv]] = A[[piv, rk]]
        inv = pow(int(A[rk, col]), P - 2, P)
        A[rk] = A[rk] * inv % P
        ot = np.nonzero(A[:, col])[0]
        ot = ot[ot != rk]
        if len(ot):
            A[ot] = (A[ot] - A[ot, col].reshape(-1, 1) * A[rk] % P) % P
        rk += 1
    return rk


def Erow(h, s):
    row = [0] * (2 ** s)
    b = bitsl(h)
    for i in range(-(s - 1), len(b)):
        row[win(b, i, s)] += 1
        row[0] -= 1
    return row


for u, smax in ((3, 10), (5, 8), (1, 4)):
    for s in range(1, smax + 1):
        rows = [[a - b for a, b in zip(Erow(u * h, s), Erow(h, s))] for h in range(1, 2 ** (s + 2))]
        rk = rank_mod(rows)
        want = 0 if u == 1 else 2 ** (s - 1)
        # kernel basis: constant + coboundaries of basis pi = e_q
        basis = [[1] * (2 ** s)]
        if s > 1:
            for q in range(2 ** (s - 1)):
                basis.append([(1 if (w >> 1) == q else 0) - (1 if (w & (2 ** (s - 1) - 1)) == q else 0)
                              for w in range(2 ** s)])
        inker = all(sum(a * b for a, b in zip(rw, bv)) == 0 for rw in rows for bv in basis)
        kd = rank_mod(basis)
        check(f"[RANK] u={u} s={s}: rank {rk} (want {want}); const+cobdry in kernel {inker}, dim {kd}",
              rk == want and inker and kd == 2 ** (s - 1))

# ---------------------------------------------------------------- [MB]
def mbs(x):
    x = Fraction(x)
    assert x.denominator % 6 in (1, 5)
    r3 = x.numerator * pow(x.denominator, -1, 27) % 27
    r2 = x.numerator * pow(x.denominator, -1, 2) % 2
    if r3 == 26:
        return (x + 1) / 27, Fraction(1, 27)
    if r2 == 0:
        return x / 2, Fraction(1, 2)
    return (3 * x + 1) / 2, Fraction(3, 2)


def mbi(n):
    if n % 27 == 26:
        return (n + 1) // 27
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


BR = {0: (1, 1, 27), 1: (1, 0, 2), 2: (3, 1, 2)}
orbits = {}
for Lw in range(1, 13):
    for word in product((0, 1, 2), repeat=Lw):
        # Horner composition with ints: x -> (A x + B)/W
        A, B, Wd = 1, 0, 1
        for bch in word:
            u, v, w = BR[bch]
            A, B, Wd = A * u, u * B + v * Wd, Wd * w
        if A == Wd:
            continue
        y = Fraction(B, Wd - A)
        if y.denominator % 2 == 0 or y.denominator % 3 == 0:
            continue
        z, okw, orb = y, True, []
        for bch in word:
            u, v, w = BR[bch]
            z2, _ = mbs(z)
            if z2 != (u * z + v) / w:
                okw = False
                break
            orb.append(z)
            z = z2
        if okw and z == y:
            key = min(orb)
            if key not in orbits:
                orbits[key] = len(set(orb))
expo = []
for key, per in orbits.items():
    z, lam = key, Fraction(1)
    for _ in range(per):
        z, q = mbs(z)
        lam *= q
    assert z == key
    if lam > 1:
        expo.append((key, per, lam))
expo.sort()
print("  mb_s3_27 orbits:", len(orbits), "expanding:", [(str(a), b, str(c)) for a, b, c in expo])
check("[MB] mb_s3_27: 16274 rational periodic orbits of period <= 12; expanding exactly "
      "{-10 (9/8), -10138/139 (11, 2187/2048)}",
      len(orbits) == 16274 and [(a, b, c) for a, b, c in expo] ==
      [(Fraction(-10138, 139), 11, Fraction(2187, 2048)), (Fraction(-10), 3, Fraction(9, 8))])
hg = True
for d in (10, 20, 40):
    hit = None
    for Lw in range(1, 5):
        for wd in product((0, 1, 2), repeat=Lw):
            word = (2, 2, 1) * d + wd
            A, B, Wd = 1, 0, 1
            for bch in word:
                u, v, w = BR[bch]
                A, B, Wd = A * u, u * B + v * Wd, Wd * w
            if A == Wd:
                continue
            y = Fraction(B, Wd - A)
            if y.denominator % 6 not in (1, 5):
                continue
            z, okw = y, True
            for bch in word:
                u, v, w = BR[bch]
                z2, _ = mbs(z)
                if z2 != (u * z + v) / w:
                    okw = False
                    break
                z = z2
            if okw and z == y and Fraction(A, Wd) > 1 and y not in (-5, -7, -10):
                hit = (y, Fraction(A, Wd), word)
                break
        if hit:
            break
    if not hit:
        hg = False
        continue
    y, lam, word = hit
    k = 1
    while lam ** k < 4:
        k += 1
    a2 = sum(1 for bch in word if bch) * k
    a3 = 3 * sum(1 for bch in word if bch == 0) * k
    N = 12
    m2, m3 = 2 ** (N + a2), 3 ** (N + a3)
    r2 = y.numerator * pow(y.denominator, -1, m2) % m2
    r3 = y.numerator * pow(y.denominator, -1, m3) % m3
    n = (r2 * m3 * pow(m3, -1, m2) + r3 * m2 * pow(m2, -1, m3)) % (m2 * m3) + m2 * m3 * 999983
    z = n
    for _ in range(k * len(word)):
        z = mbi(z)
    hg = hg and Fraction(z) == y + lam ** k * (n - y) and z >= 2 * n and (z - n) % 6 ** N == 0
check("[MB] mb_s3_27: for d = 10, 20, 40 an expanding rational periodic point follows (-5,-7,-10)^d, "
      "exact shadow identity on integers", hg)

# ---------------------------------------------------------------- [BRUTE]
for nm in ["sf3_7", "sf3_17", "sf3_57", "sf3_157", "sf3_357", "sf3_137", "sf3_13", "sf3_135"]:
    sysd = SYS[nm]
    stops = {1, 2, 4} if nm != "sf3_13" else None
    known = {}
    cyc_seen = set()
    good = True
    for n0 in range(1, 200000):
        n, seen, path = n0, set(), []
        steps = 0
        while n not in known and n not in seen:
            seen.add(n); path.append(n)
            n = istep(sysd, n)
            steps += 1
            if steps > 10 ** 5 or n > 10 ** 30:
                good = False
                break
        if n in seen:
            i = path.index(n)
            cyc_seen.add(min(path[i:]))
            tgt = min(path[i:])
        else:
            tgt = known.get(n)
        for q in path:
            known[q] = tgt
    if nm == "sf3_137":
        # round 3 lists sf3_137 as 'divergence expected' (positive drift); srs.md leaves it out
        check(f"[BRUTE] sf3_137: some n < 2e5 escape 10^30 / 10^5 steps (divergence expected); cycles "
              f"seen {sorted(cyc_seen)}", (not good) and sorted(cyc_seen) == [1, 3, 7, 39])
        continue
    want = [1, 3] if nm == "sf3_13" else [1]
    check(f"[BRUTE] {nm}: all n < 2e5 reach cycles with minima {sorted(cyc_seen)}",
          good and sorted(cyc_seen) == want)

# ---------------------------------------------------------------- [TYPEB]
# Counter-example to theory.md section 0 ("[the W2 classes, counters included] do not
# even reach type (b)"): the type-(b) system acc_h16 has a certificate in the class
# "residue data + counter v_2(n+1) at the single orbit {-1,-2} + lexicographic tuple".
#   V(n) = (lev(n mod 16), phi(n)),  lev = longest path to a sink in the SCC DAG of G_4,
#   phi = c(r) n on the contracting SCC,  2 v_2(n+1) on node 15,  2 v_2(n/2+1) + 1 on node 14,
#   0 on transient nodes.  Descent: lev drops, or lev equal and phi drops by >= 1/2.
sysd = SYS["acc_h16"]
K = 4
E = edges(sysd, K)
comps = sccs(list(E), E)
cid = {v: i for i, c in enumerate(comps) for v in c}
succ = {i: set() for i in range(len(comps))}
for a in E:
    for b, _ in E[a]:
        if cid[a] != cid[b]:
            succ[cid[a]].add(cid[b])
lev = {}


def L_(i):
    if i not in lev:
        lev[i] = 1 + max((L_(j) for j in succ[i]), default=-1)
    return lev[i]


for i in succ:
    L_(i)
internal = {i: [(a, b) for a in comps[i] for b, _ in E[a] if cid[b] == i] for i in range(len(comps))}
shadow_c = cid[15]
contr = [i for i in range(len(comps)) if internal[i] and i != shadow_c]
# weights on contracting SCCs: exact c(r) from Bellman-Ford longest paths, verified with Fractions
import math
cw = {}
theta = Fraction(99, 100)
for i in contr:
    nodes = comps[i]
    pot = {v: 0.0 for v in nodes}
    for _ in range(len(nodes) + 2):
        for a, b in internal[i]:
            u, v_, w = sysd[1][a % 16]
            wt = math.log(u / w) - math.log(float(theta))
            pot[b] = max(pot[b], pot[a] + wt)
    for v in nodes:
        cw[v] = Fraction(math.exp(-pot[v])).limit_denominator(10 ** 6)
okc = all(cw[b] * Fraction(sysd[1][a % 16][0], sysd[1][a % 16][2]) <= theta * cw[a]
          for i in contr for a, b in internal[i])
beta = max(cw.values()) * 5   # c(s) * max(v,0)/w with v <= 5, w >= 1


def V(n):
    r = n % 16
    i = cid[r]
    if i == shadow_c:
        if r == 15:
            ph = 2 * ((n + 1) & -(n + 1)).bit_length() - 2
        else:
            ph = 2 * ((n // 2 + 1) & -(n // 2 + 1)).bit_length() - 1
        return (lev[i], Fraction(ph))
    if i in contr:
        return (lev[i], cw[r] * n)
    return (lev[i], Fraction(0))


# internal contracting step: V(Tn) <= theta V(n) + beta <= V(n) - 1/2 once V(n) >= (beta + 1/2)/(1 - theta)
thr = (beta + 1) / ((1 - theta) * min(cw.values()))
desc_ok, bad = okc, []
for n in range(1, 300000):
    a, b = V(n), V(istep(sysd, n))
    if not (b[0] < a[0] or (b[0] == a[0] and b[1] <= a[1] - Fraction(1, 2))):
        bad.append(n)
check(f"[TYPEB] acc_h16 (type b): SCC sizes {sorted(len(c) for c in comps)}, shadow SCC {sorted(comps[shadow_c])}; "
      f"lexicographic (DAG level, c(r) n | counter v_2(n+1)) potential descends off a finite set: "
      f"failures below 3e5 all < {max(bad) if bad else 0} (bound {float(thr):.0f})",
      okc and all(n < thr for n in bad))

print("ALL PASS" if OK else "SOME CHECK FAILED")
raise SystemExit(0 if OK else 1)
