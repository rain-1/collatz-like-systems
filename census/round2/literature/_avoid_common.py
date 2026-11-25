import math
def survey(step, target, N):
    """Every 1 <= n <= N reaches `target` (a set). Evidence only."""
    for n in range(1, N + 1):
        x, t = n, 0
        while x not in target:
            x = step(x); t += 1
            assert t < 10**5, n
    return True

def graph_edges(M, K):
    """Residue graph of C mod M (M = 2^j >= 8) with classes = K mod 8 deleted.
    Edge weights are log-slopes: 1/2 for halving, 3 for 3n+1."""
    bad = lambda r: (r % 8) in K
    E = []
    for r in range(M):
        if bad(r):
            continue
        if r % 2 == 0:
            for s in (r // 2, r // 2 + M // 2):
                if not bad(s):
                    E.append((r, s, -math.log(2)))
        else:
            s = (3 * r + 1) % M
            if not bad(s):
                E.append((r, s, math.log(3)))
    return E

def max_cycle_mean(E):
    """Karp's maximum mean cycle (float)."""
    V = sorted({u for u, _, _ in E} | {v for _, v, _ in E})
    ix = {v: i for i, v in enumerate(V)}; n = len(V); NEG = float("-inf")
    D = [[NEG] * n for _ in range(n + 1)]
    D[0] = [0.0] * n
    for k in range(1, n + 1):
        for u, v, w in E:
            a = D[k - 1][ix[u]] + w
            if a > D[k][ix[v]]:
                D[k][ix[v]] = a
    best = NEG
    for v in range(n):
        if D[n][v] == NEG:
            continue
        best = max(best, min((D[n][v] - D[k][v]) / (n - k) for k in range(n) if D[k][v] > NEG))
    return best
