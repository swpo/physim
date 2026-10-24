"""Phase trait: phase protocell whose catalyst carries a continuous heritable trait c.

Fields: S, K (catalyst), Q = c K (trait mass, moves and decays with K), L, phi. New catalyst
inherits the local trait (dQ = c * growth). Growth rate c; link output b(c) = b0 max(0, 1 -
beta (c - c_ref)): faster catalysts make fewer links (within-cell selection pushes c up, a cell
needs links to keep its wall, so between-cell selection pushes c down).
Mutation: with probability p_mut per step, one random site with K > 0.05 has its trait in a
2-px disk shifted by +-delta. Read-outs: K-weighted mean trait, per-cell traits.
"""
import numpy as np

META = {
    "name": "phase-trait-c20",
    "family": "autopoiesis",
    "parent": "threads/autopoiesis/worlds/phase_trait",
    "mutation": "same as phase_trait, ancestral trait c0 = 0.20 instead of 0.15 (convergence test)",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 1.0,
    "channels": ["S", "K catalyst", "trait c (0..0.6)", "L link", "membrane (wall)"],
    "matter": None,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(DS=0.2, DK=0.1, DL=0.1, Dp=0.1, r=0.2, a=4.0, th=0.15, F=0.006, k=0.0649, b=0.05, dL=0.02,
         gate=1, gateK=1, nophase=0, noise_amp=0.3, noise_mean=0.5, noise_KL=0.5, dt=1.0, K0=0.5, kin="logistic", c=0.2, dK=0.02, nspots=4, R0=6, IC="spots", c0=0.2, beta=3.0, c_ref=0.2, delta=0.1, p_mut=0.002, mut_r=5)


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
    return {"S": S, "K": K, "Q": P["c0"] * K, "L": L, "phi": phi, "rng": np.random.default_rng(seed + 1000), "nmut": 0}


def trait(s):
    return np.clip(s["Q"] / np.maximum(s["K"], 1e-6), 0, 1)


def step(s):
    S, K, Q, L, phi = s["S"], s["K"], s["Q"], s["L"], s["phi"]
    g = phi * phi
    c = trait(s)
    auto = c * S * K * (1 - K) * phi
    prodL = P["b"] * np.maximum(0, 1 - P["beta"] * (c - P["c_ref"])) * K * S
    lim = np.minimum(1.0, 0.5 * S / np.maximum(P["dt"] * (auto + prodL), 1e-12))
    auto, prodL = auto * lim, prodL * lim
    h = P["dt"]
    s["S"] = np.maximum(S + h * (P["DS"] * lap(S) - auto - prodL + P["F"] * (1 - S)), 0)
    s["K"] = np.maximum(K + h * (mob_div(K, g, P["DK"]) + auto - P["dK"] * K), 0)
    s["Q"] = np.maximum(Q + h * (mob_div(Q, g, P["DK"]) + c * auto - P["dK"] * Q), 0)
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
            cm = np.clip(trait(s)[m] + P["delta"] * (1 if rng.random() < 0.5 else -1), 0, 1)
            s["Q"][m] = s["K"][m] * cm
            s["nmut"] += 1
    return s


def fields(s):
    phi = s["phi"]
    return np.stack([s["S"], s["K"], trait(s) * (s["K"] > 0.05) / 0.6, s["L"], 4 * phi * (1 - phi)]).astype(np.float32)


def matter(F):
    # an individual = the inside phase; recover phi >= 1/2 region from the channels
    return (F[1] + F[3] + F[4]).astype(np.float32)


def stats(s):
    from scipy import ndimage
    lab, n = ndimage.label(s["phi"] > 0.5)
    K = s["K"]
    cbar = float(s["Q"].sum() / max(K.sum(), 1e-9))
    if n:
        ck = ndimage.sum(s["Q"], lab, np.arange(1, n + 1)) / np.maximum(ndimage.sum(K, lab, np.arange(1, n + 1)), 1e-9)
        q = np.percentile(ck, [10, 50, 90]).round(3).tolist()
    else:
        q = []
    return {"cells": int(n), "c_mean": round(cbar, 3), "c_cells_10_50_90": q, "nmut": s["nmut"]}


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
    for k in ("K", "Q", "L", "phi"):
        s[k][hole] = 0
    return s
