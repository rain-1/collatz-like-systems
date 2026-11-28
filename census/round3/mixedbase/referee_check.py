"""Independent referee check for lens "mixedbase" (round 3).

Written from scratch: imports NOTHING from the prover's code (mixedlib, pairlib, check_*,
systems.py).  Every map is re-typed from the written rules in the .md files.

Parts
  A. own descent-certificate engine + own Lemma A' (exceptional set, cycles) for all 16
     certified systems; leaf identities re-tested numerically with random 100-bit t.
  B. own enumeration of expanding cycles of n -> (a n+1)/2 | n/2 and own exact hitting-set
     search: minimality of the taming sets (lower bounds), and that each claimed R hits all.
  C. single classes: the case analysis of S3/S5 re-run with explicit witnesses
     (runs simulated on actual CRT-built integers, D'' words verified exactly), S7 for m<=199.
  D. pairing family: block lemma P1 (random 300-bit n, many parameters), P3 descent
     inequality, cycle lists, P5 obstruction cycles exactly.
  E. relatives: Theorem D and M necessity with the REPAIRED bound arguments (see REFEREE.md):
     div23: integer cycle (-84 ...) bounds q <= 83 for every q; m3_b: refined Lemma B'
     (only the q-part prime to the denominator must match) + a second cycle prime to 7.
  F. random large-n descent spot checks (EVIDENCE only).
Exit 0 iff every assertion holds.  Runtime ~1-2 min.
"""
import math, random, sys
from fractions import Fraction as F

random.seed(20261127)
FAIL = []


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("FAIL:", msg)


# ------------------------------------------------------------------ helpers
def primes_of(n):
    ps, p = [], 2
    while p * p <= n:
        if n % p == 0:
            ps.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        ps.append(n)
    return ps


def rmod(x, m):
    """residue of rational x (denominator prime to m) mod m"""
    x = F(x)
    return (x.numerator * pow(x.denominator, -1, m)) % m


def lyndon(k, n):
    """Duval: all Lyndon words over range(k) of length 1..n"""
    w = [-1]
    while w:
        w[-1] += 1
        yield tuple(w)
        m = len(w)
        while len(w) < n:
            w.append(w[len(w) - m])
        while w and w[-1] == k - 1:
            w.pop()


# ------------------------------------------------------------------ step functions (from rule text)
def mk_classes(a, m, Rc, b=1):
    """Rc: dict r -> c ; class first, then even n/2, else (a n + b)/2"""
    def T(n):
        r = n % m
        if r in Rc:
            assert (n + Rc[r]) % m == 0
            return (n + Rc[r]) // m
        if n % 2 == 0:
            return n // 2
        return (a * n + b) // 2
    def row(rho):  # rho mod 2m
        r = rho % m
        if r in Rc:
            return (1, Rc[r], m)
        if rho % 2 == 0:
            return (1, 0, 2)
        return (a, b, 2)
    return T, row, 2 * m


def mk_div23(q, Rc, prio="first"):
    def base(n):
        if n % 2 == 0:
            return (1, 0, 2)
        if n % 3 == 0:
            return (1, 0, 3)
        return (5, 1, 1)
    def row(rho):
        b = base(rho)
        if rho % q in Rc and (prio == "first" or b[0] == 5):
            return (1, Rc[rho % q], q)
        return b
    def T(n):
        u, v, w = row(n)
        assert (u * n + v) % w == 0
        return (u * n + v) // w
    return T, row, math.lcm(6, q)


def mk_m3b(q, Rc):
    def row(rho):
        if rho % q in Rc:
            return (1, Rc[rho % q], q)
        return [(1, 0, 3), (4, -1, 3), (4, 1, 3)][rho % 3]
    def T(n):
        u, v, w = row(n)
        assert (u * n + v) % w == 0
        return (u * n + v) // w
    return T, row, math.lcm(3, q)


