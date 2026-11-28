/* famscan.c -- exact classification of every table in a product family of table maps.

   Spec on stdin:
       Q mode count seed
       then for r = 0..Q-1:  n_r  u_1 v_1 w_1 ... u_{n_r} v_{n_r} w_{n_r}
   mode 0: enumerate the whole product (mixed-radix index, class 0 fastest);
   mode 1: `count` uniform random members (xorshift, `seed`).
   The options must already satisfy (H1) gcd(u,Q)=1, (H2) w | Q, w | u r + v, and positivity
   (T(n0) >= 1 at the least n0 of the class); spec.py writes them and checks this.

   For each table, at level Q, the residue graph is r -> (u r + v)/w + (Q/w) j, j < w.
   Each SCC with an internal edge gets a type, EXACTLY verified:
     z  contains a cycle with no division (W = 1)          [checked by following w = 1 nodes]
     b  a single simple cycle with U > W                   [exact big-integer comparison]
     a  every cycle contracts: integer potential c with c(s) u < c(r) w on every internal
        edge, checked in 128-bit integer arithmetic        [a simple cycle with U < W also]
     c  not a single cycle, and contains a cycle with U > W [exact big-integer comparison]
   A table is CERT (all SCCs a), B (no z, no c, some b), C (some c, no z), Z (some z).
   If neither witness can be verified (float trouble), the table is printed as FALLBACK and
   left to the exact Python harness; the count of such tables is reported.
   For CERT tables the complete cycle list is counted from the exceptional set
   F = {n : V(Tn) >= V(n)}, V(n) = c(n mod Q) n (dichotomy Theorem 2), when |F-range| <= FCAP.

   Output lines:  "B <index>", "CERT <index> <mu> <ncycles> <maxcyclemin>", "FALLBACK <index>",
   and a final "SUMMARY ..." line.  CERT lines only with flag 'printcert' in argv[1].
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#define MAXQ 64
#define MAXOPT 512
typedef __int128 i128;

static int Q, mode; static long long count; static unsigned long long seed;
static int nopt[MAXQ]; static long long ou[MAXQ][MAXOPT], ov[MAXQ][MAXOPT], ow[MAXQ][MAXOPT];
static int printcert = 0, printall = 0;
static long long FCAP = 2000000;

static unsigned long long rng(void) { seed ^= seed << 13; seed ^= seed >> 7; seed ^= seed << 17; return seed; }

/* current table */
static long long U_[MAXQ], V_[MAXQ], W_[MAXQ];
static int ns[MAXQ], sc[MAXQ][MAXQ];

/* ---- exact comparison of prod u vs prod w over a node list (big integers) ---- */
#define LIMBS 64
static void bmul(uint32_t *a, int *n, uint32_t m) {
    uint64_t c = 0; for (int i = 0; i < *n; i++) { uint64_t x = (uint64_t)a[i] * m + c; a[i] = (uint32_t)x; c = x >> 32; }
    if (c) { a[(*n)++] = (uint32_t)c; }
}
static int bcmp_(uint32_t *a, int na, uint32_t *b, int nb) {
    while (na > 1 && a[na-1] == 0) na--; while (nb > 1 && b[nb-1] == 0) nb--;
    if (na != nb) return na < nb ? -1 : 1;
    for (int i = na - 1; i >= 0; i--) if (a[i] != b[i]) return a[i] < b[i] ? -1 : 1;
    return 0;
}
/* returns sign(prod u - prod w) along cyc */
static int cyc_sign(int *cyc, int L) {
    uint32_t a[LIMBS] = {1}, b[LIMBS] = {1}; int na = 1, nb = 1;
    for (int i = 0; i < L; i++) { bmul(a, &na, (uint32_t)U_[cyc[i]]); bmul(b, &nb, (uint32_t)W_[cyc[i]]);
        if (na >= LIMBS - 2 || nb >= LIMBS - 2) { fprintf(stderr, "bignum overflow\n"); exit(3); } }
    return bcmp_(a, na, b, nb);
}

/* ---- Tarjan ---- */
static int idx_[MAXQ], low_[MAXQ], onst[MAXQ], stk[MAXQ], sp, cnt_, comp[MAXQ], ncomp;
static void dfs(int v) {
    idx_[v] = low_[v] = cnt_++; stk[sp++] = v; onst[v] = 1;
    for (int i = 0; i < ns[v]; i++) { int w = sc[v][i];
        if (idx_[w] < 0) { dfs(w); if (low_[w] < low_[v]) low_[v] = low_[w]; }
        else if (onst[w] && idx_[w] < low_[v]) low_[v] = idx_[w]; }
    if (low_[v] == idx_[v]) { int w; do { w = stk[--sp]; onst[w] = 0; comp[w] = ncomp; } while (w != v); ncomp++; }
}

