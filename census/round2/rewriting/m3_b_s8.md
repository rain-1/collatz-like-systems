# m3_b_s8: GLOBAL, partial result (round 2, rewriting lens)

Rule: 3|n -> n/3; n ≡ 1 -> (4n-1)/3; n ≡ 2 -> (4n+1)/3. Equivalently 3k -> k, 3k+1 -> 4k+1, 3k+2 -> 4k+3.
Question: GLOBAL. Known cycles: only the fixed point 1.

| question | answer | status | tier |
|---|---|---|---|
| GLOBAL | unknown. Proved: a minimal counterexample, every new cycle's minimum and infinitely many points of every divergent orbit lie in an explicit set E of density 5.053e-02. Also proved: no natural matrix interpretation of dimension <= 2 with entries <= 3 orients the core of the rewriting encoding (z3 UNSAT) | PARTIAL | 5 (partial statements: 2 and 4) |

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
- Modulus cap 3^14 = 4782969: 241664 open classes and 79391 closed leaves. The exact density is
  241664/4782969 ≈ 5.0526e-02. The small exceptions are S = [].
  The fixed point 1 itself lies in E: it sits in the open neighbourhood of the 3-adic fixed point 1 of 3k+1 -> 4k+1.
- How the density decays (cap: classes, density): 3^6: 128, 1.76e-1 | 3^8: 768, 1.17e-1 | 3^10: 5376, 9.10e-2 |
  3^12: 38912, 7.32e-2 | 3^14: 241664, 5.05e-2.
- Witness: c = -1 in Z_3. For n ≡ 2 (mod 3), n' + 1 = (4/3)(n+1). n_K = 3^K - 1 makes K rising steps, so
  its stopping time is >= K. Checked for K = 1..40. A second blocking point is the positive fixed point 1:
  n = 1 + 3^K m makes K rising steps n -> (4n-1)/3.

## Lens (b): string rewriting in mixed base 3/4, in the style of Yolcu-Aaronson-Heule
**Encoding** (srs.py, `family_srs(4, 1, 3, h=1)`, 37 rules). A word L d_1 ... d_m R represents a number in
Horner form, with ternary digits t0..t2 and base-4 digits b0..b3.
- tail rules (context x = any digit symbol): x t0 R -> x R, x t1 R -> x b1 R, x t2 R -> x b3 R;
- swap rules: t_r b_d -> b_q t_r' where 4r + d = 3q + r' (12 rules, value-preserving);
- left rules: L b_d -> L tern(d) (4 rules).

**Simulation lemma (proved).** Let n >= 3 and let w be any word of value n made only of ternary digits
(leading zeros allowed). Then w has at least 2 digits, so the tail rule for n mod 3 applies, and it
produces a word of value T(n) that ends in at most one b-digit. Each swap moves that b-digit one place
left and preserves the value. The left rule then converts it to ternary digits. The result is an
all-ternary word of value T(n). Hence an orbit that stays >= 3 forever gives an infinite derivation.
So **termination of this SRS implies GLOBAL for m3_b** (the only value < 3 that occurs is the fixed
point 1, and 2 -> 3). The check samples the lemma for 3 <= n < 3000.

**Search** (mi_search.py, z3 4.x bit-vector encoding). This is the standard rule-removal method: weakly
orient all rules, strictly orient some, delete the strict ones and repeat (Endrullis, Waldmann and
Zantema, "Matrix interpretations for proving termination of term rewriting", J. Automated Reasoning 40
(2008)). Interpretations are natural, with M[0][0] >= 1 and entries in {0..3}.
- Dimension 1: UNSAT on the full system.
- Dimension 2: removes three rules, all irrelevant to the simulation (37 -> 34). They are left4_0
  (L b0 -> L) and the tail2 rules whose context is b0 or b2, contexts that never occur in a simulating
  derivation. See m3b_mi_chain.json; the check re-verifies the chain exactly in Python. Then it is UNSAT on the remaining core. Because UNSAT on a set R also rules out strict
  progress on R from any superset, no chain of dimension-<=2, entries-<=3 interpretations ever
  removes a rule of the core. The core (34 rules) consists of all 12 swap rules, 19 of the 21 tail rules (all
  except the two junk-context ones), and the left rules for d >= 1.
- Dimension 3, entries <= 3: z3 returned "unknown" after 300 s per round. That is no evidence either
  way.
