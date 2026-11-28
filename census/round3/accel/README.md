# Round 3, lens "accel": beyond descent certificates

This folder asks when a system with an expanding p-adic periodic point (OBST in the round-2 sense)
can still be settled, and when acceleration along the expanding cycle provably cannot help.

## Files

| file | content |
|---|---|
| `trichotomy.md` | Theorems H, N and T: the SCC trichotomy, isolated expanding cycles are harmless, and the acceleration barrier. Applications to the S-family and the catalog |
| `sfamily_obst.md` | Classification of the 12 OBST S-family members (m = 2, 3). Theorem Z (half-shift conjugacy), Corollary C (3x+1 in disguise), the 8 new cores |
| `dressing.md` | Theorem K: dressed systems, with expanding fixed points whose runs are consumed by a second prime |
| `acc_h32.md`, `acc_h16.md`, `acc_h9.md` | the systems settled by Theorem H |
| `accel_lib.py` | exact library: cylinder graphs, SCCs, exact contraction weights, Theorem H prover, Theorem N witnesses, exact cycle enumeration |
| `systems.py` | every map as a step function with an id |
| `check_trichotomy.py` | checks Theorems H/N applications (about 15 s) |
| `check_sfamily.py` | checks Theorem Z, Corollary C, the simplified cores, and the exact cycles up to period 26 (about 45 s) |
| `check_dressing.py` | checks Theorem K and its systems (about 5 s) |
| `scratch/` | searches and scans (not proofs): `hsearch2.py`, `h3s*.py`, `catscan.py`, `cycles30.py`, `sfam_evidence.py` |

All three checks exit 0.

## General theorems

| name | statement | status |
|---|---|---|
| Theorem H | Unit-multiplier p-adic system, no division-free cycle, T maps positive integers to positive integers. If every SCC of the cylinder graph G_K is contracting or a single simple (expanding) cycle, then every orbit is eventually periodic and the cycle list is a finite computation (SCC-wise weighted potential, weights verified exactly) | PROVED |
| Theorem N | If some expanding cycle shares its SCC with another cycle ("free re-entry"), then there is no *generalized certificate*: a countable cylinder cover of Z_p minus finitely many periodic orbits with locally constant stopping times. This covers accelerated certificates with symbolic run exponents and bounded lookahead. Proof: the closed walks C^d W give infinitely many expanding periodic orbits accumulating at x* | PROVED |
| Theorem T | Trichotomy: (1) plain certificate ⇔ all SCCs contracting; (2) generalized certificate ⇔ no type-(c) SCC; (3) no type-(c) SCC ⇒ GLOBAL settled. The type does not depend on the level K | PROVED |
| Theorem Z | S-family: the odd-to-odd map, in z = (n−1)/2, is G_S(z) = (odd(3z+2)−1)/2 or (odd(z+1)−1)/2 by class | PROVED |
| Corollary C | For S = {n ≡ 3 mod 4}, T_S^2(2z+1) = 2T(z)+1 with T the 3x+1 map, so this member is exactly 3x+1 | PROVED |
| Theorem K | Dressing D (p∣x → q^e x/p; q∣x → x/q; else g) has the same first-return map to pq-rough numbers as the undressed U, so GLOBAL(D) ⇔ GLOBAL(U), with cycles in bijection, but D never has a descent certificate. Shows that the Markov property (M), and hence unit multipliers, is needed for the type-(c) ⇒ infinitely many expanding periodic orbits mechanism; and that absence of certificates does not imply openness | PROVED |
| S-family barrier | For m ≤ 5, no subset S gives an isolated expanding cycle; an expanding periodic point at any level projects to a closed walk in G_m with multiplier > 1, one of whose simple cycles is expanding and lies in a type-(c) SCC, so all 2 + 10 + 172 + 48880 OBST members admit no generalized certificate | PROVED (exhaustive, exact) |
| Catalog barrier | 3x+1, 5x+1, split5_1, split5_3, m3_e, perm_1932, desc_m3_4n5, desc_split7_1: explicit exact Theorem-N witnesses. A scan found no open unit-multiplier catalog system of type (b) | PROVED for the listed systems; the scan is a computation (scratch/catscan.py) |

## Systems

Tiers follow census/RANKING.md. "OBST" means no descent certificate exists (expanding periodic
point, verified exactly).

