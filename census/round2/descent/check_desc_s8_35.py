"""check: desc_s8_35.  Computational part of the tier-2 proof (see desc_s8_35.md):
the minimal stopping-time descent certificate is built by exhaustive 2-adic
search, re-verified independently (classes partition Z, each stored affine
form equals the real iterate, each descends), the exceptional set E of
non-descending positive integers is listed, and every orbit from E is run to
its cycle.  Also checks the deepest class needs all its steps.  Exit 0 iff
everything passes."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from descent_lib import *
import systems

s = systems.get("desc_s8_35")
c, got, cyc, deep = full_certificate_check(s, dict(K=4, k=6, size=6, E=[1], cycle_mins=[1]))
print("certificate: max level K =", got["K"], " steps k =", got["k"],
      " classes =", got["size"], " |E| =", len(got["E"]))
print("cycles (min, length):", sorted((min(x), len(x)) for x in cyc))
print("deepest class: n = %d mod 2^%d needs %d steps" % (deep[1], deep[0], deep[2]))
if 0:
    # the near-critical 2-adic cycle that makes the certificate deep:
    # orbit of 227/13 (scaled by d for offset d), period 13, multiplier 3^5/2^8
    d = s["table"][1][1]
    x = Fraction(227 * d, 13)
    L, A, D = padic_cycle_check(x, 2, s["m"], s["table"])
    assert (L, A, D) == (13, 243, 256)
    print("near-critical 2-adic cycle through %s: period 13, multiplier 243/256" % x)
print("PASS")
