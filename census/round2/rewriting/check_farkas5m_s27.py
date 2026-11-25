"""farkas5m_s27: n=3 mod 5 -> (n+2)/5; else even -> n/2; else (5n-3)/2.
Exit 0 iff: seed fate, the block lemma for all odd n <= 2*10^5 (not 3 mod 5),
descent for all 1 < n <= 2*10^5, and the descent tree's exceptional set is
exactly 8 classes (the 2-adic neighbourhood of 1) at each tested modulus."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import mod_table, descent_tree, density  # noqa: E402
from fractions import Fraction  # noqa: E402

TAB = (10, [(1, 0, 2), (5, -3, 2), (1, 0, 2), (1, 2, 5), (1, 0, 2),
            (5, -3, 2), (1, 0, 2), (5, -3, 2), (1, 2, 5), (5, -3, 2)])
T = mod_table(*TAB)


def T_direct(n):
    if n % 5 == 3:
        return (n + 2) // 5
    return n // 2 if n % 2 == 0 else (5 * n - 3) // 2


N = 200000
for n in range(1, N + 1):
    assert T(n) == T_direct(n)
# seed
x, path = 27, [27]
while x != 1:
    x = T(x)
    path.append(x)
assert path == [27, 66, 33, 7, 16, 8, 2, 1], path
assert T(1) == 1
# block lemma: odd n >= 3, n != 3 mod 5, n - 1 = 2^a b  =>  T^(2a+1)(n) = (b+1)/2
for n in range(3, N + 1, 2):
    if n % 5 == 3:
        continue
    a, b = 0, n - 1
    while b % 2 == 0:
        a, b = a + 1, b // 2
    x = n
    for _ in range(2 * a + 1):
        x = T(x)
    assert x == (b + 1) // 2 < n, n
# descent for every 1 < n <= N
for n in range(2, N + 1):
    x = T(n)
    k = 1
    while x >= n:
        x = T(x)
        k += 1
        assert k < 10**4
# exceptional set: 8 classes, density 8 / (5 * 2^K) at modulus 5 * 2^K, all = 1 mod 2^K
for K in (6, 10, 14, 18):
    o, closed, small = descent_tree(TAB, 5 * 2**K, small_cap=10000)
    assert len(o) == 8 and density(o) == Fraction(8, 5 * 2**K), (K, len(o))
    assert all(Q == 5 * 2**K and r % 2**(K - 2) == 1 for Q, r in o), o
    assert small == []
print("farkas5m_s27: PASS (seed 27 -> 1 in 7 steps; block lemma and descent to 2e5; "
      "E = 8 classes around the 2-adic point 1 at moduli 5*2^K, K=6..18)")
