# The tail exponent of a table map, and the trichotomy as one number (27 Nov 2026)

Status: Theorem 1 and Corollary 2 are PROVED below (short proofs; classical tools). The table is
numerical (floats). Written outside the prover/referee loop while round 4 runs; NOT refereed.
Script: `theta.py` (`python3 theta.py check` exits 0).

**Correction.** The first version of this note claimed that core K7 has exponent 3.28 and that
systems split into "run-dominated" and "fluctuation-dominated" at a threshold 1.71, with K7 on
the favourable side. That was wrong: I used a one-state formula for a map that needs two states.
The correct K7 value is 1.6317, and Theorem 1 shows that no system with free re-entry can be on
the favourable side. What is true is the sharper statement below.

## Definitions

T(n) = (u n + v)/p^e on classes mod p^m, unit multipliers, cylinder graph G_K as in
`../../round3/accel/trichotomy.md` (node r mod p^K has p^e out-edges, each followed by a fraction
p^{-e} of the class, each with slope u/p^e). For theta >= 0 let M_theta be the matrix with entries

    M_theta[r, s] = sum over edges r -> s of p^{-e} (u/p^e)^theta,

and rho(theta) its spectral radius. M_0 is stochastic, so rho(0) = 1.

* **Tail exponent** theta_1 = sup{theta >= 0 : rho(theta) <= 1} (0 if the drift is positive,
  infinity if rho never exceeds 1).
* **Run exponent** of an expanding cycle C of G_K with multiplier lambda_C > 1 and v_C divisions:
  theta_C = v_C log p / log lambda_C. It is the theta at which p^{-v_C} lambda_C^theta = 1: the
  measure lost per lap exactly pays for the growth per lap. theta_run = min over expanding simple
  cycles (infinity if there are none).

Meaning of theta_1: a start rises by a factor R with probability about R^{-theta_1}
(Corollary 2). Meaning of theta_run: the same tail if the only way to rise were to sit next to
the expanding periodic point and ride one run.

## Theorem 1 (the trichotomy in terms of exponents). PROVED

Assume the standing hypothesis of round 3 (every cycle of G_K has a division).

1. All components of type (a) (every cycle contracts)  <=>  theta_1 = infinity.
2. Components of types (a) and (b) only, at least one (b) (expanding cycles, each isolated)
   =>  theta_1 = theta_run exactly.
3. If the cycle attaining theta_run lies in a component of type (c) (free re-entry), then
   theta_1 < theta_run strictly.

So "provable by round 3's methods" is exactly "the tail is no heavier than single runs make it",
and free re-entry is exactly a strictly heavier tail. The gap theta_run - theta_1 measures how
much re-entry adds.

*Proof.* Order the nodes by strongly connected components; M_theta is block triangular, so
rho(theta) = max over components of rho_S(theta). Three facts about one component S:

(i) theta -> log rho_S(theta) is convex (Kingman: the spectral radius of a matrix whose entries
are log-convex in a parameter is log-convex), and rho_S(0) <= 1.

(ii) For any cycle C of length l in S, rho_S(theta)^l >= product of its edge weights
= p^{-v_C} lambda_C^theta, with equality iff S consists of that cycle alone. (The matrix of the
cycle alone is entrywise <= the block of S; spectral radius is monotone, and strictly monotone
for an irreducible matrix when an entry is strictly increased.)

(iii) rho_S(theta)^{1/theta} tends to the largest geometric-mean slope of a cycle of S as
theta -> infinity (max-plus limit).

Type (a): by (iii) log rho_S -> -infinity; a convex function that is <= 0 at 0 and tends to
-infinity is <= 0 everywhere, so rho_S <= 1 for all theta. Type (b): rho_S(theta)^l =
p^{-v} lambda^theta by (ii), which exceeds 1 exactly for theta > theta_C. Type (c) containing an
expanding cycle C: by (ii) with strict inequality, rho_S(theta_C) > 1, so rho exceeds 1 before
theta_C. Items 1-3 follow by taking the maximum over components; for the converse in item 1, an
expanding cycle gives rho(theta) -> infinity by (ii). ∎

