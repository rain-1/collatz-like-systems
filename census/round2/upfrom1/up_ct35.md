# up_ct35

**Rule.** n = 7 mod 8 -> n+8; n = 27 mod 32 -> n+32 (two traps); otherwise accelerated Collatz T. Seed 27 (trap).
In terms of T-parity words: n = 7 mod 8 iff the word of n starts 111; n = 27 mod 32 iff it starts 11011.

**Question.** Which n have infinite orbits?

**Answer (PROVED).** Exactly those whose T-orbit meets 7 mod 8 or 27 mod 32 before reaching 1. Every other orbit
reaches (1 2); no other cycles, no untrapped divergence.

## Proof
1. *Traps* are invariant and increasing, so trapped orbits are infinite.
2. *Parity lemma* (standard): the first k parities of the T-orbit of x depend only on x mod 2^k (bijectively).
   Checked for the two traps: x = 7 mod 8 <=> word starts 111; x = 27 mod 32 <=> 5-word = 11011.
3. Let (x_t) be an orbit that is never trapped. Then S = T along it, and its parity sequence p has no 111 starting at
   any t and no 11011 starting at any t. *Word lemma:* a 5-letter word with >= 4 ones is 11111, 01111, 10111,
   11101, 11110 (all contain 111) or 11011. Hence every window p_t..p_{t+4} has at most 3 ones.
4. *Affine bound.* For a parity word w of length 5, x_{t+5} = (3^k x_t + b_w)/32 with k = #ones <= 3; over all 5-words
   avoiding 111 and != 11011 the maximum of b_w is 58 (exhaustive). So x_{t+5} <= (27 x_t + 58)/32, which is < x_t
   for x_t >= 12 and <= 11 for x_t <= 11.
5. Hence x_{5j} decreases until it is <= 11 and then stays <= 11: the orbit is bounded, so eventually periodic.
   On a cycle not every element is >= 12 (else x_{t+5} < x_t all around the cycle), so every untrapped cycle meets
   [1,11]. Finite table: from 1..11, the untrapped orbits all end in (1 2) (7 and 9 -> 14 -> 7 are trapped).

## Tier: 2
Descent inequality on 5-step windows (from a forbidden-word lemma) plus an exhaustive finite table.

**Why not tier 1 (proved part + evidence).** Proved: no window shorter than 5 contracts. Untrapped stretches with
parity words 1, 11, 110, 1101 exist (check script exhibits them), with multipliers 3/2, 9/4, 9/8, 27/16, all > 1,
so no one-step monotonicity or block of length <= 4 gives descent. Evidence: a tier-1 argument would have to
replace the window lemma + table; I know none. Generalization (proved by the same argument): trapping every
residue mod 2^L whose L-word has more than k ones gives tier 2 whenever 3^k < 2^L; see up_ct58.

## Check
`check_up_ct35.py`: parity lemma on all residues mod 32, the word lemma, b_max = 58, the descent constants, the
5-step inequality directly on n < 100000, the four expanding short windows, and fate of all n < 400000. PASS.

## Referee
**Verdict: CONFIRMED. Final tier: 2 (agreed; it sits at the 1/2 boundary).**
I re-derived the proof. The word lemma holds (the only 5-word with >= 4 ones avoiding 111 is 11011). S = T along a never-trapped orbit, so the window words are T-words. b_max = 58, the threshold is 12, the [1,11] bound holds, and the argument that the cycle minimum is <= 11 is correct. The table [1,11] is correct (7 and 9 trapped, the rest reach 1).
Simpler proof (same tier): a Terras stopping-time tree on residues mod 32. Untrapped words are 0 | 10 | 1100 | 11010 (110 and 1101 continue, 11011 and 111 are trapped). The stopping inequalities are x/2 < x; (3x+1)/4 < x; (9x+5)/16 < x; (27x+23)/32 < x for x >= 5. So every untrapped x >= 5 descends within 5 steps, and the table shrinks to [1,4] (verified in `referee_tests.py`). This is still a residue case analysis plus a table, i.e. tier 2. It is literally the same method as up_ct11's tier-1 proof with depth 5 instead of 2. The "why not tier 1" is evidence only: it rules out short uniform windows, not a variable-length stopping argument, and that argument does work. So whether this is tier 1 or 2 is a matter of size, not of kind.
