# Collatz-type maps on the Gaussian integers (division by π = 1 + i)

Checks: `check_gaussian.py` (G0–G5, about 10 s) and `check_gcert.py` (the certificate
census, about 3 min). Arithmetic is in `rings.py` (exact pairs (a, b) = a + bi) and
`gcert.py` (the norm-descent certificate engine).

**Natural setting.** π = 1 + i is the prime above 2, and Z[i]/π = F_2. Call z *odd* if
π ∤ z. A Collatz-type map divides by π on even z and applies u z + c on odd z, where u
is odd and c is odd, so u z + c is even again. The π-adic completion is Z_2[i]. Size is
measured by |z|, and |π| = √2.

## 1. Unit multipliers: GLOBAL is always yes (Theorem N′, PROVED)

For u ∈ {1, i, −1, −i} and any odd c, the blocks (u z + c)/π^k (k ≥ 1) form a
full-branch system (theorem_N.md) with |u/π^k| ≤ 2^{-1/2}. By Theorem N part 4,
**every orbit in Z[i] is eventually periodic.** The cycles are {0} plus the necklaces
with integral fixed point. Each nonzero cycle has an odd point with
|z| ≤ |c|/(√2 − 1). `rings.all_cycles` enumerates every odd z with N(z) ≤ 6N(c),
a superset of that disc, so its list is complete (check G3 and check_rings R2):

| map | cycles on Z[i] |
|---|---|
| z+1 (G1_1) | {0}, {−i, 1−i} |
| iz+1 (Gi_1) | {0}, {1, 1+i}, {−i, 2, 1−i} |
| −z+1 (Gm1_1) | **{0} only**: every Gaussian integer reaches 0 |
| −iz+1 (Gmi_1) | **{0} only** |

"Every orbit ends at 0" is a terminating-radix-expansion statement for base π with a
twisted digit rule: z = π·T-block(z) − (digit). It is of canonical-number-system type.
Results of this kind exist in the radix-representation literature, so this is
probably known, but novelty not checked.

## 2. Theorem G: the Gaussian 1x+c map (u = 1), PROVED

T_c(z) = z/π (π | z), z + c (π ∤ z), for c odd. Folding the odd step into the next
division gives V(z) = z/π or (z + c)/π, and **V(z) ≡ π^{-1} z (mod c)** (check G0). So
the orbit of z mod c under multiplication by π is invariant. V-cycles and T-cycles
correspond one to one.

*Theorem G. For every odd c ∈ Z[i]:*

1. *Every orbit is eventually periodic.*
2. *The residue class 0 mod c carries exactly two cycles: {0} and {−ic, (1−i)c}.*
3. *Every other orbit O of ×π on Z[i]/(c) carries **one or two** cycles, and every
   residue of O is visited by each of them. If O carries one cycle, every z with
   z mod c ∈ O reaches it.*

*Proof.* 1 is §1. For 2: on cZ[i], T_c(cw) = c·T_1(w). T_1 has exactly the cycles {0}
and {−i, 1−i} (window enumeration, check G0). That a cycle visits all of O follows
from V(z) ≡ π^{-1}z.

For 3, let C_1 ≠ C_2 be V-cycles in O. Pick z_1 ∈ C_1 and z_2 ∈ C_2 with
z_1 ≡ z_2 (mod c), and set q_n = (V^n z_1 − V^n z_2)/c ∈ Z[i]. Then
q_{n+1} = (q_n + e_1 − e_2)/π, where e_k ∈ {0, 1} is the parity of V^n z_k. Also
q_n ≠ 0 for every n, since otherwise the two cycles would meet. The sequence is
periodic and satisfies |q_{n+1}| ≤ (|q_n| + 1)/√2. At the maximum of |q| this gives
|q| ≤ 1/(√2 − 1) < √6, so N(q_n) ≤ 5.

Let Γ be the graph on {q : 1 ≤ N(q) ≤ 5} with edges q → (q + δ)/π, δ ∈ {−1, 0, 1}.
The sequence (q_n) is a closed walk in Γ. Check G1(a) computes that the nodes on closed
walks form the hexagon {−1, −1+i, i, 1, 1−i, −i}, with self-loops at ±i.

