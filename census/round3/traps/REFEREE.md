# Referee report: round 3, lens "traps"

Referee files:
* `referee_check.py` is written from scratch. It imports nothing from `traps_lib`, `verify`,
  `census`, `family`, `entropy`, `minsize` or `check`. `systems.py` is imported only so that its
  step functions can be compared with the written rules.
* `referee_census.c` is my own census engine. It builds the graph, finds SCCs by bitset
  closure, and tests for expanding cycles with Bellman–Ford on exact integer weights.

`python3 referee_check.py` exits 0 in about 85 s. The prover's `check.py` exits 0 in 7.8 s.

**Overall verdict.** The mathematics is correct. I found no WRONG claim and no real GAP.
Several statements need small textual fixes (below), and two claims were missing a check of
their finite content; I have supplied those checks. needs_repair = false. The fixes are
recommended edits.

## 1. Theory (theory.md): line-by-line re-derivation

**Lemma 0 (walk lifting). CONFIRMED.**
* One step on r + 2^m Z_2 is affine with image (ar+b)/2^e + a·2^{m−e} Z_2.
* Each of the 2^e lifts mod 2^m is attained, so the preimage of each one is a level-(m+e)
  cylinder.
* Composing the steps gives the cylinder Z_W and the affine bijection.
* For a closed walk, the inverse branch is a 2^{−E} contraction. It has a unique rational fixed
  point, and that point is unique among points whose residue path is C^∞.

**Theorem 1. CONFIRMED.**
* (a)⇔(b): a cycle at level m projects to a closed walk at level m0 with the same multiplier.
* (a)⇔(c): this is Lemma 0.
* For the potential, P_a ≤ Q log2 a + 1. So a cycle of length ℓ has weight
  ≤ Qμℓ + 2ℓ ≤ 0 once Q|μ| ≥ 2; the "Q > 3/|μ|" in the text is more than enough. The potential
  itself is verified exactly in any case.
* The descent ratio bound is correct: a·2^{−P_a/Q} < 1, and halving steps give 2^{−1/Q}.
* not(c) ⇒ not(d) adapts Lemma B of round2/descent/lemmas.md (the cycle-lemma rotation).
  Points near the rotated orbit point avoid A for j steps, so the cylinder cannot be a "meets A"
  leaf, and its multiplier is > 1. The definition of a certificate "restricted to avoiders" is
  informal, but the argument is sound for the natural reading, where a leaf either meets A
  uniformly or descends.

**Theorem 2 (SCC certificate). CONFIRMED.**
* Every infinite path eventually stays in a single SCC, by the topological rank.
* If that SCC is simple, the tail equals the lift x* (Lemma 0 uniqueness).
* If it is contracting, the potential forces the orbit into [1, B].
* A trivial SCC cannot hold a path forever.
* A positive-integer cycle has multiplier < 1: ∏(a_i + b_i/x)/2^E = 1 with b ≥ 0, and the
  multiplier (odd)/2^E is never 1.
* `verify.check_certificate` tests exactly the finite content (V1–V4). Re-deriving the graph by
  brute force from n < 2^{m+β+1} suffices, because T(n) mod 2^m depends on n mod 2^{m+e}.

**Theorem 3 (homoclinic obstruction). CONFIRMED.**
* Precision is kept: D' = x* + 2^{m0+E} Z_2 follows x*'s branches with precision ≥ m0 ≥ k, β.
* The points z_t = g^t z avoid A forever. For large t their residue path starts and ends on the
  cycle of x*, so it lies in that cycle's SCC.
* If the SCC were simple, z_t would follow C^∞ and hence lie on the orbit of x*, and so would
  z. This contradicts the hypothesis on z.
* Small point: if the residue period L' of x* mod 2^m is smaller than L, the argument is
  unaffected, since x* also follows C'^∞.
* My finite test of the statement: for {0}, {1}, {5}, {7}, {5,7} mod 8 and F* mod 16, the SCC
  through x*'s residues is non-simple at every level m = k..12. This is EVIDENCE for the
  theorem, and an exact check of these instances.

**Theorem 4. CONFIRMED.**
* A closed walk with positive log-weight decomposes into simple cycles, one of which expands.
* A non-simple, non-trivial SCC has a node with two internal out-edges.
* A simple C1 visits r0 once per period, so w_i on the orbit forces w_i = x*. Then W_1 and W_2
  would both be prefixes of C1^∞, which they cannot be, since they differ right after P.
* The code (`homoclinic_from_scc`) matches the proof. `verify.check_homoclinic` checks T^j z = x*
  exactly.

**Corollary 5 and Lemma 6. CONFIRMED_WITH_FIX (wording only).**
* The logic is right: Thm 3 gives "some level ⇒ no homoclinic orbit", and Thm 4 plus the
  absence of multiplier 1 gives "no homoclinic orbit ⇒ level m0".
