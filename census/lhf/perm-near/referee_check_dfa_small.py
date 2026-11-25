import itertools,sys
sys.path.insert(0,'/home/riv/Code/collatz/census/lhf/perm-near')
from _lib import Q
def digs(n,b,lsd):
    d=[]
    while n: d.append(n%b); n//=b
    return d if lsd else d[::-1]
def search(F,seed,b,S,lsd,M=3000):
    orb=[];x=seed
    for _ in range(26): x=F(x); orb.append(x)
    ns=list(range(1,M+1)); D={n:digs(n,b,lsd) for n in set(ns)|set(orb)|{seed}|{F(n) for n in ns}}
    found=0
    for delta in itertools.product(range(S),repeat=S*b):
        def run(n):
            s=0
            for c in D[n]: s=delta[s*b+c]
            return s
        st={n:run(n) for n in D}
        for acc in range(1,2**S-1):
            A=lambda n:(acc>>st[n])&1
            if A(seed): continue
            if not all(A(o) for o in orb): continue
            if all(A(F(n)) for n in ns if A(n)): return delta,acc
    return None
for b,S in [(2,3),(3,2),(2,2)]:
    for lsd in (False,True):
        print(b,S,lsd,search(Q,8,b,S,lsd))
print('control 3n base3', search(lambda n:3*n,8,3,2,True))
print('b2 S4', [search(Q,8,2,4,l,M=400) for l in (False,True)])
