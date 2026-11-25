import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qrlib import famA, check_coset_system
q = 23
QR = {x * x % q for x in range(1, q)}
def rule(n):
    if n % q == 0: return 23
    return 1 if pow(n, (q - 1) // 2, q) == 1 else 5
ok = check_coset_system("qrA3_q23", famA(q, 3), q, [2, 3], QR, rule, q, 200000)
sys.exit(0 if ok else 1)
