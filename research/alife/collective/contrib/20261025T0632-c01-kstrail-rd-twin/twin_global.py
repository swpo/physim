"""Laplacian-only twins of kstrail (threads/chemotaxis-motility/worlds/kstrail).

kstrail moves body matter rho by taxis: -div(rho(1-rho)(chi_a grad a - chi_h grad h)).
The twins keep every field, diffusivity, decay rate, secretion and the volume-filling
factor, and replace the taxis flux by a local, mass-conserving reaction:

  drho/dt = Dr lap rho + taxis_a + rho(1-rho) (g - <g>_w)
  g = c_a a  * (mode == "full")  -  c_h h
  <g>_w = int rho(1-rho) g / int rho(1-rho)       (makes int rho exactly conserved)

mode "h"    : only the repellent taxis is replaced (attractant taxis chi_a kept): the
              question's twin, "activator + slow inhibitor" for the propulsion part.
mode "local": as "full" but with the fixed reference g0 of the uniform state instead of the
              weighted mean (local kinetics; rho is then not conserved).
Lm > 0 replaces the global weighted mean by a screened-Poisson average of range Lm (what a
fast-diffusing inhibitor gives), plus one uniform correction so that int rho stays exact.
eps > 0 adds a weak linear turnover eps (rho0 - rho) (Ohta-Kawasaki-type), which in
pure reaction-diffusion arrests coarsening at a finite body size.
mode "full" : both taxis terms replaced: a pure reaction-diffusion world (plus one
              global zero mode that conserves mass, as kstrail does).

Matching: on a mode of wavenumber k, taxis gives chi k^2 where the reaction gives c.
At the body scale (diameter ~12 px, k ~ 0.5) c ~ chi/4; c = f chi is swept.
"""
import json
import os

import numpy as np

from labkit import ops

META = {
    "name": "kstrail-rd-twin-global",
    "family": "chemotaxis",
    "parent": "kstrail",
    "mutation": "taxis flux replaced by a local mass-conserving reaction (Laplacian-only twin)",
    "size": (192, 192),
    "steps_per_frame": 60,
    "dt": 0.05,
    "channels": ["rho", "a", "h"],
    "matter": [0],
    "smooth": 1.0,
}

P = {
    "Dr": 1.2, "Da": 4.0, "ka": 0.1, "Dh": 0.2, "kh": 0.05, "beta": 1.0,
    "chi_a": 24.0, "chi_h": 4.8, "rho0": 0.05, "noise": 0.02, "dt": 0.05,
    "mode": "full", "f": 0.25, "eps": 0.0, "Lm": 0.0, "fa": None, "fh": None,
}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def _faces(u, ax):
    up, um = np.roll(u, -1, ax), np.roll(u, 1, ax)
    d1, d2 = u - um, up - u
    slope = np.where(d1 * d2 > 0, 2 * d1 * d2 / (d1 + d2 + 1e-300), 0.0)
    return u + 0.5 * slope, np.roll(u - 0.5 * slope, -1, ax)


def vf_flux_div(rho, vy, vx):
    """kstrail's conservative MUSCL volume-filling flux, unchanged."""
    out = np.zeros_like(rho)
    for v, ax in ((vy, -2), (vx, -1)):
        vf = 0.5 * (v + np.roll(v, -1, ax))
        L, R = _faces(rho, ax)
        flux = np.where(vf > 0, vf * L * (1 - R), vf * R * (1 - L))
        out += flux - np.roll(flux, 1, ax)
    return out


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    rho = np.clip(P["rho0"] + P["noise"] * rng.standard_normal((H, W)), 0, 1)
    rho = ops.fft_conv(rho, ops.gauss_kernel(H, W, 1.0))
    L = ops.lap_symbol(H, W)
    dt = P["dt"]
    p = dict(P)
    p["c_a"] = p["chi_a"] * (p["fa"] if p["fa"] is not None else p["f"])
    p["c_h"] = p["chi_h"] * (p["fh"] if p["fh"] is not None else p["f"])
    p["g0"] = p["c_a"] * P["rho0"] / P["ka"] - p["c_h"] * P["beta"] * P["rho0"] / P["kh"]
    return {"rho": rho, "a": rho / P["ka"], "h": np.zeros((H, W)) + P["beta"] * rho.mean() / P["kh"],
            "La": 1.0 / (1 - dt * (P["Da"] * L - P["ka"])), "Lh": 1.0 / (1 - dt * (P["Dh"] * L - P["kh"])),
            "Sm": 1.0 / (1 - p["Lm"] ** 2 * L), "shape": (H, W), "p": p}


def step(s):
    p, dt = s["p"], s["p"]["dt"]
    rho, a, h = s["rho"], s["a"], s["h"]
    drho = p["Dr"] * ops.laplacian(rho)
    if p["mode"] == "h":
        ay, ax = ops.grad(a)
        drho = drho - vf_flux_div(rho, p["chi_a"] * ay, p["chi_a"] * ax)
        g = -p["c_h"] * h
    else:
        g = p["c_a"] * a - p["c_h"] * h
    rho = rho + dt * (drho + p["eps"] * (p["rho0"] - rho))
    # reaction part, substepped so that the explicit rate stays below 0.25 per substep
    rate = float(np.abs(g - g.mean()).max()) * 0.25 + 1e-12
    n = max(1, int(np.ceil(rate * dt / 0.25)))
    for _ in range(n):
        w = rho * (1 - rho)
        if p["mode"] == "local":
            gw = p["g0"]
        elif p["Lm"] > 0:   # local reference: screened-Poisson average (a fast-diffusing field)
            gw = (ops.irfft2(ops.rfft2(w * g) * s["Sm"], s["shape"])
                  / (ops.irfft2(ops.rfft2(w) * s["Sm"], s["shape"]) + 1e-12))
            gw = gw + (w * (g - gw)).sum() / (w.sum() + 1e-300)   # exact conservation of int rho
        else:
            gw = (w * g).sum() / (w.sum() + 1e-300)
        rho = np.clip(rho + (dt / n) * w * (g - gw), 0, 1)
    s["a"] = ops.irfft2(ops.rfft2(a + dt * rho) * s["La"], s["shape"])
    s["h"] = ops.irfft2(ops.rfft2(h + dt * p["beta"] * rho) * s["Lh"], s["shape"])
    s["rho"] = rho
    return s


def fields(s):
    return np.stack([s["rho"], s["a"], s["h"]])


def damage(s, mask):
    s["rho"][mask] = 0
    return s
