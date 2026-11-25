# auto_sfx7_s17

**Map.** Binary suffix permutation (replace the final word on the left by the one on the right):

| input suffix | 00 | 001 | 00101 | 10 | 10101 | 11 | 1101 |
|---|---|---|---|---|---|---|---|
| output suffix | 00 | 100110 | 1110 | 1 | 10110 | 010 | 000110 |

Arithmetic form: 4q→4q, 8q+1→64q+38, 32q+5→16q+14, 4q+2→2q+1, 32q+21→32q+22, 4q+3→8q+2, 16q+13→64q+6 (q ≥ 0). Both rows are complete suffix codes, and zero maps to zero, so T permutes the positive integers.

**Question.** FATE of 17.

**Answer.** Infinite. **Status:** PROVED. **Tier:** 2.

## Orbit

17, 166, 83, 162, 81, 678, 339, 674, 337, 2726, ... Forward in time the orbit rises, falls, rises, falls in every 4-step period. Backward in time it is 17, 34, 19, 38, 1, 2, 3, 6, 13, 26, 15, 30, 37, 74, 39, 78, 133, ..., which again goes up, down, up, up in every period. Neither direction is eventually monotone.

## Proof 1 (tier 2: a congruence invariant)

Let A = {81, 83, 162, 166, 209, 211} (mod 256). Every input modulus divides 64, so for n ≡ r (mod 256) the branch is fixed by r. Also T(n) mod 256 is determined by n mod 256·64. Checking the 6·64 representatives r + 256t, 0 ≤ t < 64, shows that T maps each class of A into A (check part 3). Since 17 ∉ A and T(17) = 166 ∈ A, induction puts every T^n(17), n ≥ 1, in A, so none equals 17. T is injective, so a repeat T^i(17) = T^j(17) with i < j would force T^(j-i)(17) = 17. The orbit is therefore infinite.

**Exact least modulus.** For every M < 256 the residue graph mod M (edges r → T(n) mod M) has a path from the class of T(17) to the class of 17. This is an exhaustive computation over all M, using inputs 1..64M, which cover every residue mod 64M (check part 4). So no union of residue classes mod M < 256 is a certificate. The least such modulus is exactly 256.

## Proof 2 (tier 3: explicit closed formula)

The rules read at most 6 final bits. For any binary word X: X·10011 → X·100010 → X·10001 → X·10100110 → X10·10011. Each step matches a suffix lying in the displayed part (check part 2, symbolic). With 83 = [10·10011], we get T^(2+4k+r)(17) = [10 (10)^k U_r] for k ≥ 0, with U = (10011, 100010, 10001, 10100110). The values are unbounded, so the orbit is not eventually periodic.

## Automaton size (the lens measurement)

* An explicit **5-state** binary certificate (δ = [[1,1],[2,0],[3,3],[1,4],[4,0]], accept {4}) is verified exactly. The verification runs a closure test over all integers, using a reversed-subset automaton synchronised with the affine branches least-significant digit first (autolib.closure_violation).
* **No certificate has ≤ 4 states.** A complete backtracking search over all transition tables finds none (check part 5). The search uses only necessary constraints, and an exact closure test rejects every surviving table. SAT (pysat, exact encoding of closure on all reachable states) agrees: the minimum is 5.
* The minimal DFA of the mod-256 congruence certificate has 10 states. So the smallest certificate is **not periodic**: the automaton is a compression of the congruence argument, not a stronger argument.

## Why lower tiers fail

* Tier 0: the claim is infinite, so simulation cannot prove it.
* Tier 1 (evidence, not proof): the orbit is not eventually monotone in either time direction, so neither forward nor backward monotonicity applies. No 2-adic valuation is conserved: valuations along the period are 0,1,0,1. No congruence with modulus < 256 works (proved, part 4), which rules out every one-line parity or small-modulus bookkeeping argument.
* Tier 2 holds: a 6-class invariant mod 256, found by an exhaustive residue table.

## Theorem (tier collapse for suffix permutations), proved here

*Let T be a binary suffix permutation (finite table, input and output suffix sets each complete, 0 ↦ 0) and let s have an infinite orbit. Then some union of residue classes modulo a power of 2, together with a finite set, is a forward-closed certificate that separates s from T(s).*

