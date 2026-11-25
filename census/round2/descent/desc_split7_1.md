# desc_split7_1

**Rule.** Even n → n/2; n ≡ 1 (mod 4) → 7n+1; n ≡ 3 (mod 4) → n+1. This is SPLIT(7,1,1).
**Question (GLOBAL).** Is every positive orbit eventually periodic?
**Status.** OPEN. Tier 5.

## What is proved

**Proposition.** No descent certificate exists, for any modulus M and any number of steps k.

*Proof.* Work in Z_2. First, −1/3 ≡ 1 (mod 4), since 3^{-1} ≡ 3 and −3 ≡ 1. The orbit is

  −1/3 → 7(−1/3)+1 = −4/3 → −2/3 → −1/3.

Here −4/3 ≡ 0 (mod 4) and −2/3 ≡ 2 (mod 4), so both halvings are legal. The step multipliers are 7, 1/2 and 1/2. Starting at −1/3 the partial products are 7, 7/2 and 7/4, all greater than 1, and the product over one period is 7/4. Lemma B (lemmas.md) therefore rules out every certificate. ∎

The same holds for the whole family. By Theorem 1 of lemmas.md, SPLIT(a,b,d) has a certificate only for (a,b) ∈ {(1,1), (3,1), (1,3)} with the right d mod 4, and then a single block (k ≤ 3) works. With d = 1 and a ≡ 3 (mod 4), the frontier lies between a = 3 (certifiable, tier 1) and a = 7, which is this system. The SPLIT family has no tier-2 member at all, which explains why round 1 found the split maps only at tier 1 or tier 5.

## Evidence (not proof)

* In the random model the expected log change per odd step is −1.106, so orbits are strongly contracting on average.
* Every n ≤ 10^5 reaches the cycle through 1, (1 → 8 → 4 → 2 → 1).

## Why lower tiers fail

* **Tier 2 (descent with a finite table):** impossible, as proved above. The obstruction is a 2-adic point, so neither a larger modulus nor more steps can help.
* **Tier 2 (congruence invariants):** these can only separate basins. They cannot prove that orbits converge, and the expected answer is "yes".
* **Tier 3:** I found no automaton or closed-form structure. Points close to −1/3 run through long stretches of ×7/4 per block, as in Collatz near −1. This is the same mixed expanding/contracting obstruction as split5 in round 1.

## Check

`check_desc_split7_1.py` verifies the obstruction exactly. It also checks Theorem 1 on 1024 (a,b,d) triples, for each one either verifying a certificate or verifying an obstruction. The drift and the simulation are reported as evidence only.

## Referee

**Verdict: OPEN (agreed). Final tier 5. The no-certificate proposition is confirmed.**

* I re-derived the obstruction with exact Fractions directly from the residue table in systems.py (`referee_check.py`, part 4). −1/3 lies on the residues 1, 0, 2 mod 4 with period 3 and multiplier 7/4, and the partial products from −1/3 are 7, 7/2, 7/4, all greater than 1. Lemma B is correct. The CRT step is sound, and since every partial product exceeds 1 it also rules out the weaker certificate form "some j ≤ k works for each n".
* Lemma B also rules out residue-weighted potentials V(n) = n·c(n mod M). Integers that shadow −1/3 for j periods satisfy V(T^{3j} n)/V(n) ≥ (7/4)^j·(c_min/c_max) − o(1), so V cannot decrease uniformly. So the one-step potential method that I used to shorten desc_s32_max (below) does not apply here either.
* Theorem 1 (SPLIT family): I checked the proof line by line. The exactness of v_a and v_b, and x ≡ 1 or 3 (mod 4) for the fixed point, are both correct.
* Simulation: all n < 2·10^5 reach the 4-cycle (1, 8, 4, 2). This is evidence only.
* Tier 3 is not excluded by a proof, only by an unsuccessful search. That is the normal state for a Collatz-type map with mixed ×7/4 and contracting blocks, so tier 5 stands.
