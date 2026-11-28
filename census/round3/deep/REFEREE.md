# Referee report: round 3, lens "deep"

Referee: independent adversarial check of family.md, basins.md, split5_3_deep.md and README.md.
I re-derived every proof line by line, ran the prover's three checks (`check_family.py`,
`check_basins.py`, `check_omega.py`: all exit 0, a few seconds each) and wrote
`referee_check.py`. It imports nothing from the prover's libraries. It reimplements the maps from
the written rules, re-derives the classification, executes the B2 construction independently and
re-certifies the Ω numbers with its own θ and counts. It exits 0 in about 15 s
(`nice python3 referee_check.py`).

**Overall:** no claim is WRONG and no claim has a real GAP. There are three small fixes, recorded
below: (i) a range condition in the B4 proof; (ii) one certified decimal in the Ω3 table, which
the prover's own certificate misses by 3.5e-7 (mine certifies it); (iii) the scope wording of Ω2'.
I also make two novelty and overlap remarks. GLOBAL for split5_3 and split5_1 is honestly reported
as OPEN.

## Verdicts

| claim | verdict | notes |
|---|---|---|
| Family classification (P/C/D/K/R/O, 32/8/16/16/8/48) | CONFIRMED | Recomputed from the written definitions. All 8 R targets match. Wording nit: classes R and O depend on gcd(d,a), gcd(d,b), not only on a, b, d mod 4 and the two comparisons (the JSON summary says "decided by a,b,d mod 4 and the comparisons"). "Exactly one class" holds because the definitions are applied in order. |
| Theorem D | CONFIRMED (trivial, tier 1) | S(n) = (cn+d)/2 >= (3n+1)/2 > n. Tested for a,b <= 21, d <= 21 on all odd n < 2000 and random 256-bit n. |
| Theorem K | CONFIRMED | Conjugacy re-derived in both residue cases. Tested for c <= 23, d <= 41 and random 256-bit n. SPLIT(3,1,3) to 3x+3 to Collatz on 3Z also tested. The citation lhf/collatz3 (CLS-014 <=> P1) exists. |
| Lemmas S, R | CONFIRMED | Elementary. Lemma S tested on a,b <= 9, d <= 45 and every odd divisor e. |
| Theorem B1 (X_d) | CONFIRMED (elementary, tier 1) | Brute-force cycle sets equal the coset formula for every odd d <= 151. The count formula holds. Basin = coset on n < 3000 and random 120-bit n. |
| Theorem B2 (accessibility, Sigma_d, gcd(d,6)=1) | CONFIRMED | Re-derived Steps 1-3. They hold: the CRT compatibility (gcd(o, 2·3^{k+s}) divides 2·3^k), the translation L2U2∘(U2L2)^{-1} = −2d/3, the generation of H, and the block-following in Step 3 (the remaining 2-power is >= 2 at odd blocks). My independent implementation runs the proof on 72 random targets for d = 13, 31, 61, 7081. For each target it checks w = x (mod M) and checks every ancestor link exactly. Remark: for d = 7081 the constructed w can have millions of bits, because the 3-adic exponent grows with the number of U2 letters. The proof is still valid; literal orbit simulation is then infeasible, so the referee check verifies the ancestor chain link by link. |
| Cor B3 / Thm B4 | CONFIRMED_WITH_FIX | Fix (B4, case k not a power of 2): the proof picks D = k^a > 2^e and then r in [0, D) with r = −Dδ (mod 2^e) and r mod g in Γ mod g. That needs D >= 2^e·g, so take D = k^a > 2^e·d. With that change the digit-lemma/Cobham argument is complete. Case k = 2^m is correct (4m+d takes the 3x+d branch, so g(4m) = g(3m)). Counts 44/23 for d < 200, the shared list, split_13 cycles {1,5,13} with {1,5} shared, and split_7081's 9 classes / 10 cycles with {569,713} shared all recomputed independently. |
| Ω1 (T1, H_2(1−2/log2 c)) | CONFIRMED | Weighting (c/4)/λ = λ, λ = √c/2 checked. The covering bound needs q < 1/2, i.e. c < 16, and the stated range 5 <= c <= 13 respects that. Cycle-lemma lower bound and mass distribution are standard and correct. log2 ρ* = H_2(q_c) to 1e-20 (Decimal) for c = 5, 9, 13. For c = 5 this restates round 2, as the prover says. |
| Ω2 (upper bound) | CONFIRMED | Standard Chernoff/Perron argument. |
| Ω2' (equality) | CONFIRMED_WITH_FIX (status PARTIAL may be upgraded for T2) | T1 and T3 are complete for negative drift. T2: I re-derived the "sketched" Stirling step. log C(n0+N,N) + log C(J+N−1,N−1) ~ R·[H(p_even) + P_odd·H_geom], using H_geom = H_2(σ)/(1−σ) = (1+μ)H_2(1/(1+μ)) with μ = J/N = σ/(1−σ). That is exactly the entropy of p_e, which equals (Σ p_e ℓ_e) log ρ*. The class of sequences with fixed (n0, N, J) is closed under rotation, so the cycle lemma applies (I checked it exhaustively on small cases). So T2 is in fact proved once this identity is written out. Scope fix: the statement says "every class-O member", but the proof treats negative drift. Positive drift (dim = 1) is proved only for the (3,7)/(7,3) rows (Ω5). These are the only positive-drift O members in the table, so restrict the statement to the table or add the one-line extension of Ω5. |
| Ω3 (certified numbers) | CONFIRMED_WITH_FIX | Independent certificates (θ = p/997, rational entry upper bounds, exact 2x2 criterion; my own multinomial lower bounds) give split5_1 [0.936365, 0.936850], SPLIT(7,1,1) [0.752751, 0.753482], SPLIT(3,5,1) [0.662651, 0.663345], SPLIT(5,7,3) [0.966593, 0.967363]. All are inside the claimed intervals. Fix: the prover's own certificate for SPLIT(3,5,1) gives U = 0.66334735 > 0.663347 (θ = 2.295 is off the optimum 2.29486). `check_omega.py` hid this with a 1e-6 tolerance. True log2 ρ* = 0.6633452. Either quote 0.663348 for the prover's certificate or cite this referee certificate. The prover's check also takes log2 of the rational μ in floating point; the margins make this harmless, but it is not strictly exact. |
| Ω4 (non-descending starts) | CONFIRMED | Proof re-derived: block factor 1+d/(cx) <= 1+d/2^m and (1+d/2^m)^m <= 2 give P_j >= 1/2, and there is one n per residue word. Exponents 0.58069 (split5_3) and 0.93686 (split5_1) are certified by my upper certificates (0.5806857... and 0.9368495). |
| Ω5 (positive drift gives positive measure) | CONFIRMED | E X = (1/2)log(21/16) > 0 and X >= log(3/4) > −log 2. The union-bound/first-big-excursion argument and the excursion end-point property are correct. No integer divergence is claimed, which is correct. |
| Z3 (3Z part is SPLIT(1,5,1)) | CONFIRMED | Lemma S with e = 3 = 3 (mod 4). Mod-3 invariance in both directions. Tested on m < 20000 and random 256-bit m. |
| split5_3 GLOBAL, rising family 4^K−3 | OPEN, honestly labelled | Section 6 claims nothing beyond round 2. The (c) remark n0 ≢ 2 (mod 5) is correct. |

