# Round 3, lens "dichotomy": descent certificates as a decision procedure

The descent method from round 2 is turned into a theorem and a tool, and the tool is then
used to settle new systems in bulk. Statuses are labelled honestly throughout. Every claim
marked PROVED has a written proof and an exact check script that exits 0.

## General theorems (dichotomy.md)

| result | statement | status |
|---|---|---|
| Lemma 1 (realisation) | Assume (H1) gcd(u_r, Q) = 1 and (H2) w_r \| Q with exact division. Then every walk of the residue graph G_T is followed by an infinite progression mod Q·∏w, and T^L is affine on it. | PROVED |
| Lemma 2 (critical case) | Assume (H1) and (H2). A cycle with multiplier exactly 1 consists of translation steps n + v_r. Under positivity (P) its drift is ≥ 0. | PROVED |
| Lemma 3 (obstruction) | A cycle with multiplier ≥ 1 rules out every descent certificate. Unlike round-2 Lemma B, the proof needs no periodic point, only compactness of Ẑ_Q. This is what makes mixed moduli work. | PROVED |
| **Theorem 1 (Markov dichotomy)** | Under (H1), (H2) and (P), and for any modulus Q (prime power or mixed), the following are equivalent: a certificate exists; every cycle of G_T contracts; an integer one-step potential exists; a uniform certificate with modulus Q^{k+1} exists. | PROVED |
| Theorem 2 | A potential gives GLOBAL, an explicit finite exceptional set F, and the complete cycle list, which consists of the cycles reached from F. | PROVED |
| Theorem 3 (exact depth) | The least k over all plain certificates is k\* = 1 + (length of the longest non-descending walk). Also k\* ≤ 1 + σ/\|μ\*\|. | PROVED; agrees with the round-2 engine on all tested cases |
| §6 | Without gcd(u_r, Q) = 1 the dichotomy fails. Counterexample: odd n ↦ 4n + 4. | PROVED |
| Prop. 6 / Def. 5 | Distance to provability: the least number of classes mod Q' that must be modified to reach CERT. It is bounded below by hitting sets of expanding cycles, and this holds for any replacement branches. | PROVED |
| Theorem 7 | dist_{2^m}(3x+1) ≥ N(⌊m/2⌋), which grows exponentially in m. Exact values 1, 1, 1, 2, 2, 4, 5, 8 for m = 1..8. | PROVED; the question density → 0 is OPEN (EVIDENCE: yes) |

Relative to round 2: the referee proposition in lemmas.md covered only p = 2, even ↦ n/2 and
a single halving, and gave a proof sketch. New here: arbitrary Q and w_r | Q, an exact
treatment of the critical case, an obstruction that needs no periodic point, an exact depth
formula with bounds, explicit exceptional sets, lifting invariance, the H1 counterexample,
and a decision procedure with no UNKNOWN outcome.

Literature: the Markov chain on residues is due to Matthews and Watts (1984/85). I did not
find the deterministic dichotomy in one search; novelty is otherwise not checked. See
dichotomy.md §8.

## The tool: decide.py

    python3 decide.py Q "[(u,v,w), ...]"      # one triple per residue mod Q
    python3 decide.py --id dch_C27_2466

It outputs one of two answers.

* **CERT**: an integer potential, verified on every edge with integers; the exceptional
  set F; the complete cycle list; k\* and the number of leaves of the minimal certificate;
  and an a-priori depth bound.
* **OBST**: an exactly verified expanding cycle with the progression of integers that
  follows it, plus the rational periodic point when one exists. Alternatively, a critical
  translation cycle.

Floats are used only for the Karp search. Every answer is re-verified exactly, and there
is an exact Bellman–Ford fallback with Fractions.

## Newly settled systems

All of the following are new to the census. Each has GLOBAL = yes with the complete cycle
list, except where stated. Every one is PROVED by `check_systems.py`, and its proof is in
`<id>.md`.

