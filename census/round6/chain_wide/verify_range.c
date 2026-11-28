/* Exact range verifier for a table map T(n) = (u n + v)/w, n = r mod Q.
   Usage: verify_range LOG2N0 Q u0 v0 w0 ... u_{Q-1} v_{Q-1} w_{Q-1} -- c1 c2 ... (known cycle elements)
   For every 1 <= n < 2^LOG2N0 it iterates until a value < n, a value equal to a
   known cycle element, or failure (step cap 10^7, or value >= 2^120).
   Strong induction then gives: every n < 2^LOG2N0 has an eventually periodic orbit
   ending in a known cycle.  Values reaching 2^120 are printed as "BIG n" and
   must be finished by the caller with exact big-integer arithmetic (run_ranges.py).  Prints "OK n0 maxsteps" or "FAIL n" and exits 1. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u128;
static long long U[4096], V[4096], W[4096];
static unsigned long long C[100000]; static int nc = 0; static unsigned long long nbig = 0;
static int iscyc(u128 x) {
  if (x > (u128)C[nc - 1]) return 0;
  unsigned long long y = (unsigned long long)x; int lo = 0, hi = nc - 1;
  while (lo <= hi) { int m = (lo + hi) / 2; if (C[m] == y) return 1; if (C[m] < y) lo = m + 1; else hi = m - 1; }
  return 0;
}
static int cmp(const void *a, const void *b) {
  unsigned long long x = *(const unsigned long long *)a, y = *(const unsigned long long *)b;
  return x < y ? -1 : x > y;
}
int main(int argc, char **argv) {
  int L = atoi(argv[1]); long long Q = atoll(argv[2]); int i = 3;
  for (long long r = 0; r < Q; r++) { U[r] = atoll(argv[i++]); V[r] = atoll(argv[i++]); W[r] = atoll(argv[i++]); }
  if (strcmp(argv[i++], "--")) { fprintf(stderr, "bad args\n"); return 2; }
  while (i < argc) C[nc++] = strtoull(argv[i++], 0, 10);
  qsort(C, nc, sizeof C[0], cmp);
  u128 LIM = ((u128)1) << 120; unsigned long long N0 = 1ULL << L, maxs = 0;
  for (unsigned long long n = 1; n < N0; n++) {
    u128 x = n; unsigned long long s = 0;
    for (;;) {
      long long r = (long long)(x % (u128)Q);
      __int128 y = (__int128)U[r] * (__int128)x + V[r];
      if (y <= 0 || y % W[r]) { printf("FAIL %llu (division)\n", n); return 1; }
      x = (u128)(y / W[r]); s++;
      if (x < n || iscyc(x)) break;
      if (x >= LIM) { printf("BIG %llu\n", n); nbig++; break; }
      if (s > 10000000ULL) { printf("FAIL %llu\n", n); return 1; }
    }
    if (s > maxs) maxs = s;
  }
  printf("OK %d %llu big %llu\n", L, maxs, nbig);
  return 0;
}