* Monotonicity in A holds: a sub-SCC of a simple cycle is that cycle or trivial. I also verified
  it on every set of all 9 censuses.
* Fix needed. The summary, README and census.md say an H set is "beyond every residue method"
  and that "no residue method reaches" F*. What is proved is narrower: no Theorem-2 SCC
  certificate and no avoider descent certificate exists at any modulus 2^m. Other methods that
  use residues are not excluded, for example YAH's rewriting/SAT encodings, non-power-of-2
  moduli, or potentials that are not of the form n·2^{φ(r)/Q}. The wording should say "beyond
  every SCC/descent certificate mod 2^m".
* The summary also calls {0} one of the "$500 open sets". Per the round-2 transcription, the
  prize conjectures 4.11–4.14 are {1}, {5}, {7} and {5,7}. YAH list {0} as open, but not as a
  numbered prize conjecture.

**YAH mod-8 table. CONFIRMED.** Independently: for 3x+1 on subsets of Z/8, A is provable iff
A ⊄ {1} and A ⊄ {0,5,7}, checked on all 256 sets. I re-stepped all five witnesses in the table
exactly; for example x* = −20 (9/8) and z = −28 for {7}.

## 2. Census theorem. CONFIRMED

My own C engine classified all 9 × (256 or 65536) sets, independently of the prover's code. It
reproduces exactly:
* the provable/H counts;
* all 490 minimal provable sets, with their P0/P1 types;
* all 130 maximal H sets.

The prover's check.py does not prove that every set lies above a minimal set or below a
maximal H set; that comes from census.py, which uses the same library. My recomputation closes
this. Also verified:
* F* is the unique maximal H set containing {5,7,13,15}, and the residues whose addition makes
  it provable are exactly 1, 2, 4, 6, 9, 11 and 12;
* the lifts of {7}, {1}, {0} and {5} lie in 3, 2, 2 and 2 frontier sets, as stated;
* no minimal provable odd set mod 32 is P0 for 5x+1 or 7x+1, and none mod 16 is P0 for 7x+1
  either.

Note: the census.md line "{2}, {3}, {4}, {6} (P0), {0,1}, {1,5}, {1,7} (P0)" is ambiguous. Only
{6} and {1,7} are P0 (JSON and my engine agree); {2}, {3} and {4} are P1.

Novelty and counting: "490 new systems settled" overcounts. It includes YAH's own proved sets
{2}, {3}, {4}, {6}, {1,5}, {1,7} (and {0,1}) mod 8. Most of the 490 are routine instances of one
method, not 490 independent results. The genuinely new content is the method, the 5x+1 and
7x+1 censuses, and the frontier description.

## 3. Minimum provable odd trap size (PARTIAL). CONFIRMED

My own exhaustive search shows that every odd set of size < s is H, and it finds the exact
number of provable sets of size s:

| k | min size s | number of minimum sets |
|---|---|---|
| 3 | 1 | 1 |
| 4 | 2 | 5 |
| 5 | 3 | 9 |
| 6 | 4 | 5 |

The five k = 6 sets are the ones listed in census.md. The continuation beyond k = 6 is correctly
labelled EVIDENCE/OPEN.

## 4. Theorem F (families). CONFIRMED_WITH_FIX (missing check supplied)

* The proof is Theorem 2 with no contracting component. The graph depends only on
  (a mod 2^k, b mod 2^k). Positive lifts need a^o < 2^E. This is correct.
* Gap in the prover's check. The "no exceptions" claims of F2 (a ≥ 5) and F3 (a ≥ 9) rest on
  "every simple cycle has E ≤ 2o (mod 8) or E ≤ 3o (mod 16)". check.py [4] does not test that;
  it only simulates a < 60 (EVIDENCE).
* I verified it for every minimal odd type-F set of every class, mod 8 and mod 16. Cycles with
  o = 0 are all-halving loops with lift 0, so they are harmless.
* I recomputed the type-F minimal sets (mod 8 all/odd, mod 16 odd) independently; they match
  the JSON. The 16-row table in family.md matches as well.
* The hand proof of F1 is correct: (an+b)/2 − x* = (a/2)(n − x*) with x* = −b/(a−2). The a = 1
  exception (b, 2b) was tested for b < 400.
* Stress test (EVIDENCE): 3000 random a, b < 10^6 with n up to 200 bits behave as F1 and F2
  predict.
* Novelty: F1 is a one-line valuation argument (tier 1), and it is presented as such.

## 5. Theorem E (density). CONFIRMED_WITH_FIX

* The proof is correct: Terras bijection, the injective and hence bijective residue-walk map,
  the Perron bound, and at most 2 members per class mod 2^L in [1, X].
