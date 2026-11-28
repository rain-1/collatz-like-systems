"""Second referee's independent check for lens "mixedbase" (round 3).

Written from scratch; imports nothing from mixedlib.py, pairlib.py, the prover's check scripts,
referee_check.py or systems.py.  Every map is re-typed from the rule text in the .md files.

Sections
  A. own mixed-radix descent engine + Lemma A' (exceptional set, complete cycle list)
  B. Theorem D (div23_5n1 + one class): exact cycles, the q <= 83 bound, refined-B' scan,
     integer simulation of every exclusion witness, certification + cycle list of each survivor
  C. Theorem M (m3_b + <= 2 classes): same, bound q <= 32, extended consistency scan to 400
  D. the 12 other certified systems (single class + sparse) and the minimality lower bounds
     for m = 27, 81, 243, 25, 125, 49, 343, 729 (own cycle enumeration + own hitting-set search)
  E. EVIDENCE: random large starts for named systems
Exits 0 iff everything holds.  Runtime ~1-2 min.
"""
import sys, math, random
from fractions import Fraction as F
from itertools import product

random.seed(20261127)


def lcm(a, b):
    return a * b // math.gcd(a, b)


def rmod(y, m):
    y = F(y)
    assert math.gcd(y.denominator, m) == 1
    return y.numerator * pow(y.denominator, -1, m) % m


def primes_of(n):
    out, p = [], 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


# --------------------------------------------------------------------------- A. engine
def certify(M0, row, maxnodes=400000, maxdepth=400):
    """row(rho) -> (u, v, w) for rho mod M0.  Returns leaves [(M, r, P, Q, j)] or None."""
    sp = primes_of(M0)
    stack = [(1, 0, 1, 0, 0)]
    leaves, nodes = [], 0
    while stack:
        M, r, P, Q, j = stack.pop()
        nodes += 1
        if nodes > maxnodes or j > maxdepth:
            return None
        g = math.gcd(P, M0)
        k = M0 // g
        # the values P t + Q (t >= 0) run through the residues Q + P s mod M0, s < k.  Apply a
        # step only if one row covers all of them and the division is exact uniformly in t.
        rows = {row((Q + P * s) % M0) for s in range(k)}
        uniform = False
        if len(rows) == 1:
            u, v, w = next(iter(rows))
            uniform = (u * P) % w == 0 and (u * Q + v) % w == 0
        if not uniform:
            p = min(x for x in sp if k % x == 0)
            for s in range(p):
                stack.append((M * p, r + M * s, P * p, Q + P * s, j))
            continue
        assert (u * P) % w == 0 and (u * Q + v) % w == 0
        P, Q, j = u * P // w, (u * Q + v) // w, j + 1
        if P < M or (P == M and Q < r):
            leaves.append((M, r, P, Q, j))
        else:
            stack.append((M, r, P, Q, j))
    return leaves


def check_partition(leaves):
    # leaves n = M t + r must partition N0: total density 1 and no two overlap
    assert sum(F(1, M) for M, *_ in leaves) == 1
    L = max(M for M, *_ in leaves)
    if L <= 10 ** 6:
        seen = set()
        for M, r, *_ in leaves:
            for x in range(r, L, M):
                assert x not in seen
                seen.add(x)
        assert len(seen) == L


def lemma_A(leaves, step, row, M0):
    check_partition(leaves)
    for M, r, P, Q, j in leaves:  # re-test leaf identity on random big t
        for t in (0, 1, random.getrandbits(100), random.getrandbits(200)):
            n = M * t + r
            x = n
            for _ in range(j):
                u, v, w = row(x % M0)
                assert (u * x + v) % w == 0
                x2 = (u * x + v) // w
                if n > 0:
                    assert step(x) == x2
                x = x2
            assert x == P * t + Q
    E = []
    for M, r, P, Q, j in leaves:
        if P < M and Q >= r:
            tmax = (Q - r) // (M - P)
            E += [M * t + r for t in range(tmax + 1) if M * t + r >= 1]
    # every positive n outside E has a smaller iterate; collect cycles from E
    cyc = set()
    for e in E:
        seen = {}
        x, k = e, 0
        while x not in seen:
            seen[x] = k
            x = step(x)
            k += 1
            assert x >= 1
        c = [x]
        y = step(x)
        while y != x:
            c.append(y)
            y = step(y)
        i = c.index(min(c))
        cyc.add(tuple(c[i:] + c[:i]))
    return sorted(cyc), E


