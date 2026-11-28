# The missing theorem: integers are generic beyond their own digits (27 Nov 2026)

Status: CONJECTURE with strong numerical support. Round 5 (`../../round5/README.md`) proved a small
part of it for 3x+1 (a few digits beyond the horizon) and disproved its polynomial analogue.
For the integer family 3x+d, a subsequent [actual-height count theorem](../../round5/microrange/actual_counts.md) covers arbitrary interval lengths and locations in almost every dyadic size range, to a depth of log X plus order log log X.
Data: `survive.c` (exact 128-bit integer arithmetic), `analyse.py`, outputs `s53.txt`, `c31.txt`,
`k7.txt`, `c3m1.txt`, `c3p5.txt`.

## Setting

T is a unit-multiplier table map T(n) = (u n + v)/p^e on classes mod p^m with negative drift.
sigma(n) = the number of divisions by p ("halvings") performed before the orbit of n first goes
below n (infinite if it never does). P(b) = the Haar measure of the set of p-adic integers that
have not gone below themselves (in the slope sense) after b halvings; P(b) = p^{-(1-h) b + o(b)},
where h is the Hausdorff dimension of the non-descending set Omega (round 3).

Use N(X, b) = #{1 <= n <= X : sigma(n) > b} for starts surviving through step b. The earlier
display used sigma(n) >= b, which instead pairs with P(b-1). In the shortcut 3x+d family
the coefficient test through b steps depends only on n mod 2^b, giving exact Haar counts on
whole periods. The comparison with actual heights requires a separate argument.
For b > log_p X the residue of n mod p^b is n itself followed by zeros, and nothing is known.

## Conjecture E (count law beyond the horizon)

For every K there is a function eps(X) -> 0 such that for all X and all b <= K log_p X,

    | N(X, b) - X P(b) |  <=  eps(X) X P(b) + #(Exc ∩ [1, X]) + eps(X) ,

where Exc is the finite set of starts that never go below themselves (they end in a cycle
whose minimum is at least the start), and N counts actual drops (sigma as defined above).

*(Corrected 27 Nov 2026 after round 5, `../../round5/fourier`: the first version had the additive
error X^{eps(X)}. With that error term the consequences below do NOT follow, because it allows
up to X^{eps} exceptional starts at every depth. The form above, called E_0 in round 5, is the one
that implies them. The numerical evidence below does not distinguish the two forms.)*

In words: among the starts up to X, the number still not dropped after b halvings is what a
random continuation of the digits would give, at every depth up to any fixed multiple of the
horizon. Equivalently: for the integers n < p^m that survive m halvings, the value reached after
those m halvings is distributed, with respect to further survival, like a Haar-random p-adic
integer.

## Consequences

* **E => bounded stopping constant:** sigma(n) <= (C* + eps) log_p n for all but finitely many n,
  with C* = 1/(1 - h). In particular every large n drops below itself, which is GLOBAL for T.
* **E => sharpness:** sigma(n) >= (C* - eps) log_p n for infinitely many n.
* **Minimal form M** (all that GLOBAL needs): there is C with sigma(n) <= C log n for all large n.
  Even M is as strong as the open problems (for 3x+1 it implies the Collatz conjecture).

For split5_3, at most two actual survivors in $[2^m,2^{m+1})$ after $\lceil 2.4m\rceil$ halvings for infinitely many $m$ would already imply eventual periodicity. The implication follows from the spacing of successive tail minima. Proving the upper bound remains open. [Proof, Theorem 1 and its local test](../../../output/pdf/stopping_time_applications.pdf)

## Generalisation G (rational starts, i.e. the sibling systems)

For every fixed odd d, the same count law holds for the starts n/d (positive or negative n),
with the same P(b). The exceptions are finitely many: the starts whose orbit ends in a cycle
without ever going below the start. (n/d under 3x+1 is n under 3x+d; negative n is 3x-1.)

## Equivalent arithmetic form (the S-unit sum)

