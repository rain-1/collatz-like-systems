"""The renormalised map Theta on K in F_3[s] (coefficient lists, low degree first):
   k0=1: ((1+s)^2 K - 1)/s + 1 ;  k0=0 or 2: ((1+s) K - k0)/s."""
def theta(K):
    k0=K[0] if K else 0
    if k0==1:
        Q=[0]*(len(K)+2)
        for i,a in enumerate(K):
            Q[i]=(Q[i]+a)%3; Q[i+1]=(Q[i+1]+2*a)%3; Q[i+2]=(Q[i+2]+a)%3
        Q=Q[1:]; Q[0]=(Q[0]+1)%3
    else:
        Q=[0]*(len(K)+1)
        for i,a in enumerate(K):
            Q[i]=(Q[i]+a)%3; Q[i+1]=(Q[i+1]+a)%3
        Q=Q[1:]
    while Q and Q[-1]==0: Q.pop()
    return Q
if __name__=='__main__':
    K=[1]; times=[]; N=200000
    for n in range(N):
        if K and K[0]==1: times.append(n)
        K=theta(K)
    gaps=[b-a for a,b in zip(times,times[1:])]
    print('A-steps:',len(times),'final degree',len(K)-1,'steps',N)
    print('first gaps:',gaps[:80])
    import collections
    print('max gap by position (blocks of 500):',[max(gaps[i:i+500]) for i in range(0,len(gaps)-500,2000)])
    # gap vs degree: is gap <= c * 3^ceil(log3 deg)?
    import math
    worst=0
    for i,g in enumerate(gaps):
        D=i+1  # degree after i+1 A steps roughly
        worst=max(worst,g/ (3**math.ceil(math.log(D+1,3)+1e-9)))
    print('max gap / 3^ceil(log3(D+1)) :',worst)
