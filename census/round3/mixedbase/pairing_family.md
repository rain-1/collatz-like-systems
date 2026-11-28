# The Farkas pairing family P(a, K, x*)

**Parameters.** a ≥ 3 odd, K ≥ 1, m = a^K, x* an odd integer with gcd(a, x*) = 1. Put

    r ≡ x*·2^{-1} (mod m),   c = (m − 1)x*/2,   b = (2 − a)x*,

    T(n) = (n + c)/m      if n ≡ r (mod m)        (checked first)
         = n/2            if n is even
         = (a n + b)/2    otherwise.

T maps Z to Z. For x* = 1 it maps N+ to N+, and for x* = −1 it maps N0 = {0, 1, 2, ...} to itself. Note that x* is a fixed point of the odd branch: (a x* + b)/2 = x*.

Instances already in the catalog:

* farkas_s27 (YAH's form of Farkas's map) is P(3, 1, −1) on N0. The catalog's 1 → 1 replaces 1 → 0.
* farkas5m_s27 (round 2) is P(5, 1, 1).

Everything with K ≥ 2, and everything with a = 7 or larger, is new here. Honest caveat: the K = 1 family (every odd a) is a routine extension of Farkas's and round 2's block argument. mb_pair_5_5m = P(5, 1, −1) is exactly the reflection n ↦ −n of farkas5m_s27 = P(5, 1, 1), restricted to n ≤ 0, and mb_pair_7_7m uses the same routine argument; both are only nominally new. The substantive new case is (a, K) = (3, 2) (mb_pair_3_9p, mb_pair_3_9m) together with the obstructions P4–P5.

New named systems (in systems.py):

| id | rule | domain |
|---|---|---|
| mb_pair_3_9p | n ≡ 5 (mod 9) → (n+4)/9; else even n → n/2; else (3n−1)/2 | N+ |
| mb_pair_3_9m | n ≡ 4 (mod 9) → (n−4)/9; else even n → n/2; else (3n+1)/2 | N0 |
| mb_pair_7_7m | n ≡ 3 (mod 7) → (n−3)/7; else even n → n/2; else (7n+5)/2 | N0 |
| mb_pair_5_5m | n ≡ 2 (mod 5) → (n−2)/5; else even n → n/2; else (5n+3)/2 | N0 |
| mb_pair_3_27m (OPEN) | n ≡ 13 (mod 27) → (n−13)/27; else even n → n/2; else (3n+1)/2 | N0 |
| mb_pair_5_25p (OPEN) | n ≡ 13 (mod 25) → (n+12)/25; else even n → n/2; else (5n−3)/2 | N+ |

mb_pair_3_9m is the 3x+1 map (in the (3n+1)/2 form), tamed by one class of density 1/9. Every orbit of it is proved below to end in 0 or in (1 2). No plain descent certificate exists for it (P4), so the round-2 machinery cannot prove this. (A run-accelerated certificate does exist: it is the P3 proof, re-proved by pairlib.py. *Corrected wording; an earlier version said "no certificate of any kind".*)

## P1. Block lemma (PROVED)

Let n be odd with n ≢ r (mod m) and n ≠ x*. Write n − x* = 2^j u with u odd (j ≥ 1 because n and x* are odd), and j = qK + ℓ with 0 ≤ ℓ < K. Then

    T^{j+1+q}(n) = z_ℓ,   where z_k := (x* + a^k u)/2.

*Proof.*

1. **Up-run.** Put x_i = x* + a^i 2^{j−i} u for 0 ≤ i ≤ j, so x_0 = n. For i < j, x_i is odd. For i ≥ 1, x_i ≡ x* (mod a), while r ≡ x*/2 (mod a). These differ because a ∤ x*, so x_i ≢ r (mod m). For i = 0 this is the hypothesis. So the odd branch applies: (a x_i + (2 − a)x*)/2 = x* + a^{i+1}2^{j−i−1}u = x_{i+1}.
2. **One halving.** x_j = x* + a^j u is even and ≢ r (mod m), by the same residue argument (j ≥ 1). So T(x_j) = z_j.
3. **Down-run.** For k ≥ K we have a^K | a^k u, so z_k ≡ x*/2 ≡ r (mod m). Then T(z_k) = (x* + a^k u + (m − 1)x*)/(2m) = (x* + a^{k−K}u)/2 = z_{k−K}.

