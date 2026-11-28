"""Referee 2: independent check of census/round4/transport.

Written from scratch by the second referee.  Exact int / Fraction arithmetic only.  It does not
import transport_lib, equiv, check_transport, referee1_check or decide.  It reads library.py and
the results/*.json files only as DATA (tables and recorded joins); the tables that the main
theorems are about (3x+1, G, G', the S-family, dch_C27_2466) are rebuilt here from their rules.

Exits 1 on any failure.  Every test can fail; negative controls are included.

  python3 referee2_check.py          (about 1 minute)
"""
import json
import os
import sys
import time
from fractions import Fraction
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
FAILS = []


def check(cond, msg):
    if not cond:
        FAILS.append(msg)
        print("  FAIL:", msg)
    return cond


def lcm(a, b):
    return a // gcd(a, b) * b


# =============================================================== tables
def s_fam(m, S):
    S = set(S)
    return 2 ** m, [(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r in S else (1, 1, 1))
                    for r in range(2 ** m)]


COLLATZ = (2, [(1, 0, 2), (3, 1, 1)])
# G(z) of Prop C, derived by hand by this referee (see REFEREE2.md)
G_HAND = (4, [(3, 0, 4), (3, 1, 2), (1, -2, 4), (3, 1, 2)])
GP_HAND = (4, [(3, 0, 2), (3, 1, 4), (3, 0, 2), (1, 1, 4)])


def c27_2466():
    """From the rule text of round3/dichotomy/dch_C27_2466.md."""
    rule = {}
    for r in (1, 10, 14, 19, 23, 26):
        rule[r] = (1, 1)
    rule[16] = (1, 2)
    for r in (5, 20):
        rule[r] = (2, 1)
    for r in (2, 7, 8, 13):
        rule[r] = (2, -1)
    rule[25] = (4, 1)
    rule[11] = (4, -1)
    for r in (4, 22):
        rule[r] = (5, 1)
    rule[17] = (5, -1)
    t = []
    for r in range(27):
        if r % 3 == 0:
            t.append((1, 0, 3))
        else:
            a, b = rule[r]
            t.append((a, b, 1))
    return 27, t


def step(Q, t, n):
    u, v, w = t[n % Q]
    x = u * n + v
    assert x % w == 0, (n, t[n % Q])
    return x // w


def norm(u, v, w):
    g = gcd(gcd(u, v), w)
    u, v, w = u // g, v // g, w // g
    if w < 0:
        u, v, w = -u, -v, -w
    return (u, v, w)


