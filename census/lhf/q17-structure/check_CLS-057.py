"""Independent check for CLS-057 (qrA3_q17).

Re-implements, from scratch and with exact integers, the constructive core of the
nonautomaticity proof in census/round2/qr/qrA3_q17.md:
  (1) descent on n > 17, the cycle table, basin(2n)=basin(3n)=basin(n);
  (2) the PROGRESSION LEMMA, run as an algorithm: for a unit x (mod 17), a modulus M
      and a target cycle b in {1,5}, build x' = x (mod M), x' > bound, with basin(x') = b,
      exactly as the proof prescribes, then verify basin(x') by forward iteration;
  (3) the section identity f(D(p^j n + d_j) + r) = f(D n + r_j) used in the kernel step.
Exit 0 iff all pass.
"""
import random, sys
from math import gcd

def T(n):
    return n // 2 if n % 2 == 0 else (n + 17 * (n % 3)) // 3

def basin(n):
    while n > 17:
        n = T(n)
    seen = []
    while n not in seen:
        seen.append(n); n = T(n)
    return min(seen[seen.index(n):])           # cycle representative 1, 5 or 17

ok = True
# (1) finite table and descent
ok &= all(1 <= T(n) <= 17 for n in range(1, 18))
ok &= {basin(n) for n in range(1, 18)} == {1, 5, 17}
ok &= all(T(n) < n for n in range(18, 200000))
N = 300000
B = [0] + [basin(n) for n in range(1, N + 1)]
ok &= all(B[2 * n] == B[n] for n in range(1, N // 2 + 1))
ok &= all(B[3 * n] == B[n] for n in range(1, N // 3 + 1))
ok &= all((B[n] == 17) == (n % 17 == 0) for n in range(1, N + 1))

# (2) progression lemma as an algorithm
def path_to_cycle(x):
    """forward steps from x until 1 or 5; returns (c, steps) with steps as ('h',) or ('o', d)"""
    steps = []
    while x not in (1, 5):
        if x % 2 == 0: steps.append(('h',))
        else: steps.append(('o', x % 3))
        x = T(x)
    return x, steps

def reverse(steps, y):
    for s in reversed(steps):
        y = 2 * y if s[0] == 'h' else 3 * y - 17 * s[1]
        assert y > 0
    return y

def ord_mod(a, m):
    if m == 1: return 1
    k, v = 1, a % m
    while v != 1: v = v * a % m; k += 1
    return k

def seed_word(b, c, Q, big):
    """odd z in basin b, z = c (mod Q), z > big, via predecessors L(y)=3y, R(y)=3y-34"""
    e = ord_mod(3, Q)
    m = e
    while b * 3 ** m <= big: m += e
    z0 = b * 3 ** m                                  # = b (mod Q), basin b
    # BFS over residues mod Q
    prev = {z0 % Q: None}; frontier = [z0]; found = z0 if (z0 - c) % Q == 0 else None
    while found is None:
        nxt = []
        for y in frontier:
            for z in (3 * y, 3 * y - 34):
                if z % Q not in prev:
                    prev[z % Q] = y; nxt.append(z)
                    if (z - c) % Q == 0: found = z; break
            if found is not None: break
        assert nxt or found is not None, "residue unreachable"
        frontier = nxt
    return found

def construct(x, M, b):
    c, steps = path_to_cycle(x)
    u = v = 0; Q = M
    while Q % 2 == 0: Q //= 2; u += 1
    while Q % 3 == 0: Q //= 3; v += 1
    z = seed_word(b, c, Q, 10 ** 6)
    assert z % 2 == 1 and (z - c) % Q == 0
    t = max(u, (v + 1) // 2)
    y = c + 18 ** t * (z - c)
    return reverse(steps, y)

rng = random.Random(51)
moduli = [1, 2, 3, 17, 34, 51, 72, 85, 175, 289, 4913 // 17 * 3, 2 ** 5 * 3 ** 3 * 17, 1001, 17 * 23 * 4]
trials = 0
for M in moduli:
    for _ in range(12):
        x = rng.randrange(1, 10 ** 6)
        if x % 17 == 0: continue
        for b in (1, 5):
            xp = construct(x, M, b)
            ok &= (xp - x) % M == 0 and xp > 10 ** 6 and basin(xp) == b
            trials += 1

# (3) section identity used in the kernel argument, bases k with partner p
for k, p in ((2, 3), (4, 3), (3, 2), (6, 2), (12, 2), (18, 2), (10, 2)):
    e = 3; W = p ** e
    D = k
    while D <= 2 * W: D *= k
    for d in range(W):
        r = (-D * d) % W
        if r % 17 == 0: r += W
        ok &= 0 <= r < D and r % 17 != 0
        for j in range(e + 1):
            dj = d % p ** j
            rj, rem = divmod(D * dj + r, p ** j)
            ok &= rem == 0 and 0 <= rj < D and (D % 17 != 0 or rj % 17 != 0)
            for n in range(1, 6):
                a = D * (p ** j * n + dj) + r
                if a <= N and D * n + rj <= N:
                    ok &= B[a] == B[D * n + rj]
print("progression-lemma constructions verified:", trials)
print("CLS-057 check", "OK" if ok else "FAILED")
sys.exit(0 if ok else 1)
