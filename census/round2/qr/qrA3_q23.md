# qrA3_q23: basin = Legendre symbol mod 23

Rule: n even -> n/2; n odd -> (n + 23c)/3, with c in {0,1,2} the unique value making it integral (c = n mod 3).
Question: BASIN.

| Question | Answer | Status | Tier |
|---|---|---|---|
| BASIN | 23 \| n -> fixed point 23; (n/23) = +1 -> cycle (1 8 4 2); (n/23) = -1 -> cycle (5 17 21 7 10) | PROVED | 2 |

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
This is Lemma CD with q = 23 and M = {2, 3}. The table (check_qrA3_q23.py) shows that [1,23]
contains exactly three cycles: (1 8 4 2), (5 17 21 7 10) and (23). H = <2,3> mod 23 has
order 11. (Z/23)^* is cyclic of order 22, so its only subgroup of order 11 is the group of
quadratic residues, and H = QR. So the invariant of a unit is its Legendre symbol (n/23).
1 is a QR and 5 is a non-residue ((5/23) = (23/5) = (3/5) = -1), so each class holds exactly
one cycle. Multiples of 23 form the class d = 23, which holds the single cycle (23). By
Lemma CD(c), the rule holds for all n.

Why <2,3> is exactly the QR group: 23 = -1 mod 8 gives (2/23) = +1. 23 = 3 mod 4 and
23 = 2 mod 3 give (3/23) = -(23/3) = -(2/3) = +1. So both multipliers are squares; this is
the condition q = +-1 mod 24.

## Why not tier 1 (evidence, not a proof)
* T is not a conjugate of a rotation, even on the box: T(2) = T(3) = 1, and T([1,23]) has only 17 elements.
* The basin is not a function of size, sign pattern or 2- and 3-adic valuations: 1 and 5 are both odd and coprime to 6, and both are tiny, yet they reach different cycles. Each basin meets every residue class mod 2^a 3^b, by CRT with the class mod 23.
* No monotone quantity separates the cycles. The rule needs a genuine arithmetic invariant (a congruence), which is the definition of tier 2.
* Note on the rubric: it lists "quadratic-residue or coset invariants" under tier 3. Here the
  coset is read directly off n mod 23, so it is a congruence invariant plus a finite table, and
  we claim the lower tier 2. Systems qrB7_c53 and qrA3_q17 show where a coset invariant stops
  being enough.

## Referee (round 2)
Verdict: CONFIRMED. Final tier: 2 (agreed).

Re-derived Lemma CD: for n > q, (n+(m-1)q)/m < n iff n > q; for n <= q, T(n) <= q; m*T(n) = n + cq gives T(n) = m^{-1} n mod q, so gcd(n,q) and the H-coset of n/d mod q/d are invariant. Part (c) is sound: for n > q the orbit enters [1,q] at some m in the same class, and the rule is a class function (H equals the character kernel, checked exactly), so rule(n) = rule(m) = basin(m) = basin(n). The finite table is exhaustive over [1,q] (cycles_in walks every n in the box). check script re-run: exit 0. Independent test (referee scratch script, step function imported from systems.py, rule recomputed from scratch with Euler criterion / gcd, no memoisation): cycle list from all seeds < 4000 matches the claim, and the rule matches direct iteration for n in [1,30000] and [10^12, 10^12+3000] with 0 mismatches. |H| recomputed independently. 

Tier: tried to go lower. Tier 1 methods (monotonicity, valuations, conjugacy) cannot separate the cycles: the basin is a non-constant class function of n mod q that is invariant under multiplication by the multipliers, so it is not determined by size or by 2-/m-adic valuations (CRT gives n with any prescribed valuations in every class). The argument in the md is a reasonable sketch rather than a formal impossibility proof, but tier 1 is not a precisely axiomatised class and we accept it. The proof is literally "congruence invariant + descent + exhaustive finite table", which is the rubric definition of tier 2; the explorer was right not to claim tier 3 from the "QR invariant" rubric wording.
