"""Review wrapper: c06's pcell cost-balance world.py unchanged, with ytrait=1 muy=0.02 sy=0.05 cy=0.03 (the finding's stationary arm)."""
import importlib.util, os
_here = os.path.dirname(os.path.abspath(__file__)); _root = _here
while not os.path.isdir(os.path.join(_root, "collective")):
    _root = os.path.dirname(_root)
_spec = importlib.util.spec_from_file_location("pcell_cb", os.path.join(_root, "collective/contrib/20261025T0755-c06-pcell-cost-balance/world.py"))
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)
_m.P.update(ytrait=1, muy=0.02, sy=0.05, cy=0.03)
globals().update({k: getattr(_m, k) for k in dir(_m) if not k.startswith("__")})
