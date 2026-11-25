#!/usr/bin/env python3
"""check.py for census/advance/permswap-1cycles (CLS-047, perm_swap S).

Verifies every computational step of theorem.md, using exact integers except
in part 2, where logarithms are enclosed in rigorous rational intervals
(atanh series with an explicit tail bound). Exit code 0 iff every check passes.
"""
import sys, time
from fractions import Fraction

# ---- rigorous rational enclosures of logarithms -------------------------
def _atanh2(z, N=60):
    """enclosure [lo, hi] of 2*atanh(z) for rational 0 <= z <= 1/3"""
    s = Fraction(0); p = z
    for j in range(N):
        s += 2*p/(2*j+1); p *= z*z
    tail = 2*p/((2*N+1)*(1 - z*z))
    return s, s + tail
LOG2 = _atanh2(Fraction(1, 3))          # log 2 = 2 atanh(1/3)
def log_enc(x):
    """enclosure (lo, hi) of log x for rational x > 0"""
    x = Fraction(x); n = 0
    while x >= 2: x /= 2; n += 1
    while x < 1: x *= 2; n -= 1
    lo, hi = _atanh2((x - 1)/(x + 1))   # z <= 1/3 since x < 2
    if n >= 0: return lo + n*LOG2[0], hi + n*LOG2[1]
    return lo + n*LOG2[1], hi + n*LOG2[0]

t0 = time.time()
ok = True
def fail(msg):
    global ok
    ok = False
    print("FAIL:", msg)

def S(x):
    q, r = divmod(x, 3)
    return (2*q, 4*q+3, 4*q+1)[r]

def T(y):  # the 1932 map
    q, r = divmod(y, 3)
    return (2*q, 4*q+1, 4*q+3)[r]

# ---- 1. branch formulas -------------------------------------------------
for x in range(1, 300000):
    r = x % 3
    if r == 0:
        if 3*S(x) != 2*x: fail(f"S({x}) != 2x/3")
    elif r == 1:
        if 3*S(x) != 4*x + 5: fail(f"S({x}) != (4x+5)/3")
    else:
        if 3*S(x) != 4*x - 5: fail(f"S({x}) != (4x-5)/3")
    if x < 60000 and S(5*x) != 5*T(x): fail(f"S(5*{x}) != 5T({x})")
    if (S(x) % 5 == 0) != (x % 5 == 0): fail("5-divisibility not preserved")
print("[1] S(x)=2x/3 | (4x+5)/3 | (4x-5)/3 for x=0,1,2 mod 3 (x<3e5); S(5y)=5T(y) (y<6e4); 5|x <=> 5|S(x)")

# ---- 2. Laurent (via Bennett-Patel-Siksek Prop 5.1) cutoff ---------------
# Claim: for l >= L0 = 4500, l*log2 - log10 > 25.2*log3*max(log(5.9 l+10)+0.38, 10)^2,
# which contradicts |Lambda| < 10*2^-l.  g is increasing for l >= 4000 (derivative check below).
L0 = 4500
l2lo, _ = LOG2
_, l3hi = log_enc(3); l3lo, _ = log_enc(3)
_, l10hi = log_enc(10)
def g_lower(l):
    """rigorous lower bound for g(l) = l log2 - log10 - 25.2 log3 max(log(5.9l+10)+0.38, 10)^2"""
    _, lh = log_enc(Fraction(59, 10)*l + 10)
    m = max(lh + Fraction(38, 100), Fraction(10))
    return l*l2lo - l10hi - Fraction(252, 10)*l3hi*m*m
