#!/usr/bin/env python3
"""make_report.py -- turn out/catalog_sweep.json into the catalog table (out/catalog_table.md)
with the census status of the GLOBAL question and how it was settled before.

Status labels:
  OPEN-CLS   open census entry asking GLOBAL (CLS ids given)
  OPEN       open in a round folder (split family class O/K/P, accel 3x+1-type cores, ...)
  yes / no   GLOBAL settled (method given)
  n/a        GLOBAL is not the recorded question (FATE-only systems); our verdict still stands
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(CENSUS, "round3", "deep"))
import family_lib  # noqa: E402

R1 = {  # round 1 GLOBAL answers (settled_collatz_questions.txt)
    "div2_3n_s5": "no", "div3_2n_s5": "no", "mahler_s1": "no", "par_2_1_s27": "no",
    "par_3_2_s27": "no", "par_3_4_s27": "no", "par_4_2_s27": "no", "par_5_2_s27": "no",
    "par_6_3_s27": "no", "perm_ceil2_s1": "no", "perm_ceil3_s1": "no", "perm_suffix_a_s1": "no",
    "perm_suffix_b_s8": "no", "perm_suffix_c_s1": "no", "perm_suffix_d_s1": "no",
    "farkas_s27": "yes", "m3_a_s100": "yes", "m3_c_s100": "yes", "m3_f_s100": "yes",
    "par_1_1_s27": "yes", "par_1_5_s27": "yes", "perm_flip_s27": "yes", "splitB_71_s27": "yes",
    "splitB_7_s27": "yes", "split_13_s27": "yes", "split_5_s27": "yes", "split_7081_s27": "yes",
    "split_73_s27": "yes", "split_97_s27": "yes"}

FATE_ONLY = {"auto_sfx7_s17", "auto_sfx7_far", "auto_mix3_s7", "flipT_s8", "swT9_s8", "swT9_15_s8",
             "swT3_9_15_s8", "shiftT_s8", "twochanW_s8", "swD_s3", "perm1932_1cycle",
             "steiner_1cycle", "fx10_64_s7", "fx26_32_s7", "race_s21", "c62_64_s27", "perm12_s7",
             "swT2_8_s8"}


def deep_status(a, b, d):
    (a2, b2, d2), cls, info = family_lib.canonical(a, b, d)
    if cls == "C":
        if (a2, b2, d2) != (a, b, d):
            return "yes", f"split class R -> C member SPLIT{(a2, b2, d2)} (Lemma R + descent)"
        return "yes", "split class C: descent (round2 lemmas Thm 1)"
    if cls == "D":
        return "no", "split class D: every orbit diverges (round3/deep Theorem D)"
    if cls == "P" and a2 == 1:
        return "yes", "parity map n+d: descent"
    if cls == "K":
        return "OPEN", f"split class K: {info} (Theorem K)"
    if cls == "P":
        return "OPEN", f"parity map {a2}n+{d2}"
    return "OPEN", f"split class O ({info})"


def status(g):
    ids = [i.split("@")[0] for i in g["ids"]]
    srcs = [i.split("@")[1] for i in g["ids"]]
    if g["open_cls"]:
        return "OPEN-CLS", ",".join(sorted(set(g["open_cls"])))
    for i in ids:
        if i in R1:
            return R1[i], "round 1 census record"
    for i, s in zip(ids, srcs):
        if s.startswith("round3/mixedbase"):
            st = (g["settled_note"] or ["?"])[0].replace("status field: ", "")
            return ("yes" if st.startswith("PROVED") else "OPEN"), "round3/mixedbase: " + st
        if s.startswith("round2/upfrom1"):
            st = (g["settled_note"] or ["?"])[0].replace("status field: ", "")
            return ("no" if st.startswith("PROVED") else "OPEN"), "round2/upfrom1 (divergent orbit): " + st
        if s.startswith("round3/dichotomy"):
            return "yes", "round3/dichotomy: descent certificate"
        if s.startswith("round2/descent"):
            return "yes", "round2/descent: descent certificate"
        if i.startswith("acc_h"):
            return "yes", "round3/accel: Theorem H"
        if i.startswith("dress_"):
            return "yes", "round3/accel dressing.md (second prime consumes runs)"
        if i in ("farkas2005", "farkas5m_s27"):
            return "yes", "Farkas 2005 / round2 rewriting"
        if s.startswith("round2/qr"):
            return "yes" if i == "qrA3_q17" else "n/a", "round2/qr (basin question)"
    for i in ids:
        if i in FATE_ONLY:
            if i in ("race_s21", "c62_64_s27", "fx10_64_s7", "fx26_32_s7", "perm12_s7", "swT2_8_s8"):
                return "no", "round3/divergence: proved infinite orbit"
            if i in ("steiner_1cycle",):
                return "OPEN", "= 3x+1 (question asked: 1-cycles)"
            if i in ("perm1932_1cycle",):
                return "OPEN", "= 1932 map (question asked: 1-cycles)"
            return "n/a", "FATE question only"
    for i, s in zip(ids, srcs):
        if s.startswith("round3/accel") and (i.startswith("sf") or i.startswith("zcore")):
            return "OPEN", "round3/accel: 3x+1-type core (S-family)"
    for i, s in zip(ids, srcs):
        if s.startswith("round3/deep"):
            a, b, d = [int(x[1:]) for x in i.split("_")[1:]]
            return deep_status(a, b, d)
    return "?", ""


def resolved(r):
    if r.get("decide") == "CERT":
        return "CERT"
    h = r.get("H", "")
    if h.startswith("GLOBAL"):
        return "H'"
    if h.startswith("DIVERGES"):
        return "DIV"
    return ""


def fmt(x, nd=4):
    if x is None:
        return "-"
    if isinstance(x, float):
        return f"{x:.{nd}f}"
    return str(x)


def main():
    d = json.load(open(os.path.join(HERE, "out", "catalog_sweep.json")))
    rows = []
    for g in d["records"]:
        st, how = status(g)
        r = g["result"]
        types = r.get("types", {})
        base = list(types.values())[0] if types else "-"
        lv = f"{base}" + (f" ({len(types)} levels to {max(int(k) for k in types)})" if len(types) > 1 else "")
        cyc = r.get("cycle_mins") or r.get("H_cycle_mins")
        rows.append(dict(ids=g["ids"], rule=g["rules"][0], Q=g["Q"], st=st, how=how,
                         markov=r.get("markov"), decide=r.get("decide", "-" if r.get("markov") is False else r.get("note", "-")),
                         kstar=r.get("kstar"), types=lv, H=r.get("H", "-"), res=resolved(r),
                         cyc=cyc, t1=r.get("theta1"), tr=r.get("theta_run"), gap=r.get("gap"),
                         drift=r.get("drift"), zero=g.get("zero"), exc=g["exceptions"]))
    json.dump(rows, open(os.path.join(HERE, "out", "catalog_rows.json"), "w"), indent=1, default=str)
    # counts
    import collections
    c = collections.Counter((x["st"], x["res"] or "-") for x in rows)
    L = []
    L.append("# Catalog sweep: every census table map through the harness\n")
    L.append("Generated by make_report.py from out/catalog_sweep.json. One row per distinct table "
             "(ids sharing a table are merged). `res`: CERT = decide.py certificate (complete cycle list); "
             "H' = Theorem H' (theory.md) with type (b) or non-Markov over-approximation; DIV = a residue class "
             "proved divergent by a division-free expanding cycle. `types`: SCC types at the base level "
             "(and the number of lifted levels tried for mixed or non-Markov moduli).\n")
    L.append("## Counts (status of GLOBAL before this round x outcome of the harness)\n")
    L.append("| census status | harness outcome | tables |\n|---|---|---|")
    for (st, res), v in sorted(c.items()):
        L.append(f"| {st} | {res or 'not settled'} | {v} |")
    L.append("")
    for title, pred in [
        ("Open census entries (OPEN-CLS)", lambda x: x["st"] == "OPEN-CLS"),
        ("Systems open in round folders", lambda x: x["st"] == "OPEN"),
        ("Settled systems the harness settles again", lambda x: x["st"] in ("yes", "no") and x["res"]),
        ("Settled systems the harness does not settle", lambda x: x["st"] in ("yes", "no") and not x["res"]),
        ("GLOBAL not the recorded question", lambda x: x["st"] in ("n/a", "?")),
    ]:
        sel = [x for x in rows if pred(x)]
        L.append(f"## {title} ({len(sel)})\n")
        L.append("| ids | Q | M | status / how | decide | k* | types | Theorem H' | cycles (minima) | theta_1 | theta_run | gap | drift |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for x in sorted(sel, key=lambda x: (x["ids"][0])):
            ids = ", ".join(i.split("@")[0] for i in x["ids"][:3]) + (" ..." if len(x["ids"]) > 3 else "")
            cy = x["cyc"]
            cys = "-" if cy is None else (" ".join(map(str, cy[:6])) + (" ..." if len(cy) > 6 else ""))
            L.append(f"| {ids} | {x['Q']}{' (N0)' if x['zero'] else ''} | {'y' if x['markov'] else 'n'} | {x['st']}: {x['how']} | "
                     f"{x['decide']} | {fmt(x['kstar'])} | {x['types']} | {x['H']} | {cys} | {fmt(x['t1'])} | "
                     f"{fmt(x['tr'])} | {fmt(x['gap'])} | {fmt(x['drift'])} |")
        L.append("")
    open(os.path.join(HERE, "out", "catalog_table.md"), "w").write("\n".join(L))
    for (st, res), v in sorted(c.items()):
        print(st, res or "-", v)


if __name__ == "__main__":
    main()
