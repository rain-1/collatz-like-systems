#!/usr/bin/env python3
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from five_common import *
t0 = time.time()
check_system('par_5_11_s27', 11); check_rational_conjugacy(11, 27); check_units_invariant(11, 11)
finish(t0)
