# Round 3, lens `polynomial`: Collatz-type maps on `F_q[t]`

All maps here have the form

    T(f) = f/t                         if f(0) = 0
    T(f) = (g f − g(0) f(0) h)/t       if f(0) ≠ 0            (g(0) ≠ 0, h(0) = 1)

Over `F_2` the second line is the familiar `(g f + h)/t`. `g` is the *multiplier* and `h` the
*twist*. A polynomial orbit is eventually periodic iff its degree stays bounded. The new
systems are not in `census/systems.py`.

Run `python3 check.py`. It runs the five check scripts and takes about 40 s; each exits 0.
All arithmetic is exact (Python ints as `F_2` bit masks, tuples over `F_p`). No floating point
is used in any proof or check.

## Main results

| # | statement | status | proof / check |
|---|---|---|---|
| **A** | `F_2`, `g = 1+t`, **every** twist `h = (1+t)^a k`. GLOBAL is true. `k \| f ⇔ k \| T(f)`. A nonzero `f` reaches `{0, h}` iff `k \| f`. If `(1+t) ∤ h`, the basin of the fixed point `h` is exactly `h·F_2[t] \ {0}`. The only cycles are `{0}` and `{h}` iff `h = (1+t)^a` (generalizes HMYZ 2008). | PROVED | `onept.md`, `check_onept.py` |
| **B** | Every degree-1 multiplier `g = g0 + g1 t` over every `F_q`, twist `(g/g0)^a`. A nonzero `f` is periodic iff its Newton sequence `v_n = Σ C(n,i) g1^{n−i} g0^i a_i` never vanishes. Periodic points of degree `< p^e` correspond bijectively to nowhere-zero words of length `p^e`, `(q−1)^{p^e}` of them, with `T` acting as the shift. This completely classifies the cycles of the Snapp–Tracy maps (2008), which they only exhibited. | PROVED | `snapptracy.md`, `check_snapptracy.py` |
| **C** | Frobenius self-conjugacy. For `g = M^2 + t`, `h = 1`: `T^2∘φ = φ∘T` with `φ(u) = (Mu)^2`, and periods double exactly. Proposition C′ gives the general square-renormalization `(g, h) → (g, h′)`. For `g = 1+t+t^2`, `(1+t)^{2^{k+1}−2}` has period exactly `2^{k+2}`, so there are infinitely many cycles. This explains Nichols' "periods are powers of 2" data. | PROVED | `frobenius.md`, `check_frobenius.py` |
| **R** | Renormalization certificates (line R5, two-point R6) built from the cylinder lemma and Frobenius `G^{p^n} = G(t^{p^n})`. A finite exact identity `Φ^k(P) = P(X^{p^b})` proves a divergent orbit. Twist transfer R3 turns divergent *rational* points into divergent *polynomial* orbits of a twisted map. Negative lemma N1: for `h = 1` every polynomial periodic point has `s/L = 1/deg g`, so certificates must use non-polynomial periodic points. | PROVED | `renormalization.md` |
| **D** | Provably divergent orbits; table below. | PROVED | `divergence.md`, `certs.py`, `check_divergence.py` |
| **P** | Classification of GLOBAL for `F_2`, `deg g ≤ 2`, all `h`: complete except `g = 1+t+t^2` with `B ∤ h`, where `B = (1+t)^2(1+t+t^3)`. `F_2`, `deg g ≤ 5`, `h = 1`: partial table. `F_3`, `deg g ≤ 2`: `deg ≤ 1` true; `deg 2` false for four multipliers with twists. Degenerate `g(0) = 0` lemma. | PROVED where marked, EVIDENCE/OPEN otherwise | `classification.md`, `check_classification.py` |

## Systems settled (new ids; `systems.py` has a step function for each)

