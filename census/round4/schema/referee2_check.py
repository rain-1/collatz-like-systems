#!/usr/bin/env python3
"""referee2_check.py -- second referee's independent check for round4/schema.

Written from scratch.  Imports nothing from depthlib, schemalib, windowlib, decide.py
or referee1_check.py.  All decisions are exact (ints / Fractions); floats are only used
as guesses that are then certified exactly, or to choose a margin that is re-checked.

 [Q1] Theorem A1: for random members of D(m, word, h, i0) with RANDOM residue layouts
      (not the prover's consecutive layout), my generic exact Lambda search (BFS over
      (node, 3-exponent, 2-exponent)) gives k* = Lambda + 1 equal to my own
      implementation of the A1 formula; CERT members have an exact potential; members
      with G_exit >= Q have an exactly verified non-contracting closed walk; and
      brute force over all n <= X gives the cycle list {(1), loop}.
 [Q2] Records m = 4..10: generic exact Lambda (independent of A1) gives the stated k*;
      for m = 7..10 an integer witness built by my own Lemma-1 progression solver along
      the BFS-reconstructed deepest walk is iterated directly.
 [Q3] Theorem A3's bound vs. generic exact k* on random CERT base-2 tables, u in {1,3},
      translation nodes allowed (drift tracked).
 [Q4] B1 instances: 3x+1 / K7 cut-offs.  Exact periodic points of the blocks, 2-adic
      branch checks, avoidance of U_J, agreement mod 2^(K+i); type (c) of the cut
      systems (my Tarjan SCC); adversarial random replacements on U_J; CERT (exact
      potential) and brute-force cycle lists below J0.
 [Q5] Window part: |R_N| count, W2 potential (my own weights) on every edge of T_N,
      Lyapunov decrease above B_N, W3 cycle lists by brute force, W1' for the plain
      map (exact potential for T0_N), W4 finite facts.
 [Q6] Entropy exponent: exact test of the printed bounds 2^{0.954N} (README) and
      2^{0.9544N} (window.md) against sum_{k>5N/8} C(N,k).  (Expected to FAIL as
      printed for large N; reported, not asserted as a pass.)
 [Q7] Negative controls: the potential certifier must refuse OBST tables; the Lambda
      search must disagree with a deliberately wrong k*.
"""
import sys, math, random, time
from fractions import Fraction

ok = True
LOG2_3 = math.log2(3)


def claim(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name, flush=True)
    ok = ok and bool(cond)


