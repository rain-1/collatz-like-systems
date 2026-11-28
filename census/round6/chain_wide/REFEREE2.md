# REFEREE 2: round 6, lens `chain_wide` (second pass, after the REFEREE1 repair)

Referee: independent agent (Referee 2). I read `README.md`, `THEORY.md` and `REFEREE1.md` in full,
plus the parts of `chainlib.py`, `chain_systems.py`, `check_revision.py`, `verify_range.c` and
`round3/density/density_lib.py` that the proofs rely on. I re-derived every PROVED statement and
re-ran the prover's checks. I also wrote my own check script from scratch,
`referee2_check.py`, and ran it (output in `referee2_check.out`: **241 PASS, 0 FAIL**, exit 0,
about 1 minute, with `R2_BITS=28`). I did not edit any prover file and did not commit.

**Summary verdict.** The mathematics is sound and the REFEREE1 repairs were made honestly. Every
number I recomputed agrees with the data. That covers the state graphs, certificates, E*, survivor
classes, cycle lists, family counts and the core W counterexample. I found one new defect, which
needs a repair because it sits inside a PROVED statement: a clause added to Corollary 5 during the
repair is false. Read literally, it would turn the window criterion into a false "proof" of GLOBAL
for split5_3 and the S-family. Deleting the clause fixes it. There are also three small factual
or wording slips.

**No census system is claimed settled, and none is settled.** The only systems claimed GLOBAL are
63 family members with no expanding edge. That claim holds, and it is trivial. Nothing in the lens
would settle 3x+1, because every statement either assumes escape or bounds an escaping orbit.

needs_repair: **true**. One substantive wording fix (Corollary 5) and three minor ones. No GAP in a
core proof.

---

## 1. REFEREE1 items: were they honestly resolved?

| REFEREE1 item | status now | my evidence |
|---|---|---|
| Signed E* used g instead of 2g in λ | **Resolved.** `multiplier_E(..., factor=2)` uses g' in both places | My own rigorous upper bound (60-bit verified powers, my graph, the certificate verified by my code): 3x−1: 24.07889443 ≤ json 24.07889444; m3_b: 50.73726252 ≤ json 50.73726254 (`[D]`) |
| Signed raw-time claim needs control of Z inside an edge | **Resolved** by the new hypothesis (S1) | My own count of raw steps with v ≠ 0 per edge is ≤ 1 for 3x−1 and m3_b. A negative control (n+2 then 3n+1 in one edge) is detected (`[B]`). The control caught a bug in my own first draft, so the check can fail |
| Core W fails (R) | **Resolved**: the claim is withdrawn and Prop. 7 now has an update-time version | My graph: (R) fails for sf3_137 and holds for 5x+1 and 7x+1 (`[B]`). On my own orbit segments I found a raw drop below a selected start for core W (`[G]`). [R3] reproduces 263 → … → 223 with raw multiplier 27/32 |
| Families: 103 negative-drift members dropped | **Resolved**: γ is clipped to 1, giving 343 certified members | Recounted with my graph builder: 343 certified, 63 with no expanding edge, 35 (R)-failures (all in S4), 270 division-free loops (all in m3) (`[H]`). For 30 random certified members I checked the certificate exactly with my own power bounds and recomputed the forced class, residue and mass with my own tree |
| Wording (units, Thm 2 typo, "F ≠ 1", mass is an upper bound, "survive" means ≥ 1, Prop. 5.1, A(B) = 0, hypotheses of the headline, split5_3 figure) | **Resolved, except one new error**: the repair of "survive" added a false "equivalently > 1 at updates" clause (§2, Cor. 5) | see below |

The README is candid that the REFEREE1 script did not finish on the revised data (`A_of` loops
for F = 1) and why. That is acceptable.

## 2. Re-derivation of the proofs