## Corollary 2 (counting risers). PROVED

Let rho(theta) < 1. There is C such that for all X and R >= 1, the number of n <= X whose orbit
reaches R n at some point of its first floor(log_p X) - K digit steps is at most C X R^{-theta}.

*Proof.* The walks that first reach slope product >= R at their last step define disjoint
cylinders D_w of depth at most log_p X, each containing at most 2 X mu(D_w) integers up to X.
Then sum_w mu(D_w) <= R^{-theta} sum_w mu(D_w) slope(w)^theta <= R^{-theta} sum_t 1^T M_theta^t 1
/ p^K, a convergent series. The small additive terms in T^j(n) change R by a bounded factor. ∎

For split5_3 (theta_1 = 6.149) this says: among n <= X, at most C X^{1 - 6.1 kappa} rise by
X^kappa inside the digit horizon, so none do once kappa > 0.164, while the explicit run gives
kappa = 1/theta_run = 0.161. Inside the horizon the worst integers are essentially the explicit
ones.

## Table (numerical)

| system | type | theta_1 | theta_run | gap |
|---|---|---|---|---|
| acc_h16 (settled in round 3 by Theorem H) | b | 1.7095 | 1.7095 | 0 |
| S = {1,3,5} mod 8 core | c | 17.6416 | 17.6548 | 0.013 |
| S = {1,3} mod 8 core | c | 17.6282 | 17.6548 | 0.027 |
| split5_3 (CLS-049) | c | 6.1492 | 6.2126 | 0.063 |
| S = {5,7} core | c | 1.6431 | 1.7095 | 0.066 |
| K7 = S = {7} core | c | 1.6317 | 1.7095 | 0.078 |
| S = {1,5,7}, {3,5,7}, {1,7} cores | c | 1.629, 1.618, 1.618 | 1.7095 | 0.08 to 0.09 |
| split5_1 (CLS-048) | c | 0.5393 | 0.7565 | 0.217 |
| 3x+1 (and S = {3,7}, which is 3x+1) | c | 1.0000 | 1.7095 | 0.710 |
| m3_b (CLS-004) | c | 1.0000 | 3.8188 | 2.819 |
| 5x+1, S = {1,3,7} (core W) | c | 0 (positive drift) | | |

Values are the same at K = m and K = m + 1. Core systems are "odd n -> 3n+1 if n mod 8 in S, else
n+1; even n -> n/2".

## What this gives and what it does not

* It is one computable number that orders the open systems by how far they are from the provable
  class. split5_3 and the {1,3} cores are within a few percent of the boundary; 3x+1 and m3_b are
  far from it; split5_1 is much further out than split5_3, in line with round 3's dimension gap.
* It does NOT settle any system. Corollary 2 controls only the first log n digit steps, the same
  horizon limit as every density result.
* Backward identity (one-state maps with one digit block per step): the expected weighted number
  of children in the inverse tree is B(gamma) = rho(gamma - 1), so the backward growth exponent is
  1 + (the negative root of rho = 1). For 5x+1, 7x+1, 9x+1 this gives 0.6509, 0.3735, 0.2581, the
  values `../../round3/progressions/theorem_C_counting.md` section 4 found by a separate route.
* K7 normal form (PROVED, direct computation): on odd n the system S = {7} is
  n -> 3^{max(v-2,0)} m, where n + 1 = 2^v m with m odd. It rises only when v >= 6.

OPEN, and the natural target: a proof for a type-(c) system with small gap. A small gap means
almost all of the danger is the single run, which is explicit; the proof would have to bound the
re-entry contribution (the gap) by an argument that sees more than the first log n digits.

## Ideas tried that failed, with the reason

* K7 by "every run is followed by a net drop": false; the net factor of a run of length k is
  (3/2)^{k-1}/4, above 1 for k >= 5.
* Counting squeeze between ancestor counts and non-dropping counts: the large-deviation rate is
  convex and lies under the line it would need to cross, for every system.
* Progression theorem plus a descending progression: the two bounds are automatically consistent.
