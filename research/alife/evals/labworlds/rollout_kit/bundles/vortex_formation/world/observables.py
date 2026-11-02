"""Observe-only channels of this lab bundle's world, ``fn(module, state)``.

Copied verbatim from scripts/physim/labworlds/gc_vortex/gcv.py::eat.
"""
import numpy as np


def eat(module, s):
    """Local eating rate, e Y s omega^2 capped at Y/dt (the world's own formula; no state change, no RNG)."""
    q = s["par"]
    w2 = s["om"] ** 2
    sat = w2 / (w2 + q["wi"] ** 2)
    return np.minimum(q["e"] * s["Y"] * sat * w2, s["Y"] / q["dt"])
