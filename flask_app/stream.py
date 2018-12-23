import os
import signal
import subprocess
import sys

p=os.system('ffserver')
sys.exit(p)
#os.kill(p.pid, signal.SIGINT)
