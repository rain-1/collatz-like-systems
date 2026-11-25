# Census of Collatz-like systems, ranked by difficulty

Generated from round1.json and round2.json. Tiers are the referee's final tiers. Every proof is in results/<id>.md (round 1) or round2/<lens>/<id>.md, with a check script alongside. All proofs are agent-written and agent-refereed; none has had human review.

| tier | questions |
|---|---|
| Tier 0: direct simulation | 43 |
| Tier 1: elementary argument | 54 |
| Tier 2: congruence invariant or descent plus finite table | 12 |
| Tier 3: finite-state / structural certificate | 2 |
| Tier 4: substantial published theorem or long machine certificate | 2 |
| Tier 5: open | 66 |

## Tier 0: direct simulation

- **div235_7n1_s11** (round1) — 2|n -> n/2; else 3|n -> n/3; else 5|n -> n/5; else 7n+1. *FATE of seed* → other-cycle. 
- **div23_5n1_s7** (round1) — 2|n -> n/2; else 3|n -> n/3; else 5n+1. *FATE of seed* → other-cycle. 
- **div23_7n1_s5** (round1) — 2|n -> n/2; else 3|n -> n/3; else 7n+1. *FATE of seed* → other-cycle. 
- **farkas_s27** (round1) — 1 -> 1; n=1 mod 3 -> (n-1)/3; else even -> n/2; else -> (3n+1)/2. *FATE of seed* → other-cycle. 
- **m3_a_s100** (round1) — 3|n -> n/3; n=1 -> (2n+1)/3; n=2 -> (2n+2)/3. *FATE of seed* → other-cycle. 
- **m3_b_s8** (round1) — 3|n -> n/3; n=1 -> (4n-1)/3; n=2 -> (4n+1)/3. *FATE of seed* → other-cycle. 
- **m3_c_s100** (round1) — 3|n -> n/3; n=1 -> 2n+1; n=2 -> 2n+2. *FATE of seed* → other-cycle. 
- **m3_d_s7** (round1) — 3|n -> n/3; n=1 -> 4n+2; n=2 -> 4n+1. *FATE of seed* → returns. 
- **m3_f_s100** (round1) — 3|n -> n/3; n=1 -> n+2; n=2 -> n+1. *FATE of seed* → other-cycle. 
- **m3_g_s7** (round1) — 3|n -> n/3; n=1 -> 5n+1; n=2 -> 5n+2. *FATE of seed* → returns. 
- **par_1_1_s27** (round1) — even n -> n/2; odd n -> 1n+1. *FATE of seed* → other-cycle. 
- **par_1_5_s27** (round1) — even n -> n/2; odd n -> 1n+5. *FATE of seed* → other-cycle. 
- **par_3_13_s27** (round1) — even n -> n/2; odd n -> 3n+13. *FATE of seed* → other-cycle. 
- **par_3_17_s27** (round1) — even n -> n/2; odd n -> 3n+17. *FATE of seed* → other-cycle. 
- **par_3_1_s27** (round1) — even n -> n/2; odd n -> 3n+1. *FATE of seed* → other-cycle. 
- **par_3_3_s27** (round1) — even n -> n/2; odd n -> 3n+3. *FATE of seed* → other-cycle. 
- **par_3_5_s27** (round1) — even n -> n/2; odd n -> 3n+5. *FATE of seed* → other-cycle. 
- **par_3_7_s27** (round1) — even n -> n/2; odd n -> 3n+7. *FATE of seed* → other-cycle. 
- **par_3_9_s27** (round1) — even n -> n/2; odd n -> 3n+9. *FATE of seed* → other-cycle. 
- **par_3_m1_s27** (round1) — even n -> n/2; odd n -> 3n-1. *FATE of seed* → other-cycle. 
- **par_5_131_s27** (round1) — even n -> n/2; odd n -> 5n+131. *FATE of seed* → returns. 
- **par_5_1_s5** (round1) — even n -> n/2; odd n -> 5n+1. *FATE of seed* → other-cycle. 
- **par_5_353_s27** (round1) — even n -> n/2; odd n -> 5n+353. *FATE of seed* → other-cycle. 
- **par_5_7_s27** (round1) — even n -> n/2; odd n -> 5n+7. *FATE of seed* → other-cycle. 
- **par_6_2_s27** (round1) — even n -> n/2; odd n -> 6n+2. *FATE of seed* → other-cycle. 
- **par_7_1_s1** (round1) — even n -> n/2; odd n -> 7n+1. *FATE of seed* → returns. 
- **par_7_7_s9** (round1) — even n -> n/2; odd n -> 7n+7. *FATE of seed* → other-cycle. 
- **perm_1932_s44** (round1) — 3q->2q; 3q+1->4q+1; 3q+2->4q+3. *FATE of seed* → returns. 
- **perm_c_s8** (round1) — 2q->3q; 4q+1->3q+2; 4q+3->3q+1. *FATE of seed* → returns. 
- **perm_d_s3** (round1) — 2q->5q; 8q+1->5q+1; 8q+3->5q+2; 8q+5->5q+3; 8q+7->5q+4. *FATE of seed* → returns. 
- **perm_flip_s27** (round1) — 2q+1 -> 2q+2; 2q+2 -> 2q+1. *FATE of seed* → returns. 
- **perm_suffix_c_s1** (round1) — 4q->2q; 4q+2->4q+3; 2q+1->4q+1. *FATE of seed* → returns. 
- **perm_suffix_d_s1** (round1) — 2q->8q; 4q+1->2q+1; 8q+3->4q+2; 8q+7->8q+4. *FATE of seed* → returns. 
- **perm_swap_s8** (round1) — 3q->2q; 3q+1->4q+3; 3q+2->4q+1. *FATE of seed* → returns. 
- **split5_1_s27** (round1) — even n -> n/2; n=1 mod 4 -> 5n+1; n=3 mod 4 -> n+1. *FATE of seed* → other-cycle. 
- **split5_3_s27** (round1) — even n -> n/2; n=1 mod 4 -> 5n+3; n=3 mod 4 -> n+3. *FATE of seed* → other-cycle. 
- **splitB_71_s27** (round1) — even n -> n/2; n=1 mod 4 -> n+71; n=3 mod 4 -> 3n+71. *FATE of seed* → other-cycle. 
- **splitB_7_s27** (round1) — even n -> n/2; n=1 mod 4 -> n+7; n=3 mod 4 -> 3n+7. *FATE of seed* → other-cycle. 
- **split_13_s27** (round1) — even n -> n/2; n=1 mod 4 -> 3n+13; n=3 mod 4 -> n+13. *FATE of seed* → other-cycle. 
- **split_5_s27** (round1) — even n -> n/2; n=1 mod 4 -> 3n+5; n=3 mod 4 -> n+5. *FATE of seed* → other-cycle. 
- **split_7081_s27** (round1) — even n -> n/2; n=1 mod 4 -> 3n+7081; n=3 mod 4 -> n+7081. *FATE of seed* → other-cycle. 
- **split_73_s27** (round1) — even n -> n/2; n=1 mod 4 -> 3n+73; n=3 mod 4 -> n+73. *FATE of seed* → other-cycle. 
- **split_97_s27** (round1) — even n -> n/2; n=1 mod 4 -> 3n+97; n=3 mod 4 -> n+97. *FATE of seed* → other-cycle. 

