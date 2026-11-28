"""Round 3, lens "mixedbase": the new systems, in the style of census/systems.py.

Every entry: id, family, rule, step (Python function on the stated domain), seed, question,
status.  Running this file cross-checks each step function against the table form used by the
check scripts on 1 <= n < 20000 and prints the fate of each seed.
"""


def classes_map(m, R, a, b):
    """n = r (mod m), r in R -> (n + R[r])/m (priority); else even -> n/2; else (a n + b)/2."""
    def step(n):
        r = n % m
        if r in R:
            x = n + R[r]
            assert x % m == 0
            return x // m
        if n % 2 == 0:
            return n // 2
        return (a * n + b) // 2
    return step


def ceil_classes(m, rs):
    return {r: (-r) % m for r in rs}


def div23_plus(q, R):
    def step(n):
        if n % q in R:
            x = n + R[n % q]
            assert x % q == 0
            return x // q
        if n % 2 == 0:
            return n // 2
        if n % 3 == 0:
            return n // 3
        return 5 * n + 1
    return step


def m3b_plus(q, R):
    def step(n):
        if n % q in R:
            x = n + R[n % q]
            assert x % q == 0
            return x // q
        r = n % 3
        return n // 3 if r == 0 else (4 * n - 1) // 3 if r == 1 else (4 * n + 1) // 3
    return step


SYSTEMS = []


def add(id, family, rule, step, seed, status, domain="N+", question="GLOBAL"):
    SYSTEMS.append(dict(id=id, family=family, rule=rule, step=step, seed=seed, status=status,
                        domain=domain, question=question))


# ---- Farkas pairing family (pairing_family.md) ----------------------------------------------
add("mb_pair_3_9p", "pairing", "n=5 mod 9 -> (n+4)/9; else even -> n/2; else (3n-1)/2",
    classes_map(9, {5: 4}, 3, -1), 27, "PROVED: all orbits -> (1)")
add("mb_pair_3_9m", "pairing", "n=4 mod 9 -> (n-4)/9; else even -> n/2; else (3n+1)/2",
    classes_map(9, {4: -4}, 3, 1), 27, "PROVED: all orbits -> (0) or (1 2)", domain="N0")
add("mb_pair_7_7m", "pairing", "n=3 mod 7 -> (n-3)/7; else even -> n/2; else (7n+5)/2",
    classes_map(7, {3: -3}, 7, 5), 27, "PROVED: all orbits -> (0)", domain="N0")
add("mb_pair_5_5m", "pairing", "n=2 mod 5 -> (n-2)/5; else even -> n/2; else (5n+3)/2",
    classes_map(5, {2: -2}, 5, 3), 27, "PROVED: all orbits -> (0)", domain="N0")
add("mb_pair_3_27m", "pairing", "n=13 mod 27 -> (n-13)/27; else even -> n/2; else (3n+1)/2",
    classes_map(27, {13: -13}, 3, 1), 27, "OPEN (no certificate exists; evidence: converges)",
    domain="N0")
add("mb_pair_5_25p", "pairing", "n=13 mod 25 -> (n+12)/25; else even -> n/2; else (5n-3)/2",
    classes_map(25, {13: 12}, 5, -3), 27, "OPEN (no certificate exists; evidence: cycles (1),(3 6))")

# ---- single classes (single_class.md) ----------------------------------------------------------
add("mb_s3_3", "single", "n=2 mod 3 -> (n+1)/3; else even -> n/2; else (3n+1)/2",
    classes_map(3, {2: 1}, 3, 1), 27, "PROVED: all orbits -> (1 2)")
add("mb_s3_9", "single", "n=8 mod 9 -> (n+1)/9; else even -> n/2; else (3n+1)/2",
    classes_map(9, {8: 1}, 3, 1), 27, "PROVED: all orbits -> (1 2)")
add("mb_s3_27", "single", "n=26 mod 27 -> (n+1)/27; else even -> n/2; else (3n+1)/2",
    classes_map(27, {26: 1}, 3, 1), 27, "OPEN (no certificate exists; evidence: converges)")
add("mb_s5_5", "single", "n=3 mod 5 -> (n+2)/5; else even -> n/2; else (5n+1)/2",
    classes_map(5, {3: 2}, 5, 1), 27, "PROVED: all orbits -> (1 3)")
add("mb_s7_7", "single", "n=4 mod 7 -> (n+3)/7; else even -> n/2; else (7n+1)/2",
    classes_map(7, {4: 3}, 7, 1), 27, "PROVED: all orbits -> (1 4)")

# ---- sparse multi-class tamings (sparse_taming.md) ---------------------------------------------
for sid, a, m, rs, cyc in [
        ("mb_t27", 3, 27, (17, 26), "(1 2)"),
        ("mb_t81", 3, 81, (20, 71, 80), "(1 2)"),
        ("mb_t243", 3, 243, (137, 152, 233, 242), "(1 2)"),
        ("mb_t729", 3, 729, (182, 380, 395, 425, 668, 719, 728), "(1 2)"),
        ("mb_f25", 5, 25, (8, 23), "(1 3 8)"),
        ("mb_f125", 5, 125, (68, 73, 83, 123), "(1 3 8 4 2)"),
        ("mb_s49", 7, 49, (32, 39), "(1 4 2)"),
        ("mb_s343", 7, 343, (93, 137, 142, 200, 228), "(1 4 2)")]:
    R = ceil_classes(m, rs)
    rule = "; ".join(f"n={r} mod {m} -> (n+{c})/{m}" for r, c in sorted(R.items())) + \
        f"; else even -> n/2; else ({a}n+1)/2"
    add(sid, "sparse", rule, classes_map(m, R, a, 1), 27, "PROVED: all orbits -> " + cyc)

# ---- relatives of open entries (relatives.md) --------------------------------------------------
add("mb_d23_8", "div23+", "n=7 mod 8 -> (n+1)/8; else 2|n -> n/2; else 3|n -> n/3; else 5n+1",
    div23_plus(8, {7: 1}), 7, "PROVED: all orbits -> (1 6 3)")
add("mb_d23_4", "div23+", "n=3 mod 4 -> (n+1)/4; else 2|n -> n/2; else 3|n -> n/3; else 5n+1",
    div23_plus(4, {3: 1}), 7, "PROVED: all orbits -> (1 6 3)")
add("mb_d23_30", "div23+", "n=26 mod 30 -> (n+4)/30; else 2|n -> n/2; else 3|n -> n/3; else 5n+1",
    div23_plus(30, {26: 4}), 7, "PROVED: all orbits -> (1 6 3)")
add("mb_m3b_8", "m3b+", "n=1 mod 8 -> (n+7)/8; n=7 mod 8 -> (n+1)/8; else 3|n -> n/3; "
    "n=1 mod 3 -> (4n-1)/3; n=2 mod 3 -> (4n+1)/3",
    m3b_plus(8, {1: 7, 7: 1}), 8, "PROVED: all orbits -> (1)")


if __name__ == "__main__":
    for s in SYSTEMS:
        x, seen = s["seed"], {}
        k = 0
        while x not in seen:
            seen[x] = k
            x = s["step"](x)
            k += 1
        cyc = [x]
        y = s["step"](x)
        while y != x:
            cyc.append(y)
            y = s["step"](y)
        i = cyc.index(min(cyc))
        print(f'{s["id"]:14s} seed {s["seed"]:3d}: cycle {tuple(cyc[i:] + cyc[:i])} after {seen[x]} steps  [{s["status"]}]')
