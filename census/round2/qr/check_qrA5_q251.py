import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qrlib import famA, check_coset_system
q = 251
FIFTHS = {pow(x, 5, q) for x in range(1, q)}
lab = {pow(r, 50, q): r for r in (1, 3, 7, 9, 21)}
assert len(lab) == 5
def rule(n):
    return 251 if n % q == 0 else lab[pow(n, 50, q)]
ok = check_coset_system("qrA5_q251", famA(q, 5), q, [2, 5], FIFTHS, rule, q, 200000)
sys.exit(0 if ok else 1)
