# Provable relatives of the open mixed entries div23_5n1 (CLS-002/059) and m3_b (CLS-004/061)

The task asked: can the open entry be made provable by adding one sparse taming class, and what is the sparsest class that works? The added class has the form n ≡ r (mod q) → (n + c)/q, with c ≡ −r (mod q). It is checked either first ("first") or only in place of the expanding branch ("last").

## div23_5n1 + one class (PROVED, complete answer)

Base map: 2|n → n/2; else 3|n → n/3; else 5n+1.

**Theorem D.**

1. (Necessity, every c, either priority.) If div23_5n1 plus one class r mod q admits a descent certificate, then (q, r) is in the following list:
   * "first": (2,0), (2,1), (3,1), (3,2), (4,2), (4,3), (5,1), (5,3), (6,2), (6,5), (8,7), (10,6), (15,11), (15,13), (30,26);
   * "last": (2,1), (3,2), (6,5).
2. (Sufficiency, c = (−r) mod q.) Every pair in the list except "first" (2,0) and (4,2) is certified, so GLOBAL holds for it.
   * "first" (2,0) is the open map itself.
   * "first" (4,2) is unresolved: there is no certificate within budget and no obstruction was found.

   The complete cycle lists (Lemma A', computed and asserted by check_relatives.py) are:

   | priority, (q, r) | complete cycle list |
   |---|---|
   | first (2,1) | (1) |
   | first (3,1) | (1), (5 26 13) |
   | first (5,1) | (1) |
   | first (6,2) | (1 6 3), (5 26) |
   | first (10,6) | (1 6) |
   | last (2,1) | (1) |
   | every other certified pair: first (3,2), (4,3), (5,3), (6,5), (8,7), (15,11), (15,13), (30,26); last (3,2), (6,5) | (1 6 3) |

   *(Correction after refereeing: an earlier version said that every certified pair has the single cycle (1 6 3). That was false for the six pairs listed separately above.)*

**So the sparsest single class that makes div23_5n1 provable by descent is density 1/30.** It is unique:

* **mb_d23_30**: n ≡ 26 (mod 30) → (n+4)/30; else the div23_5n1 rules. Certificate: 12 leaves, depth 4.

The most interesting system in the list is the 2-adic one:

* **mb_d23_8**: n ≡ 7 (mod 8) → (n+1)/8; else the div23_5n1 rules. Certificate: 93 leaves, depth 24, density 1/8.
* **mb_d23_4**: n ≡ 3 (mod 4) → (n+1)/4. Certificate: 11 leaves, depth 9.

*Proof of necessity.*

* Base cycles. div23_5n1 has the expanding cycle (−1 −4 −2), with multiplier 5/4, and the expanding rational cycle through −42/13 (5 steps, multiplier 25/12). There are 9 more cycles with words of length ≤ 11; all are verified exactly in check_relatives.py.
* By Lemma B', an added class set must catch each of these cycles: it must contain a residue of one of its points. Under "last" priority, only a point in the 5n+1 branch counts.
* Bound on q (repaired). The cycle (−84 −42 −21 −7 −34 −17) is an expanding *integer* cycle: −84 → −42 → −21 → −7 → 5·(−7)+1 = −34 → −17 → 5·(−17)+1 = −84, with multiplier 5²/(2⁴·3) = 25/24. Both (−1 −4 −2) and this cycle consist of integers, so they lie in Z_q for every q, and Lemma B' applies to both for every q. One residue r must catch both, so q | y − z for some y on the first cycle and z on the second. Each such difference is nonzero, and |y − z| ≤ 83. Hence q ≤ 83, for every c and either priority. (Under "last" only points in the 5n+1 branch count, which only shrinks the set of admissible differences.)
  *(Correction: an earlier version used the −42/13 cycle here and concluded q ≤ 45. That argument fails when 13 | q, because −42/13 is not in Z_13.)*
* Refined Lemma B'. Let q = q₁q₂, where q₂ collects the primes of q that divide the denominator d of a base cycle. If no admissible point y of the cycle has y ≡ r (mod q₁), then the integers n ≡ y (mod (M0·q₁)^N), whatever their residue mod q₂, follow the cycle for N steps without being caught, because they already miss the class mod q₁. The argument of Lemma B' then goes through. So each cycle forces r ≡ y (mod q₁) for some admissible point y.
* The exhaustive scan over q ≤ 83 with this criterion, against all eleven exactly verified cycles (words ≤ 11), leaves exactly the list above. As a consistency check, the older coarse scan to q ≤ 3000 (which skips any cycle whose denominator meets q) gives the same list. ∎

## m3_b + classes (PROVED, complete answer for at most two classes)

Base map: 3|n → n/3; n ≡ 1 (mod 3) → (4n−1)/3; n ≡ 2 (mod 3) → (4n+1)/3. Both 1 and −1 are T̂-fixed points with multiplier 4/3: (4·1−1)/3 = 1 and (4·(−1)+1)/3 = −1. The point 1 is a real fixed point, and −1 is a ghost.

**Theorem M.**

* **One class r mod q.** The class must contain both of the integer points 1 and −1, so q | 2. The only single class is "odd n → (n+1)/2". It is certified (tier 1, 4 leaves), and GLOBAL holds with the **two** cycles (1) and (2 3): 2 ≡ 2 (mod 3), so 2 → (4·2+1)/3 = 3, and 3 is odd, so 3 → (3+1)/2 = 2. *(Correction: an earlier version said that every orbit reaches 1 here. That is false.)*
* **Two classes mod q (q ≥ 3).** They must contain 1 mod q and −1 mod q, which are distinct, so they are exactly {1, −1} mod q.
  * The expanding rational 2-cycle (1/7, −1/7) has multiplier 16/9. By the refined Lemma B' (see Theorem D), write q = 7^e·q₁ with 7 ∤ q₁. Then q₁ must divide a numerator of ±1/7 ∓ 1, which is 6 or 8. So every prime of q lies in {2, 3, 7}.
  * The expanding rational 4-cycle (7/25, 1/25, −7/25, −1/25) has multiplier 256/81. Its denominator 25 is prime to 42, so it lies in Z_q for every such q, and q must divide a numerator of y ∓ 1 for y on it. These numerators are 18, 24, 26 and 32, so q ≤ 32.
  * The exhaustive scan over 3 ≤ q ≤ 32 (refined criterion, all base cycles with words ≤ 11 plus the two cycles above) leaves exactly q ∈ {3, 4, 6, 8}.
  * *(Correction: an earlier version derived "q | 6 or 8" directly from the 1/7-cycle. That step fails when 7 | q, and the second cycle is needed.)*
  * All four are certified, and each has the single cycle (1). The sparsest is q = 8 (density 1/4):
    * **mb_m3b_8**: n ≡ 1 (mod 8) → (n+7)/8; n ≡ 7 (mod 8) → (n+1)/8; else the m3_b rules. Certificate: 36 leaves, depth 3. GLOBAL: every orbit reaches the fixed point 1.

So m3_b is far more rigid than div23_5n1. Its two expanding fixed points ±1 pin any taming set to the classes ±1, and a further rational cycle caps the modulus at 8. Sparser tamings of m3_b need at least three classes; I did not search these.

## Tier, novelty, check

* Tier 2: the certificates, plus exact obstructions for necessity. mb_d23_30 and mb_m3b_8 are close to tier 1, since their certificates have depth ≤ 4.
* Novelty not checked.
* Check: `check_relatives.py` (about 10 s). It does the following:
  * certifies the four named systems;
  * enumerates the exact expanding cycles of both base maps;
  * verifies exactly the cycles used in the bounds and proves q ≤ 83 (div23) and q ≤ 32 (m3_b);
  * runs the exhaustive scans with the refined Lemma B' (plus the old coarse scan to q ≤ 3000 for div23 as a consistency check);
  * certifies every survivor and asserts its complete cycle list, including (1), (2 3) for m3_b + odd class.

These systems do not settle CLS-002 or CLS-004 themselves. They locate the open maps exactly one "class" away from provable ones. In the case of m3_b, they show that the obstruction is the pair of fixed points ±1 together with the 2-cycle ±1/7.
