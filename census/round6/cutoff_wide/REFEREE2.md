# Referee 2 report: round6/cutoff_wide (second pass, after the REFEREE1 repair)

Referee: independent agent (referee 2). I did not edit the prover's files and did not commit.
My check is `referee2_check.py`. I wrote it from scratch. It imports nothing from `cwlib`, the
prover's check scripts, or `referee1_check.py`. It uses exact ints and Fractions wherever a claim
is exact. Run it with `/home/riv/Code/collatz/census/round4/wpotential/.venv/bin/python
referee2_check.py`. It takes about 20 s, exits 0, and exits 1 on any failed assertion. It
contains negative controls, which pass because the claims they test are rejected:
* the old core13/core135 H values (0.4565, 0.3755) are rejected by the same fit test that the
  corrected values pass;
* the "every class s != 26" form of Proposition B is rejected, because no class s = 2 (mod 3)
  has an entry word.

**Overall.** Nothing is claimed settled, and nothing is settled. No cycle list is claimed, so
there is nothing to brute-force for settled systems. Nothing claims 3x+1, and nothing would
settle it: Theorem W excludes only zero-entropy rigid families from ineffectively large starts.

Every REFEREE1 item was resolved, and resolved honestly. In one place the prover was right
against referee 1: on Proposition B, referee 1's proposed fix was itself false. All proofs
re-derive. One coverage statement in the headline is still broader than what is proved, a
leftover of REFEREE1 item 10. A few nits remain. **needs_repair = true, but only for a
wording fix** (section 6). No mathematics needs repair.

## 0. Checks re-run

