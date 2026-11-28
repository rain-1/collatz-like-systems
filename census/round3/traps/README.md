# Round 3, lens "traps": residue traps for 3x+1, 5x+1 and 7x+1

**Question studied.** S(T, A): every positive orbit of T meets the residue set A (mod 2^k), or
is eventually periodic with an explicit cycle list. T is C_{a,b} (n/2 | a n + b), or any map in
the same piecewise-affine 2-adic class.

**Main outcome.** A complete decision procedure for *residue-method provability*, with proofs on
both sides, has been applied exhaustively.

* **Positive side.** Every trap set is either provable with an explicit, independently verified
  certificate (types P0 and P1).
* **Negative side.** Otherwise the set carries a verified **homoclinic avoider orbit** (type H).
  That orbit rules out every SCC/descent certificate mod 2^m, at every m. (Other residue-based
  methods, such as YAH's rewriting/SAT encodings, non-power-of-2 moduli or other potentials, are
  not excluded.)
* **The YAH table.** On subsets of Z/8 for 3x+1, the P/H verdict agrees with the
  Yolcu–Aaronson–Heule proved/open table on every set they list. Their open sets {0}, {1}, {5},
  {7}, {5,7} are all H (the prize Conjectures 4.11–4.14 are {1}, {5}, {7}, {5,7}; {0} is open
  but not a numbered prize conjecture); their proved sets {2}, {3}, {4}, {6}, {1,5}, {1,7} are all P. In full:
  A ⊂ Z/8 is provable iff A ⊄ {1} and A ⊄ {0,5,7}.
* **New settled systems.** The 5x+1 and 7x+1 censuses give many new settled systems (the 490
  minimal provable sets overall include YAH's own proved mod-8 sets and are mostly routine
  instances of one method; see the census row below). None of
  their minimal sets is P0: every one needs the new Theorem 2, which removes isolated expanding
  2-adic cycles.

`python3 check.py` runs every check, exits 0, and takes about 10 s.

## General theorems (all PROVED; proofs in theory.md, family.md and entropy.md)

| # | statement | where |
|---|---|---|
| Lemma 0 | Walks in the avoider graph G_m^A lift to cylinders. A closed walk has a unique rational periodic lift with the cycle's multiplier. | theory.md |
| Thm 1 | Every cycle of G_{m0}^A contracts ⇔ (the same at every level) ⇔ no expanding periodic avoider ⇔ an avoider descent certificate exists. In that case there is an exact integer potential φ, and every avoiding orbit enters [1, B]. This is task item (1); the Karp/Bellman–Ford search is only a search, and φ is verified exactly. | theory.md |
| Thm 2 | **SCC certificate.** Suppose every SCC of G_m^A is trivial, a simple cycle, or contracting. Then S(T, A) holds, with the cycle list given by the simulation of [1, B] plus the positive-integer lifts. Expanding simple cycles (for example −1 under C, −1/3 under C_5, −1/5 under C_7) are allowed. This answers task item (4): provable despite an expanding cycle. | theory.md |
| Thm 3 | **Homoclinic obstruction.** Suppose there is z ≡ x* (mod 2^{m0}), not on the orbit of x*, with an avoiding orbit and T^j z = x*, where x* is an expanding periodic avoider. Then the SCC of x* is non-simple and non-contracting at every level m. So no SCC certificate and no descent certificate exists, at any modulus. | theory.md |
| Thm 4 | A non-simple SCC with an expanding cycle at some level yields an explicit homoclinic orbit (constructive). | theory.md |
| Cor 5 | Provable at some level ⇔ provable at level m0 = max(k, β) ⇔ no homoclinic orbit. Every trap set is exactly one of P0, P1 or H. The procedure runs in time about linear in 2^k. | theory.md |
| Thm F | **Families.** If G_k^A of C_{a0,b0} has only trivial and simple SCCs, the conclusion holds for **all** odd a ≥ 1 and b ≥ 1 in the class mod 2^k. Examples: every trajectory of n/2 \| an+b (a ≥ 3) contains a term ≡ 4 (mod 8). For a ≥ 5 there are two uniform odd trap pairs mod 8 per class; for a ≥ 9 there are six triples or quadruples mod 16. | family.md |
| Thm E | **Density on the frontier.** #{n ≤ X avoiding A} = O(X^{log2 λ}), with an exactly certified Perron bound λ. It applies to C-avoiders for arbitrary A (a C-avoider is a T-avoider), and λ < 2 is certified exactly for all 130 maximal H sets. It recovers the CLS-056 and CLS-066 exponents 0.4057 and 0.8792. For every 3x+1 frontier set mod 32 the exponent is ≤ 0.613. | entropy.md |

