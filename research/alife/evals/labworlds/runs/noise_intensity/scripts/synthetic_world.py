"""Synthetic lab world for noise checks: two zero fields ``a`` and ``c`` and no dynamics."""
import numpy as np

META = {"name": "synthetic-noise", "size": (128, 128), "dt": 1.0}
P = {"dt": 1.0}


def init(seed, size):
    return {"a": np.zeros(size), "c": np.zeros(size), "p": np.ones(size)}


def step(s):
    return s
