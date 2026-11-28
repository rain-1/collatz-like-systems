# Referee 2 report: round 4, lens "schema" (second pass, after the REFEREE1 repair)

Referee check: `referee2_check.py`. I wrote it from scratch. It imports nothing from
`depthlib`, `schemalib`, `windowlib`, `decide.py` or `referee1_check.py`. Every decision
uses ints or Fractions; floats are only guesses that are then certified exactly. It exits
0 in about 50 s with 33 PASS lines. Negative controls [Q7] show that it can say no: the
exact-potential certifier refuses the type-(c) 3x+1 cut at j = 3, the cycle finder
produces an exact expanding walk there, and the Λ search rejects wrong k\* values.
Section [Q6] was written to detect a false printed bound, and it does (see W1′).

Prover checks re-run by me on the current files:

* `check_depth.py`: **ALL PASS, exit 0**. This is the complete revised run, including
  [A2] (strengthened bound), the m = 10 formula, the λ-column check and [A5] (m = 8 took
  61 s). The README still says this run is "not yet confirmed", which is now out of date.
* `check_cutoff.py`: ALL PASS, exit 0.
* `check_window.py`: ALL PASS, exit 0.
* `referee1_check.py`: ALL PASS, exit 0.

## Headline: the hard criterion

**No type-(c) system is settled, and the folder says so plainly.** I checked every system
the folder "settles". Each one is CERT, that is, type (a), and none is a type-(c) system
in disguise:

* the D members: exact potential for m ≤ 6, A1(1) with G_exit < Q exactly for all m;
* the 3x+1 cut-offs at j ≤ 2 and the K7 cut-offs at j = 2..5: exact potentials;
* the window approximants T_N (my own W2 weights) and T0_N (exact potential);
* the K7 window approximants, K = 3..9: exact potential, with densities matching the
  text.

The parts that touch type (c) are B1, a negative theorem, and W3/W4, which are a
reformulation and a conditional statement. None of them claims a type-(c) success.

**Would anything here prove something false or famous?**

* B1 only says that some systems are *not* certifiable. It does not decide any system.
* W3 and W4 conclude only for orbits that eventually avoid R_N.
* 5x+1 control [Q6]: every 7k-window of the true 13-cycle has more than 2N/5 odd
  steps, so the W4 analogue gives no conclusion there. All negative 3x+1 cycles expand,
  so they have odd density above log 2/log 3 > 5/8 and lie in R_N. Nothing in the folder
  contradicts a known cycle or a divergent orbit.
* A1 is a theorem about designed tables. Brute force over all starts (n ≤ 4000 for 120
  random members with random residue layouts) finds exactly {(1), loop}.

## Were the REFEREE1 items honestly resolved?

| REFEREE1 item | resolved? | evidence |
|---|---|---|
| A2 headline "proof of round 3's conjecture" | yes | README bullet 1, A2 row and depth.md (correction after A2) now say "base-2 analogue for a designed reset family", with B(3^k, 2) and C(3^k) OPEN. I grepped all four .md files: no leftover overclaim. The withdrawal is stated openly. |
| [A4] "witnesses prove k\* independently of A1" | yes | withdrawn in depth.md. [A5] now gets the upper bound from decide.py's generic depth for m ≤ 8, and it passes. My [Q2] adds a third independent upper bound (generic exact Λ) for m = 4..10. |
| λ at m = 10 | yes | 3^147/2^233 = 0.99274. Checked to 5 decimals by [A3], and by me. |
| A1 case t₀ = 0 | yes | the new paragraph is correct. With t = 0 every D step takes the even branch, and no loop node leads into the chain. |
| A2 bound h + 1 + qL | yes | the proof and check are updated. I re-derived the bound. |
| A3 ε | yes | O_ε(Q^{μ+1+ε}). The remark about dropping ε when μ is stated uniformly is correct. |
| A-rec cross-family comparison | yes | README gives 791 against dch_S6_332 at modulus 64. |
| W1 leftover wording | yes | the upper bound U_left ≤ U_w(x_j) ≤ p^{(1−δ)(K−m+e_max)} is now correct. The note on irrational δ is correct, because the proof uses δ only through the real inequalities. |
| W1′ presentation (plain map) | yes | the direct proof for T₀ is correct (see below). [W1′p] and my [Q5] verify it. |
| W4 informal B1 sentence | yes | withdrawn, and replaced by what B1 actually shows. |
| B1-inst "j ≤ 2" | yes, with a leftover nit | cutoff.md table: see B1-inst below. |
| README hypotheses for B1 and W1 | yes | both are added. |

## Verdicts