static double lw[MAXQ];
/* Karp max mean cycle inside component c; returns mu, writes a cycle into cyc (length *L) */
static double karp(int c, int *nodes, int n, int *cyc, int *L) {
    static double Dm[MAXQ+1][MAXQ]; static int par[MAXQ+1][MAXQ]; int pos[MAXQ];
    for (int i = 0; i < n; i++) pos[nodes[i]] = i;
    for (int i = 0; i < n; i++) Dm[0][i] = 0;
    for (int k = 1; k <= n; k++) {
        for (int i = 0; i < n; i++) { Dm[k][i] = -INFINITY; par[k][i] = -1; }
        for (int i = 0; i < n; i++) { double x = Dm[k-1][i]; if (x == -INFINITY) continue; x += lw[nodes[i]];
            int r = nodes[i];
            for (int j = 0; j < ns[r]; j++) { int s = sc[r][j]; if (comp[s] != c) continue; int jj = pos[s];
                if (x > Dm[k][jj]) { Dm[k][jj] = x; par[k][jj] = i; } } }
    }
    double best = -INFINITY; int bv = -1;
    for (int v = 0; v < n; v++) { if (Dm[n][v] == -INFINITY) continue; double worst = INFINITY;
        for (int k = 0; k < n; k++) if (Dm[k][v] != -INFINITY) { double t = (Dm[n][v] - Dm[k][v]) / (n - k); if (t < worst) worst = t; }
        if (worst > best) { best = worst; bv = v; } }
    int walk[MAXQ+1]; int v = bv; for (int k = n; k >= 0; k--) { walk[k] = v; if (k) v = par[k][v]; }
    int seen[MAXQ]; for (int i = 0; i < n; i++) seen[i] = -1;
    *L = 0;
    for (int i = 0; i <= n; i++) { int x = walk[i];
        if (seen[x] >= 0) { int a = seen[x]; for (int j = a; j < i; j++) cyc[(*L)++] = nodes[walk[j]]; break; }
        seen[x] = i; }
    return best;
}

/* potential on component: returns 1 and fills cpot if verified exactly */
static long long cpot[MAXQ];
static int potential(int c, int *nodes, int n, double mu) {
    static const double fr[4] = {0.5, 0.25, 0.8, 0.95};
    for (int f = 0; f < 4; f++) {
        double lt = mu * fr[f]; double phi[MAXQ];
        for (int i = 0; i < n; i++) phi[nodes[i]] = 0;
        for (int it = 0; it < n + 2; it++) { int ch = 0;
            for (int i = 0; i < n; i++) { int r = nodes[i]; double b = -INFINITY;
                for (int j = 0; j < ns[r]; j++) { int s = sc[r][j]; if (comp[s] == c && phi[s] > b) b = phi[s]; }
                if (b == -INFINITY) continue; b += lw[r] - lt; if (b > phi[r] + 1e-13) { phi[r] = b; ch = 1; } }
            if (!ch) break; }
        double lo = INFINITY, hi = -INFINITY; for (int i = 0; i < n; i++) { if (phi[nodes[i]] < lo) lo = phi[nodes[i]]; if (phi[nodes[i]] > hi) hi = phi[nodes[i]]; }
        if (hi - lo > 40.0) continue;               /* exp(40) * 2^2 < 2^62 */
        double sc_ = ldexp(1.0, 61) / exp(hi - lo);
        int ok = 1;
        for (int i = 0; i < n; i++) { double x = sc_ * exp(phi[nodes[i]] - lo); if (x < 1) x = 1; cpot[nodes[i]] = (long long)llround(x); }
        for (int i = 0; i < n && ok; i++) { int r = nodes[i];
            for (int j = 0; j < ns[r]; j++) { int s = sc[r][j]; if (comp[s] != c) continue;
                if ((i128)cpot[s] * U_[r] >= (i128)cpot[r] * W_[r]) { ok = 0; break; } } }
        if (ok) return 1;
    }
    return 0;
}

