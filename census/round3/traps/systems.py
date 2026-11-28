"""New systems of the 'traps' lens (round 3).

Each trap system is  T_A(n) = 1            if n mod 2^k is in A,
                     T_A(n) = C_{a,b}(n)   otherwise,
where C_{a,b}(n) = n/2 (n even), a n + b (n odd).  GLOBAL for T_A is the
statement 'every C_{a,b} orbit meets A or is eventually periodic', with the
complete cycle list.  The families FAM_* are statements about every
(a, b) in a congruence class and are listed with a representative.
"""

SYSTEMS = {
    # id: (a, b, k, A, short description)
    "trap7_57":   (7, 1, 3, (5, 7), "7x+1; n = 5,7 mod 8 -> 1"),
    "trap5_17":   (5, 1, 3, (1, 7), "5x+1; n = 1,7 mod 8 -> 1"),
    "trap5_hi16": (5, 1, 4, (9, 11, 13, 15), "5x+1; odd n = 9..15 mod 16 -> 1"),
    "trap5_c13":  (5, 1, 5, (3, 5, 7, 15, 17, 23), "5x+1; n in {3,5,7,15,17,23} mod 32 -> 1"),
    "trap7_m32":  (7, 1, 5, (5, 7, 13, 23, 27), "7x+1; n in {5,7,13,23,27} mod 32 -> 1"),
    "trap3_m32":  (3, 1, 5, (7, 15, 25), "3x+1; n in {7,15,25} mod 32 -> 1"),
}


def make_step(a, b, k, A):
    M = 1 << k
    As = set(A)

    def T(n):
        if n % M in As:
            return 1
        return n // 2 if n % 2 == 0 else a * n + b
    return T


STEP = {sid: make_step(a, b, k, A) for sid, (a, b, k, A, _) in SYSTEMS.items()}

# Families (Theorem F): for every odd a, b >= 1 with (a, b) = (a0, b0) mod 8,
# every positive C_{a,b} orbit meets A or ends in a positive-integer lift of
# a simple cycle of the avoider graph.
FAMILIES = {
    "FAM_4mod8": "all odd a, b: trap A = {4} mod 8",
    "FAM_oddpairs8": "each (a0, b0) mod 8: the two odd pairs listed in family.md",
}
