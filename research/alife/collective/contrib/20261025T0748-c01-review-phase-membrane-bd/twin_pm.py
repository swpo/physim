"""Laplacian-only twin of phase_membrane (c01): gate=0 (uniform mobility for K and L instead of
phi^2), chi=0 (no wall-adsorption drift), and K, L diffusivities scaled by lam (a uniformly lowered
D, the matched control for a mobility gate). Everything else is phase_membrane unchanged.
WORLD_P (JSON) overrides P for sweeps; the defaults below are the twin.

Original description: Phase membrane: phase protocell whose links adsorb to the wall.

New relative to phase_protocell_noise: links drift up the gradient of the wall indicator
w = 4 phi (1 - phi), flux  -D g grad L + D g chi L grad w  (upwind), so the link that holds the
wall up (tilt a (L - th), which only matters where 0 < phi < 1) collects in a layer AT the wall:
the membrane becomes a layer of the cell's own product, not only a phase boundary.

Parent description follows.
Phase protocell: membrane = Allen-Cahn domain wall whose inside phase is held up by the
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
    "name": "phase-membrane-bd-twin",
    "family": "autopoiesis",
    "parent": "threads/autopoiesis/worlds/phase_protocell_noise",
    "mutation": "links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 1.0,
    "channels": ["S", "K catalyst", "L link", "membrane (wall)"],
    "matter": None,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(DS=0.2, DK=0.1, DL=0.1, Dp=0.1, r=0.2, a=4.0, th=0.15, F=0.006, k=0.0649, b=0.05, dL=0.02,
         gate=1, gateK=1, nophase=0, scale=1, noise_amp=0.2, noise_mean=0.0, noise_KL=0.1, noise_K=0.6, dt=1.0, K0=0.5, kin="logistic", c=0.2, dK=0.02, nspots=4, R0=6, IC="noise", chi=0.0, lam=0.1)
P.update(dict(gate=0))
import json as _json, os as _os
P.update(_json.loads(_os.environ.get("WORLD_P", "{}")))


def lap(u):
    return np.roll(u, 1, 0) + np.roll(u, -1, 0) + np.roll(u, 1, 1) + np.roll(u, -1, 1) - 4 * u


def mob_div(u, g, D):
    out = np.zeros_like(u)
    for ax in (0, 1):
        gf = 0.5 * (g + np.roll(g, -1, ax))
        flux = D * gf * (np.roll(u, -1, ax) - u)
        out += flux - np.roll(flux, 1, ax)
    return out


def upwind_div(rho, vy, vx):
    """div(rho v), first-order upwind on faces (conservative)."""
    out = np.zeros_like(rho)
    for v, ax in ((vy, 0), (vx, 1)):
        vf = 0.5 * (v + np.roll(v, -1, ax))
        flux = vf * np.where(vf > 0, rho, np.roll(rho, -1, ax))
        out += flux - np.roll(flux, 1, ax)
    return out


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    S, K, L, phi = np.ones((H, W)), np.zeros((H, W)), np.zeros((H, W)), np.zeros((H, W))
    yy, xx = np.mgrid[0:H, 0:W]
    if P["IC"] == "spots":
        for _ in range(P["nspots"]):
            sc = P["scale"]  # resolution test: same layout, lengths x sc, diffusivities x sc^2
            y, x = rng.integers(0, int(H / sc)) * sc, rng.integers(0, int(W / sc)) * sc
            d2 = ((yy - y + H / 2) % H - H / 2) ** 2 + ((xx - x + W / 2) % W - W / 2) ** 2
            m = d2 <= 16 * sc * sc
            S[m], K[m], L[m] = 0.5, P["K0"], 0.5
            phi = np.maximum(phi, 0.5 * (1 - np.tanh((np.sqrt(d2) - P["R0"] * sc) / (1.5 * sc))))
    else:  # noise: smoothed random fields everywhere, no planted structure
        from scipy import ndimage
        n = ndimage.gaussian_filter(rng.standard_normal((H, W)), 3, mode="wrap")
        phi = np.clip(P["noise_mean"] + n / n.std() * P["noise_amp"], 0, 1)
        K = P["noise_K"] * rng.random((H, W))
        L = P["noise_KL"] * rng.random((H, W))
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
    lim = np.minimum(1.0, 0.5 * S / np.maximum(P["dt"] * (auto + prodL), 1e-12))
    auto, prodL = auto * lim, prodL * lim
    h = P["dt"]
    s2 = P["scale"] ** 2
    s["S"] = np.maximum(S + h * (s2 * P["DS"] * lap(S) - auto - prodL + P["F"] * (1 - S)), 0)
    s["K"] = np.maximum(K + h * (mob_div(K, g if P["gateK"] else np.ones_like(g), s2 * P["DK"] * (P["lam"] if not P["gate"] else 1.0)) + auto - kdec * K), 0)
    adv = 0.0
    if P["chi"]:
        w = 4 * phi * (1 - phi)
        vy = s2 * P["DL"] * P["chi"] * g * 0.5 * (np.roll(w, -1, 0) - np.roll(w, 1, 0))
        vx = s2 * P["DL"] * P["chi"] * g * 0.5 * (np.roll(w, -1, 1) - np.roll(w, 1, 1))
        adv = upwind_div(L, vy, vx)
    s["L"] = np.maximum(L + h * (mob_div(L, g, s2 * P["DL"] * (P["lam"] if not P["gate"] else 1.0)) - adv + prodL - P["dL"] * L), 0)
    if P["nophase"]:
        s["phi"] = np.ones_like(phi); return s
    s["phi"] = np.clip(phi + h * s2 * P["Dp"] * lap(phi) + h * P["r"] * phi * (1 - phi) * (phi - 0.5 + P["a"] * (L - P["th"])), 0, 1)
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
    """Honour labkit's mask (labkit v0.2 places it on a mature cell, core/rim/half): reset the
    masked pixels to the bath (S=1, catalyst = links = phi = 0)."""
    s["S"][mask] = 1
    for k in ("K", "L", "phi"):
        s[k][mask] = 0
    return s
