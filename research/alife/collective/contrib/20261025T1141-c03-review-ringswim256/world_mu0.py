"""ringswim-waste-256: world_claim.py of 20261025T0806-c07-ringswim-claim unchanged except a 256^2 domain (same dx, same physics).

ringswim-waste: ringswim with a self-made waste that leaves a cell only through its wall.

  dw/dt = Dw lap w + pw K - (dw_in phi + dw_out (1 - phi)) w ;   K decay += kd w K
Waste builds up in a cell's interior roughly as R^2, so large cells lose catalyst centrally and
pinch even when a swimming cell is well fed at its front. Without it (waste=0) swimmers grow
laterally and fuse into one band that wraps the domain.

ringswim: phase_membrane (walled cells with a chi-adsorbed link ring, from noise) plus a
phoretic self-propulsion drive (fork of phase_swimdiv, toward C:swim-divide).

drive = "label":  phase_swimdiv's rigid drift: every body (phi > 1/2, grown 3 px into its halo)
                  moves with v = mu <grad S>_body (nonlocal, uses labels).
drive = "kernel": label-free, local: v = mu G_sig * (g grad S) / (G_sig * g + eps), g = phi^2,
                  a Gaussian-weighted average of the substrate gradient felt by inside matter.
                  With sig of the order of a cell radius, v is nearly uniform across a cell, so
                  the wall is translated rather than stretched (phase_trail's local divergent
                  flow tore the wall).
phi, K, L are advected by v with a conservative MUSCL (van Leer) face flux; |v| <= vmax.
Everything else is phase_membrane unchanged (parent docstring below).
Phase membrane: phase protocell whose links adsorb to the wall.

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
    "name": "ringswim-waste-256",
    "family": "autopoiesis",
    "parent": "threads/autopoiesis/worlds/phase_membrane + phase_swimdiv",
    "mutation": "links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere",
    "size": (256, 256),
    "steps_per_frame": 50,
    "dt": 1.0,
    "channels": ["S", "K catalyst", "L link", "membrane (wall)"],
    "matter": None,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(DS=0.2, DK=0.1, DL=0.1, Dp=0.1, r=0.2, a=4.0, th=0.15, F=0.006, k=0.0649, b=0.05, dL=0.02,
         gate=1, gateK=1, nophase=0, scale=1, noise_amp=0.2, noise_mean=0.0, noise_KL=0.1, noise_K=0.6, dt=1.0, K0=0.5, kin="logistic", c=0.2, dK=0.02, nspots=4, R0=6, IC="noise", chi=2.0,
         drive="label", mu=0.0, sig=6.0, vmax=0.4,
         waste=1, Dw=0.2, pw=0.01, dw_in=0.0005, dw_out=0.2, kd=0.03)
import json as _json, os as _os
P.update(_json.loads(_os.environ.get("WORLD_P", "{}")))  # screening override only


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


def _faces(u, ax):
    up, um = np.roll(u, -1, ax), np.roll(u, 1, ax)
    d1, d2 = u - um, up - u
    slope = np.where(d1 * d2 > 0, 2 * d1 * d2 / (d1 + d2 + 1e-300), 0.0)
    return u + 0.5 * slope, np.roll(u - 0.5 * slope, -1, ax)


def muscl_div(u, vy, vx):
    """div(u v), conservative MUSCL face flux (van Leer limiter)."""
    out = np.zeros_like(u)
    for v, ax in ((vy, 0), (vx, 1)):
        vf = 0.5 * (v + np.roll(v, -1, ax))
        Lf, Rf = _faces(u, ax)
        flux = vf * np.where(vf > 0, Lf, Rf)
        out += flux - np.roll(flux, 1, ax)
    return out


def _gauss_hat(H, W, sig):
    ky = np.fft.fftfreq(H)[:, None] * 2 * np.pi
    kx = np.fft.fftfreq(W)[None, :] * 2 * np.pi
    return np.exp(-0.5 * sig * sig * (ky ** 2 + kx ** 2))


def drive_velocity(s, S, phi):
    gy = 0.5 * (np.roll(S, -1, 0) - np.roll(S, 1, 0))
    gx = 0.5 * (np.roll(S, -1, 1) - np.roll(S, 1, 1))
    if P["drive"] == "kernel":
        H, W = phi.shape
        if "Ghat" not in s:
            s["Ghat"] = _gauss_hat(H, W, P["sig"])
        g = phi * phi
        sm = lambda f: np.real(np.fft.ifft2(np.fft.fft2(f) * s["Ghat"]))
        den = sm(g) + 1e-3
        vy, vx = P["mu"] * sm(g * gy) / den, P["mu"] * sm(g * gx) / den
    else:
        from scipy import ndimage
        lab, n = ndimage.label(phi > 0.5)
        for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
            for u, w in set(zip(a.tolist(), b.tolist())):
                if u and w and u != w:
                    lab[lab == w] = u
        halo = phi > 0.05
        for _ in range(3):
            grown = ndimage.grey_dilation(lab, size=3, mode="wrap")
            lab = np.where((lab == 0) & halo, grown, lab)
        idx = np.arange(1, n + 1)
        my = np.concatenate([[0.0], ndimage.mean(gy, lab, idx)]) if n else np.zeros(1)
        mx = np.concatenate([[0.0], ndimage.mean(gx, lab, idx)]) if n else np.zeros(1)
        vy, vx = P["mu"] * my[lab], P["mu"] * mx[lab]
    vm = P["vmax"]
    return np.clip(vy, -vm, vm), np.clip(vx, -vm, vm)


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
    return {"S": S, "K": K, "L": L, "phi": phi, "w": np.zeros((H, W))}


def step(s):
    S, K, L, phi = s["S"], s["K"], s["L"], s["phi"]
    g = phi * phi if P["gate"] else np.ones_like(phi)
    if P["kin"] == "gs":
        auto = S * K * K * phi  # the catalyst only works in the inside phase
        kdec = P["F"] + P["k"]
    else:  # logistic autocatalysis, saturating at K = 1
        auto = P["c"] * S * K * (1 - K) * phi
        kdec = P["dK"]
    if P["waste"]:  # self-made waste: leaves a cell only through the wall (fast decay outside)
        w = s["w"]
        s["w"] = np.maximum(w + P["dt"] * (P["Dw"] * lap(w) + P["pw"] * K - (P["dw_in"] * phi + P["dw_out"] * (1 - phi)) * w), 0)
        kdec = kdec + P["kd"] * w
    prodL = P["b"] * K * S
    lim = np.minimum(1.0, 0.5 * S / np.maximum(P["dt"] * (auto + prodL), 1e-12))
    auto, prodL = auto * lim, prodL * lim
    h = P["dt"]
    s2 = P["scale"] ** 2
    s["S"] = np.maximum(S + h * (s2 * P["DS"] * lap(S) - auto - prodL + P["F"] * (1 - S)), 0)
    s["K"] = np.maximum(K + h * (mob_div(K, g if P["gateK"] else np.ones_like(g), s2 * P["DK"]) + auto - kdec * K), 0)
    adv = 0.0
    if P["chi"]:
        w = 4 * phi * (1 - phi)
        vy = s2 * P["DL"] * P["chi"] * g * 0.5 * (np.roll(w, -1, 0) - np.roll(w, 1, 0))
        vx = s2 * P["DL"] * P["chi"] * g * 0.5 * (np.roll(w, -1, 1) - np.roll(w, 1, 1))
        adv = upwind_div(L, vy, vx)
    s["L"] = np.maximum(L + h * (mob_div(L, g, s2 * P["DL"]) - adv + prodL - P["dL"] * L), 0)
    if P["nophase"]:
        s["phi"] = np.ones_like(phi); return s
    s["phi"] = np.clip(phi + h * s2 * P["Dp"] * lap(phi) + h * P["r"] * phi * (1 - phi) * (phi - 0.5 + P["a"] * (L - P["th"])), 0, 1)
    if P["mu"]:
        vy, vx = drive_velocity(s, s["S"], s["phi"])
        for k in ("K", "L", "phi"):
            s[k] = np.maximum(s[k] - h * muscl_div(s[k], vy, vx), 0)
        s["phi"] = np.minimum(s["phi"], 1)
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
