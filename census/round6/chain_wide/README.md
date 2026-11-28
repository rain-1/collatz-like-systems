# Round 6, lens "chain_wide": the occupation bound and the chain theorem for every table map

**Bottom line.** This round settles no census system and no open question. What it does is take two
results proved only for split5_3 and prove them for every single-prime table map with unit
multipliers, a finite state graph G(T) and a certified negative drift (for the chain theorem also:
all constants `v_r ≥ 0` and the raw-prefix condition (R), or the signed version with (S1)):

* the **occupation and multiplier bound** (how often one non-periodic orbit can visit values below X,
  and how closely the orbit follows its multiplier product);
* the **chain theorem** (the successive multiplier minima of an escaping orbit are linked permanent
  survivors, and every window of B late octaves holds at least A(B) of them).

Both are then evaluated on 23 named census systems and on 4 families (709 maps, 343 of them with a
certified negative drift). Proofs are in `THEORY.md` and the finite content is checked by
`check_chain.py` (exit 0).

A small remark (Proposition 5.1, nearly tautological): for maps whose constants are all ≥ 0, the set
`N^mult` of starts whose raw multiplier never drops below 1 is empty exactly when every orbit is
eventually periodic, and otherwise Theorem 4 puts at least A(B) of its members in every late
B-octave window. So the window criterion is a real target only for the computable finite-depth
supersets, and there it is still far beyond what is proved.

All statements were written and checked by an agent and examined by two agent referees
(`REFEREE1.md`, `REFEREE2.md`); the repairs are listed in "Revision after REFEREE1" and "Revision after
REFEREE2" below. No human has reviewed them.

## Results table

