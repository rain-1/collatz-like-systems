"""Exhaustive type scan of the choice families in families.py, and Theorem-H settlement of
every type-(b) member found.

For each member: verdict of the level-m SCC classification (tblib.classify; level m
suffices because type (c) is level independent, round3/accel/trichotomy.md Lemma L, and
types (a)/(b) lift: the lift of an (a) SCC has only contracting cycles, and the lift of an
isolated expanding cycle is the periodic point's residue cycle plus transient nodes).
Verdicts: a (CERT), b (no type c, some isolated expanding cycle), c, divfree (some
division-free cycle: standing hypothesis fails), unknown (float margin; none expected).

Every type-(b) member is then settled with tblib.prove_H (exact) and its cycle list
recorded; the proof objects of all of them are written to data/<family>_H.json (or a
sample of 200 plus the cycle lists if there are more), and verify_H.py re-checks them.

Usage: python scan.py FAMILY [FAMILY ...]   (writes data/scan_<FAMILY>.json)
"""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tblib as TB
import families as FM

CHUNK = 2000


def work(args):
    name, lo, hi = args
    p, m, opts = FM.FAMILIES[name]
    cnt, bs = {}, []
    for idx in range(lo, hi):
        tab = FM.table_at(opts, idx)
        try:
            TB.check_table(p, m, tab)
        except AssertionError:
            cnt["inadmissible"] = cnt.get("inadmissible", 0) + 1
            continue
        v = TB.verdict(TB.classify(p, m, tab, weights=False))
        cnt[v] = cnt.get(v, 0) + 1
        if v == "b":
            bs.append(idx)
    return cnt, bs


def settle(args):
    name, idx = args
    p, m, opts = FM.FAMILIES[name]
    tab = FM.table_at(opts, idx)
    P = TB.prove_H(p, m, tab)
    if P is None:
        return idx, None, None
    return idx, [c[0] for c in P["cycles"]], TB.to_json(P, f"{name}#{idx}")


def main(names):
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    with Pool(10) as pool:
        for name in names:
            p, m, opts = FM.FAMILIES[name]
            N = FM.n_members(opts)
            t0 = time.time()
            tasks = [(name, lo, min(N, lo + CHUNK)) for lo in range(0, N, CHUNK)]
            cnt, bs = {}, []
            for c, b in pool.imap_unordered(work, tasks):
                for k, v in c.items():
                    cnt[k] = cnt.get(k, 0) + v
                bs += b
            bs.sort()
            res = list(pool.imap(settle, [(name, i) for i in bs], chunksize=20))
            failed = [i for i, cy, _ in res if cy is None]
            cyc_lists = {}
            for i, cy, _ in res:
                if cy is not None:
                    cyc_lists.setdefault(json.dumps(cy), []).append(i)
            proofs = [P for _, cy, P in res if cy is not None]
            if len(proofs) > 5000:
                step = len(proofs) / 200
                proofs = [proofs[int(k * step)] for k in range(200)]
            json.dump(proofs, open(os.path.join(HERE, "data", f"{name}_H.json"), "w"))
            summ = dict(family=name, p=p, m=m, members=N, counts=cnt, typeb=len(bs),
                        settle_failed=failed,
                        cycle_lists={k: len(v) for k, v in cyc_lists.items()},
                        typeb_indices=bs if len(bs) <= 5000 else bs[:5000],
                        seconds=round(time.time() - t0, 1))
            json.dump(summ, open(os.path.join(HERE, "data", f"scan_{name}.json"), "w"))
            print(name, N, cnt, "typeb", len(bs), "settle_failed", len(failed),
                  "cycle lists", dict(list(summ["cycle_lists"].items())[:6]),
                  f"{summ['seconds']}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
