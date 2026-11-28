# Sparse taming sets for 3x+1, 5x+1 and 7x+1 (multi-class)

**Family.** Let a ∈ {3, 5, 7}, m = a^K, and R a set of residues mod m. With c_r = (−r) mod m (so n ↦ (n + c_r)/m, and r = 0 gives n/m):

    T(n) = (n + c_r)/m   if n ≡ r (mod m), r ∈ R     (checked first)
         = n/2           if n even
         = (a n + 1)/2   otherwise.

The **density** of the taming set is |R|/m. A single class can do no better than 1/9 for 3x+1, 1/5 for 5x+1 and 1/7 for 7x+1 (single_class.md). With several classes the density can be made much smaller.

## Settled systems (all PROVED by verified mixed-radix certificate + Lemma A'; tier 2)

| id | a | m | R | density | leaves | max j | cycles (complete list on N+) |
|---|---|---|---|---|---|---|---|
| mb_t27 | 3 | 27 | {17, 26} | 2/27 ≈ 0.074 | 20 | 6 | (1 2) |
| mb_t81 | 3 | 81 | {20, 71, 80} | 1/27 ≈ 0.037 | 67 | 6 | (1 2) |
| mb_t243 | 3 | 243 | {137, 152, 233, 242} | 4/243 ≈ 0.016 | 243 | 19 | (1 2) |
| mb_t729 | 3 | 729 | {182, 380, 395, 425, 668, 719, 728} | 7/729 ≈ 0.0096 | 5417 | 83 | (1 2) |
| mb_f25 | 5 | 25 | {8, 23} | 2/25 = 0.08 | 24 | 4 | (1 3 8) |
| mb_f125 | 5 | 125 | {68, 73, 83, 123} | 4/125 = 0.032 | 146 | 8 | (1 3 8 4 2) |
| mb_s49 | 7 | 49 | {32, 39} | 2/49 ≈ 0.041 | 36 | 4 | (1 4 2) |
| mb_s343 | 7 | 343 | {93, 137, 142, 200, 228} | 5/343 ≈ 0.015 | 985 | 35 | (1 4 2) |

Two alternatives with density 2/27, {20, 26} and {22, 26}, are also certified (check_sparse.py).

**Proof (for each row).**

1. The engine of mixedlib.py returns a set of leaves.
2. `verify_certificate` re-checks them independently:
   * the digit-path trie is complete, so the leaves partition Z;
   * on every leaf, T^j(M t + r) = P t + Q is re-derived symbolically, with a uniform-branch assertion at each step;
   * the closing inequality P < M (or P = M and Q < r) is checked;
   * numeric checks are run, including random 80-bit t.
3. Lemma A' (lemmas.md) gives the finite exceptional set E. Here |E| = 1 in every row, namely E = {1}.
4. Simulating E gives the cycle list.

The certificate is the proof. Its size is the "leaves" column. ∎

For a = 3, 1 lies on the cycle (1 2) because T(1) = 2 and T(2) = 1. Neither 1 nor 2 is in any listed R, which the check confirms.

## Minimality (PROVED)

For each modulus above, no set R with fewer classes can carry a certificate. The plain map (a n + 1)/2, n/2 has expanding rational periodic points, for example −1, (−5 −7 −10) and (−17 ...) for a = 3, and (−1 −2) for a = 5. They are verified exactly from Lyndon words of length ≤ 14 to 20. If R misses all residues of one such cycle mod m, that cycle is still a T̂-cycle of the tamed map, and Lemma B' kills every certificate. An exhaustive branching hitting-set search shows the following.

| a | m | minimum \|R\| (lower bound proved, attained) |
|---|---|---|
| 3 | 9 | 1 (single_class.md) |
| 3 | 27 | 2 |
| 3 | 81 | 3 |
| 3 | 243 | 4 |
| 3 | 729 | 7 |
| 5 | 25 | 2 |
| 5 | 125 | 4 |
| 7 | 49 | 2 |
| 7 | 343 | 5 |

The upper bounds come from the table above. These minima are for the moduli shown, with all classes taken mod the same m.

For 3x+1, the hitting-set search over every odd modulus m ≤ 129 with two classes, and m ≤ 109 with three classes (scratch/hitscan.py, EVIDENCE for the search part), found no certificate outside m = 27 (2 classes) and m ∈ {33, 45, 81} (3 classes; density ≥ 1/27). So the powers of a are where the sparse tamings live. This fits the mechanism:

* mod 3^K, the class −1 catches every up-run of length ≥ K, because x_i + 1 = (3/2)^i(n+1);
* the remaining classes only have to break the finitely many cycle patterns built from runs shorter than K, such as the ghost cycle (−5 −7 −10) for K = 3.

## Frontier statements

* **3x+1.** Taming density → 0 is achievable: 1/9, 2/27, 1/27, 4/243, 7/729, all with GLOBAL proved. The minimal class counts for K = 2, ..., 6 are 1, 2, 3, 4, 7. Whether (min |R|)/3^K → 0 for every K is EVIDENCE only. It holds up to K = 6.
* The sparsest single class for 3x+1 is 1/9. **First open single-class cases:** mb_s3_27 (n ≡ 26 mod 27 → (n+1)/27) and mb_pair_3_27m. Both are obstructed by the ghost cycle (−5 −7 −10). Both converge for every start below 10^6 (EVIDENCE).
* **5x+1.** The sparsest settled taming is 4/125. A single class works only at 1/5.
* **7x+1.** The sparsest settled taming is 5/343. A single class works only at 1/7.

## Tier, novelty, check

* Tier 2: a finite certificate plus Lemma A'. The minimality statements are exact finite obstructions.
* Novelty not checked. I know of no prior work on taming sets for 3x+1-type maps.
* Check: `check_sparse.py`, about 15 to 30 s. It certifies every row (all 10 systems) and runs the exhaustive minimality hitting-set searches.
