# Round 5 (27-28 November 2026): attempts to prove Conjecture E

Conjecture E (`../round4/lead/CONJECTURE.md`): among the starts n <= X, the number that have
not dropped below themselves after b halvings is X P(b) up to a small error, even for b beyond
log X, where the digits of n are used up ("integers are generic beyond their own digits"). It
implies GLOBAL for the system (for 3x+1, the Collatz conjecture), with the sharp constant
1/(1 - h). Three lenses tried to prove it or neighbouring statements; each was refereed twice.
`../round5_results.json` holds every claim and verdict. Agent-written and agent-refereed; the
proofs of Theorems R and D were also read outside the loop. No human review.

**Conjecture E itself is not proved.** What was proved:

An [extension to actual stopping times](microrange/actual_counts.md) transfers Theorem D
for each odd d to every interval length in almost every dyadic size range and every
interval location. It also gives exact height-versus-slope corrections through depth
3012 for 3x+1 and 3x-1.

## 1. The first theorems beyond the horizon (`microrange/`, `fourier/`)

All for the coefficient (slope) stopping time, which is at most the actual stopping time.

* **Theorem R (reduction).** For 3x+d: split n < 2^m as r + 2^d s. The count of n surviving
  m + j steps is bracketed by sums of min_B and max_B of #{s < 2^{j'} : 3^A s + B in S}, where S is
  an in-horizon set. The bracket is uniform in the unknown intercept B, which is where the
  beyond-horizon information lives, so it is not circular.
* **Theorem C (certified counts).** For 3x+1 and 3x-1: for m = 100, 1000, 3000 and every
  j <= 12, the number of n < 2^m surviving m + j steps equals 2^m P(m+j) within 1.9% (within
  0.93% at m = 1000). For every m in [35, 1000] and j = 4, within 0.62%. The trivial bounds
  there are about -90% / +50%.
* **Theorem D (almost all octaves).** For all but M^{1 - eta/3} of the m in [M, 2M), the count
  law holds for X = 2^m at every depth up to log2 X + (0.4715 - eta) log2 log2 X, with a
  power-saving error. Holds for every 3x+d.
* **Theorem U' (every octave, exact constants).** For every b >= L the count m digits beyond
  the horizon is within an explicit constant of the prediction: 3x+1, 3x-1, 3x+5: 12.2%, 28.4%,
  46.6% for m = 1, 2, 3; K7: 28.8% and 77.2%; split5_3: 68% at m = 1.

So the count law is now a theorem a few digits past the horizon (about half of log log X digits
for almost every octave), against the multiple of log X that Conjecture E needs.

## 2. The polynomial analogue is false (`funcfield/`)

For Collatz-like maps on polynomials over F_3, F_4 and F_2 with negative drift and free re-entry
(systems A3, Q4b, S2c), the analogue of E fails at every depth beyond the horizon: because
(1 + t^2)^{3^k} = 1 + t^{2·3^k}, every zero-slope branch word of length 2·3^k has a polynomial
periodic point, giving at least X^h/(log X)^2 polynomials that never drop, where the prediction
tends to 0. Inside the horizon the count law holds.

Meaning for the integer case: any proof of E that uses only the digit, cylinder and affine
structure would also prove the false polynomial statement. A proof must use something integers
have and polynomials lack. In the integers the corresponding near-returns need 2^L - 3^a = ±1,
which happens only for (L, a) = (1,0), (1,1), (2,1), (3,2), giving the cycles 0, -1, (1 2),
(-5 -7 -10).

## 3. Fourier form and what it rules out (`fourier/`)

* E a bounded number of digits beyond the horizon is equivalent to: the Fourier coefficients of
  the survivor measure tend to 0 at each fixed frequency. OPEN.
* The coefficients do not decay uniformly: for 3x+1 the largest stay near 0.05 and sit exactly
  at frequencies ±2^v 3^a. A square-root hypothesis H on their L1 size is supported numerically
  and would give E up to 1.9 log X for 3x+1, short of the critical 20 log X.
* No argument that uses only the sizes of Fourier coefficients can prove the minimal form
  (every large n drops within C log n): translates of the survivor set have the same sizes.
* The inference "E implies bounded stopping constant" in the first version of CONJECTURE.md was
  invalid (its additive error term was too generous). The corrected form E_0 does imply it;
  CONJECTURE.md has been corrected.

## What is open

1. Theorem D for every m, not almost every m: needs control of the specific multipliers 3^A
   against the survivor set, not their average.
2. Any depth beyond log log X.
3. The same theorems for split5_3 and K7 beyond one or two digits.
4. An argument that uses the signs (phases) of the Fourier coefficients, or an Archimedean
   input (Baker-type separation of powers of 2 and 3) carried into the middle digits by carries.
