# Referee 1 report: round 4, lens "schema"

Referee check: `referee1_check.py`. I wrote it from scratch. It does not import
`depthlib`, `schemalib` or `windowlib`, and uses `round3/dichotomy/decide.py` only as a
labelled oracle in [R7] and [R10]. All decisions use ints and Fractions. The script exits 0
in about 40 s. It can fail, and its negative controls [R11] show that it does say no:
it finds no contraction potential for type-(c) tables.

Prover checks re-run: `check_cutoff.py` ALL PASS (exit 0); `check_window.py` ALL PASS
(exit 0); `check_depth.py` ALL PASS (exit 0, 22 items, including the m = 10 formula value).

## Headline: the hard criterion

The lens claims **no** type-(c) system settled, and that is correct. Every system the
folder settles is CERT, that is, type (a) by Theorem T of round 3:

* the designed D members;
* the cut-offs of 3x+1 at j = 2 and of K7 at j = 2..5;
* the window approximants T_N and the K7 approximants.

None of them is presented as a type-(c) success. The two theorems that touch type (c)
directly are negative. B1 is a wall, and W3/W4 are reformulations or conditional
statements. I found no argument in the folder that proves 3x+1, contradicts a known
cycle, or rules out a divergent orbit.

Sanity test [R11]: the window method applied to 5x+1 gives CERT approximants. The true
cycle 13 → 33 → 83 → … has odd density 3/7 > 2/5, so it lies in R_N and drops out of the
approximants. Nothing false about 5x+1 follows, because W3 and W4 only say something
about orbits that avoid R_N.

## Verdicts

| id | verdict | notes |
|---|---|---|
| A1 | CONFIRMED_WITH_FIX | proof re-derived; one trivial case omitted |
| A2 | CONFIRMED_WITH_FIX | mathematics correct; the "round-3 conjecture" label overclaims |
| A3 | CONFIRMED_WITH_FIX | ε missing in the Diophantine consequence |
| A-rec | CONFIRMED_WITH_FIX | all k\* independently confirmed, including m = 10; λ typo; one false sentence in depth.md |
| depth.md [A4] sentence | WRONG (wording) | a witness proves only the lower bound |
| B1 | CONFIRMED | re-derived step by step; adversarial test passes |
| B1-inst | CONFIRMED_WITH_FIX | "CERT only for j = 2" should read j ≤ 2 |
| W1 | CONFIRMED_WITH_FIX | wording in the leftover estimate; README omits hypotheses |
| W1′ | CONFIRMED_WITH_FIX | proved for the accelerated map; round 3 asked about the plain map; now checked and true |
| W2 | CONFIRMED | |
| W3 | CONFIRMED | a reformulation, honestly labelled |
| W4 | CONFIRMED (implication) | (S_C) correctly labelled OPEN |
| W4-ev | CONFIRMED (EVIDENCE) | values reproduced |

### A1: exact certificate, cycles and depth for D(m, word, h, i0)

I re-derived the proof.

* The branches are integral. A D node has the two successors ℓ_{i+1} and ℓ_{i+1} + Q/2,
  and the second is a reset.
* A reset piece ρ → x_1 … x_s → ρ′ has multiplier ≤ G_exit/Q. The last step before a
  reset is a D step, and laps only lose a factor λ.
* Conversely, a walk that attains G_exit closes through its reset partner. Its multiplier
  is G_exit/Q ≠ 1, since 3^x 2^{−y} is never 2^m.
* The t-coordinate dynamics are correct: t ↦ 3t on U and chain steps, t ↦ t/2 on a D step
  with t even, and t ↦ (t+1)/2 through the partner reset when t is odd.
* The minimum-element argument is correct.

**Fix (trivial):** part (2) skips the case where n_min is a chain residue e_j itself
(t_0 = 0). Such an orbit enters the loop with t = 0 and never returns to e_j, so e_j is
not on a cycle. One sentence is enough.

Part (3) is correct: a walk through a reset has a prefix ≤ G_exit/Q < 1. With k\* = Λ + 1
(Theorem 3(a) of dichotomy.md, which I read), the formula follows.

Independent checks:

* [R1]/[R2] build the tables from the text and compute G_exit on the residue graph.
  They compute Λ by an exact search over **all** walks, resets included, with the exact
  table ⌊U log₂3⌋ = bitlen(3^U) − 1.
* [R4] brute-forces all starts n ≤ 2·10^5 for m = 4, 5, 6 and for 40 random CERT members.
  The cycle lists are exactly {(1), loop}.

### A2: unbounded depth from near-critical Christoffel loops

