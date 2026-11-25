import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qrlib import famC, check_coset_system
q = 311
QR = {x * x % q for x in range(1, q)}
def rule(n):
    if n % q == 0: return 311
    return 3 if pow(n, 155, q) == 1 else 11
ok = check_coset_system("qrC_q311", famC(q), q, [2, 3, 5], QR, rule, q, 200000)
sys.exit(0 if ok else 1)
