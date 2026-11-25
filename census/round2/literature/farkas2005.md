# farkas2005: Farkas's map

## Statement

Farkas's map is defined on the odd positive integers:

    F'(x) = x/3        if x = 0 mod 3
          = (x+1)/2    if x != 0 mod 3 and x = 1 mod 4
          = (3x+1)/2   if x != 0 mod 3 and x = 3 mod 4

Source: H. M. Farkas, "Variants of the 3N+1 conjecture and multiplicative semigroups", in *Geometry, Spectral Theory, Groups, and Dynamics*, Contemp. Math. 387, AMS (2005), 121-127. The theorem is Theorem 1 there. The definition and theorem number are as quoted in E. Yolcu, S. Aaronson, M. J. H. Heule, "An Automated Approach to the Collatz Conjecture", arXiv:2105.14697 v3 (2022), Section 4.2, which re-proves it as Theorem 4.2. I could not get the Farkas paper itself, so the definition above is YAH's transcription.

To get a map on N+, conjugate by x = 2m - 1. Then F'(2m-1) = 2G(m) - 1, where

    G(m) = (m+1)/3   if m = 2 mod 3
         = (m+1)/2   else, if m is odd
         = 3m/2      else (m even)

G(1) = 1. Seed 14 (x = 27): 14 -> 5 -> 2 -> 1.

**Question (GLOBAL).** Does every orbit of G reach 1?

**Answer.** Yes. This is PROVED, at tier 1.

## Relation to round 1 (correction)

Round 1 said that the catalog entry `farkas_s27` was not Farkas's map. In fact it is Farkas's map in YAH's coordinates n = (x-1)/2, which is the map F of YAH Section 4.2, with the terminal 1 -> 0 replaced by 1 -> 1. Exactly, R(n) = G(n+1) - 1 for all n >= 2. check_farkas2005.py verifies this identity for n <= 10^6. So round 1 did study the real Farkas map, and it is genuinely tier 1.

## Proof

Strong induction on m. G(1) = 1. Let m > 1. We show that the orbit reaches a value below m.

* m = 2 mod 3: G(m) = (m+1)/3 < m.
* m odd, m != 2 mod 3: G(m) = (m+1)/2 < m.
* m even, m != 2 mod 3. Write m = 2^a c with a >= 1 and c odd.
  - For j < a, the value 3^j 2^(a-j) c is even and = 0 mod 3. If j = 0, it is m itself, which is 0 or 1 mod 3. So the 3m/2 branch applies a times and gives 3^a c, which is odd and = 0 mod 3.
  - The next step gives z_a = (3^a c + 1)/2.
  - For j >= 1, z_j = (3^j c + 1)/2 = 2 mod 3, because 3^j c + 1 = 1 mod 3 and 2^(-1) = 2 mod 3. So G(z_j) = (z_j + 1)/3 = z_(j-1).
  - After 2a + 1 steps the orbit is at z_0 = (c+1)/2 <= (m/2 + 1)/2 < m.

Every positive value is mapped to a positive value. So the orbit descends below m, and by induction it reaches 1. The only cycle is {1}.

## Tier and why not lower

Tier 1. The proof is valuation bookkeeping with an explicit closed form for the one non-monotone block, which is exactly the tier-1 template from round 1. Tier 0 cannot settle a universal claim.

The literature treats this map as non-trivial. YAH needed an arctic matrix interpretation over 5x5 matrices to prove it automatically (their eq. (9)), and the default settings of AProVE and Matchbox failed on it. So it is a machine-hard but human-easy system: a tier-4-style certificate exists for a tier-1 theorem.

## Check

check_farkas2005.py runs in about 1.4 s. It checks:

* the conjugacy F'(2m-1) = 2G(m) - 1 for m <= 10^6;
* R(n) = G(n+1) - 1 against census/systems.py for 2 <= n <= 10^6;
* the block lemma, with exact intermediate values, for every even m <= 10^6 with m != 2 mod 3;
* descent for every 1 < m <= 10^6;
* the orbit of the seed.

## Referee (round 2)

**Verdict: CONFIRMED, tier 1 (agreed).**

* Citation checked against the YAH v3 text (arXiv:2105.14697v3, Sec. 4.2). The definition of F' is transcribed exactly. YAH's proof is labelled "in the manner of Farkas [Far05, Theorem 1]". [Far05] is Contemp. Math. 387, AMS 2005, pp. 121-127. YAH state that the default configurations of AProVE and Matchbox were "too conservative" and that their own proof uses arctic matrix interpretations. Their timing table lists F as Arctic with dimension 5, which matches the 5x5 claim.
* I re-derived the conjugacy x = 2m-1 by hand, class by class: x = 0 mod 3 <-> m = 2 mod 3; x = 1 mod 4 <-> m odd. I also re-derived the block lemma. z_j = (3^j c + 1)/2 = 2 mod 3 for j >= 1, and (z_j + 1)/3 = z_(j-1). The end value z_0 = (c+1)/2 < m holds for every m >= 2. No hidden case.
* Independent test: every m <= 3*10^5 reaches 1. Round-1 `farkas_s27` equals YAH's F(n) = (n-1)/3, n/2, (3n+1)/2 on every n in [2, 2*10^5), and differs only at n = 1 (1 -> 1 instead of 1 -> 0). So the explorer's correction to round 1 is right.
* Tier 1 cannot be lowered for a universal claim. The argument is valuation bookkeeping with a closed form, the round-1 tier-1 template.
