# qrC_q311: three multipliers <2,3,5>, basin = Legendre symbol mod 311

Rule: n even -> n/2; n = 1 mod 4 -> (n + 311c)/3; n = 3 mod 4 -> (n + 311c)/5; in each case c is the minimal value in [0, m-1] making the division exact.
Question: BASIN.

| Question | Answer | Status | Tier |
|---|---|---|---|
| BASIN | 311 \| n -> 311; (n/311) = +1 -> cycle through 3 (length 13); (n/311) = -1 -> cycle through 11 (length 16) | PROVED | 2 |

## Lemma CD (coset descent), used verbatim by every tier-2 system of this lens

Let q >= 3 be odd. For each n, a multiplier m = m(n) >= 2 with gcd(m, q) = 1 is chosen by any
rule, and T(n) = (n + c*q)/m, where c in {0, ..., m-1} is the unique value with m | n + c*q.

(a) Descent into a box. T(n) >= 1. If n <= q then T(n) <= (q + (m-1)q)/m = q. If n > q then
    T(n) <= (n + (m-1)q)/m < n. So every orbit strictly decreases until it enters [1, q], and
    [1, q] is forward invariant. Every cycle meets [1, q] and therefore lies inside it. So the
    complete cycle list is a finite computation on [1, q].
(b) Invariant. m*T(n) = n + c*q, so T(n) = m^{-1} n (mod q). Hence d = gcd(n, q) is invariant.
    Writing n = d*u, the class of u mod q/d changes only by multiplication by elements of
    H = <M> (reduced mod q/d), where M is the multiplier set. The class
    K(n) = (d, coset of u in (Z/(q/d))^* / H) is therefore invariant along orbits.
(c) Every class K occurs among the residues 1..q, so it occurs in [1, q]. If the finite table
    shows exactly one cycle in each class, then by (a) and (b) every n reaches the unique cycle
    of class K(n). That is a complete proof of the BASIN rule for all n.

The check script verifies the finite part of (a) and (c): that the box is invariant, the cycle
list, one cycle per class, H equal to the claimed character kernel, and that the rule agrees
on the box. It also runs a sanity simulation, which is not part of the proof.

## Proof
This is Lemma CD with q = 311 and M = {2,3,5}. The multiplier is chosen by n mod 4, and the
lemma allows any selection rule. The three multipliers are quadratic residues:

* (2/311) = +1 because 311 = 7 mod 8.
* (3/311) = -(311/3) = -(2/3) = +1.
* (5/311) = (311/5) = (1/5) = +1.

|<2,3,5>| = 155 (checked), so H = QR. 3 is a QR and 11 is a non-residue (checked via
Euler's criterion). The table finds exactly the cycles through 3 and 11 and the fixed point
311. Lemma CD(c) gives the rule.

The search covered q < 700 with gcd(q,15) = 1. For this map, index >= 2 with one cycle per
class occurs first at 311 (index 2) and at 643 (index 3, cubic).

## Why not tier 1
Non-injective on the box (T(1) = T(208) = 104). The cycles are separated only by a
congruence invariant. Tier 2.

## Referee (round 2)
Verdict: CONFIRMED. Final tier: 2 (agreed).

Re-derived Lemma CD: for n > q, (n+(m-1)q)/m < n iff n > q; for n <= q, T(n) <= q; m*T(n) = n + cq gives T(n) = m^{-1} n mod q, so gcd(n,q) and the H-coset of n/d mod q/d are invariant. Part (c) is sound: for n > q the orbit enters [1,q] at some m in the same class, and the rule is a class function (H equals the character kernel, checked exactly), so rule(n) = rule(m) = basin(m) = basin(n). The finite table is exhaustive over [1,q] (cycles_in walks every n in the box). check script re-run: exit 0. Independent test (referee scratch script, step function imported from systems.py, rule recomputed from scratch with Euler criterion / gcd, no memoisation): cycle list from all seeds < 4000 matches the claim, and the rule matches direct iteration for n in [1,30000] and [10^12, 10^12+3000] with 0 mismatches. |H| recomputed independently. Lemma CD allows a multiplier chosen by n mod 4; descent for both branches (n+2q)/3 < n and (n+4q)/5 < n iff n > q verified. |<2,3,5>| = 155 confirmed.

Tier: tried to go lower. Tier 1 methods (monotonicity, valuations, conjugacy) cannot separate the cycles: the basin is a non-constant class function of n mod q that is invariant under multiplication by the multipliers, so it is not determined by size or by 2-/m-adic valuations (CRT gives n with any prescribed valuations in every class). The argument in the md is a reasonable sketch rather than a formal impossibility proof, but tier 1 is not a precisely axiomatised class and we accept it. The proof is literally "congruence invariant + descent + exhaustive finite table", which is the rubric definition of tier 2; the explorer was right not to claim tier 3 from the "QR invariant" rubric wording.
