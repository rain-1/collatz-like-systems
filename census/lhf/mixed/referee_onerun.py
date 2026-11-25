import sys, math
from decimal import Decimal as D, getcontext
getcontext().prec = 90
sys.path.insert(0,'/home/riv/Code/collatz/census/round2/descent'); import systems as ds
sys.path.insert(0,'/home/riv/Code/collatz/census/round2/rewriting')
import importlib.util
spec=importlib.util.spec_from_file_location('rw','/home/riv/Code/collatz/census/round2/rewriting/systems.py'); rw=importlib.util.module_from_spec(spec); spec.loader.exec_module(rw)
def accel(T, dom):
    def S(n):
        x=T(n)
        while not dom(x): x=T(x)
        return x
    return S
odd=lambda n:n%2==1; nm3=lambda n:n%3!=0
cases = {
 'CLS-048': dict(T=[s for s in rw.SYSTEMS if s['id']=='split5_1_s27'][0]['step'], dom=odd, P=2,Q=5),
 'CLS-053': dict(T=ds.get('desc_split7_1')['step'], dom=odd, P=2,Q=7),
 'CLS-051': dict(T=ds.get('desc_m3_4n5')['step'], dom=nm3, P=3,Q=2),
 'CLS-052': dict(T=ds.get('desc_s32_plus9')['step'], dom=odd, P=2,Q=3),
}
# 1) brute-force cycles of S with min < N, count runs (evidence + sanity)
N=300000
for name,c in cases.items():
    S=accel(c['T'],c['dom'])
    cyc={}
    for n in range(1,N):
        if not c['dom'](n): continue
        x=n; seen=[]
        for _ in range(400):
            x=S(x)
            if x<n: break
            if x==n:
                orbit=[n]; y=S(n)
                while y!=n: orbit.append(y); y=S(y)
                runs=sum(1 for i in range(len(orbit)) if S(orbit[i])>orbit[i] and not S(orbit[i-1])>orbit[i-1])
                cyc[n]=(len(orbit),runs); break
    print(name,'cycles (min:(len,runs)) below',N,cyc)
# 2) LMN recompute with independent formula
def lmn(logA2,b): return 24.34*max(math.log(b)+0.14,21)**2*logA2
# 3) independent finite part with high-precision logs, scanning ALL admissible k
L={p:D(p).ln() for p in (2,3,5,7)}
def finite(P,Q,low_log,c1,c0,Ymax,krange):
    surv=[]
    for Y in range(1,Ymax+1):
        X=math.floor(Y*float(L[Q]/L[P]))+1
        while P**X <= Q**Y if Y<60 else False: X+=1
        lam=X*L[P]-Y*L[Q]
        if Y<60: assert P**X>Q**Y and P**(X-1)<Q**Y
        assert lam>D('1e-40')
        nl=-float(lam.ln())
        for k in krange(Y):
            if low_log(k) <= math.log(c1*k+c0)+nl+1e-9:
                surv.append((Y,k,math.floor((c1*k+c0)/float(lam)))); 
    return surv
res={}
res['CLS-048']=finite(2,5,lambda k:math.log((2**(k+1)-1)//3) if k<1000 else (k+1)*math.log(2)-math.log(3),1.53,0.42,24999,lambda Y:[Y])
res['CLS-053']=finite(2,7,lambda k:math.log((2**(2*k+1)-1)//3) if k<500 else (2*k+1)*math.log(2)-math.log(3),5.455,0.613,95299,lambda Y:range(max(1,math.ceil((Y-0.6126)/6.3116)),Y+1))
res['CLS-051']=finite(3,2,lambda k:math.log(max(4,3**k-5)) if k<500 else k*math.log(3),3.2225,5.561,55686,lambda Y:range(max(1,math.ceil((Y-8.897)/5.1558)),Y//2+1))
res['CLS-052']=finite(2,3,lambda k:math.log(2**(k+1)-1) if k<1000 else (k+1)*math.log(2),2.558,1.578,55128,lambda Y:range(max(1,math.ceil((Y-1.5779)/3.224)),Y+1))
for kname,s in res.items():
    print(kname,'survivor Y:',sorted(set(a for a,_,_ in s)),'max n0 bound',max(b for _,_,b in s))
