# trap5_17: 5x+1 with the classes 1 and 7 (mod 8) as a trap

**System.** T(n) = 1 if n ≡ 1 or 7 (mod 8). Otherwise T(n) = n/2 for even n and 5n + 1 for odd n.

**Question (GLOBAL).** Does every orbit reach the fixed point 1? Equivalently: does every 5x+1
trajectory contain a term ≡ 1 or 7 (mod 8)?

**Answer.** Yes, with no exceptions at all. The cycle list of 5x+1 avoiding the trap is empty.
**PROVED**, tier 1. Novelty not checked.

## Proof

Let n be an odd term that is not trapped, so n ≡ 3 or 5 (mod 8).

**Case n ≡ 5 (mod 8).**
* 5n + 1 ≡ 2 (mod 8), so the next odd term is N = (5n + 1)/2, and N ≡ 1 (mod 4).
* So N ≡ 1 (trapped) or 5 (mod 8).
* We have 3N + 1 = (5/2)(3n + 1). Also n ≡ 5 (mod 8) iff 8 | 3n + 1 (i.e. v_2(3n+1) ≥ 3).
  (It is not true that 16 | 3n + 1: for n = 13, 3n + 1 = 40.)
* So v_2(3N + 1) = v_2(3n + 1) − 1: the valuation drops by one at each step, and the run
  continues exactly while the current term is ≡ 5 (mod 8), that is, while v_2 ≥ 3.
* So the run along the expanding 2-adic fixed point −1/3 is finite, and it ends in the class 1
  (mod 8), which is trapped.

**Case n ≡ 3 (mod 8).**
* 8 | 5n + 1, so the next odd term is N ≤ (5n + 1)/8 < n.
* Unless it is trapped (directly, or after a 5-run), N ≡ 3 (mod 8) again.

**Conclusion.** An untrapped orbit would have a strictly decreasing infinite sequence of positive
odd terms, which is impossible. ∎

**Machine certificate.**
* Level 3, B = 4.
* Simple component (5, 2) with lift −1/3, multiplier 5/2.
* Contracting component {0, 3, 4, 6}, worst cycle multiplier 5/8.

**Check.** `check.py` [5], including the equivalence "n ≡ 5 (mod 8) iff 8 | 3n + 1" and
v_2(3N + 1) = v_2(3n + 1) − 1 along the run (added after refereeing).