| id | rule (short) | Q | answer: complete cycle list | k\* | tier |
|---|---|---|---|---|---|
| dch_C27_2466 | 3\|n→n/3; 18 unit classes mod 27 → n+1, n+2, 2n±1, 4n±1, 5n±1 | 27 | (1 2 3), (5 11 43 45 15), (125 624 … 375) | **2466** | 2 (Lyapunov) / depth record |
| dch_B81a2_655 | 3\|n→n/3; 2n+1 on 31 classes mod 81, else n+1 | 81 | (2 5 6), (22 23 47 95 191 192 64 65 66) | 655 | 2 |
| dch_S6_332 | n/2; 3n+1 on 14 odd classes mod 64, else n+1 | 64 | (1 2) | 332 | 2 |
| dch_B81a5_254 | 3\|n→n/3; 5n+1 on 20 classes mod 81 | 81 | (2 11 56 … 6) [13], (8 41 42 14 71 72 24) | 254 | 2 |
| dch_B81a4_184 | 3\|n→n/3; 4n+1 on 18 classes mod 81 | 81 | (1 2 3) | 184 | 2 |
| dch_B27a5_66 | 3\|n→n/3; 5n+1 on {2,4,16,17,23} mod 27 | 27 | (1 2 11 12 4 21 7 8 9 3), (28 29 146 147 49 50 251 252 84) | 66 | 2 |
| dch_B27a8_65 | 3\|n→n/3; 8n+1 on {7,8,14,17} mod 27 | 27 | 5 cycles, minima 1, 7, 8, 13, 16 | 65 | 2 |
| dch_B27a4_49 | 3\|n→n/3; 4n+1 on {4,11,14,17,22} mod 27 | 27 | (1 2 3) | 49 | 2 |
| dch_B27a2_max14 | 3\|n→n/3; 2n+1 on 14 of 18 unit classes mod 27 (maximum) | 27 | (1 3) | 39 | 2 |
| dch_C9_33 | 3\|n→n/3; mod 9: 5n−1, 2n+1, 2n−1, n+1, 4n+1, 2n−1 | 9 | (2 5 6) | 33 | 2 |
| dch_C9_prod2500 | 3\|n→n/3; mod 9: 5n+1, 5n−1, 4n−1, 5n+1, 5n+1, n+1 | 9 | (1 6 2 9 3) | 6 | 1–2 |
| dch_D36a5_8 | 2\|n→n/2; 3\|n→n/3; 5n+1 on 8 of 12 unit classes mod 36 | 36 (mixed) | (1 6 3) | 27 | 2 |
| dch_D36a7_7 | same with 7n+1 on 7 of 12 | 36 | (1 2) | 15 | 2 |
| dch_D36a7_43 | same with 7n+1 on {1,31} mod 36 | 36 | (1 8 4 2) | 43 | 2 |
| dch_split5_1_nb8 | neighbour of open split5_1: 5 mod 8 → 3n+1 | 8 | (1 6 3 4 2) | 5 | 1 |
| dch_div23_5n1_nb12 | neighbour of open div23_5n1: n+1 on 5, 11 mod 12 | 12 | (1 6 3) | 4 | 1 |
| dch_s32p9_nb64 | neighbour of open desc_s32_plus9 | 64 | (1 4 2), (7 22 11 34 17 52 26 13 14) | 46 | 2 |
| C9-critical (phase_base3.md) | 3\|n→n/3; n+1 on 1,4,7, n+2 on 2,5,8 mod 9 | 9 | GLOBAL = **no**: every orbit diverges (translation cycle, drift 9) | – | 1 |

## Bulk results (all exact)

* **Phase diagrams** (phase_base3.md):
  * B(9, a) and B(27, a) for 8 values of a. That is 2.1 million tables, 76,452 of them CERT
    at Q = 27.
  * C9: 262,144 tables. 11,956 are CERT, all settled with cycle lists; 250,187 are
    OBST-expanding; 1 is critical.
  * D(36, a): 756 + 336 CERT.
  * Each CERT table is a settled system.
* **Open entries** (neighbours.md): every one of the 36 open GLOBAL table maps is OBST, so
  no plain descent proof exists at any modulus. Over all entries, 1,330 one- and two-class
  modifications at the next modulus are CERT, and these are settled systems. The table there
  gives the distance to provability of each entry. It is exact in most cases up to Q' = 64,
  with bounds beyond that.
* **Depth records** (deep.md): k\* = 2466 at modulus 27, against the round-2 record of 44.
  The record systems also have one-step Lyapunov proofs, so depth is a property of the
  certificate format. Unbounded depth is cheap with translation chains (deep.md).

## What stayed open

* Does dist_{2^m}(3x+1)/2^m tend to 0? (EVIDENCE: it is non-increasing up to m = 8.) For the
  permutation entries, does the distance grow like a positive power of the modulus?
  (EVIDENCE: 4/9, 8/27, ≥16/81, ≥32/243.)
* Is sup k\* unbounded in B(3^k, 2) and C(3^k) without translation chains? (Conjecture.)
* Is there a sharp a-threshold in B(Q, a)? (EVIDENCE: a drop between a = 8 and a = 10.)
* The open census entries themselves. The dichotomy proves only that *descent
  certificates* cannot settle them.

## Files and checks

| check | covers | runtime |
|---|---|---|
| check_dichotomy.py | Lemmas 1–4, Theorems 1–3, §6, Theorem 7, lifting, and the critical C9 system | ~1.5 min |
| check_systems.py | every system in systems.py: certificate, F, cycle list, k\*, depth witness, simulation | ~5 s |
| check_phase.py | the B9, C9 and D36 counts; `--full` adds B27 (+8 min) | 25 s |
| check_neighbours.py | open tables match the census, are OBST, the neighbour counts, and exact distances | ~25 s |

The search and scan scripts are scan_base3.py, scan_mixed.py, neighbours.py, distance.py and
deep_search.py. Their outputs are in *.out. Supporting modules are families.py,
open_tables.py and gen_docs.py; gen_docs.py writes the per-system `<id>.md` files.

## Refereeing

Fixes applied after the referee report (REFEREE.md); none affects any proof.

* README.md, neighbours.md: "34" open GLOBAL table maps corrected to 36 (open_tables.py lists 36; neighbours.out has 36 sections).
* neighbours.md: scope sentence now says 21 maps are checked against census step functions, 3 against round-2 systems, and 12 par_* maps against the catalog rule text.
* check_neighbours.py: added the missing exact comparison of the 12 par_* tables with their catalog rule text on n < 3000 (all 36 maps now compared).
* phase_base3.md, dch_C9_prod2500.md: dch_C9_prod2500 is one of two certifiable C9 tables attaining product 2500 ("a most expanding", not "the most expanding").
* dichotomy.md §7 and README.md open questions: "fell monotonically" / "decreasing" corrected to "non-increasing" up to m = 8.
* dichotomy.md, proof of Theorem 1 (c)⇒(d): the progression modulus is Q·∏_{i<k−1} w_i, which divides Q^k (replacing "divides Q·Q^{k−1}").
