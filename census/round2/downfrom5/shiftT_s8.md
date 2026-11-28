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
- **Not injective (159 maps).** The orbit of 8 enters a cycle after a transient in 100 maps and returns to 8 in 13. The original sweep left 46 unresolved. The theorem below proves escape in four of those, leaving 42 unresolved.

Within the box, FATE(8) is decided for all 17 injective non-surjective maps. Every unresolved case is either a bijection equivalent to T on a shifted lattice, or a many-to-one map.

## Four many-to-one maps for which 8 escapes

**Theorem.** For each integer $t$ from 1 to 4, define a map of the positive integers by

$$
F_t(3q)=2q+t,\qquad F_t(3q+1)=F_t(3q+2)=4q+6-t.
$$

Here $q\ge 1$ in the first branch and $q\ge 0$ in the other two. In every case $F_t^k(8)\to\infty$. Consequently each of these four maps has a negative answer to the question whether every positive orbit eventually cycles.

**Proof.** All outputs have the parity of $t$. Let $s=3(4-t)$. Direct substitution on the three input classes gives

$$
F_4(n+s)=F_t(n)+s,\qquad F_4(2u)=2J(u).
$$

The identities hold for all positive $n$ and $u$, respectively. Thus, on the invariant parity class $n\equiv t\pmod 2$, the coordinate $H_t(n)=(n+s)/2$ is a positive integer and satisfies $H_t(F_t(n))=J(H_t(n))$.

In the table, $x$ is the first point of the orbit starting from 8 in that parity class. The constants are in the census order, with denominator 3.

| $t$ | $(c_0,c_1,c_2)$ | $x$ | $H_t(x)$ |
|---:|:---|:---|---:|
| 1 | (3, 11, 7) | $F_1(8)=13$ | 11 |
| 2 | (6, 8, 4) | 8 | 7 |
| 3 | (9, 5, 1) | $F_3(8)=11$ | 7 |
| 4 | (12, 2, −2) | 8 | 4 |

The three images of $J$ are the even integers starting at 4 and the two odd classes modulo 4. Thus $J$ is injective and 2 has no predecessor. The orbit

$$
2\longmapsto3\longmapsto4\longmapsto5\longmapsto7\longmapsto9\longmapsto8\longmapsto11
$$

contains every entry of the last column. A repetition on this orbit would, by cancellation, give a positive iterate of 2 equal to 2. This contradicts the absence of a predecessor. A sequence of distinct positive integers visits each finite interval only finitely often, so this orbit tends to infinity. The identity $F_t^k(x)=2J^k(H_t(x))-s$ now gives the conclusion for all four seeds. ∎

The four maps are distinct on the census domain and each has the collision $F_t(1)=F_t(2)$. Their escaping tails are affine copies of a single orbit. The result decides FATE(8) and supplies a counterexample to universal eventual periodicity for each map. The fates of arbitrary individual seeds and the original 1932 permutation question remain separate problems.

The accompanying [exact checker](check_shiftT_parity.py) verifies the affine identities by branch, the finite orbit certificate and the census accounting. Its finite search is used only to certify repetitions.

## What stays hard

The orbit of 2 under J follows T's arithmetic. Whether it has infinitely many *decreases* is not proved. An orbit with only finitely many falls would eventually follow only the rising branches, x -> (4x -+ 1)/3. Those branches have the 3-adic invariant Cantor set of points that never meet 0 (mod 3), and that set contains the integer fixed points 1 and -1. So congruences cannot force a fall. Whether a positive integer other than 1 rises forever is a Mahler-type question (compare Mahler's Z-numbers and Flatto–Lagarias–Pollington, Acta Arith. 70 (1995) 125–147). We do not claim a reduction to any named problem.

## Why tier 1 and not 0

The claim is that the orbit is infinite, which simulation cannot prove. The proof uses only injectivity plus a 6-step finite chain.

Check: `check_shiftT_s8.py` (exit 0).

## Referee report on the original seed-8 result for J

**Verdict: CONFIRMED, tier 1 (agreed).**

The images are the evens ≥ 4, the class 1 (mod 4) and the class 3 (mod 4). These are disjoint, so J is injective and 2 has no preimage. The chain J: 2, 3, 4, 5, 7, 9, 8 checks out (`referee_check.py`). An injective orbit that starts at a non-image point cannot repeat, so the orbit of 8 is infinite.

Overstatement in the census paragraph: "FATE(8) is decided at tier 0 or 1 for every map that has a non-image point" is proved only for the 17 injective non-surjective maps in the stated box. In general, the backward chain from 8 can be infinite and aperiodic, because the inverse of the falling branch, m -> (3m - c0)/2, increases. In that case neither tier-0/1 route applies. Read the sentence as a statement about the box.
