"""The Farkas pairing family P(a, K, x*) and its run-accelerated certificate engine.

P(a, K, x*):  a >= 3 odd, K >= 1, m = a^K, x* odd with gcd(a, x*) = 1 (a prime
power here; see pairing_family.md), r = x*/2 (mod m), c = (m-1) x*/2, b = (2-a) x*.

    T(n) = (n + c)/m      if n = r (mod m)          (priority)
         = n/2            if n even
         = (a n + b)/2    otherwise.

Block lemma (pairing_family.md): for odd n, n != x*, n != r (mod m), with
n - x* = 2^j u (u odd) and j = qK + l (0 <= l < K):

    T^(j+1+q)(n) = z_l := (x* + a^l u)/2.

The accelerated map S(n) = z_l on such n, and S = T elsewhere.  Every S-step is a
positive number of T-steps.  The engine below is the mixed-radix minimal
descent search of mixedlib.certificate, run on S, with one extra kind of leaf:

  TAIL leaf.  The current value y = P t + Q is odd, not in the division class,
  and y = x* (mod 2^e) with e = v_2(P) (so j = v_2(y - x*) >= e is not fixed by the
  class).  Since l <= K-1 and |u| <= |y - x*| / 2^e,
      S(y) <= (|x*| + a^(K-1) (P t + |Q - x*|) / 2^e) / 2.
  If a^(K-1) P < 2^(e+1) M this is < n = M t + r0 for t > t0 (explicit), except
  at the single t (if any) with y = x*.
"""
from fractions import Fraction
import math
import random
from mixedlib import primes_of, cycles_from


def v2(x):
    if x == 0:
        return 10 ** 9
    return (x & -x).bit_length() - 1


