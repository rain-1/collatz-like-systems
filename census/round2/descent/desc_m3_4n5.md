# desc_m3_4n5

**Rule.** 3 | n → n/3; n ≡ 1 (mod 3) → 4n+5; n ≡ 2 (mod 3) → 2n+2.
**Question (GLOBAL).** Is every positive orbit eventually periodic?
**Status.** OPEN. Tier 5.

## What is proved

**Proposition.** No descent certificate exists, for any M and any k.

*Proof.* Work in Z_3. We have −5 ≡ 1 (mod 3), so −5 → 4(−5)+5 = −15. Then −15 ≡ 0 (mod 3), so −15 → −5. The step multipliers are 4 and 1/3. The partial products from −5 are 4 and 4/3, both greater than 1. Lemma B applies. ∎

This system lies in the mod-3 family of the brief, M3(a,c1,b,c2), with i1 = 4+5 ≡ 0 and i2 = 4+2 ≡ 0. By Theorem 2 of lemmas.md, members of that type have a certificate iff a ≤ 2 and b ≤ 2. Those members are one-block (tier 1). Here a = 4, the smallest multiplier coprime to 3 that is above the frontier. As with SPLIT, the mod-3 family has an empty middle tier.

## Evidence

* In the random model each non-multiple step changes log n by (log 4 + log 2)/2 − 1.5·log 3 ≈ −0.61 on average.
* Every n ≤ 2·10^4 reaches one of three cycles: {1, 9, 3}, {2, 6} and the 4-cycle through 16 (16 → 69 → 23 → 48 → 16).

## Why lower tiers fail

* **Tier 2:** no certificate exists (proved above).
* **Congruence invariants:** cannot prove convergence.
* **Tier 3/4:** none found.

## Check

`check_desc_m3_4n5.py` verifies the obstruction. It also checks Theorem 2 on 2916 parameter tuples. Each tuple is either certified, or Lemma-B obstructed, or has an invariant nonzero class.

## Referee

**Verdict: OPEN (agreed). Final tier 5. The no-certificate proposition is confirmed.**

* The orbit −5 → −15 → −5 in Z_3 has multiplier 4/3, and the partial products are 4 and 4/3. This was checked exactly from the table in `referee_check.py`. Lemma B applies. As for split7_1, it also rules out every residue-weighted potential n·c(n mod 3^K).
* Theorem 2: I checked the case analysis. The pairs (1,·), (·,2) and (2,1) contain a loop of nonzero classes. The remaining pairs (0,0), (2,0) and (0,1) have full blocks, and Lemma D applies to them. The proof is correct.
* Simulation: every n < 10^5 reaches one of {1, 9, 3}, {2, 6} or {16, 69, 23, 48}. This matches the claim and is evidence only.
* I found no conjugacy (a shift n + α cannot linearise all three branches at once) and no finite-state structure. Tier 5 stands.
