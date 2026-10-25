"""Active-gel mechanochemistry (after Bois-Juelicher-Grill 2011 and Kumar et al. 2014), 2D periodic.

A thin compressible active gel with friction gamma and viscosity eta. Its flow v obeys
    gamma v - eta lap v = grad sigma,   sigma = zeta * a/(1 + a) / (1 + rho b)
a: stress generator (myosin-like), b: a regulator that weakens the stress (rho > 0).
Both are carried by the gel flow (conservative advection, the non-diffusive operator),
diffuse, and turn over toward 1:
    da/dt = -div(a v) + Da lap a + ka (1 - a)
    db/dt = -badv div(b v) + Db lap b + kb (T - b),   T = 1, or T = a when bsrc = 1
With badv = 0 and bsrc = 1, b is a non-advected trail that the generator lays down.
Advection and flow derivatives are 2/3-dealiased. P['scale'] refines the grid at fixed size L.
Contractile flow runs up the stress gradient and concentrates a into peaks; b is swept in too
and weakens them, so a peak whose b lags can be pushed off its own regulator and travel.
WORLD_P (JSON) overrides P.
"""
import numpy as np, json, os

META = {"name": "active-gel", "family": "active-gel", "parent": "none (new class; after Bois-Juelicher-Grill 2011, Kumar et al. 2014)",
        "mutation": "new class: advection of stress generator and regulator by a contractile active-gel flow",
        "size": (128, 128), "steps_per_frame": 100, "dt": 0.01,
        "channels": ["generator a", "regulator b"], "matter": [0], "threshold": 3.0, "smooth": 1.0, "periodic": True}
P = dict(L=64.0, gamma=1.0, eta=1.0, zeta=20.0, rho=0.5, Da=1.0, Db=0.1, ka=0.1, kb=0.01, amp=0.05, dt=0.01, badv=0.0, bsrc=1.0, scale=1.0)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    H, W = int(round(H * P["scale"])), int(round(W * P["scale"]))
    dx = P["L"] / W
    ky = 2 * np.pi * np.fft.fftfreq(H, d=dx)[:, None]
    kx = 2 * np.pi * np.fft.rfftfreq(W, d=dx)[None, :]
    a = 1 + P["amp"] * rng.standard_normal((H, W))  # noise over the whole domain
    b = 1 + P["amp"] * rng.standard_normal((H, W))
    kk = kx ** 2 + ky ** 2
    kmax = np.pi / dx
    D = ((np.abs(ky) < 2 / 3 * kmax) & (np.abs(kx) < 2 / 3 * kmax)).astype(float)  # 2/3 dealiasing
    return {"a": a, "b": b, "ikx": 1j * kx * D, "iky": 1j * ky * D, "kk": kk, "G": 1 / (P["gamma"] + P["eta"] * kk), "dx": dx, "vmax": 0.0}


def step(s):
    dt, a, b = P["dt"], s["a"], s["b"]
    f2, i2 = np.fft.rfft2, np.fft.irfft2
    sig = P["zeta"] * a / (1 + a) / (1 + P["rho"] * b)
    S = f2(sig) * s["G"]
    sh = a.shape
    vx, vy = i2(s["ikx"] * S, sh), i2(s["iky"] * S, sh)
    s["vmax"] = float(np.sqrt(vx ** 2 + vy ** 2).max())
    da = -i2(s["ikx"] * f2(a * vx) + s["iky"] * f2(a * vy), sh) + P["ka"] * (1 - a)
    btarget = a if P["bsrc"] else 1.0
    db = -P["badv"] * i2(s["ikx"] * f2(b * vx) + s["iky"] * f2(b * vy), sh) + P["kb"] * (btarget - b)
    s["a"] = np.maximum(i2(f2(a + dt * da) / (1 + dt * P["Da"] * s["kk"]), sh), 0)
    s["b"] = np.maximum(i2(f2(b + dt * db) / (1 + dt * P["Db"] * s["kk"]), sh), 0)
    return s


def fields(s):
    return np.stack([s["a"], s["b"]]).astype(np.float32)


def stats(s):
    return {"a_max": round(float(s["a"].max()), 3), "vmax": round(s["vmax"], 3)}


def damage(s, mask):
    s["a"][mask] = 0
    s["b"][mask] = 0
    return s
