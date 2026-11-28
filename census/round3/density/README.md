# Round 3 — lens "density": exact almost-all theorems for Markov table maps

**What this folder does.** It turns the ad-hoc "how many starts never drop" arguments of round 2
(split5_3: `X^{0.585}`, split5_1: `X^{0.9383}`, split7_1: `X^{0.7549}`) into one method with a
general theorem, an exact optimality statement, and a tool that issues exact rational certificates for
any table map. It then applies the method to every open GLOBAL entry with a table rule, adds the
Korec-type and expanding-side theorems, and records precisely what the method cannot do.
**No open GLOBAL question is settled.** No new map is introduced; the "systems" are the
catalog entries, and what is settled for them is a precisely stated density question (below).

## Files

| file | content |
|---|---|
| `theory.md` | all general theorems with proofs (Lemmas 1–4, Theorems 1–6, Proposition 7) |
| `results.md` | per-system table: c_0 in closed form, certified exponents, early-drop densities |
| `density_lib.py` | state graph construction, exact drift, float search, exact certification, rigorous rational powers, slope walks, early-drop bounds |
| `systems.py` | the 38 maps as exact residue tables (ids, CLS numbers, step functions) |
| `make_certificates.py` | searches parameters and writes `certificates.json` (about 5 s) |
| `certificates.json` | every certificate (s, γ, rational weight vector w, θ, q bounds) |
| `check_density.py` | **exact** re-verification of all finite content; exit 0 iff all pass (about 3.5 minutes; `ONLY=id1,id2` restricts) |
| `check_hypH.py` | exact check of hypothesis (H) of Theorem 3 (seconds) |
| `evidence.py`, `evidence.out` | EVIDENCE only: convergence to θ*, split-order invariance, drop proportions, actual counts |

## General theorems (all PROVED unless noted; proofs in `theory.md`)

| # | statement | status |
|---|---|---|
| Lemma 1 | Every table map (u may contain primes of Q; mixed primes allowed) has an adaptive digit tree whose nodes' (state, slope factor, intercept) evolve on a finite graph G(T) when the construction terminates; checked to depth 8–12 against the real integer tree for all 38 maps | PROVED + checked |
| Thm 1 | If `N_{s,γ} w ≤ w` with `s > 0`, `0 ≤ γ ≤ 1`, then `#{n ≤ X : T^k(n) ≥ n ∀k≥1} ≤ 2^{k_0} + C_1 X^{1−γ}` with explicit `k_0`, `C_1`; the never-descending P-adic set has Haar measure 0 | PROVED |
| Thm 2 | `θ* = 1 − sup_{s>0} γ*(s)`; every `θ > θ*` is certifiable; `θ* < 1` iff the Lyapunov drift `Δ < 0` (Kingman convexity of the log spectral radius) | PROVED |
| Thm 3 | For single-prime maps under (H) (part 1 checked exactly for all contracting single-prime maps here; parts 2–3, C-dominance of ρ(P_s) and the minimiser, follow from irreducibility of G(T), which holds for all 17 maps), the number of classes mod `p^j` not certified by a slope crossing is `p^{jθ* + o(j)}`: θ* is the exact exponent of the method | PROVED (standard tilting + ergodic theorem); EVIDENCE for the rate |
| Thm 4 | Korec-type: for every `c > c_0 = 1 + Δ/Λ`, all but `O(X^{θ_c})`, `θ_c < 1`, of `n ≤ X` have an iterate `< n^c`. For 3x+1 this is Korec's `log_4 3` | PROVED |
| Prop 4.2 | `c_0` is sharp for the method: for `c < c_0`, almost every n has *all* tree values (to depth log n) `≥ n^c` | PROVED |
| Thm 5 | Expanding maps (`Δ > 0`): for every `c ∈ (1, c_0)`, all but `O(X^{θ_c})` of `n ≤ X` have an iterate `> n^c` (signed intercepts allowed: covers the 1932 permutation family) | PROVED |
| Thm 6 | Expanding single-prime maps with nonnegative intercepts: the set of n dropping below n within `log_p n` tree steps has natural density exactly `q`, computed with rigorous bounds; the full drop set has lower density `≥ q` | PROVED |
| Prop 7 | If GLOBAL holds with finitely many cycles then the drop set has density 1; so an upper-density bound `< 1` for 5x+1/7x+1 would prove a divergent orbit or infinitely many cycles | PROVED (elementary) |
| Remark | "almost all start drop" does not imply "almost all reach a known cycle"; iterating Thm 4 fails; Prop 4.2 shows depth-log n information cannot pass `n^{c_0}` | explanation + Prop 4.2 |
| E1–E4 | numerical convergence `O_j → θ*`; split-order invariance for div maps; full drop proportion ≈ q (conjecture: density(D) = q); true never-drop counts are tiny | EVIDENCE |

