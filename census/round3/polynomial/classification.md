# Classification of GLOBAL for small multipliers over `F_2` and `F_3`

Map: `T(f) = f/t` if `f(0) = 0`, else `(g f − g(0) f(0) h)/t`. Over `F_2` this reads
`(g f + h)/t`. "GLOBAL" asks whether every orbit is eventually periodic, which happens iff
every orbit has bounded degree.

## General principles (all PROVED)

* **P1 (degree drift is exact).** In the nonzero branch,
  `deg T(f) = deg f + deg g − 1` as soon as `deg f + deg g > deg h`. In the zero branch the
  degree drops by 1. There are no carries, so the degree of `T^n f` is `deg f` plus an exact
  integer walk driven by the branch sequence. The branch sequence is the `t`-adic "parity
  vector"; Terras' bijection holds (Nichols 2016, Lemma 2.3).
* **P2 (bounded multipliers).** If `deg g ≤ 1`, then
  `deg T(f) ≤ max(deg f, deg h − 1)`. Every orbit is bounded, hence eventually periodic:
  **GLOBAL is true for every `(g, h)` with `deg g ≤ 1`, over every `F_q`.** The cycle
  structure is the real question. It is completely solved by Theorem A (`onept.md`) for
  `F_2`, `g = 1+t`, all `h`. Theorem B (`snapptracy.md`) solves it for every degree-1 `g` over
  every `F_q`, with `h = (g/g(0))^a`.
* **P3 (eventually periodic parity ⇔ eventually periodic orbit).** If the branch sequence of a
  polynomial `f` is eventually periodic, with period `L` and `s` nonzero branches, then R1′
  forces a tail iterate to equal the unique `T̂^L`-fixed point of its cylinder. That point is
  `x* = H/(t^L − g^s)`, a fixed rational point, so the orbit is eventually periodic. So a
  divergent orbit has an aperiodic branch sequence. No "eventually all-odd" argument can prove
  divergence; some self-similar structure is needed (`renormalization.md`).
* **P4 (twist transfer, R3).** Divergence for `(g, h)` implies divergence for `(g, kh)` for
  every `k` with `k(0) = 1`. The base case `h = 1` is therefore the hardest. The degenerate
  case `g(0) = 0` is treated in the lemma below.
* **P5 (Frobenius).** Renormalization certificates exist exactly when the orbit organizes
  itself along `N ↦ pN` scales. The negative lemma N1 explains why `h = 1` always needs
  non-polynomial periodic points.

**Degenerate lemma (`F_2`, `g(0) = 0`).** Admissibility then forces `h(0) = 0`. Write
`g = t g_1`, `h = t h_1`; an odd `f` maps to `g_1 f + h_1`, with no division. The cases with
`deg g ≤ 2` (so `deg g_1 ≤ 1`) are:

* `g_1(0) = 1`, `h_1(0) = 1`: the image is even and the next step divides. This is the standard
  map `T_{g_1,h_1}` with `deg g_1 ≤ 1`, so GLOBAL is true by P2.
* `g_1(0) = 1`, `h_1(0) = 0`: odd stays odd.
  * `g_1 = 1`: `f ↦ f + h_1 ↦ f`; GLOBAL true.
  * `g_1 = 1 + t`: the degree goes up by 1 at every step once `deg f ≥ deg h_1`; **GLOBAL
    false**, and every odd `f` with `deg f ≥ deg h_1` diverges.
* `g_1 = t`: `f ↦ t f + h_1`.
  * If `h_1(0) = 1`, odd stays odd and the degree grows; GLOBAL false.
  * If `h_1(0) = 0`, the next step is even and the two steps compose to `f ↦ f + h_1/t`. The
    degree is bounded, so GLOBAL is true.
* `g = 0` (`g_1 = 0`): `f ↦ h_1` on odd `f`; GLOBAL true.

These are one-line arguments, tier 0/1, and are recorded only for completeness.

## `F_2`, `deg g ≤ 2`, `g(0) = 1`, all admissible `h` (`h(0) = 1`)

| g | h | GLOBAL | status | where |
|---|---|---|---|---|
| `1` | all | true; all cycles in `deg < deg h` | PROVED (P2, tier 1) | P2 |
| `1+t` | all | true; cycles `{0}`, `{h}` and cycles inside `{deg < deg h, k ∤ f}`; basin of `h` is `hF_2[t]` if `(1+t) ∤ h`; only `{0}`, `{h}` iff `h = (1+t)^a` | PROVED | `onept.md` |
| `1+t^2` | all | **false** | PROVED; `h = 1` is Matthews–Leigh 1987, re-proved; all `h` by R3 | `divergence.md` D0 |
| `1+t+t^2` | `h ∈ (1+t)^2(1+t+t^3)·F_2[t]` | **false** | PROVED (new) | `divergence.md` D4 |
| `1+t+t^2` | every other `h`, in particular `h = 1` | **OPEN** | infinitely many cycles (Theorem C) | `frobenius.md` |

So the `F_2`, `deg ≤ 2` classification is complete except for the zero-drift multiplier
`1 + t + t^2` with a twist not divisible by `B = (1+t)^2(1+t+t^3)`.

## `F_2`, `deg g = 3, 4, 5`, `h = 1` (and hence all `h`)

