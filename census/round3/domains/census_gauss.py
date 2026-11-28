import sys, time, random; import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import rings as RG, gcert as GC
G=RG.GAUSS; m=int(sys.argv[1]); U5=(1,2)
Tm0=GC.GaussMap(G,m,lambda r:((1,0),(1,0)))
odd=[r for r,v in Tm0.table.items() if v is not None]
masks=range(2**len(odd)) if len(sys.argv)<3 else random.Random(1).sample(range(2**len(odd)),int(sys.argv[2]))
st={'CERT':0,'OBST':0,'UNK':0}; t0=time.time(); deep=[]
for mask in masks:
    S={odd[i] for i in range(len(odd)) if mask>>i&1}
    Tm=GC.GaussMap(G,m,lambda r:(U5,(1,0)) if r in S else ((1,0),(1,0)))
    mean,cyc=GC.max_mean_cycle(GC.residue_graph(Tm))
    c=GC.certificate(Tm,maxK=50,maxnodes=50000)
    if c['ok']:
        st['CERT']+=1; deep.append((c['k'],c['K'],c['size'],len(S),mask))
        assert mean<0,(mask,mean)
    elif mean>0:
        GC.verify_obstruction(Tm,cyc); st['OBST']+=1
    else: st['UNK']+=1; print('UNK',mask,mean,c)
print(st,time.time()-t0)
import json; json.dump(deep,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'scratch','gscan_m%d.json'%m),'w'))
deep.sort(reverse=True); print(deep[:8])
print('max |S| cert', max(d[3] for d in deep), [d for d in deep if d[3]==max(x[3] for x in deep)][:5])
