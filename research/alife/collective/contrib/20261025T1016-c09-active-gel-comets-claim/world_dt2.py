"""Active-gel mechanochemistry (after Bois-Juelicher-Grill 2011 and Kumar et al. 2014), 2D periodic.

A thin compressible active gel with friction gamma and viscosity eta. Its flow v obeys
    gamma v - eta lap v = grad sigma,   sigma = zeta * a/(1 + a) / (1 + rho b)
a: stress generator (myosin-like), b: a regulator that weakens the stress (rho > 0).
Both are carried by the gel flow (conservative advection, the non-diffusive operator),
diffuse, and turn over toward 1:
    da/dt = -div(a v) + Da lap a + ka (1 - a)
    db/dt = -badv div(b v) + Db lap b + kb (T - b),   T = 1, or T = a when bsrc = 1
With badv = 0 and bsrc = 1, b is a non-advected trail that the generator lays down.
met = 1: a is not held at a0 by turnover but made autocatalytically from a substrate s that diffuses
and regrows, and decays:  da/dt = -div(a v) + Da lap a + kc s a - ka a,
                         ds/dt = Ds lap s + ks (1 - s) - kc s a.
t_starve >= 0: a fork; at that time s is set to 0 everywhere and stops regrowing (ks = 0).
zeta = 0 is the Laplacian-only twin (no flow: a, b, s only react and diffuse).
Advection and flow derivatives are 2/3-dealiased. P['scale'] refines the grid at fixed size L.
Contractile flow runs up the stress gradient and concentrates a into peaks; b is swept in too
and weakens them, so a peak whose b lags can be pushed off its own regulator and travel.
WORLD_P (JSON) overrides P.
"""
import numpy as np, json, os

META = {"name": "active-gel-fed-comets", "family": "active-gel", "parent": "none (new class)",
        "mutation": "new class: advection of stress generator and regulator by a contractile active-gel flow",
        "size": (128, 128), "steps_per_frame": 100, "dt": 0.01,
        "channels": ["generator a", "regulator b", "substrate s"], "matter": [0], "threshold": 1.0, "smooth": 1.0, "periodic": True}
P = dict(L=64.0, gamma=1.0, eta=1.0, zeta=60.0, rho=0.5, Da=4.0, Db=0.1, ka=0.1, kb=0.01, amp=0.05, dt=0.005, badv=0.0, bsrc=1.0, scale=1.0, a0=0.5, met=1.0, kc=0.2, ks=0.02, Ds=1.0, t_starve=-1.0)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    H, W = int(round(H * P["scale"])), int(round(W * P["scale"]))
    dx = P["L"] / W
    ky = 2 * np.pi * np.fft.fftfreq(H, d=dx)[:, None]
    kx = 2 * np.pi * np.fft.rfftfreq(W, d=dx)[None, :]
    a = P["a0"] * np.maximum(1 + P["amp"] * rng.standard_normal((H, W)), 0)  # noise over the whole domain
    b = a.copy()
    if P["met"]:
        a = np.maximum(P["a0"] * (1 + P["amp"] * rng.standard_normal((H, W))), 0)
        b = a.copy()
    kk = kx ** 2 + ky ** 2
    kmax = np.pi / dx
    D = ((np.abs(ky) < 2 / 3 * kmax) & (np.abs(kx) < 2 / 3 * kmax)).astype(float)  # 2/3 dealiasing
    return {"s": np.ones((H, W)), "a": a, "b": b, "ikx": 1j * kx * D, "iky": 1j * ky * D, "kk": kk, "G": 1 / (P["gamma"] + P["eta"] * kk), "dx": dx, "vmax": 0.0}


def step(s):
    dt, a, b = P["dt"], s["a"], s["b"]
    f2, i2 = np.fft.rfft2, np.fft.irfft2
    sig = P["zeta"] * a / (1 + a) / (1 + P["rho"] * b)
    S = f2(sig) * s["G"]
    sh = a.shape
    vx, vy = i2(s["ikx"] * S, sh), i2(s["iky"] * S, sh)
    s["vmax"] = float(np.sqrt(vx ** 2 + vy ** 2).max())
    s["t"] = s.get("t", 0.0) + dt
    if P["t_starve"] >= 0 and s["t"] >= P["t_starve"] and not s.get("starved"):
        s["s"][:] = 0.0  # fork: the substrate is removed everywhere and stops regrowing
        s["starved"] = True
    ks = 0.0 if s.get("starved") else P["ks"]
    if P["met"]:  # a is made autocatalytically from a consumed, regrowing substrate and decays
        sub = s["s"]; up = P["kc"] * sub * a
        da = -i2(s["ikx"] * f2(a * vx) + s["iky"] * f2(a * vy), sh) + up - P["ka"] * a
        s["s"] = i2(f2(sub + dt * (ks * (1 - sub) - up)) / (1 + dt * P["Ds"] * s["kk"]), sh)
    else:
        da = -i2(s["ikx"] * f2(a * vx) + s["iky"] * f2(a * vy), sh) + P["ka"] * (P["a0"] - a)
    btarget = a if P["bsrc"] else 1.0
    db = -P["badv"] * i2(s["ikx"] * f2(b * vx) + s["iky"] * f2(b * vy), sh) + P["kb"] * (btarget - b)
    s["a"] = np.maximum(i2(f2(a + dt * da) / (1 + dt * P["Da"] * s["kk"]), sh), 0)
    s["b"] = np.maximum(i2(f2(b + dt * db) / (1 + dt * P["Db"] * s["kk"]), sh), 0)
    return s


def fields(s):
    return np.stack([s["a"], s["b"], s["s"]]).astype(np.float32)


def stats(s):
    return {"a_max": round(float(s["a"].max()), 3), "vmax": round(s["vmax"], 3)}


def damage(s, mask):
    s["a"][mask] = 0
    s["b"][mask] = 0
    return s
