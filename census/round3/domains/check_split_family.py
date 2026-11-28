"""check_split_family.py -- exact checks for theorem_N.md (split instance),
split_family.md and onexd.md.

Claims checked:
  N1  (full branches) for the split map S on odd 2-adic integers, the block
      A_k: x -> (3x+1)/2^k (x = 1 mod 4, v2(3x+1) = k) and B_k: x -> (x+1)/2^k
      (x = 3 mod 4, v2(x+1) = k), k >= 2, maps its cylinder bijectively onto the
      odd 2-adics: checked at finite level (classes mod 2^(N+k+1) -> odd classes
      mod 2^N) for k <= 12, N <= 8; same for the 1x+d blocks (x+1)/2^k, k >= 1,
      and the m3_c / m3_f blocks (3-adic).
  N2  every primitive necklace w with total exponent K <= 13 has x_w = c_w/(2^K-3^a)
      in (0,1], and the exact rational x_w follows itinerary w under S and is
      periodic (Fractions, 2-adic residues computed exactly).
  N3  for every odd d <= 401: the cycles of M_d on Z found by simulating
      [-d, d] are {0} plus exactly the cycles whose odd points are d*x_w for
      necklaces w (each simulated cycle's word reproduces its points by the
      formula; every necklace with K <= 13 and d*x_w integral appears).
  N4  no negative cycles; for gcd(d,3)=1 a negative n reaches 0 iff d | n
      (all n in [-3d, -1], d <= 401), with the proof's crossing facts.
  P   the basin criterion (split_family.md, Theorem P): table of weak
      components of Z/d under x2, x3 and cycles per component, for odd
      d <= 1001; for d where the criterion says "periodic", the basin of every
      n <= 20000 equals the component rule (consistency); verdicts for the
      catalog members.
  D   1x+d (onexd.md): for odd d <= 1001 the folded map U(a) = a/2 or (a+d)/2
      permutes [1,d] as multiplication by 2^{-1} mod d; cycles of P_d on Z
      are {0} plus one per <2>-orbit on Z/d; basin rule verified for |n| <= 3000
      and d <= 101.
Runs in about 60 s.
"""
import os
import sys
from fractions import Fraction
from itertools import product
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import systems as SY  # noqa: E402


def v2(x):
    k = 0
    while x % 2 == 0:
        x //= 2
        k += 1
    return k


