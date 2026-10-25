"""Nonreciprocal Cahn-Hilliard (NRCH), Brauns & Marchetti, PRX 14, 021014 (2024), eqs. (1), 2D periodic:

    d phi/dt = lap(D11 phi + D12 psi + phi^3 - kappa lap phi)
    d psi/dt = lap(D21 phi + D22 psi)

phi phase separates (D11 < 0); psi is a conserved, purely diffusive partner. Anti-reciprocal coupling
D12 = Dt < 0, D21 = |Dt| (phi is pulled toward psi, psi is pushed away from phi): above the
drift-pitchfork |Dt| > D22, demixed domains travel. Optional Model-A reaction g = -u (phi - phi_a)(phi - phi_t) on phi (Li & Cates 2020). Optional AMB+ terms on phi (lam |grad phi|^2 in
the chemical potential, -zeta div(lap phi grad phi)) for the amb-plus focus.
Pseudo-spectral, 2/3 dealiasing, grid spacing dx; the whole linear part (kappa lap^2, a stabiliser
S lap on phi, the cross terms and D22) is implicit as a 2x2 solve per mode; phi^3 - S phi explicit.
Optional ramp [t0, t1, phi_t1]: phi_t moves linearly to phi_t1 between t0 and t1. Optional conserved noise on phi (strength D). Initial condition: uniform phi0 plus noise, psi = 0 plus noise. WORLD_P (JSON) overrides P (screening).
"""
import json, os
import numpy as np
from numpy.fft import rfft2, irfft2

META = {
    "name": "nrch",
    "family": "active-emulsion",
    "parent": None,
    "mutation": "reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive",
    "size": (192, 192),
    "steps_per_frame": 400,
    "dt": 0.05,
    "channels": ["phi", "psi"],
    "matter": [0],
    "threshold": 0.0,
    "smooth": 0.5,
    "radial_channels": [0, 1],
}

P = dict(D11=-1.0, Dt=-0.3, D22=0.1, kappa=1.0, dx=0.5, S=2.0, dt=0.05, phi0=-0.4, noise0=0.05,
         lam=0.0, zeta=0.0, u=1.5e-3, phi_a=-10.0, phi_t=-0.4, D=0.0, ramp=[3000, 8000, -0.3])
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    phi = P["phi0"] + P["noise0"] * rng.standard_normal((H, W))
    psi = P["noise0"] * rng.standard_normal((H, W))
    psi -= psi.mean()
    dx = P["dx"]
    ky = 2 * np.pi * np.fft.fftfreq(H, d=dx)[:, None]
    kx = 2 * np.pi * np.fft.rfftfreq(W, d=dx)[None, :]
    k2 = kx ** 2 + ky ** 2
    kmax = np.pi / dx
    da = (np.abs(kx) < 2 / 3 * kmax) & (np.abs(ky) < 2 / 3 * kmax)
    dt, Dt = P["dt"], P["Dt"]
    D12, D21 = Dt, abs(Dt)
    a = 1 + dt * (P["kappa"] * k2 ** 2 + P["S"] * k2)
    b = dt * D12 * k2
    c = dt * D21 * k2
    d = 1 + dt * P["D22"] * k2
    det = a * d - b * c
    return {"phi": phi, "psi": psi, "kx": kx, "ky": ky, "k2": k2, "da": da,
            "a": a, "b": b, "c": c, "d": d, "det": det, "shape": (H, W), "rng": rng}


def step(s):
    phi, k2, sh, dt = s["phi"], s["k2"], s["shape"], P["dt"]
    ph, ps = rfft2(phi), rfft2(s["psi"])
    mu = phi ** 3 + (P["D11"] - P["S"]) * phi
    nl = -k2 * rfft2(mu)
    if P["lam"] or P["zeta"]:
        kx, ky = s["kx"], s["ky"]
        gx, gy = irfft2(1j * kx * ph, sh), irfft2(1j * ky * ph, sh)
        lap = irfft2(-k2 * ph, sh)
        nl = nl - k2 * rfft2(P["lam"] * (gx * gx + gy * gy)) \
            - P["zeta"] * (1j * kx * rfft2(lap * gx) + 1j * ky * rfft2(lap * gy))
    s["t"] = s.get("t", 0.0) + dt
    if P["u"]:
        pt = P["phi_t"]
        if P["ramp"]:
            t0, t1, p1 = P["ramp"]
            pt = pt + (p1 - pt) * min(max((s["t"] - t0) / (t1 - t0), 0.0), 1.0)
        nl = nl + rfft2(-P["u"] * (phi - P["phi_a"]) * (phi - pt))
    if P["D"]:
        r = s["rng"]; kx, ky = s["kx"], s["ky"]
        nl = nl - np.sqrt(2 * P["D"] / (dt * P["dx"] ** 2)) * (1j * kx * rfft2(r.standard_normal(sh)) + 1j * ky * rfft2(r.standard_normal(sh)))
    r1 = ph + dt * nl * s["da"]
    r2 = ps
    s["phi"] = irfft2((s["d"] * r1 - s["b"] * r2) / s["det"], sh)
    s["psi"] = irfft2((s["a"] * r2 - s["c"] * r1) / s["det"], sh)
    return s


def fields(s):
    return np.stack([s["phi"], s["psi"]])


def damage(s, mask):
    s["phi"][mask] = -1.0
    return s
