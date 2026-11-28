# Round 6, lens "decision procedure and trichotomy, applied to everything"

One harness (`twlib.py`) takes any table map T(n) = (u n + v)/w on classes mod Q and returns:
the decide.py verdict (CERT with k* and the complete cycle list, or OBST with an exact
expanding cycle); the exact SCC types (a)/(b)/(c)/(z) of the residue graph at the base level
and, for mixed or non-Markov moduli, at lifted levels; the verdict of Theorem H' (below); and
the Lundberg exponents theta_1, theta_run, their gap, and the drift (floating point). I ran it on
every table map in every census catalog (540 distinct tables from 633 entries; 539 in the first
version, see the revision section) and on 18 new
families (about 54 million members). The data suggested four general statements, which are
proved in `theory.md`.

**Short answer to "has the decision procedure been applied widely".** It has now been run on
every census table map. It settles no open census entry, and no system that was open in a round
folder. All 38 open census table maps (and all 189 open round-folder maps) have a type-(c)
SCC. The isolated-cycle method (Theorem H) is now proved to give nothing beyond descent
certificates for whole classes: every Markov map with prime modulus and no division-free
cycle, every raw table mod 4 (with no division-free cycle, Theorem H' fails for another reason
when there is one), and every raw full-division table with squarefree modulus, at level Q
(Propositions P, 4, Theorem S). The class
theorems cover 29 of the 38 open census table maps, and div23_5n1, div23_7n1 and div235_7n1 at
their base level. For each single prime-power entry the conclusion was already available from
its computed type (c) and round 3's Lemma L. What is new is that the statement holds for the
whole class, including all its unscanned members. It does give something where type (b) can occur: an explicit infinite family
with an expanding positive cycle and complete cycle lists (Theorem B), 10,734 type-(b) members
of the scanned families, and the first mixed-modulus systems settled by an isolated expanding
cycle.

## Results

