import subprocess, sys, os
sys.exit(subprocess.call([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_equiv.py"), "b"]))
