# Independent round-2 recheck of Theorem B with Laurent 2008 Cor. 2 (own code; interval arithmetic via mpmath.iv)
from mpmath import iv, mp
from fractions import Fraction as Fr
iv.dps = 300
L2, L5 = iv.log(2), iv.log(5)
AL = L5 / L2
TABLE = [(10,'25.2'),(12,'23.4'),(14,'22.1'),(16,'21.1'),(18,'20.3'),(20,'19.7'),(22,'19.2'),(24,'18.8'),(26,'18.4'),(28,'18.1'),(30,'17.9')]
def up(x): return mp.make_mpf(x._mpi_[1])
def lo_(x): return mp.make_mpf(x._mpi_[0])
def mf(v):
    m,e = mp.mpf(v).man_exp
    return Fr(int(m))*Fr(2)**int(e)
def fr(x):  # exact Fraction enclosure endpoints
    return mf(lo_(x)), mf(up(x))
mp.dps = 300
alo, ahi = fr(AL)
# continued fraction convergents common to [alo, ahi]
def convs(lo, hi):
    out=[]; p0,q0,p1,q1=0,1,1,0
    while True:
        a, b = lo.numerator//lo.denominator, hi.numerator//hi.denominator
        if a!=b: return out
        p0,q0,p1,q1=p1,q1,a*p1+p0,a*q1+q0; out.append((p1,q1))
        lo, hi = 1/(hi-b), 1/(lo-a)
CV = convs(alo, ahi)
def ok(R, B=42, verbose=False):
    CR = (AL**R - 1)/(AL - 1)
    best=None
    for mstar, c2 in TABLE:
        c = iv.mpf(c2)*L5
        # find mu0 by scanning: need F(mu0)<mu0 and 2c*Lg(mu0)<mu0
        mu = iv.mpf(30)
        for _ in range(200):
            K0 = CR*(1+mu/L2)
            # b' = K + L/log5, L < K alpha + delta/log2, delta < 1
            bp = K0*(1+1/L2) + 1/(L2*L5)
            Lg = iv.mpf(max(up(iv.log(bp)+iv.mpf('0.38')), mstar))
            F = iv.log(iv.mpf(5*R)/6) + c*Lg*Lg
            if up(F) < lo_(mu) and up(2*c*Lg) < lo_(mu): break
            mu = iv.mpf(int(up(F)*1.05)+1)
        else: continue
        if best is None or lo_(mu) < best[0]: best=(int(up(mu)), mstar)
    mu0 = best[0]
    l2 = 1 + Fr(mu0)/fr(L2)[0]
    hist=[best]
    while True:
        K0 = mf(up(CR))*l2 + 1  # pad
        q=None
        for P,Q in CV:
            if Q > 2*K0: q=(P,Q); break
        P,Q=q
        assert all(abs(Fr(P,Q)-a) < Fr(1,Q*Q) for a in (alo,ahi))
        M = Fr(5*R*Q,3)/fr(L2)[0]
        hist.append((Q, float(M)))
        if M <= 2**B:
            if verbose: print(R, hist)
            return True
        new = (M.numerator//M.denominator+1).bit_length()+1
        if new >= l2: 
            if verbose: print(R, 'FAIL', hist)
            return False
        l2 = new
print('R=23 ok', ok(23, verbose=True)); print('R=24 ok', ok(24, verbose=True))
# Stern-Brocot for K
eps = Fr(5,6)/(2**42*fr(L2)[0]); lo, hi = alo, ahi+eps
a,b,c,d=0,1,1,0
while True:
    p,q=a+c,b+d
    if Fr(p,q)<=lo: a,b=p,q
    elif Fr(p,q)>=hi: c,d=p,q
    else: break
print('Kmin', q, 'nbrs', (a,b),(c,d), 'Lmin', (q*alo).__floor__()+1, 'Tsteps', q+(q*alo).__floor__()+1+1)