class Pairing:
    def __init__(self, a, K, xs):
        assert a % 2 == 1 and a >= 3 and K >= 1 and xs % 2 != 0 and math.gcd(a, xs) == 1
        self.a, self.K, self.xs = a, K, xs
        self.m = m = a ** K
        self.r = (xs * pow(2, -1, m)) % m
        self.c = (m - 1) * xs // 2
        self.b = (2 - a) * xs
        self.M0 = 2 * m

    def rule(self):
        return (f"n = {self.r} (mod {self.m}) -> (n {'+' if self.c >= 0 else '-'} {abs(self.c)})/{self.m}; "
                f"else even n -> n/2; else -> ({self.a}n {'+' if self.b >= 0 else '-'} {abs(self.b)})/2")

    def T(self, n):
        if n % self.m == self.r:
            x = n + self.c
            assert x % self.m == 0
            return x // self.m
        if n % 2 == 0:
            return n // 2
        x = self.a * n + self.b
        assert x % 2 == 0
        return x // 2

    def S(self, n):
        """accelerated map; returns (value, number of T-steps)."""
        if n % self.m == self.r or n % 2 == 0:
            return self.T(n), 1
        assert n != self.xs
        d = n - self.xs
        j = v2(d)
        u = d >> j
        q, l = divmod(j, self.K)
        z = self.xs + self.a ** l * u
        assert z % 2 == 0
        return z // 2, j + 1 + q

    # ------------------------------------------------------------------
    def _kind(self, P, Q):
        """branch of y = P t + Q for all t, or ('split', p)."""
        m = self.m
        g = math.gcd(P, 2 * m)
        rows = set()
        for i in range(2 * m // g):
            y = (Q + g * i) % (2 * m)
            rows.add('D' if y % m == self.r else ('E' if y % 2 == 0 else 'O'))
        if len(rows) > 1:
            h = 2 * m // g
            return ('split', primes_of(h)[0])
        kind = rows.pop()
        if kind == 'D':
            if P % m:          # cannot happen when rows uniform, but be safe
                return ('split', primes_of(m)[0])
            return ('D',)
        if kind == 'E':
            if P % 2:
                return ('split', 2)
            return ('E',)
        # odd branch: need j = v2(y - xs) fixed
        e = v2(P)
        dj = v2(Q - self.xs)
        if dj < e:
            return ('O', dj)
        return ('TAILQ', e)

    def certificate(self, maxnodes=2_000_000, maxdepth=500, Jmin=1):
        a, K, xs, m = self.a, self.K, self.xs, self.m
        leaves = []
        stack = [(1, 0, 1, 0, 0, ())]
        nodes = 0
        while stack:
            M, r0, P, Q, j, path = stack.pop()
            nodes += 1
            if nodes > maxnodes or j > maxdepth:
                return dict(ok=False, open=(M, r0, j, P, Q), nodes=nodes)
            if j > 0 and (P < M or (P == M and Q < r0)):
                leaves.append(('D', M, r0, j, P, Q, path))
                continue
            kd = self._kind(P, Q)
            if kd[0] == 'split':
                p = kd[1]
                for s in range(p):
                    stack.append((p * M, r0 + M * s, p * P, Q + P * s, j, path + ((p, s),)))
            elif kd[0] == 'D':
                stack.append((M, r0, P // m, (Q + self.c) // m, j + 1, path))
            elif kd[0] == 'E':
                stack.append((M, r0, P // 2, Q // 2, j + 1, path))
            elif kd[0] == 'O':
                jj = kd[1]
                q, l = divmod(jj, K)
                al = a ** l
                nP = al * (P >> (jj + 1))
                num = xs + al * ((Q - xs) >> jj)
                assert num % 2 == 0
                stack.append((M, r0, nP, num // 2, j + 1, path))
            else:  # TAILQ
                e = kd[1]
                if e >= Jmin and a ** (K - 1) * P < 2 ** (e + 1) * M:
                    leaves.append(('T', M, r0, j, P, Q, path))
                else:
                    stack.append((2 * M, r0, 2 * P, Q, j, path + ((2, 0),)))
                    stack.append((2 * M, r0 + M, 2 * P, Q + P, j, path + ((2, 1),)))
        return dict(ok=True, leaves=leaves, nodes=nodes)

    # ------------------------------------------------------------------
    def tail_t0(self, M, r0, P, Q):
        """For a TAIL leaf: every t > t0 (with P t + Q != xs) has S(y) < M t + r0."""
        a, K, xs = self.a, self.K, self.xs
        e = v2(P)
        A = Fraction(a ** (K - 1) * P, 2 ** (e + 1))
        assert A < M
        B = Fraction(abs(xs), 2) + Fraction(a ** (K - 1) * abs(Q - xs), 2 ** (e + 1))
        # S(y) <= A t + B < M t + r0  iff  t > (B - r0)/(M - A)
        return math.floor((B - r0) / (M - A))

    def exceptional(self, leaves, start=1):
        E = set()
        for L in leaves:
            kind, M, r0, j, P, Q, path = L
            if kind == 'D':
                if P < M:
                    tmax = (Q - r0) // (M - P) if Q >= r0 else -1
                else:
                    tmax = -1
            else:
                tmax = self.tail_t0(M, r0, P, Q)
                # the one t (if any) with y = xs
                if (self.xs - Q) % P == 0:
                    t1 = (self.xs - Q) // P
                    if t1 >= 0 and M * t1 + r0 >= start:
                        E.add(M * t1 + r0)
            for t in range(0, tmax + 1):
                n = M * t + r0
                if n >= start:
                    E.add(n)
        return sorted(E)

    def verify(self, leaves, trials=3):
        """Independent re-verification (trie partition, symbolic re-derivation with
        uniform-branch assertions, closing / tail inequalities, numeric checks of
        S against T, including the block lemma)."""
        a, K, xs, m = self.a, self.K, self.xs, self.m
        children, leafset = {}, set()
        for L in leaves:
            kind, M, r0, j, P, Q, path = L
            MM, rr = 1, 0
            for i, (p, s) in enumerate(path):
                children.setdefault(path[:i], {}).setdefault(p, set()).add(s)
                rr += MM * s
                MM *= p
            assert (MM, rr) == (M, r0)
            assert path not in leafset
            leafset.add(path)
        for pre, d in children.items():
            assert len(d) == 1
            (p, ss), = d.items()
            assert ss == set(range(p))
            assert pre not in leafset
            for s in ss:
                c = pre + ((p, s),)
                assert c in children or c in leafset
        assert sum(Fraction(1, L[1]) for L in leaves) == 1
        for L in leaves:
            kind, M, r0, j, P, Q, path = L
            PP, QQ = M, r0
            for _ in range(j):
                kd = self._kind(PP, QQ)
                assert kd[0] in ('D', 'E', 'O'), kd
                if kd[0] == 'D':
                    assert PP % m == 0 and (QQ + self.c) % m == 0
                    PP, QQ = PP // m, (QQ + self.c) // m
                elif kd[0] == 'E':
                    PP, QQ = PP // 2, QQ // 2
                else:
                    jj = kd[1]
                    assert v2(PP) > jj and v2(QQ - xs) == jj
                    q, l = divmod(jj, K)
                    PP, QQ = a ** l * (PP >> (jj + 1)), (xs + a ** l * ((QQ - xs) >> jj)) // 2
            assert (PP, QQ) == (P, Q)
            if kind == 'D':
                assert P < M or (P == M and Q < r0)
            else:
                kd = self._kind(P, Q)
                assert kd[0] == 'TAILQ'
                e = kd[1]
                assert a ** (K - 1) * P < 2 ** (e + 1) * M
            for t in [0, 1, 2, 5, 1000003] + [random.getrandbits(90) for _ in range(trials)]:
                n = M * t + r0
                if n <= 0:
                    continue
                y, steps = n, 0
                for _ in range(j):
                    y2, s = self.S(y)
                    # S agrees with T^s
                    z = y
                    for _ in range(s):
                        z = self.T(z)
                    assert z == y2
                    y, steps = y2, steps + s
                assert y == P * t + Q
                if kind == 'D' and P < M and t > ((Q - r0) // (M - P) if Q >= r0 else -1):
                    assert y < n
                if kind == 'T' and y != xs:
                    y2, s = self.S(y)
                    if t > self.tail_t0(M, r0, P, Q):
                        assert y2 < n
        return True

    def prove(self, maxnodes=2_000_000, start=None):
        if start is None:
            start = 1 if self.xs > 0 else 0
        res = self.certificate(maxnodes=maxnodes)
        if not res['ok']:
            return dict(ok=False, open=res['open'], nodes=res['nodes'])
        leaves = res['leaves']
        self.verify(leaves)
        E = self.exceptional(leaves, start=start)
        cyc = cycles_from(self.T, E + [start])
        return dict(ok=True, nleaves=len(leaves), ntail=sum(1 for L in leaves if L[0] == 'T'),
                    maxj=max(L[3] for L in leaves), E=len(E), Emax=max(E) if E else None,
                    cycles=cyc, leaves=leaves)
