# Referee report 2: round6/decide_wide (second pass, after the REFEREE1 repair)

Referee 2. I read `README.md`, `theory.md` and `REFEREE1.md`, and for context round 3
`accel/trichotomy.md` (Theorem H, Theorem N, Lemma L and the standing hypothesis). I re-derived
every PROVED statement by hand. I wrote my own check, `referee2_check.py`, from scratch. It has
its own residue graph, Tarjan SCC, exact SCC typing, Theorem H' and brute-force orbit tester. It
does not import `twlib.py`, `famscan`, `check_*.py` or `referee1_check.py`. It imports
`families.py` only to decode option menus (data), and it reads the `out/` files only as the
claims under test. I did not edit any of the prover's files and did not commit.

## Checks run

| check | result |
|---|---|
| `check_theory.py` (round-4 venv, on a mirror copy of the tree) | exit 0, 77 s: Lemma S 2808 pairs, 10,644,590 patterns, Theorem B 312 tables, 75 mixed tables |
| `check_harness.py` | exit 0, 103 s: 265 re-settled catalog tables, 10,734 type-(b) members, falsification, part D (227 open records, each with a (c) SCC) |
| `check_famscan.py` | exit 0: 5400 members, 0 mismatches |
| `classify6.py check` | exit 0: 26,887 tables, 0 mismatches |
| `referee2_check.py` (own, `python3 -I`) | exit 0 (sections A-K below); `quick` argument also exits 0 |

The measured run times match the revised README (about 2 min and 2.5 min).

**The check can fail.** Three mutations each produced a FAIL: asserting the old Proposition 4
(no hypothesis) on the counterexample, claiming B2(3) has only the cycles (1 2) and (5 10), and
claiming that 3x+1 is settled by Theorem H' at level 64. Section B also counts the tables where
the *old* Proposition 4 fails: 1120 (b)-next-to-(z) (table, level) pairs.

How the check works. An SCC is typed (a) only after an exact rational potential has been
verified: c(s) u <= θ c(r) w on every internal edge, with θ < 1 rational. It is typed (b) or
(c) only from an exactly computed cycle product U >= W. It is typed (z) from an actual cycle of
w = 1 nodes. Theorem H' uses the exact lap fixed point and the exact enumeration bound
β/(1-θ).

## Status of the REFEREE1 items

| REFEREE1 item | resolved? |
|---|---|
| 1. Proposition 4 WRONG as stated | **Yes.** It now has the hypothesis "G_4 has no division-free cycle". The proof uses the hypothesis exactly where the old proof failed: an odd path cannot repeat, so it reaches an even node and then 2. Without the hypothesis the statement only says "(b) next to (z), Theorem H' fails". The withdrawn statement is recorded honestly. My section B: 7654 tables, 4000 satisfying the hypothesis, no (b) at levels 4-32 among them, and no division-free cycle at any level. 1120 (b)-next-to-(z) cases without the hypothesis, all unsettled by my Theorem H'. |
| 2. "squarefree" overclaim | Yes. README line 20 now says "at level Q". |
| 3. Q = 15 claim with no example | Yes. E15 is explicit and has a proof, which I re-derived (below). It is in `check_theory.py` part 4 and in my section A. |
| 4. zcore_3_7, zcore_3_17 read on N | Yes. There are now 540 tables and 189 open round-folder tables. My code finds a (c) SCC at the base level for all 227 open records, including the zcore maps read on N0, and my Theorem H' (lo = 0) settles none of them. |
| 5. Nits (U = W, Theorem S wording, B(ii) predecessor sets and m-range, prior art) | Yes, all made. The new §0 text on U = W is correct: under (H1)/(H2) U is prime to Q and W > 1 is a product of divisors of Q. |
| 6. Runtimes | Yes. |

All the repairs are honest. None of them changes a census conclusion, and the revision section
says so.

## Verdicts

