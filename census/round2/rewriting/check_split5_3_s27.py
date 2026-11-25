"""split5_3_s27: partial theorem (descent-tree exceptional set) + up-run witness.
Exit 0 iff the recorded certificate in partial_certs.json is reproduced exactly."""
from _partial_check import run

run("split5_3_s27", lambda K: 4**K - 3, range(1, 33), lambda K: 3*(K - 1))
