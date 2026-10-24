"""Chemotactic foragers: self-attracting cell clusters that eat a regrowing nutrient
and climb its gradient.

rho : cell density with volume filling (0..1)
a   : fast attractant secreted by rho (holds the body together)
n   : nutrient, regrows logistically toward 1, consumed by rho

  d rho/dt = Dr lap rho - div( rho (1-rho) (chi_a grad a + chi_n grad n) ) + g rho n (1-rho) - d rho
  d a/dt   = Da lap a + rho - ka a
  d n/dt   = Dn lap n + r n0 (1 - n) - c rho n

Hypothesis: a cluster eats the nutrient under itself, so the nutrient gradient always
points away from where it has been: the depletion zone is a self-made repulsive trail
(cf. kstrail) and also the cell's food, so motion, size and survival are coupled.
"""
import numpy as np

from labkit import ops

META = {
    "name": "forager",
    "family": "chemotaxis",
    "parent": "kstrail",
    "mutation": "replace the secreted repellent trail by a consumed, regrowing nutrient that is also food (growth/death)",
    "size": (128, 128),
    "steps_per_frame": 40,
    "dt": 0.05,
    "channels": ["rho", "a", "n"],
    "matter": [0],
    "smooth": 1.0,
}

P = {
    "Dr": 0.3, "Da": 1.0, "ka": 0.1, "Dn": 0.3, "r": 0.02, "c": 1.0,
    "chi_a": 3.0, "chi_n": 3.0, "g": 0.2, "m": 1.0, "rh": 0.3, "d": 0.05, "kp": 0.0, "rho0": 0.15, "noise": 0.05, "dt": 0.05,
}


def vf_flux_div(rho, vy, vx):
    """Conservative upwind divergence of rho (1-rho) v: face flux = v * rho_up * (1 - rho_down)."""
    out = np.zeros_like(rho)
    for v, ax in ((vy, -2), (vx, -1)):
        vf = 0.5 * (v + np.roll(v, -1, ax))
        nb = np.roll(rho, -1, ax)
        flux = np.where(vf > 0, vf * rho * (1 - nb), vf * nb * (1 - rho))
        out += flux - np.roll(flux, 1, ax)
    return out


def lap9(u):
    """Isotropic 9-point Laplacian (Patra-Karttunen weights)."""
    e = np.roll(u, 1, 0) + np.roll(u, -1, 0) + np.roll(u, 1, 1) + np.roll(u, -1, 1)
    c = (np.roll(np.roll(u, 1, 0), 1, 1) + np.roll(np.roll(u, 1, 0), -1, 1)
         + np.roll(np.roll(u, -1, 0), 1, 1) + np.roll(np.roll(u, -1, 0), -1, 1))
    return (4 * e + c - 20 * u) / 6


def grow(rho, n, p):
    """Cooperative (Allee) growth on nutrient: dilute cells cannot grow, dense bodies saturate."""
    r2 = rho ** p["m"]
    return p["g"] * n * rho * r2 / (p["rh"] ** p["m"] + r2)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    rho = np.clip(P["rho0"] + P["noise"] * rng.standard_normal((H, W)), 0, 1)
    rho = ops.fft_conv(rho, ops.gauss_kernel(H, W, 1.0))
    L = ops.lap_symbol(H, W)
    dt = P["dt"]
    return {"rho": rho, "a": rho / P["ka"], "n": np.ones((H, W)),
            "La": 1.0 / (1 - dt * (P["Da"] * L - P["ka"])), "Ln": 1.0 / (1 - dt * P["Dn"] * L),
            "shape": (H, W), "p": dict(P)}


def step(s):
    p, dt = s["p"], s["p"]["dt"]
    rho, a, n = s["rho"], s["a"], s["n"]
    ay, ax = ops.grad(a)
    ny, nx = ops.grad(n)
    vy = p["chi_a"] * ay + p["chi_n"] * ny
    vx = p["chi_a"] * ax + p["chi_n"] * nx
    if p["kp"] > 0:   # pressure instead of volume filling: isotropic, round bodies
        mot = lap9(p["Dr"] * rho + p["kp"] * rho ** 3) - ops.upwind_flux_div(rho, vy, vx)
    else:
        mot = p["Dr"] * ops.laplacian(rho) - vf_flux_div(rho, vy, vx)
    rho = rho + dt * (mot
                      + grow(rho, n, p) - p["d"] * rho)
    rho = np.clip(rho, 0, None if p["kp"] > 0 else 1)
    s["a"] = ops.irfft2(ops.rfft2(a + dt * rho) * s["La"], s["shape"])
    n = n + dt * (p["r"] * (1 - n) - p["c"] * rho * n)
    s["n"] = np.clip(ops.irfft2(ops.rfft2(n) * s["Ln"], s["shape"]), 0, None)
    s["rho"] = rho
    return s


def fields(s):
    return np.stack([s["rho"], s["a"], s["n"]])


def damage(s, mask):
    s["rho"][mask] = 0
    return s
