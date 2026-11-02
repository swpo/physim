"""Observe-only channels of the fed-vortex lab world: fn(module, state) -> array (no state change, no RNG)."""
import numpy as np


def eat(module, s):
    """Local eating rate, e Y s omega^2 capped at Y/dt, from the current fields (the world's own formula)."""
    q = s["par"]
    w2 = s["om"] ** 2
    sat = w2 / (w2 + q["wi"] ** 2)
    return np.minimum(q["e"] * s["Y"] * sat * w2, s["Y"] / q["dt"])


def speed(module, s):
    """Flow speed |u| (world units per time) from the streamfunction of the current vorticity."""
    uy, ux = module._vel(s)
    return s["par"]["adv"] * np.hypot(uy, ux)