## Census (PROVED; census.md)

| map | sets classified | provable / H | minimal provable | frontier (maximal H) |
|---|---|---|---|---|
| 3x+1, all residues mod 8 | 256 | 247 / 9 | 7 | {1}, {0,5,7} |
| 3x+1, all residues mod 16 | 65536 | 64405 / 1131 | 47 | 8 sets |
| 3x+1, odd residues mod 32 | 65536 | 41805 / 23731 | 76 | 35 sets |
| 5x+1, mod 8 all / mod 16 all / mod 32 odd | 256 / 65536 / 65536 | 240/16, 62752/2784, 20688/44848 | 10 / 73 / 115 | 3 / 10 / 36 |
| 7x+1, mod 8 all / mod 16 all / mod 32 odd | 256 / 65536 / 65536 | 240/16, 62602/2934, 15434/50102 | 10 / 63 / 89 | 3 / 8 / 25 |

**Key frontier fact.** The YAH $500 Conjecture 4.14 ({5,7} mod 8) lifts into exactly one maximal
H set mod 16: F* = {0,3,5,7,8,10,13,14,15}.

* "Every C-trajectory not reaching 1 meets F*" is H: it is the weakest mod-16 weakening of 4.14
  that is beyond every SCC/descent certificate mod 2^m.
* Adding any one of the residues 1, 2, 4, 6, 9, 11, 12 makes it PROVED.

**Minimum sizes.** The minimum size of a provable odd trap set for 3x+1 mod 2^k is 1, 2, 3, 4 for
k = 3, 4, 5, 6. This is PROVED by exact branch and bound (minsize.py). Whether it keeps going to
density 0 is EVIDENCE/OPEN; see census.md.

## New systems (systems.py)

Every system below is: T(n) = 1 if n mod 2^k ∈ A, else C_a(n).

