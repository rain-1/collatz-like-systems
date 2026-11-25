# split5_1_s27: GLOBAL, partial result (round 2, rewriting lens)

Rule: even n -> n/2; n=1 mod 4 -> 5n+1; n=3 mod 4 -> n+1. Question: GLOBAL (is every orbit eventually periodic?). Known cycles: {1,6,3,4,2} (min 1, length 5) and a 35-cycle with min 13.

| question | answer | status | tier |
|---|---|---|---|
| GLOBAL | unknown. Proved: a minimal counterexample, every new cycle's minimum and infinitely many points of every divergent orbit lie in an explicit set E of density 1.082e-02 | PARTIAL | 5 (partial statement: 2) |

## Method: machine-found descent tree (lib.descent_tree)

The tree explores residue classes n = Q t + r (t >= 0). Along a branch it carries the exact
affine image T^s(n) = A t + B, where A and B are integers. When the residue of A t + B modulo the
branching modulus is not fixed, it splits t. A class is *closed* as soon as A < Q. Then
T^s(n) < n for every t > t0 = (B - r)/(Q - A). The finitely many n with t <= t0 are simulated
directly; any n whose orbit fails to drop below n within 10^5 steps is recorded in a finite list S.
A class is *open* when one more split would push its modulus past the cap. The union E of the
open classes is the exceptional set.

**Theorem (partial).** Every n >= 1 with n not in E ∪ S has some iterate T^k(n) < n (k >= 1).
Consequences, all proved:
1. If GLOBAL fails, the least start n0 whose orbit is not eventually periodic lies in E. If n0 were
   outside E ∪ S, it would drop to some m < n0 whose orbit is eventually periodic, and then so is
   the orbit of n0. The points of S are periodic (the check verifies this).
2. Every cycle not on the listed cycles has its minimum in E, because a cycle minimum never drops
   below itself.
3. Every orbit that is not eventually periodic visits E infinitely often. Such an orbit takes no
   value twice, so it tends to infinity. It therefore has infinitely many *tail minima* x_k (x_k <= x_i
   for all i >= k), and none of them drops below itself.

**Why the table can never be completed (tier 2 provably fails).** The system has a p-adic point c
with infinite coefficient stopping time. For every K, the positive integers n_K in c's class modulo
p^K have stopping time at least L(K) → ∞ (witness below, checked for the listed K). So E is
nonempty at every modulus, and no finite descent table settles GLOBAL. This also rules out every
Lyapunov function of the form Φ(n) = n·w(n mod M) with positive weights. Strict decrease along an
up-run of length L gives T^L(n)/n < max w / min w, but T^L(n)/n grows without bound on the
witnesses.

