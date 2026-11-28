# The blocked mixed-base system: normal form and why it is not an easy case (28 Nov 2026)

System (round 3 `mixedbase`, left open there): n = 26 mod 27 -> (n+1)/27; else even n -> n/2;
else n -> (3n+1)/2. Written outside the prover/referee loop; not refereed. `explore.c` plus the
inline checks reproduce the numbers.

**Outcome: NOT SETTLED.** The system is not a rigid case. It reduces to a split-type map with
expanding slope 9/8, the same kind of problem as split5_3.

## Normal form (PROVED by direct computation; checked for n < 200000)

Put u = n + 1. Then: 27 | u -> u/27 + 1; else u even -> 3u/2; else u odd -> (u+1)/2.
Three consecutive steps 3u/2 make the value divisible by 27, and the next step divides by 27,
so a run of three expansions has net slope 1/8. Growth is possible only through the block
"expand, expand, halve": for u = 4 mod 8 with 3 not dividing u,

    u -> (9u + 4)/8,   and with w = u + 4 = n + 5:   w = 0 mod 8 -> 9w/8.

The other clean block is "expand, halve" on u = 2 mod 4: u -> (3u + 2)/4 (slope 3/4). After
either block the value is 2 mod 3, so divisibility by 3 never interferes while the orbit uses
only these two blocks. The expanding fixed point is w = 0 (n = -5), and the cycle -5, -7, -10
is this block. So the system is, on the states that matter, the unit-multiplier 2-adic map
"w = 0 mod 8 -> 9w/8" with contracting exits: split5_3 with (9, 8) in place of (5, 4).

## It has free choices (EVIDENCE for the numbers; the mechanism is exact)

A path stays at or above its start if it uses the block of slope 9/8 often enough; for example
three such blocks followed by one block of slope 3/4 has net slope 1.068, and this pattern can
be mixed freely with four expanding blocks. So the set of surviving words has positive entropy.
Measured on all starts below 2^32: the proportion not yet dropped after b halvings decays like
2^{-0.726 b}, so the dimension of the non-descending set is about 0.27 and the critical constant
of the count law is about 1.38. The largest observed (halvings before first drop)/log2 n is 1.38.
The only start below 3*10^5 that never goes below itself is n = 1.

## Consequences

* My suggestion that this system might be settled by the shift-and-subtract cutoff, because its
  only obstruction is one cycle, was wrong. A small gap between the tail exponent and the run
  exponent does not mean that survivors have few choices.
* Everything proved for split5_3 should port with (2, 3) as the primes and rate
  kappa = 1/log2(9/8) = 5.885: the count law a little past the digits, the chain theorem (an
  escaping orbit would force at least 5 linked permanent survivors per octave, since
  (9/8)^5 < 2 < (9/8)^6), and the cutoffs for rigid schedules. None of that settles it.
* What would settle it is the count law at depth about 1.38 log2 n, i.e. 0.38 log2 n halvings
  beyond the digits. That is a smaller multiple than for split5_3 (1.4) but still linear.