## Systems table (the precise questions settled)

Question settled for each contracting entry: "what power of X bounds the number of starts `n ≤ X`
that never drop below themselves, and below which power `n^c` does almost every orbit go?"; for each
expanding entry: "above which power does almost every orbit rise, and what is the density of early
drops?". GLOBAL stays OPEN for all of them.

| id | CLS | rule | question | answer | status | tier |
|---|---|---|---|---|---|---|
| div235_7n1 | 001/058 | 2∣n→n/2; else 3∣n→n/3; else 5∣n→n/5; else 7n+1 | never-drop count; Korec threshold | `O(X^{857/913}) = O(X^{0.93866})`; every `c > 0.71732` | PROVED | 2 |
| div23_5n1 | 002/059 | 2∣n→n/2; else 3∣n→n/3; else 5n+1 | same | `O(X^{0.85958})`; `c_0 = 7 ln5/(14 ln2+6 ln3) = 0.69135` | PROVED | 2 |
| div23_7n1 | 003/060 | 2∣n→n/2; else 3∣n→n/3; else 7n+1 | same | `O(X^{0.99900})`; `c_0 = 0.95133` | PROVED | 2 |
| m3_b | 004/061 | 3∣n→n/3; (4n∓1)/3 | same | `O(X^{521/540}) = O(X^{0.96481})`; `c_0 = (4/3)log_3 2` | PROVED | 2 |
| m3_d | 005/062 | 3∣n→n/3; 4n+2; 4n+1 | same | `O(X^{0.96481})`; `c_0 = 0.84124` | PROVED | 2 |
| m3_g | 008/063 | 3∣n→n/3; 5n+1; 5n+2 | same | `O(X^{1906/1907})`; `c_0 = (2/3)log_3 5 = 0.97665` | PROVED | 2 |
| par_3_1 | 013 | 3x+1 (sanity) | same | `θ* = H(log_3 2) = 0.94996` (Terras), `c_0 = log_4 3` (Korec): known values recovered | PROVED (known) | 2 |
| 3n+d, 6n+2 | 011,012,014–018,031 | | same | same exponents as 3x+1 | PROVED | 2 |
| split5_1 | 048/064 | even→n/2; 1(4)→5n+1; 3(4)→n+1 | same | `O(X^{994/1061}) = O(X^{0.93685})` (was 0.9383), method-optimal; `c_0 = (1/4)log_2 5` | PROVED | 2 |
| split5_3 | 049/065 | even→n/2; 1(4)→5n+3; 3(4)→n+3 | same | `O(X^{457/787}) = O(X^{0.58069})` (was 0.58496), method-optimal | PROVED | 2 |
| desc_m3_4n5 | 051 | 3∣n→n/3; 4n+5; 2n+2 | same | `O(X^{0.74870})`; `c_0 = log_3 2` | PROVED | 2 |
| desc_s32_plus9 | 052 | 3n+1 / n+1 by n mod 32 | same | `O(X^{0.56976})`; `c_0 = (22/67)log_2 3` | PROVED | 2 |
| desc_split7_1 | 053 | even→n/2; 1(4)→7n+1; 3(4)→n+1 | same | `O(X^{0.75348})` (was 0.75488), method-optimal; `c_0 = (1/6)log_2 7` | PROVED | 2 |
| par_5_d | 020–022,024,025,027,029,030 | 5n+d | rise threshold; early-drop density | every `c < log_4 5 = 1.16096`; `q ∈ [0.823782, 0.824073]` | PROVED | 2 |
| par_10_2 | 010 | 10n+2 | same | as 5n+1 | PROVED | 2 |
| par_7_1, par_7_7 | 032/034, 035 | 7n+1, 7n+7 | same | `c < log_4 7 = 1.40368`; `q = 0.699249…` | PROVED | 2 |
| par_9_1 | 037 | 9n+1 | same | `c < log_2 3`; `q = 0.613870…` | PROVED | 2 |
| m3_e | 006/007 | 3∣n→n/3; 7n+2; 7n+1 | same | `c < (2/3)log_3 7 = 1.18083`; `q ∈ [0.722567, 0.722571]` | PROVED | 2 |
| perm_1932, perm_swap, perm_b | 038/040, 047, 044 | 1932 family | rise threshold | every `c < (5/3)log_3 2 = 1.05155` | PROVED | 2 |
| perm_1932inv, perm_c | 042, 045 | | rise threshold | every `c < (2/3)log_2 3 = 1.05664` | PROVED | 2 |
| perm_d | 046 | | rise threshold | every `c < log_4 5` | PROVED | 2 |

