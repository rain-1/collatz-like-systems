"""Test of the conjecture: for b beyond the horizon (b > m), the number of n in [2^m, 2^{m+1}) that have
not dropped after b halvings should be 2^m * P(b), where P(b) is the Haar frequency, measured in the
top octave (valid there because b <= top).  Prints observed vs expected, pooled by the ratio b/m."""
import sys, math
def load(f):
    d={}
    for l in open(f):
        v=l.split(); d[int(v[0])]=list(map(int,v[1:]))
    return d
for name,f,never in (('split5_3','s53.txt',5),('3x+1','c31.txt',0),('K7','k7.txt',0)):
    d=load(f); top=max(d); P=[d[top][b]/2**top for b in range(top+1)]
    print(f"\n{name}: top octave 2^{top}; P(b) decays like 2^(-{-math.log2(P[top]/P[top-8])/8:.4f} b) near b={top}  (1-h predicted)")
    print("  ratio b/m     cells   observed   expected   obs/exp   chi2/cell")
    bins={}
    for m in range(10,top-1):
        for b in range(m+1,top+1):
            e=2**m*P[b]; o=d[m][b]
            if e<5: continue
            k=min(int((b/m-1)/0.25),7)
            s=bins.setdefault(k,[0,0,0.0,0.0]); s[0]+=1; s[1]+=o; s[2]+=e; s[3]+=(o-e)**2/e
    for k in sorted(bins):
        c,o,e,x=bins[k]; print(f"  {1+0.25*k:.2f}-{1.25+0.25*k:.2f}  {c:6d} {o:10d} {e:10.1f}   {o/e:6.4f}   {x/c:6.2f}")
    # longest survivors per octave
    worst=[]
    for m in range(10,top+1):
        bmax=max(b for b in range(len(d[m])-1) if d[m][b]>0 and d[m][b]>(d[m][-1]))
        worst.append(f"{m}:{bmax/m:.2f}")
    print("  max (halvings/m) by octave:", ' '.join(worst[-14:]), ' never-drop counts in top octave:', d[top][-1])
