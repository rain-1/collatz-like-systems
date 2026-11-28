# Theorem W: the whole-prefix shift-and-subtract cutoff for any two-prime affine path

Round 6, lens `cutoff_wide`. This ports the split5_3 theorem "Large jumps and stretches of
consecutive exits" (round2/rewriting/split5_3_s27.md, lines 919-976) from one map to every
path of affine steps whose slopes are products of powers of two primes. The proof is the same
argument as there, with each split5_3-specific fact replaced by a stated hypothesis. Instances:
`check_cutoff_instances.py` (15 table systems) and `check_mb_s3_27.py` (the blocked mixed-base
system).

Status: **PROVED**, using Evertse's theorem quoted in section 4 (statement verified against
the scanned source by referee 1; see section 4). The constant is **ineffective**.

**Revision after REFEREE1.** Changes in this file, all marked in place:

* two hypotheses added: (H0) bounded division count per step, and (H3) required for every prefix.
  The truncation step of the proof used both. Every instance satisfies them;
* the count of S-unit terms corrected (J·(2/delta) short-piece singletons, not 2/delta);
* Lemma R: the window count corrected to 2/delta + 1, and the exception count argued with
  half-open arcs. The stated M(delta) is unchanged;
* split5_3 standard-exit rate corrected: kappa = log 2 / log(5/4) = 3.1063, not 6.2126;
* **withdrawn:** the statement "cycles fail (H2)". Expanding integer cycles satisfy
  (H0)-(H4) from bounded starts. Theorem W is consistent with them only because its threshold
  y_* is ineffective and must exceed every such start (section 6 and
  `check_cutoff_instances.py`);
* section 4: the Evertse display is no longer "quoted from memory".

## 1. Setting

Fix distinct primes p (the denominator prime) and l (the numerator prime). A **step** is an
affine map

    phi(y) = (l^a y + c) / p^e,      a in Z,  e >= 0,  c in Q,

and its slope is l^a / p^e. A **path** is a sequence of steps phi_1, ..., phi_n with values
y_0, y_1 = phi_1(y_0), ..., y_n. All y_j are rationals whose denominators divide a fixed
integer D_0 prime to p. (Shifted coordinates y = n - x* around a rational periodic point
x* need this.)

Write A_j and E_j for the cumulative exponents after step j, so P_j = l^{A_j} / p^{E_j} is the
**prefix slope** and E = E_n is the total number of divisions. The **events** are the steps with
c != 0, at indices j_1 < ... < j_N. For event i put

    tau_i = c_{j_i} / (l^{a_{j_i}} P_{j_i - 1}) = c_{j_i} p^{E'(i)} / l^{A(i)},
    E'(i) = E_{j_i} - e_{j_i},     A(i) = A_{j_i}.

Iterating y_j / P_j = y_{j-1} / P_{j-1} + c_j / (l^{a_j} P_{j-1}) gives the **whole-prefix
identity**

    y_0 + sum_{i=1}^N tau_i = y_n / P_n = p^E y_n / l^{A_n}.                        (1)

Since y_n and l are p-adic units or integers, |y_0 + sum tau_i|_p <= p^{-E} |D_0|_p^{-1}.

## 2. Hypotheses (constants C >= 1, J >= 1 and a function M(delta) are fixed)

* **(H0) Bounded steps.** e_j <= C for every step j. (Added after REFEREE1. A block C^k is
  split into k steps C, so this holds for every cylinder-graph or block path used here.)
* **(H1) Labels.** Every c_{j_i} lies in a fixed finite set Lambda of nonzero rationals.
* **(H2) Non-descent at events.** |tau_i| <= C for every i. This holds if every prefix slope at
  an event is at least 1/C, for example on any non-descending path.
* **(H3) Density and size, for every prefix.** For every j, the number N_j of events among
  steps 1..j satisfies N_j <= C(E_j + 1), and |A_{j'}| <= C(E_j + 1) for all j' <= j. (Revision
  after REFEREE1: originally stated for the whole path only, which is not inherited by
  prefixes. In every instance each event divides, so N_j <= E_j, and |A_j| = O(E_j) because
  the cylinder graph has no division-free cycle.)
* **(H4) Pieces.** The event indices 1..N split into at most J consecutive pieces. On each
  piece I, for i < i' in I,

      0 <= E'(i') - E'(i) <= C(i' - i + 1)   and   |A(i') - A(i)| <= C(i' - i + 1)

  (bounded geometry; arbitrarily large jumps are allowed *between* pieces). Each piece is of
  one of two kinds:
  * **shift piece** (hereditary shift invariance): for every subinterval I' of I and every
    delta in (0, 1/4) with |I'| >= 2/delta there are q, 1 <= q <= delta|I'|, and integers
    k_A, k_E with k_E >= 1, |k_A| <= Cq, k_E <= Cq, and gamma = l^{k_A} / p^{k_E} with
    |log gamma| <= C, such that c_{j_{i+q}} = c_{j_i}, A(i+q) - A(i) = k_A and
    E'(i+q) - E'(i) = k_E for all i in I' with i + q in I', except at most M(delta) indices i;
  * **geometric piece**: there is a period pi <= C with c_{j_{i+pi}} = c_{j_i} and with
    (A(i+pi) - A(i), E'(i+pi) - E'(i)) a constant nonzero vector on the piece.