| system | technique | result | status |
|---|---|---|---|
| every single-prime table map with a certified negative drift (signs allowed) | occupation bound (Thm 1, 2) | visits of a non-periodic orbit below X: `V(X) ≤ W p^θ X^θ + s⌈log_p X⌉E` for every certified θ, so `X^{θ*+o(1)}`, where θ* is the optimal moment exponent (the dimension of the non-descending set) | PROVED |
| same | multiplier bound (Thm 3) | `1 ≤ x_t/(x_0 P_t) < e^{E*}` (constants ≥ 0), or `e^{-E*} <` it `< e^{E*}` (signed: at updates; at raw times under (S1)), with E* explicit from a verified range; so `P_t → ∞` on every non-periodic orbit | PROVED |
| same, constants ≥ 0, raw-prefix condition (R) | chain theorem (Thm 4) | selected starts lie in `N^mult ⊆ N_T`; link ratio is in `(1, ρ]`, ρ = largest edge slope; exact expansion count for two-slope maps; strip `r x_i + C_i`; forced residue classes; at least `A(B) = max{k : ρ^k < 2^B}` per B late octaves | PROVED |
| same | Prop. 5.1 (remark) | `N^mult = ∅` ⇔ GLOBAL; if nonempty, at least A(B) members in every late B-window; `N^mult ∩ [1, N_0) = ∅` on any verified range | PROVED (nearly tautological) |
| same | Cor. 5 (window criterion) | infinitely many windows with fewer than A(B) finite-depth survivors ⇒ GLOBAL ("survive" = every raw prefix multiplier ≥ 1, or every root-tree update multiplier ≥ 1; the clause "> 1 at updates" added in the REFEREE1 revision is false and **withdrawn after REFEREE2**); the count law implies it at depth factor `C* = 1/(1-θ*)`; what is proved reaches depth factor 1 | PROVED (criterion) / OPEN (hypothesis) |
| 3x+1 (CLS-013) | Thm 2 + Barina's range | every element of a divergent trajectory: `#{t : T^t(n) ≤ X} ≤ 2(2^{θ} X^{θ} + (41/84)⌈log_2 X⌉ E)`, θ = 1082/1139, E ≤ 3.46 (range 2^68, quoted) or E ≤ 12.04 (2^32, own check). Lagarias (2.32) bounds only the never-dropping elements, with the same exponent | PROVED (novelty not checked) |
| 3x+1 | Thm 3 | `1 ≤ x_t/(x_0P_t) < 31.7` (2^68) or `< 1.7·10^5` (2^32) on any divergent orbit | PROVED |
| 3x+1, all 3x+d in the table | Thm 4 | an escaping orbit has at least 1 member of `N^mult` in every late octave, and 17 in every 10; every member is 3 mod 4 when d ≡ 1 (mod 4) and 1 mod 4 when d ≡ 3 (mod 4) | PROVED (conditional on escape; nothing settled) |
| split5_3 (CLS-049/065) | all | reproduces the repo: 31 per ten octaves, `256 \| x+3`, and improves the multiplier constant to `E* < 5.4·10^-5` at 2^48 and `2.84·10^-7` at 2^66 (repo: 7.3·10^-5) | PROVED |
| K7 = sf3_7 and the cores sf3_17, 57, 157, 357, 13, 135 (round 3 accel) | all | see the named table: exponents 0.36–0.79, A(10) = 17 (58 for sf3_135), forced classes 63 mod 64 (K7, 17, 57, 157), 15 mod 16 (357), 1019 mod 1024 (13, 135); multiplier constants between e^{1.1·10^-5} (sf3_135) and e^{1.24} (sf3_357) | PROVED |
| split5_1, m3_b (signed, (S1) holds), m3_d, m3_g, desc_split7_1, desc_m3_4n5, desc_s32_plus9 | all | named table. m3_b's E* recomputed after REFEREE1 (50.7372625…, was 1e-9 too small). m3_* have no forced congruence (survivors only need 4 or 3 non-divisions first); m3_g has certified θ = 1906/1907, so its constants are nearly useless (E* ≈ 6.3·10^3) | PROVED |
| 5x+1, 7x+1 (expanding) | mirror (Prop. 6, 7) | no occupation mirror: every moment exponent is > 1 (proved); the full chain theorem holds on any non-periodic orbit with `Σ 1/x_t < ∞` (proved, conditional; both maps satisfy (R)); orbit segments show it with the count A(10) attained exactly (EVIDENCE) | PROVED / EVIDENCE |
| core W (expanding) | mirror (Prop. 6, 7) | **core W fails (R)**: only the update-time conclusions of Prop. 7 apply; raw-time survival fails (orbit of 15: selected update value 263, raw orbit reaches 223 with raw multiplier 27/32). The earlier unqualified claim is withdrawn | PROVED (update times) |
| families S3 (16), S4 (256), split_{a,d} (32), m3_{a,c1,c2} (405) | all | **343** members with certified negative drift (revised from 240: 103 strongly contracting members had been dropped, now certified with γ = 1, θ = 0); constants tabulated; 35 S4 members fail (R), so for them the survival statement holds only at update times; 63 of the 343 have no expanding edge at all, so the chain is empty and the theorems hold vacuously (these maps are GLOBAL by Cor. 3.1) | PROVED (per member, data/families.json) |
| any census entry | all | **nothing settled** | OPEN |

## Per-system constants (named systems)

Here θ is the certified exponent (Thm 1–3), W is the weight constant, ρ the largest edge slope, and
`A(1)`, `A(10)` the forced counts of selected starts per 1 and per 10 late octaves. `k*` is the
number of leading expansions forced after every selected start. The forced class is the residue of
the selected start (the value itself, unshifted) mod `p^D` common to all survivor classes at tree
depth 14 (p = 2) or 9 (p = 3); the survivor mass is `Σ 1/M` over those classes, an upper bound for
their Haar mass. `C*` is the
depth factor at which the count law predicts fewer than A(B) survivors per window. `E*` is the
multiplier error (Thm 3) for the range listed, so `x_t/(x_0P_t) < e^{E*}`.

