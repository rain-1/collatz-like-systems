// Build: c++ -O3 -std=c++17 verify_long_orbit.cpp -lgmp -o verify_long_orbit
// Run: ./verify_long_orbit BACKWARD_DEPTH
// If the least period is L, then G^17(243)=8 puts 8 at inverse depth L-17
// from 243. Excluding powers of two through depth N-1 proves L >= N+17.
// The inverse endpoint is then G^(L-N-17)(8). Its bit length cannot appear
// before the first forward index K reaching that length, so L >= N+17+K.
// A positive power of three reaching 243 must pass through a power of two
// on the way. Thus the same inverse check excludes it through depth N.
// Reproduction at N=1000000000: endpoint 84982734 bits (low word 1c28f8dc),
// K=1039805591, period >= 2039805608. Peak v3=27 first at depth 255111836.
#include <gmp.h>
#include <algorithm>
#include <array>
#include <charconv>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <stdexcept>

using Index = std::uint64_t;
constexpr int leaf_steps = 8;
constexpr int levels = 19; // Largest arithmetic block: 2,097,152 steps.
constexpr int guard = 64;

// The leading bits locate each endpoint on the log2 scale without printing it.
void print_endpoint_prefix(const char* direction, mpz_srcptr n) {
    const size_t bits = mpz_sizeinbase(n, 2);
    mpz_t prefix;
    mpz_init(prefix);
    mpz_fdiv_q_2exp(prefix, n, bits > 128 ? bits - 128 : 0);
    gmp_printf("%s endpoint: %zu bits, leading min(128,bits) bits in hex: %Zx\n",
               direction, bits, prefix);
    mpz_clear(prefix);
}

struct Integer {
    mpz_t z;
    Integer() { mpz_init(z); }
    ~Integer() { mpz_clear(z); }
    Integer(const Integer&) = delete;
    Integer& operator=(const Integer&) = delete;
};

struct Block {
    unsigned value = 0, bits = 0, prefix = 0, suffix = 0, longest = 0;
    unsigned first_peak_end = 0;
};

struct Search {
    std::array<Block, 65536> inverse{};
    std::array<Block, 6561> forward{};
    std::array<Integer, levels> three, high;
    unsigned even_streak = 0, max_streak = 0;
    Index inverse_index = 0, first_peak_depth = 0;

    Search() {
        mpz_set_ui(three[0].z, 6561);
        for (int i = 1; i < levels; ++i)
            mpz_mul(three[i].z, three[i-1].z, three[i-1].z);
        for (unsigned x = 0; x < inverse.size(); ++x) {
            Block& b = inverse[x];
            unsigned n = x;
            for (unsigned i = 0; i < leaf_steps; ++i) {
                bool odd = n & 1;
                b.bits += 1 + odd;
                if (!odd && b.prefix == i) ++b.prefix;
                b.suffix = odd ? 0 : b.suffix + 1;
                if (b.suffix > b.longest) {
                    b.longest = b.suffix;
                    b.first_peak_end = i+1;
                }
                if (!odd) n = 3*n/2;
                else if ((n & 3) == 1) n = (3*n+1)/4;
                else n = (3*n-1)/4;
            }
            b.value = n;
        }
        for (unsigned x = 0; x < forward.size(); ++x) {
            Block& b = forward[x];
            unsigned n = x;
            for (int i = 0; i < leaf_steps; ++i) {
                unsigned r = n % 3;
                b.bits += 1 + (r != 0);
                n = r == 0 ? 2*(n/3) : 4*(n/3) + 2*r-1;
            }
            b.value = n;
        }
    }

    void observe(unsigned length, Index end) {
        if (length > max_streak) {
            max_streak = length;
            first_peak_depth = end;
        }
    }

    void record(const Block& b) {
        observe(even_streak + b.prefix, inverse_index + b.prefix);
        observe(b.longest, inverse_index + b.first_peak_end);
        even_streak = b.prefix == leaf_steps ? even_streak + leaf_steps : b.suffix;
        inverse_index += leaf_steps;
    }

    // On writing n = q*M + r the branch sequence depends only on r.
    // For k steps, differences transform by 2^e/3^k, or by its inverse.
    // Recurse on the small remainder, then restore the high part exactly.
    template<bool backwards>
    unsigned advance(mpz_ptr n, int level) {
        if (level == 0) {
            if constexpr (backwards) {
                const Block& b = inverse[mpz_get_ui(n) & 65535];
                record(b);
                mpz_fdiv_q_2exp(n, n, 16);
                mpz_mul_ui(n, n, 6561);
                mpz_mul_2exp(n, n, 16 - b.bits);
                mpz_add_ui(n, n, b.value);
                return b.bits;
            } else {
                const Block& b = forward[mpz_fdiv_q_ui(n, n, 6561)];
                mpz_mul_2exp(n, n, b.bits);
                mpz_add_ui(n, n, b.value);
                return b.bits;
            }
        }
        unsigned k = leaf_steps << level;
        mpz_ptr q = high[level].z;
        if constexpr (backwards) {
            mpz_fdiv_q_2exp(q, n, 2*k);
            mpz_fdiv_r_2exp(n, n, 2*k);
        } else {
            mpz_fdiv_qr(q, n, n, three[level].z);
        }
        unsigned e = advance<backwards>(n, level-1);
        e += advance<backwards>(n, level-1);
        if (mpz_cmp_ui(q, 0) != 0) {
            if constexpr (backwards) {
                mpz_mul(q, q, three[level].z);
                mpz_mul_2exp(q, q, 2*k-e);
            } else {
                mpz_mul_2exp(q, q, e);
            }
            mpz_add(n, n, q);
        }
        return e;
    }

