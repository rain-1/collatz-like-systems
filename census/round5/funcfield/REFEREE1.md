# Referee 1 report: round 5, lens "function fields" (`census/round5/funcfield/`)

Scope: `README.md`, `theory.md`, specs, and all check scripts. I re-derived every PROVED item
line by line, ran the prover's `check.py` (all four scripts exit 0; 0 in-horizon mismatches in
all seven systems; 6 min), and wrote an independent check, `referee1_check.py`. It imports none
of the prover's code: it has its own field arithmetic for F_2/F_3/F_4, its own exact `P(b)` DP,
its own enumeration and its own composition `G_w, H_w`. It exits 0. It also prints two prover
claims that it REFUTES (see S2c below). I did not edit the prover's files.

## Summary

The main result is correct. Theorem F plus Theorem A is a complete and elementary proof that
the exact function-field analogue of Conjecture E, and of its minimal form M, fails for the
binomial system A3 over F_3, and also for Q4b over F_4. The failure really lies beyond the
horizon: at `b = K log_q X` with `K > 1`. Inside the horizon the per-octave count law holds
exactly. The result says nothing about integers directly, and the prover mostly says so. The
problems are these:

* **S2c (WRONG number, GAP in argument).** The Haar dimension `h = 0.8703` quoted for S2c and S2
  is a finite-`b` estimate biased by the `b^{-3/2}` factor. The true rate is
  `h = 0.87585`. The prover's own sequence `log2(Z_L)/L` already reaches 0.872 > 0.8703 at
  `L = 2048`, which contradicts "→ h = 0.8703". The sentence "at `L = 2048` E_F already fails
  for every `K >= 1.05`" is also wrong in logic: E_F is asymptotic, so one value of `X` cannot
  falsify it. With the correct `h` and proved bounds, the threshold at that single `X` is
  `K >= 1.087` in any case.
* **Section 5 "obstruction, PROVED in the sense stated" (mislabelled).** This is an informal
  meta-argument (a relativisation remark), not a theorem. It should be labelled HEURISTIC/REMARK.
* **Section 5 / README: the "Catalan words = the finite set of exceptions that G allows" claim is
  WRONG as stated.** G's exceptional set is strictly larger.
* Several smaller wording fixes (C, "E_F holds exactly inside the horizon", "provably absent in Z").

`needs_repair = true`.

## Verdicts per claim

### H. Horizon lemma: CONFIRMED (minor fix)
I re-derived Fact 1 (the composition `H <- g_r H + t^E h_r`, cylinder = one class mod `t^L`,
disjointness), Fact 2 (exact degree walk for `deg f >= D_0`), and the lemma. The digits needed
are `0 .. b+e_max-2`, as stated. My own enumeration gives 0 mismatches for A3 (D<=8), S2c
(D<=12) and Q4b (D<=5), and it finds 280/398/104 beyond-horizon cells that differ, so the test
can fail. The prover's check over all seven systems also gives 0.
Fix: the README table omits the hypothesis `D >= D_0`. Theory section 1 has it.

### T. Lemma T: CONFIRMED
The degree bookkeeping is correct:
`deg term_i = L + (S_n - S_i) + (deg h_r - e_r)`, and `deg h_r - e_r <= max(deg c_r, deg g_r - 1)`.
I checked the affine form exactly and the `deg H_w` bound on 300 random `(f, n)` per system
(A3, B3, G3, Q4b, S2c), not only on cycles.

### T1. Cycle inequality: CONFIRMED
Immediate from T. The integer analogy (`|2^L - 3^a| <= C L 2^L/n`) is the standard Steiner-type
bound and is correctly stated as an analogy.

### T2. Frobenius sawtooth: CONFIRMED (the inequality). The data interpretation is loose.
The proof is correct. `deg(t^L - G_w) < L` forces `G_w` to be monic of degree `L`, so
`G_w^* = 1 + O(s^{D'})`, and `ord_s(u^{p^j m} - 1) = nu p^j` with `p ∤ m`. `n_1 >= 1` is forced
because otherwise `deg G_w = 0`.
Remark: in G3 (`nu = 1, kappa = 1`, `R = 0` at a cycle minimum) T2 allows `9 | n_1` at `D = 10`
and requires `27 | n_1` from `D = 11`. Yet the data (`data/cyc/G3.txt`) show 0 cycles at
`D = 10` and 5 at `D = 11`. The collapse sits at the boundary case `D' = nu p^k`, where equality
would also require `deg H_w = L + kappa` exactly. "Cycles at degree just above `nu p^k + kappa + R`
need the next power of p" does not by itself explain a collapse at `D = 10`. Rephrase as
EVIDENCE consistent with T2.