/* ---- cycles of a CERT table from the exceptional set ---- */
static int ovf = 0;
static long long Tn(long long n) { int r = (int)(n % Q); if (n > 100000000000000000LL) { ovf = 1; return 1; } return (U_[r] * n + V_[r]) / W_[r]; }
static int count_cycles(long long *maxmin) {
    /* global potential: all comps are type a; cpot filled for nodes in nontrivial comps;
       nodes in trivial comps: set c by backward induction so that c(s)u < c(r)w also on
       edges between components.  Simplest: recompute a global potential with Karp-free BF. */
    double mu = -INFINITY; int nodes[MAXQ]; for (int i = 0; i < Q; i++) nodes[i] = i;
    for (int r = 0; r < Q; r++) lw[r] = log((double)U_[r]) - log((double)W_[r]);
    /* global max mean = max over comps; recompute quickly */
    for (int c = 0; c < ncomp; c++) { int nn = 0, nd[MAXQ]; for (int r = 0; r < Q; r++) if (comp[r] == c) nd[nn++] = r;
        int cyc[MAXQ+1], L; int hasedge = 0;
        for (int i = 0; i < nn; i++) for (int j = 0; j < ns[nd[i]]; j++) if (comp[sc[nd[i]][j]] == c) hasedge = 1;
        if (!hasedge) continue; double m = karp(c, nd, nn, cyc, &L); if (m > mu) mu = m; }
    if (mu == -INFINITY) mu = -1.0;
    /* global potential with all edges: treat whole graph as one 'component' */
    int save[MAXQ]; for (int r = 0; r < Q; r++) { save[r] = comp[r]; comp[r] = 0; }
    int ok = potential(0, nodes, Q, mu);
    for (int r = 0; r < Q; r++) comp[r] = save[r];
    if (!ok) return -1;
    long long work = 0; long long Nr[MAXQ];
    for (int r = 0; r < Q; r++) { Nr[r] = 0; if (V_[r] > 0) for (int j = 0; j < ns[r]; j++) { int s = sc[r][j];
            i128 den = (i128)cpot[r] * W_[r] - (i128)cpot[s] * U_[r]; i128 num = (i128)cpot[s] * V_[r];
            i128 b = num / den; if (b > (i128)4e18) return -1; if (b > Nr[r]) Nr[r] = (long long)b; }
        work += Nr[r] / Q + 1; if (work > FCAP) return -1; }
    long long mins[4096]; int nm = 0; *maxmin = 0; ovf = 0;
    for (int r = 0; r < Q; r++) for (long long n = (r ? r : Q); n <= Nr[r]; n += Q) {
        long long y = Tn(n); if ((i128)cpot[y % Q] * y < (i128)cpot[r] * n) continue;  /* not in F */
        /* Brent cycle detection */
        long long power = 1, lam = 1, tort = n, hare = Tn(n); long steps = 0;
        while (tort != hare) { if (power == lam) { tort = hare; power *= 2; lam = 0; } hare = Tn(hare); lam++;
            if (++steps > 100000000L) return -1; }
        if (ovf) return -1;
        long long m = hare, x = Tn(hare); while (x != hare) { if (x < m) m = x; x = Tn(x); if (ovf) return -1; }
        int f = 0; for (int i = 0; i < nm; i++) if (mins[i] == m) { f = 1; break; }
        if (!f) { if (nm >= 4096) return -1; mins[nm++] = m; if (m > *maxmin) *maxmin = m; }
    }
    return nm;
}

/* ---- classify current table; returns code 0 CERT 1 B 2 C 3 Z 4 FALLBACK; *mu_out max mean ---- */
static int classify(double *mu_out) {
    for (int r = 0; r < Q; r++) { long long w = W_[r]; long long y0 = (U_[r] * r + V_[r]) / w; long long step = Q / w;
        ns[r] = (int)w; long long b = ((y0 % step) + step) % step; for (int j = 0; j < w; j++) sc[r][j] = (int)(b + step * j);
        lw[r] = log((double)U_[r]) - log((double)W_[r]); }
    for (int r = 0; r < Q; r++) idx_[r] = -1; sp = 0; cnt_ = 0; ncomp = 0;
    for (int r = 0; r < Q; r++) if (idx_[r] < 0) dfs(r);
    int hasz = 0, zdiv = 0, zneu = 0, hasc = 0, hasb = 0, fb = 0; double mumax = -INFINITY;
    for (int c = 0; c < ncomp; c++) {
        int nd[MAXQ], nn = 0; for (int r = 0; r < Q; r++) if (comp[r] == c) nd[nn++] = r;
        int ne = 0; for (int i = 0; i < nn; i++) for (int j = 0; j < ns[nd[i]]; j++) if (comp[sc[nd[i]][j]] == c) ne++;
        if (ne == 0) continue;
        /* division-free cycle? w=1 nodes have one successor */
        int zc = 0;
        for (int i = 0; i < nn; i++) { int r = nd[i]; int vis[MAXQ] = {0}; int x = r, k = 0;
            while (W_[x] == 1 && comp[x] == c && !vis[x]) { vis[x] = 1; x = sc[x][0]; k++; }
            if (W_[x] == 1 && comp[x] == c && vis[x]) { /* cycle through x */
                int y = x, um = 0; long long dr = 0;
                do { if (U_[y] > 1) um = 1; dr += V_[y]; y = sc[y][0]; } while (y != x);
                if (um || dr > 0) zdiv = 1; else zneu = 1; zc = 1; } }
        if (zc) { hasz = 1; continue; }
        if (ne == nn) { int cyc[MAXQ], L = 0, x = nd[0];
            do { cyc[L++] = x; int nx = -1; for (int j = 0; j < ns[x]; j++) if (comp[sc[x][j]] == c) nx = sc[x][j]; x = nx; } while (x != nd[0]);
            int sg = cyc_sign(cyc, L); double m = 0; for (int i = 0; i < L; i++) m += lw[cyc[i]]; m /= L; if (m > mumax) mumax = m;
            if (sg > 0) hasb = 1; else if (sg == 0) { fb = 1; } /* U = W with W > 1 impossible under H1 */
            continue; }
        int cyc[MAXQ+1], L; double mu = karp(c, nd, nn, cyc, &L); if (mu > mumax) mumax = mu;
        if (L > 0 && cyc_sign(cyc, L) > 0) { hasc = 1; continue; }
        if (mu < -1e-12 && potential(c, nd, nn, mu)) continue;     /* type a, verified */
        fb = 1;
    }
    *mu_out = mumax;
    if (zdiv) return 3;
    if (zneu) return 5;
    if (fb) return 4;
    if (hasc) return 2;
    if (hasb) return 1;
    return 0;
}

