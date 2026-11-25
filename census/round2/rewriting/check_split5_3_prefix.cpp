// Build: g++ -O3 -std=c++17 check_split5_3_prefix.cpp -o /tmp/split-prefix
#include <algorithm>
#include <array>
#include <boost/multiprecision/cpp_int.hpp>
#include <iostream>
#include <stdexcept>
#include <string>

using Integer = unsigned __int128;
constexpr unsigned budget = 512;

std::string decimal(Integer n) {
    std::string digits;
    do {
        digits.push_back('0' + static_cast<int>(n % 10));
        n /= 10;
    } while (n);
    std::reverse(digits.begin(), digits.end());
    return digits;
}

struct PrefixSearch {
    unsigned bits;
    std::array<unsigned, budget + 1> allowed{};
    Integer covered = 0, survivors = 0, witness = 0;
    unsigned latest = 0;

    explicit PrefixSearch(unsigned width) : bits(width) {
        // 5^(j-h) >= 4^j. Test whether h may increase at bit j.
        boost::multiprecision::cpp_int power = 1, threshold = 1;
        for (unsigned j = 1; j <= budget; ++j) {
            threshold *= 4;
            allowed[j] = allowed[j-1];
            if (power >= threshold) ++allowed[j];
            else power *= 5;
        }
    }

    void record(unsigned j, Integer y) {
        if (y >= 4 && j > latest) {
            latest = j;
            witness = y;
        }
    }

    void finish(Integer y, Integer z, unsigned j, unsigned ones, bool flag) {
        while (j < budget) {
            ++j;
            if (z % 2) {
                if (++ones > allowed[j]) {
                    record(j, y);
                    return;
                }
                z = z/2 + 2;
            } else {
                z /= 2;
                if (flag) {
                    if (z > ~Integer{0}/5) throw std::overflow_error("bit iterate");
                    z *= 5;
                }
                flag = !flag;
            }
        }
        throw std::runtime_error("unfinished start " + decimal(y));
    }

    // For y = r + 2^j * t, the current bit-state integer is b + a*t.
    // Here a = 5^floor((j-ones)/2) and b/a <= 3*j by the updates.
    void visit(unsigned j, Integer r, Integer a, Integer b, unsigned ones, bool flag) {
        if (j == bits) {
            ++covered;
            ++survivors;
            if (r >= 4) finish(r, b, j, ones, flag);
            return;
        }
        for (unsigned digit = 0; digit <= 1; ++digit) {
            const Integer next_r = r + (Integer{digit} << j);
            const Integer z = b + a*digit;
            if (z % 2) {
                if (ones + 1 > allowed[j+1]) {
                    covered += Integer{1} << (bits-j-1);
                    // Use the largest representative so a valid start is recorded even if next_r < 4.
                    const Integer last = (Integer{1} << bits) - (Integer{1} << (j+1)) + next_r;
                    record(j+1, last);
                } else {
                    visit(j+1, next_r, a, z/2 + 2, ones+1, flag);
                }
            } else if (flag) {
                visit(j+1, next_r, 5*a, 5*(z/2), ones, false);
            } else {
                visit(j+1, next_r, a, z/2, ones, true);
            }
        }
    }
};

int main(int argc, char **argv) {
    std::string argument = argc > 1 ? argv[1] : "66";
    if (argc > 2 || argument.empty() || argument.find_first_not_of("0123456789") != std::string::npos)
        throw std::invalid_argument("expected a bit depth from 3 through 66");
    auto value = std::stoul(argument);
    if (value < 3 || value > 66) throw std::invalid_argument("expected 3 to 66 bits");
    PrefixSearch search(static_cast<unsigned>(value));
    search.visit(0, 0, 1, 0, 0, false);
    Integer bound = Integer{1} << search.bits;
    if (search.covered != bound) throw std::logic_error("incomplete residue partition");
    std::cout << "Partitioned " << decimal(bound) << " residues; " << decimal(search.survivors)
              << " pass at full depth (including zero).\n";
    // Include three more shifted starts to cover every 1 <= x < 2^bits.
    for (Integer y = bound; y < bound+3; ++y) search.finish(y, y, 0, 0, false);
    std::cout << "For 4 <= y <= " << decimal(bound+2) << ", latest first crossing at bit "
              << search.latest << ", attained at y=" << decimal(search.witness) << "\n";
}
