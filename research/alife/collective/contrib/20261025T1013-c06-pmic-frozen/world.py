"""pmic: catalyst particles that make the amphiphile of the FCH micelle they live in.

Hybrid of c03's FCH micelle-fission world (functionalized Cahn-Hilliard, eta1=4, eta2=5) and
pcell's identity-carrying catalyst particles. The uniform amphiphile feed is replaced by local
synthesis from a fed precursor, catalysed by the particles, and amphiphile decays slowly, so a
micelle persists only while its own particles keep making amphiphile:
    du/dt = lap mu_u + kf * Ky * S - kdec (u - u_bg),   mu_u as in c03 (FCH)
    dS/dt = DS lap S + F (1 - S) - kf * Ky * S
Ky = sum over particles of m * y_p (Gaussian deposit, sigma sig px); K = the same with y_p = 1.
particles: per unit time a particle duplicates at rate c S (1 - K) g(u) (daughter copies its yield y
  and an inert marker z, each mutating with prob muy by a Gaussian step sy), dies at rate dK,
  and takes a Brownian step (diffusivity Dp). A step to lower g is accepted with prob
  (g_new / g_old)^2 (gate=1), g(u) = clip((u - u_bg) / (1 - u_bg), 0, 1), so particles stay in the
  amphiphile-rich micelle core. Optional cost: duplication x (1 + cy (1 - y)).
Units as c03: epsilon = 1, dx = 0.5, dt = 0.02.
"""
import numpy as np
from scipy import ndimage

