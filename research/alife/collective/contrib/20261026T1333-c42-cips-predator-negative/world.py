"""CIPS predator-prey (c42). Prey: c40's catalysis-induced enzyme condensates on a consumed, regrowing fuel F
(20261026T1025-c40-cips-turnover-divide-claim). Predator: a second enzyme q, made everywhere by turnover like e,
that drifts up its own product r (catalysis-induced phase separation again); its catalysis CONSUMES the prey
enzyme e (cat2 = kr e q^2 (1-r)), so a predator condensate can only exist where it digests prey enzyme, and a
prey condensate it sits on loses its enzyme. Neither kind is built from its food: e and q are made uniformly at
d*e0 and dq*q0; food only lets them condense.
  d q/dt = Dq lap q - div(chiq q(1-q) grad r) + dq (q0 - q)
  d r/dt = Dr lap r + kr e^ne q^2 (1-r) - ksr r   (ne=2: cooperative in the prey enzyme)
  d e/dt  += - y2 kr e q^2 (1-r)
pred_on 0: q held at 0 (prey-only twin).

Parent docstring:
Catalysis-induced phase separation (CIPS) on a consumed, regrowing fuel: c40 defaults (repeated division).

Defaults (c40): cooperative catalysis n=2, kc=2, De=0.1, chi=3, DF=2, kF=0.2, e0=0.12, enzyme turnover d=0.003
(linearly stable bath: lsa growth rate -2e-3), started from a random field (std 0.03, correlation 16 px).

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
    "name": "cips-predator-prey",
    "family": "catalysis-induced-phase-separation",
    "parent": "collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5",
    "mutation": "c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)",
    "size": (128, 128),
    "steps_per_frame": 1000,
    "dt": 0.1,
    "channels": ["e prey", "p", "F", "q predator", "r"],
    "matter": [0, 3],
    "species": {"prey": [0], "predator": [3]},
    "threshold": 0.5,
    "smooth": 1.0,
}

P = {
    "De": 0.1, "chi": 3.0, "kc": 2.0, "ks": 1.0, "DF": 2.0, "y": 1.0, "kF": 0.2,
    "Dp": 1.0,          # product diffusivity (1: c23 world)
    "n": 2.0,           # catalysis order in e (1: c23 world; 2: cooperative, e.g. a dimer-active enzyme)
    "d": 0.003,           # enzyme turnover rate (0: c23 world)
    "Lsc": 2.0,         # length scale in px: every diffusivity and chi multiplied by Lsc^2 (Lsc=1 is the question's dx=1 model)
    "hold": 0,          # 1: fuel held at 1 (reservoir, Cotton et al.)
    "e0": 0.12, "noise": 0.03, "dt": 0.1,
    "rf_len": 16.0,      # >0: initial noise is a smoothed random field with this correlation length (px)
    "plant_asp": 1.0,   # aspect ratio of the planted disk (x semi-axis = plant_r * plant_asp)
    "plant_r": 0.0,     # >0: mechanism test only, one planted enzyme disk (e=0.9) of this radius at the centre
    "fork_t": -1.0,     # time at which kF -> 0 everywhere (-1: never)
    "fork_d": -1.0,     # >=0: enzyme turnover rate after fork_t (control: 0 removes turnover with the fuel; -1: unchanged)
    "pred_on": 1, "q0": 0.06, "dq": 0.003, "Dq": 0.1, "chiq": 3.0, "kr": 2.0, "ksr": 1.0, "Dr": 1.0, "y2": 1.0, "ne": 2.0, "mq": 2.0, "t_intro": 0.0,
    "q_noise": 0.02,
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
    xi = rng.standard_normal((H, W))
    if p_["rf_len"] > 0:
        # random field: white noise smoothed over rf_len px, rescaled to std 1 (still unstructured over the whole domain)
        from scipy.ndimage import gaussian_filter
        xi = gaussian_filter(xi, p_["rf_len"], mode="wrap")
        xi = (xi - xi.mean()) / xi.std()
    e = p_["e0"] + p_["noise"] * xi
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
    xq = rng.standard_normal((H, W))
    if p_["rf_len"] > 0:
        from scipy.ndimage import gaussian_filter
        xq = gaussian_filter(xq, p_["rf_len"], mode="wrap"); xq = (xq - xq.mean()) / xq.std()
    qf = np.clip(p_["q0"] + p_["q_noise"] * xq, 0, 1) * (p_["pred_on"] > 0) * (p_["t_intro"] <= 0)
    rr = np.zeros((H, W))
    L = ops.lap_symbol(H, W) * p_["Lsc"] ** 2     # all diffusion lengths scaled by Lsc
    dt = p_["dt"]
    yy, xx = np.mgrid[0:H, 0:W]
    return {"e": e, "p": p, "F": F, "q": qf, "r": rr, "xq": xq,
            "Lq": 1.0 / (1 - dt * p_["Dq"] * L), "Lr": 1.0 / (1 - dt * (p_["Dr"] * L - p_["ksr"])), "t": 0.0, "shape": (H, W), "par": p_,
            "Le": 1.0 / (1 - dt * p_["De"] * L), "Lp": 1.0 / (1 - dt * (p_["Dp"] * L - p_["ks"])),
            "LF": 1.0 / (1 - dt * p_["DF"] * L), "yy": yy, "xx": xx}


def step(s):
    q, dt = s["par"], s["par"]["dt"]
    e, p, F = s["e"], s["p"], s["F"]
    sh = s["shape"]
    cat = q["kc"] * F * np.clip(e, 0, None) ** q["n"] * (1 - p)
    dd = q["d"]
    if q["fork_d"] >= 0 and q["fork_t"] >= 0 and s["t"] >= q["fork_t"]:
        dd = q["fork_d"]
    qq, rr = s["q"], s["r"]
    if q["pred_on"] and q["t_intro"] > 0 and abs(s["t"] - q["t_intro"]) < dt / 2:
        # predators appear: the predator enzyme is switched on at its noisy bath level (same field as at t=0)
        qq = np.clip(q["q0"] + q["q_noise"] * s["xq"], 0, 1); s["q"] = qq
    if q["pred_on"] and s["t"] < q["t_intro"]:
        qq = 0.0 * qq
    cat2 = q["kr"] * np.clip(e, 0, None) ** q["ne"] * np.clip(qq, 0, None) ** q["mq"] * (1 - rr)
    cat2 = np.minimum(cat2, 0.5 * np.clip(e, 0, None) / (dt * q["y2"]))
    e = e - dt * vf_flux_div(e, p, q["chi"] * q["Lsc"] ** 2) + dt * dd * (q["e0"] - e) - dt * q["y2"] * cat2
    if q["pred_on"] and s["t"] >= q["t_intro"]:
        qn = qq - dt * vf_flux_div(qq, rr, q["chiq"] * q["Lsc"] ** 2) + dt * q["dq"] * (q["q0"] - qq)
        s["q"] = ops.irfft2(ops.rfft2(qn) * s["Lq"], sh)
        s["r"] = ops.irfft2(ops.rfft2(rr + dt * cat2) * s["Lr"], sh)
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
    return np.stack([s["e"], s["p"], s["F"], s["q"], s["r"]])


def damage(s, mask):
    s["e"] = np.where(mask, 0.0, s["e"]); s["q"] = np.where(mask, 0.0, s["q"])
    return s