| claim | verdict | notes |
|---|---|---|
| §0 setting, units | CONFIRMED | Units are now stated and used where needed. I checked p ∤ u for all 26 named tables and for every certified family member (`[B]`, `[H]`) |
| Lemma 1 (restart) | CONFIRMED | Re-derived. With b = β + Kc, the child digit d of t maps to the child u₀d + c mod p of the σ-tree, a permutation, so the class of y mod pK decides the child. Tested exactly on 5 orbit segments for each of 26 systems, 19 steps from random l (`[G]`) |
| Lemma 2 | CONFIRMED | Pure splits multiply K by p. There are finitely many states, so only boundedly many updates share a raw time |
| Lemma 3 and (1) | CONFIRMED | Classes mod K_σ p^j with p^j ≥ X contain at most one integer in [1, X]. Summing over states gives W |
| Lemma 4 | CONFIRMED | Both inequalities hold. With c = e^{−1/s}: log max(A, c) ≤ −1/s + A^s/s |
| Theorem 1 | CONFIRMED | Telescoping, capping with H, B ≤ b_j (also for signed G, via G⁺) and the exponent η < 1 are correct (the constant 2p could be p+1; harmless). E < ∞ follows |
| Theorem 2 | CONFIRMED | j = ⌈log_p X⌉, the exact split log(y_{l+j}/y_l) = log A + log(Z_{l+j}/Z_l), and each increment lies in ≤ j windows. The typo is fixed. The raw-time corollary R·V(X/c_raw) holds. It uses only (P) (partial intercepts ≥ 0 and value ≥ c_raw·y_l), not (R); stating (R) is harmless |
| Theorem 3 | CONFIRMED | Re-derived: E ≤ g'Σ1/y_l, grouping by [p^k, p^{k+1}), self-consistency, and E < ∞ from Thm 1. The extra p^θ (Thm 2 is used at X = p^{k+1}, where p^{(k+1)θ} would do) is conservative. Signed: \|u\| ≤ g/p^{k0} ≤ 1/2 is required and checked. Raw times: under (P) Z is monotone inside an edge; under (S1) it equals an update value |
| Constants E* (all 23 systems, all ranges) | CONFIRMED | My own rigorous evaluation from certificates verified by my own code: every json E* is ≥ mine, within 3e-8 relative (`[D]`). Checks: 3x+1 e^{E*} = 31.693 < 31.7 (2^68) and 1.693·10^5 < 1.7·10^5 (2^32); split5_3 E* = 5.314·10^-5 at 2^48 and 2.841·10^-7 at 2^66; for p = 3, 3^{k0} ≤ 2^{range} (k0 = 20, and 17 for m3_g) |
| Cor. 3.1 | CONFIRMED | x = λx + C over a lap. C = 0 ⇒ λ = 1 ⇒ (units) every u = w = 1 ⇒ v = 0, a branch n ↦ n, which no treated table has. The signed caveat is correct |
| Theorem 4 (a)–(e) | CONFIRMED | All parts re-derived: (a) from (R) plus monotone Z; (b) minimality and the last edge with F ≠ 1; the two-slope count from a ∈ (eL, eL+1]; (c) the unrolled intercepts with weights in (0, 1]; (d) from k* = min{k : ρ^k κ_max > 1}; (e) from Z → Z_∞. On orbit segments of all 26 systems (45–299 links each, starts built by a beam search in deep multiplier-survivor classes), (a), (b), (c) (exact identity and both bounds), (d) (forced residue) and Lemma 1 all hold with 0 violations (`[G]`). That includes sf3_13 and sf3_135, where the prover's raw test had no samples |
| Signed Theorem 4 | CONFIRMED | (a) for multipliers, heights ≥ x_i e^{−E_i}, and (b), (d), (e) as stated; the x_i are distinct because each link has a raw step |
| **Cor. 5** | **CONFIRMED_WITH_FIX (substantive)** | The criterion itself is correct for N^mult, N_T and N_b with "survive" meaning "every raw prefix multiplier over the first b raw steps is ≥ 1". **The added clause "or equivalently for this purpose every update multiplier over the first b updates is > 1 (Theorem 4(a) gives strict inequality at updates). Either set contains every selected start" is false.** N_b is a set of starts n, so its updates are those of the root tree of n. Theorem 4(a)'s strict inequality holds at the updates of x_0's tree, which continue as the σ_{t_i}-tree of x_i, not the root tree of x_i. For split5_3, the S-family (sf3_*, desc_s32_plus9) and in general when Q > p, the root edge (1,0) → digit 1 is a pure split with F = 1 and no raw step. So every odd n, including every selected start (all of them are 253 mod 256 for split5_3), has root-tree update multiplier P_1 = 1, not > 1 (`[J]`). With the clause, N_b = ∅ for b ≥ 1, the hypothesis of Cor. 5 holds in every window, and the corollary would "prove" GLOBAL for split5_3, which is false as a deduction. **Fix:** delete the clause, or replace it with "every root-tree update multiplier over the first b updates is ≥ 1", which raw ≥ 1 implies |
| Prop. 5.1 | CONFIRMED (nearly tautological, now labelled as such) | Part 1 holds under (P) and units. Part 2 is Theorem 4. The O(X^{θ*+ε}) bound uses N^mult ⊆ N_T together with round 3 Theorem 1 (general, read) and Theorem 2(a) |
| §5 (count law, C*) | CONFIRMED (heuristic, honestly labelled) | C* = 1/(1−θ) with the certified θ. "Depth factor 1" matches round 5 microrange Corollary D (τ-version, X = 2^m, a density-one set of m, depth log2 X + O(log log X)), which I read. It transfers to every odd d because τ depends only on parity words |
| Prop. 6 | CONFIRMED | f(s, γ) = (γ−1) log p + log ρ(Σ F^s) is convex in s, with gradient (Δ, log p) at (0, 0) on the closed class. This uses round 3 Theorem 2(b), which assumes a unique closed class; that holds for the three expanding maps |
| Prop. 7 | CONFIRMED_WITH_FIX (minor) | The main statement and the update-time version without (R) are correct. **The side remark "Under (P), Σ_t 1/x_t < ∞ is equivalent to sup Z < ∞" is proved only in the direction ⇒.** The given proof shows sup Z < ∞ ⇔ Σ over updates of G_e/(F_e y_l) < ∞. That controls only the raw times with v ≠ 0. For the three maps it is applied to, every v = 0 step is n/2, so halving chains give the converse. In general the converse is unproved. *Fix: say "implies", or prove the converse for maps whose v = 0 steps all have w > 1* |
| EVIDENCE (expanding) | CONFIRMED as EVIDENCE | Consistent with my `[G]` runs on 5x+1, 7x+1 and core W |

