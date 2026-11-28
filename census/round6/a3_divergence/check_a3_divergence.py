"""Exact check of the A3 divergence proof (see README.md).  Exits 1 on any failure.
A3 over F_3: f(0)=0: f/t; f(0)=1: (1+t^2)(f-1)/t; f(0)=2: (f-2)/t + 1."""
import random, sys
from a3 import step
from theta import theta
ok=True
def chk(c,msg):
    global ok
    if not c: ok=False; print('FAIL',msg)
def trim(P):
    P=list(P)
    while P and P[-1]==0: P.pop()
    return P
def add(a,b):
    n=max(len(a),len(b)); return trim([((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%3 for i in range(n)])
def mul(a,b):
    if not a or not b: return []
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b): r[i+j]=(r[i+j]+x*y)%3
    return trim(r)
q=[0,2,1,0,2,2,0,2]                      # 2t + t^2 + 2t^4 + 2t^5 + 2t^7
c=[1,2]                                   # 1 + 2t
def subs6(K):                             # K(t^6)
    r=[0]*(6*len(K)) if K else []
    for i,a in enumerate(K): r[6*i]=a
    return trim(r)
def fK(K): return tuple(add(c,mul(subs6(K),q)))
def T6(f):
    w=''
    for _ in range(6): w+=str(f[0] if f else 0); f=step(f)
    return f,w
# 1. the seed
chk(fK([1])==(1,1,1,0,2,2,0,2),'seed f_1')
# 2. conjugacy T^6(f_K) = f_{Theta(K)} and branch words, exhaustively for deg K <= 6 and randomly beyond
words={0:'121212',1:'111111',2:'102101'}
import itertools
cnt=0
for d in range(0,7):
    for K in itertools.product(range(3),repeat=d+1):
        K=trim(K); g,w=T6(fK(K)); k0=K[0] if K else 0
        chk(w==words[k0],('word',K,w)); chk(tuple(g)==fK(theta(K)),('conj',K)); cnt+=1
rnd=random.Random(7)
for _ in range(400):
    K=trim([rnd.randrange(3) for _ in range(rnd.randrange(8,60))])
    g,w=T6(fK(K)); chk(w==words[K[0] if K else 0],'word rnd'); chk(tuple(g)==fK(theta(K)),'conj rnd'); cnt+=1
# 3. degrees: deg f_K = 6 deg K + 7 for K != 0; Theta raises deg by 1 iff k0 = 1, else keeps it
for _ in range(300):
    K=trim([rnd.randrange(3) for _ in range(rnd.randrange(1,40))])
    if not K: continue
    chk(len(fK(K))-1==6*(len(K)-1)+7,'deg f_K'); L=theta(K)
    chk(len(L)-len(K)==(1 if K[0]==1 else 0),('deg theta',K))
# 4. the key lemma: for L = s + (1+s)^2 M and 3^m - 2 > deg M, the constant term after n = 3^m - 2
#    steps of N (K -> ((1+s)K - k0)/s) equals 1.  N^n has constant term sum_j C(n,j) k_j.
def N(K):
    Q=[0]*(len(K)+1)
    for i,a in enumerate(K): Q[i]=(Q[i]+a)%3; Q[i+1]=(Q[i+1]+a)%3
    return trim(Q[1:])
for _ in range(200):
    M=trim([rnd.randrange(3) for _ in range(rnd.randrange(0,24))])
    L=add([0,1],mul([1,2,1],M)); m=1
    while 3**m-2<=len(M)-1: m+=1
    X=L
    for _ in range(3**m-2): X=N(X)
    chk((X[0] if X else 0)==1,('lemma',M))
# 5. the orbit of K = 1: every gap between degree-raising steps is at most 3^m - 1, where 3^m - 2 > deg M
K=[1]; last=None; n=0; maxratio=0
for n in range(60000):
    if K and K[0]==1:
        if last is not None:
            D=len(K)-1; m=1            # the previous raising step produced L of degree D, L = s + (1+s)^2 M, deg M = D - 2
            while 3**m-2<=D-2: m+=1
            chk(n-last<=3**m-1,('gap',n,last,D))   # L appears one step after the raising step
        last=n
    K=theta(K)
chk(len(K)-1>15000,'degree growth')
print('conjugacy cases checked:',cnt,' final degree of K after 60000 steps:',len(K)-1)
print('CHECK','passed' if ok else 'FAILED'); sys.exit(0 if ok else 1)
