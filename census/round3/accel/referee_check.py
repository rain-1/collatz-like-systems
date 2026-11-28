"""Independent referee check for lens 'accel' (round 3).

Written from scratch from the rules as stated in the .md files.  Nothing from
accel_lib.py, check_*.py or descent_lib.py is imported.  systems.py is imported
ONLY to compare its step functions against the referee's own rule
implementations (section [DEF]).

Sections (all exact, ints / Fractions):
  [DEF]  referee rule implementations == prover systems.py on 1..10^5 and on
         random 200-bit inputs.
  [H]    Theorem H applied independently to acc_h32, acc_h16, acc_h9:
         affine branches derived from the rule itself, G_K built, own SCCs,
         exact multiplicative Bellman-Ford weights (c(s) q <= theta c(r)),
         exact cycle bound, enumeration of candidates, type-(b) points.
  [EV]   EVIDENCE: n <= 3*10^5 and 300 random inputs of 64..256 bits reach the
         claimed cycles (consistency only, not proof).
  [N]    Theorem N witnesses rebuilt independently for several systems: the
         periodic point y_d of C^d W is checked to be genuinely periodic under
         the p-adic extension of the map (orbit computed on rationals), with
         the right multiplier, y_d = x* mod p^(K+d v_C), y_d not on O(x*).
  [S]    S-family m=2..5: no SCC of G_m is an expanding simple cycle; count of
         subsets with an expanding cycle at level m vs round-2 OBST counts.
  [Z]    Theorem Z and Corollary C on random large z.
  [CYC]  independent enumeration of all cycles of period <= 26 for the S-family
         cores sf3_137, sf3_7, sf3_37, sf3_17, sf3_13 (pruned DFS over closed walks).
  [K]    Theorem K run identity / first-return identity on random inputs;
         dress_* cycles; equality of first return with catalog div23_5n1.
Runtime: about 1-2 minutes.
"""
import sys, os, random, math
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(20261127)
OK = True


def claim(name, cond):
    global OK
    print(("PASS " if cond else "FAIL ") + name)
    OK = OK and bool(cond)


# ------------------------------------------------------------- own rules
def r_h32(n):
    if n % 2 == 0:
        return n // 2
    r = n % 32
    if r in (5, 9, 21, 25):
        return n + 1
    if r == 29:
        return n + 9
    return 3 * n + 1


def r_h16(n):
    if n % 2 == 0:
        return n // 2
    r = n % 16
    if r in (5, 9):
        return n + 1
    if r == 13:
        return n + 5
    return 3 * n + 1


def r_h9(n):
    q, r = divmod(n, 9)
    if n % 3 == 0:
        return n // 3
    if r in (1, 4, 7):
        return 6 * q + r
    return {2: 12 * q + 4, 5: 12 * q + 7, 8: 12 * q + 11}[r]


def r_sf(m, S):
    S = set(S)
    def T(n):
        if n % 2 == 0:
            return n // 2
        return 3 * n + 1 if n % (2 ** m) in S else n + 1
    return T


def dressedR(p, q, e, g):
    def D(x):
        if x % p == 0:
            return q ** e * x // p
        if x % q == 0:
            return x // q
        return g(x)
    return D


def div23_5n1(n):          # census/systems.py: div_else([2,3],5,1)
    if n % 2 == 0:
        return n // 2
    if n % 3 == 0:
        return n // 3
    return 5 * n + 1


# ------------------------------------------------------------- [DEF]
sys.path.insert(0, HERE)
import systems as SY
pairs = [("acc_h32", r_h32), ("acc_h16", r_h16), ("acc_h9", r_h9),
         ("dress_23_x1", dressedR(2, 3, 1, lambda x: x + 1)),
         ("dress_32_x1", dressedR(3, 2, 2, lambda x: x + 1)),
         ("dress_23_3x1", dressedR(2, 3, 1, lambda x: 3 * x + 1)),
         ("dress_23_5x1", dressedR(2, 3, 1, lambda x: 5 * x + 1))]
for m, S in SY.SF:
    pairs.append((SY.sf_id(m, S), r_sf(m, S)))
for sid, f in pairs:
    g = SY.get(sid)["step"]
    xs = list(range(1, 100001)) + [random.getrandbits(200) + 1 for _ in range(2000)]
    claim(f"[DEF] {sid}: systems.py step == referee rule", all(f(x) == g(x) for x in xs))


