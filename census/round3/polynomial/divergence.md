# Provably divergent orbits

All maps have the form `T(f) = f/t` if `f(0) = 0`, and `(g f − g(0) f(0) h)/t` otherwise; over
`F_2` the second branch is `(g f + h)/t`. The lemmas R1–R6 are in `renormalization.md`.
`check_divergence.py` re-verifies every identity below exactly. It also checks
`T^{τN}(f_N) = f_{p^b N}` independently by direct simulation for every `N = p^n` with
`deg f_{p^b N} ≤ 4000`. Throughout, `X = t^N` and `N` is a power of `p`.

For each system the question is **GLOBAL**: is every orbit eventually periodic? The answer
below is always **no**, with an explicit divergent orbit. By R3(a) the answer is also no for
every twist `k·h` with `k(0) = 1`.

---

## D1. `p2_t3`: `F_2`, `g = 1 + t^3`, `h = 1` — PROVED (GLOBAL false)

Put `ρ = 1/(1 + t + t^3)` (R4) and `P(X) = 1 + X^6 + X^9`. In `F_2[X]`,
`P = (1 + X + X^3)(1 + X + X^2 + X^4 + X^6)`. Every irreducible factor of the denominator of
`ρ` therefore divides `P`, and so

    f_N := ρ P(t^N) = (1 + t + t^3)^{N−1} (1 + X + X^2 + X^4 + X^6)

is a polynomial for every `N`. For example, `f_1 = 1 + t + t^2 + t^4 + t^6`.

Let `Y = X^3`, so that `g(X) = 1 + Y`. The four phases of `Φ` (R5) are:

| state P | λ | v | Φ(P) |
|---|---|---|---|
| `1 + Y^2 + Y^3` | 1 | 6 | `1 + (1+Y)^6(1+Y) = Y + Y^2 + … + Y^7` |
| `Y + … + Y^7` | 0 | 3 | `1 + Y + … + Y^6` |
| `1 + Y + … + Y^6` | 1 | 3 | `Y^2 + Y^6 + Y^8` (see below) |
| `Y^2 + Y^6 + Y^8` | 0 | 6 | `1 + Y^4 + Y^6 = P(X^2)` |

The third row computes `(P−1)/X^3 = 1 + Y + … + Y^5 = (1+Y^6)/(1+Y)`. Multiplying by
`g(X)^3 = (1+Y)^3` gives `(1+Y)^2(1+Y^6) = 1 + Y^2 + Y^6 + Y^8`, and adding 1 gives
`Y^2 + Y^6 + Y^8`.

So `τ = 6 + 3 + 3 + 6 = 18` and **`T^{18N}(f_N) = f_{2N}`** for all `N = 2^n`. The orbit of
`f_1 = 1 + t + t^2 + t^4 + t^6` visits `f_{2^n}`, whose degree is `9·2^n − 3`. ∎

Novelty: Matthews–Leigh treat `t^n + 1` only for even `n` (as reported by Nichols 2016, §2).
Nichols states that for most `m` of degree `≥ 3` the existence of a genuinely divergent
trajectory is open. I did not find this case in the literature; novelty not fully checked.

## D2. Family `p2_cube_k`: `F_2`, `g = (1+t)^{K+1}` with `K = 2^k`, `k ≥ 1`, `h = 1` — PROVED; the orbit of 1 diverges

Let `w = t + g`, `ρ = 1/w` (R4), and `P = w(X)`. Then `f_N = ρ w(t^N) = w^{N−1}` (R2), so
`f_1 = 1`. Write `u = 1 + X`, so that `g(X) = u^{K+1}` and `w(X) = 1 + u + u^{K+1}`. Since
`u^K = 1 + X^K`, put `Z = X^K`.

1. `λ = 1`. `P − 1 = u(1 + u^K) = u·X^K`, so `v = K`. Then
   `Φ = 1 + g(X)^K u = 1 + u^n` with `n = K^2 + K + 1` (odd).
2. `λ = 0`. `1 + u^n = X·(1 + u + … + u^{n−1})`, because `u − 1 = X`. So `v = 1` and
   `Φ = Σ_{i<n} u^i`.
3. `λ = n mod 2 = 1`. Here `Φ − 1 = u(1 + u^{K^2+K})/X`, and
   `1 + u^{K(K+1)} = 1 + (1+Z)^{K+1} = 1 + (1+Z)(1+Z^K) = Z + Z^K + Z^{K+1}`. So
   `Φ − 1 = u·X^{K−1}(1 + Z^{K−1} + Z^K)`, with `v = K − 1`. Then, using `u^{K^2} = 1 + Z^K`,

       Φ = 1 + u^{(K+1)(K−1)}·u·(1 + Z^{K−1} + Z^K)
         = 1 + (1 + Z^K)(1 + Z^{K−1} + Z^K)
         = Z^{K−1} + Z^{2K−1} + Z^{2K}.

