"""CLS-036 (9n+1). Computational part of CLS-036.md. Exact integers. Exit 0 iff all pass.
(i) step agrees with census; (ii) Theorem A sanity: residue graph mod M (M even <= 1000):
class of 1 reachable from every class; (iii) Theorem C: 9n+1 has NO cycle with <= 1000 odd terms."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sevnine_lib as S
ok = S.run_standard('P9')
f = S.STEPS['P9']
ok &= f(1) == 10 and f(10) == 5   # 5 lies on the orbit of 1
sys.exit(0 if ok else 1)
