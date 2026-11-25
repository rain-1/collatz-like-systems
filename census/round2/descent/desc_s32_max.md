# desc_s32_max

**Rule.** Even n → n/2. For odd n, apply 3n+1 if n mod 32 ∈ S0 = {1,3,5,7,11,13,15,17,21,23,25,29}. For the other four odd classes (9, 19, 27, 31 mod 32), apply n+1.
**Question (GLOBAL).** Is every positive orbit eventually periodic?
**Answer.** Yes. Every orbit reaches the cycle 1 → 4 → 2 → 1.
**Status.** PROVED. Tier 2.

## Proof

The exhaustive 2-adic search (Lemma C) closes every class:

* 144 classes in all, with moduli up to 2^30;
* at most k = 44 steps;
* every stored affine form T^j(n) = P t + R is re-verified by direct iteration, and the classes are checked to partition Z.

Every closed class has P < 2^K, so T^j(n) < n except for finitely many t. The exceptional set of positive integers is E = {1}. By Lemma A every orbit reaches 1, and {1, 4, 2} is the only cycle. ∎

## Why lower tiers fail (proved)

* **No short descent.** The class n ≡ 495114287 (mod 2^29) has first descent time 44: on it T^j(n) ≥ n for every j < 44. By Lemma C, *every* descent certificate has k ≥ 44. So a one-block or few-block argument cannot work. Odd steps on 7, 11, 15, 23 (mod 32) take n ↦ (3n+1)/2 and grow, and chains of them occur.
* **The reason for the depth.** The 2-adic rational 227/13 is periodic with period 13. Its branch word is 15, 14, 7, 22, 11, 2, 17, 20, 26, 29, 24, 28, 30 (mod 32), and its multiplier is 3^5/2^8 = 243/256. This is the maximum-mean cycle of the cylinder graph, at −0.0040 per step. It contracts, but only barely. Points near it climb for dozens of steps before the deficit 256/243 builds up, and the certificate has to resolve them up to modulus 2^29–2^30.
* **Tier 1 (monotonicity, valuation bookkeeping, exact conjugacy):** there is no monotone quantity on fewer than 44 steps (above). No conjugacy is known.

## Where this sits on the frontier

S0 is one of the 17 certifiable sets of the maximum size, 12 of 16 odd classes, at modulus 32 (exhaustive scan, lemmas.md). It is also maximal: adding any of 9, 19, 27, 31 creates a verified growing 2-adic cycle, with multipliers 243/128, 81/64, 9/8 and 3/2 (see desc_s32_plus9). So 3n+1 is applied on 3/4 of the odd classes and descent is still certifiable. The near-critical 243/256 cycle of this system becomes the 243/128 obstruction of S0 ∪ {9}.

## Check

`check_desc_s32_max.py` runs in a few seconds. It rebuilds and verifies the 144-class certificate, checks E = {1}, the cycle {1, 4, 2}, and the 44-step witness, and verifies the 227/13 cycle exactly.

## Referee

**Verdict: PROVED (confirmed). Tier 2 (agreed). The "why lower tiers fail" section is overstated.**

* My independent engine (`referee_check.py`, part 1) uses only the step function and its own refinement rule. It reproduces k = 44 and E = {1}. It produces 677 leaves at level ≤ 31 because it refines more finely, and first-descent times are intrinsic, so they agree. All n < 3·10^5 reach 1. I checked the 227/13 cycle exactly: residues 15, 14, 7, 22, 11, 2, 17, 20, 26, 29, 24, 28, 30, with multiplier 243/256.
* **A much shorter tier-2 proof (a one-step weighted potential).** Take the mod-32 transition graph: an odd r has the single edge to (u r + 1) mod 32, and an even r has edges to r/2 and r/2 + 16. Its maximum cycle mean is −0.00401, which is exactly the 243/256 cycle. So integer weights c(r) exist (listed in `referee_check.py`, between 200 and 2068) with q·c(target) ≤ (499/500)·c(source) on every edge.
  * Let V(n) = n·c(n mod 32). Then V(Tn) ≤ (499/500)·V(n) + 2068.
  * So V, which takes integer values, strictly decreases whenever n > 5170.
  * Every n ≤ 5170 reaches 1 by simulation.
  * This proves GLOBAL with a 32-entry table and one step.
* **Consequence for the explorer's claims.** "No one-block or bounded-block argument can work" holds only for plain certificates of the form T^j(n) < n. That is what Lemma C bounds, and the bound k ≥ 44 is correct for that form. With weights, one step is enough. So the depth of 44 is an artefact of the certificate format, not a measure of difficulty.
* **Tier.** The tier stays 2, because the proof needs a 32-entry weight table plus a finite check up to 5170. No tier-1 argument exists in the s8_35 style: a fixed bounded-block argument without weights is a plain certificate, and Lemma C rules those out below 44 steps.
