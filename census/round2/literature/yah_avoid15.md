# yah_avoid15: Collatz with the classes 1 and 5 mod 8 sent to 1

## Statement

The map C_K is the Collatz map C (n -> n/2 for even n, n -> 3n+1 for odd n), except that n = 1 or 5 mod 8 is sent to 1. The constant branch makes 1 a fixed point.

**Question (GLOBAL).** Does every orbit reach 1?

This holds exactly when every C-trajectory meets the classes {1, 5} mod 8. That is the residue-avoidance question of E. Yolcu, S. Aaronson, M. J. H. Heule, "An Automated Approach to the Collatz Conjecture", arXiv:2105.14697 v3 (2022), Section 4.5, for the set {1, 5}. The text after their Conjecture 4.14 says they proved "its versions with {1, 5} and {1, 7} ... both manually and automatically". They print no proof.

**Answer.** Yes. Every C-trajectory meets 1 or 5 mod 8 within finitely many steps. This is PROVED, at tier 1.

## Proof

Halving an even number never lands in a forbidden class unless the result is odd. Even n halves down to an odd o. If o = 1 or 5 mod 8, the next step goes to 1. Otherwise:

* **o = 3 mod 8.** Then 3o + 1 = 2 mod 8, which is allowed, and (3o+1)/2 = 12q + 5 for o = 8q + 3. That value is 5 mod 8 if q is even and 1 mod 8 if q is odd. Either way the next step goes to 1.
* **o = 7 mod 8.** Write o + 1 = 2^a b with a >= 3 and b odd. For j <= a-2 let o_j = 3^j 2^(a-j) b - 1. Then o_0 = o. While a - j >= 3, o_j = 7 mod 8, 3o_j + 1 = 6 mod 8 (allowed), and (3o_j + 1)/2 = o_(j+1), using (3x+1)/2 + 1 = 3(x+1)/2. At j = a-2 the value is o_(a-2) = 4 * 3^(a-2) b - 1 = 3 mod 8, and the previous case applies.

So every orbit reaches 1 in finitely many steps, and {1} is the only cycle.

## Tier and why not lower

Tier 1: a case split mod 8 plus the standard valuation run (x + 1 -> 3(x+1)/2).

Note that the residue-graph method of YAH Proposition 4.7 fails here at every modulus 2^j. Check part (iv) verifies this for j <= 64, and checks for j <= 9 that the max mean equals log(3/2)/2. The class -1 mod 2^j carries the loop 7 -> 6 -> 7 with slope 3/2, so the graph always has a cycle with mean log-slope log(3/2)/2 > 0. A pure congruence-graph certificate does not exist. The argument needs the valuation run, which is an infinite family of closed forms. This system is therefore an example where tier 1 succeeds but the more mechanical tier-2 method (graph plus potential) provably fails.

## Check

check_yah_avoid15.py verifies:

* the mod-8 facts, on residues up to 16 * 64;
* the persistent -1 loop, for every modulus 2^j with j <= 64, and the max mean for j <= 9;
* the run lemma, with exact closed forms, for every n = 7 mod 8 below 10^6;
* that every n <= 10^6 reaches 1. This last part is evidence only.

## Referee (round 2)

**Verdict: CONFIRMED, tier 1 (agreed).**

* Source checked. YAH v3, after Conj. 4.11-4.13: "we were able to prove (both manually and automatically) its versions with {1, 5} and {1, 7}". No proof is printed, as the explorer said.
* I re-derived the proof.
  - Classes 1 and 5 go straight to 1, and all even classes are allowed.
  - o = 3 mod 8 goes to 12q + 5, which is in {1, 5} mod 8.
  - o = 7 mod 8 with o + 1 = 2^a b (a >= 3): (3o+1)/2 = 3 * 2^(a-1) b - 1. This is 7 mod 8 while a - 1 >= 3, and exactly 3 mod 8 when the exponent reaches 2. The even values in between are 6 mod 8, which is allowed.
  - No case is missing.
* Independent survey: every n <= 3*10^5 reaches 1.
* why_not_lower: the claim that the graph method fails at every 2^j is a proof, not just an assertion. The -1 loop (M-1 -> M-2 -> M-1) exists for every j, by a one-line congruence.
* Referee addition: delete the node -1 mod 2^j and the max mean cycle of the remaining graph is -log 2 for j = 3, 5, 7, 8 (referee_avoid_graph_stats.py). So "accelerate the -1 runs, then apply graph plus potential" is a complete mechanical method here. It is consistent with tier 1.
