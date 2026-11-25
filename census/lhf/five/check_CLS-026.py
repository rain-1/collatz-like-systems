#!/usr/bin/env python3
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from five_common import *
t0 = time.time()
check_system('par_5_3_s27', 3); check_dZ_conjugacy(3); check_orbit_of_7_class()
finish(t0)
