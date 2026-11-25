# up_tok3

**Rule.** even n -> n/2; n = 1 mod 4 -> n+3; n = 3 mod 4 -> n+4. Seed 37.
Perturbation of the trivial "n+3" descent map: the class 3 mod 4 is turned into a trap.

**Question.** Which n have infinite orbits?

**Answer (PROVED).** The orbit of n is finite (eventually in the cycle 1 -> 4 -> 2 -> 1) iff

    n = 2^a (4B+1) with a >= 0, B >= 0, and every maximal run of 0s in binary(B) has even length
    (the trailing run of 0s included; B = 0 allowed).

Equivalently, written MSB-first, binary(n) lies in the regular language  (1 (1 | 00)* 01 | 1) 0*.
All other n diverge (they reach 3 mod 4 and then increase by 4 forever). |E cap [1,2^k)| = F_{k+2} - 1
(Fibonacci; checked for k <= 16), so the finite-orbit set E has density 0 and the divergent set D has density 1.
Seed 37 = 4*9+1, 9 = 1001b: runs "00" even, so 37 is in E (orbit 37,40,20,10,5,8,4,2,1,...).

## Proof
*Trap:* n = 3 mod 4 -> n+4 = 3 mod 4 and larger, so the orbit is infinite.
Halving an even number never meets the trap, so n and its odd part m have the same fate; m = 3 mod 4 is
trapped at once. For m = 4B+1 the orbit is 4B+1 -> 4B+4 -> 2B+2 -> B+1 (intermediates even). Let Q(B) mean
"the orbit of B+1 never meets 3 mod 4". Then n is in E iff Q(B), and
- B = 0: B+1 = 1 -> 4 -> 2 -> 1 never meets 3 mod 4: Q(0) true.
- B = 2Y+1 (odd): B+1 = 2(Y+1) -> Y+1, so Q(B) = Q(Y).            [consume bit "1"]
- B = 4Z+2: B+1 = 4Z+3 is trapped, Q(B) false.                    [bits "01" from below: reject]
- B = 4Z, Z >= 1: B+1 = 4Z+1 -> 4Z+4 -> 2Z+2 -> Z+1, so Q(B) = Q(Z). [consume bits "00"]
In the last two recursive cases the argument strictly decreases, so the recursion terminates, and Q(B) holds iff
binary(B), read from the least significant bit, splits into tokens "1" and "00" up to its top bit; i.e. iff every
maximal 0-run of B has even length. Untrapped orbits reach 1, so they are eventually periodic, and the only cycle
outside the trap is (1 4 2). The recursion is literally a 2-state automaton (states "fresh" and "after 0") with a
reject sink, reading n LSB-first; reversing gives the MSB-first expression above.

## Tier: 3
The answer is a regular language, certified by a finite automaton in base 2.

**Why not tier 2 (proved).** A tier-2 answer is a finite union of residue classes, possibly corrected on a finite
table. Any such set is finite or has positive natural density. E is infinite (it contains all 2^a) and has
density 0: the number of B < 2^j with even 0-runs is at most the number of tilings of a length-j strip by
tiles of length 1 and 2, F_{j+1}, so |E cap [1,2^k)| <= sum_{j<=k} F_{j+1} = O(phi^k) = o(2^k). Likewise D has
density 1 but an infinite complement, so it is not a finite union of residue classes up to a finite set either. So neither E nor D has a congruence description.
Remark (general lemma, same proof): for any map whose non-trap branches are n -> n + d_r with fixed odd d_r,
plus halving, the state "current value = (unread high bits) + carry" has carry bounded by max d_r, so the
finite-orbit set is always regular. E.g. n+7 instead of n+3 gives a 7-state LSB-first Nerode count (computed,
suffix length <= 10, 10-bit extension window). Multiplier-1 traps can therefore give tier 2 (if an invariant
makes the answer periodic, cf. up_qr7) or tier 3, never worse.

## Check
`check_up_tok3.py`: the three recursion identities for B < 50000, trap invariance, rule == simulation for all
n < 2^18, the counts F_{k+2}-1 and decreasing density. PASS.

## Referee
**Verdict: CONFIRMED (the answer and the proof). Final tier: 3 (agreed, with a caveat).**
The recursion identities hold, recursion termination is fine (B -> Y or Z, both strictly smaller), and the token reading is right. Independent test: the MSB regex `(1(1|00)*01|1)0*` agrees with a memoized simulation for all n < 2^21, and the count F_{k+2}-1 holds for k <= 21. That count is only checked, but nothing depends on it. The tiling upper bound used in the density argument is proved.
Tier caveat: the *method* is elementary. It is a residue-mod-4 recursion that descends on B with base case B = 0, i.e. tier-1/2 machinery. Tier 3 is earned only by the *form of the answer*: a 2-state automaton. The why-not-tier-2 argument is a real proof, but only against a *congruence* description (an infinite density-0 set is not a finite union of residue classes up to a finite set). It does not exclude other tier-2 methods.
**Consistency issue (lens-wide):** if this question accepted "the trap basin, decided in O(log n) steps" as its answer, as up_ct11/35/58 do, it would be tier 1, because n+3 with halving descends. If up_ct11 had to give a closed description, as here, it would be OPEN. The census should pick one standard. I suggest stating tok3's question as BASIN-with-closed-form and the ct* questions as GLOBAL ("divergent set = trap basin").
The general "bounded carry implies regular" lemma is only sketched. I checked the sketch for odd d_r: current value = unread high part + carry, carry <= (c+1)/2 + max d, lookahead mod 2^e for the branch, and a guessed odd-modulus residue. It is plausible and I believe it is correct, but it is not written out. The claim in the lens summary that an exhaustive mod-8 search found no congruence answer is unverified (no script ships it).
