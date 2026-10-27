"""Cubic-quintic complex Ginzburg-Landau pulses living on a consumed, regrowing gain medium (c43).

Extends c03's cgle-solitons (20261025T0841-c03-cgle-solitons), whose pulses never split or moved: the fixed linear
gain delta is replaced by a local gain field g that the light |A|^2 depletes and that regrows (a class-B laser medium).

A (complex): A_t = (g - l) A + (beta + i D/2) lap A + (eps + i)|A|^2 A + (mu + i nu)|A|^4 A
g (real):    g_t = Dg lap g + gam (g0 - g) - sig g |A|^2

g - l < 0 everywhere at g = g0 < l keeps the dark state linearly stable; a pulse burns a gain hole under itself.
Linear part of A and of g exact in Fourier (integrating factor), the rest Heun. Initial condition: smoothed complex noise
over the whole domain, g = g0. Rendered channels: |A|, Re A, g.
"""
import json, os
import numpy as np
from scipy import ndimage

META = {
    "name": "cgle-gain",
    "family": "cgle",
    "parent": "collective/contrib/20261025T0841-c03-cgle-solitons",
    "mutation": "the CGLE linear gain becomes a local gain medium g, depleted by |A|^2 and regrowing toward g0",
    "size": (96, 96),
    "steps_per_frame": 500,
    "dt": 0.01,
    "channels": ["|A|", "Re A", "g"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(L=40.0, l=1.0, g0=0.9, beta=0.125, D=1.0, eps=1.45, mu=-0.3, nu=-0.1, Dg=0.5, gam=0.02, sig=0.05,
         amp=0.6, smooth=2.0, dt=0.01)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    z = rng.standard_normal((H, W)) + 1j * rng.standard_normal((H, W))
    z = ndimage.gaussian_filter(z.real, P["smooth"], mode="wrap") + 1j * ndimage.gaussian_filter(z.imag, P["smooth"], mode="wrap")
    A = P["amp"] * z / np.abs(z).std()
    ky = 2 * np.pi * np.fft.fftfreq(H, d=P["L"] / H)
    kx = 2 * np.pi * np.fft.fftfreq(W, d=P["L"] / W)
    kk = ky[:, None] ** 2 + kx[None, :] ** 2
    E = np.exp((-P["l"] - (P["beta"] + 0.5j * P["D"]) * kk) * P["dt"])
    Eg = np.exp((-P["gam"] - P["Dg"] * kk) * P["dt"])
    return {"A": A, "g": np.full((H, W), P["g0"]), "E": E, "Eg": Eg}


def NL(a, g):
    p = np.abs(a) ** 2
    return g * a + (P["eps"] + 1j) * p * a + (P["mu"] + 1j * P["nu"]) * p * p * a, P["gam"] * P["g0"] - P["sig"] * g * p


def step(s):
    A, g, E, Eg, dt = s["A"], s["g"], s["E"], s["Eg"], P["dt"]
    Ah, gh = np.fft.fft2(A), np.fft.fft2(g)
    na, ng = NL(A, g)
    ka, kg = np.fft.fft2(na), np.fft.fft2(ng)
    A1 = np.fft.ifft2(E * (Ah + dt * ka)); g1 = np.fft.ifft2(Eg * (gh + dt * kg)).real
    na2, ng2 = NL(A1, g1)
    s["A"] = np.fft.ifft2(E * (Ah + 0.5 * dt * ka) + 0.5 * dt * np.fft.fft2(na2))
    s["g"] = np.fft.ifft2(Eg * (gh + 0.5 * dt * kg) + 0.5 * dt * np.fft.fft2(ng2)).real
    return s


def fields(s):
    return np.stack([np.abs(s["A"]), s["A"].real, s["g"]]).astype(np.float32)


def damage(s, mask):
    s["A"][mask] = 0
    return s
