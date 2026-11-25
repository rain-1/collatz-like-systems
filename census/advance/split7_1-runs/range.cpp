// Exact residue-tree certificate: every 1 <= n < 2^bits reaches the cycle (1 8 4 2)
// of T: even n -> n/2; n = 1 mod 4 -> 7n+1; n = 3 mod 4 -> n+1.
// Build: g++ -O3 -std=c++17 -pthread range.cpp -o range ; run: ./range BITS [SPLIT]
#include <algorithm>
#include <atomic>
#include <cstdint>
#include <iostream>
#include <mutex>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

using Integer = unsigned __int128;

static std::string decimal(Integer n) {
    std::string s;
    do { s.push_back('0' + int(n % 10)); n /= 10; } while (n);
    std::reverse(s.begin(), s.end());
    return s;
}

static const Integer LIMIT = (~Integer{0}) / 16;
static const Integer BIG = Integer{1} << 100;   // a,b < 2^100 and t < 2^60 keep a*t+b < 2^127

static Integer step(Integer n) {
    if (n % 2 == 0) return n / 2;
    if (n > LIMIT) throw std::overflow_error("raw iterate too large");
    return n % 4 == 1 ? 7 * n + 1 : n + 1;
}

struct Stats {
    Integer covered = 0;
    std::uint64_t nodes = 0, direct = 0, leaves_maxdepth = 0;
    unsigned max_steps = 0;
    unsigned max_depth_closed = 0;
    void add(const Stats &o) {
        covered += o.covered; nodes += o.nodes; direct += o.direct;
        leaves_maxdepth += o.leaves_maxdepth;
        max_steps = std::max(max_steps, o.max_steps);
        max_depth_closed = std::max(max_depth_closed, o.max_depth_closed);
    }
};

struct Cert {
    unsigned bits;
    Stats st;
    // Node: n = 2^depth * t + r (t >= 0), and a*t + b equals T^k(n) for some k >= 0
    // (the same k for every t). At a leaf, a*t+b < n is checked or simulated; a positive
    // iterate below n suffices by strong induction on n.
    void visit(unsigned depth, Integer r, Integer a, Integer b) {
        ++st.nodes;
        const Integer M = Integer{1} << depth;
        if (a >= BIG || b >= BIG) throw std::overflow_error("node coefficient too large");
        if (a < M || (a == M && b < r) || depth == bits) {
            Integer stop = Integer{1} << (bits - depth);
            const Integer first = (r == 0) ? 1 : 0;   // exclude n = 0
            st.covered += stop - first;
            if (depth == bits) ++st.leaves_maxdepth;
            else st.max_depth_closed = std::max(st.max_depth_closed, depth);
            if (a <= M && b < r) return;               // a*t+b < M*t+r for all t >= 0
            if (a < M) {
                // for t > (b-r)/(M-a): a t + b < M t + r
                Integer lim = (b >= r) ? (b - r) / (M - a) + 1 : 0;
                stop = std::min(stop, lim);
            }
            for (Integer t = first; t < stop; ++t) {
                const Integer n = M * t + r;
                Integer x = a * t + b;
                ++st.direct;
                unsigned s = 0;
                while (x >= n && x != 1) {   // x = 1: on the cycle (1 8 4 2)
                    if (++s > 10000000) throw std::runtime_error("unresolved " + decimal(n));
                    x = step(x);
                }
                st.max_steps = std::max(st.max_steps, s);
            }
            return;
        }
        for (unsigned d = 0; d < 2; ++d) {
            const Integer cr = r + d * M;
            const Integer y = b + d * a;   // value = 2a u + y on the child, t = 2u + d
            if (y % 2 == 0) visit(depth + 1, cr, a, y / 2);            // halve
            else if (a % 2) visit(depth + 1, cr, 2 * a, y);             // odd; residue mod 4 unknown yet
            else if (y % 4 == 1) visit(depth + 1, cr, 7 * (a / 2), (7 * y + 1) / 4); // 7x+1, /2, /2
            else visit(depth + 1, cr, a / 2, (y + 1) / 4);              // x+1, /2, /2
        }
    }
};

struct Task { unsigned depth; Integer r, a, b; };

int main(int argc, char **argv) {
    unsigned bits = argc > 1 ? std::stoul(argv[1]) : 40;
    unsigned split = argc > 2 ? std::stoul(argv[2]) : 14;
    if (bits < 1 || bits > 60) throw std::invalid_argument("bits in 1..60");
    // cycle check
    { Integer x = 1; for (int j = 1; j <= 4; ++j) { x = step(x); if ((x == 1) != (j == 4)) throw std::logic_error("cycle"); } }
    // Expand the top of the tree (identically to Cert::visit) into tasks.
    std::vector<Task> tasks; Stats top;
    std::vector<Task> frontier{{0, 0, 1, 0}};
    Cert topc{bits};
    while (!frontier.empty()) {
        Task k = frontier.back(); frontier.pop_back();
        const Integer M = Integer{1} << k.depth;
        if (k.a < M || (k.a == M && k.b < k.r) || k.depth == bits) { topc.visit(k.depth, k.r, k.a, k.b); continue; }
        if (k.depth == split) { tasks.push_back(k); continue; }
        ++topc.st.nodes;
        for (unsigned d = 0; d < 2; ++d) {
            const Integer cr = k.r + d * M, y = k.b + d * k.a;
            if (y % 2 == 0) frontier.push_back({k.depth + 1, cr, k.a, y / 2});
            else if (k.a % 2) frontier.push_back({k.depth + 1, cr, 2 * k.a, y});
            else if (y % 4 == 1) frontier.push_back({k.depth + 1, cr, 7 * (k.a / 2), (7 * y + 1) / 4});
            else frontier.push_back({k.depth + 1, cr, k.a / 2, (y + 1) / 4});
        }
    }
    top.add(topc.st);
    std::atomic<size_t> next{0};
    std::mutex mu; Stats total = top; std::string err;
    unsigned nth = std::max(1u, std::thread::hardware_concurrency());
    std::vector<std::thread> th;
    for (unsigned i = 0; i < nth; ++i) th.emplace_back([&] {
        Cert c{bits};
        try {
            for (size_t j; (j = next++) < tasks.size();) c.visit(tasks[j].depth, tasks[j].r, tasks[j].a, tasks[j].b);
        } catch (const std::exception &e) { std::lock_guard<std::mutex> g(mu); err = e.what(); }
        std::lock_guard<std::mutex> g(mu); total.add(c.st);
    });
    for (auto &t : th) t.join();
    if (!err.empty()) { std::cerr << "FAIL " << err << "\n"; return 1; }
    if (total.covered != (Integer{1} << bits) - 1) { std::cerr << "FAIL coverage " << decimal(total.covered) << "\n"; return 1; }
    std::cout << "bits=" << bits << " covered=" << decimal(total.covered) << " nodes=" << total.nodes
              << " direct=" << total.direct << " maxdepth_leaves=" << total.leaves_maxdepth
              << " max_extra_steps=" << total.max_steps << " OK\n";
    return 0;
}