int main(int argc, char **argv) {
    if (argc > 1 && strstr(argv[1], "printcert")) printcert = 1;
    if (argc > 1 && strstr(argv[1], "printall")) { printall = 1; printcert = 1; }
    if (scanf("%d %d %lld %llu", &Q, &mode, &count, &seed) != 4) return 2;
    if (Q > MAXQ) return 2;
    for (int r = 0; r < Q; r++) { if (scanf("%d", &nopt[r]) != 1) return 2; if (nopt[r] < 1 || nopt[r] > MAXOPT) { fprintf(stderr, "bad option count\n"); return 2; }
        for (int i = 0; i < nopt[r]; i++) if (scanf("%lld %lld %lld", &ou[r][i], &ov[r][i], &ow[r][i]) != 3) return 2; }
    long long total = 1; double dtot = 1; for (int r = 0; r < Q; r++) { dtot *= nopt[r]; }
    if (mode == 0) { if (dtot > 4e12) { fprintf(stderr, "too many\n"); return 2; } total = (long long)dtot; } else total = count;
    long long cnt[6] = {0}; long long cert_cyc_known = 0, cert_cyc_hist[64] = {0}; int maxcyc = 0;
    int digit[MAXQ] = {0};
    for (long long it = 0; it < total; it++) {
        unsigned long long id = 0, mulr = 1;
        if (mode == 0) { /* digits already set */ }
        else for (int r = 0; r < Q; r++) digit[r] = (int)(rng() % (unsigned long long)nopt[r]);
        for (int r = 0; r < Q; r++) { U_[r] = ou[r][digit[r]]; V_[r] = ov[r][digit[r]]; W_[r] = ow[r][digit[r]]; }
        double mu; int code = classify(&mu); cnt[code]++;
        char ix[512]; int p = 0; for (int r = 0; r < Q; r++) p += sprintf(ix + p, "%d%s", digit[r], r < Q-1 ? "." : "");
        (void)id; (void)mulr;
        if (code == 1) printf("B %s\n", ix);
        else if (printall && code == 2) printf("C %s\n", ix);
        else if (printall && code == 3) printf("Z %s\n", ix);
        else if (code == 5) printf("ZN %s\n", ix);
        else if (code == 4) printf("FALLBACK %s\n", ix);
        else if (code == 0) { long long mm = 0; int nc = count_cycles(&mm);
            if (nc >= 0) { cert_cyc_known++; if (nc < 63) cert_cyc_hist[nc]++; else cert_cyc_hist[63]++; if (nc > maxcyc) maxcyc = nc; }
            if (printcert) printf("CERT %s %.9f %d %lld\n", ix, mu, nc, mm); }
        if (mode == 0) { for (int r = 0; r < Q; r++) { if (++digit[r] < nopt[r]) break; digit[r] = 0; } }
    }
    printf("SUMMARY total %lld CERT %lld B %lld C %lld Z %lld ZN %lld FALLBACK %lld cert_cycles_known %lld maxcycles %d hist",
           total, cnt[0], cnt[1], cnt[2], cnt[3], cnt[5], cnt[4], cert_cyc_known, maxcyc);
    for (int i = 0; i < 64; i++) if (cert_cyc_hist[i]) printf(" %d:%lld", i, cert_cyc_hist[i]);
    printf("\n");
    return 0;
}
