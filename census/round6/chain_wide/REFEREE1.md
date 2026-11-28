# REFEREE 1: round 6, lens `chain_wide`

Referee: independent agent (Referee 1). I read `README.md` and `THEORY.md` in full, re-derived every
PROVED statement, re-ran the prover's checks, and wrote and ran my own check script
`referee1_check.py` (output in `referee1_check.out`: 266 PASS, 4 FAIL; the 4 FAILs are the findings
below and are meant to fail until they are repaired). I did not edit any prover file and did not commit.

**Summary verdict.** The mathematics is sound. Lemmas 1–4, Theorems 1–4, Corollaries 3.1 and 5,
Proposition 5.1 and Propositions 6–7 hold as stated for the systems they are applied to, with three
small exceptions. All are repairable without changing a headline result.
1. The signed multiplier constants (3x−1, m3_b) are computed with a formula that differs from Theorem 3
   and come out about 1e-9 (relative) **below** the bound that Theorem 3 proves.
2. Core W, one of the three expanding examples, fails hypothesis (R). So the raw-time part of Prop. 7
   does not apply to it, and I found a concrete raw drop.
3. The families coverage statement is wrong. 103 negative-drift members were dropped by a code
   assertion, and the README describes them as "positive drift".

There are also some wording and labelling fixes. **No census system is claimed settled, and none is
settled.** The theorems only describe what an escaping orbit would look like. They cannot settle 3x+1,
and the README says so plainly.

needs_repair: **true** (substantive fixes 1–3 below; no GAP in a core proof, nothing WRONG in the
mathematics).

---

## 1. Prover's checks

* `check_chain.py` with the numpy venv: exit 0 in 13.5 s. Its output is identical to `data/check_chain.out`.
  It has two honest SKIPs, for sf3_13 and sf3_135.
* `verify_range.c`, recompiled by me. `./vr 32 …` for split5_3 gives `OK 32 84 big 0` (85 s), which
  matches `data/ranges_32.log`. Negative control: when I removed the cycles at 5, 61 and 125 from the
  list, it gave `FAIL 5`. So the verifier can fail. The C code is sound: `__int128` products stay below
  2^127 for `u < 128` and `x < 2^120`, and BIG starts are finished exactly in Python. The induction
  "every n < N0 reaches a smaller value or a listed cycle" ⇒ "every n < N0 is eventually periodic" is
  valid. It also implies that **no unlisted cycle** has its minimum below 2^32 (2^27 for m3_g), because
  such a minimum would neither drop nor hit a listed cycle.

## 2. Re-derivation of the proofs

Setting (§0). Section 0 says that unit multipliers "are not needed for the statements below". That is
**not true for Corollary 3.1, second half**, or for Prop. 5.1, which assume them, and it is not true for
the finiteness of G(T). In the treated systems the condition holds everywhere. I checked p ∤ u for all
26 named tables ([A]). By construction it also holds in every family: m3 skips a ≡ 0 mod 3, and the
S/split families have odd u. *Fix: delete that sentence, or say "used in Cor. 3.1(ii) and Prop. 5.1;
all systems treated have them".*