| # | claim | verdict |
|---|---|---|
| 1 | Lemma 0 | CONFIRMED |
| 2 | Theorem H' (any modulus, any multipliers, (D)) | CONFIRMED |
| 3 | Proposition Z | CONFIRMED |
| 4 | Proposition P | CONFIRMED |
| 5 | Corollary P' and the "no type (b) at any level" wording (README row 36, Prop 4 "every level") | CONFIRMED_WITH_FIX |
| 6 | Lemma S, Theorem S (level Q) | CONFIRMED |
| 7 | Example E15 | CONFIRMED |
| 8 | Proposition 4 (corrected) | CONFIRMED |
| 9 | Theorem B(i), B2(u) | CONFIRMED |
| 10 | Theorem B(ii), Bp(u) | CONFIRMED |
| 11 | §4 classification table | CONFIRMED_WITH_FIX (nit) |
| 12 | Theorem C6 | CONFIRMED |
| 13 | div23 with 5n ± 1 (and 5n + 5) | CONFIRMED |
| 14 | Q = 12 mixed (b) system; 74 mixed examples; novelty remark | CONFIRMED |
| 15 | catalog sweep: 244/256, 15/42, 0/227 | CONFIRMED |
| 16 | 38 open census table maps all type (c); coverage 29 + 3 | CONFIRMED |
| 17 | family scans | CONFIRMED |
| 18 | `typeb_list.jsonl` | CONFIRMED |
| 19 | 14 non-Markov mixedbase systems re-settled | CONFIRMED |
| 20 | exponents EVIDENCE; honest limits; no open question settled | CONFIRMED |

needs_repair = false. One proof-text fix is recommended (item 5). The conclusion it concerns
is true: I reconstruct the missing argument below and check it numerically. The
census-relevant consequence, that Theorem H' fails at every level, already follows from the
text as written.

## Details

### 1-3. Lemma 0, Theorem H', Proposition Z. CONFIRMED
I re-derived each one line by line. Points I checked specifically:

- **Hypotheses that might not carry over to the new maps.** The type-(b) part of Theorem H'
  uses only that the residue mod K fixes the branch (Q | K), that every f^j(m) is an integer,
  and (D). It does not use unit multipliers, the Markov property, or the subgroup the
  multipliers generate. So it carries over to non-Markov maps and to non-unit multipliers.
- **The integrality bound.** v_p(a - x*) >= min(v_p(a), v_p(x*)) >= min(0, v_p(x*)) for an
  integer a. This is correct.
- **The type-(a) part.** It uses x >= 0 only, so it also works on N0. Negative additive
  constants are handled by max(v, 0).
- **What the over-approximating graph gives.** For a non-Markov map the graph has spurious
  edges. That can only make the hypothesis harder to satisfy, never make it false, so every
  conclusion stays valid.
- **No external theorem is quoted.** Everything used is internal to the repository (round 3
  Theorem 1, Lemma L). Nothing is quoted from memory.

### 4. Proposition P. CONFIRMED
A node with w = p has g = gcd(u, p) = 1, so it has all p successors. That forces C = (r).
Every other node must then avoid r, hence has w = 1, hence there is a division-free cycle on
Z/p minus {r}. For p = 2 this is the loop on the other residue. This is correct.

### 5. Corollary P' and "no type (b) at any level". CONFIRMED_WITH_FIX
Round 3's Lemma L, as written in `trichotomy.md` line 111, says only "type (c) at one level
implies type (c) at every level". Corollary P' correctly concludes "a type-(c) SCC at every
level". That is enough for "Theorem H' never applies".

Two places say more:

- README row 36 says "no type (b) at any level unless a division-free cycle exists".
- The "Every level" paragraph of Proposition 4 says "no type (b) at level 2^k", and it cites
  "the going-up argument of Corollary P'".

**theory.md contains no going-up argument.** Corollary P' has only the two-line Lemma L
proof. The argument is in REFEREE1 §5, and it needs one extra point, given here.

Let C' be an expanding cycle at level p^k, and P its projection (a closed walk of G_p, in a
(c) SCC Σ, with at least one division, because there is no division-free cycle). Let R be the
primitive root of P. Because Σ is not a single cycle, some node of Σ has two internal
out-edges. Route through that node and leave by each edge: this gives two closed walks
through the start of P that are not prefix-comparable, so at least one of them, X, is not a
power of R.

REFEREE1's version ("use an edge of Σ outside C'_proj") fails when P covers every edge of Σ,
which is why this step is needed.

