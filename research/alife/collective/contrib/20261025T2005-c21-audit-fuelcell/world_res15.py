"""(c21 audit: the claimed world at 1.5x resolution, dx = 2/3 on 192x192, same physical domain.) Active nematic droplets: Cahn-Hilliard droplets that carry their own nematic order and
stir themselves through an active stress, on a Brinkman-Stokes fluid (c11).

After Giomi & DeSimone, PRL 112, 147802 (2014) ("Spontaneous division and motility in active
nematic droplets"), simplified to a dry-friction Stokes fluid so that the flow is one
spectral solve per step. 2D periodic, pseudo-spectral.

phi: droplet phase (+1 inside, -1 outside), model H:
    dphi/dt + v.grad phi = M lap mu + kr (phi_b - phi),   mu = a (phi^3 - phi) - k lap phi
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
    "name": "nematic-fuelcell-res15",
    "family": "active-nematic",
    "parent": None,
    "mutation": "new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow",
    "size": (192, 192),
    "steps_per_frame": 100,
    "dt": 0.05,
    "channels": ["phi (droplet)", "order |Q|", "shell s", "fuel f"],
    "matter": [0],
    "threshold": 0.0,
    "smooth": 0.5,
    "periodic": True,
    "radial_channels": [0, 1, 2, 3],
}

P = dict(dx=2.0 / 3, dt=0.05, a=1.0, k=1.5, M=1.0, S=2.0, c=1.0, phi_c=0.0, G=0.5, L=1.0,
         lam_f=0.5, zeta=4.5, eta=1.0, xi=0.02, phi0=-0.4, noise=0.2, qnoise=0.05, kr=0.012, phi_b=-0.6, Ds=0.5, chis=3.0, ks=0.02, kds=0.02, Df=2.0, beta=5.0, sh=0.45, nh=12, kf=0.15, kdf=0.02, f0=3.0, linear=0)
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
            "vx": np.zeros((H, W)), "vy": np.zeros((H, W)), "t": 0.0, "s": np.zeros((H, W)), "f": np.zeros((H, W))}


def _d(f_hat, k):
    return ifft2(1j * k * f_hat).real


def step(s):
    dt, kx, ky, k2, da = P["dt"], s["kx"], s["ky"], s["k2"], s["da"]
    phi, q1, q2 = s["phi"], s["q1"], s["q2"]
    Ph, Q1, Q2 = fft2(phi), fft2(q1), fft2(q2)
    # chemical potential and capillary force
    mu = P["a"] * (phi ** 3 - phi) - P["k"] * ifft2(-k2 * Ph).real
    px, py = _d(Ph, kx), _d(Ph, ky)
    fu = s["f"]
    g = fu / (fu + P["f0"])
    A1, A2 = fft2(g * q1), fft2(g * q2)
    fx = mu * px - P["zeta"] * (_d(A1, kx) + _d(A2, ky))
    fy = mu * py - P["zeta"] * (_d(A2, kx) - _d(A1, ky))
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
    if P["linear"]:
        # Laplacian-only twin: CH replaced by linear diffusion at CH's bulk diffusivity 2 a M
        rhs = Ph - dt * fft2(adv_phi) * da
        rhs[0, 0] += dt * P["kr"] * P["phi_b"] * phi.size
        Ph = rhs / (1 + dt * 2 * P["a"] * P["M"] * k2 + dt * P["kr"])
    else:
        nl = P["a"] * (phi ** 3 - phi) - P["S"] * phi
        rhs = Ph - dt * fft2(adv_phi) * da - dt * P["M"] * k2 * fft2(nl) * da
        rhs[0, 0] += dt * P["kr"] * P["phi_b"] * phi.size
        Ph = rhs / (1 + dt * P["M"] * (P["k"] * k2 ** 2 + P["S"] * k2) + dt * P["kr"])
    # Q: bulk terms explicit, L lap implicit
    inside = 0.5 * (1 + np.clip(phi, -1, 1))
    QQ = q1 * q1 + q2 * q2
    bulk = -P["c"] * (P["phi_c"] - phi) - P["c"] * QQ
    r1 = -(vx * _d(Q1, kx) + vy * _d(Q1, ky)) - 2 * om * q2 + P["lam_f"] * inside * Exx + P["G"] * bulk * q1
    r2 = -(vx * _d(Q2, kx) + vy * _d(Q2, ky)) + 2 * om * q1 + P["lam_f"] * inside * Exy + P["G"] * bulk * q2
    imp = 1 + dt * P["G"] * P["L"] * k2
    Q1 = (Q1 + dt * fft2(r1) * da) / imp
    Q2 = (Q2 + dt * fft2(r2) * da) / imp
    # surfactant: made inside droplets, decays, adsorbs at the interface (drift up grad w, w = 1 - phi^2)
    sf = s["s"]
    w = 1 - np.clip(phi, -1, 1) ** 2
    Wh = fft2(w)
    wx, wy = _d(Wh, kx), _d(Wh, ky)
    Sh = fft2(sf)
    fxs = P["Ds"] * P["chis"] * sf * wx + vx * sf
    fys = P["Ds"] * P["chis"] * sf * wy + vy * sf
    src = P["ks"] * 0.5 * (1 + np.clip(phi, -1, 1)) - P["kds"] * sf
    Sh = (Sh + dt * (-(1j * kx * fft2(fxs) + 1j * ky * fft2(fys)) + fft2(src)) * da) / (1 + dt * P["Ds"] * k2)
    # fuel: made inside droplets, decays, diffuses with a permeability lowered by the shell
    D = P["Df"] / (1 + P["beta"] * (sf / P["sh"]) ** P["nh"])
    Fh = fft2(fu)
    gx, gy = D * _d(Fh, kx) - vx * fu, D * _d(Fh, ky) - vy * fu
    srcf = P["kf"] * (0.5 * (1 + np.clip(phi, -1, 1))) ** 4 - P["kdf"] * fu
    Fh = (Fh + dt * ((1j * kx * fft2(gx) + 1j * ky * fft2(gy)) + fft2(srcf) + P["Df"] * k2 * Fh) * da) / (1 + dt * P["Df"] * k2)
    s["f"] = np.maximum(ifft2(Fh).real, 0)
    s["s"] = np.maximum(ifft2(Sh).real, 0)
    s["phi"], s["q1"], s["q2"] = ifft2(Ph).real, ifft2(Q1).real, ifft2(Q2).real
    s["vx"], s["vy"], s["om"] = vx, vy, om
    return s


def fields(s):
    om = s.get("om", np.zeros_like(s["phi"]))
    return np.stack([s["phi"], np.sqrt(s["q1"] ** 2 + s["q2"] ** 2), s["s"], s["f"]]).astype(np.float32)


def stats(s):
    return {"vmax": round(float(np.hypot(s["vx"], s["vy"]).max()), 4), "mean_phi": round(float(s["phi"].mean()), 4)}
