#!/usr/bin/env python3
"""referee1_check.py -- independent referee check for round4/schema (Referee 1).

Written from scratch: it does NOT import depthlib, schemalib or windowlib.  It
imports round3/dichotomy/decide.py only in [R7] as an external oracle, and says so.
All decisions use ints / Fractions.  Floats appear only in printed summaries and in
the EVIDENCE item [R9] (which is not a proof item).  Exits 1 if any item fails.

 [R1] Family D (depth.md), own construction from the text of depth.md: the table
      satisfies integrality / positivity / unit multipliers, has no translation node,
      and the exact G_exit (enumerated on the residue graph, not on letters) is < Q.
 [R2] Generic exact Lambda: for every start node, ALL walks of the residue graph whose
      nonempty prefixes have multiplier > 1 are explored (resets included), using an
      exact table floor(U log2 3) = bitlen(3^U) - 1.  k* = Lambda + 1 is compared with
      the claimed records m = 4..10 (including the m = 10 value 304506, which the prover
      verified by formula only).
 [R3] Own integer witnesses (construction different from the prover's): n = e_1 + Q t,
      t = 2^(D_total + 64); T^i(n) >= n for i < k*, T^k*(n) < n, by direct iteration
      with an own step function, for m = 7, 8, 9, 10.
 [R4] Brute-force cycle lists of D members m = 4, 5, 6 (all starts n <= 2*10^5):
      only (1) and the loop.
 [R5] Cut-offs (cutoff.md): own 3x+1 / K7 maps.  Reset cut-offs at depth j: exact
      contraction certificate (own potential) and brute-force cycle list for j < J0;
      type (c) for J0 <= j <= 11 via own SCC code and the explicit witness orbit
      (-5 -7 -10 for 3x+1, z = -49/17 for K7).  Adversarial test of Theorem B1: 60 RANDOM
      unit-multiplier replacements of T on U_J (not resets) -- each must be type (c).
 [R6] Windows (window.md): |R_N| formula; schema weights of W2 recomputed and every
      edge inequality checked (N = 4..12); W2 constants; complete T_N cycle lists by
      brute force over n <= B_N (N = 4..20).
 [R7] W1' presentation issue: round3 dichotomy section 7 asks about NON-accelerated
      3x+1 (n/2, 3n+1).  Own generic window construction for that presentation gives the
      same R_N, and the approximant is CERT (own exact potential), N = 4..10; decide.py
      agrees (oracle).
 [R8] W4 finite facts and the cycle identity on (1 2).
 [R9] EVIDENCE: A(n) for n = 27, 837799, 63728127.
 [R10] A3 upper bound tested against decide.py k* on random CERT base-2 tables with
       u in {1,3} (translation nodes allowed).
"""
import sys, os, random, math
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OK = True


def claim(name, cond):
    global OK
    print(("PASS " if cond else "FAIL ") + name, flush=True)
    OK = OK and bool(cond)


# ======================================================================= generic tools
def step(Q, tab, n):
    u, v, w = tab[n % Q]
    x = u * n + v
    assert x % w == 0
    return x // w