# ------------------------------------------------------------- affine data
def branches(f, p, m):
    """Derive the affine branch n -> a n + b (a, b Fractions) on each class mod
    p^m from the step function itself, and check affinity on many points."""
    Q = p ** m
    out = []
    for r in range(Q):
        n1, n2 = r + Q, r + 2 * Q
        a = Fraction(f(n2) - f(n1), Q)
        b = f(n1) - a * n1
        for t in list(range(3, 40)) + [random.getrandbits(100) for _ in range(20)]:
            n = r + Q * t
            assert f(n) == a * n + b
        out.append((a, b))
    return out


def vp(x, p):
    k = 0
    while x % p == 0:
        x //= p
        k += 1
    return k


def graphK(br, p, m, K):
    PK = p ** K
    E = {}
    for r in range(PK):
        a, b = br[r % p ** m]
        e = vp(a.denominator, p)
        assert a.denominator == p ** e and a.numerator % p != 0   # unit multiplier
        img = a * r + b
        assert img.denominator == 1
        mod = PK // p ** e
        base = int(img) % mod
        E[r] = [(base + i * mod, a) for i in range(p ** e)]
    return E


def sccs(nodes, E):
    # Kosaraju, iterative
    seen, order = set(), []
    for v in nodes:
        if v in seen:
            continue
        stack = [(v, iter([s for s, _ in E[v]]))]
        seen.add(v)
        while stack:
            u, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                stack.pop()
                order.append(u)
            elif nxt not in seen:
                seen.add(nxt)
                stack.append((nxt, iter([s for s, _ in E[nxt]])))
    R = {v: [] for v in nodes}
    for v in nodes:
        for s, _ in E[v]:
            R[s].append(v)
    comp, out = {}, []
    for v in reversed(order):
        if v in comp:
            continue
        cur, st = [], [v]
        comp[v] = len(out)
        while st:
            u = st.pop()
            cur.append(u)
            for w in R[u]:
                if w not in comp:
                    comp[w] = len(out)
                    st.append(w)
        out.append(cur)
    return out


def exact_weights(comp, E):
    cs = set(comp)
    ed = [(r, s, q) for r in comp for s, q in E[r] if s in cs]
    for k in range(1, 40):
        theta = 1 - Fraction(1, 2 ** k)
        c = {v: Fraction(1) for v in comp}
        for _ in range(len(comp) + 2):
            ch = False
            for r, s, q in ed:
                nv = theta * c[r] / q
                if nv < c[s]:
                    c[s] = nv
                    ch = True
            if not ch:
                break
        if not ch and all(c[s] * q <= theta * c[r] for r, s, q in ed) and min(c.values()) > 0:
            return theta, c
    return None


def apply_affine_padic(br, p, m, y):
    a, b = br[int(y.numerator * pow(y.denominator, -1, p ** m)) % p ** m]
    return a * y + b


