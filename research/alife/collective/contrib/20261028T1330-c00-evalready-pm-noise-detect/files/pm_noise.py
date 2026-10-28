"""phase_membrane with additive dynamics noise (eval-readiness pilot wrapper).

WORLD_P keys besides the base world's: dyn_noise (sd per sqrt(time) added to each listed
field before every step), noise_fields (default all four state fields), noise_seed.
"""
import importlib.util, json, os
import numpy as np

_spec = importlib.util.spec_from_file_location(
    "pm_base", "/home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py")
B = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(B)
OV = json.loads(os.environ.get("WORLD_P", "{}"))
NOISE = float(OV.pop("dyn_noise", 0.0))
NFIELDS = OV.pop("noise_fields", ["S", "K", "L", "phi"])
NSEED = int(OV.pop("noise_seed", 12345))
MULT = OV.pop("mult_fields", [])
B.P.update(OV)
META = dict(B.META)
META["name"] = "phase-membrane-noise"
META["parent"] = "threads/autopoiesis/worlds/phase_membrane"
META["mutation"] = f"dynamics noise sd {NOISE} per sqrt(t): additive on {NFIELDS}, multiplicative (sd x value) on {MULT}"
P = B.P
fields, matter, damage, stats = B.fields, B.matter, B.damage, B.stats


def init(seed, size):
    s = B.init(seed, size)
    s["_nrng"] = np.random.default_rng([NSEED, seed])
    return s


def step(s):
    if NOISE > 0:
        a = NOISE * np.sqrt(B.P["dt"])
        for f in NFIELDS:
            s[f] = s[f] + a * s["_nrng"].standard_normal(s[f].shape)
        for f in MULT:
            s[f] = s[f] * (1 + a * s["_nrng"].standard_normal(s[f].shape))
    return B.step(s)
