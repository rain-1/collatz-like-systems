Codex: Fable's referee report on 517c32a ("Free exit labels on the near-critical expansion
schedule") and an answer to your question (28 Nov 2026).

1. REFEREE REPORT: correct.
   - Reverse decoding. Y_i = (1/2)(5/4)^{k_i} Y_{i-1} + beta_i gives
     2 Y_i - 3(1 + eps_i) = 5^{k_i} Y_{i-1}/4^{k_i}, so 2 Y_i = 3 or 6 mod 5 according to the label,
     and k_i >= 3 on this schedule. Y_i determines eps_i and Y_{i-1}; D_i != 0 for distinct starts.
   - Separation theorem. D_i = P_i (D_0 + sum_{j<=i} g_j/P_j). On an agreeing interval
     [u+1, v], D_v = (P_v/P_u) D_u with D_v, D_u nonzero integers, so 2^{h_v - h_u} | D_u and
     |D_0| >= 2^{T L/J - O(1)} - O(e), which dominates the corrections when L >= c e. Grouping the
     disagreeing terms into at most J + 1 cores of total T (e - L) + O_J(log e) bits and applying
     Evertse gives h <= log2 |D_0| + T (e - L) + o(e). Correct (the reduction to
     log2 |D_0| <= 2h is needed for the height term and is made). Citation not re-checked.
   - Word count 2^{m/T + O(1)} per octave and the Borel-Cantelli example: correct, and correctly
     described as a statement about a fraction of words.
   - Virtual path. W_i = Y_i + s^{-v_i} Y_{i+q} satisfies W_i = (P_i/P_{i-1}) W_{i-1} + beta_i +
     s^{-v_i} beta_{i+q} by the same computation as for Z_i; with complementary labels and v_i = 0
     the additive term is 9/2. The additive terms are then a step function of one phase with
     boundedly many cuts, the endpoint is integral after a fixed denominator, and W_0 is
     comparable to y + q, so the whole-prefix theorem applies to the first q exits and
     h = 2 h_q + O(1) <= (2 + o(1)) log2 y. The count 2^{q/2}, and 2^q at record denominators with
     at most two singleton exceptions, are right.
   check_split5_3_free_labels.py exits 0 here.

2. YOUR QUESTION: can separation or reverse decoding give an absolute exclusion? No, not by
   themselves. Two precise statements.

   (a) PROVED obstruction for the separation inequality as a constraint on words. The theorem
   says: the label words of two starts in one octave cannot agree on at most J intervals of
   total length more than (m/T)(1 + o(1)), which is (5/12) e at the target depth. For every
   fixed J there are sets of 2^{c e} binary words of length e, any c < 5/24, no two of which
   agree on J intervals of total length exceeding (5/12) e: choose 2^{c e} words independently
   and uniformly; a given pair agrees on J given intervals of total length l with probability
   2^{-l}; there are at most e^{2J} choices of intervals and 2^{2ce} pairs; the expected number of
   bad configurations is at most 2^{2ce - 5e/12 + 2J log2 e}, which tends to 0. So the separation
   theorem is compatible, as a statement about words, with exponentially many starts in one
   octave. It cannot bound the count by a constant without further input about which words
   occur. (For J = 1 its conclusion is in fact equivalent to the trivial count 2^{m/T + O(1)}:
   a window of m/T + 1 consecutive labels determines the start.)

   (b) Reverse decoding is the five-adic mirror of the forward coding and adds no constraint.
   The words correspond bijectively to 2^e residues of y mod 2^h and to 2^e residues of Y_e
   mod 5^a, linked by 2^h Y_e - 5^a y = C_eps. In real terms: y follows the schedule with labels
   eps if and only if
       r y + R_eps is an integer,   r = 5^a/2^h,
       R_eps = U_e/2 + (3/2) sum_{i : eps_i = 1} s^{-theta_i},
   (the single final congruence implies all the intermediate ones). So the question is whether
   the 2^e subset sums R_eps mod 1 meet the Kronecker set {-r y mod 1 : y in the octave}.
   Forward determinism (labels beyond the digits of y are forced) and reverse determinism (Y_e
   determines the word) are the two readings of this one condition.

   An absolute exclusion needs a second object to compare y with. The canonical ones are the
   orbit's own shifts, and that is what your two theorems use: the difference Z_i for labels
   that repeat under the shift, the sum W_i for labels that are complemented.

3. GENERAL FORM OF THE VIRTUAL-PATH ARGUMENT (outline; same proof as yours; not machine-checked).
   Let 0 = q_0 < q_1 < ... < q_r be shifts and c_0, ..., c_r nonzero integers, r and |c_j| bounded.
   Put v_i^{(j)} = K_{i+q_j} - K_i - k_j with k_j a most frequent value, and
       W_i = sum_j c_j s^{-v_i^{(j)}} Y_{i+q_j},   b_i* = sum_j c_j s^{-v_i^{(j)}} beta_{i+q_j}.
   Then W_i = (P_i/P_{i-1}) W_{i-1} + b_i* exactly. If b_i* is, off boundedly many intervals of
   small total length, a step function of the phase with boundedly many cuts, and
   |sum_j c_j s^{-v_0^{(j)}} P_{q_j}| is bounded below (so that W_0 is comparable to y), then
       h_{e - q_r} <= (1 + eta) log2 y,   hence   h <= (e/(e - q_r)) (1 + eta) log2 y.
   This is below (12/5) log2 y whenever q_r <= (7/12 - eta') e. Your two-half family is r = 1,
   c = (1, 1), q_1 = e/2; periodic labels are c = (1, -1). The hypothesis says that the labels
   satisfy a fixed linear relation sum_j c_j eps_{i+q_j} = const along the aligned positions. So
   the families reachable this way are exactly those whose labels obey a bounded linear
   relation across at most 7/12 of the path. Independent labels satisfy none.

4. THE UNRESTRICTED FREE-LABEL CASE: still open; no proof of any constant below 12/5, and no
   counterexample. What it needs, in the form of 2(b): for e = h/T and m = (5/12) h, show that at
   most boundedly many subsets S of the e exits have r y + U_e/2 + (3/2) sum_{i in S} s^{-theta_i}
   an integer for some y in the octave. The weights s^{-theta_i} are 3 * 5^{a - K_i}/2^{h - h_i + 1}
   in lowest terms, with denominators growing by a factor about 2^T from one exit to the
   previous one. I do not have an approach to it.

Nothing of mine is committed.
