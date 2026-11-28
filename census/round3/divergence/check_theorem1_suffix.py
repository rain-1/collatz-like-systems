"""Check for theorem1_suffix.md (Theorem 1: suffix maps).  Exit 0 on success.

Claims tested exactly:
 * the decision procedure terminates on 400 random b-suffix maps x 29 seeds,
 * every 'pump' answer carries a certificate that verify_pump_certificate
   re-checks symbolically (rewrite of each Y_i) and numerically,
 * every 'periodic' answer is confirmed by direct simulation,
 * worked examples: round-2 SFX7 (seed 17) and a non-injective binary map.
"""
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from suffix_maps import SuffixMap, random_suffix_map, decide, verify_pump_certificate, val  # noqa: E402


def confirm_periodic(T, s, t0, per):
    x = s
    for _ in range(t0):
        x = T(x)
    y = x
    for _ in range(per):
        y = T(y)
    assert y == x


def main():
    rng = random.Random(20261127)
    stats = {"pump": 0, "periodic": 0}
    maps = 0
    noninj = 0
    while maps < 400:
        b = rng.choice([2, 3])
        try:
            T = random_suffix_map(b, rng, splits=rng.randint(1, 4), maxout=4)
        except (ValueError, AssertionError):
            continue
        maps += 1
        outs = [bb for _, bb in T.rules]
        # crude non-injectivity witness: two distinct n with equal image
        img = {}
        for n in range(1, 400):
            y = T(n)
            if y in img and img[y] != n:
                noninj += 1
                break
            img[y] = n
        for s in range(1, 30):
            r = decide(T, s, 4000)
            assert r[0] != "unknown", (T.rules, s)
            stats[r[0]] += 1
            if r[0] == "pump":
                verify_pump_certificate(T, s, r)
            else:
                confirm_periodic(T, s, r[1], r[2])
    print("random maps:", maps, "non-injective among them:", noninj, "decisions:", stats)
    assert stats["pump"] > 1000 and stats["periodic"] > 500 and noninj > 100

    # round-2 SFX7 permutation, seed 17
    SFX7 = [("00", "00"), ("001", "100110"), ("00101", "1110"), ("10", "1"),
            ("10101", "10110"), ("11", "010"), ("1101", "000110")]
    T = SuffixMap(2, SFX7)
    r = decide(T, 17)
    assert r[0] == "pump"
    verify_pump_certificate(T, 17, r)
    print("SFX7 seed 17:", r[0], "t0=%d p=%d P=%s V=%s" % (r[1], r[2], r[3], r[5]))

    # a non-injective binary suffix map: 2q->q, 4q+1->8q+6, 4q+3->8q+3
    T = SuffixMap(2, [("0", ""), ("01", "110"), ("11", "011")])
    assert T(2 * 11) == T(4 * 1 + 3) == 11        # non-injective
    found = None
    for s in range(1, 200):
        r = decide(T, s)
        if r[0] == "pump":
            verify_pump_certificate(T, s, r)
            found = found or (s, r)
        else:
            confirm_periodic(T, s, r[1], r[2])
    s, r = found
    print("non-injective example, first divergent seed", s, "t0=%d p=%d P=%s Ys=%s V=%s" % (r[1], r[2], r[3], r[4], r[5]))
    print("OK")


if __name__ == "__main__":
    main()
