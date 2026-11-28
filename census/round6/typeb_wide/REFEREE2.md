# Referee 2 report: round 6, lens typeb_wide (Theorem H applied widely), after the repair

28 November 2026. This is the second independent referee pass. I read the revised README, REFEREE1.md
and every prover script I relied on: tblib.py, verify_H.py, sat_typeH.py, sat_family.py,
sat_sfam_H.py, check_sat_precision.py, check_sat_sc22.py, check_iso63.py, sbrute.c, mods.py,
families.py, check_examples.py, check_gap.py and gap.py. For context I read round3/README.md,
round5/README.md, round3/traps/family.md (Corollary F1) and round4/wpotential/README.md. I did not
edit any prover file and did not commit. My only new files are `referee2_check.py` and this report.

## What I ran

**The prover's checks.** All exit 0:
* `check_examples.py` (ALL PASS)
* `shapes.py`
* `mixed27.py check`
* `check_iso63.py` (7,740 configurations, 34,560 members, nb = 34,560)
* `check_gap.py` (venv)
* `check_sat_precision.py` (venv; incomplete at 4096 exactly for {S3_m8, D27} with caps, complete
  at 2^22 for every row)
* `check_sat_sc22.py` (venv; C9 53, SH3_m3 2, SH5_m3 3, D9 0; 8 stored re-runs unsat)
* `verify_H.py data/*_H.json` (3,317 objects)
* `check_scans.py`
* `referee1_check.py` (exit 0)

I also summed the C-scan files myself:
* a = 3: 4096/4096 slices, nb = 34,560, nH = 0, nunc = 0.
* a = 5: 4096/4096 slices, nb = 2,218,464, nH = 0, nunc = 0.

**My own script `referee2_check.py`.** I wrote it from scratch. It imports nothing from this folder.
It uses round3/dichotomy/open_tables.py only for the census definitions of the open maps, and it
reads the prover's data only to compare against. Run it with `python3 referee2_check.py`: about 50 s,
exit 0, ALL PASS.

It has its own components: cylinder graph, Kosaraju SCCs, a Kahn test for division-free cycles,
exact simple-cycle products, and a Karp search that is used only to locate certificates. Every
(c) verdict is backed by an exact expanding closed walk. Every (a) verdict used in a proof is backed
by exact rational weights c(s) u/p^e <= theta c(r). The script also has its own Theorem-H cycle
enumeration and its own brute force.

I checked that it can fail. While I was developing it, it failed on my own transcription errors.
In a mutation test it rejects a cycle list with one cycle dropped, and it classifies sh8 with
5 -> n+1 as (c).

The script's sections:
* **[NAMED]** 12 systems: sh8, sh4, sh16, sh32, the 5x+1 relative, c9a, c9b, the perm_1932inv,
  perm_c and split5_3 representatives, and 3x+1 and 3x-1 with P8. I built each table myself from the
  README's verbal description. For each one:
  * the hypotheses hold (unit u >= 1, w = p^e, exact on each class, T(Z>0) in Z>0);
  * the verdict is (b);
  * my Theorem-H cycle minima equal the README's;
  * the README's isolated expanding point lies on the isolated periodic orbit;
  * brute force over **all n <= 10^6** (sh32: 3·10^5) reaches only those cycles.
* **[P8]** 160 pairs (a, d) with a <= 63 and 1 - a <= d < 120. For each pair:
  * G_3 is exactly the contracting SCC {0, 4}, plus one simple 2-cycle {x*, 2x*} mod 8 with
    multiplier a/2, plus trivial nodes;
  * the cycles are as predicted;
  * brute force over n <= 20000 agrees.

  Separately, every n <= 50000 of 3x+1 with P8 enters M4.
* **[Y]** Theorem Y for d = 0..150, with the real map on Z_(6) rationals (the 26 mod 27 branch takes
  priority). I checked the word HEH(EEH)^d, the exact multiplier, (multiplier > 1) iff d >= 9,
  v_2(s_d) = 0, v_3(s_d) = 2d + 3, that the orbits avoid -5, -7 and -10, and that they are pairwise
  disjoint. For d = 9..13 I took the cycle-lemma point y and an integer n = y mod 6^N, and checked
  that the orbit of n stays above n for a whole period.
