"""Exact completeness bound for the z3 encoding of sat_typeH.py (added after REFEREE1, item 4).

The encoding replaces log2 of each branch multiplier q = u/w by integers:
  * on every non-C edge inside one level it demands psi(s) - psi(r) <= -ceil(SC lq) - 1;
  * for the designated expanding cycle D it demands sum floor(SC lq) > 0.
An UNSAT answer means "no type-(b) member" only if every genuine type-(b) member satisfies
these constraints.  By the theory of difference constraints that holds iff
  (C) every simple contracting cycle (exact multiplier < 1) of length <= Q has
      sum (ceil(SC lq) + 1) <= 0   (so psi exists on the type-(a) SCCs), and
  (E) every simple expanding cycle (exact multiplier > 1) of length <= Q has
      sum floor(SC lq) >= 1        (so the designated cycle is admitted).
A simple cycle of G_m has length <= Q = p^m, and its multiplier depends only on how many
edges of each branch type (u, w) it uses.  This script enumerates EVERY count vector over the
branch types of a row with total length <= Q (a superset of the realisable cycles), decides
the sign of the multiplier exactly with integers, and evaluates (C) and (E) with the very
integers the encoder uses (it imports SC-scaled values from sat_typeH's own formula).

Rows: the six z3 UNSAT rows of README (S3 m = 7, 8; S5 m = 7; S7 m = 6; SPL_d1 m = 5; D27)
and the two m = 6 z3 runs (S3, S5) used only as cross-checks.
For SC = 4096 (the value used in the first run) it also prints the rows where (C) or (E)
fails, which reproduces REFEREE1's finding (S3 m = 8 and D27).
Exit 0 iff every row passes at the SC now set in sat_typeH.py, and the SC = 4096 failure
set (with the realisability caps) is exactly {S3 m=8, D27}; without the caps (crude) S3 m=7 and S5 m=7 also fail at 4096.
"""
import itertools, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import families as FM
import sat_typeH as ST


def rows():
    return {
        "S3_m6": (2, 6, FM.s_family(6, 3)), "S5_m6": (2, 6, FM.s_family(6, 5)),
        "S3_m7": (2, 7, FM.s_family(7, 3)), "S3_m8": (2, 8, FM.s_family(8, 3)),
        "S5_m7": (2, 7, FM.s_family(7, 5)), "S7_m6": (2, 6, FM.s_family(6, 7)),
        "SPL_d1_m5": (2, 5, FM.split_family(5, 1)), "D27": FM.FAMILIES["D27"],
    }


def caps(p, m, opts, types):
    """Necessary conditions for a count vector to be realised by a simple cycle of G_m
    (each class is visited at most once and uses one of its own branches):
      Hall:  for every set T of types, sum_{t in T} n_t <= #classes offering a type in T;
      odd->even (2-adic rows whose non-dividing branches all have u, v odd and sit on odd
      classes): each such step lands on an even class, whose step is a halving, so
      #non-dividing steps <= #halvings."""
    k = len(types)
    offer = [{types.index((u, w)) for (u, v, w) in o} for o in opts]
    hall = []
    for mask in range(1, 2 ** k):
        T = {i for i in range(k) if mask >> i & 1}
        hall.append((T, sum(1 for of in offer if of & T)))
    oddeven = p == 2 and all((r % 2 == 1 and u % 2 == 1 and v % 2 == 1) if w == 1 else
                             (r % 2 == 0 and w == 2) for r, o in enumerate(opts) for (u, v, w) in o)
    nd = [i for i, (u, w) in enumerate(types) if w == 1]
    hv = [i for i, (u, w) in enumerate(types) if w == 2]

    def ok(vec):
        for T, c in hall:
            if sum(vec[i] for i in T) > c:
                return False
        if oddeven and sum(vec[i] for i in nd) > sum(vec[i] for i in hv):
            return False
        return True
    return ok, oddeven


def check(p, m, opts, SC, refined=True):
    Q = p ** m
    types = sorted({(u, w) for o in opts for (u, v, w) in o})
    realisable, _ = caps(p, m, opts, types)
    lq = [math.log2(u) - math.log2(w) for (u, w) in types]       # sat_typeH.Fraction_log
    cw = [math.ceil(SC * x) + 1 for x in lq]
    fw = [int(math.floor(SC * x)) for x in lq]
    worst_c, worst_e = None, None
    k = len(types)

    def rec(i, left, vec):
        nonlocal worst_c, worst_e
        if i == k:
            if sum(vec) == 0 or (refined and not realisable(vec)):
                return
            num = den = 1
            for (u, w), n in zip(types, vec):
                num *= u ** n
                den *= w ** n
            if num < den:
                s = sum(c * n for c, n in zip(cw, vec))
                if worst_c is None or s > worst_c[0]:
                    worst_c = (s, tuple(vec))
            elif num > den:
                s = sum(f * n for f, n in zip(fw, vec))
                if worst_e is None or s < worst_e[0]:
                    worst_e = (s, tuple(vec))
            return
        for n in range(left + 1):
            vec.append(n)
            rec(i + 1, left - n, vec)
            vec.pop()

    rec(0, Q, [])
    ok = (worst_c is None or worst_c[0] <= 0) and (worst_e is None or worst_e[0] >= 1)
    return ok, types, worst_c, worst_e


if __name__ == "__main__":
    allok = True
    SCnow = ST.SC
    print("SC in sat_typeH.py:", SCnow)
    fails = {}
    for name, (p, m, opts) in rows().items():
        for refined in (False, True):
            for SC in (4096, SCnow):
                ok, types, wc, we = check(p, m, opts, SC, refined)
                tag = "refined" if refined else "crude  "
                print(f"{name:10s} {tag} SC={SC:8d} types {types}: max contracting slack {wc}, "
                      f"min expanding slack {we} -> {'complete' if ok else 'NOT complete'}", flush=True)
                if not ok:
                    fails.setdefault((tag.strip(), SC), set()).add(name)
                    if SC == SCnow:
                        allok = False
    for k in sorted(fails):
        print("not complete:", k, sorted(fails[k]))
    allok = allok and fails.get(("refined", 4096)) == {"S3_m8", "D27"}
    print("ALL PASS" if allok else "FAIL")
    sys.exit(0 if allok else 1)