| system / class | technique | result | status |
|---|---|---|---|
| every census table map (540 tables) | harness | table `out/catalog_table.md`; 244 of 256 GLOBAL-yes tables and 15 of 42 GLOBAL-no tables re-settled automatically; 0 of the 227 open ones (226 in the first version, see the revision section) | PROVED (each verdict exact; `check_harness.py`) |
| 38 open census table maps | decide + SCC types + exponents | all OBST, all type (c) (mixed ones at every level tried, up to 576-600); exponents in the table below | PROVED (types), EVIDENCE (exponents: floats) |
| any table map, any modulus, any multipliers | **Theorem H'** (port of round 3's Theorem H) | if every SCC at some level is (a) or (b), and each (b) cycle has a prime with v_p(W) > v_p(U), then GLOBAL holds with a computable cycle list | PROVED (theory.md §1) |
| Markov tables with prime modulus (par_a_d with a odd, m3_*, perm_1932, perm_b, perm_swap, desc_m3_4n5, 3x+d, 5x+d, ...) | **Proposition P + Corollary P'** | no type (b) at any level unless a division-free cycle exists (going-up argument written out in theory.md after REFEREE2), so Theorem H settles exactly the CERT ones; by Theorem N there is no generalized certificate either | PROVED (§2) |
| raw tables mod 4 (split family, split5_1, split5_3, desc_split7_1) | **Proposition 4** (corrected after REFEREE1) | if G_4 has no division-free cycle (true for every census member: odd v): no type (b) at any level. Otherwise (b) can occur, but only next to a (z) SCC, and Theorem H' fails anyway. The first version, without the hypothesis, was WRONG | PROVED (§2) |
| raw full-division tables, Q squarefree (div23_*, div235_* type) | **Theorem S** | at level Q: no type-(b) SCC containing a division node; every expanding cycle lies in a (c) SCC or next to a division-free cycle | PROVED (§2); other levels EVIDENCE |
| E15 (Q = 15, general branches: 3 \| r -> (n + (15-r) mod 15)/5; 1 -> (7n-1)/3; 2 -> n+14; else n + 15 - r) | Theorem H' | type (b) {1, 2} (multiplier 7/3) next to (a) only; every orbit reaches the fixed point 3 | PROVED (§2, added after REFEREE1) |
| B2(u): even -> n/2; n = 1,3,5,7 (mod 8) -> n+1, u(n-3)+6, n+5, n+3 (odd u >= 3) | **Theorem B(i)** | no descent certificate (expanding positive cycle (3 6), multiplier u/2); GLOBAL yes with cycles exactly (1 2), (3 6), (5 10) | PROVED (§3) |
| Bp(u): p \| n -> n/p; n = 1 (mod p^2) -> u(n-1)+p; other units -> n + ((2p - n) mod p^2) (p odd, u > p, p ∤ u) | **Theorem B(ii)** | no descent certificate (expanding positive cycle (1 p)); GLOBAL yes with cycles exactly (1 p), (2 2p) | PROVED (§3) |
| type (b) by modulus, raw full-division tables | §4 | never with a division node at prime Q or squarefree Q (level Q); never at Q = 4 without a division-free cycle; always possible at p^m != 2, 4, p; found at mixed Q = 12, 20, 24, 28, 36 | PROVED (examples, impossibility); general mixed case OPEN |
| div23 family mod 6, all multipliers prime to 6 | **Theorem C6** | complete certificate classification (36 successor patterns); a certificate needs u1, u5 ∈ {1, 5}; (5, 5) iff v1 = 1, v5 = 5 mod 6 | PROVED (§6; grid check 26,887 tables) |
| "div23 with 5n ± 1" (5n+1 on 1 mod 6, 5n-1 on 5 mod 6) | decide.py | GLOBAL yes, only cycle (1 6 3), k* = 4 | PROVED (new, easy) |
| 18 families, ~54 million members (counts below) | famscan.c (exact) | about 1.19 million CERT members (random samples can repeat a member) (each a settled system with cycle count), 10,734 type-(b) members (settled by Theorem H/H'), all listed with witnesses | PROVED per member; random-sample frequencies are EVIDENCE |
| 14 non-Markov mixedbase systems (mb_s3_3 ... mb_t729, mb_f25, mb_f125, mb_s49, mb_s343, mb_d23_30, mb_m3b_8) | Theorem H' on the over-approximating graph | re-settled automatically (all SCCs type (a)) | PROVED |
| open mixedbase systems (mb_s3_27, mb_pair_3_27m, mb_pair_5_25p) | lifted levels | type (c) at every level up to ~500; nothing gained | EVIDENCE (no barrier is proved for non-Markov maps) |

## The open census entries

All OBST and type (c). theta_1 is the Lundberg tail exponent and theta_run the run exponent
(round4/lundberg), both floating point. A small gap means the danger is almost all in single
runs. "covered" says which theorem proves that Theorem H can never apply.

| entries | CLS | Q | types | theta_1 | theta_run | gap | drift | covered by |
|---|---|---|---|---|---|---|---|---|
| split5_3 | 049, 065 | 4 | c | 6.1492 | 6.2126 | 0.0634 | -0.194 | Prop 4 |
| desc_s32_plus9 | 052 | 32 | c | 7.3488 | 7.5691 | 0.2203 | -0.238 | type (c) + Lemma L (this entry only) |
| desc_split7_1 | 053 | 4 | c | 2.2580 | 2.4772 | 0.2192 | -0.277 | Prop 4 |
| split5_1 | 048, 064 | 4 | c | 0.5393 | 0.7565 | 0.2172 | -0.194 | Prop 4 |
| desc_m3_4n5 | 051 | 3 | c | 3.4994 | 3.8188 | 0.3194 | -0.243 | Prop P |
| div235_7n1 | 001, 058 | 30 | c (14 levels to 600) | 0.8227 | 1.4178 | 0.5951 | -0.190 | Thm S (level 30) |
| div23_7n1 | 003, 060 | 6 | c (20 levels to 576) | 0.0801 | 0.5533 | 0.4732 | -0.028 | Thm S (level 6) |
| div23_5n1 | 002, 059 | 6 | c (20 levels to 576) | 2.2586 | 3.3856 | 1.1270 | -0.186 | Thm S (level 6) |
| par_3_d (d = -1, 1, 3, 5, 7, 9, 13, 17) | 011-018 | 2 | c | 1.0000 | 1.7095 | 0.7095 | -0.096 | Prop P |
| m3_b, m3_d | 004, 005, 061, 062 | 3 | c | 1.0000 | 3.8188 | 2.8188 | -0.174, -0.105 | Prop P |
| m3_g | 008, 063 | 3 | c | 0.0906 | 2.1507 | 2.0600 | -0.015 | Prop P |
| m3_e | 007 | 3 | c | 0 (drift > 0) | 1.2966 | - | +0.119 | Prop P |
| par_5_d (d = 1, 3, 5, 7, 11, 131, 353) | 020-030 | 2 | c | 0 (drift > 0) | 0.7565 | - | +0.074 | Prop P |
| par_7_1, par_7_7, par_9_1 | 032-037 | 2 | c | 0 (drift > 0) | 0.553, 0.553, 0.461 | - | +0.19, +0.19, +0.27 | Prop P |
| perm_1932 (and auto_1932), perm_b, perm_swap | 038-047 | 3 | c | 0 (drift > 0) | 3.8188 | - | +0.057 | Prop P |
| perm_1932inv, perm_c | 042, 045 | 4 | c | 0 (drift > 0) | 1.7095 | - | +0.059 | (Q = 4, not raw: not covered) |
| perm_d | 046 | 8 | c | 0 (drift > 0) | 0.7565 | - | +0.223 | not covered |
| par_10_2, par_6_2 | 010, 031 | 2 | c (non-Markov, 9 levels) | - | - | - | - | (H1 fails) |

Other open entries are not table maps (qrA3_q17 basin question, up_ct3, yah_avoid57, flipT,
swT9: FATE questions) and are listed in `out/catalog_table.md` under "GLOBAL not the
recorded question".

## Settled systems the harness does not re-settle (and how they were settled)

27 GLOBAL-no tables: 16 split class D members (round3/deep Theorem D, elementary growth), 11
maps with proved divergent orbits (mahler, par_4_2, perm_ceil2, perm_ceil3, perm_suffix_b,
round 3 divergence systems race, c62_64, fx10_64, fx26_32, perm12, swT2_8). The harness only
proves divergence from a division-free residue cycle (Proposition Z), which these do not have.
12 GLOBAL-yes tables: dress_* (4; dressing.md: a second prime consumes runs, non-Markov),
farkas_s27, farkas2005, farkas5m_s27, mb_pair_3_9p/3_9m/5_5m/7_7m (Farkas pairing closed
form), and perm_flip (all orbits are 2-cycles: a neutral division-free cycle, which Theorem H'
excludes by hypothesis). These are type (c) on the over-approximating graph at every level
tried, so the run-accelerated arguments of round 3 are genuinely needed there.

## The family scans (new; not scanned in rounds 2-3)

Raw tables: non-units -> n/p (least prime of Q dividing n), units -> u n + v from the menu in
`families.py`. G3_2 also allows (u n + v)/3 on units. Exhaustive families give exact counts;
random families give sample frequencies (with replacement).

| family | Q | mode | members | CERT | type (b) only | type (c) | division-free | max cycles | max k* (among the 400 nearest-critical CERT) |
|---|---|---|---|---|---|---|---|---|---|
| P2_2 (u ∈ 1,3,5,7; v ∈ ±1,±3,5,7) | 4 | exh. | 483 | 48 | 0 | 435 | 0 | 3 | 3 |
| P2_3 same menu | 8 | exh. | 278,208 | 21,038 | 348 | 256,822 | 0 | 6 | 7 |
| P2_4 (u ∈ 1,3,5; v ∈ 1,3) | 16 | exh. | 1,679,616 | 143,159 | 256 | 1,536,201 | 0 | 5 | 32 |
| P2_4 big menu | 16 | sample | 3,000,000 | 73,853 | 1,296 | 2,924,851 | 0 | 7 | 111 |
| P2_5 (u ∈ 1,3,5; v ∈ 1,3) | 32 | sample | 3,000,000 | 97,603 | 96 | 2,902,301 | 0 | 7 | 616 |
| P3_1 (u ∈ 1,2,4,5,7; v ∈ ±1,±2) | 3 | exh. | 323 | 13 | 0 | 152 | 158 | 2 | 3 |
| P3_2 (u ∈ 1,2,4,5) | 9 | exh. | 12,779,520 | 369,208 | 6,272 | 5,673,865 | 6,730,175 | 5 | 23 |
| P3_3 | 27 | sample | 2,000,000 | 3,630 | 44 | 938,326 | 1,058,000 | 5 | 2120 |
| G3_2 (also (un+v)/3 on units) | 9 | sample | 3,000,000 | 191,613 | 2,349 | 1,874,387 | 931,651 | 6 | 21 |
| P5_1 (u ∈ 1,2,3,4,6) | 5 | exh. | 129,200 | 2,041 | 0 | 30,887 | 96,272 | 4 | 5 |
| P5_2 (u ∈ 1..4) | 25 | sample | 2,000,000 | 2,810 | 4 | 430,652 | 1,566,534 | 6 | 500 |
| M_6 (u ∈ 1,5,7,11; v ∈ 1,2,3,-1) | 6 | exh. | 240 | 20 | 0 | 188 | 32 | 2 | 5 |
| M_10 (u ∈ 1,3,7,9) | 10 | exh. | 61,440 | 3,907 | 0 | 45,757 | 11,776 | 4 | 36 |
| M_12 | 12 | exh. | 61,440 | 2,033 | 1 | 51,470 | 7,936 | 4 | 21 |
| M_18 | 18 | exh. | 15,728,640 | 183,350 | 0 | 13,517,770 | 2,027,520 | 7 | 62 |
| M_24 (u ∈ 1,5,7; v ∈ 1,2) | 24 | exh. | 1,679,616 | 39,161 | 60 | 1,639,099 | 1,296 | 4 | 195 |
| M_24 big menu | 24 | sample | 3,000,000 | 19,275 | 7 | 2,605,923 | 374,795 | 4 | 248 |
| M_36 (u ∈ 1,5,7; v ∈ 1,2) | 36 | sample | 3,000,000 | 32,311 | 1 | 2,725,157 | 242,531 | 4 | 587 |

What the counts say. Type (b) is absent in every family with prime or squarefree modulus and at
Q = 4, as the theorems require (members with a division-free cycle are counted in their own
column; all Q = 4 families here have odd v). It is rare elsewhere: at most about 0.13% of members (P2_3), and it is absent
from all 15.7 million members of M_18. The deepest certificates found here (2120 at Q = 27,
616 at Q = 32, 587 at Q = 36) do not beat round 3's record 2466. A single residue mod 27/32/36
can hold a non-descending run of that length with small multipliers. Division-free cycles
dominate the base-3 and base-5 families because unit -> unit steps are common there.

Type-(b) members: `out/typeb_list.jsonl`, one JSON line each (10,734 lines) with the table,
each (b) cycle (residues, exact U/W, periodic point x*, the prime p of condition (D)), and the
complete cycle list. Examples:

* Q = 8: even -> n/2; 1 -> n+1, 3 -> 3n-3, 5 -> n+5, 7 -> n+3 (mod 8): this is B2(3), with
  cycles (1 2), (3 6), (5 10).
* Q = 25, all multipliers < 5: a (b) cycle of residues (2 5 1) with multiplier 6/5 and
  x* = 2 (cycle (1 2 5)). The full table is the first P5_2 line of the file.
* Q = 12, mixed Markov: 2|n -> n/2; else 3|n -> n/3; n = 1, 5, 7, 11 (mod 12) -> 11n+3, n+2,
  n+3, n-1. The isolated cycle is the residue pair (2 1) with multiplier 11/2 and x* = -2/3.
  Theorem H' gives the single cycle (5 7 10). As far as the files of rounds 1-5 show, this is
  the first census system settled by an isolated expanding cycle at a mixed modulus.

Deepest and most-cycle CERT members per family: `out/cert_top.json`.

## Files

| file | what |
|---|---|
| `twlib.py` | the harness: graph at any level, exact SCC typing, Theorem H', exponents, decide.py wrapper |
| `extract.py`, `catalog.py` | recover tables from catalog step functions; load every systems.py |
| `sweep_catalog.py`, `make_report.py` | catalog sweep -> `out/catalog_sweep.json`, `out/catalog_table.md` |
| `famscan.c` (`famscan`) | exact C scanner for product families (integer potentials checked in 128-bit, big-integer cycle comparisons) |
| `families.py`, `run_families.sh`, `postprocess.py` | family definitions, the scans, summaries, type-(b) list, deepest CERT |
| `search_b_moduli.py` | type-(b) search over all 2 <= Q <= 64 (`out/b_moduli*.txt`) |
| `classify6.py` | Theorem C6 table (`out/classify6.md`) and its check |
| `theory.md` | Theorems H', S, B, C6; Propositions Z, P, 4; Corollary P'; proofs |
| `check_theory.py` | Lemma S (2808 cases), 10.6 million successor patterns (Props P, 4, Thm S), Theorem B on 312 tables, Theorem H' on 75 mixed-modulus (b) tables (74 + E15), the mod-4 counterexample, the Theorem B(ii) predecessor sets; about 2 min |
| `check_harness.py` | every re-settled catalog verdict and every type-(b) member against iteration; decide.py on a subsample; falsification tests (3x-1, 3x+5, 5x+1, 3x+1 stay unproved; wrong cycle lists rejected); part D: every open record classified with a (c) SCC, zcore maps on N0; about 2.5 min |
| `check_famscan.py` | famscan against decide.py and twlib on 300 random members of each family (0 mismatches) |

All checks exit 0. `python3 classify6.py check` exits 0. The interpreter is the round-4 venv
(`round4/wpotential/.venv/bin/python`; numpy is needed for the exponents only).

## Honest limits

* No open census question is settled. Every open table map is type (c), and for the
  prime-modulus and mod-4 ones Theorem H is now proved useless at every level. For the mixed
  squarefree ones (div23_5n1, div23_7n1, div235_7n1) it is proved useless only at the base
  level. Higher levels showed type (c) up to about 600 residues (EVIDENCE).
* Theorem N (the barrier for every generalized certificate) remains proved only for prime-power
  Markov maps. For mixed or non-Markov maps a type-(c) SCC says only that this proof fails.
* The exponents theta_1, theta_run and the drift are floating-point (bisection on spectral
  radii, Karp in floats). They are EVIDENCE, as in round 4.
* famscan's verdicts are exact (integer potentials, big-integer cycle products). Members where
  float search failed would be reported as FALLBACK; none occurred. It was cross-checked
  against decide.py on 5,400 random members.
* The "new settled systems" from the scans are mostly arbitrary tables. The natural ones are
  the infinite families B2(u), Bp(u) and the D6 classification with "div23 with 5n ± 1". I did
  not search the literature for Theorem B or C6. They are elementary, and similar constructions
  may be folklore.
* The catalog status labels (`make_report.py`) were assigned by rules from the census files and
  the round READMEs. A few FATE-only systems are labelled "n/a".
* The table recognizer (`extract.py`) is heuristic. Every table it returns is re-checked
  against the step function on 1 <= n <= 20000, and the statements are about the returned table
  (farkas_s27 with its 1 -> 1 rule is read on N0).

## What stayed open

* Level independence of type (c) for Markov maps with mixed squarefree modulus, which would
  extend Theorem S to every level and close Theorem H off for div23_5n1 and its relatives.
* The barrier (Theorem N) for mixed and non-Markov maps.
* Type (b) at mixed non-squarefree moduli in general. Why does M_18 have none?
* A complete list of (multiplier set, modulus) pairs admitting type (b) beyond Theorem B and
  the small-multiplier examples at Q = 25.

## Revision after REFEREE1

Referee 1 (`REFEREE1.md`) confirmed most claims, found one false statement, and asked for
several fixes. What changed:

1. **Proposition 4 was WRONG as stated, and is corrected.** The first version said that no
   raw table mod 4 has a type-(b) SCC, with no hypothesis. Counterexample (the referee's):
   even n -> n/2, n = 1 (mod 4) -> 3n + 2, n = 3 (mod 4) -> 3n + 1. The SCC {2, 3} is a
   single cycle with multiplier 3/2 (type (b)), next to the division-free loop 1 -> 1 (type
   (z); the class 1 mod 4 diverges). The corrected statement (theory.md §2) adds the
   hypothesis "G_4 has no division-free cycle" and says that without it a (b) SCC occurs only
   next to a (z) SCC, where Theorem H' fails anyway. The proof is rewritten so that the
   hypothesis is used where the old proof failed ("both 1 and 3 return to 2"), and the
   extension to every level 2^k is spelled out. Every census application has odd v, so no
   census conclusion changes. `check_theory.py` part 2 now asserts that the counterexample is
   (b) next to (z) and that Theorem H' does not return GLOBAL for it.
2. **"Squarefree" overclaim in the headline.** Theorem S is a level-Q statement; the headline
   now says "at level Q", and Theorem S's conclusion reads "no type-(b) SCC containing a
   division node" (a division-free single cycle is (b) and (z) by the §0 words; (z) takes
   precedence).
3. **Q = 15.** The first version claimed type (b) with general branches at Q = 15 with no
   example in the folder. There is now an explicit table, E15 (theory.md §2, with proof):
   type (b) {1, 2} with multiplier 7/3 next to type (a) only, settled by Theorem H' (only cycle:
   the fixed point 3). It is checked in `check_theory.py` part 4. The Q = 4 claim for general
   branches is now attributed to the counterexample above (a raw table, (b) next to (z)).