After the m halvings that use up its digits, a surviving n < p^m sits at
beta = (u^a n + c)/p^m, where c = sum_j v_j u^{a - a_j} p^{e_j} has one term per step. E says
that the low digits of beta are generic. In the 2,5 case and on a cylinder of the last j digits,
those digits are the MIDDLE binary digits of 5^A s + B for s < 2^j: bits j to 2j-1 of a product
of a j-bit number with a large power of 5. So E is a statement about the middle digits of
u^A s, uniformly in A, where A grows with the number of steps.

## Evidence

Observed N versus predicted 2^m P(b), for octaves [2^m, 2^{m+1}) and depths b beyond the horizon
(b > m). P(b) is measured in the top octave, where b is inside the horizon. Only cells with
expected count at least 5 are used; chi2/cell near 1 or below means the deviations are at the
level of counting noise.

| system | starts | b/m range | cells | observed | expected | ratio | chi2/cell |
|---|---|---|---|---|---|---|---|
| 3x+1 | n < 2^34 | 1.00-1.25 | 86 | 138,702,577 | 138,702,313.5 | 1.0000 | 0.04 |
| | | 1.25-1.50 | 62 | 3,126,955 | 3,126,885.3 | 1.0000 | 0.20 |
| | | 1.50-1.75 | 45 | 194,888 | 195,161.6 | 0.9986 | 0.33 |
| | | 1.75-2.00 | 26 | 17,612 | 17,642.4 | 0.9983 | 0.25 |
| | | 2.00-2.25 | 23 | 4,503 | 4,543.1 | 0.9912 | 0.10 |
| | | 2.25-2.50 | 13 | 914 | 939.0 | 0.9733 | 0.09 |
| | | 2.50-3.00 | 20 | 509 | 528.7 | 0.963 | 0.26 |
| split5_3 | n < 2^36 | 1.00-1.25 | 86 | 41,632 | 41,680.8 | 0.9988 | 0.46 |
| | | 1.25-1.50 | 36 | 869 | 834.3 | 1.0416 | 0.92 |
| K7 | z < 2^34 | 1.00-1.25 | 86 | 836,267 | 836,223.6 | 1.0001 | 0.11 |
| | | 1.25-1.50 | 60 | 19,453 | 19,605.3 | 0.9922 | 0.77 |
| | | 1.50-1.75 | 36 | 1,382 | 1,270.3 | 1.0879 | 1.78 |
| | | 1.75-2.00 | 11 | 94 | 93.2 | 1.0082 | 0.99 |
| 3x-1 (G, negative n), against the 3x+1 P(b) | n < 2^28 | 1.0-1.5 | 123 | 17,871,534 | 17,871,721.5 | 1.0000 | 0.13 |
| | | 1.5-2.0 | 60 | 89,032 | 88,576.0 | 1.0051 | 0.37 |
| | | 2.0-2.5 | 29 | 3,079 | 3,025.3 | 1.0178 | 0.68 |
| | | 2.5-3.2 | 13 | 245 | 302.0 | 0.811 | 1.08 |
| 3x+5 (G, d = 5), against the 3x+1 P(b) | n < 2^28 | 1.0-1.5 | 123 | 17,871,243 | 17,871,721.5 | 1.0000 | 0.19 |
| | | 1.5-2.0 | 60 | 88,940 | 88,576.0 | 1.0041 | 0.46 |
| | | 2.0-2.5 | 29 | 2,962 | 3,025.3 | 0.979 | 1.34 |
| | | 2.5-3.2 | 13 | 258 | 302.0 | 0.854 | 0.56 |

Further checks: the decay rate of P(b) for split5_3 near b = 35 is 2^{-0.4165 b}; 1 - h = 0.4193.
No start in [64, 2^32) of 3x+1 survives 600 halvings. For 3x-1 none in [64, 2^28) does; for 3x+5
exactly five do (123, 171, 187, 259, 347), all ending in the cycles with minima 187 and 347, as
G allows. Largest sigma(n)/log2 n seen: split5_3 about 2.07 (C* = 2.385); K7 about 3.0.

Limits of the test: the comparison needs P(b), which is measured only up to b = 33 to 35, so the
tested depths reach three times the horizon for small octaves and 1.5 times for large ones. Cells
near the critical ratio C* have expected counts below 1 and cannot be tested by counting. The
slight deficit in the last 3x+1 and sibling rows is within noise (chi2 below 1.4) but is noted.