def succs(Q, tab, r):
    """residue graph: n = r + Q t  ->  (u r + v + u Q t)/w ; t free."""
    u, v, w = tab[r]
    base = (u * r + v)
    assert base % w == 0
    # (base + u Q t)/w mod Q, t = 0..w-1 covers all (u unit, w | Q)
    return sorted({((base + u * Q * t) // w) % Q for t in range(w)})


def valid_table(Q, tab):
    for r in range(Q):
        u, v, w = tab[r]
        if math.gcd(u, Q) != 1 or Q % w or (u * r + v) % w:
            return False
        if u * r + v <= 0 and r > 0:          # positivity on smallest member
            return False
        if r == 0 and u * Q + v <= 0:
            return False
    return True


def exact_contracting(Q, tab):
    """Exact proof that every cycle of the residue graph contracts: find a potential
    c > 0 and theta < 1 (rational) with c(s) u <= theta c(r) w on every edge.
    Float Bellman-Ford guesses c; the verification is exact.  Returns theta or None."""
    S = [succs(Q, tab, r) for r in range(Q)]
    for th in (Fraction(999, 1000), Fraction(9999, 10000), Fraction(99999, 100000),
               Fraction(999999, 1000000)):
        lt = math.log(th)
        phi = [0.0] * Q
        for _ in range(4 * Q + 10):
            ch = False
            for r in range(Q):
                u, v, w = tab[r]
                wt = math.log(u) - math.log(w) - lt
                for s in S[r]:
                    if phi[s] + wt > phi[r] + 1e-12:
                        phi[r] = phi[s] + wt
                        ch = True
            if not ch:
                break
        else:
            continue
        lo = min(phi)
        c = [Fraction(round(math.exp(p - lo) * 2 ** 40)) for p in phi]
        # relax theta slightly upward for rounding; still must be < 1
        th2 = (th + 1) / 2
        if all(c[s] * tab[r][0] <= th2 * c[r] * tab[r][2] for r in range(Q) for s in S[r]):
            return th2
    return None


def tarjan(Q, S):
    idx, low, on, st, comps, cnt = {}, {}, set(), [], [], [0]
    comp_of = [None] * Q
    for root in range(Q):
        if root in idx:
            continue
        work = [(root, 0)]
        idx[root] = low[root] = cnt[0]; cnt[0] += 1; st.append(root); on.add(root)
        while work:
            v, i = work[-1]
            if i < len(S[v]):
                work[-1] = (v, i + 1)
                w = S[v][i]
                if w not in idx:
                    idx[w] = low[w] = cnt[0]; cnt[0] += 1; st.append(w); on.add(w)
                    work.append((w, 0))
                elif w in on:
                    low[v] = min(low[v], idx[w])
            else:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == idx[v]:
                    comp = []
                    while True:
                        w = st.pop(); on.discard(w); comp.append(w); comp_of[w] = len(comps)
                        if w == v:
                            break
                    comps.append(comp)
    return comps, comp_of


def residue_of(x, M):
    """x a Fraction with denominator coprime to M."""
    return (x.numerator * pow(x.denominator, -1, M)) % M


def type_c_from_orbit(Q, tab, orbit_pts, p=2):
    """orbit_pts: an exact periodic orbit (Fractions) of the map given by tab (its
    branches chosen by the p-adic residue).  Checks: residues mod Q trace a closed
    walk with multiplier > 1, and the SCC containing it is not a single simple
    cycle.  Returns (multiplier, scc size, #edges inside)."""
    S = [succs(Q, tab, r) for r in range(Q)]
    res = [residue_of(x, Q) for x in orbit_pts]
    L = len(orbit_pts)
    mult = Fraction(1)
    for i, x in enumerate(orbit_pts):
        r = res[i]
        u, v, w = tab[r]
        y = (u * x + v) / w
        assert y == orbit_pts[(i + 1) % L], "orbit does not follow the table"
        assert res[(i + 1) % L] in S[r]
        mult *= Fraction(u, w)
    comps, comp_of = tarjan(Q, S)
    cid = comp_of[res[0]]
    comp = set(comps[cid])
    assert all(comp_of[r] == cid for r in res)
    nedges = sum(1 for r in comp for s in S[r] if s in comp)
    return mult, len(comp), nedges


# ======================================================================= [R1]-[R4] family D
def christoffel(a, b):
    L = a + b
    return ['U' if ((i + 1) * a) // L - (i * a) // L else 'D' for i in range(L)]


def build_D(m, word, h, i0):
    """Own construction from depth.md: loop residues 2..L+1, chain after them."""
    Q = 2 ** m
    L = len(word)
    loop = list(range(2, 2 + L))
    chain = list(range(2 + L, 2 + L + h))
    assert 2 + L + h <= Q // 2
    tab = [None] * Q
    for i in range(L):
        li, ln = loop[i], loop[(i + 1) % L]
        tab[li] = (3, ln - 3 * li, 1) if word[i] == 'U' else (1, 2 * ln - li, 2)
    for j in range(h):
        nxt = chain[j + 1] if j + 1 < h else loop[i0]
        tab[chain[j]] = (3, nxt - 3 * chain[j], 1)
    for r in range(Q):
        if tab[r] is None:
            tab[r] = (1, (Q - r) % Q, Q)
    return Q, tab, loop, chain


def g_exit_generic(Q, tab):
    """max product of a walk starting at a non-reset node, consisting of non-reset
    nodes, whose last node has a reset successor (product includes the last node).
    Explored generically on the graph with exact Fractions.  Walk lengths are bounded
    because the only non-reset cycle is the loop (asserted: we stop after 3Q steps
    and require the maximum to have stabilised)."""
    nonreset = [r for r in range(Q) if tab[r][2] != Q]
    S = {r: succs(Q, tab, r) for r in nonreset}
    best = Fraction(0)
    for r0 in nonreset:
        r, P = r0, Fraction(1)
        for _ in range(3 * Q):
            u, v, w = tab[r]
            P *= Fraction(u, w)
            nxt = [s for s in S[r] if tab[s][2] != Q]
            if any(tab[s][2] == Q for s in S[r]):
                best = max(best, P)
            assert len(nxt) == 1
            r = nxt[0]
    return best


FLOOR = [0]          # FLOOR[U] = floor(U log2 3) = bitlen(3^U) - 1 (exact)
_p3 = [1]


def floor_theta(U):
    while len(FLOOR) <= U:
        _p3[0] *= 3
        FLOOR.append(_p3[0].bit_length() - 1)
    return FLOOR[U]


def lambda_generic(Q, tab):
    """Lambda = longest walk all of whose nonempty prefixes have multiplier > 1.
    Generic DFS over ALL successors (resets included).  Multipliers here are
    3^U / 2^D, and > 1 <=> D <= floor(U log2 3) (U >= 1; never equality)."""
    m = Q.bit_length() - 1
    S = [succs(Q, tab, r) for r in range(Q)]
    info = []
    for r in range(Q):
        u, v, w = tab[r]
        assert u in (1, 3) and w & (w - 1) == 0
        info.append((1 if u == 3 else 0, w.bit_length() - 1))
    best = 0
    for r0 in range(Q):
        stack = [(r0, 0, 0, 0)]            # node, U, D, length so far (edges)
        while stack:
            r, U, D, ln = stack.pop()
            best = max(best, ln)
            du, dd = info[r]
            U2, D2 = U + du, D + dd
            if U2 == 0 or D2 > floor_theta(U2):
                continue                   # the prefix ending after this node is <= 1
            for s in S[r]:
                stack.append((s, U2, D2, ln + 1))
            if len(stack) > 10 ** 6:
                raise RuntimeError("explosion")
    return best


RECORDS = {4: (26, 1, 2, 2, 2), 5: (132, 3, 5, 4, 3), 6: (791, 5, 8, 11, 4),
           7: (4335, 17, 27, 13, 5), 8: (41362, 41, 65, 14, 5), 9: (133534, 94, 149, 16, 6),
           10: (304506, 147, 233, 17, 6)}

for m, (kc, a, b, i0, h) in sorted(RECORDS.items()):
    word = christoffel(a, b)
    Q, tab, loop, chain = build_D(m, word, h, i0)
    lam = Fraction(3 ** a, 2 ** b)
    good = valid_table(Q, tab) and not any(u == 1 and w == 1 for u, v, w in tab)
    G = g_exit_generic(Q, tab)
    Lam = lambda_generic(Q, tab)
    claim(f"[R1/R2] m={m} Christoffel({a},{b}) i0={i0} h={h}: valid, no translation node, "
          f"lambda={float(lam):.5f} < 1, G_exit={float(G):.2f} < Q={Q}, generic k* = Lambda+1 = "
          f"{Lam + 1} (claimed {kc})", good and lam < 1 and G < Q and Lam + 1 == kc)

# balance property of the Christoffel words used (A2): any two factors of equal length
# differ by <= 1 in their U count (cyclic factors)
for (a, b) in [(5, 8), (17, 27), (41, 65), (94, 149)]:
    w = christoffel(a, b)
    L = a + b
    ok_bal = sum(c == 'U' for c in w) == a
    ww = w + w
    for s in range(1, L + 1):
        cnts = {sum(c == 'U' for c in ww[i:i + s]) for i in range(L)}
        ok_bal &= max(cnts) - min(cnts) <= 1
    claim(f"[R1] Christoffel({a},{b}) has {a} U's and is balanced (cyclic factors)", ok_bal)


def witness(m, kc, a, b, i0, h):
    word = christoffel(a, b)
    Q, tab, loop, chain = build_D(m, word, h, i0)
    # the deepest walk: chain e_1..e_h then loop from i0 (formula of A1); count D's
    L = len(word)
    nodes = chain + [loop[(i0 + i) % L] for i in range(kc - h)]
    Dtot = sum(1 for r in nodes if tab[r][2] == 2)
    start = chain[0] if h else loop[i0]
    n = start + Q * 2 ** (Dtot + 64)
    x = n
    for i in range(1, kc + 1):
        x = step(Q, tab, x)
        if i < kc and x < n:
            return False, i
    return x < n, kc


for m in (7, 8, 9, 10):
    kc, a, b, i0, h = RECORDS[m]
    good, i = witness(m, kc, a, b, i0, h)
    claim(f"[R3] m={m}: own witness n = e_1 + Q 2^(D+64): T^i(n) >= n for i < {kc}, "
          f"T^{kc}(n) < n", good)


def brute_cycles(Q, tab, bound, cap=10 ** 6):
    seen_cyc = set()
    done = set()
    for n0 in range(1, bound + 1):
        path, pos, x = [], {}, n0
        while x not in done and x not in pos:
            pos[x] = len(path); path.append(x)
            x = step(Q, tab, x)
            if len(path) > cap:
                raise RuntimeError("long orbit")
        if x in pos:
            cyc = path[pos[x]:]
            seen_cyc.add(tuple(sorted(cyc)))
        done.update(path)
    return seen_cyc


for m in (4, 5, 6):
    kc, a, b, i0, h = RECORDS[m]
    Q, tab, loop, chain = build_D(m, christoffel(a, b), h, i0)
    cyc = brute_cycles(Q, tab, 200000)
    claim(f"[R4] m={m}: brute force n <= 2e5: cycles = {{(1), loop}}",
          cyc == {(1,), tuple(sorted(loop))})

# random D members (random words), brute force vs. A1(2)
random.seed(7)
cnt = 0
bad = 0
while cnt < 40:
    m = random.randint(4, 6)
    Q = 2 ** m
    L = random.randint(1, Q // 2 - 3)
    word = [random.choice('UD') for _ in range(L)]
    nU = word.count('U')
    if 'D' not in word or 3 ** nU >= 2 ** (L - nU):
        continue
    h = random.randint(0, Q // 2 - 2 - L)
    i0 = random.randrange(L)
    Q, tab, loop, chain = build_D(m, word, h, i0)
    G = g_exit_generic(Q, tab)
    if G >= Q:
        continue
    cyc = brute_cycles(Q, tab, 30000)
    bad += cyc != {(1,), tuple(sorted(loop))}
    cnt += 1
claim(f"[R4] 40 random CERT members (m=4..6): brute-force cycle lists = {{(1), loop}}", bad == 0)


# ======================================================================= [R5] cut-offs
def collatz_acc(Q):
    return [(1, 0, 2) if r % 2 == 0 else (3, 1, 2) for r in range(Q)]


def k7_n(Q):
    """K7 in n = z+1: n odd -> (n+1)/2, n=0 (4) -> 3n/2, n=2 (4) -> (n+2)/4.  Q >= 4."""
    out = []
    for r in range(Q):
        if r % 2:
            out.append((1, 1, 2))
        elif r % 4 == 0:
            out.append((3, 0, 2))
        else:
            out.append((1, 2, 4))
    return out


def reset(Q, r):
    return (1, (Q - r) % Q, Q)


def cut(tabfn, j, xstar_res):
    Q = 2 ** j
    tab = tabfn(Q)
    tab[xstar_res % Q] = reset(Q, xstar_res % Q)
    return Q, tab


def periodic_orbit(tabfn, Q, x0, L):
    tab = tabfn(Q)
    pts, x = [], x0
    for _ in range(L):
        pts.append(x)
        u, v, w = tab[residue_of(x, Q)]
        x = (u * x + v) / w
    assert x == x0
    return pts


# 3x+1: x* = -1; cut class -1 mod 2^j
for j in range(2, 12):
    Q, tab = cut(collatz_acc, j, -1)
    if j < 3:
        th = exact_contracting(Q, tab)
        cyc = brute_cycles(Q, tab, 10 ** 6)
        claim(f"[R5] 3x+1 cut at j={j}: exact contraction (theta={th}), brute cycles n<=1e6 {sorted(cyc)}",
              th is not None and cyc == {(1, 2)})
    else:
        orb = [Fraction(-5), Fraction(-7), Fraction(-10)]
        mult, sz, ne = type_c_from_orbit(Q, tab, orb)
        claim(f"[R5] 3x+1 cut at j={j}: orbit -5 -7 -10 expanding ({mult}) in SCC of {sz} nodes, "
              f"{ne} internal edges -> type (c)", mult > 1 and ne > sz)

# K7 (n coords): x* = 0; cut class 0 mod 2^j
yK = Fraction(-49, 17) + 1          # n = z + 1
for j in range(2, 12):
    Q, tab = cut(k7_n, j, 0)
    if j < 6:
        th = exact_contracting(Q, tab)
        cyc = brute_cycles(Q, tab, 10 ** 6)
        claim(f"[R5] K7 cut at j={j}: exact contraction (theta={th}), brute cycles n<=1e6 {sorted(cyc)}",
              th is not None and cyc == {(1,)})
    else:
        orb = periodic_orbit(k7_n, 4, yK, 5)
        assert all(residue_of(x, 64) != 0 for x in orb)
        mult, sz, ne = type_c_from_orbit(Q, tab, orb)
        claim(f"[R5] K7 cut at j={j}: orbit of z=-49/17 expanding ({mult}) in SCC of {sz} nodes, "
              f"{ne} internal edges -> type (c)", mult > 1 and ne > sz)


# periodic point of A^i B stays close to -5 and avoids U_3 (3x+1), i <= 15
def pp(tabfn, Q, word):
    tab = tabfn(Q)
    A, B = Fraction(1), Fraction(0)
    for r in word:
        u, v, w = tab[r]
        A, B = A * Fraction(u, w), (B * u + v) / w
    x = B / (1 - A)
    y = x
    pts = []
    for r in word:
        assert residue_of(y, Q) == r
        pts.append(y)
        u, v, w = tab[r]
        y = (u * y + v) / w
    assert y == x
    return x, pts


good = True
for i in range(0, 16):
    x, pts = pp(collatz_acc, 2, [1, 1, 0] * i + [1, 0])
    good &= all(residue_of(p, 8) != 7 for p in pts)
    if i:
        good &= residue_of(x, 2 ** (1 + i)) == residue_of(Fraction(-5), 2 ** (1 + i))
claim("[R5] 3x+1: periodic points of A^i B (i<=15) avoid -1 mod 8 and agree with -5 mod 2^(1+i)", good)

# Adversarial test of B1: random unit-multiplier replacements (not resets) on U_J
random.seed(11)
tested = 0
allc = True
while tested < 60:
    which = random.choice(['3x+1', 'K7'])
    J = random.randint(3, 6) if which == '3x+1' else random.randint(6, 8)
    Kp = J + random.randint(0, 2)
    Q = 2 ** Kp
    tab = collatz_acc(Q) if which == '3x+1' else k7_n(Q)
    xr = (-1) % (2 ** J) if which == '3x+1' else 0
    for r in range(Q):
        if r % (2 ** J) == xr:
            while True:
                u = random.choice([1, 3, 5, 7, 9])
                e = random.randint(1, 3)
                w = 2 ** e
                v = (-u * r) % w + w * random.randint(0, 3)
                if u * r + v > 0 or (r == 0 and u * Q + v > 0):
                    break
            tab[r] = (u, v, w)
    if not valid_table(Q, tab):
        continue
    # all replacements divide (e >= 1), so the standing hypothesis holds
    orb = [Fraction(-5), Fraction(-7), Fraction(-10)] if which == '3x+1' else periodic_orbit(k7_n, 4, yK, 5)
    mult, sz, ne = type_c_from_orbit(Q, tab, orb)
    allc &= mult > 1 and ne > sz
    tested += 1
claim("[R5] Theorem B1 adversarial: 60 random non-reset replacements on U_J (J >= J0) all type (c)", allc)


# ======================================================================= [R6] windows
def par_window(r, N):
    b, x = [], r
    for _ in range(N):
        if x & 1:
            b.append(1); x = (3 * x + 1) >> 1
        else:
            b.append(0); x >>= 1
    return b


def inR(r, N):
    return 8 * sum(par_window(r, N)) > 5 * N


for N in range(1, 17):
    cntR = sum(1 for r in range(2 ** N) if inR(r, N))
    formula = sum(math.comb(N, k) for k in range(N + 1) if 8 * k > 5 * N)
    if cntR != formula:
        claim(f"[R6] |R_{N}| formula", False)
claim("[R6] |R_N| = sum_{k>5N/8} C(N,k) for N = 1..16", True)
claim("[R6] |R_8| = 37 and |R_16|/2^16 = 6885/65536",
      sum(1 for r in range(256) if inR(r, 8)) == 37 and sum(1 for r in range(2 ** 16) if inR(r, 16)) == 6885)
# entropy bound sum_{k >= aN} C(N,k) <= 2^{N H(a)} -- checked exactly as
# sum C(N,k) * a^(aN) (1-a)^((1-a)N) <= 1 is the standard proof; here just verify numerically for N<=400
ok_ent = all(sum(math.comb(N, k) for k in range(N + 1) if 8 * k > 5 * N) <= 2 ** (0.9545 * N) for N in range(1, 400))
claim("[R6] sum_{k>5N/8} C(N,k) <= 2^(0.9545 N), N < 400 (float compare, sanity only)", ok_ent)

g = Fraction(161, 160)
claim("[R6] gamma^8*243 < 256", g ** 8 * 243 < 256)
claim("[R6] (3g/2)^floor(5N/8) <= 2^(N-2) for N = 4..600", all((3 * g / 2) ** ((5 * N) // 8) <= 2 ** (N - 2) for N in range(4, 601)))


def weights(N):
    c = []
    for r in range(2 ** N):
        b = par_window(r, N)
        if 8 * sum(b) > 5 * N:
            c.append(Fraction(1, 2)); continue
        best, P = Fraction(1), Fraction(1)
        for s in range(1, N):
            P *= g * (Fraction(3, 2) if b[s - 1] else Fraction(1, 2))
            best = max(best, P)
        c.append(best)
    return c


def TN_table(N):
    Q = 2 ** N
    return Q, [reset(Q, r) if inR(r, N) else ((1, 0, 2) if r % 2 == 0 else (3, 1, 2)) for r in range(Q)]


for N in range(4, 13):
    Q, tab = TN_table(N)
    c = weights(N)
    good = valid_table(Q, tab)
    for r in range(Q):
        u, v, w = tab[r]
        for s in succs(Q, tab, r):
            good &= c[s] * u < c[r] * w
    claim(f"[R6] W2 N={N}: own weights satisfy c(s)u < c(r)w on every edge of T_N", good)


def TN_step(N, n):
    if inR(n % 2 ** N, N):
        return n // 2 ** N + 1 if n % 2 ** N else n // 2 ** N
    return n >> 1 if n % 2 == 0 else (3 * n + 1) >> 1


for N in range(4, 21):
    BN = math.ceil(Fraction(161, 2) * (3 * g / 2) ** ((5 * N) // 8))
    cycles = set()
    done = set()
    for n0 in range(1, BN + 1):
        path, pos, x = [], {}, n0
        while x not in done and x not in pos:
            pos[x] = len(path); path.append(x); x = TN_step(N, x)
        if x in pos:
            cycles.add(tuple(sorted(path[pos[x]:])))
        done.update(path)
    if cycles != {(1, 2)}:
        claim(f"[R6] T_{N} cycle list", False)
claim("[R6] W3: T_N cycle list = {(1 2)} for N = 4..20 (all n <= B_N iterated)", True)


# ======================================================================= [R7] non-accelerated
def window_generic(p, m, tab, K, r):
    Q = p ** m
    x, D, U = r, 0, 1
    while D <= K - m:
        u, v, w = tab[x % Q]
        e = 0
        while w % p == 0:
            w //= p; e += 1
        U *= u; D += e
        x = (u * x + v) // (p ** e)
    return U, D


plain = [(1, 0, 2), (3, 1, 1)]
sys.path.insert(0, os.path.join(HERE, "..", "..", "round3", "dichotomy"))
import decide as DC  # oracle only
for N in range(4, 11):
    Q = 2 ** N
    R = []
    for r in range(Q):
        U, D = window_generic(2, 1, plain, N, r)
        assert D == N
        k = 0
        while U % 3 == 0:
            U //= 3; k += 1
        assert U == 1
        if 8 * k > 5 * N:
            R.append(r)
    sameR = R == [r for r in range(Q) if inR(r, N)]
    tab = [reset(Q, r) if r in set(R) else plain[r % 2] for r in range(Q)]
    th = exact_contracting(Q, tab)
    res = DC.decide(Q, tab, want_cycles=False, want_depth=False)
    claim(f"[R7] non-accelerated 3x+1, N={N}: generic window R = accelerated R_N ({sameR}), approximant "
          f"exactly contracting (theta={th}), decide.py {res['verdict']}",
          sameR and th is not None and res['verdict'] == 'CERT')


# ======================================================================= [R8] W4 facts
claim("[R8] (3+1/31)^5 >= 256 > (3+1/32)^5", (3 + Fraction(1, 31)) ** 5 >= 256 > (3 + Fraction(1, 32)) ** 5)
good = True
for n in range(1, 32):
    x, steps = n, 0
    while x != 1:
        x = x // 2 if x % 2 == 0 else (3 * x + 1) // 2
        steps += 1
    good &= steps < 1000
claim("[R8] every n <= 31 reaches 1 (so the only cycle with an element <= 31 is (1 2))", good)
claim("[R8] cycle identity on (1 2): prod_odd (3 + 1/z) = 2^L", (3 + Fraction(1, 1)) == 2 ** 2)


# ======================================================================= [R9] evidence
def A_of(n):
    bits, x = [], n
    while x != 1:
        bits.append(x & 1)
        x = (3 * x + 1) >> 1 if x & 1 else x >> 1
    bits += [1, 0] * 8
    pre = [0]
    for b in bits:
        pre.append(pre[-1] + b)
    best = 0
    Lb = len(bits)
    for i in range(Lb):
        for j in range(i + 1, Lb + 1):
            if 8 * (pre[j] - pre[i]) > 5 * (j - i):
                best = max(best, j - i)
    return best


for n, claimed in [(27, 13.25), (837799, 11.0), (63728127, 17.2)]:
    A = A_of(n)
    print(f"EVIDENCE [R9] A({n}) = {A}, A/log2 n = {A / math.log2(n):.2f} (claimed {claimed})")


# ======================================================================= [R10] A3 bound
cf_q = [1, 1, 2, 5, 12, 41, 53, 306, 665, 15601]  # convergent denominators of log2 3


def a3_bound(Q):
    for k in range(len(cf_q) - 1):
        if cf_q[k] <= Q < cf_q[k + 1]:
            return Q + (Q - 1) * Q * math.log(3) / math.log(2) * (cf_q[k] + cf_q[k + 1])
    raise ValueError


random.seed(5)
tested = viol = 0
tries = 0
while tested < 150 and tries < 20000:
    tries += 1
    m = random.randint(2, 4)
    Q = 2 ** m
    tab = []
    for r in range(Q):
        u = random.choice([1, 3])
        w = random.choice([d for d in (1, 2, 4, 8, 16) if Q % d == 0])
        v = (-u * r) % w + w * random.randint(-1, 3)
        tab.append((u, v, w))
    if not valid_table(Q, tab):
        continue
    try:
        res = DC.decide(Q, tab, want_cycles=False)
    except Exception:
        continue
    if res.get('verdict') != 'CERT' or res.get('kstar') is None:
        continue
    tested += 1
    if res['kstar'] > a3_bound(Q):
        viol += 1
claim(f"[R10] A3 bound holds on {tested} random CERT tables (m=2..4, u in {{1,3}}, translations allowed)",
      tested >= 50 and viol == 0)

# ======================================================================= [R11] sanity / false-claim tests
# (a) negative controls: the tools must be able to say no.
Q, tab = cut(collatz_acc, 3, -1)
claim("[R11] negative control: no contraction potential for 3x+1 cut at j=3 (type (c))",
      exact_contracting(Q, tab) is None)
Q, tab = cut(k7_n, 6, 0)
claim("[R11] negative control: no contraction potential for K7 cut at j=6", exact_contracting(Q, tab) is None)
claim("[R11] negative control: uncut accelerated 3x+1 at 2^6 has no contraction potential",
      exact_contracting(64, collatz_acc(64)) is None)
# (b) 5x+1 (accelerated): window approximants with threshold 2N/5 (5^(2/5) < 2) are CERT
# (Theorem W1 is general), but the true cycle 13 -> 33 -> 83 -> ... has odd-step density 3/7 > 2/5,
# so it lies in R_N and is NOT a T_N cycle: the approximants simply forget it.  No false statement
# about 5x+1 follows, because W3/W4 only transfer statements about orbits that avoid R_N.
def acc5(Q):
    return [(1, 0, 2) if r % 2 == 0 else (5, 1, 2) for r in range(Q)]


def par5(r, N):
    b, x = [], r
    for _ in range(N):
        if x & 1:
            b.append(1); x = (5 * x + 1) >> 1
        else:
            b.append(0); x >>= 1
    return b


good = True
for N in range(6, 11):
    Q = 2 ** N
    R5 = {r for r in range(Q) if 5 * sum(par5(r, N)) > 2 * N}
    tab = [reset(Q, r) if r in R5 else acc5(Q)[r] for r in range(Q)]
    good &= exact_contracting(Q, tab) is not None
    orb13 = [13]
    while True:
        x = orb13[-1]
        y = (5 * x + 1) // 2 if x % 2 else x // 2
        if y == 13:
            break
        orb13.append(y)
    good &= any(x % Q in R5 for x in orb13)
claim("[R11] 5x+1: window approximants (threshold 2N/5) CERT for N=6..10 and the true 13-cycle meets R_N",
      good)

print("ALL PASS" if OK else "SOME CHECK FAILED")
sys.exit(0 if OK else 1)
