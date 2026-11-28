# Referee 1 report: round 6, lens typeb_wide (Theorem H applied widely)

28 November 2026. Independent referee. Context read: this folder's README and every script,
round3/README.md, round3/accel/trichotomy.md, round3/traps/family.md, round3/dichotomy/neighbours.md,
round4/lundberg/README.md, round4/wpotential (README, referee reports), round6/blocked27/README.md.
I did not edit any prover file and did not commit.

## What I ran

* The prover's checks, all exit 0: `check_examples.py` (55 PASS), `shapes.py`, `mixed27.py check`,
  `check_gap.py` (venv python), `check_scans.py` (default mode; 5,291 proof objects re-verified,
  C-scan summaries 4096/4096 slices for a = 3 and a = 5), `verify_H.py data/*_H.json`.
* My own script `referee1_check.py`, written from scratch. It imports nothing from this folder
  and reads the prover's data only to compare. It has its own cylinder graph, Kosaraju SCCs, exact
  simple-cycle multipliers, an exact expanding closed walk for every (c) verdict, exact rational
  contraction weights for every (a) SCC used in a proof, its own Theorem-H cycle enumeration, and
  brute force. Run with `python3 referee1_check.py`: about 1 minute, exit 0, **ALL PASS**. Sections:
  * [NAMED] sh8, sh4, sh16, sh32, the 5x+1 relative, c9a, c9b, the perm_1932inv, perm_c and split5_3
    representatives, and the P8 neighbours of 3x+1 and 3x-1. For each: hypotheses hold (unit u >= 1,
    w = p^e, exact on each class, T(Z>0) in Z>0), the verdict is (b), my Theorem-H cycle list equals
    the README's, and brute force over **all n <= 10^6** (n <= 2*10^5 for sh32) reaches exactly those
    cycles.
  * [P8] 265 pairs (a, d) with a <= 21. Theorem-H cycles = prediction = brute force n <= 20000.
  * [NEG] 3x+1, 3x-1, 5x+1, 7x+1 are type (c) at levels 1..10, with an exact expanding walk.
  * [SCAN] full recounts of S3/S5/S7 for m <= 4, SH3 m = 3, the type-(b) counts of SH3 and SH5 at m = 4
    (358, 458; 25 random members of each settled independently), C9 (all four counts), SPL m = 3, 4
    for d = 1, 3, 5, and B9 for all eight a. All agree with the stored data.
  * [MODS] I rebuilt the menu from the docstring and recomputed one-class counts for par_3_1@8 and @16,
    par_5_1@8, perm_1932inv@8 and @16, split5_3@8 and @16, split5_1@8 and @16, and m3_e@9. All equal
    `out/mods_one.log`. The two-class count for perm_1932inv@8 is b = 68, a = 0. 193 random stored
    type-(b) neighbours (6 per map and mode) were re-settled by my code and by brute force.
  * [G1] the gap example: the SCC structure, plus my own exact Collatz-Wielandt certificate at
    t = 12/7.
  * [Y] Theorem Y for d = 0..120, run with the real map on Z_(6) rationals, plus rising integer
    progressions for d = 9..14.
* Extra z3 runs on scratch copies of the prover's encodings (the venv python has z3). The results are
  under items 4 and 3 below.

## Verdicts

