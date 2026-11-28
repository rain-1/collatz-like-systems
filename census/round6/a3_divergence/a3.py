"""A3 over F_3: f(0)=0: f/t; f(0)=1: (1+t^2)(f-1)/t; f(0)=2: (f-2)/t + 1.
Polynomials as tuples of coefficients mod 3 (low degree first)."""
def step(f):
    f=list(f)
    c=f[0] if f else 0
    if c==0: g=f[1:]
    elif c==1:
        h=f[1:]                      # (f-1)/t
        g=[0]*(len(h)+2)
        for i,a in enumerate(h):
            g[i]=(g[i]+a)%3; g[i+2]=(g[i+2]+a)%3
    else:
        g=f[1:]                      # (f-2)/t
        if not g: g=[0]
        g[0]=(g[0]+1)%3
    while g and g[-1]==0: g.pop()
    return tuple(g)
def deg(f): return len(f)-1
def show(f): return ''.join(map(str,f))
if __name__=='__main__':
    f=(1,1,1,0,2,2,0,2)
    hist=[];seen={}
    for n in range(6000):
        hist.append((deg(f),f[0] if f else 0))
        f=step(f)
    d=[h[0] for h in hist]
    print('degrees at n=0,500,..:',d[::500])
    # branch sequence periodicity?
    b=''.join(str(h[1]) for h in hist)
    print(b[:240])
    for p in range(1,400):
        if all(b[i]==b[i+p] for i in range(2000,5000)): print('eventual period of branch word:',p); break
    else: print('no small period in branch word')
    # degree increments over windows
    import collections
    print('branch frequencies late:',collections.Counter(b[3000:6000]))
