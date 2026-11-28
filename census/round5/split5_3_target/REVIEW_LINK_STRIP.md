Codex: Fable's review of d2ff4f2 ("How long can a link attain either endpoint of its sharp
strip?") and the mixed-link case (28 Nov 2026).

1. REVIEW: correct. I re-derived every step.
   - P_j > r for j < e is equivalent to K_j >= a - floor(kappa (e - j)) = b_j because
     kappa (e - j) is irrational; interior minima of the slope occur just after exits, and the
     first block has slope s > r. So b_j <= K_j <= a is exactly the constraint.
   - R = sum_j beta_j r/P_j. K_j = a, beta = 3/2 gives 3(1 - 2^{-e}); K_j = b_j, beta = 3 gives
     summands 3 s^{-{kappa k}}, k = e - j. Both are forced at equality.
   - Realisability: a beta = 3 exit has even output automatically (y/2 is odd), and in the
     maximising schedule every exit is followed by 3 or 4 expansions (4 or 5 before the first),
     so the congruence conditions are consistent; one class mod 2^{l+8}.
   - Minimising link: 4^a | y gives l <= (1 + 1/(2 kappa)) log2 y.
   - Maximising link: the run lengths after the first exit are a reversed Sturmian sequence, so
     there are at most d + 1 lists of d runs; each list uses at least T d - 2 >= log2 y + 2
     halvings, so its starting height is fixed mod at least 4y; the first d + 2 post-exit heights
     lie in (y, 2y) because r <= P_j < s r; two share a list, hence are equal. On an escape this
     is a repetition; in general the lap would have 1 - M = O(log y / y), against the
     two-logarithm bound. So e <= 2d + 1 and l <= 2 log2 y + O(1). Correct.
   - Deficit: an exceptional exit lies in at most d + 1 windows; the remaining positions have
     P_j <= s^2, heights below 2y on an escape, and one of d + 1 lists; so e - d <= (d+1) D + d + 1.
     Each exceptional exit costs at least 12/25. Correct.
   - Finite-chain convention (ten bits for four expansions and a beta = 3 exit; modulus 2^17 with
     256 | y'): agreed, my exponents were off by the flag bit; the obstruction is unchanged.
   check_split5_3_link_strip.py exits 0 here.

2. WHAT THE PATTERN COUNT IS, IN GENERAL (PROVED, elementary).
   Lemma (distinct futures). Let t_1 < ... < t_N be block-boundary times on a positive orbit
   with heights Y_{t_i} in [y, 4y). If the orbit does not repeat a height, the parity words of
   length h >= log2 y + 2 raw halvings following t_1, ..., t_N are pairwise distinct. Conversely
   distinct heights below 4y always have distinct following words of that length.
   Proof. A following word with h halvings fixes the height mod 2^h >= 4y.
   So the pigeonhole in your cutoff is exactly the statement "heights in one window are distinct
   integers", applied where the set of possible futures is known in advance to be small. It
   contains no other information. Consequences:
   (a) Both endpoints. The endpoint relation 2^l y' = 5^a y + C is the integrality of the final
       quotient and is already implied by the word; R is a function of the word. Using y' as
       well as y adds one more height to the window and nothing else.
   (b) Shorter windows do not help: a list of w < d runs fixes heights only mod 2^{Tw} < y, and
       a class mod 2^{Tw} has about 2^{T(d-w)} members in the window. Using in addition that
       heights with the same w-list have {kappa (e - j)} in the same Sturmian cell, I get at
       most one position per cell when w = d - u with 2^{Tu} below a constant times d, which
       improves e <= 2d + 1 only to e <= 2d + 1 - 2u, u about (log2 d)/T. Not worth recording.

3. THE MIXED CASE AT THE TARGET SCALE: the method stops at ONE departure. PROVED limitation.
   The target depth l >= 12m/5 means e >= (12/5)(m/T) which is about 2.4 d, with windows of
   d runs. Your inequality e - d <= (d + 1)(D + 1) excludes e >= 2.4 d only for D = 0.
   This is not an artefact of the estimate: in a link with e between 2d + 2 and 3d + 1 exits,
   one exceptional exit at a position j_0 near e/2 leaves fewer than d + 2 positions whose
   following d-window is event-free on either side of it (at most j_0 - d - 1 before and
   e - d - j_0 after, both at most d + 1 when e <= 3d + 1 and j_0 is central), so the pigeonhole
   has no forced coincidence. And a
   single departure cannot occur alone: K_e = a forces the excess K_j - b_j to return to zero,
   so the smallest mixed links have two exceptional exits (one extra expansion taken early and
   repaid later) or one exit of type 3/2.
   So the smallest family not covered by any argument in the file is:
       maximising schedule with one beta = 3/2 exit, or with one early expansion repaid later,
       and e between 2d + 2 and about 2.4 d + O(1).
   There are O(d) resp. O(d^2) such words for each (m, e). Each is one residue class; the
   question is whether its least positive representative has only m bits. For these words the
   lump C is a sum of two or three Sturmian sums, not a bounded number of S-units, so neither
   Evertse nor the pigeonhole applies. I have no proof for this family and no counterexample.
   I think it is the right next test case: it is the first place where a new idea is needed,
   and it is small enough that a uniform argument, if one exists, should be visible on it.

4. REMARK (sketch only, not written out or checked). Counting positions whose window has at most
   k events, instead of none, should give an inequality of the shape
   e <= d + (d + 1) E/(k + 1) + (number of k-event patterns, about (C d)^{k+1}) + (positions at
   high slope), so a link much longer than d^{k+1} needs about k + 1 events per window or must
   climb. This says nothing at the target scale e of order d, so I did not pursue it.

No proved advance on the 12m/5 target. Nothing of mine is committed.
