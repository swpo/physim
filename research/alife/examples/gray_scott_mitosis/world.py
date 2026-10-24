"""Gray-Scott "mitosis" spots (Pearson 1993 regime; Karl Sims parameters, 5-point Laplacian).

Diffusive baseline and positive control for split detection: spots grow, divide and fill
space. Expect many persistent splits and generations, but no boundary, no heredity.
"""
import numpy as np

from labkit import ops

META = {
    "name": "gray-scott-mitosis-ref",
    "family": "reaction-diffusion",
    "parent": None,
    "mutation": "reference",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 1.0,
    "channels": ["u (substrate)", "v (autocatalyst)"],
    "matter": [1],
}

DU, DV, F, K = 0.2, 0.1, 0.0367, 0.0649


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    u, v = np.ones((H, W)), np.zeros((H, W))
    for _ in range(4):
        y, x = rng.integers(0, H), rng.integers(0, W)
        m = ops.disk(H, W, y, x, 4)
        u[m], v[m] = 0.5, 0.25
    v += 0.01 * rng.random((H, W))
    return {"u": u, "v": v}


def step(s):
    u, v = s["u"], s["v"]
    uvv = u * v * v
    s["u"] = u + DU * ops.laplacian(u) - uvv + F * (1 - u)
    s["v"] = v + DV * ops.laplacian(v) + uvv - (F + K) * v
    return s


def fields(s):
    return np.stack([s["u"], s["v"]])


def damage(s, mask):
    s["v"][mask] = 0
    s["u"][mask] = 1
    return s