def theorem_H_ref(name, f, p, m, K, expect_min):
    br = branches(f, p, m)
    E = graphK(br, p, m, K)
    PK = p ** K
    comps = sccs(list(range(PK)), E)
    cyc_mins = set()
    nontriv = []
    for comp in comps:
        cs = set(comp)
        ed = [(r, s, q) for r in comp for s, q in E[r] if s in cs]
        if not ed:
            continue
        if len(ed) == len(comp):          # strongly connected with |E|=|V|: simple cycle
            nxt = {r: (s, q) for r, s, q in ed}
            seq, lam, r = [comp[0]], Fraction(1), comp[0]
            while nxt[r][0] != comp[0]:
                lam *= nxt[r][1]
                r = nxt[r][0]
                seq.append(r)
            lam *= nxt[r][1]
            # standing hypothesis: a division on the cycle
            assert any(br[s % p ** m][0].denominator > 1 for s in seq)
            # composed affine map along seq -> periodic point
            A, B = Fraction(1), Fraction(0)
            for s in seq:
                a, b = br[s % p ** m]
                A, B = a * A, a * B + b
            x = B / (1 - A)
            # check x really follows seq under the p-adic extension
            y = x
            for s in seq:
                assert int(y.numerator * pow(y.denominator, -1, PK)) % PK == s
                y = apply_affine_padic(br, p, m, y)
            assert y == x
            kind = "expanding-simple" if lam > 1 else "contracting-simple"
            if x.denominator == 1 and x > 0:
                cyc_mins.add(min(cycle_from(f, int(x))))
            nontriv.append((kind, len(comp), str(x), str(lam)))
            continue
        w = exact_weights(comp, E)
        claim(f"[H] {name}: SCC of size {len(comp)} has exact contraction weights", w is not None)
        if w is None:
            return
        theta, c = w
        beta = max(c[s] * max(br[r % p ** m][1], 0) for r, s, q in ed)
        Vmax = beta / (1 - theta)
        nmax = math.floor(Vmax / min(c.values()))
        nontriv.append(("contracting", len(comp), f"theta={theta}", f"nmax={nmax}"))
        assert nmax < 5 * 10 ** 6
        for n in range(1, nmax + 1):
            r = n % PK
            if r in cs and c[r] * n <= Vmax:
                cyc_mins.add(min(cycle_from(f, n)))
    claim(f"[H] {name}: SCC structure {sorted(nontriv)}; no SCC outside types (a)/(b)", True)
    claim(f"[H] {name}: cycle minima from Theorem H = {sorted(cyc_mins)} (expected {expect_min})",
          sorted(cyc_mins) == expect_min)
    # x* = -1 is fixed and expanding
    y = Fraction(-1)
    claim(f"[H] {name}: -1 is a p-adic fixed point", apply_affine_padic(br, p, m, y) == y
          or apply_affine_padic(br, p, m, apply_affine_padic(br, p, m, y)) == y)


def cycle_from(f, n, cap=10 ** 6):
    seen = {}
    while n not in seen:
        seen[n] = 1
        n = f(n)
        assert len(seen) < cap
    c, z = [n], f(n)
    while z != n:
        c.append(z)
        z = f(z)
    return c


theorem_H_ref("acc_h32", r_h32, 2, 5, 5, [1, 3, 19])
theorem_H_ref("acc_h32 (level K=7)", r_h32, 2, 5, 7, [1, 3, 19])
theorem_H_ref("acc_h16", r_h16, 2, 4, 4, [1, 3])
theorem_H_ref("acc_h16 (level K=6)", r_h16, 2, 4, 6, [1, 3])
theorem_H_ref("acc_h9", r_h9, 3, 2, 2, [1, 4, 7])
theorem_H_ref("acc_h9 (level K=4)", r_h9, 3, 2, 4, [1, 4, 7])
claim("[H] acc_h32 cycle (19 58 29 38)", cycle_from(r_h32, 19) == [19, 58, 29, 38])
claim("[H] acc_h32 cycle (3 10 5 6), (1 4 2)", cycle_from(r_h32, 3) == [3, 10, 5, 6]
      and cycle_from(r_h32, 1) == [1, 4, 2])

# ------------------------------------------------------------- [EV]
for name, f, exp in (("acc_h32", r_h32, [1, 3, 19]), ("acc_h16", r_h16, [1, 3]),
                     ("acc_h9", r_h9, [1, 4, 7])):
    mins = set()
    memo = {}
    for n in range(1, 300001):
        path, x = [], n
        while x not in memo and len(path) < 10 ** 5:
            if x in path[-200:]:
                break
            path.append(x)
            x = f(x)
        if x in memo:
            res = memo[x]
        else:
            res = min(cycle_from(f, x))
        for y in path:
            if y <= 10 ** 7:
                memo[y] = res
        mins.add(res)
    for _ in range(300):
        mins.add(min(cycle_from(f, random.getrandbits(random.randint(64, 256)) + 1)))
    claim(f"[EV] {name}: n<=3e5 and 300 random big n reach only {sorted(mins)}", sorted(mins) == exp)


