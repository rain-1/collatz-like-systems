# desc_s32_plus9

**Rule.** Even n → n/2. For odd n, apply 3n+1 if n mod 32 ∈ S0 ∪ {9} = {1,3,5,7,9,11,13,15,17,21,23,25,29}. For n ≡ 19, 27, 31 (mod 32), apply n+1.
**Question (GLOBAL).** Is every positive orbit eventually periodic?
**Status.** OPEN. Tier 5. This system is one step past the certificate frontier of desc_s32_max.

## What is proved

**Proposition.** No descent certificate exists, for any M and any k.

*Proof.* The 2-adic rational y = −227/115 is periodic with period 12. Its residues mod 32 along the orbit are 15, 14, 7, 22, 11, 2, 1, 4, 18, 9, 28, 30. That is five 3n+1 steps (on 15, 7, 11, 1, 9) and seven halvings, so the multiplier is 3^5/2^7 = 243/128 > 1. All partial products from y are > 1, which is checked exactly. Lemma B applies. ∎

Compare with desc_s32_max. Its near-critical cycle has the same first six branches and the same five odd steps, but eight halvings (243/256). Switching class 9 from n+1 to 3n+1 removes one guaranteed halving from a nearby cycle. The maximal Lyapunov exponent then goes from −0.004 to positive, and certificates disappear.

The other one-class enlargements of S0 are also obstructed (checked):

| added class | periodic point | multiplier |
|---|---|---|
| 19 | −65/17 | 81/64 |
| 27 | −10 | 9/8 |
| 31 | −1 | 3/2 |

## Evidence (not proof)

* In the random model the drift is −0.833 per odd step, almost as contracting as S0 (−0.927).
* Every n ≤ 2·10^5 reaches 1.

So the heuristic expects GLOBAL = yes, and descent can provably never show it.

## Why lower tiers fail

* **Tier 2 descent:** impossible (proved).
* **Congruence invariants:** cannot give convergence.
* **Tier 3/4:** not found. The obstruction is a 12-periodic 2-adic orbit that mixes ×3 and ×1/2 steps. Any proof would have to control the integer orbits that shadow it for long stretches, which is the same difficulty as Collatz near its own 2-adic cycles. That puts it at tier 5 unless a new structural invariant exists.

## Check

`check_desc_s32_plus9.py` verifies the obstruction and the three other one-class obstructions. It also confirms that S0 itself is certifiable, and reports the drift and the simulation as evidence.

## Referee

**Verdict: OPEN (agreed). Final tier 5. The no-certificate proposition is confirmed.**

* I recomputed the orbit of −227/115 exactly from the table. It has period 12, residues 15, 14, 7, 22, 11, 2, 1, 4, 18, 9, 28, 30, and multiplier 243/128. The smallest partial product from that starting point is 3/2 > 1, so Lemma B applies. It also rules out the residue-weighted potentials that shortened desc_s32_max: the mod-32 graph contains this growing cycle.
* Simulation: all n < 3·10^5 reach 1. This is evidence only.
* Nothing at tier 3 was found by either party. The frontier statement is correct: S0 is certifiable (by a certificate, or by the potential in `referee_check.py`), and S0 ∪ {9} is obstructed.
