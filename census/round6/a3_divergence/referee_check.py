"""Independent referee check of the A3 divergence proof (README.md).  Written from scratch:
does not import a3.py, theta.py or check_a3_divergence.py.  Exact arithmetic over F_3
(Python ints mod 3 and numpy int64 arrays reduced mod 3).  Exits 1 on any failure,
including a mutation test that is NOT detected.

Polynomials are coefficient lists / arrays, lowest degree first, with no trailing zeros
(the zero polynomial is the empty list).

Usage: python3 referee_check.py [raw_steps] [theta_steps]   (defaults 60000 60000)
"""
import itertools, math, random, sys
import numpy as np

P = 3
FAIL = []


def fail(msg):
    FAIL.append(msg)
    print('FAIL', msg)


# ---------------------------------------------------------------- pure-Python F_3[x]
def norm(a):
    a = [x % P for x in a]
    while a and a[-1] == 0:
        a.pop()
    return a


def padd(a, b):
    n = max(len(a), len(b))
    return norm([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def psub(a, b):
    return padd(a, [-x for x in b])


def pmul(a, b):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return norm(r)


def ppow(a, e):
    r = [1]
    for _ in range(e):
        r = pmul(r, a)
    return r


def pshift(a, k):          # a * x^k
    return norm([0] * k + list(a)) if a else []


def pdivx(a):              # exact division by x; asserts divisibility
    if a and a[0] % P:
        raise ArithmeticError('not divisible by x: %r' % (a,))
    return norm(a[1:])


def ct(a):
    return a[0] if a else 0


def deg(a):
    return len(a) - 1 if a else -1


def subst6(K):             # K(t^6)
    r = []
    for i, k in enumerate(K):
        r += [k] + ([0] * 5 if i < len(K) - 1 else [])
    return norm(r)


# ---------------------------------------------------------------- the system, written afresh
ONE_T2 = [1, 0, 1]         # 1 + t^2


def A3(f, mult=ONE_T2):
    c = ct(f)
    if c == 0:
        return pdivx(f)
    if c == 1:
        return pmul(mult, pdivx(psub(f, [1])))
    return padd(pdivx(psub(f, [2])), [1])


SEED = norm([1, 1, 1, 0, 2, 2, 0, 2])   # 1 + t + t^2 + 2t^4 + 2t^5 + 2t^7
C = [1, 2]                              # 1 + 2t
Q = [0, 2, 1, 0, 2, 2, 0, 2]            # 2t + t^2 + 2t^4 + 2t^5 + 2t^7


def fK(K, q=Q):
    return padd(C, pmul(subst6(K), q))


def theta(K, raise_exp=2):
    """Theta from the README formulas, via generic arithmetic; division by s asserted exact."""
    k0 = ct(K)
    if k0 == 1:
        return padd(pdivx(psub(pmul(ppow([1, 1], raise_exp), K), [1])), [1])
    return pdivx(psub(pmul([1, 1], K), [k0]))


def T6(f, mult=ONE_T2):
    w = ''
    for _ in range(6):
        w += str(ct(f))
        f = A3(f, mult)
    return f, w


WORD = {0: '121212', 1: '111111', 2: '102101'}


def all_polys(maxdeg):
    for tup in itertools.product(range(P), repeat=maxdeg + 1):
        yield norm(list(tup))


def rand_poly(rnd, d):     # exactly degree d (d >= 0)
    return norm([rnd.randrange(P) for _ in range(d)] + [rnd.randrange(1, P)])


# ---------------------------------------------------------------- Step 1
def check_conjugacy(Ks, mult=ONE_T2, q=Q, raise_exp=2, tag=''):
    bad = 0
    for K in Ks:
        try:
            g, w = T6(fK(K, q), mult)
            th = theta(K, raise_exp)
        except ArithmeticError as e:
            bad += 1; continue
        if w != WORD[ct(K)] or g != fK(th, q):
            bad += 1
    return bad


def step1(rnd):
    print('Step 1')
    if fK([1]) != SEED:
        fail('seed is not f_1')
    # characteristic-3 identities
    if ppow(ONE_T2, 3) != subst6([1, 1]) or ppow(ONE_T2, 6) != subst6([1, 2, 1]):
        fail('(1+t^2)^3 = 1+t^6 or (1+t^2)^6 = (1+t^6)^2')
    # base cases, explicitly
    for k0, img in ((0, [0]), (1, [0, 1]), (2, [2])):
        g, w = T6(fK(norm([k0])))
        if g != fK(norm(img)) or w != WORD[k0]:
            fail('base case %d' % k0)
        if theta(norm([k0])) != norm(img):
            fail('Theta(%d)' % k0)
    print('  f_0 =', fK([]), ' f_2 =', fK([2]), ' T^6 f_1 = f_s:', T6(SEED)[0] == fK([0, 1]))
    # mod t^6 dependence of the first 6 branches and the affine law on cylinders
    for _ in range(3000):
        g = norm([rnd.randrange(P) for _ in range(rnd.randrange(1, 40))])
        h = norm([rnd.randrange(P) for _ in range(rnd.randrange(0, 40))])
        G = padd(g, pshift(h, 6))
        T1, w1 = T6(g); T2, w2 = T6(G)
        if w1 != w2:
            fail('branch word depends on coefficients >= 6: %r %r' % (g, h)); break
        a = w1.count('1')
        if psub(T2, T1) != pmul(ppow(ONE_T2, a), h):
            fail('affine law T^6(g+t^6h)=T^6(g)+(1+t^2)^a h: %r %r' % (g, h)); break
    # exhaustive conjugacy for deg K <= 5 (729 polynomials incl. K = 0) and random beyond
    allK = list(all_polys(5))
    b = check_conjugacy(allK)
    if b: fail('conjugacy fails on %d of %d K with deg <= 5' % (b, len(allK)))
    randK = [rand_poly(rnd, rnd.randrange(6, 121)) for _ in range(500)]
    b2 = check_conjugacy(randK)
    if b2: fail('conjugacy fails on %d random K' % b2)
    # K with k0 = 0 and k0 = 2 among the random ones, specifically
    zK = [norm([0] + rand_poly(rnd, rnd.randrange(5, 60))) for _ in range(100)]
    tK = [norm([2] + rand_poly(rnd, rnd.randrange(5, 60))) for _ in range(100)]
    b3 = check_conjugacy(zK + tK)
    if b3: fail('conjugacy fails on %d K with k0 in {0,2}' % b3)
    print('  conjugacy: %d exhaustive (deg<=5) + %d random (deg 6..120) + 200 k0 in {0,2}' % (len(allK), len(randK)))
    return allK, randK


# ---------------------------------------------------------------- Step 2
def step2(rnd, allK, randK):
    print('Step 2')
    for K in allK + randK:
        if not K:
            if theta(K) != []: fail('Theta(0) != 0')
            continue
        if deg(fK(K)) != 6 * deg(K) + 7:
            fail('deg f_K %r' % K)
        L = theta(K)
        if deg(L) != deg(K) + (1 if ct(K) == 1 else 0):
            fail('deg Theta %r' % K)
        if L[-1] != K[-1]:
            fail('leading coefficient of Theta %r' % K)
    # per-step degree changes for deg >= 2: branch 0: -1, 1: +1, 2: -1
    for _ in range(2000):
        f = rand_poly(rnd, rnd.randrange(2, 40))
        dd = deg(A3(f)) - deg(f)
        if dd != {0: -1, 1: 1, 2: -1}[ct(f)]:
            fail('one-step degree change %r' % f)


# ---------------------------------------------------------------- Step 3
def Nmap(K):
    return pdivx(psub(pmul([1, 1], K), [ct(K)]))


def binom3(n, j):          # C(n, j) mod 3 by Lucas
    r = 1
    while n or j:
        a, b = n % 3, j % 3
        if b > a:
            return 0
        r = r * math.comb(a, b) % 3
        n //= 3; j //= 3
    return r


def lemma_failures(Ms, offset=-2):
    """For L = s + (1+s)^2 M, m >= 1 minimal with 3^m - 2 > deg M, n = 3^m + offset:
    constant term of N^n(L) must be 1.  offset = -2 is the README; others are mutations."""
    bad = 0
    for M in Ms:
        L = padd([0, 1], pmul([1, 2, 1], M))
        m = 1
        while 3 ** m - 2 <= deg(M):
            m += 1
        X = L
        for _ in range(3 ** m + offset):
            X = Nmap(X)
        if ct(X) != 1:
            bad += 1
    return bad


def step3(rnd):
    print('Step 3')
    # N(K)_i = k_i + k_{i+1};  N equals Theta on k0 in {0, 2}
    for _ in range(1000):
        K = norm([rnd.randrange(P) for _ in range(rnd.randrange(0, 30))])
        NK = Nmap(K)
        exp = norm([(K[i] if i < len(K) else 0) + (K[i + 1] if i + 1 < len(K) else 0) for i in range(len(K))])
        if NK != exp: fail('N coefficient formula %r' % K)
        if ct(K) != 1 and theta(K) != NK: fail('Theta != N off the raising branch %r' % K)
    # CT N^n(K) = CT (1+1/s)^n K = sum_j C(n,j) k_j, and N^n(K) = polynomial part of (1+1/s)^n K
    for _ in range(300):
        K = norm([rnd.randrange(P) for _ in range(rnd.randrange(0, 25))])
        n = rnd.randrange(0, 60)
        X = K
        for _ in range(n): X = Nmap(X)
        num = pmul(ppow([1, 1], n), K)           # (1+s)^n K = s^n (1+1/s)^n K
        polypart = norm(num[n:])
        if X != polypart: fail('N^n = polynomial part, n=%d K=%r' % (n, K))
        if ct(X) != sum(binom3(n, j) * (K[j] if j < len(K) else 0) for j in range(n + 1)) % 3:
            fail('CT via Lucas')
    # coefficient of s^{n-1} in (1+s)^n is n mod 3
    for n in range(1, 200):
        if binom3(n, n - 1) != n % 3: fail('C(n,n-1)')
    # the raising image L
    for _ in range(300):
        M = norm([rnd.randrange(P) for _ in range(rnd.randrange(0, 30))])
        K = padd([1], pshift(M, 1))
        if theta(K) != padd([0, 1], pmul([1, 2, 1], M)): fail('L = s + (1+s)^2 M')
    # key lemma: exhaustive for deg M <= 6 (including M = 0) and random up to deg 40
    Ms = list(all_polys(6)) + [norm([rnd.randrange(P) for _ in range(rnd.randrange(8, 42))]) for _ in range(300)]
    b = lemma_failures(Ms)
    if b: fail('key lemma fails for %d M' % b)
    print('  key lemma on %d M (all deg <= 6, 300 random to deg 40)' % len(Ms))
    # exact gap statement: from a raising step at K = 1 + sM, the next raising step comes after
    # at most 3^m - 1 steps; test on random starting K directly with Theta
    worst = 0
    for _ in range(300):
        M = norm([rnd.randrange(P) for _ in range(rnd.randrange(0, 40))])
        K = padd([1], pshift(M, 1))
        m = 1
        while 3 ** m - 2 <= deg(M): m += 1
        X = theta(K); g = 1
        while ct(X) != 1:
            X = theta(X); g += 1
            if g > 3 ** m: break
        if g > 3 ** m - 1: fail('gap from raising step at %r is %d > 3^m - 1' % (K, g))
        worst = max(worst, g / (3 ** m - 1))
    print('  gap from random raising starts: max gap/(3^m-1) = %.3f' % worst)
    # M = 0 case explicitly: K = 1 -> s -> 1 + s
    if theta([1]) != [0, 1] or theta([0, 1]) != [1, 1]: fail('M = 0 case')


# ---------------------------------------------------------------- Remark
def remark():
    print('Remark (periodicity off the raising branch)')
    for d in range(0, 6):
        Vd = [K for K in all_polys(d)]
        img = {tuple(Nmap(K)) for K in Vd}
        if len(img) != len(Vd): fail('N not a bijection on V_%d' % d)
    # every K of degree <= 5: Theta-orbit either is purely periodic avoiding k0 = 1, or hits k0 = 1
    nper = nhit = 0
    for K in all_polys(5):
        X = K; seen = []; hit = False
        for _ in range(3 ** 6 + 1):          # N has order dividing 3^6 on V_5 (unipotent)
            if ct(X) == 1: hit = True; break
            seen.append(tuple(X)); X = theta(X)
            if tuple(X) == tuple(K): break
        if hit:
            nhit += 1
        else:
            if tuple(X) != tuple(K): fail('non-raising orbit not purely periodic %r' % K)
            nper += 1
    print('  deg<=5: %d purely periodic non-raising orbits, %d orbits that raise' % (nper, nhit))


# ---------------------------------------------------------------- raw orbit (numpy, exact mod 3)
def np_trim(a):
    nz = np.flatnonzero(a)
    return a[:nz[-1] + 1] if nz.size else a[:0]


def np_A3(f):
    c = int(f[0]) if f.size else 0
    if c == 0:
        return f[1:], 0
    h = f[1:]
    if c == 1:
        g = np.zeros(h.size + 2, dtype=np.int64)
        g[:h.size] += h; g[2:] += h
        return np_trim(g % 3), 1
    g = h.copy() if h.size else np.zeros(1, dtype=np.int64)
    g[0] = (g[0] + 1) % 3
    return np_trim(g), 2


def np_theta(K):
    k0 = int(K[0]) if K.size else 0
    if k0 == 1:
        g = np.zeros(K.size + 2, dtype=np.int64)
        g[:K.size] += K; g[1:K.size + 1] += 2 * K; g[2:] += K
        g[0] -= 1; g %= 3
        assert g[0] == 0
        g = g[1:].copy(); g[0] = (g[0] + 1) % 3
        return np_trim(g)
    g = np.zeros(K.size + 1, dtype=np.int64)
    g[:K.size] += K; g[1:] += K
    g[0] -= k0; g %= 3
    assert g[0] == 0
    return np_trim(g[1:])


def np_fK(K):
    n = 6 * max(K.size - 1, 0) + 8
    f = np.zeros(n, dtype=np.int64)
    f[0] += 1; f[1] += 2
    for j, qj in enumerate(Q):
        if qj:
            f[j:j + 6 * K.size:6] += qj * K
    return np_trim(f % 3)


def raw_orbit(steps, seed_list, verify_conj=True):
    """Returns list of failure strings (does not print)."""
    errs = []
    f = np.array(seed_list, dtype=np.int64)
    K = np.array([1], dtype=np.int64)
    blockdeg = []; minafter = []
    word = ''
    for n in range(steps):
        if n % 6 == 0:
            b = n // 6
            dK = K.size - 1
            df = f.size - 1
            if df != 6 * dK + 7:
                errs.append('block %d: deg T^6n f = %d != 6*%d+7' % (b, df, dK))
                if len(errs) > 5: return errs, blockdeg, f
            if verify_conj and not np.array_equal(f, np_fK(K)):
                errs.append('block %d: T^6n f != f_Theta^n(1)' % b)
                if len(errs) > 5: return errs, blockdeg, f
            if b > 0 and word != WORD[k0prev]:
                errs.append('block %d word %s != %s' % (b - 1, word, WORD[k0prev]))
            blockdeg.append(df); minafter.append(df)
            k0prev = int(K[0]) if K.size else 0
            K = np_theta(K)
            word = ''
        d = f.size - 1
        minafter[-1] = min(minafter[-1], d)
        f, br = np_A3(f)
        word += str(br)
    for i in range(1, len(blockdeg)):
        if blockdeg[i] < blockdeg[i - 1]:
            errs.append('block degree decreased at %d' % i); break
    # every degree in block i (steps 6i .. 6i+5) is >= blockdeg[i] - 1 >= every earlier block value - 1
    for i in range(len(blockdeg)):
        if minafter[i] < blockdeg[i] - 1:
            errs.append('intermediate degree in block %d dips %d below' % (i, blockdeg[i] - minafter[i])); break
    return errs, blockdeg, f


def raw_check(steps):
    print('Raw A3 orbit of the seed, %d steps' % steps)
    res = raw_orbit(steps, SEED)
    errs, blockdeg, f = res
    for e in errs: fail(e)
    # global: degree after step k never below max over earlier blocks minus 1
    print('  blocks: %d, final block degree %d, final degree %d; first block degrees %s'
          % (len(blockdeg), blockdeg[-1], f.size - 1, blockdeg[:12]))


def theta_orbit_check(steps):
    print('Theta orbit of K = 1, %d steps: gap bound and rate bound' % steps)
    K = np.array([1], dtype=np.int64)
    last = None; worst = 0; D = 0
    for n in range(steps + 1):
        D = K.size - 1
        if D < math.sqrt(2 * n / 3) - 2:
            fail('rate bound fails at n=%d D=%d' % (n, D)); break
        if n == steps: break
        if int(K[0]) == 1:
            if last is not None:
                # D = degree produced by the previous raising step; deg M = D - 2
                m = 1
                while 3 ** m <= D: m += 1
                if n - last > 3 ** m - 1:
                    fail('gap %d > 3^m - 1 = %d at n=%d, D=%d' % (n - last, 3 ** m - 1, n, D)); break
                if n - last > 3 * D:
                    fail('gap exceeds 3D at n=%d' % n); break
                worst = max(worst, (n - last) / (3 ** m - 1))
            last = n
        K = np_theta(K)
    print('  final degree %d; max gap/(3^m-1) = %.3f; D_n/n = %.4f, sqrt(2n/3)-2 = %.1f'
          % (D, worst, D / steps, math.sqrt(2 * steps / 3) - 2))


# ---------------------------------------------------------------- mutation tests (must FAIL)
def mutations(rnd):
    print('Mutation tests (each must be detected)')
    Ks = list(all_polys(3))
    muts = {
        'A3 branch-1 multiplier 1+t instead of 1+t^2': check_conjugacy(Ks, mult=[1, 1]),
        'q with t^7 coefficient 1 instead of 2': check_conjugacy(Ks, q=[0, 2, 1, 0, 2, 2, 0, 1]),
        'Theta raising branch with (1+s)^1': check_conjugacy(Ks, raise_exp=1),
        'key lemma with n = 3^m - 3': lemma_failures(list(all_polys(5)), offset=-3),
        'key lemma with n = 3^m - 1': lemma_failures(list(all_polys(5)), offset=-1),
    }
    errs, _, _ = raw_orbit(600, norm([1, 1, 1, 0, 2, 2, 0, 1]))
    muts['raw orbit from mutated seed (t^7 coeff 1)'] = len(errs)
    for name, nbad in muts.items():
        ok = nbad > 0
        print('  %-48s detected: %s (%d)' % (name, ok, nbad))
        if not ok: fail('mutation not detected: ' + name)


if __name__ == '__main__':
    raw_steps = int(sys.argv[1]) if len(sys.argv) > 1 else 60000
    th_steps = int(sys.argv[2]) if len(sys.argv) > 2 else 60000
    rnd = random.Random(20261128)
    allK, randK = step1(rnd)
    step2(rnd, allK, randK)
    step3(rnd)
    remark()
    mutations(rnd)
    raw_check(raw_steps)
    theta_orbit_check(th_steps)
    print('REFEREE CHECK', 'FAILED (%d)' % len(FAIL) if FAIL else 'passed')
    sys.exit(1 if FAIL else 0)
