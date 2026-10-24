"""Phase kinds: phase protocell with two heritable catalyst kinds and in-run mutation.

K1 (cooperative) and K2 (selfish) share substrate, links and the phase. Both grow logistically
on the shared capacity 1 - K1 - K2 inside the phase; K2 replicates faster (c2 > c1) but makes
fewer links (b2 < b1). Mutation: each step, with probability p_mut, one random site with
K1 > 0.05 has a 2-px disk of K1 converted to K2 (a stochastic point event of the world's own
dynamics, not an external template). Within a cell K2 outcompetes K1; a cell full of K2 makes
too few links to hold its phase and dies. Kinds breed true through division.

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
    "name": "phase-kinds-parasite",
    "family": "autopoiesis",
    "parent": "threads/autopoiesis/worlds/phase_kinds",
    "mutation": "mutant kind K2 is selfish: faster (c2=0.3 vs 0.2) but makes no links (b2=0)",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 1.0,
    "channels": ["S", "K1 (cooperative)", "K2 (selfish)", "L link", "membrane (wall)"],
    "matter": None,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(DS=0.2, DK=0.1, DL=0.1, Dp=0.1, r=0.2, a=4.0, th=0.15, F=0.006, k=0.0649, b=0.05, dL=0.02,
         gate=1, gateK=1, nophase=0, noise_amp=0.3, noise_mean=0.5, noise_KL=0.5, dt=1.0, K0=0.5, kin="logistic", c=0.2, dK=0.02, nspots=4, R0=6, IC="spots", c2=0.3, b2=0.0, p_mut=0.0003, mut_r=2)


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
    else:  # noise: smoothed random fields everywhere, no planted structure
        from scipy import ndimage
        n = ndimage.gaussian_filter(rng.standard_normal((H, W)), 3, mode="wrap")
        phi = np.clip(P["noise_mean"] + n / n.std() * P["noise_amp"], 0, 1)
        K = P["noise_KL"] * rng.random((H, W))
        L = P["noise_KL"] * rng.random((H, W))
    K += 0.01 * rng.random((H, W)) * phi
    return {"S": S, "K": K, "K2": np.zeros((H, W)), "L": L, "phi": phi, "rng": np.random.default_rng(seed + 1000), "nmut": 0}


def step(s):
    S, K, K2, L, phi = s["S"], s["K"], s["K2"], s["L"], s["phi"]
    g = phi * phi
    free = 1 - K - K2
    auto1 = P["c"] * S * K * free * phi
    auto2 = P["c2"] * S * K2 * free * phi
    prodL = (P["b"] * K + P["b2"] * K2) * S
    lim = np.minimum(1.0, 0.5 * S / np.maximum(P["dt"] * (auto1 + auto2 + prodL), 1e-12))
    auto1, auto2, prodL = auto1 * lim, auto2 * lim, prodL * lim
    h = P["dt"]
    s["S"] = np.maximum(S + h * (P["DS"] * lap(S) - auto1 - auto2 - prodL + P["F"] * (1 - S)), 0)
    s["K"] = np.maximum(K + h * (mob_div(K, g, P["DK"]) + auto1 - P["dK"] * K), 0)
    s["K2"] = np.maximum(K2 + h * (mob_div(K2, g, P["DK"]) + auto2 - P["dK"] * K2), 0)
    s["L"] = np.maximum(L + h * (mob_div(L, g, P["DL"]) + prodL - P["dL"] * L), 0)
    s["phi"] = np.clip(phi + h * P["Dp"] * lap(phi) + h * P["r"] * phi * (1 - phi) * (phi - 0.5 + P["a"] * (L - P["th"])), 0, 1)
    rng = s["rng"]
    if P["p_mut"] > 0 and rng.random() < P["p_mut"]:
        idx = np.flatnonzero(s["K"] > 0.05)
        if len(idx):
            H, W = K.shape
            y, x = divmod(int(rng.choice(idx)), W)
            yy = (np.arange(H)[:, None] - y + H // 2) % H - H // 2
            xx = (np.arange(W)[None, :] - x + W // 2) % W - W // 2
            m = yy ** 2 + xx ** 2 <= P["mut_r"] ** 2
            s["K2"][m] += s["K"][m]
            s["K"][m] = 0
            s["nmut"] += 1
    return s


def fields(s):
    phi = s["phi"]
    return np.stack([s["S"], s["K"], s["K2"], s["L"], 4 * phi * (1 - phi)]).astype(np.float32)


def matter(F):
    # an individual = the inside phase; recover phi >= 1/2 region from the channels
    return (F[1] + F[2] + F[3] + F[4]).astype(np.float32)


def stats(s):
    phi = s["phi"]
    from scipy import ndimage
    lab, n = ndimage.label(phi > 0.5)
    k1 = ndimage.sum(s["K"], lab, np.arange(1, n + 1)); k2 = ndimage.sum(s["K2"], lab, np.arange(1, n + 1))
    return {"K1": round(float(s["K"].sum()), 1), "K2": round(float(s["K2"].sum()), 1), "cells": int(n),
            "cells_K1": int((k1 > k2).sum()), "cells_K2": int((k2 >= k1).sum()), "nmut": s["nmut"]}


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
    for k in ("K", "K2", "L", "phi"):
        s[k][hole] = 0
    return s