4. **zcore_3_7 and zcore_3_17** (round 3, written in z = (n-1)/2 >= 0) were read on the positive
   integers, failed positivity and were never classified, yet were counted among the "188 open
   round-folder maps of type (c)". `sweep_catalog.py` now reads every zcore_* map on N0. This
   also separates zcore_2_3 / zcore_3_37 (on N0) from steiner_1cycle (on N), so there are now
   540 distinct tables and 189 open round-folder tables. All 189 and all 38 OPEN-CLS tables
   are classified and contain a type-(c) SCC at the base level; `check_harness.py` part D
   asserts this (it fails on the old sweep file, as it should). The four zcore tables are
   read on N0, where decide.py (positive integers only) is not run; their types are (c). The
   settled counts are unchanged: 244 of 256 GLOBAL-yes and 15 of 42 GLOBAL-no tables
   re-settled, none of the open ones.
5. **Nits.** §0 now says what happens to a single-cycle SCC with U = W (no type; impossible
   under (H1)/(H2); off them the harness labels it 'b' but condition (D) fails, so Theorem H'
   returns NONE). Theorem B(ii): "only 0 and p lead to 1" corrected to "only p leads to 1;
   only 0 and 1 lead to p" (now asserted in `check_theory.py` part 3), and the modulus range
   now reads "every p^m with m >= 2 (odd p) or m >= 3 (p = 2)". The §4 rows for prime and
   squarefree moduli now state the division-node and division-free caveats. Theorem B now
   cites the earlier type-(b) examples in this repository (round 3 acc_h9, acc_h16, acc_h32;
   round 4 F3m2, 36 tables): what is new is the explicit infinite family with positive
   expanding cycles and complete cycle lists.
