"""Autochemotactic spots that flee their own trail.

rho : cell density with volume filling (0..1)
a   : fast, short-lived attractant secreted by rho  -> self-aggregation (body)
h   : slow, long-lived repellent secreted by rho    -> self-repulsive trail (propulsion)

  d rho/dt = Dr lap rho - div( rho (1-rho) (chi_a grad a - chi_h grad h) )
  d a/dt   = Da lap a + rho - ka a
  d h/dt   = Dh lap h + beta rho - kh h

Hypothesis: the spot sits on top of its own accumulating repellent; any displacement
puts the old trail behind it and the gradient pushes it forward (symmetry breaking).
"""
import numpy as np

from labkit import ops

META = {
    "name": "kstrail",
    "family": "chemotaxis",
    "parent": None,
    "mutation": "Keller-Segel with volume filling + second, slow self-secreted repellent (trail)",
    "size": (128, 128),
    "steps_per_frame": 60,
    "dt": 0.05,
    "channels": ["rho", "a", "h"],
    "matter": [0],
    "smooth": 1.0,
}

P = {
    # lengths are ~2x the first screens (body radius ~6 px) so bodies are resolved and
    # headings are not pulled to the grid diagonals (see NOTEBOOK)
    "Dr": 1.2, "Da": 4.0, "ka": 0.1, "Dh": 0.2, "kh": 0.05, "beta": 1.0,
    "chi_a": 24.0, "chi_h": 4.8, "rho0": 0.05, "noise": 0.02, "dt": 0.05, "growth": 0.0,
}


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


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    rho = np.clip(P["rho0"] + P["noise"] * rng.standard_normal((H, W)), 0, 1)
    rho = ops.fft_conv(rho, ops.gauss_kernel(H, W, 1.0))
    L = ops.lap_symbol(H, W)
    dt = P["dt"]
    return {"rho": rho, "a": rho / P["ka"], "h": np.zeros((H, W)) + P["beta"] * rho.mean() / P["kh"],
            "La": 1.0 / (1 - dt * (P["Da"] * L - P["ka"])), "Lh": 1.0 / (1 - dt * (P["Dh"] * L - P["kh"])),
            "shape": (H, W), "p": dict(P)}


def step(s):
    p, dt = s["p"], s["p"]["dt"]
    rho, a, h = s["rho"], s["a"], s["h"]
    ay, ax = ops.grad(a)
    hy, hx = ops.grad(h)
    vy = p["chi_a"] * ay - p["chi_h"] * hy
    vx = p["chi_a"] * ax - p["chi_h"] * hx
    rho = rho + dt * (p["Dr"] * ops.laplacian(rho) - vf_flux_div(rho, vy, vx)
                      + p["growth"] * rho * (1 - rho))
    rho = np.clip(rho, 0, 1)
    s["a"] = ops.irfft2(ops.rfft2(a + dt * rho) * s["La"], s["shape"])
    s["h"] = ops.irfft2(ops.rfft2(h + dt * p["beta"] * rho) * s["Lh"], s["shape"])
    s["rho"] = rho
    return s


def fields(s):
    return np.stack([s["rho"], s["a"], s["h"]])


def damage(s, mask):
    s["rho"][mask] = 0
    return s
