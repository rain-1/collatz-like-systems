# Round 3, lens "deep": split5_3, split5_1 and the whole split family

Scope: a deep attack on CLS-049/065 split5_3 = SPLIT(5,1,3) and CLS-048/064 split5_1 = SPLIT(5,1,1),
and a classification of the family SPLIT(a,b,d): even n -> n/2, n = 1 (mod 4) -> a n + d,
n = 3 (mod 4) -> b n + d (a, b, d odd).

**Bottom line.**
* GLOBAL for split5_3 and split5_1 is **still OPEN**. I did not find a proof, and section 6 of
  split5_3_deep.md records exactly what blocks each line of attack.
* What was settled:
  * the **whole family** is classified: descent, provably divergent, exactly conjugate to a parity
    map, reducible, or open;
  * **BASIN** is solved completely for two infinite families of settled maps, which covers 7
    catalog systems;
  * the **exact Hausdorff dimension of the non-descending set** is computed for every split map.
    That dimension separates split5_3 (0.581) sharply from split5_1 (0.937).

Files: `family.md` (classification), `basins.md` (basin theorems), `split5_3_deep.md` (Ω theory and
the deep attack), `systems.py` (step functions, ids `split_a{a}_b{b}_d{d}`), libraries
`family_lib.py`, `basins_lib.py`, `access_lib.py`, `omega_lib.py`, checks `check_family.py`,
`check_basins.py`, `check_omega.py`. Each check exits 0 and runs in under 10 s. Everything they test is
exact integer or rational arithmetic, except the clearly labelled float displays.

## General theorems