6. The runtimes in the files table were overstated; they are now the measured ones.

All checks were re-run after the revision and exit 0: `check_theory.py`, `check_harness.py`,
`check_famscan.py` (unchanged inputs), `classify6.py check` (unchanged inputs). Nothing in this
revision settles a new open system; the honest limits and open list above stand.


## Revision after REFEREE2

Referee 2 (`REFEREE2.md`, own check `referee2_check.py`) confirmed every claim and every
REFEREE1 repair; needs_repair = false. Two text fixes were recommended and are made:

1. **Going-up argument (Corollary P', Proposition 4 "every level").** theory.md cited "the
   going-up argument of Corollary P'", but Corollary P' contained only the Lemma L step, which
   gives "type (c) at every level", not "no type (b) at any level". The argument is now written
   out in theory.md §2 after Corollary P', following REFEREE2's reconstruction (projection P of a
   lifted expanding cycle, its primitive root R, a closed walk X through a branching node of the
   (c) SCC that is not a power of R, and the periodic point of P^d X, which starts at a node of
   the lifted cycle). It includes REFEREE2's extra step for the case where P covers every edge of
   the SCC. I checked each step by hand. It is stated for a base level p^m, so it serves both
   Corollary P' (m = 1) and Proposition 4 (base level 4). The README row for prime moduli and
   the §4 rows now cite it in place of Lemma L alone. No conclusion changes.
2. **§4 table, row p^m:** "for every multiplier u > p" now reads "u > p with p ∤ u", as in
   Theorem B.
