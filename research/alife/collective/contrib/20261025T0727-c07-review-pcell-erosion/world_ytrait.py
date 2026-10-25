"""c06's pcell cheater-erosion world with the claimed parameters as defaults (for a labkit re-run).

Loads collective/contrib/20261025T0711-c06-pcell-cheater-erosion/world.py unchanged and sets
ytrait=1, muy=0.02, sy=0.05, cy=0.5 (the 'real' arm of the finding).
"""
import importlib.util
import os

_here = os.path.dirname(os.path.abspath(__file__))
_src = os.path.join(_here, "..", "20261025T0711-c06-pcell-cheater-erosion", "world.py")
_spec = importlib.util.spec_from_file_location("pcell_c06", _src)
_w = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_w)
_w.P.update(ytrait=1, muy=0.02, sy=0.05, cy=0.5)

META = dict(_w.META, name="pcell-ytrait")
P = _w.P
init, step, fields = _w.init, _w.step, _w.fields
particles, stats, damage = _w.particles, _w.stats, _w.damage
