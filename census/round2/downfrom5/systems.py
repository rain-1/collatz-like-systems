"""Round 2, lens "downfrom5": minimal modifications of the 1932 permutation.

T is Collatz's 1932 permutation  3q -> 2q, 3q+1 -> 4q+1, 3q+2 -> 4q+3.
sigma_A (A a set of residues mod 18) is the involution of Z_{>0} that swaps
n <-> n+1 whenever n = a (mod 18) for some a in A (the pairs {a, a+1} are
disjoint).  sigma_A o T differs from T by at most 1 everywhere.

Every system: dict(id, family, rule, step, seed, question).
Use get(id).
"""


def T(n):
    q, r = divmod(n, 3)
    return 2 * q if r == 0 else (4 * q + 1 if r == 1 else 4 * q + 3)


def sigma(M, A):
    A = set(A)
    up = {a % M for a in A}
    down = {(a + 1) % M for a in A}
    assert not (up & down)

    def s(n):
        r = n % M
        return n + 1 if r in up else (n - 1 if r in down else n)
    return s


def D(n):
    """round-1 perm_d: 2q -> 5q; 8q+r -> 5q+(r+1)/2 for r = 1,3,5,7."""
    if n % 2 == 0:
        return 5 * n // 2
    q, r = divmod(n, 8)
    return 5 * q + (r + 1) // 2


def flipT(n):
    m = T(n)
    return m + 1 if m % 2 else m - 1


def shiftT(n):
    q, r = divmod(n, 3)
    return 2 * q + 2 if r == 0 else (4 * q + 1 if r == 1 else 4 * q + 3)


def twochanW(n):
    if n % 2:
        r = n % 6
        if r == 1:
            return 4 * n + 1
        if r == 3:
            return 4 * n + 5
        return (2 * n - 1) // 3
    if n % 4 == 0:
        return n // 2
    if n % 8 == 2:
        return (3 * n - 4) // 2
    return 3 * n // 2


def compose(s, f):
    return lambda n: s(f(n))


SYSTEMS = []


def add(id, family, rule, step, seed, question):
    SYSTEMS.append(dict(id=id, family=family, rule=rule, step=step,
                        seed=seed, question=question))


add("flipT_s8", "perm-near-1932",
    "n -> T(n)+1 if T(n) odd, T(n)-1 if T(n) even; i.e. 3q->2q-1; 3q+1->4q+2; 3q+2->4q+4",
    flipT, 8, "FATE")
add("swT9_s8", "perm-near-1932",
    "n -> sigma_{9}(T(n)), sigma_{9} swaps 9<->10 (mod 18)",
    compose(sigma(18, [9]), T), 8, "FATE")
add("swT9_15_s8", "perm-near-1932",
    "n -> sigma_{9,15}(T(n)), swaps 9<->10 and 15<->16 (mod 18)",
    compose(sigma(18, [9, 15]), T), 8, "FATE")
add("swT3_9_15_s8", "perm-near-1932",
    "n -> sigma_{3,9,15}(T(n)), swaps 3<->4 (mod 6) after T",
    compose(sigma(18, [3, 9, 15]), T), 8, "FATE")
add("shiftT_s8", "injection-near-1932",
    "3q -> 2q+2; 3q+1 -> 4q+1; 3q+2 -> 4q+3",
    shiftT, 8, "FATE")
add("twochanW_s8", "perm-forced-falls",
    "n=1 (6) -> 4n+1; n=3 (6) -> 4n+5; n=5 (6) -> (2n-1)/3; "
    "n=0 (4) -> n/2; n=2 (8) -> (3n-4)/2; n=6 (8) -> 3n/2",
    twochanW, 8, "FATE")
add("swD_s3", "perm-near-perm_d",
    "n -> sigma(D(n)), D = perm_d (2q->5q; 8q+r->5q+(r+1)/2), "
    "sigma swaps 3<->4, 11<->12, 14<->15 (mod 20)",
    compose(sigma(20, [3, 11, 14]), D), 3, "FATE")


def get(id):
    for s in SYSTEMS:
        if s["id"] == id:
            return s
    raise KeyError(id)
