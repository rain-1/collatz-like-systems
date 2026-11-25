# up_ct3

**Rule.** n = 7 mod 8 -> n+8 (trap); otherwise accelerated Collatz T. Seed 27 (27 -> 41 -> 62 -> 31, trapped). One trap class removed from up_ct35.

**Question.** Which n have infinite orbits? (Is it exactly the trap basin, i.e. is every untrapped orbit
eventually periodic, and is (1 2) the only untrapped cycle?)

**Answer: OPEN.** Conjecturally yes (it follows from the Collatz conjecture), but I cannot prove it and know no
technique that does.

## What is proved / known
- Trapped orbits are infinite (trap invariant, increasing).
- Every n <= 2^68 is trapped or reaches 1: this follows from the computational verification that all such n reach 1
  under Collatz (D. Barina, "Convergence verification of the Collatz problem", J. Supercomputing 77 (2021),
  2681-2688, verification bound 2^68). The check script verifies n < 10^6 directly.
- An untrapped divergent orbit would be a divergent Collatz orbit whose parity sequence avoids 111, i.e. has every
  run of odd steps of length <= 2.

## Why every method on the ladder fails here (proved)
- The descent/window method of up_ct35/up_ct58 needs a window length L and a bound k on ones with 3^k < 2^L.
  Words avoiding 111 can have ones-density 2/3 > log 2/log 3: for every j the residue class mod 2^{3j} with word
  (110)^j is untrapped for its whole 3j steps and multiplies by (9/8)^j -> infinity (check script exhibits it for
  j <= 14). So no window, of any length, contracts uniformly, and no finite table can close the argument.
- No congruence / finite-automaton argument can rule the growth pattern out: every finite parity word is realized by
  a residue class, and the infinite expanding pattern (110)^infinity is realized by an actual untrapped T-cycle on the
  negative integers, -5 -> -7 -> -10 -> -5 (multiplier 9/8 per period, balanced by the additive terms). Arguments
  that see only residues apply equally to the 2-adic integer -5, so the obstacle is integrality + positivity of a
  non-periodic orbit - exactly the Collatz obstacle.
- Cycle question: an untrapped cycle with K odd steps among L steps needs 2^L > 3^K (positivity) and the density
  K/L is not excluded by the 111-ban (allowed up to 2/3). Known no-m-cycle results (Simons-de Weger 2005; C. Hercher,
  J. Integer Sequences 26 (2023) Art. 23.3.5: no m-cycles for m <= 91, m = number of odd runs) bound runs, not run lengths, so they do not settle it either.

## Tier: 5
Threshold phenomenon (the main finding of this lens): with traps "parity word contains too many ones in a window",
the problem is tier 1-2 exactly when the trap-free shift has maximal ones-density < log 2/log 3, and becomes a
Collatz-type open problem when that density exceeds it. up_ct58 (density 0.625, PROVED) and up_ct3 (density 0.667,
OPEN) straddle the threshold 0.6309.

## Check
`check_up_ct3.py`: fate of all n < 10^6 (trapped or reaches (1 2)); for j <= 14 an untrapped (110)^j stretch;
the negative cycle -5 -> -7 -> -10. PASS (the computational part only; the question itself is open).

## Referee
**Verdict: OPEN, agreed. Final tier: 5.**
I checked: the fate of n < 10^6; the (110)^j stretches (the lift step in the check is valid because each of the 8 lifts carries a distinct word); and the negative cycle -5 -> -7 -> -10 (residues 3, 1, even mod 8, so untrapped). The citations are real and correctly applied: Barina, J. Supercomput. 77 (2021) 2681-2688, 2^68. Untrapped orbits are Collatz orbits, so the reduction is exact. Hercher's m-cycle bound counts odd runs, as the explorer says. The stopping-time tree does not close either: 103 open branches remain at depth 30 (`referee_tests.py`).
I could not finish it. A divergent untrapped orbit has parity density in [log2/log3, 2/3] with odd runs <= 2. I know no technique that excludes it.
**Correction to the lens's threshold claim:** density > log2/log3 kills the *window/stopping-time method*. It does NOT by itself make a trap system open. Counterexample: trap evens (n -> n+2) and odd n -> (3n+1)/2. The allowed shift is {1^inf}, density 1, and the window method fails (2^L - 1 stays untrapped for L steps, multiplier (3/2)^L). Yet every n >= 1 is trapped within log2(n+1) steps, because n's T-word starts with 1^L iff n = -1 mod 2^L. That is tier 1. So log2/log3 is a sharp edge for the descent method, not for provability. Openness of up_ct3 comes from the allowed shift being rich (positive entropy, with many words above the threshold), not from density alone.
