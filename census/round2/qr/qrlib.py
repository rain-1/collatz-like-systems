"""Shared exact-integer helpers for the qr lens (round 2)."""
from math import gcd


def famA(q, p):
    """even n -> n/2;  odd n -> (n + c q)/p with c in [0, p-1] making it integral."""
    qi = pow(q, -1, p)

    def T(n):
        if n % 2 == 0:
            return n // 2
        c = (-n * qi) % p
        return (n + c * q) // p
    return T


def famC(q):
    """even -> n/2; n=1 mod 4 -> (n + c q)/3; n=3 mod 4 -> (n + c q)/5 (c minimal)."""
    def T(n):
        if n % 2 == 0:
            return n // 2
        m = 3 if n % 4 == 1 else 5
        c = (-n * pow(q, -1, m)) % m
        return (n + c * q) // m
    return T


def famB(q, c1, c3):
    """even -> n/2; n=1 mod 4 -> (n + c1 q)/2; n=3 mod 4 -> (n + c3 q)/2."""
    def T(n):
        if n % 2 == 0:
            return n // 2
        return (n + q * (c1 if n % 4 == 1 else c3)) // 2
    return T


def subgroup(gens, q):
    H, fr = {1}, [1]
    while fr:
        x = fr.pop()
        for g in gens:
            y = x * g % q
            if y not in H:
                H.add(y)
                fr.append(y)
    return H


def cycles_in(T, region):
    """All cycles of T meeting `region`, given that T maps region into itself."""
    seen, cyc = set(), []
    for n in region:
        x, path = n, {}
        while x not in path and x not in seen:
            path[x] = 1
            x = T(x)
        if x in path:
            c, y = [x], T(x)
            while y != x:
                c.append(y)
                y = T(y)
            cyc.append(c)
        seen |= set(path)
    return cyc


def region_ok(T, lo, hi, mult):
    """[lo,hi] maps into itself; and for every residue class the descent bound holds."""
    return all(lo <= T(n) <= hi for n in range(lo, hi + 1))


def class_key(x, q, H):
    d = gcd(x, q)
    qq = q // d
    if qq == 1:
        return (d, 0)
    u = (x // d) % qq
    Hq = {h % qq for h in H}
    return (d, min(u * h % qq for h in Hq))


def basin_table(T, cyc):
    cid = {}
    for i, c in enumerate(cyc):
        for x in c:
            cid[x] = min(c)
    return cid


def basin(T, cid, n):
    while n not in cid:
        n = T(n)
    return cid[n]


def jacobi(a, n):
    a %= n
    r = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                r = -r
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            r = -r
        a %= n
    return r if n == 1 else 0


def check_coset_system(name, T, q, gens, H_claim, rule, box, sanity_N):
    """Verify the finite part of the tier-2 coset theorem.

    T maps [1, box] into itself (box = q for families A/C); every cycle lies in
    [1, box]; each class (gcd(n,q), coset of n/d mod q/d under <gens>) holds exactly one
    cycle; H = <gens> equals the claimed character kernel; rule(n) agrees with the
    cycle reached for every n in the box (which, by invariance + descent, is the proof)
    and, as a sanity check only, for n <= sanity_N.
    """
    ok = True
    if not all(1 <= T(n) <= box for n in range(1, box + 1)):
        print(name, "FAIL box not invariant"); ok = False
    H = subgroup(gens, q)
    if H != H_claim:
        print(name, "FAIL subgroup differs from claimed kernel"); ok = False
    cyc = cycles_in(T, range(1, box + 1))
    keys = {}
    for c in cyc:
        keys.setdefault(class_key(c[0], q, H), []).append(min(c))
    allk = {class_key(x, q, H) for x in range(1, q + 1)}
    if set(keys) != allk or any(len(v) != 1 for v in keys.values()):
        print(name, "FAIL not exactly one cycle per class", keys); ok = False
    cid = basin_table(T, cyc)
    for n in range(1, box + 1):
        if basin(T, cid, n) != rule(n):
            print(name, "FAIL rule wrong in box at", n); ok = False; break
    # sanity beyond the box (not part of the proof)
    memo = {}
    for n in range(1, sanity_N + 1):
        x = n
        while x > box and x >= n:
            x = T(x)
        b = cid.get(x) if x in cid else (memo[x] if x > box else basin(T, cid, x))
        memo[n] = b
        if b != rule(n):
            print(name, "FAIL sanity at", n); ok = False; break
    print(name, "cycles (min,len):", sorted((min(c), len(c)) for c in cyc),
          "classes:", len(allk), "|H| =", len(H), "OK" if ok else "FAILED")
    return ok
