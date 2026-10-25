"""Laplacian-only twin of swimfission (c01). Everything as swimfission except the taxis flux
-div(rho(1-rho)(chi_a grad a - chi_h grad h)), which is replaced by the local reaction
rho(1-rho)(c_a a - c_h h - ref), ref = screened-Poisson average (range Lm) of the same
quantity plus one uniform correction, so the conversion conserves int rho exactly (as the taxis
flux does). c_a = fa chi_a, c_h = fh chi_h. Same construction as
collective/contrib/20261025T0632-c01-kstrail-rd-twin/twin.py. chi_n is 0 in swimfission. Growth starts at t_on = 400 (not 150), because the twin forms
bodies more slowly; switched on at 150 it grows the uniform state and floods the domain.

Original description:
Swimmers that eat, grow and divide by binary fission (fork of toxforage).

Only change: the cohesion attractant diffuses less (Da 4 -> 2), so its range sqrt(Da/ka) falls from
6.3 to 4.5 px. A swimmer that grows by eating at its front elongates beyond the attractant
range, pinches at the waist and splits into two daughter swimmers (cf. active-droplets: division
needs a body larger than its internal transport length).

Parent description:
Toxic-trail swimmers that must also eat (fork of toxtrail).

Growth now needs a consumed nutrient n:  g n rho^3/(rh^2+rho^2); n regrows at rate r toward 1
and diffuses (Dn); c = nutrient used per unit of growth. Swimmers leave both waste and depleted
food behind, so the trail is doubly repulsive (waste repels by taxis, food attracts by taxis chi_n).

Parent description:
Trail swimmers whose trail is toxic waste: growth + self-poisoning (fork of kstrail).

Added kinetics:  + g rho rho^2/(rh^2+rho^2) - kd h rho   (switched on at t >= t_on)
A body that stops moving sits in its own accumulating waste h and dies from the inside;
a swimmer leaves its waste behind. Prediction: motility becomes a condition for survival, and
growth plus inner die-back makes large bodies hollow into rings that rupture into several swimmers
(fission).

Original kstrail description:
Autochemotactic spots that flee their own trail.

rho : cell density with volume filling (0..1)
a   : fast, short-lived attractant secreted by rho  -> self-aggregation (body)
h   : slow, long-lived repellent secreted by rho    -> self-repulsive trail (propulsion)

  d rho/dt = Dr lap rho - div( rho (1-rho) (chi_a grad a - chi_h grad h) )
  d a/dt   = Da lap a + rho - ka a
  d h/dt   = Dh lap h + beta rho - kh h

Hypothesis: the spot sits on top of its own accumulating repellent; any displacement
puts the old trail behind it and the gradient pushes it forward (symmetry breaking).
"""
import json
import os

import numpy as np

from labkit import ops

META = {
    "name": "swimfission-rd-twin",
    "family": "chemotaxis",
    "parent": "toxforage",
    "mutation": "shorter cohesion range (Da 4 -> 2): grown swimmers exceed it and divide",
    "size": (160, 160),
    "steps_per_frame": 120,
    "dt": 0.05,
    "channels": ["rho", "a", "h", "n"],
    "matter": [0],
    "smooth": 1.0,
}

P = {
    # lengths are ~2x the first screens (body radius ~6 px) so bodies are resolved and
    # headings are not pulled to the grid diagonals (see NOTEBOOK)
    "Dr": 1.2, "Da": 2.0, "ka": 0.1, "Dh": 0.2, "kh": 0.05, "beta": 1.0,
    "chi_a": 24.0, "chi_h": 4.8, "rho0": 0.05, "noise": 0.02, "dt": 0.05, "g": 0.1, "rh": 0.3, "kd": 0.005, "t_on": 400.0, "r": 0.06, "c": 2.0, "Dn": 0.5, "chi_n": 0.0, "fa": 0.25, "fh": 0.5, "Lm": 3.0,
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
    rho = np.clip(P["rho0"] + P["noise"] * rng.standard_normal((H, W)), 0, 1)
    rho = ops.fft_conv(rho, ops.gauss_kernel(H, W, 1.0))
    L = ops.lap_symbol(H, W)
    dt = P["dt"]
    return {"rho": rho, "a": rho / P["ka"], "h": np.zeros((H, W)) + P["beta"] * rho.mean() / P["kh"],
            "La": 1.0 / (1 - dt * (P["Da"] * L - P["ka"])), "Lh": 1.0 / (1 - dt * (P["Dh"] * L - P["kh"])),
            "Sm": 1.0 / (1 - P["Lm"] ** 2 * L),
            "shape": (H, W), "p": dict(P), "n": np.ones((H, W)),
            "Ln": 1.0 / (1 - dt * (P["Dn"] * L - P["r"]))}


def step(s):
    p, dt = s["p"], s["p"]["dt"]
    rho, a, h = s["rho"], s["a"], s["h"]
    s["t"] = s.get("t", 0.0) + dt
    n = s["n"]
    kin, grow = 0.0, 0.0
    if s["t"] >= p["t_on"]:
        grow = p["g"] * n * rho * rho ** 2 / (p["rh"] ** 2 + rho ** 2)
        kin = grow - p["kd"] * h * rho
    s["n"] = np.clip(ops.irfft2(ops.rfft2(n + dt * (p["r"] - p["c"] * grow)) * s["Ln"], s["shape"]), 0, None)
    rho = rho + dt * (p["Dr"] * ops.laplacian(rho) + kin)
    g = p["fa"] * p["chi_a"] * a - p["fh"] * p["chi_h"] * h
    rate = float(np.abs(g - g.mean()).max()) * 0.25 + 1e-12
    k = max(1, int(np.ceil(rate * dt / 0.25)))
    for _ in range(k):
        w = rho * (1 - rho)
        gw = (ops.irfft2(ops.rfft2(w * g) * s["Sm"], s["shape"])
              / (ops.irfft2(ops.rfft2(w) * s["Sm"], s["shape"]) + 1e-12))
        gw = gw + (w * (g - gw)).sum() / (w.sum() + 1e-300)
        rho = np.clip(rho + (dt / k) * w * (g - gw), 0, 1)
    s["a"] = ops.irfft2(ops.rfft2(a + dt * rho) * s["La"], s["shape"])
    s["h"] = ops.irfft2(ops.rfft2(h + dt * p["beta"] * rho) * s["Lh"], s["shape"])
    s["rho"] = rho
    return s


def fields(s):
    return np.stack([s["rho"], s["a"], s["h"], s["n"]])


def damage(s, mask):
    s["rho"][mask] = 0
    return s
