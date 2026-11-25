"""Round 2, lens "upfrom1": perturb trivial maps until they break.

Common shape of every system here: a "trap" (a residue class C mod M sent to
n + M, so it stays in C and increases forever) bolted onto an otherwise
contracting or Collatz-type map.  The precise question for each system is

    WHICH n HAVE INFINITE ORBITS?   (exact description of the divergent set,
                                     with proof that every other orbit is
                                     eventually periodic and the cycle list)

Same style as census/systems.py: SYSTEMS is a list of dicts with
id, rule, step, seed (plus tier/status for convenience).
"""


def T(n):
    """Accelerated Collatz map."""
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def parity_word(n, L):
    """First L parities of the T-orbit of n (depends only on n mod 2^L)."""
    w = []
    for _ in range(L):
        w.append(n % 2)
        n = T(n)
    return w


# ---- multiplier-1 maps with a trap ------------------------------------------
def qr7_step(n):
    if n % 2 == 0:
        return n // 2
    if n % 28 == 3:
        return n + 28          # trap: stays = 3 mod 28
    return n + 7


def tok3_step(n):
    if n % 2 == 0:
        return n // 2
    if n % 4 == 1:
        return n + 3
    return n + 4               # trap: n = 3 mod 4 stays 3 mod 4


# ---- Collatz with trapdoors ---------------------------------------------------
def ct11_step(n):
    if n % 4 == 3:
        return n + 4           # trap: parity word starts 11
    return T(n)


def ct35_step(n):
    if n % 8 == 7:
        return n + 8           # trap: parity word starts 111
    if n % 32 == 27:
        return n + 32          # trap: parity word starts 11011
    return T(n)


# trap classes mod 256: 8-step parity word with >= 6 ones (so untrapped words
# have <= 5 ones in every window of 8; 3^5 = 243 < 256)
CT58_TRAPS = frozenset(r for r in range(256)
                       if sum(parity_word(r + 256, 8)) >= 6)


def ct58_step(n):
    if n % 256 in CT58_TRAPS:
        return n + 256
    return T(n)


def ct3_step(n):
    if n % 8 == 7:
        return n + 8           # trap: parity word starts 111
    return T(n)


SYSTEMS = [
    dict(id="up_qr7", tier=2, status="PROVED",
         rule="even n -> n/2; n=3 mod 28 -> n+28; other odd n -> n+7",
         step=qr7_step, seed=27),
    dict(id="up_tok3", tier=3, status="PROVED",
         rule="even n -> n/2; n=1 mod 4 -> n+3; n=3 mod 4 -> n+4",
         step=tok3_step, seed=37),
    dict(id="up_ct11", tier=1, status="PROVED",
         rule="n=3 mod 4 -> n+4; else even n -> n/2, odd n -> (3n+1)/2",
         step=ct11_step, seed=27),
    dict(id="up_ct35", tier=2, status="PROVED",
         rule="n=7 mod 8 -> n+8; n=27 mod 32 -> n+32; else even n -> n/2, odd n -> (3n+1)/2",
         step=ct35_step, seed=27),
    dict(id="up_ct58", tier=2, status="PROVED",
         rule="n mod 256 in R -> n+256 (R = residues whose 8-step Collatz parity word has >= 6 ones, 37 classes); "
              "else even n -> n/2, odd n -> (3n+1)/2",
         step=ct58_step, seed=27),
    dict(id="up_ct3", tier=5, status="OPEN",
         rule="n=7 mod 8 -> n+8; else even n -> n/2, odd n -> (3n+1)/2",
         step=ct3_step, seed=27),
]

BY_ID = {s["id"]: s for s in SYSTEMS}


def get(id):
    return BY_ID[id]