On a shift piece the condition gives tau_{i+q} = gamma^{-1} tau_i for every non-exceptional i.

## 3. Theorem W. PROVED (conditional on Evertse, section 4)

**Theorem W.** For every eta > 0 there is y_* = y_*(eta, p, l, C, J, M, Lambda, D_0) such that
every path satisfying (H0)-(H4) with |y_0| >= y_* has

    E <= (1 + eta) log_p |y_0|.

The bound holds uniformly over all such paths: jump sizes, piece locations, rotation phases and
labels are all free. The coefficient 1 is sharp for every family of paths that contains words
of every length. A word with E divisions in a cylinder graph G_K is followed by one residue
class mod p^{K+E}, and its least positive member y satisfies E >= log_p y - K.

*Proof.* Suppose not. Then there are eta > 0 and paths with |y_0| -> infinity and
E > (1 + eta) log_p |y_0|. Truncate each path after the first step with
E_j >= (1 + eta/2) log_p |y_0|. Truncation keeps (H0)-(H4). (H0), (H1) and (H2) are
conditions on single steps. (H3) is assumed for every prefix. For (H4), the pieces of the
truncated path are the old pieces, with the last one cut short. A sub-interval of a shift
piece is a shift piece, because the shift condition is required for all of its
subintervals. A sub-interval of a geometric piece is a geometric piece. By (H0),
(1 + eta/2) log_p|y_0| <= E <= (1 + eta/2) log_p|y_0| + C, and by (H3) for this prefix
N = O(log |y_0|). Write y = y_0 and Y = y_n.

