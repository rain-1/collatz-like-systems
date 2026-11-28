/* survive.c -- exact enumeration of stopping times for polynomial table maps over F_q, q in {2,3,4}.

   A system is a prefix code of branches.  Branch i: digits r_0..r_{e-1} (f = r mod t^e),
       T(f) = g * (f - r) / t^e + c ,      g(0) != 0.
   Each step consumes exactly e t-adic digits (Terras bijection), slope deg g - e.

   sigma(f) = number of t-divisions performed up to the end of the first step after which
   deg T^k(f) < deg f  (the zero polynomial has degree -infinity).  Capped at BCAP.

   Usage: survive SPECFILE Dmin Dmax BCAP
   Output lines:  "S D b N"  with N = #{deg f = D : sigma(f) > b}, b = 0..BCAP
                  "R D sigma f-coeffs"  for the record (max sigma) start in each degree
   F_4 = {0,1,w,w^2} coded 0,1,2,3 with w^2 = w+1: addition is XOR of 2-bit codes.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFN 16384
static int q;
static unsigned char ADD[4][4], MUL[4][4], NEG[4];
static int nbr;
static int be[64], br[64][16], bdg[64], bg[64][32], bdc[64], bc[64][32];
/* trie over digits for branch lookup */
static int trie[4096][4]; static int ntrie = 1; /* value: >=0 child node, -2-i leaf branch i, -1 none */

static void field_init(void) {
    for (int a = 0; a < q; a++) for (int b = 0; b < q; b++) {
        if (q == 2 || q == 4) ADD[a][b] = a ^ b;
        else ADD[a][b] = (a + b) % 3;
        if (q == 2) MUL[a][b] = a & b;
        else if (q == 3) MUL[a][b] = (a * b) % 3;
        else {
            /* log table: 1 = w^0, 2 = w^1, 3 = w^2 */
            if (a == 0 || b == 0) MUL[a][b] = 0;
            else { int la = a - 1, lb = b - 1; MUL[a][b] = (unsigned char)(((la + lb) % 3) + 1); }
        }
    }
    for (int a = 0; a < q; a++) for (int b = 0; b < q; b++) if (ADD[a][b] == 0) NEG[a] = b;
}

static void read_spec(const char *fn) {
    FILE *fp = fopen(fn, "r");
    if (!fp) { perror("spec"); exit(2); }
    char tok[64];
    nbr = 0;
    while (fscanf(fp, "%63s", tok) == 1) {
        if (!strcmp(tok, "q")) { if (fscanf(fp, "%d", &q) != 1) exit(2); }
        else if (!strcmp(tok, "B")) {
            int i = nbr++;
            if (fscanf(fp, "%d", &be[i]) != 1) exit(2);
            for (int j = 0; j < be[i]; j++) if (fscanf(fp, "%d", &br[i][j]) != 1) exit(2);
            if (fscanf(fp, "%63s", tok) != 1 || strcmp(tok, "G")) exit(3);
            if (fscanf(fp, "%d", &bdg[i]) != 1) exit(2);
            for (int j = 0; j <= bdg[i]; j++) if (fscanf(fp, "%d", &bg[i][j]) != 1) exit(2);
            if (fscanf(fp, "%63s", tok) != 1 || strcmp(tok, "C")) exit(3);
            if (fscanf(fp, "%d", &bdc[i]) != 1) exit(2);
            for (int j = 0; j <= bdc[i]; j++) if (fscanf(fp, "%d", &bc[i][j]) != 1) exit(2);
            if (bg[i][0] == 0) { fprintf(stderr, "g(0)=0\n"); exit(3); }
        } else if (tok[0] == '#') { int ch; while ((ch = fgetc(fp)) != '\n' && ch != EOF); }
        else { fprintf(stderr, "bad token %s\n", tok); exit(3); }
    }
    fclose(fp);
    for (int k = 0; k < 4096; k++) for (int d = 0; d < 4; d++) trie[k][d] = -1;
    for (int i = 0; i < nbr; i++) {
        int node = 0;
        for (int j = 0; j < be[i]; j++) {
            int d = br[i][j];
            if (j == be[i] - 1) { if (trie[node][d] != -1) { fprintf(stderr, "not prefix code\n"); exit(3);} trie[node][d] = -2 - i; }
            else { if (trie[node][d] == -1) trie[node][d] = ntrie++; else if (trie[node][d] < 0) { fprintf(stderr, "not prefix code\n"); exit(3);} node = trie[node][d]; }
        }
    }
    /* completeness check: every node has all q children */
    for (int k = 0; k < ntrie; k++) for (int d = 0; d < q; d++) if (trie[k][d] == -1) { fprintf(stderr, "incomplete code\n"); exit(3); }
}