* **[ISO63]** My own enumeration, with a different algorithm, of the S with {62, 63} an SCC: 7,740
  configurations and 34,560 distinct members. It agrees with the C-scan nb **slice by slice in all
  4096 slices**, which is stronger than the total (slices 0..2047, where 63 is not in S, all have
  nb = 0). For all 34,560 members I also checked two things: {62, 63} is the only expanding
  simple-cycle SCC, and the residue cycle 59, 50, 57, 44, 54 lies in one non-simple SCC. Since
  59, 57 in S and the cycle has exact multiplier 9/8, and S3 has no division-free cycle, that SCC is
  of type (c). 60 random members went through the full exact classifier.
* **[SCAN]** Random samples of SH3 m = 4, SH5 m = 4 and C9, about 1,550 members each, including the
  stored type-(b) members (60 sampled for SH3/SH5, all 53 for C9). My verdict is (b) exactly when
  the index is in the stored list. About 30% of the sampled (b) members were settled and brute-forced.
  Full recounts of B9 (all eight a), S5 m = 5 (2,155 / 63,381; I use floats, which is exact here
  because I computed the cycle-mean separation bound 1.5e-3), and SPL m = 3 for d = 1, 3, 5. All
  equal the stored counts. I also checked Proposition K directly: x -> d x is a graph isomorphism
  of G_3 for every SPL member.
* **[MODS]** I reimplemented the menu from the docstring. Recounts of one-class par_9_1@8,
  desc_split7_1@8, split5_3@16 and perm_1932inv@32, and two-class perm_c@8 (b = 68), all equal the
  stored counts. I took 60 random stored type-(b) neighbours and checked, for each:
  * the modification is in the menu and the table matches the proof object;
  * the hypotheses hold and my verdict is (b);
  * my Theorem-H cycle list equals the stored one;
  * brute force over n <= 10^5 agrees.

  The totals 304,296, 530,668 and 1,974 are reproduced.
