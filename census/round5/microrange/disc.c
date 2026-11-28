// Uniform-in-intercept discrepancy of lines against a survivor set (exact integer arithmetic).
//
// For K, j' (jp), thresholds th[1..K] and an odd u, let
//   S = { x mod 2^K : A_i(x) >= th[i] for i = 1..K }      (A_i = odd Terras steps among the first i)
//   Phi(B) = #{ 0 <= s < 2^jp : (u s + B) mod 2^K in S }.
// For each job prints "|S| max_B Phi(B) min_B Phi(B)" (B over all of Z/2^K).
//
// Modes
//   disc batch       : read jobs "K jp u th1 .. thK" from stdin until EOF; jobs run in parallel (OpenMP);
//                      results printed in input order.
//   disc allu K jp th1..thK : for u = 3^a mod 2^K, a = 0 .. 2^(K-2)-1, print "a max min",
//                      preceded by "size |S|" (parallel over a).
//   disc naive K jp u th1..thK : same quantities by direct definition (O(2^K 2^jp)); for testing only.
// S is built by a depth-first walk of the digit tree: T^i(r + 2^i t) = 3^a t + b on the class r mod 2^i,
// the next parity is that of b + 3^a e for the next digit e of t, subtrees that fail a threshold are dead,
// subtrees whose odd count already meets every later threshold are entirely alive.
// Phi is computed by the sliding update Phi(B+u) = Phi(B) - S[B] + S[B + u 2^jp]; u is odd, so
// B, B+u, B+2u, ... visits every residue.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef struct { int K; int th[64]; int sufmax[66]; uint64_t *W; uint64_t size; } Ctx;

static inline void setbit(uint64_t *W, uint64_t x) { W[x >> 6] |= (uint64_t)1 << (x & 63); }
static inline int getbit(const uint64_t *W, uint64_t x) { return (W[x >> 6] >> (x & 63)) & 1; }

static void rec(Ctx *c, int i, uint64_t r, int a, uint64_t b, uint64_t p3) {
  // invariant: T^i(r + 2^i t) = 3^a t + b, p3 = 3^a, thresholds 1..i met
  if (i == c->K) { setbit(c->W, r); c->size++; return; }
  if (a >= c->sufmax[i + 1]) {           // every continuation survives
    uint64_t n = (uint64_t)1 << (c->K - i), st = (uint64_t)1 << i;
    for (uint64_t t = 0; t < n; t++) setbit(c->W, r + st * t);
    c->size += n; return;
  }
  for (uint64_t e = 0; e < 2; e++) {
    uint64_t cc = p3 * e + b, r2 = r + (e << i);
    if (!(cc & 1)) { if (a >= c->th[i + 1]) rec(c, i + 1, r2, a, cc >> 1, p3); }
    else { if (a + 1 >= c->th[i + 1]) rec(c, i + 1, r2, a + 1, (3 * cc + 1) >> 1, 3 * p3); }
  }
}

static void build(Ctx *c) {
  int K = c->K;
  size_t words = (((size_t)1 << K) + 63) / 64;
  memset(c->W, 0, words * 8);
  c->sufmax[K + 1] = -1000000;
  for (int i = K; i >= 1; i--) c->sufmax[i] = c->th[i] > c->sufmax[i + 1] ? c->th[i] : c->sufmax[i + 1];
  c->size = 0;
  rec(c, 0, 0, 0, 0, 1);
}

static void scan(const Ctx *c, int jp, uint64_t u, uint64_t *mx, uint64_t *mn) {
  int K = c->K; const uint64_t *W = c->W;
  uint64_t Q = (uint64_t)1 << K, mask = Q - 1, N = (uint64_t)1 << jp;
  uint64_t phi = 0;
  for (uint64_t s = 0; s < N; s++) phi += getbit(W, (u * s) & mask);
  uint64_t step = (u * N) & mask, B = 0, hi = phi, lo = phi;
  const uint64_t L = 24, ahead = (L * u) & mask;
  for (uint64_t t = 1; t < Q; t++) {
    __builtin_prefetch(&W[((B + ahead) & mask) >> 6]);
    __builtin_prefetch(&W[((B + ahead + step) & mask) >> 6]);
    phi = phi - getbit(W, B) + getbit(W, (B + step) & mask);
    B = (B + u) & mask;
    if (phi > hi) hi = phi;
    if (phi < lo) lo = phi;
  }
  *mx = hi; *mn = lo;
}

