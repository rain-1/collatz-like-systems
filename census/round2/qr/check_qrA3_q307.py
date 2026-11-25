import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qrlib import famA, check_coset_system
q = 307
CUBES = {pow(x, 3, q) for x in range(1, q)}
# cubic character chi(n) = n^((q-1)/3) mod q, a cube root of unity
lab = {pow(1, 102, q): 1, pow(5, 102, q): 5, pow(7, 102, q): 7}
assert len(lab) == 3 and q == 8**2 + 27 * 3**2   # 307 = x^2+27y^2: 2 is a cube mod 307
def rule(n):
    return 307 if n % q == 0 else lab[pow(n, 102, q)]
ok = check_coset_system("qrA3_q307", famA(q, 3), q, [2, 3], CUBES, rule, q, 200000)
sys.exit(0 if ok else 1)