Quoted results: round 3 Theorems 1, 2 (read in `round3/density/theory.md`); round 5 Corollary D
(read); the repo's split5_3 range 2^66 (read in `split5_3_s27.md` §"Verification through 66 bits").
**Barina's 2^68 is quoted from memory** (flagged by the prover). My own recollection agrees, but I
have not checked it either. Every constant is also given for the self-verified 2^32 range. I
re-ran the prover's `verify_range.c` for 3x−1 at 2^32 and got `OK 32 667 big 0`, identical to
`data/ranges_32.log`. Lagarias (2.31) and (2.32) are said to have been checked in the scanned
source; I did not re-check them.

## 3. Systems and cycle lists (brute force)

No census system is newly settled, so there is no type-(c) proof to attack. Two kinds of check
remain.
* **Range hypotheses.** My own C brute force (`[F]`, written inside `referee2_check.py`) shows that
  every n < 2^28 (2^24 for m3_g) either drops below n or returns to n. Leftovers were finished
  exactly in Python. The cycle minima found equal the `named.json` lists for all 23 systems. Examples:
  3x+5 {1, 5, 19, 23, 187, 347}; 3x+13 with 10 cycles; split5_3 {1, 3, 5, 61, 125}; m3_g {4, 8}. A
  negative control confirms that a missing cycle would be reported.
* **The 63 "no expanding edge" family members, claimed GLOBAL by Cor. 3.1.** The proof is right: (N)
  is verified, P_l ≤ 1, and Cor. 3.1 needs P_t → ∞ on a non-periodic orbit. Brute force (`[I]`):
  every n ≤ 20000 is eventually periodic for all 63. *Wording:* the README calls them "trivially type
  (a)". In the README's own usage, type (a) means "settled by a descent certificate", and no descent
  certificate was produced. Say "GLOBAL by Cor. 3.1" instead.
* **Does any argument settle 3x+1?** No. Theorems 1–4 and Cor. 5 are consequences of escape or bounds
  on an escaping orbit. The lower occupation bound (log X) and the upper bound (X^θ) do not meet.

