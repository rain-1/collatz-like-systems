# Theorem F: trap sets that work for whole congruence families of maps

Status: **PROVED**. The finite content (the type-F property of each listed set) is checked in
`check.py` [4], on brute-force graphs. Novelty: for a = 3, b = 1 and A = {4} this is one of the
classes YAH report as proved (as transcribed in census/round2/literature/yah_avoid57.md). I have
not checked whether the general family statements are new.

## Statement

Let C_{a,b}(n) = n/2 for even n and a n + b for odd n, where a and b are odd and ≥ 1. Fix k and a
set A of residues mod 2^k. In the avoider graph G_k^A of C_{a,b}:

* odd r has the single edge r → (a r + b) mod 2^k;
* even r has the edges r → r/2 and r → r/2 + 2^{k−1};
* nodes in A are deleted.

So the graph depends only on a0 = a mod 2^k and b0 = b mod 2^k. Call (a0, b0, A) of **type F**
if every SCC of this graph is trivial or a single simple cycle.

**Theorem F.** Let (a0, b0, A) be of type F. Then for **every** odd a ≥ 1 and odd b ≥ 1 with
a ≡ a0 and b ≡ b0 (mod 2^k), every positive orbit of C_{a,b} meets A, or ends in a cycle through
a positive integer of the form

    x*_C(a, b) = c_C(a, b) / (2^{E_C} − a^{o_C}),

where C is a simple component with o_C odd steps and E_C halvings, and c_C is the composed
additive constant. Such a positive integer can exist only when a^{o_C} < 2^{E_C}.

*Proof.* This is Theorem 2 of theory.md with no contracting component. Every avoiding orbit
eventually stays in a simple component, and its tail is then exactly the lift x*_C (Lemma 0).
When a^{o_C} > 2^{E_C} the lift is expanding, and an expanding lift cannot be a positive integer
(theory.md, Theorem 2). No potential and no simulation are needed, so nothing depends on the
size of a or b. ∎

## Explicit corollaries (checked)

The enumeration (`family.py`) gives the following.

**Mod 8, all residues.** For every class (a0, b0), the minimal type-F sets include **{4}**. There
are 8 minimal type-F sets per class. Two of them are singletons: {4} and {2}, or {4} and {6},
depending on (a0, b0).

**Mod 8, odd residues.** Every class (a0, b0) has exactly **two** minimal odd type-F pairs:

| (a0,b0) | pairs | (a0,b0) | pairs |
|---|---|---|---|
| 1,1 | {3,7} {5,7} | 5,1 | {1,3} {3,7} |
| 1,3 | {1,5} {5,7} | 5,3 | {1,3} {1,5} |
| 1,5 | {1,3} {3,7} | 5,5 | {3,7} {5,7} |
| 1,7 | {1,3} {1,5} | 5,7 | {1,5} {5,7} |
| 3,1 | {1,5} {3,5} | 7,1 | {1,5} {1,7} |
| 3,3 | {1,7} {3,7} | 7,3 | {3,5} {3,7} |
| 3,5 | {1,5} {1,7} | 7,5 | {1,5} {3,5} |
| 3,7 | {3,5} {3,7} | 7,7 | {1,7} {3,7} |

**Mod 16, odd residues.** Every class has 6 minimal odd type-F sets, all triples or quadruples.
They are listed in `results/family_k4_odd.json`.

**Exceptions.** In all of these sets, every simple cycle with an odd step has a^o < 2^E only for
a ≤ 3 (mod 8) or a ≤ 7 (mod 16), because the largest threshold 2^{E/o} is 4 and 8 respectively.
Precisely: every simple cycle of every minimal odd type-F set has E ≤ 2o (mod 8) or E ≤ 3o
(mod 16), where o is the number of odd steps and E the number of halvings. Then for a ≥ 5 we get
a^o ≥ 5^o > 4^o ≥ 2^E, and for a ≥ 9 we get a^o ≥ 9^o > 8^o ≥ 2^E, so no lift is a positive
integer. Cycles with o = 0 are all-halving loops with lift 0, so they are harmless. This finite
fact is checked exactly in `check.py` [4], for every class mod 8 and mod 16 (added after
refereeing; before that, only the simulation for a < 60 tested it, which is EVIDENCE). This
gives the following uniform statements.

* **Corollary F1.** For all odd a ≥ 3 and odd b ≥ 1, every positive orbit of n ↦ n/2 | a n + b
  contains a term ≡ 4 (mod 8).
  * a = 3 is included. The lift has o = 1, E = 1, multiplier 3/2 > 1.
  * For a = 1 the only exception is the cycle (b, 2b).
  * Hand proof. If an odd n has v_2(a n + b) ≥ 2, the halving chain passes through 4·odd ≡ 4
    (mod 8). Otherwise the next odd value is (a n + b)/2. Put x* = −b/(a − 2). Then
    (a n + b)/2 − x* = (a/2)(n − x*), so the 2-adic valuation of n − x* drops by one at each such
    step, and such steps cannot continue forever (n ≠ x*). Tier 1.
* **Corollary F2.** For odd a ≥ 5 and odd b ≥ 1, every positive orbit of C_{a,b} meets both
  odd pairs listed for (a mod 8, b mod 8). There are no exceptions. For example:
  * every 5x+1 trajectory contains a term ≡ 1 or 3 (mod 8), and one ≡ 3 or 7 (mod 8);
  * every 7x+1 trajectory contains a term ≡ 1 or 5, and one ≡ 1 or 7 (mod 8).
* **Corollary F3.** For odd a ≥ 9 and odd b ≥ 1, the same holds for each of the 6 minimal sets
  mod 16 of the class (a mod 16, b mod 16).

The 3x+1 instances (a = 3): {4}, {3,5} and {1,5} are consistent with YAH (classes 4 and {1,5}
proved there). {3,5} holds with the trivial cycle (1 4 2) as the only exception: it is the lift
with o = 1, E = 2, multiplier 3/4.

## What this does not give

Type F is the case without contracting components. As soon as a contracting component is
needed (for example 7x+1 with A = {5,7} mod 8; see trap7_57.md), the conclusion depends on the
size of a, through the potential. That trap set is certifiable for a = 7 only when its cycles
contract, which needs a^o < 2^E. So it is not a family statement.

## Check

`check.py` [4] does the following:

* recomputes the type-F minimal sets mod 8 and mod 16 on independently built brute-force
  graphs;
* checks exactly, on the same brute-force graphs, that every simple cycle of every minimal odd
  type-F set has E ≤ 2o (mod 8) or E ≤ 3o (mod 16); this is the finite content of the
  "no exceptions" claims of F2 and F3;
* for every (a0, b0) mod 8, each odd pair and {4}, and all a < 60 and b < 40 in the class,
  simulates n < 400. Each orbit that ends in a cycle avoiding A must contain an exact
  positive-integer lift. This part (718200 orbits) is EVIDENCE only.
