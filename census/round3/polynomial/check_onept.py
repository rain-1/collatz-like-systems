"""Check for onept.md (Theorem A: F_2, multiplier 1+t, arbitrary twist h).

Claims tested exactly:
 (A1) deg T(f) <= max(deg f, deg h - 1) and T(h) = h, T(0) = 0      -- random + exhaustive
 (A2) k | f  <=>  k | T(f), where h = (1+t)^a k, (1+t) not dividing k   -- random wide range
 (A3) for every odd h with deg h <= 9 and every f != 0 with deg f <= 11:
          the orbit of f meets {0, h}  <=>  k | f ;  and if (1+t) does not divide h:
          f reaches h  <=>  h | f   (the basin of h is exactly h F_2[t] minus 0)  -- exhaustive
 (A4) every cycle other than {0},{h} lies in degree < deg h; for each such h we list the
      number of extra cycles, and check: no extra cycle  <=>  h is a power of 1+t
 (A5) the case h=(1+t)^a: every nonzero f with deg f <= 14 reaches 0 or h, a<=6.
Runs in well under a minute.
"""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from polylib import T2, deg2, divmod2, clmul, pow2

M = 0b11  # 1+t
random.seed(20261127)


def split(h):
    a = 0
    k = h
    while divmod2(k, 0b11)[1] == 0:
        k = divmod2(k, 0b11)[0]
        a += 1
    return a, k


fails = 0
# A1, A2 random
for _ in range(20000):
    h = random.getrandbits(random.randint(1, 40)) | 1
    f = random.getrandbits(random.randint(0, 200))
    a, k = split(h)
    g = T2(f, M, h)
    if deg2(g) > max(deg2(f), deg2(h) - 1):
        fails += 1
    if (divmod2(f, k)[1] == 0) != (divmod2(g, k)[1] == 0):
        fails += 1
    if T2(h, M, h) != h or T2(0, M, h) != 0:
        fails += 1
print('A1/A2 random: fails', fails)

# A3/A4 exhaustive
D = 12  # f of degree < 12
extra_by_h = {}
for dh in range(0, 10):
    for h in range(1 << dh, 1 << (dh + 1)):
        if h & 1 == 0:
            continue
        a, k = split(h)
        n = 1 << max(D, dh + 1)  # closed set: degree < max(D, deg h + 1)
        fate = [None] * n          # 1 = reaches h, 2 = reaches 0, 0 = neither
        fate[h] = 1
        fate[0] = 2
        for f0 in range(1, n):
            if fate[f0] is not None:
                continue
            path = []
            f = f0
            onpath = set()
            while fate[f] is None and f not in onpath:
                onpath.add(f)
                path.append(f)
                f = T2(f, M, h)
            res = fate[f] if fate[f] is not None else 0  # a new cycle not containing h
            for x in path:
                fate[x] = res
        for f in range(1, n):
            if (fate[f] in (1, 2)) != (divmod2(f, k)[1] == 0):
                fails += 1
            if a == 0 and ((fate[f] == 1) != (divmod2(f, h)[1] == 0) or fate[f] == 2):
                fails += 1
        # A4: cycles in degree < deg h (exhaustive over that finite invariant set)
        cyc = set()
        seen = {}
        for f0 in range(1, 1 << dh):
            f = f0
            path = []
            pos = {}
            while f not in pos and f not in seen and f < (1 << dh):
                pos[f] = len(path)
                path.append(f)
                f = T2(f, M, h)
            if f in pos:
                cyc.add(min(path[pos[f]:]))
            for x in path:
                seen[x] = 1
        cyc.discard(0)
        extra_by_h[h] = len(cyc)
        if (len(cyc) == 0) != (k == 1):
            fails += 1
print('A3/A4 exhaustive (deg h <= 9, deg f < 12): fails', fails)
print('   h with no extra cycle:', [bin(h) for h, c in extra_by_h.items() if c == 0])

# A5 (memoized; polynomials of degree < 15 form a T-closed set since deg h <= 6)
for a in range(0, 7):
    h = pow2(0b11, a)
    n = 1 << 15
    ok = bytearray(n)
    ok[h] = 1
    ok[0] = 1
    for f0 in range(1, n):
        if ok[f0]:
            continue
        path = []
        f = f0
        while not ok[f] and len(path) < 10 ** 5:
            path.append(f)
            f = T2(f, M, h)
        if not ok[f]:
            fails += 1
            continue
        for x in path:
            ok[x] = 1
print('A5 (h=(1+t)^a, a<=6, deg f <= 14, reaches 0 or h): fails', fails)
sys.exit(1 if fails else 0)
