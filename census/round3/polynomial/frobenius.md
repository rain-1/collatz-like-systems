# Theorem C — Frobenius self-conjugacy of `m = M^2 + t` over `F_2` (and the square-renormalization proposition)

Maps over `F_2`: `T_{m,h}(f) = f/t` (f even), `(m f + h)/t` (f odd), with `m(0) = h(0) = 1`.

**Theorem C.** Let `M ∈ F_2[t]` with `M(0) = 1`, `m = M^2 + t`, `h = 1`, and
`φ(u) = (M u)^2 = M(t^2)·u(t^2)`. Then

    T^2(φ(u)) = φ(T(u))   for every u ∈ F_2[t].

Moreover, if `deg M ≥ 1` (that is, `deg m ≥ 2`), `T(φ(u))` is never in the image of `φ` unless `u = 0`. So if `u` is periodic with
period `L`, then `φ(u)` is periodic with period **exactly** `2L`. The same reasoning maps a
divergent orbit to a divergent orbit.

**Corollary C1 (`m = 1 + t + t^2`, `M = 1 + t`).** For every `k ≥ 0`, `(1+t)^{2^{k+1}−2}` lies
on a cycle of length exactly `2^{k+2}`. This is `φ^k(1)`; the cycle of `1` is
`1 → 1+t → t^2 → t → 1`. So `T_{1+t+t^2,1}` has infinitely many cycles, of unbounded length
and degree. This matches Nichols' observation (2016, §2.2.2) that the observed periods are
divisible by 4 and are "nearly all powers of 2".

**Proposition C′ (general square renormalization).** Write `m = m_e(t^2) + t·m_o(t^2)` and
`h = h_e(t^2) + t·h_o(t^2)`, and assume

* (i) `m_o(0) + h_o(0) = 1`, and
* (ii) `h_e·(1 + m_o) = m_e·h_o`.

Then for every polynomial `A`, `T_{m,h}^2(A(t^2)) = A′(t^2)` with `A′ = T_{m,h′}(A)` and
`h′ = t(1 + m_o)h_o + m_e h_e`. So `T_{m,h}^2` restricted to squares is conjugate to
`T_{m,h′}`.

Special case:

* `h = 1` forces `m_o = 1`, that is `m = M^2 + t`. Then `h′ = M` (here `m_e = M`), and
  `T_{m,M}` restricted to `M·F_2[t]` is `T_{m,1}` by the twist transfer R3. This gives Theorem C.

**Separate case: `m = M^2`, `h = H^2` (not a special case of C′).** This pair violates
hypothesis (i): here `m_o = h_o = 0`, so `m_o(0) + h_o(0) = 0`. Nevertheless the identity

    T_{M^2,H^2}^2(F^2) = (T_{M,H}F)^2

holds for every `F ∈ F_2[t]` (with `M(0) = H(0) = 1`), by a direct computation. If `F` is even,
then `F^2` is even and `F^2/t` has only odd powers, so it is again even; hence
`T^2(F^2) = F^2/t^2 = (F/t)^2 = (T_{M,H}F)^2`. If `F` is odd, then
`M^2F^2 + H^2 = (MF+H)^2` with `(MF+H)(0) = 0`, so the first step gives
`(MF+H)^2/t = t·((MF+H)/t)^2`, which is even. The second step therefore divides by `t` and gives
`((MF+H)/t)^2 = (T_{M,H}F)^2`. So any divergent orbit of `T_{M,H}` squares to one of
`T_{M^2,H^2}`.

Status: **PROVED**. `check_frobenius.py` checks:

* the identity of Theorem C for all `M` with `deg M ≤ 4` (320000 random `u`);
* Proposition C′ for all 64 pairs `(m, h)` with `deg ≤ 5` that satisfy (i) and (ii);
* the `M^2, H^2` case, on random inputs;
* C1 for `k ≤ 9`, by direct simulation of the exact period.

## Proof

Write `y = t^2`. For a polynomial `f = A(y) + t·B(y)` and the general `(m, h)`, the
odd-branch formula is

    m f + h = [m_e A + y m_o B + h_e] + t [m_o A + m_e B + h_o]      (all in y),

so `T(f) = (m_o A + m_e B + h_o) + t·(m_e A + y m_o B + h_e)/y`.

Start from `f = A(y)` (`B = 0`).

* **`A(0) = 0`.** `T(f) = t·(A/y)(y)` is even, so `T^2(f) = (A/y)(y) = (T_{m,h′}A)(y)`.
* **`A(0) = 1`.** `T(f) = A_1 + t·B_1` with `A_1 = m_o A + h_o` and `B_1 = (m_e A + h_e)/y`.
  Its parity is `m_o(0) + h_o(0) = 1` by (i), so the second step is odd. Its odd part is
  `(m_e A_1 + y m_o B_1 + h_e)/y`, whose numerator is
  `m_e m_o A + m_e h_o + m_o m_e A + m_o h_e + h_e = m_e h_o + h_e(1 + m_o)`. By (ii) this is
  `0`, so `T^2(f)` is again a square. Its even part is

      m_o A_1 + m_e B_1 + h_o = [ (y m_o^2 + m_e^2) A + y(1+m_o) h_o + m_e h_e ] / y.

  In characteristic 2, `m_e(y)^2 + y·m_o(y)^2 = m(y)`. So the even part is
  `(m(y)A + h′(y))/y = T_{m,h′}(A)(y)`.

For Theorem C: (i) and (ii) hold with `m_o = 1` and `h = 1`, and `h′ = m_e = M`. Then for any `u`,

    T^2(φ u) = T^2((Mu)(y)) = (T_{m,M}(Mu))(y) = (M·T_{m,1}(u))(y) = φ(T u),

where the third equality is R3 with `k = M`.

**Not in the image.** Let `V = φ(v)`, a nonzero square.

* If `V` is even, `T(V) = V/t` has only odd powers, so it is not a square.
* If `V` is odd, `T(V) = V + (M^2 V + 1)/t`. Since `M^2 V = (M^2 v)^2`, the quotient is
  `(M^2 V + 1)/t = t·((M^2 v + 1)/t)^2`. It has only odd powers, and it is nonzero because
  `deg M ≥ 1` gives `M^2 v ≠ 1`.
  Adding `V`, which has only even powers, gives a non-square.

So `T^j(φu) ∈ image(φ)` only for even `j`. Then `T^{2i}(φu) = φ(T^i u)`, and injectivity of `φ`
gives that the period of `φ(u)` is exactly twice the period of `u`. ∎

Novelty: the conjugacy `T^2∘φ = φ∘T` is, to my knowledge, not in Nichols (who only reports
the cycle-length data); novelty not fully checked.
