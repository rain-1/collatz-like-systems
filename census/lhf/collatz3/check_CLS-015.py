"""check_CLS-015: 3n+5.  Exact integers.  Exit 0 iff all computational parts pass.
See CLS-015.md for what is proved and which part is computational."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as c

d = 5
ok, cyc = c.run_family(d)
ok &= c.report("1-cycle list equals the one stated in CLS-015.md", cyc == [(1, 1, 5), (1, 2, 1), (3, 2, 19)])
ok &= c.report("Lemma O (2-adic obstruction) sampled for j<=8", c.check_two_adic_obstruction(d, 8))
ok &= c.report("gcd(F(n),d)=gcd(n,d), n<=2e4", c.check_gcd_preserved(d, 20000))
ok &= c.report("F_d(g m) = g F_(d/g)(m) for g|d, m<=2e4", c.check_scaling(d, 20000))
# Lemma R: n coprime to d  <->  y = n/d under 3y+1 on Z_(2): F_d(n)/d = C(n/d)
from fractions import Fraction as Q
def C(y):
    return y / 2 if y.numerator % 2 == 0 else 3 * y + 1
ok &= c.report("F_d(n)/d == C(n/d) as rationals, n<=2e4 coprime to d",
               all(Q(c.F(d)(n), d) == C(Q(n, d)) for n in range(1, 20001) if n % d))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
