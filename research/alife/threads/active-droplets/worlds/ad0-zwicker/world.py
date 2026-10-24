"""Active emulsion, Zwicker-style (Zwicker, Seyboldt, Juelicher 2017), 2D.

phi in [-1, 1] is droplet material (+1 inside). Cahn-Hilliard transport plus a
non-conserved chemical source that turns precursor into droplet material in the
dilute phase and degrades it inside droplets:

    d phi/dt = M lap(mu) + s(phi),   mu = phi^3 - phi - kappa lap(phi)
    s = kp*(1 - phi)/2 - kd*(1 + phi)/2          (production outside, decay inside)

Semi-implicit spectral (linear stabilization A); 4th-order term implicit.
Initial condition: noisy uniform background (no planted droplets) unless P['seeds']>0.
"""
import numpy as np
from labkit import ops

META = {
    "name": "ad0-zwicker",
    "family": "phase-field",
    "parent": None,
    "mutation": "reference: Cahn-Hilliard + first-order production/degradation (active emulsion)",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 0.2,
    "channels": ["phi (droplet material)"],
    "matter": [0],
    "threshold": 0.0,
}

P = dict(M=1.0, kappa=1.0, kp=0.004, kd=0.004, dt=0.2, A=2.0, phi0=-0.6, noise=0.05, seeds=0, r0=6.0)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    for _ in range(P["seeds"]):
        m = ops.disk(H, W, rng.integers(0, H), rng.integers(0, W), P["r0"])
        phi[m] = 0.9
    ky, kx = ops.wavenumbers(H, W)
    k2 = kx ** 2 + ky ** 2
    dt, M = P["dt"], P["M"]
    return {"phi": phi, "k2": k2, "den": 1 + dt * M * k2 * (P["A"] + P["kappa"] * k2), "shape": (H, W)}


def step(s):
    phi, k2, dt, M = s["phi"], s["k2"], P["dt"], P["M"]
    src = P["kp"] * (1 - phi) / 2 - P["kd"] * (1 + phi) / 2
    nl = ops.rfft2(phi ** 3 - phi - P["A"] * phi)
    ph = ops.rfft2(phi)
    ph = (ph - dt * M * k2 * nl + dt * ops.rfft2(src)) / s["den"]
    s["phi"] = ops.irfft2(ph, s["shape"])
    return s


def fields(s):
    return s["phi"][None]


def damage(s, mask):
    s["phi"][mask] = -1.0
    return s