| g | `h = 1` | twisted results | where |
|---|---|---|---|
| `1+t^3` | **false** (PROVED, new) | — | D1 |
| `(1+t)^3 = 1+t+t^2+t^3` | **false**; orbit of 1 diverges (PROVED; probably Matthews) | — | D2 |
| `1+t+t^3` | OPEN | false for `h ∈ (1+t+t^2)F_2[t]` (D3, `k = 1`) | D3 |
| `1+t^2+t^3` | OPEN | none found | — |
| `1+t^4 = (1+t)^4` | **false**, PROVED (D0 + squaring); all `h` by R3(a) | — | D0, `frobenius.md` (`M^2, H^2` case) |
| `(1+t+t^2)^2` | OPEN | false for `h ∈ (1+t+t^2+t^4)F_2[t]` | D6 |
| `1+t^3+t^4` | OPEN | false for `h ∈ (1+t+t^3+t^4)F_2[t]` | D6 |
| other degree 4 | OPEN | none found | — |
| `(1+t)^5` | **false**; orbit of 1 diverges (PROVED, new) | — | D2 (`k = 2`) |
| `1+t+t^5` | OPEN | false for `h ∈ C_2 F_2[t]` | D3 (`k = 2`) |
| `1+t^5`, `1+t^3+t^5` | OPEN | twisted line certificates found by the scan; not written up | scratch |
| infinite family `(1+t)^{2^k+1}` | **false** for all `k ≥ 1` (PROVED) | — | D2 |
| infinite family `1+t+t^{2^k+1}` | OPEN for `h = 1` | false for `h ∈ C_k F_2[t]`, all `k ≥ 1` (PROVED) | D3 |

**`1 + t^4` (PROVED, D0 + squaring).** Apply the `M^2, H^2` case of `frobenius.md` with
`M = 1+t^2` and `H = 1`: `T_{1+t^4,1}^2(F^2) = (T_{1+t^2,1}F)^2` for every `F`, and by
induction `T_{1+t^4,1}^{2n}(F^2) = (T_{1+t^2,1}^n F)^2`. By D0, `T_{1+t^2,1}^{5N}(u_N) = u_{2N}`
for every `N = 2^n`, where `u_N = (1 + t^{3N}(t+t^2))/(1+t+t^2)` is a polynomial. Hence

    T_{1+t^4,1}^{10N}(u_N^2) = u_{2N}^2,

so the orbit of the polynomial `u_1^2` passes through every `u_{2^n}^2`, whose degree is
unbounded. GLOBAL is therefore false for `g = 1+t^4`, `h = 1`, and by R3(a) for every `h`.
This is also the Matthews–Leigh construction for `t^n + 1` with even `n`, as reported by
Nichols.

## `F_3`, all `(g, h)` with `deg g ≤ 2`

* `deg g ≤ 1`: GLOBAL true for all `h` (P2). The complete cycle list is Theorem B for
  `h = (g/g0)^a`; other `h` were not classified.
* `deg g = 2`: 12 multipliers `g = g0 + g1 t + g2 t^2`. The degree drift is `+1/3` per step.

| g | `h = 1` | twisted | where |
|---|---|---|---|
| `2+t^2` | OPEN | **false** for `h ∈ (1+t+2t^2)F_3[t]` | D5 `p3_a` |
| `1+2t^2` | OPEN | **false** for `h ∈ (1+2t+2t^2)F_3[t]` | D5 `p3_c` |
| `1+t+t^2` | OPEN | **false** for `h ∈ (1+t^2)F_3[t]` | D5 `p3_b` |
| `2+t+2t^2` | OPEN | **false** for `h ∈ (1+t^2)F_3[t]` | D5 `p3_d` |
| other 8 | OPEN | no line certificate with `P` of degree `< 8` | `scratch/phi3b.py` |

## Searches behind the OPEN entries (EVIDENCE only)

* `g = 1+t+t^2` over `F_2`, `h = 1`:
  * line certificates: none with `deg P ≤ 12`;
  * two-point certificates: every pair of periodic points with periods `≤ 6` and every `Q`
    with `deg Q ≤ 12` gives 36 self-similar renormalized orbits, **none** with polynomial
    `f_N`. With periods `≤ 8` and `deg Q ≤ 10`, the least common denominator is always a
    multiple of `(1+t)^2(1+t+t^3)`;
  * the Matthews–Leigh-type pair (`r`, 4-cycle point) for `deg Q ≤ 18`: every renormalized
    orbit violates the integrality condition within 26 phases.

  Data-driven stretch analysis of orbits from seeds of degree `≤ 11` shows that at most 26%
  of the parity sequence lies in long periodic stretches, against 100% for the
  Matthews–Leigh map. Nichols' long orbit of `t^6+t^2+t+1` grows at about 0.2 degrees per
  step in my convention (degree 3980 after 20000 steps, odd fraction 0.599; Nichols reports
  slope 2/5, perhaps with a different step count). It shows no visible Frobenius
  self-similarity (EVIDENCE, `scratch/exp5.py`).
* `F_3`, `h = 1`: line certificates need `rad(g − t) | P`. None exists with `deg P < 8` for
  any of the 12 multipliers.
