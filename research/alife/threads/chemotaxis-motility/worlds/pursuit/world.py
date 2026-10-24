"""Pursuit and predation between two species of trail-fleeing chemotactic swimmers.

Each species i (0 = prey p, 1 = predator q) is a kstrail swimmer: volume-filled density
rho_i, its own fast attractant a_i (cohesion) and slow repellent h_i (self-propulsion).
Cross-taxis: predators climb the prey attractant, prey descend the predator attractant.
Predation: predator density converts prey density on contact (rate k, yield e); prey
grow on a regrowing nutrient n with cooperative (Allee) growth; predators die at rate dq.

  d rho_i/dt = D lap rho_i - div( rho_i(1-rho_i) v_i ) + R_i
  v_p = chi_a grad a_p - chi_h grad h_p - chi_x grad a_q
  v_q = chi_a grad a_q - chi_h grad h_q + chi_y grad a_p
  R_p = g n p^2/(rh^2+p^2) - k p q - dp p ;  R_q = e k p q - dq q
  d n/dt = Dn lap n + r (1-n) - c g n p^2/(rh^2+p^2)
"""
import json
import os

import numpy as np

from labkit import ops

META = {
    "name": "pursuit",
    "family": "chemotaxis",
    "parent": "kstrail",
    "mutation": "two kstrail species with cross-taxis (predator up prey signal, prey down predator signal) + predation and nutrient-limited prey growth",
    "size": (160, 160),
    "steps_per_frame": 60,
    "dt": 0.05,
    "channels": ["prey", "predator", "n"],
    "matter": [0, 1],
    "smooth": 1.0,
}

P = {
    "Dr": 1.2, "Da": 4.0, "ka": 0.1, "Dh": 0.2, "kh": 0.05, "beta": 1.0,
    "chi_a": 24.0, "chi_h": 4.8, "chi_x": 8.0, "chi_y": 8.0,
    "k": 0.0, "e": 0.5, "dq": 0.0, "dp": 0.0, "g": 0.0, "rh": 0.3, "r": 0.01, "c": 1.0, "Dn": 0.5,
    "t_on": 0.0, "rho0": 0.05, "qfrac": 0.5, "noise": 0.02, "dt": 0.05,
}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))  # screening override only; packs use the defaults above


def _faces(u, ax):
    """MUSCL (van Leer limited) left/right states at face i+1/2 along axis ax."""
    up, um = np.roll(u, -1, ax), np.roll(u, 1, ax)
    d1, d2 = u - um, up - u
    slope = np.where(d1 * d2 > 0, 2 * d1 * d2 / (d1 + d2 + 1e-300), 0.0)
    left = u + 0.5 * slope                         # state just left of face i+1/2
    right = np.roll(u - 0.5 * slope, -1, ax)       # state just right of face i+1/2
    return left, right


def vf_flux_div(rho, vy, vx):
    """Conservative divergence of rho (1-rho) v with face flux v * rho_up * (1 - rho_down).

    Second-order MUSCL reconstruction (van Leer limiter) to cut the anisotropic numerical
    diffusion of first-order upwinding, which made swimmers prefer diagonal headings.
    Volume filling (Painter & Hillen 2002) keeps 0 <= rho <= 1."""
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
    rho = np.stack([P["rho0"] + P["noise"] * rng.standard_normal((H, W)),
                    P["qfrac"] * P["rho0"] + P["noise"] * rng.standard_normal((H, W))])
    rho = np.clip(ops.fft_conv(rho, ops.gauss_kernel(H, W, 1.0)), 0, 1)
    L = ops.lap_symbol(H, W)
    dt = P["dt"]
    return {"rho": rho, "a": rho / P["ka"], "h": P["beta"] * rho / P["kh"], "n": np.ones((H, W)),
            "La": 1.0 / (1 - dt * (P["Da"] * L - P["ka"])), "Lh": 1.0 / (1 - dt * (P["Dh"] * L - P["kh"])),
            "Ln": 1.0 / (1 - dt * (P["Dn"] * L - P["r"])), "shape": (H, W), "p": dict(P)}


def step(s):
    p, dt = s["p"], s["p"]["dt"]
    rho, a, h, n = s["rho"], s["a"], s["h"], s["n"]
    ay, ax = ops.grad(a)
    hy, hx = ops.grad(h)
    vy = p["chi_a"] * ay - p["chi_h"] * hy
    vx = p["chi_a"] * ax - p["chi_h"] * hx
    vy[0] -= p["chi_x"] * ay[1]
    vx[0] -= p["chi_x"] * ax[1]
    vy[1] += p["chi_y"] * ay[0]
    vx[1] += p["chi_y"] * ax[0]
    pr, q = rho
    food = p["g"] * n * pr * pr ** 2 / (p["rh"] ** 2 + pr ** 2)
    eat = p["k"] * pr * q
    s["t"] = s.get("t", 0.0) + dt
    R = np.stack([food - eat - p["dp"] * pr, p["e"] * eat - p["dq"] * q])
    if s["t"] < p["t_on"]:   # kinetics off while swimmers condense from the noise
        food, R = 0 * food, 0 * R
    mot = np.stack([p["Dr"] * ops.laplacian(rho[i]) - vf_flux_div(rho[i], vy[i], vx[i]) for i in range(2)])
    rho = np.clip(rho + dt * (mot + R), 0, 1)
    s["a"] = ops.irfft2(ops.rfft2(a + dt * rho) * s["La"], s["shape"])
    s["h"] = ops.irfft2(ops.rfft2(h + dt * p["beta"] * rho) * s["Lh"], s["shape"])
    s["n"] = np.clip(ops.irfft2(ops.rfft2(n + dt * (p["r"] - p["c"] * food)) * s["Ln"], s["shape"]), 0, None)
    s["rho"] = rho
    return s


def fields(s):
    return np.concatenate([s["rho"], s["n"][None]])


def damage(s, mask):
    s["rho"][:, mask] = 0
    return s
