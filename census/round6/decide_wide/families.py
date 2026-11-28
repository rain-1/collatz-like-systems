"""families.py -- the product families scanned in this round (new; see README for what was
scanned before).  A family is (Q, opts) with opts[r] the list of allowed branches (u, v, w) on
class r mod Q.  Every option is checked here: (H1) gcd(u, Q) = 1, (H2) w | Q, w | u r + v,
(P) T(n0) >= 1 at the least n0 of the class.  Options failing (P) are dropped.

Naming:
  P2_m_<menu>  Q = 2^m: even n -> n/2; odd class r -> u n + v       (raw parity tables)
  P3_m_<menu>  Q = 3^m: 3|n -> n/3; unit class r -> u n + v
  P5_m_<menu>  Q = 5^m: 5|n -> n/5; unit class r -> u n + v
  M_Q_<menu>   Q mixed: 2|n -> n/2, else p|n -> n/p (p the other primes of Q in increasing
               order), else unit class r -> u n + v
  G3_2         Q = 9: 3|n -> n/3; unit class r -> u n + v or (u n + v)/3 (shortcut branches)
"""
import math
import itertools

MENUS = {
    # p = 2: odd multipliers
    "u135v13": ([1, 3, 5], [1, 3]),
    "u1357v1357m": ([1, 3, 5, 7], [1, 3, 5, 7, -1, -3]),
    "u135v1m": ([1, 3, 5], [1, 3, 5, -1]),
    # p = 3
    "u1245v12m": ([1, 2, 4, 5], [1, 2, -1, -2]),
    "u12457v12m": ([1, 2, 4, 5, 7], [1, 2, -1, -2]),
    # p = 5
    "u12346v12m": ([1, 2, 3, 4, 6], [1, 2, -1, -2]),
    "u1234v12m": ([1, 2, 3, 4], [1, -1, 2]),
    # mixed (u must be prime to Q; filtered)
    "u157v123m": ([1, 5, 7, 11], [1, 2, 3, -1]),
    "u1357v12m": ([1, 3, 7, 9], [1, 2, -1, 3]),
    "u157v12": ([1, 5, 7], [1, 2]),
}


def least(r, Q):
    return r if r > 0 else Q


def ok_option(Q, r, u, v, w):
    if not (u >= 1 and w >= 1 and math.gcd(u, Q) == 1 and Q % w == 0 and (u * r + v) % w == 0):
        return False
    return (u * least(r, Q) + v) // w >= 1


def div_branch(Q, r):
    """Division rule for r: 2|r -> n/2, else first other prime p of Q with p | r -> n/p."""
    ps = sorted({p for p in range(2, Q + 1) if Q % p == 0 and all(p % q for q in range(2, p))})
    for p in ps:
        if r % p == 0:
            return (1, 0, p)
    return None


def family(name):
    kind, rest = name.split("_", 1)
    if kind in ("P2", "P3", "P5"):
        p = int(kind[1])
        m, menu = rest.split("_", 1)
        Q = p ** int(m)
    elif kind == "M":
        q, menu = rest.split("_", 1)
        Q = int(q)
    elif kind == "G3":
        Q, menu = 9, "u1245v12m"
    else:
        raise ValueError(name)
    us, vs = MENUS[menu]
    opts = []
    for r in range(Q):
        d = div_branch(Q, r)
        if d is not None:
            opts.append([d])
            continue
        o = [(u, v, 1) for u in us for v in vs if ok_option(Q, r, u, v, 1)]
        if kind == "G3":
            o += [(u, v, 3) for u in us for v in range(-4, 5) if ok_option(Q, r, u, v, 3)]
        opts.append(o)
    for r, o in enumerate(opts):
        for (u, v, w) in o:
            assert ok_option(Q, r, u, v, w), (name, r, u, v, w)
    return Q, opts


def size(opts):
    s = 1
    for o in opts:
        s *= len(o)
    return s


def spec_text(Q, opts, mode, count=0, seed=1):
    lines = [f"{Q} {mode} {count} {seed}"]
    for o in opts:
        lines.append(" ".join([str(len(o))] + [f"{u} {v} {w}" for (u, v, w) in o]))
    return "\n".join(lines) + "\n"


def decode(opts, ix):
    digits = [int(x) for x in ix.split(".")]
    return [opts[r][d] for r, d in enumerate(digits)]


FAMILIES = [
    # (name, mode, count) ; mode 0 exhaustive, 1 random sample
    ("P2_2_u1357v1357m", 0, 0),
    ("P2_3_u1357v1357m", 0, 0),
    ("P2_4_u135v13", 0, 0),
    ("P2_4_u1357v1357m", 1, 3000000),
    ("P2_5_u135v13", 1, 3000000),
    ("P3_1_u12457v12m", 0, 0),
    ("P3_2_u1245v12m", 0, 0),
    ("P3_3_u1245v12m", 1, 2000000),
    ("G3_2", 1, 3000000),
    ("P5_1_u12346v12m", 0, 0),
    ("P5_2_u1234v12m", 1, 2000000),
    ("M_6_u157v123m", 0, 0),
    ("M_10_u1357v12m", 0, 0),
    ("M_12_u157v123m", 0, 0),
    ("M_18_u157v123m", 0, 0),
    ("M_24_u157v12", 0, 0),
    ("M_24_u157v123m", 1, 3000000),
    ("M_36_u157v12", 1, 3000000),
]

if __name__ == "__main__":
    for name, mode, cnt in FAMILIES:
        Q, opts = family(name)
        print(f"{name:22s} Q={Q:3d} members={size(opts):.3e} mode={'exhaustive' if mode == 0 else 'sample %d' % cnt}")
