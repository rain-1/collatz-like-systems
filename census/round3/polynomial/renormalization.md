# Frobenius renormalization: lemmas behind every divergence proof in this folder

Status: **PROVED** (all lemmas are short and complete; the finite content of each application is
checked exactly by `check_divergence.py`).

## Setting

`p` is a prime, `g, h ∈ F_p[t]` with `g(0) ≠ 0`, `h(0) = 1`. The map is

    T(f) = f/t                         if f(0) = 0
    T(f) = (g f − g(0) f(0) h)/t       if f(0) ≠ 0.

Over `F_2` this is the familiar `f/t` or `(g f + h)/t`. Write `g0 = g(0)`. The division is exact,
so `T` maps `F_p[t]` into itself. The same formula defines `T̂ : F_p[[t]] → F_p[[t]]`, which
restricts to `T` on polynomials. The *branch* of `x` is its constant term `x(0) ∈ F_p`. A
polynomial orbit is eventually periodic iff its degrees are bounded, because there are only
finitely many polynomials of each degree. So an orbit **diverges** iff it contains
polynomials of unbounded degree.

## R1 (cylinder lemma)

For `c, z ∈ F_p[[t]]` and `n ≥ 0`:

    T̂^n(c + t^n z) = T̂^n(c) + g^{s_n(c)} z,   s_n(c) = #{0 ≤ i < n : T̂^i(c)(0) ≠ 0}.

*Proof.* Induction on `n`. For `n ≥ 1`, `c + t^n z` has the same branch `λ = c(0)` as `c`. If
`λ = 0`, `T̂(c + t^n z) = T̂(c) + t^{n−1} z`. If `λ ≠ 0`,
`T̂(c + t^n z) = (g c − g0 λ h)/t + g t^{n−1} z = T̂(c) + t^{n−1}(g z)`. Apply the induction
hypothesis to `T̂(c)`. ∎

**R1′ (periodic phase).** Let `c` be `T̂`-periodic with period `L`, and let `s` of the `L`
branches in one period be nonzero. Then `T̂^{jL}(c + t^{jL} z) = c + g^{sj} z` for all `j ≥ 0`
and all `z`.

## R2 (Frobenius)

For `G ∈ F_p[t]` and `N = p^n`, `G(t)^N = G(t^N)`. This holds because the coefficients lie in
`F_p` and `x ↦ x^p` is additive in characteristic `p`.

## R3 (twist transfer)

Let `k ∈ F_p[t]` with `k(0) = 1`. For every `u ∈ F_p[[t]]`,

    T̂_{g,kh}(k u) = k · T̂_{g,h}(u).

*Proof.* `(ku)(0) = u(0)`, so both sides take the same branch. In the nonzero branch,
`(g k u − g0 u(0) k h)/t = k (g u − g0 u(0) h)/t`. ∎

Consequences:

* **(a) Multiples.** If `T_{g,h}` has a divergent orbit `u`, then `k u` is a divergent orbit of
  `T_{g,kh}`. So "GLOBAL fails" passes from `h` to every multiple of `h`. In particular
  divergence for `h = 1` gives divergence for every twist `h`.
* **(b) Denominators.** Let `u = a/B` be a rational power series with `B(0) = 1`. Then every
  `T̂^n_{g,h}(u)` again has denominator dividing `B`: the numerator `g a − g0 λ h B` has zero
  constant term, so the step divides it by `t`. Hence `B·T̂^n_{g,h}(u) ∈ F_p[t]`, and by R3,
  `T^n_{g,Bh}(B u) = B·T̂^n_{g,h}(u)`. A rational power series with an unbounded `T̂_{g,h}`-orbit
  therefore yields a genuinely divergent **polynomial** orbit of the twisted map `T_{g,Bh}`.

## R4 (the constant-branch fixed points)

Let `ρ = g0 h/(g − t) ∈ F_p(t) ∩ F_p[[t]]`; note `(g − t)(0) = g0 ≠ 0`. Then `ρ(0) = 1` and
`g ρ − g0 h = t ρ`, so `T̂(ρ) = ρ`. Since `T̂(λx) = λT̂(x)` for `λ ∈ F_p^*`, each `λρ`
(`λ ∈ F_p`) is a fixed point whose branch is constantly `λ`. The point `0·ρ = 0` is the
all-`0` fixed point.

## R5 (line renormalization)

For `P ∈ F_p[X]` nonconstant, set `λ = P(0)` and `v = ord_X(P − λ)`, and define

    Φ(P) = λ + g(X)^{v·[λ≠0]} · (P − λ)/X^v.

**Claim.** For every `N = p^n`, `T̂^{vN}(ρ·P(t^N)) = ρ·Φ(P)(t^N)`.

*Proof.* Write `P = λ + X^v P′`. Then `ρP(t^N) = λρ + t^{vN}·ρP′(t^N)`. By R1′ with the fixed
point `λρ` (`L = 1`, `s = [λ≠0]`) and `j = vN`, this goes to `λρ + g^{vN[λ≠0]}·ρP′(t^N)`.
R2 gives `g^{vN} = g(t^N)^v`. ∎

