import sys, importlib.util, itertools
from math import gcd
sys.path.insert(0,'/home/riv/Code/collatz/census')
import systems as s1
spec=importlib.util.spec_from_file_location("d","/home/riv/Code/collatz/census/round2/downfrom5/systems.py")
d=importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
T=s1.get('perm_1932_s8')['step']; U=s1.get('perm_1932inv_s8')['step']; B=s1.get('perm_b_s7')['step']
P=d.get('flipT_s8')['step']; Q=d.get('swT9_s8')['step']
print(s1.get('perm_b_s7')['seed'], d.get('flipT_s8')['seed'], d.get('swT9_s8')['seed'], s1.get('perm_1932inv_s8')['seed'])
N=10**5
assert all(U(T(n))==n and T(U(n))==n for n in range(1,N))
assert all(B(n)==T(n+1)-1 for n in range(1,N))
assert all(P(n)==T(n+3)-3 for n in range(1,N))
# Q: sigma(T(n)) and Q=T on 0,1,2 mod 27; bijectivity sample
def sig(m):
    r=m%18; return m+1 if r==9 else m-1 if r==10 else m
assert all(Q(n)==sig(T(n)) for n in range(1,N))
assert all(Q(n)==T(n) for n in range(1,N) if n%27 in (0,1,2))
img=set(Q(n) for n in range(1,3*N)); assert all(m in img for m in range(1,N))
# brute-force residue graph: edges from actual n, subset of true edges
def sc_brute(K):
    L=K*27//gcd(K,27)
    adj=[set() for _ in range(K)]
    for n in range(1,3*L+1):
        adj[n%K].add(Q(n)%K)
    def reach(adj,s):
        seen={s};st=[s]
        while st:
            v=st.pop()
            for w in adj[v]:
                if w not in seen: seen.add(w); st.append(w)
        return len(seen)==K
    radj=[set() for _ in range(K)]
    for v in range(K):
        for w in adj[v]: radj[w].add(v)
    return reach(adj,0) and reach(radj,0)
bad=[K for K in range(1,301) if not sc_brute(K)]
print('non-SC K<=300:',bad)
for K in [324,432,486,576,648,729,864,972,1152,1296,1458,2187,2592]:
    print(K, sc_brute(K))
