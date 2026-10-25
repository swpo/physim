"""Review wrapper: c06's pcell world (unchanged) with nkinds=2, y2=0.7, as in the finding's y2 arm."""
import importlib.util, os
_spec = importlib.util.spec_from_file_location("pcell_claimed", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../20261025T0648-c06-pcell-yield-selection/world.py"))
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)
_m.P.update(nkinds=2, y2=0.7)
globals().update({k: getattr(_m, k) for k in dir(_m) if not k.startswith("__")})
META = dict(_m.META)  # same name as the claimed world