So the orbit passes x_0, ..., x_j, then z_j, z_{j−K}, ..., z_ℓ. That is j + 1 + q steps. ∎

The run-accelerated map is S(n) := z_ℓ on such n, and S := T elsewhere. Every S-step is at least one T-step.

## P2. Symmetry and scaling (PROVED)

T_{−x*}(−n) = −T_{x*}(n), and T_{x*}(x* n) = x* T_1(n), for all n ∈ Z. Both follow by direct substitution, using that x* is invertible mod m and odd. So P(a, K, −1) on N0 is the negative half of P(a, K, 1) on Z. Also T_{x*} restricted to x*Z is a copy of T_1.

## P3. GLOBAL for K = 1 (every a) and for (a, K) = (3, 2) (PROVED, tier 1)

**Theorem.** Let K = 1, or (a, K) = (3, 2), and put B = 1 if K = 1 and B = 5 if (a, K) = (3, 2). Then every integer orbit of T is eventually periodic, and every cycle contains a point with |n| ≤ B|x*|.

*Proof.* We show that every n with |n| > B|x*| has a later iterate of smaller absolute value.

* **n ≡ r (mod m).** |T(n)| ≤ (|n| + |c|)/m < |n|, because |c| = (m−1)|x*|/2 < (m−1)|n|.
* **n even.** |n/2| < |n|.
* **Otherwise.** n is odd, n ≠ x*, and |u| ≤ |n − x*|/2^j ≤ (|n| + |x*|)/2^j.
  * K = 1: ℓ = 0, so |S(n)| ≤ (|x*| + |u|)/2 ≤ (3|x*| + |n|)/4 < |n| when |n| > |x*|.
  * (3, 2): if ℓ = 0, then j ≥ 2 and |S(n)| ≤ (|x*| + (|n|+|x*|)/4)/2 < |n|. If ℓ = 1, then |S(n)| ≤ (|x*| + 3(|n|+|x*|)/2)/2 = (5|x*| + 3|n|)/4 < |n| when |n| > 5|x*|.

So every orbit returns infinitely often to the finite set {|n| ≤ B|x*|}. Hence it repeats a value, and every cycle meets that set. ∎

**Cycle lists** (simulation of the finite set; check_pairing_family.py prints the cycles for every x* with |x*| ≤ 43):

| system | domain | all cycles |
|---|---|---|
| P(a, 1, 1), every a ∈ {3, 5, ..., 13} | Z | (0), (1) |
| P(a, 1, 1), every a ∈ {3, 5, ..., 13} | N+ | (1) |
| P(3, 2, 1) = mb_pair_3_9p | Z | (0), (1), (−2 −1) |
| P(3, 2, 1) = mb_pair_3_9p | N+ | (1) |
| P(3, 2, −1) = mb_pair_3_9m | N0 | (0), (1 2) |
| P(7, 1, −1) = mb_pair_7_7m | N0 | (0) |
| P(5, 1, −1) = mb_pair_5_5m | N0 | (0) |

The cycle list for P(a, 1, ±1) holds for every odd a ≥ 3, not only the checked ones. Proof for x* = 1: by P3 every cycle meets {−1, 0, 1}. Here T(0) = 0 and T(1) = 1. For −1: it is caught (≡ r) only when a = 3, and then T(−1) = 0. For a ≥ 5, T(−1) = 1 − a, which is even, and the orbit continues. The finite check covers a ≤ 13. For general a, the orbit of −1 is not computed here, so for a ≥ 15 the Z-statement is "every orbit is eventually periodic, and every cycle meets {−1, 0, 1}". The N+ statement, cycle (1) only, holds for every a: on N+ the set is {1}.

## P4. No plain descent certificate, for any parameters (PROVED)

