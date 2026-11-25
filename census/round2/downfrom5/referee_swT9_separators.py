import time
from _common import residue_graph, closure, is_affine_on_classes
from systems import T
s9=lambda n: n+1 if n%18==9 else (n-1 if n%18==10 else n)
R=lambda n: T(s9(n))
assert is_affine_on_classes(R,18)
# sanity: swT9_15 R separates at 12
s915=lambda n: n+1 if n%18 in (9,15) else (n-1 if n%18 in (10,16) else n)
R2=lambda n:T(s915(n))
print("R915 sep K=12:", 8%12 not in closure(residue_graph(R2,12,18),R2(8)%12))
t=time.time(); found=[]
Ks=list(range(601,2501))+[2**a*3**b for a in range(13) for b in range(9) if 2500<2**a*3**b<=20000]
for K in Ks:
    C=closure(residue_graph(R,K,18),R(8)%K)
    if 8%K not in C: found.append(K)
print("R9 separators:",found, time.time()-t)
