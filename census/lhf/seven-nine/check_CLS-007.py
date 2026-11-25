"""CLS-007 (m3_e). Computational part of CLS-007.md. Exact integers. Exit 0 iff all pass.
(i) step agrees with census; (ii) Theorem A sanity: residue graph mod M (3 | M <= 1000):
class of 1 reachable from every class; (iii) Theorem C: the only cycles with <= 1000 terms
not divisible by 3 are {1,9,3} and the 14-cycle through 4."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sevnine_lib as S
ok = S.run_standard('M3E')
f = S.STEPS['M3E']
c = [4]
while True:
    c.append(f(c[-1]))
    if c[-1] == 4: break
ok &= len(c) - 1 == 14 and sum(1 for x in c[:-1] if x % 3) == 5
ok &= f(1) == 9 and f(9) == 3 and f(3) == 1
sys.exit(0 if ok else 1)
