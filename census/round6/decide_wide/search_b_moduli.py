#!/usr/bin/env python3
"""search_b_moduli.py -- for every modulus 2 <= Q <= 64, sample the raw full-division family
   R(Q): r not prime to Q -> n/p, p the least prime of Q dividing r;
         r prime to Q     -> u n + v, u prime to Q with 1 <= u <= 13, -4 <= v <= 4, (P)
and record the first type-(b) member found (famscan, exact), or none in N samples.
Output: out/b_moduli.txt.  Theorem S (theory.md) predicts none for squarefree Q.
"""
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import families as F  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 400000
LAND = len(sys.argv) > 2 and sys.argv[2] == "land"


def raw_family(Q, land=False):
    """land=True: keep only unit branches whose image class is not a unit (avoids the
    division-free cycles that dominate the unrestricted family)."""
    opts = []
    for r in range(Q):
        d = F.div_branch(Q, r)
        if d is not None:
            opts.append([d])
            continue
        allo = [(u, v, 1) for u in range(1, 14) if math.gcd(u, Q) == 1
                for v in range(-4, 5) if F.ok_option(Q, r, u, v, 1)]
        lo = [t for t in allo if math.gcd(t[0] * r + t[1], Q) > 1]
        opts.append(lo if (land and lo) else allo)
    return opts


def squarefree(Q):
    return all(Q % (p * p) for p in range(2, Q + 1))


def main():
    out = open(os.path.join(HERE, "out", "b_moduli_land.txt" if LAND else "b_moduli.txt"), "w")
    for Q in range(2, 65):
        opts = raw_family(Q, LAND)
        spec = F.spec_text(Q, opts, 1, N, 1000 + Q)
        p = subprocess.run([os.path.join(HERE, "famscan")], input=spec, capture_output=True,
                           text=True, check=True)
        bl = [l.split()[1] for l in p.stdout.splitlines() if l.startswith("B ")]
        summ = [l for l in p.stdout.splitlines() if l.startswith("SUMMARY")][0]
        ex = F.decode(opts, bl[0]) if bl else None
        line = f"Q={Q} squarefree={squarefree(Q)} nB={len(bl)} {summ} example={ex}"
        print(line, flush=True)
        out.write(line + "\n")


if __name__ == "__main__":
    main()