gL0 = g_lower(L0)
if not gL0 > 1: fail(f"g(L0) lower bound {float(gL0)} not > 1")
# g' >= log2 - 2*25.2*log3*(log(5.9l+10)+0.38)*5.9/(5.9l+10) where the max is the log term
# (and g' = log2 where the max is 10). (log u + 0.38)/u decreases for u > e^0.62, so the
# worst case on [4000, inf) is l = 4000.
u = Fraction(59, 10)*4000 + 10
_, lu = log_enc(u)
dmin = l2lo - 2*Fraction(252, 10)*l3hi*(lu + Fraction(38, 100))*Fraction(59, 10)/u
if not dmin > Fraction(1, 10): fail("derivative bound")
print(f"[2] cutoff: g(4500) >= {float(gL0):.6f} > 1 and g' >= {float(dmin):.4f} > 0 on [4000,inf); so l < 4500")
# b' = (k+l) + (2k+l)/log3 with k < 1.40943 l + 3.41 (k-bound checked exactly in part 3):
c1 = Fraction(240943, 100000) + Fraction(381886, 100000)/l3lo
c0 = Fraction(341, 100) + Fraction(682, 100)/l3lo
if not (c1 < Fraction(59, 10) and c0 < 10): fail("b' bound")
print(f"    b' <= {float(c1):.5f} l + {float(c0):.4f} <= 5.9 l + 10")
# the analytic k-bound k < (l log(3/2) + log(8/3))/log(4/3) <= 1.40943 l + 3.41 (all l):
l15hi = log_enc(Fraction(3, 2))[1]; l83hi = log_enc(Fraction(8, 3))[1]; l43lo = log_enc(Fraction(4, 3))[0]
if not (l15hi/l43lo < Fraction(140943, 100000) and l83hi/l43lo < Fraction(341, 100)): fail("k slope")
print(f"    k-bound: log(3/2)/log(4/3) < {float(l15hi/l43lo):.7f} <= 1.40943, log(8/3)/log(4/3) < {float(l83hi/l43lo):.6f} <= 3.41")
# log-value sanity
if not (LOG2[1]-LOG2[0] < Fraction(1, 10**40)): fail("log2 enclosure too wide")

# ---- 3. exact finite scan --------------------------------------------------
# For 1 <= l < L0 and every k >= 1 with 3*4^k*2^l < 8*3^(k+l) (the k-bound), test
# |3^(k+l) - 2^(2k+l)| <= 5(4^k - 3^k).
cands = []
maxratio = Fraction(0)
for l in range(1, L0):
    A = 3**(l+1); B = 2**(l+2); P4 = 4; P3 = 3   # k = 1
    k = 1
    while 3*P4*(1 << l) < 8*A:
        if abs(A - B) <= 5*(P4 - P3):
            cands.append((k, l, abs(A - B)))
        k += 1; A *= 3; B *= 4; P4 *= 4; P3 *= 3
    kmax = k - 1
    if l >= 100:
        if not Fraction(kmax) < Fraction(140943, 100000)*l + Fraction(341, 100):
            fail(f"kmax bound at l={l}")
print(f"[3] exact scan l < {L0}, k <= kmax(l): {len(cands)} candidate pairs (k,l,|D|): {cands}")

# ---- 4. e-enumeration and simulation ------------------------------------
found = []
for (k, l, D) in cands:
    emax = 5*(4**k - 3**k)//D
    for e in range(1, emax+1):
        if e % 3 == 0: continue
        x = x0 = 2**l * e
        good = True
        for i in range(k):
            if x % 3 == 0: good = False; break
            x = S(x)
        if good and x == 3**l * e:
            cyc = [x0]; y = S(x0)
            while y != x0: cyc.append(y); y = S(y)
            found.append((k, l, e, cyc))
print("[4] 1-cycles with l >= 1 (k, l, e, cycle from its minimum):")
for f in found: print("     ", f)
expect = {(2,1,1), (1,1,5), (2,1,7), (3,2,5)}
if {(k,l,e) for k,l,e,_ in found} != expect: fail("unexpected cycle list")

# x0 in {2,4}: orbit of 4 is a 2-block cycle (not a 1-cycle); orbit of 2 is (2,1,3).
orb = [4]; y = S(4)
while y != 4: orb.append(y); y = S(y)
blocks = sum(1 for i in range(len(orb)) if orb[i] % 3 == 0 and orb[i-1] % 3 != 0)
if blocks != 2: fail("orbit of 4")
print(f"    orbit of 4 = {orb}: {blocks} blocks of multiples of 3 (not a 1-cycle)")

# ---- 5. brute-force sanity: all cycles with minimum < 1e5 -------------------
seen = set(); allc = []
for s in range(1, 100000):
    if s in seen: continue
    x = S(s); orb = [s]; good = True
    while x != s:
        if x < s or len(orb) > 5000: good = False; break
        orb.append(x); x = S(x)
    if good:
        seen.update(orb)
        b = sum(1 for i in range(len(orb)) if orb[i] % 3 == 0 and orb[i-1] % 3 != 0)
        allc.append((min(orb), len(orb), b))
print("[5] brute force, cycles with minimum < 1e5 (min, length, #blocks):", allc)
one = sorted(m for m, L, b in allc if b <= 1)
if one != [1, 5, 10, 14, 20]: fail("brute force 1-cycle list")

print(f"time {time.time()-t0:.1f}s")
print("ALL CHECKS PASSED" if ok else "SOME CHECK FAILED")
sys.exit(0 if ok else 1)
