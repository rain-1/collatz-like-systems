"""Catalog of Collatz-like systems for the difficulty census.

Every system is a map on the positive integers given by `step`. Each has a
designated `seed`. Two questions are asked of every system:

  FATE    What happens to the forward orbit of the seed? Exactly one of:
          returns to the seed / enters a cycle not containing the seed /
          is infinite (all terms distinct).
  GLOBAL  Is every positive orbit eventually periodic?

Use get(id) to obtain a system; SYSTEMS lists them all in order.
"""


def parity(a, d):
    return lambda n: n // 2 if n % 2 == 0 else a * n + d


def mod_table(m, table):
    """table[r] = (u, v, w): n = r mod m  ->  (u*n + v) // w, exact division."""
    def step(n):
        u, v, w = table[n % m]
        x = u * n + v
        assert x % w == 0, (n, m)
        return x // w
    return step


def div_else(primes, a, d):
    """Divide by the first listed prime dividing n; otherwise a*n + d."""
    def step(n):
        for q in primes:
            if n % q == 0:
                return n // q
        return a * n + d
    return step


def farkas(n):
    if n == 1:
        return 1
    if n % 3 == 1:
        return (n - 1) // 3
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


SYSTEMS = []


def add(id, family, rule, step, seed):
    SYSTEMS.append(dict(id=id, family=family, rule=rule, step=step, seed=seed))


# ---- parity maps: even n -> n/2, odd n -> a*n + d -------------------------
for a, d, seed in [(1, 1, 27), (1, 5, 27), (2, 1, 27), (3, 2, 27), (3, 4, 27),
                   (4, 2, 27), (6, 3, 27), (6, 2, 27), (10, 2, 7), (5, 2, 27),
                   (3, 1, 27), (3, -1, 27), (3, 3, 27), (3, 5, 27), (3, 7, 27),
                   (3, 9, 27), (3, 13, 27), (3, 17, 27), (5, 1, 5), (5, 1, 7),
                   (5, 3, 27), (5, 5, 27), (5, 7, 27), (5, 11, 27), (5, 131, 27),
                   (5, 353, 27), (7, 1, 3), (7, 7, 9), (7, 1, 1), (9, 1, 5)]:
    tag = f"par_{a}_{'m' if d < 0 else ''}{abs(d)}_s{seed}"
    add(tag, "parity", f"even n -> n/2; odd n -> {a}n{d:+d}", parity(a, d), seed)

# ---- permutations of the positive integers --------------------------------
add("perm_1932_s8", "permutation", "3q->2q; 3q+1->4q+1; 3q+2->4q+3",
    mod_table(3, [(2, 0, 3), (4, -1, 3), (4, 1, 3)]), 8)
add("perm_1932_s44", "permutation", "3q->2q; 3q+1->4q+1; 3q+2->4q+3",
    mod_table(3, [(2, 0, 3), (4, -1, 3), (4, 1, 3)]), 44)
add("perm_1932inv_s8", "permutation", "2q->3q; 4q+1->3q+1; 4q+3->3q+2",
    mod_table(4, [(3, 0, 2), (3, 1, 4), (3, 0, 2), (3, -1, 4)]), 8)
add("perm_swap_s8", "permutation", "3q->2q; 3q+1->4q+3; 3q+2->4q+1",
    mod_table(3, [(2, 0, 3), (4, 5, 3), (4, -5, 3)]), 8)
add("perm_b_s7", "permutation", "3q->4q; 3q+1->4q+2; 3q+2->2q+1",
    mod_table(3, [(4, 0, 3), (4, 2, 3), (2, -1, 3)]), 7)
add("perm_c_s8", "permutation", "2q->3q; 4q+1->3q+2; 4q+3->3q+1",
    mod_table(4, [(3, 0, 2), (3, 5, 4), (3, 0, 2), (3, -5, 4)]), 8)
add("perm_d_s3", "permutation",
    "2q->5q; 8q+1->5q+1; 8q+3->5q+2; 8q+5->5q+3; 8q+7->5q+4",
    mod_table(8, [(5, 0, 2), (5, 3, 8), (5, 0, 2), (5, 1, 8), (5, 0, 2),
                  (5, -1, 8), (5, 0, 2), (5, -3, 8)]), 3)
add("perm_flip_s27", "permutation", "2q+1 -> 2q+2; 2q+2 -> 2q+1",
    lambda n: n + 1 if n % 2 else n - 1, 27)
add("perm_suffix_a_s1", "permutation", "2q->4q; 4q+1->4q+2; 4q+3->2q+1",
    mod_table(4, [(2, 0, 1), (1, 1, 1), (2, 0, 1), (1, -1, 2)]), 1)
