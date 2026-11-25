import sys, re
from systems import BY_ID, CT58_TRAPS
# qr7 independent: memoized fate to 10^6
S=BY_ID['up_qr7']['step']
fate={}
def f(n):
    path=[];seen=set()
    while True:
        if n in fate: r=fate[n];break
        if n%28==3: r='D';break
        if n in seen:
            r={1:'C1',2:'C1',4:'C1',8:'C1',7:'C7',14:'C7'}.get(n,'X');break
        seen.add(n);path.append(n);n=S(n)
    for p in path: fate[p]=r
    return r
bad=[n for n in range(1,10**6) if f(n)!=('D' if n%7 in(3,5,6) else 'C7' if n%7==0 else 'C1')]
print('qr7 bad',bad[:5])
# tok3: MSB regex vs sim to 2^20
S=BY_ID['up_tok3']['step']
rx=re.compile(r'(1(1|00)*01|1)0*')
fate={}
def g(n):
    path=[];seen=set()
    while True:
        if n in fate: r=fate[n];break
        if n%4==3: r=False;break
        if n in seen: r=(n in(1,2,4));break
        seen.add(n);path.append(n);n=S(n)
    for p in path: fate[p]=r
    return r
K=21
bad=[n for n in range(1,1<<K) if g(n)!=bool(rx.fullmatch(bin(n)[2:]))]
print('tok3 bad',bad[:5])
fib=[0,1]
while len(fib)<K+4: fib.append(fib[-1]+fib[-2])
cnt=0;ok=True;c=[]
for k in range(1,K+1):
    cnt=sum(1 for n in range(1,1<<k) if fate.get(n,g(n)))
    c.append(cnt==fib[k+2]-1)
print('fib',all(c))
from fractions import Fraction
traps={'up_ct11':(4,lambda r:r%4==3),'up_ct35':(32,lambda r:r%8==7 or r%32==27),
       'up_ct58':(256,lambda r:r%256 in CT58_TRAPS),'up_ct3':(8,lambda r:r%8==7)}
def tree(M,trapped,maxdepth=60):
    # explore residue classes r mod 2^d (x = r + 2^d y): track x_t = (a*y + c) with a=3^k * 2^{d-t}...
    # represent x_t = (3^k * x + b)/2^t exactly for x = r mod 2^d; trap decided on x_t mod M -> need d >= t+log2 M
    import math
    m=M.bit_length()-1
    stack=[(0,0)] # (r, d) classes; we stop at first t with 3^k<2^t
    worst_thr=0;maxt=0;open_=0
    stack=[(r,m) for r in range(1<<m)]
    while stack:
        r,d=stack.pop()
        # simulate as far as determined: positions t with t+m<=d
        x=r+(1<<d)*0; k=0;b=0; t=0; trappedflag=False;stopped=False
        xs=r
        while t+m<=d:
            # x_t residue known mod 2^{d-t}
            if trapped(xs % M): trappedflag=True;break
            if 3**k<2**t and t>0: stopped=True;break
            if xs%2: k+=1; b=3*b+2**t; xs=(3*xs+1)//2
            else: xs//=2
            t+=1
        if trappedflag: continue
        if not stopped and t+m<=d+0 and 3**k<2**t and t>0: stopped=True
        if stopped:
            # need (3^k x + b)/2^t < x  <=> x > b/(2^t-3^k)
            thr=b//(2**t-3**k)+1   # descent for x >= thr
            worst_thr=max(worst_thr,thr);maxt=max(maxt,t)
            continue
        if d>=maxdepth: open_+=1;continue
        stack+= [(r,d+1),(r+(1<<d),d+1)]
    return worst_thr,maxt,open_
for k,(M,tr) in traps.items():
    print(k,tree(M,tr,40 if k!='up_ct3' else 30))
# stopping-time (Terras) trees: expected (threshold, max stopping time, open branches)
exp={'up_ct11':(2,2,0),'up_ct35':(5,5,0),'up_ct58':(25,8,0)}
OK=True
for k,v in exp.items():
    got=tree(*traps[k],40)
    if got!=v: OK=False;print('tree mismatch',k,got)
# table [1,thr) for each: untrapped orbits end in (1 2)
for k,(M,tr) in traps.items():
    if k=='up_ct3': continue
    S=BY_ID[k]['step']
    for n in range(1,exp[k][0]):
        x=n;seen=set()
        while x not in seen and not tr(x%M): seen.add(x);x=S(x)
        if not tr(x%M) and x not in (1,2): OK=False;print('table',k,n)
# ct3: tree does not close (open branches persist at depth 30)
if tree(*traps['up_ct3'],30)[2]==0: OK=False
# counterexample to 'above threshold => open': trap evens (n -> n+2), odd n -> (3n+1)/2.
# Allowed words = 1^inf only (density 1), window method fails, yet every n>=1 is trapped
# because the only 2-adic integer with all-ones parity word is -1.
def Sx(n): return n+2 if n%2==0 else (3*n+1)//2
for n in range(1,10**5):
    x=n
    for _ in range(60):
        if x%2==0: break
        x=Sx(x)
    if x%2: OK=False;print('evens-trap',n)
assert 'bad' in dir()
print('PASS' if OK and not bad else 'FAIL'); sys.exit(0 if OK and not bad else 1)
