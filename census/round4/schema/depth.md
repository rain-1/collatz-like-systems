# Part A: certificate depth is unbounded in a designed base-2 family, with an exact formula

Lens "schema", round 4. Revised after REFEREE1 (corrections are marked in place).
Check: `check_depth.py` (exits 0, about 12 minutes, mostly the m = 10 formula and the
m = 8 decide.py depth run). Library:
`depthlib.py`. Search scripts, which are not proofs: `search_depth.py`, `best_member.py`.

Round 3 (`round3/dichotomy/deep.md`) conjectured that the least certificate depth k\* is
unbounded in natural families, and that the mechanism is cycle multipliers approaching 1.
Here the analogous statement is proved for an explicit designed family in base 2 with
multiplier 3. (The conjecture as stated in deep.md concerns the base-3 families B(3^k, 2)
and C(3^k), and it remains OPEN; see the correction after Theorem A2.) The family has an
exact formula for k\*, a matching integer witness, and a growth rate in terms of the
continued fraction of log₂3.

Notation follows `round3/dichotomy/dichotomy.md`: a table map at modulus Q,
n ≡ r (mod Q) ↦ (u_r n + v_r)/w_r, its residue graph G_T, and Theorem 3 there:
**k\* = Λ + 1**, where Λ is the length of the longest walk all of whose nonempty prefixes
have multiplier > 1. There are no translation nodes in this family, so the drift clause of
Theorem 3 never applies.

## The family D(m, word, h, i0)

Fix Q = 2^m. Choose a **loop word**, a cyclic word of length L in the letters
U = "multiply by 3" (u = 3, w = 1) and D = "halve" (u = 1, w = 2), with a ≥ 1 letters U and
b letters D, and lap multiplier λ = 3^a/2^b < 1. Choose a chain length h ≥ 0 and an
entry rotation i0. Use distinct residues in [2, Q/2):

* **loop residues** ℓ_0, …, ℓ_{L−1}. If letter i is U, the branch is
  n ↦ 3n + (ℓ_{i+1} − 3ℓ_i). If letter i is D, the branch is n ↦ (n + 2ℓ_{i+1} − ℓ_i)/2.
  In both cases T(ℓ_i) = ℓ_{i+1} exactly. A D node has the two successors ℓ_{i+1} and
  ℓ_{i+1} + Q/2.
* **chain residues** e_1, …, e_h with branch n ↦ 3n + (next − 3e_j). The next residue is
  e_{j+1}, and for e_h it is ℓ_{i0}.
* **every other residue r is a reset**, n ↦ (n + Q − r)/Q = ⌊n/Q⌋ + 1 (for r = 0 the
  branch is n ↦ n/Q). Its multiplier is 1/Q and it has Q successors. Residue 1 is a reset,
  so T(1) = 1.

(H1), (H2) and (P) hold, the multipliers are 3, 1/2 and 1/Q, and there is **no
translation node**. So the depth below does not come from translation chains, which
already give unbounded depth trivially (deep.md, part J). Let P_i(s) be the product of the
s letters of the loop word starting at position i (cyclically). Define

    G_exit = max{ G · P_i(s) : 1 ≤ s ≤ L, letter i+s−1 is D, and either G = 1 (any i)
                                or G = 3^j with 1 ≤ j ≤ h (i = i0) }.

This is the largest gain of a walk that starts at a loop or chain node and ends with a
halving step, which is the only kind of step that can lead into a reset.

## Theorem A1 (exact certificate and exact depth). PROVED

Let λ < 1.

1. **Certificate.** T has a descent certificate iff G_exit < Q.
2. **Cycles.** If G_exit < Q, every positive orbit is eventually periodic, and the
   complete cycle list is: the fixed point 1, and the L-cycle (ℓ_0 ℓ_1 … ℓ_{L−1}).
3. **Depth.** If G_exit < Q, then

       k* = max( h + t*(i0, 3^h),  max_i t*(i, 1) ),    t*(i, G) = min{ t ≥ 1 : G·P_i(t) < 1 },

   where P_i(t) is read along the periodic word: P_i(kL + s) = λ^k P_i(s). This gives
   t*(i, G) = min over s ∈ [1, L] of (k_s L + s), with k_s the least k ≥ 0 such that
   G P_i(s) λ^k < 1.