- Subsystems (one tail rule removed; that is, orbits that halt on reaching the corresponding class):
  without tail0 (37 -> 30 rules), the search stalls at 27 rules (dimension 2 UNSAT). Without tail1 it
  stalls at 26. Without tail2 it stalls at 28 (dimension 2 UNSAT, dimension 3 unknown). None of the
  subsystems was proved terminating. Each subsystem is itself a nontrivial question. For example,
  without tail0 it asks whether every orbit of 3k+1 -> 4k+1, 3k+2 -> 4k+3 eventually hits a multiple
  of 3. Every step multiplies by about 4/3, so this is a Mahler/Z-number-type avoidance question.
The swap rules are where the carries of the base change happen. They are exactly where a natural
interpretation has to "know" the value, and a small matrix cannot. Yolcu et al. could not solve their full
3x+1 system either. They did solve all 11 one-rule-removed subsystems of their encoding, but those
subsystems are different from the ones above.

## Tier
- Partial theorem (E): tier 2. The full GLOBAL question cannot be settled at tier 2, because E is
  nonempty at every modulus (witness).
- Rewriting: proving SN would be a tier-4 certificate. We obtained only the negative bounded-search
  result above. It is a solver-certified UNSAT for the stated parameter box, and evidence (not proof)
  that no small certificate exists.
- GLOBAL stays OPEN (tier 5).

Check: `check_m3_b_s8.py` reproduces E exactly, checks the witness, samples the simulation lemma, and
re-verifies the stored partial interpretation chain with exact integer arithmetic.

## Referee (round 2)
**Verdict.** GLOBAL: open-agreed, final tier 5. Partial theorem (E): confirmed, tier 2. I could not finish the proof. The open part is a 3x+1-type convergence problem, and no lower-tier method closes the class of the p-adic blocking point.

Independent tests (referee, scratchpad scripts ref1.py/cantor.py, not in repo):
- systems.py step agrees with the lib.py table for n < 20000.
- check_<id>.py rerun: exit 0, about 1 s.
- My own consistency test against the systems.py step function, with E rebuilt at a smaller cap: every n in [2, 6e4) outside E ∪ S drops below itself (10^6-step cap). So do 300 random 200-bit n outside E (2e4-step cap). Zero failures.
- I re-derived the closure logic of lib.descent_tree. A split by g = M/gcd(A,M) fixes the residue because A·g = lcm(A,M) ≡ 0 (mod M). A2 = uA/w is integral (asserted). A leaf closes when A2 < Q, which gives T^s(Qt+r) < Qt+r for t > (B2-r)/(Q-A2). Small t are simulated, and non-descenders are recorded in S and checked to be periodic. Consequences 1-3 (minimal counterexample, cycle minima, tail minima of divergent orbits) are correct.

Gap (repaired here). The .md derives "E is nonempty at every modulus" from the unbounded stopping time of the witnesses n_K. That inference is incomplete on its own: a closed leaf can contain a late-descending n among its finitely many simulated small t. Correct argument: c is a p-adic fixed point of the expanding block, and the tree branch through c has A/Q equal to the product of the branch slopes. Along that branch the product is >= 1 after every step, so the class of c never closes, at any cap. The other use of the witnesses, "no finite descent table", is valid by pigeonhole: finitely many classes, each with a bounded step count and finitely many exceptions, cannot contain infinitely many n_K with stopping time going to infinity.
Minor point: the lens says bounded-weight potentials are killed by free re-entry. The proof actually given kills them with the unbounded up-run ratio, not with re-entry.

Rewriting part (referee):
- Simulation lemma: re-derived. The swap rule preserves value, since 12P + 4r + d = 12P + 3q + r'. The only orbits below 3 are 2 -> 3 -> 1 and the fixed point 1. So SN implies GLOBAL, together with "the only cycle is {1}". Confirmed.
- MI chain: re-verified exactly by the check.
- z3 UNSAT on the 34-rule core: I reran mi_search.one_round with z3 from the scratchpad venv, and dimension 1 and dimension 2 (entries <= 3) both return unsat.
- Bit width 28 cannot overflow: there are at most 3-symbol words with entries <= 3 at dimension 2.
- The "no chain ever removes a core rule" argument is valid.
- This is a bounded negative search result. It does not lower or raise any tier.
- Nit: the usage line in mi_search.py says "B s1 s2 h", but the code parses B1 s1 B2 s2 h.
