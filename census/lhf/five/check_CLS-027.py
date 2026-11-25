#!/usr/bin/env python3
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from five_common import *
t0 = time.time()
check_system('par_5_3_s27', 3); check_dZ_conjugacy(3); check_units_invariant(3, 3); check_first_odd_step_leaves_5Z(3)
finish(t0)
