# trap3_m32: 3x+1 with the trap {7, 15, 25} (mod 32)

**System.** T(n) = 1 if n mod 32 ∈ {7, 15, 25}. Otherwise T(n) = n/2 for even n and 3n + 1 for
odd n.

**Answer (GLOBAL).** Every Collatz trajectory meets 7, 15 or 25 (mod 32), or reaches 1. This is
one of the 9 smallest provable odd trap sets mod 32 (3 of the 16 odd classes, density 3/16).
Compare YAH's single class 3 mod 8 (density 1/4 of the odd classes). **PROVED** by a Theorem-2
certificate; tier 2. Novelty not checked.

**Certificate (level 5, B = 122).**
* **Simple component:** (31, 30), the −1 run, multiplier 3/2.
* **Contracting component:** the 27 remaining nodes. Its worst cycle is
  6 → 19 → 26 → 29 → 24 → 12 → 22 → 27 → 18 → 9 → 28 → 14 → 23 → 6, multiplier 3^5/2^8 = 243/256,
  lifting to 1006/13.
* **Potential:** Q = 256, P_3 = 406.

Where the three residues act:

* **15.** A −1 run C: 2^t u − 1 → … → 3·2^{t−1}u − 1 lowers v_2(n+1) by one per odd step, so
  every run that starts with v_2(n+1) ≥ 5 (class 31) passes through the class 15 (mod 32),
  where v_2(n+1) = 4, and is trapped there.
* **7.** It catches the terms with v_2(n+1) = 3 that are ≡ 7 (mod 32). The terms ≡ 23 (mod 32)
  are handled by the contracting component.
* **25.** 25 ≡ −7 lies on the 9/8 cycle −5 → −14 → −7 → −20 → −10 (residues 27, 18, 25, 12, 22).

Deleting any one residue leaves a homoclinic orbit (H), so all three are necessary.

**Check.** `check.py` [2], [5].