| id | statement | status | file / check |
|---|---|---|---|
| Thm D | SPLIT(a,b,d) with a+d = 3b+d = 2 (mod 4) and a,b >= 3: every orbit diverges, no cycles | PROVED (easy, tier 1) | family.md / check_family T4 |
| Thm K | SPLIT(a,b,d) with a+d = 3b+d = 2 (mod 4), min(a,b) = 1, c = max(a,b): on odd values x = (n-d)/2 conjugates it exactly to x -> x/2, (cx + d(c-1)/2)/2 | PROVED | family.md / T5 |
| Lemma R, S | scaling conjugacy on eZ; reduction of GLOBAL to a smaller-d member when e = gcd(d,a) > 1 and the other branch contracts | PROVED | family.md / T6 |
| Classification | each of the 128 members with a,b <= 7, d <= 15 lies in exactly one class: P 32, C 8, K 16, D 16, R 8, O 48 | PROVED | family.md / T1 |
| Thm B1 | X_d = SPLIT(1,1,d), every odd d: cycles <-> cosets of <2> in Z/d (explicit elements and lengths); basin of n = coset of n mod d | PROVED | basins.md / check_basins B1 |
| Thm B2 | Sigma_d (split_d / splitB_d), gcd(d,6)=1: every merging class meets every progression compatible with the <2,3>-class mod d | PROVED | basins.md / B2 (proof executed constructively on random targets) |
| Cor B3, Thm B4 | basin of a cycle is a congruence set iff it is alone in its <2,3>-class; otherwise not ultimately periodic on any progression and not automatic in any base | PROVED | basins.md / B0, B3a, B4 |
| Thm Ω1 | i.i.d.-type members (SPLIT(c,1,d), c = 1 mod 4, d = 3 mod 4; SPLIT(1,c,d), d = 1 mod 4; 5 <= c <= 13): dim_H Ω = H_2(1 - 2/log_2 c); split5_3: 0.5806841232 | PROVED | split5_3_deep.md / check_omega O0, O1 |
| Thm Ω2, Ω2' | every class-O member with negative drift, and the positive-drift (3,7)/(7,3) rows (via Ω5): dim_H Ω = log_2 min_θ ρ(M_θ) (2x2 transfer matrix) | upper bound PROVED for all members; equality PROVED for T1, T2 (split5_1 type; the Stirling/entropy identity is written out, following the referee) and T3 with negative drift, and for the (3,7)/(7,3) rows | split5_3_deep.md / O3 |
| Thm Ω3 | certified two-sided numbers for every class-O type, e.g. split5_1: dim Ω in [0.936275, 0.936852] | PROVED | O3 |
| Thm Ω4 | #{n <= X never below n} = O(X^{dim Ω}); split5_3 O(X^0.58069), split5_1 O(X^0.93686) | PROVED | O4 (sanity) |
| Thm Ω5 | positive-drift members ((3,7), (7,3) rows): Ω has positive Haar measure | PROVED | O5 |
| Z3 | on 3Z split5_3 is conjugate to SPLIT(1,5,1); GLOBAL(split5_3) => GLOBAL(SPLIT(1,5,1)) | PROVED | Z3 |
| (c) | least split5_3 counterexample is not 2 mod 5; bounded-depth ancestor search cannot exclude more than 1/4 of the candidates in n = -3 mod 4^D (from round 2's two-sided theorem) | PROVED | C |

## Systems settled or sharply classified (new to the catalog unless marked)

| id | rule | question | answer | status | tier |
|---|---|---|---|---|---|
| split_a3_b5_d3 (and the 15 other class-D members) | n=1 mod 4 -> 3n+3; n=3 mod 4 -> 5n+3 | GLOBAL | no: every orbit diverges, no cycles | PROVED | 1 (easy) |
| split_a1_b3_d1 | n=1 -> n+1; n=3 -> 3n+1 | GLOBAL | equivalent to Collatz no-divergence (P1); cycles <-> Collatz cycles | PROVED equivalence (GLOBAL OPEN) | 5 |
| split_a3_b1_d3 ("split_3") | n=1 -> 3n+3; n=3 -> n+3 | GLOBAL | equivalent to P1 (via 3x+3, CLS-014) | PROVED equivalence | 5 |
| split_a1_b7_d1, split_a7_b1_d3 (and other class-K members) | | GLOBAL | conjugate to accelerated 7x+3, 7x+9 (expected divergent) | PROVED equivalence | 5 |
| X_d = split_a1_b1_d{d}, all odd d | n odd -> n+d | BASIN, cycles | cosets of <2> mod d, explicit | PROVED | 1 |
| split_5, split_73, split_97, splitB_7, splitB_71 (catalog) | | BASIN | union of <2,3>-classes mod d (5 \| n; 7 \| n; ...); split_5 was already settled in results/split_5_s27.md (not new) | PROVED | 1 |
| split_13 (catalog) | n=1 -> 3n+13; n=3 -> n+13 | BASIN | 13Z -> cycle 13; basins of cycles 1 and 5 split the non-multiples of 13, nonautomatic in every base | PROVED | 3 |
| split_7081 (catalog) | | BASIN | cycles 569 and 713 share a class (nonautomatic basins); the other 8 cycles have congruence basins | PROVED | 3 |
| Sigma_d, gcd(d,6)=1, d < 200 | split_d / splitB_d | BASIN | 44 values congruence-only, 23 with shared classes (list in basins.md) | PROVED | 1-3 |
| split_a1_b5_d1 | n=1 -> n+1; n=3 -> 5n+1 | GLOBAL | open; it is the 3Z part of split5_3; dim Ω = 0.5807 | OPEN (EVIDENCE: only cycle {1,2} for starts <= 3000) | 5 |
| split5_3 (catalog) | | GLOBAL | open; dim Ω = 0.58068 exactly; non-descending starts O(X^0.58069) | OPEN | 5 |
| split5_1 (catalog) | | GLOBAL | open; dim Ω in [0.93627, 0.93686]; non-descending starts O(X^0.93686) | OPEN | 5 |
| 48 class-O members | see family.md | GLOBAL | open; drift sign and dim Ω tabulated | OPEN | 5 |

## Open frontier (precise)

1. GLOBAL for split5_3 is equivalent to "no positive integer y = n+3 >= 4 lies in Ω with a
   never-crossing digit walk" (round 2's prefix criterion). Ω has dimension 0.5807 and measure 0.
   No argument here excludes integers from it.
2. Rising family: does 5^K - 3 fall below 4^K - 3 for all K >= 4? This is equivalent to a
   statement about the 2-adic digits of 5^K. Bounded-depth class certificates provably cannot
   settle all K (round 2). OPEN.
3. (Closed by the referee.) Ω2' for type T2: the referee re-derived the Stirling/duality step,
   and it is now written out in split5_3_deep.md. The certified numbers do not depend on it.
4. BASIN for Sigma_d with 3 | d (for example SPLIT(3,1,9), where 3Z \ 9Z drains into 9Z) is not
   covered by B2. The invariant there is directed, and the basins look density-zero and tree-like
   (EVIDENCE only).
5. The 48 class-O members, including SPLIT(1,5,1), which is new and is the simplest open piece of
   split5_3.

Literature: novelty not checked (no web search was used). Theorems D, R, S and B1 are elementary
and probably folklore. B2-B4 adapt the method of round2/rewriting/split5_3_components.md (itself
after Monks et al.) to settled maps. The Ω dimension computations are standard large-deviation
arguments applied to these maps. Overlap: the split_5 basin rule is already in
results/split_5_s27.md (commit 304d67b), and the concurrent round-3 lenses `progressions`
(applications_basins.md) and `domains` (split_family.md, Theorem P) derive the same
congruence/non-congruence dichotomy for the split catalog members; results agree and credit is
shared.

## Refereeing

Fixes applied from REFEREE.md:
* basins.md, Theorem B4 (k not a power of 2): D = k^a > 2^e·d instead of > 2^e, so that r in [0, D) exists.
* split5_3_deep.md Ω3 table: SPLIT(3,5,1) upper value 0.663347 -> 0.663348 (prover's certificate); referee's sharper 0.663345 cited.
* check_omega.py: table endpoints now compared exactly (rational lower bound; mu^Q <= 2^P for the upper bound), 1e-6 tolerance removed.
* split5_3_deep.md Ω2': T2 Stirling/entropy identity written out in the proof; T2 equality upgraded to PROVED (README row and open-frontier item 3 updated).
* split5_3_deep.md / README Ω2': scope restricted to negative-drift class-O members plus the (3,7)/(7,3) rows via Ω5.
* basins.md / README: split_5 basin noted as already settled (results/split_5_s27.md); overlap with round3/progressions and round3/domains noted.
* family.md: classification wording notes that classes R and O also depend on gcd(d,a), gcd(d,b), and that the classes are applied in order.
