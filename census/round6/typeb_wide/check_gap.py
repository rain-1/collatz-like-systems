"""Exact checks for the tail-exponent statements (README section "Gap").  Needs numpy
(run with census/round4/wpotential/.venv/bin/python).

[G1] gap zero does not imply type (b): the S-family member S = {3,7,15,23,31,35,39,41,47,51,
     55,57,59,63} (mod 64; 3n+1 on S, n+1 on the other odd classes) has the isolated
     expanding cycle {63, 62} (x* = -1, theta_C = log 2 / log(3/2)) and a type-(c) component;
     every non-trivial component other than {63, 62} has rho_S(t) <= 1 at a rational
     t >= theta_C (exact Collatz-Wielandt certificate), so theta_1 = theta_run = theta_C.
     Note (REFEREE2): the choice t >= theta_C is made by a float comparison.  For G1,
     t = 665/389 and the float margin is about 2.8e-7; the inequality holds exactly,
     since t >= log 2/log(3/2) is 2^1054 <= 3^665 (checked exactly in referee2_check.py).
[G2] boundary of the standing hypothesis: sh8 lifted to modulus 16 with n = 9 (16) -> n + 16.
     The class 9 mod 16 is a division-free self-loop (every n = 9 mod 16 diverges linearly);
     the other components are the isolated cycle of -1 and contracting ones, certified as in
     G1, and the translation block has rho = 1 for every theta.  So theta_1 = theta_run =
     log 2/log(3/2) > 0, the gap is zero, and divergent orbits exist.
Exit 0 iff both pass.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tblib as TB
import gap

ok = True
S = {3, 7, 15, 23, 31, 35, 39, 41, 47, 51, 55, 57, 59, 63}
tab = [(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r in S else (1, 1, 1)) for r in range(64)]
cl = TB.classify(2, 6, tab)
bs = [c for c in cl["comps"] if c["kind"] == "b"]
r = gap.analyse(2, 6, tab)
g1 = (TB.verdict(cl) == "c" and len(bs) == 1 and sorted(bs[0]["nodes"]) == [62, 63]
      and r["gap_zero_certified"] and any(k == "c" for k, *_ in r["comps"]))
print("[G1]", "PASS" if g1 else "FAIL", "theta_C =", r["theta_b"], "t =", r["t"], "components:", r["comps"])
ok &= g1

sh8 = [(1, 0, 2), (1, 1, 1), (1, 0, 2), (3, 1, 1), (1, 0, 2), (1, 5, 1), (1, 0, 2), (3, 1, 1)]
t16 = [sh8[x % 8] for x in range(16)]
t16[9] = (1, 16, 1)
TB.check_table(2, 4, t16)
cl = TB.classify(2, 4, t16)
kinds = sorted(c["kind"] for c in cl["comps"] if c["kind"] != "trivial")
# divergence of the class 9 mod 16: T(n) = n + 16 keeps the class
T = TB.step_fn(2, 4, t16)
div_ok = all(T(9 + 16 * k) == 9 + 16 * (k + 1) for k in range(1000))
# certificates for every component with internal edges except the isolated cycle and the
# translation loop
bcomp = [c for c in cl["comps"] if c["kind"] == "b"]
thb = min(gap.theta_C(2, c["U"], c["e"]) for c in bcomp)
from fractions import Fraction as Fr
t = Fr(thb).limit_denominator(1000)
while float(t) < thb:
    t += Fr(1, 1000)
cert = True
for c in cl["comps"]:
    if c["kind"] in ("a", "c") and not c.get("simple"):
        cert &= gap.certify_rho_le1(2, 4, t16, c["nodes"], t)
    if c["kind"] == "c":
        cert = False
g2 = "divfree" in kinds and len(bcomp) == 1 and div_ok and cert
print("[G2]", "PASS" if g2 else "FAIL", "component kinds:", kinds, "theta_C =", thb)
ok &= g2
print("ALL PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
