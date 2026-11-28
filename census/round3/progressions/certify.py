"""The algorithm of Theorem A: from a p-shift table, compute the exact profinite invariant and a
proof object (all finite data used by the proof), then classify the cycles.

Usage: nice python3 certify.py  -> writes certificates.json and prints a table.
"""

import json
import sys as _sys
from fractions import Fraction as Fr
from math import gcd

import plib
from plib import vp, strip, primes_of


def lap_numerator(S, c):
    """Product of the numerators u along the cycle through c (one lap) and the lap length."""
    a, x, L = 1, c, 0
    while True:
        a *= S.table[x % S.P][0]
        x = S.T(x)
        L += 1
        if x == c:
            return a, L


def certify(entry):
    S = entry["sys"]
    out = dict(id=S.name, p=S.p, kappa=S.kappa, U=S.U)
    errs = S.validate()
    out["valid"] = not errs
    if errs:
        out["errors"] = errs
        return out
    out["A1_dilation"] = S.has_dilation()
    out["A0_strongly_connected"] = S.state_graph_strongly_connected()
    mv = S.moves()
    out["moves"] = [dict(r=m["r"], u=m["u"], v=m["v"], src=m["src"], dst=m["dst"],
                         kind=m["kind"]) for m in mv]
    if not (out["A1_dilation"] and out["A0_strongly_connected"]):
        out["theorem_A"] = False
        return out
    # ---- translations and delta
    loops = plib.fundamental_loops(S)
    trans = plib.translations(S, loops)
    delta = plib.delta_from_translations(S, trans)
    out["loops"] = [dict(word=w, slope=str(f.a), shift=str(f.b)) for (w, f) in loops]
    # keep the translations realising delta (a minimal certifying subset)
    cert_trans, d = [], 0
    for (i, j, t) in trans:
        g = gcd(d, strip(t.numerator, S.bad))
        if g != d:
            cert_trans.append(dict(loops=[i, j], amount=str(t)))
            d = g
        if d == delta:
            break
    out["translations"] = cert_trans
    out["delta"] = delta
    if delta == 0:
        out["theorem_A"] = False
        out["reason"] = "no translation found in the loop group (invariant not finite-modulus)"
        return out
    cls = plib.groupoid_classes(S, delta)
    assert plib.check_symmetric(S, delta, cls)
    dstar, state_free, rep = plib.minimal_invariant(S, delta, cls)
    out["invariant_modulus"] = dstar
    out["state_free"] = state_free
    # class table at modulus dstar: list of (state, residue) groups
    groups = {}
    for (s, z), c in sorted(rep.items()):
        groups.setdefault(c, []).append((s, z))
    out["classes"] = [groups[c] for c in sorted(groups)]
    # ---- initial accessibility
    if S.U:
        ia = plib.ia_game(S)
        L2 = ia["L2"]
        enter = ia["enter"]
        out["IA"] = dict(L_U=ia["L"], L2=L2, live_nodes=len(ia["live"]),
                         all_nodes=S.S * L2, enterable=len(enter))
        # entry: every merging class contains an enterable point
        e_ok = all(plib.e_image_residues(S, m, L2) <= enter for m in mv if m["kind"] == "E")
        try:
            Bnd, necyc = plib.non_E_cycles(S)
            ne_ok = all(any(x % L2 in enter for x in c) for c in necyc)
        except AssertionError:
            Bnd, necyc, ne_ok = None, None, False
        out["IA"]["E_images_enterable"] = e_ok
        out["IA"]["nonE_bound"] = Bnd
        out["IA"]["nonE_cycles"] = necyc
        out["IA"]["nonE_cycles_enterable"] = ne_ok
        out["IA"]["no_X_moves"] = all(m["kind"] != "X" for m in mv)
        all_enter = len(enter) == L2
        out["IA"]["all_enterable"] = all_enter
        ok = (len(ia["live"]) > 0 and (all_enter or (e_ok and ne_ok))
              and out["IA"]["no_X_moves"])
        out["IA"]["holds"] = ok
    else:
        out["IA"] = dict(holds=True, note="U empty: no U-adic condition")
    out["theorem_A"] = out["IA"]["holds"]
    # ---- cycles and their classes
    def g(n):
        return rep[(n % S.S, n % dstar)]
    cyc = []
    for c0 in entry["cycles"]:
        cy = plib.cycle_of(S, c0)
        assert cy is not None and c0 in cy, (S.name, c0)
        a, L = lap_numerator(S, c0)
        cyc.append(dict(rep=c0, length=len(cy), cls=g(c0), lap_numerator=a,
                        min=min(cy)))
    out["cycles"] = cyc
    by = {}
    for c in cyc:
        by.setdefault(c["cls"], []).append(c["rep"])
    out["shared_classes"] = {str(k): v for k, v in by.items() if len(v) > 1}
    out["expanding_cycle"] = next((c["rep"] for c in cyc if c["lap_numerator"] > 1), None)
    out["theorem_B"] = bool(out["theorem_A"] and state_free and out["expanding_cycle"])
    return out


def main():
    import systems
    res = []
    for e in systems.SYSTEMS:
        c = certify(e)
        c["global"] = e["global_"]
        c["cls_census"] = e["cls"]
        res.append(c)
        print(f"{c['id']:16s} A={c.get('theorem_A')} d*={c.get('invariant_modulus')} "
              f"classes={len(c.get('classes', []))} stfree={c.get('state_free')} "
              f"shared={c.get('shared_classes')} B={c.get('theorem_B')}")
    with open("certificates.json", "w") as f:
        json.dump(res, f, indent=1, default=str)


if __name__ == "__main__":
    main()
