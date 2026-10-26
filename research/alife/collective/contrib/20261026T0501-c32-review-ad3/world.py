"""Self-made membranes: fuel-fed dividing droplets (ad1-fuel) that synthesize an amphiphile.

Droplet material phi (Cahn-Hilliard, slow mobility M), fuel u, amphiphile psi.
The amphiphile is made wherever droplet material is made (a by-product of the same
fuel-consuming reaction), decays slowly, and is attracted to interfaces by the
free-energy term -s_a psi |grad phi|^2 (standard ternary-surfactant coupling), so it
collects in a thin shell at the droplet boundary. Its back-reaction lowers the local
interfacial stiffness (kappa_eff = kappa - 2 s psi), i.e. lowers surface tension.

    prod  = k u c^2,  c = (1 + phi)/2
    dphi  = M lap(phi^3 - phi - kappa lap phi + 2 s div(psi grad phi)) + prod - kd c
    du    = Du lap u + F (1 - u) - prod
    dpsi  = Dp div(grad psi - chi psi grad|grad phi|^2) + kp prod - gp psi
"""
import numpy as np
from labkit import ops

META = {
    "name": "ad3-membrane",
    "family": "phase-field",
    "parent": "ad1-fuel",
    "mutation": "fuel reaction also makes an amphiphile psi that is drawn to |grad phi|^2 (ternary surfactant coupling) and lowers interfacial stiffness",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.5,
    "channels": ["phi (droplet material)", "u (fuel)", "psi (amphiphile)"],
    "matter": [0],
    "threshold": 0.0,
}

P = dict(M=0.03, kappa=1.0, k=0.1, kd=0.02, F=0.004, Du=2.0, Dp=0.3, chi=8.0, kp=0.5, gp=0.01, s=0.0,
         dt=0.5, A=2.0, phi0=-0.95, noise=0.01, soup=0, seeds=2, r0=6.0)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    for _ in range(P["seeds"]):
        m = ops.disk(H, W, rng.integers(0, H), rng.integers(0, W), P["r0"])
        phi[m] = 0.9
    for _ in range(P["soup"]):  # random blobs of random size/amplitude: unstructured start
        m = ops.disk(H, W, rng.integers(0, H), rng.integers(0, W), rng.uniform(1.5, 6))
        phi[m] = rng.uniform(-0.6, 0.9)
    ky, kx = ops.wavenumbers(H, W)
    k2 = kx ** 2 + ky ** 2
    dt, M = P["dt"], P["M"]
    return {"phi": phi, "u": np.ones((H, W)), "psi": np.zeros((H, W)), "k2": k2, "shape": (H, W),
            "den": 1 + dt * M * k2 * (P["A"] + P["kappa"] * k2), "denu": 1 + dt * P["Du"] * k2,
            "denp": 1 + dt * P["Dp"] * k2}


def step(s):
    phi, u, psi, k2, dt, M = s["phi"], s["u"], s["psi"], s["k2"], P["dt"], P["M"]
    c = np.clip((1 + phi) / 2, 0, 1)
    prod = P["k"] * u * c ** 2
    gy, gx = ops.grad(phi)
    mu_nl = phi ** 3 - phi - P["A"] * phi
    if P["s"]:
        mu_nl = mu_nl + 2 * P["s"] * ops.div(psi * gy, psi * gx)
    ph = (ops.rfft2(phi) - dt * M * k2 * ops.rfft2(mu_nl) + dt * ops.rfft2(prod - P["kd"] * c)) / s["den"]
    s["phi"] = ops.irfft2(ph, s["shape"])
    s["u"] = ops.irfft2((ops.rfft2(u) + dt * ops.rfft2(P["F"] * (1 - u) - prod)) / s["denu"], s["shape"])
    g2 = gy ** 2 + gx ** 2
    vy, vx = ops.grad(g2)
    drift = -P["Dp"] * P["chi"] * ops.upwind_flux_div(psi, vy, vx)
    rp = drift + P["kp"] * prod - P["gp"] * psi
    s["psi"] = np.clip(ops.irfft2((ops.rfft2(psi) + dt * ops.rfft2(rp)) / s["denp"], s["shape"]), 0, None)
    return s


def fields(s):
    return np.stack([s["phi"], s["u"], s["psi"]])


def damage(s, mask):
    s["phi"][mask] = -1.0
    s["psi"][mask] = 0.0
    return s
