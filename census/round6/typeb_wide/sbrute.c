/* Exhaustive scan of the S-family F(a, d, m, S) at level m (independent of z3).
   even n -> n/2;  odd n -> a n + d if n mod 2^m in S, else n + d.
   For every S (bitmask over the 2^(m-1) odd classes, restricted to the slice
   given on the command line) compute the SCCs of G_m and report:
     nb   = number of S with an SCC that is an expanding simple cycle
     nH   = number of those in which every other non-trivial SCC has max cycle mean < -1e-9
            (candidate type-(b) systems; printed, and re-verified exactly in Python)
     nunc = number with some non-simple SCC whose max mean is within 1e-9 of 0 (printed)
   Usage: sbrute a d m slice nslices            (m <= 6)
*/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdint.h>

static int Q, H, M, A, D;
static int succ[64][2], ns[64];
static double wt[64];   /* log multiplier of the step from node r (same for all its edges) */

static int idx[64], low[64], onst[64], st[64], sp, cnt, comp[64], ncomp;

static void strong(int v) {
  idx[v] = low[v] = cnt++; st[sp++] = v; onst[v] = 1;
  for (int i = 0; i < ns[v]; i++) {
    int w = succ[v][i];
    if (idx[w] < 0) { strong(w); if (low[w] < low[v]) low[v] = low[w]; }
    else if (onst[w] && idx[w] < low[v]) low[v] = idx[w];
  }
  if (low[v] == idx[v]) {
    int w;
    do { w = st[--sp]; onst[w] = 0; comp[w] = ncomp; } while (w != v);
    ncomp++;
  }
}

/* Karp max mean over the SCC c */
static double karp(int c, int *nodes, int n) {
  static double Dk[66][64];
  int loc[64];
  for (int i = 0; i < Q; i++) loc[i] = -1;
  for (int i = 0; i < n; i++) loc[nodes[i]] = i;
  for (int i = 0; i < n; i++) Dk[0][i] = 0.0;
  for (int k = 1; k <= n; k++) {
    for (int i = 0; i < n; i++) Dk[k][i] = -1e300;
    for (int i = 0; i < n; i++) {
      if (Dk[k-1][i] < -1e299) continue;
      int r = nodes[i];
      for (int j = 0; j < ns[r]; j++) {
        int s = succ[r][j];
        if (comp[s] != c) continue;
        double x = Dk[k-1][i] + wt[r];
        if (x > Dk[k][loc[s]]) Dk[k][loc[s]] = x;
      }
    }
  }
  double best = -1e300;
  for (int i = 0; i < n; i++) {
    if (Dk[n][i] < -1e299) continue;
    double mn = 1e300;
    for (int k = 0; k < n; k++) {
      if (Dk[k][i] < -1e299) continue;
      double x = (Dk[n][i] - Dk[k][i]) / (n - k);
      if (x < mn) mn = x;
    }
    if (mn > best) best = mn;
  }
  return best;
}

int main(int argc, char **argv) {
  A = atoi(argv[1]); D = atoi(argv[2]); M = atoi(argv[3]);
  long slice = atol(argv[4]), nsl = atol(argv[5]);
  Q = 1 << M; H = Q / 2;
  int nodd = Q / 2;
  uint64_t total = 1ULL << nodd;
  uint64_t lo = total / nsl * slice, hi = (slice == nsl - 1) ? total : total / nsl * (slice + 1);
  long nb = 0, nH = 0, nunc = 0;
  for (int r = 0; r < Q; r += 2) { ns[r] = 2; succ[r][0] = r / 2; succ[r][1] = r / 2 + H; wt[r] = -log(2.0); }
  for (uint64_t mask = lo; mask < hi; mask++) {
    for (int k = 0; k < nodd; k++) {
      int r = 2 * k + 1;
      ns[r] = 1;
      if (mask >> k & 1) { succ[r][0] = (int)(((long)A * r + D) % Q); wt[r] = log((double)A); }
      else { succ[r][0] = (r + D) % Q; wt[r] = 0.0; }
    }
    for (int i = 0; i < Q; i++) idx[i] = -1, onst[i] = 0;
    sp = cnt = ncomp = 0;
    for (int i = 0; i < Q; i++) if (idx[i] < 0) strong(i);
    /* per component: node count, internal edge count, sum of weights */
    int csz[64] = {0}, ced[64] = {0};
    double csum[64] = {0};
    for (int r = 0; r < Q; r++) {
      csz[comp[r]]++;
      for (int j = 0; j < ns[r]; j++) if (comp[succ[r][j]] == comp[r]) { ced[comp[r]]++; csum[comp[r]] += wt[r]; }
    }
    int hasb = 0;
    for (int c = 0; c < ncomp; c++) if (ced[c] == csz[c] && ced[c] > 0 && csum[c] > 1e-9) hasb = 1;
    if (!hasb) continue;
    nb++;
    int bad = 0, unc = 0;
    for (int c = 0; c < ncomp && !bad; c++) {
      if (ced[c] == 0 || ced[c] == csz[c]) continue;
      int nodes[64], n = 0;
      for (int r = 0; r < Q; r++) if (comp[r] == c) nodes[n++] = r;
      double mu = karp(c, nodes, n);
      if (mu > 1e-9) bad = 1; else if (mu > -1e-9) unc = 1;
    }
    if (bad) continue;
    if (unc) { nunc++; printf("UNC %llu\n", (unsigned long long)mask); continue; }
    nH++;
    printf("H %llu\n", (unsigned long long)mask);
  }
  printf("DONE a=%d d=%d m=%d slice=%ld/%ld nb=%ld nH=%ld nunc=%ld\n", A, D, M, slice, nsl, nb, nH, nunc);
  return 0;
}
