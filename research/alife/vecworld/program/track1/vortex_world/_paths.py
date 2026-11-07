"""Import paths: the vw library (read-only) and the ALife lab's labkit (for the numpy source world)."""
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
VW1 = "/home/user/evalwork/vecworld/vw1"
LAB = "/home/user/physim/research/alife"
SRC_SEL = os.path.join(LAB, "collective/contrib/20261027T0845-c53-fed-vortex-selection-claim/world.py")
RESULTS = os.path.join(HERE, "results")
for _p in (VW1, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
os.makedirs(RESULTS, exist_ok=True)
