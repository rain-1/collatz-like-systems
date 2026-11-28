"""Which census maps satisfy the hypotheses of Theorems G1/G2, and their constants.

For every system in census/systems.py and round2/{descent,rewriting}/systems.py, try to recognise the step
function as a single-prime table map: for p in (2, 3, 5) and k <= 4, every class r mod p^k must act as
n -> (u n + v) / p^e with u coprime to p (checked on 40 members of the class, exact Fractions).  Then
(SG): all u are powers of one integer g >= 2 (u = 1 allowed).  The first (p, k) that works is used.
Failures are reported with the reason.  For maps passing (SG), the constants of cwconst are computed.

usage: python hyp_scan.py   -> data/hyp_scan.json and a printed table
"""
import os, sys, json, math, importlib.util
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import cwlib
from cwlib import System


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def infer(step, p, k):
    Q = p ** k
    rows = []
    for r in range(Q):
        ns = [r + Q * t for t in range(1, 41)]
        try:
            ys = [step(n) for n in ns]
        except Exception:
            return None, "step raised"
        sl = Fraction(ys[1] - ys[0], ns[1] - ns[0])
        if sl == 0:
            return None, "constant branch"
        for n, y in zip(ns, ys):
            if Fraction(y - ys[0]) != sl * (n - ns[0]):
                return None, "not affine on classes"
        num, den = sl.numerator, sl.denominator
        e = 0
        while den % p == 0:
            den //= p
            e += 1
        if den != 1 or num % p == 0 or num < 0:
            return None, f"slope {sl} not a p-adic unit / p^e"
        u = num
        v = ys[0] * p ** e - u * ns[0]
        rows.append((u, v, e))
    return rows, None


def common_generator(us):
    us = sorted(set(u for u in us if u != 1))
    if not us:
        return None
    for g in range(2, min(us) + 1):
        ok = True
        for u in us:
            x = u
            while x % g == 0:
                x //= g
            if x != 1:
                ok = False
                break
        if ok:
            return g
    return None


def scan():
    mods = [("census", os.path.join(CENSUS, "systems.py")),
            ("descent", os.path.join(CENSUS, "round2", "descent", "systems.py")),
            ("rewriting", os.path.join(CENSUS, "round2", "rewriting", "systems.py"))]
    seen_rules = {}
    out = []
    for tag, path in mods:
        mod = load(path, "sys_" + tag)
        for s in mod.SYSTEMS:
            rid = s["id"]
            rule = s["rule"]
            if rule in seen_rules:
                continue
            seen_rules[rule] = rid
            rec = dict(id=rid, src=tag, rule=rule)
            found = None
            reasons = []
            for p in (2, 3, 5):
                for k in range(1, {2: 7, 3: 5, 5: 3}[p]):
                    rows, why = infer(s["step"], p, k)
                    if rows is not None:
                        found = (p, k, rows)
                        break
                    reasons.append(f"p={p},k={k}: {why}")
                if found:
                    break
            if not found:
                rec["SG"] = False
                r2 = [x for x in reasons if x.startswith("p=2")][-1]
                rec["why"] = "no single-prime unit table mod p^k (p=2: k<=6, p=3: k<=4, p=5: k<=2); " + r2
                out.append(rec)
                continue
            p, k, rows = found
            g = common_generator([u for (u, v, e) in rows])
            if g is not None:      # normalise: gcd of the exponents a_r equal to 1
                ex = [cwlib.log_exact(g, u) for (u, v, e) in rows]
                c = 0
                for a_ in ex:
                    c = math.gcd(c, a_)
                g = g ** c
            rec.update(p=p, k=k)
            if g is None:
                rec["SG"] = False
                us = sorted(set(u for (u, v, e) in rows))
                rec["why"] = ("all multipliers are 1 (no expansion; trivial group)" if us == [1]
                              else f"multipliers {us} are not powers of one integer")
                out.append(rec)
                continue
            if math.gcd(g, p) != 1:
                rec["SG"] = False
                rec["why"] = "generator not coprime to p"
                out.append(rec)
                continue
            name = f"scan_{rid}"
            cwlib.SYS[name] = dict(p=p, k=k, g=g, rows=rows)
            try:
                S = System(name)
            except RuntimeError as ex:
                rec["SG"] = False
                rec["why"] = f"(F) fails: {ex}"
                out.append(rec)
                continue
            rec["SG"] = True
            rec["g"] = g
            rec["sysname"] = name
            out.append(rec)
    return out


if __name__ == "__main__":
    import cwconst
    res = scan()
    for rec in res:
        if rec.get("SG"):
            S = System(rec["sysname"])
            sc = S.surv_counts(80)
            if sc[-1] == 0:
                b0 = sc.index(0)
                rec.update(empty_from=b0)
                print(f"{rec['id']:22s} p={rec['p']} k={rec['k']} g={rec['g']}: R_b is empty for b >= {b0} "
                      f"(every start drops within {b0} digits); count law trivial", flush=True)
                continue
            o, pot = cwconst.constants(rec["sysname"], K0=200 if rec["p"] == 2 else 120)
            rec.update({k_: o[k_] for k_ in ("states", "drift", "h", "h_up", "h0", "alpha", "H2", "c1", "c2",
                                              "pot", "bad", "rescue", "Cstar", "H0")})
            print(f"{rec['id']:22s} p={rec['p']} k={rec['k']} g={rec['g']} st={o['states']} drift={o['drift']:+.4f} "
                  f"h={o['h']:.5f} h0={o['h0']:.4f} c1={o['c1']:.4f} c2={o['c2']:.4f} Pot={o['pot']} "
                  f"bad={o['bad']} r={o['rescue']} C*={o['Cstar']:.3f}", flush=True)
        else:
            print(f"{rec['id']:22s} FAILS: {rec['why']}", flush=True)
    json.dump(res, open(os.path.join(HERE, "data", "hyp_scan.json"), "w"), indent=1, default=str)
