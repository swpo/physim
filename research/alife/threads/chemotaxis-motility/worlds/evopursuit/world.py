"""Heritable evasion under predation: prey swimmers carry an allele that makes their body flee harder,
at a growth cost (fork of ecology + swimevo alleles; predation-driven selection between kinds).

Prey = A + B (alleles confined to and carried by the body as in swimevo; own-density cooperative growth
purifies bodies; symmetric patch mutations A<->B at rate m). Prey bodies divide (short cohesion
range Da_p = 2, the swimfission mechanism). Predators q as in ecology (pursue the prey signal, eat on
contact, die from their own toxic trail).
Prey velocity:  chi_a grad a_p - chi_h grad h_p - chi_x (1 + e fB) grad a_q,   fB = local B fraction
B growth:  g (1 - cost) n B^3/(rh^2+B^2)   vs   g n A^3/(rh^2+A^2)
Prediction: with predators, B (better evaders) should spread despite the cost; without predators
(pred = 0) A should win; with e = cost = 0 the alleles are neutral.
"""
import json
import os

import numpy as np

from labkit import ops

META = {
    "name": "evopursuit",
    "family": "chemotaxis",
    "parent": "ecology + swimevo (alleles: active-droplets/ad5-evolve)",
    "mutation": "prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)",
    "size": (160, 160),
    "steps_per_frame": 240,
    "dt": 0.05,
    "channels": ["preyA", "preyB", "predator", "n"],
    "matter": [0, 1, 2],
    "smooth": 1.0,
}

P = {
    "Dr": 1.2, "Da_p": 2.0, "Da_q": 4.0, "ka": 0.1, "Dh": 0.2, "kh": 0.05, "beta": 1.0,
    "chi_a": 24.0, "chi_h": 4.8, "chi_x": 8.0, "chi_y": 8.0,
    "k": 0.1, "e_yield": 0.5, "g": 0.1, "rh": 0.3, "r": 0.06, "c": 2.0, "Dn": 0.5, "kd": 0.005,
    "e": 1.0, "cost": 0.15, "m": 0.02, "Rm": 4.0, "pred": 1.0,
    "t_on": 150.0, "rho0": 0.05, "qfrac": 0.5, "noise": 0.02, "dt": 0.05,
}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))  # screening override only; packs use the defaults above


def _faces(u, ax):
    """MUSCL (van Leer limited) left/right states at face i+1/2 along axis ax."""
    up, um = np.roll(u, -1, ax), np.roll(u, 1, ax)
    d1, d2 = u - um, up - u
    slope = np.where(d1 * d2 > 0, 2 * d1 * d2 / (d1 + d2 + 1e-300), 0.0)
    left = u + 0.5 * slope                         # state just left of face i+1/2
    right = np.roll(u - 0.5 * slope, -1, ax)       # state just right of face i+1/2
    return left, right


def vf_flux_div(rho, vy, vx):
    """Conservative divergence of rho (1-rho) v with face flux v * rho_up * (1 - rho_down).

    Second-order MUSCL reconstruction (van Leer limiter) to cut the anisotropic numerical
    diffusion of first-order upwinding, which made swimmers prefer diagonal headings.
    Volume filling (Painter & Hillen 2002) keeps 0 <= rho <= 1."""
    out = np.zeros_like(rho)
    for v, ax in ((vy, -2), (vx, -1)):
        vf = 0.5 * (v + np.roll(v, -1, ax))
        L, R = _faces(rho, ax)
        flux = np.where(vf > 0, vf * L * (1 - R), vf * R * (1 - L))
        out += flux - np.roll(flux, 1, ax)
    return out


def vf_face_fluxes(rho, vy, vx):
    """Face fluxes (per axis) of the volume-filling MUSCL scheme, plus the upwind side mask."""
    out = []
    for v, ax in ((vy, -2), (vx, -1)):
        vf = 0.5 * (v + np.roll(v, -1, ax))
        L, R = _faces(rho, ax)
        out.append((ax, np.where(vf > 0, vf * L * (1 - R), vf * R * (1 - L)), vf > 0))
    return out