# =============================================================== own first-return engine
def first_return(Q, t, MX, rX, tmax=24, pmax=20000):
    """Symbolic first return of T to X = rX (mod MX) in z-coordinates n = MX z + rX.
    State: z = L k + c (k >= 0 free integer), current value = al k + be (integers).
    Returns list of (L, c, A, B, D, time) meaning G(z) = (A z + B)/D on z = c (mod L), or None."""
    out = []
    stack = [(1, 0, MX, rX, 0)]
    while stack:
        if len(stack) + len(out) > pmax:
            return None
        L, c, al, be, tt = stack.pop()
        if tt >= 1:
            need = MX // gcd(MX, al)
            if need > 1:
                for i in range(need):
                    stack.append((L * need, c + L * i, al * need, be + al * i, tt))
                continue
            if (be - rX) % MX == 0:
                # G(z) = (al (z - c)/L + be - rX)/MX
                A, B, D = norm(al, -al * c + L * (be - rX), L * MX)
                out.append((L, c, A, B, D, tt))
                continue
        if tt >= tmax:
            return None
        need = Q // gcd(Q, al)
        if need > 1:
            for i in range(need):
                stack.append((L * need, c + L * i, al * need, be + al * i, tt))
            continue
        u, v, w = t[be % Q]
        if (u * al) % w or (u * be + v) % w:
            raise ValueError("table not exact on class")
        stack.append((L, c, (u * al) // w, (u * be + v) // w, tt + 1))
    return out


def canon_pieces(pieces, Lmax=1 << 16):
    L = 1
    for p in pieces:
        L = lcm(L, p[0])
        if L > Lmax:
            return None
    full = [None] * L
    for (M, c, A, B, D, _) in pieces:
        for r in range(c % M, L, M):
            if full[r] is not None:
                raise ValueError("overlap")
            full[r] = (A, B, D)
    if any(f is None for f in full):
        raise ValueError("gap")
    for q in range(1, L + 1):
        if L % q == 0 and all(full[r] == full[r % q] for r in range(L)):
            return (q, tuple(full[:q]))


def canon_table(Q, t):
    pcs = [(Q, r) + norm(*t[r]) + (1,) for r in range(Q)]
    return canon_pieces(pcs)


def induced(Q, t, MX, rX, tmax=24, pmax=20000, Lmax=1 << 16):
    if MX == 1:
        return canon_table(Q, t), 1
    pcs = first_return(Q, t, MX, rX, tmax, pmax)
    if pcs is None:
        return None, None
    return canon_pieces(pcs, Lmax), max(p[5] for p in pcs)


# =============================================================== Karp, exact
def max_mean_sign(nodes, edges, mult):
    """Sign of the maximum cycle mean of log(mult) in a strongly connected node set (Karp,
    multiplicatively, exact).  edges[x] = successors inside; mult[x] = Fraction for every edge
    out of x.  Returns +1, 0, -1 (or None if no cycle)."""
    nodes = list(nodes)
    N = len(nodes)
    s = nodes[0]
    Dk = [dict() for _ in range(N + 1)]
    Dk[0][s] = Fraction(1)
    for k in range(1, N + 1):
        cur = Dk[k]
        for x, val in Dk[k - 1].items():
            nv = val * mult[x]
            for y in edges[x]:
                if y not in cur or nv > cur[y]:
                    cur[y] = nv
    best = None
    for v in nodes:
        if v not in Dk[N]:
            continue
        # min over k of sign(D_N/D_k - 1) as a mean comparison; we need the minimum of
        # (log D_N - log D_k)/(N-k); its sign is the min of the signs only if we compare
        # actual values, so compare exactly via cross powers.
        vals = []
        for k in range(N):
            if v in Dk[k]:
                vals.append((Dk[N][v] / Dk[k][v], N - k))
        # min_k r_k^(1/e_k): compare r^(1/e) values exactly by r1^e2 vs r2^e1
        mn = vals[0]
        for (r, e) in vals[1:]:
            if r ** mn[1] < mn[0] ** e:
                mn = (r, e)
        if best is None or mn[0] ** best[1] > best[0] ** mn[1]:
            best = mn
    if best is None:
        return None
    r = best[0]
    return (r > 1) - (r < 1)


def sccs(nodes, succ):
    """Iterative Tarjan."""
    index, low, on, st, out = {}, {}, set(), [], []
    cnt = 0
    for v0 in nodes:
        if v0 in index:
            continue
        work = [(v0, iter(succ[v0]))]
        index[v0] = low[v0] = cnt
        cnt += 1
        st.append(v0)
        on.add(v0)
        while work:
            v, it = work[-1]
            adv = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = cnt
                    cnt += 1
                    st.append(w)
                    on.add(w)
                    work.append((w, iter(succ[w])))
                    adv = True
                    break
                elif w in on:
                    low[v] = min(low[v], index[w])
            if adv:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = st.pop()
                    on.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                out.append(comp)
    return out


# =============================================================== unit p-adic type (own)
def unit_prime(Q, t):
    if Q < 2:
        return None
    p = next(d for d in range(2, Q + 1) if Q % d == 0)
    x = Q
    while x % p == 0:
        x //= p
    if x != 1:
        return None
    for (u, v, w) in t:
        y = w
        while y % p == 0:
            y //= p
        if u < 1 or u % p == 0 or y != 1 or Q % w:
            return None
    return p


def cyl_graph(Q, t):
    succ = {}
    for r in range(Q):
        u, v, w = t[r]
        base = (u * r + v) // w
        step_ = Q // w
        succ[r] = sorted({(base + i * step_) % Q for i in range(w)})
    return succ


def type_of(Q, t):
    """Trichotomy type of a unit p-adic table at level Q: returns (type, info).
    'critical' if a division-free cycle exists; else 'c' if some non-simple SCC has max cycle
    mean > 0; 'b' if some simple-cycle SCC is expanding (and no (c)); else 'a'."""
    assert unit_prime(Q, t)
    succ = cyl_graph(Q, t)
    nd = [r for r in range(Q) if t[r][2] == 1]
    nds = set(nd)
    for comp in sccs(nd, {r: [s for s in succ[r] if s in nds] for r in nd}):
        cs = set(comp)
        if any(s in cs for r in comp for s in succ[r]):
            return 'critical', comp
    res = 'a'
    info = None
    for comp in sccs(list(range(Q)), succ):
        cs = set(comp)
        ed = {r: [s for s in succ[r] if s in cs] for r in comp}
        ne = sum(len(v) for v in ed.values())
        if ne == 0:
            continue
        mult = {r: Fraction(t[r][0], t[r][2]) for r in comp}
        sg = max_mean_sign(comp, ed, mult)
        if sg > 0:
            if ne > len(comp):
                return 'c', sorted(comp)
            res, info = 'b', sorted(comp)
    return res, info


# =============================================================== Lemma S (own)
def lemma_S(Q, t, MX, rX):
    """Lemma S of transport_theorems.md, implemented from the statement.  Returns (ok, info)."""
    M = lcm(Q, MX)
    for (u, v, w) in t:
        M = lcm(M, w)
    d = None
    for p in range(2, Q + 1):
        if Q % p == 0 and all(p % s for s in range(2, p)):
            if all(norm(*t[r]) == (1, 0, p) for r in range(0, Q, p)):
                d = p
                break
    G = {rX % MX}
    if d is not None:
        for c in range(MX):
            x = c
            for _ in range(MX + 1):
                if x == rX % MX:
                    G.add(c)
                    break
                x = x * d % MX
    succ = {}
    for x in range(M):
        u, v, w = t[x % Q]
        y = (u * x + v) // w
        g = gcd(u * M // w, M)
        succ[x] = sorted({(y + g * i) % M for i in range(M // g)})
    bad = [x for x in range(M) if x % MX not in G]
    bs = set(bad)
    sub = {x: [y for y in succ[x] if y in bs] for x in bad}
    contr = []
    for comp in sccs(bad, sub):
        cs = set(comp)
        ed = {x: [y for y in sub[x] if y in cs] for x in comp}
        if not any(ed.values()):
            continue
        if d is not None and all(norm(*t[x % Q]) == (1, 0, d) for x in comp):
            continue
        mult = {x: Fraction(t[x % Q][0], t[x % Q][2]) for x in comp}
        if max_mean_sign(comp, ed, mult) < 0:
            contr.append(sorted(comp))
            continue
        return False, sorted(comp)[:6]
    return True, dict(M=M, G=sorted(G), d=d, contracting=contr)


# =============================================================== parts
def part1_propC_thmF():
    print("[1] Prop C and Theorem F: identities with the own engine")
    c, tm = induced(*COLLATZ, 3, 2, tmax=10)
    check(c == canon_table(*G_HAND) and tm == 3, "Prop C identity / return time %s %s" % (c, tm))
    # brute force
    for z in range(0, 200000):
        n = 3 * z + 2
        y = step(*COLLATZ, n)
        k = 1
        while y % 3 != 2:
            y = step(*COLLATZ, y)
            k += 1
        if not check(k <= 3 and (y - 2) // 3 == step(*G_HAND, z), "Prop C brute z=%d" % z):
            break
    # G' = conjugate by y = z+1
    for y in range(1, 100000):
        if not check(step(*GP_HAND, y) == step(*G_HAND, y - 1) + 1, "G' conj y=%d" % y):
            break
    # Theorem F
    F4 = []
    for S0 in [(), (1,), (9,), (1, 9)]:
        S = (3, 7, 15) + S0
        F4.append(S)
        Q, t = s_fam(4, S)
        c, tm = induced(Q, t, 4, 3, tmax=10)
        check(c == canon_table(*G_HAND) and tm == 4, "Thm F identity S=%s" % (S,))
        for z in range(0, 100000):
            n = 4 * z + 3
            y = step(Q, t, n)
            while y % 4 != 3:
                y = step(Q, t, y)
            if not check((y - 3) // 4 == step(*G_HAND, z), "Thm F brute S=%s z=%d" % (S, z)):
                break
    # negative controls: every other 4-bit S with 3,7,15 in S but violating a hypothesis fails
    bad = 0
    for mask in range(256):
        S = tuple(2 * i + 1 for i in range(8) if mask >> i & 1)
        if tuple(sorted(S)) in [tuple(sorted(x)) for x in F4]:
            continue
        Q, t = s_fam(4, S)
        c, _ = induced(Q, t, 4, 3, tmax=24)
        if c == canon_table(*G_HAND):
            bad += 1
            check(False, "an S outside Theorem F also gives G: %s" % (S,))
    check(bad == 0, "Theorem F hypothesis is sharp among the 256 sets m=4")
    # perturbed G is rejected
    Gx = (4, [(3, 0, 4), (3, 1, 2), (1, 2, 4), (3, 1, 2)])
    check(induced(*COLLATZ, 3, 2)[0] != canon_table(*Gx), "control: perturbed G rejected")
    return F4


def part2_types(F4):
    print("[2] types (own cylinder graph, exact Karp) and Lemma S")
    ty, info = type_of(*GP_HAND)
    check(ty == 'c', "G' type %s" % ty)
    ty, info = type_of(*G_HAND)
    check(ty == 'c', "G type %s" % ty)
    # the two expanding loops quoted for G'
    succ = cyl_graph(*GP_HAND)
    check(0 in succ[0] and Fraction(3, 2) > 1, "G' self-loop 0->0 (3/2)")
    check(1 in succ[2] and 2 in succ[1] and Fraction(3, 2) * Fraction(3, 4) == Fraction(9, 8),
          "G' cycle 2->1->2 (9/8)")
    check(type_of(*COLLATZ)[0] == 'c', "3x+1 itself is type (c)")
    for S in F4:
        ty, info = type_of(*s_fam(4, S))
        check(ty == 'c', "T_S type %s %s" % (S, ty))
        ok, inf = lemma_S(*s_fam(4, S), 4, 3)
        exp = [[1, 2, 4]] if 1 in S else [[1, 2]]
        check(ok and inf['contracting'] == exp, "Lemma S T_S %s: %s" % (S, inf))
    ok, inf = lemma_S(*COLLATZ, 3, 2)
    check(ok and inf['G'] == [1, 2] and inf['contracting'] == [], "Lemma S (C, 2 mod 3) %s" % inf)
    # negative controls
    check(not lemma_S(*COLLATZ, 4, 1)[0], "control: Lemma S rejects (3x+1, 1 mod 4)")
    check(not lemma_S(*COLLATZ, 3, 0)[0], "control: Lemma S rejects (3x+1, 0 mod 3)")
    check(lemma_S(*COLLATZ, 4, 3)[0], "control: (3x+1, 3 mod 4) accepted (correct)")
    fivex = (2, [(1, 0, 2), (5, 1, 1)])
    check(not lemma_S(*fivex, 4, 3)[0], "control: Lemma S rejects (5x+1, 3 mod 4)")
    # an exact-1 cycle must not be called contracting: n -> n+2 on odd, n/2 on 0 mod 4 ...
    tneut = (4, [(1, 0, 2), (1, 4, 1), (1, 0, 2), (1, 4, 1)])   # odd n -> n+4: neutral loop 3 -> 3
    check(not lemma_S(*tneut, 4, 1)[0], "control: neutral cycle rejected")
    # Karp sign sanity
    check(max_mean_sign([0], {0: [0]}, {0: Fraction(1)}) == 0, "Karp neutral")
    check(max_mean_sign([0, 1], {0: [1], 1: [0, 1]}, {0: Fraction(3), 1: Fraction(1, 2)}) == 1,
          "Karp expanding 2-cycle 3/2")


def part3_B2_and_cycles(F4):
    print("[3] every 3x+1 cycle meets 2 mod 3 (residue facts, brute) and Theorem F cycle lists")
    for n in range(1, 300000):
        if n % 3 == 1:
            a = step(*COLLATZ, n)
            b = step(*COLLATZ, a)
            if not check(a % 3 == 2 or b % 3 == 2, "B2 n=%d" % n):
                break
        if n % 3 == 0 and n % 2 == 1:
            if not check(step(*COLLATZ, n) % 3 == 1, "B2 odd 0 mod 3 n=%d" % n):
                break
    N = 10 ** 6
    for S in F4:
        Q, t = s_fam(4, S)
        fate = {}
        cycles = set()
        avoid_end = set()
        for n0 in range(1, N + 1):
            if n0 in fate:
                continue
            path, pos = [], {}
            x = n0
            met3 = False
            while x not in fate and x not in pos:
                pos[x] = len(path)
                path.append(x)
                x = step(Q, t, x)
                if len(path) > 10 ** 5:
                    check(False, "T_S orbit too long n=%d" % n0)
                    return
            if x in pos:
                cyc = path[pos[x]:]
                m = min(cyc)
                i = cyc.index(m)
                cyc = tuple(cyc[i:] + cyc[:i])
                cycles.add(cyc)
                f = cyc
            else:
                f = fate[x]
            for y in path:
                fate[y] = f
        exp = {(1, 4, 2) if 1 in S else (1, 2), (3, 10, 5, 6)}
        check(cycles == exp, "T_S cycles %s: %s" % (S, sorted(cycles)))
        # orbits that never meet 3 mod 4 end in the small cycle; those that meet it end in (3 10 5 6)
        for n0 in range(1, 20000):
            x = n0
            met = False
            for _ in range(2000):
                if x % 4 == 3:
                    met = True
                x = step(Q, t, x)
            f = fate[n0]
            if not check(met == (f == (3, 10, 5, 6)), "T_S fate vs 3 mod 4 n=%d S=%s" % (n0, S)):
                break
    # G' orbits: all y <= 10^6 reach the fixed point 1 (only cycle found)
    fate = {1: 1}
    for y0 in range(1, N + 1):
        path = []
        y = y0
        seen = set()
        while y not in fate:
            if y in seen:
                check(False, "G' extra cycle through %d" % y)
                return
            seen.add(y)
            path.append(y)
            y = step(*GP_HAND, y)
        for q in path:
            fate[q] = 1
    print("  T_S cycle lists and G' (y <= 10^6) confirmed")


def part4_joins():
    print("[4] every recorded join, own engine + own Lemma S")
    sys.path.insert(0, HERE)
    from library import build    # data only
    lib = {s['id']: (s['Q'], [tuple(x) for x in s['table']], s['status']) for s in build()}
    n = 0
    for kind in ('lib', 'sfam4', 'sfam5'):
        d = json.load(open(os.path.join(HERE, 'results', 'equiv_%s.json' % kind)))
        for j in d['joins']:
            canon = (j['canon'][0], tuple(tuple(r) for r in j['canon'][1]))
            for (i, MX, rX, _) in j['members']:
                if i in lib:
                    Q, t, st = lib[i]
                    check(st == 'open', "join member is a settled system: %s %s" % (i, st))
                else:
                    m = int(i[2])
                    S = tuple(int(x) for x in i[4:].split('-'))
                    Q, t = s_fam(m, S)
                c, _ = induced(Q, t, MX, rX, tmax=24, pmax=20000)
                check(c == canon, "join identity %s %d %d" % (i, MX, rX))
                if MX > 1:
                    check(lemma_S(Q, t, MX, rX)[0], "join Lemma S %s %d %d" % (i, MX, rX))
                if unit_prime(Q, t):
                    check(type_of(Q, t)[0] == 'c', "join member not type (c): %s" % i)
                n += 1
    check(n == 4857, "join member count %d" % n)
    d = json.load(open(os.path.join(HERE, 'results', 'equiv_sfam5.json')))
    big = max(d['classes'], key=len)
    check(len(d['classes']) == 42 and sum(len(c) for c in d['classes']) == 264 and len(big) == 20,
          "class counts %d %d %d" % (len(d['classes']), sum(len(c) for c in d['classes']), len(big)))
    print("  %d join members re-proved" % n)
    return lib


CORES = {'sf3_7': (7,), 'sf3_17': (1, 7), 'sf3_57': (5, 7), 'sf3_157': (1, 5, 7),
         'sf3_357': (3, 5, 7), 'sf3_137': (1, 3, 7), 'sf3_13': (1, 3), 'sf3_135': (1, 3, 5)}


def exact_unbounded_2(Q, t, s, r):
    """Own exact criterion for a unit 2-adic table and X = r mod 2^s."""
    K = max(Q.bit_length() - 1, s)
    QK = 1 << K
    tt = [t[x % Q] for x in range(QK)]
    succ = cyl_graph(QK, tt)
    nonX = [x for x in range(QK) if x % (1 << s) != r]
    ns = set(nonX)
    sub = {x: [y for y in succ[x] if y in ns] for x in nonX}
    oncyc = set()
    for comp in sccs(nonX, sub):
        cs = set(comp)
        if any(y in cs for x in comp for y in sub[x]):
            oncyc |= cs
    # alive = non-X vertices that can reach a non-X cycle inside non-X
    alive = set(oncyc)
    ch = True
    while ch:
        ch = False
        for x in nonX:
            if x not in alive and any(y in alive for y in sub[x]):
                alive.add(x)
                ch = True
    return any(y in alive for x in range(QK) if x % (1 << s) == r for y in succ[x])


def part5_cores():
    print("[5] the 8 cores and 3x+1: bounded returns, distinctness, exact on 2-power classes")
    sysl = [(k, s_fam(3, S)) for k, S in CORES.items()] + [('3x+1', COLLATZ)]
    nexact = 0
    for (k, (Q, t)) in sysl:
        for s in range(1, 6):
            for r in range(1 << s):
                unb = exact_unbounded_2(Q, t, s, r)
                c, _ = induced(Q, t, 1 << s, r, tmax=80, pmax=200000)
                check((c is not None) == (not unb), "exact vs search %s 2^%d r=%d" % (k, s, r))
                nexact += not unb
    check(nexact == 16, "bounded on 2-power classes: %d (prover: 16)" % nexact)
    for tmax, pmax in ((24, 20000), (80, 100000)):
        seen = {}
        nb = 0
        for (k, (Q, t)) in sysl:
            for MX in range(1, 33):
                for rX in range(MX):
                    c, _ = induced(Q, t, MX, rX, tmax=tmax, pmax=pmax)
                    if c is None:
                        continue
                    nb += 1
                    key = repr(c)
                    if key in seen and seen[key] != k:
                        check(False, "cores collide %s %s" % (seen[key], k))
                    seen.setdefault(key, k)
        check(nb == 43, "bounded canonical returns tmax=%d: %d (prover: 43)" % (tmax, nb))
        print("  tmax=%d pmax=%d: %d bounded (incl. 9 maps), no collision" % (tmax, pmax, nb))


def part6_falsification(lib):
    print("[6] falsification tests of O1 / O2 / Theorem E on the library")
    # (a) O1 test: every bounded first return of a CERT system that is a unit p-adic table must
    #     have no expanding cycle in its cylinder graph (else Lemma R + Lemma B contradiction).
    # (b) O2 test: bounded returns of Theorem-H systems to p-adic classes are never type (c).
    # (c) no canonical return of a divergent / open system equals one of a settled system with
    #     Lemma S on both sides.
    H = {}
    ntest = {'cert_unit': 0, 'thmH_padic_unit': 0}
    classes = [(1, 0)] + [(M, r) for M in range(2, 25) for r in range(M)]
    for i, (Q, t, st) in lib.items():
        p = unit_prime(Q, t)
        for (MX, rX) in classes:
            try:
                c, _ = induced(Q, t, MX, rX, tmax=24, pmax=20000, Lmax=4096)
            except ValueError:
                continue
            if c is None:
                continue
            L, rows = c
            if L > 512 and unit_prime(L, list(rows)):
                ntest['skipped_L>512'] = ntest.get('skipped_L>512', 0) + 1
            elif st == 'cert' and unit_prime(L, list(rows)):
                ty = type_of(L, list(rows))[0]
                ntest['cert_unit'] += 1
                check(ty in ('a',), "O1 FALSIFIED? CERT %s on %d mod %d gives type %s"
                      % (i, rX, MX, ty))
            if L <= 512 and st == 'thmH' and p and (MX == 1 or unit_prime(MX, [(1, 0, 1)] * MX) == p) \
                    and unit_prime(L, list(rows)):
                ntest['thmH_padic_unit'] += 1
                ty = type_of(L, list(rows))[0]
                check(ty != 'c', "O2 FALSIFIED? %s on %d mod %d type (c)" % (i, rX, MX))
            suff = MX == 1 or lemma_S(Q, t, MX, rX)[0]
            if suff:
                H.setdefault(repr(c), set()).add((i, st))
    settled = {'cert', 'thmH', 'mixed', 'dress'}
    for key, mem in H.items():
        sts = {s for (_, s) in mem}
        if sts & settled and sts - settled:
            check(False, "join between settled and unsettled: %s" % sorted(mem))
    print("  tests: %s; %d distinct sufficient canonical returns, none mixes settled/unsettled"
          % (ntest, len(H)))
    check(ntest['cert_unit'] > 0, "O1 test is non-vacuous")
    # (d) 3x+1: no bounded return on classes M <= 64 is a type (a)/(b) table (would 'prove' Collatz)
    nb = 0
    for MX in range(2, 65):
        for rX in range(MX):
            c, _ = induced(*COLLATZ, MX, rX, tmax=30, pmax=20000)
            if c is None:
                continue
            nb += 1
            if c[0] <= 512 and unit_prime(c[0], list(c[1])):
                check(type_of(c[0], list(c[1]))[0] == 'c', "3x+1 return not type (c) %d %d" % (MX, rX))
    print("  3x+1: %d bounded returns on 2 <= M <= 64, all type (c) when unit" % nb)


def part7_growth_and_c27():
    print("[7] Lemma R witness for G', Lemma B for dch_C27_2466")
    for d in range(1, 30):
        y = 2 ** (d + 1) * 7          # y = 2^{d+1} k, k odd: d steps of 3y/2 stay even
        x = y
        for _ in range(d):
            x = step(*GP_HAND, x)
        check(x * 2 ** d == 3 ** d * y, "G' growth d=%d" % d)
    Q, t = c27_2466()
    sys.path.insert(0, HERE)
    from library import by_id
    s = by_id('dch_C27_2466')
    check([tuple(x) for x in s['table']] == t, "library table of dch_C27_2466 matches its rule")
    check(unit_prime(Q, t) == 3, "dch_C27_2466 is unit 3-adic")
    ty, _ = type_of(Q, t)
    check(ty == 'a', "dch_C27_2466 type %s (expected (a): plain certificate)" % ty)
    worst = Fraction(0)
    cyc = set()
    for n in range(1, 200001):
        x, mx = n, n
        seen = set()
        while x not in seen:
            seen.add(x)
            x = step(Q, t, x)
            mx = max(mx, x)
            if len(seen) > 10 ** 5:
                check(False, "C27 long orbit %d" % n)
                return
        worst = max(worst, Fraction(mx, max(n, 2000)))
        # canonical cycle
        c = [x]
        y = step(Q, t, x)
        while y != x:
            c.append(y)
            y = step(Q, t, y)
        cyc.add(min(c))
    check(cyc == {1, 5, 125}, "C27 cycles (min elements) %s" % cyc)
    print("  dch_C27_2466: n <= 2e5, max orbit / max(n, 2000) = %.3f; cycles via %s"
          % (float(worst), sorted(cyc)))
    # the 80/81 cycle of length 11 exists in the cylinder graph mod 27
    succ = cyl_graph(Q, t)
    best = None
    stack = [(r, [r], Fraction(1)) for r in range(Q)]
    while stack:
        r, path, m = stack.pop()
        m2 = m * Fraction(t[r][0], t[r][2])
        for s_ in succ[r]:
            if s_ == path[0] and (best is None or m2 > best[0]):
                best = (m2, path)
            if s_ > path[0] and s_ not in path and len(path) < 12:
                stack.append((s_, path + [s_], m2))
    check(best is not None and best[0] == Fraction(80, 81) and len(best[1]) == 11,
          "C27 max cycle multiplier %s length %d" % (best[0], len(best[1])))


if __name__ == "__main__":
    t0 = time.time()
    F4 = part1_propC_thmF()
    part2_types(F4)
    part3_B2_and_cycles(F4)
    lib = part4_joins()
    part5_cores()
    part6_falsification(lib)
    part7_growth_and_c27()
    print("time %.1f s" % (time.time() - t0))
    if FAILS:
        print("REFEREE2 CHECKS FAILED:", len(FAILS))
        sys.exit(1)
    print("REFEREE2 CHECKS PASSED")