## Tier 1: elementary argument

- **div2_3n_s5** (round1) — 2|n -> n/2; else 3n. *FATE of seed* → infinite. 
- **div2_3n_s5** (round1) — 2|n -> n/2; else 3n. *GLOBAL* → no. 
- **div3_2n_s5** (round1) — 3|n -> n/3; else 2n. *FATE of seed* → infinite. 
- **div3_2n_s5** (round1) — 3|n -> n/3; else 2n. *GLOBAL* → no. 
- **farkas_s27** (round1) — 1 -> 1; n=1 mod 3 -> (n-1)/3; else even -> n/2; else -> (3n+1)/2. *GLOBAL* → yes. 
- **m3_a_s100** (round1) — 3|n -> n/3; n=1 -> (2n+1)/3; n=2 -> (2n+2)/3. *GLOBAL* → yes. 
- **m3_c_s100** (round1) — 3|n -> n/3; n=1 -> 2n+1; n=2 -> 2n+2. *GLOBAL* → yes. 
- **m3_f_s100** (round1) — 3|n -> n/3; n=1 -> n+2; n=2 -> n+1. *GLOBAL* → yes. 
- **mahler_s1** (round1) — even n -> 3n/2; odd n -> (3n+1)/2. *FATE of seed* → infinite. 
- **mahler_s1** (round1) — even n -> 3n/2; odd n -> (3n+1)/2. *GLOBAL* → no. 
- **par_1_1_s27** (round1) — even n -> n/2; odd n -> 1n+1. *GLOBAL* → yes. 
- **par_1_5_s27** (round1) — even n -> n/2; odd n -> 1n+5. *GLOBAL* → yes. 
- **par_2_1_s27** (round1) — even n -> n/2; odd n -> 2n+1. *FATE of seed* → infinite. 
- **par_2_1_s27** (round1) — even n -> n/2; odd n -> 2n+1. *GLOBAL* → no. 
- **par_3_2_s27** (round1) — even n -> n/2; odd n -> 3n+2. *FATE of seed* → infinite. 
- **par_3_2_s27** (round1) — even n -> n/2; odd n -> 3n+2. *GLOBAL* → no. 
- **par_3_4_s27** (round1) — even n -> n/2; odd n -> 3n+4. *FATE of seed* → infinite. 
- **par_3_4_s27** (round1) — even n -> n/2; odd n -> 3n+4. *GLOBAL* → no. 
- **par_4_2_s27** (round1) — even n -> n/2; odd n -> 4n+2. *FATE of seed* → infinite. 
- **par_4_2_s27** (round1) — even n -> n/2; odd n -> 4n+2. *GLOBAL* → no. 
- **par_5_2_s27** (round1) — even n -> n/2; odd n -> 5n+2. *FATE of seed* → infinite. 
- **par_5_2_s27** (round1) — even n -> n/2; odd n -> 5n+2. *GLOBAL* → no. 
- **par_6_3_s27** (round1) — even n -> n/2; odd n -> 6n+3. *FATE of seed* → infinite. 
- **par_6_3_s27** (round1) — even n -> n/2; odd n -> 6n+3. *GLOBAL* → no. 
- **perm_ceil2_s1** (round1) — 2m->2(m+ceil(m/2)); 4q+1->2(3q+1); 4q+3->2q+1. *FATE of seed* → infinite. 
- **perm_ceil2_s1** (round1) — 2m->2(m+ceil(m/2)); 4q+1->2(3q+1); 4q+3->2q+1. *GLOBAL* → no. 
- **perm_ceil3_s1** (round1) — 2m->2(m+ceil(m/3)); 4q+1->2(4q+1); 4q+3->2q+1. *FATE of seed* → infinite. 
- **perm_ceil3_s1** (round1) — 2m->2(m+ceil(m/3)); 4q+1->2(4q+1); 4q+3->2q+1. *GLOBAL* → no. 
- **perm_flip_s27** (round1) — 2q+1 -> 2q+2; 2q+2 -> 2q+1. *GLOBAL* → yes. 
- **perm_suffix_a_s1** (round1) — 2q->4q; 4q+1->4q+2; 4q+3->2q+1. *FATE of seed* → infinite. 
- **perm_suffix_a_s1** (round1) — 2q->4q; 4q+1->4q+2; 4q+3->2q+1. *GLOBAL* → no. 
- **perm_suffix_b_s8** (round1) — 2q+1->16q+12; 8q+4->2q+1; 4q+2->4q+2; 16q->8q; 16q+8->16q+4. *FATE of seed* → infinite. 
- **perm_suffix_b_s8** (round1) — 2q+1->16q+12; 8q+4->2q+1; 4q+2->4q+2; 16q->8q; 16q+8->16q+4. *GLOBAL* → no. 
- **perm_suffix_c_s1** (round1) — 4q->2q; 4q+2->4q+3; 2q+1->4q+1. *GLOBAL* → no. 
- **perm_suffix_d_s1** (round1) — 2q->8q; 4q+1->2q+1; 8q+3->4q+2; 8q+7->8q+4. *GLOBAL* → no. 
- **splitB_71_s27** (round1) — even n -> n/2; n=1 mod 4 -> n+71; n=3 mod 4 -> 3n+71. *GLOBAL* → yes. 
- **splitB_7_s27** (round1) — even n -> n/2; n=1 mod 4 -> n+7; n=3 mod 4 -> 3n+7. *GLOBAL* → yes. 
- **split_13_s27** (round1) — even n -> n/2; n=1 mod 4 -> 3n+13; n=3 mod 4 -> n+13. *GLOBAL* → yes. 
- **split_5_s27** (round1) — even n -> n/2; n=1 mod 4 -> 3n+5; n=3 mod 4 -> n+5. *GLOBAL* → yes. 
- **split_7081_s27** (round1) — even n -> n/2; n=1 mod 4 -> 3n+7081; n=3 mod 4 -> n+7081. *GLOBAL* → yes. 
- **split_73_s27** (round1) — even n -> n/2; n=1 mod 4 -> 3n+73; n=3 mod 4 -> n+73. *GLOBAL* → yes. 
- **split_97_s27** (round1) — even n -> n/2; n=1 mod 4 -> 3n+97; n=3 mod 4 -> n+97. *GLOBAL* → yes. 
- **auto_mix3_s7** (round2/automata) — 6|n -> n/2; n=2 mod 6 -> (3n+2)/2; n=4 mod 12 -> (3n-8)/4; n=10 mod 12 -> (3n-2)/4; n odd -> (3n+1)/2 (a permu. *FATE of 7* → Infinite. The forward orbit looks chaotic. The smallest base-3 certificate has exactly 7 states (SAT). The smallest base-2 certificate has between 10 (SAT: none. 
- **auto_sfx7_far** (round2/automata) — same 7-rule suffix permutation as auto_sfx7_s17. *FATE of 2^21+5 (side question: size of the smallest automaton certificate)* → Infinite. The smallest binary automaton certificate has between 10 and 29 states. More generally, the seed 2^(2I+1)+5 needs at least I states.. 
- **auto_sfx7_s17** (round2/automata) — Binary suffix permutation ..00->..00, ..001->..100110, ..00101->..1110, ..10->..1, ..10101->..10110, ..11->..0. *FATE of 17* → Infinite. The orbit rises and falls in every period in both time directions. The smallest automaton certificate has exactly 5 states. The smallest congruence ce. 
- **desc_s8_35** (round2/descent) — even n -> n/2; n=3,5 mod 8 -> 3n+1; n=1,7 mod 8 -> n+1. *GLOBAL: is every positive orbit eventually periodic?* → yes; every orbit reaches the cycle {1,2}. 
- **shiftT_s8** (round2/downfrom5) — J: 3q->2q+2 (q>=1); 3q+1->4q+1; 3q+2->4q+3 (T with one constant changed; J-T ∈ {0,2}; injective, not surjectiv. *FATE of seed 8* → Infinite. 
- **swT3_9_15_s8** (round2/downfrom5) — Q(n)=sigma(T(n)) with sigma swapping 3<->4 (mod 6); |Q-T|<=1, Q is a permutation. *FATE of seed 8* → Infinite; the orbit is strictly increasing. Also the only cycle of Q is {1}.. 
- **twochanW_s8** (round2/downfrom5) — n≡1 (6)->4n+1; n≡3 (6)->4n+5; n≡5 (6)->(2n-1)/3; n≡0 (4)->n/2; n≡2 (8)->(3n-4)/2; n≡6 (8)->3n/2 (a permutation. *FATE of seed 8* → Infinite. The orbit has infinitely many rises and falls (every rise is followed by a run of v_3(4m∓1)>=1 falls) and a branch itinerary that is not eventually pe. 
- **farkas2005** (round2/literature) — m=2 mod 3 -> (m+1)/3; else m odd -> (m+1)/2; else m even -> 3m/2. This is Farkas's F'(x) = x/3 if 3|x, (x+1)/2. *GLOBAL: does every orbit reach the fixed point 1?* → Yes. 1 is the only cycle. Correction to round 1: catalog farkas_s27 IS Farkas's map (YAH coordinates n=(x-1)/2): R(n) = G(n+1)-1 for n>=2, checked to 10^6.. 
- **yah_avoid15** (round2/literature) — n=1 or 5 mod 8 -> 1; else even n -> n/2; odd n -> 3n+1. *GLOBAL: does every orbit reach 1? (= every Collatz trajectory meets 1 or 5 mod 8; YAH Sec.* → Yes. Every Collatz trajectory meets 1 or 5 mod 8 in finitely many steps.. 
- **yah_avoid6** (round2/literature) — n=6 mod 8 -> 1; else even n -> n/2; odd n -> 3n+1. *GLOBAL: does every orbit enter {1,4,2}? (= YAH Prop. 4.7 / Thm 4.10, class 6)* → Yes. 
- **farkas5m_s27** (round2/rewriting) — n=3 mod 5 -> (n+2)/5; else even n -> n/2; else (5n-3)/2   (NEW). *GLOBAL (and FATE of 27)* → Yes: every orbit reaches the fixed point 1, the only cycle. Seed: 27 -> 66 -> 33 -> 7 -> 16 -> 8 -> 2 -> 1.. 
- **up_ct11** (round2/upfrom1) — n=3 mod 4 -> n+4 (trap); else even n -> n/2, odd n -> (3n+1)/2. *Which n have infinite orbits?* → Exactly the n whose T-orbit meets 3 mod 4 before reaching 1. All other orbits reach (1 2); there is no other cycle and no untrapped divergence. Membership is de. 

## Tier 2: congruence invariant or descent plus finite table

- **desc_s32_d65** (round2/descent) — even n -> n/2; odd n -> 3n+65 if n mod 32 in {1,3,5,7,11,13,15,17,21,23,25,29}, else n+65. *CYCLES: list all cycles with a completeness proof* → exactly 8 cycles, with minima 1, 5, 7, 13, 39, 65, 299, 1135 and lengths 21, 5, 29, 4, 5, 3, 8, 13. x -> 65x conjugates the 2-adic map of desc_s32_max to this one, because 65 = 1 mod 32. So the certificate has the same 144-class, k = 44 shape; it is rebuilt and verified directly. The exceptional set E has 63 elements (largest 1519), and running them gives ex
- **desc_s32_max** (round2/descent) — even n -> n/2; odd n -> 3n+1 if n mod 32 in {1,3,5,7,11,13,15,17,21,23,25,29}, else (9,19,27,31 mod 32) n+1. *GLOBAL: is every positive orbit eventually periodic?* → yes; every orbit reaches 1 -> 4 -> 2 -> 1. An exhaustive 2-adic search gives a 144-class certificate with moduli up to 2^30 and k = 44 steps. Every affine form is re-verified independently. The exceptional set is E = {1}, so Lemma A applies. The depth is explained by the near-critical 2-adic 13-cycle t
- **swD_s3** (round2/downfrom5) — P(n)=sigma(D(n)), D = perm_d (2q->5q; 8q+r->5q+(r+1)/2), sigma swapping 3<->4, 11<->12, 14<->15 (mod 20); |P-D. *FATE of seed 3* → Infinite (orbit 3,2,5,4,10,25,16,...; not monotone: 838 falls in 3000 steps). The exact residue graph mod 4 (P affine on classes mod 32) shows {n ≢ 3 mod 4} is P-closed, with 3 outside and P(3)=2 inside; injectivity gives non-return. The itinerary is non-periodic because composite slopes 5^h/2^e are non-integral. Falls are not congruenc
- **swT9_15_s8** (round2/downfrom5) — Q(n)=sigma(T(n)), with T the 1932 map (3q->2q, 3q+1->4q+1, 3q+2->4q+3) and sigma swapping 9<->10 and 15<->16 (. *FATE of seed 8* → Infinite: the orbit never returns. It is unbounded (infinitely many rises) and its branch itinerary is not eventually periodic. Infinitely many falls is NOT pro. Conjugate to R = T o sigma. The set S = {odd} ∪ {2 mod 12} is R-closed: by the mod-36 table of R, only odd classes 3 and 21 (mod 36) fall and both land in 2 mod 12, and every class 2 mod 12 rises to an odd number. So sigma(S), a union of 21 classes mod 36, is 
- **qrA3_q23** (round2/qr) — n even -> n/2; n odd -> (n+23c)/3, c in {0,1,2} minimal (c = n mod 3). *BASIN: which cycle does each n reach?* → If 23 | n, n reaches the fixed point 23. If the Legendre symbol (n/23) = +1, n reaches the cycle (1 8 4 2). If (n/23) = -1, n reaches the cycle (5 17 21 7 10).. Lemma CD (coset descent): [1,q] is forward invariant, every n>q descends, and T(n) = m^{-1} n mod q, so gcd(n,q) and the coset of <2,3> are invariant. <2,3> has order 11, so it is the quadratic residues (2 and 3 are both squares since 23 = -1 mod 24). A finite
- **qrA3_q307** (round2/qr) — n even -> n/2; n odd -> (n+307c)/3, c = (-n) mod 3. *BASIN* → If 307 | n, n reaches 307. Otherwise the cubic character n^102 mod 307 decides: value 1 -> cycle through 1 (length 18); value chi(5) -> cycle through 5 (length . Lemma CD with H = <2,3> equal to the cubes mod 307. 2 is a cube because 307 = 8^2 + 27*3^2 (Gauss); 2^102 = 3^102 = 1 and |H| = 102 are checked. This is the first prime in the family where <2,3> has index 3 (searched q < 600). A finite table shows exactly one 
- **qrA3_q95** (round2/qr) — n even -> n/2; n odd -> (n+95c)/3, c in {0,1,2} minimal. *BASIN* → gcd(n,95) = 95 -> 95; gcd = 5 -> cycle (5 65 85 60 30 15); gcd = 19 -> cycle (19 38). For gcd = 1: Jacobi symbol (n/95) = +1 -> cycle (1 32 16 8 4 2); (n/95) = . Lemma CD for composite q = 5*19: gcd(n,q) and the coset in (Z/(q/d))^*/H are invariant. H = <2,3> has index 2 and lies in the kernel of the Jacobi symbol, since J(2) = J(3) = (-1)(-1) = 1, so H equals that kernel. Neither Legendre factor alone is invariant. A 
- **qrA5_q251** (round2/qr) — n even -> n/2; n odd -> (n+251c)/5, c in {0..4} minimal. *BASIN* → If 251 | n, n reaches 251. Otherwise n reaches the cycle through r, where r in {1,3,7,9,21} is the unique element with r^50 = n^50 mod 251 (cycle lengths 8, 8, . Lemma CD with H = <2,5> = the fifth powers mod 251 (index 5; 2^50 = 5^50 = 1 and |H| = 50 are checked). A finite table gives one cycle per quintic class. For contrast, in the same family q=191 has 2 cycles per coset.
- **qrC_q311** (round2/qr) — n even -> n/2; n=1 mod 4 -> (n+311c)/3; n=3 mod 4 -> (n+311c)/5; c minimal. *BASIN* → If 311 | n, n reaches 311. If (n/311) = +1, n reaches the cycle through 3 (length 13). If (n/311) = -1, n reaches the cycle through 11 (length 16).. Lemma CD, which allows any rule for choosing the multiplier. Here H = <2,3,5> = QR mod 311 by quadratic reciprocity, and |H| = 155 is checked. A finite table gives one cycle per class. The first index-3 (cubic) case for this map is q = 643.
- **up_ct35** (round2/upfrom1) — n=7 mod 8 -> n+8; n=27 mod 32 -> n+32 (traps = parity words 111..., 11011); else even n -> n/2, odd n -> (3n+1. *Which n have infinite orbits?* → Exactly the n whose T-orbit meets 7 mod 8 or 27 mod 32 before reaching 1. Every other orbit reaches (1 2), with no other cycles and no untrapped divergence.. A parity-word lemma plus a word lemma: 5-words avoiding 111 and 11011 have at most 3 ones. Then x_{t+5} <= (27x_t+58)/32, where b_max=58 is found exhaustively; this is below x_t for x_t>=12, and [1,11] is closed. A finite table over 1..11 finishes it, and ever
- **up_ct58** (round2/upfrom1) — n mod 256 in R -> n+256 (R = 37 residues whose 8-step Collatz parity word has >=6 ones); else even n -> n/2, o. *Which n have infinite orbits?* → Exactly the n whose T-orbit meets R mod 256 before reaching 1. All other orbits reach (1 2).. Same scheme as up_ct35, with the window as close as practical to the critical density: untrapped 8-windows have <=5 ones (density 0.625 < log2/log3 = 0.6309). This gives x_{t+8} <= (243x+1688)/256, below x for x>=130, and [1,129] is closed. A finite table over
- **up_qr7** (round2/upfrom1) — even n -> n/2; n=3 mod 28 -> n+28 (trap); other odd n -> n+7. *Which n have infinite orbits?* → Exactly n = 3,5,6 mod 7 (the quadratic non-residues mod 7). n = 0 mod 7 ends in the cycle (7 14); n = 1,2,4 mod 7 ends in (1 8 4 2).. Invariant: halving acts as x -> 4x on Z/7 and n+7, n+28 fix n mod 7, so A0={0}, A1={1,2,4}, A3={3,5,6} are each invariant. The n+7 map descends to [1,7], and a finite table gives exactly three cycles, one per class; the A3 cycle (3 10 5 12 6) contains the trap

## Tier 3: finite-state / structural certificate

- **qrB7_c53** (round2/qr) — n even -> n/2; n=1 mod 4 -> (n+35)/2; n=3 mod 4 -> (n+21)/2. *BASIN* → 7 | n -> cycle (7 14). n a QR mod 7 -> cycle (1 18 9 22 11 16 8 4 2). n a non-residue mod 7 -> cycle (3 12 6) or (5 20 10): two cycles in one coset, decided by . Descent into [1,35]; T(n) = 4n mod 7 gives the coset invariant. A carry-transducer induction shows T^k(n) = 2*(n>>(k+1)) + b_k + s_k with bounded carry s_k. This yields a 38-state automaton, minimized to 20 states and verified against direct iteration for n < 
- **up_tok3** (round2/upfrom1) — even n -> n/2; n=1 mod 4 -> n+3; n=3 mod 4 -> n+4 (trap). *Which n have infinite orbits?* → The orbit is finite (reaches 1->4->2->1) iff n = 2^a(4B+1) with B>=0 and every maximal 0-run of binary(B) of even length (trailing run included). Equivalently b. The orbit of 4B+1 reaches B+1. The recursion on B is: B odd gives Q(Y); B=4Z+2 is trapped; B=4Z gives Q(Z); B=0 gives 1. This is a 2-state LSB-first automaton with a reject sink, so the finite-orbit set is a regular language; the regex was checked against simu

## Tier 4: substantial published theorem or long machine certificate

- **perm1932_1cycle** (round2/literature) — 3q -> 2q; 3q+1 -> 4q+1; 3q+2 -> 4q+3 (catalog perm_1932). *CYCLES restricted to 1-cycles (one maximal block of non-multiples of 3): list them all* → Exactly (1), (2,3), (4,5,7,9,6). A 1-cycle has minimum x0 = 2^l e and satisfies e(3^(k+l)-2^(2k+l)) = S with |S| <= 4^k-3^k. This gives k <= 2l+3, and for l>=2, |(2k+l)log2-(k+l)log3| < 2^(1-l). Rhin's bound then gives l <= 118. An exact scan of l <= 600 leaves five candidate (k,l) pairs; enu
- **steiner_1cycle** (round2/literature) — even n -> n/2; odd n -> (3n+1)/2. *CYCLES restricted to 1-cycles (one maximal odd block then one even block): list them all* → Only (1,2). 1-cycles with (k odd, l even) steps correspond exactly to d = 2^(k+l)-3^k > 0 with d | 2^l-1, which gives 0 < (k+l)log2 - k log3 < 2^(1-k). Rhin's bound |u1 log2+u2 log3| >= H^-13.3 (Rhin, Progr. Math. 71 (1987) 155-164, as quoted in Simons arXiv:2205.10582, L

## Tier 5: open

- **div235_7n1_s11** (round1) — 2|n -> n/2; else 3|n -> n/3; else 5|n -> n/5; else 7n+1. *GLOBAL* → unknown. No proof. Heuristic drift ln7-2ln2-(3/4)ln3-(5/16)ln5=-0.77<0, and every n<=10^6 converges to the only cycle found, {1,8,4,2}.
- **div23_5n1_s7** (round1) — 2|n -> n/2; else 3|n -> n/3; else 5n+1. *GLOBAL* → unknown. No proof. Heuristic drift ln5-2ln2-(3/4)ln3=-0.60<0 suggests yes, and every n<=10^6 converges to the only cycle found, {1,6,3}.
- **div23_7n1_s5** (round1) — 2|n -> n/2; else 3|n -> n/3; else 7n+1. *GLOBAL* → unknown. No proof. There is a second cycle, of length 34 with minimum 19 (verified in checks/div23_7n1_s5.py). Drift is only weakly negative (-0.26), and every n<=10^6 reaches the cycle with minimum 1 or the one with minimum 19.
- **m3_b_s8** (round1) — 3|n -> n/3; n=1 -> (4n-1)/3; n=2 -> (4n+1)/3. *GLOBAL* → unknown. Generic 3-branch Collatz-type map (3k->k, 3k+1->4k+1, 3k+2->4k+3) with contracting mean drift of about -0.175 per step. All n<2e5 reach 1, but there is no proof.
- **m3_d_s7** (round1) — 3|n -> n/3; n=1 -> 4n+2; n=2 -> 4n+1. *GLOBAL* → unknown. Accelerated map is 3k->k, 3k+1->4k+2, 3k+2->4k+3, with drift of about -0.175. All n<2e5 reach the 5-cycle through 1 or the 16-cycle through 7. There is no proof.
- **m3_e_s7** (round1) — 3|n -> n/3; n=1 -> 7n+2; n=2 -> 7n+1. *FATE of seed* → unknown. Simulation of 2e5 steps reaches 34528 bits without meeting either known cycle ({1,9,3} or the 14-cycle through 4). The growth rate of 0.172 bits/step matches the positive drift heuristic (2/3)log(7/3)-(1/3)log3 ≈ +0.199.
- **m3_e_s7** (round1) — 3|n -> n/3; n=1 -> 7n+2; n=2 -> 7n+1. *GLOBAL* → unknown. Conjecturally the answer is no, since almost all orbits should diverge. Proving it would need one proven divergent orbit.
- **m3_g_s7** (round1) — 3|n -> n/3; n=1 -> 5n+1; n=2 -> 5n+2. *GLOBAL* → unknown. Accelerated map is 3k->k, 3k+1->5k+2, 3k+2->5k+4, with drift of only about -0.026, so it is barely contracting. All n<2e5 reach {4,21,7,36,12} or {8,42,14,72,24}. There is no proof.
- **par_10_2_s7** (round1) — even n -> n/2; odd n -> 10n+2. *FATE of seed* → unknown. For odd n, F(F(n)) = 5n+1, so this map is exactly the 5x+1 map with one extra step inserted. The fate of seed 7 is therefore the open question of whether the 5x+1 orbit of 7 is bounded. Simulating 20000 steps found no repeat, with the current term about 470 di
- **par_10_2_s7** (round1) — even n -> n/2; odd n -> 10n+2. *GLOBAL* → unknown. By the same reduction, this question is equivalent to 'every 5x+1 orbit is eventually periodic'. That is open, and heuristically false.
- **par_3_13_s27** (round1) — even n -> n/2; odd n -> 3n+13. *GLOBAL* → unknown. An instance of the Lagarias 3x+k problem. 13Z is invariant and T(13m)=13*C(m), so a 'yes' would imply that 3x+1 has no divergent trajectory.
- **par_3_17_s27** (round1) — even n -> n/2; odd n -> 3n+17. *GLOBAL* → unknown. An instance of the 3x+k problem. 17Z is invariant and T(17m)=17*C(m), so a 'yes' would imply that 3x+1 has no divergent trajectory.
- **par_3_1_s27** (round1) — even n -> n/2; odd n -> 3n+1. *GLOBAL* → unknown. This is the no-divergence half of the Collatz (3x+1) conjecture, which is open.
- **par_3_3_s27** (round1) — even n -> n/2; odd n -> 3n+3. *GLOBAL* → unknown. Every orbit enters 3Z after its first odd step, and on 3Z the map is conjugate to Collatz. So the question is equivalent to the no-divergence half of the Collatz conjecture.
- **par_3_5_s27** (round1) — even n -> n/2; odd n -> 3n+5. *GLOBAL* → unknown. 5Z is invariant and F(5m) = 5C(m), so a 'yes' here would imply that no Collatz trajectory diverges. The question contains that open problem.
- **par_3_7_s27** (round1) — even n -> n/2; odd n -> 3n+7. *GLOBAL* → unknown. 7Z is invariant and F(7m) = 7C(m), so a 'yes' here would imply that no Collatz trajectory diverges. The question contains that open problem.
- **par_3_9_s27** (round1) — even n -> n/2; odd n -> 3n+9. *GLOBAL* → unknown. Every orbit enters 3Z and then 9Z, and T(9y)=9*C(y) with C the 3x+1 map. So the GLOBAL question is exactly equivalent to there being no divergent 3x+1 trajectory.
- **par_3_m1_s27** (round1) — even n -> n/2; odd n -> 3n-1. *GLOBAL* → unknown. Replacing n by -n turns this map into 3x+1 on the negative integers. So the question is equivalent to 'no negative 3x+1 trajectory diverges', which is part of the 3x+1 conjecture on Z and is open.
- **par_5_11_s27** (round1) — even n -> n/2; odd n -> 5n+11. *FATE of seed* → unknown. 200000 steps with no repetition, reaching 21721 bits, about the random-model rate of 0.107 bits/step. This is evidence only (checks/par_5_11_s27.py).
- **par_5_11_s27** (round1) — even n -> n/2; odd n -> 5n+11. *GLOBAL* → unknown. On 11Z the map is exactly 11*(5n+1 map), so GLOBAL contains the open 5n+1 problem.
- **par_5_131_s27** (round1) — even n -> n/2; odd n -> 5n+131. *GLOBAL* → unknown. On 131Z the map is exactly 131*(5n+1 map), so GLOBAL contains the open 5n+1 problem.
- **par_5_1_s5** (round1) — even n -> n/2; odd n -> 5n+1. *GLOBAL* → unknown. This is the 5x+1 problem. It is conjectured NO (positive drift log2(5)-2), but no orbit is provably divergent.
- **par_5_1_s7** (round1) — even n -> n/2; odd n -> 5n+1. *FATE of seed* → unknown. Simulation only: 7->36->18->9->..., 2134 bits after 20000 steps with no repeat. This is evidence, not proof.
- **par_5_1_s7** (round1) — even n -> n/2; odd n -> 5n+1. *GLOBAL* → unknown. The 5x+1 problem, as for par_5_1_s5. A proof that 7 diverges would settle it as NO.
- **par_5_353_s27** (round1) — even n -> n/2; odd n -> 5n+353. *GLOBAL* → unknown. On 353Z the map is exactly 353*(5n+1 map), so GLOBAL contains the open 5n+1 problem.
- **par_5_3_s27** (round1) — even n -> n/2; odd n -> 5n+3. *FATE of seed* → unknown. Tier-1 reduction: 3Z is invariant and T(3m)=3*U(m) with U the 5x+1 map. Since 27=3*9 and 9 lies on the 5x+1 orbit of 7, the fate is exactly that of 7 under 5x+1.
- **par_5_3_s27** (round1) — even n -> n/2; odd n -> 5n+3. *GLOBAL* → unknown. Splits into the 5x+1 problem on 3Z (exact conjugacy) and a separate 5x+3 problem on the invariant complement. A YES would imply 5x+1 YES; a proof that 7 diverges would give NO.
- **par_5_5_s27** (round1) — even n -> n/2; odd n -> 5n+5. *FATE of seed* → unknown. Tier-1 reduction: odd n maps to 5(n+1), which is in 5Z, and T(5m)=5*U(m). Since 27->140=5*28 and 28->14->7 under 5x+1, the fate is exactly that of 7 under 5x+1.
- **par_5_5_s27** (round1) — even n -> n/2; odd n -> 5n+5. *GLOBAL* → unknown. Every orbit enters 5Z at its first odd step and stays there, conjugate to 5x+1. So the GLOBAL question is exactly equivalent to the 5x+1 global question.
- **par_5_7_s27** (round1) — even n -> n/2; odd n -> 5n+7. *GLOBAL* → unknown. On 7Z the map is exactly 7*(5n+1 map), so a yes would prove every 5n+1 orbit eventually periodic, which is open and heuristically false.
- **par_6_2_s27** (round1) — even n -> n/2; odd n -> 6n+2. *GLOBAL* → unknown. For odd n, T(n)=2(3n+1) and T^2(n)=3n+1, so each orbit is a 3n+1 orbit with one extra point inserted after every odd term. The odd-to-odd map is exactly the Syracuse map.
- **par_7_1_s1** (round1) — even n -> n/2; odd n -> 7n+1. *GLOBAL* → unknown. Whether every 7n+1 orbit is eventually periodic is open and heuristically false (positive drift; the orbit of 3 appears to diverge).
- **par_7_1_s3** (round1) — even n -> n/2; odd n -> 7n+1. *FATE of seed* → unknown. Return to the seed is excluded by a PROVED tier-2 mod-7 invariant: odd steps give 1 mod 7 and halving multiplies by 4 mod 7, so {1,2,4} (the quadratic residues) is forward-closed. T(3)=22 is in it and 3 is not. Whether the orbit ends in another cycle or is inf
- **par_7_1_s3** (round1) — even n -> n/2; odd n -> 7n+1. *GLOBAL* → unknown. Whether every 7n+1 orbit is eventually periodic is open and heuristically false (log7-2log4... drift >0; the orbit of 3 appears to diverge).
- **par_7_7_s9** (round1) — even n -> n/2; odd n -> 7n+7. *GLOBAL* → unknown. Every orbit enters 7Z after its first odd step, and 7Z is invariant and conjugate to 7n+1. So GLOBAL is exactly equivalent to the open GLOBAL question for 7n+1 (the equivalence itself is tier 1).
- **par_9_1_s5** (round1) — even n -> n/2; odd n -> 9n+1. *FATE of seed* → unknown. This is also the orbit of 1 (1 -> 10 -> 5). 200000 steps show no repetition and the size reaches 79200 bits, about the random-model rate of 0.39 bits/step. This is evidence only (checks/par_9_1_s5.py).
- **par_9_1_s5** (round1) — even n -> n/2; odd n -> 9n+1. *GLOBAL* → unknown. Whether every 9n+1 orbit is eventually periodic is open and heuristically false (log9-2log2>0, and the orbit of 1 appears to diverge).
- **perm_1932_s44** (round1) — 3q->2q; 3q+1->4q+1; 3q+2->4q+3. *GLOBAL* → unknown. Same map as perm_1932_s8. A 'yes' would settle the 1932 orbit-of-8 problem; no infinite orbit has been proved.
- **perm_1932_s8** (round1) — 3q->2q; 3q+1->4q+1; 3q+2->4q+3. *FATE of seed* → unknown. This is Collatz's 1932 orbit-of-8 problem itself. Proved (tier 1): the map is a bijection, so the orbit cannot enter a cycle that omits 8; the only options are returning to 8 or an infinite orbit.
- **perm_1932_s8** (round1) — 3q->2q; 3q+1->4q+1; 3q+2->4q+3. *GLOBAL* → unknown. A 'yes' would settle the orbit of 8; a 'no' needs one orbit proved infinite, and none is known for T.
- **perm_1932inv_s8** (round1) — 2q->3q; 4q+1->3q+1; 4q+3->3q+2. *FATE of seed* → unknown. The map is exactly the inverse of the 1932 permutation T. For a bijection the forward orbit is a finite cycle exactly when the backward orbit is, so this is equivalent to the 1932 orbit-of-8 problem. Bijectivity rules out entering a cycle that omits 8.
- **perm_1932inv_s8** (round1) — 2q->3q; 4q+1->3q+1; 4q+3->3q+2. *GLOBAL* → unknown. Its orbits are the same sets as the orbits of T, so this is equivalent to GLOBAL for the 1932 permutation.
- **perm_b_s7** (round1) — 3q->4q; 3q+1->4q+2; 3q+2->2q+1. *FATE of seed* → unknown. Exact conjugacy (tier 1): B(n) = T(n+1) - 1, with T the 1932 permutation. The orbit of 7 under B is the T-orbit of 8 shifted down by 1, so this is equivalent to the 1932 orbit-of-8 problem.
- **perm_b_s7** (round1) — 3q->4q; 3q+1->4q+2; 3q+2->2q+1. *GLOBAL* → unknown. The conjugacy matches B on the positive integers with T on the integers >= 2, a set T maps onto itself (T fixes 1). So this is equivalent to GLOBAL for the 1932 permutation.
- **perm_c_s8** (round1) — 2q->3q; 4q+1->3q+2; 4q+3->3q+1. *GLOBAL* → unknown. The map is the inverse of perm_swap, so its orbits are those of perm_swap. On multiples of 5 it acts as 5 times the inverse of the 1932 map, so a 'yes' would settle the 1932 orbit-of-8 problem.
- **perm_d_s3** (round1) — 2q->5q; 8q+1->5q+1; 8q+3->5q+2; 8q+5->5q+3; 8q+7->5q+4. *GLOBAL* → unknown. The map is a bijection, so 'yes' means every orbit is a finite cycle. Drift is positive in both directions (forward (1/2)log(25/16)), and 1990 of the first 2000 starts do not cycle in the baseline run. Still, no orbit has been proved infinite and nothing prove
- **perm_swap_s8** (round1) — 3q->2q; 3q+1->4q+3; 3q+2->4q+1. *GLOBAL* → unknown. Exact identity (tier 1): S(n) = 5*T(n/5), where T is the 1932 map on rationals whose denominator is prime to 3. So multiples of 5 are invariant and the orbit of 40 is 5 times the T-orbit of 8. A 'yes' would therefore settle the 1932 problem.
- **split5_1_s27** (round1) — even n -> n/2; n=1 mod 4 -> 5n+1; n=3 mod 4 -> n+1. *GLOBAL* → unknown. No proof found. The heuristic log-drift is -0.58 per odd step, so convergence is expected. All starts up to 2e5 reach the cycles with minimum elements 1 and 13 (evidence only).
- **split5_3_s27** (round1) — even n -> n/2; n=1 mod 4 -> 5n+3; n=3 mod 4 -> n+3. *GLOBAL* → unknown. No proof found. The heuristic log-drift is -0.58 per odd step, so convergence is expected. All starts up to 2e5 reach five cycles, with minimum elements 1, 3, 5, 61 and 125 (evidence only).
- **auto_1932_s8** (round2/automata) — 3q->2q; 3q+1->4q+1; 3q+2->4q+3. *NONRETURN of 8* → OPEN. Proved side result: no automaton certificate with 11 or fewer states exists in base 2 or in base 3.. CEGAR SAT (CaDiCaL) with only necessary constraints: 300 forward iterates accepted, 300 backward iterates rejected, and closure implications for every n up to 3000. Every k up to 11 is UNSAT in both bases. The check re-proves base 2 up to 6 states and base 3 u
- **desc_m3_4n5** (round2/descent) — 3|n -> n/3; n=1 mod 3 -> 4n+5; n=2 mod 3 -> 2n+2. *GLOBAL: is every positive orbit eventually periodic?* → unknown. Proved: no descent certificate exists. Evidence: every n <= 2e4 reaches one of the cycles {1,9,3}, {2,6}, {16,69,23,48}, and the drift is about -0.61 p. The 3-adic 2-cycle -5 -> -15 -> -5 has multiplier 4/3, with partial products 4 and 4/3, so Lemma B applies. Theorem 2 covers the mod-3 family: when 3 does not divide ab, a certificate exists iff the class graph has no loop avoiding 0 and every full block (1->0
- **desc_s32_plus9** (round2/descent) — even n -> n/2; odd n -> 3n+1 if n mod 32 in {1,3,5,7,9,11,13,15,17,21,23,25,29}, else (19,27,31 mod 32) n+1. *GLOBAL: is every positive orbit eventually periodic?* → unknown. Proved: no descent certificate exists. Evidence: every n <= 2e5 reaches 1, and the drift is -0.833 per odd step.. The 2-adic 12-cycle through -227/115 has five 3n+1 steps and seven halvings, so its multiplier is 243/128, and all partial products are > 1 (checked exactly). Lemma B applies. It shares its first six branches with the 243/256 near-critical cycle of desc_s32_ma
- **desc_split7_1** (round2/descent) — even n -> n/2; n=1 mod 4 -> 7n+1; n=3 mod 4 -> n+1. *GLOBAL: is every positive orbit eventually periodic?* → unknown. Proved: no descent certificate exists for any modulus or any number of steps. Evidence: every n <= 1e5 reaches the cycle through 1, and the random-mode. The 2-adic orbit -1/3 -> -4/3 -> -2/3 -> -1/3 has multiplier 7/4, and every partial product is > 1. By Lemma B, no certificate exists for any M or k. Theorem 1 (lemmas.md) covers the whole family: SPLIT(a,b,d) has a certificate iff a < 2^{v_a} and b < 2^{v_b},
- **flipT_s8** (round2/downfrom5) — P(n)=T(n)±1, flipping the parity of T(n): 3q->2q-1, 3q+1->4q+2, 3q+2->4q+4; a permutation with |P-T|=1. *FATE of seed 8* → Equivalent to Collatz's 1932 orbit-of-8 problem. Exact conjugacy P(n) = T(n+3)-3 on Z>0 (T permutes {1,2,3}), and T(8)=11, so P^k(8) = T^k(11)-3 and P-return of 8 holds iff 8 is T-periodic. Also proved: the bijective members of the constant family n -> (2n+c0)/3, (4n+c1)/3, (4n+c2)/3 are exactly T, perm_swap
- **swT9_s8** (round2/downfrom5) — Q(n)=sigma(T(n)) with sigma swapping 9<->10 (mod 18) only; |Q-T|<=1, Q is a permutation. *FATE of seed 8* → Unknown: either returns or infinite (injectivity rules out entering another cycle). Tried: no return in 1e5 steps; exact residue-graph closure shows no congruence separator for every K<=150 and K in {162,216,243,288,324}; exhaustive DFA search finds no automaton certificate with <=4 states in base 2 or <=3 states in base 3 (MSD- or LSD-first)
- **yah_avoid57** (round2/literature) — n=5 or 7 mod 8 -> 1; else even n -> n/2; odd n -> 3n+1. *GLOBAL: does every orbit enter {1,4,2}? (= Yolcu-Aaronson-Heule Conjecture 4.14, $500 priz* → Unknown. True for all n <= 10^6.. Tried three approaches. (1) Residue graph plus potential: provably impossible at every modulus 2^j, because the 2-adic integer -7 has the C-cycle -7,-20,-10,-5,-14 (classes 1,4,6,3,2) of slope 9/8 (checked j<=64). (2) Valuation runs: each run of the reduced br
- **qrA3_q17** (round2/qr) — n even -> n/2; n odd -> (n+17c)/3, c = n mod 3. *BASIN (strong form): give a finite-state rule deciding whether n reaches (1 6 3) or (5 13 * → Proved: the cycles are exactly (1 6 3), (5 13 10) and (17), all orbits reach them, and 17 | n iff n reaches 17. Also proved: no congruence rule separates (1 6 3. Lemma CD gives descent and the cycle table. Non-periodicity follows from basin(2n) = basin(n) and basin(3n) = basin(n) for odd n: a CRT argument reduces any period to an m' coprime to 6, then g(x) = g(x+17) and g(3x) = g(x), and since 5 = 3^5 mod 17 this force
- **div235_7n1_s11** (round2/rewriting) — 2|n -> n/2; else 3|n -> n/3; else 5|n -> n/5; else 7n+1. *GLOBAL* → Unknown. Proved (partial): every n outside E ∪ {1} drops below itself. E has 191954 classes at cap 30^5, density ≈ 1.20e-2. It blocks at -1 in the 30-adics, wit. Descent tree over the mod-30 table.
- **div23_5n1_s7** (round2/rewriting) — 2|n -> n/2; else 3|n -> n/3; else 5n+1. *GLOBAL* → Unknown. Proved (partial): every n outside E ∪ {1} drops below itself. E has 24529 classes at cap 6^9, density ≈ 3.72e-3, nonempty at every modulus. It blocks a. Descent tree over the mod-6 table with the first-prime-divides priority.
- **div23_7n1_s5** (round2/rewriting) — 2|n -> n/2; else 3|n -> n/3; else 7n+1. *GLOBAL* → Unknown. Proved (partial): every n outside E ∪ {1} drops below itself; the minimum 19 of the 34-cycle lies in E. E has 79931 classes at cap 6^8 and density ≈ 7.. Descent tree over the mod-6 table, plus verification that the 34-cycle's minimum is exceptional.
- **m3_b_s8** (round2/rewriting) — 3k -> k; 3k+1 -> 4k+1; 3k+2 -> 4k+3. *GLOBAL* → Unknown. Proved (partial): the exceptional set E has 241664 classes mod 3^14, density ≈ 5.05e-2, and is nonempty at every modulus. Blocking points are -1 and 1 . Descent tree mod 3^K. The SRS encoding is in the style of Yolcu-Aaronson-Heule (JAR 2023). Matrix-interpretation search used z3 QF_BV with the Endrullis-Waldmann-Zantema rule-removal criterion. The partial chain is re-verified in pure Python, and the simulatio
- **m3_d_s7** (round2/rewriting) — 3|n -> n/3; n=1 mod 3 -> 4n+2; n=2 mod 3 -> 4n+1. *GLOBAL* → Unknown. Proved (partial): every n outside E ∪ {1,7} drops below itself. E has 241664 classes mod 3^14, density ≈ 5.05e-2, nonempty at every modulus. It blocks . Descent tree on the raw map mod 3^K, with exact verification of the cycles {1,...} (length 5) and the 16-cycle with minimum 7.
- **m3_g_s7** (round2/rewriting) — 3|n -> n/3; n=1 mod 3 -> 5n+1; n=2 mod 3 -> 5n+2. *GLOBAL* → Unknown. Proved (partial): every n outside E ∪ {4,8} drops below itself. E has 84480 classes mod 3^12 and density ≈ 0.159. Its decay is the slowest in the batch. Descent tree mod 3^K, plus verification of the two 5-cycles (minima 4 and 8).
- **split5_1_s27** (round2/rewriting) — even n -> n/2; n=1 mod 4 -> 5n+1; n=3 mod 4 -> n+1. *GLOBAL: is every orbit eventually periodic?* → Unknown. Proved (partial): every n outside E ∪ {1,13} has an iterate below n, where E is an explicit union of 181544 classes mod 2^24 with exact density 22693/2. A machine-generated coefficient-stopping-time tree over classes mod 2^K, with exact affine images. A class closes when its slope is < 1, and small t are simulated directly. The theorem about minimal counterexamples, cycles and divergent orbits follows from the
- **split5_3_s27** (round2/rewriting) — even n -> n/2; n=1 mod 4 -> 5n+3; n=3 mod 4 -> n+3. *GLOBAL* → Unknown. Proved (partial): every n outside E ∪ {1,3,5,61,125} drops below itself. E has 4775 classes mod 2^32 and exact density 4775/2^32 ≈ 1.11e-6, the thinnes. Same descent tree as split5_1_s27 at cap 2^32, plus exact verification that the small exceptions are on the five known cycles.
- **up_ct3** (round2/upfrom1) — n=7 mod 8 -> n+8 (trap); else even n -> n/2, odd n -> (3n+1)/2. *Which n have infinite orbits (is it exactly the trap basin, with (1 2) the only untrapped * → OPEN. The Collatz conjecture implies yes. Every n <= 2^68 is trapped or reaches 1 (Barina, J. Supercomputing 77 (2021) 2681-2688); the check verifies n<10^6.. Tried the window-descent method of ct35/ct58. Proved it fails for every window length: 111-free words can have ones-density 2/3 > log2/log3, and for each j the residue class mod 2^{3j} with word (110)^j stays untrapped and multiplies by (9/8)^j. Congruence and
