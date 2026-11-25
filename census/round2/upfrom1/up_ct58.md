# up_ct58

**Rule.** If n mod 256 lies in R -> n+256, where R is the set of 37 residues r mod 256 whose 8-step T-parity word
has >= 6 ones; otherwise accelerated Collatz T. Seed 27 (trapped: 27 in R).
Purpose: push the ladder as close as possible to the critical odd-step density log 2/log 3 = 0.6309... with an
8-window: allowed density 5/8 = 0.625.

**Question.** Which n have infinite orbits?

**Answer (PROVED).** Exactly those whose T-orbit meets R (mod 256) before reaching 1; all other orbits reach (1 2).

## Proof
Same scheme as up_ct35. Traps are invariant and increasing. An untrapped orbit has, at every time t, an 8-word with
at most 5 ones (that is the definition of R, via the parity lemma). Then x_{t+8} = (3^k x_t + b_w)/256 with k <= 5,
and the maximum of b_w over all 8-words with <= 5 ones is 1688 (exhaustive). So x_{t+8} <= (243 x_t + 1688)/256,
which is < x_t for x_t >= 130 and <= 129 for x_t <= 129. Thus untrapped orbits are bounded, every untrapped cycle
meets [1,129], and the finite table (all starts <= 129, in fact all n < 300000) shows they end in (1 2).

## Tier: 2
Descent inequality + finite table (table now of size 129 instead of 11; contraction 243/256 = 0.949).

**Why not tier 1.** As for up_ct35 (evidence): untrapped stretches of length up to 7 with multiplier > 1 exist
(e.g. word 1101101 has 3^5/2^7 = 1.90), so short-block monotonicity fails.

## Check
`check_up_ct58.py`: |R| = 37, parity-word/residue correspondence mod 256, b_max = 1688, descent constants, fate of
all n < 300000. PASS.

## Referee
**Verdict: CONFIRMED. Final tier: 2 (agreed).**
|R| = 37, b_max = 1688 over 8-words with <= 5 ones, threshold 130 (13*130 > 1688), and the floor bound 129 all check out. The 8-word depends only on n mod 256, and the cycle-minimum argument holds.
Simpler variant: the stopping-time tree on residues closes with maximal stopping time 8 and descent for every untrapped x >= 25, so the table shrinks from [1,129] to [1,24] (verified in `referee_tests.py`). This is the same method and the same tier. The "why not tier 1" is evidence only (as for up_ct35).
