"""CLS-066 (up_ct3): computational part of the proofs in CLS-066.md. Exact integers only.

(1) Terras bijection: n mod 2^L <-> first L T-parity bits, and T^i(n) = 7 mod 8 iff bits i..i+2 are 111.
(2) t_L = #111-free words of length L satisfies t_L = t_{L-1}+t_{L-2}+t_{L-3} (brute force L <= 16).
(3) Upper bound: #{n <= X : n never trapped} <= 2 t_L, L = floor(log2 X), checked by direct
    simulation for X = 2^k, k <= 20 (every n < 2^21 either gets trapped or reaches 1 untrapped).
(4) Equivalence with YAH Conj 4.13 on n < 2^20: the up_ct3 orbit of n is untrapped and reaches (1 2)
    iff the C-trajectory (n/2, 3n+1) of n reaches 1 without meeting 7 mod 8; and trapped iff meets 7 mod 8.
(5) up_ct3 step from census/round2/upfrom1/systems.py agrees with the map used here.
"""
import sys, os
from itertools import product
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'round2', 'upfrom1'))
from systems import get

def T(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def word(n, L):
    w = []
    for _ in range(L):
        w.append(n & 1); n = T(n)
    return tuple(w)

ok = True
# (1)
for L in range(1, 15):
    ws = [word(r, L) for r in range(2 ** L)]
    if len(set(ws)) != 2 ** L: ok = False; print("bijection fails", L)
    for r in range(2 ** L):
        if word(r + 2 ** L, L) != ws[r]: ok = False; print("not periodic", L, r)
for r in range(8):
    if (word(r, 3) == (1, 1, 1)) != (r == 7): ok = False; print("7<->111 fails", r)
# (2)
def free(w, bad):
    return all(tuple(w[i:i + 3]) not in bad for i in range(len(w) - 2))
t = [sum(free(w, {(1, 1, 1)}) for w in product((0, 1), repeat=L)) for L in range(17)]
for L in range(3, 17):
    if t[L] != t[L - 1] + t[L - 2] + t[L - 3]: ok = False; print("recurrence fails", L)
print("t_L:", t[:12])
# (3),(4)
step = get('up_ct3')['step']
for n in range(1, 5000):
    exp = n + 8 if n % 8 == 7 else T(n)
    if step(n) != exp: ok = False; print("step mismatch", n)
K = 20
untrapped = 0
counts = {}
for n in range(1, 2 ** K + 1):
    m = n; trapped = False
    while True:
        if m % 8 == 7: trapped = True; break
        if m == 1: break
        m = T(m)
    # C-trajectory version
    c = n; c_meet = False
    while True:
        if c % 8 == 7: c_meet = True; break
        if c == 1: break
        c = c // 2 if c % 2 == 0 else 3 * c + 1
    if c_meet != trapped: ok = False; print("equivalence mismatch", n)
    if not trapped: untrapped += 1
    if n & (n - 1) == 0:
        counts[n.bit_length() - 1] = untrapped
while len(t) <= K:
    t.append(t[-1] + t[-2] + t[-3])
for k in range(1, K + 1):
    if counts[k] > 2 * t[k]: ok = False; print("bound fails", k)
print("untrapped counts up to 2^k:", [counts[k] for k in range(1, K + 1)])
print("2*t_k              :", [2 * t[k] for k in range(1, K + 1)])
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
