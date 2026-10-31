"""Reviewer's independent noise wrapper for c53 fed vortices (not derived from fv_noise.py).
WORLD_P keys consumed here: sd (per sqrt(t)), form ('B' = additive om + proportional Y), nseed.
Noise is added AFTER each base step (PhySim adds it after the reaction update); FFT workers forced to 1."""
import importlib.util, json, os
import numpy as np
from labkit import ops
ops.WORKERS = 1
BASE = "/home/user/physim/research/alife/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py"
_raw = os.environ.get("WORLD_P", "{}")
_kw = json.loads(_raw)
SD = float(_kw.pop("sd", 0.0)); FORM = _kw.pop("form", "B"); NSEED = int(_kw.pop("nseed", 4242))
os.environ["WORLD_P"] = json.dumps(_kw)
_sp = importlib.util.spec_from_file_location("fvchk_base", BASE)
_B = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_B)
os.environ["WORLD_P"] = _raw
META = dict(_B.META); META["name"] = "fed-vortices-reviewcheck"
META["mutation"] = f"review check: noise sd {SD} form {FORM} after each step"
P = _B.P
fields = _B.fields

def init(seed, size):
    s = _B.init(seed, size)
    s["_rng"] = np.random.default_rng([NSEED, int(seed)])
    return s

def step(s):
    s = _B.step(s)
    if SD > 0:
        a = SD * np.sqrt(s["par"]["dt"]); g = s["_rng"]
        s["om"] = s["om"] + a * g.standard_normal(s["om"].shape)
        if FORM == "B":
            s["Y"] = s["Y"] * (1.0 + a * g.standard_normal(s["Y"].shape))
    return s
