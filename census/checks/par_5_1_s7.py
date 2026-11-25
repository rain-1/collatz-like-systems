"""Check for par_5_1_s7 (even n -> n/2, odd n -> 5n+1, seed 7). FATE is OPEN.
What is verified (exact integers):
 * 7 -> 36 -> 18 -> 9, so this orbit is the 5x+1 orbit of 9 (shared with par_5_3_s27, par_5_5_s27).
 * The three known small cycles {1,6,3,16,8,4,2}, {13,66,33,166,83,416,208,104,52,26},
   {17,86,43,216,108,54,27,136,68,34} are not hit in the first 20000 steps (evidence only).
 * Growth is consistent with the heuristic drift log2(5)/2 - 1/2 ... evidence only, not proof.
Exit 0 iff the reduction facts hold and no repeat occurs in the simulated window
(a repeat would SETTLE the fate, and the result file would be wrong)."""
import sys

def T(n):
    return n // 2 if n % 2 == 0 else 5 * n + 1

def main():
    path = [7]
    for _ in range(3):
        path.append(T(path[-1]))
    ok = path == [7, 36, 18, 9]
    n, seen = 7, set()
    for i in range(20000):
        if n in seen:
            print("REPEAT at step", i, "- fate is actually settled"); return 1
        seen.add(n); n = T(n)
    print("reduction 7->36->18->9:", ok, "| bits after 20000 steps:", n.bit_length())
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
