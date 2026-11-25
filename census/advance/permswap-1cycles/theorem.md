# permswap-1cycles: the 1-cycles of perm_swap S (CLS-047)

**Status: PROVED.** The proof is complete. It uses one literature constant, Laurent's two-log bound (2008). I consulted that bound in the form restated verbatim by Bennett–Patel–Siksek (details below), but not in Laurent's original paper. It also uses an exact finite computation (`check.py`).

## The map

S(3q) = 2q, S(3q+1) = 4q+3, S(3q+2) = 4q+1. This is a bijection of Z_{>0}, and S(5y) = 5T(y), where T is Collatz's 1932 map T(3q) = 2q, T(3q+1) = 4q+1, T(3q+2) = 4q+3.

**Branch formulas.**

    S(x) = 2x/3          if x ≡ 0 (mod 3)
    S(x) = (4x + 5)/3    if x ≡ 1 (mod 3)
    S(x) = (4x - 5)/3    if x ≡ 2 (mod 3)

To check these: x = 3q+1 gives (12q+9)/3 = 4q+3, and x = 3q+2 gives (12q+3)/3 = 4q+1. So off the multiples of 3, S(x) = (4x + 5δ)/3 with δ = ±1. The inhomogeneous terms are ±5, as the task said.

**Consequences.**

- On a non-multiple of 3, S(x) > x if and only if x > 5. The only exceptions are S(2) = 1 < 2 and the fixed point S(5) = 5. (Only the minus branch matters here, and (4x-5)/3 > x iff x > 5.)
- On a multiple of 3, S(x) = 2x/3 < x.
- S preserves 5-divisibility (CLS-047.md, Step 0). Also, 3 | 5y iff 3 | y. So y ↦ 5y conjugates T to S|_{5Z} and preserves the "multiple of 3" pattern.

## Definition

Call an element of a cycle an *ascent* if it is not a multiple of 3, and a *descent* if it is.

A **1-cycle** is a cycle whose cyclic sequence contains at most one maximal block of descents. Equivalently, it is one block of k ≥ 1 ascents followed by one block of l ≥ 0 descents. This is the same convention as perm1932_1cycle.md.

This agrees with "exactly one local minimum" (a local minimum being x_{i-1} > x_i < x_{i+1}) for every cycle that avoids {2, 5}. On such a cycle, the step at x_i goes up exactly when x_i is an ascent, so the local minima are exactly the first elements of the ascent blocks. The only cycles through 2 or 5 are (1, 3, 2) and (5). The cycle (1, 3, 2) has one local minimum (namely 1) and one block, so it qualifies under both definitions. The fixed point (5) is the degenerate case l = 0.

## Theorem

The 1-cycles of S are exactly the following five.

| Cycle | Relation to 5Z | (k, l, e) | x_0 = 2^l e |
|---|---|---|---|
| (5) | in 5Z, equals 5·(1) | l = 0 | |
| (10, 15) | in 5Z, equals 5·(2, 3) | (1, 1, 5) | |
| (20, 25, 35, 45, 30) | in 5Z, equals 5·(4, 5, 7, 9, 6) | (3, 2, 5) | |
| (1, 3, 2) | coprime to 5; as a block it is 2 → 1 → 3 | (2, 1, 1) | 2 |
| (14, 17, 21) | coprime to 5 | (2, 1, 7) | 14 |

The three cycles inside 5Z are exactly 5× the 1-cycles (1), (2, 3), (4, 5, 7, 9, 6) of the 1932 map T. So this theorem independently reproves perm1932_1cycle.md, using Laurent's bound in place of Rhin's.

The cycles coprime to 5 are exactly (1, 3, 2) and (14, 17, 21). These are new 1-cycles that do not come from T.

For comparison, the other cycles of S with minimum below 10^5 have more than one block:

