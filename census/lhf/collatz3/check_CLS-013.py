"""check_CLS-013: 3n+1.  Exact integers.  Exit 0 iff all computational parts pass.
See CLS-013.md for what is proved and which part is computational."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as c

d = 1
ok, cyc = c.run_family(d)
ok &= c.report("1-cycle list equals the one stated in CLS-013.md", cyc == [(1, 1, 1)])
ok &= c.report("Lemma O (2-adic obstruction) sampled for j<=8", c.check_two_adic_obstruction(d, 8))
r = c.ellison_sanity(1000)
ok &= c.report("numerical sanity of Ellison bound for 28<=K<=1000 (not a proof)", r[0])
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
