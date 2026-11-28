"""Check for c62_64_s27.md.  Exit 0 on success.

 (1) table: T(n) = n/2 (even), (3n+1)/2 (odd), except n = 62 (mod 64) -> 4n+5;
     non-injective (T(253) = 380 = T(760));  Haar-average log-slope < 0 (exact
     comparison 3^32 * 8 < 4^32, see below);
 (2) U = {41, 62, 124, 190, 253, 318, 380, 446} (mod 512) is forward closed,
     ascent witness (Lemma A-up) and forced falls (Lemma F) verify exactly;
 (3) the pump T^3(n) = 3n + 6 on n = 253 (mod 512) (symbolic: checked on the
     class as an affine identity at many points incl. huge ones) and the orbit
     of 27 reaches 253 at step 3;
 (4) Lemma I does NOT apply: U has a closed walk with 2-adic unit product
     (that is the pump), reported for honesty.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from systems import get  # noqa: E402
from divlib import is_closed, ascent_certificate, verify_ascent, nonfall_subgraph_acyclic, aperiodic_certificate  # noqa: E402


def main():
    T = get("c62_64_s27")["rcwa"]
    T.check()
    for n in range(1, 100001):
        ref = 4 * n + 5 if n % 64 == 62 else (n // 2 if n % 2 == 0 else (3 * n + 1) // 2)
        assert T(n) == ref
    assert T(253) == T(760) == 380
    # average log slope over one period (Haar measure on Z_2):
    # (1/64)[31 log(1/2) + 32 log(3/2) + log 4] < 0  <=>  3^32 * 4 < 2^32 * 2^31 ... exact:
    num = 3 ** 32 * 4          # product of numerators over the 64 classes
    den = 2 ** 31 * 2 ** 32    # product of denominators
    assert num < den
    U = [41, 62, 124, 190, 253, 318, 380, 446]
    assert is_closed(T, 512, U)
    cert = ascent_certificate(T, 512, U)
    assert cert and verify_ascent(T, cert)
    assert nonfall_subgraph_acyclic(T, 512, U)
    for t in list(range(0, 2000)) + [10 ** 40 + 3, 7 ** 90]:
        n = 512 * t + 253
        assert T(T(T(n))) == 3 * n + 6 and (3 * n + 6) % 512 == 253
    x = 27
    for _ in range(3):
        x = T(x)
    assert x == 253
    assert aperiodic_certificate(T, 512, U, 2) is None
    print("c62_64_s27: trap mod 512 verified; pump T^3(n)=3n+6 on 253 mod 512; drift < 0")
    print("OK")


if __name__ == "__main__":
    main()
