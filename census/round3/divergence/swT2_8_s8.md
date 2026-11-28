# swT2_8_s8: a two-swap neighbour of the 1932 map that needs a large certificate

**Rule (a permutation).** Q(n) = σ(G(n)). Here G is the 1932 permutation
(3q ↦ 2q, 3q+1 ↦ 4q+1, 3q+2 ↦ 4q+3), and σ swaps n ↔ n+1 whenever
n ≡ 2 or 8 (mod 18): it exchanges 2 ↔ 3 and 8 ↔ 9 within each block of 18.
So |Q(n) − G(n)| ≤ 1 for all n, and Q is affine on classes mod 54. It changes G
at the same density as round 2's swT9_15_s8 (two swapped pairs mod 18).

**Question.** FATE of 8.

| claim | status | tier |
|---|---|---|
| 8 never returns; the orbit is infinite | PROVED | 2 |
| a congruence separator exists mod 2304 = 2^8·9 (732 of 2304 classes) | PROVED | 2 |
| no union of residue classes mod 2^i 3^j < 2304 separates 8, and none mod 2^i 3^j with i ≤ 7 for any j | PROVED | — |
| the itinerary is not eventually periodic | PROVED (all slopes have denominator 3) | — |
| infinitely many falls | EVIDENCE: 2235 falls in the first 20000 steps, the last at step 19988 | — |

The orbit begins 8, 11, 15, 10, 13, 17, 23, 31, 41, 55, 73, 97, 128, 170, 227, 303,
202, 269, …. It rises mostly, with recurring falls.

## Proof

The separator was found with Lemma P3 (`theorem5_precision3.md`). In the
full-class graph Γ_8 (nodes mod 2^8·9 = 2304), the forward closure of the class
of Q(8) = 11 has 732 nodes and does not contain 8. Let U be the union of these
732 classes mod 2304. Every node's three subclasses are mapped by Q into nodes
of the closure, so Q(U) ⊆ U. The check re-verifies this independently of
Lemma P3: it lifts U to 2196 classes mod 6912 = 128·54 and runs the exact
residue graph of the 54-periodic affine table (divlib.images). Also 8 ∉ U and
Q(8) ∈ U. Q is a bijection (σ is an involution and G a permutation), so 8 never
returns and the orbit is infinite.

The itinerary is aperiodic by Lemma I with p = 3: every slope is 2/3 or 4/3.

**Least modulus.** For i ≤ 7, every sink component of Γ_i contains the class of 8. By Corollary P3, no separator exists
modulo 2^i·3^j for i ≤ 7 and any j. The other moduli 2^i 3^j below 2304 are 256,
512, 768, 1024, 1536 and 2048. For each, the smallest periodic forward-closed
set containing 11 (saturate in Γ_i) contains 8. So 2304 is the least modulus of
the form 2^i 3^j. Moduli with a prime factor ≥ 5 were not examined.

## Why tier 2, and why it matters

The proof is a congruence invariant plus a finite table (tier 2). Compared with
swT9_15_s8 (modulus 36, 21 classes), the same density of change to G needs a
certificate 64 times finer: modulus 2304 with 732 classes. Among swap sets with at most two pairs (a ≠ 0), only {9, 15}, {2, 8} and
{7, 10} are separable for i ≤ 12. The orbit of 8 under {7, 10} shows no fall in
20000 steps, so {9, 15} and {2, 8} are the only non-monotone ones (the
monotonicity of {7, 10} is evidence only). Among single swaps,
none is separable for i ≤ 12. So within the ±1-swap families this is the
frontier: two swapped pairs out of nine.

**Novelty:** new system; novelty not checked.
Check: `check_theorem5_precision3.py`, part (C).
