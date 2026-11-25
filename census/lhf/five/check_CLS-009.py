#!/usr/bin/env python3
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from five_common import *
t0 = time.time()
check_system('par_10_2_s7', 2, mult=10); check_orbit_of_7_class()
finish(t0)
