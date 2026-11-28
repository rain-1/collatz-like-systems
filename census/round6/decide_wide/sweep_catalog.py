#!/usr/bin/env python3
"""sweep_catalog.py -- run the harness on every table map in the census catalogs.

Output: out/catalog_sweep.json (one record per distinct table, with all ids that share it)
        out/catalog_sweep.txt  (one line per distinct table)
Runtime: a few minutes (use nice).  Per-table time limit 240 s (recorded as TIMEOUT).
"""
import json
import math
import os
import signal
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import catalog  # noqa: E402
import twlib  # noqa: E402


class TO(Exception):
    pass


def _alarm(sig, frm):
    raise TO()


def key_of(Q, tab):
    return f"{Q}:{tab}"


def jsonable(x):
    if isinstance(x, float):
        return x if math.isfinite(x) else str(x)
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, (int, str)) or x is None:
        return x
    return str(x)


def main():
    es, skipped = catalog.entries()
    og = catalog.open_global_ids()
    st = catalog.settled_ids()
    groups = {}
    nontable = []
    for e in es:
        t = catalog.table_of(e)
        if t is None:
            nontable.append((e["id"], e["source"], e["rule"]))
            continue
        Q, tab, exc, how = t
        k = key_of(Q, tab)
        # Revision after REFEREE1: the round-3 zcore_* maps are written in the coordinate
        # z = (n-1)/2 >= 0 and live on N0 ("GLOBAL (on z >= 0)"); reading them on the positive
        # integers made zcore_3_7 / zcore_3_17 fail positivity and stay unclassified.
        zero = e["domain"] == "N0" or exc == [1] or e["id"].startswith("zcore_")
        k = k + (":N0" if zero else "")
        g = groups.setdefault(k, dict(Q=Q, table=tab, ids=[], exceptions=exc, how=how, zero=zero,
                                      rules=[], open_cls=[], settled_note=[]))
        g["ids"].append(f"{e['id']}@{e['source']}")
        g["rules"].append(e["rule"])
        if e["id"] in og:
            g["open_cls"] += og[e["id"]]
        if e["id"] in st:
            g["settled_note"].append(st[e["id"]])
        if e.get("status_field"):
            g["settled_note"].append(f"status field: {e['status_field']}")
    signal.signal(signal.SIGALRM, _alarm)
    recs = []
    fout = open(os.path.join(HERE, "out", "catalog_sweep.txt"), "w")
    for k, g in groups.items():
        t0 = time.time()
        signal.alarm(240)
        try:
            res = twlib.analyse(g["Q"], g["table"], maxnodes=600, zero=g["zero"])
            s = twlib.summary(res)
            if "H" in res and res["H"]["status"] == "GLOBAL":
                s["H_cycles"] = res["H"]["cycles"]
            if "decide" in res and res["decide"].get("cycles"):
                s["cycles"] = res["decide"]["cycles"]
        except TO:
            s = dict(error="TIMEOUT")
        except Exception as ex:  # recorded, not hidden
            s = dict(error=repr(ex)[:300])
        signal.alarm(0)
        g2 = {kk: vv for kk, vv in g.items()}
        g2["result"] = s
        g2["seconds"] = round(time.time() - t0, 2)
        recs.append(g2)
        line = (f"{'OPEN ' + ','.join(sorted(set(g['open_cls']))) if g['open_cls'] else 'settled':28s} "
                f"Q={g['Q']:<5d} {s.get('decide', '-'):5s} types={s.get('types')} H={s.get('H', '-')} "
                f"t1={s.get('theta1')} tr={s.get('theta_run')} gap={s.get('gap')} drift={s.get('drift')} "
                f"exc={g['exceptions'][:5]} ids={g['ids'][:4]}{'...' if len(g['ids']) > 4 else ''} "
                f"{s.get('error', '')}")
        print(line, flush=True)
        fout.write(line + "\n")
        fout.flush()
    json.dump(dict(records=jsonable(recs), nontable=nontable, skipped=skipped),
              open(os.path.join(HERE, "out", "catalog_sweep.json"), "w"), indent=1)
    print(len(recs), "distinct tables;", len(nontable), "non-table entries;", len(skipped), "skipped")


if __name__ == "__main__":
    main()
