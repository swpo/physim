"""Phase protocell: membrane = Allen-Cahn domain wall whose inside phase is held up by the
cell's own chemistry.

phi  inside-phase order parameter (1 inside, 0 outside). Allen-Cahn with a chemical tilt:
       d phi = Dp lap phi + r phi (1-phi) (phi - 1/2 + a (L - th))
     Without links the inside phase is metastable and curvature makes any domain shrink;
     links above th tilt the double well so the inside phase spreads.
S    substrate, free diffusion everywhere, fed from a reservoir (F (1 - S)).
K    catalyst: Gray-Scott autocatalysis S K^2, decays (F + k) K; mobility DK phi^2
     (catalyst cannot leave the inside phase).
L    link/lipid: made by K (b K S), decays dL; mobility DL phi^2 (held inside).
M    rendered membrane = 4 phi (1 - phi) (the domain wall), plus the wall carries the
     tension: nothing else.
Loop: K makes L, L holds the phase up, the phase holds K and L in. Damage to the wall is
repaired by curvature flow + tilt; division happens when K splits into two spots and the
L-poor neck between them reverts to the outside phase.
"""
import numpy as np

META = {
    "name": "phase-protocell",
    "family": "autopoiesis",
    "parent": "threads/autopoiesis/worlds/gated_protocell",
    "mutation": "membrane is an Allen-Cahn domain wall (always closed) instead of a polymerized field; the inside phase is tilted by catalyst-made links; K and L mobility ~ phi^2",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 1.0,
    "channels": ["S", "K catalyst", "L link", "membrane (wall)"],
    "matter": None,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(DS=0.2, DK=0.1, DL=0.1, Dp=0.1, r=0.2, a=4.0, th=0.15, F=0.006, k=0.0649, b=0.05, dL=0.02,
         gate=1, gateK=1, nophase=0, K0=0.5, kin="logistic", c=0.2, dK=0.02, nspots=4, R0=6, IC="spots")


def lap(u):
    return np.roll(u, 1, 0) + np.roll(u, -1, 0) + np.roll(u, 1, 1) + np.roll(u, -1, 1) - 4 * u


def mob_div(u, g, D):
    out = np.zeros_like(u)
    for ax in (0, 1):
        gf = 0.5 * (g + np.roll(g, -1, ax))
        flux = D * gf * (np.roll(u, -1, ax) - u)
        out += flux - np.roll(flux, 1, ax)
    return out


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    S, K, L, phi = np.ones((H, W)), np.zeros((H, W)), np.zeros((H, W)), np.zeros((H, W))
    yy, xx = np.mgrid[0:H, 0:W]
    if P["IC"] == "spots":
        for _ in range(P["nspots"]):
            y, x = rng.integers(0, H), rng.integers(0, W)
            d2 = ((yy - y + H / 2) % H - H / 2) ** 2 + ((xx - x + W / 2) % W - W / 2) ** 2
            m = d2 <= 16
            S[m], K[m], L[m] = 0.5, P["K0"], 0.5
            phi = np.maximum(phi, 0.5 * (1 - np.tanh((np.sqrt(d2) - P["R0"]) / 1.5)))
    else:  # noise: random patches of catalyst, no phase
        K = 0.3 * (rng.random((H, W)) < 0.002)
        L = K.copy()
        phi = K.copy()
    K += 0.01 * rng.random((H, W)) * phi
    return {"S": S, "K": K, "L": L, "phi": phi}


def step(s):
    S, K, L, phi = s["S"], s["K"], s["L"], s["phi"]
    g = phi * phi if P["gate"] else np.ones_like(phi)
    if P["kin"] == "gs":
        auto = S * K * K * phi  # the catalyst only works in the inside phase
        kdec = P["F"] + P["k"]
    else:  # logistic autocatalysis, saturating at K = 1
        auto = P["c"] * S * K * (1 - K) * phi
        kdec = P["dK"]
    prodL = P["b"] * K * S
    lim = np.minimum(1.0, 0.5 * S / np.maximum(auto + prodL, 1e-12))
    auto, prodL = auto * lim, prodL * lim
    s["S"] = np.maximum(S + P["DS"] * lap(S) - auto - prodL + P["F"] * (1 - S), 0)
    s["K"] = np.maximum(K + mob_div(K, g if P["gateK"] else np.ones_like(g), P["DK"]) + auto - kdec * K, 0)
    s["L"] = np.maximum(L + mob_div(L, g, P["DL"]) + prodL - P["dL"] * L, 0)
    if P["nophase"]:
        s["phi"] = np.ones_like(phi); return s
    s["phi"] = np.clip(phi + P["Dp"] * lap(phi) + P["r"] * phi * (1 - phi) * (phi - 0.5 + P["a"] * (L - P["th"])), 0, 1)
    return s


def fields(s):
    phi = s["phi"]
    return np.stack([s["S"], s["K"], s["L"], 4 * phi * (1 - phi)]).astype(np.float32)


def matter(F):
    # an individual = the inside phase; recover phi >= 1/2 region from the channels
    return (F[3] + 2 * (F[2] > 0.02)).astype(np.float32) if False else (F[1] + F[2] + F[3]).astype(np.float32)


def stats(s):
    phi = s["phi"]
    from scipy import ndimage
    lab, n = ndimage.label(phi > 0.5)
    return {"K": round(float(s["K"].sum()), 1), "L": round(float(s["L"].sum()), 1), "area": int((phi > 0.5).sum()), "cells": int(n)}


def damage(s, mask):
    """move labkit's centroid disk outward by the cell's equivalent radius along +x so it
    removes part of the wall and interior; reset to bath inside the disk."""
    H, W = mask.shape
    ys, xs = np.nonzero(mask)
    if len(ys) == 0:
        return s
    r = np.sqrt(len(ys) / np.pi)
    R = r / np.sqrt(0.3)
    cy, cx = ys.mean(), xs.mean() + 0.8 * R
    yy, xx = np.mgrid[0:H, 0:W]
    dy = (yy - cy + H / 2) % H - H / 2
    dx = (xx - cx + W / 2) % W - W / 2
    hole = dy ** 2 + dx ** 2 <= (1.2 * r) ** 2
    s["S"][hole], s["K"][hole], s["L"][hole], s["phi"][hole] = 1, 0, 0, 0
    return s
