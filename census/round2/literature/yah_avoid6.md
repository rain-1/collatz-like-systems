# yah_avoid6: Collatz with the class 6 mod 8 sent to 1

## Statement

The map is C_K with K = {6}: n = 6 mod 8 goes to 1, even n goes to n/2, odd n goes to 3n+1. The cycle {1, 4, 2} avoids 6 mod 8, so it is still a cycle.

**Question (GLOBAL).** Does every orbit enter {1, 4, 2}?

This holds exactly when every C-trajectory either reaches 1 or meets 6 mod 8. That is Proposition 4.7 of Yolcu-Aaronson-Heule, arXiv:2105.14697 v3 (2022), restated as part of their Theorem 4.10, which covers the classes 2, 3, 4 and 6 mod 8.

**Answer.** Yes. This is PROVED, at tier 1 (on the 1/2 border).

## YAH's proof (a tier-2 method)

Take the residue graph of C mod 8 with class 6 deleted. YAH list its eight simple cycles. Each one composes to an affine contraction, for example (0,4,2,5,0) gives (3n+8)/8. check_yah_avoid6.py confirms that the maximum mean log-slope cycle of this graph is -0.0959 < 0.

A caution: as written, YAH's step "the path is a concatenation of simple cycles" needs a potential function to be rigorous, because walks interleave cycles. Max mean < 0 gives one. Choose rational weights c_r with c_s * slope(r->s) < c_r. Then Phi(n) = c_(n mod 8) n decreases strictly once n is past a finite threshold, and the small cases form a finite table.

## Direct proof (tier 1)

Track only the odd iterates o of a C_6 orbit. Class 7 never occurs after a step, because 3o + 1 = 6 mod 8 there and the orbit goes to 1.

* **o = 3 mod 8:** 3o + 1 = 2 mod 8, and the next odd value is o' = (3o+1)/2, which is 1 or 5 mod 8.
* **o = 1 mod 8:** 3o + 1 = 4 mod 8. Halving gives 2 or 6 mod 8, and 6 means the orbit goes to 1. Otherwise o' = (3o+1)/4 < o (for o > 1), and o' is 1 or 5 mod 8.
* **o = 5 mod 8:** 3o + 1 = 0 mod 8, so o' <= (3o+1)/8 < o.

A value that is 3 mod 8 can only follow one that is 5 mod 8. Now take the odd iterates that are not 3 mod 8. If such an o is followed by a 3-class value, the next value after that is at most (3(3o+1)/8 + 1)/2 = (9o+11)/16 < o. So the non-3-class odd iterates strictly decrease until the orbit reaches 1 or meets 6 mod 8. A strictly decreasing sequence of positive integers is finite, so every orbit ends in {1, 4, 2}.

## Tier and why not lower

The direct proof uses mod-8 transitions and one two-step block inequality, with no table. I classify it as tier 1. A referee could fairly call it the easiest kind of tier 2, since it is a congruence graph with a descent inequality. Tier 0 cannot settle a universal claim. This is the closest the YAH family comes to the middle tier, and it still collapses.

## Check

check_yah_avoid6.py verifies:

* every transition fact, on all odd n < 2^16;
* each odd-to-odd descent claim, for odd o < 10^6;
* the mod-8 max mean cycle < 0;
* a survey of n <= 10^6, which is evidence only.

## Referee (round 2)

**Verdict: CONFIRMED, tier 1 (agreed).**

* Source checked: YAH v3 Prop. 4.7 (proof by the eight simple cycles of the mod-8 graph) and Thm 4.10 (classes 2, 3, 4, 6). The explorer's remark that "concatenation of simple cycles" needs a potential to be rigorous is fair.
* I re-derived every case.
  - o = 7: goes to 1.
  - o = 3: o' = 12q + 5, which is 1 or 5 mod 8. The even value 3o+1 = 2 mod 8 is never forbidden.
  - o = 1: either the middle even value is 6 mod 8 (goes to 1), or o' = (3o+1)/4 is 1 or 5 mod 8 and o' < o for o > 1.
  - o = 5: o' <= (3o+1)/8. If o' = 3 mod 8, then o'' <= (9o+11)/16 < o for o >= 2.
  - A starting value that is even, or 3 mod 8, enters the class-1/5 subsequence after at most one odd step.
  - So the class-1/5 odd iterates strictly decrease. There is no finite table and no threshold.
* Independent survey: every n <= 3*10^5 enters {1, 2, 4}.
* Tier: the argument is a mod-8 case split plus one two-step inequality, valid for all n. That is tier 1 by the round-1 convention. It is not the tier-2 pattern of "inequality plus exhaustive finite table".
