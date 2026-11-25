# desc_s8_35

**Rule.** Even n → n/2; n ≡ 3, 5 (mod 8) → 3n+1; n ≡ 1, 7 (mod 8) → n+1.
**Question (GLOBAL).** Is every positive orbit eventually periodic?
**Answer.** Yes. Every orbit reaches the cycle {1, 2}.
**Status.** PROVED. Tier 2 (the smallest case in the middle; arguably at the edge of tier 1).

## Proof

The minimal stopping-time certificate (Lemma C) has 6 classes. Each row gives the class, the number of steps j, the value of T^j, and the condition for descent.

| class | j | T^j(n) | descent |
|---|---|---|---|
| n = 2t | 1 | t | t ≥ 1 |
| n = 8t+1 | 2 | 4t+1 (via 8t+2) | t ≥ 1 |
| n = 8t+5 | 3 | 6t+4 (via 24t+16, 12t+8) | always |
| n = 8t+7 | 2 | 4t+4 (via 8t+8) | always |
| n = 16t+3 | 6 | 9t+2 (via 48t+10, 24t+5, 72t+16, 36t+8, 18t+4) | always |
| n = 16t+11 | 4 | 12t+9 (via 48t+34, 24t+17, 24t+18) | always |

Each intermediate value lies in the residue class that its next branch requires. For example, 24t+5 ≡ 5 (mod 8) and 24t+17 ≡ 1 (mod 8). The classes partition the positive integers. The only positive integer that does not descend is n = 1 (E = {1}), and 1 → 2 → 1. By Lemma A every orbit reaches {1, 2}, and that is the only cycle. ∎

## Why lower tiers fail

* **One block fails.** A block is one odd step plus the halvings it guarantees. On n ≡ 3 (mod 8) the block is n ↦ (3n+1)/2, which grows. The class 3 (mod 16) needs two odd steps and 6 steps in total. By Lemma C every certificate needs k ≥ 6. So no monotonicity or one-block argument works.
* **Tier 1 by conjugacy:** no conjugacy to a trivial map is known.
* **Referee note.** With only 6 rows a referee may call this "tier 1 with bookkeeping". It is the smallest member of the middle tier. Its depth comes from the cylinder-graph cycle with mean log-multiplier −0.096 per step, which means two odd steps and enough halvings to give a per-cycle multiplier of 9/16.

## Frontier context

Mod 8 has 16 subsets S (lemmas.md). Six are certifiable, and the largest has |S| = 2: S = {1,5} and S = {3,5}. Adding 7 creates the 2-adic fixed point −1. Adding 1 to {3,5} gives a verified growing cycle (see `family_scan.out`).

## Check

`check_desc_s8_35.py` rebuilds and independently verifies the certificate. It also checks E = {1} and the cycle {1, 2}, and that class 3 (mod 16) needs all 6 steps.

## Referee

**Verdict: PROVED (confirmed). Tier lowered to 1.**

I checked each of the 6 rows of the table by hand, and they are all correct. My independent engine (`referee_check.py`, part 1) gives k = 6 and E = {1}.

**Tier-1 proof (two-block valuation bookkeeping).** Let B(n) be the next odd value after an odd n. Then:

* n = 8t+1 gives B(n) = 4t+1 < n for t ≥ 1.
* n = 8t+7: 8 divides n+1, so B(n) ≤ t+1 < n.
* n = 8t+5: 3n+1 = 8(3t+2), so B(n) ≤ 3t+2 < n.
* n = 8t+3 gives B(n) = (3n+1)/2 = 12t+5, which is ≡ 1 or 5 (mod 8). By the two lines above, the next block takes it to at most max((3n+3)/4, (9n+5)/16), which is < n for n ≥ 3.

So every odd n > 1 drops below itself within two blocks, and every orbit reaches 1. The argument uses only the residues mod 8 that define the map and no refinement table. This is the "valuation bookkeeping" of tier 1. The explorer's own note anticipated this. The k ≥ 6 bound is correct, but it only says that a single block is not enough. A fixed two-block argument is still tier 1.