| # | claim | verdict |
|---|---|---|
| 1 | Theorem H as a proof object plus an independent verifier (PROVED method) | CONFIRMED |
| 2 | counter potential phi = l(v_p(n - x_i) + E_i) - i; lexicographic second proof | CONFIRMED |
| 3 | S-family 3n+1 / 5n+1 / 7n+1, exhaustive (m <= 5, C scan m = 6): no type (b) | CONFIRMED (one sub-statement unchecked, see 3) |
| 4 | z3 rows (S3 m = 7, 8; S5 m = 7; S7 m = 6; SPL m = 5; D27) "PROVED modulo z3", encoding "sound and complete" | CONFIRMED_WITH_FIX |
| 5 | SPL m <= 4 exhaustive; Proposition CS (scaling conjugacy) | CONFIRMED |
| 6 | B9, B27, D9 tables; CERT counts equal round 3 | CONFIRMED |
| 7 | SH3, SH5, C9 type-(b) counts (2, 358; 3, 458; 53), all settled; C27 and SH3 m = 5 existence | CONFIRMED |
| 8 | named systems sh8, sh4, sh16, sh32, 5x+1 relative, c9a, c9b | CONFIRMED |
| 9 | Proposition M (minimal modulus) | CONFIRMED |
| 10 | Theorem P8 | CONFIRMED_WITH_FIX (attribution) |
| 11 | open-map one- and two-class neighbours (counts, representatives) | CONFIRMED_WITH_FIX (one coverage sentence) |
| 12 | perm_1932inv, perm_c: Theorem-H neighbours at distance 2 at level 8, none CERT | CONFIRMED |
| 13 | par_5_d, par_7_d, par_9_1: distance 1 via P8 | CONFIRMED |
| 14 | gap zero does not imply type (b) (G1) | CONFIRMED |
| 15 | boundary example G2, and the sentence "'gap zero and theta_1 > 0 implies GLOBAL' holds exactly under the standing hypothesis" | example CONFIRMED; **sentence WRONG** |
| 16 | Theorem Y (homoclinic periodic points y_d of mb_s3_27) | CONFIRMED |
| 17 | Corollary: mb_s3_27 has no generalized certificate; system stays OPEN | CONFIRMED (wording nit) |
| 18 | no open census entry settled; all open table maps type (c); nothing here touches 3x+1 | CONFIRMED |
| 19 | honesty / coverage / novelty statements | CONFIRMED_WITH_FIX (see the list at the end) |
| 20 | headline numbers (3.4 M, 835,000 = 304,296 + 530,668, 874, 2,030, 1,974, 5,291) | CONFIRMED |

## Details

**1. Theorem H, mechanised.** I re-derived the proof. The hypotheses actually used are these. Every
u is a p-unit and u >= 1, so branches increase and checking positivity at the least member of each
class suffices. Each w is a power of p dividing u n + v on the whole class (including u Q = 0 mod w).
There is no division-free cycle. Every SCC is trivial, a simple cycle, or contracting with exact
weights. The verifier's H1 (each part strongly connected, and the level drops strictly on every edge
between parts) does force the parts to be exactly the SCCs. The simple-cycle case is correct for
contracting and expanding cycles alike. The periodic point B/(1 - A) has denominator p^D - U, which
is prime to p, so it is a p-adic integer. The counter drops by exactly 1 inside a lap. At the wrap
it drops by l D - l + 1 >= 1, and it is >= lK - l + 1 > -l. The weighted case is round 3's argument,
and beta is computed over internal edges only, which is correct. An integer periodic point that is
<= 0 cannot lie on a cycle of a map preserving Z>0, so restricting to x* > 0 is right. A remark,
not a defect: round 3's `accel_lib.theorem_H` already implemented the proof. What is new here is the
serialised proof object and the verifier that does not import the generator, and both are sound.

**2. Counter potential.** It is a formal identity and correct. On contracting SCCs the
"descent off a finite set" means phi(Tn) - Vmax <= theta(phi(n) - Vmax), so the orbit enters the
finite set {c(r) n <= Vmax + 1}. The descent is well founded because phi = c(r) n with n an integer.
The README's wording is acceptable.