| claim | verdict | notes |
|---|---|---|
| Lemma 1 (restart) | CONFIRMED | Re-derived. With `a = K u0` and u0 a unit, the child digit of t is fixed by `y mod pK`. The new state `(K', β')` is the same in both trees because `ad+b ≡ Kd''+β (mod Kp)` and division by w keeps the congruence mod `K' = Kp/w`. My own tree code checks `y_{l+1} = F y_l + G` exactly at every update of every orbit in [G] (an assertion). |
| Lemma 2 | CONFIRMED | Updates at one raw time differ in K. There are finitely many states. |
| Lemma 3, (1) | CONFIRMED | Iterating `N w ≤ w` gives `Σ A^s ≤ (w(σ)/w_min) p^{jθ}`. Classes mod `K p^j ≥ X` hold at most one integer ≤ X, and the pairs for a fixed σ have distinct y. |
| Lemma 4 | CONFIRMED | |
| Theorem 1 | CONFIRMED | The telescoping with `H = log min(·, X)`, the bound `log max(A, c) ≤ −1/s + A^s/s` with `c = e^{−1/s}`, `B ≤ b_j` (also with signed G, via G⁺) and the exponent bookkeeping are all correct. |
| Theorem 2 (V(X) ≤ W p^θ X^θ + s⌈log_p X⌉E) | CONFIRMED_WITH_FIX | The proof is correct. Typo: "log A_l ≤ −1/s + A_l^s" should read "+ A_l^s/s" (the next line already uses /s). The raw-time corollary `R·V(X/c_raw)` is correct under (P)+(R). The README 3x+1 row is consistent with it: R = 2, c_raw = 1, W = 1, s = 41/84. |
| Theorem 3 (multiplier bound), (P) case | CONFIRMED | Recomputed in 50-digit Decimal from the formula ([E]). Every (P) value in `named.json` is ≥ my value and within 3e-8 relative (rigorous upward rounding). 3x+1: e^{E*} = 31.69 (2^68) and 1.693e5 (2^32), so "< 31.7" and "< 1.7·10^5" hold. split5_3 at 2^48: 5.32e-5 < 5.4e-5 < log 1.000073. For p = 3, `3^{k0} ≤ 2^{range}` was checked. |
| Theorem 3, signed case | **CONFIRMED_WITH_FIX** | THEORY states `E* = g'WpθS1/(1 − g' s S2)` with g' = 2g. `chainlib.multiplier_E_signed` returns `2·gWpθS1/(1 − g s S2)`, which has g, not 2g, in the denominator. That is smaller than the proved bound: par_3_m1 24.07889438 < 24.07889443, and m3_b 50.73726249 < 50.73726252. Both FAIL in [E]; the relative gap is about 1e-9, larger than the 36-bit rounding slack. Numerically harmless, but the "exact" constants are not upper bounds. *Fix: use 2g in `lam` too, and recompute.* The raw-time two-sided statement for signed maps also needs a remark. E controls Z only at updates, and inside an edge Z can move with intermediate constants. For both signed named systems, every edge has at most one raw step with v ≠ 0 (checked in [E]), so raw-time Z equals an update-time Z there. *Fix: state this condition, or restrict the signed claim to update times.* |
| Cor. 3.1 | CONFIRMED | `C = 0 ⇒ λ = 1 ⇒` all u = w = 1 (this step needs units) `⇒ v = 0`. The 3x−1 lap multipliers 3/2, 9/8 and 2187/2048 were checked by hand. |
| Theorem 4 (a)–(e) | CONFIRMED | All parts re-derived. (b): the last non-unit edge is not the first one, so the update before it lies after t_i. Wording: "if the link has more than one edge" should be "more than one edge with F ≠ 1". The two-slope count follows from `a ∈ (eL, eL+1]`. (c): the unrolled intercepts have weights `P_{t_{i+1}}/P_{end(k)} ∈ (0,1]`. (d): "the first k* edges expand" should read "the first k* edges with F ≠ 1". (e) is correct. In the signed case the x_i need not increase, but "last i with x_i < X" still works, and the x_i are distinct because each link has a raw step. **Tested on integer orbits ([G])**: for each of the 23 named systems I built 6 starts whose root path keeps P ≥ 1 for 120 (p = 2) or 80 (p = 3) updates, then selected the successive last minima. Over 20–141 links per system, (a), (b) with the exact two-slope formula, (c), monotone Z, and the forced class (d) all hold. That includes 23 and 17 forced-class hits for sf3_13 and sf3_135, the two systems where the prover's own test found no samples. |
| Forced classes and survivor counts (README table) | CONFIRMED | My own σ-tree code (all states, depth 14 or 9) reproduces exactly, for all 23 systems, every D, residue, number of classes and rational mass in `named.json`. It also reproduces ρ, A(1), A(10), k*, R, c_raw, (R), the sign flag and g. Note: the "survivor mass" is Σ 1/M over the classes of all states. Root classes of different states can overlap, so it is an upper bound on the Haar mass of the union, not the mass itself. *Fix: say "at most".* For 3x+d, members of N^mult (raw definition) are 3 mod 4 when d ≡ 1 (mod 4) and 1 mod 4 when d ≡ 3 (mod 4). Confirmed by hand and in [G] for all 8 values of d. |
| Certificates / θ | CONFIRMED | All 23 certificates (the prover's w) were re-verified with my integer n-th-root power bounds ([D]), and θ and W agree. 3x+1: θ = 1082/1139 = 0.9499561 > θ* = 0.9499555 (numerical optimum), consistent with Lagarias's η ≈ 0.05004. |
| Signed version of Thm 4 | CONFIRMED_WITH_FIX | Same remark as Theorem 3 (raw-time heights inside edges). Fine for 3x−1 and m3_b. |
| Cor. 5 | CONFIRMED | Correct. When A(B) = 0 (split5_1 and desc_s32_plus9 with B = 1) the criterion is vacuous, which deserves a word. "Survive" in N_b should mean ≥ 1, not > 1: the S-family has slope-1 steps. |
| Prop. 5.1 | CONFIRMED (presentation) | Correct, but nearly tautological: N^mult ≠ ∅ ⇔ a divergent orbit exists ⇔ (Thm 4) infinitely many members. Calling it "the main new point" and a "gap statement" oversells it. Its content is only the remark that the window criterion is useful for finite-depth supersets only. The O(X^{θ*+ε}) bound uses N^mult ⊆ N_T, which holds only under (P). That hypothesis is stated. |
| §5 count-law discussion (C* = 1/(1−θ*)) | CONFIRMED (heuristic) | Conjecture E (round4/lead) has an additive `#Exc + eps(X)` error. So at depth K m with K > C* it does force window counts below A(B) ≥ 1. The quoted "proved depth factor 1 (m + O(log m))" matches round5/microrange Corollary D. That result covers the τ-version, X = 2^m and almost every octave; it carries over to all odd d because the parity-vector bijection holds for every odd d. Say "τ-version, density-one set of m" when quoting it. |
| Prop. 6 | CONFIRMED | Convexity of log ρ(N_{s,γ}) with gradient (Δ, Λ) is quoted from round 3, Theorem 2(b). |
| Prop. 7 | CONFIRMED as stated; **application to core W is WRONG** | Core W (sf3_137) **fails (R)**. The edge from state (4,1) with residue 5 has raw prefix slopes 1, 1/2, 3/2, 3/4, and 1/2 < 3/4. The prover never checked (R) for the expanding maps: `named.json` covers only the contracting ones. On the orbit of 15 under core W, the selected multiplier minimum 263 is followed by the raw orbit 263, 790, …, 445, 446, 223, with raw multiplier 27/32 < 1 and value 223 < 263. *Fix: in the README row and §6, say that core W satisfies only the update-time conclusions (like the 31 S4 members). 5x+1 and 7x+1 satisfy (R), checked.* |
| EVIDENCE (expanding) | CONFIRMED as EVIDENCE | Rerun with my own code for (b), (c) and monotone Z on 270, 503 and 204 links. |

## 3. Wide scans (families)

* All 709 family rows are present. 240 are certified (9 + 171 + 24 + 36), and 31 S4 members fail (R).
  All of these counts are confirmed.
* Random sample of 30 certified members, recomputed with my own code: number of states, ρ, A(1),
  A(10), (R), sign, forced D, residue and mass at depth 14 or 9. All agree. 10 of them also had their
  certificates verified exactly with my own power bounds.
* **Coverage statement is wrong (CONFIRMED_WITH_FIX).** The README says non-certified means positive
  drift or a graph error. In fact **103** non-certified members have *negative* drift: S3 6, S4 84,
  split 4, m3 9. They failed only because `chainlib.certificate` asserts γ ≤ 1, and their best
  certificate has γ > 1, which means a very strongly contracting map. Since `N_{s,1} ≤ N_{s,γ}`
  entrywise, they satisfy (N) with γ = 1 (θ = 0). I verified this exactly for 12 of them. So the
  theorems apply to 343 members, not 240. These members are most likely already settled by descent,
  so the theorems hold vacuously for them. *Fix: clip γ to 1 (or record those members separately), and
  correct the "non-certified reasons" text, which currently shows an empty `cert: ` message.*

## 4. Ranges and cycle lists

There are no newly settled systems, so there is nothing to attack as a type-(c) proof. As a cross-check
of the range hypotheses of Theorem 3:
* For all 23 systems, brute force over all starts ≤ 65536 (4096 for m3_g) finds exactly the cycle
  minima listed in `named.json`.
* A numpy re-run shows that every n < 2^22 (2^16 for m3_g, plus 2^14 exact in Python) reaches a smaller
  value or a listed cycle. Starts that went above 2^56 were finished exactly.

## 5. Honesty, labels, novelty

* "Settles nothing" is accurate. Nothing in the lens would settle 3x+1: every statement is conditional
  on escape or is a bound on an escaping orbit. The occupation lower bound (log X) and upper bound
  (X^θ) do not meet, as the README says.
* Barina's 2^68 is flagged as quoted from memory. My own recollection agrees, but I have not checked it
  either. All constants are also given for the self-verified 2^32 range. Lagarias (2.31) and (2.32) are
  said to have been checked in the scanned source; I did not re-check them. "Novelty not checked" is
  stated, and that is appropriate. Bounding every element of a divergent trajectory, rather than U_D,
  is plausibly folklore-adjacent and needs a literature search before anyone calls it new.
* The README's "both results were proved only for split5_3" and "every single-prime table map with
  negative drift" should add: with unit multipliers, a finite G(T), and (for the chain theorem) (P) and
  (R).
* Minor: README row K7 says "multiplier constants e^{0.22} … down to e^{1.1·10^-5}", which is
  consistent with the table. README row split5_3 says "2.9·10^-7 at 2^66", while the table says 2.84e-07.
  Both are correct, but use one figure.

## 6. Required repairs

1. Signed E*: use g' = 2g in the self-consistency denominator, as THEORY states, and regenerate
   `named.json` for par_3_m1 and m3_b. Add the raw-time condition for signed maps (at most one
   nonzero-v step per edge, or update times only).
2. Core W fails (R): correct the README and §6 claims.
3. Families: include the 103 members with γ > 1 by clipping γ to 1, or report them correctly, and fix
   the coverage sentence.
4. Wording: the §0 sentence on units; the Theorem 2 /s typo; "edges with F ≠ 1" in 4(b) and 4(d);
   "survivor mass" is an upper bound; "survive" in N_b means ≥ 1; tone down Prop. 5.1 as the "main new
   point".
