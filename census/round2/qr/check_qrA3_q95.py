import os, sys
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qrlib import famA, check_coset_system, jacobi
q = 95
KER = {x for x in range(1, q) if gcd(x, q) == 1 and jacobi(x, q) == 1}
# Neither Legendre factor alone is invariant: (2/5) = (2/19) = -1.
assert jacobi(2, 5) == -1 and jacobi(2, 19) == -1 and jacobi(3, 5) == -1 and jacobi(3, 19) == -1
def rule(n):
    d = gcd(n, q)
    if d == 95: return 95
    if d == 5: return 5
    if d == 19: return 19
    return 1 if jacobi(n, q) == 1 else 7
ok = check_coset_system("qrA3_q95", famA(q, 3), q, [2, 3], KER, rule, q, 200000)
sys.exit(0 if ok else 1)
