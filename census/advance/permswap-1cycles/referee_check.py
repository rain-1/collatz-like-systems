#!/usr/bin/env python3
"""Referee (round 1) independent check for census/advance/permswap-1cycles.

Written independently of check.py:
  * the map is taken from census/systems.py (perm_swap_s8 mod_table) and
    cross-checked against the brief's definition;
  * logarithms come from Python's decimal module (ln is correctly rounded),
    at 60 digits, with explicit safety margins, not from check.py's series;
  * the scan uses the cycle equation in a different form: for each (k, l)
    the exact set of attainable e is found by simulating, but the k-range is
    taken LARGER than the proof needs (k <= kmax(l) + 3) as a margin test, and
    the l-range is the full 1..4499;
  * a definition-level brute force counts strict local minima of every cycle
    with minimum < 10^5 and compares with the block count.
Exit 0 iff everything passes.
"""
import sys, os, time
from decimal import Decimal as Dm, getcontext
getcontext().prec = 60
t0 = time.time()
ok = True
def need(cond, msg):
    global ok
    if not cond:
        ok = False
        print("FAIL:", msg)

# ---- the map, from the catalog ----------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
try:
    from census.systems import mod_table
    S_cat = mod_table(3, [(2, 0, 3), (4, 5, 3), (4, -5, 3)])