By (M), P^d X has a unique periodic point y_d. It is congruent to x*(C') to precision growing
with d. So its level-p^k orbit is a closed walk through a node of C' whose projection is not a
power of R. That orbit is therefore not a power of C', and the SCC of C' is not a single
simple cycle.

My section C checks the claim numerically: random Markov tables with prime modulus and no
division-free cycle, at lifted levels (p = 2 up to 64, 3 up to 81, 5 up to 125, 7 up to 49;
803 (table, level) pairs), plus 3x+1, 3x-1, 5x+1 and desc_m3_4n5 at every level up to 256.
None has type (b), and type (c) is level independent in every case.

**Fix.** Add this argument to Corollary P' (or cite REFEREE1 §5 with the step above), or
weaken README row 36 and the Proposition 4 "every level" sentence to "a type-(c) SCC at every
level".

### 6. Lemma S and Theorem S. CONFIRMED
I re-derived the CRT step, S(s*(r)) = S(r), injectivity, and the fact that Z is a cycle of Σ
distinct from C. The hypothesis "q depends only on S(r)" is necessary for q(s*(r)) = q, and it
holds for the census least-prime rule.

My section D:

- 720 random raw tables at Q ∈ {6, 10, 14, 15, 21, 22, 30, 35, 42, 66, 70, 105}, with random
  prime-support rules;
- s* is a permutation of the q-nodes in every case;
- every type-(b) SCC consists of units only (so it is also (z)).

### 7. Example E15. CONFIRMED
I re-derived it by hand:

- The w = 5 nodes have successors exactly R = {0, 3, 6, 9, 12}.
- Node 1 has k = 35, g = 5, and successors {2, 7, 12}.
- 2 → 1, and every other node goes to 0.
- The lap map is (7x + 41)/3, with x* = -41/4.
- On R, T(n) = (n + 15 - r)/5 < n for n >= 4, and 3 is fixed.

My code: types ab at levels 15, 45, 75 and 135. My Theorem H' gives the cycle list {(3)}, and
brute force over n <= 10^6 finds only (3).

### 8. Proposition 4 (corrected). CONFIRMED
This is the second application of a hypothesis that held on the original maps: the census
tables all have odd v, and the first version silently assumed it. The corrected version states
it. The proof is now valid:

- Odd paths cannot repeat without a division-free cycle.
- Only 2 has odd successors.
- 2 → 1 and 2 → 3 both lie in the SCC of 2.

The level-2^k extension for the division-free case is also right: the deterministic walk of
w = 1 nodes over a w = 1 cycle closes up. See item 5 for the "no (b)" wording at higher levels.

### 9-10. Theorem B. CONFIRMED
**B2(u).** I re-derived G_8 (1, 5, 7 → 2; 3 → 6; 2 → {1, 5}; 6 → {3, 7}), x* = 3, and the
return map G(n) = (n + 1)/2 or (n + 5)/2. My code: types exactly ab at levels 8 to 128, with
the (b) multiplier u/2, for u ∈ {3, 5, 7, 9, 11, 15, 17, 31, 63, 127}. My Theorem H' gives the
cycle list {(1 2), (3 6), (5 10)}. Brute force agrees over n <= 10^6 (u <= 7) or n <= 2·10^5.

**Bp(u).** I re-derived the graph and the predecessor sets (only p leads to 1; only 0 and 1
lead to p), and F(q) by cases on q mod p. My own derivation, with a = q mod p:
n + v_n = p(p⌊q/p⌋ + 2) when a <= 1, and p^2⌊q/p⌋ + p^2 + 2p when a >= 2. This matches
theory.md. F(q) < q for q >= 1, and v_s never needs the value 0 (2p is not a unit).

My code, for p ∈ {3, 5, 7, 11, 13} and six values of u each: types ab at p^2 and p^3 (and p^4
for p <= 5), one (b) SCC with multiplier u/p, Theorem H' list {(1 p), (2 2p)}, and brute force
agrees. The hypotheses p ∤ u (for (H1) and (D)) and u > p are both used and both stated.

### 11. §4 table. CONFIRMED_WITH_FIX (nit)
- Row "p^m, m >= 2, p^m != 4: yes, for every multiplier u > p": add "p ∤ u" (as in Theorem B).
- The prime, squarefree and Q = 4 rows now carry the correct caveats.
- The mixed rows are labelled correctly: examples PROVED, general case OPEN, and the
  "none found" lists are evidence about specific menus.

### 12-13. Theorem C6 and the 5n ± 1 systems. CONFIRMED
`classify6.py check` passes. My section J, on 6474 D6 members (u ∈ {1, 5, 7, 11, 13, 17, 25},
|v| <= 6), confirms both corollaries with my own SCC typing:

- no certificate with a multiplier >= 7;
- (5, 5) is certifiable iff (s1, s5) = (0, 0).

"5n ± 1": type (a), and brute force over n <= 10^6 finds only (1 6 3). The 5n + 5 variant has
exactly (1 6 3) and (5 30 15).

### 14. Mixed type (b). CONFIRMED
**Q = 12 example.** Types ab; the (b) SCC is {1, 2} with multiplier 11/2; x*(2) = -2/3
exactly; Theorem H' and brute force over n <= 10^6 both give {(5 7 10)}.

**The other mixed tables.** All 74 tables (the Q = 6 and Q = 10 tables of `check_theory.py`
and the 72 of `typeb_mixed_examples.txt`, at moduli 6, 10, 12, 20, 24, 28 and 36) are Markov
and of type ab. My Theorem H' list equals brute force (n <= 20,000) for each of them.

**Novelty remark.** It is scoped to "the files of rounds 1-5", and that is consistent with
REFEREE1's search.

### 15-16. Catalog and coverage. CONFIRMED
**Counts.** From `catalog_rows.json` I recount 244 of 256 "yes" and 15 of 42 "no" re-settled,
0 of 227 open, and 540 tables in all.

**Sample of the GLOBAL records.** For 80 of the 250 records settled by Theorem H', my own
Theorem H' at the stated level gives the listed cycle list. Brute force (n <= 20,000 or 4000)
reaches only listed cycles, and every such record is labelled "yes" or "n/a".

**Open records.** Every one of the 227 open records has a (c) SCC at its base level in my code
and is not settled by my Theorem H'.

**Coverage of the 38 OPEN-CLS tables.** My own rule-based recount gives:

- 26 by Proposition P;
- 3 by Proposition 4 (raw tables mod 4, odd v);
- 3 by Theorem S (squarefree, level Q only);
- 6 not covered: desc_s32_plus9, par_6_2, par_10_2, perm_1932inv, perm_c, perm_d.

This is exactly "29 + 3", and the README table names the uncovered six correctly.

**The type-(c) attack.** The task asks for any claimed settled type-(c) system to be attacked,
including checking whether the argument would also settle 3x+1. No type-(c) system is claimed
settled. My section E runs my Theorem H' on 3x+1, 3x-1, 3x+5, 5x+1, split5_1, split5_3,
desc_split7_1, div23_5n1, div23_7n1 and div235_7n1 at several levels each (up to about 300).
It returns NONE with a (c) witness every time.

### 17-18. Family scans and `typeb_list.jsonl`. CONFIRMED
**Exhaustive recount.** I recounted six exhaustive families completely with my own code. Each
row is (members, CERT, B, C, Z):

| family | recount |
|---|---|
| P2_2 | 483, 48, 0, 435, 0 |
| P3_1 | 323, 13, 0, 152, 158 |
| M_6 | 240, 20, 0, 188, 32 |
| P5_1 | 129,200, 2041, 0, 30,887, 96,272 |
| M_10 | 61,440, 3907, 0, 45,757, 11,776 |
| M_12 | 61,440, 2033, 1, 51,470, 7936 |

Every row equals the README table exactly.

**All 18 files.**

- Every SUMMARY line adds up, matches the CERT and B lines in the file, and has FALLBACK = 0.
- 433 sampled CERT lines: all type (a) in my code, and the recorded cycle count equals brute
  force.
- 213 sampled B lines: all of type ab.
- 420 random unlisted members of the exhaustive families: all (c) or (z).

**`typeb_list.jsonl`.** It has 10,734 lines, and the per-family counts match the table. For 200
sampled members, my Theorem H' cycle list equals the listed one and equals brute force, and
every listed x* agrees exactly.

### 19. Non-Markov mixedbase. CONFIRMED
All 14 non-Markov records (mb_s3_3 ... mb_m3b_8, including mb_t729 at K = 1458) are type (a)
at the stated level in my code. My Theorem H' gives the listed cycles, and brute force reaches
no other cycle.

The catalog also re-settles two Markov mixedbase records (mb_d23_4, mb_d23_8), so 16 mb_
records are re-settled in total. The README's "14 non-Markov" is accurate.

### 20. Labels and honesty. CONFIRMED
- The exponents are floats and are labelled EVIDENCE.
- Higher levels for the squarefree maps are labelled EVIDENCE.
- The barrier for mixed and non-Markov maps is stated as OPEN.
- "I did not search the literature for Theorem B or C6" is stated.
- Prior art at 9, 16 and 32 is cited.
- The headline "settles no open census entry" is correct.
- The README answers the question as asked: the decision procedure has now been run on every
  census table map, and it yields new settled systems only where type (b) can occur.

## Summary of recommended changes (none affects a conclusion)

1. Corollary P' and Proposition 4 "every level": either add the going-up argument (item 5,
   including the choice of X when P covers Σ), or weaken README row 36 and the Proposition 4
   sentence to "a type-(c) SCC at every level". The dangling reference to "the going-up
   argument of Corollary P'" must go either way.
2. §4 row p^m: add "p ∤ u".