*Proof.* (1) A chain node has out-degree 1, and so does a U node. A D node has the
successors ℓ_{i+1} and its partner ℓ_{i+1} + Q/2 ∈ [Q/2, Q), which is a reset. Within
loop ∪ chain, each chain node e_j has only e_{j−1} as a predecessor, and e_1 has none.
So a cycle that avoids resets lies in the loop, and the only such cycle is the loop, with
multiplier λ < 1. Any other cycle passes through resets. Cut it at its reset nodes. Each
piece has the form ρ → x_1 → … → x_s → ρ′, with ρ, ρ′ resets and x_i loop or chain
nodes. If s = 0 the piece has multiplier 1/Q. If s ≥ 1, then x_s is a D node (only D
nodes have reset successors). The walk x_1 … x_s starts at a loop node, or at a chain node
and then runs through the rest of the chain into ℓ_{i0}. Walks longer than one lap only
lose a factor λ. So its product is ≤ G_exit, and the piece has multiplier ≤ G_exit/Q. If
G_exit < Q, every cycle contracts, and Theorem 1 of dichotomy.md gives a certificate.
Conversely, let x_1 … x_s attain G_exit. Its last node x_s has a reset successor ρ′, and
ρ′ → x_1 is an edge, because resets reach every residue. This closes a walk of multiplier
G_exit/Q. G_exit has the form 3^x 2^{−y} with y ≥ 0, so it is never equal to 2^m, and
G_exit ≥ Q means the closed walk expands. Lemma 3 of dichotomy.md then excludes any
certificate.

(2) GLOBAL follows from Theorem 2 of dichotomy.md. For the cycle list, write a loop-class
integer as ℓ_i + Qt and a chain-class integer as e_j + Qt. A chain step and a U step send
t to 3t. A D step sends t to t/2 if t is even. If t is odd, it moves to the partner reset
class, and the reset then gives (t+1)/2. Let n_min be the least element of a cycle.

* If n_min is in a reset class and n_min ≥ 2, then T(n_min) = ⌊n_min/Q⌋ + 1 < n_min,
  which is impossible.
* If n_min = ℓ_i + Q t_0 or e_j + Q t_0 with t_0 ≥ 1, the orbit cannot stay in
  loop ∪ chain forever. After k laps t is multiplied by λ^k, and t must stay a positive
  integer. So it exits through a D step at some odd t. The value after the reset is
  (t+1)/2 ≤ t_0 · G_exit + 1/2 < Q t_0 + 2 ≤ n_min, which is again impossible.

* If n_min = e_j is a chain residue itself (t_0 = 0; this case was missing before
  REFEREE1): along the chain t stays 0, so the orbit enters the loop at ℓ_{i0} with t = 0.
  With t = 0 every D step takes the even branch, so the orbit stays on the loop residues
  forever. No loop node has a chain node as successor, so the orbit never returns to e_j,
  and e_j is not on a cycle.

So n_min = 1, giving the fixed point, or n_min = ℓ_i with t_0 = 0, and then t stays 0 and
the cycle is the loop.

(3) A walk that starts at a reset descends at its first step. A walk that passes through a
reset has a prefix ending just after it, with multiplier ≤ G_exit/Q < 1. So non-descending
walks run through chain and loop nodes only, possibly ending at a reset; the last node's
multiplier does not count. Starting at e_j, the prefix products are 3, 9, …, 3^{h−j+1}, and
then 3^{h−j+1} P_{i0}(t). Starting at loop node i they are P_i(t). The longest such walk
from e_j has length (h − j + 1) + t*(i0, 3^{h−j+1}) − 1, which is largest for j = 1,
because t* is nondecreasing in G. From loop node i it has length t*(i, 1) − 1. Now apply
k\* = Λ + 1. ∎

**Check.** For 300 random members (random words, h, i0, m = 4..7) `decide.py`
independently gives CERT, the same k\*, and the same cycle list. For 40 random members
with G_exit ≥ Q it gives OBST. The integer witnesses below confirm the depth formula
directly.

## Theorem A2 (unbounded depth with near-critical loops). PROVED