**3. S-family.** The m <= 4 counts were recomputed (item list above). The prover's check
reproduces m = 5 and the round-3 OBST counts. In the C scan, a simple cycle of G_6 has A <= 32 odd
steps and B <= 32 halvings, so every cycle mean is at least 0.0136/64 > 2e-4 away from 0, far above
float error. The 1e-9 threshold is therefore exact here. One correction to the README: the bound
"B <= 64" is loose but harmless. The scan only examines members that have an expanding simple-cycle
SCC, which is the right filter for "no type (b)". *Unchecked sub-statements:*
(i) "34,560 members have an isolated expanding SCC ({63, 62}, x* = -1)". The C scan does not record
which SCC is isolated. I checked the identification with two z3 queries on a copy of `sat_sfamily.py`
at a = 3, m = 6. "Isolated expanding simple cycle avoiding node 63" is UNSAT, and "rooted at 63 but
not the 2-cycle 63 -> 62 -> 63" is UNSAT. So the identification holds, modulo z3. Please add such a
check or say how it was established. (ii) "The companion (c) SCC always contains the residue cycle
of -5, -7, -10" is not checked by any script. It sits in an EVIDENCE paragraph, so either label it
as unverified or check it.

**4. z3 rows.** The `sat_typeH.py` encoding is sound for SAT answers, because every hit is
re-verified by `prove_H` and by `verify_H`. UNSAT answers need *completeness*, and the docstring only
says "once SC is large enough", with SC fixed at 4096. I checked when SC = 4096 suffices. A
contracting cycle forces the psi constraints to be infeasible when sum(ceil(SC log2 q) + 1) > 0, and
an expanding designated cycle is missed when sum floor(SC log2 q) <= 0. I took the maximum over all
edge-count vectors that fit in Q nodes. For the S-family I added the constraint #odd <= #halvings.
* S3 m = 7, S5 m = 7, S7 m = 6, SPL m = 5: both slacks have the right sign, so SC = 4096 is complete.
  CONFIRMED modulo z3.
* **S3 m = 8**: a contracting cycle with 41 steps 3n+1, 24 steps n+1 and 65 halvings (130 nodes,
  multiplier 3^41/2^65 = 0.9886) has slack +103, so it would be wrongly excluded.
* **D27**: a contracting count vector 1/3 x3, 2/3 x7, 5/3 x12 (22 nodes) has slack +2. Expanding
  vectors such as 2/3 x10, 4/3 x7, 5/3 x4 (21 nodes) fail the floor test, so they would be missed as
  the designated cycle.
So for these two rows the UNSAT did not cover every case. I re-ran both on a scratch copy with
SC = 2^22, where both slacks have the right sign (for D27: contracting max -25294, expanding min
+2995). Both are still **UNSAT** (S3 m = 8 in 2.9 s, D27 in 0.25 s). The conclusions stand modulo z3.
*Fix*: raise SC in `sat_typeH.py` (2^22 works for every row) or add this precision bound. Replace
"the encoding is sound and complete" by "complete for the stated moduli at the chosen SC, by the
explicit bound".

**5. SPL and Proposition CS.** The rows for d = 1, 3, 5 are identical at m = 3 and 4, and I
recomputed them. The conjugacy x -> d x maps even classes to even classes (d odd), u n + d to u n + 1,
and n/2 to n/2, and it permutes the family members. It is correct, including the remark that cycle
lists are not transferred. Nit: "Proposition CS" and "Conjecture CS" share a name.

**6, 7. Base-3 and shift families.** I recomputed B9 (all a), C9 (11,956 / 53 / 117,111 / 133,024),
SH3 m = 3 (480 / 2 / 143), and the type-(b) counts 358 and 458 of SH3 and SH5 at m = 4. B27 agrees
with round 3 through the prover's check. All 53 + 30 + 2000 + 358 + 458 + 2 + 3 proof objects pass
`verify_H`, and my independent sample settlement agrees.

**8. Named systems.** All confirmed: verdict (b), the isolated periodic orbits (sh8: -1; 5x+1
relative: -1/3; c9a: -1/2, multiplier 5/3; c9b: the positive cycle (1 3) with multiplier 4/3), the
cycle lists, and brute force to 10^6.

