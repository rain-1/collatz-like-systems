/* Exact verification for the S-family cores (round3/accel/sfamily_obst.md):
 *   T_S(n) = n/2 (n even); 3n+1 if n mod 8 in S, else n+1 (n odd).
 * For every n in [lo, hi] that is not in the given list of known cycle
 * elements, iterate T_S until the value drops below n.  Exit status 0 iff
 * every such n drops.  Arithmetic is unsigned __int128 with an explicit
 * overflow guard (a value above 2^120 aborts with status 3).
 *
 * usage: sfverify SMASK lo hi [known cycle elements ...]
 *   SMASK: bit r set  <=>  r mod 8 in S (only odd r matter).
 * prints: checked count, max steps to drop, max peak (as a decimal string).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;

static void pr(u128 x, char *buf) {
    char t[64]; int i = 0;
    if (x == 0) { strcpy(buf, "0"); return; }
    while (x) { t[i++] = '0' + (int)(x % 10); x /= 10; }
    for (int j = 0; j < i; j++) buf[j] = t[i - 1 - j];
    buf[i] = 0;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage\n"); return 2; }
    unsigned smask = (unsigned)strtoul(argv[1], 0, 10);
    unsigned long long lo = strtoull(argv[2], 0, 10), hi = strtoull(argv[3], 0, 10);
    int nk = argc - 4;
    unsigned long long known[64];
    for (int i = 0; i < nk && i < 64; i++) known[i] = strtoull(argv[4 + i], 0, 10);
    const u128 LIM = ((u128)1) << 120;
    unsigned long long checked = 0, maxsteps = 0;
    u128 maxpeak = 0;
    for (unsigned long long n = lo; n <= hi; n++) {
        int isk = 0;
        for (int i = 0; i < nk; i++) if (known[i] == n) isk = 1;
        if (isk) continue;
        u128 x = n, peak = n;
        unsigned long long steps = 0;
        while (x >= n) {
            if (x & 1) {
                if ((smask >> (unsigned)(x & 7)) & 1) x = 3 * x + 1; else x = x + 1;
            } else x >>= 1;
            steps++;
            if (x > peak) peak = x;
            if (x > LIM) { fprintf(stderr, "overflow guard at n=%llu\n", n); return 3; }
            if (steps > 100000000ULL) { fprintf(stderr, "no drop for n=%llu\n", n); return 1; }
        }
        checked++;
        if (steps > maxsteps) maxsteps = steps;
        if (peak > maxpeak) maxpeak = peak;
    }
    char b[64]; pr(maxpeak, b);
    printf("checked %llu maxsteps %llu maxpeak %s\n", checked, maxsteps, b);
    return 0;
}
