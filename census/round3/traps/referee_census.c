/* Referee: independent census of trap sets for C_a (n/2 | a n + 1).
 * Level m = k (beta = 1).  Graph: odd r -> (a r + 1) mod 2^k (one edge),
 * even r -> r/2, r/2 + 2^(k-1).  Nodes in A deleted.
 * Provable  <=> every nontrivial SCC is simple (all internal outdeg = 1)
 *               or has no expanding cycle (a^o > 2^E).
 * Expanding test: integer weights P (odd edge), -Q (halving edge), where
 * sign(oP - EQ) = sign(a^o - 2^E) for all o <= 64, E <= 200 was verified
 * exactly in Python (ref_weights in referee_check.py); simple cycles have
 * o + E <= 32, so positive-cycle detection with these weights is exact.
 * Output per subset mask (bit j <-> U[j] in A): one char
 *   '0' = H, '1' = provable with an expanding simple cycle somewhere (P1),
 *   '2' = provable, no expanding cycle at all (P0).
 * usage: ref_census a k all|odd P Q
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

int main(int argc, char **argv) {
    int a = atoi(argv[1]), k = atoi(argv[2]);
    int odd = strcmp(argv[3], "odd") == 0;
    long long P = atoll(argv[4]), Q = atoll(argv[5]);
    int K = 1 << k;
    int U[64], n = 0;
    for (int r = 0; r < K; r++) if (!odd || (r & 1)) U[n++] = r;
    int out[64][2], deg[64];
    for (int r = 0; r < K; r++) {
        if (r & 1) { out[r][0] = (int)(((long long)a * r + 1) % K); deg[r] = 1; }
        else { out[r][0] = r / 2; out[r][1] = r / 2 + K / 2; deg[r] = 2; }
    }
    for (long s = 0; s < (1L << n); s++) {
        uint64_t alive = 0;
        for (int r = 0; r < K; r++) alive |= 1ULL << r;
        for (int j = 0; j < n; j++) if (s >> j & 1) alive &= ~(1ULL << U[j]);
        uint64_t reach[64];  /* reach[v]: nodes reachable in >= 1 step */
        for (int r = 0; r < K; r++) {
            reach[r] = 0;
            if (!(alive >> r & 1)) continue;
            for (int t = 0; t < deg[r]; t++) if (alive >> out[r][t] & 1) reach[r] |= 1ULL << out[r][t];
        }
        for (int w = 0; w < K; w++) for (int v = 0; v < K; v++)
            if (reach[v] >> w & 1) reach[v] |= reach[w];
        int provable = 1, anyexp = 0;
        uint64_t done = 0;
        for (int v = 0; v < K && provable; v++) {
            if (!(alive >> v & 1) || (done >> v & 1)) continue;
            if (!(reach[v] >> v & 1)) { done |= 1ULL << v; continue; } /* trivial */
            uint64_t S = 0;
            for (int u = 0; u < K; u++)
                if ((alive >> u & 1) && (reach[v] >> u & 1) && (reach[u] >> v & 1)) S |= 1ULL << u;
            done |= S;
            int simple = 1;
            for (int u = 0; u < K; u++) if (S >> u & 1) {
                int c = 0;
                for (int t = 0; t < deg[u]; t++) if (S >> out[u][t] & 1) c++;
                if (c != 1) simple = 0;
            }
            /* positive cycle detection (Bellman-Ford longest path) */
            long long d[64];
            for (int u = 0; u < K; u++) d[u] = 0;
            int cnt = __builtin_popcountll(S), changed = 1, it;
            for (it = 0; it <= cnt && changed; it++) {
                changed = 0;
                for (int u = 0; u < K; u++) if (S >> u & 1)
                    for (int t = 0; t < deg[u]; t++) {
                        int w = out[u][t];
                        if (!(S >> w & 1)) continue;
                        long long wt = (u & 1) ? P : -Q;
                        if (d[u] + wt > d[w]) { d[w] = d[u] + wt; changed = 1; }
                    }
            }
            int expanding = changed; /* still relaxing after |S|+1 rounds */
            if (expanding) anyexp = 1;
            if (expanding && !simple) provable = 0;
        }
        putchar(provable ? (anyexp ? '1' : '2') : '0');
    }
    putchar('\n');
    return 0;
}
