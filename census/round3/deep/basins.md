# Basins of the certifiable split maps

The certifiable members of SPLIT(a,b,d) (class C of family.md, plus a = b = 1) all satisfy GLOBAL
with every cycle meeting [1, d]. The sharp remaining question for each of them is **BASIN: which
cycle does each start reach?** This note answers it for two infinite families.

* X_d = SPLIT(1,1,d) (odd n -> n + d), every odd d: Theorem B1, complete and explicit.
* Sigma_d (odd n -> whichever of n + d, 3n + d is divisible by 4) for every d with gcd(d,6) = 1.
  Sigma_d = SPLIT(3,1,d) = split_d when d = 1 (mod 4) and SPLIT(1,3,d) = splitB_d when d = 3
  (mod 4). Theorems B2-B4: the basin of a cycle is a congruence class union **exactly when** no
  other cycle shares its invariant class modulo d; otherwise it is not ultimately periodic on any
  progression and is not automatic in any integer base.

| system | question | answer | status | tier |
|---|---|---|---|---|
| X_d, every odd d | BASIN and cycle list | cycles <-> cosets of <2> in Z/d; basin of n = coset of n mod d; cycle of coset K = (integers of [1,d] in K) together with r + d for each odd such r | PROVED | 1 |
| Sigma_d, gcd(d,6)=1 | BASIN | basin of C = {n : n mod d in I(C)} iff C is the only cycle in its <2,3>-class I(C); otherwise nonautomatic in every base | PROVED | 3 |
| split_5, split_73, split_97, splitB_7, splitB_71 (catalog) | BASIN | congruence classes mod d (see table); split_5 already settled in results/split_5_s27.md | PROVED | 1 |
| split_13 (catalog) | BASIN | 13Z -> cycle 13; the basins of cycles 1 and 5 split the non-multiples of 13 nonautomatically in every base | PROVED | 3 |
| split_7081 (catalog) | BASIN | 9 invariant classes; cycles 569 and 713 share one, their basins are nonautomatic; the other 8 cycles have congruence basins | PROVED | 3 |

Check: `check_basins.py` (all finite content: invariance, cycle lists, class tables, the
constructive accessibility proof executed on random targets, the identities used in Theorem B4).

Novelty: Theorem B1 is elementary; I have not seen it stated but did not check the literature
("novelty not checked"). Theorems B2-B4 adapt the argument of round2/rewriting/split5_3_components.md
(itself adapting Monks et al. on sufficient sets in the 3x+1 graph) from the split5_3 map to a
whole family of *settled* maps, where it gives a complete answer to BASIN. Novelty not checked.

Overlap (referee note): the split_5 basin rule (5 | n) was already settled in
results/split_5_s27.md (commit 304d67b), so that row is not new. The concurrent round-3 lenses
`progressions` (applications_basins.md) and `domains` (split_family.md, Theorem P) derive the same
congruence/non-congruence dichotomy for the split catalog members; the results agree and credit
is shared.

## Theorem B1: X_d = SPLIT(1,1,d)

**Theorem B1.** Let d be odd and T = X_d. For a residue class K of Z/d under multiplication by
powers of 2 (a coset r<2>, including {0}), let K^ be the set of integers in [1, d] whose residue
lies in K (residue 0 is represented by d). Then

1. C(K) = K^ ∪ {r + d : r in K^, r odd} is a cycle of T of length |K| + #{odd r in K^};
2. these are all the cycles, one for each K, so there are exactly sum over e | d of phi(e)/ord_e(2)
   cycles;
3. n reaches C(K) if and only if n mod d lies in K.

*Proof.* T(n) = n or n/2 modulo d (n + d = n), so the coset of n mod d is invariant. By
Lemma C of family.md every orbit enters [1, d] and is eventually periodic. Take a cycle and an odd
value n on it. If n > d, then S(n) = (n + d)/2^v <= (n + d)/2 < n and S never maps a value <= d
above d, so the odd values could not return to n; hence all odd cycle values are <= d, the even
values n + d lie in [d+1, 2d], and every value produced by a halving is <= d.