| id | verdict | notes |
|---|---|---|
| A1 | CONFIRMED | re-derived; generic Λ, potential, cycle brute force and OBST walks all agree |
| A2 | CONFIRMED | correctly labelled as a base-2 analogue |
| A3 | CONFIRMED | re-derived; 150 random tables with translations, no violation |
| A-rec | CONFIRMED | all 7 k\* reproduced by generic exact Λ; my own witnesses for m = 7..10 |
| B1 | CONFIRMED | re-derived Steps 1–6 |
| B1-inst | CONFIRMED_WITH_FIX | table row "3x+1, j = 1, 2: cycle (1 2)": for j = 1 the cycle list is {(1)} |
| W1 | CONFIRMED | including the K7 instance (my own check, K = 3..9) |
| W1′ | CONFIRMED_WITH_FIX | the printed numeric exponents 2^{0.954N} (README) and 2^{0.9544N} (window.md) are false for large N |
| W2 | CONFIRMED | my own weights checked on every edge, N = 4..12; Lyapunov decrease above B_N |
| W3 | CONFIRMED | cycle lists by brute force over n ≤ max(B_N, 30000), N = 4..26; a reformulation, honestly labelled |
| W4 | CONFIRMED (implication) | (S_C) correctly OPEN |
| W4-ev | CONFIRMED (EVIDENCE) | label correct; values were reproduced by REFEREE1, and I did not re-run them |
| README revision note | CONFIRMED_WITH_FIX | "complete revised run not yet confirmed" is stale: check_depth.py now exits 0 with ALL PASS |

### A1

I re-derived all three parts.

(1) **Out-degrees.** U and chain nodes have out-degree 1. A D node has ℓ_{i+1} and the
reset partner ℓ_{i+1} + Q/2 as successors.

**Cycles that avoid resets.** The chain is entered only at e_1, which has no
predecessor, so the only reset-free cycle is the loop.

**Reset pieces.** A piece ρ x_1 … x_s ρ′ has x_s of type D. Laps only lose a factor λ,
so the piece multiplier is ≤ G_exit/Q.

**Converse.** Close the walk through the reset partner. G_exit = 3^x 2^{−y} is never
equal to 2^m, so G_exit ≥ Q gives an expanding cycle, and Lemma 3 applies.

(2) **t-coordinate dynamics.**
* An integer n = ℓ_i + Qt goes to ℓ_{i+1} + 3Qt on a U step.
* On a D step it goes to ℓ_{i+1} + Q(t/2) if t is even.
* If t is odd, it goes to the partner class with t′ = (t−1)/2, and the reset then gives
  (t+1)/2.

**Minimum element.** The exit value is (t+1)/2 ≤ t₀G_exit + 1/2 < n_min. The reset
classes and the t₀ = 0 cases are handled correctly. Nothing is missing.

(3) **Depth.** Walks through a reset descend at the step after the reset. The formula
follows from k\* = Λ + 1, with t\* nondecreasing in G.

**Independent tests [Q1].**
* 120 random CERT members, m = 4..7, with **random** residue layouts (the prover always
  uses consecutive residues). In every case: an exact potential exists, my generic
  Λ + 1 equals my own implementation of the formula, and brute force over n ≤ 4000 gives
  {(1), loop}.
* 30 members with G_exit ≥ Q. Each has a closed walk with multiplier ≥ 1, verified
  exactly.

### A2

