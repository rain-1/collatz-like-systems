# shiftT_s8

**Rule.** J: 3q -> 2q+2 (q >= 1); 3q+1 -> 4q+1; 3q+2 -> 4q+3. This is T with the constant of the falling branch raised by 2, so J(n) - T(n) is in {0, 2}. J is injective but not surjective.

**Question (FATE).** What is the fate of the seed 8?

| answer | status | tier |
|---|---|---|
| infinite | PROVED | 1 |

## Proof

The three branch images are the evens >= 4, the class 1 (mod 4) and the class 3 (mod 4). These are pairwise disjoint and each branch is injective, so J is injective and 2 is not in J(Z_{>0}). The J-orbit of 2 is 2 -> 3 -> 4 -> 5 -> 7 -> 9 -> 8 -> ... If J^i(2) = J^j(2) with i < j, injectivity would give 2 = J^{j-i}(2), which is in the image, a contradiction. So the orbit of 2 is infinite, and so is its tail from 8.

## Census of the constant family (seed 8)

F(c0,c1,c2) is the family n -> (2n+c0)/3, (4n+c1)/3, (4n+c2)/3 by n mod 3 (see flipT_s8.md). In the box c0 in [-6,12], c1 in [-7,11], c2 in [-8,11]:

- **Injective, not surjective (17 maps).** Each is tier 0 or tier 1. Either the backward chain from 8 returns to 8 (8 is periodic: 3 maps), or it reaches a non-image point (8 is provably on an infinite orbit: 14 maps). This is checked exactly.
- **Bijective (4 maps, the complete list over all c; see flipT_s8.md).** T and flipT are the 1932 problem (OPEN). In S and S(n+3)-3 the seed 8 returns (tier 0).
- **Not injective (159 maps).** The orbit of 8 enters a cycle (100 maps), returns (13 maps), or stays unresolved (46 maps). The unresolved ones are many-to-one maps with positive drift, of the same kind as 5n+1. None of them was certified.

So, with T's slopes and branch reading held fixed, FATE(8) is decided at tier 0 or 1 for every map that has a non-image point. Every unresolved case is either a bijection that is T itself on a shifted lattice, or a many-to-one map.

## What stays hard

The orbit of 2 under J follows T's arithmetic. Whether it has infinitely many *decreases* is not proved. An orbit with only finitely many falls would eventually follow only the rising branches, x -> (4x -+ 1)/3. Those branches have the 3-adic invariant Cantor set of points that never meet 0 (mod 3), and that set contains the integer fixed points 1 and -1. So congruences cannot force a fall. Whether a positive integer other than 1 rises forever is a Mahler-type question (compare Mahler's Z-numbers and Flatto–Lagarias–Pollington, Acta Arith. 70 (1995) 125–147). We do not claim a reduction to any named problem.

## Why tier 1 and not 0

The claim is that the orbit is infinite, which simulation cannot prove. The proof uses only injectivity plus a 6-step finite chain.

Check: `check_shiftT_s8.py` (exit 0).

## Referee

**Verdict: CONFIRMED, tier 1 (agreed).**

The images are the evens ≥ 4, the class 1 (mod 4) and the class 3 (mod 4). These are disjoint, so J is injective and 2 has no preimage. The chain J: 2, 3, 4, 5, 7, 9, 8 checks out (`referee_check.py`). An injective orbit that starts at a non-image point cannot repeat, so the orbit of 8 is infinite.

Overstatement in the census paragraph: "FATE(8) is decided at tier 0 or 1 for every map that has a non-image point" is proved only for the 17 injective non-surjective maps in the stated box. In general, the backward chain from 8 can be infinite and aperiodic, because the inverse of the falling branch, m -> (3m - c0)/2, increases. In that case neither tier-0/1 route applies. Read the sentence as a statement about the box.
