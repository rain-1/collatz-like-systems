# Wholesale application: the profinite invariant of every census p-shift system, and the basin
# questions it settles

Source data: `certificates.json` (produced by `certify.py`, checked by `check_applications.py`
and `check_theorem_A.py`). Theorems used: A (`theorem_A_sufficiency.md`) and B
(`theorem_B_automatic_labels.md`). For every row, the hypotheses (A0), (A1), (IA), the
translation certificate for δ, the class table, state-independence and the existence of an
expanding cycle are verified by the check scripts.

The *basin question* is: is there a finite-state rule (an automaton in some integer base) telling
the basins of the cycles apart? It is a well-posed, settled question even when GLOBAL is open,
because "reaches the cycle C" is a label in the sense of Theorem B.

## 1. Table of invariants

g = the exact profinite invariant (finest T-invariant function of n mod M over all M).
"cycles per class": the known cycles (complete when GLOBAL is settled) grouped by class.

| system (census) | GLOBAL | d* | invariant g(n) | cycles per class | Thm B |
|---|---|---|---|---|---|
| m3_a = shortcut of m3_c (round 1) | settled | 1 | trivial | {1, 2} | yes |
| desc_s32_d65 (round 2) | settled | 65 | gcd(n, 65) | 65: {65}; 1: {1, 7}; 5: {5, 1135}; 13: {13, 39, 299} | yes |
| qrB7_c53 (round 2) | settled | 7 | 0 / square / non-square mod 7 | 0: {7}; sq: {1}; non-sq: {3, 5} | no (no expanding cycle) |
| par_1_5 | settled | 5 | 5 ∣ n | {5}; {1} | no |
| split_5 | settled | 5 | 5 ∣ n | {5}; {1} | yes |
| split_13 | settled | 13 | 13 ∣ n | {13}; {1, 5} | yes |
| split_73 | settled | 73 | 3 classes mod 73 | one each | yes |
| split_97 | settled | 97 | 3 classes mod 97 | one each | yes |
| split_7081 | settled | 7081 | 9 classes | 569 and 713 share; others alone | yes |
| splitB_7 | settled | 7 | 7 ∣ n | one each | yes |
| splitB_71 | settled | 71 | 3 classes | one each | yes |
| 3x+1 (CLS-013) | open | 1 | trivial | {1} | yes |
| 3x−1 (CLS-018) | open | 1 | trivial | {1, 5, 17} | yes |
| 3x+5 (CLS-015) | open | 5 | 5 ∣ n | 5Z: {5}; units: {1, 19, 23, 187, 347} | yes |
| 3x+7 (CLS-016) | open | 7 | 7 ∣ n | {7}; {5} | yes |
| 3x+13 (CLS-011) | open | 13 | 13 ∣ n | {13}; {1,131,211,227,251,259,283,287,319} | yes |
| 3x+17 (CLS-012) | open | 17 | 17 ∣ n | {17}; {1, 23} | yes |
| 5x+1 (CLS-022/024) | open | 1 | trivial | {1, 13, 17} | yes |
| 5x+3 (CLS-027) | open | 3 | 3 ∣ n | 3Z: {3, 39, 51}; units: {1, 43, 53, 61} | yes |
| 5x+7 (CLS-030) | open | 7 | 7 ∣ n | 7Z: {7, 91, 119}; units: {1, 9, 57} | yes |
| 5x+11 (CLS-020) | open | 11 | 11 ∣ n | 11Z: {11, 143, 187}; units: {1, 141} | yes |
| 7x+1 (CLS-032/034) | open | 1 | trivial | {1} | yes |
| 9x+1 (CLS-037) | open | 1 | trivial | none known | (no known cycle) |
| split5_1 (CLS-048/064) | open | 1 | trivial | {1, 13} | yes |
| split5_3 (CLS-049/065) | open | 3 | 3 ∣ n | 3Z: {3}; units: {1, 5, 61, 125} | yes |
| desc_split7_1 (CLS-053) | open | 1 | trivial | {1} | yes |
| desc_s32_plus9 (CLS-052) | open | 1 | trivial | {1} | yes |
| m3_b (CLS-004/061) | open | 1 | trivial | {1} | yes |
| m3_d (CLS-005/062) | open | 1 | trivial | {1, 7} | yes |
| m3_e (CLS-007) | open | 1 | trivial | {1, 4} | yes |
| m3_g (CLS-008/063) | open | 1 | trivial | {4, 8} | yes |
| desc_m3_4n5 (CLS-051) | open | 1 | trivial | {1, 2, 16} | yes |
| 5x+5, 7x+7, 3x+3, 3x+9 | open | – | (IA fails) | – | – |
| perm_1932 | open | – | (A1 fails: permutation) | – | – |

Known cycles of open systems were found by searching starts ≤ 3000 (all listed values are
verified cycle points; completeness is open and irrelevant for the theorems below). For the split
family the classes agree with `../deep/basins.md` (independent computation, same answers).

## 2. Basin questions settled

For every row with "Thm B = yes":

* **(a) Complete list of automatic labels.** A label is k-automatic for some k iff it is a
  function of g iff it is periodic mod d*. (Theorem B.)
* **(b) Cycles alone in their class** have basin ⊆ {g = their class}; if GLOBAL is settled,
  basin = that class exactly (a congruence rule). (Theorem A + GLOBAL.)
