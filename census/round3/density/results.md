# Per-system results (round 3, lens "density")

All numbers below are exact rational certificates from `certificates.json`, re-verified by
`check_density.py` (exit 0). The theorems they instantiate are in `theory.md`. **Nothing here settles
an open GLOBAL question**: these are density statements about open systems.

Columns:
* `c_0 = 1 + Δ/Λ`, exact closed form (the Lyapunov drift per unit of log-modulus, Theorem 2(b)).
* **θ (never drop)**: certified rational with `H(X) ≤ 2^{k_0} + C_1 X^θ` (Theorem 1). `θ*` = optimum of
  the method (Theorem 3: exact exponent of the uncertified set, single-prime maps). For the mixed-prime
  maps (div23, div235), θ* is the optimum over Theorem-1 certificates (Theorem 2a); Theorem 3
  (exactness) does not apply to them.
* **Korec**: a certified sample `c > c_0` with `#{n ≤ X : no iterate < n^c} = O(X^{θ_c})` (Theorem 4;
  this holds for every `c > c_0`). **Sharp**: a certified `c < c_0` for which the depth-log n tree certifies
  no iterate below `n^c` except on `O(X^{θ})` starts (Proposition 4.2).
* Expanding maps: a certified sample `c < c_0` with `#{n ≤ X : every iterate ≤ n^c} = O(X^{θ_c})`
  (Theorem 5, holds for every `c ∈ (1, c_0)`), and the early-drop density `q` (Theorem 6).

## Contracting systems (Δ < 0)

| system | CLS | states | c_0 (closed form) | θ never-drop (certified) | θ* (float) | Korec sample c → θ_c | sharp c → θ |
|---|---|---|---|---|---|---|---|
| div235_7n1 | 001/058 | 24 | 40165 ln7 / (80330 ln2 + 27334 ln3 + 14445 ln5) = 0.71732 | 857/913 = 0.93866 | 0.93866 | 37/50 → 0.99956 | 69/100 → 0.99935 |
| div23_5n1 | 002/059 | 5 | 7 ln5 / (14 ln2 + 6 ln3) = 0.69135 | 453/527 = 0.85958 | 0.85958 | 18/25 → 0.99887 | 67/100 → 0.99937 |
| div23_7n1 | 003/060 | 5 | 5 ln7 / (10 ln2 + 3 ln3) = 0.95133 | 999/1000 = 0.99900 | 0.99900 | 49/50 → 0.99965 | 93/100 → 0.99980 |
| m3_b | 004/061 | 1 | (4/3) log_3 2 = 0.84124 | 521/540 = 0.96481 | 0.96481 | 87/100 → 0.99892 | 41/50 → 0.99943 |
| m3_d | 005/062 | 1 | (4/3) log_3 2 = 0.84124 | 521/540 = 0.96481 | 0.96481 | 87/100 → 0.99892 | 41/50 → 0.99943 |
| m3_g | 008/063 | 1 | (2/3) log_3 5 = 0.97665 | 1906/1907 = 0.99948 | 0.99948 | 989/1000 → 0.99985 | 19/20 → 0.99933 |
| par_3_1 (3x+1, sanity) | 013 | 1 | log_4 3 = 0.79248 (Korec) | 1082/1139 = 0.94996 | H(log_3 2) = 0.949955 (Terras) | 41/50 → 0.99913 | 77/100 → 0.99942 |
| 3n+d, d ∈ {−1,3,5,7,9,13,17}; 6n+2 | 011,012,014–018, 031 | 1 | log_4 3 | 1082/1139 | 0.94996 | same | same |
| split5_1 | 048/064 | 2 | (1/4) log_2 5 = 0.58048 | 994/1061 = 0.93685 | 0.93685 | 61/100 → 0.99964 | 14/25 → 0.99982 |
| split5_3 | 049/065 | 2 | (1/4) log_2 5 = 0.58048 | 457/787 = 0.58069 | 0.58068 | 61/100 → 0.99814 | 14/25 → 0.99910 |
| desc_m3_4n5 | 051 | 1 | log_3 2 = 0.63093 | 432/577 = 0.74870 | 0.74870 | 33/50 → 0.99855 | 61/100 → 0.99925 |
| desc_s32_plus9 | 052 | 8 | (22/67) log_2 3 = 0.52044 | 780/1369 = 0.56976 | 0.56976 | 11/20 → 0.99882 | 1/2 → 0.99944 |
| desc_split7_1 | 053 | 2 | (1/6) log_2 7 = 0.46789 | 703/933 = 0.75348 | 0.75348 | 49/100 → 0.99957 | 11/25 → 0.99930 |