- the 11-cycle through 4 (2 blocks);
- the 34-cycle through 16 (8 blocks);
- the 12-cycle through 220 = 5·44 (4 blocks; this is 5× T's 44-cycle).

## Proof

**Step 1 (l = 0).** Suppose every element of the cycle is a non-multiple of 3. Let M be its maximum. Then S(M) ≤ M, so M ∈ {2, 5}. M = 2 is impossible, since S(2) = 1 and S(1) = 3 is a multiple of 3. So the cycle is (5).

A block of descents alone cannot form a cycle, because descents strictly decrease. So from now on k ≥ 1 and l ≥ 1.

**Step 2 (shape).** Rotate the cycle so that x_0, ..., x_{k-1} are the ascents and x_k, ..., x_{k+l-1} are the descents, with x_{k+l} = x_0.

The descents give x_{k+j} = (2/3)^j x_k. For these to be multiples of 3 for j < l, and x_0 not to be, we need x_k = 3^l e and x_0 = 2^l e with 3 ∤ e.

Conversely, suppose x_0 = 2^l e with 3 ∤ e, the first k iterates are non-multiples of 3, and S^k(x_0) = 3^l e. Then the orbit is exactly such a 1-cycle.

**Step 3 (cycle equation).** Put Y_i = 3^i x_i. Then Y_{i+1} = 4Y_i + 5δ_i 3^i. Hence

    3^{k+l} e = 4^k 2^l e + 5 Σ_{i<k} δ_i 4^{k-1-i} 3^i,

so

    e·|D| ≤ 5(4^k − 3^k),   where D = 3^{k+l} − 2^{2k+l}.

D is never 0: it is odd minus even.

**Step 4 (small minimum).** Here x_0 is even, since l ≥ 1, and 3 ∤ x_0. So x_0 ∈ {2, 4} or x_0 ≥ 8.

- x_0 = 2 lies on (1, 3, 2), which is a 1-cycle.
- x_0 = 4 lies on the 11-cycle (4, 7, 11, 13, 19, 27, 18, 12, 8, 9, 6), which has 2 descent blocks.

So assume x_0 ≥ 8. Then every ascent x_i ≥ x_0 > 5, by the monotonicity noted above.

**Step 5 (k is bounded by l).** From S(x) ≥ (4x − 5)/3 on ascents we get x_{i+1} − 5 ≥ (4/3)(x_i − 5). So

    (4/3)^k (x_0 − 5) ≤ x_k − 5 < (3/2)^l x_0.

Since x_0/(x_0 − 5) ≤ 8/3, this gives

    (4/3)^k < (8/3)(3/2)^l.

Equivalently, 3·4^k·2^l < 8·3^{k+l}. Hence

    k < (l·log(3/2) + log(8/3)) / log(4/3) < 1.40943 l + 3.41.

**Step 6 (small linear form).** Let Λ = (2k+l) log 2 − (k+l) log 3. Then

    |D| = max(A, B)(1 − e^{−|Λ|}) ≥ B·min(|Λ|, 1)/2,

where A = 3^{k+l} and B = 2^{2k+l}. This uses 1 − e^{−x} ≥ x/2 on [0, 1], which holds by concavity together with 1 − e^{−1} > 1/2.

From Step 3, |D| < 5·4^k, so min(|Λ|, 1) < 10·2^{−l}. For l ≥ 4 the right side is below 1, so

    0 < |Λ| < 10·2^{−l}.

**Step 7 (two-log bound).**

*Source.* M. Laurent, "Linear forms in two logarithms and interpolation determinants II", Acta Arith. 133 (2008), 325–348, Corollary 2 with m = 10. I consulted it as restated verbatim in M. Bennett, V. Patel, S. Siksek, "Perfect powers that are sums of consecutive cubes", arXiv:1603.08901, Proposition 5.1, which they describe as "a special case of Corollary 2 of Laurent [8] (with m = 10 in the notation of that paper)". The statement is:

> Let α_1, α_2 be positive real, multiplicatively independent algebraic numbers, with log α_1 and log α_2 real and positive. Let D = [Q(α_1, α_2) : Q]. Let b_1, b_2 be positive integers, and let A_1, A_2 > 1 be real numbers such that log A_i ≥ max{h(α_i), |log α_i|/D, 1/D} for i = 1, 2. Put b′ = b_1/(D log A_2) + b_2/(D log A_1), and let Λ = b_2 log α_2 − b_1 log α_1. Then
>
>     log|Λ| ≥ −25.2 D^4 (max{log b′ + 0.38, 10/D, 1})^2 log A_1 log A_2.

(The statement as quoted implicitly assumes Λ ≠ 0, which holds here.)

*Application.* Take α_1 = 3, α_2 = 2, b_1 = k + l, b_2 = 2k + l, D = 1, log A_1 = log 3 (≥ max{log 3, log 3, 1}) and log A_2 = 1 (= max{log 2, log 2, 1}). Then

    b′ = (k + l) + (2k + l)/log 3 ≤ 5.885 l + 9.62 < 5.9 l + 10,

using Step 5. Combining with Step 6, any 1-cycle with l ≥ 4 and x_0 ≥ 8 satisfies g(l) ≤ 0, where

    g(l) = l log 2 − log 10 − 25.2 log 3 · max{log(5.9 l + 10) + 0.38, 10}^2.

Two facts about g, both checked in `check.py`:

- g(4500) > 25 (verified with rigorous rational enclosures of the logarithms).
- g′(l) > 0.54 on [4000, ∞). Where the max equals 10, g′ = log 2. Where it equals the log term, g′ ≥ log 2 − 50.4 log 3 (log u + 0.38)·5.9/u with u = 5.9 l + 10, and (log u + 0.38)/u is decreasing in u.

So g > 0 for all l ≥ 4500, and therefore **l ≤ 4499**.

**Step 8 (finite scan, exact integers).** For every 1 ≤ l ≤ 4499 and every k ≥ 1 with 3·4^k·2^l < 8·3^{k+l} (the bound of Step 5), test the necessary condition |D| ≤ 5(4^k − 3^k) from Step 3. Exactly 15 pairs (k, l) pass, all with l ≤ 5.

For each of these pairs and every e with 1 ≤ e ≤ 5(4^k − 3^k)/|D| and 3 ∤ e, test the exact criterion of Step 2 by simulating S from x_0 = 2^l e. The only hits are (k, l, e) = (2, 1, 1), (1, 1, 5), (2, 1, 7) and (3, 2, 5). They give (1, 3, 2), (10, 15), (14, 17, 21) and (20, 25, 35, 45, 30).

Together with Steps 1 and 4, this proves the theorem. ∎

The scan does not need the l ≥ 4 restriction of Step 6, since it covers every l ≤ 4499. Steps 6 and 7 are used only to bound l. The bound on k used in the scan is the one from Step 5, which holds whenever x_0 ≥ 8. The cases x_0 ∈ {2, 4} were settled directly in Step 4.

## What is conditional

Only the Laurent constant, as described in Step 7. I read it in arXiv:1603.08901, Proposition 5.1, a verbatim restatement of a special case of Laurent 2008, Corollary 2. I did not read Laurent's paper itself.

As a margin check, the cutoff is robust. The exact computation already runs to l = 4499, and with the weaker LMN 1995 constants (24.34, max{log b′ + 0.14, 21}) the cutoff would be about l ≈ 1.7·10^4. That is still a feasible scan, but it was not run.

## How to verify

`python3 check.py` takes about 95 s on an idle machine (309 s when run alongside another copy; well under 10 minutes) and exits 0 iff every check passes. It does the following:

1. Checks the branch formulas (4x ± 5)/3 and 2x/3 for x < 3·10^5, the identity S(5y) = 5T(y), and that S preserves 5-divisibility.
2. Computes the cutoff with rigorous rational log enclosures (atanh series with an explicit tail bound): g(4500) > 1, the derivative bound on [4000, ∞), the bound b′ ≤ 5.9 l + 10, and the slope constants 1.40943 and 3.41 of Step 5.
3. Runs the exact scan over l < 4500 and k ≤ kmax(l), listing the 15 candidate pairs. It also checks kmax(l) < 1.40943 l + 3.41.
4. Runs the e-enumeration and simulation, finding exactly the four (k, l, e) above, and checks that the orbit of 4 has 2 blocks.
5. As a sanity check, finds by brute force all cycles with minimum < 10^5: minima 1, 4, 5, 10, 14, 16, 20, 220. The 1-cycles among them have minima 1, 5, 10, 14, 20.

## Referee (round 1)

**Verdict: CONFIRMED.** I re-derived every step and found no mathematical gap. The one literature input is now checked against Laurent's original paper, so the result no longer needs to be marked CONDITIONAL. There are two wording slips, listed below; neither affects the proof.

**Literature constant, checked against the original.** I read M. Laurent, "Linear forms in two logarithms and interpolation determinants II", Acta Arith. 133.4 (2008), 325–348, from the IMPAN download (pp. 325–330, which include Table 1 and Corollaries 1–2 on p. 328). I also checked the LaTeX source of Bennett–Patel–Siksek, arXiv:1603.08901, Prop. 5.1, and the prover's quotation of it is verbatim.

What the original says:
- Λ = b2 log α2 − b1 log α1, where b1 and b2 are positive integers.
- D = [Q(α1,α2):Q]/[R(α1,α2):R], which is 1 here.
- b′ = b1/(D log A2) + b2/(D log A1), with A_i > 1 and log A_i ≥ max{h(α_i), |log α_i|/D, 1/D}.
- Corollary 2 assumes α1 and α2 are multiplicatively independent, and that α1, α2, log α1 and log α2 are real and positive. It then gives log|Λ| ≥ −C2 D^4 (max{log b′ + 0.38, m/D, 1})^2 log A1 log A2 for each pair in Table 1.
- Table 1 gives C2(10) = 25.2.

The application in Step 7 meets all of these hypotheses:
- α1 = 3 and α2 = 2 are multiplicatively independent.
- h(3) = log 3 ≥ 1, so log A1 = log 3 is admissible.
- log A2 = 1 = max{log 2, 1}.
- b1 = k + l and b2 = 2k + l are positive.
- b′ = (k + l) + (2k + l)/log 3 matches the formula above.

**Steps checked by hand.**
- Branch formulas: correct.
- Step 2: the block shape x_0 = 2^l e, x_k = 3^l e with 3 ∤ e is correct.
- Step 3: the recursion Y_{i+1} = 4Y_i + 5δ_i 3^i and the bound |Σ| ≤ 4^k − 3^k are correct.
- Step 4: x_0 is even and not a multiple of 3, so x_0 ∈ {2, 4} or x_0 ≥ 8. This is correct.
- Step 5: S(x) − 5 ≥ (4/3)(x − 5) holds on every ascent, with no need for x > 5. Together with x_0/(x_0 − 5) ≤ 8/3 this gives the strict bound 3·4^k·2^l < 8·3^{k+l}. That inequality is monotone in k, since its ratio grows by 4/3 per step, so the scan's early stop is valid.
- Step 6: 1 − e^{−x} ≥ min(x, 1)/2, and e|D| < 5·4^k. Both are correct.
- Step 7: on [4000, ∞) the max equals the log term, because log 23610 + 0.38 ≈ 10.45 > 10. Also g′ ≥ 0.5486 there.
- Definition: on a cycle that avoids {2, 5}, the up-steps are exactly the non-multiples of 3. So the strict local minima are exactly the starts of the ascent blocks.

**Independent computation** (`referee_check.py`, my own code, about 155 s, exit 0):
- (A) The map from `census/systems.py` (perm_swap_s8 `mod_table`) equals the brief's S for n ≤ 2·10^5. On the same range it confirms the ±5 branches, that every ascent other than 2 and 5 rises, and that S(5y) = 5T(y).
- (B) Logarithms are computed with Python `decimal` at 60 digits, independently of check.py's atanh enclosures; the margins are at least 0.5, far above rounding.
  - g(4500) = 25.41.
  - g > 0 at every integer in [4455, 4500], and at every 7th integer in [4500, 60000], where it exceeds 20.
  - g′ ≥ 0.5486 on [4000, ∞).
  - The constants 1.40943, 3.41, 5.9 and 10 all check out.
- (C, D) Exact scan over 1 ≤ l ≤ 4499, with k running 3 beyond the Step-5 bound.
  - 21 pairs (k, l) pass |D| ≤ 5(4^k − 3^k). Six of them, (5,1), (6,1), (7,1), (7,2), (8,2) and (9,2), are excluded only by the k-bound.
  - Simulating every admissible e for all 21 pairs, including the descent closure back to 2^l e, gives exactly (1,1,5), (2,1,1), (2,1,7) and (3,2,5).
  - So for small l the result does not depend on Step 5 at all.
- (E) Brute force over every cycle with minimum below 10^5, counting *strict local minima* directly from the definition rather than blocks.
  - The cycles have minima 1, 4, 5, 10, 14, 16, 20 and 220. For each one of length > 1, the number of local minima equals the number of blocks.
  - The cycles with one local minimum, plus the fixed point, have minima 1, 5, 10, 14 and 20.
- I also re-ran the prover's `check.py`: exit 0, 74 s on this machine. It reports the same 15 pairs and the same four hits.

**Gap list.** There are no substantive gaps. Items 1 and 2 are wording only, and item 3 is a status update.
1. *Wording, § Consequences:* "On a non-multiple of 3, S(x) > x if and only if x > 5" is false as written, since S(1) = 3 > 1 and S(4) = 7 > 4. The correct statement is "S(x) > x iff x ∉ {2, 5}". The proof only ever uses the correct version: in Step 1, the local-minimum equivalence, and Step 5, which needs no lower bound on x.
2. *Definitional, the fixed point (5):* (5) has zero *strict* local minima. It counts as a 1-cycle only under the theorem's block definition ("at most one block"), which is how the theorem states it. A reader using the literal "exactly one strict local minimum" should treat (5) as the degenerate l = 0 case. The other four cycles have exactly one strict local minimum under both readings.
3. *Status update:* the CONDITIONAL note can be removed. The Laurent 2008 Corollary 2 constant (m = 10, C2 = 25.2, +0.38) was read in the original, on p. 328.
