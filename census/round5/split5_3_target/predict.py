"""split5_3 at the two-survivor depth b = ceil(12m/5): the Haar prediction 2^m P(b) (exact integer path counts; logs printed as floats)
and the exact brute-force counts for small m (from ../../round4/lead/s53.txt, actual drops).

Coordinates N = n + 3:  N = 0 mod 4 -> 5N/4 (two halvings);  N = 2 mod 4 -> N/2 + 3;  N odd -> (N+3)/2.
P(b) = Haar measure of the 2-adic N whose slope 5^a / 2^h is >= 1 at every step end with h <= b.
States: F (next digits fresh), E (value known to be even, after the N = 2 mod 4 step)."""
import math, sys
L5=math.log2(5)
def lg(x):
    if x==0: return float('-inf')
    k=x.bit_length()
    return k-60+math.log2(x>>(k-60)) if k>60 else math.log2(x)
def table(bmax):
    """Exact integer counts.  A path at halving count h in state F is a cylinder of measure 2^-h, in
    state E of measure 2^-(h+1); every transition keeps the integer count.  Returns log2 P(h)."""
    pw5=[1]
    layers=[dict() for _ in range(bmax+3)]
    layers[0][(0,'F')]=1
    P=[0.0]*(bmax+1)
    for h in range(bmax+1):
        lay=layers[h]; f=e=0
        for (a,st),w in lay.items():
            while len(pw5)<=a: pw5.append(pw5[-1]*5)
            if pw5[a] < (1<<h): continue          # dropped: 5^a < 2^h  (exact)
            if st=='F':
                f+=w
                for key,hh in (((a,'F'),h+1),((a+1,'F'),h+2),((a,'E'),h+1)):
                    layers[hh][key]=layers[hh].get(key,0)+w
            else:
                e+=w
                for key,hh in (((a+1,'F'),h+2),((a,'E'),h+1)):
                    layers[hh][key]=layers[hh].get(key,0)+w
        P[h]=lg(2*f+e)-h-1
        layers[h]=None
    return P
def Pb(bmax):
    P=table(bmax); return P
if __name__=='__main__':
    mmax=int(sys.argv[1]) if len(sys.argv)>1 else 1500
    bmax=math.ceil(12*mmax/5)+2
    # recompute keeping the run-crossing correction approximate: use alive mass at h=b (lower) and h=b-1 (upper)
    P=table(bmax)
    print("decay exponent of P near b=%d: %.5f  (1-h = 0.41932)"%(bmax-2, -(P[bmax-2]-P[bmax-402])/400))
    print("   m      b   log2 P at h=b, b-1 (step-end masses)   log2(2^m P), larger of the two   predicted count")
    for m in list(range(8,40,4))+[50,75,100,150,200,300,500,750,1000,1500,2000,3000]:
        if m>mmax: break
        b=math.ceil(12*m/5); lo=P[b]; up=max(P[b],P[b-1])
        print(f"{m:5d} {b:6d}   [{lo:9.3f},{up:9.3f}]        {m+up:9.3f}        {2**(m+up):.3e}")
