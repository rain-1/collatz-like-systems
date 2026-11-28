"""EVIDENCE: first-drop stopping time measured in halvings, divided by log2(n), for split5_3 and 3x+1.
Prediction tested: limsup = 1/(1 - h), h = Hausdorff dimension of the non-descending set
(split5_3: h = 0.5806841 -> 2.385;  3x+1: h = 0.949955 -> 19.98)."""
import math, sys
def s53(n):  return n//2 if n%2==0 else (5*n+3 if n%4==1 else n+3)
def c31(n):  return n//2 if n%2==0 else 3*n+1
def halvings_to_drop(step,n,cap=100000):
    x=n;b=0
    while b<cap:
        if x%2==0: b+=1
        x=step(x)
        if x<n: return b
    return None
for name,step,N,cyc in (('split5_3',s53,3*10**6,{1,2,3,4,5,6,8,10,12,14,28,61,125}),('3x+1',c31,3*10**6,{1,2,4})):
    best={}
    for n in range(130,N):
        b=halvings_to_drop(step,n)
        if b is None: print('no drop',n); continue
        L=int(math.log2(n)); r=b/math.log2(n)
        if r>best.get(L,(0,0))[0]: best[L]=(r,n,b)
    print(name)
    for L in sorted(best): print(f"  2^{L:<2d} max ratio {best[L][0]:6.3f} at n={best[L][1]} (halvings {best[L][2]})")
