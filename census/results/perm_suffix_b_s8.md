# perm_suffix_b_s8

Rule: 2q+1 -> 16q+12; 8q+4 -> 2q+1; 4q+2 -> 4q+2; 16q -> 8q; 16q+8 -> 16q+4

| question | answer | status | tier |
|---|---|---|---|
| FATE (seed) | infinite (8, 4, 1, 12, 3, 28, 7, 60, 15, ...; odd terms are 2^k - 1) | PROVED | 1 |
| GLOBAL | no | PROVED | 1 |

## Proof

Write odd n = 2q+1. Then f(n) = 16q+12 = 8n+4, which is 4 mod 8, so f(f(n)) = 2*(n)+1 (since 8n+4 = 8q'+4 with q' = n, giving 2q'+1 = 2n+1). Hence g = f^2 restricted to odd numbers is g(n) = 2n+1, odd and > n.

FATE (tier 1): 8 = 16*0+8 -> 4 = 8*0+4 -> 1. From 1 the odd terms are g^k(1) = 2^(k+1) - 1, strictly increasing, interleaved with the even terms 8n+4 = 2^(k+4) - 4, also strictly increasing. All terms are distinct, so the orbit is infinite.

GLOBAL (tier 1): No. The orbit of 1 (equivalently of any odd number, or of 8) is infinite by the same argument. (Values 4q+2 are fixed points, so some orbits are periodic, but not all.)

## Check

checks/perm_suffix_b_s8.py verifies, with exact integer arithmetic, that the catalog step function agrees with the case formulas used above for all n < 200000, the monotonicity/closed-form facts on that range, and the seed orbit prefix. The proof itself is the algebra above; the check only guards against a mismatch between the catalog code and the stated rule.

## Referee

Verdict: FATE confirmed (tier 1), GLOBAL confirmed (tier 1). Code: odd n -> 8n+4, and 8n+4 is 4 mod 8, so it maps to (8n+4-4)/4+1 = 2n+1. 8 -> 4 -> 1, then the odd terms are 2^k-1, strictly increasing. Check script re-run (OK); independent test of the key lemma over n < 10^5 also passed. The argument is pure algebra on the catalog code, so it does not depend on simulation, and it uses no injectivity assumption.
