# lhf/five: the 5n+d family (CLS-009, 010, 022-023)

Shared lemmas used by every CLS file in this directory. All are proved here in full;
the computational spot checks are in five_common.py (called by every check_CLS-*.py).
Write T_d(n) = n/2 (n even), 5n+d (n odd), U = T_1 (the 5x+1 map).

**L1 (dZ conjugacy).** For odd d, dZ is forward invariant and T_d(dm) = d U(m).
Proof: dm even iff m even (d odd); dm/2 = d(m/2); 5dm + d = d(5m+1).

**L2 (rational conjugacy, exact).** For odd d and any positive integer n, the T_d-orbit of n is
d times the U-orbit of the rational n/d, where U acts on rationals with odd denominator by
x/2 if the numerator is even, 5x+1 otherwise. Proof: L1 with m = n/d in the ring Z_(2); parity
of n/d (as a 2-adic integer) equals parity of n because d is odd. Hence
GLOBAL(T_d) <=> "every positive rational with denominator dividing d has an eventually periodic
U-orbit" (Lagarias' rational extension of 5x+1), and the union over all odd d of the GLOBAL(T_d)
questions is exactly the rational 5x+1 problem.

**L3 (scaling lattice).** If d | d' (both odd) then T_{d'} restricted to (d'/d)Z is conjugate to T_d
(same proof as L1). So a divergent T_d orbit gives a divergent T_{d'} orbit, and GLOBAL(T_{d'}) = yes
implies GLOBAL(T_d) = yes. In particular a single divergent 5x+1 orbit answers NO to GLOBAL for
every odd d. All d in our list (1,3,7,11,131,353) are 1 or prime, so 5x+1 is the only common
sub-problem.

**L4 (the "seeds divisible by 5" route is empty).** If 5 does not divide d, every odd step lands
in d mod 5 != 0, and n/2 is a unit mod 5 whenever n is. So after its first odd step (which
every positive orbit takes) every orbit lies forever in the units mod 5, where
output/pdf/binary_certificates_5np.pdf and the congruence note already exclude binary-automaton
and congruence certificates. For d = 5 every orbit enters 5Z after one odd step and is 5 times a
U-orbit (L1), to which the same remark applies with d = 1. So seeds divisible by 5 give no new
handle on any of these maps.

**L5 (no eventually-periodic-parity divergence certificate).** If a positive T_d orbit has an
eventually periodic parity sequence then it is eventually periodic. Proof: let the parity block
of length p repeat from time J, with a odd steps. If a = 0 the orbit halves forever, impossible.
Otherwise T^p acts on y_i = T^{J+ip}(n) as g(y) = (5^a y + c)/2^p with a fixed integer c >= 0,
so y_{i+1} = g(y_i). Put y* = c/(2^p - 5^a), a 2-adic integer (denominator odd) with g(y*) = y*.
Then y_i - y* = (5^a/2^p)^i (y_0 - y*), so |y_0 - y*|_2 = 2^{-ip} |y_i - y*|_2 <= 2^{-ip} for all i
(y_i, y* are 2-adic integers). Hence y_0 = y* is an integer fixed by g, and since y_0 carries the
parity word, T^p(y_0) = g(y_0) = y_0. This kills route (a)'s "strictly increasing affine subsequence on
an invariant class" and "attracting 2-adic fixed point" certificates for all these maps: any
divergent orbit has aperiodic parity.

Consequently every GLOBAL=NO in this family needs one provably divergent orbit with aperiodic
parity; no such orbit is known for any 5n+d map, and we did not find one. Nothing below
settles an item; the items collapse into three classes:

* Class A (exactly the 5x+1 orbit of 7): CLS-009, CLS-023, CLS-026, CLS-028.
* Class B (exactly 5x+1 GLOBAL): CLS-010, CLS-022, CLS-024, CLS-029.
* Class C (rational 5x+1 with denominator d; implied NO by any divergent 5x+1 orbit):
  CLS-027 (d=3), CLS-030 (7), CLS-020 (11), CLS-021 (131), CLS-025 (353).
* CLS-019 (FATE 27 under 5n+11) <=> fate of the rational 27/11 under 5x+1.
Implications: A "infinite" => B "no" => every C "no".
