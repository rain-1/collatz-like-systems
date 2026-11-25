"""Round 2, lens 'descent': systems at and around the descent-certificate
frontier.  Same style as census/systems.py: a list of dicts with id, rule,
step, seed, plus the residue table used by the checks.

Families (see lemmas.md):
  SPLIT(a,b,d)  even -> n/2; n=1 mod 4 -> a n + d; n=3 mod 4 -> b n + d
  M3(a,c1,b,c2) 3|n -> n/3; n=1 mod 3 -> a n + c1; n=2 mod 3 -> b n + c2
  S-family      even -> n/2; odd n -> 3n + d if n mod 2^m in S, else n + d
"""

SYSTEMS = []

S0 = (1, 3, 5, 7, 11, 13, 15, 17, 21, 23, 25, 29)   # 12 of the 16 odd classes mod 32


def mod_table(Q, table):
    def step(n):
        u, v, w = table[n % Q]
        x = u * n + v
        assert x % w == 0
        return x // w
    return step


def s_table(m, S, d=1):
    Q = 2 ** m
    return [(1, 0, 2) if r % 2 == 0 else ((3, d, 1) if r in S else (1, d, 1))
            for r in range(Q)]


def add(id, question, rule, p, m, table, seed):
    SYSTEMS.append(dict(id=id, question=question, rule=rule, p=p, m=m,
                        table=table, step=mod_table(p ** m, table), seed=seed))


add("desc_split7_1", "GLOBAL",
    "even n -> n/2; n=1 mod 4 -> 7n+1; n=3 mod 4 -> n+1",
    2, 2, [(1, 0, 2), (7, 1, 1), (1, 0, 2), (1, 1, 1)], 27)

add("desc_m3_4n5", "GLOBAL",
    "3|n -> n/3; n=1 mod 3 -> 4n+5; n=2 mod 3 -> 2n+2",
    3, 1, [(1, 0, 3), (4, 5, 1), (2, 2, 1)], 7)

add("desc_s8_35", "GLOBAL",
    "even n -> n/2; n=3,5 mod 8 -> 3n+1; n=1,7 mod 8 -> n+1",
    2, 3, s_table(3, (3, 5)), 27)

add("desc_s32_max", "GLOBAL",
    "even n -> n/2; odd n -> 3n+1 if n mod 32 in {1,3,5,7,11,13,15,17,21,23,25,29}, "
    "else (n = 9,19,27,31 mod 32) n+1",
    2, 5, s_table(5, S0), 27)

add("desc_s32_d65", "CYCLES",
    "even n -> n/2; odd n -> 3n+65 if n mod 32 in {1,3,5,7,11,13,15,17,21,23,25,29}, "
    "else (n = 9,19,27,31 mod 32) n+65",
    2, 5, s_table(5, S0, 65), 27)

add("desc_s32_plus9", "GLOBAL",
    "even n -> n/2; odd n -> 3n+1 if n mod 32 in {1,3,5,7,9,11,13,15,17,21,23,25,29}, "
    "else (n = 19,27,31 mod 32) n+1",
    2, 5, s_table(5, S0 + (9,)), 27)

BY_ID = {s["id"]: s for s in SYSTEMS}


def get(id):
    return BY_ID[id]