| system | origin | theta (certified) | W | rho | A(1) | A(10) | k* | forced class (depth 14 / 9) | survivor mass | C* = 1/(1-theta) | verified range | E* (own range) | E* (literature range) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| par_3_1 | CLS-013 | 1082/1139 = 0.94996 | 1 | 3/2 | 1 | 17 | 2 | 3 mod 2^2 | 0.0448 | 19.98 | 2^32 | 12 (s = 1/2) | 3.46 (s = 1/2) at 2^68 |
| par_3_m1 (signed) | CLS-018 | 1082/1139 = 0.94996 | 1 | 3/2 | 1 | 17 | 2 | 1 mod 2^2 | 0.0448 | 19.98 | 2^32 | 24.1 (s = 1/2) | - |
| par_3_3 | CLS-014 | 1082/1139 = 0.94996 | 1 | 3/2 | 1 | 17 | 2 | 1 mod 2^2 | 0.0448 | 19.98 | 2^32 | 36.1 (s = 1/2) | - |
| par_3_5 | CLS-015 | 1082/1139 = 0.94996 | 1 | 3/2 | 1 | 17 | 2 | 3 mod 2^2 | 0.0448 | 19.98 | 2^32 | 60.2 (s = 1/2) | - |
| par_3_7 | CLS-016 | 1082/1139 = 0.94996 | 1 | 3/2 | 1 | 17 | 2 | 1 mod 2^2 | 0.0448 | 19.98 | 2^32 | 84.3 (s = 1/2) | - |
| par_3_9 | CLS-017 | 1082/1139 = 0.94996 | 1 | 3/2 | 1 | 17 | 2 | 3 mod 2^2 | 0.0448 | 19.98 | 2^32 | 108 (s = 1/2) | - |
| par_3_13 | CLS-011 | 1082/1139 = 0.94996 | 1 | 3/2 | 1 | 17 | 2 | 3 mod 2^2 | 0.0448 | 19.98 | 2^32 | 157 (s = 1/2) | - |
| par_3_17 | CLS-012 | 1082/1139 = 0.94996 | 1 | 3/2 | 1 | 17 | 2 | 3 mod 2^2 | 0.0448 | 19.98 | 2^32 | 205 (s = 1/2) | - |
| sf3_7 | round3/accel sf3_7 (core K7) | 597/797 = 0.74906 | 3.29 | 3/2 | 1 | 17 | 2 | 63 mod 2^6 | 0.00117 | 3.98 | 2^32 | 0.222 (s = 3/4) | - |
| sf3_17 | round3/accel sf3_17 | 207/262 = 0.79008 | 4.65 | 3/2 | 1 | 17 | 1 | 63 mod 2^6 | 0.00191 | 4.76 | 2^32 | 0.973 (s = 4/5) | - |
| sf3_57 | round3/accel sf3_57 | 305/424 = 0.71934 | 8.59 | 3/2 | 1 | 17 | 2 | 63 mod 2^6 | 0.00113 | 3.56 | 2^32 | 0.25 (s = 29/40) | - |
| sf3_157 | round3/accel sf3_157 | 345/446 = 0.77354 | 3.31 | 3/2 | 1 | 17 | 1 | 63 mod 2^6 | 0.00153 | 4.42 | 2^32 | 0.438 (s = 4/5) | - |
| sf3_357 | round3/accel sf3_357 | 171/217 = 0.78802 | 6.51 | 3/2 | 1 | 17 | 2 | 15 mod 2^4 | 0.00531 | 4.72 | 2^32 | 1.24 (s = 3/4) | - |
| sf3_13 | round3/accel sf3_13 | 372/869 = 0.42808 | 13.6 | 3/2 | 1 | 17 | 1 | 1019 mod 2^10 | 0.000122 | 1.75 | 2^32 | 0.000208 (s = 159/40) | - |
| sf3_135 | round3/accel sf3_135 | 522/1453 = 0.35926 | 3.47 | 9/8 | 5 | 58 | 3 | 1019 mod 2^10 | 4.58e-05 | 1.56 | 2^32 | 1.07e-05 (s = 157/40) | - |
| split5_1 | CLS-048/064 | 994/1061 = 0.93685 | 2.09 | 5/2 | 0 | 7 | 1 | 5 mod 2^3 | 0.0214 | 15.84 | 2^32 | 44.1 (s = 11/40) | - |
| split5_3 | CLS-049/065 | 457/787 = 0.58069 | 2.29 | 5/4 | 3 | 31 | 4 | 253 mod 2^8 | 0.000244 | 2.38 | 2^32 | 0.00556 (s = 9/4) | 2.84e-07 (s = 9/4) at 2^66 |
| m3_b (signed) | CLS-004/061 | 521/540 = 0.96481 | 1 | 4/3 | 2 | 24 | 4 | none (D = 0) | 0.091 | 28.42 | 2^32 | 50.7 (s = 19/40) | - |
| m3_d | CLS-005/062 | 521/540 = 0.96481 | 1 | 4/3 | 2 | 24 | 4 | none (D = 0) | 0.091 | 28.42 | 2^32 | 50.7 (s = 19/40) | - |
| m3_g | CLS-008/063 | 1906/1907 = 0.99948 | 1 | 5/3 | 1 | 13 | 3 | none (D = 0) | 0.182 | 1907.00 | 2^27 | 6.26e+03 (s = 1/20) | - |
| desc_split7_1 | CLS-053 | 703/933 = 0.75348 | 2.17 | 7/4 | 1 | 12 | 2 | 5 mod 2^4 | 0.00342 | 4.06 | 2^32 | 0.166 (s = 19/20) | - |
| desc_m3_4n5 | CLS-051 | 432/577 = 0.74870 | 1 | 4/3 | 2 | 24 | 2 | 4 mod 3^2 | 0.00376 | 3.98 | 2^32 | 0.107 (s = 59/40) | - |
| desc_s32_plus9 | CLS-052 | 780/1369 = 0.56976 | 235 | 9/4 | 0 | 8 | 1 | 7 mod 2^3 | 0.000309 | 2.32 | 2^32 | 0.204 (s = 9/5) | - |

