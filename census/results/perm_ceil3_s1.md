# perm_ceil3_s1

Rule: 2m -> 2(m+ceil(m/3)); 4q+1 -> 2(4q+1); 4q+3 -> 2q+1

| question | answer | status | tier |
|---|---|---|---|
| FATE (seed) | infinite (1 -> 2 -> 4 -> 6 -> ...; all terms after the first are even and strictly increasing) | PROVED | 1 |
| GLOBAL | no | PROVED | 1 |

## Proof

Let F(m) = m + ceil(m/3). For m >= 1, ceil(m/3) >= 1, so F(m) > m.

FATE (tier 1): 1 = 4*0+1 -> 2*(4*0+1) = 2. Every even n = 2m maps to 2F(m), which is even and > n. So from 2 on the orbit stays in the even numbers and is strictly increasing; all terms are distinct and the orbit is infinite. (The even subsequence is 2*F^k(1), i.e. the Mahler-type iteration m -> m + ceil(m/3); its fine arithmetic is irrelevant to these two questions because monotonicity already decides them.)

GLOBAL (tier 1): No. Every even start has an infinite strictly increasing orbit by the same argument.

## Check

checks/perm_ceil3_s1.py verifies, with exact integer arithmetic, that the catalog step function agrees with the case formulas used above for all n < 200000, the monotonicity/closed-form facts on that range, and the seed orbit prefix. The proof itself is the algebra above; the check only guards against a mismatch between the catalog code and the stated rule.

## Referee

Verdict: FATE confirmed (tier 1), GLOBAL confirmed (tier 1). Code: 1 -> 2; even 2m -> 2(m+ceil(m/3)) > 2m and even. Check script re-run (OK); independent test of the key lemma over n < 10^5 also passed. The argument is pure algebra on the catalog code, so it does not depend on simulation, and it uses no injectivity assumption.