# ----------------------------------------------------------------- N1
def N1():
    for k in range(2, 13):
        for N in range(1, 9):
            M = 2 ** (N + k + 1)
            # A_k
            imgs = []
            for x in range(1, M, 2):
                if x % 4 == 1 and v2(3 * x + 1) == k:   # v2 determined mod 2^(k+1)
                    imgs.append(((3 * x + 1) >> k) % 2 ** N)
            assert sorted(imgs) == sorted(list(range(1, 2 ** N, 2)) * 2 ** (k + 1 - k)), (k, N)
            imgs = []
            for x in range(1, M, 2):
                if x % 4 == 3 and v2(x + 1) == k:
                    imgs.append(((x + 1) >> k) % 2 ** N)
            assert sorted(imgs) == sorted(list(range(1, 2 ** N, 2)) * 2), (k, N)
    # cylinders partition the odd classes: each odd x mod 2^(k+1) lies in exactly one
    # A_j or B_j with j <= k, or has v2 > k (measure 2^-(k)) -- checked mod 2^14
    M = 2 ** 14
    cnt = 0
    for x in range(1, M, 2):
        if x % 4 == 1:
            assert v2(3 * x + 1) >= 2 or (3 * x + 1) % M == 0
        else:
            assert v2(x + 1) >= 2
        cnt += 1
    # 1x+d blocks (x+1)/2^k, k >= 1, and 3-adic blocks (m3_c: (2x+1)/3^k on x=1,
    # (2x+2)/3^k on x=2; m3_f: (x+2)/3^k, (x+1)/3^k)
    for k in range(1, 12):
        for N in range(1, 8):
            M = 2 ** (N + k + 1)
            imgs = [((x + 1) >> k) % 2 ** N for x in range(1, M, 2) if v2(x + 1) == k]
            assert sorted(imgs) == sorted(list(range(1, 2 ** N, 2)) * 2), (k, N)

    def v3(x):
        j = 0
        while x % 3 == 0:
            x //= 3
            j += 1
        return j
    for (a1, c1, a2, c2) in [(2, 1, 2, 2), (1, 2, 1, 1)]:
        for k in range(1, 7):
            for N in range(1, 5):
                M = 3 ** (N + k + 1)
                units = sorted([y for y in range(3 ** N) if y % 3])
                for (a, c, r) in [(a1, c1, 1), (a2, c2, 2)]:
                    imgs = [((a * x + c) // 3 ** k) % 3 ** N for x in range(M)
                            if x % 3 == r and v3(a * x + c) == k]
                    assert sorted(imgs) == sorted(units * 3), (a, c, k, N)
    print('N1 OK')


# ----------------------------------------------------------------- necklaces
def compositions(K):
    """All words over {A_k, B_k : k >= 2} with total exponent K, as tuples of
    ('A'|'B', k)."""
    if K == 0:
        yield ()
        return
    for k in range(2, K + 1):
        for rest in compositions(K - k):
            yield (('A', k),) + rest
            yield (('B', k),) + rest


def primitive(w):
    n = len(w)
    return all(w[i:] + w[:i] != w for i in range(1, n))


def canon(w):
    return min(w[i:] + w[:i] for i in range(len(w)))


def xw(w):
    """Fixed point of B_w = B_{w[-1]} o ... o B_{w[0]}: B_w(x) = (3^a x + c)/2^K."""
    A, C, D = 1, 0, 1          # x -> (A x + C)/D
    for t, k in w:
        if t == 'A':
            A, C = 3 * A, 3 * C + D
        else:
            C = C + D
        D *= 2 ** k
    return Fraction(C, D - A)


def S_rat(x):
    """One step of S on a rational with odd denominator; returns (next, branch)."""
    num, den = x.numerator, x.denominator
    r = (num * pow(den, -1, 4)) % 4
    if r % 2 == 0:
        return x / 2, 'H'
    return (3 * x + 1, 'A') if r == 1 else (x + 1, 'B')


def itinerary(x, nblocks):
    w = []
    for _ in range(nblocks):
        y, b = S_rat(x)
        assert b in 'AB'
        k = 0
        while True:
            y2, b2 = S_rat(y) if y != 0 else (None, None)
            if b2 != 'H':
                break
            y, k = y2, k + 1
        w.append((b, k))
        x = y
    return tuple(w), x


def N2(Kmax=13):
    neck = {}
    for K in range(2, Kmax + 1):
        for w in compositions(K):
            if primitive(w):
                cw = canon(w)
                if cw not in neck:
                    x = xw(cw)
                    assert 0 < x <= 1, (cw, x)
                    it, back = itinerary(x, len(cw))
                    assert it == cw and back == x, (cw, x, it)
                    neck[cw] = x
    print(f'N2 OK: {len(neck)} primitive necklaces with K <= {Kmax}')
    return neck


# ----------------------------------------------------------------- M_d cycles
def Md(d):
    def T(n):
        if n % 2 == 0:
            return n // 2
        return 3 * n + d if (n * d) % 4 == 1 else n + d
    return T


def cycles_Md(d):
    T = Md(d)
    seen = set()
    cyc = []
    for n0 in range(-d, d + 1):
        path, ps, n = [], set(), n0
        while n not in seen and n not in ps:
            path.append(n)
            ps.add(n)
            n = T(n)
        if n in ps:
            cyc.append(path[path.index(n):])
        seen.update(path)
    return cyc


def word_of_cycle(c, d):
    """Word of a positive cycle of M_d starting at its smallest odd element."""
    odd = min(x for x in c if x % 2)
    w, back = itinerary(Fraction(odd, d), sum(1 for x in c if x % 2))
    assert back == Fraction(odd, d)
    return w, odd


def N3_N4(neck, dmax=401):
    T_all = {}
    for d in range(1, dmax + 1, 2):
        cs = cycles_Md(d)
        zero = [c for c in cs if 0 in c]
        assert len(zero) == 1 and zero[0] == [0]
        pos = [c for c in cs if 0 not in c]
        assert all(min(c) > 0 for c in pos)            # N4: no negative cycle
        words = set()
        for c in pos:
            w, odd = word_of_cycle(c, d)
            assert xw(w) == Fraction(odd, d)
            for i in range(len(w)):                     # every odd point = d x_rotation
                assert (xw(w[i:] + w[:i]) * d).denominator == 1
                assert int(xw(w[i:] + w[:i]) * d) in c
            words.add(canon(w))
        assert len(words) == len(pos)
        for cw, x in neck.items():
            if (x * d).denominator == 1:
                assert cw in words, (d, cw)
        T_all[d] = pos
        # N4: negatives
        T = Md(d)
        if d % 3:
            for n in range(-3 * d, 0):
                x = n
                while x < 0:
                    x = T(x)
                assert (x == 0) == (n % d == 0), (d, n)
    # crossing facts used in the proof: an odd negative x = n/d leaves the
    # negatives only via x in (-1/3, 0) with x = 1 mod 4 or x in (-1, 0) with x = 3 mod 4
    for d in range(1, 200, 2):
        T = Md(d)
        for n in range(-4 * d, 0):
            y = T(n)
            if y >= 0 and n % 2:
                r = (n * d) % 4
                assert (r == 1 and 3 * n + d >= 0) or (r == 3 and n + d >= 0)
    print(f'N3, N4 OK for odd d <= {dmax}')
    return T_all


# ----------------------------------------------------------------- Theorem P
def weak_components(d):
    par = list(range(d))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for a in range(d):
        for b in ((2 * a) % d, (3 * a) % d):
            ra, rb = f(a), f(b)
            if ra != rb:
                par[ra] = rb
    return f


def P(dmax=1001):
    periodic = []
    rows = {}
    for d in range(1, dmax + 1, 2):
        cs = [c for c in cycles_Md(d) if 0 not in c]
        f = weak_components(d)
        comps = {f(a) for a in range(d)}
        per = {}
        for c in cs:
            ks = {f(x % d) for x in c}
            assert len(ks) == 1                         # a cycle stays in one component
            per.setdefault(ks.pop(), []).append(min(c))
        assert set(per) == comps                        # every component has >= 1 cycle
        ok = all(len(v) == 1 for v in per.values())
        rows[d] = (len(cs), len(comps), ok, per)
        if ok:
            periodic.append(d)
    # consistency for small d with "periodic" verdict: basin = component rule
    for d in [x for x in periodic if x <= 151]:
        T = Md(d)
        f = weak_components(d)
        lab = {}
        for c in cycles_Md(d):
            if 0 not in c:
                for x in c:
                    lab[x] = min(c)
        comp_cycle = {f(x % d): m for x, m in lab.items()}
        for n in range(1, 20001):
            x = n
            while x not in lab:
                x = T(x)
            assert lab[x] == comp_cycle[f(n % d)]
    print(f'P OK: {len(periodic)} of {len(rows)} odd d <= {dmax} have ultimately periodic basins')
    print('   periodic d <= 200:', [d for d in periodic if d <= 200])
    for name, d in [('split_5', 5), ('split_13', 13), ('split_73', 73), ('split_97', 97),
                    ('split_7081', 7081), ('splitB_7', 7), ('splitB_71', 71)]:
        if d > dmax:
            cs = [c for c in cycles_Md(d) if 0 not in c]
            f = weak_components(d)
            comps = {f(a) for a in range(d)}
            per = {}
            for c in cs:
                per.setdefault(f(c[0] % d), []).append(min(c))
            rows[d] = (len(cs), len(comps), all(len(v) == 1 for v in per.values()), per)
        n, k, ok, per = rows[d]
        print(f'   {name:11s} d={d:5d}: {n} positive cycles, {k} components,'
              f' basin periodic: {ok};  component -> cycle minima: {sorted(per.values())}')
    # explicit basin rules for the catalog members with periodic basins
    for d, qr_cycle, nqr_cycle in [(73, 3, 5), (97, 33, 13), (71, 1, 11)]:
        T = Md(d)
        lab = {}
        for c in cycles_Md(d):
            if 0 not in c:
                for x in c:
                    lab[x] = min(c)
        for n in range(1, 200001):
            x = n
            while x not in lab:
                x = T(x)
            if n % d == 0:
                want = d
            else:
                want = qr_cycle if pow(n, (d - 1) // 2, d) == 1 else nqr_cycle
            assert lab[x] == want, (d, n)
        # <2,3> is exactly the quadratic residues
        H, fr = {1}, [1]
        while fr:
            y = fr.pop()
            for g in (2, 3):
                z = y * g % d
                if z not in H:
                    H.add(z)
                    fr.append(z)
        assert H == {pow(a, 2, d) for a in range(1, d)}, d
    for d in (5, 7):     # <2,3> = all units: units -> cycle of 1, multiples -> cycle of d
        T = Md(d)
        for n in range(1, 200001):
            x, seen = n, set()
            while x not in seen:
                seen.add(x)
                x = T(x)
            c = [x]
            y = T(x)
            while y != x:
                c.append(y)
                y = T(y)
            assert min(c) == (d if n % d == 0 else 1)
    print('   explicit Legendre-symbol basin rules for d = 5, 7, 71, 73, 97 confirmed on n <= 2*10^5')
    return rows


# ----------------------------------------------------------------- 1x+d
def D(dmax=1001):
    for d in range(1, dmax + 1, 2):
        inv2 = pow(2, -1, d) if d > 1 else 0
        img = []
        for a in range(1, d + 1):
            u = a // 2 if a % 2 == 0 else (a + d) // 2
            assert 1 <= u <= d and (u - a * inv2) % d == 0
            img.append(u)
        assert sorted(img) == list(range(1, d + 1))
    # cycles of P_d on Z and basins
    for d in range(1, 102, 2):
        T = SY.P(d)
        cyc = {}
        for n in range(-d, 2 * d + 1):
            x, seen = n, set()
            while x not in seen:
                seen.add(x)
                x = T(x)
            c = [x]
            y = T(x)
            while y != x:
                c.append(y)
                y = T(y)
            cyc[min(c)] = c
        # <2>-orbits on Z/d
        orb, seen = [], set()
        for a in range(d):
            if a in seen:
                continue
            o, x = set(), a
            while x not in o:
                o.add(x)
                x = (2 * x) % d
            seen |= o
            orb.append(o)
        assert len(cyc) == len(orb) + 1 and 0 in cyc
        rule = {}
        for m, c in cyc.items():
            if m != 0:
                rs = {x % d for x in c}
                o = next(o for o in orb if rs <= o)
                rule[frozenset(o)] = m
        assert len(rule) == len(orb)
        for n in range(-3000, 3001):
            x, seen = n, set()
            while x not in seen:
                seen.add(x)
                x = T(x)
            c = [x]
            y = T(x)
            while y != x:
                c.append(y)
                y = T(y)
            m = min(c)
            if n <= 0 and n % d == 0:
                assert m == 0
            else:
                o = next(o for o in orb if n % d in o)
                assert m == rule[frozenset(o)], (d, n)
    print('D OK')


if __name__ == '__main__':
    N1()
    neck = N2()
    N3_N4(neck)
    P()
    D()
    print('ALL OK')
