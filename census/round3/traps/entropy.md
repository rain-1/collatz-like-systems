# Theorem E: how many integers can avoid a trap? (density bounds on the H frontier)

Status: **PROVED**. The exponent certificates are checked exactly in `check.py` [6]
(`entropy.py`, plus the λ < 2 certificates for all 130 maximal H sets). This generalises Theorem 2 of census/lhf/traps/CLS-056.md and CLS-066.md. Those
results are the special cases A = {5,7} and A = {7} mod 8 for 3x+1, and entropy.py reproduces
their exponents log2(plastic) = 0.40569 and log2(tribonacci) = 0.87915. I have not checked
novelty.

## Statement

Let T = T_{a,b} be the shortcut map: n/2 for even n, (a n + b)/2 for odd n, with a and b odd.
Let A be a set of residues mod 2^k, and let M be the adjacency matrix of the avoider graph
G_k^A(T). Here every node r has the two lifts of T(r) as out-edges, and nodes in A are deleted.

Suppose λ > 0 is rational and v is a positive rational vector with M v ≤ λ v. Then for every
X ≥ 2^k,

    #{1 ≤ n ≤ X : T^i(n) mod 2^k ∉ A for all i ≥ 0} ≤ 2 (Σv / min v) λ^{⌊log2 X⌋ − k}  =  O(X^{log2 λ}).

If A consists of odd residues, the T-orbit and the C_{a,b}-orbit of n contain the same odd
numbers. So the same bound counts the n whose C_{a,b}-orbit avoids A.

For arbitrary A (including sets with even residues, such as F*), the T_{a,b}-orbit of n is a
subsequence of the C_{a,b}-orbit, since T(n) = C(C(n)) for odd n and T(n) = C(n) for even n. So
an n whose C_{a,b}-orbit avoids A also has a T-orbit that avoids A, and the bound above still
counts the C_{a,b}-avoiders. The exponent is < 1 only when λ < 2; `check.py` [6] certifies
λ < 2 exactly (rational M v ≤ λ v) for all 130 maximal H sets of the nine censuses, including
the mod-8 and mod-16 sets with even residues (for F*, the exponent is 0.4057).

## Proof

1. **Terras bijection.** For a and b odd, n mod 2^L ↦ (T^i(n) mod 2)_{i<L} is a bijection onto
   {0,1}^L. This is the standard induction:
   T^i(n + 2^L t) = T^i(n) + a^{#odd} 2^{L−i} t.
2. **Residue walks.** Consider Ψ: n mod 2^L ↦ (T^i(n) mod 2^k)_{0≤i≤L−k}. It is well defined,
   because T^i(n) mod 2^{L−i} depends only on n mod 2^L, and L − i ≥ k.
3. **Ψ is injective.** Its entries give the parities v_0, …, v_{L−k}. The last entry
   T^{L−k}(n) mod 2^k gives v_{L−k}, …, v_{L−1} by Terras at length k. So Ψ determines the parity
   vector, and hence n.
4. **Ψ is onto the walks.** Ψ(n) is a walk of length L − k in the full graph G_k. That graph has
   exactly 2^k · 2^{L−k} = 2^L walks of length L − k, since every node has out-degree 2. So Ψ is a
   bijection onto walks. (check.py confirms the count by brute force for L ≤ k + 7.)
5. **Counting avoiders.** The classes mod 2^L whose first L − k + 1 iterates avoid A correspond
   to the walks of length L − k in G_k^A. There are 1ᵀ M^{L−k} 1 ≤ (Σv / min v) λ^{L−k} of them.
6. **Counting integers.** Take L = ⌊log2 X⌋. Each class mod 2^L has at most two members in
   [1, X]. ∎

## Results on the frontier (maximal H sets, odd residues mod 32)

By theory.md, these statements are exactly the ones where every SCC/descent certificate mod 2^m
fails (H). For each one, Theorem E bounds the possible counterexamples. Full lists are in
`results/entropy_frontier.json`.

| map | frontier sets | smallest exponent | largest exponent |
|---|---|---|---|
| 3x+1 | 35 | 0.2232 ({1,3,5,11,13,17,19,21,23,25,29,31}) | 0.6125 ({1,5,7,9,11,13,17,19,25,27,29}) |
| 5x+1 | 36 | 0.1542 | 0.5760 |
| 7x+1 | 25 | 0.1542 | 0.5754 |

So for every 3x+1 frontier statement S(A) mod 32, all but O(X^0.613) integers n ≤ X satisfy it,
and this comes with a proof. For 5x+1 and 7x+1, the integers ≤ X whose orbits avoid the frontier
set number O(X^0.576), by proof. Whether any of them avoids it forever (for example a divergent
5x+1 orbit) is OPEN.
