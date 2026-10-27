"""c00 wrapper: c52 digestion-ecology world (collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py),
unchanged physics; the one change is labkit.ops.WORKERS = 1 (one FFT thread per process, so the run uses one core).
The FFT thread count does not change the update rule."""
import importlib.util
from labkit import ops
ops.WORKERS = 1
_SRC = "/home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py"
_spec = importlib.util.spec_from_file_location("c52_digestion_world", _SRC)
_w = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_w)
META = dict(_w.META)
P = _w.P
init, step, fields, q_bath, damage = _w.init, _w.step, _w.fields, _w.q_bath, _w.damage
