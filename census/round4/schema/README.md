# Round 4, lens "schema": certificate schemas and the critical limit

**Bottom line.** No type-(c) system was settled; the hard success criterion was not met.
What this lens did produce:

1. **(A)** A proof of the **base-2 analogue** of round 3's depth conjecture for a designed
   reset family: an exact depth formula, a Diophantine Q² log Q growth law along the
   convergents of log₂3, and new depth records. The conjecture as stated in round 3, for
   the base-3 families B(3^k, 2) and C(3^k), remains **OPEN**. (The first version called
   this "a proof of round 3's conjecture"; withdrawn after REFEREE1.)
2. **(B)** A proof that the proposed "limit of cut-off systems" method cannot work for
   any type-(c) system. This extends the wall.
3. A working alternative family of approximants (window approximants). It has an explicit
   certificate schema, and it answers a round-3 open question. The extra statement it
   would need is stated exactly; it is equivalent to the original conjecture, or stronger.

All of this is agent-written. It was examined by one referee (REFEREE1.md, check
`referee1_check.py`), and this version repairs every item of that report; see "Revision
after REFEREE1" below. Labels: PROVED, EVIDENCE, OPEN.

## Results

| id | statement | status | file |
|---|---|---|---|
| A1 | Designed family D(m, word, h, i0): base 2, multipliers 3 and 1/2, resets, no translation nodes. CERT ⇔ λ < 1 and G_exit < Q. Exact k\* formula. Complete cycle list = {(1), the loop}. (Chain-residue case t₀ = 0 added after REFEREE1.) | PROVED | depth.md |
| A2 | With Christoffel loops, k\* ≥ h + 1 + qL, q = ⌊h log 3/\|log λ\|⌋. Using the convergents 2/1, 8/5, 65/41, 485/306, … of log₂3, λ → 1 and k\* ≥ c Q² log Q along a subsequence of moduli. This is the base-2 analogue of the round-3 conjecture for a designed reset family; the conjecture for B(3^k, 2) and C(3^k) remains OPEN. | PROVED | depth.md |
| A3 | Every CERT base-2 table with u ∈ {1, 3} has k\* ≤ Q + (log 3/log 2)(a_{k+1}+2)Q²(Q−1), where q_k ≤ Q < q_{k+1}. So depth is polynomial in Q: k\* = O_ε(Q^{μ+1+ε}), μ an effective irrationality measure of log₂3 (ε added after REFEREE1). The gap between Q² log Q and Q³ is OPEN. | PROVED (bound); OPEN (gap) | depth.md |
| A-rec | Depth records in this family: k\* = 41362 at modulus 256, **133534 at modulus 512**, **304506 at modulus 1024**. Upper bounds: A1 formula; independently decide.py for m ≤ 8 ([A5]) and REFEREE1 [R2] for m ≤ 10. Lower bounds: integer witnesses for m = 7, 8, 9 (mine) and m = 7..10 (REFEREE1 [R3]). Like-for-like base-2 comparison at modulus 64: 791 here against dch_S6_332. (dch_C27_2466 is base 3 at modulus 27, a cross-family comparison.) | PROVED | depth.md |
| B1 | **Cut-off wall.** If T is of type (c) and F is any finite set, every unit-multiplier T′ that satisfies the standing hypothesis (every cycle of its cylinder graph contains a division) and agrees with T outside a small enough neighbourhood of F is again of type (c). So T′ has no descent or accelerated certificate, and Theorem H does not apply. | PROVED | cutoff.md |
| B1-inst | Exact thresholds. 3x+1 cut at depth j: CERT exactly for j ≤ 2; type (c) for all j ≥ 3 (explicit witness −5). K7 cut at depth j: CERT for j = 2..5, each with the single cycle z = 0; type (c) for all j ≥ 6 (witness z = −49/17, multiplier 81/64). | PROVED | cutoff.md |
| W1 | Window approximants T_K (resets exactly on the high-multiplier windows R_K) are CERT, for every unit-multiplier system satisfying the standing hypothesis, (H1)–(P), and (1−δ)(K−m+e_max) < K (automatic when e_max ≤ m). | PROVED | window.md |
| W1′ | dist_{2^N}(3x+1)/2^N → 0 exponentially: dist ≤ Σ_{k>5N/8} C(N,k) ≤ 2^{N·H(5/8)} with H(5/8) = 0.95443… (so ≤ 2^{0.9545N}). This was OPEN in round3/dichotomy §7. Proved for the non-accelerated map n/2, 3n+1 that §7 is about (same R_N; direct proof and check [W1′p] added after REFEREE1), and for the accelerated map. | PROVED | window.md |
| W2 | An explicit certificate schema for 3x+1, uniform in N ≥ 4: the weights are a closed formula in the parity vector, and the exceptional set lies in [1, 80·2^{0.371N}]. | PROVED | window.md |
| W3 | For each N in [4, 26]: an orbit reaches (1 2) iff it eventually avoids R_N. So taking N → ∞ adds nothing; each member alone is equivalent to the conjecture. | PROVED | window.md |
| W4 | (S_C) ⇒ Collatz. (S_C): no N-window of the orbit of n has more than 5N/8 odd steps once N ≥ C log₂ n. It is a size statement, not a cylinder statement, and it is stronger than the conjecture. | PROVED (implication); OPEN (S_C) | window.md |
| W4-ev | max A(n)/log₂ n is 13.25 for n ≤ 20000 and 17.2 at 63728127, consistent with (S_C) for C ≈ 20. | EVIDENCE | window.md |

