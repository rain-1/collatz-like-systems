# Referee report: round 3, lens `polynomial`

Referee: independent adversarial verification. The prover's files were not modified. The
referee wrote two files here: `referee_check.py` and this report.

## What was done

1. I re-derived every proof line by line: `onept.md`, `snapptracy.md`, `frobenius.md`,
   `renormalization.md`, `divergence.md` and `classification.md`.
2. I ran `python3 check.py`. All five scripts exit 0, in about 46 s total. I read each script and
   confirmed that it tests the finite content the proofs need. The two-point check verifies the
   periodic words, the R6 integrality, polynomiality for all `N = 2^n` through the residue cycle
   of `t^(2^n) mod D`, and direct simulation. The line check verifies `Φ^k(P) = P(X^{p^b})`, the
   radical criterion, and direct simulation.
3. I wrote `referee_check.py` from scratch. It has its own `F_2`/`F_p`/`F_4` arithmetic and its
   own renormalization map, and it does not import `polylib`, `certs` or the prover's checks. It
   imports `systems.py` only to test it against the written rules. It exits 0 in about 40 s.
   - **S.** Every `systems.py` step function agrees with the rule written in the `.md` files, on
     random inputs of degree up to 300.
   - **A.** Theorem A was checked exhaustively for all `h` with `deg h ≤ 8` and all `f` with
     `deg f < 11`. This covers (3)–(7), the extra cycles lying in degree `< deg h` and avoiding
     multiples of `k`, and "no extra cycle ⇔ `k = 1`". Items (1) and (2) were checked on 30000
     random `(f, h)` with `deg f ≤ 400`. Items (3), (4) and (7) were also checked on random large
     multiples `k·u` (deg ≤ 130) and on non-multiples.
   - **B.** I counted the periodic points by brute force for `F_3` (deg < 9), `F_4` (deg < 4),
     `F_5` (deg < 5) and `F_2` (deg < 16), with several `g`. The Newton criterion matched, the
     count matched `(q−1)^{p^e}`, and the periods matched the least period of the γ-extended
     Newton sequence. On large inputs I took random nowhere-zero words of length 27, 81, 25, 125,
     16, 64 and 128 and inverted the triangular map. I then checked directly that every one of
     the `p^e` steps takes the nonzero branch and that `S^{p^e} f = γ f`. Setting one letter to
     zero gives a non-periodic point, as predicted. Item (4) was checked exhaustively for six
     twisted cases (a = 1, 2, 3), and the twisted orbits are bounded.
   - **C.** The identity `T²φ = φT` and the non-square property of `T(φu)` were checked for 300
     random `M` with `deg M ≤ 10` and `deg u ≤ 500`. Exact period doubling was checked on actual
     cycles for four `M`. C1 was checked for `k ≤ 11`. For Prop. C′ I tested 400 random `(m, h)`
     of degree up to about 17, built to satisfy (ii), on random `A` with `deg A ≤ 200`.
   - **D.** Every line certificate was re-derived with my own `Φ`, checking `b` and `τ` against
     the text, polynomiality for all `N = p^n` (residue cycle), direct simulation and increasing
     degrees. This also covers `p2_cube_k` for `k = 1..4` (τ = 6, 20, 72, 272) and `p2_tri_k`
     for `k = 1..5`. I checked `D0` and `D4` by hand and by simulation, together with the
     residues, the periodic words and the formula `B·u_N`. The closed forms
     `T^{6(2^n−1)}(1) = (1+t²+t³)^{2^n−1}` (n ≤ 7), `deg f_{2^n} = 9·2^n − 3` (p2_t3),
     `deg f_N = 2N+3` (p2_crit) and the all-ones orbit of `p2_tri_k` were confirmed.
   - **R3** was checked on random large `k, u` over `F_2`, `F_3` and `F_5`. **N1** was checked on
     every cycle reached from small seeds, for eight multipliers. **P2** was checked on random
     inputs over `F_2`, `F_3`, `F_5` and `F_7`.
   - **Mutation test.** I mutated the twist of p2_crit, the τ of p2_t3 and the cycle criterion of
     Theorem A. The check reported 21 failures, so it can fail.
