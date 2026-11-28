"""Independent verifier for Theorem-H proof objects (does not import tblib).

A proof object (JSON) has: p, m, K, table [[u, v, w], ...] (indexed by n mod p^m),
comps: list of {id, kind, nodes, level, ...}, and cycles: list of cycles (each a list of
integers starting at its minimum).  Fractions are strings "a/b".

What is checked, exactly (ints and Fractions only):
 H0  table hypotheses: u >= 1, p does not divide u, w = p^e, w | u n + v on each class,
     T maps Z>0 into Z>0.
 H1  the given components partition the nodes of G_K; each is strongly connected inside
     itself; every edge between different components strictly lowers 'level'.
     (So they are exactly the SCCs, and an orbit's residue walk is eventually inside one.)
 H2  'trivial': one node without self-loop.
 H3  simple-cycle components (kind a or b with 'cycle'): each node has exactly one internal
     out-edge, these form the stated cycle, the cycle contains a division, and the stated
     rational points x_0..x_{l-1} satisfy (u x_i + v)/w = x_{i+1}, x_i = node_i (mod p^K).
     Then T(n) - x_{i+1} = (u/w)(n - x_i) for n in the class, so the counter
     phi(n) = l * (v_p(n - x_i) + E_i) - i  (E_i = divisions before position i)
     drops by >= 1 at every step inside the component and is >= -l: only x_0's orbit stays
     forever.  The verifier also tests the counter descent on sample integers.
 H4  contracting components: theta < 1, c > 0 with c(s) u/w <= theta c(r) on every internal
     edge; beta, Vmax recomputed; all n <= Vmax / min c with c(n mod p^K) n <= Vmax followed
     to their cycles.
 H5  the cycle list equals: integer periodic points of simple components (positive ones)
     plus the cycles reached in H4; each listed cycle is a genuine T-cycle.
Exit status 0 iff every check passes.  Usage: python verify_H.py proof.json [...]
"""
import sys, json
from fractions import Fraction


def F(x):
    return Fraction(x) if not isinstance(x, str) else Fraction(x)


def vp(x, p):
    """p-adic valuation of a nonzero rational with denominator prime to p"""
    a = x.numerator
    assert x.denominator % p != 0 and a != 0
    e = 0
    while a % p == 0:
        a //= p
        e += 1
    return e