Follow one primitive period. Odd steps keep the residue and each halving multiplies it by
2^{-1}, so the residues of the successive halving results are rho, rho/2, rho/4, ... . Two halving
results with equal residue are equal integers (both lie in [1, d]), which cannot happen inside one
primitive period unless they are the same occurrence. Since the residue returns after the period,
the number of halvings h is a multiple of |K|, and h <= |K| by the previous sentence. So h = |K|
and the halving results run once through K^. Every odd value of the cycle is a halving result, and
every value above d is r + d for the odd r preceding it. This gives 1, and it shows that the cycle
is determined by K, since it contains the integers of K^. Conversely every coset contains a start
in [1, d] whose limit cycle lies in the same coset. This gives 2 and 3; the count of cosets of <2>
in Z/d is the stated sum. ∎

Example: d = 7: cosets {0}, {1,2,4}, {3,5,6} give the cycles (7,14), (1,8,4,2), (3,10,5,12,6).

## Theorems B2-B4: Sigma_d with gcd(d, 6) = 1

Write A(x) = (3x + d)/4 and B(x) = (x + d)/4 for the two odd blocks (each is three steps of the
map) and E(x) = x/2. Let H = <2, 3> in (Z/d)^*. Define the invariant class
I(n) = H · (n mod d), a subset of Z/d.

**Lemma B0.** I(T n) = I(n). Every orbit is eventually periodic, every cycle meets [1, d], and every
class I contains at least one cycle.

*Proof.* T(n) is congruent to n, 3n or n·2^{-1} mod d. Lemma C of family.md gives the rest; every
class contains some n in [1, d] and its limit cycle. ∎

Two starts *merge* if their forward orbits share a value.

**Theorem B2 (accessibility).** Let y >= 1, M >= 1, and x >= 1 with I(x) = I(y). Then there are
arbitrarily large w = x (mod M) whose orbits merge with the orbit of y.

*Proof.* Enlarge M to a multiple of d and write M = 2^u 3^v Q with gcd(Q, 6) = 1, d | Q.

*Inverse steps.* For an odd z and h >= 2 put L_h(z) = 2^h z - d and, when 2^h z = d (mod 3),
U_h(z) = (2^h z - d)/3. Both are odd. When positive, they are ancestors of z: L_h(z) + d = 2^h z
is divisible by 4, so the map takes the n + d branch and then h halvings; and
3 U_h(z) + d = 2^h z likewise. Ancestors of y have the class I(y).

*Step 1 (one residue modulo Q, all residues modulo powers of 3).* Replace y by an odd ancestor z
with 3 ∤ z: the odd part of y is a forward iterate of y, hence merges with it; if 3 divides it,
apply L_h with h large (3 ∤ d). Let o = ord_Q(2) and k = v_3(o). For h with 3^{k+1} | 2^h z - 4d,
define

    w(h) = U_2^k(U_h(z)) = d + 4^k (2^h z - 4d)/3^{k+1}.

The identity U_2(x) - d = (4/3)(x - d) gives the formula, and each U_2 step is legal because its
input minus d is divisible by the remaining power of 3; the first step is legal because
2^h z = 4d = d (mod 3). For s >= 0 and t mod 3^s, the condition w(h) = t (mod 3^s) reads

    2^h z = 4d + 3^{k+1} 4^{-k} (t - d)   (mod 3^{k+1+s}).

The right side is a unit, and 2 is a primitive root modulo every power of 3 (it is one modulo 9),
so the solutions form one class of h modulo 2·3^{k+s}, all lying in one fixed class h_0 modulo
2·3^k (the case s = 0). We also impose h = h_0 (mod o). This is compatible, because
gcd(o, 2·3^{k+s}) divides 2·3^k. Then w(h) mod Q depends only on h mod o, so it is one residue
r_0, independent of s and t, and h can be arbitrarily large. Call a residue r mod Q *accessible*
if for all s and t there are arbitrarily large odd ancestors of y that are = r (mod Q) and
= t (mod 3^s). We have shown that r_0 is accessible.

