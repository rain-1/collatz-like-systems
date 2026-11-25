# perm_flip_s27

Rule: 2q+1 -> 2q+2; 2q+2 -> 2q+1 (odd n -> n+1, even n -> n-1)

| question | answer | status | tier |
|---|---|---|---|
| FATE (seed) | returns to seed (27 -> 28 -> 27, period 2) | PROVED | 0 |
| GLOBAL | yes (every orbit is a 2-cycle) | PROVED | 1 |

## Proof

FATE (tier 0): 27 is odd, f(27)=28; 28 is even, f(28)=27.

GLOBAL (tier 1): f swaps 2q+1 and 2q+2 for every q >= 0, so f(f(n)) = n for all n >= 1, and f has no fixed points (f(n) = n+-1). Every orbit is purely periodic with period exactly 2.

## Check

checks/perm_flip_s27.py verifies, with exact integer arithmetic, that the catalog step function agrees with the case formulas used above for all n < 200000, the monotonicity/closed-form facts on that range, and the seed orbit prefix. The proof itself is the algebra above; the check only guards against a mismatch between the catalog code and the stated rule.

## Referee

Verdict: FATE confirmed (tier 0), GLOBAL confirmed (tier 1). Code: odd n -> n+1, even n -> n-1, so f is a fixed-point-free involution and every orbit is a 2-cycle. 27 -> 28 -> 27. Check script re-run (OK); independent test of the key lemma over n < 10^5 also passed. The argument is pure algebra on the catalog code, so it does not depend on simulation, and it uses no injectivity assumption.
