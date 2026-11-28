#!/usr/bin/env python3
"""postprocess.py -- from out/fam_*.txt (famscan output) build
   out/families_summary.md   counts per family
   out/typeb_list.jsonl      every type-(b) member: table, the (b) cycle(s) with residues, exact
                             multiplier U/W, periodic point x*, the prime that kills other
                             orbits, and the complete cycle list from Theorem H' (exact, twlib)
   out/cert_top.json         per family: the 25 deepest CERT members (exact k* by
                             decide.stopping_depth among the 400 with max cycle mean closest
                             to 0) and the members with the most cycles
Runtime: ~10-20 minutes (nice).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import families as F  # noqa: E402
import twlib  # noqa: E402


def read(name):
    B, CERT, summ = [], [], None
    fn = os.path.join(HERE, "out", f"fam_{name}.txt")
    if not os.path.exists(fn):
        import gzip
        fh = gzip.open(fn + ".gz", "rt")
    else:
        fh = open(fn)
    for line in fh:
        p = line.split()
        if p[0] == "B":
            B.append(p[1])
        elif p[0] == "CERT":
            CERT.append((p[1], float(p[2]), int(p[3]), int(p[4])))
        elif p[0] == "SUMMARY":
            summ = line.strip()
    return B, CERT, summ


def parse_summary(s):
    t = s.split()
    d = {}
    i = 1
    while i < len(t) - 1 and t[i] != "hist":
        d[t[i]] = t[i + 1]
        i += 2
    d["hist"] = " ".join(t[i + 1:])
    return d


def main():
    fs = open(os.path.join(HERE, "out", "families_summary.md"), "w")
    fb = open(os.path.join(HERE, "out", "typeb_list.jsonl"), "w")
    top = {}
    fs.write("| family | Q | mode | members tested | CERT | type (b) only | type (c) | division-free (Z div / neutral) | cycles per CERT member (histogram) |\n")
    fs.write("|---|---|---|---|---|---|---|---|---|\n")
    for name, mode, cnt in F.FAMILIES:
        Q, opts = F.family(name)
        B, CERT, summ = read(name)
        d = parse_summary(summ)
        fs.write(f"| {name} | {Q} | {'exhaustive' if mode == 0 else 'random sample'} | {d['total']} | {d['CERT']} | "
                 f"{d['B']} | {d['C']} | {d['Z']} / {d['ZN']} | {d['hist']} |\n")
        # type (b)
        for ix in B:
            tab = F.decode(opts, ix)
            lev = twlib.classify_level(Q, tab, Q)
            assert "b" in lev["types"] and "c" not in lev["types"] and "z" not in lev["types"]
            H = twlib.theorem_H(Q, tab, lev)
            assert H["status"] == "GLOBAL", (name, ix, H)
            bc = [dict(cycle=c["cycle"], U=c["U"], W=c["W"], xstar=str(c["xstar"]), p=c["p"])
                  for c in lev["comps"] if c["type"] == "b"]
            fb.write(json.dumps(dict(family=name, Q=Q, index=ix, table=tab, b=bc,
                                     cycles=H["cycles"])) + "\n")
        # CERT: deepest and most cycles
        CERT.sort(key=lambda x: -x[1])           # mu closest to 0 first
        deep = []
        for ix, mu, nc, mm in CERT[:400]:
            tab = F.decode(opts, ix)
            try:
                k, nl = twlib.D.stopping_depth(Q, tab, twlib.D.residue_graph(Q, tab))
            except AssertionError:
                k, nl = None, None
            deep.append(dict(index=ix, table=tab, mu=mu, kstar=k, leaves=nl, ncycles=nc))
        deep.sort(key=lambda x: -(x["kstar"] or 0))
        mx = max((x[2] for x in CERT), default=0)
        most = [dict(index=ix, table=F.decode(opts, ix), ncycles=nc, maxmin=mm)
                for ix, mu, nc, mm in CERT if nc == mx][:25]
        top[name] = dict(deepest=deep[:25], most_cycles=most, max_cycles=mx)
        print(name, "B", len(B), "CERT", len(CERT), "max k*", deep[0]["kstar"] if deep else None,
              "max cycles", mx, flush=True)
    json.dump(top, open(os.path.join(HERE, "out", "cert_top.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
