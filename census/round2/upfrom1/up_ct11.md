# up_ct11

**Rule.** n = 3 mod 4 -> n+4 (trap); otherwise the accelerated Collatz map T (even n -> n/2, odd n -> (3n+1)/2).
Seed 27 (trapped at once). The base point of the "Collatz with trapdoors" ladder: every residue class whose
T-parity word starts "11" is a trap.

**Question.** Which n have infinite orbits?

**Answer (PROVED).** Exactly those n whose T-orbit meets a number = 3 mod 4 before reaching 1; every other orbit
reaches the cycle (1 2). There are no other cycles and no untrapped divergence. Membership is decided by
simulating at most O(log n) steps.

## Proof
Trap: n = 3 mod 4 -> n+4 stays 3 mod 4 and increases. Off the trap: even n -> n/2 < n; n = 1 mod 4 ->
(3n+1)/2, which is even, then (3n+1)/4 < n for n > 1. So untrapped orbits strictly decrease along 1- or 2-step
blocks until they reach 1, and 1 -> 2 -> 1. Each block multiplies by at most 3/4 (+1/4), giving the O(log n) bound.

## Tier: 1
One-line two-step descent (the parity word of an untrapped orbit never contains "11", so every 2-window has
at most one odd step and 3 < 2^2).

## Note: what is NOT known about this system
The answer is a decision procedure, not a closed description. Evidence suggests the finite-orbit set E is
**not** a regular language in base 2 (so no tier-3 description of the type found for up_tok3): LSB-first
Nerode classes distinguished with a 9-bit extension window grow with suffix length L = 0..12 as
1,2,4,6,8,11,16,23,33,48,70,101,146 (MSB-first: 1,2,4,8,15,24,31,46,58,77,90,110,130), and
|E cap [1,2^k)| for k = 1..20 is 1,2,4,7,12,19,29,43,64,91,131,184,259,362,508,710,997,1400,1969,2768
(ratio ~1.40, no visible linear recurrence). A proof of non-regularity would need, e.g., to show that the fate
of 2^{2j}+1 (which reduces to the fate of (3^j+1)/2^v) is not eventually periodic in j - a number-theoretic
question about powers of 3 that I could not settle. So: GLOBAL behaviour tier 1, regular description OPEN.

## Check
`check_up_ct11.py`: the two-step identity on n = 1 mod 4 (n < 200000) and, for all n < 300000, that the orbit is
trapped or ends in (1 2). PASS.

## Referee
**Verdict: CONFIRMED for the GLOBAL claim (divergent set = trap basin; (1 2) is the only untrapped cycle). Final tier: 1 (agreed).**
If n = 4k+1, then (3n+1)/2 = 6k+2 is even and never 3 mod 4, and the next value (3n+1)/4 < n for n > 1. As a check, a stopping-time tree over residues (`referee_tests.py`) closes at depth 2 with threshold 2.
Caveat: the "answer" is a decision procedure, not a closed description. Read with up_tok3's standard (exact closed classification), the question is OPEN. Non-regularity is only evidenced (Nerode counts), not proved, and I did not settle it. The question should be recorded as GLOBAL.
