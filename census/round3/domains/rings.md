# Collatz-type maps on Z[ω], Z[√−2], Z[√2]

Check: `check_rings.py` (under 1 s). Arithmetic: `rings.py`. All four quadratic orders
used here (with Z[i], see gaussian.md) have a prime π of small norm:

| order | π | N(π) | O/π | units of absolute value 1 in every embedding |
|---|---|---|---|---|
| Z[i] | 1+i | 2 | F_2 | ±1, ±i |
| Z[ω] (Eisenstein) | 1−ω | 3 | F_3 | ±1, ±ω, ±ω² |
| Z[√−2] | √−2 | 2 | F_2 | ±1 |
| Z[√2] (real) | √2 | −2 | F_2 | ±1 (in both real embeddings) |

The generic map is T(z) = z/π if π | z, else u_r z + c_r on the residue class r ≠ 0
mod π, with π | u_r r + c_r.

## Theorem R (GLOBAL for unit multipliers, PROVED)

*If every u_r has absolute value 1 in every archimedean embedding, then every orbit in O
is eventually periodic, and the cycles are {0} plus the cycles through odd points z
with |σz| ≤ C/(|σπ| − 1) for every embedding σ, where C = max_r |σc_r|.*

*Proof.* Theorem N (theorem_N.md), parts 1–4. The blocks (u z + c)/π^k satisfy
|σ(u/π^k)| ≤ |σπ|^{-1} < 1 in every embedding. For Z[√2] the two real embeddings both
have |σ√2| = √2. The bound on cycle points comes from the maximum argument:
M ≤ (M + C)/|σπ|. ∎

`rings.window` enumerates a superset of that region using exact integer tests:
N(z) ≤ 6·max N(c) for |π|² = 2 and ≤ 2·max N(c) for |π|² = 3; for Z[√2],
|a| + |b|√2 ≤ 3·max(|c_0| + 2|c_1|), tested as 2b² ≤ (A − |a|)². Then `all_cycles`
follows every point of it. Hence each list below is **complete** (check R2):

| id | map | all cycles |
|---|---|---|
| E_f | Z[ω]: z/(1−ω); z+2 if z ≡ 1; z+1 if z ≡ 2 (mod 1−ω) | {0}, {1+ω, 2+ω}, {2+2ω, 4+2ω} |
| E_w | Z[ω]: z/(1−ω); ωz − 1 if z ≡ 1; ωz + 1 if z ≡ 2 | {0}, {−1, 1−ω, 1, −1+ω} |
| ZM2_1 | Z[√−2]: z/√−2 if divisible, else z+1 | **{0} only**: every element of Z[√−2] reaches 0 |
| ZP2_1 | Z[√2]: z/√2 if divisible, else z+1 | {0}, {1+√2, 2+√2}, {1, 2, √2} (as 1 → 2 → √2 → 1) |

The E_f rule is the Eisenstein analogue of catalog m3_f (n ≡ 1 ↦ n+2, n ≡ 2 ↦ n+1,
3 | n ↦ n/3), read in Z[ω] with 3 replaced by its prime factor 1−ω. On Z,
m3_f has the cycles {0}, {1, 3} (theorem_Z.md). In Z[ω] the rational cycle is lost,
because 3 = −ω²(1−ω)² now takes two divisions, and two new cycles appear.

"ZM2_1 has only the cycle {0}" says that every element of Z[√−2] has a terminating
expansion −z = Σ d_j (√−2)^j with digits d_j ∈ {0, 1}: base √−2 with digits {0, 1} is
a complete number system on Z[√−2]. Statements of this kind are classical in the theory
of canonical number systems (radix representations in quadratic orders), so this is
probably known. Novelty not checked. The contrast is with Z[i] and base 1+i, where the
cycle {−i, 1−i} survives (gaussian.md), and with Z and base 2, where the negative
integers reach 0 and the positive ones the cycle (1 2).

## Residue orbits (data; partial theory)

For u = 1 every one of these maps folds to V(z) = (z + c e(z))/π ≡ π^{-1}z (mod c), so
the orbit of z mod c under ×π is invariant and every orbit carries at least one cycle.
How many it carries (check R3; rows are c, N(c), number of cycles, number of ×π-orbits
on O/(c), and the histogram of cycles per orbit):

* **Z[i]:** 1 or 2 per nonzero orbit, 2 on the zero orbit. **PROVED** (Theorem G,
  gaussian.md).
* **Z[√−2]: at most 2 per orbit and exactly 1 on the zero orbit, PROVED.** The
  Theorem G argument (gaussian.md) carries over verbatim. Here |π| = √2, so the
  differences again have N(q) ≤ 5. The closed-walk part of the triple product graph is
  24 states with unique transitions, forming 6 cycles, and along each the three parity
  words are rotations of one another (check R4). The zero orbit is c·(the c = 1 map),
  whose only cycle is {0} (R2). Two cycles in one orbit do occur, but rarely: in a
  scan of 192 values of c (scratch/zm2.py, |a| ≤ 15, 0 ≤ b ≤ 11) only
  c = ±15, ±5+5√−2, ±5+10√−2, ±7+7√−2 have one. In check R3 every orbit carries
  exactly one cycle. So for most c the basin of the Z[√−2] map z/√−2, z + c is exactly
  the ×√−2-orbit of z mod c, a pure congruence rule with no sign condition, unlike
  1x+d on Z.
* **Z[ω]:** the zero orbit carries 3 cycles (c·{0} and two more), and nonzero orbits
  carry 1, 2 or 3 in the data. EVIDENCE.
* **Z[√2]:** 1, 2 or 3 per orbit in the data. EVIDENCE.

**Open (sharp).** Is the number of cycles per ×π-orbit bounded by 3 in Z[ω] and
Z[√2]? For Z[i] and Z[√−2] the bound 2 is proved by a finite product-graph
computation. For Z[ω] (digits e ∈ {0, ±1}, differences up to N(q) ≤ 7) and Z[√2]
(differences bounded in two real embeddings), the same method needs a quadruple-product
graph whose closed walks force all parity words to be rotations of each other. That
computation was not done.