* **[PREC]** My own recomputation of the z3 completeness bound (difference constraints over all
  count vectors of length <= Q, with Hall caps and, for 2-adic rows, #non-dividing <= #halvings).
  Complete at SC = 2^22 for S3 m = 7, 8, S5 m = 7, S7 m = 6, SPL_d1 m = 5 and D27. At SC = 4096 the
  incomplete set is exactly {S3_m8, D27}.
* **[M]** Proposition M (i): every shape at modulus p = 2, 3, 5. Proposition M (iii): the 49
  modulus-4 shapes with n/2 on the even classes.
* **[G1]** The gap example. My own exact Collatz-Wielandt certificate at t = 665/389 on the
  34-node (c) SCC, with rational upper bounds U >= 3^t and U >= 2^-t checked by exact powers. The
  inequality t > theta_C is checked exactly as 2^1054 < 3^665. The SCC structure is (a,1), (a,2),
  (b,{62,63}), (c,34).
* **[NEG]** 3x+1, 3x-1, 5x+1, 7x+1 and 3x+5 are type (c) at levels 1..10, each with an exact
  expanding walk.

## Were the REFEREE1 items resolved honestly?

| REFEREE1 item | resolution in the revised folder | my check | status |
|---|---|---|---|
| 15 (WRONG) "gap zero and theta_1 > 0 implies GLOBAL" | The sentence is withdrawn. §4 now lists what is proved and lists the implication as OPEN. The Withdrawn paragraph states correctly why the claim would have been too strong: it would settle G1. | Text read. G1 reverified independently. | resolved |
| 10 Theorem P8 attribution | P8 now cites round3/traps/family.md Corollary F1 as its core, and calls P8 "F1 turned into a provable neighbour, not a new mechanism". | F1 exists as quoted (odd a >= 3, odd b >= 1). P8's extension to d >= 1 - a is genuine (it adds 3x-1). | resolved |
| 11 "every par_* (mod 8, 16)" | Row 46 now says: every par_* at 8; at 16 only par_3_*. | mods_ONE: par_5_*, par_7_*, par_9_1 @16 have b = 0; par_3_* @16 have b = 11. | resolved |
| 4 z3 completeness | SC raised to 2^22. check_sat_precision.py verifies the bound per row. Every row was re-run at 2^22 and is still unsat. "Sound and complete" is replaced by an accurate statement. | Bound recomputed independently, same result. The out/sc22 files say unsat. | resolved (still "modulo z3", as labelled) |
| 3 (i) {63,62} for all 34,560 | check_iso63.py: exact enumeration, plus equality with the C-scan total. | My own enumeration agrees per slice in all 4096 slices. The C-scan float sign decision is exact by the separation bound (min abs(A log 3 - B log 2) > 0.0135 for A, B <= 32). | resolved |
| 3 (ii) ghost cycle in the companion SCC | Checked for all members in check_iso63.py. | Reproduced for all 34,560. | resolved |
| edit 5 external theorems | Kingman's log-convexity and the Collatz-Wielandt bound are named, as quoted from memory. | Both are stated correctly. Kingman (1961) covers matrices whose entries are log-convex or zero, and sums of exponentials in theta qualify. | resolved |
| nits | Proposition K renamed, B <= 32, Outcome wording. | All present. "Prop. CS" survives only in referee1_check.py, which is not the prover's file. | resolved |

The repair changed no count, cycle list or proof object. I checked this by recomputation, not by
trusting the statement.

## Verdicts

| # | claim | verdict |
|---|---|---|
| 1 | Theorem H as a proof object, with an independent verifier (PROVED, method) | CONFIRMED |
| 2 | Counter potential phi = l(v_p(n - x_i) + E_i) - i, and the lexicographic second proof | CONFIRMED |
| 3 | S3/S5/S7 exhaustive at m <= 5, and the C scan at m = 6: no type (b). Plus the S3 m = 6 identification ({63,62} is the only isolated SCC; the ghost cycle is in a (c) SCC) | CONFIRMED |
| 4 | z3 rows (S3 m = 7, 8; S5 m = 7; S7 m = 6; SPL m = 5; D27), "PROVED modulo z3, completeness bound checked" | CONFIRMED_WITH_FIX (wording: SPL m = 5 was run for d = 1 only; d = 3, 5 follow from Prop. K) |
| 5 | SPL m <= 4; Proposition K | CONFIRMED |
| 6 | B9, B27, D9 tables; CERT counts equal round 3 | CONFIRMED |
| 7 | SH3, SH5, C9 type-(b) counts (2, 358; 3, 458; 53), all settled; C27 and SH3 m = 5 existence | CONFIRMED |
| 8 | Named systems sh8, sh4, sh16, sh32, the 5x+1 relative, c9a, c9b | CONFIRMED_WITH_FIX (attribution: the 5x+1 relative is not in check_examples.py) |
| 9 | Proposition M | CONFIRMED |
| 10 | Theorem P8 (with the F1 attribution) | CONFIRMED_WITH_FIX (two quoted x* values) |
| 11 | Open-map one- and two-class neighbours | CONFIRMED_WITH_FIX (coverage wording in row 47) |
| 12 | perm_1932inv, perm_c: Theorem-H neighbours at two classes, none at one, none CERT | CONFIRMED |
| 13 | par_5_d, par_7_d, par_9_1: distance 1 via P8 | CONFIRMED |
| 14 | G1: gap zero does not imply type (b) | CONFIRMED (nit: t >= theta_C is tested in floats in check_gap.py; it holds exactly) |
| 15 | §4 after the repair: what is proved and what is OPEN; G2 | CONFIRMED |
| 16 | Theorem Y | CONFIRMED |
| 17 | Corollary: no generalized certificate for mb_s3_27; the system stays OPEN | CONFIRMED |
| 18 | No open census entry is settled; every open unit table map is of type (c); nothing touches 3x+1 | CONFIRMED |
| 19 | Headline numbers (3.4 M, 835,000, 874, 2,030, 1,974, 5,291) | CONFIRMED |
| 20 | Honesty, coverage and novelty statements | CONFIRMED_WITH_FIX (minor edits listed below) |

## Details

**1, 2. Theorem H and the counter.** I re-derived both line by line.

Hypotheses used:
* u >= 1 and u a p-unit, so branches increase and checking positivity at the least member of each
  class suffices;
* w = p^e divides u r + v and u Q, so the map is exact on the whole class;
* there is no division-free cycle, so every simple-cycle SCC has D >= 1.

On n ≡ node_i we have T(n) - x_{i+1} = (u/w)(n - x_i). Inside a lap phi drops by exactly 1, and at
the wrap it drops by lD - l + 1 >= 1. Since phi >= -(l - 1), only x_i can stay forever.

In the weighted case, V(Tn) <= theta V(n) + beta uses n > 0 and max(v, 0), which handles the
negative v that appears in the new maps (perm_1932inv rep: n - 4; perm_c rep: n - 2; c9a, c9b:
2n - 1). Every point of a cycle inside Sigma satisfies V <= Vmax: take the maximum of V on the cycle
and look at its predecessor.

An integer periodic point that is not positive cannot be on a cycle. Also, a periodic orbit with
one integer point consists of integers only, because T is exact on the classes. So verify_H's test
on x_0 alone is enough.

Nothing in the proof uses a property of 3x+1 that the new maps lack. There are no ineffective
constants, and only one prime is involved per system.

**3. S-family.** I reverified the C scan's float decisions. Simple cycles of G_6 have
A, B <= 32. min abs(A ln 3 - B ln 2) = 0.01355 (at 12, 19), and min abs(A ln 5 - B ln 2) = 0.0237.
Cycle means are therefore at least 2e-4 away from 0, which is far above both the 1e-9 threshold and
float error. My per-slice ISO63 comparison is the strongest check here. It turns REFEREE1's z3-based
identification into a z3-free, slice-wise equality. I also confirmed "isolated expanding SCCs occur
from m = 6 in S3 and m = 5 in S5": S3 m = 4, 5 have 0 such members, and S5 m = 5 has 128.

**4. z3.** I re-derived the completeness reduction for a genuine type-(b) member:
* take C = the expanding simple-cycle SCCs and D = one of them;
* give levels in topological order, distinct per SCC (at most Q + 1 values are needed);
* take psi from longest-path potentials on the (a) SCCs.

These potentials exist iff no simple contracting cycle has sum(ceil(SC lq) + 1) > 0. The designated
cycle is admitted iff sum floor(SC lq) >= 1. The od/od2/root constraints can always be met. The
caps are valid necessary conditions:
* Hall: a simple cycle visits each class once, with that class's single branch;
* in S and SPL, every non-dividing step lands on an even class, and that class halves.

My recomputation matches the prover's numbers, for example S3 m = 8 at 2^22: -69,215 and +12,606.

*Fix (wording only):* results row 34 says "common d in {1,3,5} ... m = 5 by z3", but only SPL_d1
m = 5 was run (out/sc22/satfam_SPL_d1_m5.txt). For d = 3, 5 the conclusion follows from
Proposition K, which is correct and transfers types. Say so in the row.

**8. Named systems.** All confirmed with my own transcription of the README text, which is a test
of the README as well as of the code:
* cycle minima and isolated orbits: sh8 (-1, -2); 5x+1 relative (-1/3, -2/3); c9a (-1/2, -3/2);
  c9b (1, 3, multiplier 4/3); split5_3 rep (-5/3, -16/3); perm reps (0);
* brute force to 10^6 agrees.

*Fix:* §2 says "Natural examples (all PROVED, check_examples.py)", but the 5x+1 relative is not in
check_examples.py's NAMED list. It is checked in referee1_check.py and in this referee2_check.py.
Either add it to NAMED or cite the referee scripts.

**9. Proposition M.** (i) holds: at modulus p a dividing class has all p nodes as successors, so a
simple SCC containing a division is an unreachable self-loop. The other p - 1 nodes are then
division-free and form a functional graph, which contains a cycle. A division-free cycle at level 1
persists at every level, because the lap map permutes the lifts. My shape check for p = 2, 3, 5
and the 0/49 count agree.

**10. Theorem P8.** I re-derived the proof:
* M4 is invariant, and on M4, n = 4k evolves by k -> k/2 (k even) or k + 1 (k odd), which reaches
  the cycle (4 8);
* off M4, each odd iterate n_j has a n_j + d ≡ 2 (mod 4), so n_{j+1} - x* = (a/2)(n_j - x*), which
  forces n_0 = x*;
* x* = -d/(a-2) is odd whenever it is an integer, so 2x* ≡ 2 (mod 4), which is consistent;
* a + d >= 1 is exactly positivity.

The G_3 structure (contracting {0, 4} plus one isolated 2-cycle) holds for all (a, d). An infinite
path of G_3 avoiding {0, 4} carries 2-adic points, by compactness, and the valuation argument shows
that these are only x*. I confirmed it on 160 random pairs.

*Fix (numbers):* §3 says P8 "keeps each one's expanding fixed point: -1 for 3x+1, -1/3 for 5x+1,
**-2/5 for 7x+1, -2/7 for 9x+1**". The fixed points of the odd branch composed with one halving,
x* = -d/(a - 2), are -1/5 and -1/7. -2/5 and -2/7 are the even points 2x* of the same 2-cycles. The
list mixes the two conventions. Write -1/5 and -1/7 (or "the 2-cycle (-1/5, -2/5)").

**11. Neighbours.** All recounts agree. *Fix (coverage):* results row 47 says "two-class
modifications at moduli 4, 8, 9 ... type-(b) neighbours for par_*". In fact only par_3_1, par_3_m1,
par_5_1, par_7_1 and par_9_1 were run in two-class mode (mods_TWO_9.json has 23 keys). The §3 table
states this correctly, so the row should name the five maps.

**12, 13.** These are confirmed from the stored counts and my recount of perm_c@8 two-class
(68 b, 0 a). "At most 2" for perm_1932inv and perm_c is an upper bound under this folder's menu, and
it is stated that way. The comparison with round 3's descent distance 3 is a comparison across
menus, and it is worded as such ("Theorem-H neighbours, not descent neighbours").

**14, 15. Gap.** G1 is confirmed with my own exact certificate. Nit: check_gap.py chooses
t >= theta_C with a float comparison. The margin is 2.8e-7 and the inequality holds exactly, as my
exact check shows. §4 as revised is accurate. The open question (whether gap zero implies GLOBAL
under the standing hypothesis) is labelled OPEN, and G1 is correctly named as the test case.

**16, 17. Theorem Y and its corollary.** I re-derived every line.
* Letters: H is halving and E is (3x+1)/2. So W = HEH is x -> (3x + 2)/8 and C = EEH is
  z -> (9z + 5)/8.
* Constants: c = 27/8, and s_d = 27·9^d/(8^{d+1} - 3·9^d).
* Lap points: v_2(z_j + 5) = 3(d - j) and v_3(z_j + 5) = 2j + 3. These force E, E, H at residues
  22, 20, 17 mod 27, never 26.
* At y_d: s_d ≡ -9 (mod 2^{3d+3}) because v_2(z_0 + 5) = 3d. The residues of y_d mod 27 along W
  are 22, 11, 17.
* Distinct orbits follow from v_3(z_{d-1} + 5) = 2d + 1.

The corollary's transfer of Theorem N is valid for any cover, finite or countable, and under either
reading of "almost all". The rising progression has positive relative density in the cylinder.
Nit: the cycle lemma (Raney) is used without being named. It is elementary.

The system is correctly left OPEN. Within the project, Theorem Y is new: it settles round4/
wpotential's "infinitely many: OPEN" item. Neither round6/blocked27 nor any other round6 folder
contains it, by grep.

**18. 3x+1 and open entries.** No open entry is claimed settled, and none is. Theorem H needs the
absence of (c) SCCs. 3x+1, 3x-1, 5x+1 and 7x+1 are (c) at every level I tested (1..10). The
"3x+1 + P8" system is a different map, with only the cycle (4 8), and the README says so.

No type-(c) system is claimed settled anywhere in the folder. The only (c) systems discussed (G1
and mb_s3_27, which is (c)-like) are explicitly left OPEN.

## Required edits (all minor; no proof, count or label changes)

1. §3, P8 paragraph: replace "-2/5 for 7x+1, -2/7 for 9x+1" by "-1/5 for 7x+1, -1/7 for 9x+1"
   (or name the 2-cycles).
2. Results row 47: replace "par_*" by "par_3_1, par_3_m1, par_5_1, par_7_1, par_9_1".
3. Results row 34: "m = 5 by z3 for d = 1; d = 3, 5 by Proposition K".
4. §2 "Natural examples (... check_examples.py)": add the 5x+1 relative to check_examples.py, or
   cite referee1_check.py / referee2_check.py for it.
5. Nit: in check_gap.py / gap.py, test t >= theta_C exactly. For lambda = U/p^e and
   t = a/b, the test is p^(e(a + b)) <= U^a, which for G1 is 2^1054 < 3^665. Alternatively, say in
   the docstring that the float margin is 2.8e-7.

## Overall

The repair is honest and complete. REFEREE1's WRONG sentence is withdrawn and replaced by correct
statements, the P8 attribution is in place, and the z3 completeness gap is closed by a bound that I
recomputed independently. The {63, 62} identification is now exact, and I strengthened it to a
slice-by-slice equality with the C scan. Every PROVED theorem re-derives: Theorem H and its
verifier, the counter, Propositions M and K, P8, Theorem Y and its corollary, and G1. Every count I
recomputed matches, and every sampled proof object re-settles with brute force. No open census
entry is settled, and the folder does not claim otherwise. The remaining issues are four wording or
number fixes and one nit, none of which affects a result. **needs_repair: false.**
