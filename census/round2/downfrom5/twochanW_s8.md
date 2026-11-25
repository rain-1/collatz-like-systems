# twochanW_s8

**Rule (a permutation of Z_{>0}).**

| input class | output | output class |
|---|---|---|
| n = 1 (mod 6) | 4n+1 | 5 (mod 24) |
| n = 3 (mod 6) | 4n+5 | 17 (mod 24) |
| n = 5 (mod 6) | (2n-1)/3 | 3 (mod 4) |
| n = 0 (mod 4) | n/2 | evens |
| n = 2 (mod 8) | (3n-4)/2 | 1 (mod 12) |
| n = 6 (mod 8) | 3n/2 | 9 (mod 12) |

Each branch sends the k-th element of its input class to the k-th element of its output class. Both columns of classes partition Z, so P is a bijection (checked exactly).

**Where it comes from.** On the odd numbers n = 2m-1, P is the map W(m) = T(m) if 3 | m and W(m) = 3T(m) otherwise: P(2m-1) = 2W(m) - 1. In words, W is the 1932 map with every rising output multiplied by 3. Its acceleration to the next non-multiple of 3 is exactly twice T's: W_acc(m) = 2 T_acc(m). W misses the numbers coprime to 6. The even channel (4k -> 2k; 4k+2 -> those missing odd encodings) feeds them in and makes P bijective.

**Question (FATE).** What is the fate of the seed 8?

| answer | status | tier |
|---|---|---|
| infinite, with infinitely many rises and falls and a non-eventually-periodic branch itinerary | PROVED | 1 |

## Proof

1. *Trap.* Let S = odd ∪ {2 mod 4} ∪ {4 mod 8}. Odd inputs give odd outputs, the class 2 (mod 4) maps into odds, and 4 (mod 8) maps to 2 (mod 4). So P(S) ⊆ S. Also 8 is not in S and P(8) = 4 is in S. By injectivity the orbit of 8 never returns, so it is infinite. The orbit begins 8, 4, 2, 1, 5, 3, 17, 11, 7, ...
2. *Forced falls.* On the odds, the rising branches send n = 1 (mod 6) to 24j+5 and n = 3 (mod 6) to 24j+17. Both outputs are 5 (mod 6), which is the falling branch (2n-1)/3 < n. So after step 3 every rise is followed by a fall.
3. *Infinitely many rises.* An infinite orbit of distinct positive integers is unbounded.
4. *Non-periodic itinerary.* The slopes are 4 (rises) and 2/3 (falls). Every period word contains a fall, because a rise is never followed by a rise. So the composite slope 4^a (2/3)^b has b >= 1 and denominator 3^b. The lemma in swT9_15_s8.md excludes an eventually periodic itinerary for an infinite orbit.

After a rise from m (with 3 not dividing m), the run of falls has length exactly v_3(3T(m)) = v_3(4m -+ 1) >= 1, so the orbit's own 3-adic arithmetic chooses it. The rise/fall pattern is therefore not enslaved to a monotone return map, unlike the examples in more_orbit_certificates.pdf. Whether the sign word itself is eventually periodic is not settled here.

## Tier 1, and the lesson

Every step uses only a 2-adic valuation trap and a mod-6 forcing check, so this is tier 1, not tier 2. Tier 0 cannot prove an infinite orbit.

**What we learn.** Infinitude, infinitely many rises and falls, and a non-periodic itinerary all come cheaply once the T-like dynamics run on a channel that is not surjected: W has non-image points. For a permutation, the price is a second channel to feed those points in. That is the gap between this example and T, where no such channel exists.

Check: `check_twochanW_s8.py` (exit 0).

## Referee

**Verdict: CONFIRMED, tier 1 (agreed).**

Re-derivation:
- Bijection: the output classes 5 mod 24, 17 mod 24, 3 mod 4, evens, 1 mod 12 and 9 mod 12 tile Z, and each branch is order-preserving onto a full tail. `referee_check.py` checks injectivity for n < 2·10^5 and surjectivity onto [1, 10^5].
- The trap is literally S = {v_2(n) ≤ 2}. One has v_2(P(n)) = v_2(n) - 1 when v_2(n) ≥ 2, and 0 otherwise. Along the orbit, v_2 runs 3, 2, 1, 0, 0, ..., so this is genuine valuation bookkeeping, consistent with tier 1.
- Rises from classes 1 and 3 (mod 6) land in class 5 (mod 6), so every rise is followed by a fall.
- Unboundedness gives infinitely many rises, and therefore infinitely many falls.
- Every period word contains a fall, so the lemma gives a non-periodic itinerary.
- The fall-run length v_3(4m ∓ 1) is also correct.