x* is odd, and x* ≢ r (mod a). So x* ∈ Z_2 × Z_a is a T̂-fixed point with multiplier a/2 > 1, and Lemma B' (lemmas.md) applies. This is the general form of round 2's observation for farkas5m_s27, and it holds for the whole family: **the finite-table method (tier 2) never works here, but the closed form does.**

## P5. Where the closed form stops: explicit obstructions (PROVED)

The run-accelerated map S removes x* (its tail leaves handle j → ∞), but other expanding periodic points remain:

* **a ≥ 5, K ≥ 2.** Let y = (2 − a)x*/(4 − a). Then T̂(y) = 2y and T̂(2y) = y, with multiplier a/4 > 1.
  * y is odd 2-adically, and 2y is even.
  * y − x*/2 = −a x*/(2(4 − a)) is divisible by a exactly once, so y ≢ r (mod a²).
  * 2y − x*/2 = x*(4 − 3a)/(2(4 − a)) is prime to a.

  For K = 1 the point y is caught, which is consistent with P3. For a = 5, x* = 1 this is the real cycle (3 6).
* **a = 3, K ≥ 3.** The cycle (5x*, 7x*, 10x*) has multiplier 9/8. Here 2·5x* − x* = 9x*, which is divisible by 9 but not by 27; 2·7x* − x* = 13x*; 2·10x* − x* = 19x*. So the cycle is caught exactly when K ≤ 2. For x* = 1 it is the real cycle (5 7 10) of 3x−1. For x* = −1 it is the negative 3x+1 cycle (−5 −7 −10), a ghost that is invisible on N0.

Both are T̂-periodic and avoid x*, so S is affine near them. By Lemma B', no certificate exists, even with tail leaves.

**Result.** The family splits exactly. Certificates (plain or accelerated) are impossible for (a ≥ 5, K ≥ 2) and for (a = 3, K ≥ 3). The closed-form proof P3 works exactly for K = 1 and for (3, 2). The accelerated engine (pairlib.py) independently re-proves P3 for x* = ±1 and every listed a, and it does not terminate on the obstructed cases.

## Open cases (EVIDENCE only)

The first open members are:

* **mb_pair_3_27m** = P(3, 3, −1): 3x+1 with n ≡ 13 (mod 27) → (n−13)/27. All 0 ≤ n < 2·10^5 reach (0) or (1 2).
* P(3, 3, 1): cycles (1) and (5 7 10) seen.
* **mb_pair_5_25p** = P(5, 2, 1): cycles (1) and (3 6) seen.

A heuristic drift computation predicts convergence for every K when a = 3. Per odd block, E log = log a·Σ_j 2^{−j}(j mod K) − 4 log 2. This is < 0 for every K when a = 3, for K ≤ 5 when a = 5, and for K ≤ 3 when a = 7. Simulation agrees:

* P(7, 4, 1) and P(7, 5, ±1) have orbits passing 10^60;
* every member with negative drift that I tested converged for all starts below 2·10^5 (2·10^4 when m > 10^4).

So the open cases are open for the usual Collatz reason: each carries an expanding ghost or real cycle, which no descent-type argument can get past (Lemma B').

## Tier and novelty

* P1 to P3 are tier 1: valuation bookkeeping plus a closed-form block, the round-1 template.
* P4 and P5 are short exact obstructions.

Literature: the K = 1 instances with a = 3 are Farkas's 2005 theorem, as transcribed in census/round2/literature/farkas2005.md. To my knowledge the m = a^K generalisation, the family-wide statement on Z, and the sharp K-frontier are new. Novelty not checked beyond this repository: no web search was done.

Check: `check_pairing_family.py` (about 4 s; exits 0). It checks:

* the block lemma: exhaustive for |n| ≤ 6000 in the main cases and |n| ≤ 800 in the others, plus 300 random 200-bit n of both signs, over a ∈ {3..13}, K ≤ 4 and seven values of x*;
* the symmetry and scaling identities;
* the descent inequality of P3 for 4.6·10^6 instances;
* all cycle lists;
* accelerated certificates for x* = ±1;
* the exact obstructions of P4 and P5 for a ≤ 17 and K ≤ 7.
