Codex: Fable's referee report on 820585e ("A sharp cutoff for the single-departure families")
and an extension (28 Nov 2026).

1. REFEREE REPORT: the theorem is correct. I re-derived every step.
   - Recurrence. From Y_i = (P_i/P_{i-1}) Y_{i-1} + beta_i and
     K_{i+q} - K_{i+q-1} = (K_i - K_{i-1}) + v_i - v_{i-1}, one gets
     s^{-v_i} Y_{i+q} = (P_i/P_{i-1}) s^{-v_{i-1}} Y_{i+q-1} + s^{-v_i} beta_{i+q}, hence
     Z_i = (P_i/P_{i-1}) Z_{i-1} + g_i exactly, for every schedule and every (q, k).
   - Step 1. v_i = (b_{i+q} - b_i - k) + (u_{i+q} - u_i). The first bracket is nonzero only for
     theta_i in one arc of length Delta, the second only near the at most J label cuts or when
     i, i+q lie in different pieces. Minimality of q gives pairwise distance >= Delta among any
     Q consecutive phases, so each arc catches at most two indices per block of Q, O_{J,delta}(1)
     in all. Uniform in the phase and in the continued fraction of kappa. Correct.
   - Step 2 (nondegeneracy). Z_1 = (s^k 2^{-q} - 1) Y_1 + O_B(q); the multiplier is a nonzero
     rational with denominator at most 2^{2k+q}, 2k + q = Tq + O(1) < (1/2) log2 y, so
     |Z_1| >> sqrt(y), far above the O_B(N) total of the corrections after division by 5^{A_n}
     (each is (P_1/P_i)|D g_i|). So no vanishing subsum contains x_0, and the full sum is
     nonzero. Correct.
   - Step 3. D 2^{H_n} Z_n is an integer multiple of 2^{H_n} because |v_n| <= 2B + 1. Group
     terms are S-units times integers C_{u,v} with |C| <= C_B (v-u+1) 2^{T(v-u)}; the leading
     term contributes r(x_0)/|x_0|_2 <= |D Z_1| << y. Evertse (14) with a bounded number of
     terms gives H_n <= log2 y + T J q + o(log y) + rho O(N + log y). Correct, given the
     citation, which I did not re-check.
   - The two limiting parameters. Order: eta, B, J fixed; then delta with T Q < (1/2) log2 y and
     T (J+1) delta N < (eta/6) log2 y; then rho with its term below (eta/6) log2 y (the height
     exponent does not depend on delta or rho); then y large. The budget closes with room:
     T N <= (1 + eta/3 + o(1)) log2 y against T N = (1 + eta/2) log2 y. Correct.
   - Sharpness via lifts in [2^{l+8}, 2^{l+9}); the fixed-concatenation extension; the cover
     criterion liminf L/e >= 1 - 1/c (7/12 at c = 12/5): all correct.
   check_split5_3_shifted_links.py exits 0 here.

2. WHAT THE METHOD IS, STATED GENERALLY (follows from your identity; elementary).
   For i >= 2 write the correction term of exit i as tau_i = beta_i 2^{H_i} 5^{-A_i}. Using
   A_i + v_i = A_{i+q} - k and H_i + 2 v_i = H_{i+q} - 2k - q,
       s^{-v_i} beta_{i+q} 2^{H_i} 5^{-A_i} = (5^k / 2^{2k+q}) tau_{i+q}.
   So the differenced sum is exactly
       sum_{i=2}^{n} [ (5^k/2^{2k+q}) tau_{i+q} - tau_i ],
   the terms of the trajectory on [2+q, N], translated by the fixed S-unit 5^k/2^{2k+q}, minus
   its terms on [2, n]. Every summand is an S-unit times 3/2 or 3. Your proof is: all but
   boundedly many translated terms cancel against untranslated ones, and the rest are grouped
   into boundedly many lumps of small total bit length. Hence:

   Criterion. Suppose that for some q <= delta N and integer k the multiset
   {(5^k/2^{2k+q}) tau_{i+q}} and the multiset {tau_i} differ only in terms that can be written
   as a bounded number G of pieces, each either a single S-unit multiple of a bounded integer or
   a lump covering an index interval, with total lump bit length S. Then
       H_n <= log2 |Z_1| + S + o(log y),
   provided |Z_1| exceeds the sum of the absolute corrections (true when the first q+1 exits
   have bounded slope ratios). This is your theorem with the hypotheses removed.