def allele_flux_div(rho, frac, faces):
    """Divergence of the allele flux: total face flux times the upwind allele fraction."""
    out = np.zeros_like(rho)
    for ax, flux, pos in faces:
        fk = np.where(pos, frac, np.roll(frac, -1, ax))
        fl = flux * fk
        out += fl - np.roll(fl, 1, ax)
    return out


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    rho = np.stack([P["rho0"] + P["noise"] * rng.standard_normal((H, W)),
                    P["qfrac"] * P["rho0"] + P["noise"] * rng.standard_normal((H, W))])
    rho = np.clip(ops.fft_conv(rho, ops.gauss_kernel(H, W, 1.0)), 0, 1)
    rho[1] *= P["pred"]
    L = ops.lap_symbol(H, W)
    dt = P["dt"]
    La = np.stack([1.0 / (1 - dt * (P["Da_p"] * L - P["ka"])), 1.0 / (1 - dt * (P["Da_q"] * L - P["ka"]))])
    return {"A": rho[0].copy(), "B": np.zeros((H, W)), "q": rho[1].copy(),
            "a": rho / P["ka"], "h": P["beta"] * rho / P["kh"], "n": np.ones((H, W)),
            "La": La, "Lh": 1.0 / (1 - dt * (P["Dh"] * L - P["kh"])),
            "Ln": 1.0 / (1 - dt * (P["Dn"] * L - P["r"])), "shape": (H, W), "p": dict(P),
            "rng": np.random.default_rng(seed + 1000), "mutations": []}


def step(s):
    p, dt = s["p"], s["p"]["dt"]
    A, B, q, a, h, n = s["A"], s["B"], s["q"], s["a"], s["h"], s["n"]
    pr = A + B
    fB = np.where(pr > 1e-6, B / np.maximum(pr, 1e-6), 0.0)
    ay, ax = ops.grad(a)
    hy, hx = ops.grad(h)
    ev = p["chi_x"] * (1 + p["e"] * fB)
    vyp = p["chi_a"] * ay[0] - p["chi_h"] * hy[0] - ev * ay[1]
    vxp = p["chi_a"] * ax[0] - p["chi_h"] * hx[0] - ev * ax[1]
    vyq = p["chi_a"] * ay[1] - p["chi_h"] * hy[1] + p["chi_y"] * ay[0]
    vxq = p["chi_a"] * ax[1] - p["chi_h"] * hx[1] + p["chi_y"] * ax[0]
    s["t"] = s.get("t", 0.0) + dt
    on = s["t"] >= p["t_on"]
    gA = p["g"] * n * A ** 3 / (p["rh"] ** 2 + A ** 2) if on else 0.0
    gB = p["g"] * (1 - p["cost"]) * n * B ** 3 / (p["rh"] ** 2 + B ** 2) if on else 0.0
    kk = p["k"] if on else 0.0
    kd = p["kd"] if on else 0.0
    faces = vf_face_fluxes(pr, vyp, vxp)
    divB = allele_flux_div(pr, fB, faces)
    divT = sum(fl - np.roll(fl, 1, ax_) for ax_, fl, _ in faces)
    B = B + dt * (p["Dr"] * ops.laplacian(B) - divB + gB - kk * B * q - kd * h[0] * B)
    A = A + dt * (p["Dr"] * ops.laplacian(A) - (divT - divB) + gA - kk * A * q - kd * h[0] * A)
    q = q + dt * (p["Dr"] * ops.laplacian(q) - vf_flux_div(q, vyq, vxq) + p["e_yield"] * kk * pr * q - kd * h[1] * q)
    A, B, q = np.clip(A, 0, None), np.clip(B, 0, None), np.clip(q, 0, 1)
    tot = A + B
    over = np.where(tot > 1, 1 / np.maximum(tot, 1e-9), 1.0)
    A, B = A * over, B * over
    if on and s["rng"].random() < p["m"] * dt:
        w = np.where(tot > 0.35, tot, 0).ravel()
        if w.sum() > 0:
            k = s["rng"].choice(w.size, p=w / w.sum())
            H, W = s["shape"]
            cy, cx = divmod(k, W)
            yy = np.minimum(np.abs(np.arange(H) - cy), H - np.abs(np.arange(H) - cy))[:, None]
            xx = np.minimum(np.abs(np.arange(W) - cx), W - np.abs(np.arange(W) - cx))[None, :]
            d = yy ** 2 + xx ** 2 <= p["Rm"] ** 2
            A[d], B[d] = B[d].copy(), A[d].copy()
            s["mutations"].append((round(s["t"], 2), int(cy), int(cx)))
    rho = np.stack([A + B, q])
    s["a"] = ops.irfft2(ops.rfft2(a + dt * rho) * s["La"], s["shape"])
    s["h"] = ops.irfft2(ops.rfft2(h + dt * p["beta"] * rho) * s["Lh"], s["shape"])
    food = gA + gB
    s["n"] = np.clip(ops.irfft2(ops.rfft2(n + dt * (p["r"] - p["c"] * food)) * s["Ln"], s["shape"]), 0, None)
    s["A"], s["B"], s["q"] = A, B, q
    return s


def fields(s):
    return np.stack([s["A"], s["B"], s["q"], s["n"]])


def damage(s, mask):
    for k in ("A", "B", "q"):
        s[k][mask] = 0
    return s
