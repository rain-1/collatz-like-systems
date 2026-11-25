# yah_avoid57: Collatz with the classes 5 and 7 mod 8 sent to 1 (OPEN)

## Statement

The map is C_K with K = {5, 7}: n = 5 or 7 mod 8 goes to 1, and otherwise the map is the Collatz map (n/2 for even n, 3n+1 for odd n).

**Question (GLOBAL).** Does every orbit enter {1, 4, 2}?

This holds exactly when every C-trajectory either reaches 1 or meets 5 or 7 mod 8. That is Conjecture 4.14 of Yolcu-Aaronson-Heule, arXiv:2105.14697 v3 (2022), Section 4.5. The authors offer a $500 reward for it, and for their Conjectures 4.11-4.13 (the single classes 1, 5 and 7).

YAH Proposition 4.15 reduces it to the convergence of the partial map

    G(n) = (3n+1)/4   if n = 1 mod 32
         = (9n+7)/8   if n = 57 mod 64
         = halt       otherwise

The conjecture holds exactly when no positive integer has an infinite G-orbit. The open question is whether some C-trajectory can avoid 5 and 7 mod 8 forever.

**Answer.** Unknown, so the status is OPEN (tier 5). Every n <= 10^6 does enter {1, 4, 2}.

## What was tried, and why each lower tier fails

1. **Tier 0.** Simulation cannot prove a universal claim.

2. **Tier 2: residue graph plus potential, as in YAH Prop. 4.7.** This method provably fails at every modulus 2^j, j >= 3. The 2-adic integer -7 has the period-5 C-orbit -7 -> -20 -> -10 -> -5 -> -14 -> -7. Its classes are 1, 4, 6, 3, 2 mod 8, none of them forbidden, and the cycle has slope 3*3/2^3 = 9/8 > 1. Reducing mod 2^j gives a cycle in the residue graph for every j:
   - (3r+1) mod 2^j is the image of an odd class;
   - r/2 + {0, 2^(j-1)} are the images of an even class, and (2^j - 20)/2 + 2^(j-1) = -10 mod 2^j.

   A strictly decreasing potential therefore cannot exist at any 2-power modulus. Check part (ii) verifies this for j = 3..64. For j <= 9 the maximum mean cycle equals log(9/8)/5 exactly, so this is the only obstruction there.

3. **Tier 1: valuation runs, as in the proofs of farkas2005 and yah_avoid15.** These do kill each individual run of the (9n+7)/8 branch. Since (9n+7)/8 + 7 = 9(n+7)/8, a run of r consecutive applications needs 8^r | n + 7, so every run is finite and has a closed form. The (3n+1)/4 branch contracts and has its fixed point at 1. The difficulty is the interleaving. An infinite G-orbit would alternate finite expanding runs (factor 9/8 each) with contracting steps (factor 3/4). This is the same mixed expanding/contracting structure as the 3x+1 problem itself.

   Heuristically G should halt: a step survives with 2-adic probability 3/64. But no method turns that heuristic into a proof. The set of 2-adic integers whose G-orbit never halts is a nonempty Cantor set, containing 1 and -7. The question is exactly whether it contains a positive integer other than 1.

4. **Tier 3-4: automata and matrix interpretations.** YAH report (Section 4.5) that their SAT-based matrix-interpretation search proved the classes 2, 3, 4, 6 and the pairs {1, 5} and {1, 7}, but not this case. I ran no SAT search myself, because z3 and SAT tooling are not installed here.

## Why it matters for the census

The pair {1, 7} is tier 1-2, but {5, 7} is open. In the solved cases, either the residue graph has no expanding cycle at all ({6} and {1, 7}, where the max mean is -0.096), or the only expanding cycle is the loop through -1. That loop's runs are finite by valuation, and in {1, 5}, {2} and {3} each exit (at 3 mod 8) is forced into a forbidden class within two steps. For {4} the exit leads into a short contracting descent; I did not write that proof out. In {5, 7}, the expanding 9/8 cycle exits into a contracting branch that can feed back into it.

The single classes {1}, {5} and {0} are also open. Their max-mean statistic, log(3/2)/2, is the same as in the solved cases {2}, {3} and {4}, so that statistic alone does not separate the tiers. What separates them is whether the exits from the expanding loops can return. The graph data are in _avoid_common.py.

## Check

check_yah_avoid57.py, about 1.7 s, verifies:

* the survey for n <= 10^6;
* the persistent 9/8 cycle mod 2^j for j <= 64;
* the max mean value for j <= 9;
* the YAH reduction to G, for every odd n = 1 mod 8 below 10^6.

It proves nothing about the question itself.

## Referee (round 2)

**Verdict: OPEN, agreed. Tier 5.**

* Source checked: YAH v3 Conj. 4.14 and Prop. 4.15. The $500 reward is stated for "any of the following conjectures", that is, 4.11-4.14. The explorer's G (1 mod 32 -> (3n+1)/4; 57 mod 64 -> (9n+7)/8) matches YAH's proof of Prop. 4.15.
  - Correction: the "Why it matters" section lists the open single classes as {1}, {5}, {0}. YAH list 0, 1, 5 and 7 as open, with 0 following from 5. The class {7} is missing from the explorer's list. The JSON entry has it right.
* Independent test: I re-checked the reduction to G on three lifts of every residue n = 1 mod 8 below 2^12. Exact behaviour: class 1 mod 32 gives (3n+1)/4, class 57 mod 64 gives (9n+7)/8, and every other class meets 5 or 7 mod 8. The proof that the 9/8 cycle through -7 persists mod 2^j is a correct one-line congruence.
* Attempt to finish: none succeeded. An infinite G-orbit interleaves the 9/8 runs (each run finite, since 8^r | n+7) with 3/4 contractions. That needs control of the 2-adic digits of an integer orbit, which is the same obstruction as 3x+1. No SAT tooling was available (z3 is absent here too).
* Referee addition (referee_avoid_graph_stats.py). Delete the 2-adic node -1 and recompute the max mean log-slope cycle mod 2^j (j = 3, 5, 7, 8).
  - All solved sets ({2}, {3}, {4}, {6}, {1,5}, {1,7}) are negative: -log 2 or -0.0959.
  - All open sets ({0}, {1}, {5}, {7}, {5,7}) are positive. For {1} it is positive only from j = 5 on; at j = 3 it is -0.0959.
  - So "max mean with the -1 loop removed" separates solved from open on this family. The plain max mean (0.2027 for {0}, {1}, {2}, {3}, {4}, {5}, {1,5}) does not.
  - This is a finite-modulus diagnostic and proves nothing about openness.
