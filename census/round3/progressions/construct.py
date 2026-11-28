"""Constructive form of the proof of Theorem A (theorem_A_sufficiency.md, Sections 3-6).

construct(S, info, y, x, N) returns (n, data) with n = x (mod N) and an explicit number of
steps m such that T^m(n) is a forward iterate of y; every step is replayed and asserted by
verify().  `info` is the precomputed data of certify (delta, invariant, IA game).
"""

from math import gcd
from collections import deque

import plib
from plib import vp, lcm


def prepare(S):
    """Precompute everything the construction needs for the system S."""
    loops = plib.fundamental_loops(S)
    trans = plib.translations(S, loops)
    delta = plib.delta_from_translations(S, trans)
    cls = plib.groupoid_classes(S, delta)
    dstar, state_free, rep = plib.minimal_invariant(S, delta, cls)
    info = dict(delta=delta, dstar=dstar, rep=rep)
    if S.U:
        info["ia"] = plib.ia_game(S)
    return info


def g(S, info, n):
    return info["rep"][(n % S.S, n % info["dstar"])]


def entry_point(S, info, y, limit=10 ** 5):
    """A forward iterate y0 of y that is enterable (Lemma 5 of the theorem file)."""
    if not S.U:
        return y, 0
    L2, enter = info["ia"]["L2"], info["ia"]["enter"]
    x = y
    for k in range(limit):
        if x % L2 in enter:
            return x, k
        x = S.T(x)
    raise AssertionError("no enterable forward iterate found")


def groupoid_word(S, s0, z0, s1, z1, Q):
    """BFS word of moves from (s0, z0) to (s1, z1) on states x Z/Q."""
    mv = S.moves()
    start, goal = (s0, z0 % Q), (s1, z1 % Q)
    prev = {start: None}
    dq = deque([start])
    while dq:
        nd = dq.popleft()
        if nd == goal:
            w = []
            while prev[nd] is not None:
                nd, i = prev[nd]
                w.append(i)
            return w[::-1]
        (a, x) = nd
        for i, m in enumerate(mv):
            if m["src"] != a:
                continue
            y = (m["dst"], ((S.p * x - m["v"]) * pow(m["u"], -1, Q)) % Q if Q > 1 else 0)
            if y not in prev:
                prev[y] = (nd, i)
                dq.append(y)
    return None


