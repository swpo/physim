"""c06's pcell yield-selection world with the claimed arm as defaults (nkinds=2, y2=0.7) for a labkit re-run."""
import importlib.util
import os

_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "20261025T0648-c06-pcell-yield-selection", "world.py")
_spec = importlib.util.spec_from_file_location("pcell_yield_c06", _src)
_w = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_w)
_w.P.update(nkinds=2, y2=0.7)
META = dict(_w.META, name="pcell-y07")
P = _w.P
init, step, fields = _w.init, _w.step, _w.fields
particles, stats, damage = _w.particles, _w.stats, _w.damage