# ------------------------------------------------------------------ A. engine
def certify(M0, row, maxleaves=100000, maxdepth=400):
    """n = M t + r (t >= 0), T^j(n) = P t + Q.  Close at first j>=1 with P<M or (P==M, Q<r)."""
    leaves = []
    stack = [(1, 0, 1, 0, 0)]
    while stack:
        M, r, P, Q, j = stack.pop()
        if j >= 1 and (P < M or (P == M and Q < r)):
            leaves.append((M, r, P, Q, j))
            if len(leaves) > maxleaves:
                return None
            continue
        if j > maxdepth:
            return None
        g = math.gcd(P, M0)
        rws = {row((Q + g * s) % M0) for s in range(M0 // g)}
        u, v, w = next(iter(rws))
        if len(rws) == 1 and (u * P) % w == 0 and (u * Q + v) % w == 0:
            # same row on the whole progression P t + Q, division exact for every t
            stack.append((M, r, u * P // w, (u * Q + v) // w, j + 1))
        else:
            p = min(primes_of(M0 // math.gcd(P, M0)))
            for s in range(p):
                stack.append((M * p, r + s * M, P * p, Q + s * P, j))
    return leaves


def lemmaA(leaves, T, domain_min=1, cap=10**6):
    E = []
    for M, r, P, Q, j in leaves:
        if P < M and Q >= r:
            tmax = (Q - r) // (M - P)
            for t in range(tmax + 1):
                n = M * t + r
                if n >= domain_min:
                    E.append(n)
    cycles = set()
    for e in E:
        seen = {}
        x, k = e, 0
        while x not in seen:
            seen[x] = k
            x = T(x)
            k += 1
            assert k < cap
        cyc = [x]
        y = T(x)
        while y != x:
            cyc.append(y)
            y = T(y)
        i = cyc.index(min(cyc))
        cycles.add(tuple(cyc[i:] + cyc[:i]))
    return E, sorted(cycles)


def partition_ok(leaves):
    # leaves partition N0: total density 1 and pairwise disjoint (checked via sorting by tree)
    dens = sum(F(1, M) for M, *_ in leaves)
    if dens != 1:
        return False
    # disjointness: no leaf class contains another's representative at a coarser level
    byM = {}
    for M, r, *_ in leaves:
        byM.setdefault(M, set()).add(r)
    Ms = sorted(byM)
    for M, r, *_ in leaves:
        for M2 in Ms:
            if M2 < M and M % M2 == 0 and (r % M2) in byM[M2]:
                return False
    return True


def leaf_numeric(leaves, T, ntests=3):
    for M, r, P, Q, j in leaves:
        for _ in range(ntests):
            t = random.getrandbits(100)
            n = M * t + r
            x = n
            for _ in range(j):
                x = T(x)
            if x != P * t + Q:
                return False
    return True


def part_A():
    print("== A. certificates (own engine) + Lemma A'")
    specs = []
    specs.append(("mb_s3_3", *mk_classes(3, 3, {2: 1}), [(1, 2)]))
    specs.append(("mb_s3_9", *mk_classes(3, 9, {8: 1}), [(1, 2)]))
    specs.append(("mb_s5_5", *mk_classes(5, 5, {3: 2}), [(1, 3)]))
    specs.append(("mb_s7_7", *mk_classes(7, 7, {4: 3}), [(1, 4)]))
    for sid, a, m, R, cyc in [
            ("mb_t27", 3, 27, (17, 26), [(1, 2)]),
            ("mb_t81", 3, 81, (20, 71, 80), [(1, 2)]),
            ("mb_t243", 3, 243, (137, 152, 233, 242), [(1, 2)]),
            ("mb_t729", 3, 729, (182, 380, 395, 425, 668, 719, 728), [(1, 2)]),
            ("mb_f25", 5, 25, (8, 23), [(1, 3, 8)]),
            ("mb_f125", 5, 125, (68, 73, 83, 123), [(1, 3, 8, 4, 2)]),
            ("mb_s49", 7, 49, (32, 39), [(1, 4, 2)]),
            ("mb_s343", 7, 343, (93, 137, 142, 200, 228), [(1, 4, 2)])]:
        specs.append((sid, *mk_classes(a, m, {r: (-r) % m for r in R}), cyc))
    specs.append(("mb_d23_8", *mk_div23(8, {7: 1}), [(1, 6, 3)]))
    specs.append(("mb_d23_4", *mk_div23(4, {3: 1}), [(1, 6, 3)]))
    specs.append(("mb_d23_30", *mk_div23(30, {26: 4}), [(1, 6, 3)]))
    specs.append(("mb_m3b_8", *mk_m3b(8, {1: 7, 7: 1}), [(1,)]))
    for sid, T, row, M0, cyc in specs:
        L = certify(M0, row)
        check(L is not None, sid + " own engine found no certificate")
        if L is None:
            continue
        check(partition_ok(L), sid + " leaves do not partition")
        check(leaf_numeric(L, T), sid + " leaf identity fails numerically")
        E, cycles = lemmaA(L, T)
        check(cycles == cyc, f"{sid} cycles {cycles} != claimed {cyc}")
        print(f"  {sid:10s} M0={M0:5d} leaves={len(L):5d} maxj={max(l[4] for l in L):3d} |E|={len(E)} cycles={cycles}")


# ------------------------------------------------------------------ B. expanding plain cycles + hitting sets
def plain_cycles(a, L):
    """expanding cycles of U:y->(a y+1)/2 (odd), D:y->y/2 (even). letter 0=U, 1=D."""
    out = {}
    for w in lyndon(2, L):
        k = w.count(0)
        if a ** k <= 2 ** len(w):
            continue
        lam, mu = F(1), F(0)
        for c in w:
            if c == 0:
                lam, mu = lam * a / 2, (a * mu + 1) / 2
            else:
                lam, mu = lam / 2, mu / 2
        y = mu / (1 - lam)
        orb, z, ok = [], y, True
        for c in w:
            if z.denominator % 2 == 0 or (z.numerator % 2 == 1) != (c == 0):
                ok = False
                break
            orb.append(z)
            z = (a * z + 1) / 2 if c == 0 else z / 2
        check(ok and z == y, f"word {w} fixed point does not follow word")
        out[min(orb)] = orb
    return list(out.values())


def has_hitting_set(sets, s):
    sets = sorted(set(sets), key=lambda A: bin(A).count('1'))
    # drop supersets
    red = []
    for A in sets:
        if not any((B & A) == B for B in red):
            red.append(A)
    sets = red

    def lb(unhit):
        used, cnt = 0, 0
        for A in unhit:
            if not (A & used):
                used |= A
                cnt += 1
        return cnt

    def rec(chosen, budget):
        unhit = [A for A in sets if not (A & chosen)]
        if not unhit:
            return True
        if budget == 0 or lb(unhit) > budget:
            return False
        A = unhit[0]
        e = A
        while e:
            bit = e & -e
            e ^= bit
            if rec(chosen | bit, budget - 1):
                return True
        return False
    return rec(0, s)


def part_B():
    print("== B. minimality of taming sets (own cycle enumeration + own hitting-set search)")
    cases = [(3, 27, 2, (17, 26), 14), (3, 81, 3, (20, 71, 80), 16),
             (3, 243, 4, (137, 152, 233, 242), 18),
             (3, 729, 7, (182, 380, 395, 425, 668, 719, 728), 20),
             (5, 25, 2, (8, 23), 14), (5, 125, 4, (68, 73, 83, 123), 18),
             (7, 49, 2, (32, 39), 14), (7, 343, 5, (93, 137, 142, 200, 228), 16)]
    cyccache = {}
    for a, m, mn, R, L in cases:
        if (a, L) not in cyccache:
            cyccache[(a, L)] = plain_cycles(a, L)
        cyc = cyccache[(a, L)]
        sets = []
        for orb in cyc:
            check(all(math.gcd(z.denominator, m) == 1 for z in orb), "denominator not prime to m")
            mask = 0
            for z in orb:
                mask |= 1 << rmod(z, m)
            sets.append(mask)
        Rmask = sum(1 << r for r in R)
        check(all(A & Rmask for A in sets), f"claimed R={R} mod {m} misses an expanding cycle")
        no_small = not has_hitting_set(sets, mn - 1)
        check(no_small, f"a={a} m={m}: hitting set of size {mn-1} exists")
        print(f"  a={a} m={m}: {len(cyc)} expanding cycles (words<={L}); no hitting set of size {mn-1}: {no_small}")


# ------------------------------------------------------------------ C. single classes
def run_uncaught(a, b, m, r, c, n, steps, xstar):
    """simulate actual T from integer n; assert odd-branch run never caught; identity holds"""
    T = mk_classes(a, m, {r: c}, b)[0]
    x = n
    for i in range(steps):
        if x % m == r or x % 2 == 0:
            return False
        x2 = T(x)
        if x2 - xstar != F(a, 2) * (x - xstar):
            return False
        x = x2
    return True


def crt(res):
    n, M = 0, 1
    for r, m in res:
        # solve n' = n mod M, n' = r mod m
        g = math.gcd(M, m)
        assert (r - n) % g == 0
        l = M // g * m
        k = ((r - n) // g * pow(M // g, -1, m // g)) % (m // g)
        n = (n + M * k) % l
        M = l
    return n, M


def cycle_uncaught(orb, a, b, m, r):
    """exact: orbit is a T^-cycle of the tamed map (no point in class r mod m)."""
    if any(math.gcd(z.denominator, 2 * m) > 1 for z in orb):
        return False
    return all(rmod(z, m) != r for z in orb)


def word_point(a, b, m, r, c, word):
    """fixed point of word over U (odd branch), D (halve), Q (class); verify exactly."""
    lam, mu = F(1), F(0)
    for ch in word:
        if ch == "U":
            lam, mu = lam * a / 2, (a * mu + b) / 2
        elif ch == "D":
            lam, mu = lam / 2, mu / 2
        else:
            lam, mu = lam / m, (mu + c) / m
    y = mu / (1 - lam)
    z = y
    for ch in word:
        if math.gcd(z.denominator, 2 * m) > 1:
            return None
        caught = rmod(z, m) == r
        if ch == "Q":
            if not caught:
                return None
            z = (z + c) / m
        else:
            if caught or (z.numerator % 2 == 1) != (ch == "U"):
                return None
            z = (a * z + b) / 2 if ch == "U" else z / 2
    return (y, lam) if z == y else None


def part_C():
    print("== C. single taming classes (S3, S5 case analyses with exact witnesses; S7 m<=199)")
    N = 30
    # ---- S3
    cyc3 = [F(-5), F(-7), F(-10)]
    cnt = {}
    for m in range(3, 152, 2):
        for r in range(m):
            for c in {(-r) % m, (-r) % m - m}:
                if (m, r) in [(3, 2), (9, 8)]:
                    continue
                if r != (-1) % m:
                    ok = cycle_uncaught([F(-1)], 3, 1, m, r); kind = "fixed"
                elif m % 3:
                    n, _ = crt([((-1) % 2 ** N, 2 ** N), (0, m)])
                    n += 2 ** N * m * random.getrandbits(40)
                    ok = run_uncaught(3, 1, m, r, c, n, N - 1, F(-1)); kind = "run"
                else:
                    ok = cycle_uncaught(cyc3, 3, 1, m, r); kind = "cycle"
                check(ok, f"S3 witness fails m={m} r={r} c={c}")
                cnt[kind] = cnt.get(kind, 0) + 1
    print("  S3 witnesses verified, odd m<=151:", cnt)
    # ---- S5
    xs = F(-1, 3)
    c2 = [F(-1), F(-2)]
    c3 = [F(-14, 17), F(-7, 17), F(-9, 17)]
    cnt = {}
    Dcache = {}
    for m in range(3, 152, 2):
        k3 = 0
        mm = m
        while mm % 3 == 0:
            mm //= 3; k3 += 1
        l5 = 0
        while mm % 5 == 0:
            mm //= 5; l5 += 1
        m2 = mm
        for r in range(m):
            c = (-r) % m
            if (m, r) == (5, 3):
                continue
            if k3 == 0:
                if (3 * r + 1) % m:
                    ok = cycle_uncaught([xs], 5, 1, m, r); kind = "fixed"
                elif m2 > 1:
                    x0 = rmod(xs, 2 ** N)
                    n, _ = crt([(x0, 2 ** N), (0, m)])
                    ok = run_uncaught(5, 1, m, r, c, n + 2 ** N * m * random.getrandbits(40), N - 1, xs)
                    kind = "run"
                else:
                    ok = cycle_uncaught(c2, 5, 1, m, r); kind = "cycle(-1 -2)"
            elif m2 > 1:
                x0 = rmod(xs, 2 ** N)
                base = 0 if rmod(xs, m2) == r % m2 else rmod(xs, m2)
                n, _ = crt([(x0, 2 ** N), (base, m2)])
                ok = run_uncaught(5, 1, m, r, c, n + 2 ** N * m * random.getrandbits(40), N - 1, xs)
                kind = "run(m'')"
            elif l5 == 0:
                # m = 3^k: word U^(m-1) Q
                if m not in Dcache:
                    Dcache[m] = None
                res = word_point(5, 1, m, r, c, "U" * (m - 1) + "Q")
                ok = res is not None and res[1] > 1
                kind = "word"
            else:
                five = 5 ** l5
                if r % five != rmod(xs, five):
                    x0 = rmod(xs, 2 ** N)
                    n, _ = crt([(x0, 2 ** N), (rmod(xs, five), five)])
                    ok = run_uncaught(5, 1, m, r, c, n + 2 ** N * m * random.getrandbits(40), N - 1, xs)
                    kind = "run(5^l)"
                else:
                    ok = cycle_uncaught(c2, 5, 1, m, r) or cycle_uncaught(c3, 5, 1, m, r)
                    kind = "cycles"
            check(ok, f"S5 witness fails m={m} r={r} kind={kind}")
            cnt[kind] = cnt.get(kind, 0) + 1
    print("  S5 witnesses verified, odd m<=151:", cnt)
    # verify the two auxiliary cycles exactly under plain map
    for orb in (c2, c3):
        for i, z in enumerate(orb):
            nz = (5 * z + 1) / 2 if z.numerator % 2 else z / 2
            check(nz == orb[(i + 1) % len(orb)], "aux cycle wrong")
    # ---- S7 (m <= 199): need an expanding plain cycle prime to m missing r
    cyc7 = plain_cycles(7, 14)
    bad = []
    for m in range(3, 200, 2):
        sets = []
        for orb in cyc7:
            if all(math.gcd(z.denominator, m) == 1 for z in orb):
                sets.append({rmod(z, m) for z in orb})
        for r in range(m):
            if all(r in S for S in sets):
                bad.append((m, r))
    check(bad == [(7, 4)], f"S7 survivors {bad}")
    print("  S7 survivors (odd m<=199):", bad)


# ------------------------------------------------------------------ D. pairing family
def pair_T(a, K, xs):
    m = a ** K
    r = (xs * pow(2, -1, m)) % m
    c = (m - 1) * xs // 2
    b = (2 - a) * xs
    def T(n):
        if n % m == r:
            assert (n + c) % m == 0
            return (n + c) // m
        if n % 2 == 0:
            return n // 2
        return (a * n + b) // 2
    return T, m, r, c, b


def part_D():
    print("== D. pairing family")
    # named systems match the parameterisation
    for (a, K, xs), (rr, cc, bb) in {(3, 2, 1): (5, 4, -1), (3, 2, -1): (4, -4, 1),
                                      (7, 1, -1): (3, -3, 5), (5, 1, -1): (2, -2, 3),
                                      (3, 3, -1): (13, -13, 1), (5, 2, 1): (13, 12, -3)}.items():
        _, m, r, c, b = pair_T(a, K, xs)
        check((r, c, b) == (rr, cc, bb), f"pairing param mismatch {(a,K,xs)}")
    # P1 block lemma
    tests = 0
    for a in (3, 5, 7, 9, 11, 15, 21):
        for K in (1, 2, 3, 4):
            for xs in (1, -1, 5, -7, 11, 13, -17):
                if math.gcd(a, xs) != 1:
                    continue
                T, m, r, c, b = pair_T(a, K, xs)
                cand = [random.getrandbits(300) * random.choice((1, -1)) | 1 for _ in range(40)]
                cand += [n for n in range(-401, 402, 2)]
                for n in cand:
                    if n % m == r or n == xs:
                        continue
                    d = n - xs
                    j = (d & -d).bit_length() - 1
                    u = d >> j
                    q, l = divmod(j, K)
                    x = n
                    for _ in range(j + 1 + q):
                        x = T(x)
                    check(2 * x == xs + a ** l * u, f"P1 fails a={a} K={K} x*={xs} n={n}")
                    tests += 1
    print("  P1 block lemma tests:", tests)
    # P3 descent inequality on actual orbits, + cycle lists
    for a, K in [(3, 1), (5, 1), (7, 1), (9, 1), (13, 1), (3, 2)]:
        B = 1 if K == 1 else 5
        for xs in (1, -1, 3 if a % 3 else 5, -5 if a % 5 else -7, 19, -23):
            if math.gcd(a, xs) != 1:
                continue
            T, m, r, c, b = pair_T(a, K, xs)
            ns = list(range(-3000, 3001)) + [random.getrandbits(256) * random.choice((1, -1)) for _ in range(300)]
            for n in ns:
                if abs(n) <= B * abs(xs):
                    continue
                x, k = T(n), 1
                while abs(x) >= abs(n):
                    x = T(x); k += 1
                    if k > 4 * abs(n).bit_length() + 50:
                        check(False, f"P3 no descent a={a} K={K} x*={xs} n={n}")
                        break
    # cycle lists for named systems (simulate |n| <= B|x*| in the domain)
    def cycles_of(T, start):
        cyc = set()
        for e in start:
            seen = set(); x = e
            while x not in seen:
                seen.add(x); x = T(x)
            cy = [x]; y = T(x)
            while y != x:
                cy.append(y); y = T(y)
            i = cy.index(min(cy)); cyc.add(tuple(cy[i:] + cy[:i]))
        return sorted(cyc)
    T = pair_T(3, 2, 1)[0]
    check(cycles_of(T, range(-5, 6)) == [(-2, -1), (0,), (1,)], "P(3,2,1) Z cycles")
    check(cycles_of(T, range(1, 6)) == [(1,)], "mb_pair_3_9p cycles")
    T = pair_T(3, 2, -1)[0]
    check(cycles_of(T, range(0, 6)) == [(0,), (1, 2)], "mb_pair_3_9m cycles")
    check(cycles_of(pair_T(7, 1, -1)[0], range(0, 2)) == [(0,)], "mb_pair_7_7m")
    check(cycles_of(pair_T(5, 1, -1)[0], range(0, 2)) == [(0,)], "mb_pair_5_5m")
    for a in range(3, 41, 2):
        check(cycles_of(pair_T(a, 1, 1)[0], range(1, 2)) == [(1,)], "K=1 N+")
    # P5 obstruction cycles, exact (rational T^ with S-adic residues)
    def That(a, K, xs, y):
        m = a ** K
        r = (xs * pow(2, -1, m)) % m
        if rmod(y, m) == r:
            return (y + F((m - 1) * xs, 2)) / m
        if y.numerator % 2 == 0:
            return y / 2
        return (a * y + (2 - a) * xs) / 2
    cnt = 0
    for a in range(5, 40, 2):
        for K in range(2, 7):
            for xs in (1, -1, 3, -5, 7, 11):
                if math.gcd(a, xs) != 1:
                    continue
                y = F((2 - a) * xs, 4 - a)
                check(math.gcd(y.denominator, 2 * a) == 1, "P5 denominator")
                check(That(a, K, xs, y) == 2 * y and That(a, K, xs, 2 * y) == y, f"P5 2-cycle a={a} K={K}")
                # K=1 caught
                check(That(a, 1, xs, y) != 2 * y, f"P5 K=1 should be caught a={a}")
                cnt += 1
    for K in range(3, 9):
        for xs in (1, -1, 5, -7, 11):
            if xs % 3 == 0:
                continue
            z = F(5 * xs)
            seq = [z]
            for _ in range(3):
                seq.append(That(3, K, xs, seq[-1]))
            check(seq == [5 * xs, 7 * xs, 10 * xs, 5 * xs], f"P5 a=3 K={K} cycle")
            cnt += 1
    for K in (1, 2):
        z = F(5); seq = [z]
        for _ in range(3):
            seq.append(That(3, K, 1, seq[-1]))
        check(seq != [5, 7, 10, 5], "a=3 K<=2 should catch")
    print("  P3 inequality, cycle lists, P5 cycles verified;", cnt, "P5 instances")


# ------------------------------------------------------------------ E. relatives (repaired bounds)
def gen_cycles(M0, rows, L):
    """rows: list of (u,v,w, pred(res mod M0)). expanding rational cycles, den prime to M0."""
    out = {}
    ps = primes_of(M0)
    for wd in lyndon(len(rows), L):
        lam, mu = F(1), F(0)
        for i in wd:
            u, v, w, _ = rows[i]
            lam, mu = lam * F(u, w), (u * mu + v) / w
        if lam <= 1:
            continue
        y = mu / (1 - lam)
        if any(y.denominator % p == 0 for p in ps):
            continue
        z, orb, ok = y, [], True
        for i in wd:
            u, v, w, pred = rows[i]
            if not pred(rmod(z, M0)):
                ok = False; break
            orb.append(z); z = (u * z + v) / w
        if ok and z == y:
            out[min(orb)] = orb
    return list(out.values())


# actual complete cycle lists (own engine + Lemma A') where they differ from the claimed (1 6 3)
ACTUAL_D23 = {("first", 2, 1): [(1,)], ("first", 3, 1): [(1,), (5, 26, 13)], ("first", 5, 1): [(1,)],
              ("first", 6, 2): [(1, 6, 3), (5, 26)], ("first", 10, 6): [(1, 6)], ("last", 2, 1): [(1,)]}


def part_E():
    print("== E. relatives: Theorem D / M necessity with repaired bound arguments")
    rows = [(1, 0, 2, lambda x: x % 2 == 0), (1, 0, 3, lambda x: x % 2 == 1 and x % 3 == 0),
            (5, 1, 1, lambda x: x % 2 == 1 and x % 3 != 0)]
    cyc = gen_cycles(6, rows, 11)
    A = [F(-1), F(-4), F(-2)]
    Bc = [F(-84), F(-42), F(-21), F(-7), F(-34), F(-17)]
    check(any(set(o) == set(A) for o in cyc), "(-1 -4 -2) missing")
    check(any(set(o) == set(Bc) for o in cyc), "(-84 ...) integer cycle missing")
    bound = int(max(abs(y - z) for y in A for z in Bc))
    print(f"  div23: integer expanding cycles (-1 -4 -2) and (-84 -42 -21 -7 -34 -17): any q has q | y-z, q <= {bound}")

    def survivors(q, prio):
        out = []
        for r in range(q):
            ok = True
            for orb in cyc:
                # refined Lemma B': q1 = part of q prime to the denominators
                d = math.lcm(*[z.denominator for z in orb])
                q1 = q
                for p in primes_of(q):
                    if d % p == 0:
                        while q1 % p == 0:
                            q1 //= p
                pts = [z for z in orb if prio == "first" or (z.numerator % 2 and rmod(z, 3) != 0)]
                if not any(rmod(z, q1) == r % q1 for z in pts) if q1 > 1 else not pts:
                    ok = False; break
            if ok:
                out.append((q, r))
        return out
    surv = {"first": [], "last": []}
    for q in range(2, bound + 1):
        for prio in surv:
            surv[prio] += survivors(q, prio)
    claimed = {"first": [(2, 0), (2, 1), (3, 1), (3, 2), (4, 2), (4, 3), (5, 1), (5, 3), (6, 2), (6, 5),
                         (8, 7), (10, 6), (15, 11), (15, 13), (30, 26)],
               "last": [(2, 1), (3, 2), (6, 5)]}
    check(surv == claimed, f"div23 survivors {surv}")
    print("  div23 survivors (q <= bound, refined criterion) equal the claimed list:", surv == claimed)
    for prio in surv:
        for q, r in surv[prio]:
            if (prio, q, r) in [("first", 2, 0), ("first", 4, 2)]:
                continue
            T, row, M0 = mk_div23(q, {r: (-r) % q}, prio)
            L = certify(M0, row, maxleaves=50000)
            check(L is not None, f"div23 {prio} {q} {r} not certified")
            if L:
                E, cy = lemmaA(L, T)
                exp = ACTUAL_D23.get((prio, q, r), [(1, 6, 3)])
                check(cy == exp, f"div23 {prio} {q} {r} cycles {cy}")
                if cy != [(1, 6, 3)]:
                    print(f"  ** relatives.md claims cycle (1 6 3) for {prio} ({q},{r}); actual complete list: {cy}")
    print("  all listed div23 pairs except first (2,0),(4,2) certified by own engine")
    # ---- m3_b
    rows3 = [(1, 0, 3, lambda x: x % 3 == 0), (4, -1, 3, lambda x: x % 3 == 1), (4, 1, 3, lambda x: x % 3 == 2)]
    cyc3 = gen_cycles(3, rows3, 9)
    C1 = [o for o in cyc3 if F(1, 7) in o]
    check(len(C1) == 1 and set(C1[0]) == {F(1, 7), F(-1, 7)}, "1/7 cycle")
    # q = 7^e q1, q1 | num(z -+ 1) for z in C1 (refined lemma)
    nums = {abs((z - s).numerator) for z in C1[0] for s in (1, -1)}
    # second cycle with denominator prime to 7, smallest numerators
    cand = [o for o in cyc3 if all(z.denominator % 7 for z in o) and len(o) > 1]
    C2 = min(cand, key=lambda o: max(abs((z - s).numerator) for z in o for s in (1, -1)))
    b2 = max(abs((z - s).numerator) for z in C2 for s in (1, -1))
    print(f"  m3_b: 1/7-cycle numerators {sorted(nums)}; second cycle {[str(z) for z in C2]} (den prime to 42),"
          f" bound for q with primes in {{2,3,7}}: {b2}")
    check(all(math.gcd(z.denominator, 42) == 1 for z in C2), "C2 den")
    bound3 = max(max(nums), b2)
    survm = []
    for q in range(3, bound3 + 1):
        Rq = {1 % q, (-1) % q}
        ok = True
        for orb in cyc3:
            d = math.lcm(*[z.denominator for z in orb])
            q1 = q
            for p in primes_of(q):
                if d % p == 0:
                    while q1 % p == 0:
                        q1 //= p
            if q1 == 1:
                continue
            if not any(rmod(z, q1) in {s % q1 for s in Rq} for z in orb):
                ok = False; break
        if ok:
            survm.append(q)
    check(survm == [3, 4, 6, 8], f"m3_b survivors {survm}")
    print("  m3_b + {1,-1} mod q survivors for q <=", bound3, ":", survm)
    for q in survm:
        T, row, M0 = mk_m3b(q, {1 % q: (-1) % q, (-1) % q: 1})
        L = certify(M0, row)
        check(L is not None, f"m3b q={q} no cert")
        if L:
            check(lemmaA(L, T)[1] == [(1,)], f"m3b q={q} cycles")
    T, row, M0 = mk_m3b(2, {1: 1})
    L = certify(M0, row)
    cy = lemmaA(L, T)[1] if L else None
    check(L is not None and cy == [(1,), (2, 3)], "m3b odd class")
    print("  m3_b survivors q=3,4,6,8 certified with cycle (1) only")
    print(f"  ** m3_b + (odd -> (n+1)/2) is certified, but its complete cycle list is {cy}, not (1) only "
          "(2 -> 3 -> 2)")


# ------------------------------------------------------------------ F. evidence
def part_F():
    print("== F. random large-n descent (EVIDENCE only)")
    for sid, T in [("mb_s3_9", mk_classes(3, 9, {8: 1})[0]),
                   ("mb_t729", mk_classes(3, 729, {r: (-r) % 729 for r in (182, 380, 395, 425, 668, 719, 728)})[0]),
                   ("mb_d23_8", mk_div23(8, {7: 1})[0]), ("mb_pair_3_9m", pair_T(3, 2, -1)[0])]:
        for _ in range(200):
            n = random.getrandbits(400) + 1
            x, k = n, 0
            while x >= 3:
                x = T(x); k += 1
                assert k < 10**6
        print("  ", sid, "200 random 400-bit starts reach < 3")


if __name__ == "__main__":
    part_A(); part_B(); part_C(); part_D(); part_E(); part_F()
    if FAIL:
        print(len(FAIL), "FAILURES"); sys.exit(1)
    print("REFEREE CHECK: ALL OK")
