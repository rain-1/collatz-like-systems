"""One- and two-class modifications of the open census table maps that are of type (b)
(provable by Theorem H while keeping an expanding cycle).

Open maps: round3/dichotomy/open_tables.py (OPEN), restricted to single-prime moduli
(the div23_* / div235_* maps are mixed-base and are not unit-multiplier p-adic systems).
Each map (Q, table) is lifted to Q' = Q p^j and the branch on one class (or two classes)
mod Q' is replaced by a branch from the menu
    (u', v', p^e')  with  1 <= u' <= u (u' a p-unit), 0 <= e' <= 2, every target residue
    t mod Q'/p^e' realised once, v' the integer of least absolute value realising t,
    exact on the class and keeping T(Z>0) in Z>0.
So the menu contains damping (u' < u), resets, shifts (u' = u, v' changed) and extra
divisions.  Every modified table is classified exactly (tblib); every type-(b) table is
settled with prove_H (complete cycle list) and its proof object written to data/.

Usage: python mods.py ONE|TWO [maxQ] [comma-separated name prefixes]       output: data/mods_<mode>.json, printed table
"""
import sys, os, json, math, itertools, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "round3", "dichotomy"))
import tblib as TB
from open_tables import OPEN


def prime_of(Q):
    p = 2
    while Q % p:
        p += 1
    q = Q
    while q % p == 0:
        q //= p
    return p if q == 1 else None


def lift(Q, tab, Q2):
    return [tuple(tab[r % Q]) for r in range(Q2)]


def menu(p, Q2, r, br):
    u, v, w = br
    out = []
    for u2 in range(1, u + 1):
        if u2 % p == 0:
            continue
        for e2 in range(0, 3):
            w2 = p ** e2
            if Q2 % w2:
                continue
            M = Q2 // w2
            seen = set()
            # v2 ranges over a window wide enough to realise every target t mod M
            cands = sorted(range(-w2 * M - 2 * Q2, w2 * M + 2 * Q2 + 1), key=abs)
            for v2 in cands:
                if (u2 * r + v2) % w2:
                    continue
                t = ((u2 * r + v2) // w2) % M
                if t in seen:
                    continue
                n0 = r if r else Q2
                if u2 * n0 + v2 < w2:
                    continue
                seen.add(t)
                b2 = (u2, v2, w2)
                if b2 != tuple(br):
                    out.append(b2)
                if len(seen) == M:
                    break
    return out


def classify_tab(p, m, tab):
    try:
        TB.check_table(p, m, tab)
    except AssertionError:
        return "inadmissible"
    return TB.verdict(TB.classify(p, m, tab, weights=False))


def job(args):
    name, p, m, base, mods = args
    tab = list(base)
    for r, b in mods:
        tab[r] = b
    v = classify_tab(p, m, tab)
    if v != "b":
        return name, v, None
    P = TB.prove_H(p, m, tab)
    if P is None:
        return name, "b-unsettled", None
    return name, "b", dict(mods=mods, cycles=[c[0] for c in P["cycles"]],
                           proof=TB.to_json(P, f"{name} mods {mods}"),
                           expanding=[str(c["xstar"][0]) for c in P["comps"] if c["kind"] == "b"])


def main(mode, maxQ, only=None):
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    results = {}
    tasks = []
    seen_base = set()
    for name, (Q, tab) in OPEN.items():
        p = prime_of(Q)
        if p is None or (only and not any(name.startswith(o) for o in only)):
            continue
        for j in (1, 2, 3):
            Q2 = Q * p ** j
            if Q2 > maxQ:
                break
            m = round(math.log(Q2, p))
            assert p ** m == Q2
            base = lift(Q, tab, Q2)
            key = (Q2, tuple(base))
            if key in seen_base:
                continue
            seen_base.add(key)
            menus = [menu(p, Q2, r, base[r]) for r in range(Q2)]
            label = f"{name}@{Q2}"
            if mode == "ONE":
                for r in range(Q2):
                    for b in menus[r]:
                        tasks.append((label, p, m, base, ((r, b),)))
            else:
                for r1, r2 in itertools.combinations(range(Q2), 2):
                    for b1 in menus[r1]:
                        for b2 in menus[r2]:
                            tasks.append((label, p, m, base, ((r1, b1), (r2, b2))))
    print("tasks", len(tasks), flush=True)
    t0 = time.time()
    with Pool(10) as pool:
        for name, v, rec in pool.imap_unordered(job, tasks, chunksize=200):
            R = results.setdefault(name, dict(counts={}, typeb=[]))
            R["counts"][v] = R["counts"].get(v, 0) + 1
            if rec is not None:
                R["typeb"].append(rec)
    for name, R in results.items():
        print(f"{name:32s} {R['counts']}", flush=True)
    json.dump(results, open(os.path.join(HERE, "data", f"mods_{mode}_{maxQ}.json"), "w"))
    print(f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 64,
         sys.argv[3].split(",") if len(sys.argv) > 3 else None)
