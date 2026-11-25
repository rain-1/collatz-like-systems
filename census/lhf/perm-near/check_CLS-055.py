"""swT9_s8 (CLS-055): exact checks.
1. Q (local) equals the catalog step on 1..2e5; Q is affine on classes mod 27.
2. The pieces n = 0, 1, 2 (mod 27) of Q coincide with T (so for 3 | K fails, but
   for 3 not dividing K, Q's residue graph contains T's), used in the proof.
3. Lemma A computationally: Q's residue graph mod K is strongly connected for
   every K <= 1200 and every K = 2^a 3^b <= 300000.
4. DFA certificates: none with <= 6 states base 2, <= 4 base 3, <= 3 base 6,
   MSD- and LSD-first (exhaustive backtracking with symmetry breaking).
   Positive control: the same search finds certificates for n -> 3n, n -> 2n.
5. No return of 8 within 1e5 steps (evidence only).
"""
import sys
import time
from _lib import catalog, Q, T, affine_on_classes, strongly_connected, dfa_search

t0 = time.time()
ok = True
Qc = catalog("swT9_s8")["step"]
ok &= all(Qc(n) == Q(n) for n in range(1, 200000))
ok &= affine_on_classes(Q, 27)
# pieces 0,1,2 mod 27 equal T (on a long range; both sides affine on these classes)
ok &= all(Q(27 * t + r) == T(27 * t + r) for r in (0, 1, 2) for t in range(0, 5000) if 27 * t + r > 0)
print("basic", ok)

bad = [K for K in range(1, 1201) if not strongly_connected(Q, K, 27)]
Ks = sorted(2 ** a * 3 ** b for a in range(20) for b in range(13) if 1200 < 2 ** a * 3 ** b <= 300000)
bad += [K for K in Ks if not strongly_connected(Q, K, 27)]
print("non-strongly-connected moduli:", bad, round(time.time() - t0, 1), "s")
ok &= not bad

for b, smax in ((2, 6), (3, 4), (6, 3)):
    for msd in (True, False):
        r = dfa_search(Q, 8, b, smax, msd)
        print("DFA base", b, "states <=", smax, "MSD" if msd else "LSD", "found" if r else "none")
        ok &= r is None
ok &= dfa_search(lambda n: 3 * n, 8, 3, 2, False) is not None
ok &= dfa_search(lambda n: 2 * n, 8, 2, 6, False) is not None

x = 8
for i in range(100000):
    x = Q(x)
    if x == 8:
        ok = False
        print("returned at", i + 1)
        break
print("no return in 1e5 steps; bits", x.bit_length(), round(time.time() - t0, 1), "s")
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
