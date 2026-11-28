"""Theorem E: counting avoiders through the shortcut avoider graph.

T = T_{a,b}: n/2 (even), (a n + b)/2 (odd), a, b odd.  For a set A of
residues mod 2^k let M be the 0/1 adjacency matrix of G_k^A(T) (both lifts
of every step, nodes in A deleted).  Theorem E: for X >= 2^k,

  #{1 <= n <= X : T^i(n) mod 2^k not in A for all i >= 0}
        <= 2 * (sum v / min v) * lam^(L-k),   L = floor(log2 X),

for every rational lam > 0 and positive rational vector v with M v <= lam v.
Hence the count is O(X^theta) with theta = log2(lam).  For a set A of odd
residues the T-orbit meets A iff the C_{a,b}-orbit does.

check_all() builds (lam, v) by floating power iteration, rounds them to
rationals and verifies M v <= lam v exactly.  It also reproduces the two
known exponents log2(plastic) = 0.40569 (A = {5,7} mod 8, CLS-056) and
log2(tribonacci) = 0.87915 (A = {7} mod 8, CLS-066) for 3x+1.
"""
import sys, os, json, math
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify as V


def adjacency(a, b, k, A):
    br = [(1, 0, 1), (a, b, 1)]
    adj = V.brute_graph(br, 1, k, set(A), k)
    return adj


def walks_count(adj, length):
    cnt = {u: 1 for u in adj}
    for _ in range(length):
        cnt = {u: sum(cnt[v] for v in adj[u]) for u in adj}
    return sum(cnt.values())


def perron_certificate(adj, delta=1e-6):
    """lam = rho*(1+delta) rounded up to a rational, v = (I - M/lam)^-1 1
    (float solve, rounded); then M v = lam (v - 1) <= lam v holds with slack
    lam per coordinate, which absorbs the rounding.  Verified exactly by the
    caller."""
    import numpy as np
    nodes = sorted(adj)
    if not nodes:
        return Fraction(0), {}
    ix = {u: i for i, u in enumerate(nodes)}
    n = len(nodes)
    M = np.zeros((n, n))
    for u in nodes:
        for w in adj[u]:
            M[ix[u], ix[w]] += 1
    rho = float(max(abs(np.linalg.eigvals(M))))
    while True:
        lam = Fraction(int(max(rho, 1e-9) * (1 + delta) * 10 ** 9) + 1, 10 ** 9)
        vf = np.linalg.solve(np.eye(n) - M / float(lam), np.ones(n))
        if min(vf) > 0:
            v = {u: Fraction(int(vf[ix[u]] * 10 ** 6) + 1, 10 ** 6) for u in nodes}
            if all(sum(v[w] for w in adj[u]) <= lam * v[u] for u in nodes):
                return lam, v
        delta *= 4


def theta(lam):
    return math.log2(lam) if lam > 0 else float("-inf")


def check_one(a, b, k, A, expect_theta=None, tol=1e-4):
    adj = adjacency(a, b, k, A)
    lam, v = perron_certificate(adj)
    nodes = sorted(adj)
    for u in nodes:
        assert sum(v[w] for w in adj[u]) <= lam * v[u]
    # exact walk-count bound for small L (sanity of the inequality)
    C = sum(v.values()) / min(v.values()) if v else 0
    for Lw in range(0, 12):
        assert walks_count(adj, Lw) <= C * lam ** Lw
    # brute-force class count = walk count (the bijection in the proof)
    for Lb in range(k, k + 8):
        M = 1 << Lb
        good = 0
        for n in range(M):
            x = n; ok = True
            for i in range(Lb - k + 1):
                if x % (1 << k) in A:
                    ok = False; break
                x = x // 2 if x % 2 == 0 else (a * x + b) // 2
            good += ok
        assert good == walks_count(adj, Lb - k), (a, b, k, A, Lb)
    th = theta(lam)
    if expect_theta is not None:
        assert abs(th - expect_theta) < tol, (th, expect_theta)
    return th


def check_all(verbose=False):
    plastic = 1.324717957244746
    trib = 1.839286755214161
    check_one(3, 1, 3, {5, 7}, math.log2(plastic))
    check_one(3, 1, 3, {7}, math.log2(trib))
    out = {}
    for fn, (a, k) in [("census_C3_k5_odd.json", (3, 5)), ("census_C5_k5_odd.json", (5, 5)),
                       ("census_C7_k5_odd.json", (7, 5))]:
        d = json.load(open(os.path.join(HERE, "results", fn)))
        ths = []
        for Hs in d["maximal_H"]:
            th = check_one(a, 1, k, set(Hs))
            ths.append((round(th, 5), Hs))
        ths.sort()
        out[fn] = ths
        if verbose:
            print(fn, "frontier exponents: min", ths[0], "max", ths[-1])
    return out


if __name__ == "__main__":
    out = check_all(verbose=True)
    json.dump(out, open(os.path.join(HERE, "results", "entropy_frontier.json"), "w"), indent=1)
