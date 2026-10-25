"""Review wrapper: threads/autopoiesis/worlds/membrane_evo/world.py unchanged except p_death=0 (no imposed death disks)."""
import importlib.util, os
_here = os.path.dirname(os.path.abspath(__file__))
_root = _here
while not os.path.isdir(os.path.join(_root, "threads")):
    _root = os.path.dirname(_root)
_spec = importlib.util.spec_from_file_location("membrane_evo", os.path.join(_root, "threads/autopoiesis/worlds/membrane_evo/world.py"))
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)
_m.P.update(p_death=0.0)
globals().update({k: getattr(_m, k) for k in dir(_m) if not k.startswith("__")})
