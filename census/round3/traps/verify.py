"""Independent verifier for SCC certificates and homoclinic witnesses.

Written separately from traps_lib.py: it re-derives the avoider graph by
brute force, and checks a certificate only through the conditions used in
the proof of Theorem 2 (README.md / theory.md):

  (V1) every residue r mod 2^m outside A gets a component id c(r) and a
       rank; for every graph edge u -> v (v outside A):
           rank(c(u)) > rank(c(v))  or  c(u) == c(v);
  (V2) each component is
       - 'functional': every node has <= 1 out-edge inside the component;
         then the lifts of its cycles are computed exactly, and any lift that
         is a positive integer must be a listed cycle; or
       - 'contracting': integers Q, P_a, phi(r) with a^Q < 2^{P_a} (or a=1,
         P=0) and phi(u) >= phi(v) + P_a - Q e + 1 on every internal edge;
  (V3) (a(B+1)+|b|)^Q < 2 (a(B+1))^Q for the B used and every branch with
       b != 0 occurring in a contracting component;
  (V4) every n in [1, B] is simulated until it meets A or closes a cycle,
       and the cycles found are the claimed list.
All arithmetic is exact (int / Fraction).
"""
from fractions import Fraction


def step(br, beta, n):
    a, b, e = br[n % (1 << beta)]
    y = a * n + b
    assert y % (1 << e) == 0
    return y >> e


def rres(x, m):
    x = Fraction(x)
    return (x.numerator * pow(x.denominator, -1, 1 << m)) % (1 << m)


def step_q(br, beta, x):
    a, b, e = br[rres(x, beta)]
    return (a * Fraction(x) + b) / (1 << e)


def brute_graph(br, beta, m, A, k):
    """edges(u) = {T(n) mod 2^m : n = u mod 2^m}, from all n < 2^(m+beta+1)
    (T(n) mod 2^m depends on n mod 2^(m+e), e <= beta)."""
    M = 1 << m
    bad = lambda r: (r % (1 << k)) in A
    adj = {}
    for u in range(M):
        if bad(u):
            continue
        S = set()
        for t in range(1 << (beta + 1)):
            n = u + t * M
            S.add(step(br, beta, n) % M)
        adj[u] = sorted(s for s in S if not bad(s))
    return adj


def check_certificate(br, beta, A, k, m, comps, B, cycles):
    """comps: list of (kind, nodes, data) in Tarjan order (sinks first);
    data for 'contracting' is (Q, P, phi)."""
    adj = brute_graph(br, beta, m, A, k)
    cid = {}
    for idx, (kind, nodes, data) in enumerate(comps):
        for u in nodes:
            assert u not in cid
            cid[u] = idx
    assert set(cid) == set(adj), "partition does not cover the graph"
    # (V1)
    for u, vs in adj.items():
        for v in vs:
            assert cid[u] == cid[v] or cid[u] > cid[v], ("order", u, v)
    found_int_points = []
    maxQ_needed = []
    for idx, (kind, nodes, data) in enumerate(comps):
        ns = set(nodes)
        internal = [(u, v) for u in nodes for v in adj[u] if v in ns]
        if kind in ("trivial", "simple") or not internal:
            outd = {}
            for (u, v) in internal:
                outd[u] = outd.get(u, 0) + 1
            assert all(d <= 1 for d in outd.values()), "not functional"
            # cycles of the functional graph and their exact lifts
            nxt = {u: v for (u, v) in internal}
            seen = set()
            for s in nodes:
                path = []
                y = s
                while y in nxt and y not in seen and y not in path:
                    path.append(y); y = nxt[y]
                if y in path:
                    cyc = path[path.index(y):]
                    num, c, E = 1, 0, 0
                    for r in cyc:
                        a, b, e = br[r % (1 << beta)]
                        num, c, E = a * num, a * c + b * (1 << E), E + e
                    assert E >= 1
                    x = Fraction(c, (1 << E) - num)
                    z = x
                    for r in cyc:
                        assert rres(z, m) == r
                        z = step_q(br, beta, z)
                    assert z == x
                    if x.denominator == 1 and x > 0:
                        found_int_points.append(int(x))
                seen.update(path)
        else:
            assert kind == "contracting"
            Q, P, phi = data
            for a, p in P.items():
                assert (a == 1 and p == 0) or a ** Q < (1 << p)
            for (u, v) in internal:
                a, b, e = br[u % (1 << beta)]
                assert phi[u] >= phi[v] + P[a] - Q * e + 1, ("potential", u, v)
                if b != 0:
                    # (V3)
                    assert (a * (B + 1) + abs(b)) ** Q < 2 * (a * (B + 1)) ** Q
    # (V4)
    Mk = 1 << k
    fate = {}
    cyc_found = set()
    for n0 in range(1, B + 1):
        x = n0
        path = []
        pos = {}
        while True:
            if x in fate:
                f = fate[x]; break
            if x % Mk in A:
                f = "A"; break
            if x in pos:
                cyc = path[pos[x]:]
                i = cyc.index(min(cyc))
                f = tuple(cyc[i:] + cyc[:i])
                cyc_found.add(f)
                break
            pos[x] = len(path); path.append(x)
            x = step(br, beta, x)
        for y in path:
            fate[y] = f
    for p in found_int_points:
        # a positive-integer lift must be a genuine cycle; record it
        x = p; cyc = [p]
        x = step(br, beta, x)
        while x != p:
            cyc.append(x); x = step(br, beta, x)
            assert len(cyc) < 10 ** 6
        i = cyc.index(min(cyc))
        cyc_found.add(tuple(cyc[i:] + cyc[:i]))
    assert sorted(cyc_found) == sorted(tuple(c) for c in cycles), (cyc_found, cycles)
    return True


def check_homoclinic(br, beta, A, k, x, L, z, j):
    """x: periodic point of period L with multiplier > 1 whose orbit avoids
    A; z = x (mod 2^max(k,beta)), z not on the orbit, the first j points of
    the orbit of z avoid A and T^j(z) = x."""
    m0 = max(k, beta)
    orb = [Fraction(x)]
    for _ in range(L - 1):
        orb.append(step_q(br, beta, orb[-1]))
    assert step_q(br, beta, orb[-1]) == orb[0]
    num, E = 1, 0
    for y in orb:
        a, b, e = br[rres(y, beta)]
        num *= a; E += e
        assert rres(y, k) not in A
    assert num > (1 << E)
    assert Fraction(z) not in orb
    assert rres(z, m0) == rres(x, m0)
    y = Fraction(z)
    for _ in range(j):
        assert rres(y, k) not in A
        y = step_q(br, beta, y)
    assert y == orb[0]
    return True