META = {
    "name": "pmic",
    "family": "hybrid-particle-field",
    "parent": "collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py",
    "mutation": "uniform amphiphile feed -> local synthesis by gated catalyst particles from a fed precursor, plus amphiphile decay",
    "size": (128, 128),
    "steps_per_frame": 250,
    "dt": 0.02,
    "channels": ["amphiphile u (u + 1.6)", "K particles", "precursor S"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 1.0,
    "periodic": True,
    "radial_channels": [0, 1, 2],
}

P = dict(eta1=4.0, eta2=5.0, delta=0.3, mean=-1.3, amp=0.3, dx=0.5, dt=0.02, Sst=4.0, u_bg=-1.6,
         kf=0.03, kdec=0.002, DS=1.0, F=0.01, c=0.2, dK=0.02, Dp=0.1, m=0.1, sig=1.0, gate=1,
         K0=0.3, cy=0.0, muy=0.0, sy=0.05, ymax=2.0, ytrait=0, y0=1.0, Nmax=300000)


def Wp(u, d):
    return (u + 1) * ((u - 1) ** 2 / 2 - d) + 0.5 * (u + 1) ** 2 * (u - 1)


def Wpp(u, d):
    return ((u - 1) ** 2 / 2 - d) + 2 * (u + 1) * (u - 1) + 0.5 * (u + 1) ** 2


def lap(f, dx):
    return (np.roll(f, 1, 0) + np.roll(f, -1, 0) + np.roll(f, 1, 1) + np.roll(f, -1, 1) - 4 * f) / dx ** 2


def gfun(u):
    return np.clip((u - P["u_bg"]) / (1 - P["u_bg"]), 0, 1)


def density(s, H, W, w=None):
    iy = s["py"].astype(np.int64) % H
    ix = s["px"].astype(np.int64) % W
    cnt = np.bincount(iy * W + ix, weights=w, minlength=H * W).reshape(H, W) * P["m"]
    return ndimage.gaussian_filter(cnt, P["sig"], mode="wrap") if P["sig"] > 0 else cnt


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    dx = P["dx"]
    u = P["mean"] + P["amp"] * rng.standard_normal((H, W))  # white noise over the whole domain
    lam = P["K0"] * rng.random((H, W)) / P["m"]
    cnt = rng.poisson(lam)
    iy, ix = np.nonzero(cnt)
    rep = cnt[iy, ix]
    N = int(rep.sum())
    py = np.repeat(iy, rep) + rng.random(N)
    px = np.repeat(ix, rep) + rng.random(N)
    ky = 2 * np.pi * np.fft.fftfreq(H, d=dx)
    kx = 2 * np.pi * np.fft.fftfreq(W, d=dx)
    kk = ky[:, None] ** 2 + kx[None, :] ** 2
    s = {"u": u, "S": np.ones((H, W)), "kk": kk, "rng": rng, "t": 0,
         "py": py, "px": px, "y": np.full(N, P["y0"]), "z": np.full(N, P["y0"]),
         "uid": np.arange(N, dtype=np.int64), "next": N, "kind": np.zeros(N, np.int8)}
    s["K"] = density(s, H, W)
    s["phi"] = gfun(u)
    return s


def step(s):
    u, S, kk, d, dt, rng = s["u"], s["S"], s["kk"], P["delta"], P["dt"], s["rng"]
    H, W = u.shape
    dx = P["dx"]
    py, px = s["py"], s["px"]
    iy = py.astype(np.int64) % H
    ix = px.astype(np.int64) % W
    g = gfun(u)
    yp = s["y"] if P["ytrait"] == 1 else np.full(len(py), P["y0"])
    # particle demography
    cost = np.maximum(1 + P["cy"] * (1 - yp), 0) if P["cy"] else 1.0
    pdup = np.clip(P["c"] * cost * S[iy, ix] * (1 - s["K"][iy, ix]) * g[iy, ix] * dt, 0, 1)
    uu = rng.random(len(py))
    dup = uu < pdup
    die = (uu >= pdup) & (uu < pdup + P["dK"] * dt)
    # synthesis of amphiphile from precursor by the particles (weighted by yield)
    Ky = density(s, H, W, w=yp)
    syn = P["kf"] * Ky * S
    dupS = np.bincount(iy[dup] * W + ix[dup], minlength=H * W).reshape(H, W) * P["m"]
    s["S"] = np.maximum(S + dt * (P["DS"] * lap(S, dx) + P["F"] * (1 - S) - syn) - dupS, 0)
    # FCH step (c03), with local synthesis and decay instead of a uniform feed
    U = np.fft.fft2(u)
    lu = np.fft.ifft2(-kk * U).real
    wp = Wp(u, d)
    nl = np.fft.ifft2(kk * np.fft.fft2(wp)).real - Wpp(u, d) * (lu - wp) + P["eta1"] * lu - P["eta2"] * wp
    Sst = P["Sst"]
    U = (U - dt * kk * np.fft.fft2(nl) + dt * Sst * kk ** 2 * U) / (1 + dt * (kk ** 3 + Sst * kk ** 2))
    s["u"] = np.fft.ifft2(U).real + dt * (syn - P["kdec"] * (u - P["u_bg"]))
    # births, deaths, mutation
    nd = int(dup.sum())
    yd = s["y"][dup].copy(); zd = s["z"][dup].copy()
    if P["muy"] > 0 and nd:
        f1 = rng.random(nd) < P["muy"]
        yd[f1] = np.clip(yd[f1] + P["sy"] * rng.standard_normal(f1.sum()), 0, P["ymax"])
        f2 = rng.random(nd) < P["muy"]
        zd[f2] = np.clip(zd[f2] + P["sy"] * rng.standard_normal(f2.sum()), 0, P["ymax"])
    keep = ~die
    py = np.concatenate([py[keep], py[dup] + 0.3 * rng.standard_normal(nd)])
    px = np.concatenate([px[keep], px[dup] + 0.3 * rng.standard_normal(nd)])
    yy = np.concatenate([s["y"][keep], yd]); zz = np.concatenate([s["z"][keep], zd])
    uid = np.concatenate([s["uid"][keep], np.arange(s["next"], s["next"] + nd, dtype=np.int64)])
    s["next"] += nd
    # gated Brownian step (positions in px; Dp in physical units)
    sd = np.sqrt(2 * P["Dp"] * dt) / dx
    ny = py + sd * rng.standard_normal(len(py))
    nx = px + sd * rng.standard_normal(len(px))
    if P["gate"]:
        g2 = gfun(s["u"])
        p0 = g2[py.astype(np.int64) % H, px.astype(np.int64) % W]
        p1 = g2[ny.astype(np.int64) % H, nx.astype(np.int64) % W]
        acc = np.where(p1 >= p0, 1.0, (p1 / np.maximum(p0, 1e-9)) ** 2)
        ok = rng.random(len(py)) < acc
        py, px = np.where(ok, ny, py) % H, np.where(ok, nx, px) % W
    else:
        py, px = ny % H, nx % W
    if len(py) > P["Nmax"]:
        sel = rng.choice(len(py), int(P["Nmax"]), replace=False)
        py, px, yy, zz, uid = py[sel], px[sel], yy[sel], zz[sel], uid[sel]
    s["py"], s["px"], s["y"], s["z"], s["uid"] = py, px, yy, zz, uid
    s["kind"] = np.zeros(len(py), np.int8)
    s["K"] = density(s, H, W)
    s["phi"] = gfun(s["u"])  # body indicator for the shared genealogy tool (phi > 1/2: micelle core)
    s["t"] += 1
    return s


def fields(s):
    return np.stack([s["u"] - P["u_bg"], s["K"], s["S"]]).astype(np.float32)


def particles(s):
    return np.stack([s["px"], s["py"], s["y"]], 1)


def stats(s):
    return {"N": int(len(s["py"])), "mean_u": round(float(s["u"].mean()), 4), "S": round(float(s["S"].mean()), 3),
            "ybar": round(float(s["y"].mean()), 3) if len(s["y"]) else None}


def damage(s, mask):
    H, W = mask.shape
    hit = mask[s["py"].astype(np.int64) % H, s["px"].astype(np.int64) % W]
    for k in ("py", "px", "y", "z", "uid", "kind"):
        s[k] = s[k][~hit]
    s["u"][mask] = P["u_bg"] + 0.1
    s["K"] = density(s, H, W)
    return s
