"""Negative control: smoothed noise that is re-drawn every step. Nothing here is alive.

Expect many short-lived components, no persistent individuals, and spurious splits/merges
that do not form persistent lineages.
"""
import numpy as np

from labkit import ops

META = {
    "name": "noise-control",
    "family": "control",
    "parent": None,
    "mutation": "reference",
    "size": (128, 128),
    "steps_per_frame": 1,
    "dt": 1.0,
    "channels": ["noise"],
}


def init(seed, size):
    return {"rng": np.random.default_rng(seed), "K": ops.gauss_kernel(*size, 3.0), "x": np.zeros(size)}


def step(s):
    s["x"] = 0.7 * s["x"] + 0.3 * ops.fft_conv(s["rng"].standard_normal(s["x"].shape), s["K"])
    return s


def fields(s):
    return s["x"][None]
