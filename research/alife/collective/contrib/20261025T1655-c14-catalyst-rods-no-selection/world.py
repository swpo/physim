"""prod (c14): c11's ringed active-nematic droplets (20261025T1141-c11-active-nematic-ringed) whose growth is
made by identity-carrying Brownian catalyst particles from a fed, diffusing fuel u (prod = kc Ky c u), with the
bath relaxing to an undersaturated phi_b = -0.8, so a droplet without catalyst shrinks. Particles replicate
inside droplets (r c (1 - K)), die faster outside (g (1 - c) + dK), ride the self-made flow and take a gated
Brownian step. Everything else is c11's world.

Active nematic droplets: Cahn-Hilliard droplets that carry their own nematic order and
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
from scipy import ndimage
from numpy.fft import fft2, ifft2

META = {
    "name": "prod-catalyst-rods",
    "family": "active-nematic",
    "parent": None,
    "mutation": "new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow",
    "size": (128, 128),
    "steps_per_frame": 100,
    "dt": 0.05,
    "channels": ["phi (droplet)", "order |Q|", "surfactant s", "K particles"], "old_channels": ["phi (droplet)", "order |Q|", "surfactant s"],
    "matter": [0],
    "threshold": 0.0,
    "smooth": 0.5,
    "periodic": True,
    "radial_channels": [0, 1, 2],
}

P = dict(dx=1.0, dt=0.05, a=1.0, k=1.5, M=1.0, S=2.0, c=1.0, phi_c=0.0, G=0.5, L=1.0,
         lam_f=0.5, zeta=0.8, eta=1.0, xi=0.02, phi0=-0.4, noise=0.2, qnoise=0.05, kr=0.012, phi_b=-0.6, Ds=0.5, chis=3.0, ks=0.02, kds=0.02,
         kc=0.04, r=0.2, g=0.05, dK=0.002, DK=0.05, m=0.1, sig=1.0, gq=2.0, nK=0.3, y0=1.0, muy=0.0, sy=0.1, ymax=1.2, Nmax=200000, F=0.007, Du=1.0)
P["phi_b"] = -0.8
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
    cnt = rng.poisson(P["nK"] * rng.random((H, W)) / P["m"])
    iy, ix = np.nonzero(cnt); rep = cnt[iy, ix]
    py = np.repeat(iy, rep) + rng.random(rep.sum()); px = np.repeat(ix, rep) + rng.random(rep.sum()); N = len(py)
    return {"py": py, "px": px, "y": np.full(N, P["y0"]), "z": np.full(N, P["y0"]), "uid": np.arange(N, dtype=np.int64), "next": N,
            "kind": np.zeros(N, np.int8), "rng": rng, "births": np.zeros(1, np.int64), "deaths": np.zeros(1, np.int64), "flips": 0,
            "u": np.ones((H, W)), "phi": phi, "q1": q1, "q2": q2, "kx": kx, "ky": ky, "k2": k2, "k2s": k2s, "da": da,
            "vx": np.zeros((H, W)), "vy": np.zeros((H, W)), "t": 0.0, "s": np.zeros((H, W))}


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
    s["s"] = np.maximum(ifft2(Sh).real, 0)
    s["phi"], s["q1"], s["q2"] = ifft2(Ph).real, ifft2(Q1).real, ifft2(Q2).real
    s["vx"], s["vy"], s["om"] = vx, vy, om
    # catalyst particles: make droplet material, replicate inside droplets, ride the flow, gated by c
    H, W = phi.shape; rng = s["rng"]
    c = 0.5 * (1 + np.clip(s["phi"], -1, 1))
    K = dens(s, H, W); Ky = dens(s, H, W, s["y"])
    prod = P["kc"] * Ky * c * (s["u"] if P["F"] > 0 else 1.0)
    s["phi"] = s["phi"] + dt * prod
    if P["F"] > 0:  # fuel: fed from a bath, diffuses, consumed by production
        Uh = fft2(s["u"] + dt * (P["F"] * (1 - s["u"]) - prod))
        s["u"] = np.maximum(ifft2(Uh / (1 + dt * P["Du"] * k2)).real, 0)
    py, px = s["py"], s["px"]
    iy = py.astype(np.int64) % H; ix = px.astype(np.int64) % W
    cp, Kp = c[iy, ix], K[iy, ix]
    pdup = np.clip(P["r"] * cp * (1 - Kp) * dt, 0, 1); pdie = (P["g"] * (1 - cp) + P["dK"]) * dt
    u = rng.random(len(py)); dup = u < pdup; die = (u >= pdup) & (u < pdup + pdie); keep = ~die; nd = int(dup.sum())
    s["births"] += nd; s["deaths"] += int(die.sum())
    yd = s["y"][dup].copy(); zd = s["z"][dup].copy()
    if P["muy"] > 0 and nd:
        f = rng.random(nd) < P["muy"]; yd[f] = np.clip(yd[f] + P["sy"] * rng.standard_normal(f.sum()), 0, P["ymax"])
        f = rng.random(nd) < P["muy"]; zd[f] = np.clip(zd[f] + P["sy"] * rng.standard_normal(f.sum()), 0, P["ymax"])
    py = np.concatenate([py[keep], py[dup] + 0.3 * rng.standard_normal(nd)]); px = np.concatenate([px[keep], px[dup] + 0.3 * rng.standard_normal(nd)])
    s["y"] = np.concatenate([s["y"][keep], yd]); s["z"] = np.concatenate([s["z"][keep], zd])
    s["uid"] = np.concatenate([s["uid"][keep], np.arange(s["next"], s["next"] + nd)]); s["next"] += nd
    iy = py.astype(np.int64) % H; ix = px.astype(np.int64) % W
    dxg = P["dx"]
    ay = py + dt * vy[iy, ix] / dxg; ax = px + dt * vx[iy, ix] / dxg  # advection by the self-made flow (grid units)
    sd = np.sqrt(2 * P["DK"] * dt) / dxg
    ny = ay + sd * rng.standard_normal(len(py)); nx = ax + sd * rng.standard_normal(len(px))
    c0 = c[ay.astype(np.int64) % H, ax.astype(np.int64) % W]; c1 = c[ny.astype(np.int64) % H, nx.astype(np.int64) % W]
    acc = np.where(c1 >= c0, 1.0, (c1 / np.maximum(c0, 1e-9)) ** P["gq"]); ok = rng.random(len(py)) < acc
    s["py"] = np.where(ok, ny, ay) % H; s["px"] = np.where(ok, nx, ax) % W
    s["kind"] = np.zeros(len(s["py"]), np.int8)
    if len(s["py"]) > P["Nmax"]:
        sel = rng.choice(len(s["py"]), int(P["Nmax"]), replace=False)
        for kk in ("py", "px", "y", "z", "uid", "kind"): s[kk] = s[kk][sel]
    return s


def dens(s, H, W, w=None):
    iy = s["py"].astype(np.int64) % H; ix = s["px"].astype(np.int64) % W
    cc = np.bincount(iy * W + ix, weights=w, minlength=H * W).reshape(H, W) * P["m"]
    return ndimage.gaussian_filter(cc, P["sig"], mode="wrap")


def fields(s):
    om = s.get("om", np.zeros_like(s["phi"]))
    H, W = s["phi"].shape
    return np.stack([s["phi"], np.sqrt(s["q1"] ** 2 + s["q2"] ** 2), s["s"], dens(s, H, W)]).astype(np.float32)


def particles(s):
    return np.stack([s["px"], s["py"], s["y"]], 1)


def stats(s):
    return {"vmax": round(float(np.hypot(s["vx"], s["vy"]).max()), 4), "mean_phi": round(float(s["phi"].mean()), 4)}
