"""c34 nematic-marangoni rods with dynamics noise (eval-readiness pilot wrapper, test 1).

WORLD_P keys besides the base world's (popped before the base module is loaded, so the base
world sees only its own keys):
  dyn_noise    sd a per sqrt(time); each step adds a*sqrt(dt)*xi to the listed fields
  noise_fields additive white noise (default: all five state fields phi, q1, q2, s, c)
  mult_fields  proportional noise: f <- f * (1 + a sqrt(dt) xi)
  cons_fields  conserved noise: f <- f + a sqrt(dt) * div(eta) / sd(div eta) (eta a white vector
               field, spectral divergence, dealiased; normalised so the per-pixel sd equals the
               additive form's; it adds no mass at k = 0)
  noise_seed   noise stream seed (stream = [noise_seed, labkit seed])
"""
import importlib.util, json, os
import numpy as np
from numpy.fft import fft2, ifft2

BASE = "/home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py"
_OV = json.loads(os.environ.get("WORLD_P", "{}"))
NOISE = float(_OV.pop("dyn_noise", 0.0))
NFIELDS = _OV.pop("noise_fields", ["phi", "q1", "q2", "s", "c"])
MULT = _OV.pop("mult_fields", [])
CONS = _OV.pop("cons_fields", [])
NSEED = int(_OV.pop("noise_seed", 12345))
_saved = os.environ.get("WORLD_P")
os.environ["WORLD_P"] = json.dumps(_OV)
_spec = importlib.util.spec_from_file_location("mg_base", BASE)
B = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(B)
if _saved is None:
    os.environ.pop("WORLD_P", None)
else:
    os.environ["WORLD_P"] = _saved

META = dict(B.META)
META["name"] = "active-nematic-marangoni-noise"
META["parent"] = "collective/contrib/20261026T0505-c34-nematic-marangoni"
META["mutation"] = (f"dynamics noise sd {NOISE} per sqrt(t): additive on {NFIELDS}, proportional on {MULT}, "
                    f"conserved (div of white flux) on {CONS}")
P = B.P
fields, stats = B.fields, B.stats


def init(seed, size):
    s = B.init(seed, size)
    s["_nrng"] = np.random.default_rng([NSEED, seed])
    return s


def _cons_noise(s, rng):
    kx, ky, da = s["kx"], s["ky"], s["da"]
    ex = fft2(rng.standard_normal(kx.shape))
    ey = fft2(rng.standard_normal(kx.shape))
    xi = ifft2(1j * (kx * ex + ky * ey) * da).real
    if "_csd" not in s:  # sd of div(eta) for unit white eta: sqrt(mean of k^2 over kept modes)
        s["_csd"] = float(np.sqrt((s["k2"] * da).sum() / da.size))
    return xi / s["_csd"]


def add_noise(s, a, rng, nfields=None, mult=None, cons=None):
    nfields = NFIELDS if nfields is None else nfields
    mult = MULT if mult is None else mult
    cons = CONS if cons is None else cons
    if a <= 0:
        return s
    sa = a * np.sqrt(B.P["dt"])
    for f in nfields:
        s[f] = s[f] + sa * rng.standard_normal(s[f].shape)
    for f in mult:
        s[f] = s[f] * (1 + sa * rng.standard_normal(s[f].shape))
    for f in cons:
        s[f] = s[f] + sa * _cons_noise(s, rng)
    return s


def step(s):
    s = add_noise(s, NOISE, s["_nrng"])
    return B.step(s)
