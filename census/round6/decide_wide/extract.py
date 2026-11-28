"""extract.py -- recover a table form (Q, [(u, v, w)]) from a step function.

`extract(step)` tries moduli Q = 2^a 3^b 5^c 7^d 11^e <= QMAX in increasing order.  On each
class r mod Q it fits T(n) = alpha n + beta from two points n >= Q (t >= 1) and accepts Q if the
fit holds exactly at t = 1..12 and at four large t.  The table is then checked exactly against
the step function at every n in [1, NCHECK] (n <= Q included), and the n where they differ are
returned as `exceptions` (e.g. Farkas's rule 1 -> 1).  A system for which no Q works is
reported as not a table map.  This is a recognizer, not a proof: every table it returns is
re-checked against the step function, and the census statements in the sweep are about the
returned table (with the listed exceptions).
"""
from fractions import Fraction
import math

QMAX = 2200
NCHECK = 20000


def smooth(limit):
    out = set()
    for a in range(12):
        for b in range(8):
            for c in range(5):
                for d in range(4):
                    for e in range(3):
                        q = 2 ** a * 3 ** b * 5 ** c * 7 ** d * 11 ** e
                        if q <= limit:
                            out.add(q)
    return sorted(out)


QS = smooth(QMAX)


def _val(step, n):
    try:
        y = step(n)
    except Exception:
        return None
    if isinstance(y, bool) or not isinstance(y, int):
        return None
    return y


def fit_class(step, Q, r):
    n1, n2 = Q + r, 2 * Q + r
    y1, y2 = _val(step, n1), _val(step, n2)
    if y1 is None or y2 is None:
        return None
    al = Fraction(y2 - y1, Q)
    be = y1 - al * n1
    for t in list(range(3, 14)) + [101, 977, 10007, 123457]:
        n = t * Q + r
        y = _val(step, n)
        if y is None or y != al * n + be:
            return None
    if al <= 0:
        return None
    w = al.denominator * be.denominator // math.gcd(al.denominator, be.denominator)
    u, v = al * w, be * w
    assert u.denominator == 1 and v.denominator == 1
    return (int(u), int(v), int(w))


def extract(step, qs=QS, ncheck=NCHECK):
    if _val(step, 7) is None:
        return None
    for Q in qs:
        tab = []
        for r in range(Q):
            f = fit_class(step, Q, r)
            if f is None:
                break
            tab.append(f)
        else:
            # integrality on every class
            if not all((u * r + v) % w == 0 and (u * Q) % w == 0 for r, (u, v, w) in enumerate(tab)):
                continue
            exc = []
            for n in range(1, ncheck + 1):
                u, v, w = tab[n % Q]
                y = _val(step, n)
                if y is None or y * w != u * n + v:
                    exc.append(n)
            if len(exc) > 50:
                continue
            return dict(Q=Q, table=tab, exceptions=exc)
    return None


def minimal_modulus(Q, table):
    """Smallest divisor Q' of Q such that the table is periodic mod Q'."""
    for d in sorted(x for x in range(1, Q + 1) if Q % x == 0):
        if all(table[r] == table[r % d] for r in range(Q)):
            return d, table[:d]
    return Q, table
