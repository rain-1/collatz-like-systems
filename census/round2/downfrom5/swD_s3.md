# swD_s3

**Rule.** P(n) = sigma(D(n)), where D is round 1's perm_d (2q -> 5q; 8q+r -> 5q+(r+1)/2 for r = 1,3,5,7) and sigma swaps 3 <-> 4, 11 <-> 12 and 14 <-> 15 (mod 20). So |P - D| <= 1, and P is a permutation of Z_{>0} that is affine on classes mod 32, with slopes 5/2 (even n, rises) and 5/8 (odd n, falls).

**Question (FATE).** What is the fate of the seed 3? (Under D itself, 3 lies on the 3-cycle 3 -> 2 -> 5.)

| answer | status | tier |
|---|---|---|
| infinite | PROVED | 2 |

## Proof

Let A = {n : n ≢ 3 (mod 4)}. The exact residue graph of P mod 4 shows that A is closed: for each class in A and each of its subclasses mod 32, the image lies in A. The check script computes this from the affine pieces. Also 3 is not in A and P(3) = sigma(2) = 2 is in A. By injectivity the orbit of 3 never returns, so it is infinite.

The orbit begins 3, 2, 5, 4, 10, 25, 16, 40, 100, 250, 625, 392, ... It is not monotone: there are 838 falls in the first 3000 steps. The branch itinerary is not eventually periodic. Every composite slope is 5^h / 2^e with e >= h >= 1, which is not an integer, so the lemma in swT9_15_s8.md applies. Infinitely many rises follow because the orbit is unbounded. Infinitely many falls are *not* proved: inside the trap mod 80 the rising (even) classes contain a cycle, so congruences cannot force a fall.

## Tier 2, and why not tier 1

The certificate is a congruence class invariant, verified by a 32-row table, which is tier 2. Tier-1 routes are not available:
- *Monotonicity.* The orbit falls hundreds of times in the computed range.
- *5-adic bookkeeping.* No separator exists mod 5^k for k <= 4.
- *Smaller modulus.* No separator exists for K < 4.

A referee could argue that a single mod-4 class is "valuation bookkeeping" and so tier 1. Compared with the T analogue swT9_15_s8, which needs a mixed modulus 36, this is the weaker tier-2 claim.

**Role.** This shows the cube phenomenon of swT9_15_s8 is not special to T. Composing perm_d with a sigma that moves values by at most 1 turns a map with no known infinite orbit into one whose 3-orbit is certified by a congruence trap, while the falls keep their arithmetic character. Over all 10946 matchings sigma of adjacent swaps mod 20, the orbit of 3 returns in 6719 cases, is separated by a congruence (K in {20, 40, 80, 160}) in 1147, and is unresolved in 3080. Every separated case with sigma of size <= 2 has at most one fall: it is eventually monotone, which is tier 1.

Check: `check_swD_s3.py` (exit 0).

## Referee

**Verdict: CONFIRMED, tier 2 (agreed, weak).**

Independent check: P(n+128) - P(n) ∈ {80, 320}. Both are ≡ 0 (mod 4) and ≡ 0 (mod 20), and the latter keeps the sigma correction unchanged. So it suffices to verify P(n) ≢ 3 (mod 4) for the residues n ≢ 3 (mod 4) mod 128. `referee_check.py` does this, plus the periodicity, for n < 5120. In fact every n with P(n) ≡ 3 (mod 4) is ≡ 3 (mod 4) (its classes mod 128 are listed in the output), and P(3) = 2, so 3 never returns. Injectivity holds because D is a bijection and sigma an involution. The itinerary lemma applies: slopes 5/2 and 5/8 compose to 5^h/2^e with e ≥ h ≥ 1, never an integer, and the denominator argument works with 2 in place of 3.

On tier: unlike twochanW, the closure is not readable off the rule as a valuation statement. It needs the sigma table mod 20 combined with the classes mod 32 or 128. So it is a congruence-table certificate, tier 2, consistent with the round-1 precedent par_7_1_s3 (a mod-7 trap, tier 2). I found no monotone or valuation argument.
