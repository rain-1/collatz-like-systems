"""Breakdown of the bounded first returns found by search_nonunit.py (Revision after REFEREE1,
fix 6).  Lists every (B, M_Y, r_Y) with a bounded first return, and classifies it as
 - 'pairing' : B is a Farkas pairing system P(a, K, x*),
 - 'dressed' : B is a dressed system,
and checks that r_Y = 0 and that the canonical return is not a unit p-adic table.
Exits 1 if the counts differ from the expected ones (24 pairing + 7 dressed at M_Y <= 144).
usage: python3 nonunit_breakdown.py [maxM]   (default 144, about the run time of search_nonunit)
"""
import os
import sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import search_nonunit as sn  # noqa
from transport_lib import induced_canonical, is_unit_padic  # noqa

EXPECTED = {144: {'pairing': 24, 'dressed': 7}, 48: None}


def main(maxM):
    rows = []
    for B in sn.population():
        for MY in sn.moduli(maxM):
            for rY in range(MY):
                try:
                    canon, pcs, st = induced_canonical(B['Q'], B['table'], MY, rY, tmax=30,
                                                       pmax=4000, Lmax=1 << 14)
                except (AssertionError, ZeroDivisionError):
                    continue
                if st != 'ok' or canon is None:
                    continue
                kind = 'pairing' if B['id'].startswith('P(') else 'dressed'
                unit = canon[0] != 1 and is_unit_padic(*canon) is not None
                rows.append((kind, B['id'], MY, rY, unit))
    for r in rows:
        print(*r)
    cnt = Counter(r[0] for r in rows)
    print("counts:", dict(cnt), "total", len(rows))
    bad = [r for r in rows if r[3] != 0 or r[4]]
    if bad:
        print("FAIL: return to a nonzero class or a unit table:", bad)
        return 1
    exp = EXPECTED.get(maxM)
    if exp is not None and dict(cnt) != exp:
        print("FAIL: expected", exp)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 144))