**9. Proposition M.** I re-derived (i): at modulus p every dividing class has all p nodes as
successors. So a simple-cycle SCC containing a division is a self-loop {r} that no other node
reaches. Every other node is then division-free, and they form a functional graph on p - 1 nodes,
which contains a division-free cycle. This is level independent, because (a) and division-free
cycles lift and (c) is Lemma L. The shape reduction in (ii) and (iii) is right: the realisation
v = w t - u r + w p^m k works. The counts 128/2401 and 0/49 are reproduced by `shapes.py`.

**10. Theorem P8.** The proof is correct (I re-derived it line by line). The trap M4 is invariant
with k -> k/2 or k + 1. Off M4 the odd iterates satisfy n_{j+1} = (a n_j + d)/2, and
n_j - x* = (a/2)^j (n_0 - x*) forces n_0 = x*. The condition a + d >= 1 is exactly positivity. It
is checked on 630 pairs by the prover and on 265 pairs by me, with brute force. **Fix (attribution):**
the core of the proof, that every orbit of n/2 | an+b meets 4 mod 8 via x* = -b/(a-2) and the
valuation drop, is **round3/traps/family.md Corollary F1** (FAM_4mod8 in round3/traps/README.md),
stated there for odd b >= 1. P8 is F1 extended to d >= 1 - a, which adds 3x-1, plus the trivial
dynamics on M4. The README must cite F1 and present P8 as "F1 turned into a Theorem-H-provable
neighbour". It currently reads as if new.

**11. Open-map neighbours.** The counts I recomputed all agree. **Fix:** results-table row 45 says
"type-(b) neighbours exist for every par_* map (mod 8, 16)". At modulus 16, one-class neighbours of
type (b) exist only for the par_3_* maps (11 each). par_5_*, par_7_* and par_9_1 have none at 16
(log: par_5_1@16 {'divfree': 40, 'c': 840}). The section-3 table is correct ("8: 2/0"). Reword the
row as "every par_* map at modulus 8; par_3_* also at 16".

**12, 13. Distances.** perm_1932inv@8 two-class gives 68 (b) and 0 (a), and I recomputed this. The
round-3 distances (8:3 for the permutations, 8:2 and 8:[2,4] for par_5/7/9) match
`round3/dichotomy/neighbours.md`. The README correctly says that the new neighbours are Theorem-H
neighbours and not descent neighbours.

**14. G1.** Confirmed. The S-family member at m = 6 has SCCs (a,1), (a,2), (b,{62,63}), (c,34). I
certified rho_S(12/7) <= 1 exactly on both non-simple SCCs, with 12/7 > theta_C = 1.70951. With
Kingman log-convexity and rho_S(0) <= 1 this gives theta_1 = theta_C. Every expanding cycle of the
(c) SCC has run exponent > 12/7, so theta_run = theta_C and the gap is zero. This is a correct
observation that lundberg Theorem 1 is not an equivalence.

**15. G2 and the concluding sentence.** The example is correct: the class 9 mod 16 is a
division-free self-loop n -> n + 16, so rho = 1 for every theta there. The remark about
theta_1 = 0 for an expanding division-free loop is also right. **WRONG:** the sentence "So 'gap zero
and theta_1 > 0 implies GLOBAL' holds exactly under the standing hypothesis" is not proved and is not
supported by anything in the folder. G1 itself satisfies the standing hypothesis, has gap zero and
theta_1 > 0, and is of type (c). Its GLOBAL status is unknown, and Theorem H and Theorem N say it
has no generalized certificate. If the sentence were true it would settle G1, and every type-(c)
system whose minimising cycle is isolated. *Fix*: replace it by the proved statements. Under the
standing hypothesis, type (b) implies gap zero and GLOBAL. Gap zero does not imply type (b) (G1), and
whether it implies GLOBAL is open. Without the standing hypothesis, gap zero and theta_1 > 0 can
coexist with divergent orbits (G2).