# --------------------------------------------------------------------------- cycles
def word_cycles(letters, Mb, maxlen):
    """letters: list of (u, v, w, residue-set mod Mb).  Exact expanding rational cycles of the
    base map whose orbit follows the word; returns list of (points, letter indices)."""
    found = {}
    for L in range(1, maxlen + 1):
        for word in product(range(len(letters)), repeat=L):
            lam, mu = F(1), F(0)
            for k in word:
                u, v, w, _ = letters[k]
                lam, mu = lam * F(u, w), (mu * u + v) / w
            if lam <= 1:
                continue
            y = mu / (1 - lam)
            if math.gcd(y.denominator, Mb) != 1:
                continue
            pts, ok, x = [], True, y
            for k in word:
                u, v, w, S = letters[k]
                if rmod(x, Mb) not in S:
                    ok = False
                    break
                pts.append(x)
                x = (u * x + v) / w
            if ok and x == y:
                key = frozenset(pts)
                if key not in found:
                    found[key] = (pts, word)
    return list(found.values())


def coprime_part(q, d):
    g = math.gcd(q, d)
    while g > 1:
        q //= g
        g = math.gcd(q, d)
    return q


def caught(q, R, pts, admissible):
    d = 1
    for y in pts:
        d = lcm(d, y.denominator)
    q1 = coprime_part(q, d)
    if q1 == 1:
        return True
    R1 = {r % q1 for r in R}
    return any(admissible(i) and rmod(y, q1) in R1 for i, y in enumerate(pts))


def simulate_witness(Mb, q, R, pts, word, letters, tamed_row, M0):
    """Integer test of the refined Lemma B': integers n = y0 mod (Mb*q1)^K follow the base cycle
    for 3 periods without being caught, and T^L(n) = lam*n + mu with lam > 1."""
    d = 1
    for y in pts:
        d = lcm(d, y.denominator)
    q1 = coprime_part(q, d)
    L = len(pts)
    steps = 3 * L
    mod = (Mb * q1) ** (steps + 2)
    n = rmod(pts[0], mod) + mod * (random.getrandbits(64) + 1)
    lam, mu = F(1), F(0)
    for k in word:
        u, v, w, _ = letters[k]
        lam, mu = lam * F(u, w), (mu * u + v) / w
    assert lam > 1
    x = n
    for i in range(steps):
        u, v, w = tamed_row(x % M0)
        k = word[i % L]
        assert (u, v, w) == letters[k][:3], "caught or wrong branch"
        x = (u * x + v) // w
        if i == L - 1:
            assert x == lam * n + mu and x > n


# --------------------------------------------------------------------------- B. Theorem D
def div23_row_base(rho):
    if rho % 2 == 0:
        return (1, 0, 2)
    if rho % 3 == 0:
        return (1, 0, 3)
    return (5, 1, 1)


def div23_tamed(q, R, prio):
    M0 = lcm(6, q)

    def row(rho):
        b = div23_row_base(rho % 6)
        if rho % q in R and (prio == 'first' or b[0] == 5):
            return (1, (-(rho % q)) % q, q)
        return b

    def step(n):
        u, v, w = row(n % M0)
        assert (u * n + v) % w == 0
        return (u * n + v) // w
    return M0, row, step


def canon(cs):
    out = []
    for c in cs:
        c = list(c)
        i = c.index(min(c))
        out.append(tuple(c[i:] + c[:i]))
    return sorted(out)


