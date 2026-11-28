# Round 3, lens "mixedbase": maps that mix two bases

This round looks at Farkas-type maps, where a division class mod an odd m sits on top of a 2-adic expanding branch, together with their close relatives. These maps are continuous on Z_2 × Z_m and on neither factor alone, so the one-prime engine of round 2 cannot even state them.

## What was built

* **mixedlib.py** — a mixed-radix descent-certificate engine for any residue-class affine map, with any modulus M0. It includes:
  * an independent verifier: full-trie partition check, symbolic re-derivation with uniform-branch assertions, and numeric checks;
  * Lemma A' (the exceptional set and the complete cycle list);
  * exact verification of S-adic periodic points;
  * an exact word search for expanding cycles (Lyndon words);
  * a residue-graph search used only as a heuristic.
* **pairlib.py** — the Farkas pairing family P(a, K, x*), its closed-form block, and a run-accelerated engine. Its "tail leaves" handle the unbounded up-runs that make plain certificates impossible.
* **lemmas.md** — mixed-radix versions of the round-2 lemmas:
  * A' (certificate ⇒ GLOBAL plus cycle list);
  * B' (an expanding S-adic periodic point ⇒ no certificate);
  * C' (engine terminates ⇔ a certificate exists);
  * R (an unbounded uncaught run ⇒ no certificate);
  * D'' (fixed points of words when some primes expand and others contract).

## General theorems

