"""Regenerate partial_certs.json (descent-tree exceptional sets) for the 8 open systems."""
import json
from lib import *

TARGETS = {
    "split5_1_s27": (SPLIT5_1, 2**24, {1: 5, 13: 35}),
    "split5_3_s27": (SPLIT5_3, 2**32, {1: 4, 3: 2, 5: 5, 61: 10, 125: 11}),
    "m3_b_s8": (M3_B, 3**14, {1: 1}),
    "m3_d_s7": (M3_D, 3**14, {1: 5, 7: 16}),
    "m3_g_s7": (M3_G, 3**12, {4: 5, 8: 5}),
    "div23_5n1_s7": (DIV23_5N1, 6**9, {1: 3}),
    "div235_7n1_s11": (DIV235_7N1, 30**5, {1: 4}),
    "div23_7n1_s5": (DIV23_7N1, 6**8, {1: 4, 19: 34}),
}

if __name__ == "__main__":
    out = {}
    for name, (sy, mod, cyc) in TARGETS.items():
        o, closed, small = descent_tree(sy, mod, small_cap=100000)
        d = density(o)
        out[name] = dict(modulus=mod, open=len(o), closed=closed,
                         density=[d.numerator, d.denominator], density_float=float(d),
                         small=sorted(set(small)))
        print(name, out[name]["open"], float(d), out[name]["small"], flush=True)
    json.dump(out, open("partial_certs.json", "w"), indent=1)
