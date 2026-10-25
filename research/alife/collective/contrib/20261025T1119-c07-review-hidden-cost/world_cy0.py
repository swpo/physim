"""c06's pcell-multilevel world (20261025T0820-c06-pcell-multilevel-claim/world.py) loaded unchanged with cy=0 (no explicit replication cost of yield), for a labkit re-run."""
import importlib.util
import os

_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "20261025T0820-c06-pcell-multilevel-claim", "world.py")
_spec = importlib.util.spec_from_file_location("pcell_ml_c06", _src)
_w = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_w)
_w.P.update(cy=0.0)
META = dict(_w.META, name="pcell-multilevel-cy0")
P = _w.P
init, step, fields = _w.init, _w.step, _w.fields
particles, stats, damage = _w.particles, _w.stats, _w.damage