# ------------------------------------------------------------- [N]
def barrier(name, f, p, m, xstar, K=None, dmax=12):
    K = K or m
    br = branches(f, p, m)
    E = graphK(br, p, m, K)
    PK = p ** K
    res = lambda y, k: int(y.numerator * pow(y.denominator, -1, p ** k)) % p ** k
    # orbit of x*
    orb, y = [], Fraction(xstar)
    while y not in orb:
        orb.append(y)
        y = apply_affine_padic(br, p, m, y)
    assert y == orb[0]
    C = [res(z, K) for z in orb]
    lamC = Fraction(1)
    for z in orb:
        lamC *= br[res(z, m)][0]
    vC = sum(vp(br[res(z, m)][0].denominator, p) for z in orb)
    Cedges = {(C[i], C[(i + 1) % len(C)]) for i in range(len(C))}
    # find an edge a->b not in C, inside the SCC of C[0], and a closed walk W through C[0]
    comps = sccs(list(range(PK)), E)
    comp = next(cc for cc in comps if C[0] in cc)
    cs = set(comp)
    W = None
    for a in comp:
        for b, _ in E[a]:
            if b in cs and (a, b) not in Cedges:
                W = bfs(E, cs, C[0], a) + bfs(E, cs, b, C[0])[:-1]
                # W as node list starting at C[0], closed back to C[0]
                break
        if W:
            break
    assert W is not None, "SCC is a simple cycle"
    W = W  # nodes visited, consecutive pairs are edges, last -> C[0]
    ok = True
    ys = []
    for d in range(dmax + 1):
        walk = C * d + W
        # composed map
        A, B = Fraction(1), Fraction(0)
        for s in walk:
            a, b = br[s % p ** m]
            A, B = a * A, a * B + b
        yd = B / (1 - A)
        # genuine periodicity under the p-adic extension, following the walk
        z = yd
        for s in walk:
            ok &= res(z, K) == s
            z = apply_affine_padic(br, p, m, z)
        ok &= z == yd
        ok &= res(yd, K + d * vC) == res(Fraction(xstar), K + d * vC)
        # not on the orbit of x*
        z, seen = yd, set()
        for _ in range(len(walk)):
            seen.add(z)
            z = apply_affine_padic(br, p, m, z)
        ok &= not (seen & set(orb))
        ys.append((d, yd, A))
    lamW = ys[0][2]
    ok &= all(A == lamC ** d * lamW for d, _, A in ys)
    ok &= lamC > 1 and ys[-1][2] > 1
    ok &= len({y for _, y, _ in ys}) == len(ys)
    claim(f"[N] {name}: x*={xstar} lamC={lamC} |W|={len(W)} lamW={lamW}; y_0..y_{dmax} genuine "
          f"periodic points, expanding from d={next(d for d, _, A in ys if A > 1)}", ok)


def bfs(E, cs, a, b):
    """Shortest node path a ... b inside cs (list incl. both ends)."""
    prev, fr = {a: None}, [a]
    while fr:
        nf = []
        for u in fr:
            for v, _ in E[u]:
                if v in cs and v not in prev:
                    prev[v] = u
                    nf.append(v)
        fr = nf
    assert b in prev
    path, x = [b], b
    while prev[x] is not None:
        x = prev[x]
        path.append(x)
    return path[::-1]


