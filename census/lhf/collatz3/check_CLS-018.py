"""check_CLS-018: 3n-1.  Exact integers.  Exit 0 iff all computational parts pass.
See CLS-018.md for what is proved and which part is computational."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as c

d = -1
ok, cyc = c.run_family(d)
ok &= c.report("1-cycle list equals the one stated in CLS-018.md", cyc == [(1, 0, 1), (2, 1, 5)])
ok &= c.report("Lemma O (2-adic obstruction) sampled for j<=8", c.check_two_adic_obstruction(d, 8))
C = c.F(1)
ok &= c.report("F_-1(n) = -C(-n) for 1<=n<=2e4 (conjugacy to 3x+1 on negatives)",
               all(c.F(-1)(n) == -C(-n) for n in range(1, 20001)))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