**Balance.** The bound 6^{#U}/2^s ≤ 6λ^{s/L} uses λ^{1/L} = 6^{a/L}/2. I checked this
identity.

**Detrended rotation.** It gives log P_{i0}(s) ≥ (s/L) log λ ≥ log λ.

**Depth bound.** For k ≤ q − 1, 3^h λ^k P(s) ≥ 3^h λ^{k+1} ≥ 3^h λ^q ≥ 1. So
t\* ≥ qL + 1 and k\* ≥ h + qL + 1.

**Convergents.** I computed the continued fraction of log₂3 at 100 digits:
[1; 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55, 1]. This matches the text. 2/1, 8/5,
65/41, 485/306 and 24727/15601 all satisfy 3^q < 2^p.

**Asymptotics.**
* p − qθ < 1/q′.
* h ≍ log Q.
* L ≥ Q/4 − h − 2.
* q′ ≥ q ≥ L/2.6. This fails only for the trivial first convergent 2/1.

So k\* ≥ c′Q² log Q along the subsequence. The weaker printed form (⌊·⌋ − 1) is still
true.

**Label.** The statement is now honestly labelled: a base-2 designed-family analogue,
with the deep.md conjecture OPEN.

### A3

I re-derived each step:
* σ ≤ (Q−1)(log 3 + |μ\*|), because cycles have nonpositive weight after subtracting
  μ\*, and simple paths have at most Q − 1 edges.
* Case 3^a/2^b ≤ 1/2 (this includes a = 0).
* Case b = ⌈aθ⌉ with 0 < a ≤ Q < q_{k+1}: ‖aθ‖ ≥ ‖q_kθ‖ > 1/(q_k + q_{k+1}).
* q_{k+1} ≤ (a_{k+1} + 1) q_k.

[Q3] compares the bound with the generic exact k\* (drift tracked for translation walks)
on 150 random CERT tables, m = 1..4. There are 0 violations.

### A-rec

[Q2] builds each record table from the text: the Christoffel word, the stated i0 and h,
and a **random** residue layout. It then computes Λ by a generic exact search over
(node, 3-exponent, 2-exponent) states, resets included, without using the A1 formula.
It gets 26, 132, 791, 4335, 41362, 133534 and 304506, and G_exit < Q exactly in each case.

For m = 7..10, I also built my own Lemma-1 progression along the deepest walk, which I
reconstructed from the search, and iterated n = a + M·2^80 directly. In each case
T^i(n) ≥ n for i < k\* and T^{k\*}(n) < n. At m = 10 the modulus has 186717 bits.

So every record now has three independent confirmations: the A1 formula, decide.py or
REFEREE1 [R2], and this report. The family-relative caveats are correct.

### B1

I re-derived each step against trichotomy.md, using its definitions of (M), types
(a)/(b)/(c) and Theorem N.

* **Step 1.** W′ is closed at r and not a power of C. A factor of C^∞ that starts at r
  is a prefix of C^∞, because r occurs once on C. So W′ leaves C^∞ within ℓ edges.
* **Step 2.** A C-stretch cannot cross a whole W′ to the left: that would make W′ a
  factor of C^∞ ending at r. The interval I_d and the disjointness for
  d′ ≥ d + 3 + |W′|/ℓ are correct.
* **Steps 3 and 4.** These are compactness, plus the fact that U_J(F) is a union of
  classes mod p^{K′}.
* **Step 5.** A shared level-K walk with D divisions pins a point mod p^{K+D}.
* **Step 6.** Uniqueness under (M) for T′ needs T′'s standing hypothesis, which is
  assumed.

The theorem is correct. It is honestly described as a sharpening of Theorem N plus
compactness.

### B1-inst

[Q4] confirms the following independently:

* y_A = −5 with multiplier 9/8, and y_A = −49/17 with multiplier 81/64. These are exact
  rational fixed points. Their 2-adic branch letters check out, they avoid U_3 and U_6,
  and the y_i agree with y_A mod 2^{K + #divisions} while differing from it.
* With my own Tarjan SCC code, the cut systems (3x+1 at j = 3..10, presented at 2^j and
  2^{j+1}; K7 at j = 6..11) are of type (c).
* 40 random dividing replacements on U_J are also of type (c).
* Below J0, all the cut systems are CERT by exact potential. For 3x+1 at j = 2 the cycle
  list is {(1 2)}. For K7 at j = 2..5, every z ≤ 2·10^5 reaches 0.

**Fix (nit):** in cutoff.md, the instances table has a row "3x+1 | 1, 2 | CERT, cycle (1 2)".
For j = 1 the map is n odd ↦ (n+1)/2, n even ↦ n/2. Its only cycle is the fixed point (1),
since 2 ↦ 1 ↦ 1. The prover's own [C3] reports cycle minima [1] for both j, which does
not separate the two cases. Write "j = 1: cycle (1); j = 2: cycle (1 2)".

### W1

I re-derived the proof:
* the window is determined by r mod p^K because D ≤ K − m;
* the greedy cut works because every node of the walk lies outside R_K;
* full windows satisfy U ≤ p^{(1−δ)D};
* the leftover piece satisfies U_left ≤ p^{(1−δ)(K−m+e_max)};
* a piece through a reset has multiplier ≤ p^{−K+(1−δ)(K−m+e_max)} < 1.

[Q5] also checks the K7 instance (p = 2, m = 2, e_max = 2, δ = 1/5) for K = 3..9. All
are CERT by exact potential, and |R_K|/2^K = 1/8, 1/8, 3/32, 9/64, 11/128, 25/256, 35/512,
as in the text.

Nit, not required: the general "Density" paragraph ("μ(R_K) → 0 whenever δ is smaller
than the typical log-contraction") is an unproved large-deviation statement for general
systems. It is not in the README table and not labelled. Consider marking it EVIDENCE or
heuristic.

### W1′

**Mathematics: correct.**

* *Plain map T₀.* Every 3n+1 step is followed by a halving at the same D, so the window
  ends right after the N-th halving and is the accelerated N-window. So R_N is the same
  set.
* *CERT for T₀,N.* A cycle avoiding R_N has multiplier^j ≤ 3^{5N/8}·(3^{5N/8}/2^N)^{#full
  windows}, and the number of full windows grows linearly in j. A piece through a reset
  has multiplier ≤ 2^{−N}·3^{5N/8} < 1.
* [Q5] confirms R_N(T₀) = R_N(accelerated), and that T₀,N is CERT by exact potential for
  N = 4..9.
* T₀,N satisfies (H1), (H2) and (P) at modulus 2^N. So Definition 5 of dichotomy.md
  gives dist_{2^N}(T₀) ≤ |R_N|, which answers the §7 question.

**Fix (required, text only): the printed numeric exponents are false.** The correct
Chernoff bound is Σ_{k>5N/8} C(N,k) ≤ 2^{N·H(5/8)} with H(5/8) = 0.954434…. The text
rounds this exponent **down**, and an upper bound with a smaller exponent is a stronger,
false claim for large N, because the tail is only 2^{NH}/Θ(√N):

* README row W1′: "≤ 2^{0.954N}". This is false at N = 20000. I verified exactly that
  the sum exceeds 2^{19080}. It fails from roughly N ≈ 15500 on.
* window.md, Corollary W1′ display: "≤ 2^{0.9544 N}". This is false at N = 400000. I
  verified exactly that bitlen(sum) = 381765 > 381760. It fails from roughly
  N ≈ 2.7·10^5 on.

The first display in window.md, "≤ 2^{N·H(5/8)}, H(5/8) = 0.9544", is fine, because H is
the symbol. Replace both numeric forms with 2^{N·H(5/8)} (H(5/8) = 0.95443…) or with
2^{0.9545N}. The conclusion (exponential decay of dist/2^N) is unaffected. REFEREE1
tested 0.9545 only up to N < 400, and so did not catch this.

### W2

I re-derived all three edge cases:
* r′ ∉ R_N: the s = N term is ≤ (γ3^{5/8}/2)^N ≤ 1 ≤ c(r), since γ^8·243 < 256;
* r′ ∈ R_N: 3/4 < 1;
* reset: c_max ≤ (3γ/2)^{⌊5N/8⌋} ≤ 2^{N−2}, since 0.371N ≤ N − 2 for N ≥ 4.

I also re-derived the bound on the exceptional set from c(r) − (3/2)c(s) ≥ c(r)/161 and
n > 4c_max at resets.

[Q5] computes my own weights and checks c(s)u < c(r)w on every edge for N = 4..12. It
also checks that V(T_N n) < V(n) for every n in (B_N, B_N + 4·2^N].

### W3

(1) The orbit is a T_N-orbit after t₀. V takes values in a discrete set (finitely many
rational c values times integers), so it cannot decrease forever, and the orbit enters
[1, B_N] infinitely often. (2) The windows of (1 2) contain ⌈N/2⌉ ≤ 5N/8 odd steps for
N ≥ 4.

[Q5] brute-forces T_N from every n ≤ max(B_N, 30000), N = 4..26. Only (1 2) appears.

The "empty induction" description is accurate and honest.

### W4

* The cycle identity ∏_odd(3 + 1/z) = 2^L holds for the accelerated map.
* (S_C) applies to windows of length kL ≥ max(4, C log₂ n) inside the final cycle.
* (94/31)^5 ≥ 256 > (97/32)^5 holds exactly.
* All n ≤ 31 reach 1.

(S_C) is correctly labelled OPEN. The remark that it implies logarithmic stopping-time
bounds is informal but correct in direction.

## Labels and novelty

* The bottom line, the "Where exactly it stalls" section and the Honest limits section
  are accurate.
* The novelty statement ("not checked for any item"; Christoffel words standard;
  resemblance to Terras/Everett) is appropriately modest.
* The trap/divergence caveat is appropriate.
* The only label problems left are the two false numeric exponents (W1′), the j = 1
  cycle wording (B1-inst) and the stale "not yet confirmed" sentence in the README
  revision section.

## Required repairs (all text-only; no mathematics changes)

1. README row W1′: replace 2^{0.954N} by 2^{N·H(5/8)} (H(5/8) = 0.95443…) or 2^{0.9545N}.
   Make the same change in the window.md Corollary W1′ display, which currently reads
   2^{0.9544N}.
2. cutoff.md instances table: for 3x+1 at j = 1 the cycle is (1), not (1 2).
3. README "Revision after REFEREE1": the full `check_depth.py` run now exits 0 with ALL PASS
   ([A1]–[A5], including m = 10 and [A5] m = 8). Replace "not yet confirmed".
4. Optional: mark the general density remark in window.md as heuristic.

With these edits every claim stands as CONFIRMED. No further mathematical refereeing is
needed.
