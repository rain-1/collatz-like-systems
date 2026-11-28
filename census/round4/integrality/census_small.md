# Small type-(c) unit tables, sorted by excursion structure (task 1)

Lens "integrality", round 4. Scripts: `census_small.py` (enumeration, about
25 s), `analyze_census.py` (sorting and orbit statistics, about 45 s),
`check_census.py` (exact re-check, about 1 min, exits 0). The data are in
`enum_*.json` and `census_small_summary.json`.

## Families (all exact)

| family | p, modulus | fixed branches | menu per free class | tables |
|---|---|---|---|---|
| F2m2 | 2, 4 | even n → n/2 | (u n + v)/w, u ∈ {1,3,5}, w ∈ {1,2,4}, v the two values of least \|v\| (one positive, one negative) with w \| u r + v | 18² |
| F2m3 | 2, 8 | even n → n/2 | same with u ∈ {1,3} | 12⁴ |
| F3m2 | 3, 9 | 3\|n → n/3 | (u n + v)/3, u ∈ {1,2,4}, two values of v | 6⁶ |
| F3m2b | 3, 9 | 3\|n → n/3 | (u n + v)/3, u ∈ {1,4,10} (u ≡ 1 mod 3; 10 ≡ 1 mod 9) | 6⁶ |

Types are computed exactly on G_m by `intlib.scc_types`. Both the expanding and
the contracting witness cycles are found by an exact multiplicative
Bellman–Ford in Fractions. 'c_mixed' means type (c) with an expanding *and* a
contracting cycle in the same SCC: the genuine Collatz-like case.
'c_exp' means type (c) where no cycle of that SCC contracts. (The first
version added "which is trivially divergent"; that was asserted without proof,
since orbits can leave the SCC, and is withdrawn. Nothing is claimed about
c_exp orbits.) Every type-(c) table was run through dichotomy/decide.py and is
OBST (asserted). A sample of 200 c_mixed tables per family is type (c) again at
level m+1 (Lemma L, check [E-lift]).

| family | fails (P) | (a) | (b) | c_mixed | c_exp |
|---|---|---|---|---|---|
| F2m2 | 86 | 54 | 0 | **168** | 16 |
| F2m3 | 8064 | 6612 | 0 | **6044** | 16 |
| F3m2 | 20736 | 9200 | 36 | **16668** | 16 |
| F3m2b | 14256 | 417 | 0 | **31225** | 758 |

No table in these families has a division-free cycle. Type (b) occurs only in
F3m2 (36 tables). Revision after REFEREE1: the first version said "all
settled by Theorem H" without running it. `check_typeb.py` now runs
`accel_lib.theorem_H` on all 36 (hypotheses hold at level K = 2) and records
the complete cycle lists in `typeb_cycles.json`: 18 tables have cycle minima
{1, 2}, 12 have {1}, 6 have {2}. PROVED (Theorem H); a brute-force cross-check
to n <= 20000 agrees. These are type (b), not type (c), so they do not bear on
the hard criterion.

## Sorting by excursion structure

Each c_mixed SCC is classified by its expanding fixed points (self-loops of
G_m with multiplier > 1), the branch multiplier u at the loop, s = v_p(u − 1)
(so u^k ≡ 1 mod p^s, i.e. the "predictable low digits" of the lens), and the sign
of x*. LONG means every expanding cycle of the SCC has length >= 2. Orbit
columns: a sample of up to 150 tables per class, orbits of all n <= 1500 (5000
steps, cap 10^30). They are EVIDENCE only.

| family | structure | tables | sampled | every sampled orbit reached a cycle | max log(peak)/log(n) |
|---|---|---|---|---|---|
| F2m2 | LONG | 72 | 72 | 58 | 8.1 |
| F2m2 | FP(u=5, s=2, x* neg. integer) | 24 | 24 | 22 | 6.4 |
| F2m2 | FP(u=5, s=2, x* pos. integer) | 24 | 24 | 22 | 5.3 |
| F2m2 | FP(u=5, s=2, x* non-integer) | 19 | 19 | 5 | 8.0 |
| F2m2 | FP(u=3, s=1, pos./neg. integer) | 19 | 19 | 19 | 6.6 |
| F2m3 | LONG | 3548 | 150 | 144 | 4.4 |
| F2m3 | FP(u=3, s=1, pos. integer) | 1448 | 150 | 145 | 4.4 |
| F2m3 | FP(u=3, s=1, neg. integer) | 920 | 150 | 141 | 3.4 |
| F3m2 | FP(u=4, s=1, pos. integer) | 7254 | 150 | 148 | 1.8 |
| F3m2 | FP(u=4, s=1, neg. integer) | 4840 | 150 | 149 | 2.0 |
| F3m2 | both signs | 2974 | 150 | 143 | 5.8 |
| F3m2 | LONG | 1600 | 150 | 150 | 1.8 |
| F3m2b | FP(u=10, s=2, non-integer) | 8458 | 150 | 97 | 13.2 |
| F3m2b | LONG | 5719 | 150 | 134 | 11.8 |
| F3m2b | FP(u=4, s=1, pos. integer) | 4129 | 150 | 129 | 8.4 |
| F3m2b | FP(u=4, s=1, neg. integer) | 3113 | 150 | 120 | 8.3 |

(The full list, including the smaller mixed classes, is in
`census_small_summary.json`.)

What the sorting shows:

* **High s does not make a class tamer.** The classes with u ≡ 1 (mod 9)
  (s = 2) are the ones with the most non-converging samples. Theorem M of
  `mixing.md` explains why the congruence class of u is irrelevant: the
  post-run point is uniform whatever s is. What matters for convergence is the
  drift, and u = 10 > 9 makes many of these tables expand on average.
* **The sign of x* does not separate the classes either.** Expanding fixed
  points at positive integers occur (they are genuine expanding cycles of T on
  positive integers, e.g. x* = 2 for the branch n ≡ 2 (mod 9) → (4n−2)/3). They behave like the
  negative ones. Integers that shadow x* from above grow, and deep shadowing
  forces n far above x*.
* **Base 3 with every step dividing by 3 (F3m2) is the most regular group.**
  The peak exponent stays near log_3 4 ≈ 1.26 to 2, because each step consumes
  exactly one ternary digit, so no orbit can gain more than a factor (4/3)
  per digit. This is the only place where an "integrality" bound is visibly
  sharp (see G3 below). It bounds growth per excursion, not the number of
  excursions.

## The new core G3 (PROVED type (c), OPEN)

The simplest c_mixed table found in base 3 is

    G3(n) = (4n+1)/3   if n ≡ 8 (mod 9),
    G3(n) = ⌈n/3⌉      otherwise.

It is type (c) at levels 2 and 3. Its SCC contains the expanding fixed point
x* = −1 (multiplier 4/3) and the contracting fixed point 1. decide.py says
OBST. In excursion form: n = 3^k m − 1 (k >= 2, 3 ∤ m) goes to 4^{k−1} m after
k steps, and everything else is "delete the last ternary digit and round up".
EVIDENCE: every n <= 10^11 reaches 1 (`g3verify.c`); the largest peak exponent
for n <= 3·10^5 is 1.238, against the integrality ceiling log_3 4 ≈ 1.262
(attained in the limit by n = 3^k − 1). PROVED (`cycles.md`, Corollary C2):
every other cycle has length >= 222404 (Z0 = 10^11 run) and all elements
> 10^11. GLOBAL for G3 is OPEN. It is the base-3 analogue of K7. Its first-return
process is i.i.d. with unbounded expanding branches (Theorem M), exactly as
for 3x+1.

## Novelty

Not checked.
