# desc_s32_d65

**Rule.** Even n → n/2. For odd n, apply 3n+65 if n mod 32 ∈ S0 = {1,3,5,7,11,13,15,17,21,23,25,29}. For the other odd classes (9, 19, 27, 31 mod 32), apply n+65.
**Question (CYCLES).** List all cycles, and prove the list is complete.
**Answer.** There are exactly 8 cycles. They are listed by minimum, with their lengths:

| minimum | length |
|---|---|
| 1 | 21 |
| 5 | 5 |
| 7 | 29 |
| 13 | 4 |
| 39 | 5 |
| 65 | 3 |
| 299 | 8 |
| 1135 | 13 |

**Status.** PROVED. Tier 2.

## Proof

Since 65 ≡ 1 (mod 32), multiplying by 65 preserves every residue class mod 32. Also 3(65x)+65 = 65(3x+1) and 65x+65 = 65(x+1). So x ↦ 65x conjugates the 2-adic extension of desc_s32_max to this map. The descent multipliers are therefore the same, and the certificate has the same shape: 144 classes, levels up to 2^30, k = 44. The engine rebuilds it directly for this map and verifies it independently.

The exceptional set E has 63 elements, the largest being 1519. Running each element of E until it repeats gives exactly the 8 cycles above. By Lemma A, every cycle minimum lies in E, so the list is complete. Every orbit is eventually periodic. ∎

## Why lower tiers fail

* **Certificate depth:** every certificate needs k ≥ 44 (Lemma C, same 44-step class as desc_s32_max).
* **A finite table is needed:** the cycle list is not determined by any congruence or valuation rule. In particular, the cycle through 1135 is the integer image of the near-critical 2-adic cycle: 1135 = 65·227/13, period 13, multiplier 243/256. The near-critical orbit that forces the deep certificate is realized here as a genuine integer cycle.

## Check

`check_desc_s32_d65.py` verifies the certificate, recomputes E, checks the 8 cycle minima, and verifies that 1135 lies on a 13-cycle with multiplier 243/256.

## Referee

**Verdict: PROVED (confirmed). Tier 2 (agreed).**

* The conjugacy x ↦ 65x is correct (65 ≡ 1 mod 32). My independent engine reproduces k = 44, |E| = 63 and max E = 1519. Simulation of all n < 3·10^5 finds exactly the 8 cycles, with the stated minima and lengths.
* **Alternative proof with a one-step potential.** The mod-32 transition graph is the same as for desc_s32_max, because 3r + 65 ≡ 3r + 1 (mod 32). So the same weights give V(Tn) ≤ (499/500)·V(n) + 65·2068, and V strictly decreases for n > 336050. Every n ≤ 336050 is simulated, which takes about 15 s in `referee_check.py`. They reach exactly the 8 listed cycles. Every cycle contains a point with n ≤ 336050, so the list is complete. This is a second, independent proof.
* **Tier.** It stays 2, since a finite table is unavoidable for a list of 8 cycles. As with desc_s32_max, the "k ≥ 44" depth applies only to plain descent certificates.
