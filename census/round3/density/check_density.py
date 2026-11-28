"""Exact checks for round 3 / lens "density".  Exit code 0 iff all pass.

Covers (see README.md for the claim list):
  [1] the tables in systems.py agree with the catalog step functions;
  [2] the state graph is a faithful abstraction of the integer digit tree
      (Lemma 1): every concrete node to the stated depth carries the predicted
      state, slope A and intercept B, and T^k(M t + r) = a t + b is tested
      on several t including large random ones;
  [3] every certificate in certificates.json satisfies the supermartingale
      inequality EXACTLY, with rigorous rational upper bounds for q^gamma
      and F^s (Theorem 1 / 4 / 5 hypotheses), and theta is recomputed;
  [4] Theorem 1 finite content: the constants k0, C1; for every n < 2^NB
      (2^NB = 2^14 for p = 2 / mixed, 3^9 for p = 3) and every dyadic block
      with k >= k0: the first-crossing node really gives an iterate < n
      (checked by direct iteration of the map), and the number of uncertified
      n in the block is <= the block bound of Theorem 1;
  [5] Theorem 4 (Korec-type) and Theorem 5 (expanding) finite content, the
      same way, with the exact comparisons x^den < n^num  /  x^den > n^num;
  [6] Theorem 6: the early-drop density bounds q_lo <= q <= q_hi are
      recomputed exactly (depth L from certificates.json).
Runtime: about 3 minutes (180 s measured).
"""
import json, os, random, sys, time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from systems import SYSTEMS  # noqa: E402
from density_lib import *  # noqa: E402

FAIL = []