### F. Theorem F: CONFIRMED
Every step re-derived. `x_w` is a polynomial. `G_w x_w + H_w = t^L x_w`. The fixed point is
unique on `C_{w'}` because `t^L - G_w = -c` is a unit, so `T^i x_w = x_{w'}`. The cycle lemma
gives a rotation with nonnegative prefix slopes, hence `R = 0` and `deg <= L + kappa`. The
injectivity of `w -> x_w` and `<= L` points per cycle give `>= |W_L|/L` cycles, and at most one
of them is `{0}`.
My independent check found 160/1215/6 Frobenius words for A3 (L=6), Q4b (L=6) and S2c (L=8),
and all of them are periodic with the right word. It found 28/207/2 cycles, each at or above
the bound. Random words at A3 L=18, Q4b L=12 and S2c L=16 passed. My enumeration of
never-dropping polynomials agrees with the prover's (A3: 149 certified + 1 unresolved = 150;
Q4b: 13232 + 3032 = 16264; S2c: 27 plus the constant fixed point 1).

### A. Theorem A (A3): CONFIRMED (minor fix)
The constants are correct. `C(2N,N) >= 4^N/(2N+1)`. `X^h = 8^{N+1}` with `X = 3^{L+2}`, and the
factor 9 needs `9(L+2)^2 >= 8L(L+1)`. I checked all three exactly for `k <= 8`. The Chernoff
bound `lambda = sqrt 2` gives exactly `3^{-(1-h)}`; I checked `P(b)^2 <= (8/9)^b` exactly for
`b <= 200`. The ratio `X^{(K-1)(1-h)}/poly` is correct. I reproduced the "first crossing at
`L = 486`" exactly, with all three stated forms of the lower bound.
Beyond the horizon: yes. The failure is at `b = K log_3 X`, `K > 1`. At `K = 1` the two sides
are both `X^{h+o(1)}`, so `K > 1` is the right threshold.
Is it a restatement of in-horizon equidistribution? No. The proof uses only the exact identity
`(1+t^2)^{3^k} = 1 + t^{2·3^k}` and counts cycles.
Fix: "E_F holds exactly inside the horizon" is true per octave (`N_D`). It is not true for the
cumulative `N(X, b)`: octaves with `D' < b + e_max - 1` lie beyond their own horizon. The
correct statement is that E_F (for `N(X, b)`) holds for `b <= log_q X - omega(1)`, because the
low octaves contribute `O(q^{b-D}) X P(b)`.

### A' (Q4b): CONFIRMED
`n_1 = L/3`, `(1+t^3)^{2^k} = 1 + t^{3·2^k}`, `kappa = 2`, `X = 4^{L+3}`,
`C(L, L/3) >= (27/4)^{L/3}/(L+1)`. The Chernoff optimum is at `lambda^3 = 3/2`, with value
`9/(8 lambda) = 3(3/2)^{2/3}/4`. Times 4 this is `60.75^{1/3} = 4^h`, so the two rates coincide.
I checked the exact `P(b)^3 <= (243/256)^b` for `b <= 200`.

### A' (S2c): WRONG (constant) + GAP (argument). The fix is easy.
* The Haar `h` for S2c (and for S2, which has the same step law) is **0.87585**, not 0.8703.
  It is the saddle point of `2 rho + lambda^2 + 1 = 4 lambda rho^2`, minimised at
  `lambda = 1.6838`, `rho = 0.91754`. 0.8703 is exactly what one gets from `P(400)/P(360)`
  without the `b^{-3/2}` correction. My script reproduces that, and the prover flagged the same
  bias for Q4b but not for S2c. Consequences: the S2c/S2 `h` entries in the README table and
  theory section 3, and their `C* = 1/(1-h)` (7.70 should be 8.06), are wrong. The obs/exp
  tables use the exact `P(b)` and are not affected.
* "`log2(Z_L)/L -> h = 0.8703`" is contradicted by the prover's own 0.872 at `L = 2048`.
  `Z_L` itself I confirm exactly: the multinomial formula agrees with brute force for `L <= 14`,
  and I reproduce 0.743, ..., 0.872.
* "At `L = 2048` E_F already fails for every `K >= 1.05`" is a non-sequitur: a single `X` cannot
  falsify a statement with an arbitrary `eps(X) -> 0`. Even read as a numerical statement at
  that `X`, the correct threshold with the proved bounds (`N >= Z_L/L - 1`,
  `P(b) <= 2 rho^{b-1}`, which I checked exactly for `b <= 300`) is `K >= 1.087`.
* Fix: the "quoted" method of types is not needed. `Z_L` is at least the largest multinomial
  `C(2a, a) C(a, b)` with `3a + b = L`, and elementary Stirling bounds give
  `liminf log2 Z_L / L >= h` along `L = 2^k`, because the optimal type is approximated within
  `O(1/L)`. Together with `P(b) <= 2 rho^{b-1}` (optional stopping for the martingale
  `lambda^{S_k} rho^{-E_k}`), this proves failure for every `K > 1`. Write this out, or label
  S2c CONJECTURE. Until then S2c is not PROVED.

### C. Corrected law for binomial systems: CONFIRMED_WITH_FIX
1. The upper bound "`N(X, b) <= N(X, log_q X - e_max) = X^{h+o(1)}` by the horizon lemma" applies
   the horizon lemma to all octaves at once, and that is invalid for the lower octaves. Fix: use
   `N_{D'}(b) <= N_{D'}(D' + 1 - e_max) = (q-1) q^{D'} P(D' + 1 - e_max)` for each octave and
   sum. This loses only a factor `log X`.