def construct(S, info, y, x, N, bump=0):
    p, kappa = S.p, S.kappa
    mv = S.moves()
    data = {}
    # Step 0: entry point
    y0, k0 = entry_point(S, info, y)
    data["y0"], data["k0"] = y0, k0
    # Step 1: decompose N, the lift parameters
    e = vp(N, p)
    NU = 1
    for l in S.U:
        NU *= l ** vp(N, l)
    Q0 = N // (p ** e * NU)
    Q = lcm(Q0, info["delta"])
    t = max(0, e - kappa + 1)
    c, a = x, 1
    for _ in range(t):
        a *= S.table[c % S.P][0]
        c = S.T(c)
    data.update(t=t, c=c, a=a, Q=Q)
    prec = {l: vp(a * NU, l) for l in S.U}
    oQ = plib.mult_order(p, Q) if Q > 1 else 1
    h0 = kappa - 1
    # Step 2: initial ball and ball growing (Section 4)
    ball_words = []
    if S.U:
        ia = info["ia"]
        L2, live = ia["L2"], ia["live"]
        O = oQ
        for l in S.U:
            O = lcm(O, plib.mult_order(p, l))
            if l == 2:
                O = lcm(O, 2)
        # choose h0 >= kappa-1 with (0, p^h0 y0 mod L2) live
        h = kappa - 1
        while (0, pow(p, h, L2) * y0 % L2) not in live:
            h += 1
            assert h < kappa + 4 * L2 * O + 10
        h0 = h
        J = {l: vp(pow(p, O) - 1, l) for l in S.U}
        # ball centre (as integer) and radius exponents (relative to l-adic valuation of y0)
        centre = pow(p, h0) * y0
        jr = {l: J[l] + vp(y0, l) for l in S.U}
        state = 0
        rho = centre % Q
        steps = 0
        while any(jr[l] > 0 for l in S.U):
            steps += 1
            assert steps < 10 ** 4
            # if the ball is wide at some l, move the centre to a live residue mod L2
            if any(jr[l] < vp(L2, l) for l in S.U):
                M = 1
                for l in S.U:
                    M *= l ** min(jr[l], vp(L2, l))
                base = centre % M
                cand = None
                for kk in range(L2 // M if L2 % M == 0 else L2):
                    zz = (base + M * kk) % L2
                    if (state, zz) in live:
                        cand = zz
                        break
                assert cand is not None, "no live residue in a wide ball"
                # replace centre by a representative = cand (mod L2), = centre (mod l^jr)
                Mfull = 1
                for l in S.U:
                    Mfull *= l ** jr[l]
                r = plib.crt_pair(centre % Mfull, Mfull, cand, L2)
                assert r is not None
                centre = r[0]
            w = plib.find_ia_word(S, state, centre, L2, live)
            assert w is not None, "IA word not found"
            ball_words.append(w)
            for i in w:
                m = mv[i]
                assert m["src"] == state
                xx = p * centre - m["v"]
                for l in S.U:
                    ev = vp(m["u"], l)
                    if jr[l] > 0:
                        jr[l] = max(0, jr[l] - ev)
                # the centre satisfies the U-domain condition (find_ia_word checked it mod L2)
                assert xx % m["u"] == 0, "centre not in domain"
                centre = xx // m["u"]
                state = m["dst"]
                rho = ((p * rho - m["v"]) * pow(m["u"], -1, Q)) % Q if Q > 1 else 0
        data["ball_words"] = ball_words
    else:
        state, rho = 0, (pow(p, h0) * y0) % Q
    # Step 3: groupoid word to the target (state of c, c mod Q)
    gw = groupoid_word(S, state, rho, c % S.S, c, Q)
    assert gw is not None, "target not in the same class"
    data["groupoid_word"] = gw
    # Step 4: backward propagation of the U-adic requirement
    allwords = [i for w in ball_words for i in w] + gw
    req = {}
    for l in S.U:
        res, j = c % l ** prec[l], prec[l]
        for i in reversed(allwords):
            m = mv[i]
            ev = vp(m["u"], l)
            j2 = j + ev
            res = ((m["u"] * res + m["v"]) * pow(p, -1, l ** j2)) % l ** j2
            j = j2
        req[l] = (res, j)
    # Step 5: solve for the dilation exponent h
    hh, mod = h0 % max(oQ, 1), max(oQ, 1)
    if Q > 1:
        hh, mod = plib.crt_pair(h0, oQ, h0, oQ)
    for l, (res, j) in req.items():
        if j == 0:
            continue
        lj = l ** j
        yl = y0 // l ** vp(y0, l)
        vy = vp(y0, l)
        # need p^h * y0 = res (mod l^j)
        if vy >= j:
            assert res % lj == 0
            continue
        assert res % l ** vy == 0 and (res // l ** vy) % l != 0 or vy == 0
        target = (res // l ** vy) * pow(yl, -1, l ** (j - vy)) % l ** (j - vy)
        r = plib.dlog(p, target, l ** (j - vy))
        assert r is not None, "dilation equation unsolvable (ball miscomputed)"
        hl, ol = r
        sol = plib.crt_pair(hh, mod, hl, ol)
        assert sol is not None, "CRT incompatibility in dilation exponent"
        hh, mod = sol
    h = hh
    while h < h0 or h < kappa - 1:
        h += mod
    h += mod * bump
    # Step 6: replay; if some intermediate value is not positive, enlarge h by the period
    # (all congruences are kept, every value grows) -- Lemma 6 of the theorem file.
    for _ in range(200):
        z = pow(p, h) * y0
        okpos = True
        for i in allwords:
            z2 = S.move_int(mv[i], z)
            assert z2 is not None, "move not admissible"
            if z2 <= 0:
                okpos = False
                break
            z = z2
        if okpos and z >= c:
            break
        okpos = False
        h += mod
    assert okpos, "positivity / size not reached"
    data["h"] = h
    y2 = z
    assert (y2 - c) % (a * S.S) == 0, "lift congruence"
    n = x + p ** t * (y2 - c) // a
    data["n"], data["y2"] = n, y2
    data["steps_to_y0"] = t + len(allwords) + h
    return n, data


def verify(S, y, x, N, n, data):
    """Exact replay: n = x (mod N), T^t(n) = y2, and T^(steps) (n) = y0 = T^k0(y)."""
    assert n > 0 and (n - x) % N == 0
    z = n
    for _ in range(data["t"]):
        z = S.T(z)
    assert z == data["y2"]
    z = n
    for _ in range(data["steps_to_y0"]):
        z = S.T(z)
    w = y
    for _ in range(data["k0"]):
        w = S.T(w)
    assert z == w == data["y0"]
    return True
