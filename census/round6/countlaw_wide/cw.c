// cw.c: exact local functions for a general unit-multiplier p-adic table map (round 6, countlaw_wide).
//
// The table: n = r mod Q = p^k  ->  (u_r n + v_r) / p^{e_r}, u_r = g^{a_r}.
// Node rule (round3/density/theory.md Lemma 1, as in round5/fourier/rb.c): with s known low digits of the
// current value x, a step is applied iff every residue mod Q congruent to x mod p^min(s,k) uses the same row;
// it consumes e digits.
//
// usage:
//   cw gfun p k g "u v e a ..." s c K OUT
//       for the node state (s known digits, value = c mod p^s) and every z < p^K, process the s+K known digits
//       of the value c + p^s z and write the pair (a*, e*) (int16 each; first all a*, then all e*) attaining the
//       minimum prefix slope g^a/p^e over the decided steps, the start (0,0) included.
//   cw uprime RANKFILE p L g M
//       Theorem U' constants: RANKFILE holds int32 ranks of the minimum prefix slope per z < p^L (larger rank =
//       larger slope); allowed sets S_q = {rank >= q}, q = 1..R-1.  For every S_q, every unit w in <g mod p^L>
//       and every window [c, c + p^{L-m}) (m = 1..M): max |C p^m - |S|| / |S| with C = #(wS cap window).
//       Prints "m num den" (exact) per m.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef __int128 i128;
static int P, K_, NR; static long QQ; static long U_[64], V_[64]; static int E_[64], A_[64];
static int dec[16][1 << 16];   // dec[s][c] for s <= k: row index or -1
static long ipow(long b, int e){ long r = 1; while (e--) r *= b; return r; }
static i128 pg[200], pp[200]; static int G_;
static inline i128 mod128(i128 x, i128 m){ i128 r = x % m; return r < 0 ? r + m : r; }
// slope (a1,e1) < (a2,e2) ?
static inline int less(int a1, int e1, int a2, int e2){
  int da = a1 - a2, de = e1 - e2;   // g^a1/p^e1 < g^a2/p^e2  <=> g^da < p^de
  if (da <= 0 && de >= 0) return !(da == 0 && de == 0);
  if (da >= 0 && de <= 0) return 0;
  if (da > 0) return pg[da] < pp[de];          // de > 0
  return pp[-de] < pg[-da];                   // da < 0, de < 0: g^da < p^de <=> p^-de < g^-da
}
static void setup(void){
  QQ = ipow(P, K_);
  for (int s = 0; s <= K_; s++){ long ps = ipow(P, s);
    for (long c = 0; c < ps; c++){ int rw = -2;
      for (long r = c; r < QQ; r += ps){ int rr = (int)r;
        if (rw == -2) rw = rr;
        else if (!(U_[rr] == U_[rw] && V_[rr] == V_[rw] && E_[rr] == E_[rw])) { rw = -1; break; } }
      dec[s][c] = rw; } }
}
int main(int argc, char **argv){
  if (argc < 2) return 2;
  if (!strcmp(argv[1], "gfun")){
    P = atoi(argv[2]); K_ = atoi(argv[3]); G_ = atoi(argv[4]);
    char *rows = argv[5]; long Qk = 1; for (int i = 0; i < K_; i++) Qk *= P;
    NR = (int)Qk; char *tok = strtok(rows, " ");
    for (int r = 0; r < NR; r++){ U_[r] = atol(tok); tok = strtok(0, " "); V_[r] = atol(tok); tok = strtok(0, " ");
      E_[r] = atoi(tok); tok = strtok(0, " "); A_[r] = atoi(tok); tok = strtok(0, " "); }
    int s0 = atoi(argv[6]); long c0 = atol(argv[7]); int L = atoi(argv[8]);
    int k = K_; setup();
    pg[0] = pp[0] = 1;
    for (int i = 1; i < 200; i++){ pg[i] = pg[i-1] * G_; pp[i] = pp[i-1] * P; if (pg[i] < 0 || pp[i] < 0 || pg[i] > ((i128)1 << 120) || pp[i] > ((i128)1 << 120)) { pg[i] = pp[i] = 0; break; } }
    long N = ipow(P, L); long ps0 = ipow(P, s0);
    int16_t *oa = malloc(2 * N), *oe = malloc(2 * N);
    for (long z = 0; z < N; z++){
      i128 x = (i128)c0 + (i128)ps0 * z; int s = s0 + L; int a = 0, e = 0, ba = 0, be = 0; int steps = 0;
      for (;;){
        int kk = s < k ? s : k; i128 pk = ipow(P, kk);
        int rw = dec[kk][(long)mod128(x, pk)];
        if (rw < 0) break;
        i128 y = (i128)U_[rw] * x + V_[rw]; i128 pe = ipow(P, E_[rw]);
        if (mod128(y, pe) != 0) { fprintf(stderr, "inexact\n"); return 5; }
        x = y / pe;   // exact (possibly negative)
        s -= E_[rw]; a += A_[rw]; e += E_[rw];
        if (a >= 120 || e >= 120 || (a > 0 && pg[a] == 0) || pp[e] == 0) { fprintf(stderr, "overflow\n"); return 8; }
        if (less(a, e, ba, be)) { ba = a; be = e; }
        if (++steps > 100000) { fprintf(stderr, "chain\n"); return 7; }
        if (a >= 190 || e >= 190) { fprintf(stderr, "overflow\n"); return 8; }
      }
      oa[z] = (int16_t)ba; oe[z] = (int16_t)be;
    }
    FILE *f = fopen(argv[9], "wb"); fwrite(oa, 2, N, f); fwrite(oe, 2, N, f); fclose(f);
    return 0;
  }
  if (!strcmp(argv[1], "uprime")){
    int p = atoi(argv[3]), L = atoi(argv[4]); long g = atol(argv[5]); int M = atoi(argv[6]);
    long N = ipow(p, L);
    int32_t *rk = malloc(4 * N); FILE *f = fopen(argv[2], "rb"); if (!f) return 3;
    if ((long)fread(rk, 4, N, f) != N) return 4; fclose(f);
    int R = 0; for (long z = 0; z < N; z++) if (rk[z] + 1 > R) R = rk[z] + 1;
    long nu = 0; long *units = malloc(8 * N); long u = 1;
    do { units[nu++] = u; u = (u * g) % N; } while (u != 1);
    long long bn[16], bd[16]; for (int m = 0; m < 16; m++){ bn[m] = 0; bd[m] = 1; }
    for (int q = 1; q < R; q++){
      long sz = 0; for (long z = 0; z < N; z++) sz += rk[z] >= q;
      #pragma omp parallel
      {
        uint8_t *B = malloc(N); int32_t *cs = malloc(4 * (2 * N + 1));
        long long ln[16], ld[16]; for (int m = 0; m < 16; m++){ ln[m] = 0; ld[m] = 1; }
        #pragma omp for schedule(dynamic, 16)
        for (long iu = 0; iu < nu; iu++){
          long w = units[iu]; memset(B, 0, N);
          for (long z = 0; z < N; z++) if (rk[z] >= q) B[(long)(((i128)w * z) % N)] = 1;
          cs[0] = 0; for (long y = 0; y < 2 * N; y++) cs[y + 1] = cs[y] + B[y % N];
          for (int m = 1; m <= M; m++){
            long W = N / ipow(p, m); long long pm = ipow(p, m); int32_t mx = -1, mn = 1 << 30;
            for (long c = 0; c < N; c++){ int32_t C = cs[c + W] - cs[c]; if (C > mx) mx = C; if (C < mn) mn = C; }
            long long d1 = (long long)mx * pm - sz, d2 = sz - (long long)mn * pm; long long d = d1 > d2 ? d1 : d2;
            if ((i128)d * ld[m] > (i128)ln[m] * sz) { ln[m] = d; ld[m] = sz; }
          }
        }
        #pragma omp critical
        for (int m = 1; m <= M; m++) if ((i128)ln[m] * bd[m] > (i128)bn[m] * ld[m]) { bn[m] = ln[m]; bd[m] = ld[m]; }
        free(B); free(cs);
      }
    }
    printf("p %d L %d g %ld sets %d units %ld\n", p, L, g, R - 1, nu);
    for (int m = 1; m <= M; m++) printf("%d %lld %lld\n", m, bn[m], bd[m]);
    return 0;
  }
  if (!strcmp(argv[1], "win")){
    // cw win GFILE p K QUERYFILE : GFILE from gfun (a* then e*, int16, p^K each).  Each query line:
    //   u N ne thr_0 .. thr_{ne-1}   (z in S iff a*(z) >= thr[e*(z)], thr beyond ne-1 = +inf)
    // prints per query: "max min |S|" of #{0 <= t < N : (u t + B) mod p^K in S} over all B.
    int p = atoi(argv[3]), K = atoi(argv[4]); long Q = ipow(p, K);
    int16_t *ga = malloc(2 * Q), *ge = malloc(2 * Q);
    FILE *f = fopen(argv[2], "rb"); if (!f) return 3;
    if ((long)fread(ga, 2, Q, f) != Q || (long)fread(ge, 2, Q, f) != Q) return 4; fclose(f);
    uint8_t *B = malloc(Q); FILE *qf = fopen(argv[5], "r"); if (!qf) return 3;
    long u, N; int ne; static int thr[4096];
    while (fscanf(qf, "%ld %ld %d", &u, &N, &ne) == 3){
      for (int i = 0; i < ne; i++) if (fscanf(qf, "%d", &thr[i]) != 1) return 5;
      // uinv mod Q
      i128 a0 = u % Q, m0 = Q, x0 = 1, x1 = 0; long t0 = (long)a0, t1 = Q; i128 s0 = 1, s1 = 0;
      while (t1) { long q = t0 / t1; long tt = t0 - q * t1; t0 = t1; t1 = tt; i128 ss = s0 - (i128)q * s1; s0 = s1; s1 = ss; }
      if (t0 != 1) return 6;
      long uinv = (long)mod128(s0, Q); (void)m0; (void)x0; (void)x1;
      memset(B, 0, Q); long sz = 0;
      for (long z = 0; z < Q; z++){ int e = ge[z]; if (e < ne && ga[z] >= thr[e]) { B[(long)(((i128)uinv * z) % Q)] = 1; sz++; } }
      long C = 0; for (long y = 0; y < N; y++) C += B[y % Q];
      long mx = C, mn = C;
      for (long c = 1; c < Q; c++){ C += B[(c + N - 1) % Q] - B[c - 1]; if (C > mx) mx = C; if (C < mn) mn = C; }
      printf("%ld %ld %ld\n", mx, mn, sz); fflush(stdout);
    }
    return 0;
  }
  return 2;
}
