"""Heritable catalysts in fuel-fed dividing droplets (fork of ad1-fuel).

Droplet material phi (Cahn-Hilliard, slow mobility), fuel u (diffuses, fed from a bath),
and two catalyst species a, b that live only inside droplets (they decay in the dilute
phase), replicate there, and cross-inhibit (beta > 1) so each droplet becomes pure a or
pure b. Droplet material is made from fuel only by catalyst:

    prod     = u c^2 (ka a + kb b),           c = (1 + phi)/2
    dphi/dt  = M lap(phi^3 - phi - kappa lap phi) + prod - kd c
    du/dt    = Du lap u + F (1 - u) - prod
    da/dt    = Dc lap a + r c a (1 - a - beta b) - g (1 - c) a - mu a + mu b
    db/dt    = Dc lap b + r c b (1 - b - beta a) - g (1 - c) b - mu b + mu a

Kinds: a-droplets (ka) and b-droplets (kb). Division (core starvation -> ring -> breakup)
splits the catalyst with the material, so kinds should breed true. mu: mutation (a <-> b
conversion), so variation can also arise during the run.
"""
import numpy as np
from labkit import ops

META = {
    "name": "ad2-catalysts",
    "family": "phase-field",
    "parent": "ad1-fuel",
    "mutation": "production requires one of two cross-inhibiting, droplet-confined catalysts that replicate inside droplets",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.5,
    "channels": ["phi (droplet material)", "u (fuel)", "a (catalyst A)", "b (catalyst B)"],
    "matter": [0],
    "threshold": 0.0,
}

P = dict(M=0.03, kappa=1.0, ka=0.1, kb=0.1, kd=0.02, F=0.004, Du=2.0, Dc=0.05, r=0.05, beta=1.5,
         g=0.05, mu=0.0, dt=0.5, A=2.0, phi0=-0.95, noise=0.01, seeds=4, r0=6.0)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    a, b = np.zeros((H, W)), np.zeros((H, W))
    for i in range(P["seeds"]):
        m = ops.disk(H, W, rng.integers(0, H), rng.integers(0, W), P["r0"])
        phi[m] = 0.9
        (a if i % 2 == 0 else b)[m] = 0.9
    ky, kx = ops.wavenumbers(H, W)
    k2 = kx ** 2 + ky ** 2
    dt, M = P["dt"], P["M"]
    return {"phi": phi, "u": np.ones((H, W)), "a": a, "b": b, "k2": k2, "shape": (H, W),
            "den": 1 + dt * M * k2 * (P["A"] + P["kappa"] * k2), "denu": 1 + dt * P["Du"] * k2,
            "denc": 1 + dt * P["Dc"] * k2}


def step(s):
    phi, u, a, b, k2, dt, M = s["phi"], s["u"], s["a"], s["b"], s["k2"], P["dt"], P["M"]
    c = np.clip((1 + phi) / 2, 0, 1)
    prod = u * c ** 2 * (P["ka"] * a + P["kb"] * b)
    src = prod - P["kd"] * c
    ph = (ops.rfft2(phi) - dt * M * k2 * ops.rfft2(phi ** 3 - phi - P["A"] * phi) + dt * ops.rfft2(src)) / s["den"]
    s["phi"] = ops.irfft2(ph, s["shape"])
    s["u"] = ops.irfft2((ops.rfft2(u) + dt * ops.rfft2(P["F"] * (1 - u) - prod)) / s["denu"], s["shape"])
    r, beta, g, mu = P["r"], P["beta"], P["g"], P["mu"]
    ra = r * c * a * (1 - a - beta * b) - g * (1 - c) * a - mu * a + mu * b
    rb = r * c * b * (1 - b - beta * a) - g * (1 - c) * b - mu * b + mu * a
    s["a"] = np.clip(ops.irfft2((ops.rfft2(a) + dt * ops.rfft2(ra)) / s["denc"], s["shape"]), 0, None)
    s["b"] = np.clip(ops.irfft2((ops.rfft2(b) + dt * ops.rfft2(rb)) / s["denc"], s["shape"]), 0, None)
    return s


def fields(s):
    return np.stack([s["phi"], s["u"], s["a"], s["b"]])


def damage(s, mask):
    s["phi"][mask] = -1.0
    s["a"][mask] = 0
    s["b"][mask] = 0
    return s
