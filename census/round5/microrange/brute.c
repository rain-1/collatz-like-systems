// Exact counts for the 3x+1 Terras map T(x) = x/2 (x even), (3x+1)/2 (x odd).
// For every n in [1, 2^M) record
//   tau(n)   = least i >= 1 with 3^{A_i} < 2^i   (coefficient stopping time; A_i = odd steps among the first i)
//   sigma(n) = least i >= 1 with T^i(n) < n       (integer stopping time)
// (capped at CAP), and print, for each m <= M and each b <= CAP,
//   Ntau(m,b) = #{1 <= n < 2^m : tau(n) > b},  Nsig(m,b) = #{1 <= n < 2^m : sigma(n) > b}.
// usage: brute M [d]   (d = 1 gives 3x+1; any odd d gives 3x+d, tau is the same notion)
// Output lines: "tau m c0 c1 ... cCAP" and "sig m c0 ... cCAP".
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
typedef __int128 i128;
#define CAP 120
static int amin[CAP + 2];
int main(int argc, char **argv) {
  int M = atoi(argv[1]);
  long d = argc > 2 ? atol(argv[2]) : 1;
  // amin[i] = least a with 3^a >= 2^i (exact, via 128-bit for i <= 120: 3^a < 2^127 needs a <= 80)
  for (int i = 0; i <= CAP; i++) {
    u128 p2 = (u128)1 << i, p3 = 1; int a = 0;
    while (p3 < p2) { p3 *= 3; a++; }
    amin[i] = a;
  }
  static uint64_t ct[64][CAP + 2], cs[64][CAP + 2];
  #pragma omp parallel
  {
    static __thread uint64_t lt[64][CAP + 2], ls[64][CAP + 2];
    #pragma omp for schedule(dynamic, 65536)
    for (uint64_t n = 1; n < ((uint64_t)1 << M); n++) {
      i128 x = (i128)n; int A = 0, tau = -1, sig = -1;
      for (int i = 1; i <= CAP; i++) {
        if (x & 1) { x = (3 * x + d) / 2; A++; } else x = x / 2;   // x stays >= 0 for d >= -1
        if (tau < 0 && A < amin[i]) tau = i;
        if (sig < 0 && x < (i128)n) sig = i;
        if (tau >= 0 && sig >= 0) break;
      }
      if (tau < 0) tau = CAP + 1;
      if (sig < 0) sig = CAP + 1;
      int L = 64 - __builtin_clzll(n);   // n < 2^L
      lt[L][tau > CAP ? CAP + 1 : tau]++;
      ls[L][sig > CAP ? CAP + 1 : sig]++;
    }
    #pragma omp critical
    for (int L = 0; L < 64; L++) for (int b = 0; b <= CAP + 1; b++) { ct[L][b] += lt[L][b]; cs[L][b] += ls[L][b]; }
  }
  // N(m,b) = #{n < 2^m : stop > b} = sum_{L<=m} sum_{t > b} count[L][t]
  for (int kind = 0; kind < 2; kind++)
    for (int m = 1; m <= M; m++) {
      printf(kind ? "sig %d" : "tau %d", m);
      for (int b = 0; b <= CAP; b++) {
        uint64_t s = 0;
        for (int L = 1; L <= m; L++) for (int t = b + 1; t <= CAP + 1; t++) s += kind ? cs[L][t] : ct[L][t];
        printf(" %llu", (unsigned long long)s);
      }
      printf("\n");
    }
  return 0;
}
