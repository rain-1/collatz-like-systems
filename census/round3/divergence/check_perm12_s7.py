"""Check for perm12_s7.md.  Exit 0 on success.

 (1) the 7 branches are order-preserving bijections between the input and output
     classes, and both families of classes partition the integers (exact, one
     period); T is injective on 1..3*10^5 and its image covers 1..10^5;
 (2) U = {1, 5, 9, 11} (mod 12) is forward closed (exact residue graph), 7 is not
     in U, and T(7) = 47 is in U;
 (3) every closed walk in U passes a fall class (Lemma F) and every closed walk
     has a 3-adic denominator (Lemma I, exact witness);
 (4) minimality: no union of residue classes mod K < 12 separates 7 (exact);
 (5) EVIDENCE: periodic points below 3000 are exactly 8, 21, 35; the backward
     orbit of 7 (40 steps) is not monotone.
"""
import os
import sys
from math import lcm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from systems import get  # noqa: E402
from divlib import images, is_closed, nonfall_subgraph_acyclic, aperiodic_certificate, verify_aperiodic  # noqa: E402

INP = [(6, 0), (6, 1), (6, 2), (6, 4), (6, 5), (12, 3), (12, 9)]
OUT = [(12, 3), (24, 23), (4, 0), (12, 7), (4, 1), (4, 2), (24, 11)]


def main():
    T = get("perm12_s7")["rcwa"]
    T.check()
    # (1)
    for fam in (INP, OUT):
        L = lcm(*[u for u, _ in fam])
        for n in range(L, 2 * L):
            assert sum(1 for u, r in fam if n % u == r) == 1
    for (u, r), (v, s) in zip(INP, OUT):
        rr, ss = (r if r else u), (s if s else v)
        for q in range(0, 50):
            assert T(rr + u * q) == ss + v * q
    seen = {}
    for n in range(1, 300001):
        y = T(n)
        assert y not in seen
        seen[y] = n
    assert all(y in seen for y in range(1, 100001))
    print("(1) bijection ok")
    # (2)
    U = [1, 5, 9, 11]
    assert is_closed(T, 12, U) and 7 % 12 not in U and T(7) % 12 in U
    print("(2) separator mod 12 ok; T(7) =", T(7))
    # (3)
    assert nonfall_subgraph_acyclic(T, 12, U)
    ap = aperiodic_certificate(T, 12, U, 3)
    assert ap and verify_aperiodic(T, ap)
    print("(3) forced falls and 3-adic aperiodicity ok")
    # (4)
    for K in range(1, 12):
        KK = lcm(K, 12)
        cur = {T(7) % K}
        while True:
            lifts = [r for r in range(KK) if r % K in cur]
            img = set()
            for r in lifts:
                img |= {x % K for x in images(T, KK, r)}
            new = cur | img
            if new == cur:
                break
            cur = new
        assert 7 % K in cur, K
    print("(4) no separator modulo K < 12")
    # (5)
    per = set()
    for n in range(1, 3000):
        x = n
        for _ in range(3000):
            x = T(x)
            if x == n:
                per.add(n)
                break
            if x > 10 ** 40:
                break
    assert per == {8, 21, 35}, per
    b = [7]                      # seen[y] = T^{-1}(y)
    while len(b) < 40:
        b.append(seen[b[-1]])
        assert T(b[-1]) == b[-2]
    ups = sum(1 for i in range(len(b) - 1) if b[i + 1] > b[i])
    assert 0 < ups < len(b) - 1
    print("(5) periodic points < 3000:", sorted(per), "; backward orbit", b[:12], "...")
    print("OK")


if __name__ == "__main__":
    main()