Now suppose three distinct cycles C_1, C_2, C_3 lie in O, aligned at a common residue.
Then (q_12, q_13) is a closed walk in the product graph whose states have q_12, q_13 and
q_13 − q_12 all in Γ. Each transition carries the parity triple (e_1, e_2, e_3). Check
G1(b) computes that the closed-walk part of this product graph consists of two 6-cycles
with **unique** transitions. Along each, the three parity words are rotations of 000111.
So z_1, z_2 and z_3 have π-adic V-itineraries that are shifts of one another. A point is
determined by its itinerary: V is the digit shift on −z/c, which has π-adic digits in
{0, 1}. So z_2 = V^s(z_1) for some s, hence C_1 = C_2. That is a contradiction, so O
carries at most two cycles. The last claim of 3 holds because orbits keep their residue
orbit and every orbit ends in a cycle. ∎

**Data (check G2).** Over the 95 odd c with |Re c|, |Im c| ≤ 9 and Im c ≥ 0, there are
398 nonzero ⟨π⟩-orbits, and 44 of them carry two cycles. For example, c = 3: Z[i]/3 = F_9
and π generates F_9^*, so all 8 units form one orbit, and it carries two 12-cycles. Two
cycles in one orbit need not have the same T-length; c = −9+8i has a pair of lengths 20
and 22.

**Theorem PG (congruence basins, PROVED, c a Gaussian prime).** Let f(z) be the cycle
reached by z ∉ cZ[i]. Say that f is periodic modulo a nonzero ideal (P) if f(z) = f(z′)
whenever z ≡ z′ (mod P) and z, z′ ∉ cZ[i]. (Unlike the case of Z, there is no
"ultimately" here, and intermediate translates may fall into cZ[i], so the hypothesis
is stated pointwise for pairs off cZ[i].) *f is periodic modulo some nonzero ideal iff
every ⟨π⟩-orbit on (Z[i]/c)^* carries exactly one cycle.*

*Proof.* This is the Theorem P argument (split_family.md) with 2 replaced by π. The
identities are f(πz) = f(z), and f(z) = f(z + c) for odd z. Suppose f is periodic
modulo P in the sense above, and write P = π^u m′ with π ∤ m′. Choose e ≥ u with π^e ≡ 1 (mod m′). Then f(z) is a
function h of z mod m′ on non-multiples of c, and it satisfies h(ρ) = h(ρ + c) and
h(πρ) = h(ρ). Here CRT supplies odd representatives that avoid cZ[i], which works because
z ∉ cZ[i] ⇔ z + c ∉ cZ[i]. The two invariances combine: for every j ≥ 0,
h(ρ) = h(π^j ρ) = h(π^j ρ + c) = h(ρ + π^{−j} c), where π^{−j} is the inverse of π^j
modulo m′ (π is a unit mod m′). So h is invariant under translation by every element of
c·Z[π, π^{−1}] = c·Z[i] modulo m′, that is, by the ideal (c, m′) modulo m′. (Translation
by c alone does not suffice: Z[i]/m′ is not cyclic as an additive group; for m′ = 3,
Z[i]/3 = F_9 while Z·c has order 3.) Since c is prime, g = gcd(m′, c) is 1 or c, and
(c, m′) is everything when g = 1 and (c) when g = c. If g = 1, h is invariant under all
translations, so f is constant off cZ[i]: at most one cycle on the units. If g = c, h factors through (Z[i]/c)^* and is constant on ⟨π⟩-orbits. Two cycles
in one orbit then contradict this. The converse is item 3 of Theorem G. ∎

So for c = 3 (a Gaussian prime) the basin of the two 12-cycles is **not** a congruence
rule. For c = 2+i (N = 5, π ≡ −1 mod c) each unit orbit {±1}, {±2} carries one cycle,
and the basin is the congruence rule.

## 3. Non-unit multipliers: a norm-descent certificate census (PROVED per system)

The Gaussian S-family: T_S(z) = z/π (π | z); (1+2i)z + 1 if z mod π^m ∈ S; z + 1 for
the other odd z. The multiplier 1+2i has norm 5. With S = all odd classes this is a
"Gaussian 5x+1" with positive drift (log 5 − 2 log 2 per block on average).

`gcert.certificate` builds the minimal norm-descent tree on classes z = π^K t + r,
t ∈ Z[i]. Along a node T^j(z) = P t + R exactly. The node closes when N(P) < 2^K. Then
|T^j z| < |z| outside a finite disc of t, and Lemma A (with |·| in place of n) gives
GLOBAL and the cycle list from the finite exceptional set E. `gcert.verify` re-checks
that the classes partition Z_2[i] (measure 1 and a prefix code), that every affine
form matches the true iterate at five values of t up to 10^12, and that N(P) < 2^K.
`gcert.exceptional` bounds |t| by exact integer arithmetic.

