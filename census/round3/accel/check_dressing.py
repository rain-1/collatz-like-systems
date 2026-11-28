"""Check for dressing.md (Theorem K: dressed systems).

Claims checked (exact integer arithmetic):
  [K1]  Run identity: for x = p^i q^k w (w coprime to pq), D^(i + e i + k)(x) = w
        and U^(i+k)(x) = w, with every intermediate D-value >= w and no
        intermediate value coprime to pq; tested for all x < 3*10^5 and 2000
        random x < 2^200, for the four dressings in systems.py.
  [K2]  No descent certificate: for n = 0 mod p^N, D^j(n) = (q^e/p)^j n for
        j <= N (tested N <= 40 on random multiples).
  [K3]  dress_23_x1 and dress_32_x1: R(w) = rough(w+1) <= (w+1)/2 < w for every
        rough w >= 5 (algebraic; tested), R(1) = 1, so every orbit is
        eventually periodic and the only cycles are (1 2 3) resp. (1 2).
        Also all orbits from x < 10^5 reach those cycles (consistency).
  [K4]  dress_23_3x1: R(w) = Syracuse(w) = odd(3w+1) on rough w (tested), so
        GLOBAL is equivalent to the 3x+1 problem; dress_23_5x1: the
        rough-return maps of D and of div23_5n1 coincide (tested), cycles
        biject: D-cycle through 1 is (1 6 9 3), div23_5n1's is (1 6 3).
Runtime: about 30 s.
"""
import sys, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import systems as SY
import accel_lib as AL

ok = True


def claim(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok = ok and bool(cond)


random.seed(7)
GS = {"x+1": lambda x: x + 1, "3x+1": lambda x: 3 * x + 1, "5x+1": lambda x: 5 * x + 1}


def val(x, p):
    c = 0
    while x % p == 0:
        x //= p
        c += 1
    return c, x


XS = list(range(1, 300000)) + [random.getrandbits(200) + 1 for _ in range(2000)]
for sid in ("dress_23_x1", "dress_32_x1", "dress_23_3x1", "dress_23_5x1"):
    s = SY.get(sid)
    p, q, e, gname = s["dress"]
    D = s["step"]
    U = SY.undressed(p, q, GS[gname])
    good = True
    for x in XS:
        i, y = val(x, p)
        k, w = val(y, q)
        z = x
        for t in range(i + e * i + k):
            z = D(z)
            if t < i + e * i + k - 1:
                if z < w or (z % p and z % q):
                    good = False
        good &= z == w
        z = x
        for _ in range(i + k):
            z = U(z)
        good &= z == w
    claim(f"[K1] {sid}: run identity D^(i+ei+k)(p^i q^k w) = w, U^(i+k)(...) = w", good)
    good = True
    for N in range(1, 41):
        n = p ** N * random.randrange(1, 10 ** 6)
        z = n
        for j in range(1, N + 1):
            z = D(z)
            good &= z * p ** j == q ** (e * j) * n and z > n
    claim(f"[K2] {sid}: D^j(n) = (q^e/p)^j n > n for n = 0 mod p^N, j <= N", good)

# [K3]
for sid, cyc in (("dress_23_x1", [1, 3, 2]), ("dress_32_x1", [1, 2])):
    s = SY.get(sid)
    D = s["step"]
    good = all(SY.rough(w + 1, (2, 3)) * 2 <= w + 1 for w in range(5, 300000) if w % 2 and w % 3)
    good &= SY.rough(2, (2, 3)) == 1
    claim(f"[K3] {sid}: rough(w+1) <= (w+1)/2 for rough w in [5, 3e5); R(1) = 1", good)
    c = AL.cycle_of(D, 1)
    claim(f"[K3] {sid}: the cycle through 1 is {c}", sorted(c) == sorted(cyc))
    claim(f"[K3] {sid}: all x < 1e5 reach it (consistency)",
          all(min(AL.cycle_of(D, x)) == 1 for x in range(1, 100000)))

# [K4]
s = SY.get("dress_23_3x1")
D = s["step"]


def rough_return(F, w):
    z = F(w)
    while z % 2 == 0 or z % 3 == 0:
        z = F(z)
    return z


RW = [w for w in range(1, 200000) if w % 2 and w % 3] + \
     [w for w in (random.getrandbits(200) for _ in range(3000)) if w % 2 and w % 3]
claim("[K4] dress_23_3x1: rough-return map = Syracuse odd(3w+1)",
      all(rough_return(D, w) == SY.odd_part(3 * w + 1) for w in RW))
claim("[K4] dress_23_3x1: cycle through 1 is (1 4 6 9 3)", AL.cycle_of(D, 1) == [1, 4, 6, 9, 3])
s = SY.get("dress_23_5x1")
D = s["step"]
DIV = SY.undressed(2, 3, lambda x: 5 * x + 1)
claim("[K4] dress_23_5x1: rough-return maps of D and div23_5n1 coincide",
      all(rough_return(D, w) == rough_return(DIV, w) for w in RW))
claim("[K4] cycles through 1: D (1 6 9 3), div23_5n1 (1 6 3)",
      AL.cycle_of(D, 1) == [1, 6, 9, 3] and AL.cycle_of(DIV, 1) == [1, 6, 3])

print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
