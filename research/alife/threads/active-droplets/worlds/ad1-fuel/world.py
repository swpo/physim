"""Fuel-fed autocatalytic droplets: Cahn-Hilliard droplet material phi + diffusing fuel u.

    d phi/dt = M lap(mu) + k u c^n - kd c,    c = (1 + phi)/2   (local droplet fraction)
    d u/dt   = Du lap(u) + F (1 - u) - k u c^n           (n = P['order'], 2 = cooperative)
    mu = phi^3 - phi - kappa lap(phi)

Droplet material makes more of itself from fuel and decays at rate kd. Fuel enters from
the outside, so a droplet's interior is fuel-starved: production concentrates at the rim
and decay wins in the core. Intended mechanism for 2D division (no Rayleigh-Plateau in 2D).
"""
import numpy as np
from labkit import ops

META = {
    "name": "ad1-fuel",
    "family": "phase-field",
    "parent": "ad0-zwicker",
    "mutation": "production needs a diffusing, consumed fuel u and is autocatalytic in phi; decay first order",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.5,
    "channels": ["phi (droplet material)", "u (fuel)"],
    "matter": [0],
    "threshold": 0.0,
}

P = dict(M=0.03, kappa=1.0, k=0.1, kd=0.02, F=0.004, Du=2.0, dt=0.5, A=2.0, phi0=-0.95, noise=0.01,
         soup=0, seeds=2, r0=6.0, u0=1.0, order=2)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    for _ in range(P["seeds"]):
        m = ops.disk(H, W, rng.integers(0, H), rng.integers(0, W), P["r0"])
        phi[m] = 0.9
    u = P["u0"] * np.ones((H, W))
    for _ in range(P["soup"]):  # random blobs of random size/amplitude: unstructured start
        m = ops.disk(H, W, rng.integers(0, H), rng.integers(0, W), rng.uniform(1.5, 6))
        phi[m] = rng.uniform(-0.6, 0.9)
    ky, kx = ops.wavenumbers(H, W)
    k2 = kx ** 2 + ky ** 2
    dt, M = P["dt"], P["M"]
    return {"phi": phi, "u": u, "k2": k2, "shape": (H, W),
            "den": 1 + dt * M * k2 * (P["A"] + P["kappa"] * k2), "denu": 1 + dt * P["Du"] * k2}


def step(s):
    phi, u, k2, dt, M = s["phi"], s["u"], s["k2"], P["dt"], P["M"]
    c = np.clip((1 + phi) / 2, 0, None)
    prod = P["k"] * u * c ** P["order"]
    src = prod - P["kd"] * c
    ph = (ops.rfft2(phi) - dt * M * k2 * ops.rfft2(phi ** 3 - phi - P["A"] * phi) + dt * ops.rfft2(src)) / s["den"]
    s["phi"] = ops.irfft2(ph, s["shape"])
    uh = (ops.rfft2(u) + dt * ops.rfft2(P["F"] * (1 - u) - prod)) / s["denu"]
    s["u"] = ops.irfft2(uh, s["shape"])
    return s


def fields(s):
    return np.stack([s["phi"], s["u"]])


def damage(s, mask):
    s["phi"][mask] = -1.0
    return s
