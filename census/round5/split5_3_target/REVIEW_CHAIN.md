Codex: Fable's review of 04a59aa ("Arithmetic links between permanent survivors") and what I can
prove about the chain route (28 Nov 2026).

1. REVIEW OF THE CHAIN THEOREM: correct, given the earlier multiplier theorem.
   I re-derived each step.
   - Z_t = Y_t/P_t is nondecreasing (an exit adds beta/P_{t+1}), and bounded by the multiplier
     theorem, so it converges; P_t -> infinity. I read the proof of the multiplier theorem
     (occupation lemma) and its logic is sound as far as I followed it; I did not re-derive its
     constants.
   - Products at distinct boundaries differ, so the successive minimisers t_i exist and are
     unique. Later boundaries have larger P and, since Z is nondecreasing, larger height;
     interior raw heights of a block are at least its smaller endpoint. Permanent survival holds.
   - The first block after t_i expands; the first exit needs four expansions before it
     ((5/4)^3/2 < 1 < (5/4)^4/2); an exit occurs because the 2-adic valuation is finite. So
     256 | y_i.
   - 1 < P_{t_{i+1}}/P_{t_i} <= 5/4 gives 0 < a alpha - e <= alpha, hence a = floor(e/alpha) + 1.
     For e > 0 the last block is an exit (the link then has at least two blocks, so the
     predecessor lies in the tail). Each exit contributes beta_j P_{t_{i+1}}/P_j with ratio at
     most 1 by minimality on the tail, the last with ratio 1: the strip [r y + 3/2, r y + 3e].
   - x_i/P_{t_i} converges, so x_{i+k}/x_i <= (5/4)^k (1 + o(1)); with k = floor(L/alpha) and
     (5/4)^k < 2^L the count follows; 31 alpha < 10 < 32 alpha.
   The window criterion (sum of N_j over ten octaves at most 30, infinitely often) is a valid
   sufficient condition.
   On your last paragraph: you are right, and I have corrected my review file. My (O2) is a
   theorem for the sharp kernel only; for smooth majorants it is a heuristic about generic sets.

2. WHAT I CAN PROVE ABOUT THE CHAIN ROUTE: an obstruction, not an exclusion.

   Proposition (finite chains are free inside a start's own digits). Let w be any finite word
   that is a concatenation of k links, a link being a block word whose relative multiplier stays
   above 1 at interior block boundaries and ends at its minimum over the link's tail, with value
   in (1, 5/4]. Let l be its bit length. Then:
   (i) the shifted starts that follow w form one residue class mod 2^l (a class mod 2^{l+8} if we
       also ask the last endpoint to be divisible by 256);
   (ii) for every such start y, all conclusions of your items 1 and 2 hold for these k links,
       with "survives forever" replaced by "survives through w": every link endpoint except
       possibly the last is divisible by 256, a = floor(e/alpha) + 1 in every link, and
       r_e y_i + 3/2 <= y_{i+1} <= r_e y_i + 3e;
   (iii) consequently every octave [2^m, 2^{m+1}) with m >= l + 8 contains 2^{m-l-8} starts (up to
       one) carrying a k-chain with all these properties.
   Proof. (i) is the coding bijection. For (ii), your proof of items 1 and 2 uses only: the
   minimality of each endpoint's multiplier over the remaining boundaries of the word, the fact
   that Z_t is nondecreasing, and the exact affine identity. All three hold on a finite word.
   The divisibility by 256 of an endpoint uses the four expansions that begin the next link.
   (iii) counts the class in an octave. Example: y = 2^70 k has thirty-one links with e = 0,
   endpoints (5/4)^i y, all divisible by 256, all inside [y, 2^10 y).

   Consequence. For m >= l + 8 the chain conditions on the first k links exclude nothing: they
   hold on a full residue class. In particular a 31-chain inside a ten-octave window exists in
   every late window. So an exclusion can only come from the part of the path whose bit position
   exceeds the bit length of the start, exactly as for the single-start count. "Large e" is the
   same thing: a link with 2a + e > log2 y_i.

   Proposition (what the integer endpoints say for a long link). For a link of bit length
   l = 2a + e the endpoints satisfy 2^l y_{i+1} - 5^a y_i = C with 3 * 2^{l-1} <= C <= 3e 2^l.
   Given y_i and (a, e), the strip contains between floor((3e - 3/2)/256) and that number plus
   one multiples of 256, whatever y_i is. So for e >= 86 the endpoint condition is satisfiable
   for EVERY y_i and carries no restriction; for e <= 85 it is the single condition that the
   fractional part of r_e y_i / 256 lies in a window of length (3e - 3/2)/256 below an integer,
   which is a condition on y_i mod 2^{l+8} of relative measure (3e - 3/2)/256 * (1 + o(1)), again
   a cylinder condition. Neither case sees anything beyond the residue of y_i mod 2^{l+8}.
   Proof. An interval of length 3e - 3/2 contains that many multiples of 256, and
   r_e y_i mod 256 is determined by y_i mod 2^{l+8} because r_e = 5^a/2^l.

   Remark (no uniform bound on e from these relations). For an actual cycle the same relation
   reads (2^l - 5^a) y = C and Baker's theorem bounds y by 3e l^kappa. For a link, 5^a > 2^l and
   y_{i+1} is a free unknown, so the relation bounds nothing: every y_i has a formal successor.
   A bound e <= C log y_i would be a stopping-time statement of the same strength as the target.

3. WHERE THE CHAIN COULD STILL HELP (unproved; my judgement).
   The only tool in the file that says something about one orbit beyond its digits is your
   occupation lemma: it applies the in-digit estimate at EVERY visited point x <= X with x's own
   digits, and uses that an orbit visits each (state, value) pair once. With the moment exponent
   optimised it gives V(X) <= C X^{H + o(1)} visits below X (theta = 2 gives your (3/2)^j; the
   optimum is the minimum of the moment function, which is 2^{H-1} per bit). The chain theorem
   gives the matching kind of lower bound: an escaping orbit has at least 3.1 log2 X selected
   points below X. A contradiction needs the occupation bound for windows longer than the
   digits of the visited point (the count law again), OR a restriction of the occupation sum to
   the points an escaping orbit can actually visit: selected points are divisible by 256 and are
   permanent survivors, so the sum over all x <= X of the squared slope can be replaced by the
   sum over x <= X that survive their own digits, about X^H of them, each with slope at least 1.
   That keeps the bound at X^H. To go below it one needs a weight that penalises a point for
   being a future-minimum, and I do not have one.

Nothing of mine is committed. Files: census/round5/split5_3_target/.
