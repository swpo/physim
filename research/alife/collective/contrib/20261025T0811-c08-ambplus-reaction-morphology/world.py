"""Active Model B+ (Tjhung, Nardini & Cates, PRX 8, 031080, 2018) with an optional
Model-A reaction (Li & Cates, J. Stat. Mech. 2020, canonical Model AB), 2D, periodic.

    d phi/dt = lap(mu) - zeta div((lap phi) grad phi) + g(phi) + noise
    mu = -A phi + A phi^3 - K lap(phi) + lam |grad phi|^2
    g  = -u (phi - phi_a)(phi - phi_t)                      (u = 0: pure AMB+, conserved)
    noise = -div(sqrt(2 D) Lambda)  (conserved, additive)

Pseudo-spectral derivatives with 2/3 dealiasing; semi-implicit Euler-Maruyama: K lap^2 and a
linear stabiliser S lap (added and subtracted) are implicit, everything else explicit.
Region B (zeta, lam both negative, e.g. (-4, -1)) reverses Ostwald ripening for dense droplets.
Defaults: region B arm of the morphology finding (u=3e-4, phi_t=-0.2). Arms in runs/list.txt.
Parameters can be overridden with the env var WORLD_P (JSON), for screening only.
"""
import json, os
import numpy as np
from numpy.fft import rfft2, irfft2

META = {
    "name": "ambplus-ab",
    "family": "active-emulsion",
    "parent": None,
    "mutation": "reference: Active Model B+ (zeta, lambda) with an optional Model-A birth/death reaction",
    "size": (128, 128),
    "steps_per_frame": 1000,
    "dt": 0.03,
    "channels": ["phi"],
    "matter": [0],
    "threshold": 0.0,
    "smooth": 0.5,
}

P = dict(A=0.25, K=1.0, zeta=-1.6, lam=-0.8, S=1.0, dt=0.03, D=0.0,
         u=3e-4, phi_a=-10.0, phi_t=-0.2, phi0=-0.4, noise0=0.05)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    phi = P["phi0"] + P["noise0"] * rng.standard_normal((H, W))
    ky = 2 * np.pi * np.fft.fftfreq(H)[:, None]
    kx = 2 * np.pi * np.fft.rfftfreq(W)[None, :]
    k2 = kx ** 2 + ky ** 2
    da = (np.abs(kx) < 2 / 3 * np.pi) & (np.abs(ky) < 2 / 3 * np.pi)
    dt = P["dt"]
    den = 1 + dt * (P["K"] * k2 ** 2 + P["S"] * k2)
    return {"phi": phi, "kx": kx, "ky": ky, "k2": k2, "da": da, "den": den,
            "shape": (H, W), "rng": rng}


def step(s):
    phi, kx, ky, k2, sh, dt = s["phi"], s["kx"], s["ky"], s["k2"], s["shape"], P["dt"]
    ph = rfft2(phi)
    gx, gy = irfft2(1j * kx * ph, sh), irfft2(1j * ky * ph, sh)
    lap = irfft2(-k2 * ph, sh)
    mu = P["A"] * (phi ** 3 - phi) + P["lam"] * (gx * gx + gy * gy) - P["S"] * phi
    rhs = -k2 * rfft2(mu) - P["zeta"] * (1j * kx * rfft2(lap * gx) + 1j * ky * rfft2(lap * gy))
    if P["u"]:
        rhs = rhs + rfft2(-P["u"] * (phi - P["phi_a"]) * (phi - P["phi_t"]))
    rhs = rhs * s["da"]
    if P["D"]:
        r = s["rng"]
        nx, ny = r.standard_normal(sh), r.standard_normal(sh)
        rhs = rhs - s["da"] * np.sqrt(2 * P["D"] / dt) * (1j * kx * rfft2(nx) + 1j * ky * rfft2(ny))
    s["phi"] = irfft2((ph + dt * rhs) / s["den"], sh)
    return s


def fields(s):
    return s["phi"][None]


def damage(s, mask):
    s["phi"][mask] = P["phi_t"] if P["u"] else -1.0
    return s