def section_D():
    print("== B. Theorem D")
    letters = [(1, 0, 2, {0, 2, 4}), (1, 0, 3, {3}), (5, 1, 1, {1, 5})]
    cycs = word_cycles(letters, 6, 11)
    print("   div23_5n1 expanding rational cycles, words <= 11:", len(cycs))
    A = [F(-1), F(-4), F(-2)]
    B = [F(-84), F(-42), F(-21), F(-7), F(-34), F(-17)]
    sets = [set(p) for p, w in cycs]
    assert set(A) in sets and set(B) in sets
    # direct exact verification of A and B with the base step
    def bstep(y):
        u, v, w = div23_row_base(rmod(y, 6))
        return (u * y + v) / w
    for C, lam in ((A, F(5, 4)), (B, F(25, 24))):
        l = F(1)
        for i, y in enumerate(C):
            assert bstep(y) == C[(i + 1) % len(C)]
            u, v, w = div23_row_base(rmod(y, 6))
            l *= F(u, w)
        assert l == lam
    diffs = {abs(int(y - z)) for y in A for z in B}
    assert 0 not in diffs and max(diffs) == 83
    # q > 83: A and B alone already exclude every r (consistency of the bound, q up to 600)
    for q in range(84, 601):
        for r in range(q):
            assert not (any((y - r) % q == 0 for y in A) and any((z - r) % q == 0 for z in B))
    want = {'first': [(2, 0), (2, 1), (3, 1), (3, 2), (4, 2), (4, 3), (5, 1), (5, 3), (6, 2), (6, 5),
                      (8, 7), (10, 6), (15, 11), (15, 13), (30, 26)],
            'last': [(2, 1), (3, 2), (6, 5)]}
    nsim = 0
    for prio in ('first', 'last'):
        surv = []
        for q in range(2, 84):
            for r in range(q):
                witness = None
                for pts, word in cycs:
                    adm = (lambda i, pts=pts: True) if prio == 'first' else \
                        (lambda i, pts=pts: rmod(pts[i], 6) in (1, 5))
                    if not caught(q, {r}, pts, adm):
                        witness = (pts, word)
                        break
                if witness is None:
                    surv.append((q, r))
                else:
                    M0, row, step = div23_tamed(q, {r}, prio)
                    simulate_witness(6, q, {r}, witness[0], witness[1], letters, row, M0)
                    nsim += 1
        print("   %s survivors q<=83:" % prio, surv)
        assert surv == want[prio], (prio, surv)
    print("   every exclusion witnessed by an integer simulation (%d pairs)" % nsim)
    special = {('first', 2, 1): [(1,)], ('first', 3, 1): [(1,), (5, 26, 13)],
               ('first', 5, 1): [(1,)], ('first', 6, 2): [(1, 6, 3), (5, 26)],
               ('first', 10, 6): [(1, 6)], ('last', 2, 1): [(1,)]}
    for prio in ('first', 'last'):
        for q, r in want[prio]:
            M0, row, step = div23_tamed(q, {r}, prio)
            if prio == 'first' and (q, r) in ((2, 0), (4, 2)):
                assert certify(M0, row, maxnodes=100000, maxdepth=200) is None
                print("   %s (%d,%d): no certificate within budget (claimed open/unresolved)" % (prio, q, r))
                continue
            lv = certify(M0, row)
            assert lv is not None, (prio, q, r)
            cl, E = lemma_A(lv, step, row, M0)
            assert canon(cl) == canon(special.get((prio, q, r), [(1, 6, 3)])), (prio, q, r, cl)
            print("   %s (%d,%d): leaves=%d depth=%d |E|=%d cycles=%s" %
                  (prio, q, r, len(lv), max(x[4] for x in lv), len(E), cl))
    # named systems
    for name, q, r, nl in (("mb_d23_8", 8, 7, 93), ("mb_d23_4", 4, 3, 11), ("mb_d23_30", 30, 26, 12)):
        M0, row, step = div23_tamed(q, {r}, 'first')
        lv = certify(M0, row)
        cl, E = lemma_A(lv, step, row, M0)
        # leaf counts are engine-dependent (this engine splits on every prime of M0); the
        # prover's counts (nl) are not asserted, only the certificate's existence and cycles
        assert cl == [(1, 6, 3)], (name, len(lv), cl)
        print("   %s: certified (%d leaves in this engine; prover's engine %d), cycles %s" % (name, len(lv), nl, cl))


