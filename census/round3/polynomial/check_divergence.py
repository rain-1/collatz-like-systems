"""Check for every divergence certificate in certs.py (proof: renormalization.md, Lemmas R1-R6,
and the per-system files).  For each certificate it tests exactly:

  (1) the renormalized identity  Phi^k(P) = P(X^(p^b))  (line) or Psi^k(mu,Q) = (mu,Q(X^(2^b)))
      (two-point), including the integrality side conditions of Lemma R6;
  (2) the periodic points used are T-hat-periodic with the declared words (two-point);
  (3) polynomiality of f_N for EVERY N = p^n (coefficientwise in X, so it is a statement about
      all n at once), via the sufficient condition of Lemma R5/R6;
  (4) independently of the lemmas, by direct exact simulation of T on polynomials:
      T^(tau N)(f_N) = f_(p^b N) for N = p^n, n = 0..n_max (degrees up to a few thousand);
  (5) deg f_N is strictly increasing in n (so the orbit is unbounded).
Runs in about a minute.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from polylib import (lcm2, divmod2, Fp, Tp, line_renorm, rad_divides, periodic_point2, orbit_period2,
                     clmul, pow2, subst2, radd2, rmul2, rnorm2, deg2, frob2, T2)
from certs import CERTS

fails = 0


def bits(tup):
    return sum(c << i for i, c in enumerate(tup))


def fail(msg):
    global fails
    fails += 1
    print('   FAIL:', msg)


for C in CERTS:
    p = C['p']
    F = Fp(p)
    g = F.tr(C['g'])
    h = F.tr(C['h'])
    print(C['id'], '-', C['note'])
    if C['kind'] == 'line':
        P = F.tr(C['P'])
        r = line_renorm(F, g, P)
        if r is None:
            fail('no self-similarity')
            continue
        k, b, taus = r
        tau = sum(taus)
        print('   Phi^%d(P) = P(X^%d), phase lengths (units of N) %s, tau = %dN' % (k, p ** b, taus, tau))
        w = F.sub(g, (0, 1))                      # g - t
        rho = F.rnorm((F.smul(g[0], h), w))       # g(0) h / (g - t)
        rho_poly = (rho[1] == (1,))
        # Lemma R5: if every irreducible factor of den(rho) divides P(X) in F_p[X], then
        # den(rho) | P(t^N) as soon as N >= deg den(rho)   (rho_poly is the case den = 1)
        radok = rad_divides(F, rho[1], P)
        if not radok:
            fail('no polynomiality criterion applies')
        Nmin = max(1, len(rho[1]) - 1)

        def ispoly(N):
            return not F.divmod(F.mul(rho[0], F.subst(P, N)), rho[1])[1]

        def fN(N):
            num = F.mul(rho[0], F.subst(P, N))
            q, rem = F.divmod(num, rho[1])
            assert not rem
            return q
        # below Nmin check polynomiality directly (exact)
        n0 = 0
        while not ispoly(p ** n0):
            n0 += 1
        if any(not ispoly(p ** j) for j in range(n0, 12)):
            fail('polynomiality gap')
        Nmin = p ** n0
        print('   polynomiality: rho = %s ; rad(den rho) | P(X): %s ; f_N polynomial for all N = p^n >= %d'
              % (rho, radok, Nmin))
        n = 0
        while p ** n < Nmin:
            n += 1
        degs = []
        while True:
            N = p ** n
            f = fN(N)
            f2 = fN(N * p ** b)
            if len(f2) > 4000:
                break
            x = f
            if p == 2:
                xi = bits(x)
                gi = bits(g)
                hi = bits(h)
                for _ in range(tau * N):
                    xi = T2(xi, gi, hi)
                ok = (xi == bits(f2))
            else:
                for _ in range(tau * N):
                    x = Tp(F, x, g, h)
                ok = (x == f2)
            if not ok:
                fail('direct simulation at N=%d' % N)
            degs.append(len(f) - 1)
            n += b
        print('   direct simulation T^(tau N) f_N = f_(p^b N) checked for %d values of N; deg f_N: %s'
              % (len(degs), degs))
        if any(degs[i] >= degs[i + 1] for i in range(len(degs) - 1)):
            fail('degrees not increasing')
        if C['N0'] < Nmin:
            fail('declared N0 too small')
    elif C['kind'] == 'twopoint':
        assert p == 2
        m = bits(g)
        hb = bits(h)
        w1, w2 = C['w1'], C['w2']
        c1 = periodic_point2(w1, m)
        c2 = periodic_point2(w2, m)
        per1 = orbit_period2(c1, m)
        per2 = orbit_period2(c2, m)
        if per1 is None or per1[2] != w1 or per2 is None or per2[2] != w2:
            fail('periodic points')
        sl = [(per1[1], per1[0]), (per2[1], per2[0])]
        d = radd2(c1, c2)
        Q0 = bits(C['Q'])
        mu, Q = 0, Q0
        tau = 0
        ok = False
        for k in range(1, 50):
            v = (Q & -Q).bit_length() - 1
            s, L = sl[mu]
            Lodd = L
            while Lodd % 2 == 0:
                Lodd //= 2
            if v % Lodd or (s * v) % L:
                fail('integrality side condition of Lemma R6')
                break
            tau += v
            Q = clmul(pow2(m, s * v // L), Q >> v) ^ 1
            mu = 1 - mu
            if mu == 0 and Q == frob2(Q0, 1):
                ok = True
                break
        if not ok:
            fail('no self-similarity')
            continue
        print('   Psi^%d(0,Q) = (0,Q(X^2)), tau = %dN; c1 = %s, c2 = %s' % (k, tau, c1, c2))
        # polynomiality for all N: B*(c1 + Q(X) d) must have polynomial coefficients in X
        B = hb
        coeffs = {0: c1}
        i = 0
        Qb = Q0
        while Qb:
            if Qb & 1:
                coeffs[i] = radd2(coeffs.get(i, (0, 1)), d)
            Qb >>= 1
            i += 1
        polycoef = {}
        coefB = {i: rmul2((B, 1), c) for i, c in coeffs.items()}
        if all(x[1] == 1 for x in coefB.values()):
            polycoef = {i: x[0] for i, x in coefB.items()}
            print('   f_N = sum_i X^i * %s  (polynomial coefficients, so f_N in F_2[t] for every N)'
                  % {i: bin(c) for i, c in polycoef.items()})
            fNpoly = None
        else:
            # common denominator D; f_N = Num(t, t^N)/D.  Num(t,t^N) mod D depends only on
            # X_n = t^(2^n) mod D, and X_{n+1} = X_n^2 mod D is eventually periodic in n:
            # checking every value of the sequence proves polynomiality for all N = 2^n.
            D = 1
            for x in coefB.values():
                D = lcm2(D, x[1])
            nums = {i: clmul(x[0], divmod2(D, x[1])[0]) for i, x in coefB.items()}
            Xn = divmod2(2, D)[1]
            seenX = []
            while Xn not in seenX:
                seenX.append(Xn)
                Xn = divmod2(clmul(Xn, Xn), D)[1]
            for Xv in seenX:
                acc = 0
                for i, c in nums.items():
                    acc ^= clmul(c, pow2(Xv, i))
                if divmod2(acc, D)[1]:
                    fail('not polynomial for some N=2^n')
            print('   f_N = Num(t,t^N)/D, D = %s; polynomial for all N = 2^n (checked on all %d residues of t^(2^n) mod D)'
                  % (bin(D), len(seenX)))
            fNpoly = (nums, D)
        def fN(N):
            if fNpoly is None:
                r = 0
                for i, c in polycoef.items():
                    r ^= c << (i * N)
                return r
            nums, D = fNpoly
            r = 0
            for i, c in nums.items():
                r ^= c << (i * N)
            q, rem = divmod2(r, D)
            assert rem == 0
            return q
        degs = []
        n = 0
        while True:
            N = 1 << n
            f = fN(N)
            f2 = fN(2 * N)
            if deg2(f2) > 4000:
                break
            x = f
            for _ in range(tau * N):
                x = T2(x, m, hb)
            if x != f2:
                fail('direct simulation at N=%d' % N)
            degs.append(deg2(f))
            n += 1
        print('   direct simulation checked for %d values of N; deg f_N: %s' % (len(degs), degs))
        if any(degs[i] >= degs[i + 1] for i in range(len(degs) - 1)):
            fail('degrees not increasing')
print('fails', fails)
sys.exit(1 if fails else 0)