Obstruction (Gaussian Lemma B). The residue graph mod π^m has edges: odd r goes to
(u r + c) mod π^m, and even s goes to the two classes of s/π. A cycle in it has a
π-adic periodic point with the same multiplier (Lemma D: the cylinder maps onto its
starting class). If |multiplier| > 1, the round-2 Lemma B argument applies verbatim
with |·| = complex absolute value, and no certificate exists for any modulus or depth.
`gcert.verify_obstruction` recomputes the fixed point exactly in Q(i), follows its true
π-adic orbit, and checks the multiplier and the cycle-lemma partial products.

**Census.** Every S is classified exactly, with no unknown cases:

| m | odd classes | subsets | CERT | OBST | largest certifiable S | deepest certificate (k, K) |
|---|---|---|---|---|---|---|
| 3 | 4 | 16 | 3 | 13 | 1 | (5, 3) |
| 4 | 8 | 256 | 18 | 238 | 3 | (10, 7) |
| 5 | 16 | 65536 | 2277 | 63259 | 9 | (63, 44) |

m = 3 and 4 are re-run in check_gcert.py. The m = 5 row is from census_gauss.py
(about 5 minutes; output in scratch/gscan_m5.out). Obstructions are verified there
exactly, but certificates are only built, not re-verified, except for the systems below
and a 400-subset sample in the check. The certifiable density is 3.5% at m = 5, against
25% for the 2-adic 3x+1/x+1 S-family (round 2): a norm-5 multiplier is far more
expensive than 3. Four systems are settled completely (PROVED):

* **GS5_deep** (m = 5, S = 5 of the 16 odd classes, see systems.py): a certificate with
  965 leaves, K = 44 and k = 63 steps. |E| = 26. **Every orbit reaches 0. The only
  cycle is {0}.**
* **GS5_max** (m = 5, |S| = 7): a certificate with 666 leaves, K = 37 and k = 52.
  **Cycles {0} and {−i, 1−i}.**
* **GS5_9** (m = 5, |S| = 9, the maximum possible at m = 5): a certificate with 92
  leaves, K = 23 and k = 30. |E| = 181. **Cycles {0} and one 18-cycle through
  −2−2i, i, 6, 4−4i, …**
* **GS4_max** (m = 4, |S| = 3): 12 leaves, k = 10. Cycles {0} and {−i, 1−i}.

These are tier 2 in the census sense (a certificate plus a finite table). As in the
2-adic S-family, the depth comes from near-critical π-adic cycles.

## 4. Where GLOBAL fails or is out of reach

* **Gaussian 5x+1** (u = 1+2i on every odd class, G5_1): OPEN. There is a fixed point
  z = i: (1+2i)i + 1 = −1 + i = π·i. Its multiplier is |1+2i|/|π| = √(5/2) > 1, so by
  Lemma B no descent certificate exists (exact, check G4). Seeds 1 and 3 reach |z|^2 of
  about 2^1970 after 2·10^4 steps (EVIDENCE of divergence). This is the Gaussian
  counterpart of 5x+1 and presumably just as hard.
* **The naive lift** z/2 if 2 | z, else z + 1 (dividing by the rational prime 2 instead
  of π): GLOBAL **fails, PROVED.** If Im z is odd, z is never divisible by 2, so the
  orbit is z, z+1, z+2, …, which is infinite (check G5). The trivial mechanism is the
  point. The 1x+1 map is tame on Z, and its lift is tame with the prime π but not with
  2, because Z[i]/2 has the non-unit, nonzero classes i and 1+i, which the "+1" rule
  never clears.
* **Negative finding.** For the full-branch maps of §1–3 an orbit can never be proved
  divergent by a congruence trap. Suppose an orbit followed a periodic itinerary
  forever. It would equal the unique π-adic periodic point of that word (Theorem N,
  part 1), and if that point is in Z[i] the orbit is periodic. Any divergent orbit
  therefore has an aperiodic itinerary, the same situation as for 5x+1 on Z.

Novelty: I did not search the literature on Gaussian-integer Collatz variants, so
novelty not checked. Theorem G and the certificate census are, to my knowledge, not
in print.
