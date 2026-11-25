from fractions import Fraction as F
import math
SET={1,3,5,7,9,11,13,15,17,21,23,25,29}
def res(x,m):  # 2-adic residue of rational with odd denom
    return (x.numerator*pow(x.denominator,-1,m))%m
def T(x):
    r=res(x,64)
    if r%2==0: return x/2
    return 3*x+1 if r%32 in SET else x+1
x=F(-227,115); orb=[x]; 
for i in range(12): x=T(x); orb.append(x)
print('12-cycle closes:',orb[-1]==orb[0], [res(o,32) for o in orb[:12]])
# odd-map steps and up/down
odds=[o for o in orb[:12] if res(o,2)==1]
def S(x):
    y=T(x)
    while res(y,2)==0: y=y/2
    return y
print('odd points',odds,'S rises?',[ (res(o,32), res(o,4)==3 and res(o,32) in SET) for o in odds])
# LMN monotonic sweep
def F_(k,lowlog,c1,c0,logA2,b):
    return lowlog(k)-math.log(c1*k+c0)-24.34*max(math.log(b(k))+0.14,21)**2*logA2
cfgs={'040':(lambda k:(k+1)*math.log(2)-math.log(3),1.53,.42,math.log(5),lambda k:(k*math.log2(5)+1)/math.log(5)+k,25000),
'053':(lambda k:(2*k+1)*math.log(2)-math.log(3),5.455,.613,math.log(7),lambda k:2.443*(6.3116*k+.6126)+.52,15100),
'054':(lambda k:k*math.log(3)+math.log(1-5/3**min(k,600)),3.2225,5.561,math.log(3),lambda k:(5.1558*k+8.897)*(1/math.log(3)+math.log(2)/math.log(3))+1,10800),
'055':(lambda k:(k+1)*math.log(2),2.558,1.578,math.log(3),lambda k:(3.224*k+1.5779)*(math.log2(3)/math.log(3)+1)+1/math.log(3),17100)}
for n,(ll,c1,c0,la,b,k0) in cfgs.items():
    ks=[k0]+[int(k0*1.01**i) for i in range(1,3000)]
    vals=[F_(k,ll,c1,c0,la,b) for k in ks]
    print(n,'F(k0)=%.2f'%vals[0],'min over sweep to %.1e: %.2f'%(ks[-1],min(vals)), 'increasing',all(a<c for a,c in zip(vals,vals[1:])))
