#!/usr/bin/env python3
"""Independent referee check for census/round3/deep (written from the .md texts only;
imports nothing from the prover's libraries).

Sections
  F   family.md: classification re-implemented from the written definitions; Theorems D, K,
      Lemmas S, R on exhaustive small and random 256-bit inputs; SPLIT(3,1,3) <-> 3x+3.
  B1  X_d = SPLIT(1,1,d), odd d <= 151: brute-force cycles vs the coset formula, cycle count
      formula, basin = coset on n <= 3000 and random 120-bit n.
  BS  Sigma_d, gcd(d,6)=1, d < 200 and d = 7081: classes of <2,3>, cycles, shared counts
      (44 / 23), catalog rows, congruence basins on random large n.
  B2  an independent constructive implementation of the accessibility proof (Steps 1-3),
      executed on random (y, x, M) for d = 13, 31, 61, 7081 with y in each of two cycles
      sharing a class; the produced w is checked to satisfy w = x mod M and to merge with y:
      every link of the constructed odd-ancestor chain is checked by the exact parent identity
      (Sigma_d(par) = child * 2^j, j >= 2), the u forward blocks from w are simulated literally,
      and when w has <= 20000 bits the whole orbit of w is also simulated until it hits y.
      (For d = 7081 the construction can give w with millions of bits, so literal simulation
      of every orbit is not affordable; the chain check is exact and complete.)
  B4  the identity g(4m) = g(3m) (f(4m+d) path), and f(2m)=f(m) closure facts.
  OM  Omega: coding bijection/affinity; H_2(q_c) by Decimal (60 digits); rho_min by Decimal;
      independent rigorous upper certificates (rational theta, rational entry upper bounds,
      exact 2x2 criterion, Decimal log2) and independent lower bounds (exact multinomial
      counts with my own parameter search), compared with the claimed intervals; exact
      loop-word DP lower bounds log2(Z_m)/m; cycle-lemma count check at excursion level.
  Z3  split5_3 on 3Z vs SPLIT(1,5,1).
Exit 0 iff all pass.  Runtime: about 15 seconds.
"""
import math
import random
import sys
from collections import deque
from decimal import Decimal, getcontext
from fractions import Fraction
from math import gcd, comb

getcontext().prec = 60
rng = random.Random(97531)
FAIL = []


def ok(c, msg):
    if not c:
        FAIL.append(msg)
        print("FAIL:", msg)


def SPLIT(a, b, d):
    def f(n):
        if n % 2 == 0:
            return n // 2
        return a * n + d if n % 4 == 1 else b * n + d
    return f


def nextodd(f, n):
    x, k = f(n), 1
    while x % 2 == 0:
        x, k = f(x), k + 1
    return x, k


# ============================== F ==========================================
def v_of(a, b, d):
    return (2 if (a + d) % 4 == 0 else 1), (2 if (3 * b + d) % 4 == 0 else 1)


def my_class(a, b, d):
    va, vb = v_of(a, b, d)
    if a == b:
        return 'P'
    if a < 2 ** va and b < 2 ** vb:
        return 'C'
    if va == 1 and vb == 1:
        return 'D' if min(a, b) >= 3 else 'K'
    e = gcd(d, a)
    if e > 1 and b < 2 ** vb:
        return 'R'
    e = gcd(d, b)
    if e > 1 and a < 2 ** va:
        return 'R'
    return 'O'


cnt = {}
for a in (1, 3, 5, 7):
    for b in (1, 3, 5, 7):
        for d in range(1, 16, 2):
            c = my_class(a, b, d)
            cnt[c] = cnt.get(c, 0) + 1
ok(cnt == {'P': 32, 'C': 8, 'K': 16, 'D': 16, 'R': 8, 'O': 48}, f"F counts {cnt}")
# Theorem D condition equivalence: a+d=2, 3b+d=2 mod 4 <=> a+b=0, d=2-a mod 4
for a in range(1, 40, 2):
    for b in range(1, 40, 2):
        for d in range(1, 40, 2):
            l = (a + d) % 4 == 2 and (3 * b + d) % 4 == 2
            r = (a + b) % 4 == 0 and (d - 2 + a) % 4 == 0
            ok(l == r, f"F D-cond {a,b,d}")
