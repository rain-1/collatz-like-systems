# perm1932_1cycle: 1-cycles of Collatz's 1932 permutation

## Statement

The map is g(3q) = 2q, g(3q+1) = 4q+1, g(3q+2) = 4q+3. This is the catalog map `perm_1932` (round-1 seeds 8 and 44), the inverse of Collatz's f(2n) = 3n, f(4n+1) = 3n+1, f(4n-1) = 3n-1. It has the same cycles. In Simons's notation it is P(1,3,2,2).

On non-multiples of 3, g(x) = (4x + eps)/3 with eps = -1 for x = 1 mod 3 and eps = +1 for x = 2 mod 3. So g(x) > x except at the fixed point x = 1. On multiples of 3, g(x) = 2x/3 < x.

A **1-cycle** is a cycle with one local minimum: one maximal block of k >= 1 non-multiples of 3 followed by one block of l multiples of 3.

**Question (CYCLES, restricted to 1-cycles).** List all 1-cycles.

**Answer.** Exactly (1), (2, 3) and (4, 5, 7, 9, 6). This is PROVED, at tier 4.

**Literature.** J. L. Simons, "Cycles and divergent trajectories for a class of permutation sequences", arXiv:2205.10582 (2022), Corollary 11(a), states this for m <= 2. That proof relies on a numerical lower bound X0 = 10^6 for cycle elements, obtained from a computer search, and on Rhin's bound. The proof below handles m = 1 without any X0 search. As far as I know this exact argument is not in print; I checked only Simons's version.

## Proof

**Case l = 0.** All terms are non-multiples of 3, and g is strictly increasing on them except at 1. So the only such cycle is (1).

**Case l >= 1.** Let x0 be the minimum.

* **Descent block.** The descent needs x_k = 3^l e and x0 = 2^l e with 3 not dividing e. The intermediate values 3^(l-j) 2^j e are multiples of 3.
* **Ascent block.** Put Y_i = 3^i x_i. Then Y_(i+1) = 4 Y_i + 3^i eps_i, so

      3^k x_k = 4^k x0 + S,   where S = sum over i < k of eps_i 4^(k-1-i) 3^i,

  and |S| <= 4^k - 3^k.
* Substituting gives e D = S with D = 3^(k+l) - 2^(2k+l), which is nonzero. Since e >= 1, |D| <= 4^k - 3^k < 4^k.

**k is bounded in terms of l.** Put A = 3^(k+l) and B = 2^(2k+l). Then |A - B| < 4^k gives A > B - 4^k = 4^k (2^l - 1). So (3/4)^k > (2^l - 1)/3^l >= 2^(l-1)/3^l, which gives

    k < (l log(3/2) + log 2) / log(4/3) <= 2l + 3.

**Transcendence step (l >= 2).** Let Lambda = (2k+l) log 2 - (k+l) log 3. Then |D| = max(A,B)(1 - e^(-|Lambda|)) >= B min(|Lambda|, 1)/2 = 4^k 2^(l-1) min(|Lambda|, 1). Combined with |D| < 4^k this gives |Lambda| < 2^(1-l). Rhin's bound, with H = 2k + l < 3.82 l + 4.82, gives (3.82 l + 4.82)^(-13.3) < 2^(1-l). This forces l <= 118. The case l = 1 is covered by the scan below.

**Exact finite part.** For every l <= 600 and k <= 2l + 3, the pairs with |D| <= 4^k - 3^k are exactly (1,1), (2,1), (3,2), (4,3) and (7,5). For each of them, enumerate every e <= (4^k - 3^k)/|D| not divisible by 3 and test x0 = 2^l e directly. The only cycles of the right shape are:

* (k, l, e) = (1, 1, 1): the cycle (2, 3);
* (k, l, e) = (3, 2, 1): the cycle 4 -> 5 -> 7 -> 9 -> 6 -> 4.

## Tier and why not lower

Tier 4, because Rhin's effective irrationality measure is needed for l > 600. Without it the argument is a finite scan.

The reasons lower tiers fail are the same as for steiner_1cycle (evidence, not a proof). The cycle equation is a near-coincidence 3^(k+l) ~ 2^(2k+l), and no congruence or automaton argument is known that bounds such coincidences.

**Comparison with round 1.** The FATE of the orbit of 8 under this map is tier 5. So restricting the question from "all orbits" to "1-cycles" moves this map from tier 5 to tier 4, the same move that Steiner's theorem makes for 3x+1.

## Check

check_perm1932_1cycle.py, about 0.2 s, does:

* the exact scan for l <= 600 and k <= 2l + 3;
* the e-enumeration and simulation;
* the k-range lemma, checked numerically;
* the l = 0 monotonicity, for x < 10^5;
* the Rhin cutoff, 118 < 600.

## Referee (round 2)

**Verdict: CONFIRMED, tier 4 (agreed).**

* I re-derived each step.
  - g(x) = (4x + eps)/3 off multiples of 3, with eps = -1 for x = 1 mod 3 and eps = +1 for x = 2 mod 3.
  - Y_(i+1) = 4 Y_i + 3^i eps_i, which gives e D = S with |S| <= 4^k - 3^k.
  - The k-bound k < 1.41 l + 2.41.
  - |D| >= 4^k 2^(l-1) min(|Lambda|, 1), using 1 - e^(-x) >= (1 - 1/e) x on [0, 1]. Hence |Lambda| < 2^(1-l) for l >= 2.
  - Rhin with H = 2k + l < 3.82 l + 4.82, which gives the cutoff l <= 118.
  - The e-enumeration tests the exact cycle shape, so it is exhaustive.
* Independent tests.
  - A scan with a wider k range (k < 3l + 10, l < 400) finds the same five candidate pairs.
  - A brute-force search of every cycle with minimum <= 2*10^5 finds (1), (2,3), (4,5,7,9,6) (one block each) and the 12-element cycle through 44 (four blocks). So nothing is missed below 2*10^5.
* Citation checked in the arXiv text: Simons Cor. 11(a) says "for m <= 2 no other cycles than (1), (2,3), (4,6,9,7,5)". His Lemma 10 applies Rhin with u1 = 2K + L and u2 = -(K + L), as here. The explorer's proof drops the X0 = 10^6 search for m = 1, and that is legitimate.
  - Side note, not affecting this claim: Simons's Cor. 11(b) lists the 44-cycle as 10 elements with m = 3. Under this map it has 12 elements (it also contains 93 and 62) and 4 descent blocks. Either his list has a typo or his m is counted differently.
* Tier: the same near-coincidence 3^(k+l) ~ 2^(2k+l) as in Steiner's theorem. No elementary bound is known, so tier 4 stands. The why_not_lower is evidence, not a proof.
