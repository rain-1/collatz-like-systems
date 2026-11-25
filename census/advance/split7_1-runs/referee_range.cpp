// Referee (round 1) independent range certificate for CLS-053.
// T: even n -> n/2; n = 1 mod 4 -> 7n+1; n = 3 mod 4 -> n+1.
// Written from the definition, NOT from range.cpp: a node is (d, r, A, B) meaning
// "for every n = 2^d t + r (t >= 0), A t + B = T^k(n) for a k independent of t".
// Raw T steps are applied greedily whenever the parity (and, for odd values, the
// residue mod 4) of A t + B is independent of t; otherwise t is split by one bit.
// A class is closed when A t + B < 2^d t + r for every admissible t (checked as
// A <= 2^d and B < r), or by direct simulation of the finitely many remaining t.
// Coverage of 1..2^bits-1 is counted exactly.
// Build: g++ -O3 -std=c++17 -pthread referee_range.cpp -o rr ; run: ./rr BITS
#include <atomic>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <mutex>
#include <thread>
#include <vector>
typedef unsigned __int128 u128;
static unsigned BITS;
static const u128 CAP = ((u128)1) << 120;

static void die(const char *m) { fprintf(stderr, "FAIL %s\n", m); exit(1); }

static u128 Traw(u128 x) {
    if ((x & 1) == 0) return x >> 1;
    if (x > CAP) die("overflow in simulation");
    return (x & 3) == 1 ? 7 * x + 1 : x + 1;
}

struct St { u128 cov = 0; uint64_t nodes = 0, sims = 0; };

static void node(unsigned d, u128 r, u128 A, u128 B, St &s) {
    ++s.nodes;
    // greedy raw steps
    for (;;) {
        if (A > CAP || B > CAP) die("coefficient overflow");
        if ((A & 1) == 0 && (B & 1) == 0) { A >>= 1; B >>= 1; continue; }      // even for all t
        if ((A & 3) == 0 && (B & 1) == 1) {                                     // odd, residue mod 4 fixed
            if ((B & 3) == 1) { A = 7 * A; B = 7 * B + 1; } else { B = B + 1; }
            continue;
        }
        break;  // parity or residue depends on t
    }
    u128 M = ((u128)1) << d;
    u128 cnt = ((u128)1) << (BITS - d);          // t in [0, cnt) gives n < 2^BITS
    u128 t0 = (r == 0) ? 1 : 0;                   // exclude n = 0
    if (A <= M && B < r) { s.cov += cnt - t0; return; }
    if (A < M || d == BITS) {
        u128 tmax = cnt;                          // simulate t < tmax
        if (A < M) {
            // for t with (M-A) t > B - r the value is below n
            u128 lim = (B >= r) ? (B - r) / (M - A) + 1 : 0;
            if (lim < tmax) tmax = lim;
        }
        for (u128 t = t0; t < tmax; ++t) {
            u128 n = M * t + r, x = A * t + B;
            ++s.sims;
            uint64_t k = 0;
            while (x >= n && !(x == 1)) { x = Traw(x); if (++k > 100000000ULL) die("no drop"); }
        }
        s.cov += cnt - t0;
        return;
    }
    // split on bit d of n: t = 2u + e
    node(d + 1, r, 2 * A, B, s);
    node(d + 1, r + M, 2 * A, B + A, s);
}

int main(int argc, char **argv) {
    BITS = argc > 1 ? atoi(argv[1]) : 32;
    unsigned top = BITS < 14 ? BITS : 14;
    // enumerate classes mod 2^top as root tasks: (top, r, 2^top, r) is a valid node
    std::vector<u128> rs;
    for (uint64_t r = 0; r < (1ULL << top); ++r) rs.push_back(r);
    std::atomic<size_t> nx{0};
    std::mutex mu; St tot;
    std::vector<std::thread> th;
    unsigned nt = std::thread::hardware_concurrency(); if (!nt) nt = 1;
    for (unsigned i = 0; i < nt; ++i) th.emplace_back([&] {
        St s; size_t j;
        while ((j = nx++) < rs.size()) node(top, rs[j], ((u128)1) << top, rs[j], s);
        std::lock_guard<std::mutex> g(mu); tot.cov += s.cov; tot.nodes += s.nodes; tot.sims += s.sims;
    });
    for (auto &t : th) t.join();
    u128 want = (((u128)1) << BITS) - 1;
    printf("bits=%u covered=%llu want=%llu nodes=%llu sims=%llu %s\n", BITS,
           (unsigned long long)tot.cov, (unsigned long long)want,
           (unsigned long long)tot.nodes, (unsigned long long)tot.sims, tot.cov == want ? "OK" : "BAD");
    return tot.cov == want ? 0 : 1;
}
