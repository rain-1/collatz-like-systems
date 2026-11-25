"""Round 2, literature lens: Collatz-like systems with a published theorem.

Same style as census/systems.py: each entry is a dict with id, rule, step,
seed, plus the single precise question asked of it (`question`) and the
literature source (`source`). Every step is an exact integer map on the
positive integers.
"""


def farkas_G(m):
    """Farkas's map F'(x) on odd x, written on m = (x+1)/2 in N+.
    F'(x) = x/3 if 3|x; (x+1)/2 if x = 1 mod 4; (3x+1)/2 if x = 3 mod 4
    (Farkas 2005).  With x = 2m-1:  F'(2m-1) = 2 G(m) - 1."""
    if m % 3 == 2:
        return (m + 1) // 3
    if m % 2 == 1:
        return (m + 1) // 2
    return 3 * m // 2


def farkas_Fprime(x):
    """Farkas's original map on odd positive integers (for the conjugacy check)."""
    assert x % 2 == 1
    if x % 3 == 0:
        return x // 3
    if x % 4 == 1:
        return (x + 1) // 2
    return (3 * x + 1) // 2


def avoid(K):
    """Collatz map C (n/2, 3n+1) except that n = k mod 8 for k in K is sent to 1.
    'Every orbit reaches 1' <=> every C-trajectory reaches 1 or meets a class in K
    (the residue-class avoidance questions of Yolcu-Aaronson-Heule, Sec. 4.5)."""
    K = frozenset(K)

    def step(n):
        if n % 8 in K:
            return 1
        return n // 2 if n % 2 == 0 else 3 * n + 1
    return step


def T(n):
    """Accelerated Collatz map: n/2 or (3n+1)/2."""
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def perm1932(n):
    """Collatz's 1932 permutation in the catalog's direction (= perm_1932_s8):
    3q -> 2q, 3q+1 -> 4q+1, 3q+2 -> 4q+3.  Simons (2022) calls it P(1,3,2,2)."""
    q, r = divmod(n, 3)
    return 2 * q if r == 0 else 4 * q + 1 if r == 1 else 4 * q + 3


SYSTEMS = [
    dict(id="farkas2005", family="literature",
         rule="m=2 mod 3 -> (m+1)/3; else m odd -> (m+1)/2; else m even -> 3m/2  "
              "(Farkas's F' on x=2m-1)",
         step=farkas_G, seed=14,
         question="GLOBAL: does every orbit reach the fixed point 1?",
         source="H. M. Farkas, Variants of the 3N+1 conjecture and multiplicative "
                "semigroups, Contemp. Math. 387 (2005) 121-127, Thm 1; "
                "Yolcu-Aaronson-Heule 2021/23, Thm 4.2"),
    dict(id="yah_avoid6", family="literature",
         rule="n=6 mod 8 -> 1; else even n -> n/2; else odd n -> 3n+1",
         step=avoid({6}), seed=27,
         question="GLOBAL: does every orbit enter the cycle {1,4,2}?",
         source="Yolcu-Aaronson-Heule, Prop. 4.7 / Thm 4.10"),
    dict(id="yah_avoid15", family="literature",
         rule="n=1 or 5 mod 8 -> 1; else even n -> n/2; else odd n -> 3n+1",
         step=avoid({1, 5}), seed=27,
         question="GLOBAL: does every orbit reach the fixed point 1?",
         source="Yolcu-Aaronson-Heule, remark after Conj. 4.14"),
    dict(id="yah_avoid57", family="literature",
         rule="n=5 or 7 mod 8 -> 1; else even n -> n/2; else odd n -> 3n+1",
         step=avoid({5, 7}), seed=27,
         question="GLOBAL: does every orbit enter the cycle {1,4,2}? "
                  "(= Yolcu-Aaronson-Heule Conjecture 4.14)",
         source="Yolcu-Aaronson-Heule, Conj. 4.14 and Prop. 4.15"),
    dict(id="steiner_1cycle", family="literature",
         rule="even n -> n/2; odd n -> (3n+1)/2",
         step=T, seed=27,
         question="CYCLES restricted to one local minimum: list every cycle "
                  "consisting of one maximal block of odd terms followed by one "
                  "block of even terms",
         source="R. P. Steiner, A theorem on the Syracuse problem, Proc. 7th "
                "Manitoba Conf. Numer. Math. (1977) 553-559; Rhin 1987"),
    dict(id="perm1932_1cycle", family="literature",
         rule="3q -> 2q; 3q+1 -> 4q+1; 3q+2 -> 4q+3",
         step=perm1932, seed=8,
         question="CYCLES restricted to one local minimum: list every cycle "
                  "with exactly one maximal block of non-multiples of 3",
         source="J. L. Simons, Cycles and divergent trajectories for a class of "
                "permutation sequences, arXiv:2205.10582 (2022), Cor. 11(a); "
                "Rhin 1987"),
]

BY_ID = {s["id"]: s for s in SYSTEMS}


def get(id):
    return BY_ID[id]