| id | rule | question | answer | status | tier |
|---|---|---|---|---|---|
| trap7_57 | 7x+1, A = {5,7} mod 8 → 1 | GLOBAL | yes; the only cycle is (1 8 4 2) | PROVED (hand + certificate) | 1 |
| trap5_17 | 5x+1, A = {1,7} mod 8 → 1 | GLOBAL | yes; every 5x+1 trajectory meets 1 or 7 mod 8, with no exceptions | PROVED (hand + certificate) | 1 |
| trap5_hi16 | 5x+1, A = {9,11,13,15} mod 16 → 1 | GLOBAL | yes; untrapped orbits end in (1 6 3 16 8 4 2) | PROVED (hand potential, near-critical 125/128; certificate) | 2 |
| trap5_c13 | 5x+1, A = {3,5,7,15,17,23} mod 32 → 1 | complete fate | every orbit meets A or ends in the 13-cycle; A is minimal | PROVED (certificate) | 2 |
| trap7_m32 | 7x+1, A = {5,7,13,23,27} mod 32 → 1 | GLOBAL | yes; the only untrapped cycle is (1 8 4 2) | PROVED (certificate) | 2 |
| trap3_m32 | 3x+1, A = {7,15,25} mod 32 → 1 | GLOBAL | yes (a minimum-size odd trap mod 32) | PROVED (certificate) | 2 |
| FAM_4mod8 | n/2 \| an+b, all odd a ≥ 3, b ≥ 1; A = {4} mod 8 | every orbit meets A? | yes, uniformly in a and b | PROVED (Thm F, hand proof) | 1 |
| FAM_oddpairs8 | n/2 \| an+b, odd a ≥ 5, b ≥ 1; the two odd pairs for (a,b) mod 8 | every orbit meets A? | yes, uniformly | PROVED (Thm F) | 1–2 |
| 490 census sets | every minimal provable set of the 9 censuses (not 490 new results: they include YAH's proved mod-8 sets {2}, {3}, {4}, {6}, {1,5}, {1,7} (and {0,1}), and most are routine instances of one method; the new content is the method, the 5x+1 and 7x+1 censuses and the frontier description) | S(C_a, A) | certified, with cycle list | PROVED | 2 |

**What stays OPEN.** Every H set: 130 maximal H sets are listed, and they include the YAH
conjectures and F*. For these, the following hold, all PROVED:

* no SCC or descent certificate exists at any modulus 2^m (Thm 3);
* there are explicit homoclinic witnesses;
* the counterexamples have density 0, by Thm E (via the C-avoider/T-avoider remark and the
  exact λ < 2 certificates for all 130 maximal H sets).

Whether they hold is open. Settling any of them needs control of interleaved runs near an
expanding 2-adic cycle, which is the 3x+1 difficulty itself. It is a precise negative finding
that no SCC/descent certificate mod 2^m can work there; other residue-based methods are not
excluded.

**Novelty.**
* The YAH comparison uses the YAH statements as transcribed in
  census/round2/literature/yah_avoid*.md (arXiv:2105.14697 v3, §4.5).
* Theorem 1 is close to YAH's residue-graph ranking (their Prop. 4.7, as transcribed there).
* I did not check the novelty of Theorems 2–4, F and E, or of the census. Thm E generalises
  census/lhf/traps CLS-056 and CLS-066.

## Files

* `traps_lib.py`: maps, avoider graphs, Tarjan, certificate builder, lifts, Theorem-4
  construction.
* `verify.py`: an independent verifier. It re-derives the graph by brute force and checks only
  what the proof of Theorem 2 uses.
* `census.py`: exhaustive classification. Its output is `results/census_*.json`.
* `family.py`: Theorem F. Output: `results/family_k*.json`.
* `entropy.py`: Theorem E. Output: `results/entropy_frontier.json`.
* `minsize.py`: minimum provable sets. Output: `results/minsize_*.json`.
* `systems.py`: the new systems as step functions.
* `theory.md`, `census.md`, `family.md`, `entropy.md`, and one `<id>.md` per named system.
* `check.py`: all checks; sections [1]–[7] are mapped to the claims in its docstring.

## Refereeing

Fixes applied from REFEREE.md (no mathematical change to any claim):

* trap7_57.md: "n ≡ 3 (mod 8) iff 16 | 5n+1" corrected to "iff 8 | 5n+1"; run argument restated via v_2(5N+1) = v_2(5n+1) − 1.
* trap5_17.md: "n ≡ 5 (mod 8) iff 16 | 3n+1" corrected to "iff 8 | 3n+1"; run argument restated likewise.
* check.py [5]: now tests both congruence equivalences and the valuation drop exactly, not only the multiplicative identity.
* family.md, check.py [4]: added the exact check that every simple cycle of every minimal odd type-F set has E ≤ 2o (mod 8) / E ≤ 3o (mod 16).
* entropy.md: added the remark that a C-avoider is a T-avoider, so Thm E applies to arbitrary A (including even residues).
* check.py [6]: exact certificate λ < 2 for all 130 maximal H sets, including the mod-8/mod-16 sets with even residues and F*.
* README, census.md, theory.md, entropy.md, trap5_c13.md: "beyond every residue method" narrowed to "beyond every SCC/descent certificate mod 2^m".
* README, census.md, theory.md: {0} no longer described as one of the prize Conjectures 4.11–4.14.
* README, census.md: "490 census sets" qualified (includes YAH's proved mod-8 sets; mostly routine instances).
* census.md: P0/P1 markers of the mod-8 minimal provable sets disambiguated (only {6} and {1,7} are P0).
