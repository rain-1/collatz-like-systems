# auto_sfx7_far

**Map.** The same seven-rule binary suffix permutation as auto_sfx7_s17.
**Seed.** y = 2^21 + 5 = 2097157.
**Question.** FATE of y. Side question: the size of the smallest automaton certificate.

**Answer.** Infinite. **Status:** PROVED. **Tier:** 2. The smallest binary automaton certificate has between 10 and 29 states. The lower bound is proved by hand, and the general family bound is proved below.

## Proof of FATE (tier 2)

y lies on the backward orbit of 17, and T^44(y) = 17 (finite computation).

Backward closed form: for m ≥ 2 the inverse rules send 1 0^m 101 → 1 0^m 1010 → 1 0^m 111 → 1 0^m 1110 → 1 0^(m+2) 101. This is checked symbolically on the visible suffix. Hence x_(−4i−4) = 2^(2i+1)+5, x_(−4i−5) = 2^(2i+2)+10, x_(−4i−6) = 2^(2i+1)+7 and x_(−4i−7) = 2^(2i+2)+14 for i ≥ 1, and y = x_(−44).

Certificate: C = (classes 81, 83, 162, 166, 209, 211 mod 256) ∪ {T(y), …, T^44(y)}. This is a congruence plus a finite table of 44 entries. Closure follows because the classes are closed (auto_sfx7_s17) and the finite part is an orbit segment ending at 17, with T(17) = 166 in the classes. Also y ≡ 5 (mod 256) and y is not in the segment. The check verifies closure of C exactly. Injectivity then gives an infinite orbit.

## Lower bound: every certificate has ≥ 10 states

**General statement.** For y_I = 2^(2I+1)+5 (I ≥ 2), every automaton certificate (MSB-first binary, arbitrary behaviour on leading zeros) has at least I states.

*Proof.* Take the words w_a = 1 0^(2a) for 0 ≤ a < I. For a < b let z = 0^(2(I−1−b)) 1110. Then w_b z = 2^(2I+2)+14 = x_(−4I−7). This point comes strictly before y_I = x_(−4I−4) in time, so it reaches y_I and every certificate must reject it. Next, w_a z = 2^(2i+2)+14 with i = I − (b−a), and 1 ≤ i ≤ I−1, so it equals x_(−4i−7). This point comes strictly after y_I, so it is a forward iterate of y_I and every certificate must accept it. If w_a and w_b reached the same state, so would w_a z and w_b z. □

The check verifies the size-10 instance (I = 10) by exact orbit membership.

## Upper bounds

* The exact forward-orbit automaton from suffix_orbit.exact_dfa, minimised, has **29 states** and is a verified certificate.
* The tier-2 set C above needs 36 states as a minimal DFA.

The exact minimum lies in [10, 29]. The SAT search was too slow at this size, so the gap is reported as is.

## Why lower tiers fail / what this shows

* Tier 1 fails for the same reasons as auto_sfx7_s17 (non-monotone in both time directions, no small modulus). Tier 2 holds.
* The point of this entry: the size of the smallest automaton certificate is unbounded along one orbit of a fixed 7-rule map (≥ I for y_I), while the difficulty tier stays 2. The size measures how far back on the orbit the seed sits (the certificate must count zeros), not proof difficulty. This is the non-monotone analogue of the k+2 family in suffix_orbit_theorem.pdf p.3.

## Referee

**Verdict:** the answer is CONFIRMED (infinite), and the fooling-set bound is CONFIRMED. The tier is LOWERED from 2 to **1**.

I checked T^44(2^21+5) = 17 independently, and the backward closed form for i = 1..10. I re-verified the fooling set from raw orbit sets: 2000 forward and 200 backward iterates (referee_check.py, R4 and R5).

The general proof that y_I needs at least I states is correct. w_b z = 2^(2I+2)+14 = x_(−4I−7) lies strictly before y_I, so every certificate rejects it. w_a z = x_(−4i−7) with 1 ≤ i ≤ I−1 lies strictly after y_I, so every certificate accepts it. The condition i ≥ 1 is needed for the closed form, and it holds.

The upper bound of 29 states is verified by an exact closure test. The minimum within [10, 29] was not settled, and the md reports this honestly.

**Tier-1 proof.** T^44(y) = 17 by direct computation. Then, by the referee proof in auto_sfx7_s17.md, T^(46+4k)(y) = (256·4^k − 7)/3 is strictly increasing. So the orbit is infinite. This is a finite simulation plus a tier-1 lemma, so tier 1.

The lens's main point stands, and is in fact strengthened: certificate size is unbounded along one orbit while the tier stays fixed, now at 1.

**Final tier: 1.**
