"""Lundberg exponent theta_1 and run exponent theta_run on the cylinder graph (floats: illustration).
Table: p, m, rows r -> (u, v, e) meaning T(n) = (u n + v)/p^e on n = r mod p^m."""
import math, sys, itertools
import numpy as np
def graph(p,m,tab,K):
    Q=p**K; E=[]
    for r in range(Q):
        u,v,e=tab[r%p**m]; assert (u*r+v)%p**e==0
        base=((u*r+v)//p**e)%p**(K-e)
        for j in range(p**e): E.append((r,base+j*p**(K-e),u,e))
    return Q,E
def rho(p,Q,E,th):
    M=np.zeros((Q,Q))
    for r,s,u,e in E: M[r,s]+=p**(-e)*(u/p**e)**th
    return max(abs(np.linalg.eigvals(M)))
def theta1(p,Q,E,hi=60.0):
    if rho(p,Q,E,1e-6)>1: return 0.0
    if rho(p,Q,E,hi)<=1: return math.inf
    lo=0.0
    for _ in range(80):
        mid=(lo+hi)/2
        if rho(p,Q,E,mid)>1: hi=mid
        else: lo=mid
    return lo
def sccs(Q,E):
    adj=[[] for _ in range(Q)]
    for r,s,u,e in E: adj[r].append(s)
    idx={};low={};st=[];on=set();out=[];c=[0]
    sys.setrecursionlimit(10000)
    def dfs(v):
        idx[v]=low[v]=c[0];c[0]+=1;st.append(v);on.add(v)
        for w in adj[v]:
            if w not in idx: dfs(w);low[v]=min(low[v],low[w])
            elif w in on: low[v]=min(low[v],idx[w])
        if low[v]==idx[v]:
            comp=[]
            while True:
                w=st.pop();on.discard(w);comp.append(w)
                if w==v:break
            out.append(comp)
    for v in range(Q):
        if v not in idx: dfs(v)
    return out
def analyse(name,p,m,tab,K):
    Q,E=graph(p,m,tab,K)
    t1=theta1(p,Q,E)
    # expanding simple cycles, per SCC (DFS; small graphs only)
    best=math.inf; types=[]
    for comp in sccs(Q,E):
        S=set(comp); edges=[x for x in E if x[0] in S and x[1] in S]
        if not edges: continue
        adj={}
        for r,s,u,e in edges: adj.setdefault(r,[]).append((s,u,e))
        loc=math.inf; ncyc=0
        for start in sorted(S):
            stack=[(start,[start],0.0,0)]
            while stack:
                v,path,lg,dv=stack.pop()
                for s,u,e in adj.get(v,[]):
                    l2=lg+math.log(u)-e*math.log(p); d2=dv+e
                    if s==start:
                        ncyc+=1
                        if l2>1e-12: loc=min(loc,d2*math.log(p)/l2)
                    elif s>start and s not in path and len(path)<40: stack.append((s,path+[s],l2,d2))
        simple=(len(edges)==len(S))
        ty='a' if loc==math.inf else ('b' if simple else 'c')
        types.append(ty); best=min(best,loc)
    kind=''.join(sorted(set(types)))
    print(f"{name:26s} K={K} SCC types={kind:4s} theta_1={t1:8.4f}  theta_run={best:8.4f}  gap={best-t1:7.4f}")
    return t1,best,kind
def sfam(S):  # odd n: 3n+1 if n mod 8 in S else n+1 ; even: n/2   (raw form, p=2, m=3)
    return [(1,0,1) if r%2==0 else ((3,1,0) if r in S else (1,1,0)) for r in range(8)]
SYS={
 '3x+1 (shortcut)':(2,1,[(1,0,1),(3,1,1)]),
 'K7 (z-form)':(2,2,[(1,0,1),(1,-1,2),(1,0,1),(3,1,1)]),
 'm3_b':(3,1,[(1,0,1),(4,-1,1),(4,1,1)]),
 'split5_3':(2,2,[(1,0,1),(5,3,0),(1,0,1),(1,3,0)]),
 'split5_1':(2,2,[(1,0,1),(5,1,0),(1,0,1),(1,1,0)]),
 '5x+1':(2,1,[(1,0,1),(5,1,1)]),
}
for S in ([7],[3,7],[1,7],[5,7],[1,5,7],[3,5,7],[1,3],[1,3,5],[1,3,7]):
    SYS['S='+str(S)+' mod 8']=(2,3,sfam(S))
def h16(r):
    if r%2==0: return (1,0,1)
    if r%16 in (5,9): return (1,1,0)
    if r%16==13: return (1,5,0)
    return (3,1,0)
SYS['acc_h16 (settled, type b)']=(2,4,[h16(r) for r in range(16)])
if __name__=='__main__' and len(sys.argv)==1:
    for name,(p,m,tab) in SYS.items():
        for K in ([m,m+1] if p**(m+1)<=32 else [m]):
            analyse(name,p,m,tab,K)

def check():
    """Numerical check of the exponent trichotomy (floats, tolerance 1e-6); exits 1 on failure."""
    ok=True
    for name,(p,m,tab) in SYS.items():
        vals=[]
        for K in ([m,m+1] if p**(m+1)<=32 else [m]):
            t1,tr,kind=analyse(name,p,m,tab,K); vals.append(t1)
            if 'c' in kind: ok&=(t1<tr-1e-6)          # strict inequality with free re-entry
            elif 'b' in kind: ok&=abs(t1-tr)<1e-6     # equality for isolated expanding cycles
            else: ok&=(t1==math.inf)
        ok&=max(vals)-min(vals)<1e-6 if vals[0]!=math.inf else True   # independent of K
    print('CHECK', 'passed' if ok else 'FAILED'); sys.exit(0 if ok else 1)
if __name__=='__main__' and len(sys.argv)>1 and sys.argv[1]=='check': check()