*Proof.* By the suffix orbit theorem (output/pdf/suffix_orbit_theorem.pdf, reproved there by a pumping argument), T^(i+kp+r)(s) = [P V^k U_r]_2 for k ≥ 0 and 0 ≤ r < p, with V nonempty. Extend T to the 2-adic integers Z_2 by the same rules. Write [c]_e for the cylinder of 2-adic integers agreeing with c in the last e bits. If e is at least the longest input suffix, a rule a → b sends [c]_e exactly onto [T(c)]_(e+|b|-|a|), since 2^|a| q + a ↦ 2^|b| q + b. Let ω_r ∈ Z_2 be the limit of P V^k U_r as k → ∞, the left-infinite word …VVVU_r. By continuity T(ω_r) = ω_(r+1) for r < p-1, and T(ω_(p-1)) = ω_0. Set e_0 = E and e_(r+1) = e_r + |b_r| - |a_r| along the rules used in one period. The total change over a period is |V| ≥ 1. Choose E so large that every e_r is at least the longest input suffix. Then U = ∪_r [ω_r]_(e_r) satisfies T([ω_r]_(e_r)) = [ω_(r+1)]_(e_(r+1)) for r < p-1, and T([ω_(p-1)]_(e_(p-1))) = [ω_0]_(E+|V|) ⊆ [ω_0]_E. Hence T(U) ⊆ U, and U ∩ N is a union of classes mod 2^(max e_r) closed under T. The orbit points P V^k U_r lie in U once k is large, say from time t_0 on. Then C = (U ∩ N) ∪ {T(s), …, T^(t_0-1)(s)} is forward closed. The points ω_r are T-periodic and s is not, so s ≠ ω_r, and s ∉ U once E is large. Also s is not among its own later iterates. □

**Consequence.** Every FATE question for a binary suffix permutation is decided, and has a proof of tier ≤ 2: either a finite cycle by simulation, or a congruence-plus-finite-table certificate. The pump witness computes the certificate explicitly. The same proof works in any base b, and for any residue-class map whose slopes are powers of b and whose orbit converges b-adically to a periodic cycle with net contraction. For this seed the finite part is empty and E = 8. Here the 2-adic attracting cycle is ω = …101010·U_r, and A consists of its windows.

## Referee

**Verdict:** the answer is CONFIRMED (infinite orbit). The tier is LOWERED from 2 to **1**.

**What I re-derived.** I checked bijectivity, the 6-class mod-256 table (with my own string-level rewriter), the M < 256 exhaustion (inputs 1..64M cover every residue mod 64M, and the largest input modulus is 64, so the table is complete), and the 5-state certificate (also checked numerically up to 2^20). I re-proved "no certificate with ≤ 4 states" by an independent brute force over all binary DFA tables with ≤ 4 states, using only necessary constraints (referee_check.py, R6). The SAT claim cannot be reproduced here because pysat is not installed. The pure-Python backtracking and my brute force already settle the ≤ 4 bound, so the minimum of exactly 5 stands.

**Tier-1 proof.** For every word X, the rules read only the displayed bits:
X·10011 → X·100010 → X·10001 → X·10100110 → X·10·10011.
Numerically, T^4(32X+19) = 128X+83 = 4n+7 for every n ≡ 19 (mod 32), and 4n+7 ≡ 19 (mod 32) again. Also T^2(17) = 83 ≡ 19 (mod 32). So T^(2+4k)(17) = (256·4^k − 7)/3. This is strictly increasing, so the orbit is unbounded and therefore infinite (no injectivity argument needed). It is a single affine branch of T^4 on one cylinder, the same kind of argument the lens itself rates tier 1 for auto_mix3_s7 (T(9·2^(k+1)) = 9·2^k).

The md's "Proof 2" labels this closed form tier 3, as an "explicit closed formula for a non-monotone orbit". But the formula needs only one 4-step affine identity, and the subsequence it gives is monotone. That is monotonicity plus valuation bookkeeping, which is tier 1.

**On why_not_lower.** "The orbit is not eventually monotone" is true, but it does not rule out tier 1: a monotone subsequence is enough. "No modulus < 256 is a certificate for T" is proved, but it only rules out congruence certificates for T itself. The class 19 mod 32 is invariant under T^4, not under T. So the least-modulus statement does not measure difficulty.

**On the tier-collapse theorem.** The proof is correct, given the cited suffix-orbit theorem (output/pdf/suffix_orbit_theorem.pdf, whose pump argument I read and find sound). Its conclusion can be sharpened. The pump witness gives T^p(2^W X + a) = 2^(W+|V|) X + [VA] for every X ≥ 1, which is strictly greater than 2^W X + a. So every infinite orbit of a binary suffix permutation is settled at **tier 1**, plus a finite search for the witness, not tier 2.

**Final tier: 1.**