barrier("3x+1", lambda n: n // 2 if n % 2 == 0 else 3 * n + 1, 2, 1, -1)
barrier("5x+1", lambda n: n // 2 if n % 2 == 0 else 5 * n + 1, 2, 1, Fraction(-1, 3))
barrier("perm_1932", lambda n: 2 * n // 3 if n % 3 == 0 else ((4 * n - 1) // 3 if n % 3 == 1 else (4 * n + 1) // 3),
        3, 1, -1)
barrier("split5_3", lambda n: n // 2 if n % 2 == 0 else (5 * n + 3 if n % 4 == 1 else n + 3), 2, 2, -3)
barrier("sf3_137 (W)", r_sf(3, (1, 3, 7)), 2, 3, -1)
barrier("sf3_7 (K7)", r_sf(3, (7,)), 2, 3, -1)
barrier("sf3_13", r_sf(3, (1, 3)), 2, 3, -5, dmax=30)
barrier("sf3_137 at level K=6", r_sf(3, (1, 3, 7)), 2, 3, -1, K=6)


# ------------------------------------------------------------- [S]
def sfam_graph(m, S):
    Q = 2 ** m
    E = {}
    for r in range(Q):
        if r % 2 == 0:
            E[r] = [(r // 2, (0, 1)), (r // 2 + Q // 2, (0, 1))]
        else:
            E[r] = [((3 * r + 1) % Q, (1, 0))] if r in S else [((r + 1) % Q, (0, 0))]
    return E


def has_expanding_cycle(m, E):
    # float Karp max mean (search only) for counting; log weights
    Q = 2 ** m
    l3, l2 = math.log(3), math.log(2)
    nodes = list(range(Q))
    NEG = float("-inf")
    D = [[NEG] * Q for _ in range(Q + 1)]
    D[0] = [0.0] * Q
    for k in range(1, Q + 1):
        for a in nodes:
            if D[k - 1][a] == NEG:
                continue
            for b, (i3, i2) in E[a]:
                v = D[k - 1][a] + i3 * l3 - i2 * l2
                if v > D[k][b]:
                    D[k][b] = v
    best = NEG
    for v in nodes:
        if D[Q][v] == NEG:
            continue
        best = max(best, min((D[Q][v] - D[k][v]) / (Q - k) for k in range(Q) if D[k][v] != NEG))
    return best > 1e-12


for m in (2, 3, 4, 5):
    Q = 2 ** m
    odd = list(range(1, Q, 2))
    bad, nexp = 0, 0
    for mask in range(1 << len(odd)):
        S = {odd[i] for i in range(len(odd)) if mask >> i & 1}
        E = sfam_graph(m, S)
        for comp in sccs(list(range(Q)), E):
            cs = set(comp)
            ed = [(a, b, w) for a in comp for b, w in E[a] if b in cs]
            if ed and len(ed) == len(comp):
                if 3 ** sum(w[0] for *_, w in ed) > 2 ** sum(w[1] for *_, w in ed):
                    bad += 1
        if m <= 4:
            nexp += has_expanding_cycle(m, E)
    claim(f"[S] m={m}: no expanding simple-cycle SCC over all {1 << len(odd)} subsets", bad == 0)
    if m <= 4:
        print(f"      m={m}: subsets with an expanding cycle already at level m: {nexp}")


# ------------------------------------------------------------- [Z]
def odd(x):
    while x % 2 == 0:
        x //= 2
    return x


def Tcol(z):
    return z // 2 if z % 2 == 0 else (3 * z + 1) // 2


okZ = True
for m, S in SY.SF:
    T = r_sf(m, S)
    for _ in range(3000):
        z = random.getrandbits(random.choice([8, 40, 200]))
        n = T(2 * z + 1)
        while n % 2 == 0:
            n = T(n)
        if (2 * z + 1) % 2 ** m in S:
            G = (odd(3 * z + 2) - 1) // 2
        else:
            G = (odd(z + 1) - 1) // 2
        okZ &= n == 2 * G + 1
claim("[Z] Theorem Z: next odd T_S value of 2z+1 is 2G_S(z)+1 (random z, all 12 S)", okZ)
okC = True
for m, S in ((2, (3,)), (3, (3, 7))):
    T = r_sf(m, S)
    for z in list(range(0, 5000)) + [random.getrandbits(300) for _ in range(3000)]:
        okC &= T(T(2 * z + 1)) == 2 * Tcol(z) + 1
claim("[Z] Corollary C: T_S^2(2z+1) = 2T(z)+1 for S={3 mod 4}, m=2,3", okC)


# ------------------------------------------------------------- [CYC]
def cycles_upto(m, S, L):
    """All T_S cycles of period <= L via closed walks in G_m, pruned DFS.
    Composed map kept as x -> (3^a x + B)/2^b with integers."""
    Q = 2 ** m
    E = {}
    for r in range(Q):
        if r % 2 == 0:
            E[r] = [(r // 2, 0), (r // 2 + Q // 2, 0)]
        else:
            E[r] = [((3 * r + 1) % Q, 1)] if r in S else [((r + 1) % Q, 2)]
    T = r_sf(m, S)
    found = set()
    for r0 in range(Q):
        # can[t][s]: walk of length t from s to r0 exists
        can = [set([r0])]
        for t in range(1, L + 1):
            can.append({s for s in range(Q) if any(b in can[t - 1] for b, _ in E[s])})
        stack = [(r0, 0, 1, 0, 0)]  # node, length, 3^a, B, b   map x -> (A x + B)/2^b
        while stack:
            s, l, A, B, b = stack.pop()
            if l > 0 and s == r0 and b > 0:
                den = 2 ** b - A
                if den != 0 and B % den == 0:
                    x = B // den
                    if x > 0 and x % Q == r0:
                        cyc = cycle_from(T, x)
                        if len(cyc) <= L:
                            found.add(min(cyc))
            if l == L:
                continue
            for nb, kind in E[s]:
                if (L - l - 1) >= 0 and any(nb in can[t] for t in range(0, L - l)):
                    if s % 2 == 0:
                        # x -> x/2 : (A x + B)/2^b -> (A x + B)/2^(b+1)
                        stack.append((nb, l + 1, A, B, b + 1))
                    elif kind == 1:
                        # 3y+1 with y = (A x + B)/2^b : (3A x + 3B + 2^b)/2^b
                        stack.append((nb, l + 1, 3 * A, 3 * B + 2 ** b, b))
                    else:
                        stack.append((nb, l + 1, A, B + 2 ** b, b))
    return sorted(found)


EXPCYC = {(3, (1, 3, 7)): [1, 3, 7, 39], (3, (7,)): [1], (3, (3, 7)): [1, 3],
          (3, (1, 7)): [1], (3, (1, 3)): [1, 3], (2, (3,)): [1, 3]}
for (m, S), exp in EXPCYC.items():
    got = cycles_upto(m, set(S), 26)
    claim(f"[CYC] sf{m}_{''.join(map(str, S))}: cycles of period <= 26 have minima {got}", got == exp)
claim("[CYC] sf3_137 9-cycle through 7",
      cycle_from(r_sf(3, (1, 3, 7)), 7) == [7, 22, 11, 34, 17, 52, 26, 13, 14])
claim("[CYC] sf3_137 15-cycle through 39", len(cycle_from(r_sf(3, (1, 3, 7)), 39)) == 15)


# ------------------------------------------------------------- [K]
def rough(x, ps):
    for q in ps:
        while x % q == 0:
            x //= q
    return x


okK = True
for (p, q, e) in ((2, 3, 1), (3, 2, 2), (2, 5, 1), (5, 2, 3), (3, 5, 1)):
    for gname, g in (("x+1", lambda x: x + 1), ("3x+1", lambda x: 3 * x + 1), ("5x+1", lambda x: 5 * x + 1)):
        D = dressedR(p, q, e, g)
        for _ in range(300):
            w = rough(random.getrandbits(80) + 1, (p, q))
            i, k = random.randint(0, 12), random.randint(0, 12)
            x = p ** i * q ** k * w
            y = x
            for _ in range(i + e * i + k):
                y = D(y)
            okK &= y == w
            # first return of D from w equals rough(g(w))
            y, steps = D(w), 1
            while rough(y, (p, q)) != y:
                y = D(y)
                steps += 1
                assert steps < 10 ** 4
            okK &= y == rough(g(w), (p, q))
claim("[K] run identity D^(i+ei+k)(p^i q^k w) = w and first return = rho(g(w)) (5 prime pairs x 3 maps)", okK)
claim("[K] dress_23_x1 cycle (1 2 3)", cycle_from(dressedR(2, 3, 1, lambda x: x + 1), 1) == [1, 2, 3])
claim("[K] dress_32_x1 cycle (1 2)", cycle_from(dressedR(3, 2, 2, lambda x: x + 1), 1) == [1, 2])
claim("[K] dress_23_5x1 cycle (1 6 9 3); div23_5n1 cycle (1 6 3)",
      cycle_from(dressedR(2, 3, 1, lambda x: 5 * x + 1), 1) == [1, 6, 9, 3]
      and cycle_from(div23_5n1, 1) == [1, 6, 3])
okR = True
D5 = dressedR(2, 3, 1, lambda x: 5 * x + 1)
for _ in range(3000):
    w = rough(random.getrandbits(120) + 1, (2, 3))
    y = div23_5n1(w)
    while rough(y, (2, 3)) != y:
        y = div23_5n1(y)
    okR &= y == rough(5 * w + 1, (2, 3))
claim("[K] div23_5n1 first return on 6-rough numbers = rho(5w+1) (so equals dressed one)", okR)
# dress_23_x1 / dress_32_x1: every x <= 2e5 reaches the cycle (evidence; proof is R(w) < w)
for name, D, c0 in (("dress_23_x1", dressedR(2, 3, 1, lambda x: x + 1), 1),
                    ("dress_32_x1", dressedR(3, 2, 2, lambda x: x + 1), 1)):
    claim(f"[K] {name}: x <= 2e5 reach cycle through 1 (evidence)",
          all(min(cycle_from(D, x)) == 1 for x in range(1, 200001)))

print("ALL PASS" if OK else "SOME FAIL")
sys.exit(0 if OK else 1)
