"""Referee (round 1) independent check for census/advance/9n1-cycles/theorem.md.

Independent of check.py: logs come from the decimal module (correctly rounded
ln at 150 digits, widened by 1e-140), the continued fraction is taken from
interval endpoints, the minimum bound is computed by brute minimisation of
||k*alpha|| over convergent denominators, and the finite scan is a separate C
program (scan.c) iterating the catalog map step by step, with a big-integer
Python fallback for 128-bit overflow.

Usage: python3 referee_check.py [R]   (default 13).  Exit 0 iff all pass.
"""
import os, subprocess, sys
from decimal import Decimal, getcontext
from fractions import Fraction as F
from concurrent.futures import ThreadPoolExecutor

R = int(sys.argv[1]) if len(sys.argv) > 1 else 13
getcontext().prec = 150
EPS = F(1, 10**140)
def lnI(n):
    v = F(Decimal(n).ln())
    return v - EPS, v + EPS
L2, L3, L10 = lnI(2), lnI(3), lnI(10)
A = (2*L3[0]/L2[1], 2*L3[1]/L2[0])            # alpha = log_2 9

# --- definition-level sanity: run structure of S vs. the catalog map ---
def S(n): return (9*n+1)//2 if n % 2 else n//2
for x in range(1, 4001, 2):                  # 7S(x)+1 = (9/2)(7x+1), a = v2(7x+1)
    assert 2*(7*S(x)+1) == 9*(7*x+1)
    t = 7*x+1; a = (t & -t).bit_length()-1
    y = x
    for j in range(a): assert y % 2 == 1; y = S(y)
    assert y % 2 == 0

# --- C_R and Laurent step ---
C = sum(A[1]**i for i in range(R))
cb = 2 + L10[1]/(L2[0]*L3[0])                  # b' <= cb*k
assert cb < F(503, 100)
def ln_up(x):                                   # upper bound for ln of positive Fraction
    v = F(Decimal(x.numerator).ln() - Decimal(x.denominator).ln())
    return v + EPS
logR7 = ln_up(F(R, 7))
def fk(k):
    L = ln_up(cb*k) + F(38, 100)
    assert L >= 10
    return C*(3 + (max(logR7, 0) + F(252, 10)*L3[1]*L*L)/L2[0])
# own choice of K0: smallest power of 10 times 1,2,5 for which f(K0) < K0
K0 = None
for e in range(8, 20):
    for c in (1, 2, 5):
        k = c*10**e
        if ln_up(cb*k) + F(38, 100) >= 10 and fk(k) < k:
            K0 = k; break
    if K0: break
assert K0 is not None
print(f"[Laurent] R={R}: C_R={float(C):.6g}, first K0 with f(K0)<K0: {K0} (f={float(fk(K0)):.4g}); prover used 2e12")
K0p = 2*10**12
assert fk(K0p) < K0p
# monotonicity of f(k)/k for L>2 is analytic; spot check on a geometric grid
k = K0p
for _ in range(200):
    assert fk(k) < k; k = k*3//2

# --- continued fraction and min ||k alpha|| ---
lo, hi = A
cf = []
while True:
    a, b = lo.numerator//lo.denominator, hi.numerator//hi.denominator
    if a != b: break
    cf.append(a); lo, hi = 1/(hi-a), 1/(lo-a)
P, Q = [cf[0], cf[0]*cf[1]+1], [1, cf[1]]
for a in cf[2:]:
    P.append(a*P[-1]+P[-2]); Q.append(a*Q[-1]+Q[-2])
print(f"[CF] {len(cf)} partial quotients certified; first: {cf[:12]}")
def dist_lo(i):
    u, v = Q[i]*A[0]-P[i], Q[i]*A[1]-P[i]
    assert u*v > 0
    return min(abs(u), abs(v))
kmax = K0p
while True:
    i = max(j for j in range(len(Q)) if Q[j] <= kmax)   # q_i <= kmax < q_{i+1}
    assert Q[i+1] > kmax
    d = dist_lo(i)                                         # min_{1<=k<=kmax} ||k alpha|| = ||q_i alpha||
    Mb = F(R)/(7*L2[0]*d)                                  # m < Mb
    M = Mb.numerator//Mb.denominator + 1
    nk = int(C*(7*M+1).bit_length())
    print(f"[CF] k<={kmax}: q_i={Q[i]} -> m < {M}; new k<={nk}")
    if nk >= kmax: break
    kmax = nk
MF = M
print(f"[CF] final bound m < {MF}")

# --- independent C scan ---
here = os.path.dirname(os.path.abspath(__file__))
exe = os.path.join(os.environ.get("TMPDIR", "/tmp"), f"ref9n1scan_{os.getpid()}")
subprocess.run(["gcc", "-O2", "-o", exe, os.path.join(here, "scan.c")], check=True)
def big(m):
    x = m
    for r in range(R):
        n = x
        while True:
            n = (9*n+1)//2
            if n % 2 == 0: break
        while n % 2 == 0: n //= 2
        x = n
        if x <= m: return x == m
    return False
# cross-check C vs Python on a small range
small = subprocess.run([exe, "1", "200001", str(R)], capture_output=True, text=True, check=True).stdout
sov = {int(l.split()[1]) for l in small.splitlines() if l.startswith("OVERFLOW")}
assert "HIT" not in small and not any(big(m) for m in range(1, 200001, 2))
step = 4*10**6
jobs = [(s, min(s+step, MF)) for s in range(1, MF, step)]
def go(j): return subprocess.run([exe, str(j[0]), str(j[1]), str(R)], capture_output=True, text=True, check=True).stdout
with ThreadPoolExecutor(os.cpu_count()) as ex:
    outs = list(ex.map(go, jobs))
total = 0; ovf = []
for o in outs:
    for line in o.splitlines():
        if line.startswith("HIT"): raise SystemExit(f"FAIL {line}")
        if line.startswith("OVERFLOW"): ovf.append(int(line.split()[1]))
        if line.startswith("DONE"): total += int(line.split("count=")[1].split()[0])
assert total == MF//2, (total, MF//2)
for m in ovf: assert not big(m), m
os.remove(exe)
print(f"[scan] {total:,} odd m < {MF} (= all odd m in range) excluded through {R} runs; "
      f"{len(ovf)} 128-bit overflows re-done in Python, none a cycle")
print("REFEREE PASS")