*Step 1 (the factor).* Fix delta in (0, 1/4), to be chosen. Shift pieces with fewer than 2/delta
events are treated as singletons. On each remaining shift piece pi choose (q_pi, gamma_pi) from
(H4). Put F = prod_pi (1 - gamma_pi), a product of at most J factors. Each factor is nonzero:
k_E >= 1 gives l^{k_A} != p^{k_E} by unique factorization. Moreover

    |1 - gamma_pi| >= p^{-k_E} l^{-max(0, -k_A)} >= p^{-C' q_pi},

because 1 - gamma is a nonzero integer divided by p^{k_E} l^{max(0,-k_A)}. Here
C' = C(1 + log l / log p). Since q_pi <= delta N = O(delta log |y|),

    |F| |y| >= |y|^{1 - O(J C' C delta)} >= |y|^{1/2}                              (2)

for delta small enough, depending only on (C, J, p, l).

*Step 2 (pairing inside a shift piece).* Let I = [u, v] be a long shift piece with shift q and
ratio gamma. Then

    (1 - gamma) sum_{i=u}^{v} tau_i = sum_{i=v-q+1}^{v} tau_i - gamma sum_{i=u}^{u+q-1} tau_i
                                       + sum_{i=u}^{v-q} (tau_i - gamma tau_{i+q}).

Every term of the last sum vanishes except at the at most M(delta) exceptional indices, whose
two terms are kept as separate singletons. Each end sum is a single integer multiple of an
S-unit:

    sum_{i=s}^{s'} tau_i = p^{E'_min} l^{-A_max} Core,
    Core = sum_i c_{j_i} p^{E'(i) - E'_min} l^{A_max - A(i)},

taken over at most q consecutive events of the piece. By bounded geometry (H4) and (H1),
D_1 Core is an integer with |D_1 Core| <= C_1 (q + 1) p^{C' C q}, where D_1 is a common
denominator of Lambda.

*Step 3 (geometric pieces).* On a geometric piece with period pi, split the events into the pi
residue classes. Along a class, tau_{i+pi} = g tau_i with g = p^{k_E} / l^{k_A} != 1, so the
sum is tau_first (1 - g^T)/(1 - g) = (tau_first - g tau_last)/(1 - g). Both endpoint terms are
at most C in size by (H2). Only finitely many g are possible, because pi <= C and the vector is
bounded by (H4). A fixed integer therefore clears every 1/(1 - g). Each class contributes two
S-unit terms with bounded prime-to-S parts.

*Step 4 (the S-unit equation).* Multiply (1) by F. Use Step 2 for the factor (1 - gamma_pi) of
the piece's own sum, and expand the other factors prod_{pi' != pi} (1 - gamma_pi') into signed
monomials. Do the same for singletons and geometric terms. The result writes F(y + sum tau) as
x_0 + sum_{j >= 1} x_j, where:

* x_0 = F y is the leading term;
* there are at most n_terms = 1 + 2^J (2J + 2J M(delta) + 2J C + 2J/delta) correction terms.
  The last summand counts singletons from at most J short pieces of fewer than 2/delta events
  each. (Revision after REFEREE1: this read 2/delta. It is bounded either way.)
* each correction term is an S-unit (S = {infinity, p, l}) times either an end core, a
  bounded label, or a bounded geometric endpoint.

Before clearing denominators, the absolute sum of all correction terms is
O_{C,J}(N) = O(log |y|), using |tau| <= C and |gamma| <= e^C. By (2) this is smaller than
|x_0|. Delete zero terms and vanishing subsums until none remain. The leading term survives
every deletion: a vanishing subsum containing it would need correction terms of total size at
least |x_0|.

Clear denominators by one integer Z = D_0 D_1 D_2 p^{a_1} l^{a_2}, where D_2 clears the
geometric denominators and a_1, a_2 = O(E + delta N) by (H3) and (H4). Call the resulting
integers x_j. Their sum is Z F p^E Y / l^{A_n}. Its p-adic norm is at most
p^{-E} |Z F|_p |D_0|_p^{-1}, and |x_0|_p = |Z F y|_p. All ordinary sizes are at most
p^{O(E + log |y|)}, with a constant independent of delta and rho.

Apply Evertse's inequality (section 4) with T = {p} and r(x) = |x| |x|_p |x|_l:

    p^{-E} |ZF|_p / |D_0|_p >= |sum x_j|_p >= c(delta, rho) |x_0|_p H^{-rho} / prod_j r(x_j).

The common factor |Z|_p cancels. The factor r(x_0)/|x_0|_p = |x_0| |x_0|_l is the prime-to-l
part of |ZFy| divided by its p-part. It is at most |y| D_0 D_1 D_2 times the numerator of F,
which is at most p^{O(J C' delta N)}. The end cores contribute at most
2J 2^J (C' C delta N + O(log N)) base-p digits. Singletons and geometric terms contribute O(1)
digits each, and there are O_delta(1) of them. Taking log_p:

    E <= log_p |y| + O_{C,J}(delta N) + O_{C,J,delta}(log(N + 2)) + O(rho (E + log_p |y|))
           + O_{C,J,delta,rho}(1).                                                   (3)

Since N = O(log |y|), choose delta and then rho small enough that the two linear terms total
less than (eta/4) log_p |y|. Then (3) gives E <= (1 + eta/4 + o(1)) log_p |y|. This
contradicts E >= (1 + eta/2) log_p |y| for |y| large. ∎

**Which hypothesis does what.**

* (H0) and (H3) for every prefix let the proof truncate a long path just past
  (1 + eta/2) log_p |y| divisions without losing the hypotheses (added after REFEREE1).
* (H2) keeps the correction terms small, so the leading term (2) is never cancelled.
* (H3) turns the bound into one in log |y|.
* The bounded number J of pieces and the bounded M(delta) keep the number of S-unit terms
  bounded. That is the only uniformity Evertse's constant needs.
* Hereditary shift invariance with q <= delta|I| makes the end cores cost delta N digits.
* k_E >= 1 makes F nonzero.

Without (H2) the statement fails for contracting cycles. A contracting integer cycle (lap slope
< 1), read around an expanding point x*, is a rigid periodic path of unbounded length from a
bounded start. It is excluded only because its tau_i grow.

**Expanding cycles satisfy every hypothesis.** (Revision after REFEREE1; this corrects the
withdrawn claim "cycles fail (H2)".) Take an expanding integer cycle, read in y = n - x*
around the fixed point x* of its expanding branch. For example, take the 3x-1 cycles 5, 7, 10
and 17, ..., 34 around x* = 1, or the 3x+1 cycles -5, -7, -10 and -17, ... around x* = -1.
Such a cycle is one geometric piece with one label. It has |tau_i| <= 1, a bounded start
|y_0| (4 or 16 in these examples), and E unbounded as the number of laps grows. This is
checked exactly by `check_cutoff_instances.py` (function `cycle_check`).

Theorem W is consistent with these cycles only because y_* is ineffective and must exceed
|y_0| for every such cycle. So Theorem W cannot exclude any finite set of cycles, and it gives
no information about cycles at all.

## 4. The external theorem

**Evertse 1984**, *On sums of S-units and linear recurrences*, Compositio Math. 53 (1984),
225-244, Theorem 2 (p. 228). I downloaded the PDF from Numdam and extracted the text of the
statement, but my extraction could not read the displayed inequality (14), which is an image.
**Revision after REFEREE1:** referee 1 rendered pp. 226 and 228 of the Numdam scan as images
and confirmed the display below verbatim (REFEREE1.md, section 1). The display is therefore
verified against the source, by the referee and not by me. The referee also confirmed four
points:

* hypothesis (13) requires every nonempty subsum to be nonzero, singletons included;
* C depends only on (eps, S, K, n);
* for K = Q, the height is ||x|| = max_k |x_k| (eq. (2), p. 226);
* the theorem is ineffective.

> THEOREM 2: Let n be a non-negative integer and S a finite set of primes on K, enclosing
> S_infinity. Then for every epsilon > 0 a constant C exists, depending only on epsilon, S, K, n,
> such that for each non-empty subset T of S and every vector x = (x_0, ..., x_n) in O_K^{n+1}
> with sum_{k in {i_0..i_s}} x_k != 0 for each non-empty subset {i_0, ..., i_s} of {0, ..., n}:
>
>   (prod_{k=0}^{n} prod_{v in S} |x_k|_v) · prod_{v in T} |x_0 + ... + x_n|_v
>        >= C (prod_{v in T} max_k |x_k|_v) · H(x)^{-epsilon}.          (14)

It is used here with K = Q, S = {infinity, p, l}, T = {p}, H(x) = max_k |x_k|, epsilon = rho,
and n + 1 = n_terms bounded in terms of (J, delta, C). After the deletion in Step 4 no nonempty
subsum vanishes, so the hypothesis holds. C is **ineffective**, because the proof goes through
the Subspace Theorem. Hence y_* in Theorem W is ineffective.

## 5. Lemma R: rotation schedules satisfy (H4). PROVED

**Normal form.** Let C be a closed walk of a cylinder graph with slope lambda_C > 1, followed
forever by the rational point x*. In y = n - x*, the walk C acts as y -> lambda_C y, with no
event. Let {X_lambda} be finitely many closed exit walks at the same node, all with the **same
slope** mu = l^{a_X} / p^{e_X} < 1, with e_X >= 1. In y-coordinates each acts as
y -> mu y + c_lambda, with c_lambda != 0 (`check_cutoff_instances.py` (a)). A block word is
C^{k_1} X_{lambda_1} C^{k_2} X_{lambda_2} ...; its events are the exits. The near-critical rate
is

    kappa = log(1/mu) / log(lambda_C).

For an exit word of slope p^{-v} this is the task's kappa = log p^v / log lambda. For 3x+1,
lambda = 3/2 and mu = 1/2 give kappa = log 2 / log(3/2).

**Lemma R.** Suppose that on a piece of block indices, K_i = k_1 + ... + k_i satisfies

    K_i = c + floor(kappa i + t) + w(phi_i),    lambda_i = Lambda(phi_i),    phi_i = {kappa i + t},

with c in Z unrestricted, t real, and w, Lambda step functions on the circle with at most J arcs
and |w| <= B. Then the piece is a shift piece with M(delta) = 2(2J + 1)(1/delta + 2) and
gamma = lambda_C^{k - kappa q} in [lambda_C^{-1}, lambda_C], and it has bounded geometry.

*Proof.* Since every exit has the same exponent vector (a_X, e_X), we have
A(i+q) - A(i) = a_C (K_{i+q} - K_i) + q a_X, and similarly for E'. Shift invariance at i
therefore means K_{i+q} - K_i = k and lambda_{i+q} = lambda_i.

Convention: the arcs of w and Lambda are left-closed, right-open, [a, b).

Given I' and delta, with |I'| >= 2/delta, let Q = floor(delta |I'|), so Q >= 2. Let q in
[1, Q] minimize ||kappa q||, let k be the nearest integer to kappa q, and put
epsilon = kappa q - k, with |epsilon| = Delta. Then

    K_{i+q} - K_i - k = floor(phi_i + epsilon) + w(phi_i + epsilon) - w(phi_i),
    lambda_{i+q} = Lambda(phi_i + epsilon).

This is 0 with matching labels unless phi_i lies in one of at most 2J + 1 **half-open** arcs
of length Delta:

* for the floor term: [1 - Delta, 1) if epsilon > 0, or [0, Delta) if epsilon < 0;
* for each of the at most 2J cut points c of w and Lambda: [c - Delta, c) if epsilon > 0, or
  [c, c + Delta) if epsilon < 0.

In each case the value changes exactly when phi and phi + epsilon lie on different sides of the
point, and with left-closed arcs this set is the half-open arc shown.

Any Q consecutive phases are pairwise at least Delta apart on the circle, since
||kappa (i - i')|| >= Delta for 0 < |i - i'| < Q. Two points of a half-open arc of length Delta
are less than Delta apart, so each arc holds at most **one** of any Q consecutive phases.

Cut I' into ceil(|I'|/Q) windows of Q consecutive indices (the last may be shorter). Since
delta|I'| >= 2, we have Q >= delta|I'| - 1 >= delta|I'|/2, so ceil(|I'|/Q) < |I'|/Q + 1 <=
2/delta + 1. The number of exceptional indices is therefore at most
(2J + 1)(2/delta + 1) <= 2(2J + 1)(1/delta + 2) = M(delta).

(Revision after REFEREE1: the original text claimed "<= 1/delta + 2 windows" with "a closed arc
holds at most 2". The window count was false, for example delta = 1/6 and |I'| = 17 give 9
windows. The stated M(delta) survives by the argument above. `check_cutoff_instances.py`
checks the window inequality exactly for delta = 1/d, d = 5..40, and |I'| <= 4000. It also
checks the sharper per-window bound |X| <= ceil((e - q)/Q) on all 15 instances.)

If kappa is rational and Delta = 0, every pair matches. In all cases k_E = e_C k + e_X q >= 1,
|k_A|, k_E <= Cq, and |log gamma| = Delta log lambda_C <= log lambda_C.

Bounded geometry: K_{i'} - K_i <= kappa (i' - i) + 2B + 1 and >= kappa (i' - i) - 2B - 1. ∎

Periodic exit patterns of bounded period, including exits of **different** slopes, are
geometric pieces. A ramp of consecutive exits with no expansions in between is a geometric
piece with period 1. A ramp whose label string has a bounded number of switches splits into
that many geometric pieces.

**Not ported.** Some split5_3 results are not proved here in the general setting:

* the varying-rate version with unbounded rates;
* the two-phase linked version;
* the complementary-halves and multi-shift linked-label theorems;
* the separation theorem;
* the power bound with free labels.

Their split5_3 proofs use only the same ingredients, but I have not written the general
versions out, so they are not claimed.

## 6. Instances (all PROVED as consequences of Theorem W plus Lemma R; data from the checks)

The two hypotheses added after REFEREE1 hold in every instance. For (H0), every step is a
single cylinder-graph edge or a single block C or X, with C^k split into k copies of C, so e
is bounded by the largest block. For (H3) on every prefix, each event is an exit and divides,
so N_j <= E_j. Also |A_j| <= (max a) · (number of steps) = O(E_j + 1), because every closed
walk of these graphs divides.

For each system, C is the least expanding simple cycle of G_m, rotated by the cycle lemma, and
W is the shortest contracting re-entry walk found. The family covered is block words
C^{k_1} W C^{k_2} W ... with K_i in the rotation form of Lemma R, plus at most J pieces, jumps
and periodic ramps. Conclusion: from every start with |y| >= y_* (ineffective), such a path has
at most (1 + eta) log_p |y| divisions.

| system | p, l | x* | lambda_C | W slope | kappa_W | standard exit, kappa |
|---|---|---|---|---|---|---|
| 3x+1 (Terras) | 2, 3 | -1 | 3/2 | 3/4 | 0.7095 | y -> (y+1)/2, kappa = log2/log(3/2) = 1.7095 |
| 3x-1 (control) | 2, 3 | 1 | 3/2 | 3/4 | 0.7095 | same; x* = 1 is a real cycle |
| 3x+5 (control) | 2, 3 | -5 | 3/2 | 3/4 | 0.7095 | same |
| 5x+1 (control) | 2, 5 | -1/3 | 5/2 | 5/8 | 0.5129 | y -> y/2 + 1/6, kappa = 0.7565 |
| K7 = core S={7} | 2, 3 | -1 | 3/2 (2 steps) | 3/8 | 2.4190 | exits (y+1)/2 and (y+2)/4 have different slopes; one-rate families use one slope class |
| core S={1,3} mod 8 | 2, 3 | -5 | 9/8 (5 steps) | 3/4 | 2.4425 | |
| core S={1,3,5} mod 8 | 2, 3 | -5 | 9/8 (5 steps) | 9/16 | 4.8849 | |
| cores {5,7}, {1,5,7}, {1,7} | 2, 3 | -1 | 3/2 | 3/8 | 2.4190 | |
| core {3,5,7}; core W {1,3,7} | 2, 3 | -1 | 3/2 | 27/32 | 0.4190 | |
| split5_3 | 2, 5 | -3 | 5/4 (3 steps) | 5/8 | 2.1063 | exits y/2 + 3/2, y/2 + 3 (slope 1/2): kappa = log 2/log(5/4) = 3.1063 (repo's kappa; the repo's T = 2 kappa + 1 = 7.2126). Revision after REFEREE1: this cell read 6.2126 = 2 kappa |
| split5_1 | 2, 5 | -1/3 | 5/2 | 5/8 | 0.5129 | |
| m3_b | 3, 2 | 1 | 4/3 | 4/9 | 2.8188 | exit (y-2)/3, kappa = log3/log(4/3) = 3.8188 |
| mb_s3_27 (mixed base) | 2, 3 | -5 | 9/8 (3 steps) | 3/8 | 8.3274 | never-blocked words only (`check_mb_s3_27.py`) |

The x* column is the rotated cycle point. K7 and the cores rotate to -2 in `check_entropy_code.py`
because that script picks a different cycle-lemma start. Exact checks per system:

* the shifted forms;
* the identity (1) on the actual integer orbit of a realized 80-block word;
* the pairing decomposition of Step 2, exactly;
* the exception count of Lemma R.

**EVIDENCE** (consistent with Theorem W, not a proof of it): for e = 100..300 blocks, the least
positive and least negative integer lifts of the near-critical word satisfy log_p|y|/E in
[0.98, 1.002] for every system. If the theorem failed, the bound 0.8 asserted in the check would
eventually break.

**What the instances do and do not give.** Each instance says that a specific zero-entropy
family of paths cannot be followed far beyond the digit horizon. It says nothing about escaping
orbits in general, since nothing forces an orbit to contain long rigid stretches. It says nothing
about cycles. Expanding integer cycles satisfy (H0)-(H4) from bounded starts, so they are compatible
with Theorem W only through the threshold y_*, and Theorem W cannot exclude any finite set of
cycles. (Revision after REFEREE1: this sentence previously said that cycles "fail (H2)". That is
withdrawn. Only contracting cycles fail (H2).) For 3x+1 the near-critical schedule has a
single exit label, so there is no free-label problem. All the freedom of 3x+1's non-descending
words lies in the schedule offsets K_i - kappa i, which (H4) bounds. In split5_3 the freedom was
two equal-slope labels.

**Reformulation for one schedule.** For a fixed infinite rigid word, (1) and Theorem W say that
its unique p-adic point xi satisfies |xi - n|_p >= |n|^{-1-eta} for all integers |n| >= n_*(eta).
This is an ineffective approximation-exponent statement for these p-adic numbers. Novelty is not
checked. Results of this shape for lacunary S-unit series are classical consequences of the
p-adic Subspace Theorem (Corvaja-Zannier-type arguments), so this is likely not new in substance.
