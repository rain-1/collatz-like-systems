# Round 6, lens "countlaw_wide": the count law beyond the digit horizon for general table maps

Agent-written (one prover). Examined by two referees ([REFEREE1.md](REFEREE1.md), [REFEREE2.md](REFEREE2.md), independent checks
`referee1_check.py`, `referee2_check.py`) and revised after each; see "Revision after REFEREE1" and
"Revision after REFEREE2" at the end. Every claim is
labelled PROVED / EVIDENCE / OPEN. Proofs are in [THEORY.md](THEORY.md). No literature search was done.

**Bottom line.** The round-5 count-law theorems (microrange R, C, D; fourier U'; split5_3 one-ended
and two-ended) are ported to every unit-multiplier p-adic table map whose multipliers are powers of a
single integer g. The one-ended theorem (G1) is proved for every such map that satisfies the finiteness
condition (F) and the rescue condition (P); (P) is a per-system check, and it holds for all 23 systems
in the tables. The two-ended theorem (G2) is a sketch conditional on a ballot hypothesis (B2), for which
there is numerical evidence only. For split5_3 the two-ended law is PROVED in `split5_3_s27.md`, in that
file's own coding, and the general formula here reproduces its constant 0.459918. Translating that proof to
the coding used here is not written out. The certified counts (C_G) and the every-octave constants (U'_G) were
computed for K7, split5_3, m3_b and, for U'_G, for 19 census systems. **No system is settled.** In
particular no type-(c) system and no open census entry is settled. These are statements about
how many starts survive about log_p X + c log_p log_p X digits. A counting proof of GLOBAL along these
lines would need control out to C* log_p X digits, with C* = 1/(1-h) between 1.56 and 1906 for the
contracting open systems here. (GLOBAL itself does not require this; see the GLOBAL section.)

## Results

| id | statement | status | where |
|---|---|---|---|
| R_G | Reduction for any table map: N(p^m, m+j) is bracketed by Σ_nodes min_B / max_B #{t < p^{K-j} : g^A t + B ∈ S}, with S, A in-horizon, B arbitrary. | PROVED. Checked in 1452 brute-force cases on 14 systems and node by node (582 nodes, 8 systems; a wrong multiplier is detected); reproduces round-5 microrange numbers for 3x+1. | THEORY §1, `check_all.py` 3 |
| F_G | Averaged discrepancy for u uniform on <g mod p^K>: E max_B \|Φ - Φ̄\| <= ι (p/(p-1))(1 + K ln p) sqrt(\|S\|). ι is the index of the closure of <g> in Z_p^* (2 for g = 3, 5 mod 2^k; 4 for 7 mod 2^k; 2 for 4, 7 mod 3^k; 1 for 2, 5 mod 3^k). | PROVED | §2, part 4 |
| P_G | Every non-empty continuation set has at least p^{h0 K - O(1)} elements for K >= K1, under the checked condition (P). K1 can be about 10 to 15 (sf3_13, desc_s32_plus9). (P) holds for all 23 systems; "bad" states occur for 6 of them and are handled by the rescue argument. | PROVED | §3, part 5 |
| G1 | **One-ended count law, general.** Assume (SG), (F), (P) ((P) is checked per system). Then for all but M^{1-η/2} of the m in [M, 2M), \|N(p^m,b)/p^mP(b) - 1\| <= M^{-η/3} for every b <= m + (h_*/2 - η) log_p M. | PROVED | §4 |
| G1' | Same for the actual stopping count (T^i(n) >= n) on the octave [p^{m-1}, p^m), with exceptional set 2M^{1-η/4} + O(log M) and error O(M^{-η/6}) (corrected after REFEREE1; the O(log M) octaves come from Lemma X: elementary, unique factorization only). Hypothesis H0 (rows n -> n + v with no multiplication or division have v >= 0) holds for all 23 systems. | PROVED | §4 |
| X | Exceptional octaves of Lemma X, computed exactly for 10 <= m <= 3000 for every system: only small octaves are flagged (m <= 17, where n >= 8tV can fail); there is no Diophantine exception (no g^A within the critical distance of p^E) up to m = 3000. So for 18 <= m <= 3000 and b <= m + 2 log_p m, slope count = actual count on the octave, for every system. Brute force on whole octaves agrees. | PROVED (exact) | part 7 |
| G2 | **Two-ended count law**, depth up to m + (c_2 - η) log_p M with c_2 = min(1, h_*/2 + H_2/(2α log_p g)). | Conditional sketch on (B2) for every system. For split5_3: PROVED in split5_3_s27.md in its own coding (y = n + 3, bit coding, actual survivors); the formula here gives the same constant 0.459918; the translation to the present coding is not written out. (First version said "PROVED for split5_3"; withdrawn.) | §5 |
| B2 | Ballot asymptotics \|R_n\| ≍ ρ*^n n^{-3/2}, uniform. The normalised ratio stays in a band of width 0.25 to 1.7 (natural log) for n in [100, 1200], for all 19 contracting systems. For m3_g (ratio rising monotonically), sf3_13 and sf3_135 (large oscillations) the data neither confirm nor refute the exponent 3/2. For all 19 systems the maximum of the normalised ratio occurs in the last third of [100, 1200], so a slow upward drift is generic (REFEREE2). | EVIDENCE (weak for m3_g, sf3_13, sf3_135); OPEN as a theorem for every system | `evidence_b2.py` |
| h | h = log_p min_θ ρ(M(θ)) for every system. Proved enclosure h0 <= h_* <= h <= h_up, with h_up equal to h to 6 digits and h0 at K0 = 1500 within 0.011 of h. Matches round 3 `density` θ* to 5 digits for every common system. | PROVED (bounds); h = h_* is PROVED for single-state systems and split5_3, EVIDENCE otherwise | `cwconst.py` |
| C_G | Certified relative errors of N(p^m, m+j), j = 1..10, m = 100 and 1000, for K7, split5_3 and m3_b (tables below). | PROVED (exact integer computation) | `cert.py` |
| U'_G | Every-octave constants D'_{L,m} for 19 systems (table below). | PROVED (exact rationals) | `everyoct.py` |
| GLOBAL | Nothing settled. Per-system critical constant C* = 1/(1-h) is in the constants table. | none | §7 |

## Constants per system (Theorems G1, G2; `data/constants_K1500.txt`)

p = base, g = generator of the multipliers, st = automaton states, drift = Haar mean of log slope per digit,
h = growth exponent of survivors, h0 = proved lower bound on h_* (K0 = 1500), c1 = h/2 (G1 depth constant;
h0/2 is the proved admissible value where h_* = h is not proved), c2 = G2 constant (conditional on B2; for
split5_3 it equals the constant proved in s27 in its own coding), Pot = per-state relabelling makes the walk i.i.d. (gives h_* = h), C* = 1/(1-h).

| system | type / census | p | g | st | drift | h | h0 | c1 | c2 | Pot | C* |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3x+1, 3x-1, 3x+5 | controls | 2 | 3 | 1 | -0.144 | 0.949956 | 0.9417 | 0.4750 | 0.7603 | yes | 19.98 |
| K7 (z-form) = sf3_7 | (c), open core | 2 | 3 | 2 (3) | -0.419 | 0.749059 | 0.7395 | 0.3745 | 0.5456 | no | 3.985 |
| sf3_17 | (c), open core | 2 | 3 | 4 | -0.327 | 0.790075 | 0.7798 | 0.3950 | 0.5771 | no | 4.764 |
| sf3_57 | (c), open core | 2 | 3 | 4 | -0.419 | 0.719337 | 0.7094 | 0.3597 | 0.5138 | no | 3.563 |
| sf3_157 | (c), open core | 2 | 3 | 3 | -0.327 | 0.773541 | 0.7636 | 0.3868 | 0.5564 | no | 4.416 |
| sf3_357 | (c), open core | 2 | 3 | 3 | -0.327 | 0.788017 | 0.7784 | 0.3940 | 0.5755 | no | 4.717 |
| sf3_13 | (c), open core | 2 | 3 | 4 | -0.419 | 0.428077 | 0.4180 | 0.2140 | 0.3552 | no | 1.749 |
| sf3_135 | (c), open core | 2 | 3 | 3 | -0.379 | 0.359256 | 0.3503 | 0.1796 | 0.2926 | no | 1.561 |
| sf3_137 (W) | open, drift > 0 | 2 | 3 | 3 | +0.039 | 1 | 0.9971 | 0.5 | - | no | ∞ |
| split5_1 | (c), CLS-048/064 | 2 | 5 | 2 | -0.291 | 0.936849 | 0.9280 | 0.4684 | 0.6541 | no | 15.84 |
| split5_3 | (c), CLS-049/065 | 2 | 5 | 2 | -0.291 | 0.580684 | 0.5707 | **0.29034** | **0.45992** (= s27) | yes | 2.385 |
| desc_split7_1 | (c), CLS-053 | 2 | 7 | 2 | -0.369 | 0.753482 | 0.7442 | 0.3767 | 0.5910 | no | 4.057 |
| desc_s32_plus9 | (c), CLS-052 | 2 | 3 | 8 | -0.332 | 0.569758 | 0.5603 | 0.2849 | 0.4719 | no | 2.324 |
| m3_b, m3_d | (c), CLS-004/005 | 3 | 4 | 1 | -0.174 | 0.964814 | 0.9598 | 0.4824 | 0.8538 | yes | 28.42 |
| m3_g | (c), CLS-008 | 3 | 5 | 1 | -0.026 | 0.999475 | 0.9962 | 0.4997 | 0.8407 | yes | 1906.1 |
| desc_m3_4n5 | (c), CLS-051 | 3 | 2 | 1 | -0.405 | 0.748700 | 0.7425 | 0.3744 | 0.6122 | yes | 3.979 |
| 5x+1, m3_e, perm_1932 | expanding / permutation | 2, 3, 3 | 5, 7, 2 | 1 | > 0 | 1 | 0.998+ | 0.5 | - | yes | ∞ |

Cross-checks: h agrees with round 3 `density` θ* (3x+1 0.94996, m3_b 0.96481, m3_g 0.99948, split5_1
0.93685, split5_3 0.58068, desc_m3_4n5 0.74870, desc_s32_plus9 0.56976, desc_split7_1 0.75348). The one-ended
split5_3 constant h/2 = 0.29034 and the two-ended 0.45992 equal those of `split5_3_s27.md`. The 3x+1
constant 0.47498 = H(λ)/2 is not a round-5 result: round 5 (microrange Theorem D) proved only
h0/2 >= 0.4715 and withdrew H(λ)/2. Here G1, together with h_* = h for single-state systems (Raney's lemma
plus types, THEORY §5), gives depth (0.47498 - η) log_2 M for 3x+1, a small strengthening of round-5
Theorem D. (Corrected after REFEREE2, N1.) K7 in z-form and sf3_7 in n-form have the same h, as the
conjugacy predicts. For expanding maps c2 is not stated (G2 needs θ* > 0).

**Hypotheses fail for** (`hyp_scan.py`, all of census/systems.py plus round 2 descent and rewriting,
`data/hyp_scan.txt`):
* mixed primes: div23_5n1, div23_7n1, div235_7n1, farkas, farkas5m, and the round-3 mixedbase blocked system.
  The branch depends on n mod 3 or mod 5 inside a 2-adic map, so no single-prime digit tree decides it.
  The census density lens has exponents for these, but Lemma T fails: there is no p-adic node state.
* non-unit multipliers: 2n+1, 4n+2, 6n+2, 6n+3, 10n+2 (u divisible by p), and the suffix permutations.
* trivial multiplier group (all u = 1: n+1, n+5, m3_f, perm_flip). Lemma F_G has no averaging. The count is
  then a pure digit statement.
* (F) fails, an infinite decided chain: 3n+2, 3n+4, 5n+2, div3_2n, div2_3n. In general (F) fails exactly
  when there is a cycle of division-free decided steps among residue classes; in these five maps the cycle
  has length 1 (a class maps into itself with no division), and those orbits grow without bound.
* the hypotheses hold but the result is trivial: split_d (d = 5, 13, 73, 97, 7081), splitB_7/71, m3_a, m3_c,
  desc_s8_35, desc_s32_max, desc_s32_d65. There R_b is empty for every b from some point on: b >= 2 for
  the split maps, b >= 1 for m3_a and m3_c, b >= 4 for desc_s8_35, b >= 30 for desc_s32_max and
  desc_s32_d65 (`data/hyp_scan.txt`; checked up to b = 30 and empty thereafter because emptiness
  propagates). This is a *slope* descent certificate. It gives actual descent only for n large enough to
  absorb the additive constants (for example the +7081), and several of these maps have extra cycles among
  small n. The count law is 0 = 0.
* the hypotheses hold and the theorem is true but says nothing about GLOBAL: expanding maps (5x+d, 7x+d,
  9x+1, m3_e, mahler) and the permutations perm_1932, perm_1932inv, perm_swap, perm_b, perm_c, perm_d,
  perm_ceil2. All have positive log-drift, so h = 1, and a positive proportion of every octave survives
  every depth.

## Certified counts C_G (Theorem R_G evaluated in exact integers)

rel = (bound - p^m P(m+j)) / p^m P(m+j). The bracket uses all intercepts B, so it uses no information on
digits beyond the horizon. K = j + j' is the split parameter. Files are `data/certified_<system>.txt` and
`data/log_cert*.txt`.

| j | K7 (p=2, K=28) m=100 | m=1000 | split5_3 (p=2, K=28) m=100 | m=1000 | m3_b (p=3, K=17) m=100 | m=1000 |
|---|---|---|---|---|---|---|
| 1 | [-0.00051, +0.00051] | [-0.00036, +0.00036] | [-0.00342, +0.00342] | [-0.00728, +0.00728] | [-0.00002, +0.00002] | [-0.00003, +0.00003] |
| 2 | [-0.00276, +0.00310] | [-0.00082, +0.00081] | [-0.00407, +0.00407] | [-0.01050, +0.00888] | [-0.00004, +0.00004] | [-0.00009, +0.00011] |
| 3 | [-0.00354, +0.00436] | [-0.00126, +0.00126] | [-0.00794, +0.00770] | [-0.01165, +0.00998] | [-0.00020, +0.00019] | [-0.00017, +0.00017] |
| 4 | [-0.00630, +0.00750] | [-0.00191, +0.00206] | [-0.01878, +0.01534] | [-0.01697, +0.02285] | [-0.00060, +0.00055] | [-0.00053, +0.00056] |
| 5 | [-0.01131, +0.01235] | [-0.00340, +0.00380] | [-0.02805, +0.02683] | [-0.03394, +0.04069] | [-0.00149, +0.00136] | [-0.00161, +0.00151] |
| 6 | [-0.01319, +0.01754] | [-0.00563, +0.00599] | [-0.04957, +0.04684] | [-0.05572, +0.05847] | [-0.00412, +0.00344] | [-0.00350, +0.00341] |
| 7 | [-0.01828, +0.02471] | [-0.01074, +0.01033] | [-0.09528, +0.10810] | [-0.08846, +0.10442] | [-0.00715, +0.00654] | [-0.00646, +0.00654] |
| 8 | [-0.02682, +0.03989] | [-0.01487, +0.01572] | [-0.15283, +0.17983] | [-0.11796, +0.15513] | [-0.01468, +0.01396] | [-0.01235, +0.01164] |
| 9 | [-0.03333, +0.05224] | [-0.02391, +0.02543] | [-0.17701, +0.19786] | [-0.18618, +0.21279] | [-0.02820, +0.02968] | [-0.02533, +0.02486] |
| 10 | [-0.05192, +0.07418] | [-0.04139, +0.04250] | [-0.26637, +0.35090] | [-0.22489, +0.26907] | [-0.06755, +0.06685] | [-0.05014, +0.05148] |

Coarser runs (K = 24 for K7 and split5_3, K = 16 for m3_b) are in `data/log_cert_*.txt`. They are consistent with these and weaker, e.g. split5_3 j = 10 at m = 100: [-0.523, +0.856] at K = 24 against [-0.266, +0.351] at K = 28.

Reading: at m = 1000 the number of n < p^1000 that survive 1000 + j digits is pinned to within the
stated relative error. At m = 1000, K7 is within 1.1% for j <= 7 and within 4.3% at j = 10. m3_b is within 0.7% for
j <= 7 and 5.2% at j = 10 (base 3 gives fewer line points: 3^7 at j = 10 against 2^18). split5_3 is the weakest
(h = 0.58, so its continuation sets are small): within 1.2% only for j <= 3, and 27% at j = 10. For comparison, round 5 found that
for 3x+1 the in-horizon sandwich alone gives about -84% / +48% at j = 10; I did not compute it for these systems.
The precision is limited by the 2^{K-j} line points standing in for 2^K residues (same limitation as round 5).

## Every-octave constants U'_G (`data/everyoct.txt`)

For every b >= L: |N(p^{b-m}, b)/(p^{b-m} P(b)) - 1| <= D'_{L,m} (k = 1). Exact rationals. Values >= 1 give no
lower bound.

| system | L | D'_{L,1} | D'_{L,2} | D'_{L,3} |
|---|---|---|---|---|
| 3x+1 | 14 | 213/1627 = 0.1309 | 213/749 = 0.2843 | 349/749 = 0.4659 |
| 3x-1 | 14 | 213/1627 = 0.1309 | 213/749 = 0.2843 | 349/749 = 0.4659 |
| 3x+5 | 14 | 213/1627 = 0.1309 | 213/749 = 0.2843 | 349/749 = 0.4659 |
| K7 | 14 | 29/77 = 0.3766 | 127/137 = 0.9270 | 73/55 = 1.3272 |
| sf3_7 | 14 | 15/37 = 0.4054 | 31/33 = 0.9393 | 73/55 = 1.3272 |
| sf3_17 | 14 | 101/363 = 0.2782 | 23/33 = 0.6969 | 7/6 = 1.1666 |
| sf3_57 | 14 | 11/37 = 0.2972 | 63/97 = 0.6494 | 107/85 = 1.2588 |
| sf3_157 | 14 | 108/367 = 0.2942 | 93/149 = 0.6241 | 17/15 = 1.1333 |
| sf3_357 | 14 | 9/41 = 0.2195 | 19/41 = 0.4634 | 7/9 = 0.7777 |
| sf3_13 | 14 | 1/1 = 1.0000 | 5/2 = 2.5000 | 5/1 = 5.0000 |
| sf3_135 | 14 | 1/1 = 1.0000 | 3/1 = 3.0000 | 27/5 = 5.4000 |
| split5_1 | 14 | 89/569 = 0.1564 | 145/559 = 0.2593 | 143/375 = 0.3813 |
| split5_3 | 14 | 4/5 = 0.8000 | 19/9 = 2.1111 | 23/5 = 4.6000 |
| desc_split7_1 | 14 | 69/109 = 0.6330 | 381/331 = 1.1510 | 485/331 = 1.4652 |
| desc_s32_plus9 | 14 | 1/2 = 0.5000 | 5/3 = 1.6666 | 13/5 = 2.6000 |
| m3_b | 9 | 289/832 = 0.3473 | 17/28 = 0.6071 | 13/14 = 0.9285 |
| m3_d | 9 | 17/56 = 0.3035 | 29/56 = 0.5178 | 115/128 = 0.8984 |
| m3_g | 9 | 139/768 = 0.1809 | 45/128 = 0.3515 | 17/32 = 0.5312 |
| desc_m3_4n5 | 9 | 61/103 = 0.5922 | 122/103 = 1.1844 | 98/37 = 2.6486 |
| K7 | 16 | 19/52 = 0.3653 | 12/13 = 0.9230 | - |
| split5_3 | 16 | 17/25 = 0.6800 | 44/25 = 1.7600 | - |
| m3_b | 10 | 173/512 = 0.3378 | 16669/31744 = 0.5251 | - |

The 3x+1 row reproduces round-5 `fourier` exactly (213/1627, 213/749, 349/749). The L = 16 rows for K7 (19/52, 12/13) and split5_3 (17/25, 44/25) reproduce the round-5 values exactly, from independent code.
sf3_13 and sf3_135 (h = 0.43, 0.36) get nothing at L = 14: their smallest continuation sets are tiny.

## What the general theorem implies and does not imply about GLOBAL

**Direction of the implication (corrected after REFEREE1).** GLOBAL does not imply that every start drops
within C* log_p X digits; it allows stopping times much longer than that. Conjecture E at depth
(C* + ε) log_p X, plus a proof that there are no new cycles, would be a *sufficient* route to GLOBAL by
counting. It is not a necessary condition. The first version said "GLOBAL needs control out to C* log_p X
digits"; that is withdrawn.

For every contracting system in the table, G1 says: in almost every octave the survivor count stays equal
to the Haar prediction X P(b) up to b = log_p X + (h_*/2) log_p log_p X. That prediction is
X^{1 - (1-h) b / log_p X}. A count that tracks this prediction can show that every start of the octave
drops only at a depth b where X P(b) < 1, that is b > C* log_p X. G1 and G2 stop at depth (1 + o(1)) log_p X. The missing factor is C*:
1.56 (sf3_135), 1.75 (sf3_13), 2.32 (desc_s32_plus9), 2.38 (split5_3), 3.6 to 4.8 (the other S-cores,
desc_split7_1, desc_m3_4n5), 15.8 (split5_1), 20.0 (3x+1), 28.4 (m3_b, m3_d), 1906 (m3_g).
The cores sf3_13 and sf3_135 have the smallest C*: there the Haar prediction already falls below 1 at
1.56 log_2 X digits. Among the systems in this table that is the least extrapolation of Conjecture E (the
mixed-prime and other excluded maps have no C* computed here), but it is still an extrapolation by a factor
1.5 beyond anything proved. The theorems are counts with relative errors.
They are consistent with any finite set of extra cycles (3x-1 and 3x+5 have the same constants as 3x+1)
and with divergent orbits (5x+1, m3_e and W satisfy G1 with h = 1). So they cannot settle GLOBAL by
themselves, and they do not. No individual orbit is controlled.

## Honest limits

* G1 is "almost every octave", with X = p^m (or the octave [p^{m-1}, p^m)). For every octave only U'_G
  holds, with a fixed error and m < L digits.
* G2 is a conditional sketch. For split5_3 the result is proved in s27 in a different coding, and
  the translation is not written out here. For other systems it needs (B2), which I did not prove even for
  single-state systems. The classical ballot asymptotic would cover those, but I have not written it out. For
  multi-state systems I know no proof.
* h_* = h is proved for single-state systems (Raney's lemma plus types) and for split5_3 (the same
  (Pot)/Raney argument run from both states of G, with a buffer word from each; THEORY §5. Before REFEREE2
  this was cited from s27's continuation-set bound, which is stated in s27's coding). For the other
  multi-state systems only h0 (K0 = 1500) is proved, 0.010 to 0.011 below h. The proved G1 constant there
  is h0/2, about 0.005 below h/2.
* The certified tables cover two values of m and j <= 10 for three systems. The split5_3 entries at j >= 7
  are weak (10 to 35%).
* Floating point enters only in the minimisation over θ (the reported h and c2). h_up is a proved
  upper bound via a Collatz-Wielandt vector in 60-digit Decimal arithmetic with a safety margin. Everything
  in R_G, C_G, U'_G, P_G and X is exact integer arithmetic.
* Quoted external results: Fekete's lemma, Raney's cyclic lemma, the method of types, the Erdős–Turán
  inequality (G2 only; quoted from memory with an unspecified absolute constant), and the
  lifting-the-exponent facts behind ι (checked numerically for L <= 20). Lemma X uses only |g^A - p^E| >= 1.

## What stayed open

1. (B2) for any system, and hence G2. For split5_3, the translation of s27's two-ended proof to the
   present coding.
2. G1 for every octave with error tending to 0. This is the round-5 O2 problem, now for every system:
   it needs a bound for the specific multipliers g^A rather than their average.
3. Any depth beyond (1 + o(1)) log_p X. Conjecture E at C* log_p X is untouched for every system.
4. Mixed-prime maps (div23_*, farkas): no node-state reduction. A count law for them would need a
   different Lemma T.

## Files

| file | content |
|---|---|
| `THEORY.md` | statements and proofs (R_G, F_G, P_G, G1, G1', X, G2, B1, U'_G, GLOBAL) |
| `cwlib.py` | systems, digit automaton, exact DP survivor counts, thresholds |
| `cw.c` (`cw`) | exact minimum-prefix-slope functions (`gfun`), window extremes (`win`), U' constants (`uprime`) |
| `cert.py` | Theorem R_G brackets and the certified tables C_G |
| `everyoct.py` | Theorem U'_G constants |
| `cwconst.py` | h, h_up, h0, ι, α, H_2, c1, c2, Pot, G/B states, C* |
| `hyp_scan.py` | recognises census maps as single-prime table maps, reports failures, computes constants |
| `evidence_b2.py` | numerical evidence for (B2) |
| `check_all.py` | exact checks, parts 1 to 9; exits 0 iff all pass (about 12 min in total; part 9 added after REFEREE1) |
| `REFEREE1.md`, `referee1_check.py` | referee report and independent check (not edited by the prover) |
| `data/` | constants, certified tables, U' constants, scan, exceptional octaves, logs. `log_check_378.txt` is an old log that records a failure of the then-buggy mutation test of part 3; it is superseded by `log_check_rev1.txt` (all parts pass). |

## Revision after REFEREE1

REFEREE1 checked everything independently and found **no mathematical error**. It asked for relabelling
and wording fixes. Each one is made in this README and in THEORY.md (marked **[Rev]**, list in THEORY §8):

| referee item | what was wrong | repair |
|---|---|---|
| G1 wording | "fully proved in that generality" | Now "for (SG) maps satisfying (F) and (P)"; (P) is a per-system check. |
| G1' bookkeeping | G1 at m - 1 was used one digit beyond its range | G1 applied with η/2. Exceptions are now 2M^{1-η/4} + O(log M) and the error is O(M^{-η/6}). Statement and proof rewritten (THEORY §4). |
| P_G, K1 | K1 not discussed | Note added: K1 can be about 10 to 15 (sf3_13, desc_s32_plus9). This does not affect asymptotic use. |
| G2 "PROVED for split5_3" | **withdrawn as stated.** s27 proves it for a different counting set, and the transfer is not written out | Relabelled: PROVED in s27 in its own coding; constant reproduced; translation not written. Lemma B1 corrected (it no longer says (B2) "is" s27's theorem). |
| B2 evidence | "bounded" overstated for three systems | m3_g, sf3_13 and sf3_135 marked as neither confirming nor refuting the exponent 3/2. |
| GLOBAL "needs" | **wrong direction, withdrawn** | Rephrased as a sufficient route: "a counting proof along these lines would need...". |
| hypothesis scan | "R_b empty from b = 1 to 30" | Exact starting depths given. Marked as a slope certificate that does not exclude extra cycles among small n. |
| "least extrapolation anywhere in the census" | overreach | Now "among the systems in this table". |
| (F) failure | "some class maps into itself" | Now "a cycle of division-free decided steps", of any length. |
| §5 notation | k used for two things | Terminal length renamed ℓ. |
| ι list | m3_e (g = 7 mod 3^k, ι = 2) missing | Added. |
| round-5 reproduction | claimed without a script | `check_all.py` part 9 recomputes 3x+1, m = 1000, K = 24, j = 1..8 and compares with `round5/microrange/data/certified_siblings.txt` (d = 1). All 8 rows agree to the printed 5 decimals. |

Nothing that was PROVED before is now downgraded except G2 for split5_3, which moves from "PROVED here" to
"PROVED in s27 in its own coding, transfer not written out". No new system is settled. The overall verdict
is unchanged: no census system, and in particular no type-(c) system or open entry, is settled by this lens.

## Revision after REFEREE2

REFEREE2 re-derived every proof, recomputed all 23 systems with its own code, and found **no
mathematical error** (needs_repair: no). It asked for one citation fix and three wording nits. All are
made in this README and in THEORY.md (marked **[Rev2]**, list in THEORY §9):

| referee item | what was wrong | repair |
|---|---|---|
| h_* = h for split5_3 | cited from the continuation-set bound of `split5_3_s27.md`, which is stated in s27's (z, s) bit coding of y = n + 3: a coding transfer of the kind withdrawn for G2 | Replaced by this file's own (Pot)/Raney argument, run from both states of G = {(0,0), (1,1)}: potential φ(1,1) - φ(0,0) = -(1/2) log(5/4), labels {1/2, √5/2} from both states, dip 0, buffer words "1 0" from (0,0) and "0" from (1,1), both reaching slope 5/4 > √(5/4) (THEORY §5). The G1 constant 0.29034 for split5_3 now rests on this file alone. The exact check is REFEREE2's `referee2_check.py` section J; `check_all.py` part 6 still checks a buffer word from the root only. |
| N1 (3x+1 constant) | 0.47498 presented as "the round-5 H(λ)/2" | Round 5 proved only h0/2 >= 0.4715 and withdrew H(λ)/2. Now stated as following from G1 and h_* = h for single-state systems here, a small strengthening of round-5 Theorem D. |
| N2 (B2 evidence) | the slow upward drift was described only for m3_g | One sentence added: for all 19 systems the maximum of the normalised ratio occurs in the last third of the range, so the drift is generic. |
| N3 (external results) | THEORY header said Erdős–Turán is in Section 7 and omitted Raney's lemma, the method of types and lifting the exponent | THEORY header list aligned with the README list (Erdős–Turán in Section 5). |

No status changes. The verdict is unchanged: no census system is settled by this lens.

