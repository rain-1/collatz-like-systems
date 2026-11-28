"""Systems studied by the round-3 'deep' lens.

All maps are on positive integers.  The basic family is

    SPLIT(a, b, d):  n even -> n/2 ;  n = 1 mod 4 -> a n + d ;  n = 3 mod 4 -> b n + d

with a, b, d odd and positive.  Catalog members: split_d = SPLIT(3,1,d),
splitB_d = SPLIT(1,3,d), split5_d = SPLIT(5,1,d).  Every member of the family
table in family.md is available as SYSTEMS["split_a{a}_b{b}_d{d}"].

The parity map PAR(c, e): x even -> x/2, x odd -> (c x + e)/2 (the accelerated
'cx+e' map) is used for the exact conjugacies of class K (family.md, Theorem K).
"""


def split_step(a, b, d):
    def step(n):
        if n % 2 == 0:
            return n // 2
        return a * n + d if n % 4 == 1 else b * n + d
    step.__name__ = f"split_a{a}_b{b}_d{d}"
    return step


def par_step(c, e):
    """Accelerated parity map; e must have the parity making c x + e even for odd x."""
    def step(x):
        if x % 2 == 0:
            return x // 2
        y = c * x + e
        assert y % 2 == 0
        return y // 2
    step.__name__ = f"par_acc_{c}_{e}"
    return step


SYSTEMS = {}
for a in (1, 3, 5, 7):
    for b in (1, 3, 5, 7):
        for d in range(1, 16, 2):
            SYSTEMS[f"split_a{a}_b{b}_d{d}"] = dict(
                rule=f"even n -> n/2; n=1 mod 4 -> {a}n+{d}; n=3 mod 4 -> {b}n+{d}",
                step=split_step(a, b, d), a=a, b=b, d=d)

# certifiable members used in basins.md (d up to 199)
for (a, b) in [(1, 1), (3, 1), (1, 3)]:
    for d in range(1, 200, 2):
        key = f"split_a{a}_b{b}_d{d}"
        if key not in SYSTEMS:
            SYSTEMS[key] = dict(
                rule=f"even n -> n/2; n=1 mod 4 -> {a}n+{d}; n=3 mod 4 -> {b}n+{d}",
                step=split_step(a, b, d), a=a, b=b, d=d)
