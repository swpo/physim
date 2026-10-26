"""Two-enzyme catalysis-induced phase separation with non-reciprocal chemotaxis, on a consumed, regrowing fuel.

e1, e2 : enzymes (conserved; no reaction, no decay term), volume filling on the total e1 + e2
p1, p2 : products of each enzyme's catalysis (decay)
F      : fuel consumed by both catalyses, regrown toward 1 at rate kF

  d e_i/dt = De lap e_i - div( e_i (1 - e1 - e2) sum_j chi_ij grad p_j )
  d p_i/dt = lap p_i + kc F e_i (1 - p_i) - ks p_i
  d F/dt   = DF lap F - y kc F sum_i e_i (1 - p_i) + kF (1 - F)

chi_11, chi_22 > 0 make each enzyme condense on its own product (CIPS, Cotton et al. 2022); chi_12 > 0 and
chi_21 < 0 make e1 chase p2 while e2 flees p1 (non-reciprocal, Agudo-Canalejo & Golestanian PRL 2019), which
can turn an e1-e2 composite into a self-propelled body. Lengths scaled by Lsc as in
20261025T1845-c23-cips-metabolic-claim. Conservative MUSCL face flux; int e1 and int e2 are conserved.
"""
import json
import os

import numpy as np

from labkit import ops

META = {
    "name": "cips-nr-turnover",
    "family": "catalysis-induced-phase-separation",
    "parent": "collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py",
    "mutation": "two conserved enzymes with non-reciprocal cross-chemotaxis (e1 chases p2, e2 flees p1)",
    "size": (256, 256),
    "steps_per_frame": 100,
    "dt": 0.1,
    "channels": ["e1", "e2", "p1", "p2", "F"],
    "matter": json.loads(os.environ.get("WORLD_P", "{}")).get("matter", [0, 1]),
    "threshold": 0.4,
    "smooth": 1.0,
}

P = {
    "De": 0.01, "c11": 1.0, "c22": 1.0, "c12": 1.0, "c21": -1.0,
    "kc": 1.0, "ks": 1.0, "DF": 1.0, "y": 1.0, "kF": 0.2, "hold": 0, "Lsc": 3.0,
    "e10": 0.1, "e20": 0.1, "noise": 0.01, "dt": 0.1,
    "fork_t": -1.0,
    "n": 1.0,   # c35: catalysis order in e_i
    "d": 0.0,   # c35: uniform enzyme turnover d (e_i0 - e_i), independent of fuel
}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def _faces(u, ax):
    up, um = np.roll(u, -1, ax), np.roll(u, 1, ax)
    d1, d2 = u - um, up - u
    slope = np.where(d1 * d2 > 0, 2 * d1 * d2 / (d1 + d2 + 1e-300), 0.0)
    return u + 0.5 * slope, np.roll(u - 0.5 * slope, -1, ax)


def flux_div(e, et, vfs):
    """div of e (1 - et) v with face velocities vfs[ax]; upwinded MUSCL e, downstream vacancy (1 - et)."""
    out = np.zeros_like(e)
    for ax in (-2, -1):
        vf = vfs[ax]
        L, R = _faces(e, ax)
        tL, tR = _faces(et, ax)
        flux = np.where(vf > 0, vf * L * np.clip(1 - tR, 0, 1), vf * R * np.clip(1 - tL, 0, 1))
        out += flux - np.roll(flux, 1, ax)
    return out


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    q = dict(P)
    e1 = np.clip(q["e10"] + q["noise"] * rng.standard_normal((H, W)), 0, 1)
    e2 = np.clip(q["e20"] + q["noise"] * rng.standard_normal((H, W)), 0, 1)
    F = np.ones((H, W))
    p1 = q["kc"] * e1 / (q["kc"] * e1 + q["ks"])
    p2 = q["kc"] * e2 / (q["kc"] * e2 + q["ks"])
    L = ops.lap_symbol(H, W) * q["Lsc"] ** 2
    dt = q["dt"]
    return {"e1": e1, "e2": e2, "p1": p1, "p2": p2, "F": F, "t": 0.0, "shape": (H, W), "par": q,
            "Le": 1.0 / (1 - dt * q["De"] * L), "Lp": 1.0 / (1 - dt * (L - q["ks"])), "LF": 1.0 / (1 - dt * q["DF"] * L)}


def step(s):
    q, dt, sh = s["par"], s["par"]["dt"], s["shape"]
    e1, e2, p1, p2, F = s["e1"], s["e2"], s["p1"], s["p2"], s["F"]
    k = q["Lsc"] ** 2
    et = e1 + e2
    g1 = {ax: (np.roll(p1, -1, ax) - p1) for ax in (-2, -1)}
    g2 = {ax: (np.roll(p2, -1, ax) - p2) for ax in (-2, -1)}
    v1 = {ax: k * (q["c11"] * g1[ax] + q["c12"] * g2[ax]) for ax in (-2, -1)}
    v2 = {ax: k * (q["c21"] * g1[ax] + q["c22"] * g2[ax]) for ax in (-2, -1)}
    c1 = q["kc"] * F * np.clip(e1, 0, None) ** q["n"] * (1 - p1)
    c2 = q["kc"] * F * np.clip(e2, 0, None) ** q["n"] * (1 - p2)
    n1 = e1 - dt * flux_div(e1, et, v1)
    n2 = e2 - dt * flux_div(e2, et, v2)
    n1 = n1 + dt * q["d"] * (q["e10"] - e1)
    n2 = n2 + dt * q["d"] * (q["e20"] - e2)
    s["e1"] = ops.irfft2(ops.rfft2(n1) * s["Le"], sh)
    s["e2"] = ops.irfft2(ops.rfft2(n2) * s["Le"], sh)
    s["p1"] = ops.irfft2(ops.rfft2(p1 + dt * c1) * s["Lp"], sh)
    s["p2"] = ops.irfft2(ops.rfft2(p2 + dt * c2) * s["Lp"], sh)
    if not q["hold"]:
        kF = 0.0 if (q["fork_t"] >= 0 and s["t"] >= q["fork_t"]) else q["kF"]
        s["F"] = ops.irfft2(ops.rfft2(F + dt * (-q["y"] * (c1 + c2) + kF * (1 - F))) * s["LF"], sh)
    s["t"] += dt
    return s


def fields(s):
    return np.stack([s["e1"], s["e2"], s["p1"], s["p2"], s["F"]])


def damage(s, mask):
    s["e1"] = np.where(mask, 0.0, s["e1"])
    s["e2"] = np.where(mask, 0.0, s["e2"])
    return s
