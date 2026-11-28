# split5_3 at the two-survivor depth: attempt, and the exact remaining gap (28 Nov 2026)

Request (handed over from the session that wrote commits 54ff27e and 8830ba6): prove that for
infinitely many m at most two starts in [2^m, 2^{m+1}) stay at or above their start through
b = ceil(12m/5) halvings. By 54ff27e this would exclude escaping orbits of split5_3.

**Outcome: NOT PROVED.** I found no proof and no alternative global argument. This note
records what was checked, what the target is in the language of rounds 4 and 5, the numbers,
and the exact gap. Nothing here is a new theorem. Not refereed.
Script: `predict.py` (exact integer path counts).

## 1. What I checked of the reduction

* Tail minima: a tail minimum s > 3 has s = 1 mod 4 (otherwise the next block is below s), so
  with y = s + 3 the next block end is 5y/4, and the following tail minimum has y' <= 5y/4.
  Since (5/4)^3 < 2, an escaping orbit has at least three tail minima in every large octave, and
  each is a permanent survivor. So "at most two survivors for infinitely many m" does exclude
  escaping orbits. I re-derived this; it is correct.
* The exact survival test and the periodic-stretch theorem of 8830ba6 rest on Matveev's and
  Evertse's theorems. I did not re-check those citations.

## 2. Where the target sits

The non-descending 2-adic set of split5_3 has dimension h = 0.5806841 (round 3), so the Haar
measure of points surviving b halvings is P(b) = 2^{-(1-h) b + o(b)} with 1 - h = 0.41932, and
the critical depth of the count law is b = m/(1-h) = 2.3848 m (`../../round4/lead/CONJECTURE.md`).
The requested depth 2.4 m is just past it: the predicted count is 2^m P(2.4m), about
2^{-0.0064 m} times a factor near m^{-3/2}.

| m | b = ceil(12m/5) | log2 of predicted count 2^m P(b) | predicted count |
|---|---|---|---|
| 8 to 32 | 20 to 77 | -7.5 to -8.5 | 0.003 to 0.006 |
| 100 | 240 | -11.3 | 4e-4 |
| 500 | 1200 | -17.8 | 4e-6 |
| 1000 | 2400 | -23.1 | 1e-7 |
| 2000 | 4800 | -29.4 | 1e-9 |

Exact counts (all starts below 2^36, actual drops): the number of survivors at depth
ceil(12m/5) is 0 for every octave 7 <= m <= 35 (and 1 for m = 6, the cycle minimum 125).
So the statement asked for is what the count law predicts for every large m, with a predicted
total over all m >= 8 well below 1. The request is the count law (Conjecture E_0) for split5_3
at depth 1.4 m beyond the horizon, in a weakened form (a bound of 2, infinitely many m).

## 3. What is proved beyond the horizon, and how far it is from 1.4 m

* Round 5 `fourier` Theorem U': for split5_3, one digit beyond the horizon, the count is within
  68% of the prediction for every octave. Nothing at two digits.
* Round 5 `microrange` Theorems R, C, D (for 3x+d): about (1/2) log2 log2 X digits beyond the
  horizon for almost every octave. Not written for split5_3.
* 8830ba6: survivors at the target depth cannot be more than 49.75% covered by boundedly many
  short-period stretches.

The target needs 1.4 m digits beyond the horizon.

## 4. Why the available tools stop

1. **Evertse / Subspace (the route of 8830ba6).** The inequality needs every term to be an
   S-unit times a bounded factor. An irregular gap of length l enters as one lumped integer
   C_{u,v} of about l bits, whose part prime to 10 can be as large as the integer itself. With
   all of the word irregular the inequality reads b <= log2 y + (bits of C) + o(b), which is true
   and empty. Splitting the gap into its own S-unit terms makes the number of terms grow with b,
   outside the theorem. This cannot be repaired within that method.
2. **Linear forms in logarithms (Matveev, Yu).** They separate one power of 5 from one power of
   2 (used correctly in 8830ba6 for the survival test), and they lose a factor log b when asked
   about valuations; they say nothing about sums with many terms.
3. **The round-5 reduction.** Writing n = r + 2^d s, the count is bracketed uniformly in the
   unknown intercept by the discrepancy of the points 5^A s + B, s < 2^{j'}, against an
   in-horizon set S mod 2^{j + j'}. Averaged over the multiplier this discrepancy is small as
   long as 2^j is below sqrt(|S|), which would allow j up to about 0.41 m for split5_3. But for a
   given m only a few specific multipliers 5^A occur, and nothing controls a specific one. The
   average is available only when the modulus is at most m, which is why the proved range is
   log log.
4. **Any argument using only digits, cylinders and affine maps** is excluded outright: the
   polynomial analogue of the count law is false (round 5 `funcfield`), because Frobenius gives
   many polynomial periodic points. The proof must use a fact about integers such as the
   separation of powers of 2 and 5, and must carry it into the middle binary digits of 5^A s.

## 5. The exact gap

Let W_b be the set of words passing the multiplier test of 8830ba6 at depth b = ceil(12m/5)
(about 2^{0.58 b} words), and y_w in [0, 2^{b+1}) the residue coded by w. By 8830ba6 the count is
exactly #{w in W_b : 2^m + 3 <= y_w < 2^{m+1} + 3}. The missing statement is:

> for infinitely many m, at most two of the residues y_w, w in W_b, lie in the interval
> [2^m + 3, 2^{m+1} + 3), an interval of relative length 2^{m-b} = 2^{-1.4 m}.

Equivalent forms: (a) for each passing word, 5^{A_b} y_w + C_w = 2^b z with C_w the sum of
3 * 2^i 5^{A_b - A_{i+1}} over the one-bits; the question is how often this sum of about b/2
S-units is congruent mod 2^b to -5^{A_b} y with y of only m bits. (b) 5-adically: z must lie in
one residue class mod 5^{A_b} and in an interval 2^{1.4 m} times shorter than the modulus.
(c) Fourier: cancellation in the sum over frequencies of the transform of W_b against a Dirichlet
kernel of length 2^m, which needs the signs of the coefficients, not only their sizes (round 5).

The weakening to "infinitely many m" and "at most two" does not make any of the tools above
applicable: each fails already to show the count is below 2^{0.57 m} at this depth. A count
bounded only on average over m would suffice, and averaging over m is the one mechanism that
worked in round 5, but there it reached log log X digits, not 1.4 m.
