"""A lab world with LabWorld dynamics noise applied before every native step (for labkit packs).

The base world, noise declaration and noise seed come from the NOISY_SPEC environment variable (JSON, written by
nsweep.py behav). The noise is LabStepper.add_noise itself, from a generator seeded by (noise_seed, seed)."""
import json, os, sys
import numpy as np

SPEC = json.loads(os.environ["NOISY_SPEC"])
sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import labworld as LW  # noqa: E402

WORLD = LW.LabWorld(path=SPEC["path"], fields=tuple(SPEC["fields"]), steps_per_tick=1, native_dt=SPEC["native_dt"],
                    noise={f: tuple(v) for f, v in SPEC["noise"].items()}, noise_corr=SPEC["noise_corr"],
                    noise_intensity=tuple(SPEC["noise_intensity"]), overrides=SPEC["overrides"], dx=SPEC["dx"],
                    sys_path=tuple(SPEC["sys_path"]))
_ST = LW.LabStepper(WORLD, {})
B = _ST.module
if hasattr(B, "ops") and hasattr(B.ops, "WORKERS"):
    B.ops.WORKERS = 1
META = dict(B.META)
META["name"] = f"{B.META['name']}-noise"
P = getattr(B, "P", {})
for _name in ("fields", "matter", "damage", "stats", "particles"):
    if hasattr(B, _name):
        globals()[_name] = getattr(B, _name)


def init(seed, size):
    s = B.init(seed, size)
    s["_nrng"] = np.random.default_rng([int(SPEC["noise_seed"]), int(seed)])
    return s


def step(s):
    s = _ST.add_noise(s, s["_nrng"], WORLD.native_dt)
    return B.step(s)
