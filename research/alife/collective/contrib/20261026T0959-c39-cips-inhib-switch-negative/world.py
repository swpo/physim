"""(c39: kI_t switches the inhibitor source on at time kI_t; kI_t=0 is the original world.)
Catalysis-induced phase separation (CIPS) on a consumed, regrowing fuel.

e : enzyme, with uniform turnover: made everywhere at rate s0 = d*e0, lost at rate d*e
    (the turnover does not depend on F; c35's change to c23's world)
p : product of catalysis (decays)
F : fuel, consumed by catalysis, regrown toward 1 at rate kF (or held at 1: the reservoir)

  d e/dt = De lap e - div( chi e (1-e) grad p ) + d (e0 - e)        (drift up the product: a chemotactic
                                                           stand-in for Cotton et al.'s
                                                           Flory-Huggins cross-diffusion)
  d p/dt = Dp lap p + kc F e (1-p) - ks p
  d F/dt = DF lap F - y kc F e (1-p) + kF (1-F)

Cotton, Golestanian & Agudo-Canalejo (PRL 129, 158101, 2022): enzyme catalysis alone can phase
separate the enzyme; with fuel held by a reservoir the domains coarsen without end. Question
(Q:cips-fuel-limited-condensates): does a consumed fuel cap body size and make bodies split?
Numerics: periodic, dx=1, implicit spectral diffusion for all fields, explicit reactions,
conservative MUSCL volume-filling face flux for the enzyme drift (int e conserved exactly).
"""
import json
import os

import numpy as np

from labkit import ops

