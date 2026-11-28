# perm12_s7: a new mixed-slope permutation with a non-monotone infinite orbit

**Rule (a permutation of Z_{>0}; affine on classes mod 12).**

| input class | T(n) | output class | slope |
|---|---|---|---|
| n ≡ 0 (mod 6) | 2n − 9 | 3 (mod 12) | 2 |
| n ≡ 1 (mod 6) | 4n + 19 | 23 (mod 24) | 4 |
| n ≡ 2 (mod 6) | (2n + 8)/3 | 0 (mod 4) | 2/3 |
| n ≡ 4 (mod 6) | 2n − 1 | 7 (mod 12) | 2 |
| n ≡ 5 (mod 6) | (2n − 7)/3 | 1 (mod 4) | 2/3 |
| n ≡ 3 (mod 12) | (n + 3)/3 | 2 (mod 4) | 1/3 |
| n ≡ 9 (mod 12) | 2n − 7 | 11 (mod 24) | 2 |

Each branch maps the k-th element of its input class to the k-th element of its
output class. Both columns of classes partition Z, so T is a bijection.

**Provenance.** I found this map by a random search over mixed-slope class
permutations (`scratch/randperm2.py`). The filters were: a congruence separator
exists, every cycle of the trap contains a fall, the trap has a p-adic
aperiodicity witness, and the backward orbit is not monotone. Its slope set
{2, 4, 2/3, 1/3} differs from every catalog permutation: the 1932 type has
2/3, 4/3; perm_d has 5/2, 5/8; perm_c and the suffix permutations differ too, as
does mix3. Non-conjugacy is not proved; "not conjugate to the catalog" rests
only on this difference in shape.

**Question.** FATE of 7.

| claim | status | tier |
|---|---|---|
| 7 never returns; the orbit is infinite | PROVED | 2 |
| the orbit has infinitely many falls and an itinerary mod 12 that is not eventually periodic | PROVED | 2 |
| no union of residue classes mod K < 12 separates 7; mod 12 is the least modulus | PROVED | — |
| the periodic points below 3000 are exactly 8 (fixed) and {21, 35} | EVIDENCE | — |
| GLOBAL (complete cycle list) | OPEN | — |

## Proof

U = {1, 5, 9, 11} (mod 12) is forward closed:

* 1 ↦ 4n+19, which is 11 (mod 12);
* 9 ↦ 2n−7 = 24q+11, which is 11 (mod 12);
* 5 ↦ (2n−7)/3 = 8q+1, which is 1, 9 or 5 (mod 12);
* 11 ↦ (2n−7)/3 = 8q+5, which is 5, 1 or 9 (mod 12).

7 ∉ U and T(7) = 47 ∈ U. By induction every T^j(7), j ≥ 1, lies in U, so none
equals 7. T is injective, so a repetition T^i(7) = T^j(7) with i < j would give
T^{j−i}(7) = 7. The orbit is therefore infinite (and unbounded). It begins
7, 47, 29, 17, 9, 11, 5, 1, 23, 13, 71, 45, 83, ….

The fall classes in U are 5 and 11. Every closed walk in U passes through one of
them, since the non-fall classes 1 and 9 only map to 11. So falls recur at least
every 2 steps (Lemma F). Every closed walk contains a 2/3 step, and the other
slopes (2 and 4) have no factor 3, so v₃(product) ≤ −1. Lemma I then shows the
itinerary is not eventually periodic, so there is no affine pump along the orbit.

U contains the 2-cycle {21, 35} (21 ≡ 9, 35 ≡ 11). So U is a separator, not a
cycle-free trap. This is legitimate only because T is injective.

## Why tier 2 and not tier 1

* No forward pump exists (Lemma I).
* The orbit has infinitely many falls (Lemma F).
* The backward orbit 7, 4, 2, 3, 6, 15, 12, 14, 39, 24, 32, 44, … is not monotone
  either (checked for 40 steps). I found no tier-1 backward argument, so the
  "backward loophole" of round 2 (auto_mix3_s7) is not known to apply. This is
  evidence, not proof.
* The least separating modulus is exactly 12 (check part 4).

**Novelty:** new system; novelty not checked. Check: `check_perm12_s7.py`
(exit 0, under 1 s).