typedef struct { int K, jp; uint64_t u; int th[64]; uint64_t size, mx, mn; } Job;

int main(int argc, char **argv) {
  if (argc >= 2 && !strcmp(argv[1], "batch")) {
    size_t cap = 1024, n = 0; Job *J = malloc(cap * sizeof(Job));
    int K, jp; unsigned long long u;
    while (scanf("%d %d %llu", &K, &jp, &u) == 3) {
      if (n == cap) { cap *= 2; J = realloc(J, cap * sizeof(Job)); }
      if (K < 2 || K > 31 || jp > K || !(u & 1)) return 3;
      J[n].K = K; J[n].jp = jp; J[n].u = u;
      for (int i = 1; i <= K; i++) if (scanf("%d", &J[n].th[i]) != 1) return 2;
      n++;
    }
    #pragma omp parallel
    {
      Ctx c; c.K = -1; c.W = NULL; size_t have = 0;
      #pragma omp for schedule(dynamic, 1)
      for (size_t q = 0; q < n; q++) {
        size_t words = (((size_t)1 << J[q].K) + 63) / 64;
        if (words > have) { free(c.W); c.W = malloc(words * 8); have = words; }
        c.K = J[q].K; memcpy(c.th, J[q].th, sizeof c.th);
        build(&c);
        J[q].size = c.size;
        scan(&c, J[q].jp, J[q].u, &J[q].mx, &J[q].mn);
      }
      free(c.W);
    }
    for (size_t q = 0; q < n; q++)
      printf("%llu %llu %llu\n", (unsigned long long)J[q].size, (unsigned long long)J[q].mx, (unsigned long long)J[q].mn);
    return 0;
  }
  if (argc >= 4 && !strcmp(argv[1], "allu")) {
    Ctx c; c.K = atoi(argv[2]); int jp = atoi(argv[3]);
    if (argc != 4 + c.K) return 2;
    for (int i = 1; i <= c.K; i++) c.th[i] = atoi(argv[3 + i]);
    c.W = malloc(((((size_t)1 << c.K) + 63) / 64) * 8);
    build(&c);
    printf("size %llu\n", (unsigned long long)c.size);
    uint64_t na = (uint64_t)1 << (c.K - 2), mask = ((uint64_t)1 << c.K) - 1;
    uint64_t *MX = malloc(na * 8), *MN = malloc(na * 8);
    #pragma omp parallel for schedule(dynamic, 16)
    for (uint64_t a = 0; a < na; a++) {
      uint64_t u = 1, base = 3, e = a;     // u = 3^a mod 2^K
      while (e) { if (e & 1) u = (u * base) & mask; base = (base * base) & mask; e >>= 1; }
      scan(&c, jp, u, &MX[a], &MN[a]);
    }
    for (uint64_t a = 0; a < na; a++) printf("%llu %llu %llu\n", (unsigned long long)a, (unsigned long long)MX[a], (unsigned long long)MN[a]);
    return 0;
  }
  if (argc >= 5 && !strcmp(argv[1], "naive")) {
    int K = atoi(argv[2]), jp = atoi(argv[3]); uint64_t u = strtoull(argv[4], 0, 10);
    int th[64]; if (argc != 5 + K) return 2;
    for (int i = 1; i <= K; i++) th[i] = atoi(argv[4 + i]);
    uint64_t Q = (uint64_t)1 << K, mask = Q - 1, N = (uint64_t)1 << jp;
    unsigned char *S = malloc(Q); uint64_t size = 0;
    for (uint64_t x0 = 0; x0 < Q; x0++) {       // direct simulation of the Terras map
      uint64_t x = x0; int a = 0, ok = 1;
      for (int i = 1; i <= K; i++) {
        if (x & 1) { x = (3 * x + 1) / 2; a++; } else x /= 2;
        if (a < th[i]) { ok = 0; break; }
      }
      S[x0] = ok; size += ok;
    }
    uint64_t hi = 0, lo = ~(uint64_t)0;
    for (uint64_t B = 0; B < Q; B++) {
      uint64_t phi = 0;
      for (uint64_t s = 0; s < N; s++) phi += S[(u * s + B) & mask];
      if (phi > hi) hi = phi;
      if (phi < lo) lo = phi;
    }
    printf("%llu %llu %llu\n", (unsigned long long)size, (unsigned long long)hi, (unsigned long long)lo);
    return 0;
  }
  fprintf(stderr, "usage: disc batch | disc allu K jp th.. | disc naive K jp u th..\n");
  return 1;
}
