"""Cross-check: every step function in systems.py equals the table used in the check scripts
(on 0/1 <= n < 30000) and maps its domain into itself.  Runs in a few seconds."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from systems import SYSTEMS
from mixedlib import step_fn
from pairlib import Pairing
import check_sparse, check_single_class, check_relatives

tables = {
    "mb_pair_3_9p": Pairing(3, 2, 1).T, "mb_pair_3_9m": Pairing(3, 2, -1).T,
    "mb_pair_7_7m": Pairing(7, 1, -1).T, "mb_pair_5_5m": Pairing(5, 1, -1).T,
    "mb_pair_3_27m": Pairing(3, 3, -1).T, "mb_pair_5_25p": Pairing(5, 2, 1).T,
    "mb_s3_3": step_fn(*check_single_class.table(3, 2, 1, 3)),
    "mb_s3_9": step_fn(*check_single_class.table(9, 8, 1, 3)),
    "mb_s3_27": step_fn(*check_single_class.table(27, 26, 1, 3)),
    "mb_s5_5": step_fn(*check_single_class.table(5, 3, 2, 5)),
    "mb_s7_7": step_fn(*check_single_class.table(7, 4, 3, 7)),
}
for sid, a, m, R in check_sparse.SYSTEMS:
    tables[sid] = step_fn(*check_sparse.table(a, m, set(R)))
for sid, bM, row, q, R in check_relatives.NAMED:
    tables[sid] = step_fn(*check_relatives.build(bM, row, q, R))

for s in SYSTEMS:
    T = tables[s["id"]]
    lo = 0 if s["domain"] == "N0" else 1
    for n in range(lo, 30000):
        y = s["step"](n)
        assert y == T(n), (s["id"], n)
        assert y >= lo, (s["id"], n)
print("systems.py agrees with the check tables for", len(SYSTEMS), "systems; ALL OK")
