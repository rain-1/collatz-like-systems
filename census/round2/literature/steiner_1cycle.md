# steiner_1cycle: 1-cycles of the 3x+1 map (Steiner's theorem)

## Statement

The map is T(n) = n/2 for even n and (3n+1)/2 for odd n.

A **1-cycle** is a cycle with exactly one local minimum. Equivalently, it is one maximal block of k >= 1 odd terms followed by one block of l >= 1 even terms. T has no fixed points in N+, and every cycle contains both parities. A local minimum must be odd, since T(n) > n exactly when n is odd, and the term before it must be even.

**Question (CYCLES, restricted to 1-cycles).** List all 1-cycles.

**Answer.** Only (1, 2). This is PROVED, at tier 4.

**Sources.**

* R. P. Steiner, "A theorem on the Syracuse problem", Proc. 7th Manitoba Conference on Numerical Mathematics and Computing (1977), 553-559. This is the original theorem, proved with Baker's theory of linear forms in logarithms.
* Extensions: J. L. Simons, "On the nonexistence of 2-cycles for the 3x+1 problem", Math. Comp. 74 (2005), 1565-1572; J. Simons and B. de Weger, "Theoretical and computational bounds for m-cycles of the 3n+1 problem", Acta Arith. 117 (2005), 51-70, covering m <= 68; C. Hercher, "There are no Collatz m-cycles with m <= 91", J. Integer Seq. 26 (2023), Article 23.3.5, Theorem 23.
* The transcendence input used below is G. Rhin, "Approximants de Padé et mesures effectives d'irrationalité", Séminaire de Théorie des Nombres, Paris 1985-86, Progr. Math. 71, Birkhäuser (1987), 155-164. I use it in the form quoted and applied by J. L. Simons, arXiv:2205.10582 (2022), proofs of Lemmas 10 and 12: for integers u0, u1, u2 with H = max(|u1|, |u2|),

      |u0 + u1 log 2 + u2 log 3| >= H^(-13.3).

  I could not read Rhin's original. Any lower limit on H that his proposition may carry is unverified here. The exact scan below goes to H = 2 * 10^4, far past the cutoff, so it covers any small threshold.

## Proof (reproduced; the only citation needed is Rhin's bound)

**1. Reduction to a divisibility.** Let n be the odd minimum of a 1-cycle with k odd steps then l halvings. Write n + 1 = 2^k' b with b odd.

Since (3x+1)/2 + 1 = 3(x+1)/2, the odd block runs through 3^j 2^(k'-j) b - 1, and these stay odd exactly while j < k'. So k = k' and the block ends at the even number 3^k b - 1. The halving block then needs 3^k b - 1 = 2^l n with n odd.

Substituting n = 2^k b - 1 gives

    b (2^(k+l) - 3^k) = 2^l - 1.

Conversely, every pair k, l >= 1 with d = 2^(k+l) - 3^k > 0 and d | 2^l - 1 gives a 1-cycle with b = (2^l - 1)/d (odd, because d is odd). So 1-cycles correspond exactly to such pairs (k, l).

**2. The pair must be a very good approximation.** From 0 < d <= 2^l - 1 < 2^l we get 2^l (2^k - 1) < 3^k. Put u = 2^l / 3^k. Then:

* u < 1/(2^k - 1) <= 2^(1-k);
* 2^l < 2 (3/2)^k, so l <= k and H := k + l <= 2k;
* Lambda := (k+l) log 2 - k log 3 = log(2^(k+l) / 3^k) < log(1 + u) < u.

So 0 < Lambda < 2^(1-k).

**3. Transcendence bound.** Rhin's bound with u0 = 0, u1 = k + l, u2 = -k gives Lambda >= (k+l)^(-13.3) >= (2k)^(-13.3). Then 2^(1-k) > (2k)^(-13.3), that is, (k-1) log 2 < 13.3 log(2k). This forces k <= 103.

**4. Finite check.** For each k, l is forced to be the least l with 2^(k+l) > 3^k. The next one fails: 2^(l+1)(2^k - 1) >= 2^(k+l) > 3^k. An exact scan of every k <= 10000 finds that d < 2^l and d | 2^l - 1 hold only for (k, l) = (1, 1). That pair gives d = 1, b = 1, n = 1, the cycle (1, 2).

## Tier and why not lower

Tier 4: the proof needs an effective irrationality measure for log 3 / log 2 (Rhin, or Baker as in Steiner's paper) plus a finite computation.

Why tier 3 and below fail (evidence, not a proof):

* The obstruction is an exponentially good rational approximation, |(k+l) - k log2(3)| < 2^(1-k) / log 2.
* No congruence argument can rule this out uniformly. For each fixed modulus M, the divisibility d | 2^l - 1 is a condition on (k, l) mod the orders of 2 and 3 mod M, and some residue pair satisfies it.
* Elementary methods (continued fractions alone) give the convergents but no lower bound for |q alpha - p| in terms of q. Every known effective bound for this linear form goes through Baker's theory or Padé approximants (Rhin).
* The finite scan alone is tier 0 evidence and cannot cover all k.

## Check

check_steiner_1cycle.py, about 1.5 s:

* exact scan of k <= 10^4, finding only (1, 1);
* confirms that the Rhin cutoff is 103;
* direct search: the only T-cycle with odd minimum <= 10^6 is {1, 2}.

## Referee (round 2)

**Verdict: CONFIRMED, tier 4 (agreed).**

* I re-derived each step.
  - The odd run: x+1 -> 3(x+1)/2.
  - The cycle equation b(2^(k+l) - 3^k) = 2^l - 1, and its converse: b is odd, so v2(n+1) = k, and n is odd, so v2(3^k b - 1) = l.
  - The bounds l <= k and 0 < Lambda < 2^(1-k).
  - The Rhin cutoff k <= 103.
  - The claim that only the least l can work: for l+1, 2^(l+1)(2^k - 1) >= 2^(k+l) > 3^k.
* Rhin's statement is quoted from a secondary source, arXiv:2502.00948: |u0 + u1 log2 + u2 log3| >= H^(-13.3) for H = max(|u1|, |u2|) >= 2. So the threshold is H >= 2, which the explorer's scan covers many times over. Simons arXiv:2205.10582 applies the same "proposition on p. 160" of Rhin.
* Independent scan: every k <= 3000 and every 1 <= l <= k+2 with d > 0 and d | 2^l - 1. Only (1, 1) appears.
* Lower tier attempted. From d | 2^l - 1 it follows that d | 3^k - 2^k, which gives 3^k - 2^k = n d. This is an identity, not a contradiction.
  - arXiv:1805.10496 ("A Dual-Radix Approach to Steiner's 1-Cycle Theorem") gives "algebraic" proofs. The abstract's unconditional result is only for the 3x-1 system "under an exponential upper bound on the iterates", so it does not remove the transcendence input here.
  - The why_not_lower argument is evidence, not a proof. A tier-3 lower bound would itself be an effective irrationality measure for log2(3) by elementary means, which is not known. Tier 4 stands.

## Constants audit (26 Nov 2026)
The linear-forms constant quoted above is superseded. VERIFIED: with Laurent 2008 the cutoff is k < 3997, inside the existing scan. The result now depends only on M. Laurent, Acta Arith. 133 (2008), Corollary 2, read in the primary source. See census/advance/constants-audit/theorem.md.
