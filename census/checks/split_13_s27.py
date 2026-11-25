"""Check for split_13_s27: FATE by exact simulation (tier 0); GLOBAL via the descent
lemma (every odd image is divisible by 4) plus exhaustive cycle list on [1,13]."""
import sys
from _split_common import check_fate, check_descent
check_fate("split_13_s27", 2, 6)
check_descent("split_13_s27", 13, 3, 1)
print("PASS")
sys.exit(0)