| id | field | rule (odd branch) | question | answer | status | tier |
|---|---|---|---|---|---|---|
| `p2_onept_h7` | F2 | `((1+t)f + 1+t+t^2)/t` | GLOBAL, cycles, basin | cycles `{0}`, `{h}`, `{1,t}`; basin of `h` = multiples of `1+t+t^2` | PROVED | 2 |
| `p2_onept_family` | F2 | `((1+t)f + h)/t`, all `h` | GLOBAL, cycles | Theorem A | PROVED | 2 |
| `p3_st`, `p4_st`, `pq_st_family` | F3, F4, Fq | `(g f − g0 f(0)(g/g0)^a)/t`, `deg g = 1` | GLOBAL, all cycles | Theorem B | PROVED | 2 |
| `p2_t3` | F2 | `((1+t^3)f + 1)/t` | GLOBAL | **false**; `T^{18N}(f_N) = f_{2N}`; seed `1+t+t^2+t^4+t^6` | PROVED (new) | 3 |
| `p2_cube_k` | F2 | `((1+t)^{2^k+1}f + 1)/t`, all `k ≥ 1` | fate of 1 | **diverges**: `T^{(4^k+2^k)N}(w^{N−1}) = w^{2^k N−1}`, `w = t + g` | PROVED (`k = 1` probably known, Matthews) | 3 |
| `p2_tri_k` | F2 | `((1+t+t^{2^k+1})f + h)/t`, `C_k \| h` | GLOBAL | **false**: `T^{2N}((1+t)^{N−1}) = (1+t)^{2^k N−1}` for `h = C_k` | PROVED (new) | 1–2 (two-phase, one-line certificate; the twist makes `ρ` polynomial) |
| `p2_crit` | F2 | `((1+t+t^2)f + 1+t+t^2+t^5)/t` | GLOBAL (zero drift) | **false**: `T^{4N}(f_N) = f_{2N}`, `f_N = (1+t+t^3)(1+X+X^2) + (1+t)^2(X+X^2)` | PROVED (new) | 3 |
| `p2_ML` | F2 | `((1+t^2)f + h)/t`, all `h` | GLOBAL | **false** for every `h` | PROVED (`h = 1` is Matthews–Leigh 1987) | 3 |
| `p3_a`, `p3_b`, `p3_c`, `p3_d` | F3 | `g` ∈ {`2+t^2`, `1+t+t^2`, `1+2t^2`, `2+t+2t^2`}, `h = (g−t)/g0` | GLOBAL | **false**, e.g. `T^{8N}(1+t^{2N}) = 1+t^{6N}` | PROVED (new) | 3 |
| `p2_sq111`, `p2_1034` | F2 | `g = (1+t+t^2)^2` resp. `1+t^3+t^4`, `h = t+g` | GLOBAL | **false** | PROVED | 3 |

Each divergence result also holds for every twist `k·h` with `k(0) = 1` (R3).

## Open, with what was proved and tried

* **`p2_nichols`: `g = 1+t+t^2`, `h = 1` over `F_2`.** This is Nichols' central question:
  is there a divergent orbit? It stays **OPEN**. Proved here:
  * infinitely many cycles (Theorem C);
  * divergence for the twist `h = (1+t)^2(1+t+t^3)` and all its multiples (D4);
  * Lemma N1, which shows that any certificate must cancel the denominator `(1+t)^2` of the
    all-odd point.

  Searches (EVIDENCE): no line certificate with `deg P ≤ 12`; 36 self-similar two-point
  families with periods `≤ 6` and `deg Q ≤ 12`, none polynomial; every two-point family with
  periods `≤ 8` needs a twist divisible by `(1+t)^2(1+t+t^3)`. See `classification.md`.
* `F_2`, `h = 1`: `1+t+t^3`, `1+t^2+t^3`, most degree 4–5 multipliers. Also every `F_3`
  degree-2 multiplier with `h = 1` (no line certificate with `deg P < 8`). OPEN.
