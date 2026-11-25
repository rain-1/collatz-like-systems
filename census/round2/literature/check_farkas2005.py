"""check_farkas2005: exact-integer checks for the Farkas map G (systems.py).
1. Conjugacy F'(2m-1) = 2G(m)-1 for all m <= 10^6 (F' = Farkas's original map).
2. Round-1 catalog map farkas_s27 (census/systems.py) satisfies R(n) = G(n+1)-1, n >= 2.
3. Block lemma: for even m = 2^a c (c odd), m != 2 mod 3, G^(2a+1)(m) = (c+1)/2,
   with the exact intermediate values of the proof, for all such m <= 10^6.
4. Every 1 < m <= 10^6 descends below itself (sanity; the proof covers all m).
5. FATE of the seed 14 (x = 27 in Farkas's coordinates)."""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from systems import farkas_G as G, farkas_Fprime as Fp
sys.path.insert(0, os.path.join(here, "..", ".."))
import importlib.util
spec = importlib.util.spec_from_file_location("cat1", os.path.join(here, "..", "..", "systems.py"))
cat1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(cat1)
R = cat1.get("farkas_s27")["step"]
N = 10**6
for m in range(1, N + 1):
    assert Fp(2 * m - 1) == 2 * G(m) - 1, m
for n in range(2, N + 1):
    assert R(n) == G(n + 1) - 1, n
assert G(1) == 1
for m in range(2, N + 1, 2):
    if m % 3 == 2:
        continue
    a, c = 0, m
    while c % 2 == 0:
        a += 1; c //= 2
    x = m
    for j in range(1, a + 1):          # a steps of 3x/2
        x = G(x); assert x == 3**j * 2**(a - j) * c, (m, j)
    x = G(x); assert x == (3**a * c + 1) // 2   # odd step (m+1)/2 on 3^a c
    for j in range(a - 1, -1, -1):     # a steps of (x+1)/3
        assert x % 3 == 2
        x = G(x); assert x == (3**j * c + 1) // 2, (m, j)
    assert x < m
for m in range(2, N + 1):
    x, t = G(m), 0
    while x >= m:
        x = G(x); t += 1
        assert t < 10**4, m
orb = [14]
while orb[-1] != 1:
    orb.append(G(orb[-1]))
print("farkas2005 OK; seed 14 orbit:", orb)