add("perm_suffix_b_s8", "permutation",
    "2q+1->16q+12; 8q+4->2q+1; 4q+2->4q+2; 16q->8q; 16q+8->16q+4",
    lambda n: (8 * n + 4 if n % 2 else (n - 4) // 4 + 1 if n % 8 == 4
               else n if n % 4 == 2 else n // 2 if n % 16 == 0 else n - 4), 8)
add("perm_suffix_c_s1", "permutation", "4q->2q; 4q+2->4q+3; 2q+1->4q+1",
    lambda n: n // 2 if n % 4 == 0 else n + 1 if n % 4 == 2 else 2 * n - 1, 1)
add("perm_suffix_d_s1", "permutation",
    "2q->8q; 4q+1->2q+1; 8q+3->4q+2; 8q+7->8q+4",
    lambda n: (4 * n if n % 2 == 0 else (n + 1) // 2 if n % 4 == 1
               else (n + 1) // 2 if n % 8 == 3 else n - 3), 1)


def ceil_family(d):
    F = lambda m: m + (m + d - 1) // d
    def step(n):
        if n % 2 == 0:
            return 2 * F(n // 2)
        return 2 * ((d + 1) * (n // 4) + 1) if n % 4 == 1 else n // 2
    return step


add("perm_ceil2_s1", "permutation",
    "2m->2(m+ceil(m/2)); 4q+1->2(3q+1); 4q+3->2q+1", ceil_family(2), 1)
add("perm_ceil3_s1", "permutation",
    "2m->2(m+ceil(m/3)); 4q+1->2(4q+1); 4q+3->2q+1", ceil_family(3), 1)

# ---- split maps on residues mod 4 -----------------------------------------
for d, seed in [(5, 27), (13, 27), (73, 27), (97, 27), (7081, 27)]:
    add(f"split_{d}_s{seed}", "split",
        f"even n -> n/2; n=1 mod 4 -> 3n+{d}; n=3 mod 4 -> n+{d}",
        (lambda d: lambda n: n // 2 if n % 2 == 0 else
         3 * n + d if n % 4 == 1 else n + d)(d), seed)
for d, seed in [(7, 27), (71, 27)]:
    add(f"splitB_{d}_s{seed}", "split",
        f"even n -> n/2; n=1 mod 4 -> n+{d}; n=3 mod 4 -> 3n+{d}",
        (lambda d: lambda n: n // 2 if n % 2 == 0 else
         n + d if n % 4 == 1 else 3 * n + d)(d), seed)
for d, seed in [(1, 27), (3, 27)]:
    add(f"split5_{d}_s{seed}", "split",
        f"even n -> n/2; n=1 mod 4 -> 5n+{d}; n=3 mod 4 -> n+{d}",
        (lambda d: lambda n: n // 2 if n % 2 == 0 else
         5 * n + d if n % 4 == 1 else n + d)(d), seed)

# ---- maps branching on residues mod 3 -------------------------------------
add("m3_a_s100", "mod3", "3|n -> n/3; n=1 -> (2n+1)/3; n=2 -> (2n+2)/3",
    mod_table(3, [(1, 0, 3), (2, 1, 3), (2, 2, 3)]), 100)
add("m3_b_s8", "mod3", "3|n -> n/3; n=1 -> (4n-1)/3; n=2 -> (4n+1)/3",
    mod_table(3, [(1, 0, 3), (4, -1, 3), (4, 1, 3)]), 8)
add("m3_c_s100", "mod3", "3|n -> n/3; n=1 -> 2n+1; n=2 -> 2n+2",
    mod_table(3, [(1, 0, 3), (2, 1, 1), (2, 2, 1)]), 100)
add("m3_d_s7", "mod3", "3|n -> n/3; n=1 -> 4n+2; n=2 -> 4n+1",
    mod_table(3, [(1, 0, 3), (4, 2, 1), (4, 1, 1)]), 7)
add("m3_e_s7", "mod3", "3|n -> n/3; n=1 -> 7n+2; n=2 -> 7n+1",
    mod_table(3, [(1, 0, 3), (7, 2, 1), (7, 1, 1)]), 7)
add("m3_f_s100", "mod3", "3|n -> n/3; n=1 -> n+2; n=2 -> n+1",
    mod_table(3, [(1, 0, 3), (1, 2, 1), (1, 1, 1)]), 100)
add("m3_g_s7", "mod3", "3|n -> n/3; n=1 -> 5n+1; n=2 -> 5n+2",
    mod_table(3, [(1, 0, 3), (5, 1, 1), (5, 2, 1)]), 7)

# ---- mixed division rules --------------------------------------------------
add("farkas_s27", "mixed",
    "1 -> 1; n=1 mod 3 -> (n-1)/3; else even -> n/2; else -> (3n+1)/2", farkas, 27)
add("div23_5n1_s7", "mixed", "2|n -> n/2; else 3|n -> n/3; else 5n+1",
    div_else([2, 3], 5, 1), 7)
add("div235_7n1_s11", "mixed",
    "2|n -> n/2; else 3|n -> n/3; else 5|n -> n/5; else 7n+1",
    div_else([2, 3, 5], 7, 1), 11)
add("div23_7n1_s5", "mixed", "2|n -> n/2; else 3|n -> n/3; else 7n+1",
    div_else([2, 3], 7, 1), 5)
add("mahler_s1", "mixed", "even n -> 3n/2; odd n -> (3n+1)/2",
    lambda n: (3 * n + n % 2) // 2, 1)
add("div3_2n_s5", "mixed", "3|n -> n/3; else 2n",
    lambda n: n // 3 if n % 3 == 0 else 2 * n, 5)
add("div2_3n_s5", "mixed", "2|n -> n/2; else 3n",
    lambda n: n // 2 if n % 2 == 0 else 3 * n, 5)

BY_ID = {s["id"]: s for s in SYSTEMS}
assert len(BY_ID) == len(SYSTEMS)


def get(id):
    return BY_ID[id]
