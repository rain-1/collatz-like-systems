// Reproducible exact-arithmetic checks for Collatz's 1932 permutation.
// Compile: g++ -std=c++20 -O3 collatz_1932_two_sided.cpp -lgmpxx -lgmp -o orbit8
// Run: ./orbit8 [steps_per_direction]   (default: 1,000,000)
// This does not prove that the orbit of 8 is infinite.
#include <gmpxx.h>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <unordered_set>

struct Fingerprint {
    uint64_t low64;
    size_t bit_length;
    bool operator==(const Fingerprint& o) const {
        return low64 == o.low64 && bit_length == o.bit_length;
    }
};
struct FingerprintHash {
    size_t operator()(const Fingerprint& x) const {
        return x.low64 ^ (x.bit_length * UINT64_C(0x9e3779b97f4a7c15));
    }
};
static Fingerprint fingerprint(const mpz_class& n) {
    return {mpz_getlimbn(n.get_mpz_t(), 0), mpz_sizeinbase(n.get_mpz_t(), 2)};
}
static void forward(mpz_class& n, mpz_class& quotient) {
    unsigned r = mpz_fdiv_ui(n.get_mpz_t(), 3);
    mpz_fdiv_q_ui(quotient.get_mpz_t(), n.get_mpz_t(), 3);
    if (r == 0) n = 2 * quotient;
    else if (r == 1) n = 4 * quotient + 1;
    else n = 4 * quotient + 3;
}
static void backward(mpz_class& n) {
    if (mpz_even_p(n.get_mpz_t())) {
        n *= 3; n /= 2;
    } else if (mpz_fdiv_ui(n.get_mpz_t(), 4) == 1) {
        n *= 3; ++n; n /= 4;
    } else {
        n *= 3; --n; n /= 4;
    }
}
int main(int argc, char** argv) {
    size_t steps = argc >= 2 ? std::strtoull(argv[1], nullptr, 10) : 1000000;
    std::unordered_set<Fingerprint, FingerprintHash> forward_fingerprints;
    forward_fingerprints.reserve(steps + 1);
    mpz_class a = 8, b = 8, q;
    forward_fingerprints.insert(fingerprint(a));
    size_t c_forward = 0, c_backward = 0;
    for (size_t i = 0; i < steps; ++i) {
        c_forward += (mpz_fdiv_ui(a.get_mpz_t(), 3) == 0);
        forward(a, q);
        if (!forward_fingerprints.insert(fingerprint(a)).second) {
            std::printf("A forward fingerprint repeated at step %zu: investigate exact equality.\n", i+1);
            return 1;
        }
    }
    for (size_t i = 0; i < steps; ++i) {
        backward(b);
        c_backward += (mpz_fdiv_ui(b.get_mpz_t(), 3) == 0);
        if (forward_fingerprints.contains(fingerprint(b))) {
            std::printf("Forward/backward fingerprint overlap at backward step %zu: investigate exact equality.\n", i+1);
            return 2;
        }
    }
    // Equal integers necessarily share fingerprints, so the complete absence of
    // fingerprint matches rigorously implies that there are no equal integers.
    std::printf("No cycle with period <= %zu.\n", 2*steps);
    std::printf("Forward zeros: %zu; backward zeros: %zu.\n", c_forward, c_backward);
    std::printf("G^N(8) bits: %zu; G^(-N)(8) bits: %zu.\n",
                mpz_sizeinbase(a.get_mpz_t(), 2), mpz_sizeinbase(b.get_mpz_t(), 2));
    // Every positive n satisfies G(n)+1 <= (4/3)*(n+1).
    // If a cycle has period L=2*steps+t, then G^t(a)=b, so
    // (4/3)^t*(a+1) >= b+1. Find the exact least possible t.
    mpz_class left = a + 1, right = b + 1;
    size_t t = 0;
    while (left < right) { left *= 4; right *= 3; ++t; }
    std::printf("Required middle-segment length >= %zu.\n", t);
    std::printf("A hypothetical cycle has period >= %zu.\n", 2*steps+t);
}
