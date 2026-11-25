# qrA3_q95: basin = Jacobi symbol (n/95), although neither Legendre factor is invariant

Rule: n even -> n/2; n odd -> (n + 95c)/3, with c in {0,1,2} minimal.
Question: BASIN.

| Question | Answer | Status | Tier |
|---|---|---|---|
| BASIN | Let d = gcd(n,95). d = 95 -> 95; d = 5 -> cycle through 5 (5 65 85 60 30 15); d = 19 -> cycle (19 38); d = 1 and Jacobi (n/95) = +1 -> cycle (1 32 16 8 4 2); d = 1 and (n/95) = -1 -> cycle through 7 (length 12) | PROVED | 2 |

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
This is Lemma CD with composite q = 95 = 5*19 and M = {2,3}.

* Classes with d = 5: u = n/5 mod 19. <2,3> mod 19 is all of (Z/19)^*, since 2 is a primitive root mod 19. So this is one class, which holds the single cycle through 5.
* Classes with d = 19: u mod 5. <2,3> = (Z/5)^*, so this is one class, holding the cycle (19 38).
* d = 95: the fixed point 95.
* Units: (Z/95)^* has order 72, and |H| = 36 (checked), so H has index 2. The Jacobi symbol J(n) = (n/5)(n/19) is a homomorphism onto {+-1} with J(2) = (-1)(-1) = 1 and J(3) = (-1)(-1) = 1. So H is contained in ker J, and both have index 2, so H = ker J. Neither Legendre symbol alone is invariant, because (2/5) = -1 and (2/19) = -1. Only their product is.

The table shows exactly one cycle per class: 5 classes and 5 cycles. Lemma CD(c) gives the rule.

So a product of primes yields a genuinely composite character. Contrast q = 1081 = 23*47,
where both primes have <2,3> = QR: there are 4 unit classes (the pair of Legendre symbols)
plus non-unit classes, 8 classes in all, but 12 cycles. That is several cycles per class, and
the situation of qrA3_q17 recurs.

## Why not tier 1
Non-injective on the box (T(2) = T(3) = 1). Units with the same valuations reach different
cycles. Tier 2.

## Referee (round 2)
Verdict: CONFIRMED. Final tier: 2 (agreed).

Re-derived Lemma CD: for n > q, (n+(m-1)q)/m < n iff n > q; for n <= q, T(n) <= q; m*T(n) = n + cq gives T(n) = m^{-1} n mod q, so gcd(n,q) and the H-coset of n/d mod q/d are invariant. Part (c) is sound: for n > q the orbit enters [1,q] at some m in the same class, and the rule is a class function (H equals the character kernel, checked exactly), so rule(n) = rule(m) = basin(m) = basin(n). The finite table is exhaustive over [1,q] (cycles_in walks every n in the box). check script re-run: exit 0. Independent test (referee scratch script, step function imported from systems.py, rule recomputed from scratch with Euler criterion / gcd, no memoisation): cycle list from all seeds < 4000 matches the claim, and the rule matches direct iteration for n in [1,30000] and [10^12, 10^12+3000] with 0 mismatches. |H| recomputed independently. Composite case re-derived: for d = 5 (resp. 19) the invariant is the coset of n/d mod 19 (resp. 5) under <2,3>; 2 is a primitive root mod 19 and mod 5, so each of these is a single class, matching the single cycles through 5 and 19. |<2,3> mod 95| = 36 = Jacobi kernel, confirmed.

Tier: tried to go lower. Tier 1 methods (monotonicity, valuations, conjugacy) cannot separate the cycles: the basin is a non-constant class function of n mod q that is invariant under multiplication by the multipliers, so it is not determined by size or by 2-/m-adic valuations (CRT gives n with any prescribed valuations in every class). The argument in the md is a reasonable sketch rather than a formal impossibility proof, but tier 1 is not a precisely axiomatised class and we accept it. The proof is literally "congruence invariant + descent + exhaustive finite table", which is the rubric definition of tier 2; the explorer was right not to claim tier 3 from the "QR invariant" rubric wording.
