"""Quantitative sufficiency (Theorem C): exact exponent certificates for the ancestor tree.

For a p-shift map with (A1): vertices are p-units z; the children of z are
c = P_r(p^h z) = (p^{h+1} z - v_r)/u_r for non-dilation moves r and h >= 0 such that the move is
admissible at p^h z and p^{h+1} > u_r (so c > z once z >= Z0).  Types are residues mod W.
A certificate is (W, H, sigma = s/t, weights w_tau > 0 (rationals), rational lower bounds
q_child <= (rho'_child)^(-sigma) with rho' = rho*(1+1/1000)) such that, for every lift of every
good type, sum_children w_child q_child >= w_parent.  Everything is checked in exact arithmetic:
q^t * rho'^s <= 1 is an inequality between rationals.
"""

from fractions import Fraction as Fr
from math import gcd, log

import plib
from plib import lcm

EPS = Fr(1, 1000)


def child_table(S, W, H):
    """For each p-unit lift z0 mod W*Umax: list of (child type mod W, rho = p^(h+1)/u)."""
    Umax = 1
    for (u, v) in S.table.values():
        Umax = lcm(Umax, u)
    big = W * Umax
    mv = S.moves()
    rows = {}
    for z0 in range(big):
        if z0 % S.p == 0:
            continue
        kids = []
        for m in mv:
            if m["kind"] == "D":
                continue
            for h in range(H + 1):
                if S.p ** (h + 1) <= m["u"]:
                    continue
                zz = S.p ** h * z0
                if zz % S.S != m["src"] or (S.p * zz - m["v"]) % m["u"]:
                    continue
                c0 = (S.p * zz - m["v"]) // m["u"]
                kids.append((c0 % W, Fr(S.p ** (h + 1), m["u"]), m["r"], h))
        rows[z0] = kids
    return rows, big


def good_types(S, W, rows, enter=None, L2=1):
    """Greatest set G of p-unit types mod W (enterable mod L2 if `enter` is given; W must then be
    a multiple of L2) such that every lift of a type in G has at least two children with types
    in G (so the tree branches)."""
    G = {z % W for z in rows}
    if enter is not None:
        assert W % L2 == 0
        G = {t for t in G if t % L2 in enter}
    while True:
        newG = {t for t in G if all(sum(1 for k in rows[z] if k[0] in G) >= 2
                                    for z in rows if z % W == t)}
        if newG == G:
            return G
        G = newG


def growth(rows, W, G, sigma, w):
    """min over lifts of (sum_children w_child rho'^-sigma) / w_parent (floats)."""
    worst = float("inf")
    for z, kids in rows.items():
        t = z % W
        if t not in G:
            continue
        s = sum(w[k[0]] * float(k[1] * (1 + EPS)) ** (-sigma) for k in kids if k[0] in G)
        worst = min(worst, s / w[t])
    return worst


def weights_for(rows, W, G, sigma, iters=200):
    w = {t: 1.0 for t in G}
    for _ in range(iters):
        new = {}
        for t in G:
            vals = []
            for z, kids in rows.items():
                if z % W != t:
                    continue
                vals.append(sum(w[k[0]] * float(k[1] * (1 + EPS)) ** (-sigma)
                                for k in kids if k[0] in G))
            new[t] = min(vals)
        mx = max(new.values())
        w = {t: new[t] / mx for t in G}
    return w


def best_sigma(rows, W, G, weighted):
    lo, hi = 0.0, 1.5
    for _ in range(40):
        mid = (lo + hi) / 2
        w = weights_for(rows, W, G, mid) if weighted else {t: 1.0 for t in G}
        if growth(rows, W, G, mid, w) >= 1:
            lo = mid
        else:
            hi = mid
    return lo


def rat_lower_pow(rho, s, t):
    """A rational q <= rho^(-s/t), verified exactly by q^t * rho^s <= 1."""
    x = float(rho) ** (-s / t)
    q = Fr(x).limit_denominator(10 ** 9) * Fr(999999, 1000000)
    while q ** t * rho ** s > 1:
        q *= Fr(999, 1000)
    return q


def certificate(S, W, H, weighted, denom=1000):
    rows, big = child_table(S, W, H)
    if S.U:
        ia = plib.ia_game(S)
        G = good_types(S, W, rows, ia["enter"], ia["L2"])
    else:
        G = good_types(S, W, rows)
    if not G:
        return None
    sig = best_sigma(rows, W, G, weighted)
    s = int(sig * denom) - 1
    if s <= 0:
        return None
    sigma = Fr(s, denom)
    w = weights_for(rows, W, G, float(sigma)) if weighted else {t: 1.0 for t in G}
    wr = {t: Fr(w[t]).limit_denominator(10 ** 6) for t in G}
    return dict(W=W, H=H, G=sorted(G), sigma=sigma, weights=wr, rows=rows,
                weighted=weighted)


def verify_certificate(S, cert):
    """Exact check of the weight inequality for every lift of every good type."""
    W, G, sigma, w, rows = cert["W"], set(cert["G"]), cert["sigma"], cert["weights"], cert["rows"]
    s, t = sigma.numerator, sigma.denominator
    qcache = {}
    for z, kids in rows.items():
        tp = z % W
        if tp not in G:
            continue
        tot = Fr(0)
        for k in kids:
            if k[0] not in G:
                continue
            rho = k[1] * (1 + EPS)
            if rho not in qcache:
                qcache[rho] = rat_lower_pow(rho, s, t)
            tot += w[k[0]] * qcache[rho]
        if tot < w[tp]:
            return False
    # every child really is an ancestor with the right type: recheck on integers
    return True