# ------------------------------------------------------------------ generic table tools
def succ(Q, tab, r):
    u, v, w = tab[r]
    s0 = ((u * r + v) // w) % (Q // w)
    return [s0 + j * (Q // w) for j in range(w)]


def check_hyp(Q, tab):
    """(H1), (H2), (P) exactly."""
    for r in range(Q):
        u, v, w = tab[r]
        if not (u >= 1 and math.gcd(u, Q) == 1 and w >= 1 and Q % w == 0 and (u * r + v) % w == 0):
            return False
        n = r if r >= 1 else Q
        if (u * n + v) // w < 1:
            return False
    return True


def step(Q, tab, n):
    u, v, w = tab[n % Q]
    x = u * n + v
    assert x % w == 0
    return x // w


def gt1(x, y):
    """3^x / 2^y > 1 exactly (float guess with margin, exact fallback)."""
    d = x * LOG2_3 - y
    if d > 1e-6:
        return True
    if d < -1e-6:
        return False
    return 3 ** x > 2 ** y


def lam_pair(u, w):
    """multiplier u/w with u in {1,3}, w a power of 2 -> (x, y)."""
    x = {1: 0, 3: 1}[u]
    y = w.bit_length() - 1
    assert 1 << y == w
    return x, y


def exact_Lambda(Q, tab, keep_parents=False, limit=10 ** 7):
    """Generic Lambda of Theorem 3 (dichotomy.md) for base-2 tables with u in {1,3}:
    longest walk all of whose nonempty prefixes have multiplier > 1, or = 1 with
    translation drift >= 0.  States (node, x, y, drift) with drift None unless the
    prefix is a pure translation walk.  Returns Lambda (and the deepest walk)."""
    layer = {}
    for r in range(Q):
        layer[(r, 0, 0, 0)] = None        # empty prefix: multiplier 1, drift 0
    parents = []
    t = 0
    while True:
        new = {}
        for st in layer:
            r, x, y, dr = st
            u, v, w = tab[r]
            a, b = lam_pair(u, w)
            x2, y2 = x + a, y + b
            if x2 == 0 and y2 == 0:
                if dr is None:
                    continue
                dr2 = dr + v
                if dr2 < 0:
                    continue
            else:
                if not gt1(x2, y2):
                    continue
                dr2 = None
            for s in succ(Q, tab, r):
                key = (s, x2, y2, dr2)
                if key not in new:
                    new[key] = st
        if not new:
            break
        t += 1
        if keep_parents:
            parents.append(new)
        layer = new
        if t > limit:
            raise RuntimeError("Lambda search too long")
    walk = None
    if keep_parents and t > 0:
        st = next(iter(layer))
        walk = [st[0]]
        for i in range(t - 1, -1, -1):
            st = parents[i][st]
            walk.append(st[0])
        walk.reverse()
    return t, walk


def exact_potential(Q, tab, iters=4000):
    """Try to certify CERT: value iteration (floats) for g(r) = max(1, gamma*(u/w)*max g(s)),
    then rationalise and verify c(s) u < c(r) w on every edge EXACTLY.  Returns True only
    if the exact verification passes (a proof of CERT by Theorem 1(c))."""
    S = [succ(Q, tab, r) for r in range(Q)]
    for gamma in (1.0005, 1.002, 1.01, 1.05):
        g = [1.0] * Q
        for _ in range(iters):
            ch = False
            for r in range(Q):
                u, v, w = tab[r]
                val = max(1.0, gamma * u / w * max(g[s] for s in S[r]))
                if val > 1e300:
                    break
                if val > g[r] * (1 + 1e-15):
                    g[r] = val
                    ch = True
            if not ch:
                break
        c = [Fraction(x).limit_denominator(10 ** 9) for x in g]
        good = True
        for r in range(Q):
            u, v, w = tab[r]
            cm = max(c[s] for s in S[r])
            if not (cm * u < c[r] * w):
                good = False
                break
        if good:
            return True
    return False


def nonneg_cycle(Q, tab):
    """Find a closed walk with multiplier >= 1 (Bellman-Ford on log weights, float),
    then VERIFY its multiplier exactly.  Returns the exact multiplier or None."""
    S = [succ(Q, tab, r) for r in range(Q)]
    wt = [math.log(tab[r][0] / tab[r][2]) for r in range(Q)]
    dist = [0.0] * Q
    par = [None] * Q
    last = None
    for it in range(Q + 1):
        last = None
        for r in range(Q):
            for s in S[r]:
                if dist[r] + wt[r] > dist[s] + 1e-12:
                    dist[s] = dist[r] + wt[r]
                    par[s] = r
                    last = s
        if last is None:
            return None
    x = last
    for _ in range(Q):
        x = par[x]
    cyc = [x]
    y = par[x]
    while y != x:
        cyc.append(y)
        y = par[y]
    cyc.reverse()
    for i in range(len(cyc)):
        assert cyc[(i + 1) % len(cyc)] in S[cyc[i]]
    mult = Fraction(1)
    for r in cyc:
        mult *= Fraction(tab[r][0], tab[r][2])
    return mult if mult >= 1 else None


def cycles_bruteforce(Q, tab, X, cap=10 ** 7):
    """All cycles reached from n = 1..X (sets of elements)."""
    done = set()
    cyc = set()
    for n0 in range(1, X + 1):
        if n0 in done:
            continue
        path = {}
        seq = []
        n = n0
        while n not in done and n not in path:
            path[n] = len(seq)
            seq.append(n)
            n = step(Q, tab, n)
            if len(seq) > cap:
                raise RuntimeError("orbit too long")
        if n in path:
            cyc.add(tuple(sorted(seq[path[n]:])))
        done.update(seq)
    return cyc


def progression(Q, tab, nodes):
    """My own Lemma-1 solver: (a, M) with every n = a (mod M) following nodes."""
    a = nodes[0]
    M = Q
    Y, K = a, Q            # T^i(a + M t) = Y + K t
    for i in range(len(nodes) - 1):
        r = nodes[i]
        assert Y % Q == r
        u, v, w = tab[r]
        Y1 = (u * Y + v)
        assert Y1 % w == 0 and (u * K) % w == 0
        Y1 //= w
        K1 = u * K // w
        g = math.gcd(K1, Q)
        need = (nodes[i + 1] - Y1) % Q
        assert need % g == 0, "not an edge"
        mod = Q // g
        t0 = (need // g) * pow((K1 // g) % mod, -1, mod) % mod if mod > 1 else 0
        a += M * t0
        Y = Y1 + K1 * t0
        M *= mod
        K = K1 * mod
    return a, M


# ------------------------------------------------------------------ family D (from the text)
def christoffel(a, b):
    L = a + b
    return ['U' if ((i + 1) * a) // L - (i * a) // L == 1 else 'D' for i in range(L)]


def build_D(m, word, h, i0, rng=None):
    Q = 2 ** m
    L = len(word)
    pool = list(range(2, Q // 2))
    if rng is not None:
        rng.shuffle(pool)
    assert L + h <= len(pool)
    ell = pool[:L]
    ch = pool[L:L + h]
    tab = [None] * Q
    for i, c in enumerate(word):
        r, s = ell[i], ell[(i + 1) % L]
        tab[r] = (3, s - 3 * r, 1) if c == 'U' else (1, 2 * s - r, 2)
    for j in range(h):
        nxt = ch[j + 1] if j + 1 < h else ell[i0]
        tab[ch[j]] = (3, nxt - 3 * ch[j], 1)
    for r in range(Q):
        if tab[r] is None:
            tab[r] = (1, (Q - r) % Q, Q)
    return Q, tab, ell, ch


def A1_formula(word, h, i0, Q):
    """My implementation of G_exit and the k* formula of Theorem A1 (exact)."""
    L = len(word)
    f = {'U': Fraction(3), 'D': Fraction(1, 2)}
    lam = Fraction(1)
    for c in word:
        lam *= f[c]

    def P(i, s):
        x = Fraction(1)
        for k in range(s):
            x *= f[word[(i + k) % L]]
        return x
    Gex = Fraction(0)
    starts = [(i, Fraction(1)) for i in range(L)] + [(i0, Fraction(3) ** j) for j in range(1, h + 1)]
    for i, G in starts:
        for s in range(1, L + 1):
            if word[(i + s - 1) % L] == 'D':
                Gex = max(Gex, G * P(i, s))

    def tstar(i, G):
        best = None
        for s in range(1, L + 1):
            x = G * P(i, s)
            k = 0
            while x * lam ** k >= 1:
                k += 1
            t = k * L + s
            best = t if best is None else min(best, t)
        return best
    if lam >= 1:
        return lam, Gex, None
    k = max(h + tstar(i0, Fraction(3) ** h), max(tstar(i, Fraction(1)) for i in range(L)))
    return lam, Gex, k


# ================================================================== [Q1]
rng = random.Random(4242)
t0 = time.time()
nc = no = 0
good = True
bad_note = ""
while nc < 120 or no < 30:
    m = rng.randint(4, 7)
    Q = 2 ** m
    L = rng.randint(1, min(16, Q // 2 - 3))
    word = [rng.choice('UD') for _ in range(L)]
    if 'D' not in word:
        continue
    lamv = Fraction(3) ** word.count('U') / Fraction(2) ** word.count('D')
    if lamv >= 1:
        continue
    h = rng.randint(0, min(5, Q // 2 - 2 - L))
    i0 = rng.randrange(L)
    lam, Gex, kf = A1_formula(word, h, i0, Q)
    Qm, tab, ell, ch = build_D(m, word, h, i0, rng)
    if not check_hyp(Qm, tab):
        good = False; bad_note = "hyp"; break
    if any(u == 1 and w == 1 for (u, v, w) in tab):
        good = False; bad_note = "translation"; break
    if Gex < Q and nc < 120:
        Lam, _ = exact_Lambda(Qm, tab)
        cert = exact_potential(Qm, tab)
        cyc = cycles_bruteforce(Qm, tab, 4000)
        expect = {(1,), tuple(sorted(ell))}
        if not (cert and Lam + 1 == kf and cyc == expect):
            good = False; bad_note = f"cert {cert} Lam+1 {Lam+1} kf {kf} cyc {cyc}"; break
        nc += 1
    elif Gex >= Q and no < 30:
        mult = nonneg_cycle(Qm, tab)
        if mult is None:
            good = False; bad_note = "no nonneg cycle"; break
        no += 1
claim(f"[Q1] A1 on {nc} random CERT members (random layouts): exact potential, generic "
      f"Lambda+1 = formula, cycles(n<=4000) = {{(1), loop}}; {no} members with G_exit >= Q "
      f"have an exact closed walk of multiplier >= 1 ({time.time()-t0:.0f}s) {bad_note}", good)

# ================================================================== [Q2]
REC = {4: (26, 1, 2, 2, 2), 5: (132, 3, 5, 4, 3), 6: (791, 5, 8, 11, 4), 7: (4335, 17, 27, 13, 5),
       8: (41362, 41, 65, 14, 5), 9: (133534, 94, 149, 16, 6), 10: (304506, 147, 233, 17, 6)}
MAXM = int(sys.argv[1]) if len(sys.argv) > 1 else 10
for m in sorted(REC):
    if m > MAXM:
        continue
    k, a, b, i0, h = REC[m]
    t0 = time.time()
    word = christoffel(a, b)
    assert word.count('U') == a and word.count('D') == b
    Q, tab, ell, ch = build_D(m, word, h, i0, random.Random(m))
    hyp = check_hyp(Q, tab)
    # G_exit < Q exactly, computed directly (CERT by A1(1) + Theorem 1; also potential for small m)
    f = {'U': Fraction(3), 'D': Fraction(1, 2)}
    L = a + b
    Gex = Fraction(0)
    for i, G in [(i, Fraction(1)) for i in range(L)] + [(i0, Fraction(3) ** j) for j in range(1, h + 1)]:
        x = G
        for s in range(1, L + 1):
            x *= f[word[(i + s - 1) % L]]
            if word[(i + s - 1) % L] == 'D':
                Gex = max(Gex, x)
    lam = Fraction(3 ** a, 2 ** b)
    Lam, walk = exact_Lambda(Q, tab, keep_parents=(m >= 7))
    msg = f"m = {m}: hyp {hyp}, G_exit = {float(Gex):.3f} < Q = {Q}: {Gex < Q}, lam = {float(lam):.5f}, generic Lambda+1 = {Lam+1}"
    cond = hyp and Gex < Q and lam < 1 and Lam + 1 == k
    if m <= 6:
        cert = exact_potential(Q, tab)
        msg += f", exact potential {cert}"
        cond &= cert
    if m >= 7:
        assert len(walk) == Lam + 1
        aa, M = progression(Q, tab, walk)
        n = aa + M * 2 ** 80
        x = n
        wit = True
        for i in range(1, k + 1):
            x = step(Q, tab, x)
            if i < k and x < n:
                wit = False
                break
        wit &= x < n
        msg += f", own witness ({M.bit_length()}-bit modulus) T^i(n)>=n for i<k*, T^k*(n)<n: {wit}"
        cond &= wit
    claim(f"[Q2] {msg} == {k} ({time.time()-t0:.0f}s)", cond)

# ================================================================== [Q3]
CONV = [1, 1, 2, 5, 12, 41, 53, 306, 665, 15601]   # denominators of log2(3) convergents
rng = random.Random(77)
t0 = time.time()
cnt = viol = 0
tries = 0
while cnt < 150 and tries < 20000:
    tries += 1
    m = rng.randint(1, 4)
    Q = 2 ** m
    tab = []
    for r in range(Q):
        u = rng.choice([1, 3])
        w = 2 ** rng.randint(0, m)
        v0 = (-u * r) % w
        v = v0 + w * rng.randint(-1, 2)
        tab.append((u, v, w))
    if not check_hyp(Q, tab):
        continue
    # translation cycles with negative drift violate (P) already; translation vertices allowed
    if not exact_potential(Q, tab, iters=2000):
        continue
    Lam, _ = exact_Lambda(Q, tab, limit=10 ** 5)
    ks = Lam + 1
    kk = max(i for i in range(len(CONV) - 1) if CONV[i] <= Q)
    qk, qk1 = CONV[kk], CONV[kk + 1]
    bound = Q + (Q - 1) * Q * math.log(3) / math.log(2) * (qk + qk1)
    cnt += 1
    if ks > bound:
        viol += 1
claim(f"[Q3] A3 bound vs generic exact k* on {cnt} random CERT tables (m=1..4, u in {{1,3}}, "
      f"translations allowed): {viol} violations ({time.time()-t0:.0f}s)", cnt >= 100 and viol == 0)


# ================================================================== [Q4] B1 instances
def mod2k(fr, k):
    """residue of a 2-adic rational (odd denominator) mod 2^k."""
    M = 1 << k
    assert fr.denominator % 2 == 1
    return fr.numerator * pow(fr.denominator, -1, M) % M


def acc3x1_branch(z):
    """accelerated 3x+1 on a 2-adic rational: returns (next, letter)."""
    if mod2k(z, 1) == 1:
        return (3 * z + 1) / 2, 1
    return z / 2, 0


def periodic_point(word, branch_maps):
    """fixed point of the composition of affine maps listed by word letters."""
    A, B = Fraction(1), Fraction(0)
    for c in word:
        a, b = branch_maps[c]
        A, B = a * A, a * B + b
    return B / (1 - A), A


def tarjan(nodes_n, S):
    index = {}
    low = {}
    on = set()
    st = []
    comp = [None] * nodes_n
    cid = 0
    counter = [0]
    sys.setrecursionlimit(100000)
    for v0 in range(nodes_n):
        if v0 in index:
            continue
        stack = [(v0, iter(S[v0]))]
        index[v0] = low[v0] = counter[0]; counter[0] += 1
        st.append(v0); on.add(v0)
        while stack:
            v, it = stack[-1]
            adv = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter[0]; counter[0] += 1
                    st.append(w); on.add(w)
                    stack.append((w, iter(S[w])))
                    adv = True
                    break
                elif w in on:
                    low[v] = min(low[v], index[w])
            if adv:
                continue
            stack.pop()
            if stack:
                low[stack[-1][0]] = min(low[stack[-1][0]], low[v])
            if low[v] == index[v]:
                while True:
                    w = st.pop(); on.discard(w)
                    comp[w] = cid
                    if w == v:
                        break
                cid += 1
    return comp


def typec_at(Q, tab, orbitA):
    """orbitA: residues mod Q of the periodic orbit of y_A (a closed walk).  Checks that
    this closed walk has multiplier > 1 and lies in an SCC with more internal edges than
    nodes (so the SCC is not a single simple cycle): type (c)."""
    S = [succ(Q, tab, r) for r in range(Q)]
    for i in range(len(orbitA)):
        assert orbitA[(i + 1) % len(orbitA)] in S[orbitA[i]]
    mult = Fraction(1)
    for r in orbitA:
        mult *= Fraction(tab[r][0], tab[r][2])
    comp = tarjan(Q, S)
    c = comp[orbitA[0]]
    assert all(comp[r] == c for r in orbitA)
    nodes = [r for r in range(Q) if comp[r] == c]
    edges = sum(1 for r in nodes for s in S[r] if comp[s] == c)
    return mult > 1 and edges > len(nodes), mult, len(nodes)


def acc_cut_table(j, K):
    """accelerated 3x+1 with reset on class -1 mod 2^j, presented at modulus 2^K (K >= j)."""
    Q = 2 ** K
    J = 2 ** j
    tab = []
    for r in range(Q):
        if r % J == J - 1:
            tab.append((1, J - (r % J), J))
        elif r % 2:
            tab.append((3, 1, 2))
        else:
            tab.append((1, 0, 2))
    return Q, tab


t0 = time.time()
maps3 = {1: (Fraction(3, 2), Fraction(1, 2)), 0: (Fraction(1, 2), Fraction(0))}
yA, AA = periodic_point([1, 1, 0], maps3)
good = yA == -5 and AA == Fraction(9, 8)
orbits = []
for i in range(0, 13):
    wd = [1, 1, 0] * i + [1, 0]
    y, A = periodic_point(wd, maps3)
    # verify the 2-adic letters along the orbit and avoidance of -1 mod 8
    z = y
    for c in wd:
        z2, let = acc3x1_branch(z)
        good &= let == c and mod2k(z, 3) != 7
        z = z2
    good &= z == y and y != yA
    good &= (mod2k(y, 1 + 3 * i) == mod2k(yA, 1 + 3 * i))   # agree mod 2^{K + #divisions}
    orbits.append(y)
z = yA
for c in [1, 1, 0]:
    good &= mod2k(z, 3) != 7
    z, _ = acc3x1_branch(z)
claim("[Q4] 3x+1 blocks A=(110), B=(10): y_A = -5 (mult 9/8), y_i of A^iB (i<=12) have the stated "
      "2-adic letters, avoid -1 mod 8, differ from y_A and agree with it mod 2^(1+3i)", good)

good = True
info = []
for j in range(3, 11):
    for K in (j, j + 1):
        if K > 11:
            continue
        Q, tab = acc_cut_table(j, K)
        orbA = []
        z = yA
        for c in [1, 1, 0]:
            orbA.append(mod2k(z, K))
            z, _ = acc3x1_branch(z)
        tc, mult, sz = typec_at(Q, tab, orbA)
        good &= tc
        info.append((j, K, sz))
claim(f"[Q4] 3x+1 cut at j = 3..10 (presented at 2^j and 2^(j+1)): the -5 closed walk (mult 9/8) "
      f"lies in an SCC that is not a single cycle -> type (c)", good)

good = True
for j in (1, 2):
    Q, tab = acc_cut_table(j, max(j, 1))
    if j == 1:
        Q, tab = 2, [(1, 0, 2), (1, 1, 2)]   # odd n -> (n+1)/2
    pot = exact_potential(Q, tab)
    cyc = cycles_bruteforce(Q, tab, 10 ** 5)
    good &= pot and cyc == {(1, 2)} if j == 2 else pot and cyc == {(1,)}
claim("[Q4] 3x+1 cut j=2 (n=3 mod 4 -> (n+1)/4) is CERT (exact potential), cycles n<=1e5 = {(1 2)}; "
      "j=1 CERT with cycle (1)", good)
# note: for j = 1 the cut map n odd -> (n+1)/2 has the fixed point 1 (not the cycle (1 2)).

# adversarial random replacements on U_J for 3x+1, J = 3, 4, K' up to J+2
rng = random.Random(9)
good = True
for trial in range(40):
    J = rng.choice([3, 4])
    Kp = J + rng.randint(0, 2)
    Q = 2 ** Kp
    tab = []
    for r in range(Q):
        if r % (2 ** J) == 2 ** J - 1:
            u = rng.choice([1, 3, 5, 7, 9, 11])
            e = rng.randint(1, Kp)
            w = 2 ** e
            v = (-u * r) % w + w * rng.randint(0, 2)
            tab.append((u, v, w))
        elif r % 2:
            tab.append((3, 1, 2))
        else:
            tab.append((1, 0, 2))
    orbA = []
    z = yA
    for c in [1, 1, 0]:
        orbA.append(mod2k(z, Kp))
        z, _ = acc3x1_branch(z)
    tc, mult, sz = typec_at(Q, tab, orbA)
    good &= tc
claim("[Q4] adversarial: 40 random dividing replacements of 3x+1 on U_J (J=3,4, K'<=J+2) are all type (c)", good)

# K7: z even -> z/2, z=3(4) -> (3z+1)/2, z=1(4) -> (z-1)/4
mapsK = {'A': (Fraction(3, 2), Fraction(1, 2)), 'Q': (Fraction(1, 4), Fraction(-1, 4)),
         'H': (Fraction(1, 2), Fraction(0))}


def k7_letter(z):
    r = mod2k(z, 2)
    return 'H' if r % 2 == 0 else ('A' if r == 3 else 'Q')


yK, AK = periodic_point(list("AAAAQ"), mapsK)
good = yK == Fraction(-49, 17) and AK == Fraction(81, 64)
for i in range(0, 10):
    wd = list("AAAAQ") * i + list("AAAAQH")
    y, A = periodic_point(wd, mapsK)
    z = y
    for c in wd:
        good &= k7_letter(z) == c and mod2k(z, 6) != 63
        a, b = mapsK[c]
        z = a * z + b
    good &= z == y and y != yK and mod2k(y, 2 + 6 * i) == mod2k(yK, 2 + 6 * i)
z = yK
orbK = []
for c in "AAAAQ":
    good &= k7_letter(z) == c and mod2k(z, 6) != 63
    a, b = mapsK[c]
    z = a * z + b
claim("[Q4] K7 blocks A^4Q, A^4QH: y_A = -49/17 (mult 81/64); y_i (i<=9) follow the words 2-adically, "
      "avoid z = -1 mod 64, differ from y_A and agree mod 2^(2+6i)", good)


def k7_cut_table(j):
    Q = 2 ** j
    tab = []
    for r in range(Q):
        if r == Q - 1:
            tab.append((1, 1 - Q, Q))           # (z+1)/2^j - 1
        elif r % 2 == 0:
            tab.append((1, 0, 2))
        elif r % 4 == 3:
            tab.append((3, 1, 2))
        else:
            tab.append((1, -1, 4))
    return Q, tab


good = True
for j in range(6, 12):
    Q, tab = k7_cut_table(j)
    orb = []
    z = yK
    for c in "AAAAQ":
        orb.append(mod2k(z, j))
        a, b = mapsK[c]
        z = a * z + b
    tc, mult, sz = typec_at(Q, tab, orb)
    good &= tc
claim("[Q4] K7 cut at j = 6..11: the -49/17 closed walk lies in an SCC that is not a single cycle -> type (c)", good)

good = True
for j in range(2, 6):
    Q, tab = k7_cut_table(j)
    pot = exact_potential(Q, tab)
    # brute force over z >= 0 (n = z + 1 >= 1): orbits must reach 0
    reach = True
    for z0 in range(0, 200001):
        z = z0
        for _ in range(10000):
            if z == 0:
                break
            u, v, w = tab[z % Q]
            z = (u * z + v) // w
        reach &= z == 0
    good &= pot and reach
claim("[Q4] K7 cut at j = 2..5: CERT (exact potential) and every z in [0, 2e5] reaches the fixed point 0", good)
print(f"     ({time.time()-t0:.0f}s)")


# ================================================================== [Q5] window part
def parity_ones(n, N):
    k = 0
    for _ in range(N):
        if n & 1:
            k += 1
            n = (3 * n + 1) >> 1
        else:
            n >>= 1
    return k


t0 = time.time()
good = True
for N in range(1, 17):
    cnt = sum(1 for r in range(2 ** N) if 8 * parity_ones(r, N) > 5 * N)
    vecs = set()
    for r in range(2 ** N):
        n, v = r, 0
        for i in range(N):
            v = 2 * v + (n & 1)
            n = (3 * n + 1) >> 1 if n & 1 else n >> 1
        vecs.add(v)
    good &= cnt == sum(math.comb(N, k) for k in range(N + 1) if 8 * k > 5 * N) and len(vecs) == 2 ** N
claim("[Q5] |R_N| = sum_{k>5N/8} C(N,k) and the Terras parity map is a bijection, N = 1..16", good)

gam = Fraction(161, 160)
claim("[Q5] gamma^8 * 243 < 256", gam ** 8 * 243 < 256)


def W2_weights(N):
    Q = 2 ** N
    c = []
    R = set()
    for r in range(Q):
        n = r
        bits = []
        for _ in range(N):
            bits.append(n & 1)
            n = (3 * n + 1) >> 1 if n & 1 else n >> 1
        if 8 * sum(bits) > 5 * N:
            R.add(r)
            c.append(Fraction(1, 2))
            continue
        best = Fraction(1)
        x = Fraction(1)
        for s in range(1, N):
            x *= gam * (Fraction(3, 2) if bits[s - 1] else Fraction(1, 2))
            best = max(best, x)
        c.append(best)
    return c, R


def TN_table(N, R):
    Q = 2 ** N
    tab = []
    for r in range(Q):
        if r in R:
            tab.append((1, (Q - r) % Q, Q))
        elif r & 1:
            tab.append((3, 1, 2))
        else:
            tab.append((1, 0, 2))
    return Q, tab


good = True
lyap = True
for N in range(4, 13):
    c, R = W2_weights(N)
    Q, tab = TN_table(N, R)
    cmax = max(c)
    good &= check_hyp(Q, tab)
    good &= cmax <= (3 * gam / 2) ** ((5 * N) // 8) <= 2 ** (N - 2)
    for r in range(Q):
        u, v, w = tab[r]
        if r in R:
            good &= cmax * u < c[r] * w
        else:
            for s in succ(Q, tab, r):
                good &= c[s] * u < c[r] * w
    BN = math.ceil(Fraction(161, 2) * (3 * gam / 2) ** ((5 * N) // 8))
    for n in range(BN + 1, BN + 4 * Q):
        Tn = step(Q, tab, n)
        lyap &= c[Tn % Q] * Tn < c[n % Q] * n
claim("[Q5] W2: my weights satisfy c(s)u < c(r)w on every edge of T_N, c_max <= (3g/2)^floor(5N/8) <= 2^(N-2), N = 4..12", good)
claim("[Q5] W2: V(T_N n) < V(n) for every n in (B_N, B_N + 4*2^N], N = 4..12", lyap)

# W3: cycle lists of T_N, N = 4..26, all n <= max(B_N, 30000)
good = True
for N in range(4, 27):
    BN = math.ceil(Fraction(161, 2) * (3 * gam / 2) ** ((5 * N) // 8))
    X = max(BN, 30000)
    done = set()
    cyc = set()
    for n0 in range(1, X + 1):
        if n0 in done:
            continue
        path = {}
        seq = []
        n = n0
        while n not in done and n not in path:
            path[n] = len(seq)
            seq.append(n)
            if 8 * parity_ones(n, N) > 5 * N:
                n = (n >> N) + 1
            elif n & 1:
                n = (3 * n + 1) >> 1
            else:
                n >>= 1
        if n in path:
            cyc.add(tuple(sorted(seq[path[n]:])))
        done.update(seq)
    good &= cyc == {(1, 2)}
claim("[Q5] W3: T_N has the single cycle (1 2) from all n <= max(B_N, 30000), N = 4..26", good)

# W1' for the plain map T0: window = N halvings; R_N identical; T0_N CERT (exact potential)
good = True
for N in range(4, 10):
    Q = 2 ** N
    Racc = {r for r in range(Q) if 8 * parity_ones(r, N) > 5 * N}
    R0 = set()
    for r in range(Q):
        n, D, U = r, 0, 1
        while D <= N - 1:
            if n & 1:
                n, U = 3 * n + 1, U * 3
            else:
                n, D = n >> 1, D + 1
        k = round(math.log(U, 3))
        assert 3 ** k == U and D == N
        if 8 * k > 5 * N:
            R0.add(r)
    tab = []
    for r in range(Q):
        if r in R0:
            tab.append((1, (Q - r) % Q, Q))
        elif r & 1:
            tab.append((3, 1, 1))
        else:
            tab.append((1, 0, 2))
    good &= R0 == Racc and check_hyp(Q, tab) and exact_potential(Q, tab)
claim("[Q5] W1': plain map n/2, 3n+1: window set = accelerated R_N, and T0_N (reset on R_N, modulus 2^N) "
      "is CERT by an exact potential, N = 4..9", good)

# W1 for K7 (p = 2, m = 2, e_max = 2, delta = 1/5): window approximants CERT, K = 3..9.
# Residue graphs do not depend on the reset's additive constant, so the z-coordinate
# reset z -> floor(z/2^K) gives the same graph as the prover's n-coordinate reset.
good = True
dens = []
for K in range(3, 10):
    Q = 2 ** K
    R = set()
    for r in range(Q):
        z, D, U = r, 0, 1
        while D <= K - 2:
            if z % 2 == 0:
                z, D = z // 2, D + 1
            elif z % 4 == 3:
                z, D, U = (3 * z + 1) // 2, D + 1, U * 3
            else:
                z, D = (z - 1) // 4, D + 2
        assert K - 2 < D <= K
        if U ** 5 > 2 ** (4 * D):
            R.add(r)
    tab = []
    for r in range(Q):
        if r in R:
            tab.append((1, -r, Q))
        elif r % 2 == 0:
            tab.append((1, 0, 2))
        elif r % 4 == 3:
            tab.append((3, 1, 2))
        else:
            tab.append((1, -1, 4))
    good &= exact_potential(Q, tab)
    dens.append(Fraction(len(R), Q))
claim(f"[Q5] W1 for K7 (delta = 1/5): window approximants CERT by exact potential, K = 3..9; "
      f"densities {[str(d) for d in dens]}",
      good and dens == [Fraction(1, 8), Fraction(1, 8), Fraction(3, 32), Fraction(9, 64),
                        Fraction(11, 128), Fraction(25, 256), Fraction(35, 512)])

# W4 finite facts
good = Fraction(94, 31) ** 5 >= 256 > Fraction(97, 32) ** 5
for n in range(1, 32):
    x = n
    while x != 1:
        x = (3 * x + 1) // 2 if x & 1 else x // 2
good &= True
prod = Fraction(1)
for z in (1,):
    prod *= 3 + Fraction(1, z)
good &= prod == 2 ** 2          # cycle (1 2): one odd element, L = 2
claim("[Q5] W4: (3+1/31)^5 >= 256 > (3+1/32)^5; all n <= 31 reach 1; cycle identity on (1 2)", good)
print(f"     ({time.time()-t0:.0f}s)")


# ================================================================== [Q6] entropy exponent as printed
def tail(N):
    k0 = (5 * N) // 8 + 1
    c = math.comb(N, k0)
    s = 0
    k = k0
    while k <= N:
        s += c
        c = c * (N - k) // (k + 1)
        k += 1
    return s


Hq = -(5 / 8) * math.log2(5 / 8) - (3 / 8) * math.log2(3 / 8)
print(f"     H(5/8) = {Hq:.6f}")
N = 20000
s = tail(N)
e954 = s > 2 ** (954 * N // 1000)
print(f"INFO [Q6] N = {N}: sum_(k>5N/8) C(N,k) > 2^(0.954 N) exactly: {e954} "
      f"(log2 sum = {s.bit_length()-1}..{s.bit_length()}, 0.954N = {954*N//1000})")
small_ok = all(tail(N) <= 2 ** (9544 * N // 10000) for N in range(10, 2001, 10))
claim("[Q6] the printed bounds hold for N <= 2000 (multiples of 10)", small_ok)
claim("[Q6] README's 2^(0.954N) is FALSE as an all-N bound (fails at N = 20000)", e954)
t0 = time.time()
N = 400000
s = tail(N)
claim(f"[Q6] window.md's 2^(0.9544N) is FALSE as an all-N bound (exact at N = 400000: "
      f"bitlen(sum) = {s.bit_length()} > 0.9544N = {9544 * N // 10000}; {time.time()-t0:.0f}s); "
      f"the correct bound is 2^(N H(5/8)), H(5/8) = 0.95443...", s > 2 ** (9544 * N // 10000))
claim("[Q6] the Chernoff form sum <= 2^(N H(5/8)) holds at N = 400000 (float exponent, margin > 1 bit)",
      s.bit_length() < N * Hq - 1)

# 5x+1 sanity (would the window reduction 'prove' something false?): the true cycle
# 13 -> 33 -> 83 -> 208 -> 104 -> 52 -> 26 has odd density 3/7 > 2/5, so windows of length 7k
# along it exceed the threshold 2N/5: the (S_C)-analogue is false for n = 13, consistent with
# W3/W4 (which only conclude something for orbits that avoid R_N).
cyc5 = [13, 33, 83, 208, 104, 52, 26]
good = True
for k in range(1, 30):
    N = 7 * k
    for st in range(7):
        odd = sum(1 for i in range(N) if cyc5[(st + i) % 7] & 1)
        good &= 5 * odd > 2 * N
x = 13
for c in range(7):
    good &= x == cyc5[c]
    x = (5 * x + 1) // 2 if x & 1 else x // 2
good &= x == 13
claim("[Q6] 5x+1 control: every 7k-window of the 13-cycle has > 2N/5 odd steps, so no W4-type "
      "conclusion applies to it", good)

# ================================================================== [Q7] negative controls
Q, tab = acc_cut_table(3, 3)
claim("[Q7] negative control: certifier refuses 3x+1 cut at j=3 (type (c))", not exact_potential(Q, tab))
claim("[Q7] negative control: nonneg_cycle finds an expanding walk there",
      nonneg_cycle(Q, tab) is not None)
Q, tab, ell, ch = build_D(6, christoffel(5, 8), 4, 11)
Lam, _ = exact_Lambda(Q, tab)
claim("[Q7] negative control: Lambda+1 for the m=6 record is not 790 or 792", Lam + 1 not in (790, 792))

print("ALL PASS" if ok else "SOME CHECK FAILED")
sys.exit(0 if ok else 1)
