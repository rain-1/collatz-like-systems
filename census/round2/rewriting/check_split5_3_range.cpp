// Exact extension of check_split5_3_range.py to start ranges through 66 bits.
// Build with g++ -O3 -std=c++17 check_split5_3_range.cpp -o /tmp/split-range
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>

using Integer = unsigned __int128;

std::string decimal(Integer n) {
    std::string result;
    do {
        result.push_back('0' + static_cast<int>(n % 10));
        n /= 10;
    } while (n);
    std::reverse(result.begin(), result.end());
    return result;
}

constexpr std::array<unsigned, 5> roots{1, 3, 5, 61, 125};
constexpr std::array<unsigned, 5> periods{4, 2, 5, 10, 11};

Integer step(Integer n) {
    if (n % 2 == 0) return n / 2;
    const unsigned factor = n % 4 == 1 ? 5 : 1;
    if (n > (~Integer{0} - 3) / factor)
        throw std::overflow_error("raw iterate exceeds 128 bits");
    return factor * n + 3;
}

bool is_root(Integer n) {
    return n <= 125 && std::find(roots.begin(), roots.end(),
                                 static_cast<unsigned>(n)) != roots.end();
}

struct Certificate {
    unsigned bits;
    Integer covered = 0;
    std::uint64_t nodes = 0, direct = 0;
    unsigned max_steps = 0;

    // On n = 2^depth * t + r the arithmetic image a*t + b is reached.
    void visit(unsigned depth, Integer r, Integer a, Integer b) {
        ++nodes;
        const Integer modulus = Integer{1} << depth;
        if (a < modulus || (a == modulus && b < r) || depth == bits) {
            Integer stop = Integer{1} << (bits - depth);
            const Integer first = r == 0 ? 1 : 0;
            covered += stop - first;
            if (a <= modulus && b < r) return;
            if (a < modulus)
                stop = std::min(stop, (b - r) / (modulus - a) + 1);
            for (Integer t = first; t < stop; ++t) {
                const Integer n = modulus*t + r;
                Integer x = a*t + b;
                ++direct;
                unsigned steps = 0;
                while (x >= n && !is_root(x)) {
                    if (++steps > 100000)
                        throw std::runtime_error("unresolved start " + decimal(n));
                    x = step(x);
                }
                max_steps = std::max(max_steps, steps);
            }
            return;
        }
        for (unsigned digit = 0; digit < 2; ++digit) {
            const Integer child_r = r + digit*modulus;
            const Integer y = b + digit*a;
            if (y % 2 == 0) visit(depth+1, child_r, a, y/2);
            else if (a % 2) visit(depth+1, child_r, 2*a, y);
            else if (y % 4 == 1) visit(depth+1, child_r, 5*(a/2), (5*y+3)/4);
            else visit(depth+1, child_r, a, (y+3)/2);
        }
    }
};

int main(int argc, char **argv) {
    std::string argument = argc > 1 ? argv[1] : "64";
    if (argc > 2 || argument.empty() || argument.find_first_not_of("0123456789") != std::string::npos)
        throw std::invalid_argument("expected 1 to 66 bits");
    const auto requested = std::stoul(argument);
    if (requested == 0 || requested > 66) throw std::invalid_argument("expected 1 to 66 bits");
    const unsigned bits = static_cast<unsigned>(requested);
    for (unsigned i = 0; i < roots.size(); ++i) {
        Integer x = roots[i];
        for (unsigned j = 1; j <= periods[i]; ++j) {
            x = step(x);
            if ((x == roots[i]) != (j == periods[i]))
                throw std::logic_error("cycle period mismatch");
        }
    }
    // Along a path a <= (5/2)^depth. The ratio b/a increases by at
    // most 1 from selecting a digit and at most 3/2 from the additive
    // correction, since a >= 1. Thus b/a <= 3*depth and all
    // node arithmetic is < 2^101 through depth 66. For a leaf,
    // a*t <= (5/2)^depth * 2^(bits-depth) < 2^88.
    Certificate cert{bits};
    cert.visit(0, 0, 1, 0);
    if (cert.covered != (Integer{1} << bits)-1)
        throw std::logic_error("incomplete coverage");
    std::cout << decimal(cert.covered) << " starts certified, " << cert.nodes
              << " tree nodes, " << cert.direct << " individual checks, at most "
              << cert.max_steps << " extra raw steps\n";
}
