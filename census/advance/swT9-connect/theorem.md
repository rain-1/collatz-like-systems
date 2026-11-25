# swT9-connect: CLS-055 (swT9_s8) has no congruence trap at any modulus

**Status: PROVED.** This is an obstruction result. It does **not** settle the fate of 8 (return or infinite); that stays OPEN.

## Setting

T is the 1932 permutation: 3q -> 2q, 3q+1 -> 4q+1, 3q+2 -> 4q+3. sigma swaps the classes 9 and 10 (mod 18), and Q = sigma o T.

For K >= 1, G_K is the residue graph mod K. It has an edge x -> y iff some integer n >= 1 with n ≡ x (mod K) has Q(n) ≡ y (mod K).

## Theorem

For **every** K >= 1, G_K is strongly connected. Equivalently, no nonempty proper union D of residue classes mod any K satisfies Q(D) ⊆ D. As a consequence:

- no congruence trap exists at any modulus;
- no congruence separator for the seed 8 exists at any modulus, meaning no union of classes that contains Q(8) and is Q-closed but omits 8;
- no union of classes is closed under Q^{-1} either (its complement would be a Q-trap, since Q is a bijection of Z_{>0}).

So the congruence-trap route (tier 2) for the fate of 8 is closed completely. Earlier work proved this only for 3 ∤ K, and computed it for K <= 1200 and for K = 2^a 3^b <= 3e5. See `census/lhf/perm-near/CLS-055.md` for Lemma 0 (strongly connected implies no trap).

## Finite facts (verified by `check.py`)

**F1 (pieces).** For n ≡ r (mod 27), Q(n) = (α_r n + β_r)/3. These are T's pieces, (α, β) = (2, 0), (4, −1), (4, 1) for r ≡ 0, 1, 2 (mod 3), except for three classes:

| r | Q(n) |
|---|---|
| 15 | (2n − 3)/3 |
| 7 | (4n + 2)/3 |
| 20 | (4n + 4)/3 |

*Proof.* Write n = 27t + r. Then T(n) = T(r̃) + 18t (r ≡ 0 mod 3) or T(r̃) + 36t (otherwise), where r̃ is the positive representative of r. So T(n) mod 18 depends only on r, and Q(n) = T(n) + δ_r with δ_r ∈ {0, ±1} constant on the class. The values of T(r̃) mod 18 are T(15) = 10, T(7) = 9 and T(20) = 27 ≡ 9, and no other r gives 9 or 10. This is checked directly, and also on 1 <= n <= 3e5. ∎