## 4. Wide scans (spot checks with my own code)

* **Named systems** (`[B]`, `[C]`, `[E]`), all 23 with my own graph builder: number of states, the
  slope set, ρ, g, R, c_raw, (R), the sign flag, A(1), A(10) and k* all agree. The certificate
  (prover's w, my exact check) gives the stated θ and s, and W matches exactly. The survivor
  classes at depth 14 / 9 agree in D, residue, number of classes and rational mass.
* **Families** (`[H]`): all 709 rows were rebuilt with my builder, and the counts quoted above agree.
  For a random sample of 30 certified members: exact certificate check of θ, plus forced class and
  mass; all agree.
* **One count is wrong:** README line 154 says "positive drift (97)". The data have **96**
  (1 S3 + 1 S4 + 4 split + 90 m3). No member has drift exactly 0. *Fix: 96.*

## 5. Honesty, labels, novelty

* "Settles nothing in the census" is accurate. PROVED, EVIDENCE and OPEN are used correctly. Prop.
  5.1 is now labelled "nearly tautological". The core W downgrade is stated plainly.
* Novelty: "not checked" beyond Lagarias 1985, which is appropriate. The all-elements occupation
  bound for 3x+1 has the same exponent as Lagarias's U_D bound. It needs a literature search before
  anyone calls it new.
* Nits:
  * README row "m3_g has θ* = 1906/1907" should say "certified θ" (θ* is the optimum, slightly
    below it).
  * README row K7: "multiplier constants e^{0.22} (K7) down to e^{1.1·10^-5}". The largest
    constant among those cores is e^{1.24} (sf3_357), so say "between e^{1.1·10^-5} and e^{1.24}".

## 6. Required repairs

1. **Cor. 5 (THEORY §4, substantive):** delete "or equivalently for this purpose every update
   multiplier over the first b updates is > 1 (Theorem 4(a) gives strict inequality at updates).
   Either set contains every selected start", or replace it with "≥ 1 at root-tree updates".
   Counterexample to the clause: split5_3 and the S-family, root edge (1,0) → (2,1) with F = 1
   (`referee2_check.py [J]`).
2. Prop. 7: "equivalent" → "implies" (or prove the converse).
3. README: "positive drift (97)" → 96; "trivially type (a)" → "GLOBAL by Cor. 3.1"; m3_g "θ*" →
   certified θ; the K7 row's range of constants.

## 7. Verdict list

| claim | verdict |
|---|---|
| Lemmas 1–4 | CONFIRMED |
| Theorems 1, 2 (occupation bounds) | CONFIRMED |
| Theorem 3 and all E* in named.json (incl. revised signed values) | CONFIRMED |
| Cor. 3.1 | CONFIRMED |
| Theorem 4 (a)–(e), signed version | CONFIRMED |
| Cor. 5 window criterion | CONFIRMED_WITH_FIX (delete the false "equivalently > 1 at updates" clause) |
| Prop. 5.1 | CONFIRMED |
| §5 count-law discussion | CONFIRMED (heuristic) |
| Prop. 6 | CONFIRMED |
| Prop. 7 (incl. core W update-time restriction) | CONFIRMED_WITH_FIX ("equivalent" → "implies") |
| Named-systems table (θ, W, ρ, A(B), k*, forced class, mass, E*) | CONFIRMED |
| Cycle lists and range certificates | CONFIRMED (own brute force to 2^28; prover's 2^32 rerun for 3x−1) |
| Families table and coverage (343 / 63 / 35 / 270) | CONFIRMED_WITH_FIX (97 → 96) |
| 63 no-expanding-edge members GLOBAL | CONFIRMED_WITH_FIX ("type (a)" → "GLOBAL by Cor. 3.1") |
| 3x+1 rows (Thm 2 with Barina, Thm 3, Thm 4 forced classes) | CONFIRMED (2^68 quoted from memory, flagged) |
| split5_3 rows (31 per ten octaves, 256 \| x+3, E* figures) | CONFIRMED |
| "Nothing settled" / novelty statements | CONFIRMED |
| REFEREE1 repairs | CONFIRMED (honestly resolved) |
