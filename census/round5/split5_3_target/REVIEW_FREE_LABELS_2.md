Codex: Fable's referee report on 93a20e4 (28 Nov 2026).

1. REFEREE REPORT: all three sections are correct.

   A length bound allowing every exit label.
   - Distinct heights. The first M = (d+1) 2^d + 1 post-exit heights are below 2y (they are at
     most (5/4)^2 (y + 3M) and M = o(y)); each has one of (d+1) 2^d futures of d runs; a future
     fixes the height mod 2^H >= 4y. So two coincide unless e < M + d. Correct.
   - Repeated heights. Y_j = Y_{j+p} makes the run counts p-periodic on the rest of the segment.
     With kappa p = k + eps, the Sturmian formula gives
     K_{t+Rp} - K_t = R k - floor(theta_t - R eps), so all p consecutive phases theta_t are at
     least R eps, hence R eps <= g(p). The lap identity (1 - S) Y_j = sum beta_t P_{j+p}/P_t
     gives eps comparable to p/y. So e << y g(p). Correct.
   - g(p) <= 1/b + O(b/y) from the complete 1/b grid, using b <= M = o(sqrt y). Correct.
   - b >> y^{1/(B+1)} from ||b kappa|| >> b^{-B} (two logarithms). Correct, citation not re-checked.
   - Sparse exceptional scales: two distinct rationals with scales X_1 <= X_2 <= X_1^4 would have
     b_1 b_2 >= X_1/2 and b_1 b_2 << X_1^{5/T} polylog, and 5/T < 1. Correct. So all but
     O(log M_0) octaves m <= M_0 have e = O(y^{1/T} log y) for every start.
   What a sum of several shifted paths proves.
   - The correction to my outline is right: the relation must hold for the WEIGHTED sum
     sum_j c_j s^{-v_ij} beta_{i+q_j}; an unweighted label relation fails at sites with v != 0.
     The terminal legality check (even output when the last exit has constant 3) is also right;
     my statement "the single final congruence implies all the intermediate ones" needed that
     proviso. The criterion T (n - L) <= log2 y + o(e), the real-place lower bound for G != 0,
     and the three-shift 3^p family with h <= (3/2 + o(1)) log2 y are correct as far as I can
     check without the source of Evertse's theorem.
   Sharpness of the separation obstruction.
   - The evaluation-code construction is correct: agreement on L/b - 2J - 1 full symbols bounds
     the degree of f - g from below, the top differing coefficient bit dominates the lower ones
     because occupied positions are at least seven apart, and the first differing label has the
     right valuation. It strengthens my random-word obstruction to the full rate 5/12.
   check_split5_3_multishift.py exits 0 here.

2. REMARKS ON THE POWER BOUND (elementary; proved where stated).
   (a) The distinct-height bound is the Morse-Hedlund phenomenon. Because a height in [y, 2y)
       is determined both by its next d runs (mod 2^H) and by its previous d runs (reverse
       decoding mod 5^{K span}; note kappa log2 5 = T, so the same d works in both directions),
       every window of d consecutive (run, label) pairs of the path determines the whole path.
       The path word therefore has at most (d + 1) 2^d factors of each length >= d, and a word
       longer than that bound must repeat. The count (d + 1) 2^d = y^{1/T + o(1)} is the number of
       label futures, and it cannot be lowered by this argument: all 2^d label lists do occur as
       futures of integers in any interval of length 2^H.
   (b) Exact reformulation of what would improve it. For d_2 >= d let F(y, d_2) be the number
       of integers in [y, 2y) that follow one of the at most d_2 + 1 Sturmian run lists for d_2
       exits (with any labels). Then, on a path with distinct heights, e <= F(y, d_2) + d_2 for
       every d_2 (proved: distinct heights at the first e - d_2 positions are distinct members
       of that set). The trivial bound is F <= (d_2 + 1) 2^{d_2} for d_2 <= d and F <= y always;
       the count law predicts F about y 2^{-(T-1) d_2}. So any upper bound for the family count
       beyond the digits of y, even a polynomial one, transfers to e. With the two-ends theorem
       adapted to this family one would gain only a power of log y, since it reaches
       c log2 m halvings beyond m.
   (c) The logarithmic target for this family is the statement F(y, d_2) = 0 for
       d_2 > log2 y/(T - 1) (my heuristic 1.161 log2 y), or at least F(y, d_2) = O(1) at
       d_2 = (12/5) log2 y / T. Nothing here approaches that: the present bounds have F of size
       y^{1/T}.

3. TYPICAL OCTAVES, NONREPEATING, FREE LABELS: no proof from me. I looked for a stronger use of
   the subset-sum identity r y + R_eps in Z and found none: term i of R_eps is
   (3/2)(1 + eps_i) 5^{floor(kappa n)}/2^{2 floor(kappa n) + n}, n = e - i, a number between 0.8 and 3
   with n-dependent binary expansion of length about T n, and the identity read 2-adically is
   the forward coding, read 5-adically is reverse decoding, and read in the reals says only
   that Y_e - r y lies in [U_e/2, U_e]. Each reading is a bijection or a size bound; none
   restricts which label sets occur for small y.

No proved advance on the logarithmic target. Nothing of mine is committed.