4. Hand verification. I recomputed by hand the general-`k` algebra of D2 (the four phases, the
   identity `(1+Z)^{K+1} = (1+Z)(1+Z^K)`, and `τ = K² + K`) and D3. I also recomputed the
   even/odd decomposition in Prop. C′, the non-image argument of Theorem C, and the HMYZ
   all-odd-cycle computation inside Theorem A.

## Verdicts

| claim | verdict | notes |
|---|---|---|
| Theorem A (`F_2`, g = 1+t, all h), incl. `p2_onept_h7`, `p2_onept_family` | CONFIRMED | Every step is checked. (5) uses the fact that degree `< D` is invariant once `D ≥ deg h`. (6) uses `f = 1` with `k ≠ 1`. The remark's "55 polynomials reach 0 for a = 2" was re-counted: 55. |
| Theorem B (deg-1 g over `F_q`, twists `(g/g0)^a`), incl. `p3_st`, `p4_st`, `pq_st_family` | CONFIRMED | `A^{p^e} = g1^{p^e} I + g0^{p^e} Δ^{p^e}` is valid because the operators commute. In (4), order `≥ a` is absorbing, so a cycle cannot contain a point of order `< a`. GLOBAL for `a ≥ 1` follows by the same argument plus R3, and the prover states it via P2. |
| Theorem C, Prop. C′, Cor. C1 | CONFIRMED | Prop. C′ implicitly needs `m(0) = h(0) = 1`. This is stated in the file header and used in the step `(m_e A + h_e)(0) = 0`. |
| Renormalization R1–R6, R3, N1 | CONFIRMED_WITH_FIX | Two wording fixes, neither of which affects any result. **(a)** R6 lists conditions 1 and 3, but the proof only uses `L_μ \| vN` (together with E integral). As written, condition 3 excludes `N = 1` in D0's phase at the 2-cycle (`L = 2`, `v = 2`), yet D0 starts at `N0 = 1`. With the condition stated as `L_μ \| vN` the D0 chain is valid from `N = 1`, and the direct simulation confirms it. **(b)** N1 is stated for nonzero polynomial points. The "consequence" also has to allow phases at the zero fixed point (λ = 0). Those phases have `s = 0` and *lower* `deg_X`, so the conclusion `deg_X Φ ≤ deg_X P`, and hence no certificate, still holds. |
| Divergence family `(1+t)^{2^k+1}`, h = 1 (`p2_cube_k`) | CONFIRMED | The general-`k` symbolic proof is correct (re-derived by hand) and machine-checked for k ≤ 4. The novelty caveat for k = 1 (Matthews) is honest. |
| Divergence family `1+t+t^{2^k+1}` with `C_k \| h` (`p2_tri_k`) | CONFIRMED | Correct, but it is a **two-phase, one-line certificate**: the twist was chosen to make `ρ` polynomial. It is easier than "tier 3" suggests; I would call it tier 1–2. |
| `p2_t3` (g = 1+t³, h = 1) | CONFIRMED | This is the strongest new `h = 1` result: a genuine untwisted map with a non-polynomial `ρ`, whose denominator is cancelled by `P`. |
| `p2_crit` (g = 1+t+t², h = 1+t+t²+t⁵) | CONFIRMED | Confirmed in two-point form and by direct simulation. "And all multiples k·h, k(0)=1" follows from R3(a). |
| `p2_ML` (g = 1+t², all h) | CONFIRMED | The h = 1 case is known (Matthews–Leigh 1987). The re-proof and the extension to all `h` via R3(a) are correct. |
| `p3_a`–`p3_d` | CONFIRMED | All are twisted with `h = (g−t)/g0`, so `ρ = 1` and the certificates are short. The answer and the twisted status are honestly labeled. |
| `p2_sq111`, `p2_1034` | CONFIRMED | They have the same "ρ = 1" twist and are easy (one-line certificates). |
| Classification P1–P5 and the degenerate lemma | CONFIRMED_WITH_FIX | All the proved statements hold. **Fix:** in `classification.md`, the row `1+t⁴ … false` carries no status and has no proof in the folder. It should read "false (literature: Matthews–Leigh's `t^n+1`, n even, as reported by Nichols 2016; not re-proved here)". |
| `p2_nichols` and the other OPEN entries | consistent | They are correctly labeled OPEN, and the search results are labeled EVIDENCE. |

