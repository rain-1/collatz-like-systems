"""Round 3, lens 'accel': every map studied here, as a Python step function with
an id.  Same spirit as census/systems.py (dicts with id, rule, step, question).

Groups
  sf*      the 12 OBST members of the S-family (round2/descent/family_scan.py):
           even n -> n/2; odd n -> 3n+1 if n mod 2^m in S, else n+1.
  zcore_*  the same systems written in the coordinate z = (n-1)/2 on odd n
           (Theorem Z, sfamily_obst.md).
  acc_h*   constructed systems with an *isolated* expanding cycle, settled by
           Theorem H (trichotomy.md).
  dress_*  'dressed' systems (dressing.md): an expanding p-adic fixed point
           whose runs are consumed by a second prime.
Tables use the descent_lib format: table[r] = (u, v, w), n = r mod M -> (u n + v)/w.
"""

SYSTEMS = []


def mod_table(M, table):
    def step(n):
        u, v, w = table[n % M]
        x = u * n + v
        assert x % w == 0
        return x // w
    return step


def s_table(m, S):
    return [(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r in S else (1, 1, 1))
            for r in range(2 ** m)]


def add(id, question, rule, step, p=None, m=None, table=None, **kw):
    d = dict(id=id, question=question, rule=rule, step=step, p=p, m=m, table=table)
    d.update(kw)
    SYSTEMS.append(d)


# ------------------------------------------------------------------ S-family
SF = [(2, (3,)), (2, (1, 3)),
      (3, (1, 3)), (3, (1, 3, 5)), (3, (7,)), (3, (1, 7)), (3, (3, 7)),
      (3, (1, 3, 7)), (3, (5, 7)), (3, (1, 5, 7)), (3, (3, 5, 7)), (3, (1, 3, 5, 7))]


def sf_id(m, S):
    return "sf%d_%s" % (m, "".join(str(s) for s in S))


for m, S in SF:
    t = s_table(m, S)
    add(sf_id(m, S), "GLOBAL",
        "even n -> n/2; odd n -> 3n+1 if n mod %d in %s, else n+1" % (2 ** m, set(S)),
        mod_table(2 ** m, t), p=2, m=m, table=t, S=S)


def collatz_T(z):
    return z // 2 if z % 2 == 0 else (3 * z + 1) // 2


def odd_part(x):
    while x % 2 == 0:
        x //= 2
    return x


def zcore(m, S):
    """G_S(z) = (odd(T_S(2z+1)) - 1)/2, computed from the closed formulas of
    Theorem Z (not from T_S): with r = (2z+1) mod 2^m,
      r in S : z -> (odd(3z+2) - 1)/2 ;   r not in S : z -> (odd(z+1) - 1)/2."""
    Q = 2 ** m
    Sset = set(S)

    def G(z):
        if (2 * z + 1) % Q in Sset:
            return (odd_part(3 * z + 2) - 1) // 2
        return (odd_part(z + 1) - 1) // 2
    return G


for m, S in SF:
    add("zcore_" + sf_id(m, S)[2:], "GLOBAL (on z >= 0)",
        "z -> (odd(3z+2)-1)/2 if (2z+1) mod %d in %s, else (odd(z+1)-1)/2" % (2 ** m, set(S)),
        zcore(m, S), S=S, m=m)


def W137(z):
    """zcore of S={1,3,7} mod 8 in its simplest form (sfamily_obst.md)."""
    if z % 2:
        return (3 * z + 1) // 2
    if z % 4 == 2:
        return z // 2
    return 3 * z // 4


add("zcore_W", "GLOBAL / divergence",
    "z odd -> (3z+1)/2; z = 2 mod 4 -> z/2; z = 0 mod 4 -> 3z/4", W137)


def K7(z):
    """zcore of S={7} mod 8 in its simplest form."""
    if z % 2 == 0:
        return z // 2
    if z % 4 == 3:
        return (3 * z + 1) // 2
    return (z - 1) // 4


add("zcore_K7", "GLOBAL",
    "z even -> z/2; z = 3 mod 4 -> (3z+1)/2; z = 1 mod 4 -> (z-1)/4", K7)


# ------------------------------------------------------ Theorem H examples
def h_table(m, patch, default=(3, 1, 1)):
    return [(1, 0, 2) if r % 2 == 0 else patch.get(r, default) for r in range(2 ** m)]


H1 = h_table(5, {5: (1, 1, 1), 9: (1, 1, 1), 21: (1, 1, 1), 25: (1, 1, 1), 29: (1, 9, 1)})
H2 = h_table(4, {5: (1, 1, 1), 9: (1, 1, 1), 13: (1, 5, 1)})
# base 3, modulus 9:  3q -> q ; 9q+r -> 6q+r (r = 1,4,7) ; 9q+2 -> 12q+4 ;
#                     9q+5 -> 12q+7 ; 9q+8 -> 12q+11
H3 = [(1, 0, 3), (2, 1, 3), (4, 4, 3), (1, 0, 3), (2, 4, 3), (4, 1, 3), (1, 0, 3), (2, 7, 3), (4, 1, 3)]

add("acc_h32", "GLOBAL",
    "even n -> n/2; odd n -> n+1 if n = 5,9,21,25 mod 32, n+9 if n = 29 mod 32, else 3n+1",
    mod_table(32, H1), p=2, m=5, table=H1)
add("acc_h16", "GLOBAL",
    "even n -> n/2; odd n -> n+1 if n = 5,9 mod 16, n+5 if n = 13 mod 16, else 3n+1",
    mod_table(16, H2), p=2, m=4, table=H2)
add("acc_h9", "GLOBAL",
    "3q -> q; 9q+r -> 6q+r (r=1,4,7); 9q+2 -> 12q+4; 9q+5 -> 12q+7; 9q+8 -> 12q+11",
    mod_table(9, H3), p=3, m=2, table=H3)


# ------------------------------------------------------------ dressed maps
def rough(x, primes):
    for q in primes:
        while x % q == 0:
            x //= q
    return x


def dressed(p, q, e, g):
    """D(x) = q^e x/p if p|x;  x/q if p∤x, q|x;  g(x) otherwise."""
    def D(x):
        if x % p == 0:
            return q ** e * x // p
        if x % q == 0:
            return x // q
        return g(x)
    return D


def undressed(p, q, g):
    def U(x):
        if x % p == 0:
            return x // p
        if x % q == 0:
            return x // q
        return g(x)
    return U


add("dress_23_x1", "GLOBAL", "2|x -> 3x/2; else 3|x -> x/3; else x+1",
    dressed(2, 3, 1, lambda x: x + 1), dress=(2, 3, 1, "x+1"))
add("dress_32_x1", "GLOBAL", "3|x -> 4x/3; else 2|x -> x/2; else x+1",
    dressed(3, 2, 2, lambda x: x + 1), dress=(3, 2, 2, "x+1"))
add("dress_23_3x1", "GLOBAL", "2|x -> 3x/2; else 3|x -> x/3; else 3x+1",
    dressed(2, 3, 1, lambda x: 3 * x + 1), dress=(2, 3, 1, "3x+1"))
add("dress_23_5x1", "GLOBAL", "2|x -> 3x/2; else 3|x -> x/3; else 5x+1",
    dressed(2, 3, 1, lambda x: 5 * x + 1), dress=(2, 3, 1, "5x+1"))

BY_ID = {s["id"]: s for s in SYSTEMS}


def get(id):
    return BY_ID[id]
