import numpy as np, sys
N=int(sys.argv[1]) if len(sys.argv)>1 else 3_000_000
g=np.zeros(N+1,dtype=np.int8)   # 1=A (cycle 1,6,3), 2=B (5,13,10), 3=17
for n in range(1,N+1):
    if n<=17:
        m=n; seen=[]
        while m not in (1,5,17): m = m//2 if m%2==0 else (m+17*(m%3))//3
        g[n]={1:1,5:2,17:3}[m]
    else:
        t = n//2 if n%2==0 else (n+17*(n%3))//3
        g[n]=g[t]
np.save('g.npy',g)
u=g[1:]
print('density A,B,17:',[(u==k).mean() for k in (1,2,3)], 'B among units', (u==2).sum()/((u!=3).sum()), 5/16)
# factor complexity
for w in range(1,15):
    code=np.zeros(N-w+1,dtype=np.int64)
    for i in range(w): code=code*4+g[1+i:N-w+2+i]
    half=np.unique(code[:(N-w+1)//2]).size
    full=np.unique(code).size
    print(w,half,full)