In particular α_r ∈ {2, 4}, and for n ≡ n' (mod 27) we have **Q(n) − Q(n') = (α_r/3)(n − n').** (∗)

**F2.** Let H be the graph on Z/27 with r -> r' iff r' ≡ Q(r̃) (mod 9). Then H is strongly connected.

**F3 (2-adic covering).** For every class c mod 9, let the in-neighbours be the r with Q(r̃) ≡ c (mod 9). Their 2-adic image cosets β_r/3 + α_r Z_2 cover Z_2.

For example, for c = 0 the in-neighbours are r = 0, with image 2Z_2, and r = 15, with image −1 + 2Z_2. For c = 1 they are r = 1, 7, 14, 20, with images 1, 2, 3, 0 + 4Z_2. This is forced by the bijectivity of Q, but `check.py` simply verifies it mod 4 for all 9 classes.

**F4.** H contains the closed walks W1 = 0 -> 0 -> 0 -> 0 and W2 = 0 -> 9 -> 15 -> 0. Their composite maps are u ↦ 8u/27 and u ↦ (8u − 27)/27.

## Proof

### Lemma 1 (edges for 27 | K)

Let K = 3^b L with b >= 3 and 3 ∤ L. Let x be a residue mod K and x̃ its least positive representative. Then x -> y in G_K iff y ≡ Q(x̃) (mod 3^{b−1} L).

*Proof.* The integers n >= 1 with n ≡ x are n = x̃ + 3^b L s with s >= 0. Since 27 | K, all of them lie in one class mod 27. By (∗), Q(n) = Q(x̃) + α 3^{b−1} L s with α ∈ {2, 4}. Since α L is a unit mod 3, the values s = 0, 1, 2 already give all three residues mod K that are ≡ Q(x̃) (mod 3^{b−1}L), and no other residues occur. ∎

For b = 3 and L = 2^a m, this says that G_{27L} is the graph on pairs (r, u) ∈ Z/27 × Z/L, where n ≡ r (mod 27) and n ≡ u (mod L). Its edges are (r, u) -> (r', f_r(u)) for r -> r' in H, where f_r(u) = (α_r u + β_r)/3 mod L. Here 3 is invertible mod L. A walk in G_{27L} is therefore a walk r_0 -> … -> r_N in H, with u updated by the composite g_W = f_{r_{N−1}} ∘ … ∘ f_{r_0}. As a map over Z[1/3], g_W(u) = (2^e u + B)/3^N.

### Lemma 2 (G_{27L} is strongly connected for every L with 3 ∤ L)

Write L = 2^a m with gcd(m, 6) = 1. Fix a start (r_0, u_0) and a target (r', y).

*(i) 2-adic steering.* Claim: for every vertex r' of H and every y mod 2^a, there is a walk W in H ending at r' such that g_W(z) ≡ y (mod 2^a) for every z.

The proof is by induction on a, and a = 0 is the trivial walk. For a >= 1, F3 gives an in-neighbour r of r' with y ∈ β_r/3 + α_r Z_2. Let v = v_2(α_r) ∈ {1, 2}. Then y ≡ f_r(y') for some y', determined mod 2^{a−v}. If a − v >= 0, take W' from the induction for (r, y' mod 2^{a−v}) and put W = W' then r -> r'. This gives g_W(z) = f_r(y' + 2^{a−v} s) = y + 2^a s/3 ≡ y. If a = 1 and v = 2, then f_r(z) ≡ β_r/3 ≡ y (mod 2) for every z already.

*(ii) Transitivity mod m.* Every f_r is a permutation of Z/m, because 2/3 and 4/3 are units. Let Γ be the set of maps g_C on Z/m, for C a closed walk of H at 0. Γ is a finite semigroup of permutations, so it is a group, and every element of Γ is realised by a closed walk. Let k be the order of g_{W1}. Then W1^{k−1} followed by W2 realises

g_{W2} ∘ g_{W1}^{−1}(u) = (8 · (27u/8) − 27)/27 = u − 1,

by F4. So Γ contains the translation u ↦ u − 1 and is transitive on Z/m.

Now fix any vertices r_0 and t of H and a residue u_0. Take walks A1: r_0 -> 0 and A2: 0 -> t, which exist by F2. Then {g_A(u_0) : A a walk r_0 -> t} ⊇ g_{A2}(Γ · g_{A1}(u_0)) = Z/m.

*(iii) Combine.* Take W from (i) for (r', y mod 2^a), and let t be its first vertex. Since g_W is a permutation of Z/m, (ii) gives a walk A from r_0 to t with g_A(u_0) ≡ g_W^{−1}(y) (mod m). The walk A·W runs from r_0 to r' in H. Its map sends u_0 to g_W(g_A(u_0)), which is ≡ y (mod 2^a) by (i) and ≡ y (mod m) by the choice of A. By CRT it is ≡ y (mod L). By Lemma 1 (b = 3), A·W is a walk in G_{27L} from (r_0, u_0) to (r', y). ∎

### Lemma 3 (lifting from 27L to 3^b L)

Let b >= 3 and 3 ∤ L. If G_{27L} is strongly connected, then so is G_{3^b L}.

*Proof.* Put K = 3^b L, and for v mod 27L let F(v) ⊂ Z/K be its fibre, the 3^{b−3} residues ≡ v (mod 27L).

*(a) Spreading.* Fix x mod K. For 0 <= k <= b−3, let S_k = {z mod K : z ≡ Q^k(x̃) (mod 3^{b−k} L)}. We show by induction that every element of S_k is reachable from x. S_0 = {x}. For the step from k to k+1 (so b − k >= 4), take z ∈ S_{k+1} and write z − Q^{k+1}(x̃) ≡ 3^{b−k−1} L δ (mod K). For j >= 0, put w̃ = Q^k(x̃) + 3^{b−k} L j. This number is ≡ Q^k(x̃) (mod 27), so (∗) gives Q(w̃) = Q^{k+1}(x̃) + α 3^{b−k−1} L j. Choose j with α j ≡ δ (mod 3^k), which is possible since α is a unit mod 3. Then Q(w̃) ≡ z (mod 3^{b−1} L), so w̃ mod K -> z is an edge by Lemma 1, and w̃ mod K ∈ S_k. Hence S_{b−3} = F(v_0) with v_0 = Q^{b−3}(x̃) mod 27L, and all of it is reachable from x.

*(b) Fibre lifting.* Suppose v -> v' is an edge of G_{27L}, so v' ≡ Q(ṽ) (mod 9L) by Lemma 1. Then every z' ∈ F(v') has a G_K-predecessor in F(v). Indeed, z' − Q(ṽ) = 9Lδ, so take w̃ = ṽ + 27 L j with α j ≡ δ (mod 3^{b−3}). By (∗), Q(w̃) = Q(ṽ) + 9αLj ≡ z' (mod 3^{b−1}L), and Lemma 1 gives the edge.

Given any target y mod K, take a path v_0 -> v_1 -> … -> v_M = y mod 27L in G_{27L}. By (b) and induction, every element of F(v_i) is reachable from x, and in particular y ∈ F(v_M) is. ∎

### Conclusion

Let K be arbitrary and write K = 3^b L with 3 ∤ L. Put K' = 3^{max(b,3)} L. G_{K'} is strongly connected by Lemmas 2 and 3. Reduction mod K maps the edges of G_{K'} to edges of G_K, since the same witness n works, and it is onto the vertices. So G_K is strongly connected. ∎

## Remarks

- The proof is fully general. The only computation is the 27-vertex finite facts F1–F4, and F1, F3 and F4 are also checked by hand above. Nothing depends on the earlier computed range.
- Lemma 3 holds for any map that is affine on classes mod 27 with slopes in {2/3, 4/3}. Lemma 2 is where the specific map enters: through F2, F3 (bijectivity) and the translation W2 ∘ W1^{−1}, which is created by the sigma-altered piece at r = 15.
- **What this does not do.** It says nothing about whether 8 returns. It only shows that tier-2 certificates (unions of residue classes) cannot decide it, or prove any Q-orbit infinite. Other routes are untouched: DFA/automatic certificates beyond the sizes excluded in CLS-055.md, and non-congruence invariants.

## Verification

Run `python3 census/advance/swT9-connect/check.py`. It takes under 1 s and exits 0. It checks:

- F1, on 1 <= n <= 3e5 plus the class-constancy of T mod 18;
- F2;
- F3, mod 4 for all 9 classes;
- F4, the composite maps of W1 and W2.

It also runs two sanity checks that the proof does not need:

- G_K, built from actual integers n <= 81K (a subgraph, so a valid check), is strongly connected for 16 moduli divisible by 81, among them 729, 2187, 2430, 5103 and 1296;
- the constructive algorithm of Lemma 2 is executed for 280 random (start, target) pairs over several L = 2^a m, and the walk it produces lands on the target.

## Referee (round 1)

**Verdict: CONFIRMED (PROVED).** No literature constants are involved. The finite part is fully checked by machine and the reduction is valid for every K.

**What I re-derived by hand**
- **F1.** For n = 27t + r, T(n) = T(r̃) + 18t (r ≡ 0 mod 3) or + 36t (otherwise). So T(n) mod 18 depends only on r, and the sigma correction δ_r is constant on each class mod 27. The exceptional classes are exactly 7, 15 and 20.
- **Lemma 1.** With n = x̃ + Ks, Q(n) = Q(x̃) + α 3^{b−1} L s, and αL is a unit mod 3. So the edge set is exactly {y ≡ Q(x̃) mod 3^{b−1}L}. Each residue is reached with s ∈ {0, 1, 2}, and no other residues occur.
- **(r, u)-model of G_{27L}.** The condition on r' is Q(x̃) ≡ Q(r̃) mod 9, which holds because 27 | x̃ − r̃ and the slope is in {2/3, 4/3}. The u-coordinate is f_r(u) mod L. CRT makes the two conditions independent.
- **Lemma 2(i).** The induction is correct, including the cases a = 1 with v = 1 (W' is trivial) and a = 1 with v = 2 (constant mod 2). The text's "y + 2^a s/3" is exact because α = 2^v.
- **Lemma 2(ii).** Concatenating closed walks gives a semigroup, and a finite semigroup of permutations is a group. W1^{k−1}·W2 has map g_{W2} ∘ g_{W1}^{−1} = u − 1, and this holds for k = 1 too. The edges 0→9 (Q(27) = 18), 9→15 (Q(9) = 6) and 15→0 (Q(15) = σ(10) = 9) all exist.
- **Lemma 2(iii)** is correct.
- **Lemma 3(a), spreading.** The step from k to k+1 needs 27 | 3^{b−k}L, which holds because k ≤ b−4. j is chosen mod 3^k, w̃ is positive and lies in S_k, and Lemma 1 applies to w̃ mod K because Q of any positive member of the class agrees mod 3^{b−1}L. After the last step, S_{b−3} = F(v_0).
- **Lemma 3(b), fibre lifting.** The calculation 9L(δ − αj) ≡ 0 mod 3^{b−1}L ⟺ αj ≡ δ mod 3^{b−3} is correct.
- **Conclusion.** G_K is a vertex-surjective homomorphic image of G_{K'} (same witness n), so it is strongly connected.
- **Corollaries.** For "no closed union", a closed D that contains a class must contain every class reached by an edge. For Q^{-1}-closed unions, the complement argument uses the fact that T and σ are both bijections of Z_{>0}, which I checked. The separator statement is a special case.

**Independent computation** (my own code, using the map from `census/round2/downfrom5/systems.py`, `get("swT9_s8")`, with no reuse of `check.py`)
- Affine on classes mod 27 with slope in {2/3, 4/3}: checked on 27 × 200 random n up to about 1e31. The pieces derived from the integers are exactly F1.
- The Lemma 1 edge set equals the brute-force edge set (s = 0..11) for K = 27, 54, 81, 135, 243, 324, 729 and 945.
- The integer-realised subgraph of G_K is strongly connected:
  - for every K ≤ 600 (using n ≤ 4K + 27);
  - for K = 3^8, 3^9, 3^10, 2^6·3^5, 3^4·35, 3^6·13, 2·3^7 and 2·11·3^5.
- F3 holds mod 16, and F4 was checked in exact rational arithmetic.
- `check.py` was re-run: exit 0.

**Gaps:** none affecting validity. Minor points:
1. The remark in F3 that F3 is "forced by bijectivity" is a heuristic. It is not used, because F3 is verified directly.
2. `check.py`'s "F1 symbolic" line only samples t = 0..2. The all-t statement rests on the hand argument above, which is correct.
3. `check.py` contains an unused helper, `qmod9`.

**Scope** (agreeing with the author): this only rules out congruence-class (tier-2) certificates at every modulus. The fate of 8 remains OPEN.