Sample certified exponents θ_c for the Korec and expanding statements are in `results.md`.

## What stayed open, precisely

* Every GLOBAL question above (tier 5). The density method cannot reach them: Theorem 3 and
  Proposition 4.2 show that the depth-`log n` coefficient tree has exactly the exponents θ* and
  thresholds `c_0`, and no information beyond `log n` digits is uniformly distributed.
* "Almost every orbit reaches a known cycle" for any of these maps (would need a Tao-type argument;
  even 3x+1 has only the logarithmic-density `f(n)` result of Tao 2019).
* Expanding maps: whether the drop set `D` has density `q` (EVIDENCE says yes) — any upper bound
  `< 1` already implies a divergent orbit or infinitely many cycles (Prop. 7).
* Hypothesis (H) of Theorem 3 now includes C-dominance (`ρ(P_s)` attained on the closed class C near s*,
  e.g. G(T) irreducible). For the 17 maps Theorem 3 is applied to, the graphs are irreducible, and the
  minimiser part of (H) follows from (H) part 1 by convexity (`theory.md`), so it is no longer a
  numerical-only caveat for these maps. (H) is used only in the optimality Theorem 3, not in any upper bound.

## Novelty

Theorem 1/2/4 specialise to known results for 3x+1 (Terras 1976 exponent `H(log_3 2)` as recalled
from Lagarias's survey; Korec 1994 threshold `log_4 3`, as quoted in Tao, arXiv:1909.03562). Venturini
and Matthews–Watts proved "almost all n have finite stopping time" for broad generalized Collatz
families (recalled, not re-read). The *qualitative* part of Theorem 1 for general maps (density-1
finite stopping time when the Markov drift is negative) is very likely classical (Matthews–Watts 1984,
Venturini) and is not claimed as new. What is plausibly new: the explicit power-saving exponent for
each catalog map, the optimality statement (Thm 3, Prop 4.2), the general Korec-type and
expanding-side thresholds (Theorems 4 and 5), and the exact certificates; this was not
checked against the literature; **novelty otherwise not checked**.

## Reproduce

```
nice python3 make_certificates.py      # ~5 s, rewrites certificates.json
nice python3 check_density.py          # ~3.5 min, exact, exit 0  (last run: ALL CHECKS PASSED)
nice python3 check_hypH.py             # seconds, exit 0
nice python3 evidence.py               # ~35 s, EVIDENCE only
```

## Refereeing

Fixes applied after the referee report (`REFEREE.md`):
* `theory.md` Theorem 3: added to (H) the hypothesis that ρ(P_s) is attained on the closed class C near s* (e.g. G(T) irreducible), and made the lower-bound step explicit (`ρ_C` vs `ρ`).
* `theory.md` Theorem 3: replaced the numerically checked "unique interior minimiser" part of (H) by the referee's convexity argument (it follows from (H) part 1 for irreducible graphs); recorded that all 17 maps have irreducible graphs ([R7]).
* `theory.md` Theorem 6: inserted the partial-block argument (lifts of S_{j−L} plus the o(p^j) remainder), so natural density, not just density along block endpoints, is proved.
* `theory.md` Proposition 7: removed the stray editing remnant in the first sentence.
* `README.md`: Thm 3 row and "What stayed open" updated for the new (H); Novelty no longer suggests the qualitative part of Theorem 1 is new.
* `results.md`: clarified that for mixed-prime maps "θ* (float)" is the optimum over Theorem-1 certificates (Theorem 2a); Theorem 3 does not apply to them.
* `check_density.py`: docstring runtime corrected from "60–90 s" to about 3 minutes (no check changed).
