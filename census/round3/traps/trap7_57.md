# trap7_57: 7x+1 with the classes 5 and 7 (mod 8) as a trap

**System.** T(n) = 1 if n ≡ 5 or 7 (mod 8). Otherwise T(n) = n/2 for even n and 7n + 1 for odd n.

**Question (GLOBAL).** Is every orbit eventually periodic, and what is the complete list of
cycles? Equivalently: does every 7x+1 trajectory meet 5 or 7 (mod 8) or reach 1?

**Answer.** Yes. Every 7x+1 trajectory either contains a term ≡ 5 or 7 (mod 8) or reaches the
cycle (1 8 4 2). For T, the only cycle is (1 8 4 2). **PROVED**, tier 1. Novelty not checked.

## Proof

The trap classes are odd, so it suffices to follow the odd terms. Let n be an odd term that is
not trapped, so n ≡ 1 or 3 (mod 8).

**Case n ≡ 3 (mod 8).**
* 7n + 1 ≡ 6 (mod 8), so the next odd term is N = (7n + 1)/2, and N ≡ 3 (mod 4).
* So N ≡ 3 or 7 (mod 8). If N ≡ 7, the orbit is trapped.
* We have 5N + 1 = (7/2)(5n + 1). Also n ≡ 3 (mod 8) iff 8 | 5n + 1 (i.e. v_2(5n+1) ≥ 3).
  (It is not true that 16 | 5n + 1: for n = 11, 5n + 1 = 56.)
* So v_2(5N + 1) = v_2(5n + 1) − 1: the valuation drops by one at each step of this run. The run
  continues exactly while the current term is ≡ 3 (mod 8), that is, while v_2 ≥ 3, so it ends
  after finitely many steps.
* It can only end at a term ≡ 7 (mod 8), which is trapped. (The run is the expanding 2-adic
  fixed point −1/5 of (7x + 1)/2, multiplier 7/2.)

**Case n ≡ 1 (mod 8).**
* 8 | 7n + 1, so the next odd term satisfies N ≤ (7n + 1)/8 ≤ n, with equality only for n = 1.
* If N ≡ 3, 5 or 7 (mod 8), the orbit is trapped (directly, or by the first case).

**Conclusion.** An untrapped orbit therefore has odd terms ≡ 1 (mod 8) that strictly decrease
until they reach 1, and 1 → 8 → 4 → 2 → 1. ∎

**Machine certificate (Theorem 2).**
* Level m = 3, B = 13.
* Simple component: the 2-cycle (3, 6) with lift −1/5, multiplier 7/2.
* Contracting component: {0, 1, 2, 4}. Its worst cycle is 1 → 0 → 4 → 2 → 1, multiplier 7/8,
  lifting to 8 (the cycle of 1).
* Potential: Q = 64, P_7 = 180, φ = {0:0, 1:181, 2:118, 4:55}.

**Check.** `check.py` [5] verifies:
* the certificate, independently (verify.py);
* the congruence facts of the hand proof, for odd n < 2^14, including the equivalence
  "n ≡ 3 (mod 8) iff 8 | 5n + 1" and v_2(5N + 1) = v_2(5n + 1) − 1 along the run (added after refereeing; previously
  only the identity 5N + 1 = (7/2)(5n + 1) was tested);
* 200 random n of up to 256 bits, each of which reaches A or ≤ B (evidence only).
