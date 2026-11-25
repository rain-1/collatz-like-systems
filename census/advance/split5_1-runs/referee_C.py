import mpmath as mp
from fractions import Fraction as Fr
mp.mp.dps=50
th=mp.mpf(1)/4; lam=mp.mpf('0.958'); wO=1; wE=mp.mpf('0.783'); wU=1
O=(mp.mpf(5)/2)**th*wO/2+(mp.mpf(1)/2)**th*wE/2; E=(mp.mpf(1)/2)**th*(wE+wO)/2; Uu=((mp.mpf(1)/2)**th*wU+wO)/2
print("O",O,lam*wO,"E",E,lam*wE,"U",Uu,lam*wU); assert O<lam*wO and E<lam*wE and Uu<lam*wU
print("exp",mp.log(2*lam,2))
# brute-force empirical check of the counting bound and of the state machine semantics
def T(n): return n//2 if n%2==0 else (5*n+1 if n%4==1 else n+1)
def nodrop(n):
    x=T(n); s=0
    while x>=n:
        if x in (1,13) and n in (1,13) or s>10**6: return True
        if x==n: return True
        x=T(x); s+=1
    return False
for j in range(1,19):
    c=sum(1 for n in range(2**j,2**(j+1)) if nodrop(n))
    bnd=2**0.25*float(2*lam)**j/0.783
    assert c<=bnd
    print(j,c,round(bnd))
