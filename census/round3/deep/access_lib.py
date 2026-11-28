"""Constructive form of the accessibility theorem for Sigma_d, gcd(d,6)=1 (basins.md, Theorem B2).

Given an odd y, a modulus M and a target x with I(x) = I(y) (same <2,3>-orbit mod d),
construct an integer w = x (mod M), w large, whose Sigma_d-orbit passes through an
ancestor of y (so w merges with y).  Every step of the proof is executed literally,
so a successful run (verified by forward iteration) tests the proof's finite content.
"""
from math import gcd
from collections import deque
from basins_lib import sigma_step


def v_p(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def ord_mod(g, Q):
    if Q == 1:
        return 1
    k, x = 1, g % Q
    while x != 1:
        x = x * g % Q
        k += 1
    return k


def L(h, z, d):          # inverse of the n+d branch followed by h halvings
    return 2 ** h * z - d


def U(h, z, d):          # inverse of the 3n+d branch followed by h halvings
    num = 2 ** h * z - d
    assert num % 3 == 0
    return num // 3


def reaches(step, w, y, cap=10 ** 6):
    for _ in range(cap):
        if w == y:
            return True
        w = step(w)
    return False


def step1(d, z, Q, s, t, h_min):
    """Odd ancestor w of odd z (3 does not divide z) with w = r0 (mod Q) for a residue r0
    independent of (s, t), and w = t (mod 3^s).  Returns (w, r0)."""
    assert z % 2 == 1 and z % 3 != 0
    o = ord_mod(2, Q)
    k = v_p(o, 3)
    # h_0: 2^h z = 4d (mod 3^(k+1))
    m0 = 3 ** (k + 1)
    h0 = next(h for h in range(2, 2 + 2 * 3 ** k) if (pow(2, h, m0) * z - 4 * d) % m0 == 0)
    # r0 is the residue for any h = h0 (mod lcm(o, 2*3^k)); compute with h = h0 + big multiple
    mod = 3 ** (k + 1 + s)
    rhs = (4 * d + 3 ** (k + 1) * pow(4, -k, mod) * (t - d)) % mod
    period = 2 * 3 ** (k + s)          # 2 is a primitive root mod 3^j
    hs = [h for h in range(2, 2 + period) if (pow(2, h, mod) * z - rhs) % mod == 0]
    assert len(hs) == 1
    h1 = hs[0]
    assert (h1 - h0) % (2 * 3 ** k) == 0
    # combine h = h1 (mod period) and h = h0 (mod o)
    g = gcd(period, o)
    assert (h1 - h0) % g == 0
    lcm = period * o // g
    h = next(h for h in range(h1, h1 + lcm, period) if (h - h0) % o == 0)
    while h < h_min:
        h += lcm
    u = U(h, z, d)
    w = u
    for _ in range(k):
        w = U(2, w, d)
    assert w == d + 4 ** k * (2 ** h * z - 4 * d) // 3 ** (k + 1)
    assert (w - t) % 3 ** s == 0
    r0 = w % Q
    return w, r0


def residue_word(d, Q, r0, target):
    """BFS for a word in L2, L3, U2 (as residue maps mod Q) taking r0 to target."""
    i3 = pow(3, -1, Q) if Q > 1 else 0
    ops = {
        'L2': lambda r: (4 * r - d) % Q,
        'L3': lambda r: (8 * r - d) % Q,
        'U2': lambda r: (4 * r - d) * i3 % Q,
    }
    prev = {r0: None}
    dq = deque([r0])
    while dq:
        r = dq.popleft()
        if r == target % Q:
            word = []
            while prev[r] is not None:
                r, op = prev[r]
                word.append(op)
            return word[::-1]
        for name, f in ops.items():
            s = f(r)
            if s not in prev:
                prev[s] = (r, name)
                dq.append(s)
    return None


def odd_ancestor_with_residue(d, y, Q, S, target, h_min=40):
    """Odd ancestor c' of y with c' = target (mod Q) and (mod 3^S)."""
    z = y
    while z % 2 == 0:
        z //= 2          # forward iterate of y: same merging class
    if z % 3 == 0:
        h = 2
        while L(h, z, d) <= 0:
            h += 1
        z = L(h, z, d)   # positive odd ancestor coprime to 3 (3 does not divide d)
    # first get r0 (independent of s,t)
    _, r0 = step1(d, z, Q, 0, 0, h_min)
    word = residue_word(d, Q, r0, target)
    if word is None:
        return None
    # pull the 3-adic requirement back through the word
    reqs = [(S, target % 3 ** S)]
    for op in reversed(word):
        Sc, t = reqs[-1]
        if op == 'L2':
            reqs.append((Sc, (t + d) * pow(4, -1, 3 ** Sc) % 3 ** Sc if Sc else 0))
        elif op == 'L3':
            reqs.append((Sc, (t + d) * pow(8, -1, 3 ** Sc) % 3 ** Sc if Sc else 0))
        else:
            m = 3 ** (Sc + 1)
            reqs.append((Sc + 1, (d + 3 * t) * pow(4, -1, m) % m))
    s0, t0 = reqs[-1]
    w, r = step1(d, z, Q, s0, t0, h_min)
    assert r == r0
    for op in word:
        if op == 'L2':
            w = L(2, w, d)
        elif op == 'L3':
            w = L(3, w, d)
        else:
            w = U(2, w, d)
    assert (w - target) % Q == 0 and (w - target) % 3 ** S == 0 and w % 2 == 1
    return w


def blocks_forward(d, x, u):
    """Follow u blocks (E: halve; A: (3x+d)/4; B: (x+d)/4) from x; return (c, l, k)."""
    c, l, k = x, 0, 0
    for _ in range(u):
        if c % 2 == 0:
            c //= 2
            l += 1
        elif (c + d) % 4 == 0:
            c = (c + d) // 4
            l += 2
        else:
            c = (3 * c + d) // 4
            l += 2
            k += 1
    return c, l, k


def construct(d, y, M, x, h_min=40):
    """w = x (mod M), w merges with y.  Requires I(x) = I(y) mod d."""
    u = v_p(M, 2)
    v = v_p(M, 3)
    Q = M // (2 ** u * 3 ** v)
    Q = Q * d // gcd(Q, d)          # enlarge so that d | Q
    c, l, k = blocks_forward(d, x, u)
    e = v_p(c, 2)
    codd = c >> e
    cp = odd_ancestor_with_residue(d, y, Q, v + k, codd, h_min)
    if cp is None:
        return None
    cp <<= e
    assert cp >= c and (cp - c) % 3 ** k == 0
    w = x + 2 ** l * ((cp - c) // 3 ** k)
    assert (w - x) % M == 0
    # w follows the same u blocks and lands on cp, an ancestor of y
    c2, l2, k2 = blocks_forward(d, w, u)
    assert (c2, l2, k2) == (cp, l, k)
    return w, cp