    void inverse_step(mpz_ptr n) {
        unsigned low = mpz_get_ui(n) & 3;
        even_streak = (low & 1) ? 0 : even_streak + 1;
        observe(even_streak, ++inverse_index);
        mpz_mul_ui(n, n, 3);
        if (low == 1) mpz_add_ui(n, n, 1);
        if (low == 3) mpz_sub_ui(n, n, 1);
        mpz_fdiv_q_2exp(n, n, 1 + (low & 1));
    }

    static int block_level(Index budget) {
        int level = 0;
        while (level+1 < levels && (Index(leaf_steps) << (level+1)) <= budget)
            ++level;
        return level;
    }

    size_t backwards_from_243(Index depth) {
        Integer n;
        mpz_set_ui(n.z, 243);
        for (Index i = 0; i < depth;) {
            size_t bits = mpz_sizeinbase(n.z, 2);
            // Each inverse step gives at least n/2. Every block input stays
            // above 2^64. A power of two there forces 64 consecutive even inputs.
            Index budget = std::min<Index>(depth-i, bits > guard+2 ? bits-guard-2 : 0);
            if (budget < leaf_steps) {
                if (mpz_popcount(n.z) == 1)
                    throw std::runtime_error("Found a power of two in the predecessor search");
                inverse_step(n.z);
                ++i;
            } else {
                int level = block_level(budget);
                advance<true>(n.z, level);
                i += Index(leaf_steps) << level;
            }
        }
        size_t bits = mpz_sizeinbase(n.z, 2);
        print_endpoint_prefix("Backward", n.z);
        std::printf("Inverse endpoint low 32 bits: %08lx\n", mpz_get_ui(n.z) & 0xffffffffUL);
        // At positive depths the 3-adic valuation equals the immediately
        // preceding even run: an odd inverse step always produces a 3-adic unit.
        std::printf("Maximum v3 at positive depths: %u; first depth: %llu\n",
                    max_streak, (unsigned long long)first_peak_depth);
        // Cover any streak beginning just before the endpoint.
        for (int j = 0; j < guard; ++j) inverse_step(n.z);
        if (max_streak >= guard)
            throw std::runtime_error("Streak threshold reached; power-of-two exclusion inconclusive");
        return bits;
    }

    Index first_forward_bits(size_t target) {
        Integer n;
        mpz_set_ui(n.z, 8);
        Index i = 0;
        for (;;) {
            size_t bits = mpz_sizeinbase(n.z, 2);
            if (bits >= target) {
                print_endpoint_prefix("Forward", n.z);
                return i;
            }
            Index budget = target-bits-1; // G(n) <= 2n.
            if (budget < leaf_steps) {
                unsigned long r = mpz_fdiv_q_ui(n.z, n.z, 3);
                mpz_mul_2exp(n.z, n.z, 1 + (r != 0));
                if (r) mpz_add_ui(n.z, n.z, 2*r-1);
                ++i;
            } else {
                int level = block_level(budget);
                advance<false>(n.z, level);
                i += Index(leaf_steps) << level;
            }
        }
    }
};

int main(int argc, char** argv) {
    Index depth = 0;
    if (argc != 2) return 2;
    const char* end = argv[1] + std::strlen(argv[1]);
    auto parsed = std::from_chars(argv[1], end, depth);
    if (parsed.ec != std::errc{} || parsed.ptr != end || !depth || depth > 1000000000000ULL)
        return 2;
    static Search s;
    auto start = std::chrono::steady_clock::now();
    auto elapsed = [&]() {
        return std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    };
    size_t bits = s.backwards_from_243(depth);
    std::printf("Backward steps: %llu; endpoint bits: %zu; longest even run including guard: %u; seconds: %.2f\n",
                (unsigned long long)depth, bits, s.max_streak, elapsed());
    std::fflush(stdout);
    Index forward = s.first_forward_bits(bits);
    std::printf("First forward index: %llu; period lower bound: %llu; total seconds: %.2f\n",
                (unsigned long long)forward, (unsigned long long)(depth+17+forward), elapsed());
    return 0;
}
