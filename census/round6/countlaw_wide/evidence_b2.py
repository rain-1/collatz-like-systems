"""EVIDENCE for hypothesis (B2) of Theorem G2: |R_n| rho*^{-n} n^{3/2} stays bounded above and below.

|R_n| exact (DP, big integers); rho* from cwconst.minimise (float).  Prints min and max of the normalised
ratio over n in [100, NMAX] and over the last third, per contracting system.
usage: python evidence_b2.py [NMAX]
"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cwlib import System, SYS
import cwconst

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
out = open(os.path.join(HERE, "data", "evidence_b2.txt"), "w")
for name in SYS:
    S = System(name)
    th, r = cwconst.minimise(S)
    if th == 0:
        continue
    sc = S.surv_counts(NMAX)
    lr = math.log(r)
    vals = []
    for n in range(100, NMAX + 1):
        x = sc[n]
        lx = math.log(x) if x < 10 ** 300 else (len(str(x)) - 1) * math.log(10) + math.log(int(str(x)[:15]) / 1e14)
        vals.append((n, lx - n * lr + 1.5 * math.log(n)))
    lo = min(v for _, v in vals)
    hi = max(v for _, v in vals)
    tail = [v for n, v in vals if n >= NMAX * 2 // 3]
    line = (f"{name:15s} log(|R_n| rho*^-n n^1.5) over n in [100,{NMAX}]: [{lo:+.3f}, {hi:+.3f}]; "
            f"last third [{min(tail):+.3f}, {max(tail):+.3f}]")
    print(line, flush=True)
    out.write(line + "\n")
