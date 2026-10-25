"""pdrop (c14): fuel-fed Cahn-Hilliard droplets (ad2-catalysts, threads/active-droplets) whose catalyst
fields are replaced by identity-carrying Brownian catalyst particles (as pcell did for phase_membrane).

phi  droplet material, Cahn-Hilliard (semi-implicit spectral), made from fuel by catalyst, decays:
       dphi = M lap(phi^3 - phi - kappa lap phi) + u c^2 kcat Ky - kd c,   c = (1 + phi) / 2
u    fuel, fed from a bath: du = Du lap u + F (1 - u) - u c^2 kcat Ky
particles  each of mass m; K = gaussian(m * counts), Ky = gaussian(m * sum of heritable rate y).
       per step: duplicates with prob r c (1 - K) dt (daughter copies y, z; mutation muy, step sy,
       capped at ymax), dies with prob (g (1 - c) + dK) dt, Brownian step sqrt(2 DK dt) with a
       gate: a step to lower c is accepted with prob (c_new / c_old)^gq.
y is a public good inside a droplet (rate of making droplet material); z is an inert marker.
"""
import numpy as np
from scipy import ndimage
from labkit import ops

META = {"name": "pdrop", "family": "hybrid-particle-field", "parent": "threads/active-droplets/worlds/ad2-catalysts",
        "mutation": "catalyst fields -> identity-carrying Brownian particles with a heritable rate, gated by droplet material",
        "size": (128, 128), "steps_per_frame": 200, "dt": 0.5,
        "channels": ["phi (droplet material)", "u (fuel)", "K particles", "mean rate / 2"],
        "matter": [0], "threshold": 0.0, "periodic": True}

P = dict(M=0.03, kappa=1.0, kcat=0.1, kd=0.02, F=0.01, Du=0.3, A=2.0, dt=0.5, phi0=-0.3, noise=0.1,
         r=0.2, g=0.005, dK=0.002, DK=0.05, m=0.2, sig=1.0, gq=2.0, nK=0.5, y0=1.0, muy=0.0, sy=0.1, ymax=1.2, Nmax=300000)


def dens(s, H, W, w=None):
    iy = s["py"].astype(np.int64) % H; ix = s["px"].astype(np.int64) % W
    c = np.bincount(iy * W + ix, weights=w, minlength=H * W).reshape(H, W) * P["m"]
    return ndimage.gaussian_filter(c, P["sig"], mode="wrap")


def init(seed, size):
    rng = np.random.default_rng(seed); H, W = size
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    cnt = rng.poisson(P["nK"] * rng.random((H, W)) / P["m"])
    iy, ix = np.nonzero(cnt); rep = cnt[iy, ix]
    py = np.repeat(iy, rep) + rng.random(rep.sum()); px = np.repeat(ix, rep) + rng.random(rep.sum())
    N = len(py)
    ky, kx = ops.wavenumbers(H, W); k2 = kx ** 2 + ky ** 2
    dt, M = P["dt"], P["M"]
    s = {"phi": phi, "u": np.ones((H, W)), "py": py, "px": px, "y": np.full(N, P["y0"]), "z": np.full(N, P["y0"]),
         "uid": np.arange(N, dtype=np.int64), "next": N, "kind": np.zeros(N, np.int8), "rng": rng, "k2": k2, "shape": (H, W),
         "den": 1 + dt * M * k2 * (P["A"] + P["kappa"] * k2), "denu": 1 + dt * P["Du"] * k2,
         "births": np.zeros(1, np.int64), "deaths": np.zeros(1, np.int64), "flips": 0}
    return s


def step(s):
    phi, u, k2, dt, M, rng = s["phi"], s["u"], s["k2"], P["dt"], P["M"], s["rng"]
    H, W = s["shape"]
    c = np.clip((1 + phi) / 2, 0, 1)
    K = dens(s, H, W); Ky = dens(s, H, W, s["y"])
    prod = u * c ** 2 * P["kcat"] * Ky
    src = prod - P["kd"] * c
    ph = (ops.rfft2(phi) - dt * M * k2 * ops.rfft2(phi ** 3 - phi - P["A"] * phi) + dt * ops.rfft2(src)) / s["den"]
    s["phi"] = ops.irfft2(ph, s["shape"])
    s["u"] = ops.irfft2((ops.rfft2(u) + dt * ops.rfft2(P["F"] * (1 - u) - prod)) / s["denu"], s["shape"])
    py, px = s["py"], s["px"]
    iy = py.astype(np.int64) % H; ix = px.astype(np.int64) % W
    cp, Kp = c[iy, ix], K[iy, ix]
    pdup = np.clip(P["r"] * cp * (1 - Kp) * dt, 0, 1)
    pdie = (P["g"] * (1 - cp) + P["dK"]) * dt
    uu = rng.random(len(py)); dup = uu < pdup; die = (uu >= pdup) & (uu < pdup + pdie)
    s["births"] += dup.sum(); s["deaths"] += die.sum()
    keep = ~die; nd = int(dup.sum())
    yd = s["y"][dup].copy(); zd = s["z"][dup].copy()
    if P["muy"] > 0 and nd:
        f = rng.random(nd) < P["muy"]; yd[f] = np.clip(yd[f] + P["sy"] * rng.standard_normal(f.sum()), 0, P["ymax"])
        f = rng.random(nd) < P["muy"]; zd[f] = np.clip(zd[f] + P["sy"] * rng.standard_normal(f.sum()), 0, P["ymax"])
    py = np.concatenate([py[keep], py[dup] + 0.3 * rng.standard_normal(nd)])
    px = np.concatenate([px[keep], px[dup] + 0.3 * rng.standard_normal(nd)])
    s["y"] = np.concatenate([s["y"][keep], yd]); s["z"] = np.concatenate([s["z"][keep], zd])
    s["uid"] = np.concatenate([s["uid"][keep], np.arange(s["next"], s["next"] + nd)]); s["next"] += nd
    s["kind"] = np.zeros(len(py), np.int8)
    sd = np.sqrt(2 * P["DK"] * dt)
    ny = py + sd * rng.standard_normal(len(py)); nx = px + sd * rng.standard_normal(len(px))
    c0 = c[py.astype(np.int64) % H, px.astype(np.int64) % W]; c1 = c[ny.astype(np.int64) % H, nx.astype(np.int64) % W]
    acc = np.where(c1 >= c0, 1.0, (c1 / np.maximum(c0, 1e-9)) ** P["gq"])
    ok = rng.random(len(py)) < acc
    s["py"] = np.where(ok, ny, py) % H; s["px"] = np.where(ok, nx, px) % W
    if len(s["py"]) > P["Nmax"]:
        sel = rng.choice(len(s["py"]), int(P["Nmax"]), replace=False)
        for k in ("py", "px", "y", "z", "uid", "kind"): s[k] = s[k][sel]
    return s


def fields(s):
    H, W = s["shape"]; K = dens(s, H, W); Ky = dens(s, H, W, s["y"])
    yb = np.where(K > 0.05, Ky / np.maximum(K, 1e-9), 0) / 2
    return np.stack([s["phi"], s["u"], K, yb]).astype(np.float32)


def particles(s):
    return np.stack([s["px"], s["py"], s["y"]], 1)


def damage(s, mask):
    H, W = mask.shape
    hit = mask[s["py"].astype(np.int64) % H, s["px"].astype(np.int64) % W]
    for k in ("py", "px", "y", "z", "uid", "kind"): s[k] = s[k][~hit]
    s["phi"][mask] = -1.0
    return s
