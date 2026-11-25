"""swT3_9_15_s8: Q = sigma_{3,9,15} o T (swap 3<->4 mod 6 after T), seed 8.
Tier 1: 3 does not divide n  =>  3 does not divide Q(n) and Q(n) > n (n >= 2)."""
import sys
from _common import get, T, sigma, is_affine_on_classes, bijective_window
s = get("swT3_9_15_s8"); Q = s["step"]; sg = sigma(18, [3, 9, 15])
ok = True
def claim(name, c):
    global ok
    print(("PASS " if c else "FAIL ") + name); ok = ok and c
claim("sigma_{3,9,15} = swap 3<->4 (mod 6)",
      all(sg(n) == (n + 1 if n % 6 == 3 else n - 1 if n % 6 == 4 else n) for n in range(1, 100001)))
claim("step = sigma(T(n)), |Q-T|<=1 on [1,2e5]",
      all(Q(n) == sg(T(n)) and abs(Q(n) - T(n)) <= 1 for n in range(1, 200001)))
claim("Q bijective on window", bijective_window(Q, 100000))
# exact form on non-multiples of 3: Q(n) = T(n) + [T(n) = 3 mod 6], T(n) odd
claim("for 3 !| n: T(n) odd, Q(n)=T(n)+[T(n)=3 mod 6], 3 !| Q(n) (exact mod-18 table of T(n))",
      all((T(n) % 2 == 1) and Q(n) == T(n) + (1 if T(n) % 6 == 3 else 0) and Q(n) % 3 != 0
          for n in range(1, 54 * 4) if n % 3))
claim("Q affine on classes mod 27 (so the mod-54 table above is exhaustive)", is_affine_on_classes(Q, 27))
claim("Q(n) > n for 2 <= n <= 1e5, 3 !| n", all(Q(n) > n for n in range(2, 100001) if n % 3))
x = 8; xs = [8]
for _ in range(2000):
    x = Q(x); xs.append(x)
claim("orbit of 8 strictly increasing (first 2000 steps; proof is algebraic)",
      all(xs[i + 1] > xs[i] for i in range(2000)))
# CYCLES remark: on 3Z, Q(3q) < 3q
claim("Q(3q) < 3q for q <= 1e5", all(Q(3 * q) < 3 * q for q in range(1, 100001)))
sys.exit(0 if ok else 1)