# Theorem D on wider parameters (a,b up to 21)
for a in range(3, 22, 2):
    for b in range(3, 22, 2):
        for d in range(1, 22, 2):
            if v_of(a, b, d) == (1, 1):
                f = SPLIT(a, b, d)
                for n in list(range(1, 2000, 2)) + [rng.getrandbits(256) | 1 for _ in range(5)]:
                    y, k = nextodd(f, n)
                    ok(k == 2 and y > n, f"F thmD {a,b,d,n}")
# Theorem K on wider parameters (c up to 23, d up to 41)
for c in range(3, 24, 2):
    for d in range(1, 42, 2):
        for (a, b) in ((1, c), (c, 1)):
            if v_of(a, b, d) != (1, 1):
                continue
            ok(c % 4 == 3, f"F K c mod 4 {a,b,d}")
            f = SPLIT(a, b, d)
            e = d * (c - 1) // 2
            for n in list(range(1, 1500, 2)) + [rng.getrandbits(256) | 1 for _ in range(5)]:
                y, k = nextodd(f, n)
                x = (n - d) // 2
                px = x // 2 if x % 2 == 0 else (c * x + e) // 2
                ok(k == 2 and (x % 2 == 0 or (c * x + e) % 2 == 0) and (y - d) // 2 == px, f"F thmK {a,b,d,n}")
# SPLIT(3,1,3) on odd n <-> x -> x/2, (3x+3)/2 ; and 3x+3 on 3Z <-> Collatz
f = SPLIT(3, 1, 3)
for n in range(1, 5001, 2):
    y, _ = nextodd(f, n)
    x = (n - 3) // 2
    ok((y - 3) // 2 == (x // 2 if x % 2 == 0 else (3 * x + 3) // 2), f"F 313 {n}")
for y in range(-5, 3000):
    x = 3 * y
    px = x // 2 if x % 2 == 0 else (3 * x + 3) // 2
    py = y // 2 if y % 2 == 0 else (3 * y + 1) // 2
    ok(px == 3 * py, f"F 3x+3 {y}")
# Lemma S, Lemma R
for a in (1, 3, 5, 7, 9):
    for b in (1, 3, 5, 7, 9):
        for d in range(1, 46, 2):
            f = SPLIT(a, b, d)
            for e in range(3, d + 1, 2):
                if d % e:
                    continue
                g = SPLIT(a, b, d // e) if e % 4 == 1 else SPLIT(b, a, d // e)
                for m in list(range(1, 300)) + [rng.getrandbits(128) for _ in range(3)]:
                    ok(f(e * m) == e * g(m), f"F S {a,b,d,e,m}")
            ea = gcd(d, a)
            if ea > 1:
                for n in range(1, 400, 4):   # n = 1 mod 4 -> a-branch lands in eZ
                    ok((a * n + d) % ea == 0, f"F R {a,b,d}")
# the 8 R reductions as stated
for (src, tgt) in {(1, 5, 5): (1, 5, 1), (1, 5, 15): (1, 5, 3), (1, 7, 7): (7, 1, 1),
                   (3, 5, 5): (3, 5, 1), (5, 1, 5): (5, 1, 1), (5, 1, 15): (5, 1, 3),
                   (5, 3, 15): (5, 3, 3), (7, 3, 7): (3, 7, 1)}.items():
    a, b, d = src
    ok(my_class(*src) == 'R' and my_class(*tgt) == 'O', f"F Rtab {src}")
    ea, eb = gcd(d, a), gcd(d, b)
    va, vb = v_of(a, b, d)
    e = ea if (ea > 1 and b < 2 ** vb) else eb
    got = (a, b, d // e) if e % 4 == 1 else (b, a, d // e)
    ok(got == tgt, f"F Rtarget {src} {got}")
print("F done", cnt)


# ============================== B1 =========================================
def ordmod(g, m):
    if m == 1:
        return 1
    k, x = 1, g % m
    while x != 1:
        x, k = x * g % m, k + 1
    return k


def phi(n):
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def cyc_from(f, n, cap=10 ** 6):
    seen = set()
    while n not in seen:
        seen.add(n)
        n = f(n)
    c, m = [n], f(n)
    while m != n:
        c.append(m)
        m = f(m)
    return frozenset(c)


for d in range(1, 152, 2):
    f = SPLIT(1, 1, d)
    cycles = {cyc_from(f, n) for n in range(1, 2 * d + 1)}
    # cosets
    seen, cos = set(), []
    for r in range(d):
        if r in seen:
            continue
        K, x = set(), r
        while x not in K:
            K.add(x)
            x = 2 * x % d
        seen |= K
        cos.append(K)
    pred = set()
    for K in cos:
        Kh = {r if r else d for r in K}
        C = Kh | {r + d for r in Kh if r % 2}
        pred.add(frozenset(C))
        ok(len(C) == len(K) + sum(1 for r in Kh if r % 2), "B1 len")
    ok(cycles == pred, f"B1 cycles d={d}")
    ok(len(cos) == sum(phi(e) // ordmod(2, e) for e in range(1, d + 1) if d % e == 0), f"B1 count {d}")
    lab = {}
    for C in pred:
        for v in C:
            lab[v] = C
    cosof = {}
    for K in cos:
        for r in K:
            cosof[r] = frozenset(K)
    for n in list(range(1, 3000)) + [rng.getrandbits(120) for _ in range(20)]:
        x = n
        while x not in lab:
            x = f(x)
        C = lab[x]
        ok(all(cosof[v % d] == cosof[n % d] for v in C), f"B1 basin {d} {n}")
print("B1 done")


# ============================== BS =========================================
def sigma(d):
    def f(n):
        if n % 2 == 0:
            return n // 2
        return n + d if (n + d) % 4 == 0 else 3 * n + d
    return f


def classes23(d):
    lab, k = {}, 0
    for r in range(d):
        if r in lab:
            continue
        st = [r]
        lab[r] = k
        while st:
            x = st.pop()
            for g in (2, 3, pow(2, -1, d) if d > 1 else 0, pow(3, -1, d) if d > 1 else 0):
                y = x * g % d
                if y not in lab:
                    lab[y] = k
                    st.append(y)
        k += 1
    return lab, k


def sigma_data(d):
    f = sigma(d)
    cyc = {}
    for n in range(1, d + 1):
        C = cyc_from(f, n)
        cyc[min(C)] = C
    lab, k = classes23(d) if d > 1 else ({0: 0}, 1)
    per = {}
    for m, C in cyc.items():
        ls = {lab[v % d] for v in C}
        ok(len(ls) == 1, f"BS invariance on cycle {d}")
        per.setdefault(ls.pop(), []).append(m)
    return f, cyc, lab, k, per


# the formula Sigma_d = SPLIT(3,1,d) (d=1 mod 4) / SPLIT(1,3,d) (d=3 mod 4)
for d in range(1, 200, 2):
    g = SPLIT(3, 1, d) if d % 4 == 1 else SPLIT(1, 3, d)
    s = sigma(d)
    for n in range(1, 400):
        ok(g(n) == s(n), f"BS sigma=split {d}")
shared, only = [], []
for d in range(1, 200, 2):
    if gcd(d, 6) != 1:
        continue
    f, cyc, lab, k, per = sigma_data(d)
    ok(len(per) == k, f"BS every class has a cycle {d}")
    (shared if any(len(v) > 1 for v in per.values()) else only).append(d)
    # congruence basins for cycles alone in their class: random large n
    owner = {}
    for m, C in cyc.items():
        for v in C:
            owner[v] = m
    for n in [rng.getrandbits(100) + 1 for _ in range(15)]:
        x = n
        while x not in owner:
            x = f(x)
        mlist = per[lab[n % d]]
        ok(owner[x] in mlist, f"BS class invariance {d} {n}")
ok(len(shared) + len(only) == 67 and len(only) == 44 and len(shared) == 23, f"BS counts {len(only)} {len(shared)}")
listed = [13, 29, 31, 55, 61, 65, 67, 85, 91, 109, 113, 119, 125, 127, 131, 139, 143, 145, 155,
          161, 167, 169, 187]
ok(shared == listed, f"BS shared list {shared}")
expect = {5: (2, [1, 5], []), 7: (2, [1, 7], []), 13: (2, [1, 5, 13], [[1, 5]]),
          71: (3, None, []), 73: (3, None, []), 97: (3, None, [])}
for d, (k0, cm, sh) in expect.items():
    f, cyc, lab, k, per = sigma_data(d)
    ok(k == k0, f"BS classes {d} {k}")
    if cm:
        ok(sorted(cyc) == cm, f"BS cycles {d} {sorted(cyc)}")
    ok([sorted(v) for v in per.values() if len(v) > 1] == sh, f"BS shared {d}")
    ok(len(cyc) == k, f"BS ncycles {d}") if not sh else None
f7081, cyc7081, lab7081, k7081, per7081 = sigma_data(7081)
ok(k7081 == 9 and len(cyc7081) == 10, f"BS 7081 {k7081} {len(cyc7081)}")
ok([sorted(v) for v in per7081.values() if len(v) > 1] == [[569, 713]], f"BS 7081 shared {per7081}")
# split_13 catalog rule equals Sigma_13
cat13 = lambda n: n // 2 if n % 2 == 0 else (3 * n + 13 if n % 4 == 1 else n + 13)
ok(all(cat13(n) == sigma(13)(n) for n in range(1, 10000)), "BS cat13")
print("BS done: congruence-only", len(only), "shared", len(shared), "7081 cycles", sorted(cyc7081))


# ============================== B2 =========================================
def v3(n):
    k = 0
    while n % 3 == 0:
        n //= 3
        k += 1
    return k


def construct(d, y, x, M, H=60):
    """Literal execution of Steps 1-3 of Theorem B2.  Returns w."""
    f = sigma(d)
    M = M * d // gcd(M, d)
    u = v = 0
    Q = M
    while Q % 2 == 0:
        Q //= 2; u += 1
    while Q % 3 == 0:
        Q //= 3; v += 1
    # Step 3 forward: u blocks from x
    c, l, kp = x, 0, 0
    for _ in range(u):
        if c % 2 == 0:
            c //= 2; l += 1
        else:
            if (c + d) % 4 == 0:
                c = (c + d) // 4
            else:
                c = (3 * c + d) // 4; kp += 1
            l += 2
    e = 0
    co = c
    while co % 2 == 0:
        co //= 2; e += 1
    S = v + kp
    # Step 1: odd ancestor z of y with 3 not dividing z
    z = y
    while z % 2 == 0:
        z = f(z)          # odd part of y = forward iterate
    chain = [z]
    if z % 3 == 0:
        h = 2
        while 2 ** h * z <= d:
            h += 1
        z = 2 ** h * z - d
        chain.append(z)
    o = ordmod(2, Q)
    k = v3(o)
    hf = next(h for h in range(H, H + 2 * 3 ** (k + 1) + 2)
              if (2 ** h * z - 4 * d) % 3 ** (k + 1) == 0)

    def wof(h):
        num = 4 ** k * (2 ** h * z - 4 * d)
        assert num % 3 ** (k + 1) == 0
        return d + num // 3 ** (k + 1)
    r0 = wof(hf) % Q
    # Step 2: BFS on Z/Q from r0 to co mod Q with L2, L3, U2
    i3 = pow(3, -1, Q) if Q > 1 else 0
    ops = {'L2': lambda r: (4 * r - d) % Q, 'L3': lambda r: (8 * r - d) % Q,
           'U2': lambda r: (4 * r - d) * i3 % Q}
    tgt = co % Q
    # 0-1 BFS: minimise the number of U2 letters (each costs one extra power of 3)
    prev = {r0: None}
    dist = {r0: 0}
    dq = deque([r0])
    done = set()
    while dq:
        r = dq.popleft()
        if r in done:
            continue
        done.add(r)
        for nm, g in ops.items():
            s2 = g(r)
            w_ = 1 if nm == 'U2' else 0
            if s2 not in dist or dist[r] + w_ < dist[s2]:
                dist[s2] = dist[r] + w_
                prev[s2] = (r, nm)
                (dq.append if w_ else dq.appendleft)(s2)
    assert tgt in prev, "target residue not in G-orbit"
    word = []
    r = tgt
    while prev[r] is not None:
        r, nm = prev[r]
        word.append(nm)
    word.reverse()
    # backward 3-adic requirement
    t, s = co % 3 ** S, S
    for nm in reversed(word):
        if nm in ('L2', 'L3'):
            hh = 2 if nm == 'L2' else 3
            mod = 3 ** s
            t = (t + d) * pow(2, -hh, mod) % mod if mod > 1 else 0
        else:
            s += 1
            mod = 3 ** s
            t = (d + 3 * t) * pow(4, -1, mod) % mod
    # solve 2^h z = 4d + 3^(k+1) 4^(-k) (t - d)  (mod 3^(k+1+s))  by a 3-adic discrete log
    # (2 is a primitive root mod 3^N), then CRT with h = hf (mod o)  -- exactly the proof's step
    N = k + 1 + s
    mod = 3 ** N
    A = (4 * d + 3 ** (k + 1) * pow(4, -k, mod) * (t - d)) * pow(z, -1, mod) % mod
    e_ = 0 if A % 3 == 1 else 1
    ordc = 2
    for i_ in range(2, N + 1):
        m_ = 3 ** i_
        e_ = next(e_ + jj * ordc for jj in range(3) if pow(2, e_ + jj * ordc, m_) == A % m_)
        ordc *= 3
    assert pow(2, e_, mod) == A
    m1, m2 = ordc, o           # h = e_ mod 2*3^(N-1), h = hf mod o
    g_ = gcd(m1, m2)
    assert (e_ - hf) % g_ == 0, "CRT incompatible (contradicts the proof)"
    lcm_ = m1 // g_ * m2
    # brute CRT over the small factor
    h = next(hf + jj * m2 for jj in range(m1 // g_) if (hf + jj * m2 - e_) % m1 == 0)
    h %= lcm_
    while h < hf:
        h += lcm_
    assert (2 ** h * z - 4 * d) % 3 ** (k + 1) == 0 and wof(h) % 3 ** s == t % 3 ** s
    w0 = wof(h)
    assert w0 % Q == r0
    xx = (2 ** h * z - d) // 3
    chain.append(xx)
    for _ in range(k):
        xx = (4 * xx - d) // 3
        chain.append(xx)
    assert xx == w0
    # forward through the word with actual integers
    cur = w0
    for nm in word:
        if nm == 'L2':
            cur = 4 * cur - d
        elif nm == 'L3':
            cur = 8 * cur - d
        else:
            assert (4 * cur - d) % 3 == 0
            cur = (4 * cur - d) // 3
        chain.append(cur)
    cpp = cur
    assert cpp % 2 == 1 and (cpp - co) % (3 ** S * Q) == 0
    cp = 2 ** e * cpp
    num = 2 ** l * (cp - c)
    assert num % 3 ** kp == 0
    w = x + num // 3 ** kp
    construct.chain = chain
    construct.mid = (u, cp, cpp)
    return w, M


def is_parent(d, par, child):
    """par odd, and Sigma_d maps par to child * 2^j (j >= 2), child odd: par -> ... -> child."""
    if par <= 0 or par % 2 == 0 or child % 2 == 0:
        return False
    img = par + d if (par + d) % 4 == 0 else 3 * par + d
    j = (img & -img).bit_length() - 1
    return j >= 2 and img >> j == child


def merges_symbolic(d, w, yo):
    """Verify w merges with yo: simulate the u forward blocks from w literally, halve to c'',
    then check every link of the recorded odd-ancestor chain by the exact parent identity."""
    f = sigma(d)
    u, cp, cpp = construct.mid
    cur = w
    for _ in range(u):
        if cur % 2 == 0:
            cur = f(cur)
        else:
            cur = f(f(f(cur)))
    if cur != cp:
        return False
    while cur % 2 == 0:
        cur = f(cur)
    if cur != cpp:
        return False
    ch = construct.chain
    if ch[0] != yo:
        return False
    return all(is_parent(d, ch[i + 1], ch[i]) for i in range(len(ch) - 1)) and ch[-1] == cpp


def reaches(f, w, y, cap=10 ** 6):
    cap = max(cap, 40 * w.bit_length() + 10 ** 5)
    for _ in range(cap):
        if w == y:
            return True
        w = f(w)
    return False


ntests = 0
for d, pair in [(13, (1, 5)), (31, None), (61, None), (7081, (569, 713))]:
    f, cyc, lab, k, per = sigma_data(d) if d != 7081 else (f7081, cyc7081, lab7081, k7081, per7081)
    if pair is None:
        pair = next(v for v in per.values() if len(v) > 1)[:2]
    cl = lab[pair[0] % d]
    for trial in range(6 if d == 7081 else 10):
        for ycyc in pair:
            ylist = sorted(cyc[ycyc])
            y = rng.choice(ylist)
            if rng.random() < 0.5:   # also use a non-cycle ancestor-ish y
                y = y * 2 ** rng.randrange(0, 4)
            while True:
                x = rng.randrange(1, 10 ** 6)
                if lab[x % d] == cl:
                    break
            M = 2 ** rng.randrange(0, 5) * 3 ** rng.randrange(0, 3) * rng.choice([1, 5, 7, 11, 25]) \
                if d != 7081 else 2 ** rng.randrange(0, 4) * 3 ** rng.randrange(0, 2)
            if gcd(M, d) > 1 and d == 13:
                M = M  # fine; lcm taken
            w, MM = construct(d, y, x, M)
            ok(w > 0 and (w - x) % MM == 0, f"B2 congruence {d} {y} {x} {M}")
            yo = y
            while yo % 2 == 0:
                yo //= 2            # odd part of y: a forward iterate, so reaching it = merging
            ok(merges_symbolic(d, w, yo), f"B2 chain {d} {y} {x} {M}")
            if w.bit_length() <= 20000:     # literal simulation as well when affordable
                ok(reaches(f, w, yo), f"B2 merges {d} {y} {x} {M}")
            ntests += 1
            if '-v' in sys.argv:
                print('   B2', d, y, x, M, w.bit_length(), flush=True)
print("B2 constructive proof executed on", ntests, "targets")

# ============================== B4 =========================================
for d in (13, 31, 7081):
    f = sigma(d)
    for m in list(range(0, 3000)) + [rng.getrandbits(150) for _ in range(30)]:
        n = 4 * m + d
        ok(f(f(f(n))) == 3 * m + d and (3 * n + d) % 4 == 0, f"B4 {d} {m}")
print("B4 done")

# ============================== OM =========================================
LN2 = Decimal(2).ln()


def H2(x):
    x = Decimal(x)
    return -(x * x.ln() + (1 - x) * (1 - x).ln()) / LN2


for c, claim in [(5, "0.5806841231"), (9, "0.9499555"), (13, "0.9952676")]:
    q = 1 - 2 * LN2 / Decimal(c).ln()
    h = H2(q)
    ok(abs(h - Decimal(claim)) < Decimal("1e-%d" % (len(claim) - 2)), f"OM H2 c={c}: {h}")
    print("  c=%d H2(q_c)=%s" % (c, str(h)[:16]))


def moves(a, b, d):
    va, vb = v_of(a, b, d)
    return {'U': [('U', Fraction(1, 2)), ('O', Fraction(1))],
            'O': [('U' if va == 2 else 'O', Fraction(a, 2 ** va)),
                  ('U' if vb == 2 else 'O', Fraction(b, 2 ** vb))]}


def rho_dec(a, b, d, th):
    th = Decimal(th)
    M = {(s, t): Decimal(0) for s in 'UO' for t in 'UO'}
    for s, lst in moves(a, b, d).items():
        for t, sl in lst:
            M[(s, t)] += (th * (Decimal(sl.numerator) / Decimal(sl.denominator)).ln()).exp()
    A, B, C, D = M[('U', 'U')], M[('U', 'O')], M[('O', 'U')], M[('O', 'O')]
    tr, det = A + D, A * D - B * C
    return (tr + (tr * tr - 4 * det).sqrt()) / 2


def rho_min(a, b, d):
    lo, hi = Decimal(0), Decimal(10)
    for _ in range(120):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if rho_dec(a, b, d, m1) < rho_dec(a, b, d, m2):
            hi = m2
        else:
            lo = m1
    th = (lo + hi) / 2
    return th, rho_dec(a, b, d, th)


for c in (5, 9, 13):
    for mem in ((c, 1, 3), (1, c, 1), (c, 1, 7)):
        th, r = rho_min(*mem)
        q = 1 - 2 * LN2 / Decimal(c).ln()
        ok(abs(r.ln() / LN2 - H2(q)) < Decimal("1e-20"), f"OM T1 rho vs H2 {mem}")


def iroot_ceil(N, q):
    """smallest integer u with u^q >= N"""
    if N <= 0:
        return 0
    u = int(round(N ** (1.0 / q))) if N < 10 ** 300 else 1 << ((N.bit_length() + q - 1) // q)
    lo, hi = 0, max(u, 1)
    while hi ** q < N:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** q >= N:
            hi = mid
        else:
            lo = mid
    return hi


def pow_up(sl, p, q, K=10 ** 18):
    # rational u/K >= sl^(p/q):  (u/K)^q >= sl^p  <=>  u^q * den^p >= num^p * K^q
    N = sl.numerator ** p * K ** q
    D = sl.denominator ** p
    return Fraction(iroot_ceil(-(-N // D), q), K)


def upper_cert(a, b, d):
    th, r = rho_min(a, b, d)
    q = 997
    p = int((th * q).to_integral_value())
    E = {(s, t): Fraction(0) for s in 'UO' for t in 'UO'}
    for s, lst in moves(a, b, d).items():
        for t, sl in lst:
            E[(s, t)] += pow_up(sl, p, q)
    A, B, C, D = E[('U', 'U')], E[('U', 'O')], E[('O', 'U')], E[('O', 'O')]
    rr = rho_dec(a, b, d, Decimal(p) / q)
    mu = Fraction(int(rr * 10 ** 12) + 3, 10 ** 12)
    good = mu >= A and mu >= D and (mu - A) * (mu - D) >= B * C
    ok(good, f"OM upper cert {a,b,d}")
    U = (Decimal(mu.numerator) / Decimal(mu.denominator)).ln() / LN2
    return U, r.ln() / LN2


def lower_cert(a, b, d, R):
    """Independent excursion-count lower bound."""
    va, vb = v_of(a, b, d)
    th, r = rho_min(a, b, d)
    th, r = float(th), float(r)
    best = None
    if va == 2 and vb == 2:   # T3
        al, be = Fraction(a, 4), Fraction(b, 4)
        p0, pa, pb = 2 ** -th / r, float(al) ** th / r ** 2, float(be) ** th / r ** 2
        for d0 in range(-60, 61, 2):
            for da in (-1, 0, 1):
                n0, na = round(p0 * R) + d0, round(pa * R) + da
                nb = R - n0 - na
                if min(n0, na, nb) < 0:
                    continue
                if Fraction(1, 2) ** n0 * al ** na * be ** nb <= 1:
                    continue
                N = math.factorial(R) // (math.factorial(n0) * math.factorial(na) * math.factorial(nb))
                m = n0 + 2 * na + 2 * nb
                L = Fraction((N // R).bit_length() - 1, m)
                if best is None or L > best[0]:
                    best = (L, m)
    else:                     # T2: loop (valuation-1 branch), ret (valuation-2 branch)
        if va == 1:
            loop, ret = Fraction(a, 2), Fraction(b, 4)
        else:
            loop, ret = Fraction(b, 2), Fraction(a, 4)
        assert loop > 1
        sig = float(loop) ** th / r
        p0 = 2 ** -th / r
        Po = float(ret) ** th / r ** 2 / (1 - sig)
        for d0 in range(-60, 61, 2):
            n0 = round(p0 / (p0 + Po) * R) + d0
            N1 = R - n0
            for dJ in range(-3, 4):
                J = round(N1 * sig / (1 - sig)) + dJ
                if Fraction(1, 2) ** n0 * loop ** J * ret ** N1 <= 1:
                    continue
                N = comb(R, N1) * comb(J + N1 - 1, N1 - 1)
                m = n0 + 2 * N1 + J
                L = Fraction((N // R).bit_length() - 1, m)
                if best is None or L > best[0]:
                    best = (L, m)
    return best


claims = {(5, 1, 1): ("0.936275", "0.936852"), (7, 1, 1): ("0.752601", "0.753484"),
          (3, 5, 1): ("0.662525", "0.663347"), (5, 7, 3): ("0.966468", "0.967365")}
for mem, (lo, hi) in claims.items():
    U, exact = upper_cert(*mem)
    L, m = lower_cert(*mem, 24000)
    Ld = Decimal(L.numerator) / Decimal(L.denominator)
    print("  %s: my L=%.7f U=%.7f  log2 rho*=%.9f  claimed [%s, %s]" % (mem, Ld, U, exact, lo, hi))
    ok(U <= Decimal(hi), f"OM upper {mem}")
    ok(Ld >= Decimal(lo) - Decimal("0.00002"), f"OM lower {mem}")
    ok(Decimal(lo) <= exact <= Decimal(hi), f"OM interval contains rho* {mem}")
# symmetric members have identical move multisets
for x, y in [((5, 1, 1), (1, 5, 3)), ((5, 1, 1), (5, 1, 9)), ((7, 1, 1), (1, 7, 3)),
             ((3, 5, 1), (5, 3, 3)), ((5, 7, 3), (7, 5, 1)), ((5, 1, 3), (1, 5, 1))]:
    mx, my = moves(*x), moves(*y)
    ok(sorted(map(str, mx['O'])) == sorted(map(str, my['O'])), f"OM sym {x} {y}")
# split5_3 and split5_1 Omega4 exponents
U53, ex53 = upper_cert(5, 1, 3)
ok(U53 <= Decimal("0.58069"), f"OM Omega4 split5_3 {U53}")
U51, _ = upper_cert(5, 1, 1)
ok(U51 <= Decimal("0.93686"), f"OM Omega4 split5_1 {U51}")


# exact loop-word DP: Z_m = #U->U words with all prefix products >= 1; dim >= log2(Z_m)/m
def loopdp(a, b, d, m):
    mv = moves(a, b, d)
    cur = {('U', Fraction(1)): 1}
    for _ in range(m):
        nxt = {}
        for (s, P), cc in cur.items():
            for t, sl in mv[s]:
                P2 = P * sl
                if P2 >= 1:
                    nxt[(t, P2)] = nxt.get((t, P2), 0) + cc
        cur = nxt
    return sum(cc for (s, P), cc in cur.items() if s == 'U')


for mem in [(5, 1, 3), (5, 1, 1)]:
    Z = loopdp(*mem, 160)
    Lb = (Z.bit_length() - 1) / 160
    print("  loop DP m=160 %s: log2 Z/m >= %.4f" % (mem, Lb))
    ok(Lb > 0, "OM dp")
# the split5_1 DP lower bound must exceed split5_3's exact dimension (separation is real)
ok((loopdp(5, 1, 1, 160).bit_length() - 1) / 160 > 0.5806842, "OM separation")


# excursion-level cycle lemma, exhaustive small check (T2 alphabet with J self-loops)
def check_cycle_lemma(n0, N1, J, loop, ret):
    import itertools
    total = 0
    good = 0
    letters = ['E'] * n0 + ['O'] * N1
    for perm in set(itertools.permutations(letters)):
        # distribute J loops among the N1 odd excursions
        for comp in itertools.combinations_with_replacement(range(N1), J):
            js = [0] * N1
            for i in comp:
                js[i] += 1
            total += 1
            P, ok_ = Fraction(1), True
            oi = 0
            for L_ in perm:
                if L_ == 'E':
                    P /= 2
                else:
                    P *= loop ** js[oi] * ret
                    oi += 1
                if P <= 1:
                    ok_ = False
                    break
            good += ok_
    return total, good


for (n0, N1, J) in [(2, 2, 5), (3, 2, 6), (1, 3, 6), (2, 3, 7)]:
    loop, ret = Fraction(5, 2), Fraction(1, 4)
    if Fraction(1, 2) ** n0 * loop ** J * ret ** N1 > 1:
        tot, gd = check_cycle_lemma(n0, N1, J, loop, ret)
        ok(tot == comb(n0 + N1, N1) * comb(J + N1 - 1, N1 - 1), "OM count formula")
        ok(gd * (n0 + N1) >= tot, f"OM cycle lemma {n0,N1,J}: {gd}/{tot}")
print("OM done")

# coding: digit word depends only on n mod 2^J and is a bijection (independent re-run)
for (a, b, d) in [(5, 1, 3), (5, 1, 1), (7, 1, 1), (3, 7, 1), (1, 5, 1)]:
    va, vb = v_of(a, b, d)
    J = 10
    words = set()
    for r in range(2 ** J):
        res = []
        for n in (r + 2 ** J, r + 2 ** J * (1 + rng.getrandbits(64))):
            x, st, w, P = n, 'U', [], Fraction(1)
            for _ in range(J):
                if st == 'U':
                    if x % 2 == 0:
                        x //= 2; w.append(0); P /= 2
                    else:
                        st = 'O'; w.append(1)
                else:
                    if x % 4 == 1:
                        x = (a * x + d) // 2 ** va; P *= Fraction(a, 2 ** va); w.append(0)
                        st = 'U' if va == 2 else 'O'
                    else:
                        x = (b * x + d) // 2 ** vb; P *= Fraction(b, 2 ** vb); w.append(1)
                        st = 'U' if vb == 2 else 'O'
            res.append((tuple(w), x, P, n))
        ok(res[0][0] == res[1][0], "OM coding word")
        ok(res[1][1] - res[0][1] == res[0][2] * (res[1][3] - res[0][3]), "OM coding affine")
        words.add(res[0][0])
    ok(len(words) == 2 ** J, "OM coding bijection")
print("OM coding done")

# ============================== Z3 =========================================
T = SPLIT(5, 1, 3)
G = SPLIT(1, 5, 1)
for m in list(range(1, 20000)) + [rng.getrandbits(256) + 1 for _ in range(200)]:
    ok(T(3 * m) == 3 * G(m), "Z3 conj")
    ok((T(m) % 3 == 0) == (m % 3 == 0), "Z3 inv")
print("Z3 done")

if FAIL:
    print(len(FAIL), "FAILURES")
    sys.exit(1)
print("REFEREE ALL PASS")