4. `λ = 0`, `v = K(K−1)`. Then `Φ = 1 + Z^K + Z^{K+1} = 1 + X^{K^2} + X^{K^2+K}`. This equals
   `w(X^K) = X^K + (1 + X^K)^{K+1}`, since `(1+X^K)^{K+1} = (1+X^K)(1+X^{K^2})`.

So `Φ^4(P) = P(X^K)` with `τ = K + 1 + (K−1) + K(K−1) = K^2 + K`. Hence

    T^{(4^k + 2^k)N}(w^{N−1}) = w^{2^k N − 1}   for every N = 2^n,

and from `N = 1` **the trajectory of 1 is divergent** for every `g = (1+t)^{2^k+1}`. ∎ For
`k = 1, 2, 3` (`g = (1+t)^3, (1+t)^5, (1+t)^9`) this is also re-verified exactly in
`check_divergence.py` (`p2_cube`, `p2_cube5`, `p2_cube9`), including direct simulation.

A search over `g = (1+t)^j`, `2 ≤ j ≤ 19`, with `P = w(X)` finds self-similarity exactly for
`j ∈ {3, 5, 9, 17}`.

Novelty: Gallardo–Rahavandrainy (arXiv:2510.07530, introduction) cite the map
`A ↦ A/x`, `((x+1)^3 A + 1)/x` as an example of Matthews with divergent trajectories. **The
case `k = 1` is therefore probably known.** I could not check the original statement or proof.
The general family `k ≥ 2` and the closed form `T^{6(2^n−1)}(1) = (1+t^2+t^3)^{2^n−1}` are not
in the sources I saw.

## D0. `p2_ML`: `F_2`, `g = 1 + t^2`, `h = 1` (Matthews–Leigh 1987) — known; re-proved by R6

Here `r = 1/(1+t+t^2)` is the all-odd fixed point. The second point `1` has word `10`
(`1 → t → 1`). Take `Q = X^3`, so `u_N = r + X^3(1 + r)`.

* Phase at `r` (`3N` steps): the state becomes `r + (1+X^2)^3 (1+r)`, which equals
  `1 + (X^2 + X^4 + X^6)(1+r)`.
* Phase at `1` (`2N` steps = `N` periods, multiplier `g^N = g(X)`): the state becomes
  `1 + (1+X^2)(1+X^2+X^4)(1+r) = 1 + (1+X^6)(1+r) = r + X^6(1+r) = u_{2N}`.

Polynomiality holds for every `N = 2^n`, since `t^{3N} ≡ 1 mod (1+t+t^2)`. So
`T^{5N}(u_N) = u_{2N}`, in agreement with the closed form `a(5(2^n−1))` of OEIS A368120.
`check_divergence.py` (`p2_ML`) verifies this. Combined with R3(a): **for `g = 1 + t^2`, GLOBAL
fails for every twist `h`.**

## D3. Family `p2_tri_k`: `F_2`, `g = 1 + t + t^{2^k+1}` (k ≥ 1), every `h` divisible by `C_k = 1 + t + … + t^{2^k}` — PROVED

Here `t + g = 1 + t^{2^k+1} = (1+t)C_k`, and `C_k(1) = 1` (an odd number of terms), so the two
factors are coprime. With `h = C_k h'`, R4 gives `ρ = h'/(1+t)`. Take `P = 1 + X`. Then

    f_N = ρ (1 + t^N) = h' (1+t)^{N−1},

which is a polynomial. The phases are:

* `λ = 1`, `v = 1`, giving `Φ(P) = 1 + g(X)(1) = X + X^{2^k+1}`;
* `λ = 0`, `v = 1`, giving `1 + X^{2^k} = P(X^{2^k})`.

So **`T^{2N}(f_N) = f_{2^k N}`**. For `h = C_k` the divergent orbit is the all-ones polynomials:
`T^{2N}(1 + t + … + t^{N−1}) = 1 + t + … + t^{2^k N − 1}` (`N = 2^n`). ∎

Remark: `k = 0` gives `g = 1+t+t^2`, `C_0 = 1`, and `Φ(1+X) = X + X^2 ↦ 1 + X`. That is a
*cycle* of the renormalized map, not a self-similarity. It yields the cycles through
`(1+t)^{N−2}` (see `frobenius.md`), not divergence.

