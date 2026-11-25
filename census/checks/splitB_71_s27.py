"""Check for splitB_71_s27: FATE by exact simulation (tier 0); GLOBAL via the descent
lemma (every odd image is divisible by 4) plus exhaustive cycle list on [1,71]."""
import sys
from _split_common import check_fate, check_descent
check_fate("splitB_71_s27", 2, 20)
check_descent("splitB_71_s27", 71, 1, 3)
print("PASS")
sys.exit(0)