"Survivor mass" is `Σ 1/M` over the survivor classes of all states. Classes of different states can
overlap, so it is **an upper bound** for the Haar mass of the union, not the mass itself.
`A(1) = 0` (split5_1, desc_s32_plus9) makes the one-octave window criterion vacuous; use B ≥ 2.

How to read one row, for 3x+1 (the raw map n/2, 3n+1; its tree edges are n/2 and (3n+1)/2). Suppose
an orbit escapes. Then from some point on, every octave `[2^m, 2^{m+1})` contains a start `x` of
that orbit with these properties: x ≡ 3 (mod 4); every later raw multiplier of the orbit is ≥ 1;
every later value is larger than x. The next such start is `(3/2)^a 2^{-e} x + C` with
`a = ⌊1.7095 e⌋ + 1`. The verified ranges (2^32 here, 2^68 in the literature) only enter E*.

## Families (data/families.json, data/families_summary.md)

Revised after REFEREE1. "Clipped" members are strongly contracting maps whose best certificate had
γ > 1; they satisfy (N) with γ = 1 (θ = 0, so a non-periodic orbit would visit only O(log X) values
below X), checked exactly. "No expanding edge" members have every edge slope ≤ 1, so `P_l ≤ 1` on
every orbit and Corollary 3.1 already excludes non-periodic orbits; nothing in the chain theorem is
informative for them (A(B) is shown as None). A forced D of −1 means no survivor class at depth 14 /
9 at all.

### S3: 16 members, 15 with a certified negative drift
non-certified reasons: {'drift > 0': 1}
no expanding edge (all slopes <= 1, GLOBAL trivially by Cor. 3.1): 5
clipped to gamma = 1 (theta = 0): 6
| rho | A(1) | A(10) | members | theta range | C* range | forced D range | raw (R) ok | signed |
|---|---|---|---|---|---|---|---|---|
| 3/2 | 1 | 17 | 9 | 0.0000-0.9500 | 1.00-19.98 | -1-10 | True | 0 |
| 1 | None | None | 4 | 0.0000-0.0000 | 1.00-1.00 | -1--1 | True | 0 |
| 1/2 | None | None | 1 | 0.0000-0.0000 | 1.00-1.00 | -1--1 | True | 0 |
| 9/8 | 5 | 58 | 1 | 0.3593-0.3593 | 1.56-1.56 | 10-10 | True | 0 |

### S4: 256 members, 255 with a certified negative drift
non-certified reasons: {'drift > 0': 1}
no expanding edge (all slopes <= 1, GLOBAL trivially by Cor. 3.1): 45
clipped to gamma = 1 (theta = 0): 84
| rho | A(1) | A(10) | members | theta range | C* range | forced D range | raw (R) ok | signed |
|---|---|---|---|---|---|---|---|---|
| 3/2 | 1 | 17 | 189 | 0.0000-0.9999 | 1.00-6722.00 | -1-14 | False | 0 |
| 1 | None | None | 44 | 0.0000-0.0000 | 1.00-1.00 | -1--1 | True | 0 |
| 9/4 | 0 | 8 | 14 | 0.0000-0.8564 | 1.00-6.96 | -1-14 | False | 0 |
| 9/8 | 5 | 58 | 6 | 0.3250-0.3593 | 1.48-1.56 | 10-11 | True | 0 |
| 1/2 | None | None | 1 | 0.0000-0.0000 | 1.00-1.00 | -1--1 | True | 0 |
| 27/16 | 1 | 13 | 1 | 0.7294-0.7294 | 3.70-3.70 | 2-2 | True | 0 |

