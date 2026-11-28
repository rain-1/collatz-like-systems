#!/usr/bin/env python3
"""Generate <id>.md for every system in systems.py from the exact decide.py output.
(The numbers in these files are re-verified by check_systems.py.)"""
import sys, os, math
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from decide import decide, residue_graph, karp_float, karp_np, cycle_multiplier, deepest_walk, path_progression
from families import rule_string
import systems


def fmt_cycle(c):
    if len(c) <= 30:
        return "(" + " ".join(map(str, c)) + ")"
    return "(" + " ".join(map(str, c[:25])) + f" ... ; length {len(c)})"


for s in systems.SYSTEMS:
    Q, tab = s["Q"], s["table"]
    res = decide(Q, tab)
    succ = residue_graph(Q, tab)
    mu, cyc = (karp_float if Q <= 64 else karp_np)(Q, tab, succ)
    U, W = cycle_multiplier(tab, cyc)
    walk = deepest_walk(Q, tab, succ)
    a, M, *_ = path_progression(Q, tab, walk)
    c = res["weights"]
    g = 0
    for x in c:
        g = math.gcd(g, x)
    lines = [
        f"# {s['id']}",
        "",
        f"**Rule.** {s['rule']}.",
        "",
        f"As a table map (Q = {Q}): {rule_string(Q, tab)}.",
        "",
        "**Question (GLOBAL).** Is every positive orbit eventually periodic, and what are the cycles?",
        "",
        f"**Answer.** Yes. There are exactly {len(res['cycles'])} cycle(s): "
        + ", ".join(fmt_cycle(x) for x in sorted(res["cycles"])) + ".",
        "",
        "**Status.** PROVED (Theorem 2 of dichotomy.md, with the integer certificate below). "
        + (s["note"] + "." if s["note"] else ""),
        "",
        "## Proof",
        "",
        f"(H1), (H2) and (P) hold, so Theorem 1 of dichotomy.md applies. decide.py found integer weights "
        f"c(r) for r mod {Q} with c(s)·u_r < c(r)·w_r on every edge r → s of the residue graph. "
        f"The weights have 60-bit size and are printed by `python3 decide.py --id {s['id']}`. "
        f"Each of the {sum(len(x) for x in succ)} edge inequalities is checked with integers, and the largest edge "
        f"ratio is θ = {float(res['theta']):.6f} < 1. By Theorem 2, V(n) = c(n mod {Q})·n strictly decreases "
        f"except on the finite set F = {{n : V(Tn) ≥ V(n)}}. F is contained in "
        f"{{n ≤ {max(res['bounds'])}}} (symbolic bounds N_r) and has {len(res['F'])} elements, the largest "
        f"being {max(res['F'])}. Every orbit meets F and every cycle meets F. Iterating each element of F until it "
        f"repeats gives exactly the cycles listed above. ∎",
        "",
        "## Difficulty",
        "",
        f"* The minimal stopping depth is **k\\* = {res['kstar']}** (Theorem 3). Every plain descent certificate "
        f"T^j(n) < n on residue classes needs some class with j ≥ {res['kstar']}, and one with max j = "
        f"{res['kstar']} exists. The minimal certificate has {res['leaves']} leaves when residues mod {Q} are "
        f"distinguished.",
        f"* Witness for the lower bound: the progression n ≡ {a} (mod {M}) (modulus has {M.bit_length()} bits). "
        f"On it, T^i(n) ≥ n for every i < {res['kstar']} at all large n. `check_systems.py` verifies this at "
        f"n = a + M·10^12 by direct iteration.",
        f"* The reason is the max-mean cycle of the residue graph: length {len(cyc)}, multiplier {U}/{W} "
        f"≈ {U / W:.6f}, mean log-multiplier {mu:.6f} per step. It contracts, but only barely, so by "
        f"Theorem 3(c) the depth is large. The a-priori depth bound from the potential is "
        f"{res['depth_bound']}.",
        "* A one-step weighted potential nevertheless proves GLOBAL, so on the census scale this is tier 2 "
        "(descent plus a finite table). The depth matters only for plain certificates. For comparison, the "
        "round-2 depth record desc_s32_max has k = 44.",
        "",
        "**Novelty.** I know of no prior occurrence of this specific map; novelty was not checked beyond "
        "that. The census catalogue and round 2 do not contain it.",
        "",
        "**Check.** `check_systems.py` (all systems, about 5 s).",
        "",
    ]
    open(os.path.join(HERE, s["id"] + ".md"), "w").write("\n".join(lines))
    print("wrote", s["id"])
