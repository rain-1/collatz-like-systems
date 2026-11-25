import sys, importlib.util
sys.path.insert(0,'/home/riv/Code/collatz/census')
import systems as S0
def load(p):
    spec=importlib.util.spec_from_file_location("s"+str(abs(hash(p))),p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
D=load('/home/riv/Code/collatz/census/round2/descent/systems.py')
maps={}
for s in S0.SYSTEMS: maps[s['id']]=s['step']
for s in D.SYSTEMS: maps[s['id']]=s['step']
mine=['split5_1_s27','split5_3_s27','m3_b_s8','m3_d_s7','m3_g_s7','div23_5n1_s7','div235_7n1_s11','div23_7n1_s5','desc_split7_1','desc_m3_4n5','desc_s32_plus9']
def it(f,n,s):
    for _ in range(s): n=f(n)
    return n
hits=[]
for a in mine:
  f=maps[a]
  for b,g in maps.items():
    for A in [1,2,3,4,5,6,8,9]:
      for B in range(-12,13):
        if a==b and A==1 and B==0: continue
        for s in (1,2,3):
          for r in (1,2,3):
            ok=True;cnt=0
            for n in range(1,400):
                x=A*n+B
                if x<=0: continue
                try:
                    if A*it(f,n,s)+B!=it(g,x,r): ok=False;break
                except AssertionError: ok=False;break
                cnt+=1
            if ok and cnt>50: hits.append((a,b,A,B,s,r))
print("affine lattice conjugacy hits (a n + b, f^s vs g^r):", hits)
print("PASS (search ran; no hits is evidence, not proof)")