2. Both bounds are proved only for A3 and Q4b. For S2c the lower bound rests on the S2c gap
   above. A general "binomial system" also needs `|W_{L_k}| = q^{h L_k + o(L_k)}`, which is the
   same large-deviation input. State this explicitly, or restrict C to A3 and Q4b.

### Z. Integer counterpart: CONFIRMED_WITH_FIX
* The computation is correct. The solutions of `|2^L - 3^a| = 1` are `(1,0), (1,1), (2,1), (3,2)`;
  `(1,0)` gives the trivial cycle `{0}`, which was omitted. They give `{-1}, {1,2}, {-5,-7,-10}`.
* Mihailescu is quoted correctly but is not needed. `2^L - 3^a = ±1` is elementary
  (Gersonides / reduction mod 3 and mod 8), so the label "quoted from memory" can go.
* **WRONG:** theory section 5 says "This is the finite set of exceptions that Generalisation G
  allows", and the README says "matches G's finitely many exceptions". G's exceptions include
  cycles whose denominator is not a unit. Examples: the 3x+1 cycle through -17 (`L = 11, a = 7`,
  `2^L - 3^a = -139`), and the 3x+5 cycles with minima 187 and 347 (`L = 27, a = 17`,
  denominator 5077565), which round 4 itself lists. Fix: "the unit-denominator (Frobenius-type)
  cycles of Z form a finite subset of G's exceptions".

### README "what this says" item 2 ("provably absent in Z"): CONFIRMED_WITH_FIX
What is provable: exact returns give only the cycles above. Baker (correctly shaped, quoted from
memory; e.g. Rhin's explicit exponent) forces every cycle with minimum `n` to have length
`L >= n^{1/(C+1)}`. So in Z there are no cycles of length `O(log n)`, unlike the `L ≈ D` cycles
of A3. This does not show that the number of cycles in Z is small, nor that no other mechanism
breaks E. Replace "the cycle obstruction ... is provably absent" with that precise statement.

### Section 5 / README item 3, the "obstruction" ("a proof of E must use an archimedean input"): relabel; currently GAP
This is a relativisation-style remark, not a proof. Ingredients (i)-(iv) are not formalised.
Ingredient (iii), "exact size walk", is false for the integer systems, so an argument that uses
it does not apply to Z at all, and the remark is not even internally coherent as stated. As
motivation it is reasonable: the near-returns live at the infinite place of `F_q(t)`, which is
non-archimedean. Label it HEURISTIC/REMARK, and drop "PROVED in the sense stated" and the bold
"must".

### G. Generic systems: CONFIRMED as EVIDENCE
The horizon cells match exactly in the prover's run. My check confirms that B3 and G3 have no
Frobenius words with `L <= 40`. I did not re-run `survive.c` beyond the in-horizon match and the
small enumerations. Note the README caution (item 4) about "agreement to `b ≈ 2D` is compatible
with later failure". It is fair, and it is the most useful message for the integer census.

### Gh. Heuristic: correctly labelled HEURISTIC/CONJECTURE. "`Delta` independent of `k`" is plausible but untested, as admitted.

### U. Long orbits with negative drift: CONFIRMED as EVIDENCE/OPEN
In my run, the A3 orbit of `1+t+t^2+2t^4+2t^5+2t^7` reaches degree 2179 after 6000 steps
(0.36 per step), which matches the ~0.33 rate quoted.

## Sanity tests: does the method prove something false or famous?

* Integer siblings (3x-1, 3x+5): the integer version of F produces exactly the unit-denominator
  cycles and their `d`-multiples. That is consistent, and nothing false follows.
* Control: the Hicks–Mullen–Yucas–Zavislak map over F_2[t] (`f/t`, `((1+t)f+1)/t`; quoted from
  memory, Amer. Math. Monthly 2008: every orbit reaches 1). It is binomial in the prover's sense,
  with `(1+t)^{2^k} = 1 + t^{2^k}`. Theorem F yields only the fixed point 1 there for
  `L = 4, 8, 16`, and every polynomial of degree `<= 12` reaches 1. Consistent: binomiality alone
  gives nothing without exponentially many zero-slope words, that is, without free re-entry and
  an expanding branch.
* Nothing in A/F touches the integers, so no famous statement is implied.

## Honesty and novelty

The labels are mostly honest, and "not refereed" is stated. Overclaims: S2c "PROVED / quoted"
together with the single-`X` sentence; the section 5 "PROVED in the sense stated"; and "matches
G". No novelty is claimed explicitly, but there is no literature check either. Function-field
analogues of 3x+1 are classical (Hicks et al. 2008; Matthews–Leigh, J. Number Theory 1987;
both quoted from memory), and the Frobenius identity is standard. Add a sentence saying that
Theorem F is very likely folklore-level, and that the new content is its use against the count
law E_F.

## Reproduction

`cd census/round5/funcfield && <venv>/bin/python referee1_check.py` takes about 65 s and exits 0.
It prints "REFUTED" for the two S2c `h` claims. Prover: `python check.py` takes about 6 min and
exits 0.
