# trap5_hi16: 5x+1 with the odd classes 9, 11, 13, 15 (mod 16) as a trap

**System.** T(n) = 1 if n mod 16 ∈ {9, 11, 13, 15}. Otherwise T(n) = n/2 for even n and 5n + 1 for
odd n.

**Question (GLOBAL).** Is every orbit eventually periodic, and what are the cycles? Equivalently:
does every 5x+1 trajectory meet {9, 11, 13, 15} (mod 16) or reach 1?

**Answer.** Yes. Every 5x+1 trajectory meets an odd term ≡ 9, 11, 13 or 15 (mod 16), or ends in
the cycle (1 6 3 16 8 4 2). The 13-cycle and the 17-cycle are trapped, because 13 and 43 ≡ 11
(mod 16) lie in A. **PROVED**, tier 2. The proof uses a weighted potential with a near-critical
cycle of multiplier 125/128. Novelty not checked.

## Proof (by hand)

The trap classes are odd. Follow the odd terms, and let N(n) = (5n + 1)/2^v denote the next odd
term after the odd term n. For an untrapped odd n, n mod 16 ∈ {1, 3, 5, 7}. From the table of
transitions, verified exhaustively in check.py:

| n mod 16 | v | N mod 16 |
|---|---|---|
| 1 | 1 | 3 or 11 |
| 3 | ≥ 4 | anything |
| 5 | 1 | 5 or 13 |
| 7 | 2 | 1, 5, 9 or 13 |

**Class 5 is a dead end.** From n ≡ 5, the run N = (5n + 1)/2 satisfies
3N + 1 = (5/2)(3n + 1). So it is finite, and it can only exit to 13 (mod 16), which is trapped.
Hence an untrapped orbit never visits the class 5. Its odd terms then follow the graph
1 → 3, 3 → {1, 3, 7}, 7 → 1, with N ≤ (5n + 1)/2, (5n + 1)/16 and (5n + 1)/4 respectively.

**Potential.** Put V(n) = w(n mod 16)·n with w(1) = 63/25, w(3) = 1, w(7) = 79/25. For n ≥ 64 the
ratio V(N)/V(n) along each edge is bounded as follows (all inequalities exact):

| edge | bound on V(N)/V(n) | numerically |
|---|---|---|
| 1 → 3 | (5 + 1/n)/(2·63/25) | ≤ 0.9952 |
| 3 → 1 | (63/25)(5 + 1/n)/16 | ≤ 0.79 |
| 3 → 3 | (5 + 1/n)/16 | ≤ 0.32 |
| 3 → 7 | (79/25)(5 + 1/n)/16 | ≤ 0.9906 |
| 7 → 1 | (63/25)(5 + 1/n)/(4·79/25) | ≤ 0.99997 |

So V shrinks by a factor at most κ < 1 at each odd step taken from a term ≥ 64. V ≥ n, so an
untrapped orbit cannot stay ≥ 64 forever. Every untrapped orbit therefore has an odd term ≤ 63.
Finally, every n ≤ 64 either meets A or reaches 1 (finite check). ∎

The weights are forced to be tight: the cycle 3 → 7 → 1 → 3 has multiplier
(5/16)(5/4)(5/2) = 125/128. It is the 2-adic shadow of the trivial cycle's neighbourhood: the
lift of the residue cycle is 848/3.

**Machine certificate (Theorem 2, independent of the hand proof).**
* Level 4, B = 295.
* Simple component (5, 10) with lift −1/3, multiplier 5/2.
* Contracting component {0,1,2,3,4,6,7,8,12,14} with Q = 1024 and P_5 = 2378.

**Check.** `check.py` [5] verifies:
* the transition table, for all odd n < 2^16;
* the potential inequalities, exactly with Fractions at n = 64 and in the limit, together with
  monotonicity in n;
* the finite check for n ≤ 64;
* the machine certificate.
