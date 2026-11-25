"""check_CLS-031: 6n+2.  Exact integers.  Exit 0 iff all computational parts pass.
See CLS-031.md for what is proved and which part is computational."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as c

d = 1
ok, cyc = c.run_family(d)
ok &= c.report("1-cycle list equals the one stated in CLS-031.md", cyc == [(1, 1, 1)])
ok &= c.report("Lemma O (2-adic obstruction) sampled for j<=8", c.check_two_adic_obstruction(d, 8))
G = lambda n: n // 2 if n % 2 == 0 else 6 * n + 2
ok &= c.report("6n+2: G(G(n)) = 3n+1 for odd n <= 2e5",
               all(G(G(n)) == 3 * n + 1 for n in range(1, 200001, 2)))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
