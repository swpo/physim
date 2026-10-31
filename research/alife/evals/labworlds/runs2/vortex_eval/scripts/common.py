"""Shared declaration of c53's fed vortices as a PhySim evaluation candidate (vortex_eval)."""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys

ENV = "/home/user/swpo/residency-environments/environments/physim"
if ENV not in sys.path:
    sys.path.insert(0, ENV)
LAB = "/home/user/physim/research/alife"
WORLD = f"{LAB}/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py"
OUT = "/home/user/evalwork/vortex_eval"

from physim import labworld as LW  # noqa: E402

INTENSITY = 0.003
ELL = 2.0


def world(intensity=INTENSITY, ell=ELL, overrides=None, gains=None, actuators=True, steps_per_tick=1,
          native_dt=0.02, derived=()):
    gains = gains or {"om": 0.01, "Y": 0.1}
    ports = {"om": LW.Port(gain=gains["om"]), "Y": LW.Port(gain=gains["Y"], clip=(0.0, None))}
    acts = (LW.Actuator("om", 1), LW.Actuator("om", -1), LW.Actuator("Y", 1), LW.Actuator("Y", -1)) if actuators else None
    return LW.LabWorld(path=WORLD, fields=("om", "Y"), steps_per_tick=steps_per_tick, native_dt=native_dt,
                       ports=ports, noise={"om": ("additive", intensity), "Y": ("proportional", intensity)},
                       noise_corr={"om": ell, "Y": ell} if ell else {},
                       noise_intensity=("om", "Y") if intensity else (),
                       overrides=overrides or {}, dx=1.0, sys_path=(LAB,), carry=("t",), actuators=acts,
                       derived=tuple(derived))


def one_worker(module):
    if hasattr(module, "ops") and hasattr(module.ops, "WORKERS"):
        module.ops.WORKERS = 1
