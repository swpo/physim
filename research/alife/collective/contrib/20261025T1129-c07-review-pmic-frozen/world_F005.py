"""c06's pmic world (20261025T1013-c06-pmic-frozen/world.py) loaded unchanged with F=0.005, for a labkit re-run."""
import importlib.util
import os

_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "20261025T1013-c06-pmic-frozen", "world.py")
_spec = importlib.util.spec_from_file_location("pmic_c06", _src)
_w = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_w)
_w.P.update(F=0.005)
META = dict(_w.META, name="pmic-F0.005")
P = _w.P
init, step, fields = _w.init, _w.step, _w.fields
for _n in ("particles", "stats", "damage", "matter"):
    if hasattr(_w, _n):
        globals()[_n] = getattr(_w, _n)
