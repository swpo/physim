"""Observe-only channels of this lab bundle's world, ``fn(module, state)``.

Copied verbatim from scripts/physim/labworlds/gc_rods/gcrods.py::speed.
"""
import numpy as np


def speed(module, state):
    """Observe-only flow speed |v| from the module's last solve (0 before the first step)."""
    return np.hypot(state["vx"], state["vy"])
