# Theorem B — complete cycle classification for every degree-1 multiplier over every `F_q` (Snapp–Tracy maps)

System family `pq_st[q, g, a]`, with `q = p^r` (checked for `q = 2, 3, 4, 5`),
`g = g0 + g1 t` (`g0, g1 ≠ 0`) and `a ≥ 0`:

    S(f) = f/t                                 if f(0) = 0
    S(f) = (g f − g0 f(0)·(g/g0)^a)/t          if f(0) ≠ 0.

`g = 1 + t`, `a = 0` is the map of Snapp and Tracy (J. Integer Seq. 11 (2008), Art. 08.4.4,
§2.2: `T_P(f) = ((x+1)f − f(0))/x`). They showed that for `p` odd, `x^{p−1} + 1` is periodic,
so the HMYZ conclusion fails over `F_p`, `p > 2`. Their paper exhibits single cycles and does
not classify them.

Question: **GLOBAL with the complete cycle list.**

For `f = Σ a_i t^i`, define its *Newton sequence*

    v_n(f) = Σ_i C(n,i)·g1^{n−i}·g0^i·a_i ∈ F_q   (n ≥ 0).

This is the constant term of `(g1 I + g0 Δ)^n f`, where `Δ(f) = (f − f(0))/t`.

**Theorem B.** Let `a = 0`.

1. `deg S(f) ≤ deg f`, with equality in the nonzero branch. Every orbit is eventually periodic.
2. A nonzero `f` is periodic **iff** `v_n(f) ≠ 0` for every `n ≥ 0`. It suffices to check
   `0 ≤ n < p^e`, for any `e` with `p^e > deg f`.
3. Fix `e`. The map `f ↦ (v_0, …, v_{p^e−1})` is a bijection from `{deg f < p^e}` onto
   `F_q^{p^e}`. The periodic points of degree `< p^e` correspond exactly to the
   nowhere-vanishing words; there are `(q−1)^{p^e}` of them. Moreover
   `v_{n+p^e} = γ·v_n` with `γ = g1^{p^e}`, and the period of `f` is the least period of
   `n ↦ v_n`, which divides `p^e·ord(γ)`.
4. For `a ≥ 1`, the nonzero periodic points are exactly `(g/g0)^a·u` with `u` periodic for the
   `a = 0` map.

Status: **PROVED**. `check_snapptracy.py` checks (2)–(4) exhaustively:

* (2) and (3) for `F_2` with `g = 1+t`; `F_3` with all four `g`; `F_4` with three `g`; `F_5`
  with three `g`. This is every `f` of degree `< p^e` for `p^e = 16, 9, 3, 4, 5, 8`, and
  includes the converse direction and the count `(q−1)^{p^e}`.
* (4) in seven `(q, g, a)` cases.

`F_4` is implemented as `F_2[w]/(w^2+w+1)`.

Corollaries:

* `q = 2`: the only nowhere-zero word is `1…1`, so the only periodic points are `0` and `1`.
  This is HMYZ again.
* `q ≥ 3`: there are cycles of every length `p^j`, and of unbounded degree. There are
  `(q−1)^{p^e}` periodic points of degree `< p^e`; over `F_3`, 512 of degree `< 9`.
* Over `F_4` with `g = 1 + t`, `1 + ωt` is periodic with period 2:
  `v = (1, 1+ω) = (1, ω^2)`.
* A constant multiplier `g = g0` (`g1 = 0`) is degenerate: the nonzero branch is `g0 Δ`, which
  lowers the degree, so every orbit reaches `0`.

## Proof

Let `Δ(f) = (f − f(0))/t` be the shift, and put `A = g1 I + g0 Δ`. In the nonzero branch
`S(f) = (g0 f + g1 t f − g0 f(0))/t = A f` (for `a = 0`). In the zero branch `S(f) = Δ(f)`.

**(1)** In the nonzero branch, `deg(g f − g0 f(0)) = deg f + 1`, because `g1 ≠ 0`. For a
constant `f = c` it is `g1 c t`. So the degree is preserved. In the zero branch it drops by 1.
The finite sets `{deg ≤ D}` are invariant.

**(2)** The degree never increases and the zero branch lowers it, so a periodic `f ≠ 0` never
takes the zero branch. Along an all-nonzero stretch `S^n f = A^n f`, and `g1 I` commutes with
`Δ`. So `A^n = Σ_i C(n,i) g1^{n−i} g0^i Δ^i`, and the constant term of `A^n f` is `v_n(f)`
because `(Δ^i f)(0) = a_i`. Hence "periodic ⇒ `v_n ≠ 0` for all `n`".

Conversely, suppose `v_n ≠ 0` for `n < p^e`. Then the first `p^e` steps all take nonzero
branches, and `S^{p^e} f = A^{p^e} f = g1^{p^e} f + g0^{p^e} Δ^{p^e} f = γ f`. This uses
`C(p^e, i) ≡ 0 (mod p)` for `0 < i < p^e`, and that `Δ^{p^e}` kills polynomials of degree
`< p^e`. Since `γ ∈ F_q^*` and `S(λx) = λS(x)` for scalars `λ` (the branch of `λx` is `λ` times the
branch of `x`), the orbit of `γ f` is `γ` times the orbit of `f`. So all branches stay nonzero,
and `S^{p^e·ord(γ)} f = f`. So `f` is periodic, and `v_{n+p^e} = γ v_n` never vanishes.

**(3)** The coefficient of `a_n` in `v_n` is `g0^n ≠ 0`, and `v_n` involves only `a_i` with
`i ≤ n`. So `(a_0..a_{p^e−1}) ↦ (v_0..v_{p^e−1})` is triangular with invertible diagonal, hence
bijective. The Newton sequence of `S^j f` is `n ↦ v_{n+j}`, and `f` is determined by
`v|[0, p^e)`. So `S^j f = f` iff `v_{n+j} = v_n` for all `n`.

**(4)** Let `π = g/g0 = 1 + (g1/g0)t`, an irreducible of degree 1 with `π(0) = 1`; `t` is a
unit at `π`. If `ord_π f < a` and `f` takes a nonzero branch, then
`t·S(f) = g f − g0 f(0) π^a` has `π`-order `ord_π f + 1` when `ord_π f + 1 < a`, and order
`≥ a` when `ord_π f + 1 = a`. Either way the order strictly increases while it is below `a`.
In the zero branch the order is unchanged. On a cycle the order is constant and some branch is nonzero, so the order is
`≥ a`, and `f = π^a u`. By the twist transfer R3 (`k = π^a`, `k(0) = 1`),
`S_a(π^a u) = π^a S_0(u)`. Hence `f` is `S_a`-periodic iff `u` is `S_0`-periodic. ∎

Novelty: (2) and (3) give the complete classification. Snapp–Tracy only exhibit cycles. I did
not find this classification in HMYZ, Snapp–Tracy, Nichols, or Gallardo–Rahavandrainy; novelty
not fully checked.
