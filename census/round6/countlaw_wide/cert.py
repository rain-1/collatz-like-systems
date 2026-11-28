"""Theorem R_G (general reduction) and its certified instances (Theorem C_G).

bracket(S, m, j, K): exact integers L <= N(p^m, m+j) <= U and the identity value p^m P(m+j) = sum Cnt * Phibar,
computed from in-horizon data only (alive nodes at depth d = m + j - K grouped by (state, A); the continuation
set S(state, A, E) mod p^K; the multiplier g^A mod p^K; max/min over ALL intercepts).

usage:
  python cert.py SYSTEM K m1,m2,.. j1-j2      print the certified table and append it to data/certified_<SYSTEM>.txt
"""
import os, sys, subprocess, tempfile, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cwlib import System

_G = {}


def gfun(S, st, K):
    key = (S.name, st, K)
    if key in _G:
        return _G[key]
    rows = " ".join(f"{u} {v} {e} {a}" for (u, v, e), a in zip(S.rows, S.arow))
    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as tmp:
        f = os.path.join(tmp, "g.bin")
        subprocess.run([os.path.join(HERE, "cw"), "gfun", str(S.p), str(S.k), str(S.g), rows,
                        str(st[0]), str(st[1]), str(K), f], check=True)
        raw = np.fromfile(f, dtype=np.int16)
    N = S.p ** K
    a, e = raw[:N].astype(np.int64), raw[N:].astype(np.int64)
    _G[key] = (a, e)
    return a, e


def amin_array(S, upto):
    return np.array([S.amin(E) for E in range(upto + 1)], dtype=np.int64)


def cont_set(S, st, A, E, K, am=None):
    """mask of z mod p^K in S(state, A, E): every decided step has g^{A+a} >= p^{E+e}"""
    a, e = gfun(S, st, K)
    if am is None:
        am = amin_array(S, E + K + S.k + 2)
    return (A + a) >= am[E + e]


def window_extremes(mask, u, N, p, K):
    """max and min over all intercepts B of #{0 <= t < N : (u t + B) mod p^K in S}"""
    Q = p ** K
    z = np.nonzero(mask)[0].astype(np.int64)
    if len(z) == 0:
        return 0, 0
    uinv = pow(int(u), -1, Q)
    pos = (z * uinv) % Q
    ind = np.bincount(pos, minlength=Q).astype(np.int32)
    cs = np.concatenate(([0], np.cumsum(np.concatenate((ind, ind[:N])), dtype=np.int64)))
    w = cs[N:N + Q] - cs[0:Q]
    return int(w.max()), int(w.min())


def bracket(S, m, j, K, counts=None):
    """returns (L, U, mean) with mean = sum Cnt * Phibar * p^j as an exact integer (so mean / p^j is
    p^m P(m+j)); L, U are integer bounds on N(p^m, m+j)."""
    p = S.p
    d = m + j - K
    assert d >= 0 and 1 <= j <= K
    if counts is None:
        counts = S.dp(d, keep={d})[d]
    N = p ** (K - j)
    Lo = Up = 0
    mean_pj = 0                    # sum Cnt * |S|  (= p^j * sum Cnt * Phibar)
    am = amin_array(S, d + K + S.k + 2)
    nontriv = 0
    for (st, A), cnt in counts.items():
        E = d - st[0]
        mask = cont_set(S, st, A, E, K, am)
        sz = int(mask.sum())
        mean_pj += cnt * sz
        if sz == p ** K:
            Lo += cnt * N
            Up += cnt * N
            continue
        if sz == 0:
            continue
        nontriv += 1
        u = pow(S.g, A, p ** K)
        mx, mn = window_extremes(mask, u, N, p, K)
        Lo += cnt * mn
        Up += cnt * mx
    return Lo, Up, mean_pj, nontriv


CACHE = os.environ.get("CW_CACHE", "/tmp/claude-1000/cw_cache")