* Balance gives #U ≤ sa/L + 1. I checked this directly for the four words used.
* The product bound 6^{#U}/2^s ≤ 6λ^{s/L} holds.
* The detrended rotation gives P_{i0}(s) ≥ λ.
* The proof in fact gives t\* ≥ qL + 1, so k\* ≥ h + qL + 1. The stated
  h + 1 + L(q − 1) is weaker, and true.
* The convergent estimate |log λ| < log 2/q′ and the Q² log Q asymptotics are correct.

**Fix (label):** the conjecture in round3/dichotomy/deep.md is "for the B(3^k, 2) and
C(3^k) families, sup k\* → ∞". Those are base-3 families. What A2 proves is the analogous
statement for a designed base-2 family with resets. That is a real result. It also
answers deep.md's sentence "a proof needs an explicit family of tables realising such
cycles while keeping every other cycle contracting. That is OPEN", in base 2. It is
**not** a proof of the stated conjecture.

The README headline "(A) A proof of round 3's conjecture" and the table cell "the
round-3 conjecture, for this class" should be reworded. Suggested wording: "proves the
base-2 analogue of the round-3 conjecture for a designed reset family; the conjecture
for B(3^k, 2) and C(3^k) remains OPEN". The fixed-loop (5, 8) family already gives
unbounded (linear in m) depth without translation nodes. The new content is the
Diophantine Q² log Q growth.

### A3: upper bound for every CERT base-2 table with u ∈ {1, 3}

The proof is re-derived:

* Theorem 3(c) gives k\* ≤ 1 + σ/|μ\*|.
* σ ≤ (Q−1)(log 3 + |μ\*|), which gives k\* ≤ Q + (Q−1) log 3/|μ\*|.
* The two cases for the critical simple cycle are correct. If a = 0, the multiplier is
  ≤ 1/2. The best-approximation bound applies because a ≤ |C| ≤ Q < q_{k+1}.
* q_k + q_{k+1} ≤ (a_{k+1} + 2) q_k.

[R10] tests the bound against decide.py's exact k\* on 150 random CERT tables with
m = 2..4, translation nodes allowed. There were no violations.

**Fix:** "a_{k+1} = O(q_k^{μ−2})" should be O(q_k^{μ−2+ε}), and so k\* = O(Q^{μ+1+ε}). The
lens did not look up μ(log₂3). Published effective bounds exist (I recall values around
5 to 8 from Rhin and from Wu–Wang, but did not verify them). The README is honest that
this was not checked.

### A-rec: depth records

All seven k\* values (26, 132, 791, 4335, 41362, 133534, 304506) are reproduced by my
generic exact Λ computation [R2]. That computation does not use the A1 formula. The
lower bounds are confirmed by **my own** integer witnesses [R3]:

* the witness is n = e_1 + Q·2^{D+64}, a different construction from the prover's
  `path_progression`;
* I iterated it directly, including **m = 10 (k\* = 304506)**.

So the m = 10 record can be relabelled "exact; integer witness checked by referee".
CERT is confirmed by decide.py for m ≤ 9. For m = 10 it follows from G_exit = 1016.57 < 1024
(computed exactly) and A1(1).

**Fixes:**

1. In the depth.md records table, the m = 10 row gives λ = 0.99795. The correct value is
   3^147/2^233 = **0.99274**. The k\* value is unaffected.
2. depth.md says the [A4] witnesses, "together with Theorem 3(a) of dichotomy.md, prove
   those k\* independently of Theorem A1". **This is wrong as stated.** A witness shows
   only k\* ≥ the value. The upper bound needs Λ, which [A3] takes from the A1 formula
   (decide.py is called with `want_depth=False` for m ≤ 9). My [R2] supplies an
   independent Λ, so the values do stand.
3. "Previous record 2466 at modulus 27": this compares across moduli and families. The
   like-for-like base-2 comparison is dch_S6_332 against 791 at modulus 64, which the
   text gives. That is fine, but the README row should say so.

### B1: cut-off wall

I re-derived every step.

* **Step 1.** W′ leaves C^∞ within ℓ edges, because r occurs once on C.
* **Step 2.** A C-stretch is exactly a maximal run of C-edges, so the stretches are
  disjoint. Each block gives one run of length in [dℓ, (d+2)ℓ + |W′|]. Every other run
  lies inside a W′. This gives disjoint compact invariant sets X_d. The invariance of
  X_d under T̂ was checked by case analysis on the first block.
* **Step 3.** This is compactness.
* **Step 4.** U_J(F) is a union of classes mod p^J with J ≤ K′.
* **Step 5.** y_i ≡ y_A (mod p^{K+i}) because they share A_d^i, which has at least
  i divisions.
* **Step 6.** (M) holds for T′, so one simple cycle cannot carry two distinct points.

The theorem is correct. It is in effect a sharpened corollary of Theorem N plus
compactness.

Instances: the run-length formulas are correct (odd run = v₂(x+1) for accelerated 3x+1;
3z+1 run = v₂(z+1) − 1 for K7). The block maxima are 2 and 4, so J0 = 3 and J0 = 6.

[R5] checks:

* the cut systems for j = 3..11 (3x+1) and j = 6..11 (K7) are type (c), via my own SCC
  code and the explicit orbits −5 −7 −10 and z = −49/17;
* the cut-offs below J0 have exact contraction potentials, and their cycle lists by brute
  force over n ≤ 10^6 are (1 2) and z = 0 respectively;
* an **adversarial test**: 60 random **non-reset** unit-multiplier replacements on U_J,
  with K′ up to J + 2. All are type (c), as B1 predicts.

**Fix (B1-inst, README):**

* "3x+1 cut at depth j: CERT only for j = 2" should read "for j ≤ 2". The j = 1 reset is
  trivially CERT.
* The README statement of B1 omits the standing hypothesis on T′ (no division-free
  cycle), which cutoff.md states.

### W1: window approximants are CERT

The proof is re-derived. The window is well defined, because after D divisions the class
is known mod p^{K−D}, and D ≤ K − m. The greedy window decomposition and the reset-piece
bound p^{−K + (1−δ)(K−m+e_max)} < 1 are correct.

**Fix (wording):** in "Cycles avoiding R_K", the leftover is controlled by an *upper*
bound, U_left ≤ U_w(x_j) ≤ p^{(1−δ)(K−m+e_max)}, not by "U ≥ 1". The README row
"for every unit-multiplier system" should carry the hypotheses: standing hypothesis,
(H1)–(P), and (1−δ)(K−m+e_max) < K.

### W1′: dist_{2^N}(3x+1)/2^N → 0

The count |R_N| = Σ_{k>5N/8} C(N, k) is confirmed for N ≤ 16, and H(5/8) = 0.9544.

**Fix (substantive but true):** dichotomy.md §7 (Definition 5, Theorem 7, the table) is
about **non-accelerated** 3x+1 (n/2, 3n+1). window.md proves the bound for the
accelerated map, and `check_window.py` tests only that map. The claim does hold for the
question as posed:

* the window of the plain map at K = N, m = 1 is the accelerated N-window, so R_N is the
  same set;
* W1 applies with e_max = 1 = m.

[R7] verifies both statements exactly for N = 4..10, with my own potential and with
decide.py. window.md should say this explicitly.

### W2: explicit schema

I re-derived all three edge cases: r′ ∉ R_N, r′ ∈ R_N, and reset. The term s = N is
bounded by (γ·3^{5/8}/2)^N ≤ 1. I also checked c_max ≤ (3γ/2)^{⌊5N/8⌋} ≤ 2^{N−2} for
N ≥ 4, and the bound B_N on the exceptional set: odd steps need n > (161/2)c_max, and
resets need n > 4c_max.

[R6] checks every edge inequality with my own weights for N = 4..12.

### W3: T_N cycle list and the reduction

[R6] iterates T_N on all n ≤ B_N for N = 4..20, and the only cycle is (1 2). The prover
checks up to 26 (passes). The equivalence is correct, and it is honestly labelled as a
reformulation with an empty induction.

### W4: (S_C) ⇒ Collatz

The proof is correct. The cycle identity Π_odd(3 + 1/z) = 2^L holds for the accelerated
map. (3 + 1/31)^5 ≥ 256 > (3 + 1/32)^5. All n ≤ 31 reach 1. (S_C) is correctly
labelled OPEN.

Nit: "By Theorem B1 a statement of this kind cannot be replaced by a cylinder
statement" is informal. B1 concerns cut-offs near finitely many points, not all
cylinder statements.

### W4-ev

A(27) = 63 (ratio 13.25), A(837799) = 217 (11.03) and A(63728127) = 446 (17.20) are
reproduced. These are correctly labelled EVIDENCE.

## Labels and novelty

The labels are mostly honest:

* the bottom line states the failure of the hard criterion plainly;
* the novelty section says "not checked";
* the trap or divergence caveat is appropriate.

The overclaims needing repair are three: the "proof of round 3's conjecture" headline,
the [A4] "independently of Theorem A1" sentence, and the W1′ presentation mismatch. The
m = 10 λ value is a typo.

## Summary of required repairs

1. Reword A/A2: this is a base-2 designed-family analogue. The B(3^k, 2) and C(3^k)
   conjecture stays OPEN.
2. depth.md: correct λ = 0.99274 for (147, 233), and fix the [A4] sentence (witness =
   lower bound). Optionally cite referee [R2]/[R3] for m = 10.
3. window.md W1′: state that the result also holds for non-accelerated 3x+1, which is the
   question in §7, and why.
4. Minor: the A1 chain case with t_0 = 0; the W1 leftover wording; ε in A3; j ≤ 2 in
   B1-inst; hypotheses in the README rows.