## D4. `p2_crit`: `F_2`, `g = 1 + t + t^2` (the zero-drift case), `h = (1+t)^2(1+t+t^3) = 1+t+t^2+t^5` — PROVED

This is the multiplier whose `h = 1` case is the main open problem of Nichols (2016). The
twisted system is settled here by a two-point renormalization (R6). For `g` and `h = 1` it uses
two `T̂`-periodic points:

* `r = 1/(1+t)^2`, the all-odd fixed point (`L = 1`, `s = 1`);
* `c = 1/(1+t+t^3)`, periodic with word `101` (`L = 3`, `s = 2`). Indeed
  `c ↦ (t+t^2)/(1+t+t^3) ↦ (1+t)/(1+t+t^3) ↦ c`.

Put `d = r + c` and `u_N = r + (X + X^2) d`.

* Phase 1 at `r` (`v = 1`, `N` steps): `r + g(X)(1+X) d = r + (1+X^3) d = c + X^3 d`.
* Phase 2 at `c` (`v = 3`, `3N` steps, which is `N` full periods): the multiplier is
  `g^{2N} = g(X)^2 = 1 + X^2 + X^4`, giving `c + (1+X^2+X^4) d = r + (X^2 + X^4) d = u_{2N}`.

So `T̂^{4N}_{g,1}(u_N) = u_{2N}`. Multiply by `B = (1+t)^2(1+t+t^3)`, the common denominator, and
apply R3(b):

    f_N := B u_N = (1+t+t^3)(1 + X + X^2) + (1+t)^2 (X + X^2) ∈ F_2[t]   for every N,

and **`T_{g,B}^{4N}(f_N) = f_{2N}`**, with `deg f_N = 2N + 3`. The orbit of
`f_1 = (1+t+t^3)(1+t+t^2) + (1+t)^2(t+t^2) = 1 + t + t^2 + t^3 + t^5` diverges, and so does
`T_{g,kB}` for every `k` with `k(0) = 1` (R3(a)). ∎

This answers Nichols' question for these twists: in the drift-zero class, orbits provably
diverge although the averaged degree drift is 0. Each phase is monotone in degree but the
orbit is not: inside phase 2 the degree goes down on even steps.

## D5. `F_3` systems (twisted) — PROVED

Here `ρ = g0 h/(g − t) = 1`, so `f_N = P(t^N)` with `N = 3^n`.

* **`p3_a`**: `g = 2 + t^2`, `h = 1 + t + 2t^2`, `P = 1 + X^2`. In `F_3[X]`, with
  `g(X) = X^2 + 2`:
  * `λ=1, v=2`: `1 + g^2 = X^4 + X^2 + 2`;
  * `λ=2, v=2`: `2 + g^2(X^2+1) = X^6 + 2X^4 + 2X^2`;
  * `λ=0, v=2`: `X^4 + 2X^2 + 2`;
  * `λ=2, v=2`: `2 + g^2·g = 2 + (X^2+2)^3 = X^6 + 1 = P(X^3)`.

  So **`T^{8N}(1 + t^{2N}) = 1 + t^{6N}`**, and the orbit of `1 + t^2` diverges.
* **`p3_c`**: `g = 1 + 2t^2`, `h = 1 + 2t + 2t^2`, `P = 1 + X^2`; `τ = 8`, `N ↦ 3N`.
* **`p3_b`**: `g = 1 + t + t^2`, `h = 1 + t^2`, `P = X + X^2 + 2X^3`. The phases have `v`
  equal to 1, 1, 3, 3; `τ = 8`, `N ↦ 3N`.
* **`p3_d`**: `g = 2 + t + 2t^2`, `h = 1 + t^2`, `P = X + 2X^2 + 2X^3`. There are eight phases
  with `τ = 32` and `N ↦ 9N`.

In each case `F_3` has positive degree drift (`2/3·(+1) + 1/3·(−1) = +1/3` per step), so
divergence is the expected behaviour. The point is that it is now proved for these specific
systems. Novelty: I know of no divergence proof for `F_3[t]` analogues; novelty not checked.

## D6. Other twisted `F_2` certificates (degree 4) — PROVED

* `p2_sq111`: `g = (1+t+t^2)^2 = 1+t^2+t^4`, `h = t + g`, `P = 1 + X`, `τ = 3`.
* `p2_1034`: `g = 1+t^3+t^4`, `h = t + g`, `P = 1+X+X^2`, `τ = 2`.

`check_divergence.py` covers all of these (D1–D6, with `p2_tri_k` for `k = 1, 2, 3`).