META = {
    "name": "cips-turnover",
    "family": "catalysis-induced-phase-separation",
    "parent": "collective/contrib/20261025T1845-c23-cips-metabolic-claim",
    "mutation": "c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)",
    "size": (256, 256),
    "steps_per_frame": 100,
    "dt": 0.1,
    "channels": ["e", "p", "F"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 1.0,
}

P = {
    "De": 0.01, "chi": 1.0, "kc": 1.0, "ks": 1.0, "DF": 1.0, "y": 1.0, "kF": 0.2,
    "Dp": 1.0,          # product diffusivity (1: c23 world)
    "n": 1.0,           # catalysis order in e (1: c23 world; 2: cooperative, e.g. a dimer-active enzyme)
    "kI": 0.0, "kI_t": 0.0, "dI": 0.01, "DI": 0.1, "KI": 0.5,   # c35: catalysis inhibitor made by catalysis (c23 20261025T2130)
    "d": 0.0,           # enzyme turnover rate (0: c23 world)
    "Lsc": 3.0,         # length scale in px: every diffusivity and chi multiplied by Lsc^2 (Lsc=1 is the question's dx=1 model)
    "hold": 0,          # 1: fuel held at 1 (reservoir, Cotton et al.)
    "e0": 0.15, "noise": 0.01, "dt": 0.1,
    "plant_asp": 1.0,   # aspect ratio of the planted disk (x semi-axis = plant_r * plant_asp)
    "plant_r": 0.0,     # >0: mechanism test only, one planted enzyme disk (e=0.9) of this radius at the centre
    "fork_t": -1.0,     # time at which kF -> 0 everywhere (-1: never)
    "cut_t": -1.0, "cut_r": 0.0, "cut_y": 0.0, "cut_x": 0.0,   # local feed cut: kF=0 in a disk from cut_t
}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def _faces(u, ax):
    up, um = np.roll(u, -1, ax), np.roll(u, 1, ax)
    d1, d2 = u - um, up - u
    slope = np.where(d1 * d2 > 0, 2 * d1 * d2 / (d1 + d2 + 1e-300), 0.0)
    return u + 0.5 * slope, np.roll(u - 0.5 * slope, -1, ax)


def vf_flux_div(e, p, chi):
    """div of chi e(1-e) grad p, conservative: face velocity chi (p_{i+1}-p_i), upwinded MUSCL e."""
    out = np.zeros_like(e)
    for ax in (-2, -1):
        vf = chi * (np.roll(p, -1, ax) - p)
        L, R = _faces(e, ax)
        flux = np.where(vf > 0, vf * L * (1 - R), vf * R * (1 - L))
        out += flux - np.roll(flux, 1, ax)
    return out


def _ss_p(e, F, kc, ks):
    return kc * F * e / (kc * F * e + ks)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    p_ = dict(P)
    e = p_["e0"] + p_["noise"] * rng.standard_normal((H, W))
    if p_["plant_r"] > 0:
        yy, xx = np.mgrid[0:H, 0:W]
        e = np.where((yy - H / 2) ** 2 + ((xx - W / 2) / p_["plant_asp"]) ** 2 < p_["plant_r"] ** 2, 0.9, e)
    e = np.clip(e, 0.0, 1.0)
    F = np.ones((H, W))
    if not p_["hold"]:
        # uniform steady state of the fuel for the mean enzyme
        Fs = 1.0
        for _ in range(200):
            pp = _ss_p(p_["e0"], Fs, p_["kc"], p_["ks"])
            Fs = p_["kF"] / (p_["kF"] + p_["y"] * p_["kc"] * p_["e0"] * (1 - pp)) if p_["kF"] > 0 else 0.0
        F = F * Fs
    p = _ss_p(e, F, p_["kc"], p_["ks"])
    L = ops.lap_symbol(H, W) * p_["Lsc"] ** 2     # all diffusion lengths scaled by Lsc
    dt = p_["dt"]
    yy, xx = np.mgrid[0:H, 0:W]
    return {"e": e, "p": p, "F": F, "t": 0.0, "shape": (H, W), "par": p_,
            "Le": 1.0 / (1 - dt * p_["De"] * L), "Lp": 1.0 / (1 - dt * (p_["Dp"] * L - p_["ks"])),
            "LF": 1.0 / (1 - dt * p_["DF"] * L), "LI": 1.0 / (1 - dt * (p_["DI"] * L - p_["dI"])), "I": np.zeros((H, W)), "yy": yy, "xx": xx}


def step(s):
    q, dt = s["par"], s["par"]["dt"]
    e, p, F = s["e"], s["p"], s["F"]
    sh = s["shape"]
    cat = q["kc"] * F * np.clip(e, 0, None) ** q["n"] * (1 - p) / (1 + s["I"] / q["KI"])
    s["I"] = ops.irfft2(ops.rfft2(s["I"] + dt * (q["kI"] if s["t"] >= q["kI_t"] else 0.0) * cat) * s["LI"], sh)
    e = e - dt * vf_flux_div(e, p, q["chi"] * q["Lsc"] ** 2) + dt * q["d"] * (q["e0"] - e)
    s["e"] = ops.irfft2(ops.rfft2(e) * s["Le"], sh)
    s["p"] = ops.irfft2(ops.rfft2(p + dt * cat) * s["Lp"], sh)
    if q["hold"]:
        s["F"] = F
    else:
        kF = q["kF"]
        if q["fork_t"] >= 0 and s["t"] >= q["fork_t"]:
            kF = 0.0
        if q["cut_t"] >= 0 and s["t"] >= q["cut_t"]:
            H, W = sh
            dy = (s["yy"] - q["cut_y"] + H / 2) % H - H / 2
            dx = (s["xx"] - q["cut_x"] + W / 2) % W - W / 2
            kF = kF * ((dy * dy + dx * dx) > q["cut_r"] ** 2)
        Fn = F + dt * (-q["y"] * cat + kF * (1 - F))
        s["F"] = ops.irfft2(ops.rfft2(Fn) * s["LF"], sh)
    s["t"] += dt
    return s


def fields(s):
    return np.stack([s["e"], s["p"], s["F"]])


def damage(s, mask):
    s["e"] = np.where(mask, 0.0, s["e"])
    return s