except Exception as exc:  # fall back to a local copy of the catalog formula
    print("note: could not import census.systems:", exc)
    S_cat = lambda n: ((2*n)//3, (4*n+5)//3, (4*n-5)//3)[n % 3]
def S(n):
    q, r = divmod(n, 3)
    return 2*q if r == 0 else (4*q+3 if r == 1 else 4*q+1)
def T(n):
    q, r = divmod(n, 3)
    return 2*q if r == 0 else (4*q+1 if r == 1 else 4*q+3)
for n in range(1, 200001):
    need(S(n) == S_cat(n), f"catalog mismatch at {n}")
    if n % 3 == 1: need(3*S(n) == 4*n + 5, f"branch +5 at {n}")
    if n % 3 == 2: need(3*S(n) == 4*n - 5, f"branch -5 at {n}")
    if n % 3 != 0 and n not in (2, 5): need(S(n) > n, f"ascent rises at {n}")
    if n <= 40000: need(S(5*n) == 5*T(n), f"S(5y)=5T(y) at {n}")
print("[A] map = catalog perm_swap_s8; branches (4x+-5)/3; ascents rise except 2,5; S(5y)=5T(y)")

# ---- Laurent cutoff, independent log evaluation -------------------------------
ln = lambda x: Dm(x).ln()
L2, L3, L10 = ln(2), ln(3), ln(10)
def gval(l):  # g(l) with b' replaced by its upper bound 5.9 l + 10
    m = max(ln(Dm("5.9")*l + 10) + Dm("0.38"), Dm(10))
    return l*L2 - L10 - Dm("25.2")*L3*m*m
need(gval(4500) > 20, "g(4500)")
need(gval(4499) > 0, "g(4499) (just informative: true cutoff is lower)")
first = None
for l in range(4, 4501):
    if gval(l) > Dm("1e-30"):
        if first is None: first = l
    else:
        first = None
print(f"[B] g(4500) = {float(gval(4500)):.4f}; g > 0 for all integers in [{first}, 4500]")
# pointwise check on a long range in addition to the derivative argument
for l in range(4500, 60001, 7):
    need(gval(l) > 20, f"g({l})")
# derivative: on [4000, inf) the max is the log term; g' >= log2 - 50.4 log3 (log u+.38) 5.9/u
u = Dm("5.9")*4000 + 10
need(ln(u) + Dm("0.38") > 10, "max is the log term on [4000,inf)")
gp = L2 - Dm("50.4")*L3*(ln(u) + Dm("0.38"))*Dm("5.9")/u
need(gp > Dm("0.5"), "g' lower bound")
print(f"    g' >= {float(gp):.4f} on [4000, inf)")
# b' bound: k < (l log1.5 + log(8/3))/log(4/3)
a = ln(Dm(3)/2)/ln(Dm(4)/3); b = ln(Dm(8)/3)/ln(Dm(4)/3)
need(a < Dm("1.40943") and b < Dm("3.41"), "k slope")
c1 = (1 + Dm("1.40943")) + (2*Dm("1.40943") + 1)/L3
c0 = Dm("3.41") + 2*Dm("3.41")/L3
need(c1 < Dm("5.9") and c0 < 10, "b' constants")
print(f"    k-slope {float(a):.6f}, k-intercept {float(b):.5f}; b' <= {float(c1):.4f} l + {float(c0):.3f}")
# Laurent hypotheses: D=1 (rationals), h(3)=log3, h(2)=log2, A1=3, A2=e
need(L3 >= 1, "log A1 = log 3 >= 1/D = 1")

# ---- finite scan, enlarged k range ------------------------------------------
cands = []
for l in range(1, 4500):
    # kmax from the exact inequality 3*4^k*2^l < 8*3^(k+l), then 3 further.
    # Ratio LHS/RHS grows by 4/3 per k, so the condition is monotone in k.
    lhs = 3 * 4 * 2**l; rhs = 8 * 3**(l+1); kmax = 0
    while lhs < rhs:
        kmax += 1; lhs *= 4; rhs *= 3
    p3 = 3**(l+1); p2 = 2**(l+2); f4 = 4; f3 = 3
    for k in range(1, kmax + 4):
        if abs(p3 - p2) <= 5*(f4 - f3):
            cands.append((k, l, kmax))
        p3 *= 3; p2 *= 4; f4 *= 4; f3 *= 3
print(f"[C] pairs (k,l) with |D| <= 5(4^k-3^k), k <= kmax+3, l < 4500: {[(k,l) for k,l,_ in cands]}")
extra = [(k, l) for k, l, km in cands if k > km]
print(f"    of these, beyond the Step-5 k-bound (excluded only by it): {extra}; they are still simulated below")
hits = []
for k, l, _ in cands:
    Dd = abs(3**(k+l) - 2**(2*k+l))
    for e in range(1, 5*(4**k - 3**k)//Dd + 1):
        if e % 3 == 0: continue
        x = 2**l * e; good = True
        for _ in range(k):
            if x % 3 == 0: good = False; break
            x = S(x)
        if good and x == 3**l * e:
            # also check the l descents land on 2^l e
            for _ in range(l): x = S(x)
            need(x == 2**l * e, "descent closure")
            hits.append((k, l, e))
print(f"[D] hits (k,l,e): {hits}")
need(sorted(hits) == sorted([(2,1,1), (1,1,5), (2,1,7), (3,2,5)]), "hit list")

# ---- definition-level brute force -------------------------------------------
LIM = 100_000
seen = bytearray(LIM)
cycles = []
for s in range(1, LIM):
    if seen[s]: continue
    orb = [s]; x = S(s); good = True
    while x != s:
        if x < s or len(orb) > 20000: good = False; break
        orb.append(x); x = S(x)
    if not good: continue
    for y in orb:
        if y < LIM: seen[y] = 1
    n = len(orb)
    blocks = sum(1 for i in range(n) if orb[i] % 3 == 0 and orb[i-1] % 3 != 0)
    locmin = sum(1 for i in range(n) if orb[i-1] > orb[i] < orb[(i+1) % n])
    cycles.append((s, n, blocks, locmin))
print(f"[E] cycles with min < {LIM} (min, length, blocks, strict local minima): {cycles}")
for s, n, bl, lm in cycles:
    if n > 1: need(bl == lm, f"blocks != local minima for cycle at {s}")
one = sorted(s for s, n, bl, lm in cycles if lm == 1 or n == 1)
need(one == [1, 5, 10, 14, 20], f"one-local-minimum list {one}")
print(f"time {time.time()-t0:.1f}s")
print("REFEREE CHECK PASSED" if ok else "REFEREE CHECK FAILED")
sys.exit(0 if ok else 1)