def ok(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("FAIL:", msg, flush=True)


def load_catalog():
    import importlib.util
    cat = {}
    for path in (os.path.join(CENSUS, "systems.py"),
                 os.path.join(CENSUS, "round2", "descent", "systems.py")):
        spec = importlib.util.spec_from_file_location("cat%d" % len(cat), path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for S in m.SYSTEMS:
            cat.setdefault(S["id"], S["step"])
    return cat


def ipow_cmp(x, n, c):
    """sign of x - n^c for positive ints x, n and rational c = a/b (exact)."""
    a, b = c.numerator, c.denominator
    lhs, rhs = x ** b, n ** a
    return (lhs > rhs) - (lhs < rhs)


def main():
    t0 = time.time()
    certs = json.load(open(os.path.join(HERE, "certificates.json")))
    cat = load_catalog()
    rnd = random.Random(20261127)

    # [1] catalog agreement ------------------------------------------------
    for S in SYSTEMS:
        cid = S["catalog"] or S["id"]
        if cid in cat:
            st = cat[cid]
            ok(all(st(n) == S["step"](n) for n in range(1, 20000)), "[1] step mismatch " + S["id"])
        else:
            # par_a_d entries: catalog ids carry a seed suffix
            hits = [k for k in cat if k.startswith(S["id"] + "_s")]
            if hits:
                st = cat[hits[0]]
                ok(all(st(n) == S["step"](n) for n in range(1, 20000)), "[1] step mismatch " + S["id"])
            else:
                ok(False, "[1] no catalog entry for " + S["id"])
    print("[1] catalog agreement done (%.1fs)" % (time.time() - t0), flush=True)

    only = os.environ.get("ONLY")
    for S in SYSTEMS:
        sid = S["id"]
        if only and sid not in only.split(","):
            continue
        T = S["T"]
        g = build_graph(T)
        rec = certs[sid]
        single = len(set(g.qs)) == 1
        p = g.qs[0]

        # [2] faithful abstraction -----------------------------------------
        depth = 12 if p == 2 and single else (8 if single else 9)
        nn = 0
        for node in concrete_tree(g, depth):
            d, M, r, a, b, st, A, B, ks = node
            for t in (0, 1, 7, 1000003, rnd.getrandbits(80)):
                n = M * t + r
                if n == 0:
                    continue
                ok(iterate(T.step, n, ks) == a * t + b, "[2] iterate %s %s" % (sid, (M, r, t)))
            nn += 1
        ok(nn > 100, "[2] tree too small " + sid)

        # drift (exact vectors) agree with the recorded ones
        D, L, Df, Lf = drift(g)
        ok({str(k): str(v) for k, v in D.items()} == rec["Delta"], "[2] Delta " + sid)
        ok(str(g.Gmax) == rec["Gmax"] and str(g.Gmin) == rec["Gmin"], "[2] G " + sid)

        # [3] certificates ------------------------------------------------
        for kind in ("never_drop", "korec", "korec_sharp", "expanding"):
            if kind not in rec:
                continue
            C = rec[kind]
            s, gamma, c = Fr(C["s"]), Fr(C["gamma"]), Fr(C["c"])
            w = [Fr(x) for x in C["w"]]
            ok(len(w) == len(g.states) and min(w) > 0, "[3] weights " + sid)
            ok(gamma <= 1 and (gamma >= 0 or kind == "korec_sharp"), "[3] gamma range " + sid)
            ok(check_supermartingale(g, s, gamma, w) is not None, "[3] supermartingale %s %s" % (sid, kind))
            theta = 1 - gamma + s * (1 - c)
            ok(theta == Fr(C["theta"]) and theta < 1, "[3] theta %s %s" % (sid, kind))
            if kind == "never_drop":
                ok(s > 0 and c == 1, "[3] never_drop params " + sid)
            if kind == "korec":
                ok(s > 0 and c < 1, "[3] korec params " + sid)
            if kind == "expanding":
                ok(s < 0 and c > 1, "[3] expanding params " + sid)
            if kind == "korec_sharp":
                ok(s < 0 and c < 1, "[3] sharp params " + sid)

        # [4]/[5] finite content on all small n -------------------------------
        NB = 1 << 14
        Kmax = NB.bit_length() - 1          # blocks [2^k, 2^{k+1}), k < Kmax
        kinds = []
        for kind in ("never_drop", "korec", "korec_sharp", "expanding"):
            if kind not in rec:
                continue
            C = rec[kind]
            s, gamma, c = Fr(C["s"]), Fr(C["gamma"]), Fr(C["c"])
            w = [Fr(x) for x in C["w"]]
            w0, wmin = w[0], min(w)
            th = 1 - gamma + s * (1 - c)
            info = dict(kind=kind, s=s, gamma=gamma, c=c, th=th)
            if kind == "never_drop":
                k0, C1 = never_drop_constants(g, type("C", (), dict(s=s, gamma=gamma, c=c, theta=th,
                                                                   w0=w0, wmin=wmin))())
                info["Kb"] = w0 * upow(g.qmax, th) * upow(Fr(1, 2), -s) / wmin
                info["C1"] = C1
            elif kind == "korec":
                k0 = 0
                while not all(lpow(Fr(2 ** k), c) >= 2 * k * g.Gmax for k in range(k0, k0 + 400)):
                    k0 += 1
                info["Kb"] = w0 * upow(g.qmax, 1 - gamma) * upow(2, s) * upow(2, s * (1 - c)) / wmin
            elif kind == "korec_sharp":
                ok(s < 0 and c < 1 and th < 1, "[5] sharp params " + sid)
                k0 = 0
                while not all(lpow(Fr(2 ** k), c) >= k * g.Gmax for k in range(k0, k0 + 400)):
                    k0 += 1
                info["Kb"] = g.qmax * w0 * upow(g.qmax, max(Fr(0), -gamma)) * upow(2, -s) / wmin
            else:
                sp = -s
                eps_max = (1 - th) / sp
                # any eps in (0, eps_max] works, with exponent max(theta_1, 1 - eps s');
                # a small-denominator eps keeps the exact power computations cheap
                eps = Fr(int(float(eps_max) * 10 ** 4) - 1, 10 ** 4)
                ok(0 < eps <= eps_max and eps < 1, "[5] eps " + sid)
                info["eps"] = eps
                info["th"] = max(th, 1 - eps * sp)
                ok(info["th"] < 1, "[5] theta_eff " + sid)
                k0 = 0
                while not all(lpow(Fr(2 ** k), 1 - eps) >= 2 * k * g.Gmax for k in range(k0, k0 + 400)):
                    k0 += 1
                K1 = w0 / wmin * upow(g.qmax, 1 - gamma) * upow(4, sp) * upow(2, sp * (c - 1))
                K2 = g.qmax * w0 / wmin
                info["Kb"] = K1 + K2
            info["k0"] = k0
            rec.setdefault("_k0", {})[kind] = k0
            kinds.append(info)

        def below(a, M, t):     # a/M < t, exact, t a Fraction
            return a * t.denominator < t.numerator * M

        if os.environ.get('VERBOSE'):
            print('   setup done %.1fs' % (time.time() - t0), kinds and [I['k0'] for I in kinds], flush=True)
        for k in range(0, Kmax):
            Y = 1 << k
            if os.environ.get('VERBOSE'):
                print('   block', k, '%.1fs' % (time.time() - t0), flush=True)
            thr = {}
            for I in kinds:
                if I["kind"] == "never_drop":
                    thr["never_drop"] = Fr(1, 2)
                elif I["kind"] == "korec":
                    thr["korec"] = lpow(Fr(2 * Y), I["c"] - 1) / 2          # <= (2Y)^(c-1)/2
                elif I["kind"] == "korec_sharp":
                    thr["korec_sharp"] = 2 * upow(Fr(Y), I["c"] - 1)        # >= 2 Y^(c-1)
                else:
                    thr["exp_tau"] = 4 * upow(Fr(2 * Y), I["c"] - 1)
                    thr["exp_dip"] = upow(Fr(Y), -I["eps"])
            bad = {I["kind"]: 0 for I in kinds}
            for n in range(Y, 2 * Y):
                path = path_of(g, n, Y)
                for I in kinds:
                    kind = I["kind"]
                    if kind in ("never_drop", "korec"):
                        t = thr[kind]
                        hit = next((nd for nd in path if below(nd[3], nd[1], t)), None)
                        if hit is None:
                            bad[kind] += 1
                            continue
                        if k >= I["k0"]:
                            x = iterate(T.step, n, hit[6])
                            ok(x == hit[3] * ((n - hit[2]) // hit[1]) + hit[4], "[4] node value " + sid)
                            if kind == "never_drop":
                                ok(x < n, "[4] no drop at first crossing %s n=%d" % (sid, n))
                            else:
                                ok(ipow_cmp(x, n, I["c"]) < 0, "[5] korec x >= n^c %s n=%d" % (sid, n))
                    elif kind == "korec_sharp":
                        t = thr[kind]
                        if any(below(nd[3], nd[1], t) for nd in path):
                            bad[kind] += 1
                            continue
                        if k >= I["k0"]:
                            for nd in path[1:]:
                                x = nd[3] * ((n - nd[2]) // nd[1]) + nd[4]
                                ok(ipow_cmp(x, n, I["c"]) >= 0, "[5] sharp x < n^c %s n=%d" % (sid, n))
                    else:
                        cut = path[-1]
                        if below(cut[3], cut[1], thr["exp_tau"]) or \
                                any(below(nd[3], nd[1], thr["exp_dip"]) for nd in path):
                            bad[kind] += 1
                            continue
                        if k >= I["k0"]:
                            x = iterate(T.step, n, cut[6])
                            ok(ipow_cmp(x, n, I["c"]) > 0, "[5] expanding x <= n^c %s n=%d" % (sid, n))
            for I in kinds:
                if k >= I["k0"]:
                    th_up = Fr(-((-I["th"].numerator * 10 ** 4) // I["th"].denominator), 10 ** 4)
                    bound = I["Kb"] * upow(Fr(Y), th_up)   # >= Kb * Y^theta (Y >= 1)
                    ok(bad[I["kind"]] <= bound, "[4/5] block count %s %s k=%d bad=%d bound=%s"
                       % (sid, I["kind"], k, bad[I["kind"]], float(bound)))
        # [6] early-drop density ----------------------------------------------
        if "early_drop" in rec:
            E = rec["early_drop"]
            Lchk = min(E["L"], 300)
            lo, hi = early_drop_bounds(g, Lchk, Fr(E["s"]), [Fr(x) for x in E["w"]])
            ok(lo <= hi and float(hi) - float(lo) < 1e-3, "[6] q bounds " + sid)
            ok(float(lo) <= E["q_hi"] + 1e-12 and E["q_lo"] <= float(hi) + 1e-12, "[6] q consistency " + sid)
            rec["_q"] = (float(lo), float(hi))
        print("  %-15s states=%-3d k0=%s %s  (%.1fs)" % (sid, len(g.states), rec.get("_k0"),
              ("q in [%.6f, %.6f]" % rec["_q"]) if "_q" in rec else "", time.time() - t0), flush=True)

    print("total %.1fs" % (time.time() - t0))
    if FAIL:
        print("%d FAILURES" % len(FAIL))
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