* **(c) Cycles sharing a class** have basins that are dense in every progression meeting the
  class, not ultimately periodic on any such progression, and not k-automatic for any k ≥ 2; no
  automatic orbit-invariant label and no ultimately periodic set separates them. When the two
  basins exhaust the class (settled systems with exactly two cycles in it: m3_a, and
  desc_s32_d65 for the classes gcd = 1 {1, 7} and gcd = 5 {5, 1135}), no automatic set in any
  base separates them at all (Theorem B, (S2)). For open systems the literal set-separation
  statement is not claimed (corrected after REFEREE1). (Theorems A, B.)

### Newly answered basin questions (not previously analysed in the census or by other lenses)

1. **m3_a / m3_c (settled).** Cycles (1) and (2) (raw m3_c: (1 3), (2 6)). The invariant is
   trivial, so both basins meet every arithmetic progression in arbitrarily large members, and
   neither basin is automatic in any base; since the two basins exhaust ℕ, no automatic set in
   any base separates them (Theorem B (S2)). Moreover each basin has ≫ X^{1−ε} members in every
   progression for every ε > 0 (Theorem C §3, case (b) via Lemma R: this count had a GAP in the
   first version, now repaired). **PROVED.**
2. **desc_s32_d65 (settled, 8 cycles).** Exact rule: the basin of (65 …) is exactly 65ℤ. The
   other seven basins are not automatic in any base; the class gcd(n, 65) = 1 is split between the
   cycles through 1 and 7, gcd = 5 between 5 and 1135, gcd = 13 between 13, 39, 299. **PROVED.**
3. **5x+1 (open).** The basins of the three known cycles (through 1, 13, 17) are each dense in
   every progression and not automatic in any base; the only automatic labels are constants.
   GLOBAL(5x+1) holds iff the set of eventually periodic starts is k-automatic for some k
   (it contains 1, so it is automatic iff it is everything). **PROVED.**
4. **3x−1 (open).** Same with the cycles through 1, 5, 17. **PROVED.**
5. **3x+5 (open).** Labels: automatic iff periodic mod 5. The five known unit cycles (1, 19, 23,
   187, 347) have non-automatic basins; the basin of (5 20 10) is automatic iff it equals 5ℤ,
   which (as 3x+5 on 5ℤ is 5·(3x+1)) is equivalent to the Collatz conjecture. **PROVED.**
6. **3x+13 (open).** The nine known unit cycles have non-automatic basins. **PROVED.**
7. **3x+17 (open).** The unit cycles through 1 and 23 have non-automatic basins. **PROVED.**
8. **5x+3 (open).** Invariant 3 ∣ n; within each class at least three known cycles, all basins
   non-automatic. **PROVED.**
9. **5x+7 (open).** Invariant 7 ∣ n; both classes hold three known cycles; all six basins
   non-automatic. **PROVED.**
10. **5x+11 (open).** Invariant 11 ∣ n; all five known basins non-automatic. **PROVED.**
11. **split5_1 (open).** Trivial invariant; basins of (1 6 3 4 2) and of the cycle through 13 are
    not automatic in any base, though each has ≫ X^{0.692} members in every progression (Theorem C,
    case (b) via Lemma R; GAP in the first version, now repaired) (observed densities ≈0.70 and
    ≈0.30 below 10^5). **PROVED** (densities: EVIDENCE).
12. **m3_d (open).** Cycles through 1 and 7: non-automatic basins. **PROVED.**
13. **m3_e (open; CLS-006/007).** Cycles {1,9,3} and the 14-cycle through 4: non-automatic
    basins, dense in every progression. For the open start 7 (on no known cycle): the indicator of
    the merging class of 7 and the basin of {1,9,3} are not automatic in any base, and no periodic
    or automatic orbit-invariant label separates them; if the orbit of 7 is not in the basin of
    {1,9,3}, its merging class is dense in every progression, so no congruence condition on
    the class separates it from that basin. This is the label-level sharpening of the census
    remark "no congruence argument at any modulus separates the orbit from {1,9,3}". (Corrected
    after REFEREE1: the first version said no automaton can separate "the orbit of 7" from
    {1,9,3}; literally separating the orbit of 7 from the finite set {1,9,3} is trivial, e.g. by
    ℕ ∖ {1,3,9}, if the orbit avoids the cycle.) **PROVED.**
14. **m3_g (open).** Cycles through 4 and 8: non-automatic basins. **PROVED.**
15. **desc_m3_4n5 (open).** Cycles (1 9 3), (2 6), (16 69 23 48): non-automatic basins. **PROVED.**
16. **Single-cycle open systems** (3x+1, 7x+1, split7_1, desc_s32_plus9, m3_b): the invariant is
    trivial, so GLOBAL ∧ "no other cycle" ⟺ the basin of the known cycle is automatic in some
    base. (Reformulation, PROVED; for 3x+1 the input "every class meets every progression" is
    K. M. Monks, Proc. AMS 134 (2006) 2861–2872.)

### Reproduced (not counted as new)

split_5 (census), split5_3 (round 2), qrB7_c53 (round 2: invariant only; its automaton result
shows Theorem B's expanding-cycle hypothesis is necessary), split_13 / 73 / 97 / 7081, splitB_7 /
71, par_1_5 (concurrent lens `../deep/basins.md`, Theorems B1–B4).

## 3. Caveats

* "Non-automatic" is proved for the basin of a *known* cycle, whatever happens to other orbits.
* "Separates" is proved only for orbit-invariant labels and ultimately periodic sets in open
  systems; for arbitrary automatic sets only when the two basins exhaust their class (Theorem B,
  (S1), (S2)).
* For open systems the class of a hypothetical divergent orbit is a merging class too: Theorem A
  applies to it, so any divergent merging class would be dense in its class as well.
