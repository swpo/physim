"""labkit wrapper (c38 review): lab 1's sporecell2 run as 'sporecell2-lysis': k_lys=2, half/half kinds
(seed_kind1=0.5), kind 1 the worse grazer (k_cat1=0.035), no mutation (mu=0). LYSIS=0 in the environment gives the
no-lysis ablation. The world file itself is threads/particle-life/worlds/sporecell2/world.py, unchanged."""
import os, sys, importlib.util
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "threads", "particle-life", "worlds", "sporecell2", "world.py")
_s = importlib.util.spec_from_file_location("sporecell2_world_c38", _p); _w = importlib.util.module_from_spec(_s)
sys.modules["sporecell2_world_c38"] = _w; _s.loader.exec_module(_w)
META = dict(_w.META); META["name"] = "sporecell2-lysis" if os.environ.get("LYSIS", "1") == "1" else "sporecell2-nolysis"
OVER = dict(k_lys=2.0 if os.environ.get("LYSIS", "1") == "1" else 0.0, seed_kind1=0.5, k_cat1=0.035, mu=0.0)
def init(seed, size): return _w.init(seed, size, **OVER)
step = _w.step; fields = _w.fields
particles = getattr(_w, "particles", None)
if particles is None: del particles