| theorem | statement | status | file |
|---|---|---|---|
| Pairing family P1–P3 | For P(a, K, x*) (m = a^K, r = x*/2, c = (m−1)x*/2, b = (2−a)x*): closed block T^{j+1+q}(n) = (x* + a^ℓ u)/2. For K = 1 (every odd a) and (a, K) = (3, 2), every integer orbit is eventually periodic and every cycle meets \|n\| ≤ 5\|x*\| (≤ \|x*\| for K = 1); cycle lists computed. | PROVED (tier 1) | pairing_family.md |
| Pairing family P4–P5 | No plain certificate exists for any member (x* is an expanding fixed point). No accelerated certificate exists for a ≥ 5, K ≥ 2 (2-cycle y, 2y with y = (2−a)x*/(4−a)) or for a = 3, K ≥ 3 (cycle 5x*, 7x*, 10x*). So the closed form reaches exactly K = 1 and (3, 2). | PROVED | pairing_family.md |
| S3 | 3x+1 with one class r mod m: a certificate exists iff (m, r) ∈ {(3, 2), (9, 8)} (necessity for every c; sufficiency with c = 1). | PROVED | single_class.md |
| S5 | 5x+1 with one class: a certificate exists iff (m, r) = (5, 3). | PROVED | single_class.md |
| S7 | 7x+1 with one class: iff (7, 4). | PROVED for odd m ≤ 199; EVIDENCE beyond | single_class.md |
| Mechanism | A single class needs gcd(a(a−2), m) > 1. "The run visits every residue" (a ≡ 2 mod p) occurs, but for a single class it is proved not to suffice only for a = 5 (all odd m; the run growth becomes a periodic point via Lemma D'') and for a = 7 with m ≤ 199 (enumeration). The general three-condition criterion is a heuristic. | PROVED for a = 5 and for a = 7, m ≤ 199; heuristic otherwise | single_class.md |
| Minimal taming sets | Minimum number of classes for a certificate: 3x+1 mod 27/81/243/729 = 2/3/4/7; 5x+1 mod 25/125 = 2/4; 7x+1 mod 49/343 = 2/5. Lower bounds by exact hitting-set obstructions; upper bounds attained by certified systems. | PROVED | sparse_taming.md |
| Theorem D | div23_5n1 + one class: the complete list of (q, r) that can admit a certificate (q ≤ 83 from two integer expanding cycles, then an exhaustive scan with the refined Lemma B'); every listed pair except the open map itself and "first" (4,2) is certified, with its complete cycle list in relatives.md (not always (1 6 3): e.g. first (3,1) has (1) and (5 26 13)). The sparsest provable one is n ≡ 26 (mod 30) → (n+4)/30 (density 1/30), cycle (1 6 3). | PROVED (repaired after refereeing; (4,2) "first" unresolved) | relatives.md |
| Theorem M | m3_b + at most two classes: they must be the odd class (q = 2) or {1, −1} mod q with q ∈ {3, 4, 6, 8} (bound q ≤ 32 from the cycles (1/7, −1/7) and (7/25, 1/25, −7/25, −1/25) via the refined Lemma B'). All are certified. q = 2 has the two cycles (1) and (2 3); q = 3, 4, 6, 8 have only (1). The sparsest is ±1 mod 8 (density 1/4). | PROVED (repaired after refereeing) | relatives.md |

## Systems

All rules have the form "class rule (checked first); else even → n/2; else odd rule". Domain N+ unless stated. Question: GLOBAL.

| id | rule | answer | status | tier |
|---|---|---|---|---|
| mb_pair_3_9p | n≡5 (9) → (n+4)/9; (3n−1)/2 | all orbits → (1) | PROVED | 1 |
| mb_pair_3_9m | n≡4 (9) → (n−4)/9; (3n+1)/2; on N0 | all orbits → (0) or (1 2); no plain descent certificate exists (the run-accelerated one does) | PROVED | 1 |
| mb_pair_7_7m | n≡3 (7) → (n−3)/7; (7n+5)/2; on N0 | all orbits → (0) | PROVED | 1 |
| mb_pair_5_5m | n≡2 (5) → (n−2)/5; (5n+3)/2; on N0 | all orbits → (0) | PROVED (reflection n ↦ −n of round-2 farkas5m_s27; only nominally new) | 1 |
| mb_s3_3 | n≡2 (3) → (n+1)/3; (3n+1)/2 | → (1 2) | PROVED | 1 |
| mb_s3_9 | n≡8 (9) → (n+1)/9; (3n+1)/2 | → (1 2) | PROVED | 1 |
| mb_s5_5 | n≡3 (5) → (n+2)/5; (5n+1)/2 | → (1 3) | PROVED | 1 |
| mb_s7_7 | n≡4 (7) → (n+3)/7; (7n+1)/2 | → (1 4) | PROVED | 1 |
| mb_t27 | {17, 26} mod 27, (n+c)/27; (3n+1)/2 | → (1 2) | PROVED | 2 |
| mb_t81 | {20, 71, 80} mod 81; (3n+1)/2 | → (1 2) | PROVED | 2 |
| mb_t243 | {137, 152, 233, 242} mod 243; (3n+1)/2 | → (1 2) | PROVED | 2 |
| mb_t729 | {182, 380, 395, 425, 668, 719, 728} mod 729; (3n+1)/2 | → (1 2) | PROVED (5417 leaves, depth 83) | 2 |
| mb_f25 | {8, 23} mod 25; (5n+1)/2 | → (1 3 8) | PROVED | 2 |
| mb_f125 | {68, 73, 83, 123} mod 125; (5n+1)/2 | → (1 3 8 4 2) | PROVED | 2 |
| mb_s49 | {32, 39} mod 49; (7n+1)/2 | → (1 4 2) | PROVED | 2 |
| mb_s343 | {93, 137, 142, 200, 228} mod 343; (7n+1)/2 | → (1 4 2) | PROVED | 2 |
| mb_d23_8 | n≡7 (8) → (n+1)/8; else div23_5n1 | → (1 6 3) | PROVED (93 leaves, depth 24) | 2 |
| mb_d23_4 | n≡3 (4) → (n+1)/4; else div23_5n1 | → (1 6 3) | PROVED | 2 |
| mb_d23_30 | n≡26 (30) → (n+4)/30; else div23_5n1 | → (1 6 3) | PROVED | 1–2 |
| mb_m3b_8 | n≡1 (8) → (n+7)/8, n≡7 (8) → (n+1)/8; else m3_b | → (1) | PROVED | 1–2 |
| mb_pair_3_27m | n≡13 (27) → (n−13)/27; (3n+1)/2; on N0 | no plain or run-accelerated descent certificate (ghost cycle −5 −7 −10); all n < 10^6 descend | OPEN (EVIDENCE) | 5 |
| mb_s3_27 | n≡26 (27) → (n+1)/27; (3n+1)/2 | no certificate (same ghost cycle); all n < 10^6 descend | OPEN (EVIDENCE) | 5 |
| mb_pair_5_25p | n≡13 (25) → (n+12)/25; (5n−3)/2 | no certificate (real cycle (3 6)); n < 10^6 reach (1) or (3 6) | OPEN (EVIDENCE) | 5 |

The exact c for each class is given in systems.py, in sparse_taming.md, and in the other system files. For the multi-class rows, c = (−r) mod m.

## The open frontier, stated precisely

1. The first open single-class tamings of 3x+1 are mb_s3_27 and mb_pair_3_27m. Neither can be proved by any descent-type certificate (Lemma B'), even run-accelerated. Proving them would need a non-local argument.
2. In the pairing family, P(3, 3, ±1), P(5, 2, ±1) and P(7, 2, ±1) are the first open members. The heuristic predicts convergence for a = 3 at every K, but divergence for a = 7 at K ≥ 4 (orbits passing 10^60 were observed for P(7, 4, 1)).
3. Whether 3x+1 taming sets mod 3^K need only o(3^K) classes for every K is EVIDENCE: the minima are 1, 2, 3, 4, 7 for K = 2..6.
4. div23_5n1 + (n ≡ 2 mod 4 → (n+2)/4) is unresolved by both methods.

## Item (3) of the task: matrix / weighted-automaton interpretations

`pip list` shows that neither z3 nor pysat is installed, so no solver-based search for matrix interpretations was run. One negative statement is relevant here, but it is only a SKETCH (no proof file, no check). For every system above that is listed OPEN, there is a verified expanding S-adic periodic point (Lemma B'). The sketch: a potential V(n) = n·c(n mod M) + d with c(·) > 0 and eventual decrease along orbits should be impossible, by chaining V along integers that shadow the expanding cycle for many periods (the CRT argument of Lemma B'). This has not been written out, so it is not claimed as proved. An arctic or matrix interpretation of a string-rewriting encoding is not covered by this argument, and I made no attempt at one.

## Refereeing

REFEREE.md found two false sub-claims in relatives.md and two gaps in its bound arguments; all are repaired as the referee instructed (corrections are marked in the text). Theorem D: the certified pairs do not all have the single cycle (1 6 3), and the bound now uses the integer cycle (−84 −42 −21 −7 −34 −17), giving q ≤ 83. Theorem M: m3_b + odd class has the cycles (1) and (2 3), and the bound now uses the refined Lemma B' plus the cycle (7/25, 1/25, −7/25, −1/25), giving q ≤ 32. Wording overclaims were fixed: mb_pair_3_9m, S3 "exactly", the mechanism sentence, and linear potentials.

## Checks (all exit 0; run times on this machine)

| script | covers | time |
|---|---|---|
| check_pairing_family.py | P1–P5, cycle lists, accelerated certificates | ~4 s |
| check_single_class.py | S3, S5 (witness for every odd m ≤ 301, every r, two c), S7 (m ≤ 199) | ~17 s |
| check_sparse.py | all 10 multi-class systems + minimality | ~30 s |
| check_relatives.py | Theorems D and M (repaired bounds, refined Lemma B', complete cycle list of every survivor), 4 named systems | ~10 s |
| check_systems.py | systems.py step functions = check tables | <1 s |

Exploratory scans and their outputs are in scratch/. They are EVIDENCE only and are not part of any proof.

## Novelty

The K = 1, a = 3 pairing case is Farkas (2005), via census/round2/literature/farkas2005.md. The K = 1 family for general a is a routine extension of that argument, and mb_pair_5_5m is the reflection of round 2's farkas5m_s27. Everything else is new to this census. Novelty against the wider literature was not checked: no web search was done.
