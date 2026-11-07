"""Import paths: the vw library (read-only) and the numpy source world (read-only)."""
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
VW1 = "/home/user/evalwork/vecworld/vw1"
SRC = "/home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py"
RESULTS = os.path.join(HERE, "results")
for _p in (VW1, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
os.makedirs(RESULTS, exist_ok=True)


def load_source():
    """A fresh copy of the numpy source module (its P dict is module state, so each caller gets its own)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("pm_source", SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
