# Theorem A — `F_2`, multiplier `1 + t`, arbitrary twist `h`

System family `p2_onept[h]`:

    T(f) = f/t                if f(0) = 0
    T(f) = ((1+t) f + h)/t    if f(0) = 1,      h ∈ F_2[t], h(0) = 1.

`h = 1` is the map of Hicks–Mullen–Yucas–Zavislak (HMYZ 2008), and independently of
Snapp–Tracy (2008). They proved that every nonzero orbit reaches 1.

Questions: **GLOBAL** (with the complete cycle list) and **BASIN** (the exact basin of the fixed
point `h`).

Write `h = (1+t)^a k` with `(1+t) ∤ k`, so `k(0) = 1` and `k(1) = 1`.

**Theorem A.**

1. `deg T(f) ≤ max(deg f, deg h − 1)`, so every orbit is eventually periodic. The fixed points
   include `0` and `h`.
2. `k | f ⇔ k | T(f)`.
3. If `f ≠ 0` and `k ∤ f`, the orbit of `f` never meets `{0, h}`.
4. If `k | f`, the orbit of `f` reaches `0` or `h`.
5. Every cycle other than `{0}` and `{h}` lies in `{f : deg f < deg h, k ∤ f}`. In particular
   the cycle list is `{0}`, `{h}`, plus a finite exhaustive search in degree `< deg h`.
6. **Every nonzero orbit ends in `{0, h}` ⇔ `h` is a power of `1 + t`.**
7. **Exact basin when `(1+t) ∤ h`** (that is, `a = 0`): a nonzero `f` reaches `h` iff `h | f`, and
   no nonzero `f` reaches `0`. The basin of the fixed point `h` is `h·F_2[t] \ {0}`.

Status: **PROVED**. `check_onept.py` checks exactly: (1)–(2) on 20000 random pairs with
`deg f ≤ 200`; (3)–(7) exhaustively for all odd `h` with `deg h ≤ 9` and all `f` with
`deg f < 12`; (6) for `h = (1+t)^a`, `a ≤ 6`, and all `f` with `deg f ≤ 14`.

## Proof

**(1)** `deg((1+t) f + h) ≤ max(deg f + 1, deg h)`, and dividing by `t` gives the bound. The set
`{deg ≤ max(deg f, deg h − 1)}` is finite and invariant, so every orbit is eventually periodic.
`T(0) = 0`, and `T(h) = ((1+t)h + h)/t = h`.

**(2)** `k | h`, so `t·T(f) ≡ (1+t)^ε f (mod k)` with `ε ∈ {0, 1}`. Both `t` and `1+t` are units
mod `k`, because `k(0) = k(1) = 1`.

**(3)** By (2) the residue `f mod k` stays nonzero, while `0 ≡ h ≡ 0 (mod k)`. If `k = 1` the
statement is empty.

**(4)** Put `f = k u`. By the twist transfer (`renormalization.md`, R3) with `k(0) = 1`,
`T_{1+t,h}(k u) = k·T_{1+t,(1+t)^a}(u)`. So it suffices to treat `h = (1+t)^a` and `u ≠ 0`. Let
`e = ord_{1+t}(u)`. An even step keeps `e`, since `t` is a unit at `1+t`. An odd step gives
`t·T(u) = (1+t)u + (1+t)^a`. This has order `e + 1` if `e + 1 < a`, and order `≥ a` (possibly
`T(u) = 0`) if `e + 1 ≥ a`. A nonzero orbit has infinitely many odd steps, because
`u ↦ u/t` cannot be applied forever to a nonzero polynomial. So either the orbit hits `0`, or
from some time on `u = (1+t)^a v` with `v ≠ 0`. From then on
`T((1+t)^a v) = (1+t)^a·T_HMYZ(v)` (R3 again, with `k = (1+t)^a`), where
`T_HMYZ(v) = v/t` or `((1+t)v + 1)/t`.

*HMYZ in three lines.* Under `T_HMYZ` the degree never increases. An even step lowers the degree
of a nonzero `v`. `T_HMYZ(v) ≠ 0` for `v ≠ 0`. So a cycle has constant degree and consists of
odd steps only. For an all-odd cycle of length `L`,

    v = ((1+t)^L v + Σ_{i<L} (1+t)^i t^{L−1−i}) / t^L,

that is, `v·(t^L + (1+t)^L) = (1+t)^L + t^L`, which forces `v = 1`. So every nonzero orbit
reaches 1, hence `u` reaches `(1+t)^a = h`.

**(5)** Suppose a cycle has maximal degree `D ≥ deg h`. By (1), after a step from degree `D` to
degree `< D` the orbit never returns to degree `D`. So all of its elements have degree `D`, and
every step is odd. For an all-odd cycle,
`f·(t^L + (1+t)^L) = h·(t^L + (1+t)^L)/(t + (1+t)) = h·(t^L + (1+t)^L)`, so `f = h`. Cycles
other than `{0}` and `{h}` therefore lie in degree `< deg h`. By (4) they also avoid multiples
of `k` other than `0` and `h`.

**(6)** If `h = (1+t)^a`, then `k = 1` and (4) applies to every `f`. If `k ≠ 1`, then `f = 1`
satisfies `k ∤ 1`, and by (3) its orbit ends in a cycle other than `{0}` and `{h}`.

**(7)** If `a = 0`, then `T(f) = 0` forces `(1+t) f = h`, which is impossible. So no nonzero
orbit reaches `0`. By (3) and (4), `f ≠ 0` reaches `h` iff `k = h` divides `f`. ∎

Remarks.

* The exhaustive check found the `h` (with `deg h ≤ 9`) for which `{0}`, `{h}` are the only
  cycles to be exactly `1, (1+t), (1+t)^2, …, (1+t)^9`.
* For `a ≥ 1` the basin of `0` is not a clean set: for `a = 2`, 55 of the polynomials of degree
  `< 10` reach `0`. I did not describe it. The split between `0` and `h` inside `k·F_2[t]` is
  therefore left as a finite computation.
* Worked instance `p2_onept_h7`: `h = 1 + t + t^2` (`a = 0`). The cycles are `{0}`, `{h}` and
  `{1, t}`. The basin of `h` is exactly the nonzero multiples of `1+t+t^2`. All other nonzero
  `f` end in `{1, t}`.
* Stopping times: for `h = 1` a quadratic bound in `deg f` is attributed to HMYZ, and an
  `O(d^{1.5})` improvement to arXiv:2401.03210. Both are taken from search snippets and were not
  re-checked. No bound is claimed here for general `h`.

Novelty: items (2)–(7) for general `h` generalize HMYZ. I did not find them in HMYZ, Snapp–Tracy,
or Nichols; novelty not fully checked.
