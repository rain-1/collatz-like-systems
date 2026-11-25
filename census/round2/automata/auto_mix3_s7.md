# auto_mix3_s7

**Map** (a permutation; the slopes 1/2, 3/2 and 3/4 mix the bases 2 and 3):
6|n → n/2; n ≡ 2 (mod 6) → (3n+2)/2; n ≡ 4 (mod 12) → (3n−8)/4; n ≡ 10 (mod 12) → (3n−2)/4; n odd → (3n+1)/2.
Branch form: 6q→3q, 6q+2→9q+4, 12q+4→9q+1, 12q+10→9q+7, 2q+1→3q+2. The input classes and the output classes (0, 4, 1, 7 mod 9 and 2 mod 3) each partition the positive integers.

**Question.** FATE of 7.

**Answer.** Infinite. **Status:** PROVED. **Tier:** 1.

The forward orbit looks chaotic: 7, 11, 17, 26, 40, 28, 19, 29, 44, 67, 101, 152, 229, 344, 517, 776, 1165, … It has many falls and no visible closed form.

## How it was found, and why it collapses

A CEGAR SAT search over random mixed-slope residue permutations looked for base-2 or base-3 automaton certificates (satlib.search, exact closure test on each candidate). For this map and seed it found a **7-state base-3 certificate**, verified exactly. SAT shows that none exists with ≤ 6 base-3 states and none with ≤ 9 base-2 states. Every constraint in that search is necessary, so these bounds are proofs. The check re-proves ≤ 4 base-3 states in pure Python. A minimal 7-state certificate, at first sight a tier-3 object.

It is not. Two facts collapse it.

1. **The automaton is a congruence plus a finite table.** Its accepted set is exactly {n : 3 ∤ n} minus E = {5, 7, 8, 10, 14, 16, 22}. The non-multiples of 3 are forward closed: a non-multiple of 3 lies in 2 mod 6, 4 mod 12, 10 mod 12 or is odd, and those branches output 9q+4, 9q+1, 9q+7 (all 1 mod 3) or 3q+2. E is backward closed inside them, because it contains the part of the backward orbit of 7 that is prime to 3, namely {7, 10, 14, 16, 22}. That is already a tier-2 argument.
2. **The backward orbit has a one-line closed form (tier 1).** We have 9·2^(k+1) ≡ 0 (mod 6), so T(9·2^(k+1)) = 9·2^k for all k ≥ 0, and 9 → 14 → 22 → 16 → 10 → 7. So 7 has infinitely many distinct backward iterates. A periodic point of a bijection has a finite backward orbit, so 7 is not periodic. Injectivity then makes the forward orbit infinite.

**Proof (tier 1).** Bijectivity follows from the partition check. The backward chain 9·2^k → … → 7 uses one branch formula plus five evaluations. Then apply the bijection argument above. □

## Why not tier 0

The claim is infinite.

## Lens data

Of 14 mixed-slope permutations for which this search found a base-2 or base-3 certificate (3–8 states), 13 have a backward orbit that eventually satisfies an affine recurrence with period ≤ 3. That gives the same tier-1 argument. The 14th (6q→4q, 6q+2→12q+1, 6q+4→4q+2, 6q+1→12q+5, 6q+3→4q+3, 6q+5→12q+9, seed 7) has a backward orbit that is eventually strictly increasing (n ↦ 3n/2 or (3n+2)/2 on evens). That is tier 1 by monotonicity, and its certificate is "odd minus a finite set" (tier 2). In this sample, automata for mixed-slope permutations never pushed the tier above 2. **The backward-orbit loophole** is a recurring reason: for a bijection, the forward orbit is infinite iff the backward orbit is, and the backward direction is often trivial.

**Base-2 size.** In base 2 the smallest certificate has ≥ 10 states (SAT: none ≤ 9). The set {3 ∤ n} minus {7, 10, 14, 16, 22} gives a verified 13-state certificate. So a tier-1 system can need a ≥ 10-state binary automaton: certificate size and difficulty are unrelated here.

## Referee

**Verdict:** CONFIRMED. Tier 1 is AGREED.

I re-implemented the map from the formula and compared it with systems.py on 1..2·10^5. I checked that the outputs land in the classes 0 mod 3, {1, 4, 7} mod 9 and 2 mod 3, so the map is a bijection. I checked T(9·2^(k+1)) = 9·2^k for k < 300 (it also holds as algebra, because 6 | 9·2^(k+1)), and the chain 9→14→22→16→10→7. The argument is sound. The points 9·2^k are pairwise distinct backward iterates of 7, so 7 is not periodic, and injectivity makes the forward orbit infinite.

I also checked the description of the 7-state base-3 automaton as "non-multiples of 3, minus E". E is backward closed inside the non-multiples of 3: the preimages of 5 and 14 are 3 and 9, both multiples of 3; the preimage of 8 is 5; and 7←10←16←22←14 stays inside E.

Tier 0 is impossible, because the claim is infinite.

**Unverified side claims.** The SAT bounds are not reproducible in this environment (pysat is missing): none with ≤ 6 base-3 states, and none with ≤ 9 base-2 states. Only ≤ 4 base-3 states is re-proved. The "14 mixed-slope permutations" statistics have no script or data in the lens directory, so they are anecdotal.

**Final tier: 1.**
