/* Exact verification for the core G3 (base 3):
 *   G3(n) = (4n+1)/3 if n = 8 (mod 9); otherwise ceil(n/3).
 * For every n in [lo, hi] other than the fixed point 1, iterate G3 until the
 * value drops below n.  Exit 0 iff every such n drops.  unsigned __int128 with
 * an overflow guard at 2^120 (status 3).
 * usage: g3verify lo hi
 */
#include <stdio.h>
#include <stdlib.h>

typedef unsigned __int128 u128;

int main(int argc, char **argv) {
    if (argc < 3) return 2;
    unsigned long long lo = strtoull(argv[1], 0, 10), hi = strtoull(argv[2], 0, 10);
    const u128 LIM = ((u128)1) << 120;
    unsigned long long checked = 0, maxsteps = 0;
    for (unsigned long long n = lo; n <= hi; n++) {
        if (n == 1) continue;
        u128 x = n;
        unsigned long long steps = 0;
        while (x >= n) {
            if (x % 9 == 8) x = (4 * x + 1) / 3; else x = (x + 2) / 3;
            steps++;
            if (x > LIM) { fprintf(stderr, "overflow guard at n=%llu\n", n); return 3; }
            if (steps > 100000000ULL) { fprintf(stderr, "no drop for n=%llu\n", n); return 1; }
        }
        checked++;
        if (steps > maxsteps) maxsteps = steps;
    }
    printf("checked %llu maxsteps %llu\n", checked, maxsteps);
    return 0;
}
