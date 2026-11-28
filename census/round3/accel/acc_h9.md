# acc_h9: a base-3 system with an isolated expanding cycle (settled, easy)

**Rule** (n = 9q + r):
* 3q → q;
* 9q+1 → 6q+1, 9q+4 → 6q+4, 9q+7 → 6q+7;
* 9q+2 → 12q+4, 9q+5 → 12q+7, 9q+8 → 12q+11.

As a table, these are n/3, (2n+r)/3 and (4n+c)/3.

**Question.** GLOBAL, with the complete cycle list.

**Answer (PROVED).** Every positive orbit is eventually periodic. The cycles are the three fixed
points 1, 4 and 7.

**OBST.** −1 = 9·(−1)+8 ↦ 12·(−1)+11 = −1 is a 3-adic fixed point with multiplier 4/3. Lemma B
then gives no descent certificate.

**Proof.** Apply Theorem H at K = 2. The SCCs are:
* {0}: 0 → 0 at level 2, multiplier 1/3;
* {8}: self-loop, multiplier 4/3, isolated, periodic point −1;
* {1, 4, 7}: multipliers 2/3, contracting with weights 1.

The nodes 2, 3, 5 and 6 are transient. Every class reachable from outside {0, 6, 8} stays outside it.
In elementary terms: once an orbit leaves the 3-adic shadow of −1 it only meets the branches 2/3
and 1/3 apart from transient 4/3 steps, so it descends.

**Tier.** 1–2 once the SCC picture is drawn. This system is the base-3 illustration of
Theorem H, not a hard case. Novelty not checked. **Check.** `check_trichotomy.py`.
