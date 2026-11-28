"""Exact check: for b = 3 mod 4, v_2(5^k + b) = 2 + v_2(k - lam_b), lam_b = log_5(-b) in Z_2
(computed mod 2^M).  Exits 1 on failure."""
import sys
M=80
def v2(x):
    if x==0: return 10**9
    c=0
    while x%2==0: x//=2; c+=1
    return c
def dlog5(t):           # t = 1 mod 4; returns lam mod 2^(M-2) with 5^lam = t mod 2^M
    lam=0; cur=1; g=5
    for i in range(M-2):
        if (t-cur)%(1<<(i+3)): lam|=1<<i; cur=cur*g%(1<<M)
        g=g*g%(1<<M)
    assert pow(5,lam,1<<M)==t%(1<<M); return lam
ok=True; worst=0
for b in range(3,400,4):
    lam=dlog5((-b)%(1<<M))
    for k in list(range(1,3000))+[lam%(1<<j) for j in range(1,40)]:
        if k==0: continue
        lhs=v2((pow(5,k,1<<M)+b)%(1<<M)); rhs=2+v2((k-lam)%(1<<(M-2)))
        if rhs<M-4 and lhs!=rhs: ok=False; print('FAIL',b,k,lhs,rhs)
        worst=max(worst,lhs if lhs<M else 0)
print('lam_3 mod 2^40 =',dlog5((-3)%(1<<M))%(1<<40),' max valuation seen',worst,' CHECK','passed' if ok else 'FAILED')
sys.exit(0 if ok else 1)
