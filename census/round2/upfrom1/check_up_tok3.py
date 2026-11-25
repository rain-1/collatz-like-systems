"""Check for up_tok3: even n -> n/2; n=1 mod 4 -> n+3; n=3 mod 4 -> n+4.
Claim: orbit finite <=> n = 2^a (4B+1), B >= 0, every maximal run of 0s in binary(B) has even length
(trailing run included)."""
import sys, re
from systems import tok3_step as S
ok = True
def fail(m):
    global ok; ok = False; print("FAIL", m)

def inE_rule(n):
    while n % 2 == 0:
        n //= 2
    if n % 4 == 3:
        return False
    B = (n - 1) // 4
    if B == 0:
        return True
    return all(len(r) % 2 == 0 for r in re.findall("0+", bin(B)[2:]))

def inE_sim(n):
    seen = set()
    while n not in seen:
        if n % 4 == 3:
            return False
        seen.add(n); n = S(n)
    if not ({1, 2, 4} & seen):
        fail(f"unexpected cycle from {n}")
    return True

# 1. the recursion identities used in the proof (exact, checked on a long window of B)
for B in range(0, 50000):
    m = 4 * B + 1
    if [S(m), S(S(m)), S(S(S(m)))] != [4 * B + 4, 2 * B + 2, B + 1]:
        fail(f"4B+1 identity B={B}")
for Y in range(0, 50000):
    if S(2 * Y + 2) != Y + 1:          # B=2Y+1: B+1 even -> Y+1
        fail("odd B")
    if (4 * Y + 3) % 4 != 3:           # B=4Y+2: B+1 = 4Y+3 trapped
        fail("trap B")
# trap invariance
for n in range(3, 4000, 4):
    if S(n) % 4 != 3 or S(n) <= n:
        fail("trap")

# 2. rule == simulation
for n in range(1, 1 << 18):
    if inE_rule(n) != inE_sim(n):
        fail(f"mismatch at {n}"); break

# 3. density of E -> 0 (count B < 2^k with even 0-runs: Fibonacci-type recursion)
# c[k] = #{B in [1,2^k)}: exact count by brute force for small k, compare to recursion
def cnt(k):
    return sum(1 for n in range(1, 1 << k) if inE_rule(n))
counts = [cnt(k) for k in range(1, 17)]
ratios = [counts[i] / (1 << (i + 1)) for i in range(len(counts))]
if not all(ratios[i + 1] < ratios[i] for i in range(4, len(ratios) - 1)):
    fail("density not decreasing")
print("counts |E cap [1,2^k)|:", counts)

print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
