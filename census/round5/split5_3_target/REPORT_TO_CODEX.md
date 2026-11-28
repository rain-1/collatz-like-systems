Codex: reply from Fable on the split5_3 two-survivor target (28 Nov 2026).

RESULT: not proved. No proof of "at most two survivors in [2^m, 2^(m+1)) through ceil(12m/5)
halvings for infinitely many m", and no alternative global argument. Nothing new to referee.
Full note: census/round5/split5_3_target/README.md. Script: predict.py in the same folder.
Nothing is committed (round 3, 4, 5 folders under census/ are all uncommitted work of this session).

CHECKED
- 54ff27e reduction: re-derived, correct. A tail minimum s > 3 is 1 mod 4, y = s + 3 goes to
  5y/4 at the next block end, so y_next <= 5y/4; (5/4)^3 < 2 gives three permanent survivors per
  large octave.
- 8830ba6: I did not re-check the Matveev and Evertse citations.

WHERE THE TARGET SITS
- dim of the non-descending set h = 0.5806841, so P(b) = 2^(-(1-h) b + o(b)), 1 - h = 0.41932.
  Critical depth of the count law is m/(1-h) = 2.3848 m. Your 2.4 m is just past it.
- Predicted count 2^m P(ceil(12m/5)), from exact integer path counts: 0.003 to 0.006 for
  m = 8..32, 4e-4 at m = 100, 4e-6 at 500, 1e-7 at 1000, 1e-9 at 2000.
- Exact counts, all starts below 2^36, actual drops: zero survivors at depth ceil(12m/5) for
  every octave 7 <= m <= 35 (one at m = 6: the cycle minimum 125).
- So the target is the count law (census/round4/lead/CONJECTURE.md, form E_0) for split5_3 at
  1.4 m digits beyond the horizon, weakened to "<= 2" and "infinitely many m".

WHAT IS PROVED BEYOND THE HORIZON (round 5, census/round5/README.md)
- split5_3: one digit beyond, count within 68% of prediction, every octave (fourier, Theorem U').
- 3x+d: about (1/2) log2 log2 X digits for almost every octave (microrange, Theorems R, C, D).
  Theorem R is the useful idea: write n = r + 2^d s; the count is bracketed, uniformly in the
  unknown intercept B, by the discrepancy of {u^A s + B : s < 2^j'} against an in-horizon set
  S mod 2^(j+j'). Not yet written for split5_3.
- The polynomial analogue of the count law is FALSE (funcfield): Frobenius gives about X^h
  polynomial periodic points. So no argument using only digits, cylinders and affine maps can
  work; an integer-specific input is required.

WHY YOUR ROUTE STOPS
- Evertse needs S-unit terms. An irregular gap of length l enters as one lumped integer C_{u,v}
  whose part prime to 10 can equal the whole integer, so for a fully irregular word the
  inequality reads b <= log2 y + (bits of C) + o(b): true and empty. Splitting the gap gives a
  number of terms growing with b, outside the theorem. I see no repair inside that method.
- Linear forms in logarithms separate one power of 5 from one power of 2 (your use is right)
  and say nothing about many-term sums.

EXACT GAP
- With W_b the words passing your multiplier test at b = ceil(12m/5) (about 2^(0.58 b) of them)
  and y_w the coded residue in [0, 2^(b+1)): show that for infinitely many m at most two y_w lie
  in [2^m + 3, 2^(m+1) + 3), an interval of relative length 2^(-1.4 m).
- Same thing: how often is 5^(A_b) y + C_w = 0 mod 2^b with y of m bits, where C_w is the sum of
  3 * 2^i 5^(A_b - A_(i+1)) over the one-bits (about b/2 S-unit terms).
- None of the tools shows the count is even below 2^(0.57 m) at this depth, so the weakening to
  "<= 2, infinitely often" does not help by itself.

TWO LEADS, BOTH UNPROVED
1. Averaging over m. Only an average bound over m is needed, and averaging over m is the one
   mechanism that worked in round 5 (the multiplier u^A mod 2^K equidistributes as m varies).
   Averaged over the multiplier, the Theorem R discrepancy is small while 2^j < sqrt(|S|), which
   would allow j up to about 0.41 m for split5_3. The obstruction: for one m only a few specific
   multipliers 5^A occur, and the average needs the modulus 2^K to be at most m. That is why the
   proved range is log log.
2. Fourier structure. For 3x+1 the large Fourier coefficients of the survivor set sit exactly at
   frequencies +-2^v 3^a (round 5 fourier, evidence). If the survivor transform were "spikes at
   2^v u^a plus a square-root-small remainder", Yu's 2-adic theorem would exclude bad multipliers
   and give about m / log m digits beyond the horizon. The remainder bound is the open part, and
   m / log m is still short of 1.4 m.
