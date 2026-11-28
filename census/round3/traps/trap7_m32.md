# trap7_m32: 7x+1 with the trap {5, 7, 13, 23, 27} (mod 32)

**System.** T(n) = 1 if n mod 32 ∈ {5, 7, 13, 23, 27}. Otherwise T(n) = n/2 for even n and 7n + 1
for odd n.

**Answer (GLOBAL).** Every 7x+1 trajectory meets the trap or reaches (1 8 4 2). This is one of the
8 smallest provable odd trap sets mod 32 for 7x+1 (5 of the 16 odd classes). Every one-element
subset deletion is H. **PROVED** by a Theorem-2 certificate; tier 2. Novelty not checked.

**Certificate (level 5, B = 13).**
* **Simple components:** (19, 6), with lift −1/5 and multiplier 7/2; and (20, 10, 21), with lift
  −4/3 and multiplier 7/4.
* **Contracting component:** {0,1,2,4,8,9,16,18,25}, worst cycle multiplier 7/8 (the trivial
  cycle). Q = 64, P_7 = 180.
* **Trivial components:** 13 nodes.

Compare trap7_57 (mod 8, 2 of the 4 odd classes). The mod-32 set traps a smaller fraction
(5/16 < 1/2) and keeps two expanding 2-adic cycles alive as simple components.

**Check.** `check.py` [2], [5].
