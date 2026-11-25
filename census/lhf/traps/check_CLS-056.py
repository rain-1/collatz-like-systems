"""CLS-056 (yah_avoid57): computational part of CLS-056.md. Exact integers only.

(1) T^i(n) = 5 mod 8 iff T-parity bits i..i+2 are 100; = 7 mod 8 iff 111 (residues mod 8).
(2) g(m) = #words of length m starting with 1 with no factor 100 or 111: g(1..3) = 1,2,2 and
    g(m) = g(m-2) + g(m-3) for 4 <= m <= 18 (brute force); a_L = #such words of any start
    = 1 + sum_{m=1..L} g(m) (brute force L <= 18).
(3) #{n <= X : C-trajectory of n meets neither 5 nor 7 mod 8} <= 2 a_L, L = floor(log2 X),
    checked by direct simulation for X = 2^k, k <= 20 (all such n < 2^20+1 reach 1).
(4) The census step avoid({5,7}) agrees with the stated map.
(5) Odd values of the C-trajectory = odd values of the T-trajectory (n < 2^16, until 1).
"""
import sys, os
from itertools import product
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'round2', 'literature'))
from systems import get

def T(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def word(n, L):
    w = []
    for _ in range(L):
        w.append(n & 1); n = T(n)
    return tuple(w)

ok = True
want = {5: (1, 0, 0), 7: (1, 1, 1)}
for r in range(8):
    for k in range(50):
        w = word(r + 8 * k, 3)
        if (w in want.values()) != (r in want) or (r in want and w != want[r]):
            ok = False; print("class/word fail", r)
BAD = {(1, 0, 0), (1, 1, 1)}
def free(w):
    return all(tuple(w[i:i + 3]) not in BAD for i in range(len(w) - 2))
g = [0] + [sum(free(w) for w in product((0, 1), repeat=m) if w[0] == 1) for m in range(1, 19)]
if g[1:4] != [1, 2, 2]: ok = False; print("g base fail", g[:4])
for m in range(4, 19):
    if g[m] != g[m - 2] + g[m - 3]: ok = False; print("g recurrence fail", m)
a = [sum(free(w) for w in product((0, 1), repeat=L)) for L in range(19)]
for L in range(19):
    if a[L] != 1 + sum(g[1:L + 1]): ok = False; print("a_L fail", L)
print("g:", g[1:15]); print("a:", a[:15])
K = 20
while len(g) <= K: g.append(g[-2] + g[-3])
a = [1 + sum(g[1:L + 1]) for L in range(K + 1)]
step = get('yah_avoid57')['step']
for n in range(1, 5000):
    exp = 1 if n % 8 in (5, 7) else (n // 2 if n % 2 == 0 else 3 * n + 1)
    if step(n) != exp: ok = False; print("step mismatch", n)
for n in range(1, 2 ** 16):
    c, oc = n, []
    while c != 1:
        if c % 2: oc.append(c)
        c = c // 2 if c % 2 == 0 else 3 * c + 1
    t, ot = n, []
    while t != 1:
        if t % 2: ot.append(t)
        t = T(t)
    if oc != ot: ok = False; print("odd values differ", n)
cnt, counts = 0, {}
for n in range(1, 2 ** K + 1):
    c, meet = n, False
    while c != 1:
        if c % 8 in (5, 7): meet = True; break
        c = c // 2 if c % 2 == 0 else 3 * c + 1
    if not meet: cnt += 1
    if n & (n - 1) == 0: counts[n.bit_length() - 1] = cnt
for k in range(1, K + 1):
    if counts[k] > 2 * a[k]: ok = False; print("bound fails", k)
print("avoiding counts up to 2^k:", [counts[k] for k in range(1, K + 1)])
print("2*a_k                    :", [2 * a[k] for k in range(1, K + 1)])
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