static unsigned char buf[BUFN];

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage\n"); return 2; }
    read_spec(argv[1]);
    field_init();
    int Dmin = atoi(argv[2]), Dmax = atoi(argv[3]), BCAP = atoi(argv[4]);
    long long *cnt = calloc((size_t)(BCAP + 2), sizeof(long long));
    unsigned char f0[64];
    for (int D = Dmin; D <= Dmax; D++) {
        memset(cnt, 0, (size_t)(BCAP + 2) * sizeof(long long));
        int recsig = -1; unsigned char rec[64];
        /* enumerate coefficient vectors: digits 0..D-1 any, digit D nonzero */
        memset(f0, 0, sizeof f0);
        f0[D] = 1;
        for (;;) {
            /* run orbit */
            int s = 0, len = D + 1;
            memcpy(buf, f0, (size_t)len);
            int digits = 0, sig = BCAP + 1;
            while (digits <= BCAP) {
                /* find branch */
                int node = 0, j = 0, bi;
                for (;;) {
                    int d = (j < len) ? buf[s + j] : 0;
                    int nx = trie[node][d];
                    j++;
                    if (nx <= -2) { bi = -2 - nx; break; }
                    node = nx;
                }
                int e = be[bi];
                /* f - r */
                for (int k = 0; k < e; k++) {
                    if (k < len) buf[s + k] = ADD[buf[s + k]][NEG[br[bi][k]]];
                    else { /* f has fewer coefficients; extend with zeros */
                        for (int z = len; z <= k; z++) buf[s + z] = 0; len = k + 1;
                        buf[s + k] = ADD[buf[s + k]][NEG[br[bi][k]]];
                    }
                    if (buf[s + k] != 0) { fprintf(stderr, "division not exact\n"); return 4; }
                }
                s += e; len -= e; if (len < 0) len = 0;
                /* multiply by g in place, descending */
                int dg = bdg[bi];
                int nl = len > 0 ? len + dg : 0;
                for (int i = nl - 1; i >= 0; i--) {
                    unsigned char w = 0;
                    for (int jj = 0; jj <= dg; jj++) {
                        int ii = i - jj;
                        if (ii >= 0 && ii < len) w = ADD[w][MUL[bg[bi][jj]][buf[s + ii]]];
                    }
                    buf[s + i] = w;
                }
                len = nl;
                /* add c */
                for (int k = 0; k <= bdc[bi]; k++) {
                    if (k >= len) { for (int z = len; z <= k; z++) buf[s + z] = 0; len = k + 1; }
                    buf[s + k] = ADD[buf[s + k]][bc[bi][k]];
                }
                while (len > 0 && buf[s + len - 1] == 0) len--;
                digits += e;
                if (len - 1 < D) { sig = digits; break; }
                if (s > BUFN / 2) { memmove(buf, buf + s, (size_t)len); s = 0; }
                if (s + len + 64 > BUFN) { fprintf(stderr, "overflow\n"); return 5; }
            }
            if (sig > BCAP + 1) sig = BCAP + 1;
            /* sigma > b for b < sig */
            cnt[sig < BCAP + 1 ? sig : BCAP + 1]++;
            if (sig > recsig) { recsig = sig; memcpy(rec, f0, (size_t)(D + 1)); }
            /* next f0 */
            int k = 0;
            while (k < D) { f0[k]++; if (f0[k] < q) break; f0[k] = 0; k++; }
            if (k == D) { f0[D]++; if (f0[D] >= q) break; }
        }
        /* cumulative: N(b) = #{sig > b} */
        long long tail = 0;
        long long *N = calloc((size_t)(BCAP + 2), sizeof(long long));
        for (int b = BCAP + 1; b >= 0; b--) { if (b <= BCAP) N[b] = tail; tail += cnt[b]; (void)0; }
        /* N[b] = sum_{sig > b} cnt[sig] */
        for (int b = 0; b <= BCAP; b++) {
            long long v = 0; for (int sg = b + 1; sg <= BCAP + 1; sg++) v += cnt[sg];
            printf("S %d %d %lld\n", D, b, v);
        }
        printf("R %d %d", D, recsig);
        for (int k = 0; k <= D; k++) printf(" %d", rec[k]);
        printf("\n");
        fflush(stdout);
        free(N);
    }
    return 0;
}