# --------------------------------------------------------------------------- C. Theorem M
def m3b_base(rho):
    return [(1, 0, 3), (4, -1, 3), (4, 1, 3)][rho % 3]


def m3b_tamed(q, R):
    M0 = lcm(3, q)

    def row(rho):
        if rho % q in R:
            return (1, (-(rho % q)) % q, q)
        return m3b_base(rho % 3)

    def step(n):
        u, v, w = row(n % M0)
        assert (u * n + v) % w == 0
        return (u * n + v) // w
    return M0, row, step


def section_M():
    print("== C. Theorem M")
    letters = [(1, 0, 3, {0}), (4, -1, 3, {1}), (4, 1, 3, {2})]
    cycs = word_cycles(letters, 3, 11)
    print("   m3_b expanding rational cycles, words <= 11:", len(cycs))
    sets = [set(p) for p, w in cycs]
    C1 = {F(1, 7), F(-1, 7)}
    C2 = {F(7, 25), F(1, 25), F(-7, 25), F(-1, 25)}
    assert {F(1)} in sets and {F(-1)} in sets and C1 in sets and C2 in sets
    # one class: must contain the integer fixed points 1 and -1
    assert [(q, r) for q in range(2, 500) for r in range(q) if (1 - r) % q == 0 and (-1 - r) % q == 0] == [(2, 1)]
    M0, row, step = m3b_tamed(2, {1})
    lv = certify(M0, row)
    cl, E = lemma_A(lv, step, row, M0)
    assert cl == [(1,), (2, 3)], cl
    print("   odd -> (n+1)/2: leaves=%d cycles=%s" % (len(lv), cl))
    # two classes {1,-1} mod q: scan to 400 with all enumerated cycles (claim: q<=32 suffices)
    nums2 = {abs((y - e).numerator) for y in C2 for e in (1, -1)}
    assert nums2 == {18, 24, 26, 32}
    surv, nsim = [], 0
    for q in range(3, 401):
        R = {1 % q, (-1) % q}
        wit = None
        for pts, word in cycs:
            if not caught(q, R, pts, lambda i: True):
                wit = (pts, word)
                break
        if wit is None:
            surv.append(q)
        else:
            M0, row, step = m3b_tamed(q, R)
            simulate_witness(3, q, R, wit[0], wit[1], letters, row, M0)
            nsim += 1
    print("   {1,-1} mod q survivors, 3<=q<=400:", surv, "(%d exclusions simulated)" % nsim)
    assert surv == [3, 4, 6, 8]
    # the bound argument itself: for q > 32 either C1 (refined) or C2 excludes q
    for q in range(33, 3000):
        R = {1 % q, (-1) % q}
        C1l, C2l = sorted(C1), sorted(C2)
        assert not caught(q, R, C1l, lambda i: True) or not caught(q, R, C2l, lambda i: True), q
    for q in surv:
        M0, row, step = m3b_tamed(q, {1 % q, (-1) % q})
        lv = certify(M0, row)
        cl, E = lemma_A(lv, step, row, M0)
        assert cl == [(1,)], (q, cl)
        print("   q=%d: leaves=%d cycles=%s" % (q, len(lv), cl))
    M0, row, step = m3b_tamed(8, {1, 7})
    assert all(step(n) == ((n + 7) // 8 if n % 8 == 1 else (n + 1) // 8 if n % 8 == 7 else
                           n // 3 if n % 3 == 0 else (4 * n - 1) // 3 if n % 3 == 1 else (4 * n + 1) // 3)
               for n in range(1, 5000))


# --------------------------------------------------------------------------- D. other systems
def classes_tamed(a, m, R):
    M0 = lcm(2, m)

    def row(rho):
        if rho % m in R:
            return (1, (-(rho % m)) % m, m)
        if rho % 2 == 0:
            return (1, 0, 2)
        return (a, 1, 2)

    def step(n):
        u, v, w = row(n % M0)
        return (u * n + v) // w
    return M0, row, step


def hitting_min_atleast(constraints, k):
    """True iff no set of <= k-1 residues meets every constraint (exact branching)."""
    cons = sorted({frozenset(c) for c in constraints}, key=len)
    # drop supersets
    red = []
    for c in cons:
        if not any(d <= c for d in red):
            red.append(c)

    def can(rem, budget):
        if not rem:
            return True
        if budget == 0:
            return False
        c = min(rem, key=len)
        for x in c:
            if can([d for d in rem if x not in d], budget - 1):
                return True
        return False
    return not can(red, k - 1)


def section_other():
    print("== D. single-class and sparse systems")
    sysd = [("mb_s3_3", 3, 3, {2}, [(1, 2)]), ("mb_s3_9", 3, 9, {8}, [(1, 2)]),
            ("mb_s5_5", 5, 5, {3}, [(1, 3)]), ("mb_s7_7", 7, 7, {4}, [(1, 4)]),
            ("mb_t27", 3, 27, {17, 26}, [(1, 2)]), ("mb_t81", 3, 81, {20, 71, 80}, [(1, 2)]),
            ("mb_t243", 3, 243, {137, 152, 233, 242}, [(1, 2)]),
            ("mb_t729", 3, 729, {182, 380, 395, 425, 668, 719, 728}, [(1, 2)]),
            ("mb_f25", 5, 25, {8, 23}, [(1, 3, 8)]), ("mb_f125", 5, 125, {68, 73, 83, 123}, [(1, 3, 8, 4, 2)]),
            ("mb_s49", 7, 49, {32, 39}, [(1, 4, 2)]),
            ("mb_s343", 7, 343, {93, 137, 142, 200, 228}, [(1, 4, 2)])]
    for name, a, m, R, want in sysd:
        M0, row, step = classes_tamed(a, m, R)
        lv = certify(M0, row, maxnodes=2000000)
        assert lv is not None, name
        cl, E = lemma_A(lv, step, row, M0)
        assert cl == want, (name, cl)
        print("   %s: leaves=%d depth=%d cycles=%s" % (name, len(lv), max(x[4] for x in lv), cl))
    # minimality lower bounds: own cycle enumeration of n/2 | (an+1)/2, own hitting set
    print("   minimality:")
    for a, wl, mods in ((3, 16, ((27, 2), (81, 3), (243, 4), (729, 7))),
                        (5, 14, ((25, 2), (125, 4))), (7, 14, ((49, 2), (343, 5)))):
        letters = [(1, 0, 2, {0}), (a, 1, 2, {1})]
        cycs = word_cycles(letters, 2, wl)
        for m, k in mods:
            cons = [{rmod(y, m) for y in pts} for pts, w in cycs]  # denominators 2^L - a^j, prime to a
            assert hitting_min_atleast(cons, k), (a, m, k)
            print("     a=%d m=%d: %d cycles (words<=%d), no set of %d classes hits all -> min >= %d"
                  % (a, m, len(cycs), wl, k - 1, k))


# --------------------------------------------------------------------------- E. evidence
def section_evidence():
    print("== E. EVIDENCE: random 300-bit starts")
    tests = [("mb_d23_30", div23_tamed(30, {26}, 'first')[2], {1, 6, 3}),
             ("first(3,1)", div23_tamed(3, {1}, 'first')[2], {1, 5, 26, 13}),
             ("mb_m3b_8", m3b_tamed(8, {1, 7})[2], {1}),
             ("m3b+odd", m3b_tamed(2, {1})[2], {1, 2, 3}),
             ("mb_t729", classes_tamed(3, 729, {182, 380, 395, 425, 668, 719, 728})[2], {1, 2})]
    for name, step, cyc in tests:
        for _ in range(100):
            x = random.getrandbits(300) | 1
            for _ in range(200000):
                if x in cyc:
                    break
                x = step(x)
            assert x in cyc, name
        print("   %s: 100 starts reach the listed cycles" % name)


if __name__ == "__main__":
    section_D()
    section_M()
    section_other()
    section_evidence()
    print("REFEREE2 CHECK: ALL OK")
