"""Active nematic droplets: Cahn-Hilliard droplets that carry their own nematic order and
stir themselves through an active stress, on a Brinkman-Stokes fluid (c11).

After Giomi & DeSimone, PRL 112, 147802 (2014) ("Spontaneous division and motility in active
nematic droplets"), simplified to a dry-friction Stokes fluid so that the flow is one
spectral solve per step. 2D periodic, pseudo-spectral.

phi: droplet phase (+1 inside, -1 outside), model H:
    dphi/dt + v.grad phi = M lap mu,   mu = a (phi^3 - phi) - k lap phi
Q = [[q1, q2], [q2, -q1]]: nematic order, ordered only inside droplets:
    dQ/dt + v.grad Q - [Q, W] = lam_f E (inside) + G H,
    H = -c (phi_c - phi) Q - c |Q|^2 Q + L lap Q  (|Q|^2 = q1^2 + q2^2)
Fluid (Brinkman-Stokes, incompressible):
    (xi - eta lap) v + grad p = f,  f = mu grad phi (capillary) + div(-zeta Q) (active stress)
zeta > 0 extensile. The only source of motion is the droplets' own active stress, which is
proportional to their own order Q; outside droplets Q relaxes to 0. Ablation: zeta = 0
(passive nematic emulsion: coarsening only). WORLD_P (JSON) overrides P.
"""
import json, os
import numpy as np
from numpy.fft import fft2, ifft2

META = {
    "name": "active-nematic-droplets",
    "family": "active-nematic",
    "parent": None,
    "mutation": "new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow",
    "size": (128, 128),
    "steps_per_frame": 100,
    "dt": 0.05,
    "channels": ["phi (droplet)", "order |Q|", "vorticity"],
    "matter": [0],
    "threshold": 0.0,
    "smooth": 0.5,
    "periodic": True,
    "radial_channels": [0, 1],
}

P = dict(dx=1.0, dt=0.05, a=1.0, k=1.5, M=1.0, S=2.0, c=1.0, phi_c=0.0, G=0.5, L=1.0,
         lam_f=0.5, zeta=0.6, eta=1.0, xi=0.02, phi0=-0.55, noise=0.2, qnoise=0.05)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    dx = P["dx"]
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    q1 = P["qnoise"] * rng.standard_normal((H, W))
    q2 = P["qnoise"] * rng.standard_normal((H, W))
    ky = 2 * np.pi * np.fft.fftfreq(H, d=dx)[:, None] * np.ones((1, W))
    kx = 2 * np.pi * np.fft.fftfreq(W, d=dx)[None, :] * np.ones((H, 1))
    k2 = kx ** 2 + ky ** 2
    kmax = np.pi / dx
    da = ((np.abs(kx) < 2 / 3 * kmax) & (np.abs(ky) < 2 / 3 * kmax)).astype(float)
    k2s = k2.copy(); k2s[0, 0] = 1.0
    return {"phi": phi, "q1": q1, "q2": q2, "kx": kx, "ky": ky, "k2": k2, "k2s": k2s, "da": da,
            "vx": np.zeros((H, W)), "vy": np.zeros((H, W)), "t": 0.0}


def _d(f_hat, k):
    return ifft2(1j * k * f_hat).real


def step(s):
    dt, kx, ky, k2, da = P["dt"], s["kx"], s["ky"], s["k2"], s["da"]
    phi, q1, q2 = s["phi"], s["q1"], s["q2"]
    Ph, Q1, Q2 = fft2(phi), fft2(q1), fft2(q2)
    # chemical potential and capillary force
    mu = P["a"] * (phi ** 3 - phi) - P["k"] * ifft2(-k2 * Ph).real
    px, py = _d(Ph, kx), _d(Ph, ky)
    fx = mu * px - P["zeta"] * (_d(Q1, kx) + _d(Q2, ky))
    fy = mu * py - P["zeta"] * (_d(Q2, kx) - _d(Q1, ky))
    Fx, Fy = fft2(fx), fft2(fy)
    kf = (kx * Fx + ky * Fy) / s["k2s"]
    den = P["xi"] + P["eta"] * k2
    Vx = (Fx - kx * kf) / den * da
    Vy = (Fy - ky * kf) / den * da
    Vx[0, 0] = Vy[0, 0] = 0
    vx, vy = ifft2(Vx).real, ifft2(Vy).real
    # velocity gradients
    dxvx, dyvx, dxvy, dyvy = _d(Vx, kx), _d(Vx, ky), _d(Vy, kx), _d(Vy, ky)
    om = 0.5 * (dxvy - dyvx)
    Exx, Exy = 0.5 * (dxvx - dyvy), 0.5 * (dyvx + dxvy)
    # phi: advection explicit, CH stabilised semi-implicit
    adv_phi = vx * px + vy * py
    nl = P["a"] * (phi ** 3 - phi) - P["S"] * phi
    rhs = Ph - dt * fft2(adv_phi) * da - dt * P["M"] * k2 * fft2(nl) * da
    Ph = rhs / (1 + dt * P["M"] * (P["k"] * k2 ** 2 + P["S"] * k2))
    # Q: bulk terms explicit, L lap implicit
    inside = 0.5 * (1 + np.clip(phi, -1, 1))
    QQ = q1 * q1 + q2 * q2
    bulk = -P["c"] * (P["phi_c"] - phi) - P["c"] * QQ
    r1 = -(vx * _d(Q1, kx) + vy * _d(Q1, ky)) - 2 * om * q2 + P["lam_f"] * inside * Exx + P["G"] * bulk * q1
    r2 = -(vx * _d(Q2, kx) + vy * _d(Q2, ky)) + 2 * om * q1 + P["lam_f"] * inside * Exy + P["G"] * bulk * q2
    imp = 1 + dt * P["G"] * P["L"] * k2
    Q1 = (Q1 + dt * fft2(r1) * da) / imp
    Q2 = (Q2 + dt * fft2(r2) * da) / imp
    s["phi"], s["q1"], s["q2"] = ifft2(Ph).real, ifft2(Q1).real, ifft2(Q2).real
    s["vx"], s["vy"], s["om"] = vx, vy, om
    return s


def fields(s):
    om = s.get("om", np.zeros_like(s["phi"]))
    return np.stack([s["phi"], np.sqrt(s["q1"] ** 2 + s["q2"] ** 2), om]).astype(np.float32)


def stats(s):
    return {"vmax": round(float(np.hypot(s["vx"], s["vy"]).max()), 4), "mean_phi": round(float(s["phi"].mean()), 4)}
