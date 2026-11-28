"""z3 search for type-(b) (Theorem-H-provable, with an isolated expanding cycle) members of
the S-family  even n -> n/2;  odd n -> a n + 1 (n mod 2^m in S) or n + 1.
Usage: python sat_sfam_H.py a m maxsol.   Prints 'unsat' if none exists (search tool; see
sat_typeH.py for the encoding and why it is complete)."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tblib as TB
from sat_typeH import search

a, m, maxsol = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
Q = 2 ** m
opts = [[(1, 0, 2)] if r % 2 == 0 else [(a, 1, 1), (1, 1, 1)] for r in range(Q)]
t = time.time()
sols, res = search(2, m, opts, maxsol=maxsol, timeout_ms=1300000)
print("a", a, "m", m, "solver:", res, "solutions:", len(sols), f"{time.time() - t:.1f}s")
for ch, C in sols:
    tab = [opts[r][ch[r]] for r in range(Q)]
    S = [r for r in range(Q) if r % 2 and ch[r] == 0]
    P = TB.prove_H(2, m, tab)
    print(S, C, P and P["verdict"], P and P["cycles"])
