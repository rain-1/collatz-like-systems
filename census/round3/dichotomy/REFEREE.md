# Referee report: lens "dichotomy" (round 3)

Referee files (the prover's files were not modified):

* `referee_lib.py`: independent library written from the statements in dichotomy.md. It does
  not import decide.py, distance.py, neighbours.py or families.py. It provides the hypotheses
  check, the residue graph, the exact verdict (translation-cycle search, multiplicative
  Bellman–Ford with Fractions, integer potential verified with integers), a separate fast
  exact verdict that compresses w = 1 chains (for bulk counts), my own congruence-solving
  progression builder (Lemma 1), my own layered depth search (Theorem 3), the exceptional
  bounds, and the cycle enumeration.
* `referee_check.py`: exits 0. It takes about 70 s, and `--full` adds part F (the full run
  took 279 s and exited 0).
* `referee_b27.py`: exits 0. It is an independent recount of all eight B(27, a) phase-diagram
  numbers (2^18 tables per a) and takes about 4 to 5 minutes.

The prover's four check scripts were also run, all under `nice`. All exit 0:
check_systems 11 s, check_dichotomy 58 s, check_neighbours 19 s, check_phase 25 s.

## 1. General theorems (dichotomy.md): line-by-line re-derivation

**Lemma 1 (realisation): CONFIRMED.** On n = r + Qz, T(n) = (ur+v)/w + (uQ/w)z. In the
induction, the slope after i steps is K = U_i Q. One more step gives slope u·U_i·Q/w, and
gcd(u U_i Q/w, Q) = Q/w because gcd(u U_i, Q) = 1. This is the only use of (H1). So the
congruence for r_{i+1} is solvable iff r_i → r_{i+1} is an edge, and the solutions form one
class mod w. N(π) = {a + Mt} with a the least element, so every positive n ≡ a (mod M)
follows π. This fact is used tacitly in Theorems 1 and 3.
Check: part T1 compares the progression with a brute-force enumeration on 150 random tables
with moduli 2, 3, 4, 6, 8, 9, 10, 12, 15 and 18.

**Lemma 2: CONFIRMED.** ∏u is prime to Q, and every prime of ∏w divides Q. So
∏u = ∏w forces both products to be 1. Part (c) follows from (P). Check: part T2.

**Lemma 3: CONFIRMED.** In the λ > 1 case, the cycle-lemma rotation makes every partial
product > 1, over any number of laps. The nested closures a_k + M_kẐ_Q are compact, so they
have a common point. Splitting M = M_1 M_2 and applying CRT gives an infinite progression
inside both the certificate class and N(π_k). On it, T^j has slope > 1, which contradicts
T^j(n) < n. The λ = 1 case uses a rotation with every partial drift ≥ 0. No periodic point
is needed, so the remark about mixed moduli is correct. Check: part T3 iterates 4 laps of
the rotated cycle at n ≈ 10^30·M and confirms no descent, on 314 random OBST tables.

**Lemma 4 and Theorem 1: CONFIRMED.** The telescoping identity in (c)⇒(d) is correct.
Each class mod Q^{k+1} lies inside a single N(π), because M_π | Q^{k+1}. *Nit:* the text
says the modulus "divides Q·Q^{k−1}". It is Q·∏_{i<k−1} w for the walk r_0..r_{k−1}, which
divides Q^k, so the statement holds, but the wording is garbled.
Check: part T3 compares k\* from the graph with a brute-force computation on integers. For
each class a mod Q^{k\*+1} it finds the first j with T^j(n) < n at n = a + Q^{k\*+1}·10^40.
It confirms that every class descends by step k\*, and that at modulus Q^{k\*} some class
does not descend within k\*−1 steps. This was done for 86 random CERT tables with
Q ∈ {2, 3, 4, 6}. Part T4 confirms lifting invariance.

**Theorem 2: CONFIRMED.** The equivalence V(Tn) < V(n) ⇔ n(c_r w − c_s u) > c_s v holds. If
n > ⌊X/d⌋, then nd > X. Every cycle meets F, and every orbit meets F infinitely often, so
every orbit is eventually periodic.

**Theorem 3: CONFIRMED.** The lower bound works for an arbitrary certificate modulus M. The
upper bound closes walks at their first descending prefix, at modulus Q^{Λ+2}. For (c),
c = e^φ gives c(s)u/(c(r)w) ≤ e^{μ\*}. The values 44 for desc_s32_max and 332 for dch_S6_332
(111849 leaves) were re-run against the round-2 engine in part F4. No prover check script
covers these two engine comparisons, although deep.md states them.

**§6 (H1 is necessary): CONFIRMED.** For odd n, T^4(n) = (n+1)/2 symbolically. The graph
cycle 1→0→1 has multiplier 4·(1/2) = 2. Check: part T5.

**Definition 5 and Proposition 6: CONFIRMED.** Vertices outside R keep their branch, so they
keep their out-edges and multipliers. "Admissible" means a table at modulus Q' that satisfies
(H1), (H2) and (P), and the claim is correct for that class of replacements. It does not
cover replacements that are not affine at modulus Q', and the definition says so.

**Theorem 7: CONFIRMED.** The prefix-agreement argument is correct: an odd step keeps the
2-adic precision and an even step loses one bit, so the parity of the i-th iterate is
determined while at least one bit remains. The Fine–Wilf application is also correct, and so
is the entropy estimate (0.613·H(0.631) ≈ 0.58 bit). Checks:

* part 7a: periodic orbits are disjoint simple cycles for m ≤ 16.
* part 7b: independent implicit-hitting-set computation, exact for m ≤ 7.
* part F1: m = 8 gives 8, exact.
* part F2: m = 9 gives ≥ 10. This bound is not covered by any prover check script; it is
  covered only by distance.py.
* part F3: m = 10 gives ≥ 16 by greedy packing. A one-off greedy run for m = 11 gave 20 ≥ 19
  (305 s, not in the script).

*Nit:* "the density fell monotonically up to m = 8". The values .5, .25, .125, .125, .0625,
.0625, … are non-increasing, not strictly decreasing.

**Translation-chain family (deep.md): CONFIRMED** for m ≤ 8 (part T6). The argument for
general m is elementary and correct: the walk 1→3→…→2^m−1 is non-descending of length
2^{m−1}−1.

**Conjecture (unbounded k\* without translations) and the permutation growth law:**
correctly labelled EVIDENCE/OPEN. The permutation distances that are marked exact (4 of 9,
8 of 27) were re-derived in part F5.

## 2. Systems

For every one of the 17 systems:

* I rebuilt the table from the **written rule** (the JSON claims and `<id>.md`). It equals
  systems.py, and the step functions agree on n < 5000.
* dch_s32p9_nb64 agrees with round-2 desc_s32_plus9 off the two modified classes 13 and 18
  mod 64.
* I computed my own integer potential, verified with integers. Its N_r bounds are at most
  1999.
* The complete cycle list was obtained by iterating every n ≤ max N_r. It equals the claimed
  list.
* k\* from my own layered search equals the claim.
* I built a witness progression with my own congruence solver and checked it at
  t = 10^12 and t = 10^30+7.
* 40 random starts in [10^20, 10^40] reach a listed cycle. This is EVIDENCE only.

A comparison against all 284 systems with step functions in census/systems.py, round2/* and
the other round3/* folders found no coincidence on n < 400. So the systems are new to the
census.

| system | verdict | remark |
|---|---|---|
| dch_C27_2466 | CONFIRMED | cycles and k\* = 2466 re-derived |
| dch_B81a2_655 | CONFIRMED | |
| dch_S6_332 | CONFIRMED | engine agreement re-run (F4) |
| dch_B81a5_254 | CONFIRMED | |
| dch_B81a4_184 | CONFIRMED | |
| dch_B27a5_66 | CONFIRMED | |
| dch_B27a8_65 | CONFIRMED | |
| dch_B27a4_49 | CONFIRMED | |
| dch_B27a2_max14 | CONFIRMED | "maximum": no CERT set of size 15 to 18; exactly 8 sets of size 14 (P4) |
| dch_C9_33 | CONFIRMED | deepest in C9, and unique (P1b) |
| dch_C9_prod2500 | CONFIRMED | 2500 is the maximum product; *two* certifiable tables attain it, so "the most expanding" should read "a most expanding" (nit) |
| dch_D36a5_8 | CONFIRMED | max 8 attained by 6 sets (P3) |
| dch_D36a7_7 | CONFIRMED | max 7 attained by 2 sets (P3) |
| dch_D36a7_43 | CONFIRMED | |
| dch_split5_1_nb8 | CONFIRMED | tier 1, labelled as such |
| dch_div23_5n1_nb12 | CONFIRMED | tier 1, labelled as such |
| dch_s32p9_nb64 | CONFIRMED | |
| C9_critical | CONFIRMED | trivial (tier 1): the units are closed under T, and T^6 = n + 9 on units (S2) |

**Phase diagrams: CONFIRMED.** I recounted every number independently:

* C9: 11956 / 250187 / 1, plus the k\* distribution.
* B9 for all eight values of a.
* D36: 756 and 336, with the maxima and the number of maximal sets.
* B27 for all eight values of a (referee_b27.py; all counts and maxima match).

**Open entries / neighbours: CONFIRMED_WITH_FIX.**

* Every open table map is OBST. Of these, 21 were rebuilt from census step functions and 15
  from the rule text.
* All 1330 stored CERT neighbours were re-decided. They are CERT, and their cycle lists
  (prefix-compared where neighbours.json truncates them) and k\* agree.
* The exact distances spot-checked in F5 agree: perm_1932 9:4 and 27:8; split5_1 8:1, 16:1,
  32:2, 64:3; div23_5n1 12:2, 24:2, 48:4; m3_b 9:3, 27:6, 81:12. In a one-off run, perm_d
  16:5, 32:9, 64:13 also agree.
* **Fix:** README.md, neighbours.md and the claims say "34 open GLOBAL table maps", but
  open_tables.py lists **36** distinct maps, and neighbours.out has 36 sections. The count
  should read 36. Also, check_neighbours.py compares only 21 + 3 of the 36 tables with census
  step functions. The 12 remaining parametric par_* entries are not compared, though their
  rule text is trivial and my part N1 rebuilds them.

## 3. Overclaiming and novelty

* The real contribution is the general theorem (Theorems 1–3) together with the decision
  procedure. The 17 systems are mechanical instances, each settled by a weighted one-step
  Lyapunov function plus a finite check (tier 2, or tier 1). The prover says this openly
  ("Depth is not difficulty", deep.md). The depth records measure the certificate format, not
  hardness, and deep.md also says so. No overclaim.
* Novelty is stated as "not checked beyond one search", which is honest. The direction
  CERT ⇒ GLOBAL via a weighted potential is a standard Lyapunov/max-cycle-mean argument. The
  equivalence with the realisation lemma is a clean packaging, and I cannot confirm whether it
  is new.

## 4. Verdict

No GAP and no WRONG item. Every PROVED claim is confirmed. The items that need small fixes
are wording only:

1. "34" → "36" open table maps (README.md, neighbours.md).
2. dch_C9_prod2500 is one of two tables attaining product 2500.
3. "monotonically" → "non-increasing" (dichotomy.md §7).
4. "divides Q·Q^{k−1}" in the proof of (c)⇒(d) should read "divides Q^k" (dichotomy.md §5).

None of these affects any proof. needs_repair = false.
