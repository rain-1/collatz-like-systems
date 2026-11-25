"""Round 2, rewriting lens: systems in the same style as census/systems.py.

The first eight entries restate round-1 systems whose GLOBAL question was open;
this lens contributes PARTIAL results for them (see <id>.md).  farkas5m_s27 is new.
"""


def mod_table(m, table):
    """table[r] = (u, v, w): n = r mod m  ->  (u*n + v) // w, exact division."""
    def step(n):
        u, v, w = table[n % m]
        x = u * n + v
        assert x % w == 0, (n, m)
        return x // w
    return step


def div_else(primes, a, d):
    def step(n):
        for q in primes:
            if n % q == 0:
                return n // q
        return a * n + d
    return step


def split5(d):
    return lambda n: n // 2 if n % 2 == 0 else 5 * n + d if n % 4 == 1 else n + d


SYSTEMS = []


def add(id, family, rule, step, seed, question="GLOBAL"):
    SYSTEMS.append(dict(id=id, family=family, rule=rule, step=step, seed=seed,
                        question=question))


add("split5_1_s27", "split", "even n -> n/2; n=1 mod 4 -> 5n+1; n=3 mod 4 -> n+1", split5(1), 27)
add("split5_3_s27", "split", "even n -> n/2; n=1 mod 4 -> 5n+3; n=3 mod 4 -> n+3", split5(3), 27)
add("m3_b_s8", "mod3", "3|n -> n/3; n=1 -> (4n-1)/3; n=2 -> (4n+1)/3",
    mod_table(3, [(1, 0, 3), (4, -1, 3), (4, 1, 3)]), 8)
add("m3_d_s7", "mod3", "3|n -> n/3; n=1 -> 4n+2; n=2 -> 4n+1",
    mod_table(3, [(1, 0, 3), (4, 2, 1), (4, 1, 1)]), 7)
add("m3_g_s7", "mod3", "3|n -> n/3; n=1 -> 5n+1; n=2 -> 5n+2",
    mod_table(3, [(1, 0, 3), (5, 1, 1), (5, 2, 1)]), 7)
add("div23_5n1_s7", "mixed", "2|n -> n/2; else 3|n -> n/3; else 5n+1", div_else([2, 3], 5, 1), 7)
add("div235_7n1_s11", "mixed", "2|n -> n/2; else 3|n -> n/3; else 5|n -> n/5; else 7n+1",
    div_else([2, 3, 5], 7, 1), 11)
add("div23_7n1_s5", "mixed", "2|n -> n/2; else 3|n -> n/3; else 7n+1", div_else([2, 3], 7, 1), 5)

# ---- new -------------------------------------------------------------------
add("farkas5m_s27", "farkas",
    "n=3 mod 5 -> (n+2)/5; else even n -> n/2; else (5n-3)/2",
    mod_table(10, [(1, 0, 2), (5, -3, 2), (1, 0, 2), (1, 2, 5), (1, 0, 2),
                   (5, -3, 2), (1, 0, 2), (5, -3, 2), (1, 2, 5), (5, -3, 2)]), 27)