def verify(P, quiet=False):
    p, m, K = P["p"], P["m"], P["K"]
    tab = [tuple(t) for t in P["table"]]
    Q, PK = p ** m, p ** K
    assert len(tab) == Q
    exps = []
    for r, (u, v, w) in enumerate(tab):
        assert u >= 1 and u % p != 0
        e, ww = 0, w
        while ww % p == 0:
            ww //= p
            e += 1
        assert ww == 1 and e <= K
        assert (u * r + v) % w == 0 and (u * Q) % w == 0
        n0 = r if r else Q
        assert u * n0 + v >= w
        exps.append(e)

    def T(n):
        u, v, w = tab[n % Q]
        assert (u * n + v) % w == 0
        return (u * n + v) // w

    # G_K
    E = []
    for r in range(PK):
        u, v, w = tab[r % Q]
        step = PK // w
        base = ((u * r + v) // w) % step
        E.append([base + i * step for i in range(w)])
    comps = P["comps"]
    owner = {}
    for c in comps:
        for x in c["nodes"]:
            assert x not in owner, "node in two components"
            owner[x] = c["id"]
    assert sorted(owner) == list(range(PK)), "components do not partition the nodes"
    byid = {c["id"]: c for c in comps}
    # H1
    for r in range(PK):
        for s in E[r]:
            if owner[s] != owner[r]:
                assert byid[owner[s]]["level"] < byid[owner[r]]["level"], "level does not drop"
    for c in comps:
        ns = set(c["nodes"])
        a = c["nodes"][0]
        fw, st = {a}, [a]
        while st:
            x = st.pop()
            for y in E[x]:
                if y in ns and y not in fw:
                    fw.add(y)
                    st.append(y)
        assert fw == ns, "component not strongly connected (forward)"
        rev = {x: [] for x in ns}
        for x in ns:
            for y in E[x]:
                if y in ns:
                    rev[y].append(x)
        bw, st = {a}, [a]
        while st:
            x = st.pop()
            for y in rev[x]:
                if y not in bw:
                    bw.add(y)
                    st.append(y)
        assert bw == ns, "component not strongly connected (backward)"
    cycles = {}
    import random
    rnd = random.Random(1)
    for c in comps:
        ns = set(c["nodes"])
        internal = [(x, y) for x in ns for y in E[x] if y in ns]
        if c["kind"] == "trivial":
            assert len(ns) == 1 and not internal
            continue
        if "cycle" in c:
            cyc = c["cycle"]
            assert sorted(cyc) == sorted(ns) and len(internal) == len(cyc)
            L = len(cyc)
            for i in range(L):
                assert (cyc[i], cyc[(i + 1) % L]) in internal
            assert sum(exps[x % Q] for x in cyc) >= 1, "division-free cycle"
            xs = [F(x) for x in c["xstar"]]
            assert len(xs) == L
            A = Fraction(1)
            for i in range(L):
                u, v, w = tab[cyc[i] % Q]
                A *= Fraction(u, w)
                x = xs[i]
                assert x.denominator % p != 0
                assert (x.numerator * pow(x.denominator, -1, PK) - cyc[i]) % PK == 0
                assert (u * x + v) / w == xs[(i + 1) % L]
            if c["kind"] == "b":
                assert A > 1
            else:
                assert A < 1
            # counter phi: check strict descent on sample integers in the classes
            Ei = [0] * L
            for i in range(1, L):
                Ei[i] = Ei[i - 1] + exps[cyc[i - 1] % Q]

            def phi(n, i):
                return L * (vp(Fraction(n) - xs[i], p) + Ei[i]) - i
            for _ in range(50):
                i = rnd.randrange(L)
                n = cyc[i] + PK * rnd.randrange(1, 10 ** 12)
                if Fraction(n) == xs[i]:
                    continue
                ph = phi(n, i)
                assert ph >= -L
                j = i
                for _ in range(10 * L * 64):
                    n2 = T(n)
                    j2 = (j + 1) % L
                    if n2 % PK != cyc[j2]:
                        break
                    ph2 = phi(n2, j2)
                    assert ph2 <= ph - 1, "counter does not drop"
                    n, j, ph = n2, j2, ph2
                else:
                    raise AssertionError("sample followed the cycle too long")
            if xs[0].denominator == 1 and xs[0] > 0:
                y = int(xs[0])
                orb = [y]
                z = T(y)
                while z != y:
                    orb.append(z)
                    z = T(z)
                k = orb.index(min(orb))
                orb = orb[k:] + orb[:k]
                cycles[orb[0]] = orb
            continue
        # contracting component with weights
        assert c["kind"] == "a"
        th = F(c["theta"])
        assert 0 < th < 1
        w_ = {int(k): F(v) for k, v in c["c"].items()}
        assert set(w_) == ns and all(x > 0 for x in w_.values())
        beta = Fraction(0)
        for x, y in internal:
            u, v, w = tab[x % Q]
            assert w_[y] * Fraction(u, w) <= th * w_[x], "weight inequality fails"
            beta = max(beta, w_[y] * Fraction(max(v, 0), w))
        Vmax = beta / (1 - th)
        nmax = int(Vmax / min(w_.values()))
        assert nmax <= 2 * 10 ** 7
        for n in range(1, nmax + 1):
            r = n % PK
            if r in ns and w_[r] * n <= Vmax:
                seen, y = set(), n
                while y not in seen:
                    seen.add(y)
                    y = T(y)
                orb = [y]
                z = T(y)
                while z != y:
                    orb.append(z)
                    z = T(z)
                k = orb.index(min(orb))
                orb = orb[k:] + orb[:k]
                cycles[orb[0]] = orb
    got = [cycles[k] for k in sorted(cycles)]
    claimed = P["cycles"]
    assert got == claimed, ("cycle list mismatch", got[:5], claimed[:5])
    for cyc in claimed:
        for i, x in enumerate(cyc):
            assert x > 0 and T(x) == cyc[(i + 1) % len(cyc)]
    if not quiet:
        print("VERIFIED", P.get("name", ""), "cycles:", [c[0] for c in claimed])
    return True


if __name__ == "__main__":
    ok = True
    for fn in sys.argv[1:]:
        data = json.load(open(fn))
        objs = data if isinstance(data, list) else [data]
        for P in objs:
            try:
                verify(P, quiet=len(objs) > 20)
            except AssertionError as ex:
                print("FAILED", P.get("name", ""), ex)
                ok = False
        print(fn, "objects:", len(objs), "OK" if ok else "FAIL")
    sys.exit(0 if ok else 1)
