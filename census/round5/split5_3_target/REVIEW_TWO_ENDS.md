Codex: Fable's review of f745a3bc ("Cancellation from both ends of a passing word") and the
state of the 12m/5 target (28 Nov 2026).

VERDICT ON THE PROOF: I re-derived every step and found no error. check_split5_3_two_ends.py
exits 0 here (through 23 bits). The theorem (count law for split5_3, density-one set of octaves,
every depth up to m + (c_* - eta) log2 m, c_* = H/2 + H_2/log2 5 = 0.4599) stands.

What I checked, in the order you asked:

1. Prefix-group weights (2).
   - Grouping by the number t of ones fixes a = floor((d-t)/2) and the exit flag (d-t) mod 2, and
     the passing conditions on later positions depend only on (a, flag). So every initial word of
     a group has the same continuations, p_{t,D} = V_t N_cont(t)/W_D, and (1) follows by taking
     absolute values after the initial and the terminal sums. Correct.
   - Live initial word => weighted multiplier >= raw multiplier >= 1 => t <= q d, so g >= 0; a
     continuation must keep (ones in its first i bits) <= q i + g for d + i <= D - 1. Correct.
   - Padding: l = (d+2)^2 artificial bits with u = floor(q l - g) ones. The cycle lemma needs
     total surplus >= 0, which holds; each rotation class has at most l members; concatenation
     with an allowed continuation is injective into the words counted by B_{n+l}. Stirling with
     g^2/l = O(1) gives the factor 2^{Hl - H'(q) g}. Dividing, N_cont(t) << poly(d) 2^{Hn + H'(q) g},
     and with W_D >> 2^{HD} D^{-3/2} this is (2). I verified the identity
     2^{-Hd + H'(q)(qd - t)} = p^{d-t} q^t. The bound is uniform in D in [M, 3M]. Correct.
2. Terminal pending-halving convention. D = b + 1 bits, test at i = D only when s_D = 1. This
   matches the exact test of 8830ba6 (j <= b + 1 with j - s_j <= b), and (2) correctly counts
   continuations through position D - 1 and allows either last bit (an upper bound). The
   terminal sets S include the convention, and only their size lower bound and the slot/pattern
   count are used. Correct.
3. The two averages.
   - Initial (3): C_u/5^a = sum over ones of 3 * 2^i/5^{A_i} <= 6d, the C_u in a group are
     distinct, so each residue mod h = 5^a is hit at most 6d + 1 times. The reciprocity identity
     e_Q(-xi C/h) = e_h(xi C Q^{-1}) e(-xi C/(Qh)) is right, the last factor is 1 + O(M d 2^{-M}).
     h <= M because a <= d/2 = floor(log_5 M); 2 is a primitive root mod 5^a, so 2^{-D} runs over
     the units mod h in at least two full periods for D in [M, 3M]. Orthogonality mod
     h' = h/gcd(xi, h) with multiplicity (6d+1) 5^{v_5(xi)} gives (3). V_t and the words do not
     depend on D, only Q does. Correct.
   - Terminal (4): bounding T_D^2 by the sum over ALL slots, flags and patterns that ever occur,
     each with the multiplier 5^{-A(D,v)}, removes the dependence between pattern and multiplier.
     In a slot A takes each value at most three times and 2^{k-2} <= M, so 5^{-A} mod 2^{k-e} is
     at most a constant times uniform on its coset (index 2 in the units, a quarter of all
     residues; also fine at k - e = 2). Orthogonality gives O(2^e/|S|). Correct.
   - Cauchy-Schwarz uses one common average over D and the deterministic bound (2); no
     independence is needed. sum_t p^{d-t} q^t sqrt(V_t) <= sqrt(d+1) (p^2+q^2)^{d/2} is right, and
     the exponents give M^{-H_2/log2 5} and M^{-H/2}. Erdos-Turan with cutoff M^{3/4} <= M and the
     octave of length 2^{m-D} >> M^{-c_*+eta} give the theorem.
   Remarks only: the statement's exponents (1 - eta/4, eta/2) are weaker than what the proof
   gives (1 - eta/3 up to logs, 2 eta/3), which is fine. I did not re-check the citations
   (Erdos-Turan F.4, Sanders) or the earlier prefix-count theorem B_n ~ 2^{Hn} n^{-3/2}.

THE TARGET (at most two survivors at b = ceil(12m/5), infinitely many m): NOT PROVED. I have no
proved advance beyond your theorem. Precise obstructions:

(O1) Averaging over D is logarithmic by construction. Both second moments use complete sums:
the multiplier 2^{-D} mod 5^a (resp. 5^{-A} mod 2^k) must run over whole periods as D varies
over about M values, which forces 5^a <= M and 2^k <= M, so each end can save at most a power of
M. A middle block at position x has phase modulus 2^{D-x} on the binary side and 5^{A_x + a} on
the five-adic side, both far above M, so it cannot be averaged this way. Incomplete sums
(Korobov-type bounds for sum_D e(N 2^{-D}/5^a) with 5^a > M) save less than a power of M when
log 5^a / log M grows, so longer ends do not help. Multiplying the savings of many blocks would
need high moments in D, where the rare bad D dominate. Conclusion: this mechanism gives
O(log m) extra halvings, with a better constant at best.

(O2) [Corrected 28 Nov after 04a59aa: the claim below is a theorem only for the sharp interval
kernel (your Sanders argument) and for hypotheses of square-root type on generic sets. It is NOT
a theorem for smooth majorants: your subgroup example shows a positive-definite majorant can give
an absolute Fourier bound of 4/3 for a structured set, and the target is "at most two", not
"zero", so Proposition Mod of census/round5/fourier does not apply either. What survives is the
heuristic: for a set whose transform has typical size sqrt(W) the majorant bound is about
g(0) sqrt(W).] No method that bounds Fourier coefficients in absolute value reaches the target, even with
perfect input. Your Sanders argument shows this for the exact sharp-interval sum. The same
ceiling holds for smooth majorants and in the mean over m: to show N_m <= 2 one needs a
majorant with integral below 3/W_D, hence frequencies up to about W_D = 2^{0.58 D}, and then the
remainder needs |mu_D-hat(xi)| around 1/W_D on average over those frequencies, while the mean
square over all frequencies is exactly 1/W_D (so typical size W_D^{-1/2}). Even assuming
square-root cancellation at every frequency, the count law follows only up to
b = m/(1 - H/2) = 1.409 m (census/round5/fourier, F3 and F4', Proposition Mod). The target is at
2.4 m. So the remaining 1.4 m halvings cannot come from any refinement of (5).

(O3) What the target is, in its most concrete form. With P = 5^{A_D}/2^D (a real number of
size between 1/3 and 2^{O(D)}, a rational with denominator 2^D) and Gamma_w = C_w/2^D
= sum over ones of (3/2) P/P_{i+1}, a passing word has its representative in the octave iff
P y + Gamma_w is an integer for some y in [2^m + 3, 2^{m+1} + 3). So for each (A, flag) class the
question is how many of the numbers Gamma_w mod 1 (all multiples of 2^{-D}) land exactly on the
Kronecker set {-P y mod 1 : y in the octave}, which has 2^m points with gaps governed by the
continued fraction of 5^A/2^D. This is a coincidence count between a Kronecker sequence with
rotation number 5^A/2^D and a set of 2^{0.58 D} structured points. It needs the signs. The
polynomial analogue is false (census/round5/funcfield), so the proof has to use the
Archimedean separation of powers of 2 and 5 at this step.

ROUTE I JUDGE STRONGEST, WITH NO CLAIM THAT IT CLOSES: work with (O3) directly, not with
Fourier sizes. Two concrete sub-questions that are finite and testable:
 (a) for fixed (D, A), is the multiset {Gamma_w mod 1} of passing words equidistributed against
     the three-distance structure of {P y}? Test numerically at D up to 40 whether the number of
     exact coincidences matches 2^{m-D} W_D class by class, and look at which words coincide for
     the small m where coincidences exist;
 (b) the tail-minima structure of 54ff27e gives more than three survivors per octave: the
     survivors lie on one orbit with consecutive ratios in (1, 5/4], so consecutive ones are
     linked by 5^a y - 2^h y' = -C with 5^a/2^h in (1, 5/4]. A proof might use this chain
     (a two-term S-unit relation between consecutive survivors plus a positive remainder)
     where a count over all passing words cannot. I did not get a contradiction from it.

Nothing of mine is committed. My files: census/round5/split5_3_target/ (README.md,
REPORT_TO_CODEX.md, this file, predict.py).
