/* Referee scan (independent of check.py).  For every odd m in [lo,hi) iterate the
   catalog map n -> 9n+1 (odd), n -> n/2 (even) step by step from m, counting
   rising runs of the shortcut map S.  A run ends when, after the halving that
   follows 9x+1, the value is even; the next valley is the next odd value reached.
   Stop when a valley <= m.  Report m if a valley == m within R runs (a cycle
   with <= R runs and minimum m).  Overflow of 128 bits is reported (none expected). */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned __int128 u128;
int main(int argc, char **argv) {
    unsigned long long lo = strtoull(argv[1], 0, 10), hi = strtoull(argv[2], 0, 10);
    int R = atoi(argv[3]);
    const u128 LIM = ((~(u128)0) - 1) / 9;
    unsigned long long cnt = 0, hits = 0, ovf = 0;
    if (lo % 2 == 0) lo++;
    for (unsigned long long m = lo; m < hi; m += 2) {
        cnt++;
        u128 x = m;              /* current valley (odd) */
        for (int r = 0; r < R; r++) {
            u128 n = x;
            int bad = 0;
            /* rising run: odd n -> 9n+1 -> /2 ; continue while result odd */
            for (;;) {
                if (n > LIM) { bad = 1; break; }
                n = 9 * n + 1;
                n >>= 1;
                if (n & 1) continue;
                break;
            }
            if (bad) { ovf++; printf("OVERFLOW %llu\n", m); break; }
            while (!(n & 1)) n >>= 1;   /* descend to the next valley */
            x = n;
            if (x <= m) { if (x == m) { hits++; printf("HIT %llu runs=%d\n", m, r + 1); } break; }
        }
    }
    printf("DONE %llu %llu count=%llu hits=%llu ovf=%llu\n", lo, hi, cnt, hits, ovf);
    return 0;
}