**16. Theorem Y.** I re-derived every line. On branch words: W = HEH is x -> (3x + 2)/8,
c = W(-5) + 5 = 27/8, and C = EEH gives z + 5 -> (9/8)(z + 5). On valuations: v_2(s_d) = 0, since
8^{d+1} - 3·9^d is odd and the numerator is odd, and v_3(s_d) = 2d + 3. On the lap points:
v_2(z_j + 5) = 3(d - j) and v_3(z_j + 5) = 2j + 3. The residues -5, -7, -10 mod 27 are 22, 20, 17,
never 26. At y_d: y_d = -14 mod 2^{3d+3}, and y_d, y_d/2, (3y_d + 2)/4 are 22, 11, 17 mod 27. The
multiplier exceeds 1 iff d >= 9, because (9/8)^d > 8/3 iff d > 8.33. I checked periodicity with the
real map (branch D takes priority), the exact word, the multiplier, and pairwise disjointness of the
orbits for d <= 120. The distinctness argument through v_3(z_{d-1} + 5) = 2d + 1 is correct.
Novelty within the project: this resolves round4/wpotential's OPEN item "infinitely many" (only
d = 10, 20, 40 were known), and the sibling folder round6/blocked27 does not contain it.

**17. Corollary.** The transfer of Theorem N is valid. T extends continuously to Z_2 x Z_3 (27 and
2 are units in the other factor), branches are decided by (x mod 2, x mod 27), following a word is a
clopen condition, the integers are dense, and the cycle-lemma point exists because the orbit is
expanding. My check exhibits integers that stay above n for a full period for d = 9..14. *Nit*:
"which proves that it is the mixed-base analogue of type (c)" (Outcome) describes a definition, not a
theorem. Say "it behaves like type (c) in the sense of Theorem N".

**18. 3x+1 and open entries.** Nothing in this folder settles an open map. Every argument used
requires the absence of (c) SCCs, and I confirmed that 3x+1, 3x-1, 5x+1 and 7x+1 are type (c) at
levels 1..10. The "3x+1 + P8" system is a different map, with cycle (4 8) only. The labels are
honest.

**19. Honesty, coverage, novelty: required edits.**
1. §4: delete or replace the "gap zero and theta_1 > 0 implies GLOBAL" sentence (item 15).
2. Theorem P8: cite round3/traps Corollary F1 and reduce the novelty claim (item 10).
3. Results row 45: "every par_* map (mod 8, 16)" becomes "every par_* map at 8; par_3_* also at 16"
   (item 11).
4. Honest limits / `sat_typeH.py`: qualify "sound and complete". At SC = 4096 completeness fails
   for S3 m = 8 and D27. Raise SC (re-run UNSAT at SC = 2^22 confirmed) and state the precision
   bound (item 4).
5. "No external theorem is used" is inaccurate. §4 uses Kingman's log-convexity theorem and the
   Collatz-Wielandt bound (through lundberg Theorem 1). Both are classical and correctly applied,
   but they should be named.
6. State how "{63, 62}" was established for all 34,560 members, and label the "-5, -7, -10 always in
   the companion SCC" sentence as unchecked (item 3).
7. Nits: the name clash between Proposition CS and Conjecture CS; "B <= 64" in check_scans
   (32 suffices); the Outcome wording in item 17.

## Overall

The mathematics is sound and the computations reproduce. Every PROVED theorem checked out:
Theorem H as a proof object, the counter lemma, Proposition M, Proposition CS, Theorem P8,
Theorem Y and its corollary, and G1. So did every exhaustive count I recomputed, every named
system, and a sample of 193 stored neighbours. No open census entry is claimed settled, and none
is. One sentence in §4 asserts an unproved implication (WRONG). Theorem P8 needs attribution to
round 3's Corollary F1. One coverage row overstates. The completeness claim for the z3 encoding is
false at the shipped scale for two rows, although the UNSAT answers survive a re-run at a scale that
is provably complete. After these edits the folder is acceptable.