| id | rule | question | answer | status | tier |
|---|---|---|---|---|---|
| acc_h32 | even→n/2; odd: n+1 (n≡5,9,21,25 mod 32), n+9 (n≡29), else 3n+1 | GLOBAL | yes; cycles (1 4 2), (3 10 5 6), (19 58 29 38) | PROVED (Thm H), OBST | 2–3 |
| acc_h16 | even→n/2; odd: n+1 (n≡5,9 mod 16), n+5 (n≡13), else 3n+1 | GLOBAL | yes; cycles (1 4 2), (3 10 5 6) | PROVED (Thm H), OBST | 2–3 |
| acc_h9 | 3q→q; 9q+r→6q+r (r=1,4,7); 9q+2→12q+4; 9q+5→12q+7; 9q+8→12q+11 | GLOBAL | yes; fixed points 1, 4, 7 | PROVED (Thm H), OBST, easy | 1–2 |
| dress_23_x1 | 2∣x→3x/2; 3∣x→x/3; else x+1 | GLOBAL | yes; only cycle (1 2 3) | PROVED (Thm K), OBST, easy | 1 |
| dress_32_x1 | 3∣x→4x/3; 2∣x→x/2; else x+1 | GLOBAL | yes; only cycle (1 2) | PROVED (Thm K), OBST, easy | 1 |
| dress_23_3x1 | 2∣x→3x/2; 3∣x→x/3; else 3x+1 | GLOBAL | ⇔ 3x+1 | equivalence PROVED; OPEN | 5 |
| dress_23_5x1 | 2∣x→3x/2; 3∣x→x/3; else 5x+1 | GLOBAL | ⇔ div23_5n1 | equivalence PROVED; OPEN | 5 |
| sf2_13, sf3_1357 | S-family, S = all odd classes | GLOBAL | is 3x+1 | OPEN | 5 |
| sf2_3, sf3_37 | S = {3} mod 4 | GLOBAL | ≡ 3x+1 (Corollary C), cycles (1 2), (3 10 5 6) ↔ 3x+1's 0, (1 2) | equivalence PROVED; OPEN | 5 |
| sf3_7 | S = {7} mod 8 | GLOBAL | new core K7: z even→z/2, z≡3 (4)→(3z+1)/2, z≡1 (4)→(z−1)/4 | OPEN; cycles of period ≤ 26 = {(1 2)} PROVED; no generalized certificate PROVED | 5 |
| sf3_17, sf3_57, sf3_157, sf3_357 | S = {1,7}, {5,7}, {1,5,7}, {3,5,7} mod 8 | GLOBAL | new 3x+1-perturbation cores (table in sfamily_obst.md) | OPEN; same partial results | 5 |
| sf3_13, sf3_135 | S = {1,3}, {1,3,5} mod 8 | GLOBAL | new cores, obstruction −5 (period 5, 9/8) | OPEN; same partial results | 5 |
| sf3_137 | S = {1,3,7} mod 8 | GLOBAL / divergence | new core W: o ↦ 3^{⌊(v−1)/2⌋}(3o+1)/2^v; drift +0.046, so divergence is expected (z = 7, i.e. n = 15, passes 10^60) | OPEN; cycles of period ≤ 26 are exactly the 4 listed | 5 |

## Answers to the lens programme

**(1) The 12 OBST S-family systems.**
* 4 are 3x+1: two literally, and two via the new exact conjugacy z = (n−1)/2 (Corollary C).
* 8 are isolated as precisely stated new cores (explicit z-maps). For each of them the following
  are proved: no descent certificate, no generalized/accelerated certificate (Theorem N), and the
  exact cycle list up to period 26.
* One core, W, has positive drift, so its sharp question is divergence.

None of the 12 is settled. Theorem N proves that no acceleration of the requested kind can settle
any of them.

**(2) Harmless expanding cycles.** There are two sufficient criteria, with proofs:
* *isolation* (Theorem H). It is exact for unit-multiplier systems (Theorem T);
* *consumption by a second prime* (Theorem K).

These settle five new OBST systems: acc_h32, acc_h16, acc_h9, dress_23_x1 and dress_32_x1. The
last three are easy and are labeled so. acc_h32 and acc_h16 need the machine-verified SCC
potentials.

Inside the requested S-family no system has an isolated expanding cycle (m ≤ 5, exhaustive). The
settled examples therefore had to be constructed with other exits (n+5, n+9), in base 3, or with
mixed primes.

**(3) The boundary.** Theorem T(2) is the boundary. For unit-multiplier p-adic systems,
acceleration-type certificates exist exactly when no expanding cycle shares its SCC with another
cycle. Free re-entry (round2 split5_3 "Blocking mechanism") is precisely the type-(c) condition,
now with a proof that it defeats every finite-orbit acceleration. Theorem K shows that outside
unit multipliers the boundary moves: graph-level re-entry can be harmless.

## Honest limits

* No open catalog system was settled. Theorem N says why, for this whole class of methods.
* The H examples were found by computer search. They are constructed systems, not natural ones.
* Literature: no search was done. All novelty claims are "novelty not checked". The ingredients
  (Markov partitions, max-mean cycles, Lemma B, conjugacy by half-shifts, FRACTRAN-like prime
  bookkeeping) are standard.

## Refereeing

Fixes from `REFEREE.md` applied:

* `trichotomy.md`, `README.md`: Theorem H now assumes T maps positive integers to positive integers; the proof says where n > 0 is used in V(Tn) ≤ θV(n) + β.
* `trichotomy.md`, `README.md`: S-family barrier now includes the projection step (expanding periodic point at level K' → closed walk in G_m with multiplier > 1 → an expanding simple cycle, whose SCC is type (c) by the scan).
* `dressing.md`, `README.md`: replaced "the unit-multiplier hypothesis in N is necessary / cannot be dropped" by the referee's wording: (M), hence unit multipliers, is needed for the type-(c) ⇒ infinitely many expanding periodic orbits mechanism, and absence of certificates does not imply openness.