*Step 2 (closure).* If r is accessible, so are L_2(r) = 4r - d, L_3(r) = 8r - d and
U_2(r) = (4r - d)/3 (mod Q). For L_h: to get t mod 3^s at the output, ask for (t + d) 2^{-h} at the
input. For U_2: ask for (d + 3t)/4 mod 3^{s+1}; this is = d (mod 3), so U_2 is legal, and the
output is = t (mod 3^s). These three maps are permutations of Z/Q, so the accessible set is closed
under the group G they generate. Now L_2 U_2(r) = (16r - 7d)/3 and U_2 L_2(r) = (16r - 5d)/3,
so G contains the translation by -2d/3, whose powers are all translations by multiples of d
(2/3 is a unit mod Q and d | Q). Modulo d the generators multiply by 4, 8 and 4/3, which generate
H. Hence the G-orbit of r_0 is the set of all r mod Q with r mod d in I(r_0) = I(y). All of these
residues are accessible.

*Step 3 (the 2- and 3-parts of M).* From x apply u blocks (E if even, otherwise A or B). Let c be
the endpoint, 2^l the product of the block denominators (l >= u) and k' the number of A blocks;
then the endpoint is (3^{k'} x + beta)/2^l. Write c = 2^e c_o with c_o odd; I(c_o) = I(x) = I(y).
By Steps 1-2 choose an arbitrarily large odd ancestor c'' of y with c'' = c_o (mod 3^{v+k'} Q) and
put c' = 2^e c''. Set

    w = x + 2^l (c' - c)/3^{k'}.

Then w = x (mod 2^u) since l >= u, w = x (mod 3^v) since 3^{v+k'} | c' - c, and w = x (mod Q)
since 2^l/3^{k'} is a unit mod Q. Along the u blocks the value reached from w exceeds that reached
from x by 3^{k_i} (w - x)/2^{l_i}, which is divisible by 2^{l - l_i}, enough to fix the residue mod
4 (or mod 2) that selects the next block. So w follows the same blocks and ends at
c + 3^{k'}(w - x)/2^l = c'. Thus w is an ancestor of c', hence of y. ∎

**Corollary B3 (congruence basins).** Let C be a cycle of Sigma_d.
(a) If C is the only cycle in its class, its basin is exactly {n >= 1 : n mod d in I(C)}.
(b) If another cycle C' has I(C') = I(C), then every progression containing an integer of
residue class in I(C) contains arbitrarily large members of both basins. In particular neither
basin is a finite union of residue classes, and its indicator is not ultimately periodic along any
such progression.

*Proof.* (a) Every orbit ends in a cycle of its own class. (b) Theorem B2 applied to y in C and
y' in C'. If the indicator were ultimately periodic with period P on the progression Dn + r, it
would be eventually constant on the subprogression with step DP through a member of class I(C),
contradicting B2 for that subprogression. ∎

**Theorem B4 (no automaton).** Let f be any finite-valued function on the positive integers with
f(T n) = f(n). If f is automatic in some integer base k >= 2, then f(n) depends only on I(n).
In particular, in the situation of B3(b), the basins of C and C' are not k-automatic for any k.

*Proof.* Suppose f takes two values on one class Γ. By B2 (labels are constant on merging
classes) the restriction of f to any progression meeting Γ is not ultimately periodic, by the
argument of B3(b). We use the k-kernel K_k(f) = {n -> f(k^a n + r) : a >= 0, 0 <= r < k^a}, finite
exactly when f is k-automatic, and Cobham's theorem as used in
round2/rewriting/split5_3_components.md, Theorem 2: a sequence automatic in two multiplicatively
independent bases is ultimately periodic.

The digit lemma (components.md): let S be a finite set of sequences and suppose that for every
finite base-p word some member of S can read it (each successive section n -> h(p n + i) stays in
S). Then a single member reads every word. Otherwise append, one at a time, a word failing from
the current state of a surviving start; after |S| extensions no start survives, a contradiction.
A member reading every word has all its base-p sections in S, so it is p-automatic.

*Case k not a power of 2.* Since f(2n) = f(n), sections in base 2 are simple. Let S be the members
f(Dn + s) of K_k(f) (D = k^a, 0 <= s < D) whose progression meets Γ; with g = gcd(D, d) this holds
iff s mod g lies in Γ mod g. For a binary word of length e and value δ choose a with D = k^a > 2^e·d,
and r in [0, D) with r = -Dδ (mod 2^e) and r mod g in Γ mod g (compatible: coprime moduli). Such
an r exists in [0, D) because the two conditions fix r modulo 2^e·g, and D > 2^e·d >= 2^e·g. For
δ_j = δ mod 2^j put s_j = (D δ_j + r)/2^j, an integer in [0, D). The section after reading j digits
is f(D(2^j n + δ_j) + r) = f(2^j (Dn + s_j)) = f(Dn + s_j), and 2^j s_j = r (mod g) shows
s_j mod g lies in Γ mod g, because Γ is closed under multiplication by 2^{-1}. So every word is
readable within S; the digit lemma gives a member of S that is 2-automatic and k-automatic, hence
ultimately periodic by Cobham, contradicting the first paragraph.

*Case k a power of 2.* Then f is 2-automatic, and so is the shift g(m) = f(m + d). For m >= 0 the
start 4m + d takes the branch 3x + d (as 12m + 4d is divisible by 4) and then two halvings, reaching
3m + d. Hence g(4m) = g(3m) and by induction g(3^j m) = g(4^j m). For a base-3 word of length e and
value δ take D = 2^a > 3^e and r in [0, D) with r = -Dδ (mod 3^e), and s_j = (D δ_j + r)/3^j. The
section is g(3^j(Dn + s_j)) = g(4^j D n + 4^j s_j), a member of the binary kernel of g; every
progression with a power-of-2 step meets Γ since gcd(2, d) = 1. The digit lemma with p = 3 and
Cobham give the same contradiction. ∎

## Tables (d < 200, gcd(d,6) = 1, and the catalog values)

`basins_lib.py` lists all cycles (starts 1..d suffice by Lemma B0) and the classes of H.
Classes containing two or more cycles ("shared"); all other cycles have congruence basins:

| d | Sigma_d | classes | cycles (by minimum) | shared classes |
|---|---|---|---|---|
| 5 | split_5 | 2 | 1, 5 | none (basin rule: 5 \| n) |
| 7 | splitB_7 | 2 | 1, 7 | none (basin rule: 7 \| n) |
| 13 | split_13 | 2 | 1, 5, 13 | {1, 5} |
| 29 | SPLIT(3,1,29) | 2 | 4 cycles | {1, 5, 7} |
| 31 | SPLIT(1,3,31) | 2 | 3 cycles | {1, 5} |
| 55 | SPLIT(1,3,55) | 4 | 5 | {7, 23} |
| 61 | SPLIT(3,1,61) | 2 | 6 | {1, 5, 7, 9, 21} |
| 65 | SPLIT(3,1,65) | 4 | 5 | {5, 25} |
| 67 | SPLIT(1,3,67) | 2 | 3 | {5, 11} |
| 71 | splitB_71 | 3 | 3 | none |
| 73 | split_73 | 3 | 3 | none |
| 85 | SPLIT(3,1,85) | 4 | 5 | {3, 7} |
| 91 | SPLIT(1,3,91) | 4 | 5 | {7, 35} |
| 97 | split_97 | 3 | 3 | none |
| 109, 113, 119, 125, 127, 131, 139, 143, 145, 155, 161, 167, 169, 187 | | | | shared (see check output) |
| 7081 | split_7081 | 9 | 10 | {569, 713} |

Among the 67 values d < 200 with gcd(d, 6) = 1, 44 have only congruence basins and 23 have at
least one shared class. Members with 3 | d are not covered by B2 (the 3-adic step uses 3 ∤ d);
for them the invariant is not a group orbit (for example SPLIT(3,1,9) sends the class 3Z \ 9Z into
9Z), and their basins are left open here.