### split: 32 members, 28 with a certified negative drift
non-certified reasons: {'drift > 0': 4}
no expanding edge (all slopes <= 1, GLOBAL trivially by Cor. 3.1): 4
clipped to gamma = 1 (theta = 0): 4
| rho | A(1) | A(10) | members | theta range | C* range | forced D range | raw (R) ok | signed |
|---|---|---|---|---|---|---|---|---|
| 1 | None | None | 4 | 0.0000-0.0000 | 1.00-1.00 | -1--1 | True | 0 |
| 3/2 | 1 | 17 | 4 | 0.9500-0.9500 | 19.98-19.98 | 3-3 | True | 0 |
| 5/2 | 0 | 7 | 4 | 0.9369-0.9369 | 15.84-15.84 | 3-3 | True | 0 |
| 5/4 | 3 | 31 | 4 | 0.5807-0.5807 | 2.38-2.38 | 8-8 | True | 0 |
| 7/4 | 1 | 12 | 4 | 0.7535-0.7535 | 4.06-4.06 | 4-4 | True | 0 |
| 9/2 | 0 | 4 | 4 | 0.9908-0.9908 | 109.03-109.03 | 2-2 | True | 0 |
| 9/4 | 0 | 8 | 4 | 0.9500-0.9500 | 19.98-19.98 | 2-2 | True | 0 |

### m3: 405 members, 45 with a certified negative drift
non-certified reasons: {'graph error: branch loop without new information at (': 270, 'drift > 0': 90}
no expanding edge (all slopes <= 1, GLOBAL trivially by Cor. 3.1): 9
clipped to gamma = 1 (theta = 0): 9
| rho | A(1) | A(10) | members | theta range | C* range | forced D range | raw (R) ok | signed |
|---|---|---|---|---|---|---|---|---|
| 4/3 | 2 | 24 | 27 | 0.7487-0.9648 | 3.98-28.42 | 0-2 | True | 0 |
| 2/3 | None | None | 9 | 0.0000-0.0000 | 1.00-1.00 | -1--1 | True | 0 |
| 5/3 | 1 | 13 | 9 | 0.9995-0.9995 | 1907.00-1907.00 | 0-0 | True | 0 |


The families include members that round 3 already settles by descent certificates (type (a)) or by
Theorem H (type (b)). For those the chain theorem holds vacuously, since they have no escaping
orbit. The table is not filtered by type. Every non-certified member has positive drift (96) or a
state-graph error, a division-free branch loop (270, all in m3), to which nothing here applies
(`check_revision.py [R4]`). [The earlier sentence said the same but was false: 103 negative-drift
members had been dropped by an assertion `γ ≤ 1`.]

## What the chain structure implies (THEORY.md §5)

* **Empty or many (PROVED, nearly tautological: Prop. 5.1).** With constants ≥ 0, `N^mult` is either empty (⇔ GLOBAL) or has at least
  `log X / log ρ − O(1)` members below X, at least A(B) in every late B-window. Its counting function
  is also at most `O(X^{θ*+ε})`. On every verified range it is empty.
* **Weakest sufficient count.** "At most `A(B) − 1` finite-depth survivors in `[2^m, 2^{m+B})` for
  infinitely many m". For 3x+1 with B = 1 this reads: infinitely many octaves in which no start
  survives (in multiplier) to some depth `b(m)`. For split5_3 with B = 1 it reads "at most 2 per
  octave", which matches the repo's two-survivor target.
* **Count law vs proved.** The count law (Conjecture E) gives this at depth `b ≈ C* m` digits, where
  C* = 19.98 (3x+d), 2.38 (split5_3), 3.98 (K7), 15.84 (split5_1), 28.42 (m3_b, m3_d) and 1907 (m3_g).
  The proved count laws (round 5 for 3x+d, split5_3 in the repo) reach depth `m + O(log m)` in almost
  every octave. At that depth the predicted number of survivors is `2^{θ* m + o(m)}`, which is
  exponentially more than A(B). The gap is the depth factor C*, and it is the same gap as in
  Conjecture E itself.
