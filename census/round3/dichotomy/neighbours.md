# Nearest provable neighbours and distance to provability of the open entries (application 3b)

**Scope.** I took the open GLOBAL entries of census/open_collatz_systems.txt that are table
maps satisfying (H1), (H2) and (P). There are 36 distinct maps, listed in `open_tables.py`.
21 are checked against the census step functions and 3 against round2/descent/systems.py;
the other 12 (parametric par_* entries, which have no census step function) are checked
against the rule text in census/open_collatz_systems.txt. par_10_2 and par_6_2 fail (H1), because u is
even. Their accelerated forms, (10n+2)/2 = 5n+1 and (6n+2)/2 = 3n+1, are par_5_1 and
par_3_1, and their GLOBAL questions are equivalent to those.

**Every open table map is OBST** (PROVED, `check_neighbours.py` part 1). This is the dichotomy
restated: no plain descent certificate exists for any of them, at any modulus. For each map,
decide.py exhibits a verified expanding cycle and, where one exists, a rational periodic
point. Examples: −1 for 3x+1 (multiplier 3/2), −1/3 for 5x+1 (5/2), 1 for perm_1932 (4/3),
−7/13 for div23_5n1 (25/12) and −97/461 for div235_7n1 (2401/96). For the mixed-modulus
entries, Lemma 3 supplies the proof that no certificate exists. All entries are listed in
`neighbours.out`.

## One- and two-class modifications at the next modulus

Lift T to Q' = Qp, where p is the least prime of Q. Then replace the branch on one or two
classes r mod Q' using this menu:

* *damp*: (u', v, w) with u' < u, gcd(u', Q') = 1, exact and positive;
* *reset*: n ↦ ⌊n/Q'⌋ + 1.

Each modified table was decided exactly. Every CERT table is a **settled system** with
GLOBAL = yes and a complete cycle list. The lists are in `scratch/neighbours.json`, and
representatives are in `neighbours.out`.

| open entry | Q' | CERT one-class | CERT two-class | dist_{Q'} at Q'p^0, p^1, p^2, p^3 (exact, or [lower, upper]) |
|---|---|---|---|---|
| m3_b (CLS-004) | 9 | 0/14 | 0/86 | 9:3, 27:6, 81:12, 243:[16,?] |
| m3_d (CLS-005) | 9 | 0/21 | 5/192 | 9:2, 27:3, 81:6, 243:[11,?] |
| m3_e (CLS-007) | 9 | 0/33 | 1/468 | 9:2, 27:4, 81:[8,16], 243:[11,?] |
| m3_g (CLS-008) | 9 | 0/27 | 6/315 | 9:2, 27:3, 81:6, 243:[11,?] |
| par_3_d, d = 1,3,5,7,9,13,17 (CLS-011..017) | 4 | 3/6 | 11/13 | 4:1, 8:1, 16:2, 32:2 |
| par_3_m1 (CLS-018) | 4 | 2/5 | 7/9 | 4:1, 8:1, 16:2, 32:2 |
| par_5_d, d = 1,3,5,7,11,131,353 | 4 | 0/8 | 9/22 | 4:[1,2], 8:2, 16:3, 32:4 |
| par_7_1, par_7_7 | 4 | 0/10 | 10/33 | 4:[1,2], 8:2, 16:3, 32:[4,9] |
| par_9_1 (CLS-037) | 4 | 0/12 | 6/46 | 4:[1,3], 8:[2,4], 16:[3,7], 32:[5,10] |
| perm_1932 (CLS-038/040) | 9 | 0/17 | 0/128 | 9:4, 27:8, 81:[16,?], 243:[32,?] |
| perm_1932inv (CLS-042) | 8 | 0/12 | 0/62 | 8:3, 16:5, 32:7, 64:11 |
| perm_b (CLS-044) | 9 | 0/18 | 0/141 | 9:4, 27:8, 81:[16,?], 243:[32,?] |
| perm_c (CLS-045) | 8 | 0/12 | 0/62 | 8:3, 16:5, 32:7, 64:11 |
| perm_d (CLS-046) | 16 | 0/32 | 0/472 | 16:5, 32:9, 64:13, 128:[19,?] |
| perm_swap (CLS-047) | 9 | 0/16 | 0/113 | 9:4, 27:8, 81:[14,?], 243:[28,?] |
| split5_1 (CLS-048) | 8 | 4/12 | 35/60 | 8:1, 16:1, 32:2, 64:3 |
| split5_3 (CLS-049) | 8 | 4/12 | 34/60 | 8:1, 16:1, 32:1, 64:1 |
| desc_m3_4n5 (CLS-051) | 9 | 3/18 | 39/141 | 9:1, 27:1, 81:2, 243:3 |
| desc_s32_plus9 (CLS-052) | 64 | 11/90 | 923/3979 | 64:1, 128:1, 256:1 |
| desc_split7_1 (CLS-053) | 8 | 5/14 | 48/79 | 8:1, 16:1, 32:1, 64:1 |
| div23_5n1 (CLS-002) | 12 | 0/16 | 16/116 | 12:2, 24:2, 48:4, 96:5 |
| div23_7n1 (CLS-003) | 12 | 0/20 | 0/178 | 12:[2,3], 24:3, 48:5, 96:[7,12] |
| div235_7n1 (CLS-001) | 60 | 0/76 | 0/2834 | 60:5, 120:7, 240:[8,?] |

**Aggregate.** 1330 modified tables are CERT, and 130 of them use damping only. Each is a
settled system with a complete cycle list. Three representatives are written up in full
(dch_split5_1_nb8, dch_div23_5n1_nb12, dch_s32p9_nb64). Most of the others have k\* ≤ 6
and are tier 1. The exceptions are the desc_s32_plus9 neighbours, with k\* = 44–46.

**Status.**

* The "exact" distances are PROVED. The lower bound is the minimum hitting set of verified
  bad cycles, and Proposition 6 shows that this bound holds for *any* replacement
  branches. The upper bound is a verified CERT table.
* A bracket [lo, up] means both bounds are proved but they do not meet, either because the
  reset menu is not optimal or because the search timed out. "?" means no upper bound was
  found within 30 s.
* `check_neighbours.py` re-derives the counts and the exact distances for Q' ≤ 64 (23 s).

## Reading the table

* **Distance is a robust invariant.** It is ≥ 1 for every open entry at every modulus,
  since all entries are OBST. The question is how fast it grows.
* *Bounded distance*: split5_3, desc_split7_1 and desc_s32_plus9 stay at distance 1 through
  Q' = 64 or 256. Fixing a single class, at every resolution tested, removes all
  obstructions. EVIDENCE: these are the open entries closest to provable. Their obstruction
  is a single expanding cycle family living in one class.
* *Slow growth*: 3x+1 and its translates (par_3_d), and 5x+1, grow slowly. For 3x+1 there
  are exact values up to 2^8 in dichotomy.md, Theorem 7, which proves exponential growth in
  the class count. Density appears to go to 0 (EVIDENCE).
* *Fast growth*: the permutations (perm_1932, perm_b, perm_swap, perm_c, perm_1932inv,
  perm_d) need about 4/9, 8/27, … of all classes, i.e. a positive power of the modulus. The
  lower bounds 16 and 32 at 81 and 243 continue the pattern 4·2^{k−2} at 3^k. EVIDENCE
  only. A plausible reason is that a bijection preserves Haar measure, so contraction must
  be paid for everywhere. Proving this is OPEN.
* Mixed-modulus entries (div23_5n1, div23_7n1, div235_7n1) behave like the 5x+1 and 7x+1
  maps.
