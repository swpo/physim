"""Amari neural field with spike-frequency adaptation (c20; new class neural-field).

u: activity (membrane potential), a: slow adaptation current. 2D periodic, nonlocal coupling by FFT.
    du/dt = -u + (w * f(u)) - g a + h
    da/dt = eps (u - a)
    f(u) = 1 / (1 + exp(-beta (u - theta)))       (sigmoid firing rate)
    w(r) = A [exp(-b r) (b sin(r/l) + cos(r/l))]   (Laing-Troy oscillatory kernel, length l)
After Laing & Troy (2003) and Owen, Laing & Coombes (2007): with g = 0 such kernels hold stationary
bumps; adaptation (g > 0) destabilizes them into travelling, breathing or splitting bumps.
Initial condition: u = u0 + noise over the whole domain, a = 0. WORLD_P (JSON) overrides P.
"""
import json, os
import numpy as np

META = {"name": "neural-field", "family": "neural-field", "parent": None,
        "mutation": "new class: Amari neural field with an oscillatory Laing-Troy kernel and linear adaptation",
        "size": (128, 128), "steps_per_frame": 30, "dt": 0.1,
        "channels": ["activity u", "adaptation a", "firing f(u)"], "matter": [2],
        "threshold": 0.5, "smooth": 0.5, "periodic": True}
P = dict(L=64.0, A=1.0, b=0.3, l=1.0, kern="dog", we=3.0, wi=3.0, se=1.0, si=3.0, beta=20.0, theta=0.5, g=2.5, eps=0.03, h=0.0, u0=0.0, noise=0.5, dt=0.1, corr=1.0)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    dx = P["L"] / W
    y = (np.arange(H) - H // 2) * dx; x = (np.arange(W) - W // 2) * dx
    r = np.hypot(*np.meshgrid(y, x, indexing="ij")) / P["l"]
    if P["kern"] == "dog":  # normalized difference of Gaussians: local excitation, lateral inhibition
        rr = r * P["l"]
        w = P["we"] * np.exp(-rr ** 2 / P["se"] ** 2) / (np.pi * P["se"] ** 2) - P["wi"] * np.exp(-rr ** 2 / P["si"] ** 2) / (np.pi * P["si"] ** 2)
    else:
        w = P["A"] * np.exp(-P["b"] * r) * (P["b"] * np.sin(r) + np.cos(r))
    Wh = np.fft.rfft2(np.fft.ifftshift(w)) * dx * dx
    z = rng.standard_normal((H, W))
    if P["corr"] > 0:  # noise correlated over corr length units, so it is not grid-scale
        ky = 2 * np.pi * np.fft.fftfreq(H, d=dx)[:, None]; kx = 2 * np.pi * np.fft.rfftfreq(W, d=dx)[None, :]
        z = np.fft.irfft2(np.fft.rfft2(z) * np.exp(-0.5 * (kx ** 2 + ky ** 2) * P["corr"] ** 2), (H, W)); z /= z.std()
    return {"u": P["u0"] + P["noise"] * z, "a": np.zeros((H, W)), "Wh": Wh}


def f(u):
    return 1.0 / (1.0 + np.exp(-P["beta"] * (u - P["theta"])))


def step(s):
    dt, u, a = P["dt"], s["u"], s["a"]
    fu = f(u)
    conv = np.fft.irfft2(np.fft.rfft2(fu) * s["Wh"], u.shape)
    s["u"] = u + dt * (-u + conv - P["g"] * a + P["h"])
    s["a"] = a + dt * P["eps"] * (u - a)
    return s


def fields(s):
    return np.stack([s["u"], s["a"], f(s["u"])]).astype(np.float32)


def stats(s):
    fu = f(s["u"])
    return {"active_frac": round(float((fu > 0.5).mean()), 4), "umax": round(float(s["u"].max()), 3)}
