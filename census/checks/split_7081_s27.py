"""Check for split_7081_s27: FATE by exact simulation (tier 0); GLOBAL via the descent
lemma (every odd image is divisible by 4) plus exhaustive cycle list on [1,7081]."""
import sys
from _split_common import check_fate, check_descent
check_fate("split_7081_s27", 101, 334)
check_descent("split_7081_s27", 7081, 3, 1)
print("PASS")
sys.exit(0)
