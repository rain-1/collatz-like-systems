"""Table constructors for the families scanned in this folder.

All tables are lists indexed by the residue r mod Q of triples (u, v, w):
n = r (mod Q)  ->  (u n + v) / w.
"""


def base3_table(Q, choice):
    """3|n -> n/3; for 3 does not divide n: n -> a n + b with (a, b) = choice[r] (r = n mod Q)."""
    return [(1, 0, 3) if r % 3 == 0 else (choice[r][0], choice[r][1], 1) for r in range(Q)]


def base3_S(Q, a, S, b=1):
    """3|n -> n/3; n mod Q in S -> a n + b; other non-multiples of 3 -> n + b."""
    return [(1, 0, 3) if r % 3 == 0 else ((a, b, 1) if r in S else (1, b, 1)) for r in range(Q)]


def s_family(m, S, a=3, d=1):
    """even -> n/2; odd n -> a n + d if n mod 2^m in S, else n + d (round-2 S-family)."""
    Q = 2 ** m
    return [(1, 0, 2) if r % 2 == 0 else ((a, d, 1) if r in S else (1, d, 1)) for r in range(Q)]


def lift(Q, table, d):
    """The same map presented at modulus Q*d."""
    return [table[r % Q] for r in range(Q * d)]


def rule_string(Q, table):
    """Human-readable rule, grouping residues with the same branch."""
    groups = {}
    for r, t in enumerate(table):
        groups.setdefault(t, []).append(r)
    parts = []
    for (u, v, w), rs in groups.items():
        num = (f"{u}n" if u != 1 else "n") + (f"+{v}" if v > 0 else (f"{v}" if v < 0 else ""))
        f = num if w == 1 else f"({num})/{w}"
        parts.append(f"n mod {Q} in {{{','.join(map(str, rs))}}} -> {f}")
    return "; ".join(parts)