* Gap. entropy.md states the C-orbit version only for odd A. Yet README and census.md apply
  Thm E to all 130 H sets, including the mod-8 and mod-16 sets with even residues such as F*.
* One line fixes it. The T_{a,b}-orbit is a subsequence of the C_{a,b}-orbit, so a C-avoider
  is a T-avoider, and the bound still applies. One also needs λ < 2 for those sets.
* check.py [6] does not certify λ < 2 for the even-residue sets. I did, with an exact rational
  Perron certificate M v ≤ λ v and λ < 2, for all 130 maximal H sets. Examples:
  * F* has exponent 0.4057;
  * the 3x+1 mod-32 frontier exponents lie in [0.2232, 0.6125], as claimed.
* I also checked the walk-count bijection by brute force for F* for L ≤ 12.

## 6. Named systems

| id | verdict | notes |
|---|---|---|
| trap7_57 | CONFIRMED_WITH_FIX | Proof text says "n ≡ 3 (mod 8) iff 16 \| 5n+1". **False** (n = 11: 5n+1 = 56). Correct: iff 8 \| 5n+1, i.e. v_2(5n+1) ≥ 3. The run argument is unchanged, because v_2(5N+1) = v_2(5n+1) − 1 and the run continues exactly while v_2 ≥ 3. check.py tested only the identity 5N+1 = (7/2)(5n+1), so it could not catch this. Own certificate (B = 40) gives the cycle list [(1 8 4 2)]. |
| trap5_17 | CONFIRMED_WITH_FIX | Same slip: "n ≡ 5 (mod 8) iff 16 \| 3n+1" is **false** (n = 13: 3n+1 = 40). Correct: 8 \| 3n+1. The argument is otherwise intact. Own certificate (B = 47): no avoiding cycle. |
| trap5_hi16 | CONFIRMED | Hand proof re-derived. The transition table holds (checked from n mod 2^12). Here "n ≡ 5 (mod 16) iff 16 \| 3n+1" is correct. All five potential ratios are < 1 at n = 64 and decrease in n; the worst, 7→1, is 20223/20224. The finite part n ≤ 64 holds. Own certificate (B = 350): [(1 6 3 16 8 4 2)]. |
| trap5_c13 | CONFIRMED | Own certificate (B = 350) gives exactly the 13-cycle. Minimality holds: every one-element deletion is H. Exactly 10 minimal odd sets mod 32 have the 13-cycle as their only cycle. The simple lifts −4 (5/4) and −1/3 (5/2) were checked by hand. |
| trap7_m32 | CONFIRMED | Own certificate (B = 40): [(1 8 4 2)]. Minimal. Lifts −1/5 and −4/3 check out. |
| trap3_m32 | CONFIRMED | Own certificate (B = 99): [(1 4 2)]. Minimal. |
| FAM_4mod8 | CONFIRMED | Corollary F1. Tier 1, a one-line valuation argument. |
| FAM_oddpairs8 | CONFIRMED_WITH_FIX | The E ≤ 2o check was missing (§4) and is now supplied. |

* `systems.py` agrees with the written rules on n < 5000 and on 500 random 200-bit n, for all
  six systems.
* All six systems are new relative to census/systems.py; no trap system appears there. They
  are also distinct from the round-2 YAH items, which are 3x+1 mod 8 only.
* The tier labels are honest. trap7_57, trap5_17 and the families are tier 1, and they are
  presented that way.

## 7. Open items (Conjecture 4.14 and the other H sets). CONFIRMED as OPEN

What is proved for these sets is stated correctly: no SCC or descent certificate at any
modulus 2^m, explicit witnesses, and density O(X^θ) with θ < 1. The statements themselves are
correctly left OPEN.

## Recommended textual repairs (no mathematical change)

1. **trap7_57.md:** replace "n ≡ 3 (mod 8) iff 16 \| 5n + 1" with "n ≡ 3 (mod 8) iff
   8 \| 5n + 1 (i.e. v_2(5n+1) ≥ 3)".
2. **trap5_17.md:** replace "n ≡ 5 (mod 8) iff 16 \| 3n + 1" with "… iff 8 \| 3n + 1".
3. **check.py [5]:** test these two congruence equivalences, not only the multiplicative
   identity.
4. **family.md and check.py [4]:** add the check that every simple cycle of the listed sets has
   E ≤ 2o (mod 8) or E ≤ 3o (mod 16).
5. **entropy.md:** add the one-line remark that C-avoidance implies T-avoidance for arbitrary A.
   **check.py [6]:** certify λ < 2 for the even-residue H sets, including F*.
6. **README, census.md and the summary:**
   * replace "beyond every residue method" with "beyond every SCC/descent certificate mod 2^m";
   * drop {0} from the "$500" list;
   * replace "490 new systems" with wording that excludes the YAH-known mod-8 sets;
   * disambiguate the P0 markers in the mod-8 list.
