"""Check for theorem5_precision3.md and swT2_8_s8.md.  Exit 0 on success.

 (A) Lemma P3 sanity: for random sigma (delta in {-1,0,1} on classes mod 18,
     made a valid map), random i <= 4, j in {3,4}, random start class: the
     forward closure mod 2^i 3^j (exact residue graph of Q = sigma o G) contains
     every lift of some full class mod 2^i*9 together with its full-class-graph
     closure (illustration of the proved lemma);
 (B) table: every swap set A (empty, singles, disjoint pairs mod 18) is
     classified for i <= IMAX (default 10; --imax 12 reproduces the README):
     'returns' (8 periodic, simulated), 'obstructed up to IMAX', or 'not
     obstructed from i0'.  Expected: not obstructed exactly for (2,8) from 8,
     (7,10) from 5, (9,15) from 2;
 (C) swT2_8_s8: the separator U (732 full classes mod 2304) lifted to mod 6912
     is forward closed for the exact residue graph of Q, 8 not in U, Q(8) in U;
     the least modulus of the form 2^i 3^j admitting a separator is 2304.
"""
import itertools
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from precision3 import G, make_sigma, full_class_graph, obstructed  # noqa: E402
from divlib import from_function, images, is_closed, forward_closure  # noqa: E402


def part_A():
    rng = random.Random(3)
    done = 0
    while done < 40:
        A = rng.sample(range(1, 18), rng.randint(0, 3))
        try:
            sig = make_sigma(A)
        except AssertionError:
            continue
        Q = lambda n, sig=sig: sig(G(n))
        T = from_function(54, Q)
        i = rng.randint(0, 3)
        j = rng.choice([3, 4])
        K = 2 ** i * 3 ** j
        if K % 54:
            K *= 2           # residue graph needs a multiple of the map's modulus 54
            i += 1
        N = 2 ** i * 9
        r = rng.randrange(K)
        U = forward_closure(T, K, [r])
        full = [y for y in range(N) if all((y + N * k) in U for k in range(K // N))]
        assert full, (A, i, j, r)
        adj = full_class_graph(sig, i)
        seen = {full[0]}
        todo = [full[0]]
        while todo:
            u = todo.pop()
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    todo.append(w)
        for y in seen:
            assert all((y + N * k) in U for k in range(K // N)), (A, i, j, y)
        done += 1
    print("(A) Lemma P3 consistent on", done, "random instances")


def returns(sig, cap=3000):
    x = 8
    for _ in range(cap):
        x = sig(G(x))
        if x == 8:
            return True
    return False


def part_B(imax):
    # a = 0 is excluded: the pair {0, 1} would send 1 to 0
    sets = [()] + [(a,) for a in range(1, 18)] + list(itertools.combinations(range(1, 18), 2))
    notob = {}
    nret = nob = 0
    for A in sets:
        try:
            sig = make_sigma(A)
        except AssertionError:
            continue
        if returns(sig):
            nret += 1
            continue
        for i in range(imax + 1):
            ok, _ = obstructed(sig, i)
            if not ok:
                notob[A] = i
                break
        else:
            nob += 1
    expect = {(2, 8): 8, (7, 10): 5, (9, 15): 2}
    expect = {k: v for k, v in expect.items() if v <= imax}
    assert notob == expect, notob
    print("(B) i <= %d: %d sets return, %d obstructed, not obstructed: %s" % (imax, nret, nob, notob))


def part_C():
    sig = make_sigma((2, 8))
    Q = lambda n: sig(G(n))
    i, N = 8, 2 ** 8 * 9
    adj = full_class_graph(sig, i)
    st = Q(8) % N
    seen = {st}
    todo = [st]
    while todo:
        u = todo.pop()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                todo.append(w)
    assert len(seen) == 732 and 8 % N not in seen
    T = from_function(54, Q)
    K = 3 * N
    U = [r for r in range(K) if r % N in seen]
    assert is_closed(T, K, U) and 8 % K not in set(U) and Q(8) % K in set(U)
    # least modulus 2^i 3^j: i <= 7 obstructed (Lemma P3); the remaining
    # candidates below 2304 are 256, 768, 512, 1536, 1024, 2048
    for ii in range(8):
        assert obstructed(sig, ii)[0]
    for ii, D in ((8, 256), (8, 768), (9, 512), (9, 1536), (10, 1024), (11, 2048)):
        NN = 2 ** ii * 9
        a2 = full_class_graph(sig, ii)
        cur = {r for r in range(NN) if r % D == Q(8) % D}
        while True:
            new = set(cur)
            for u in cur:
                new |= set(a2[u])
            new = {r for r in range(NN) if (r % D) in {s % D for s in new}}
            if new == cur:
                break
            cur = new
        assert 8 % NN in cur, (ii, D)
    print("(C) swT2_8_s8 separator: 732 classes mod 2304, verified mod 6912; least 2^i 3^j modulus = 2304")


def main():
    imax = 10
    if "--imax" in sys.argv:
        imax = int(sys.argv[sys.argv.index("--imax") + 1])
    part_A()
    part_B(imax)
    part_C()
    print("OK")


if __name__ == "__main__":
    main()
