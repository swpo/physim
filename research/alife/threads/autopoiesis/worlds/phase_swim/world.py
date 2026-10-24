"""Phase swim: phase protocell + rigid-droplet phoresis.

New relative to phase_protocell: every cell (component of phi > 0.05) drifts with velocity
v = mu * <grad S>_cell, the substrate gradient averaged over the cell, and phi, K, L are
advected by v (first-order upwind). A symmetric cell in its own depletion halo feels no net
gradient; motion can only come from symmetry breaking of its own wake (autophoretic
instability) or from neighbours' halos. No external gradient is imposed.

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
    "name": "phase-swim",
    "family": "autopoiesis",
    "parent": "threads/autopoiesis/worlds/phase_protocell",
    "mutation": "rigid-droplet phoresis: each cell advected with mu * cell-mean grad S; parent: membrane is an Allen-Cahn domain wall (always closed) instead of a polymerized field; the inside phase is tilted by catalyst-made links; K and L mobility ~ phi^2",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 1.0,
    "channels": ["S", "K catalyst", "L link", "membrane (wall)"],
    "matter": None,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(DS=0.2, DK=0.1, DL=0.1, Dp=0.1, r=0.2, a=4.0, th=0.15, F=0.006, k=0.0649, b=0.05, dL=0.02,
         gate=1, gateK=1, nophase=0, scale=1, noise_amp=0.3, noise_mean=0.5, noise_KL=0.5, noise_K=0.5, dt=1.0, K0=0.5, kin="logistic", c=0.2, dK=0.02, nspots=1, R0=6, IC="spots", mu=3.0, chi=0.0)


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
    s["K"] = np.maximum(K + h * (mob_div(K, g if P["gateK"] else np.ones_like(g), s2 * P["DK"]) + auto - kdec * K), 0)
    adv = 0.0
    if P["chi"]:  # optional link adsorption to the wall (from phase_membrane)
        w = 4 * phi * (1 - phi)
        avy = s2 * P["DL"] * P["chi"] * g * 0.5 * (np.roll(w, -1, 0) - np.roll(w, 1, 0))
        avx = s2 * P["DL"] * P["chi"] * g * 0.5 * (np.roll(w, -1, 1) - np.roll(w, 1, 1))
        adv = upwind_div(L, avy, avx)
    s["L"] = np.maximum(L + h * (mob_div(L, g, s2 * P["DL"]) - adv + prodL - P["dL"] * L), 0)
    if P["nophase"]:
        s["phi"] = np.ones_like(phi); return s
    s["phi"] = np.clip(phi + h * s2 * P["Dp"] * lap(phi) + h * P["r"] * phi * (1 - phi) * (phi - 0.5 + P["a"] * (L - P["th"])), 0, 1)
    if P["mu"]:
        from scipy import ndimage
        lab, n = ndimage.label(s["phi"] > 0.5)  # cell bodies
        for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):  # periodic: merge across edges
            for u, w in set(zip(a.tolist(), b.tolist())):
                if u and w and u != w:
                    lab[lab == w] = u
        halo = s["phi"] > 0.05
        for _ in range(3):  # grow each body's label into its own wall/halo (3 px), never across bodies
            grown = ndimage.grey_dilation(lab, size=3, mode="wrap")
            lab = np.where((lab == 0) & halo, grown, lab)
        if n:
            gy = 0.5 * (np.roll(S, -1, 0) - np.roll(S, 1, 0))
            gx = 0.5 * (np.roll(S, -1, 1) - np.roll(S, 1, 1))
            idx = np.arange(1, n + 1)
            my = np.concatenate([[0.0], ndimage.mean(gy, lab, idx)])
            mx = np.concatenate([[0.0], ndimage.mean(gx, lab, idx)])
            vy = np.clip(P["mu"] * my[lab], -0.4, 0.4)
            vx = np.clip(P["mu"] * mx[lab], -0.4, 0.4)
            for k in ("K", "L", "phi"):
                s[k] = s[k] - h * upwind_div(s[k], vy, vx)
            s["vmax"] = float(np.hypot(vy, vx).max())
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
    """labkit gives a disk at the centroid of the largest component (only the interior of a
    walled cell, and mis-placed for cells wrapping the periodic edge). We use it only to pick
    the cell: take the phi > 1/2 component under the mask, compute its periodic centre and
    equivalent radius R, and reset to bath (S=1, catalysts=L=phi=0) a disk of radius 0.8 R
    centred 0.8 R from the cell centre along +x. That cuts the wall and ~30% of the cell; the
    erased fraction is stored in s["damage_frac"]."""
    from scipy import ndimage
    phi = s["phi"]
    H, W = phi.shape
    lab, n = ndimage.label(phi > 0.5)
    for ax in (0, 1):  # merge labels across the periodic edges
        a, b = (lab[0], lab[-1]) if ax == 0 else (lab[:, 0], lab[:, -1])
        for u, v in zip(a, b):
            if u and v and u != v:
                lab[lab == v] = u
    ids = lab[mask & (lab > 0)]
    if len(ids) == 0:
        return s
    cell = lab == np.bincount(ids).argmax()
    ys, xs = np.nonzero(cell)
    cy = np.angle(np.exp(2j * np.pi * ys / H).mean()) * H / (2 * np.pi) % H
    cx = np.angle(np.exp(2j * np.pi * xs / W).mean()) * W / (2 * np.pi) % W
    R = np.sqrt(cell.sum() / np.pi)
    yy, xx = np.mgrid[0:H, 0:W]
    dy = (yy - cy + H / 2) % H - H / 2
    dx = (xx - cx - 0.8 * R + W / 2) % W - W / 2
    hole = dy ** 2 + dx ** 2 <= (0.8 * R) ** 2
    s["damage_frac"] = float((hole & cell).sum() / cell.sum())
    s["S"][hole] = 1
    for k in ("K", "L", "phi"):
        s[k][hole] = 0
    return s
