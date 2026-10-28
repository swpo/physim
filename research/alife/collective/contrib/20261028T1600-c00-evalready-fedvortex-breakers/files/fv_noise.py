"""c53 fed vortices with dynamics noise (eval-readiness pilot wrapper).

WORLD_P keys besides the base world's:
  dyn_noise    sd per sqrt(time) unit; per step the kick has sd dyn_noise*sqrt(dt)
  noise_fields fields that get ADDITIVE noise (default ["om", "Y"])
  mult_fields  fields that get PROPORTIONAL noise, f *= (1 + kick) (default [])
  noise_seed   noise RNG seed (combined with the world seed)
The noise is applied to the state before every base step. FFT workers forced to 1 (CPU rule).
"""
import importlib.util, json, os
import numpy as np
from labkit import ops

ops.WORKERS = 1
BASE = "/home/user/physim/research/alife/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py"
OV = json.loads(os.environ.get("WORLD_P", "{}"))
NOISE = float(OV.pop("dyn_noise", 0.0))
NFIELDS = OV.pop("noise_fields", ["om", "Y"])
MULT = OV.pop("mult_fields", [])
NSEED = int(OV.pop("noise_seed", 12345))
_saved = os.environ.get("WORLD_P")
os.environ["WORLD_P"] = json.dumps(OV)          # base world sees only its own keys
_spec = importlib.util.spec_from_file_location("fv_base", BASE)
B = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(B)
if _saved is None:
    del os.environ["WORLD_P"]
else:
    os.environ["WORLD_P"] = _saved

META = dict(B.META)
META["name"] = "fed-vortices-noise"
META["parent"] = "collective/contrib/20261027T0712-c53-fed-vortex-claim"
META["mutation"] = f"dynamics noise sd {NOISE} per sqrt(t): additive on {NFIELDS}, proportional on {MULT}"
P = B.P
fields = B.fields


def init(seed, size):
    s = B.init(seed, size)
    s["_nrng"] = np.random.default_rng([NSEED, seed])
    return s


def step(s):
    if NOISE > 0:
        a = NOISE * np.sqrt(s["par"]["dt"])
        for f in NFIELDS:
            s[f] = s[f] + a * s["_nrng"].standard_normal(s[f].shape)
        for f in MULT:
            s[f] = s[f] * (1 + a * s["_nrng"].standard_normal(s[f].shape))
    return B.step(s)
