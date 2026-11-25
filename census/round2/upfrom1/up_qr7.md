# up_qr7

**Rule.** even n -> n/2; n = 3 mod 28 -> n+28; every other odd n -> n+7. Seed 27.
Perturbation of the trivial "n+7" descent map (round 1 tier 1) by one trap class 3 mod 28.

**Question.** Which n have infinite orbits?

**Answer (PROVED).** Exactly the n with n = 3, 5, 6 (mod 7), i.e. the quadratic non-residues mod 7.
Every other orbit is eventually periodic: n = 0 mod 7 ends in the cycle (7 14), n = 1, 2, 4 mod 7 ends in
(1 8 4 2). Seed 27 = 6 mod 7 diverges.

## Proof
Write S for the map and g for the plain n+7 map (g(n) = n/2 even, n+7 odd); S = g off the trap class.

1. *Trap.* If n = 3 mod 28 then S(n) = n+28 = 3 mod 28 and S(n) > n, so the orbit is strictly increasing: infinite.
2. *Invariant.* Put A0 = {0}, A1 = {1,2,4}, A3 = {3,5,6} (mod 7). n+7 and n+28 fix n mod 7; for even n,
   n/2 = 4n (mod 7) and multiplication by 4 permutes each Ai (1->4->2->1, 3->5->6->3). So each Ai is S-invariant
   and g-invariant.
3. *Descent for g.* Odd n -> n+7 (even) -> (n+7)/2, and (n+7)/2 < n iff n > 7; even n -> n/2 < n. So the
   g-orbit of any n reaches [1,7]; and [1,7] is closed under these blocks (odd n <= 7 gives (n+7)/2 <= 7, with
   intermediate n+7 <= 14). Hence every g-orbit is eventually periodic, every g-cycle meets [1,7], and enumerating
   [1,14] gives exactly three g-cycles: (1 8 4 2) in A1, (3 10 5 12 6) in A3, (7 14) in A0.
4. *A0 and A1 never hit the trap* (trap class is 3 mod 7, which lies in A3). So on A0 u A1 the S-orbit is the
   g-orbit, which ends in the g-cycle of its own class by step 2: (7 14) or (1 8 4 2).
5. *Every A3 orbit is trapped.* Until it first meets 3 mod 28 the S-orbit equals the g-orbit. If it never did,
   it would be a g-orbit inside A3 forever, hence would enter the unique A3 g-cycle (3 10 5 12 6), which contains
   3 = 3 mod 28: contradiction. So it reaches the trap and is infinite by step 1.

## Tier: 2
Congruence invariant (the three orbits of x -> 4x on Z/7) + descent inequality + an exhaustive finite table of
g-cycles.

**Why not tier 1 (evidence, not a proof).** The answer is a condition mod 7 while the map's branches and the
trap are 2-adic (mod 28) conditions; valuation bookkeeping and monotonicity do not see residues mod 7, and the
trap class has density 1/28 while the divergent set has density 3/7. The finite table is load-bearing, not
decoration: moving the trap to 19 mod 28 (also 3 mod 4 and also in A3) leaves the invariant intact but 19 is
not on the A3 g-cycle, and then e.g. n = 3 escapes (check script control). So the answer depends on which
residues lie on a cycle, which only the table decides.

## Check
`check_up_qr7.py`: invariance of A0/A1/A3 over two full periods, trap invariance, block closure of [1,7], the
g-cycle list, full classification cross-check for n < 200000, and the 19-mod-28 control. PASS.

## Referee
**Verdict: CONFIRMED. Final tier: 2 (agreed).**
I re-derived every step: n/2 = 4n (mod 7), so A0, A1 and A3 are invariant. For descent, the minimum m of any g-cycle is odd and satisfies (m+7)/2 >= m, so m <= 7, and the cycle table on [1,14] is complete. The trap residue 3 mod 28 lies in A3 and in the A3 cycle. I tested independently (`referee_tests.py`): the memoized classification of every n < 10^6 matches the mod-7 rule.
Tier: the proof uses a congruence invariant, which is the definition of tier 2. I found no tier-1 route. The invariant is intrinsic, since cycles of x -> x+7, x/2 are cosets of <2> in (Z/7)*. A basin classification by residue therefore has to see mod 7, and monotonicity or valuation bookkeeping cannot. The explorer's "why not lower" is labeled as evidence, and it is evidence. The 19-mod-28 control is correct: it shows the finite table is load-bearing, though not that tier 1 is impossible.
