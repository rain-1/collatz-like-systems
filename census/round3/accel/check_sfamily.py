"""Check for sfamily_obst.md (the 12 OBST members of the S-family).

Claims checked:
  [Z]    Theorem Z: for every S, with G_S the closed-form z-map of systems.zcore,
         (odd(T_S(2z+1)) - 1)/2 = G_S(z), on 0 <= z < 2*10^5 and 3000 random
         z < 2^300 (the proof is algebraic; this tests the formulas).
  [C]    Corollary: for S = {3} mod 4 and S = {3,7} mod 8, G_S = Collatz T
         exactly (same ranges); and T_S(2z+1) is odd after exactly two T_S
         steps, i.e. T_S^2(2z+1) = 2 T(z) + 1.
  [F]    Simplified forms: zcore(S={7}) = K7 and zcore(S={1,3,7}) = W, and the
         odd-to-odd form of W: W_odd(o) = 3^floor((v-1)/2) (3o+1)/2^v, v = v2(3o+1).
  [CYC]  Exact: complete list of T_S-cycles of period <= 26 for each of the 12
         systems (closed-walk enumeration, accel_lib.integer_cycles_upto).
  [EV]   EVIDENCE only: cycles reached from n <= 10^5, and for S={1,3,7} the
         number of n <= 10^5 whose orbit exceeds 10^60.
Runtime: about 1 minute.
"""
import sys, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import accel_lib as AL
import systems as SY

ok = True


def claim(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok = ok and bool(cond)


random.seed(20261127)
RAND = [random.getrandbits(300) for _ in range(3000)]
ZS = list(range(0, 200000)) + RAND


def odd_accel(T):
    def g(n):
        n = T(n)
        while n % 2 == 0:
            n //= 2
        return n
    return g


EXPECT_CYC = {"sf2_3": [1, 3], "sf2_13": [1], "sf3_13": [1, 3], "sf3_135": [1], "sf3_7": [1],
              "sf3_17": [1], "sf3_37": [1, 3], "sf3_137": [1, 3, 7, 39], "sf3_57": [1],
              "sf3_157": [1], "sf3_357": [1], "sf3_1357": [1]}

for m, S in SY.SF:
    sid = SY.sf_id(m, S)
    s = SY.get(sid)
    T = s["step"]
    G = SY.get("zcore_" + sid[2:])["step"]
    g = odd_accel(T)
    claim(f"[Z] {sid}: (odd(T_S(2z+1))-1)/2 == G_S(z)", all((g(2 * z + 1) - 1) // 2 == G(z) for z in ZS))
    if set(S) == {r for r in range(3, 2 ** m, 4)}:
        claim(f"[C] {sid}: G_S == Collatz T", all(G(z) == SY.collatz_T(z) for z in ZS))
        claim(f"[C] {sid}: T_S^2(2z+1) == 2T(z)+1 for z >= 0",
              all(T(T(2 * z + 1)) == 2 * SY.collatz_T(z) + 1 for z in ZS))
    cyc, walks = AL.integer_cycles_upto(2, m, s["table"], 26)
    claim(f"[CYC] {sid}: cycles of period <= 26 (exact, {walks} closed walks): minima {cyc}",
          cyc == EXPECT_CYC[sid])
    mins, div = set(), 0
    known = {}
    for n0 in range(1, 100001):
        x, path, pos = n0, [], set()
        while x not in known and x not in pos and x < 10 ** 60:
            pos.add(x)
            path.append(x)
            x = T(x)
        if x >= 10 ** 60:
            div += 1
            c = -1
        elif x in known:
            c = known[x]
        else:
            c = min(AL.cycle_of(T, x))
        for y in path:
            known[y] = c
        if c > 0:
            mins.add(c)
    print(f"  [EV] {sid}: n <= 1e5 reach cycles {sorted(mins)}; orbits passing 1e60: {div}")

K7 = SY.get("zcore_K7")["step"]
W = SY.get("zcore_W")["step"]
claim("[F] zcore_7 == K7", all(SY.get("zcore_3_7")["step"](z) == K7(z) for z in ZS))
claim("[F] zcore_137 == W", all(SY.get("zcore_3_137")["step"](z) == W(z) for z in ZS))


def W_odd(o):
    x = W(o)
    while x % 2 == 0:
        x = W(x)
    return x


def W_odd_formula(o):
    y = 3 * o + 1
    v = 0
    while y % 2 == 0:
        y //= 2
        v += 1
    return 3 ** ((v - 1) // 2) * y


claim("[F] W odd-to-odd: 3^floor((v-1)/2) (3o+1)/2^v",
      all(W_odd(o) == W_odd_formula(o) for o in [z | 1 for z in ZS]))

print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
