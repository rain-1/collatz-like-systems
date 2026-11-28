#!/usr/bin/env python3
"""check_famscan.py -- independent check of the C scanner against decide.py and twlib.

For every family in families.FAMILIES, draw N random members (default 300), run famscan in
'printall' mode on exactly those members, and compare each verdict with
   decide.py (round 3, exact):           CERT  <=>  famscan CERT
   twlib.classify_level (exact, Python): SCC type string -> CERT / B / C / Z
and, for CERT members whose cycle count famscan reports, with the complete cycle list of
decide.py.  Exits 1 on any disagreement.  Runtime ~2-4 minutes.
"""
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import families as F  # noqa: E402
import twlib  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 300


def run_members(Q, opts, members):
    """Run famscan on an explicit list of tables: a family whose option lists are singletons."""
    out = []
    for tab in members:
        spec = F.spec_text(Q, [[t] for t in tab], 0)
        p = subprocess.run([os.path.join(HERE, "famscan"), "printall"], input=spec,
                           capture_output=True, text=True, check=True)
        lines = p.stdout.strip().splitlines()
        body = [l for l in lines if not l.startswith("SUMMARY")]
        assert len(body) == 1, lines
        out.append(body[0].split())
    return out


def tw_code(Q, tab):
    lev = twlib.classify_level(Q, tab, Q)
    t = lev["types"]
    if "z" in t:
        return "Z"
    if "c" in t:
        return "C"
    if "b" in t:
        return "B"
    return "CERT"


def main():
    rnd = random.Random(20261128)
    bad = 0
    tested = 0
    for name, mode, cnt in F.FAMILIES:
        Q, opts = F.family(name)
        members = [[rnd.choice(o) for o in opts] for _ in range(N)]
        res = run_members(Q, opts, members)
        for tab, r in zip(members, res):
            code = r[0]
            tested += 1
            if code == "FALLBACK":
                continue
            tc = tw_code(Q, tab)
            if code == "ZN":
                code = "Z"
            if tc != code:
                print("MISMATCH twlib", name, tab, code, tc)
                bad += 1
            if tc != "Z":
                d = twlib.D.decide(Q, tab, want_cycles=(code == "CERT"), want_depth=False)
                if (d["verdict"] == "CERT") != (code == "CERT"):
                    print("MISMATCH decide", name, tab, code, d["verdict"])
                    bad += 1
                if code == "CERT" and int(r[3]) >= 0 and "cycles" in d:
                    if int(r[3]) != len(d["cycles"]):
                        print("MISMATCH cycles", name, tab, r[3], len(d["cycles"]))
                        bad += 1
        print(f"{name}: {N} members compared", flush=True)
    print("tested", tested, "mismatches", bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