Take the loop word to be the **Christoffel word** of slope a/L, with gcd(a, b) = 1. It is
balanced: any two factors of the same length differ by at most one in their number of U's
(standard; Lothaire, *Algebraic combinatorics on words*, ch. 2). So a factor of length s
has at most sa/L + 1 letters U, and its product is
6^{#U}/2^s ≤ 6 λ^{s/L} < 6. Take i0 to minimize S(i) − (i/L) log λ, where S is the
partial log-sum. Then P_{i0}(s) ≥ λ for 1 ≤ s ≤ L. Let h be largest with 6·3^h < 2^m
and L + h + 2 ≤ 2^{m−1}. Then G_exit < 6·3^h < Q, the member is CERT, and

    k* ≥ h + 1 + q·L,    q = max{ k : 3^h λ^k ≥ 1 } = ⌊h log 3 / |log λ|⌋.

(The first version stated the weaker h + 1 + L(q − 1). REFEREE1 noted that the proof gives
h + 1 + qL; both are true, and `check_depth.py` [A2] now tests the stronger one.)

*Proof.* 3^h λ^k P_{i0}(s) ≥ 3^h λ^{k+1} ≥ 1 for every k ≤ q − 1 and every s ∈ [1, L],
so no t = kL + s ≤ qL descends, t\*(i0, 3^h) ≥ qL + 1, and Theorem A1(3) gives
k\* ≥ h + qL + 1. ∎

Two infinite families follow.

* **Fixed loop, growing span.** Take (a, b) = (5, 8), λ = 243/256, |log λ| = 0.0521. Then
  k\* ≥ 13 (⌊21.08 h⌋ − 1), with h ≈ 0.63m. So k\* grows at least linearly in m. This is
  "depth from the span", like dch_C9_33.
* **Near-critical loops (a base-2 analogue of the round-3 conjecture; see the
  correction below).** Take the convergents p/q > log₂3 of
  the continued fraction log₂3 = [1; 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55, …], which
  are 2/1, 8/5, 65/41, 485/306, 24727/15601, …. Use (a, b) = (q, p), so
  λ = 3^q/2^p → 1, and |log λ| = log 2 · (p − q log₂3) < log 2/q′, with q′ the next
  convergent denominator. With m minimal such that the loop and the chain fit,
  Q ≤ 4(p + q + h + 2). Theorem A2 then gives

      k* ≥ (p+q) · (⌊h q′ log 3/log 2⌋ − 1) ≥ c · Q · log Q · q′ ≥ c′ · Q² log Q

  along this subsequence of moduli, using q′ ≥ q ≥ (p+q)/2.6.

**Correction (after REFEREE1): what A2 does and does not prove.** The conjecture in
round3/dichotomy/deep.md is "for the B(3^k, 2) and C(3^k) families, sup k\* → ∞". Those are
base-3 families. A2 proves the analogous statement for a designed base-2 family with
resets. That conjecture for B(3^k, 2) and C(3^k) remains **OPEN**. The first version of
this file and of the README called A2 "a proof of round 3's conjecture"; that was an
overclaim and is withdrawn. What A2 does answer is deep.md's narrower sentence "a proof
needs an explicit family of tables realising such cycles while keeping every other cycle
contracting. That is OPEN", in base 2. Unbounded depth as such is not new even within
this family: the fixed-loop (5, 8) family above already gives depth linear in m with no
translation nodes. The new content is the Diophantine Q² log Q growth along convergents.

## Theorem A3 (upper bound for every base-2, multiplier-3 table). PROVED

Let T be any CERT table map at Q = 2^m with u_r ∈ {1, 3} and w_r | Q. Let
q_k ≤ Q < q_{k+1} be consecutive convergent denominators of θ = log₂3, with partial
quotient a_{k+1}. Then

    k* ≤ Q + (Q−1) · Q · (log 3/log 2) · (q_k + q_{k+1}) ≤ Q + (log 3/log 2)(a_{k+1}+2) Q²(Q−1).

*Proof.* Theorem 3(c) of dichotomy.md gives k\* ≤ 1 + σ/|μ\*|. Removing closed subwalks
(each has total weight ≤ 0 for the weights log(u/w) − μ\*) leaves a simple path of at most
Q − 1 edges, each of weight ≤ log 3 + |μ\*|. So σ ≤ (Q−1)(log 3 + |μ\*|). The maximum
cycle mean is attained on a simple cycle C with multiplier 3^a/2^b, where a ≤ |C| ≤ Q.

* If 3^a/2^b ≤ 1/2, then |μ\*| ≥ log 2/Q.
* Otherwise b = ⌈aθ⌉ and |μ\*| ≥ log 2 · (⌈aθ⌉ − aθ)/Q ≥ log 2 · ‖aθ‖/Q. Here
  ‖aθ‖ > 1/(q_k + q_{k+1}) for 0 < a < q_{k+1} (best approximation property).

Combine the two cases. ∎

**Growth rate, compared with Diophantine bounds.** Along the convergent subsequence the
family gives k\* ≥ c Q² log Q. Every table in the class satisfies k\* = O(a_{k+1} Q³).
Baker's theorem gives log₂3 a finite effective irrationality measure μ, so for every
ε > 0, a_{k+1} = O_ε(q_k^{μ−2+ε}) and k\* = O_ε(Q^{μ+1+ε}): **depth is at most polynomial
in the modulus, and the exponent is controlled by how well log₂3 can be approximated.**
(The first version omitted the ε; fixed after REFEREE1. If one uses an effective measure
μ in the form |θ − p/q| ≥ c q^{−μ} for all q, as effective bounds are usually stated, the
ε can be dropped.) I did not look up the best published value of μ; REFEREE1 recalls
values around 5 to 8 (Rhin; Wu–Wang), also not verified. If the partial quotients of log₂3 were bounded (unknown),
the bound would be O(Q³). The gap between Q² log Q and Q³ is OPEN. A design whose gaining
path is entered only through long halving paths, rather than through a single reset, may
close it. I did not try this.

## Records (exact formula; witnesses where stated)

The deepest members found by (m = 11 with the 485/306 loop was started but not finished within the time limit, so it is omitted) `search_depth.py` / `best_member.py`. The search is not
exhaustive; the k\* values are exact for the stated tables.

| m | Q | loop (a, b) = 3^a/2^b | λ | i0 | h | k\* | how verified |
|---|---|---|---|---|---|---|---|
| 4 | 16 | (1, 2) | 0.75 | 2 | 2 | 26 | formula (Theorem A1) |
| 5 | 32 | (3, 5) | 0.84375 | 4 | 3 | 132 | formula |
| 6 | 64 | (5, 8) | 0.94922 | 11 | 4 | 791 | formula |
| 7 | 128 | (17, 27) | 0.96217 | 13 | 5 | 4335 | formula |
| 8 | 256 | (41, 65) | 0.98860 | 14 | 5 | **41362** | formula + integer witness |
| 9 | 512 | (94, 149) | 0.99067 | 16 | 6 | **133534** | formula + integer witness |
| 10 | 1024 | (147, 233) | 0.99274 | 17 | 6 | **304506** | formula; referee's own exact Λ and integer witness (REFEREE1 [R2], [R3]) |

(λ at m = 10 was misprinted as 0.99795 in the first version; the correct value is
3^147/2^233 = 0.99274. The k\* value is unaffected. `check_depth.py` [A3] now checks the
printed λ column to five decimals with exact arithmetic.)

**How each value is verified (corrected after REFEREE1).** A k\* value needs a lower bound
(a walk of length k\* − 1 whose prefixes all expand, shown by an integer witness or by the
walk itself) and an upper bound (Λ ≤ k\* − 1, which by Theorem 3(a) gives a certificate of
depth k\*).

* m = 4..8: decide.py's generic depth computation, which does not use Theorem A1, returns
  the same k\* (`check_depth.py` [A5], about 1 minute in total). So both bounds hold
  independently of A1.
* m = 7, 8, 9: integer witnesses by direct iteration ([A4]). These prove the lower bound
  only.
* m = 9, 10: my upper bound comes from the A1 formula. REFEREE1 [R2] computed Λ by an
  independent exact search over all walks, resets included, and got the same values, and
  REFEREE1 [R3] iterated its own integer witness at m = 10. So m = 10 is "exact; witness
  checked by the referee", not "formula only".

For comparison, the round-3 records were dch_C27_2466 (modulus 27, k\* = 2466) and
dch_S6_332 (modulus 64, base 2, k\* = 332). At modulus 64 this family reaches 791, and at
modulus 512 it reaches 133534, with an integer witness n of about 82 000 bits.
`check_depth.py` [A4] verifies T^i(n) ≥ n for every i < k\* and T^{k\*}(n) < n by direct
iteration for the m = 7, 8, 9 members. **Withdrawn sentence (REFEREE1):** the first
version said that these witnesses, "together with Theorem 3(a) of dichotomy.md, prove
those k\* independently of Theorem A1". That is wrong: a witness proves only k\* ≥ the
value. The upper bound needs Λ, and [A3] took it from the A1 formula. The independent
upper bounds are now [A5] (decide.py, m ≤ 8) and REFEREE1 [R2] (m ≤ 10), as listed above.

The comparison with dch_C27_2466 is across moduli and families (base 3, modulus 27,
against base 2 here). The like-for-like base-2 comparison is dch_S6_332 against 791, both
at modulus 64.

**Honest comparison.** deep.md says that depth records mean something only within a
family. This family is "base 2, multipliers 3 and 1/2, plus resets", with no translation
nodes. It is not the S-family (n/2 on every even n). The resets are what make the cycles
controllable. In the S-family, the halving nodes branch everywhere, and I did not find an
explicit family there. So the result is a base-2 analogue of the round-3 conjecture for
this designed class of tables. It is not a proof for the S-family, for B(3^k, 2), or for
C(3^k); those remain OPEN. The construction works
verbatim in base 3 (letters ×2, ×5 and ÷3, with ratios 2^x 5^y/3^z → 1); I did not run
it.

**Depth is not difficulty** (deep.md): every member also has a one-step weighted
potential. The point of Part A is the Diophantine law for k\*, not hardness.
