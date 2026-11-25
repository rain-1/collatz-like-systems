import mpmath as mp, random
mp.mp.dps = 400
def T(n): return n//2 if n%2==0 else (5*n+1 if n%4==1 else n+1)
# cycles
def cyc(m):
    c=[m]; x=T(m)
    while x!=m: c.append(x); x=T(x)
    return c
for m,p in ((1,5),(13,35)):
    c=cyc(m); assert len(c)==p and min(c)==m
    odd=[x for x in c if x%2]
    K=sum(1 for x in c if x%4==1); L=sum(1 for x in c if x%2==0)
    runs=sum(1 for i,x in enumerate(odd) if x%4==1 and odd[i-1]%4==3)
    delta=L*mp.log(2)-K*mp.log(5)
    print("cycle",m,"K",K,"L",L,"runs",runs,"delta",mp.nstr(delta,8),"bound",mp.nstr(mp.mpf(5)*runs/(6*m),8))
    assert 0<delta<mp.mpf(5)*runs/(6*m)
# run recursion G_{i+1} <= G_i + (alpha-1)k_i - 1 on random odd x = 1 mod 4
al=mp.log(5)/mp.log(2)
random.seed(1)
for _ in range(20000):
    x=random.getrandbits(random.randint(3,200))|1
    if x%4!=1: continue
    G=mp.log((3*x+1)/mp.mpf(2),2); k=0; y=x
    while y%4==1: y=(5*y+1)//2; k+=1
    assert k==((3*x+1)&-(3*x+1)).bit_length()-2 and k<=G
    v=y
    while True:
        v=(v+1); 
        while v%2==0: v//=2
        if v%4==1: break
    assert mp.log((3*v+1)/mp.mpf(2),2) <= G+(al-1)*k-1+mp.mpf(10)**-300
print("run recursion ok")
# B1: Stern-Brocot, independent
eps=mp.mpf(5)/(6*mp.mpf(2)**42*mp.log(2))
lo,hi=al,al+eps
a,b,c,d=0,1,1,0
while True:
    p,q=a+c,b+d
    if p<=lo*q: a,b=p,q
    elif p>=hi*q: c,d=p,q
    else: break
print("K_min",q,"neighbours",(a,b),(c,d))
assert abs(p-lo*q)>mp.mpf(10)**-350
Lmin=int(mp.floor(q*al))+1
print("L_min",Lmin,"K+L+1",q+Lmin+1)
# B2: R chain, independent re-derivation with generous rounding
def ok(R,Bbits=42):
    CR=(al**R-1)/(al-1)
    C=mp.mpf('24.34')*mp.log(5)
    def F(mu):
        bp=mp.mpf('2.443')*CR*(1+mu/mp.log(2))+1
        Lg=max(mp.log(bp)+mp.mpf('0.14'),21)
        return mp.log(mp.mpf(5)*R/6)+C*Lg**2, Lg
    mu=mp.mpf(1000)
    for _ in range(200):
        f,Lg=F(mu)
        if f<mu*(1-mp.mpf(10)**-20) and 2*C*Lg<mu: break
        mu=f*mp.mpf('1.01')
    else: return False,None
    hist=[int(mu)]
    cf=mp.identify  # unused
    # convergents of alpha
    convs=[]; x=al; p0,q0,p1,q1=0,1,1,0
    for _ in range(300):
        a_=int(mp.floor(x)); p0,q0,p1,q1=p1,q1,a_*p1+p0,a_*q1+q0; convs.append((p1,q1)); x=1/(x-a_)
    l2=1+mu/mp.log(2)
    for _ in range(50):
        K0=CR*l2
        P,Q=next((pp,qq) for pp,qq in convs if qq>2*K0)
        assert abs(al-mp.mpf(P)/Q)<mp.mpf(1)/Q**2
        Mb=mp.mpf(5)*R*Q/(3*mp.log(2))
        hist.append((Q,mp.nstr(Mb,6)))
        if Mb<=mp.mpf(2)**Bbits: return True,hist
        new=mp.log(2*Mb,2)
        if new>=l2*(1-mp.mpf(10)**-30): return False,hist
        l2=new
    return False,hist
for R in (22,23,24):
    print(R,ok(R))
