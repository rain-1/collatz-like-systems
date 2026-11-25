#!/usr/bin/env python3
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from five_common import *
t0 = time.time()
check_system('par_5_7_s27', 7); check_dZ_conjugacy(7); check_first_odd_step_leaves_5Z(7); check_units_invariant(7, 5)
finish(t0)
