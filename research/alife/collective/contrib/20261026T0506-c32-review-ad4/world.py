"""Protocells: fuel-fed dividing droplets with heritable catalysts and a self-made membrane.

Merge of ad2-catalysts (heredity) and ad3-membrane (amphiphile shell).
Fields: droplet material phi (Cahn-Hilliard, slow mobility), fuel u, catalysts a and b
(droplet-confined, replicating, cross-inhibiting so each droplet is pure a or pure b),
amphiphile psi (made by the same catalysed reaction, drawn to |grad phi|^2).

    prod  = u c^2 (ka a + kb b),       c = (1 + phi)/2
    dphi  = M lap(phi^3 - phi - kappa lap phi) + prod - kd c
    du    = Du lap u + F (1 - u) - prod
    da    = Dc lap a + r c a (1 - a - beta b) - g (1 - c) a        (b symmetric)
    dpsi  = Dp div(grad psi - chi psi grad|grad phi|^2) + kp prod - gp psi

Kind A (ka) and kind B (kb) differ only in catalytic rate. Seeds: alternating kinds.
"""
import numpy as np
from labkit import ops

META = {
    "name": "ad4-protocell",
    "family": "phase-field",
    "parent": "ad2-catalysts + ad3-membrane",
    "mutation": "merge: catalyst-driven production (heredity) with amphiphile synthesis and interface binding (membrane)",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.5,
    "channels": ["phi (droplet material)", "u (fuel)", "a (catalyst A)", "b (catalyst B)", "psi (amphiphile)"],
    "matter": [0],
    "threshold": 0.0,
}

P = dict(M=0.03, kappa=1.0, ka=0.15, kb=0.12, kd=0.02, F=0.004, Du=2.0, Dc=0.05, r=0.05, beta=1.5, g=0.05,
         Dp=0.3, chi=8.0, kp=0.5, gp=0.01, dt=0.5, A=2.0, phi0=-0.95, noise=0.01, soup=0, seeds=6, r0=6.0)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    a, b = np.zeros((H, W)), np.zeros((H, W))
    for i in range(P["seeds"]):
        m = ops.disk(H, W, rng.integers(0, H), rng.integers(0, W), P["r0"])
        phi[m] = 0.9
        (a if i % 2 == 0 else b)[m] = 0.9
        (b if i % 2 == 0 else a)[m] = 0.0
    for i in range(P["soup"]):  # random blobs of random size/amplitude/kind: unstructured start
        m = ops.disk(H, W, rng.integers(0, H), rng.integers(0, W), rng.uniform(1.5, 6))
        phi[m] = rng.uniform(-0.6, 0.9)
        kind = rng.random() < 0.5
        (a if kind else b)[m] = rng.uniform(0.2, 0.9)
        (b if kind else a)[m] = 0.0
    ky, kx = ops.wavenumbers(H, W)
    k2 = kx ** 2 + ky ** 2
    dt, M = P["dt"], P["M"]
    return {"phi": phi, "u": np.ones((H, W)), "a": a, "b": b, "psi": np.zeros((H, W)), "k2": k2, "shape": (H, W),
            "den": 1 + dt * M * k2 * (P["A"] + P["kappa"] * k2), "denu": 1 + dt * P["Du"] * k2,
            "denc": 1 + dt * P["Dc"] * k2, "denp": 1 + dt * P["Dp"] * k2}


def step(s):
    phi, u, a, b, psi, k2, dt, M = s["phi"], s["u"], s["a"], s["b"], s["psi"], s["k2"], P["dt"], P["M"]
    sh = s["shape"]
    c = np.clip((1 + phi) / 2, 0, 1)
    prod = u * c ** 2 * (P["ka"] * a + P["kb"] * b)
    ph = (ops.rfft2(phi) - dt * M * k2 * ops.rfft2(phi ** 3 - phi - P["A"] * phi)
          + dt * ops.rfft2(prod - P["kd"] * c)) / s["den"]
    s["phi"] = ops.irfft2(ph, sh)
    s["u"] = ops.irfft2((ops.rfft2(u) + dt * ops.rfft2(P["F"] * (1 - u) - prod)) / s["denu"], sh)
    r, beta, g = P["r"], P["beta"], P["g"]
    ra = r * c * a * (1 - a - beta * b) - g * (1 - c) * a
    rb = r * c * b * (1 - b - beta * a) - g * (1 - c) * b
    s["a"] = np.clip(ops.irfft2((ops.rfft2(a) + dt * ops.rfft2(ra)) / s["denc"], sh), 0, None)
    s["b"] = np.clip(ops.irfft2((ops.rfft2(b) + dt * ops.rfft2(rb)) / s["denc"], sh), 0, None)
    gy, gx = ops.grad(phi)
    vy, vx = ops.grad(gy ** 2 + gx ** 2)
    rp = -P["Dp"] * P["chi"] * ops.upwind_flux_div(psi, vy, vx) + P["kp"] * prod - P["gp"] * psi
    s["psi"] = np.clip(ops.irfft2((ops.rfft2(psi) + dt * ops.rfft2(rp)) / s["denp"], sh), 0, None)
    return s


def fields(s):
    return np.stack([s["phi"], s["u"], s["a"], s["b"], s["psi"]])


def damage(s, mask):
    s["phi"][mask] = -1.0
    for k in ("a", "b", "psi"):
        s[k][mask] = 0.0
    return s