## Remarks on honesty and overclaiming

- **Newness.** No polynomial-ring systems appear in `census/systems.py` or in any round-2
  folder (grep), so all the ids are new to the catalog. The domain is `F_q[t]`, not positive
  integers, and the README states openly that there is no integer transfer.
- **Easy instances.** Several "settled" systems are easy once the twist is chosen to make `ρ` a
  polynomial: `p2_tri_k`, `p2_sq111`, `p2_1034` and `p3_a`–`p3_d`. The substantive results are
  Theorems A, B and C, the general-`k` family D2, `p2_t3` (h = 1, untwisted) and `p2_crit` (the
  zero-drift multiplier). The README does flag the twisted nature of the easy ones.
- **Literature from memory.** The README's integer-transfer remark cites Lagarias (Acta Arith.
  1990) "from memory, not re-checked". The round's standards forbid quoting from memory. This
  is only a remark, not a theorem, and it is flagged. Still, the remark should drop the
  citation or verify it.
- **Stopping-time references.** In `onept.md`, the HMYZ quadratic bound and the arXiv:2401.03210
  references are flagged as taken from search snippets and are not used in any proof.
  Acceptable.

## Conclusion

No GAP or WRONG verdicts. Every PROVED claim is correct, and its finite content is verified
exactly, both by the prover's checks and independently. Two small wording fixes are listed
above: R6's divisibility condition and the status label of the `1+t⁴` row. Neither changes any
result.

---

# Second referee pass (independent re-verification)

A second, independent pass was made over the same prover files, which are unchanged. It added
`referee_check2.py`, written from scratch. Like the first check, it imports only `systems.py`,
and only to test it against the written rules. It runs in about 30 s and exits 0. A mutation test
(a wrong τ for `p2_t3`, a wrong twist for `p2_crit`, a wrong period in C1) produced 24 failures,
so the check can fail. `python3 check.py` (34 s) and the first `referee_check.py` (40 s) were
re-run, and both exit 0.

## What was re-derived by hand in this pass

* **Theorem A, all of (1)–(7).** The two units in (2) are `t` (since `k(0)=1`) and `1+t` (since `k(1)=1`). The
  `(1+t)`-order ratchet in (4) is absorbing once the order is `≥ a`. The HMYZ all-odd cycle
  forces `v = 1`, using `Σ(1+t)^i t^{L-1-i} = (1+t)^L + t^L`. In (5), once the orbit drops below
  degree `D ≥ deg h` it stays below. In (7), `(1+t)f = h` is impossible when `a = 0`.
* **Theorem B.** Three facts carry the proof: `A^{p^e} = g1^{p^e} I + g0^{p^e} Δ^{p^e}`, the
  Newton sequence is triangular, and `S(λx) = λS(x)`. In (4), the order at `π = g/g0` is
  non-decreasing and strictly increases on nonzero branches while it is `< a`.
* **Theorem C and Prop. C′.** I recomputed the even/odd split and checked
  `m(y) = m_e(y)^2 + y m_o(y)^2`. The non-square argument for `T(φu)` holds. C1 is
  `φ^k(1) = (1+t)^{2^{k+1}-2}`, which lies on the 4-cycle `1 → 1+t → t^2 → t` scaled by
  doubling, so it has period `2^{k+2}`.
* **D0–D6.** I redid all of these: D2 for general `K = 2^k` (all four phases, `τ = K²+K`,
  `Φ^4(P) = w(X^K)`), D3, D4, and D0 (both phases), as well as the factorization in D1,
  `1+X^6+X^9 = (1+X+X^3)(1+X+X^2+X^4+X^6)`, and the seeds `f_1`.

## New observations in this pass