* **Occupation vs chain.** An escaping orbit has at least `log X/log ρ − O(1)` and at most
  `W p^θ X^θ + O(log X)` visits below X. These bounds do not meet, so nothing in this lens excludes
  escape.

## Files

| file | content |
|---|---|
| `THEORY.md` | all statements and proofs (Lemmas 1–4, Theorems 1–4, Corollaries 3.1, 5, Propositions 5.1, 6, 7), literature notes |
| `chainlib.py` | σ-trees, survivor classes, forced congruences, occupation and multiplier constants (exact), chain counts |
| `chain_systems.py` | the 23 named systems and 3 expanding ones (exact tables), the families |
| `chain_table.py` | computes `data/named.json`, `data/families.json` (about 7 minutes for families, 15 s for named) |
| `make_tables.py`, `summarize_families.py` | print the tables above |
| `verify_range.c`, `run_ranges.py` | exact range certificates (every n < 2^32, or 2^27 for m3_g, reaches a value < n or a known cycle; values past 2^120 are finished in Python) → `data/ranges_*.json`, `data/ranges_32.log` |
| `check_chain.py` | exact checks [1]–[7] (exit 0; about 15 s; output in `data/check_chain.out`) |
| `check_revision.py` | exact checks [R1]–[R5] of the repairs after REFEREE1 (exit 0; about 1 min; output in `data/check_revision.out`) |
| `REFEREE1.md`, `referee1_check.py`, `referee1_check.out` | the referee report, its script and its output on the pre-revision folder (`data/referee1_check_after_revision.out`: its output after the repairs) |
| `evidence_expanding.py` | EVIDENCE for the mirror section → `data/evidence_expanding.out` |

Reproduce: `gcc -O2 -o verify_range verify_range.c; python3 run_ranges.py 32 <ids>` (about 200 CPU
seconds per system), `python3 run_ranges.py 27 m3_g`, `python3 chain_table.py`,
`python3 check_chain.py`.

## Honest limits

* No census entry is settled, and none of the theorems can settle one alone. Each is a consequence
  of escape or a bound on how an escaping orbit behaves.
* The window criterion applied to `N^mult` itself is equivalent to GLOBAL (Prop. 5.1). The only
  non-trivial targets are the finite-depth versions, and they need the count law far beyond its
  proved range.
* For maps with θ* close to 1 (3x+d, m3_b, m3_d, m3_g, split5_1) the multiplier constants are poor:
  e^{3.46} for 3x+1 even with the 2^68 range, and e^{6260} for m3_g. They are finite, which is all the
  dichotomy and the chain theorem need.
* The count A(B) is attained exactly on long 5x+1 and 7x+1 orbit segments (EVIDENCE). So it cannot be
  improved using ρ alone, but a sharper per-link analysis like split5_3's sharp strips might improve
  it for particular maps. That was not attempted here.
* (R) fails for core W (expanding) and for 35 S4 members (31 before the revision plus 4 of the newly certified ones). There, the raw-time survival in Theorem 4(a)
  holds only at update times, and `N^mult` must be read as "update-time multiplier survivors".
* The independent raw-iteration test of the forced classes ([4]) found no samples for sf3_13 and
  sf3_135 (survivor mass about 2·10^-4). For these two, only the exact tree enumeration supports the
  forced class.
* Mixed-prime maps (div23, div235) are not covered. Lemma 1 and the class counting in (1) use a single
  prime.
* Novelty was not checked, except against Lagarias's 1985 survey (read in the scanned source). The
  3x+1 verified range 2^68 (Barina 2021) is quoted from memory.

## Revision after REFEREE1

The referee found no gap in the core proofs and three substantive defects. All are repaired; the
repairs are checked by `check_revision.py` (exit 0), and `check_chain.py` still exits 0.

