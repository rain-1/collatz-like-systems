"""Shared driver for check_<id>.py of the eight open systems (partial theorems)."""
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lib import mod_table, check_partial  # noqa: E402
from gen_partial import TARGETS  # noqa: E402


def stopping_time(step, n, cap=10**6):
    x = n
    for s in range(1, cap):
        x = step(x)
        if x < n:
            return s
    return None  # no descent within cap (only used as a lower bound)


def run(name, witness, Ks, min_len):
    """witness(K) is a positive integer in the class of the p-adic point with
    infinite coefficient stopping time; min_len(K) a proved lower bound for its
    stopping time (see the .md).  We check the bound numerically."""
    certs = json.load(open(os.path.join(HERE, "partial_certs.json")))[name]
    sy, mod, cycles = TARGETS[name]
    assert certs["modulus"] == mod
    o, closed, dens = check_partial(name, sy, mod, certs["open"],
                                    Fraction(*certs["density"]), certs["small"],
                                    cycles, [])
    assert closed == certs["closed"]
    step = mod_table(*sy)
    for K in Ks:
        t = stopping_time(step, witness(K))
        assert t is None or t >= min_len(K), (K, t)
    print(f"{name}: PASS  E at modulus {mod}: {len(o)} open classes, density "
          f"{float(dens):.3e}; small exceptions {certs['small']} all periodic; "
          f"witness stopping times >= bound for K in {list(Ks)}")
