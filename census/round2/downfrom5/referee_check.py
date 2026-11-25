from systems import get, T
def st(i): return get(i)['step']
# swT9_15: verify Q = sigma T, R = T sigma conj; trap for R by hand classes; check exhaustively via period
s = lambda n: n+1 if n%18 in (9,15) else (n-1 if n%18 in (10,16) else n)
Q = st('swT9_15_s8')
R = lambda n: T(s(n))
inS = lambda n: n%2==1 or n%12==2
# R affine on classes mod 54 ; R(n+108)-R(n) in {72,144}; check closure on n<=108*k
for n in range(1,108*50):
    assert Q(n)==s(T(n))
    assert s(Q(s(n)))==R(n)
    if inS(n): assert inS(R(n)), n
assert not inS(8) and inS(R(8))
# periodicity: for n in S, n+108 in S iff n in S (108 = 0 mod 12, even); R(n+108)-R(n) is 72 or 144 => multiple of 12 and even => same S-membership
for n in range(1,500):
    d=R(n+108)-R(n); assert d%12==0, (n,d)
print("swT9_15 trap OK")
# cube {15}: return period
Q15 = lambda n: (lambda m: m+1 if m%18==15 else (m-1 if m%18==16 else m))(T(n))
x=8
for i in range(1,100):
    x=Q15(x)
    if x==8: print("cube{15} returns at",i); break
# swT3_9_15
Q3=st('swT3_9_15_s8')
for n in range(2,200000):
    if n%3: assert Q3(n)%3 and Q3(n)>n
    else: assert Q3(n)<n
print("swT3 ok")
# shiftT
J=st('shiftT_s8'); o=[2]
for _ in range(6): o.append(J(o[-1]))
print("shiftT chain",o)
img=set(J(n) for n in range(1,30000))
assert 2 not in img and len(img)==29999
# twochanW: bijection and v2 bound
W=st('twochanW_s8')
img={}
for n in range(1,200000):
    m=W(n); assert m>=1 and m not in img; img[m]=n
assert all(m in img for m in range(1,100000))
def v2(n):
    k=0
    while n%2==0: n//=2;k+=1
    return k
for n in range(1,200000):
    a,b=v2(n),v2(W(n))
    assert b==(a-1 if a>=2 else 0) or (a<=1 and b==0), (n,a,b)
    if n%2 and n%6!=5: assert W(n)%6==5
print("twochanW ok")
# swD: trap n !=3 mod 4; P(n+128)-P(n) in {80,320} -> check n<=128 suffices
P=st('swD_s3')
for n in range(1,128*40):
    if n%4!=3: assert P(n)%4!=3,n
for n in range(1,1000):
    assert (P(n+128)-P(n)) in (80,320), (n,P(n+128)-P(n))
print("swD trap ok; P(3)=",P(3))
# which n map to 3 mod 4 in swD, by n mod 128
print(sorted(set(n%128 for n in range(1,128*4) if P(n)%4==3))[:40])
# flipT conj
F=st('flipT_s8')
for n in range(1,100000): assert F(n)==T(n+3)-3
print("flipT ok")