Systems table:

| system | verdict | notes |
|---|---|---|
| class D members (e.g. SPLIT(3,5,3)) | CONFIRMED | New to the catalog but trivial (tier 1, one-line monotonicity). The prover says so. |
| SPLIT(1,3,1), split_3 = SPLIT(3,1,3), other class K | CONFIRMED | Exact equivalences. GLOBAL stays open, correctly. |
| X_d = SPLIT(1,1,d) | CONFIRMED | Tier 1, elementary. |
| split_5, split_73, split_97, splitB_7, splitB_71 BASIN | CONFIRMED | Novelty correction: the split_5 basin rule (5 \| n) is already in results/split_5_s27.md (commit 304d67b). The concurrent round-3 lenses `progressions` (applications_basins.md) and `domains` (split_family.md, Theorem P) derive the same congruence/non-congruence dichotomy for the split catalog members. Results agree; credit should be shared. |
| split_13, split_7081 BASIN (nonautomatic) | CONFIRMED (with the B4 fix) | Same overlap remark as above. |

## Did anything overclaim?

* README "Each check ... under 10 s" is accurate. The check docstrings say 1-2 min, which is
  harmless.
* README lists Ω4 as O(X^{dim Ω}). That is exact for T1 and T3. For T2 it is O(X^{log2 ρ*}),
  which is the same number once the T2 identity above is written out.
* "Settled" systems: the genuinely new nontrivial settled content is B2-B4 (a full BASIN answer
  for an infinite family of settled maps, including nonautomaticity) and the Ω-dimension theory.
  The new GLOBAL answers (class D) are trivial, and class K gives equivalences, not answers. The
  prover labels them this way, so nothing is presented as deeper than it is.
* Literature novelty was not checked by the prover. I did not check it either (no web search).

## Repairs (optional, none blocking)

1. basins.md, Theorem B4, case k not a power of 2: replace "choose a with D = k^a > 2^e" by
   "D = k^a > 2^e·d".
2. split5_3_deep.md Ω3 table and README: SPLIT(3,5,1) upper value. Write 0.663348, or cite the
   referee certificate (θ = p/997), which gives 0.663345. Tighten the 1e-6 tolerance in
   `check_omega.py`.
3. split5_3_deep.md Ω2': write out the T2 entropy identity (above), which upgrades T2 to PROVED.
   Restrict "every class-O member" to negative-drift members, plus the (3,7)/(7,3) rows via Ω5.
4. basins.md / README: note that split_5's basin was already settled, and note the overlap with
   round3/progressions and round3/domains.
