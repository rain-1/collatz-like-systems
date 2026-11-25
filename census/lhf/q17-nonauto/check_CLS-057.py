"""Independent check for CLS-057 (qrA3_q17): constructive witnesses for the
arithmetic half of the nonautomaticity proof, plus the finite identities.

Self-contained (does not import qrlib). Exact integers. Exit 0 iff all pass.
"""
import sys
from math import gcd
from collections import deque

def T(n):
    if n % 2 == 0:
        return n // 2
    c = n % 3
    return (n + 17 * c) // 3

def cyc_rep(n):
    """Run n to its cycle and return the representative 1, 5 or 17."""
    while n > 17:
        m = T(n)
        assert m < n          # descent above 17
        n = m
    while n not in (1, 5, 17):
        n = T(n)
        # the interval [1,17] is invariant (checked below), so this ends
    return n

ok = True
def need(cond, msg):
    global ok
    if not cond:
        ok = False
        print("FAIL:", msg)

# 1. Finite table, invariance of [1,17], cycles, descent bound.
need(all(1 <= T(n) <= 17 for n in range(1, 18)), "interval invariant")
need([T(n) for n in (1, 6, 3)] == [6, 3, 1], "cycle 1")
need([T(n) for n in (5, 13, 10)] == [13, 10, 5], "cycle 5")
need(T(17) == 17, "fixed 17")
seen = set()
for n in range(1, 18):
    x = n
    for _ in range(40):
        x = T(x)
    orb = []
    y = x
    while y not in orb:
        orb.append(y); y = T(y)
    seen.add(min(orb))
need(seen == {1, 5, 17}, "exactly three cycles in [1,17]")
need(all(T(n) < n for n in range(18, 200000)), "descent above 17")
need(all((T(n) % 17 == 0) == (n % 17 == 0) for n in range(1, 200000)), "17 | n iff 17 | T(n)")
need(pow(3, 5, 17) == 5, "3^5 = 5 mod 17")

# 2. Basin table and dilation identities f(2n) = f(3n) = f(n).
N = 1 << 20
B = bytearray(N + 1)
for n in range(1, N + 1):
    B[n] = n if n <= 17 and n in (1, 5, 17) else (B[T(n)] if T(n) < n else cyc_rep(n))
need(all(B[2 * n] == B[n] for n in range(1, N // 2 + 1)), "f(2n)=f(n)")
need(all(B[3 * n] == B[n] for n in range(1, N // 3 + 1)), "f(3n)=f(n)")

# 3. Inverse branches and the reverse lap (multiplier 18) at each cycle.
for y in range(1, 4001, 2):
    need(T(3 * y) == y, "L inverse")
    if 3 * y - 34 > 0:
        need(T(3 * y - 34) == y, "R inverse")
    for c in (1, 5):
        if y >= c:
            need(T(T(T(c + 18 * (y - c)))) == y, "lap")

# 4. Constructive witnesses (Lemma rough + Lemma lift + Theorem mix).
def word_b_to_c(b, c, Q):
    """BFS for a word in L(y)=3y, R(y)=3y-34 sending b to c modulo Q."""
    if Q == 1:
        return ""
    start, goal = b % Q, c % Q
    prev = {start: None}
    dq = deque([start])
    while dq:
        u = dq.popleft()
        if u == goal:
            break
        for ch, v in (("L", 3 * u % Q), ("R", (3 * u - 34) % Q)):
            if v not in prev:
                prev[v] = (u, ch); dq.append(v)
    assert goal in prev, (b, c, Q)
    w = []
    u = goal
    while prev[u] is not None:
        u, ch = prev[u]; w.append(ch)
    return "".join(reversed(w))

def apply_word(y, w):
    vals = []
    for ch in w:
        y = 3 * y if ch == "L" else 3 * y - 34
        vals.append(y)
    return y, vals

def ordmod(a, m):
    if m == 1:
        return 1
    k, x = 1, a % m
    while x != 1:
        x = x * a % m; k += 1
    return k

def rough(b, c, Q, extra=0):
    """Large odd z in basin b with z = c mod Q (Lemma rough), built explicitly."""
    w = word_b_to_c(b, c, Q)
    o = ordmod(3, Q)
    h = o * (1 + extra)
    while True:
        z, vals = apply_word(3 ** h * b, w)
        if all(v > 0 for v in vals) and z >= 17:
            return z
        h += o

def path_to_cycle(x):
    """Branch list from x to its representative c in {1,5}: ('e',) or ('o', d)."""
    br = []
    while x not in (1, 5):
        if x % 2 == 0:
            br.append(("e",))
        else:
            br.append(("o", x % 3))
        x = T(x)
    return br, x

def lift(br, y):
    """Reverse the branch list from endpoint y."""
    for b in reversed(br):
        y = 2 * y if b[0] == "e" else 3 * y - 17 * b[1]
    return y

def witness(x, M, b):
    br, c = path_to_cycle(x)
    u = v = 0
    m = M
    while m % 2 == 0: m //= 2; u += 1
    while m % 3 == 0: m //= 3; v += 1
    Q = m
    z = rough(b, c, Q)
    t = max(u, (v + 1) // 2)
    y = c + 18 ** t * (z - c)
    return lift(br, y)

count = 0
moduli = [1, 2, 3, 5, 7, 17, 18, 34, 51, 72, 85, 119, 175, 289, 2 * 3 * 17 * 5, 2**4 * 3**2 * 17, 4913, 1001]
for M in moduli:
    for x in list(range(1, 60)) + [97, 1234, 99991]:
        if x % 17 == 0:
            continue
        for b in (1, 5):
            w = witness(x, M, b)
            need(w % M == x % M, f"residue x={x} M={M}")
            need(cyc_rep(w) == b, f"basin x={x} M={M} b={b}")
            count += 1
print("constructive witnesses verified:", count)

# 5. Kernel-section identity used in Theorem kernel (sampled words, several bases).
for k, p in ((2, 3), (3, 2), (6, 2), (10, 2), (17, 2), (34, 2), (4, 3)):
    e = 4
    pe = p ** e
    D = k
    while D <= 2 * pe:
        D *= k
    for d in range(pe):
        r = (-D * d) % pe
        if r % 17 == 0:
            r += pe
        need(r % 17 != 0 and r < D, "choice of r")
        for j in range(e + 1):
            dj = d % p ** j
            q, rem = divmod(D * dj + r, p ** j)
            need(rem == 0 and 0 <= q < D, "r_j integral and in range")
            need(D % 17 != 0 or q % 17 != 0, "r_j unit")
            for n in range(0, 6):
                a = D * (p ** j * n + dj) + r
                bb = D * n + q
                if a <= N and bb <= N and a > 0 and bb > 0:
                    need(B[a] == B[bb], "section identity")

print("CLS-057", "OK" if ok else "FAILED")
sys.exit(0 if ok else 1)
