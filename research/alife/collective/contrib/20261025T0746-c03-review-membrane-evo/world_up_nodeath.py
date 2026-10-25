"""Membrane evo (committee r2 arm E): phase_membrane cells with two catalyst kinds that differ ONLY
in link yield (b2 vs b), sealed against horizontal transfer, under random turnover.

- Channel closed: catalyst face mobility D min(g_i, g_j) with g = [phi > 1/2] (zero flux on every
  boundary face), autocatalysis only where phi > 1/2, and catalyst decays fast (d_out) where
  phi < 1/2, so stranded catalyst cannot seed a neighbour.
- c2 = c1: K2 differs only in b2.
- Events from a state-independent RNG (identical across arms with the same seed): each step
  draw (u, y, x) for a whole-cell kind flip (prob p_flip: the cell under (y, x), if any, swaps
  K <-> K2, both directions), (u, y, x) for a whole-cell neutral-tag mutation (tag +- delta),
  and (u, y, x) for a disk death (prob p_death, radius r_death: reset to bath).
- The neutral tag is carried as Qt = tag (K + K2), moving and growing with the catalyst.
Event log in s["events"]: (t, type, y, x, detail).
"""
import numpy as np

META = {
    "name": "membrane-evo-up",
    "family": "autopoiesis",
    "parent": "threads/autopoiesis/worlds/membrane_evo (identical-event twin)",
    "mutation": "K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 1.0,
    "channels": ["K1", "K2", "L link", "membrane (wall)"],
    "matter": None,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(DS=0.2, DK=0.1, DL=0.1, Dp=0.1, r=0.2, a=4.0, th=0.15, F=0.006, k=0.0649, b=0.065, dL=0.02,
         gate=1, gateK=1, nophase=0, scale=1, noise_amp=0.2, noise_mean=0.0, noise_KL=0.1, noise_K=0.6, dt=1.0, K0=0.5, kin="logistic", c=0.2, dK=0.02, nspots=4, R0=6, IC="noise", chi=2.0, c2=0.2, b2=0.0845, d_out=0.2, p_flip=0.0005, p_tag=0.0005, delta=0.3, p_death=0.0, r_death=14, t_on=8000)


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
    return {"S": S, "K": K, "K2": np.zeros((H, W)), "L": L, "phi": phi, "Qt": np.ones((H, W)) * K, "ev": np.random.default_rng(seed + 777), "events": [], "t": 0}


def gate_div(u, g, D):
    out = np.zeros_like(u)
    for ax in (0, 1):
        gf = np.minimum(g, np.roll(g, -1, ax))  # min face mean: zero flux on every boundary face
        flux = D * gf * (np.roll(u, -1, ax) - u)
        out += flux - np.roll(flux, 1, ax)
    return out


def body_at(phi, y, x):
    from scipy import ndimage
    if phi[y, x] <= 0.5:
        return None
    lab, n = ndimage.label(phi > 0.5)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for u, v in set(zip(a.tolist(), b.tolist())):
            if u and v and u != v:
                lab[lab == v] = u
    cell = lab == lab[y, x]
    return ndimage.binary_dilation(cell, iterations=2) & (phi > 0.05)  # include the wall


def step(s):
    S, K, K2, L, phi = s["S"], s["K"], s["K2"], s["L"], s["phi"]
    g = phi * phi
    inside = (phi > 0.5).astype(float)
    free = 1 - K - K2
    auto1 = P["c"] * S * K * free * inside
    auto2 = P["c2"] * S * K2 * free * inside
    prodL = (P["b"] * K + P["b2"] * K2) * S
    lim = np.minimum(1.0, 0.5 * S / np.maximum(P["dt"] * (auto1 + auto2 + prodL), 1e-12))
    auto1, auto2, prodL = auto1 * lim, auto2 * lim, prodL * lim
    h = P["dt"]
    dec = P["dK"] + P["d_out"] * (1 - inside)
    Kt = K + K2
    rel = (auto1 + auto2) / np.maximum(Kt, 1e-9)
    s["S"] = np.maximum(S + h * (P["DS"] * lap(S) - auto1 - auto2 - prodL + P["F"] * (1 - S)), 0)
    s["K"] = np.maximum(K + h * (gate_div(K, inside, P["DK"]) + auto1 - dec * K), 0)
    s["K2"] = np.maximum(K2 + h * (gate_div(K2, inside, P["DK"]) + auto2 - dec * K2), 0)
    s["Qt"] = np.maximum(s["Qt"] + h * (gate_div(s["Qt"], inside, P["DK"]) + rel * s["Qt"] - dec * s["Qt"]), 0)
    w = 4 * phi * (1 - phi)
    vy = P["DL"] * P["chi"] * g * 0.5 * (np.roll(w, -1, 0) - np.roll(w, 1, 0))
    vx = P["DL"] * P["chi"] * g * 0.5 * (np.roll(w, -1, 1) - np.roll(w, 1, 1))
    s["L"] = np.maximum(L + h * (mob_div(L, g, P["DL"]) - upwind_div(L, vy, vx) + prodL - P["dL"] * L), 0)
    s["phi"] = np.clip(phi + h * P["Dp"] * lap(phi) + h * P["r"] * phi * (1 - phi) * (phi - 0.5 + P["a"] * (L - P["th"])), 0, 1)
    # ---- state-independent events: always draw the same numbers
    s["t"] += 1
    H, W = phi.shape
    ev = s["ev"]
    uf, yf, xf = ev.random(), ev.integers(H), ev.integers(W)
    ut, yt, xt, st = ev.random(), ev.integers(H), ev.integers(W), ev.random()
    ud, yd, xd = ev.random(), ev.integers(H), ev.integers(W)
    if s["t"] >= P["t_on"]:
        ph = s["phi"]
        if uf < P["p_flip"]:
            m = body_at(ph, yf, xf)
            if m is not None:
                k1, k2 = s["K"][m].sum(), s["K2"][m].sum()
                s["K"][m], s["K2"][m] = s["K2"][m].copy(), s["K"][m].copy()
                s["events"].append((s["t"], "flip", int(yf), int(xf), "K1->K2" if k1 >= k2 else "K2->K1"))
        if ut < P["p_tag"]:
            m = body_at(ph, yt, xt)
            if m is not None:
                tag = s["Qt"][m] / np.maximum(s["K"][m] + s["K2"][m], 1e-9)
                s["Qt"][m] = (s["K"][m] + s["K2"][m]) * (tag + (P["delta"] if st < 0.5 else -P["delta"]))
                s["events"].append((s["t"], "tag", int(yt), int(xt), ""))
        if ud < P["p_death"]:
            yy = (np.arange(H)[:, None] - yd + H // 2) % H - H // 2
            xx = (np.arange(W)[None, :] - xd + W // 2) % W - W // 2
            m = yy ** 2 + xx ** 2 <= P["r_death"] ** 2
            s["S"][m] = 1
            for k_ in ("K", "K2", "Qt", "L", "phi"):
                s[k_][m] = 0
            s["events"].append((s["t"], "death", int(yd), int(xd), ""))
    return s


def fields(s):
    phi = s["phi"]
    return np.stack([s["K"], s["K2"], s["L"], 4 * phi * (1 - phi)]).astype(np.float32)


def matter(F):
    # an individual = the inside phase; recover phi >= 1/2 region from the channels
    return (F[3] + 2 * (F[2] > 0.02)).astype(np.float32) if False else (F[0] + F[1] + F[2] + F[3]).astype(np.float32)


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
    for k in ("K", "K2", "L", "phi"):
        s[k][hole] = 0
    return s