def gfile(S, st, K):
    os.makedirs(CACHE, exist_ok=True)
    f = os.path.join(CACHE, f"g_{S.name}_{st[0]}_{st[1]}_{K}.bin")
    if not os.path.exists(f):
        rows = " ".join(f"{u} {v} {e} {a}" for (u, v, e), a in zip(S.rows, S.arow))
        subprocess.run([os.path.join(HERE, "cw"), "gfun", str(S.p), str(S.k), str(S.g), rows,
                        str(st[0]), str(st[1]), str(K), f + ".part"], check=True)
        os.rename(f + ".part", f)
    return f


def bracket_fast(S, m, j, K, counts):
    """same as bracket, with the continuation sets and window extremes evaluated in C (cw win)"""
    p = S.p
    d = m + j - K
    N = p ** (K - j)
    Q = p ** K
    ne = K + S.k + 3
    Lo = Up = mean_pj = 0
    byst = {}
    for (st, A), cnt in counts.items():
        E = d - st[0]
        if A >= S.amin(E + K + st[0] + S.k + 1):      # slope >= p^{K + s + k}: no continuation can drop
            Lo += cnt * N
            Up += cnt * N
            mean_pj += cnt * Q
            continue
        byst.setdefault(st, []).append((A, E, cnt))
    nontriv = 0
    for st, lst in byst.items():
        gf = gfile(S, st, K)
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".q", dir=CACHE) as qf:
            for (A, E, cnt) in lst:
                thr = [S.amin(E + e) - A for e in range(ne)]
                qf.write(f"{pow(S.g, A, Q)} {N} {ne} " + " ".join(map(str, thr)) + "\n")
            qname = qf.name
        out = subprocess.run([os.path.join(HERE, "cw"), "win", gf, str(p), str(K), qname],
                             check=True, capture_output=True, text=True).stdout.split()
        os.remove(qname)
        vals = list(map(int, out))
        for i, (A, E, cnt) in enumerate(lst):
            mx, mn, sz = vals[3 * i: 3 * i + 3]
            mean_pj += cnt * sz
            if sz == Q:
                Lo += cnt * N
                Up += cnt * N
            elif sz > 0:
                nontriv += 1
                Lo += cnt * mn
                Up += cnt * mx
    return Lo, Up, mean_pj, nontriv


def brute_N(S, m, b):
    """N(p^m, b) by direct evaluation of R_b on [0, p^m) (b <= ~24 for p = 2)"""
    mask = cont_set(S, S.root, 0, 0, b)
    return int(mask[: S.p ** m].sum())


def main():
    name, K = sys.argv[1], int(sys.argv[2])
    ms = [int(x) for x in sys.argv[3].split(",")]
    j1, j2 = map(int, sys.argv[4].split("-"))
    S = System(name)
    p = S.p
    out = open(os.path.join(HERE, "data", f"certified_{name}.txt"), "a")
    hdr = f"# {name}: Theorem R_G bounds, K = {K}; rel = (bound - p^m P(m+j)) / (p^m P(m+j))"
    print(hdr)
    out.write(hdr + "\n")
    for m in ms:
        t0 = time.time()
        ds = {m + j - K for j in range(j1, j2 + 1)} | {m + j for j in range(j1, j2 + 1)}
        allc = S.dp(max(ds), keep=ds)
        surv = {b: sum(allc[b].values()) for b in ds}
        for j in range(j1, j2 + 1):
            br = bracket_fast if os.environ.get("FAST") else bracket
            Lo, Up, mean_pj, nt = br(S, m, j, K, allc[m + j - K])
            # identity: sum over alive depth-d nodes of |S| equals |R_{m+j}| (computed by the same DP to depth m+j)
            assert mean_pj == surv[m + j], "identity sum Cnt Phibar = p^m P(m+j) failed"
            # p^m P(m+j) = |R_{m+j}| / p^j ; rel = (bound * p^j - |R_{m+j}|) / |R_{m+j}|
            R = surv[m + j]
            rl = (Lo * p ** j - R) / R
            ru = (Up * p ** j - R) / R
            line = f"m={m:5d} j={j:3d} K={K} nontrivial_types={nt:3d} rel_lower={rl:+.6f} rel_upper={ru:+.6f}"
            print(line, flush=True)
            out.write(line + "\n")
        print(f"  ({time.time() - t0:.0f} s)")
    out.close()


if __name__ == "__main__":
    main()
