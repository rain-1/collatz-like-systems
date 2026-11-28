# Phase diagrams: base-3 and mixed-modulus families (application 3a)

Every verdict below is **exact**. decide.py either verifies an integer potential (CERT), or
verifies a cycle of the residue graph with multiplier > 1 (OBST-expanding) or a translation
cycle (OBST-critical). By Theorem 1 of dichotomy.md, the verdict is CERT exactly when a
descent certificate exists. Every CERT table has GLOBAL = yes, and its complete cycle list
can be computed by Theorem 2. So each count of CERT tables is a count of **settled
systems**. Status: PROVED, as exhaustive enumeration with exact per-table certificates.
Reproduce with `scan_base3.py` (about 10 min) and `scan_mixed.py` (about 3 min).
`check_phase.py` (25 s) re-derives the B9, C9 and D36 numbers, and its `--full` option also
re-derives B27.

## Family B(Q, a, S)

The map is: 3 | n → n/3. For n mod Q in S, n → a n + 1. For every other n not divisible by
3, n → n + 1. Here S ranges over all subsets of the units mod Q.

| a | B(9): # CERT of 64 | max \|S\| of 6 | B(27): # CERT of 262144 | max \|S\| of 18 (# sets) | deepest k\* in B(27) |
|---|---|---|---|---|---|
| 2 | 24 | 4 | 57816 | 14 (8) | 45 |
| 4 | 10 | 3 | 11661 | 13 (1) | 49 |
| 5 | 8 | 3 | 4364 | 10 (7) | **66** |
| 7 | 6 | 2 | 1328 | 8 (5) | 41 |
| 8 | 6 | 2 | 1074 | 8 (6) | 65 |
| 10 | 1 | 0 | 69 | 4 (8) | 12 |
| 11 | 1 | 0 | 76 | 5 (2) | 11 |
| 13 | 1 | 0 | 64 | 5 (3) | 10 |

No OBST in this family is critical. The full distribution of CERT counts by |S| is in
`scan_base3.out`.

Observations:

1. **Doubling the depth of resolution adds a "middle".** At Q = 9, every certifiable
   table has k\* ≤ 6. At Q = 27, depths up to 66 appear. Hill-climbing at Q = 81
   (deep_search.out) reaches k\* = 655 (a = 2), 254 (a = 5), 184 (a = 4) and 126 (a = 8).
2. **There is a sharp drop between a = 8 and a = 10.** For a ≤ 8, a positive fraction of
   the 18 classes can carry a n + 1. For a ≥ 10, at most 5 can at Q = 27, and none at
   Q = 9. This is EVIDENCE only. I have no proof that the drop persists for larger Q.
3. **Maximal density.** In B(27, 2), 2n+1 can be applied on 14 of the 18 unit classes, and
   all eight sets of size 14 give GLOBAL. Example: dch_B27a2_max14, whose only cycle is
   (1 3). In B(27, 4), exactly one 13-set certifies.

## Family C9: eight affine choices per class mod 9

The map is: 3 | n → n/3. For n ≡ r (mod 9) with r ∈ {1, 2, 4, 5, 7, 8}, apply one of
n+1, n+2, 2n+1, 2n−1, 4n+1, 4n−1, 5n+1, 5n−1. This gives 8^6 = 262144 tables.

* 11956 are CERT, so they are settled with GLOBAL = yes and a complete cycle list.
  250187 are OBST-expanding.
* **1 is OBST-critical:** n+1 on 1, 4, 7 and n+2 on 2, 5, 8 mod 9. This is a translation
  cycle 1→2→4→5→7→8→1 (mod 9) with drift 9. Every orbit of n ≡ 1 (mod 9) increases by 9
  every 6 steps, so all such orbits diverge. A multiple of 3 is divided by 3 until it reaches a non-multiple. So **every positive orbit diverges** (GLOBAL = no, PROVED). This is the unique table in the family where
  the critical case of Lemma 2 occurs.
* Distribution of k\* among the CERT tables: 2:64, 3:1316, 4:2982, 5:2947, 6:2259, 7:1084,
  8:526, 9:253, 10:151, 11:47, 12:45, 13:91, 14:22, 15:16, 16:8, 17:43, 18:16, 19:28,
  20:21, 21:21, 23:2, 24:1, 25:8, 26:1, 30:1, 31:1, 32:1, 33:1.
  The deepest is **dch_C9_33**, with k\* = 33 at modulus 9 and only cycle (2 5 6).
* The largest product of multipliers among certifiable tables is 2500, and exactly two
  certifiable tables attain it. One of them, a most expanding certifiable table, is
  5n+1, 5n−1, 4n−1, 5n+1, 5n+1, n+1. It is **dch_C9_prod2500**, with k\* = 6 and only
  cycle (1 6 2 9 3).
* The same family at modulus 27 was explored by hill-climbing only (deep_search.py). It
  found **dch_C27_2466**, whose plain certificates need **2466 steps**. Its residue graph
  has an 11-cycle with multiplier 80/81 = 2^4·5/3^4.

## Mixed modulus: D(36, a, S)

The map is: 2 | n → n/2. Otherwise, 3 | n → n/3. Otherwise, apply a n + 1 if n mod 36 is
in S, and n + 1 if not. With S equal to all units, these are the open census maps
div23_5n1 and div23_7n1 (CLS-002, CLS-003).

| a | # CERT of 4096 | max \|S\| of 12 | deepest k\* |
|---|---|---|---|
| 5 | 756 | 8 (6 sets) | 27 |
| 7 | 336 | 7 (2 sets) | 43 |

At Q = 72, no S with |S| ≥ 20 of the 24 units is certifiable for either a. Examples
settled: dch_D36a5_8, where 5n+1 on 8 of 12 classes gives the single cycle (1 6 3), the
same cycle as the open map; dch_D36a7_7, with single cycle (1 2); and dch_D36a7_43.
These are the first exact phase-diagram results for a modulus mixing 2 and 3 in this
census. They rely on Lemma 3, which needs no periodic point.