**Corollary (line certificate).** Suppose `Φ^k(P) = P(X^{p^b})` for some `k, b ≥ 1`. Let the
phase valuations be `v_1, …, v_k` and put `τ = Σ v_i`. Then for every `N = p^n`,

    T̂^{τN}(ρ P(t^N)) = ρ P(t^{p^b N}).

Assume in addition that `f_N := ρP(t^N)` is a polynomial for `N = N_0`. Then the `T`-orbit of
`f_{N_0}` passes through every `f_{p^{bj} N_0}`. These are polynomials by R3/R4 (they are
`T`-images of a polynomial), and their degree tends to infinity. So **`T_{g,h}` has a divergent
orbit.**

*Polynomiality criterion.* Let `D` be the reduced denominator of `ρ`. If every irreducible
factor `π` of `D` divides `P(X)` in `F_p[X]`, then `D | P(t^N)` for all `N ≥ deg D`. Indeed,
`π(X) | P(X)` gives `π(t^N) | P(t^N)`, and `π(t^N) = π(t)^N` by R2. Two special cases:

* `ρ ∈ F_p[t]`, which happens exactly when `(g − t) | g0 h` (the "twisted" certificates);
* `h = 1`. Then `D = (g − t)/g0`, and the condition reads `rad(g − t)(X) | P(X)`.

## R6 (two-point renormalization, `p = 2`)

Let `c_1, c_2` be `T̂`-periodic with `(period, #odd) = (L_i, s_i)`, and put `d = c_1 + c_2`. A
state `(μ, Q)` with `Q ∈ F_2[X]`, `Q(0) = 0` stands for `u = c_μ + Q(t^N)d`. Let
`v = ord_X Q`. Assume:

1. `L_μ | vN`;
2. `E := s_μ v / L_μ` is an integer.

Condition 1 holds, for example, when the odd part of `L_μ` divides `v` and the 2-part of
`L_μ` divides `N`, but the proof uses only `L_μ | vN` (together with the integrality of `E`).
This matters at small `N`: in D0 the phase at the 2-cycle has `L = 2` and `v = 2`, so
`L_μ | vN` holds already at `N = 1`, although `N = 1` is not divisible by the 2-part of `L_μ`.
With the condition stated as `L_μ | vN`, the D0 chain is valid from `N_0 = 1`.

Then

    T̂^{vN}(c_μ + Q(t^N) d) = c_{μ'} + Ψ(Q)(t^N) d,   Ψ(Q) = g(X)^E Q/X^v + 1,   μ' = 3 − μ.

*Proof.* `vN` is a multiple of `L_μ` by condition 1, so R1′ with `j = vN/L_μ` gives multiplier
`g^{s_μ vN/L_μ} = g^{EN} = g(X)^E` (R2). The quotient `Q/X^v` has constant term 1, and
`c_μ + d = c_{μ'}`. ∎

If `Ψ^k(1, Q) = (1, Q(X^2))`, then as in R5, `T̂^{τN}(u_N) = u_{2N}` with `τ = Σ v`. Any
denominator is then removed by R3(b).

## N1 (negative lemma: why `h = 1` is hard)

Let `h = 1` and `d = deg g ≥ 1`. For every nonzero polynomial `f` in the nonzero branch,
`deg T(f) = deg f + d − 1`, since `g f − g0 f(0)` has degree `deg f + d`. In the zero branch
`deg T(f) = deg f − 1`. Summing over one period of a **polynomial** cycle (`L` steps, `s` of
them nonzero) gives `s(d − 1) − (L − s) = 0`, that is,

    s/L = 1/d   for every periodic point that is a polynomial.

**Consequence.** Feed R5 or R6 only polynomial periodic points (the points `λρ` with `ρ`
polynomial, or genuine cycles). Then `deg_X` is unchanged by every phase at a nonzero
polynomial periodic point: the degree change is `dE − v = d·(v/d) − v = 0`. The zero fixed
point (`λ = 0`) is also a polynomial periodic point, but N1 as stated above covers only
nonzero points, so phases at it must be allowed separately. A phase at the zero fixed point
has `s = 0`, so its multiplier is `g^0 = 1` and it only divides by `X^v`; it therefore
*lowers* `deg_X` by `v`. In every case `deg_X Φ ≤ deg_X P` (and likewise for `Ψ`). Such a renormalized orbit stays in a finite set and can never
certify divergence. Every certificate for `h = 1` must therefore use a non-polynomial periodic
point, whose denominator must be cancelled by `P` or `Q`. Over `F_2` with `g = 1+t+t^2`, the
only constant-branch point is `ρ = 1/(1+t)^2`. For that `g`, the search in `classification.md`
finds no admissible `P` of degree `≤ 12` and no admissible two-point pair with `Q` of degree
`≤ 12` and periods `≤ 6`. That is **EVIDENCE** only.

## Novelty

The cylinder lemma is the polynomial version of Terras' parity-vector correspondence (cf.
Nichols 2016, Lemma 2.3). The Frobenius-doubling mechanism is visibly what makes the
Matthews–Leigh example `m = 1 + t^2` work: OEIS A368120 records the closed form at times
`5(2^n − 1)`. To my knowledge the general line and two-point certificates, the twist
transfer R3(b) as a way to turn rational divergent points into polynomial ones, and N1 are not
stated in the cited literature. That is **novelty not fully checked**: a short web search found
nothing, and the Matthews–Leigh paper itself was not accessible.