## Where exactly it stalls

* **Cut-off schema (task B as posed):** there are no certified members beyond j = J0
  (Theorem B1). The re-entry orbits that defeat certificates (−5 for 3x+1, z = −49/17 for
  K7) sit a bounded distance from x\*, so cutting near x\* never removes them.
* **Window schema:** the certificates exist and are uniform in N, but turning them into a
  proof of T requires "every orbit eventually avoids R_N". That statement is the
  conjecture itself (W3). Its quantitative form (S_C) uses the finite digit length of n
  and would close the argument (W4), but I could not prove it for 3x+1, for K7, or for
  any designed type-(c) system.
* **Sanity checks.** Nothing here proves 3x+1 or contradicts a known cycle or divergent
  orbit. W3 and W4 are conditional. B1 is a negative theorem. The CERT systems are
  approximants, not T.

## Files

| file | content |
|---|---|
| depth.md, depthlib.py, check_depth.py | Part A (check exits 0, about 12 minutes) |
| cutoff.md, schemalib.py, check_cutoff.py | Theorem B1 and its instances (about 1 minute) |
| window.md, windowlib.py, check_window.py | Theorems W1–W4 (about 2 minutes) |
| evidence_window.py | EVIDENCE for (S_C); not a proof |
| search_depth.py, best_member.py, search_depth.out | depth search; not proofs (the reported k\* are re-verified in check_depth.py) |
| REFEREE1.md, referee1_check.py | referee report and the referee's independent check (exits 0, about 40 s); not modified by me |

Every check uses ints or Fractions. Floats and decimals are used only to *guess*:
`depthlib.tstar_big` certifies its answer with exact integer comparisons.

## Honest limits

* The depth family is designed (it uses resets). It is not the S-family or the C(3^k)
  family, and it is base 2. Only a base-2 analogue of the round-3 conjecture is proved;
  the conjecture itself (base-3 families B(3^k, 2), C(3^k)) is OPEN. Records are
  family-relative (deep.md).
* The k\* at m = 10 is verified in this folder's own checks by the exact formula only.
  REFEREE1 independently computed Λ by exhaustive walk search and iterated an integer
  witness for it ([R2], [R3] in `referee1_check.py`).
* I did not look up the best published irrationality measure of log₂3.
* Novelty: not checked for any item. Christoffel words and their balance property are
  standard; the window or large-deviation viewpoint resembles Terras/Everett density
  arguments.
* Relevant fact: round-3 `divergence/` already proved divergent orbits (fx10_64_s7) for
  systems that are technically of type (c), since every divergent orbit lives in a type-(c)
  SCC. Those are trap systems in which every cycle expands, so they do not touch the
  convergence wall. I do not count them.

## Revision after REFEREE1

REFEREE1 confirmed every theorem (several with fixes) and found no false mathematics
beyond the items below. No status was upgraded to a type-(c) success; the hard criterion
is still not met. Each item, and what was done:

| referee item | verdict | repair |
|---|---|---|
| A2 / README headline "proof of round 3's conjecture" | overclaim | **Withdrawn.** Reworded everywhere to "base-2 analogue for a designed reset family"; the B(3^k, 2) and C(3^k) conjecture is stated as OPEN (depth.md, correction after A2; README). |
| depth.md [A4] sentence "witnesses prove k\* independently of A1" | WRONG | **Withdrawn** in depth.md. A witness proves only the lower bound. Added [A5]: decide.py's generic depth computation gives the same k\* for m = 4..8, independent of A1. For m = 9, 10 the independent upper bound is REFEREE1 [R2]. |
| m = 10 λ = 0.99795 | typo | Corrected to 3^147/2^233 = 0.99274; [A3] now checks the λ column exactly. |
| A1, chain residue with t₀ = 0 | gap (trivial) | Case written out in depth.md. |
| A2 bound | weaker than proof | Stated and checked as k\* ≥ h + 1 + qL. |
| A3 Diophantine consequence | ε missing | O_ε(q_k^{μ−2+ε}), k\* = O_ε(Q^{μ+1+ε}); value of μ still not looked up. |
| A-rec comparison | cross-family | README now gives the like-for-like base-2 comparison (791 vs dch_S6_332 at modulus 64). |
| W1 leftover wording ("U ≥ 1") | wrong direction | Replaced by the upper bound U_left ≤ p^{(1−δ)(K−m+e_max)}. Also noted that the 3x+1 threshold uses an irrational δ, which the proof tolerates, and that W2 proves 3x+1's case directly. |
| W1′ presentation | substantive, but true | window.md now proves the bound for the non-accelerated map of dichotomy.md §7 (same R_N, CERT by the W1 argument with odd-step count), and `check_window.py` [W1′p] checks N = 4..10. |
| W4 sentence "by B1 ... cannot be replaced by a cylinder statement" | informal | Withdrawn; replaced by what B1 actually shows. |
| B1-inst "CERT only for j = 2" | wording | Now "exactly for j ≤ 2"; [C3] also checks j = 1. |
| README rows for B1 and W1 | hypotheses omitted | Hypotheses added. |

Re-runs after the repairs: `check_cutoff.py` and `check_window.py` exit 0 (ALL PASS), and
`referee1_check.py` still exits 0. `check_depth.py` was re-run, and every item through [A3]
m = 9 passed, including the strengthened A2 bound. The run was still in progress (the m = 10
formula, the λ-column check and the new [A5]) when this revision was handed off. *Update after
REFEREE2:* the second referee ran the complete revised `check_depth.py` ([A1]–[A5], including
the m = 10 formula, the λ-column check and [A5] at m = 8), and it exits 0 with ALL PASS. Separately, before the edit, decide.py's
generic k\* was run by hand for m = 6, 7, 8 and gave 791, 4335 and 41362, matching the
table.

## Revision after REFEREE2

REFEREE2 (`REFEREE2.md`) confirmed every claim and listed three text-only repairs, with no
change to any mathematics. All three are made:

1. **W1′ exponent (README row W1′ and window.md, Corollary W1′ display).** The numeric bounds
   2^{0.954N} (README) and 2^{0.9544N} (window.md) rounded the exponent H(5/8) = 0.954434… down,
   which makes the upper bound false for large N (from about N ≈ 15500 and N ≈ 2.7·10^5
   respectively). Both now read 2^{N·H(5/8)} with H(5/8) = 0.95443…, i.e. at most 2^{0.9545N}
   (rounded up). The conclusion (exponential decay of dist/2^N) is unchanged.
2. **cutoff.md instances table.** The row for the 3x+1 cut-off at j = 1, 2 said "cycle (1 2)"
   for both. For j = 1 the only cycle is the fixed point (1). The row now reads
   "j = 1: cycle (1); j = 2: cycle (1 2)".
3. **"Revision after REFEREE1" note on `check_depth.py`.** The statement that the complete
   revised run was "not yet confirmed" was out of date: REFEREE2 ran it in full, and it exits 0
   with ALL PASS. The note is updated.

REFEREE2's optional item (marking the general density remark in window.md as heuristic) is not
applied here.
