"""Hunters: predator protocells that chase prey protocells by smell, fuse with them and take over.

Phase protocells (Allen-Cahn wall tilted by links, phi^2-gated mobility, fed substrate S).
K1 = prey catalyst: sessile, makes links (b) and an odour w (dw = Dw lap w + pw K1 - dw w).
K2 = predator catalyst: replicates faster (c2 > c1) but makes few links (b2 << b), so a cell
full of K2 cannot hold its wall for long; each cell is advected (rigid, per-cell label) up the
cell-mean odour gradient with speed mu2 * K2-fraction (chemotaxis forked from the
chemotaxis-motility thread's pursuit world, which binds predators to prey). When a predator cell
touches a prey cell, the phases merge; inside the fused cell K2 outgrows K1 using the prey's links,
the cell grows and divides by central starvation, and the daughters hunt again.
Kinds are planted at t=0 (prey and predator blobs); mutation is off by default.
"""
import numpy as np

META = {
    "name": "hunters",
    "family": "autopoiesis",
    "parent": "threads/autopoiesis/worlds/motile_kinds; pursuit chemotaxis from chemotaxis-motility/worlds/pursuit",
    "mutation": "predator kind (fast, link-poor) swims up a prey-made odour gradient and takes over prey cells by fusion",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 1.0,
    "channels": ["S", "K1 prey", "K2 predator", "L link", "membrane (wall)", "w odour"],
    "matter": None,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(DS=0.2, DK=0.1, DL=0.1, Dp=0.1, r=0.2, a=4.0, th=0.15, F=0.006, k=0.0649, b=0.05, dL=0.02,
         gate=1, gateK=1, nophase=0, noise_amp=0.3, noise_mean=0.5, noise_KL=0.5, dt=1.0, K0=0.5, kin="logistic", c=0.2, dK=0.02, nspots=4, R0=6, IC="spots", c2=0.3, b2=0.01, p_mut=0.0, mut_r=4, mu1=0.0, mu2=20.0, Dw=0.1, pw=0.01, dw=0.01, kd=0.0, kd_ramp=0, npred=3, vclip=0.15)


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
    K2 = np.zeros((H, W))
    for _ in range(P["npred"]):  # predator blobs: same phase/link seed, catalyst K2
        y, x = rng.integers(0, H), rng.integers(0, W)
        d2 = ((yy - y + H / 2) % H - H / 2) ** 2 + ((xx - x + W / 2) % W - W / 2) ** 2
        m = d2 <= 16
        S[m], K2[m], L[m] = 0.5, 0.5, 0.5
        phi = np.maximum(phi, 0.5 * (1 - np.tanh((np.sqrt(d2) - P["R0"]) / 1.5)))
    K += 0.01 * rng.random((H, W)) * phi
    return {"S": S, "K": K, "K2": K2, "L": L, "phi": phi, "w": np.zeros((H, W)), "rng": np.random.default_rng(seed + 1000), "nmut": 0}


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
    w = s["w"]
    s["t"] = s.get("t", 0) + 1
    kd = P["kd"] * (min(1.0, s["t"] / P["kd_ramp"]) if P["kd_ramp"] > 0 else 1.0)
    s["K"] = np.maximum(K + h * (mob_div(K, g, P["DK"]) + auto1 - (P["dK"] + kd * w) * K), 0)
    s["K2"] = np.maximum(K2 + h * (mob_div(K2, g, P["DK"]) + auto2 - (P["dK"] + kd * w) * K2), 0)
    s["w"] = w + h * (P["Dw"] * lap(w) + P["pw"] * K - P["dw"] * w)
    s["L"] = np.maximum(L + h * (mob_div(L, g, P["DL"]) + prodL - P["dL"] * L), 0)
    s["phi"] = np.clip(phi + h * P["Dp"] * lap(phi) + h * P["r"] * phi * (1 - phi) * (phi - 0.5 + P["a"] * (L - P["th"])), 0, 1)
    if P["mu1"] or P["mu2"]:
        from scipy import ndimage
        lab, n = ndimage.label(s["phi"] > 0.5)
        for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):  # periodic: merge across edges
            for u, v in set(zip(a.tolist(), b.tolist())):
                if u and v and u != v:
                    lab[lab == v] = u
        halo = s["phi"] > 0.05
        for _ in range(3):
            grown = ndimage.grey_dilation(lab, size=3, mode="wrap")
            lab = np.where((lab == 0) & halo, grown, lab)
        if n:
            Sx = s["w"]  # odour
            gy = 0.5 * (np.roll(Sx, -1, 0) - np.roll(Sx, 1, 0))
            gx = 0.5 * (np.roll(Sx, -1, 1) - np.roll(Sx, 1, 1))
            idx = np.arange(1, n + 1)
            k1 = ndimage.sum(s["K"], lab, idx); k2 = ndimage.sum(s["K2"], lab, idx)
            mu = (P["mu1"] * k1 + P["mu2"] * k2) / np.maximum(k1 + k2, 1e-9)
            my = np.concatenate([[0.0], mu * ndimage.mean(gy, lab, idx)])
            mx = np.concatenate([[0.0], mu * ndimage.mean(gx, lab, idx)])
            vy = np.clip(my[lab], -P["vclip"], P["vclip"]); vx = np.clip(mx[lab], -P["vclip"], P["vclip"])
            for k_ in ("K", "K2", "L", "phi"):
                s[k_] = s[k_] - h * upwind_div(s[k_], vy, vx)
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
    return np.stack([s["S"], s["K"], s["K2"], s["L"], 4 * phi * (1 - phi), s["w"]]).astype(np.float32)


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
