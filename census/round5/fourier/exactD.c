// Exact (integer) constants for Theorem U' (the combinatorial form of Theorem U; README, Revision section).
//
// Input file: N = 2^L little-endian int32 ranks rk[z] (z < N); rk[z] = rank of g_sigma(z) among the distinct
// values of g_sigma, larger rank = larger g.  The allowed sets are S_q = {z : rk[z] >= q}, q = 1..Q-1
// (q = 0 is the full set, whose deviation is 0).
// For every allowed set S, every unit w in the chosen unit set, and every window [c, c + W) of Z/N with
// W = k N / 2^M (k = 1..2^M - 1), compute the count C = #(wS cap [c, c+W)) and the deviation
// |C 2^M - k |S||; the output is, for each k, the maximum of the exact rational |C 2^M - k|S|| / (k |S|)
// over all S, w, c, printed as "k num den".
// As w runs over a group G of units, {wS} runs over {u^{-1} S : u in G}; and
//   #{t < W : u t + c in S} = #(u^{-1} S cap [u^{-1} c, u^{-1} c + W))   (substitute t' = t + u^{-1} c),
// so the maximum over (w, window) equals the maximum over (u in G, shift c) of the quantity in Theorem U'.
//
// usage: exactD RANKFILE L M GEN     GEN = 0: all odd units;  GEN = g > 0: the cyclic group <g mod 2^L>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage\n"); return 2; }
  int L = atoi(argv[2]), M = atoi(argv[3]); long gen = atol(argv[4]);
  long N = 1L << L, mask = N - 1;
  int32_t *rk = malloc(4 * N);
  FILE *f = fopen(argv[1], "rb"); if (!f) return 3;
  if ((long)fread(rk, 4, N, f) != N) return 4; fclose(f);
  int Q = 0; for (long z = 0; z < N; z++) if (rk[z] + 1 > Q) Q = rk[z] + 1;
  // unit list
  long nu = 0; long *units = malloc(8 * N);
  if (gen == 0) { for (long u = 1; u < N; u += 2) units[nu++] = u; }
  else { long u = 1; do { units[nu++] = u; u = (u * gen) & mask; } while (u != 1); }
  int K = (1 << M);
  // best[k] as a fraction bn/bd
  long long bn[64], bd[64]; for (int k = 0; k < K; k++) { bn[k] = 0; bd[k] = 1; }
  long long sz_at[64]; int q_at[64]; long u_at[64];
  for (int q = 1; q < Q; q++) {
    long sz = 0; for (long z = 0; z < N; z++) sz += rk[z] >= q;
    #pragma omp parallel
    {
      int32_t *B = malloc(4 * 2 * N); int64_t *cs = malloc(8 * (2 * N + 1));
      long long ln[64], ld[64]; long lu[64]; for (int k = 0; k < K; k++) { ln[k] = 0; ld[k] = 1; lu[k] = 0; }
      #pragma omp for schedule(dynamic, 16)
      for (long iu = 0; iu < nu; iu++) {
        long w = units[iu];
        memset(B, 0, 4 * N);
        for (long z = 0; z < N; z++) if (rk[z] >= q) B[(w * z) & mask] = 1;   // B = 1_{wS}
        cs[0] = 0;
        for (long y = 0; y < 2 * N; y++) cs[y + 1] = cs[y] + B[y & mask];
        for (int k = 1; k < K; k++) {
          long W = (long)k * (N >> M); int64_t mx = -1, mn = 1LL << 62;
          for (long c = 0; c < N; c++) { int64_t C = cs[c + W] - cs[c]; if (C > mx) mx = C; if (C < mn) mn = C; }
          long long d1 = mx * (long long)K - (long long)k * sz, d2 = (long long)k * sz - mn * (long long)K;
          long long d = d1 > d2 ? d1 : d2;  // max |C 2^M - k |S||
          long long den = (long long)k * sz;
          if ((__int128)d * ld[k] > (__int128)ln[k] * den) { ln[k] = d; ld[k] = den; lu[k] = w; }
        }
      }
      #pragma omp critical
      for (int k = 1; k < K; k++)
        if ((__int128)ln[k] * bd[k] > (__int128)bn[k] * ld[k]) { bn[k] = ln[k]; bd[k] = ld[k]; sz_at[k] = sz; q_at[k] = q; u_at[k] = lu[k]; }
      free(B); free(cs);
    }
  }
  printf("L %d M %d gen %ld sets %d units %ld\n", L, M, gen, Q - 1, nu);
  for (int k = 1; k < K; k++)
    printf("%d %lld %lld   (%.6f; set q=%d |S|=%lld, w=%ld)\n", k, bn[k], bd[k], (double)bn[k] / bd[k], q_at[k], sz_at[k], u_at[k]);
  return 0;
}
