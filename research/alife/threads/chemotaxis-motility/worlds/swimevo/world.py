"""Heritable swimmers: two alleles carried inside dividing chemotactic swimmers
(fork of swimfission + the droplet-confined allele idea of active-droplets ad5-evolve).

rho = A + B. Both alleles move with the same flux (the face flux of the total density is split by the
upwind allele fraction) and diffuse identically, so they are confined to and carried by the body.
Growth is cooperative in each allele's OWN density, so the majority allele purifies its body:
  grow_k = g_k n k^3/(rh^2 + k^2),   g_A = g,  g_B = g (1 + s)
Death kd h k for both. Mutation: rare discrete events (rate m per unit time, after t_on) swap A <-> B inside
a disk of radius Rm centred on a random body pixel, which is symmetric, so with s = 0 the alleles are neutral.
Division (swimfission mechanism) partitions the body's allele content between the daughters.
"""
import json
import os

import numpy as np

from labkit import ops

META = {
    "name": "swimevo",
    "family": "chemotaxis",
    "parent": "swimfission + active-droplets/ad5-evolve (confined alleles)",
    "mutation": "split rho into two heritable alleles with own-density cooperative growth (body purification), symmetric patch mutations, allele B grows (1+s) faster",
    "size": (160, 160),
    "steps_per_frame": 120,
    "dt": 0.05,
    "channels": ["A", "B", "h", "n"],
    "matter": [0, 1],
    "smooth": 1.0,
}

P = {
    # lengths are ~2x the first screens (body radius ~6 px) so bodies are resolved and
    # headings are not pulled to the grid diagonals (see NOTEBOOK)
    "Dr": 1.2, "Da": 2.0, "ka": 0.1, "Dh": 0.2, "kh": 0.05, "beta": 1.0,
    "chi_a": 24.0, "chi_h": 4.8, "rho0": 0.05, "noise": 0.02, "dt": 0.05, "g": 0.1, "rh": 0.3, "kd": 0.005, "t_on": 150.0, "r": 0.06, "c": 2.0, "Dn": 0.5, "chi_n": 0.0, "s": 0.3, "m": 0.02, "Rm": 4.0,
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
    rho = np.clip(P["rho0"] + P["noise"] * rng.standard_normal((H, W)), 0, 1)
    rho = ops.fft_conv(rho, ops.gauss_kernel(H, W, 1.0))
    L = ops.lap_symbol(H, W)
    dt = P["dt"]
    return {"rho": rho, "a": rho / P["ka"], "h": np.zeros((H, W)) + P["beta"] * rho.mean() / P["kh"],
            "La": 1.0 / (1 - dt * (P["Da"] * L - P["ka"])), "Lh": 1.0 / (1 - dt * (P["Dh"] * L - P["kh"])),
            "shape": (H, W), "p": dict(P), "n": np.ones((H, W)),
            "Ln": 1.0 / (1 - dt * (P["Dn"] * L - P["r"])),
            "A": rho.copy(), "B": np.zeros((H, W)), "rng": np.random.default_rng(seed + 1000), "mutations": []}


def step(s):
    p, dt = s["p"], s["p"]["dt"]
    rho, a, h = s["rho"], s["a"], s["h"]
    ay, ax = ops.grad(a)
    hy, hx = ops.grad(h)
    vy = p["chi_a"] * ay - p["chi_h"] * hy
    vx = p["chi_a"] * ax - p["chi_h"] * hx
    s["t"] = s.get("t", 0.0) + dt
    n = s["n"]
    ny, nx = ops.grad(n)
    vy = vy + p["chi_n"] * ny
    vx = vx + p["chi_n"] * nx
    A, B = s["A"], s["B"]
    rho = A + B
    gA = gB = 0.0
    if s["t"] >= p["t_on"]:
        gA = p["g"] * n * A ** 3 / (p["rh"] ** 2 + A ** 2)
        gB = p["g"] * (1 + p["s"]) * n * B ** 3 / (p["rh"] ** 2 + B ** 2)
    grow = gA + gB
    s["n"] = np.clip(ops.irfft2(ops.rfft2(n + dt * (p["r"] - p["c"] * grow)) * s["Ln"], s["shape"]), 0, None)
    faces = vf_face_fluxes(rho, vy, vx)
    fB = np.where(rho > 1e-9, B / np.maximum(rho, 1e-9), 0.0)
    divB = allele_flux_div(rho, fB, faces)
    divT = sum(fl - np.roll(fl, 1, ax) for ax, fl, _ in faces)
    kd = p["kd"] * h if s["t"] >= p["t_on"] else 0.0
    B = B + dt * (p["Dr"] * ops.laplacian(B) - divB + gB - kd * B)
    A = A + dt * (p["Dr"] * ops.laplacian(A) - (divT - divB) + gA - kd * A)
    A, B = np.clip(A, 0, None), np.clip(B, 0, None)
    tot = A + B
    over = np.where(tot > 1, 1 / np.maximum(tot, 1e-9), 1.0)
    A, B = A * over, B * over
    # rare symmetric patch mutation inside a body
    if s["t"] >= p["t_on"] and s["rng"].random() < p["m"] * dt:
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
    s["A"], s["B"] = A, B
    rho = A + B
    s["a"] = ops.irfft2(ops.rfft2(a + dt * rho) * s["La"], s["shape"])
    s["h"] = ops.irfft2(ops.rfft2(h + dt * p["beta"] * rho) * s["Lh"], s["shape"])
    s["rho"] = rho
    return s


def fields(s):
    return np.stack([s["A"], s["B"], s["h"], s["n"]])


def damage(s, mask):
    s["A"][mask] = 0
    s["B"][mask] = 0
    return s