| script | result |
|---|---|
| `check_entropy_code.py` | exit 0 |
| `check_cutoff_instances.py` | exit 0 (lift ratios 0.98-1.002; window inequality; the 4 cycle checks) |
| `check_mb_s3_27.py` | exit 0 (W = 010, D = 25, \|U\| = 84; entry words max length 6; s = 2 (mod 3) classes descend; fit 0.3245) |
| `count_nondesc.py --check` | exit 0 |
| `count_nondesc.py --hcheck` | exit 0; every stated H is within 5e-4 of the variational minimum; core13 and core135 minimizers at theta = 4.645 and 3.999 (interior of [0, 12]) |
| `referee1_check.py` | exit 0 (its NOTE lines still print referee 1's "26 states" wording, which is superseded; see section 4) |
| `referee2_check.py` (mine) | exit 0 |

## 1. Resolution of the REFEREE1 items

| REFEREE1 item | resolved? | comment |
|---|---|---|
| Evertse quoted "from memory" | yes | I verified it again myself. I downloaded the Numdam PDF and rendered pp. 226 and 228. Display (14) and hypothesis (13) (every nonempty subsum nonzero) are as quoted in theorem_W.md section 4. C depends only on (eps, S, K, n). By eq. (2), \|\|x\|\| = max_k \|x_k\| for K = Q. |
| Theorem W truncation (e_max, (H3) not hereditary) | yes | (H0) was added, and (H3) is now required for every prefix. The truncation paragraph now argues hypothesis by hypothesis and is correct (section 2). |
| n_terms count | yes | |
| Lemma R window count | yes | The half-open-arc argument is correct (section 2). |
| split5_3 kappa | yes | 3.1063 |
| "cycles fail (H2)" | yes | The claim is withdrawn in README, theorem_W.md section 3 and section 6. My own exact check reproduces the four cycles (section 5). |
| core13/core135 H | yes | The values are corrected everywhere they appear (grep), and my own fits agree (section 3). |
| Theorem P item 4 | yes | The new proof handles e_max > 1 correctly. The first differing edge leaves a dividing node, because division-free nodes have out-degree 1. |
| Corollary P1 overreach | **partly** | Lemma Q' is new and correct, and Corollary P1 is now restricted to block-word normal form. But the headline sentences in README lines 18-21 and theorem_P.md lines 24-27 and 234-243 still state the conclusion without that restriction. See section 6. |
| Proposition B "each 27-class" | yes, and better than referee 1's fix | Referee 1's "each class != 26" is false. I re-proved and re-checked the prover's statement (section 4). |
| README Theorem H hypotheses | yes | |
| "cannot by itself decide" | yes in the sentence flagged | |
| escaping → non-descending; "smallest"; 0.04; novelty for Theorem P | yes | |

## 2. Proofs re-derived

**Theorem W: CONFIRMED.** I re-derived every step of the proof.

* **Identity (1).** It telescopes from y_j/P_j = y_{j-1}/P_{j-1} + c_j/(l^{a_j} P_{j-1}).
* **Truncation.** The truncated path has (1 + eta/2) log_p\|y\| <= E <= (1 + eta/2) log_p\|y\| + C
  by (H0). (H3) holds for the prefix by assumption. A sub-interval of a shift piece is a shift
  piece, because the shift condition quantifies over all subintervals I'. A sub-interval of a
  geometric piece is a geometric piece.
* **Step 1.** 1 - gamma = (p^{k_E} - l^{k_A})/p^{k_E} when k_A >= 0, and similarly when
  k_A < 0. The numerator is a nonzero integer by unique factorization, because k_E >= 1. My
  check confirms exactly that the denominator of 1 - gamma is a {p, l}-unit.
* **Step 2.** The pairing identity is correct. I checked it exactly on actual integer orbits of
  two-piece rotation schedules with a random jump: 13 runs on 3x+1, m3_b and core13, with
  exceptional sets of size 1 to 3. The identity (1) also holds exactly on those orbits.
* **Step 3.** The geometric sum is correct.
* **Step 4.** With S = {inf, p, l} and integers, prod_{v in S} \|x\|_v = r(x) is the
  prime-to-{p, l} part. With T = {p}, (14) gives \|sum\|_p >= C \|x_0\|_p H^{-rho} / prod r(x_j).
  Since \|sum\|_p = p^{-E} \|ZF\|_p \|Y\|_p and \|x_0\|_p = \|ZF\|_p \|y\|_p, the factor \|ZF\|_p
  cancels. What remains is \|y\| \|y\|_l <= \|y\|, because the denominator of x* is a divisor of
  l^a - p^e and so prime to l. Y != 0 for large \|y\|, since otherwise F y would be cancelled
  by o(\|F y\|) terms.
* **Deletion.** Removing vanishing subsums leaves the total unchanged. The leading term cannot
  be removed. After deletion, hypothesis (13) holds.
* **Uniformity.** n_terms depends only on (J, delta, C, M(delta)). Evertse's C therefore
  depends only on (rho, S, n_terms), and y_* is uniform over all paths with the same constants.
  It is ineffective, and the prover says so.

**Two-prime hypothesis on the new maps.** All slopes are l^a/p^e:
* 3, 5 and 1 over 2 for the Terras, core and split maps;
* 4 = 2^2 over 3 for m3_b, with l = 2;
* for mb_s3_27, a = -3 and e = 0 on the blocked step, which (H) allows. The instance uses
  never-blocked words only.

Positivity of additive constants is not used: (H2) replaces it, and Theorem H is not invoked
for any settlement.

**Lemma R: CONFIRMED.**
* K_{i+q} - K_i - k = floor(phi_i + eps) + w(phi_i + eps) - w(phi_i) is correct.
* With left-closed arcs, the exceptional sets are the half-open arcs stated.
* Two points of such an arc are less than Delta apart, while any Q consecutive phases are at
  least Delta apart, because q minimizes \|\|kappa q'\|\| over [1, Q].
* There are ceil(\|I'\|/Q) < 2/delta + 1 windows, so there are at most
  (2J+1)(2/delta+1) <= M(delta) exceptions.
* k_E = e_C k + e_X q >= 1, and gamma = lambda_C^{-eps}.

My check tests the lemma with exact rational phases on 400 random cases (random kappa, t, delta,
J <= 4 arcs for w and Lambda, \|w\| <= 3). Every window holds at most 2J + 1 exceptions, and every
total is at most M(delta); the largest total was 88. Notation nit: J denotes both the arc count
(Lemma R) and the piece count (H4).

**Theorem P (items 1-4) and the converse: CONFIRMED.**
* The cycle-lemma rotation (start after the last minimum) gives strict positivity.
* U = C^D W^{\|C\|} and V = C^{D+\|W\|} have equal length. They differ at the off-C edge,
  because G_m has no parallel edges in these systems.
* Prefix slopes are > 1, and the Moran/mass-distribution argument gives dim >= s.
* Item 4 as revised is correct.
* The converse: in type (a) the potential (★) bounds the slopes of p-adic walks without any
  positivity. In type (b) the preimages are finite. The converse needs the standing hypothesis
  (a division-free cycle would give a whole cylinder), which is part of the stated setting.

Independently, my check confirms for all 15 table systems:
* the standing hypothesis;
* (M), by enumerating all residues for walks of length <= 3 (m = 3) or 5 (m <= 2);
* a type-(c) SCC.

My own witness construction reproduces every row of the prover's table: \|C\|, \|W\|, D, \|U\|,
e_U/e_V and s, for example 0.02000 for core13 and 0.01064 for core135. Random {U, V}^n words
(n <= 4) are realized by integers. I found the class by p-adic lifting with an exhaustive
uniqueness test and confirmed it by direct iteration on two lifts. Distinct words give disjoint
classes. Item 4 holds by brute force: in random intervals of p^{m+E} integers, E <= 12 (p = 2)
or E <= 8 (p = 3), for 3x+1, 5x+1, m3_b, split5_1 and K7.

**Lemma Q and Lemma Q': CONFIRMED.** In Lemma Q':
* the word is recovered from (c_i) and the increments of E', using the distinct labels and
  e_C >= 1;
* sigma_{i+q} = sigma_i whenever i and i+1 are both non-exceptional, so \|D\| <= 2M(delta);
* the per-piece count is \|Sigma\|^{delta\|I\|} times a polynomial.

Minor imprecision: Corollary P1 compares cut walks, which may end in the middle of a block, with
block words. The number of block-word prefixes is at most (max block length) times the number of
block words, so the conclusion is unchanged.

**Corollary P1 (restricted form): CONFIRMED.** See section 6 for the headline wording.

**Proposition B: CONFIRMED.** The proof of the corrected claim is as follows. For
s = 2 (mod 3), an odd step gives (3s+1)/2 = 2 (mod 3), so the class stays 2 (mod 3). The odd map
s -> (3s+1)/2 has fixed point -1 = 26 in Z/27, and it contracts 3-adically. So
s = -1 + 3u -> -1 + 9u/2 -> -1 + 27v/2 = 26: two odd steps from any s = 2 (mod 3) land on 26.
The possible outcomes are:
* even first step: slope 1/2;
* odd, then even: slope 3/4;
* odd, odd, then the blocked step: slope 9/4 · 1/27;
* starting on 26: slope 1/27.

So a slope below 1 appears within 3 steps. My check confirms this on all \|n\| < 10^6 with
n mod 27 = 2 (mod 3).

For each of the 18 classes s = 0, 1 (mod 3), an exhaustive search over parity words of length
<= 8 finds an entry word with all prefix slopes > 1 (max length 6). The words P U V are realized
by integers in the class. No class s = 2 (mod 3) has an entry word (negative control).

I confirmed the rest of the proposition too: the skew product on all \|n\| < 5000, W = 010,
D = 25, \|U\| = \|V\| = 84, and random {U, V}^3 words realized and never blocked.

I also checked the never-blocked count DP against a direct residue count at j = 12. My fit over
[240, 480] is 0.3315, larger than the prover's 0.3245 over [120, 240]. The fit is still rising,
so "≥ 0.32 (EVIDENCE)" is honest.

## 3. Wide scans spot-checked (EVIDENCE)

My own DP of N(E) agrees exactly with direct residue enumeration for E <= 11 (p = 2) or 6
(p = 3) on 6 systems. I fitted 7 systems over E in [800, 1600]: core13 and core135, plus 5
others drawn at random.

| system | stated H | own fit [800, 1600] |
|---|---|---|
| core13 | 0.4281 | 0.4263 |
| core135 | 0.3593 | 0.3574 |
| core357 | 0.788 | 0.7861 |
| core57 | 0.7193 | 0.7174 |
| split5_1 | 0.9369 | 0.9349 |
| 3x+1 | 0.9500 | 0.9481 |
| m3_b | 0.9648 | 0.9637 |

All fits lie 0.001-0.002 below the stated values, as a finite-E fit should. The old core13 and
core135 values fail the same test. For 5x+1 and coreW the fit is > 0.995, consistent with
H = 1.

I recomputed every kappa in theorem_W.md section 6 and they agree to 6e-5. Also T = 7.2126,
log_2 3/(6T) = 0.0366, and each crit 1/(1 - H) agrees to within 0.01.

## 4. Proposition B and referee 1

The prover's rejection of referee 1's wording is correct (section 2). `referee1_check.py` still
prints "holds for 26 states". That note is superseded. Only reaching state 22 holds for those
26 classes; reaching it with all prefix slopes > 1 holds for 18. The prover handled this
honestly, with an exhaustive check and a direct-integer check.

## 5. Cycles and (H2)

I checked this exactly and independently: the cycles 5, 7, 10 and 17, ..., 34 of 3x-1 around
x* = 1, and -5, -7, -10 and -17, ... of 3x+1 around x* = -1.
* The identity (1) holds over 40 laps.
* \|tau\| <= 1/2. The maximum is 4/9 for the 3-cycles and 1024/2187 for the 11-cycles.
* The starts are bounded, \|y_0\| = 4 and 16, while E grows without bound.

So the withdrawn claim is correctly withdrawn. "Theorem W gives no information about cycles" is
the honest statement.

## 6. Labels, coverage, novelty

**Required fix (wording only; leftover of REFEREE1 item 10).** Corollary P1 is now proved only
for block words over one expanding cycle C with distinct-label exits (Lemma Q'). The prover says
so in Corollary P1 and README lines 11-13. The headline still states it without the
restriction:

* README lines 18-20: "is false at the cylinder level for every type-(c) system … No designed
  type-(c) table can have it."
* theorem_P.md lines 24-27: "no type-(c) system has this property even at the level of cylinder
  words".
* theorem_P.md lines 234-243: "Hence no statement of the form … holds"; "Designing a type-(c)
  table whose non-descending set is rigid or countable … is impossible".

Theorem P fully proves "countable is impossible", since the dimension is positive. "Rigid" is
proved only for the normal form. The prover's own caveat (theorem_P.md lines 230-232) excludes
paths over several expanding cycles, exits with coinciding labels, and other decompositions.
Fix: add "in block-word normal form (one expanding cycle, distinct-label exits)" to these three
places. Alternatively, prove a 2^{o(E)} bound for all cylinder walks that admit some
(H0)-(H4) decomposition with fixed constants. I expect that is true, but it is not written.

**Nits (no repair needed):**
* `count_nondesc.py` docstring: "H = lim log_p N(E)/E is the Hausdorff dimension". The text
  proves only dim_H N_inf <= liminf log_p N(E)/E. theorem_P.md lines 113-115 itself notes that
  N(E) can grow exponentially in type (b), where dim = 0. The README row "Non-descending set has
  H = …" should read "non-descending word count grows like p^{HE}". The label is already
  EVIDENCE.
* README line 40 / theorem_P.md line 324, "smallest among … round4/lundberg": that table also
  contains acc_h16 (type b), whose non-descending set has dimension 0. Say "among the type-(c)
  (open) systems".
* theorem_P.md line 255, mb_s3_27 "Its multipliers are not all units". The 2-adic multipliers
  3, 1 and 1/27 are all 2-adic units. The trichotomy fails to apply because the branch condition
  is mod 27, not 2-adic. The conclusion is unchanged.
* The mb_s3_27 never-blocked fit is still rising (0.3315 on [240, 480]); "≥ 0.32" is fine.

**Novelty.** "Not checked" is stated for both theorems. Calling Theorem W probably a known
p-adic Subspace consequence, and Theorem P elementary, is honest.

**"No system settled".** CONFIRMED. No settled system means no cycle list to verify. Nothing in
the folder bears on 3x+1 beyond excluding one zero-entropy family from ineffectively large
starts.

## Verdicts

| claim | verdict |
|---|---|
| REFEREE1 items resolved honestly | CONFIRMED (Corollary P1 headline only partly; see below) |
| Evertse Thm 2 (14) as quoted | CONFIRMED (re-verified from the scan, pp. 226 and 228) |
| Theorem W (with (H0), prefix-(H3)) | CONFIRMED |
| Lemma R (revised window argument) | CONFIRMED |
| Instances, 16 rows (kappa, x*, slopes, identity) | CONFIRMED |
| Expanding cycles satisfy (H0)-(H4); Theorem W says nothing about cycles | CONFIRMED |
| Theorem P items 1-4 | CONFIRMED |
| Converse (dim 0 iff no type (c)) | CONFIRMED |
| Lemma Q, Lemma Q' | CONFIRMED |
| Corollary P1 (normal form) | CONFIRMED |
| Headline "false for every type-(c) system / no designed table can have it" | CONFIRMED_WITH_FIX (restrict to block-word normal form in README 18-20, theorem_P 24-27 and 234-243) |
| Proposition B (18 classes s = 0, 1 mod 3; none in s = 2 mod 3) | CONFIRMED |
| H table (EVIDENCE) | CONFIRMED (nit: H is the word-count exponent, an upper bound for dim_H) |
| mb_s3_27 never-blocked exponent ≥ 0.32 (EVIDENCE) | CONFIRMED |
| "No system settled", no cycle lists | CONFIRMED |