* Theorem A leaves the split between `0` and `h` inside `k·F_2[t]` (case `a ≥ 1`) as a finite
  computation, and gives no stopping-time bound for general `h`.

## Task (3): transfer to integer systems

No new statement about an integer census system was obtained. The precise reason: every
divergence proof here uses `G(t)^{p^n} = G(t^{p^n})`, which makes the multiplier over `N`
steps a *sparse* polynomial in `X = t^N`. The integer analogues of R1 (Terras' 2-adic
cylinder lemma) and R3 hold. R3 is the integer fact that `3x+k` cycles are rational `3x+1`
cycles with denominator `k`. But `3^N` has no
sparse expression in `2^N`, so the closure step `Φ^k(P) = P(X^{p^b})` has no integer
counterpart. The carry-free model is exactly what makes these systems solvable. I record this
as a remark, not a theorem.

## Literature and novelty

Checked by short web searches:

* Hicks, Mullen, Yucas, Zavislak, *A polynomial analogue of the 3n+1 problem*, Amer. Math.
  Monthly 115 (2008) 615–622: `g = 1+t`, `h = 1`, all orbits reach 1. Theorem A
  generalizes this.
* Snapp, Tracy, *The Collatz problem and analogues*, J. Integer Seq. 11 (2008) 08.4.4:
  `((x+1)f − f(0))/x` has cycles over `Z_n[x]`, `n > 2`. Theorem B classifies them.
* Matthews, Leigh, J. Number Theory 25 (1987) 274–278, as described by Nichols and by OEIS
  A368120: a divergent trajectory for `m = t^2+1`, "easily extended to `t^n+1`, `n` even".
* D. Nichols, *Analogues of the 3x+1 problem in polynomial rings of characteristic 2*, Exp.
  Math. (2016), arXiv:1610.02545. It proves `P(σ=∞) > 0` for `deg m ≥ 3`, says genuine
  divergence is open for most `m`, and gives the `t^2+t+1` data.
* Gallardo, Rahavandrainy, arXiv:2510.07530 (2025): cites a Matthews example with multiplier
  `(x+1)^3` and divergent trajectories. So `p2_cube` with `k = 1` is probably not new.

Everything else (A for general `h`; B's classification; C; R5/R6/R3(b)/N1; D1, D2 for `k ≥ 2`,
D3, D4, D5, D6) was not found in these sources. **Novelty is not fully checked:** the
Matthews–Leigh paper and Matthews' later surveys were not accessible.

## Files

* Proofs: `onept.md`, `snapptracy.md`, `frobenius.md`, `renormalization.md`,
  `divergence.md`, `classification.md`.
* Code: `polylib.py` (exact arithmetic, certificate verifiers), `certs.py` (certificate data),
  `systems.py` (ids, step functions).
* Checks: `check_*.py`, and the runner `check.py`.
* `scratch/`: exploration scripts (searches, scans, outputs). These are EVIDENCE only and are
  not needed by the checks.

## Refereeing

Fixes applied from `REFEREE.md` (both passes):

* `renormalization.md` R6: conditions 1 and 3 replaced by the condition the proof uses, `L_μ | vN` (with `E` integral); noted that D0's chain is valid from `N = 1`.
* `renormalization.md` N1 consequence: phases at the zero fixed point (`λ = 0`, `s = 0`) are allowed; they lower `deg_X`, so `deg_X Φ ≤ deg_X P` still holds.
* `frobenius.md` Prop. C′: the `m = M^2, h = H^2` case moved out of the special cases (it violates (i)) and given its own line with the direct two-step computation.
* `classification.md` row `1+t^4`: labelled "false, PROVED (D0 + squaring)", with the argument `T_{1+t^4,1}^{10N}(u_N^2) = u_{2N}^2` written out.
* `README.md` integer-transfer remark: dropped the Lagarias 1990 citation quoted from memory.
* `README.md` `p2_tri_k`: tier lowered from 3 to 1–2 (two-phase, one-line certificate).
