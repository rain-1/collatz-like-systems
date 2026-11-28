"""catalog.py -- every census system that is a table map on the positive integers.

Loads census/systems.py and every round*/<lens>/systems.py, recovers a table form
(given table, or extract.extract on the step function), reduces it to its minimal modulus,
and attaches the census status of the GLOBAL question:
   open      the id has an open CLS entry asking "Is every positive orbit eventually periodic?"
   settled   otherwise (settled_collatz_questions.txt, or settled in the round folder)
Catalogs skipped on purpose (reason recorded): polynomial (maps of F_q[t]), domains entries
not on N (Gaussian etc.), traps (a constant branch n -> 1), progressions (shortcut forms of
census maps that are already loaded).
"""
import glob
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from extract import extract, minimal_modulus  # noqa: E402

SKIP = {
    "round3/polynomial/systems.py": "maps of F_q[t], not of Z",
    "round3/traps/systems.py": "constant branch n -> 1 (trap systems; decided by traps/)",
    "round3/progressions/systems.py": "shortcut forms of census maps already loaded",
}

LOCAL = ("systems", "families", "mixedlib", "pairlib", "accel_lib", "decide", "plib",
         "density_lib", "descent_lib", "rcwa", "lib")


def open_global_ids():
    txt = open(os.path.join(CENSUS, "open_collatz_systems.txt")).read()
    out = {}
    cur = None
    for line in txt.splitlines():
        m = re.match(r"^(CLS-\d+)\s+(\S+)", line)
        if m:
            cur = (m.group(1), m.group(2))
            continue
        if cur and line.strip().startswith("Open question:"):
            if "eventually periodic" in line:
                out.setdefault(cur[1], []).append(cur[0])
            cur = None
    return out


def settled_ids():
    txt = open(os.path.join(CENSUS, "settled_collatz_questions.txt")).read()
    out = {}
    for line in txt.splitlines():
        m = re.match(r"^([A-Za-z0-9_]+)\s{2,}(\S.*)$", line)
        if m and not line.startswith(" "):
            out.setdefault(m.group(1), m.group(2).strip())
    return out


def load_module(path):
    d = os.path.dirname(path)
    for k in list(sys.modules):
        if k in LOCAL:
            del sys.modules[k]
    sys.path.insert(0, d)
    try:
        spec = importlib.util.spec_from_file_location("systems", path)
        m = importlib.util.module_from_spec(spec)
        sys.modules["systems"] = m
        spec.loader.exec_module(m)
    finally:
        sys.path.remove(d)
    return m


def entries():
    files = sorted(glob.glob(os.path.join(CENSUS, "systems.py")) +
                   glob.glob(os.path.join(CENSUS, "round*", "*", "systems.py")))
    out, skipped = [], []
    for f in files:
        rel = os.path.relpath(f, CENSUS)
        if rel in SKIP:
            skipped.append((rel, SKIP[rel]))
            continue
        m = load_module(f)
        S = getattr(m, "SYSTEMS")
        items = list(S.items()) if isinstance(S, dict) else [(s.get("id"), s) for s in S]
        for sid, s in items:
            dom = s.get("domain", "N")
            if dom not in ("N", "N+", "Z>0", "positive integers") and "dress" not in str(sid):
                if rel.startswith("round3/domains") or dom not in ("N0",):
                    skipped.append((f"{rel}:{sid}", f"domain {dom}"))
                    continue
            out.append(dict(id=sid, source=rel, rule=s.get("rule", ""), step=s.get("step"),
                            table=s.get("table"), Q=s.get("Q"), p=s.get("p"), m=s.get("m"),
                            domain=dom, status_field=s.get("status")))
    return out, skipped


def table_of(e):
    """(Q, table, exceptions, how) or None."""
    if e["table"] is not None:
        tab = [tuple(t) for t in e["table"]]
        Q = e["Q"] or len(tab)
        assert len(tab) == Q
        Q2, t2 = minimal_modulus(Q, tab)
        # cross-check against the step function
        exc = []
        if e["step"] is not None:
            for n in range(1, 5000):
                u, v, w = t2[n % Q2]
                try:
                    y = e["step"](n)
                except Exception:
                    y = None
                if y is None or y * w != u * n + v:
                    exc.append(n)
        return Q2, t2, exc, "given"
    if e["step"] is None:
        return None
    try:
        r = extract(e["step"])
    except Exception:
        r = None
    if r is None:
        return None
    Q2, t2 = minimal_modulus(r["Q"], r["table"])
    return Q2, t2, r["exceptions"], "extracted"


if __name__ == "__main__":
    es, sk = entries()
    print(len(es), "entries;", len(sk), "skipped")
    og = open_global_ids()
    print("open GLOBAL ids:", len(og))
