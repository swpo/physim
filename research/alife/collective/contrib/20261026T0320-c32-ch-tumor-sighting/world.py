"""(c32) Cahn-Hilliard tumour on a consumed nutrient (Hawkins-Daarud, van der Zee, Oden 2012; Cristini & Lowengrub),
a conserved phase field with a source, as a labkit world.

  dphi/dt = M lap mu + (P sigma - A) g(phi),   mu = Psi'(phi) - eps^2 lap phi,  Psi = phi^2 (1-phi)^2 / 4 * 4
  dsig/dt = Ds lap sigma - C sigma g(phi) + B (1 - sigma)       (nutrient, regrows from a uniform supply)
  g(phi) = clip(phi, 0, 1)
Growth is proliferation where nutrient is high minus apoptosis everywhere inside; the nutrient is eaten inside
the tissue and diffuses in, so large bodies starve inside. Nothing marks individuals or divides them:
any splitting is the shape instability of a diffusion-limited growing CH body.
Initial condition: phi = 0.5 + noise everywhere (spinodal), sigma = 1. WORLD_P overrides P.
Semi-implicit spectral CH (linear stabilisation), explicit reaction.
"""
import json, os
import numpy as np

P = dict(N=192, dx=1.0, dt=0.05, M=1.0, eps=1.0, Pp=0.5, A=0.1, C=1.0, Ds=4.0, B=0.02, noise=0.05, phi0=0.3, S=2.0)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))

META = {"name": "ch-tumor", "family": "ch-tumor", "parent": None,
        "mutation": "Cahn-Hilliard tissue with nutrient-limited proliferation and apoptosis (new class)",
        "size": (int(P["N"]), int(P["N"])), "steps_per_frame": 100, "dt": P["dt"],
        "channels": ["phi (tissue)", "sigma (nutrient)"], "matter": [0], "smooth": 1.0, "periodic": True}


def init(seed, size):
    H, W = size
    rng = np.random.default_rng(seed)
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    ky = 2 * np.pi * np.fft.fftfreq(H, d=P["dx"])[:, None]
    kx = 2 * np.pi * np.fft.fftfreq(W, d=P["dx"])[None, :]
    k2 = kx ** 2 + ky ** 2
    return {"phi": phi, "sig": np.ones((H, W)), "k2": k2}


def step(s):
    phi, sig, k2, dt = s["phi"], s["sig"], s["k2"], P["dt"]
    dpsi = 2 * phi * (1 - phi) * (1 - 2 * phi)          # Psi = phi^2 (1-phi)^2
    g = np.clip(phi, 0, 1)
    src = (P["Pp"] * sig - P["A"]) * g
    ph = np.fft.fft2(phi); nl = np.fft.fft2(dpsi - P["S"] * phi)
    ph = (ph + dt * (-P["M"] * k2 * nl) + dt * np.fft.fft2(src)) / (1 + dt * P["M"] * k2 * (P["S"] + P["eps"] ** 2 * k2))
    s["phi"] = np.real(np.fft.ifft2(ph))
    sh = np.fft.fft2(sig + dt * (-P["C"] * sig * g + P["B"] * (1 - sig)))
    s["sig"] = np.clip(np.real(np.fft.ifft2(sh / (1 + dt * P["Ds"] * k2))), 0, None)
    return s


def fields(s):
    return np.stack([s["phi"], s["sig"]]).astype(np.float32)


def damage(s, mask):
    s["phi"][mask] = 0.0
    return s