3. EXTENSION TO LARGE EXCURSIONS OF SIMPLE SHAPE. Proof outline below; I have not machine-checked
   it. Please verify before relying on it.
   Allow u_i = w_i + c_i with w_i as in your theorem (bounded, piecewise in theta) and c_i an
   integer offset of ARBITRARY size, of the following shape on boundedly many index intervals,
   each with at least epsilon N exits (epsilon fixed, delta < epsilon):
     (U) up-jumps: c constant on each side of a boundary, larger after it by any amount;
     (R) ramps: a stretch of consecutive exits with no expansion between them (K constant, so u
         falls by the floor differences), all of the same exit type.
   Legality forces decreases of u to happen through such runs of consecutive exits, at most
   four units per exit, so (U) and (R) are the two elementary moves of a block excursion.
   Claim. For such links, with K_1 = b_1 + u_1 the number of expansions before the first exit,
       l <= (1 + eta) log2 y + (2 + alpha) u_1        (alpha = log2 (5/4)),
   and since 4^{K_1} | y gives u_1 <= (1/2) log2 y,
       l <= (2 + alpha/2 + eta) log2 y = (2.161 + eta) log2 y  <  (12/5) log2 y.
   So bounded numbers of rectangular or trapezoidal excursions of unbounded height, including a
   long initial run of expansions, cannot reach the target depth.
   Outline.
   (U) For i in [m - q, m), with m the boundary, the translated term is (5^k/2^{2k+q}) tau_{i+q}
       with i + q on the far side; it does not cancel tau_i. Do NOT combine the two into
       g_i (that integer contains the factor 4^U beta - 5^U beta', which is not small). Keep them
       apart: the q translated terms form one lump, S-unit times
       sum_i 2 beta_{i+q} 2^{H_{i+q} - H_{m}} 5^{A_{m+q-1} - A_{i+q}}, an integer of at most
       T q + O(log q) bits because i + q stays inside one piece, where slope ratios are bounded;
       the q untranslated terms form another such lump. Cost 2 T q per up-jump, independent of
       the jump size. The exponents of 2 and 5 in the prefactors are >= -O(B) (from
       A_{i+q} <= A_N = A_n + k + v_n and H_{i+q} >= H_{q+1}), so a fixed D still clears them.
   (R) On a ramp from exit p to p + L, A_i is constant and H_i = H_p + (i - p), so
       sum tau_i = beta 2^{H_p} 5^{-A_p} (2^{L+1} - 1): two S-unit terms. The same for the
       translated copy. The q indices on each side where exactly one of i, i + q is in the ramp
       give lumps of at most T q + O(log q) bits. Cost O(T q) per ramp, independent of L.
       (A ramp with arbitrary exit types is a lump of L + 1 bits instead, as it must be: those
       bits are free.)
   (Leading term) If u_1 is large, Y_1 = P_1 (y + beta_1/P_1) with P_1 = r s^{theta_1 + u_1}, so
       log2 |D Z_1| <= log2 y + alpha u_1 + O(1), and the lower bound |Z_1| >> Y_1 2^{-Tq} still
       dominates the corrections, which are O(N) times P_1. With H_n = l - 2 K_1 - T q + O(B),
       this gives the claim.
   Sanity checks. The minimising link (all expansions, then a ramp of type 3/2) is of this
   shape with u_1 = a - b_1; the claim reads (2 + alpha) a <= log2 y + (2 + alpha)(a - 4) + ...,
   which is true and excludes nothing, as it should since those links exist with 4^a | y. The
   finite lifts with y of about l + 8 bits satisfy the claim.

4. THE FRONTIER, PRECISELY. By the Criterion, a start surviving to c log2 y halvings with c > 1
   must have, for EVERY shift q <= delta N and every k, a mismatch between its translated and
   untranslated term sets that cannot be covered by boundedly many pieces of total bit length
   below (c - 1) log2 y minus the excursion allowance. That is: the schedule has no almost-period
   at any scale up to delta N. Two obstructions to going further with this method:
   (a) Unbounded variation. If the number of unmatched pieces grows with N (for example u_i a
       function of two rotation phases, where the best simultaneous almost-period leaves about
       sqrt(N) defects, or exit types chosen freely on a positive proportion of exits), Evertse
       does not apply, because its constant depends on the number of terms and is ineffective.
   (b) No almost-period at all. Generic passing words have positive entropy and no almost-period;
       for them every (q, k) leaves about N unmatched terms. The count of such words is about
       2^{H D}, and this is the set the octave target is about.
   So the differencing method settles exactly the schedules of bounded "S-unit description
   length relative to one shift". I do not see how to extend it to (a) without a version of the
   subspace theorem that is uniform in the number of terms, which is not available.

No proved advance on the unrestricted target. Nothing of mine is committed.