**Blocking mechanism.** The descent proof fails at exactly two points. (a) The expanding branch has
an affine conjugacy x -> ρx (ρ > 1) on a p-adic neighbourhood of c, so up-runs have unbounded
length. (b) Re-entry is free: every m is the image of p·m under the division branch (p = 2 or 3). So a
value in the class of c to any prescribed depth can be entered from a value only p times larger. Any potential with a run-length weight Φ = n·λ^{ν(n)} (ν = depth
of n in c's neighbourhood) therefore fails at the re-entry step: the output m can have ν(m) as
large as log_p(m), and Φ(m)/Φ(n) is unbounded. To finish the proof you would have to show that
re-entry into deep neighbourhoods of c cannot happen often along a single orbit. That statement
about orbit statistics is the 3x+1 obstruction.

## Certificate for this system

- Modulus cap 16777216: 181544 open classes and 17153 closed leaves. The exact density of E is
  22693/2097152 ≈ 1.0821e-02. The small exceptions are S = [1, 13], all periodic.
- How the density decays (cap: classes, density): 2^8: 13 classes, 5.08e-2 | 2^12: 156, 3.81e-2 | 2^16: 1402, 2.14e-2 | 2^20: 14339, 1.37e-2 | 2^24: 181544, 1.08e-2 | 2^26: 604496, 9.01e-3.
  The decay is slow and polynomial in the cap, and the class count keeps growing.
- Witness for "E is never empty": c = -1/3 in Z_2. For odd n = 1 mod 4 the step pair 5n+1, /2 gives n' = (5n+1)/2 with 3n'+1 = (5/2)(3n+1). n_K = (4^K - 1)/3 has 3n_K+1 = 4^K, so it makes 2K-1 consecutive such pairs, each value larger than n_K. That gives stopping time >= 4K-2, checked for K = 1..32.

## Rewriting and potentials (lens b, c)
- (c) Bounded-weight potentials n·w(n mod M) are ruled out for every M (proof above). Run-length
  weighted potentials fail at the re-entry step (blocking mechanism (b) above).
- (b) Rewriting (b) not attempted to completion. The 35-cycle through 13 means a terminating SRS would have to recognise that cycle, and a mixed base-2/base-5 encoding with a cycle-halting guard was beyond the budget. See m3_b_s8.md for the z3 results on the cleanest member of the catalog.

## What blocks a full proof
The descent tree closes every class except a closed p-adic set Ω that contains c. Ω has density
<= the tabulated values; that Ω has measure zero would follow from a Terras-type theorem and is not proved here. The
expanding branch generates c's up-runs, and the contracting branches generate the free re-entry. No
finite modulus, bounded potential or low-dimensional interpretation separates them.

## Tier
The partial theorem uses tier-2 machinery: a descent inequality plus a finite (machine-generated)
table. GLOBAL itself stays at tier 5 (OPEN). Tier 2 provably cannot settle it, because E is
nonempty at every modulus (witness).

Check: `check_split5_1_s27.py` reproduces E exactly (count, exact density, small list), checks that every
point of S is periodic and that the cycle minima lie in E ∪ S, and tests the witness bounds.

## Referee (round 2)
**Verdict.** GLOBAL: open-agreed, final tier 5. Partial theorem (E): confirmed, tier 2. I could not finish the proof. The open part is a 3x+1-type convergence problem, and no lower-tier method closes the class of the p-adic blocking point.

Independent tests (referee, scratchpad scripts ref1.py/cantor.py, not in repo):
- systems.py step agrees with the lib.py table for n < 20000.
- check_<id>.py rerun: exit 0, about 1 s.
- My own consistency test against the systems.py step function, with E rebuilt at a smaller cap: every n in [2, 6e4) outside E ∪ S drops below itself (10^6-step cap). So do 300 random 200-bit n outside E (2e4-step cap). Zero failures.
- I re-derived the closure logic of lib.descent_tree. A split by g = M/gcd(A,M) fixes the residue because A·g = lcm(A,M) ≡ 0 (mod M). A2 = uA/w is integral (asserted). A leaf closes when A2 < Q, which gives T^s(Qt+r) < Qt+r for t > (B2-r)/(Q-A2). Small t are simulated, and non-descenders are recorded in S and checked to be periodic. Consequences 1-3 (minimal counterexample, cycle minima, tail minima of divergent orbits) are correct.

Gap (repaired here). The .md derives "E is nonempty at every modulus" from the unbounded stopping time of the witnesses n_K. That inference is incomplete on its own: a closed leaf can contain a late-descending n among its finitely many simulated small t. Correct argument: c is a p-adic fixed point of the expanding block, and the tree branch through c has A/Q equal to the product of the branch slopes. Along that branch the product is >= 1 after every step, so the class of c never closes, at any cap. The other use of the witnesses, "no finite descent table", is valid by pigeonhole: finitely many classes, each with a bounded step count and finitely many exceptions, cannot contain infinitely many n_K with stopping time going to infinity.
Minor point: the lens says bounded-weight potentials are killed by free re-entry. The proof actually given kills them with the unbounded up-run ratio, not with re-entry.