Comparison with earlier census bounds (same quantity H(X)): split5_3 `0.58496 → 0.58069`
(round 2: `log_2(3/2)`), split5_1 `0.9383 → 0.93685`, split7_1 `0.75488 → 0.75348`. These three
improvements are small because the earlier hand-chosen `s` were already near-optimal; Theorem 3
shows `0.58068 / 0.93685 / 0.75348` are the exact limits of this method. All other entries in the table
are new (no density bound was recorded before for CLS-001–005, 008, 011–018, 031, 049 (other than
round 2's 0.585), 051, 052).

Constants: `k_0` (Theorem 1) is 0 for most maps and at most 7 (3n+17); the per-block constant `C_1`
is computed exactly by `never_drop_constants` (it is large but harmless; e.g. it is the factor
`w_0 q_max^θ 2^s / w_min · 2^θ/(2^θ−1)`).

Mixed-prime maps (div23, div235): the tree splits adaptively by 2, 3 (and 5) — Section 1 of
`theory.md`. Theorem 1 uses dyadic blocks and cuts at modulus `≥ Y`, so the proof is unchanged.
EVIDENCE: θ* and c_0 do not change under any of the 2 / 6 possible split orders (`evidence.py [E2]`).

What the actual counts look like (EVIDENCE, `evidence.py [E4]`): below `2^18` the starts that do not
drop within 20000 steps are only the cycle minima (e.g. 1 for 3x+1; 1, 3, 5, 61, 125 for split5_3), far
below `X^θ`. The bound θ is a theorem about the method, not the truth.

## Expanding systems (Δ > 0)

| system | CLS | states | c_0 | sample c → θ_c (Theorem 5) | early-drop density q (Theorem 6) |
|---|---|---|---|---|---|
| 5n+d, d ∈ {1,3,5,7,11,131,353} | 022/024, 027, 029, 030, 020, 021, 025 | 1 | log_4 5 = 1.16096 | 57/50 → 658447/658600 = 0.99977 | [0.823782, 0.824073] (depth 300); [0.823922, 0.824002] (depth 400) |
| 10n+2 | 010 | 1 | log_4 5 | 57/50 → 0.99977 | same as 5n+1 |
| 7n+1, 7n+7 | 032/034, 035 | 1 | log_4 7 = 1.40368 | 69/50 → 0.99980 | 0.699249 (6 digits) |
| 9n+1 | 037 | 1 | log_2 3 = 1.58496 | 39/25 → 0.99982 | 0.613870 |
| m3_e (7n+2, 7n+1) | 006/007 | 1 | (2/3) log_3 7 = 1.18083 | 29/25 → 0.99972 | [0.722567, 0.722571] |
| perm_1932 (Collatz 1932) | 038/040 | 1 | (5/3) log_3 2 = 1.05155 | 103/100 → 0.99765 | (signed intercepts: lower bound only) |
| perm_1932inv | 042 | 2 | (2/3) log_2 3 = 1.05664 | 103/100 → 0.99718 | – |
| perm_swap, perm_b | 047, 044 | 1 | (5/3) log_3 2 | 103/100 → 0.99765 | – |
| perm_c | 045 | 2 | (2/3) log_2 3 | 103/100 → 0.99718 | – |
| perm_d | 046 | 4 | log_4 5 | 57/50 → 0.99952 | – |

Read: for 5x+1, almost every n (all but `O(X^{0.99977})` of `n ≤ X`) has an iterate above `n^{1.14}`;
the same holds for every `c < 1.16096`. Exactly a fraction `q ≈ 0.8240` of all n drop below themselves
within `log_2 n` tree steps; at least 17.59% do not. EVIDENCE (`evidence.py [E3]`): in `[2^17, 2^18)`
the proportion of 5x+1 starts that drop at all (within 20000 steps) is 0.82410 ≈ q, for 7x+1 0.69920 ≈ q,
for 9x+1 0.61382 ≈ q. Conjecture: the full drop set D has density exactly q for these maps.
Proposition 7 shows that proving `upper density(D) < 1` would already prove the existence of a
divergent orbit or of infinitely many cycles, so this is not reachable here.

## Status per CLS entry

All the GLOBAL questions listed stay **OPEN** (tier 5). The density statements above are **PROVED**
(tier 2: a written inequality argument plus an exact finite certificate), except where marked EVIDENCE.
