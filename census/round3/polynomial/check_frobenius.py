"""Check for frobenius.md (Theorem C and Proposition C').

 (C1) for m = M^2 + t (M(0)=1), h = 1, phi(u) = (M u)^2:  T^2(phi(u)) = phi(T(u))
      -- 20000 random u per M, M ranging over all M with M(0)=1, deg M <= 4
 (C2) Proposition C': for m = m_e(t^2) + t m_o(t^2), h = h_e(t^2) + t h_o(t^2) with
      (i) m_o(0) + h_o(0) = 1 and (ii) h_e (1 + m_o) = m_e h_o, and A(t) any polynomial:
      T_{m,h}^2(A(t^2)) = A'(t^2) with A' = T_{m,h'}(A), h' = t(1+m_o)h_o + m_e h_e.
      -- all (m,h) with deg m <= 5, deg h <= 5 satisfying (i),(ii), 300 random A each
 (C3) for m = M^2, h = H^2:  T_{m,h}^2(F^2) = (T_{M,H} F)^2   -- random
 (C4) corollary for m = 1+t+t^2, h=1: (1+t)^(2^(k+1)-2) is periodic with period exactly 2^(k+2),
      k = 0..9 (direct simulation)
"""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from polylib import T2, clmul, frob2, pow2, deg2

random.seed(7)
fails = 0


def even_odd(a):
    e = o = 0
    i = 0
    while a:
        if a & 1:
            if i % 2 == 0:
                e |= 1 << (i // 2)
            else:
                o |= 1 << (i // 2)
        a >>= 1
        i += 1
    return e, o


# C1
cnt = 0
for M in range(1, 1 << 5, 2):
    m = frob2(M) ^ 2
    for _ in range(20000):
        u = random.getrandbits(random.randint(0, 120))
        phi = lambda x: frob2(clmul(M, x))
        if T2(T2(phi(u), m), m) != phi(T2(u, m)):
            fails += 1
        cnt += 1
print('C1: %d tests, fails %d' % (cnt, fails))

# C2
cnt = 0
cases = 0
for m in range(1, 1 << 6, 2):
    me, mo = even_odd(m)
    for h in range(1, 1 << 6, 2):
        he, ho = even_odd(h)
        if (mo & 1) ^ (ho & 1) != 1:
            continue
        if clmul(he, 1 ^ mo) != clmul(me, ho):
            continue
        cases += 1
        hp = (clmul(1 ^ mo, ho) << 1) ^ clmul(me, he)
        for _ in range(300):
            A = random.getrandbits(random.randint(0, 60))
            lhs = T2(T2(frob2(A), m, h), m, h)
            rhs = frob2(T2(A, m, hp))
            if lhs != rhs:
                fails += 1
            cnt += 1
print('C2: %d (m,h) cases, %d tests, fails %d' % (cases, cnt, fails))

# C3
for _ in range(20000):
    M = random.getrandbits(random.randint(0, 8)) | 1
    H = random.getrandbits(random.randint(0, 8)) | 1
    Fp_ = random.getrandbits(random.randint(0, 80))
    if T2(T2(frob2(Fp_), frob2(M), frob2(H)), frob2(M), frob2(H)) != frob2(T2(Fp_, M, H)):
        fails += 1
print('C3: fails', fails)

# C4
for k in range(0, 10):
    f0 = pow2(0b11, (1 << (k + 1)) - 2)
    f = f0
    L = 0
    while True:
        f = T2(f, 0b111)
        L += 1
        if f == f0 or L > (1 << (k + 3)):
            break
    if f != f0 or L != (1 << (k + 2)):
        fails += 1
    print('C4: k=%d  (1+t)^%d has period %d' % (k, (1 << (k + 1)) - 2, L))
print('fails', fails)
sys.exit(1 if fails else 0)
