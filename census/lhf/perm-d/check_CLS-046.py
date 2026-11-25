"""check_CLS-046: computational parts of CLS-046.md (perm_d_s3).

1. D agrees with census/systems.py and has the stated inverse.
2. Lemma A (letters mod m'): O_3 o O_1^{-1} is translation by 1/4 (exact rational identity).
3. Lemma B: for b <= 5 the words of length b give a bijection onto Z/5^b via T^b(C_s) mod 5^b.
4. Corroboration of the theorem: residue graph of D and of D^{-1} is strongly connected
   for every modulus M <= 400.
5. Exhaustive cycle enumeration: every cycle of length <= 11 is one of
   {1}, {2,5,3}, {6,15,9}, {26,65,41}.
Exit 0 iff all pass. Exact integer / Fraction arithmetic only.
"""
import os
import sys
from fractions import Fraction as F
from itertools import product

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from systems import get  # noqa: E402


def D(n):
    if n % 2 == 0:
        return 5 * n // 2
    q, r = divmod(n, 8)
    return 5 * q + (r + 1) // 2


def Dinv(n):
    q, r = divmod(n, 5)
    return 2 * q if r == 0 else 8 * q + 2 * r - 1


# letters: (residue, modulus, s, e) meaning T(n) = (5n + s) / 2^e on n = residue mod modulus
LET = [(0, 2, 0, 1), (1, 8, 3, 3), (3, 8, 1, 3), (5, 8, -1, 3), (7, 8, -3, 3)]

ok = True

# 1
step = get("perm_d_s3")["step"]
c1 = all(step(n) == D(n) for n in range(1, 100001)) and \
    all(Dinv(D(n)) == n and D(Dinv(n)) == n for n in range(-50000, 50001))
for (r, mod, s, e) in LET:
    c1 &= all(D(n) * 2 ** e == 5 * n + s for n in range(r - 800, 800, mod))
print("1 map/inverse/letters:", c1)
ok &= c1

# 2
z = F(7, 13)  # generic symbolic stand-in; identity is affine so check two points
def O(s, y): return (5 * y + s) / F(8)
def Oinv(s, y): return (8 * y - s) / F(5)
c2 = all(O(3, Oinv(1, y)) == y + F(1, 4) for y in (F(0), F(1), z))
print("2 O_3 o O_1^-1 = +1/4:", c2)
ok &= c2


# 3
def word_class(w):
    """Return (n_w, 2^e): the class of integers with itinerary w."""
    # backward construction: C_{l s'} = {n in dom(l): T(n) in C_s'}
    base, mod = 0, 1
    for (r, m, s, e) in reversed(w):
        # n = r + m*u, T(n) = (5n+s)/2^e must be = base mod `mod`
        t0 = (5 * r + s) // 2 ** e          # T(r)
        # T(r + m u) = t0 + 5u (since m = 2^e)
        u = ((base - t0) * pow(5, -1, mod)) % mod if mod > 1 else 0
        base, mod = r + m * u, m * mod
    return base, mod


c3 = True
for b in range(1, 6):
    seen = set()
    for w in product(LET, repeat=b):
        n0, md = word_class(w)
        m = n0
        for (r, mm, s, e) in w:
            c3 &= (m % mm == r)
            m = D(m)
        # T^b(n0 + md*t) = m + 5^b t
        m2 = n0 + md
        for _ in w:
            m2 = D(m2)
        c3 &= (m2 - m == 5 ** b)
        seen.add(m % 5 ** b)
    c3 &= len(seen) == 5 ** b
print("3 suffix words <-> Z/5^b, b<=5:", c3)
ok &= c3


# 4
def strongly(M, f, per):
    succ = [set() for _ in range(M)]
    for n in range(per * M, 2 * per * M):
        succ[n % M].add(f(n) % M)
    pred = [set() for _ in range(M)]
    for u in range(M):
        for v in succ[u]:
            pred[v].add(u)

    def reach(adj):
        seen = {0}
        st = [0]
        while st:
            u = st.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    st.append(v)
        return len(seen)
    return reach(succ) == M and reach(pred) == M


c4 = all(strongly(M, D, 8) and strongly(M, Dinv, 5) for M in range(1, 401))
print("4 residue graphs strongly connected, M<=400:", c4)
ok &= c4

# 5  T^k(n) = (5^k n + b) / 2^E on C_w; cycle point n = b / (2^E - 5^k)
K = 11
found = set()
stack = [(0, 1, 0, 0, ())]  # k, 5^k, b, E, word
while stack:
    k, A, b, E, w = stack.pop()
    if k > 0:
        den = 2 ** E - A
        if b % den == 0 and b // den >= 1:
            n = b // den
            m = n
            good = True
            for (r, mm, s, e) in w:
                if m % mm != r:
                    good = False
                    break
                m = D(m)
            if good and m == n:
                cyc = [n]
                x = D(n)
                while x != n:
                    cyc.append(x)
                    x = D(x)
                found.add(min(cyc))
    if k < K:
        for l in LET:
            r, mm, s, e = l
            # (5(A n + b)/2^E + s)/2^e = (5A n + 5b + s 2^E) / 2^(E+e)
            stack.append((k + 1, 5 * A, 5 * b + s * 2 ** E, E + e, w + (l,)))
c5 = sorted(found) == [1, 2, 6, 26]
print("5 cycles of length <= %d have minima" % K, sorted(found), c5)
ok &= c5

print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