| item | referee verdict | repair |
|---|---|---|
| signed E* (3x−1, m3_b) | values about 1e-9 (relative) **below** the proved bound, so not upper bounds | `multiplier_E` now uses `g' = 2g` in numerator and denominator; recomputed: 3x−1 24.0788944447, m3_b 50.7372625433; checked against an independent 50-digit evaluation, and the old values are checked to fail (`[R1]`) |
| signed raw-time claims | Z inside an edge not controlled | new hypothesis (S1) (at most one raw step with v ≠ 0 per edge); holds for 3x−1 and m3_b (`[R2]`, with an exact raw-Z test and a negative control); without it the signed statements are at update times only |
| core W under Prop. 7 | **WRONG**: core W fails (R) | claim withdrawn; Prop. 7 now has an update-time version, which is what applies to core W; the raw drop 263 → 223 is checked (`[R3]`); 5x+1 and 7x+1 satisfy (R) |
| families coverage | **WRONG** sentence; 103 negative-drift members dropped | γ clipped to 1 with an exact re-check; 343 certified members; every non-certified member has positive drift or a graph error (`[R4]`). While re-running, a loop in `chain_table.kstar` for maps with no expanding edge was found and fixed (those 63 members get A(B) = None) |
| (P) | (not flagged, found during repair) the raw-time steps use nonnegative partial intercepts, not just `G_e ≥ 0` | (P) restated as "every `v_r ≥ 0`"; holds for every system called (P) (`[R5]`) |
| wording | §0 units sentence false; Thm 2 typo; "edges with F ≠ 1" in 4(b), 4(d); survivor mass is an upper bound; "survive" means ≥ 1; Prop. 5.1 oversold; A(B) = 0 vacuous; hypotheses of the headline; one split5_3 figure | all fixed in `THEORY.md` (see its §8) and here |

Status changes: no PROVED statement about a named contracting system changes. The core W row is
downgraded from the full Prop. 7 to its update-time part. The headline still stands: **nothing in the
census is settled by this lens.**

The referee's own script, re-run after the repairs (`data/referee1_check_after_revision.out`): 265
PASS, including both signed [E] checks that failed before. Two FAILs remain, and both encode the
pre-revision claims that were withdrawn ("core W satisfies (R)"; "exactly 240 certified family
members, 31 failing (R)"). The run did not finish: the referee's `A_of(F, B)` loops forever for
F = 1, and the revised family data now contain certified members with ρ = 1, which its random sample
reaches. The run was stopped by hand after about 50 minutes, so its last three family checks did not
run; `check_revision.py [R4]` covers the coverage statement they test. I did not edit the referee's
script.

## Revision after REFEREE2

The second referee (`REFEREE2.md`, own script `referee2_check.py`: 241 PASS, 0 FAIL) confirmed every
proof and found one substantive wording defect plus small slips. Text fixes only; no number, check or
status changes.

| item | repair |
|---|---|
| **Cor. 5: false clause (WITHDRAWN)** | The REFEREE1 revision had added "or equivalently for this purpose every update multiplier over the first b updates is > 1 (Theorem 4(a) gives strict inequality at updates)". This is **false**: for split5_3 and the S-family the root edge (1,0) → digit 1 is a pure split with F = 1, so every odd start, including every selected start, has root-tree update multiplier exactly 1. Read literally, the clause would make `N_b` empty and the criterion would "prove" GLOBAL for split5_3. The clause is withdrawn and replaced by "every root-tree update multiplier over the first b updates is ≥ 1", which the raw condition implies (`THEORY.md` §4 and §9; referee check `[J]`) |
| Prop. 7 | "`Σ 1/x_t < ∞` is equivalent to `sup Z < ∞`" → "implies" (only that direction is proved) |
| families paragraph | positive-drift count 97 → **96** (1 S3 + 1 S4 + 4 split + 90 m3) |
| families row | "trivially type (a)" → "GLOBAL by Cor. 3.1" (no descent certificate was produced) |
| m3_g row | "θ* = 1906/1907" → "certified θ = 1906/1907" |
| K7 row | multiplier constants are between e^{1.1·10^-5} (sf3_135) and e^{1.24} (sf3_357), not "e^{0.22} (K7) down to e^{1.1·10^-5}" |

## What stayed open

Every GLOBAL question in the census. Specifically: whether infinitely many octaves have fewer than
A(B) finite-depth survivors for any of these maps; a useful mirror of the chain theorem for
expanding maps (Prop. 6 shows the moment method gives none); whether `Σ 1/x_t < ∞` on 5x+1 orbits
(EVIDENCE says yes on segments); and mixed-prime versions.
