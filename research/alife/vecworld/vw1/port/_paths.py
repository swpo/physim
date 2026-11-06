"""Import paths for the port (read-only use of VW-0 code; no bytecode is written anywhere)."""
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
VW1 = os.path.dirname(HERE)
VEC = os.path.dirname(VW1)
L0_DIR = os.path.join(VEC, "level0")
SPEC_DIR = os.path.join(VEC, "spec")
INT_DIR = os.path.join(VEC, "integrate")
RESULTS = os.path.join(HERE, "results")
for _p in (VW1, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
for _p in (INT_DIR, SPEC_DIR, L0_DIR):       # appended: VW-0 modules never shadow the port's;
    # integrate/ first so that its analyze.py shadows level0/analyze.py (as in lenia_world.py)
    if _p not in sys.path:
        sys.path.append(_p)
os.makedirs(RESULTS, exist_ok=True)