1. **Prop. C′, "special case" `m = M², h = H²` (CONFIRMED_WITH_FIX).** This pair violates
   hypothesis (i): `m_o = h_o = 0`, so `m_o(0) + h_o(0) = 0`. It is therefore *not* a special
   case of C′ as stated. The identity `T_{M²,H²}^2(F²) = (T_{M,H}F)²` is still true, by a
   two-line computation. For odd `F`, `M²F² + H² = (MF+H)²` with `(MF+H)(0) = 0`, so the first
   step gives `t·((MF+H)/t)²`, which is even, and the second step gives `((MF+H)/t)²`. The even
   case is immediate. `referee_check2.py` (tag `Csq`) verifies it on random inputs. **Fix:** move this case
   out of C′'s "special cases" and give it its own line, with the computation above.
2. **Row `1+t^4` in `classification.md`.** The first pass asked for a literature label. In fact
   the claim follows *inside this folder*. Combine item 1 (with `M = 1+t²`, `H = 1`) with D0:
   `T_{1+t^4,1}^{10N}(u_N²) = u_{2N}²`, where `u_N = (1 + t^{3N}(t+t²))/(1+t+t²)`. So GLOBAL is
   false for `g = 1+t^4`, `h = 1`, and by R3(a) for every `h`. `referee_check2.py` (tag `D_t4`)
   checks this by direct simulation for `N = 1..32`. **Fix:** label the row "false, PROVED (D0 +
   squaring)".
3. **Theorem B over `F_4` with `g1 ∉ F_2`.** This pass checked it exhaustively for `g = 1+ωt`
   and `g = ω²+t` with `deg f < 4`: 81 periodic points, as predicted.
4. **Theorem B, `F_7`.** Random nowhere-zero Newton words of length 7 were inverted to
   polynomials. All of them are periodic under `S^{42}`, while words with a zero entry are not.
5. **Theorem A**, exhaustively for all 128 odd `h` with `deg h ≤ 7` and all `f` with
   `deg f ≤ 10`: items (2), (3)/(4), (5) (cycle degree and avoidance of `k`), (6) and (7) hold
   with no exception. The cycle list of `p2_onept_h7` is exactly `{0, 1, t, 1+t+t²}`.
6. **Certificates.** A fresh `Φ` re-derived every line certificate with the stated `(b, τ)`.
   This covers `p2_cube_k` for `k ≤ 5` (τ = 6, 20, 72, 272, 1056) and `p2_tri_k` for `k ≤ 6`.
   D0 and D4 were re-verified as identities of exact rational power series (`T̂^{τN}u_N =
   u_{2N}` for `N ≤ 64`) and as polynomial orbits of `T_{g,B}`. The formula for `f_N` in D4,
   `deg f_N = 2N+3`, and the seed `1+t+t²+t³+t⁵` were also confirmed.
7. **N1.** It was checked on every polynomial cycle reached from all seeds of degree `< 10` for
   seven multipliers of degree 2–4 (`h = 1`), with no exception.

## Verdicts (second pass, agreeing with the first)

| claim | verdict |
|---|---|
| Theorem A and systems `p2_onept_h7`, `p2_onept_family` | CONFIRMED |
| Theorem B and systems `p3_st`, `p4_st`, `pq_st_family` | CONFIRMED |
| Theorem C, Cor. C1 | CONFIRMED |
| Prop. C′ | CONFIRMED_WITH_FIX (item 1: the `M²,H²` case is not covered by (i) but holds by direct computation) |
| R1–R6, R3, N1 | CONFIRMED_WITH_FIX (first pass: R6 condition 3 should be `L_μ \| vN`; N1 must also allow λ = 0 phases) |
| D2 `p2_cube_k` | CONFIRMED (k = 1 probably known: Matthews) |
| D3 `p2_tri_k` | CONFIRMED (easy, two-phase; "tier 3" overstated) |
| D1 `p2_t3`, D4 `p2_crit`, D0 `p2_ML`, D5 `p3_a..d`, D6 `p2_sq111`, `p2_1034` | CONFIRMED |
| Classification P1–P5, degenerate lemma | CONFIRMED_WITH_FIX (the `1+t^4` row can be marked PROVED, item 2) |
| README integer-transfer remark | It quotes Lagarias 1990 from memory, which the round's standards forbid. Drop the citation or verify it. It is a remark, not a claim. |

No GAP or WRONG. needs_repair = false. The fixes are wording and labelling changes only.
