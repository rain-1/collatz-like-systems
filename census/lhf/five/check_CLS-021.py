#!/usr/bin/env python3
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from five_common import *
t0 = time.time()
check_system('par_5_131_s27', 131); check_dZ_conjugacy(131); check_first_odd_step_leaves_5Z(131)
finish(t0)
