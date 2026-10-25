"""rdtrail_slow: rdtrail with the inhibitor 2.5x slower (kh 0.02, beta 0.4: same static h = 20 u), gh 0.01.

rdtrail: the reaction-diffusion twin of kstrail (no advection, no taxis).

kstrail's body is held by taxis up a fast attractant `a` and pushed by taxis down a slow
self-secreted repellent `h`. Here both taxis terms are removed. `a` and `h` keep kstrail's
linear equations exactly (Da, ka, Dh, kh, beta), and act on the body only through local
kinetics: they raise the threshold of a bistable (Allen-Cahn / Nagumo) production of u.

  du/dt = Du lap u + r u (1 - u) (u - th0 - ga a - gh h)
  da/dt = Da lap a + u - ka a          (fast, long-range inhibitor: localizes spots)
  dh/dt = Dh lap h + beta u - kh h     (slow, short-range inhibitor: the trail)

With gh = 0 this is a spot-forming activator-inhibitor; a slow third inhibitor gives the
drift bifurcation of travelling spots (Krischer & Mikhailov 1994; Schenk et al. 1997).
Du = kstrail's Dr. Scan: gh (analogue of chi_h) and kh at fixed beta/kh (inhibitor time
scale tau_h = 1/kh at fixed static strength).
"""
import json
import os

import numpy as np

from labkit import ops

META = {
    "name": "rdtrail_slow",
    "family": "reaction-diffusion",
    "parent": "kstrail",
    "mutation": "kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)",
    "size": (192, 192),
    "steps_per_frame": 60,
    "dt": 0.05,
    "channels": ["u", "a", "h"],
    "matter": [0],
    "smooth": 1.0,
}

P = {
    "Du": 1.2, "Da": 4.0, "ka": 0.1, "Dh": 0.2, "kh": 0.02, "beta": 0.4,
    "r": 1.0, "th0": 0.0, "ga": 0.1, "gh": 0.01, "rho0": 0.05, "noise": 0.02, "dt": 0.05,
    "plant": 7, "nplant": 6,
}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))  # screening override


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    u = np.clip(P["rho0"] + P["noise"] * rng.standard_normal((H, W)), 0, 1)
    u = ops.fft_conv(u, ops.gauss_kernel(H, W, 1.0))
    if P.get("plant", 0) > 0:
        # Planted control IC: nplant disks of radius `plant` at seed-random positions plus noise.
        # This gives the twin the formed bodies that kstrail makes from noise (the twin's uniform
        # state decays, so it does not form spots from noise; see README).
        yy, xx = np.mgrid[:H, :W]
        u = np.clip(P["noise"] * rng.standard_normal((H, W)), 0, 1)
        for cy, cx in rng.uniform(0, [H, W], size=(int(P["nplant"]), 2)):
            dy = (yy - cy + H / 2) % H - H / 2
            dx = (xx - cx + W / 2) % W - W / 2
            u[dy ** 2 + dx ** 2 < P["plant"] ** 2] = 1.0
        L = ops.lap_symbol(H, W)
        dt = P["dt"]
        return {"u": u, "a": np.zeros((H, W)), "h": np.zeros((H, W)),
                "La": 1.0 / (1 - dt * (P["Da"] * L - P["ka"])), "Lh": 1.0 / (1 - dt * (P["Dh"] * L - P["kh"])),
                "shape": (H, W), "p": dict(P)}
    L = ops.lap_symbol(H, W)
    dt = P["dt"]
    return {"u": u, "a": u / P["ka"], "h": np.zeros((H, W)) + P["beta"] * u.mean() / P["kh"],
            "La": 1.0 / (1 - dt * (P["Da"] * L - P["ka"])), "Lh": 1.0 / (1 - dt * (P["Dh"] * L - P["kh"])),
            "shape": (H, W), "p": dict(P)}


def step(s):
    p, dt = s["p"], s["p"]["dt"]
    u, a, h = s["u"], s["a"], s["h"]
    th = p["th0"] + p["ga"] * a + p["gh"] * h
    u = u + dt * (p["Du"] * ops.laplacian(u) + p["r"] * u * (1 - u) * (u - th))
    u = np.clip(u, 0, 1)
    s["a"] = ops.irfft2(ops.rfft2(a + dt * u) * s["La"], s["shape"])
    s["h"] = ops.irfft2(ops.rfft2(h + dt * p["beta"] * u) * s["Lh"], s["shape"])
    s["u"] = u
    return s


def fields(s):
    return np.stack([s["u"], s["a"], s["h"]])


def damage(s, mask):
    s["u"][mask] = 0
    return s
