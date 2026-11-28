# acc_h16: the smallest example found in the 3n+1/n+1/n+c family (settled)

**Rule.** Even n → n/2. For odd n, look at n mod 16:
* n+1 if n ≡ 5, 9;
* n+5 if n ≡ 13;
* 3n+1 if n ≡ 1, 3, 7, 11, 15.

**Question.** GLOBAL, with the complete cycle list.

**Answer (PROVED).** Every positive orbit is eventually periodic. The cycles are exactly
(1 4 2) and (3 10 5 6).

**OBST.** The 2-adic fixed point −1 has multiplier 3/2, so there is no descent certificate
(Lemma B).

**Proof.** Apply Theorem H at K = 4 (`trichotomy.md`). The SCCs of G_4 are:
* {0}, contracting;
* {14, 15}, an isolated expanding cycle with periodic point −1;
* a contracting SCC of 10 nodes {1,2,3,4,5,6,9,10,11,13}. It has exact weights (the same mod-8
  pattern as acc_h32) and θ = 843643/858949. Every cycle in it has n ≤ 452.

For the S-family itself (n+1 or 3n+1 only), an exhaustive search over m ≤ 5 finds no system
with an isolated expanding cycle (`check_trichotomy.py`, [S-b]). The single n+5 patch is what
makes isolation possible here.

**Tier.** 2–3. Novelty not checked. **Check.** `check_trichotomy.py`.
