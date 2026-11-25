"""check_CLS-014: 3n+3.  Exact integers.  Exit 0 iff all computational parts pass.
See CLS-014.md for what is proved and which part is computational."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as c

d = 3
ok, cyc = c.run_family(d)
ok &= c.report("1-cycle list equals the one stated in CLS-014.md", cyc == [(1, 1, 3)])
ok &= c.report("Lemma O (2-adic obstruction) sampled for j<=8", c.check_two_adic_obstruction(d, 8))
ok &= c.report("F_d(g m) = g F_(d/g)(m) for g|d, m<=2e4", c.check_scaling(d, 20000))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
