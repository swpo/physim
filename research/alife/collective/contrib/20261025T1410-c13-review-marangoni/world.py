"""Fuel-fed dividing Cahn-Hilliard droplets (ad1-fuel) in a self-generated Brinkman flow (c01).

ad1-fuel (threads/active-droplets/worlds/ad1-fuel) plus an incompressible flow v made by the
droplets' own interfacial stress, with an interfacial tension that depends on the local fuel:

    f = -(1 + alpha (u - ub)) phi grad(mu_s),   mu_s = phi^3 - phi - kappa lap phi
    (gam - eta lap) v = f - grad p,   div v = 0          (Brinkman, solved spectrally)
    d phi/dt += -div((phi+1) v),   d u/dt += -div(u v)   (first-order upwind, conservative; div v = 0)

With alpha = 0 the force is the passive Korteweg stress (it only speeds coarsening); alpha != 0
makes the stress non-gradient where the fuel differs across a droplet, which is the
Marangoni-like drive (fuel is depleted on the droplet's own wake). ub = mean fuel.
WORLD_P (JSON) overrides P.
"""
import json
import os

import numpy as np

from labkit import ops

META = {
    "name": "marangoni-droplets",
    "family": "phase-field",
    "parent": "threads/active-droplets/worlds/ad1-fuel",
    "mutation": "self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.5,
    "channels": ["phi (droplet material)", "u (fuel)", "|v| (flow speed)"],
    "matter": [0],
    "threshold": 0.0,
}

P = dict(M=0.03, kappa=1.0, k=0.1, kd=0.02, F=0.004, Du=2.0, dt=0.5, A=2.0, phi0=-0.95, noise=0.01,
         soup=0, seeds=2, r0=6.0, u0=1.0, order=2,
         alpha=0.0, gam=1.0, eta=1.0, ampf=1.0, vmax=0.5)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    for _ in range(int(P["seeds"])):
        m = ops.disk(H, W, rng.integers(0, H), rng.integers(0, W), P["r0"])
        phi[m] = 0.9
    u = P["u0"] * np.ones((H, W))
    for _ in range(int(P["soup"])):  # random blobs of random size/amplitude: unstructured start
        m = ops.disk(H, W, rng.integers(0, H), rng.integers(0, W), rng.uniform(1.5, 6))
        phi[m] = rng.uniform(-0.6, 0.9)
    ky, kx = ops.wavenumbers(H, W)
    k2 = kx ** 2 + ky ** 2
    dt, M = P["dt"], P["M"]
    return {"phi": phi, "u": u, "k2": k2, "kx": kx, "ky": ky, "shape": (H, W), "v": np.zeros((2, H, W)),
            "den": 1 + dt * M * k2 * (P["A"] + P["kappa"] * k2), "denu": 1 + dt * P["Du"] * k2}


def flow(s, phi, u):
    kx, ky, k2, sh = s["kx"], s["ky"], s["k2"], s["shape"]
    ph = ops.rfft2(phi)
    mu = phi ** 3 - phi + P["kappa"] * ops.irfft2(k2 * ph, sh)
    gy, gx = ops.grad(mu)
    w = -(1 + P["alpha"] * (u - u.mean())) * phi * P["ampf"]
    fx, fy = ops.rfft2(w * gx), ops.rfft2(w * gy)
    kk = np.where(k2 == 0, 1, k2)
    dot = (kx * fx + ky * fy) / kk                      # remove the longitudinal part (pressure)
    den = P["gam"] + P["eta"] * k2
    vx = ops.irfft2((fx - kx * dot) / den, sh)
    vy = ops.irfft2((fy - ky * dot) / den, sh)
    sp = np.sqrt(vx ** 2 + vy ** 2).max()
    s["vraw"] = max(s.get("vraw", 0.0), float(sp))
    if sp > P["vmax"]:                                   # CFL guard: report, do not hide
        vx, vy = vx * P["vmax"] / sp, vy * P["vmax"] / sp
    return vy, vx



def step(s):
    phi, u, k2, dt, M = s["phi"], s["u"], s["k2"], P["dt"], P["M"]
    vy, vx = flow(s, phi, u)
    s["v"] = np.stack([vy, vx])
    c = np.clip((1 + phi) / 2, 0, None)
    prod = P["k"] * u * c ** P["order"]
    src = prod - P["kd"] * c - ops.upwind_flux_div(phi + 1.0, vy, vx)
    ph = (ops.rfft2(phi) - dt * M * k2 * ops.rfft2(phi ** 3 - phi - P["A"] * phi) + dt * ops.rfft2(src)) / s["den"]
    s["phi"] = ops.irfft2(ph, s["shape"])
    uh = (ops.rfft2(u) + dt * ops.rfft2(P["F"] * (1 - u) - prod - ops.upwind_flux_div(u, vy, vx))) / s["denu"]
    s["u"] = ops.irfft2(uh, s["shape"])
    return s


def fields(s):
    return np.stack([s["phi"], s["u"], np.sqrt((s["v"] ** 2).sum(0))])


def damage(s, mask):
    s["phi"][mask] = -1.0
    return s
