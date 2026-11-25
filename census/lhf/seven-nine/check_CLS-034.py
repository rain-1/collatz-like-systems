"""CLS-034 (7n+1). Computational part of CLS-034.md. Exact integers. Exit 0 iff all pass.
(i) step agrees with census; (ii) Theorem A sanity: residue graph mod M (M even <= 1000):
class of 1 reachable from every class; (iii) Theorem C: only cycle with <= 1000 odd terms is {1,8,4,2}."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sevnine_lib as S
ok = S.run_standard('P7')
sys.exit(0 if ok else 1)
